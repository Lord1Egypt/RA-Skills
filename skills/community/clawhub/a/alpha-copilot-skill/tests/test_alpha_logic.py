from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from alpha_copilot import (
    build_proxy_config,
    build_report,
    merge_rankings,
    normalize_candidate,
    run_proxy_check,
    summarize_proxy_diagnostics,
)


class _Client:
    def unified_rank(self, chain_id: str, rank_type: int, size: int = 20):  # noqa: ARG002
        if rank_type == 10:
            return [
                {"contractAddress": "0xaaa", "symbol": "AAA", "name": "Alpha", "liquidity": "1200000", "volume": "2200000", "marketCap": "90000000", "holders": "12000", "protocol": "BSC"},
                {"contractAddress": "0xbbb", "symbol": "BBB", "name": "Beta", "liquidity": "200000", "volume": "500000", "marketCap": "8000000", "holders": "1500", "protocol": "BSC"},
            ]
        if rank_type == 11:
            return [
                {"contractAddress": "0xaaa", "symbol": "AAA", "name": "Alpha", "liquidity": "1200000", "volume": "2200000", "marketCap": "90000000", "holders": "12000", "protocol": "BSC"},
            ]
        return [
            {"contractAddress": "0xaaa", "symbol": "AAA", "name": "Alpha", "liquidity": "1200000", "volume": "2200000", "marketCap": "90000000", "holders": "12000", "protocol": "BSC"},
            {"contractAddress": "0xccc", "symbol": "CCC", "name": "Gamma", "liquidity": "600000", "volume": "1000000", "marketCap": "20000000", "holders": "4000", "protocol": "BSC"},
        ]

    def token_meta(self, chain_id: str, contract_address: str):  # noqa: ARG002
        return {"links": [{"label": "x", "link": f"https://x.com/{contract_address[2:]}"}]}

    def token_audit(self, chain_id: str, contract_address: str):  # noqa: ARG002
        if contract_address == "0xbbb":
            return {"extraInfo": {"buyTax": "12", "sellTax": "12", "isVerified": False}, "riskItems": [{"details": [{"title": "High tax", "isHit": True}]}]}
        return {"extraInfo": {"buyTax": "0", "sellTax": "0", "isVerified": True}, "riskItems": []}


def test_merge_rankings_rewards_repeat_hits() -> None:
    merged = merge_rankings(
        {
            "trending": [{"contractAddress": "0xaaa", "symbol": "AAA"}],
            "top_search": [{"contractAddress": "0xaaa", "symbol": "AAA"}],
            "alpha": [{"contractAddress": "0xbbb", "symbol": "BBB"}],
        }
    )
    assert merged[0]["contract_address"] == "0xaaa"


def test_normalize_candidate_builds_copy_fields() -> None:
    candidate = {
        "contract_address": "0xaaa",
        "symbol": "AAA",
        "name": "Alpha",
        "hits": [{"list": "trending", "rank": 1}],
        "score": 55,
    }
    token = {"symbol": "AAA", "name": "Alpha", "liquidity": "1200000", "volume": "2200000", "marketCap": "90000000", "holders": "12000", "protocol": "BSC"}
    audit = {"extraInfo": {"buyTax": "0", "sellTax": "0", "isVerified": True}, "riskItems": []}
    meta = {"links": [{"label": "x", "link": "https://x.com/alpha"}]}
    row = normalize_candidate(candidate, token, audit, meta, "zh")
    assert row["priority_score"] > 55
    assert "今日观察" in row["tweet_draft"]
    assert "Watchlist" in row["tweet_draft"]
    assert "0xaaa" in row["display_symbol"]
    assert "0xaaa" in row["tweet_draft"]
    assert row["tweet_draft"]


def test_build_report_returns_top_rows() -> None:
    report = build_report(chain="bsc", lang="zh", limit=2, client=_Client())
    assert report["summary"]["selected_count"] == 2
    assert report["leaderboard"][0]["symbol"] == "AAA"
    assert "0xaaa" in report["leaderboard"][0]["display_symbol"]
    assert "研究员 Alpha Copilot" in report["title"]
    assert "Researcher Alpha Copilot" in report["title"]
    assert report["summary"]["disclaimer_zh"]
    assert report["summary"]["disclaimer_en"]


def test_build_proxy_config_custom() -> None:
    class _Args:
        proxy_mode = "custom"
        http_proxy = "http://127.0.0.1:1"
        https_proxy = ""
        all_proxy = ""

    mode, proxies = build_proxy_config(_Args())
    assert mode == "custom"
    assert proxies == {"http": "http://127.0.0.1:1", "https": "http://127.0.0.1:1"}


def test_run_proxy_check_collects_results() -> None:
    class _Args:
        chain = "bsc"
        proxy_mode = "direct"
        http_proxy = ""
        https_proxy = ""
        all_proxy = ""
        contract = "0xabc"

    from alpha_copilot import BinanceWeb3Client as _Unused  # noqa: F401

    class _DiagClient:
        session = type("Session", (), {"trust_env": False})()

        def ping_root(self):
            return {"status_code": 200, "ok": True, "final_url": "https://web3.binance.com"}

        def unified_rank(self, chain_id: str, rank_type: int, size: int = 20):  # noqa: ARG002
            return [{"contractAddress": "0xabc"}]

        def token_meta(self, chain_id: str, contract_address: str):  # noqa: ARG002
            return {"name": "A"}

        def token_audit(self, chain_id: str, contract_address: str):  # noqa: ARG002
            return {"riskLevel": 1}

    import alpha_copilot as mod

    original = mod.BinanceWeb3Client
    mod.BinanceWeb3Client = lambda proxy_mode, proxies: _DiagClient()
    try:
        result = run_proxy_check(_Args())
    finally:
        mod.BinanceWeb3Client = original

    assert result["command"] == "proxy-check"
    assert len(result["checks"]) == 4
    assert result["summary"]["headline"] == "direct_connection_ok"
    assert result["summary"]["message_zh"]
    assert result["summary"]["message_en"]


def test_summarize_proxy_diagnostics_for_failed_auto_without_proxy() -> None:
    summary = summarize_proxy_diagnostics(
        diagnostics=[
            {"check": "root", "ok": False, "error": "timeout"},
            {"check": "unified_rank", "ok": False, "error": "timeout"},
        ],
        proxy_mode="auto",
        proxy_inputs={"http_proxy": "", "https_proxy": "", "all_proxy": ""},
    )
    assert summary["headline"] == "connectivity_issue_detected"
    assert summary["suggestions"]
    assert summary["suggestions_zh"]
    assert summary["suggestions_en"]
