#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from market_data import fetch_index_snapshot, fetch_sector_movers, fetch_tencent_quotes
from industry_chain import load_json as load_chain_json, select_chain_themes
from market_sentiment import build_sentiment_snapshot
from mx_toolkit import load_presets
from news_iterator import FeedItem, build_event_watchlists_payload, classify_item
from opening_window_checklist import classify_state
from runtime_config import build_status, get_output_dir, read_env_file

ROOT = Path(__file__).resolve().parents[1]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalize_alert(alert: dict) -> dict:
    return {
        "category": alert["category"],
        "score": alert["score"],
        "watchlists": alert.get("impacted_watchlists", []),
        "watchlist_scores": alert.get("watchlist_scores", {}),
        "entities": alert.get("matched_entities", []),
        "keywords": alert.get("matched_keywords", []),
    }


def main() -> None:
    indices = fetch_index_snapshot()
    assert_true(len(indices) >= 3, "expected at least 3 indices")
    assert_true(any(item.get("name") == "上证指数" for item in indices), "missing 上证指数")

    leaders = fetch_sector_movers(limit=3, rising=True)
    laggards = fetch_sector_movers(limit=3, rising=False)
    assert_true(len(leaders) == 3, "expected 3 top sectors")
    assert_true(len(laggards) == 3, "expected 3 bottom sectors")

    quotes = fetch_tencent_quotes(["sz300502", "sh688981", "sh600938"])
    assert_true(len(quotes) == 3, "expected 3 quotes")
    assert_true(all(quote.get("price") is not None for quote in quotes), "quote price missing")

    watchlists = json.loads((ROOT / "assets" / "default_watchlists.json").read_text(encoding="utf-8"))
    iterator_config = json.loads((ROOT / "assets" / "news_iterator_config.json").read_text(encoding="utf-8"))
    chain_config = load_chain_json(str(ROOT / "assets" / "industry_chains.json"))
    mx_presets = load_presets(str(ROOT / "assets" / "mx_presets.json"))
    assert_true("cross_cycle_anchor12" in watchlists, "missing cross_cycle_anchor12")
    assert_true("cross_cycle_core" in watchlists, "missing cross_cycle_core")
    assert_true("war_shock_core12" in watchlists, "missing war_shock_core12")
    assert_true("war_benefit_oil_coal" in watchlists, "missing war_benefit_oil_coal")
    assert_true("war_headwind_compute_power" in watchlists, "missing war_headwind_compute_power")
    assert_true(len(watchlists["cross_cycle_anchor12"]) >= 10, "anchor watchlist too small")
    assert_true("feeds" in iterator_config and len(iterator_config["feeds"]) >= 5, "news iterator feeds missing")
    assert_true("conflict_entities" in iterator_config, "news iterator conflict entities missing")
    assert_true(len(chain_config.get("themes", [])) >= 5, "industry chain config missing themes")
    assert_true("preopen_policy" in mx_presets, "missing MX preset preopen_policy")
    assert_true("preopen_repair_chain" in mx_presets, "missing MX preset preopen_repair_chain")

    with tempfile.TemporaryDirectory() as temp_dir:
        env_path = Path(temp_dir) / "runtime.env"
        env_path.write_text("EM_API_KEY=test-key\n", encoding="utf-8")
        env_values = read_env_file(env_path)
        assert_true(env_values.get("EM_API_KEY") == "test-key", "runtime env parsing failed")
        status = build_status(str(env_path))
        assert_true(status["capabilities"]["em_required_mode"], "EM key should be mandatory")
        assert_true(status["capabilities"]["em_enhanced_mode"], "runtime capability detection failed")
        assert_true("EM_API_KEY" in status["configured_keys"], "runtime key status missing")
        assert_true(status["eastmoney_apply_url"].startswith("https://ai.eastmoney.com/"), "missing Eastmoney apply url")
        output_dir = get_output_dir("smoke-test-output")
        assert_true(output_dir.exists(), "runtime output dir missing")

    future_release_alerts = classify_item(
        FeedItem(
            item_key="future",
            feed_key="test",
            feed_label="Test",
            source="Test",
            title="OpenAI unveiled a new model for datacenter reasoning agents",
            link="https://example.com/future",
            summary="The launch centers on AI server demand and semiconductor inference.",
            published_at="2026-03-19T00:00:00+00:00",
        ),
        iterator_config,
    )
    categories = {alert["category"] for alert in future_release_alerts}
    assert_true("huge_future" in categories, "expected huge_future classification")
    assert_true("huge_name_release" in categories, "expected huge_name_release classification")

    conflict_alerts = classify_item(
        FeedItem(
            item_key="conflict",
            feed_key="test",
            feed_label="Test",
            source="Test",
            title="Iran attack raises oil shipping disruption risk in Hormuz",
            link="https://example.com/conflict",
            summary="Energy traders watch crude, refinery routes and power costs for data center operators.",
            published_at="2026-03-19T00:00:00+00:00",
        ),
        iterator_config,
    )
    conflict_categories = {alert["category"] for alert in conflict_alerts}
    assert_true("huge_conflict" in conflict_categories, "expected huge_conflict classification")
    assert_true(
        any("war_benefit_oil_coal" in alert["impacted_watchlists"] for alert in conflict_alerts),
        "expected war_benefit_oil_coal mapping",
    )

    payload = build_event_watchlists_payload(
        [normalize_alert(alert) for alert in future_release_alerts + conflict_alerts],
        watchlists,
        hours=12,
    )
    assert_true("event_focus_core" in payload["groups"], "missing event_focus_core")
    assert_true("event_focus_huge_conflict_benefit" in payload["groups"], "missing conflict benefit pool")
    assert_true(
        any(item["symbol"] == "sh600938" for item in payload["groups"]["event_focus_huge_conflict_benefit"]),
        "expected China Offshore Oil in conflict event pool",
    )
    chain_themes = select_chain_themes(payload, ["tech_repair", "defensive_gauge"], chain_config, max_themes=3)
    chain_ids = {item["id"] for item in chain_themes}
    assert_true("optical_module_chain" in chain_ids, "expected optical-module chain theme")
    assert_true("oil_gas_chain" in chain_ids or "coal_chain" in chain_ids, "expected energy chain theme")

    state = classify_state(
        [
            {"group": "tech_repair", "above_prev_close": 3},
            {"group": "policy_beta", "above_prev_close": 1},
            {"group": "defensive_gauge", "above_prev_close": 1},
        ]
    )
    assert_true("true repair" in state.lower(), "opening-window classifier mismatch")
    sentiment = build_sentiment_snapshot(
        group_flow_rows=[
            {"group": "tech_repair", "net_flow_yi": 6.5},
            {"group": "defensive_gauge", "net_flow_yi": -2.3},
        ]
    )
    assert_true(sentiment["label"] in {"科技修复", "修复扩散", "分化震荡", "抱团行情", "分化偏弱"}, "unexpected sentiment label")

    print("smoke test passed")
    print(f"indices: {len(indices)}")
    print(f"leaders: {len(leaders)}")
    print(f"laggards: {len(laggards)}")
    print(f"quotes: {len(quotes)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"smoke test failed: {exc}", file=sys.stderr)
        raise
