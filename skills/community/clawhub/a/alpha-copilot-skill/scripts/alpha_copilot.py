#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from billing import BillingError, build_billing_client  # noqa: E402
from web3_client import BinanceWeb3Client, BinanceWeb3Error, CHAIN_ALIASES, RANK_TYPE_ALIASES  # noqa: E402


TEXT = {
    "zh": {
        "report_title": "研究员 Alpha Copilot",
        "leaderboard_title": "今日优先级榜单",
        "top_tokens_title": "值得看的 5 个币",
        "tier_s": "S级",
        "tier_a": "A级",
        "tier_b": "B级",
        "unavailable": "暂不可用",
        "disclaimer": "仅供研究与内容参考，不构成投资建议。",
        "tweet_prefix": "今日观察",
        "group_prefix": "群内速递",
        "brief_prefix": "快报",
        "fundamentals_label": "基本面",
        "liquidity_label": "流动性",
        "risk_label": "风险",
    },
    "en": {
        "report_title": "Researcher Alpha Copilot",
        "leaderboard_title": "Today's Priority Leaderboard",
        "top_tokens_title": "Top 5 Tokens To Watch",
        "tier_s": "Tier S",
        "tier_a": "Tier A",
        "tier_b": "Tier B",
        "unavailable": "unavailable",
        "disclaimer": "For research only. Not investment advice.",
        "tweet_prefix": "Watchlist",
        "group_prefix": "Desk note",
        "brief_prefix": "Brief",
        "fundamentals_label": "Fundamentals",
        "liquidity_label": "Liquidity",
        "risk_label": "Risk",
    },
}


class AppError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json_print(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def dual_text(zh: str, en: str, sep: str = " / ") -> str:
    return f"{zh}{sep}{en}"


def dual_block(zh: str, en: str) -> str:
    return f"{zh}\n{en}"


def symbol_with_contract(symbol: str, contract_address: str) -> str:
    return f"{symbol} | {contract_address}"


def build_proxy_config(args: argparse.Namespace) -> tuple[str, Dict[str, str] | None]:
    proxy_mode = (args.proxy_mode or os.getenv("ALPHA_COPILOT_PROXY_MODE") or "auto").strip().lower()
    custom_http = args.http_proxy or os.getenv("HTTP_PROXY") or os.getenv("http_proxy") or ""
    custom_https = args.https_proxy or os.getenv("HTTPS_PROXY") or os.getenv("https_proxy") or ""
    custom_all = args.all_proxy or os.getenv("ALL_PROXY") or os.getenv("all_proxy") or ""

    if proxy_mode != "custom":
        return proxy_mode, None

    proxies: Dict[str, str] = {}
    if custom_http:
        proxies["http"] = custom_http
    if custom_https:
        proxies["https"] = custom_https
    elif custom_http:
        proxies["https"] = custom_http
    if custom_all:
        proxies["all"] = custom_all
    if not proxies:
        raise AppError("custom_proxy_mode_requires_proxy_url")
    return proxy_mode, proxies


def collect_proxy_inputs(args: argparse.Namespace) -> Dict[str, str]:
    return {
        "http_proxy": args.http_proxy or os.getenv("HTTP_PROXY") or os.getenv("http_proxy") or "",
        "https_proxy": args.https_proxy or os.getenv("HTTPS_PROXY") or os.getenv("https_proxy") or "",
        "all_proxy": args.all_proxy or os.getenv("ALL_PROXY") or os.getenv("all_proxy") or "",
    }


def summarize_proxy_diagnostics(
    diagnostics: List[Dict[str, Any]],
    proxy_mode: str,
    proxy_inputs: Dict[str, str],
) -> Dict[str, Any]:
    failed = [item for item in diagnostics if not item.get("ok")]
    has_proxy = any(proxy_inputs.values())
    check_map = {item["check"]: item for item in diagnostics}

    if not failed:
        if proxy_mode == "direct":
            headline = "direct_connection_ok"
            message_en = "Direct connection succeeded. This environment does not require a proxy."
            message_zh = "直连成功。当前环境不需要代理。"
        elif has_proxy:
            headline = "proxy_connection_ok"
            message_en = "Proxy connection succeeded. Current proxy settings can be used for production runs."
            message_zh = "代理连接成功。当前代理配置可用于正式运行。"
        else:
            headline = "auto_connection_ok"
            message_en = "Auto mode succeeded without proxy env vars. Direct access is working."
            message_zh = "自动模式在无代理环境变量时也成功。当前直连可用。"
        return {
            "headline": headline,
            "message": message_en,
            "message_zh": message_zh,
            "message_en": message_en,
            "suggestions": [],
            "suggestions_zh": [],
            "suggestions_en": [],
        }

    root_failed = not check_map.get("root", {}).get("ok", False)
    rank_failed = not check_map.get("unified_rank", {}).get("ok", False)
    meta_failed = "token_meta" in check_map and not check_map["token_meta"].get("ok", False)
    audit_failed = "token_audit" in check_map and not check_map["token_audit"].get("ok", False)

    suggestions_en: List[str] = []
    suggestions_zh: List[str] = []
    if root_failed:
        suggestions_en.append("Check whether the current network can reach https://web3.binance.com at all.")
        suggestions_zh.append("先检查当前网络是否能访问 https://web3.binance.com 。")
    if proxy_mode in {"auto", "env"} and not has_proxy:
        suggestions_en.append("If the user is in mainland China, set HTTP_PROXY/HTTPS_PROXY/ALL_PROXY first, or rerun with --proxy-mode custom.")
        suggestions_zh.append("如果用户在中国大陆，先设置 HTTP_PROXY/HTTPS_PROXY/ALL_PROXY，或改用 --proxy-mode custom 重新执行。")
    if proxy_mode == "direct":
        suggestions_en.append("If the user is in mainland China, retry with proxy env vars or --proxy-mode custom.")
        suggestions_zh.append("如果用户在中国大陆，请改用代理环境变量或 --proxy-mode custom 重试。")
    if proxy_mode == "custom" and not has_proxy:
        suggestions_en.append("Custom mode requires explicit --http-proxy / --https-proxy values.")
        suggestions_zh.append("custom 模式要求显式传入 --http-proxy / --https-proxy。")
    if rank_failed and not root_failed:
        suggestions_en.append("Root access works but rank API failed. Retry once, then switch between direct and proxy modes to compare.")
        suggestions_zh.append("首页访问正常但榜单接口失败。先重试一次，再切换 direct 和代理模式做对比。")
    if meta_failed or audit_failed:
        suggestions_en.append("Core rank API works but enrichment failed. The user can still run with --skip-audit to reduce upstream dependency.")
        suggestions_zh.append("核心榜单接口可用，但补充信息接口失败。可以先用 --skip-audit 降低对上游接口的依赖。")

    return {
        "headline": "connectivity_issue_detected",
        "message": "One or more upstream checks failed. Use the suggestions below to choose direct or proxy mode.",
        "message_zh": "一项或多项上游连通性检查失败。请根据下面建议选择直连或代理模式。",
        "message_en": "One or more upstream checks failed. Use the suggestions below to choose direct or proxy mode.",
        "suggestions": suggestions_zh or suggestions_en,
        "suggestions_zh": suggestions_zh,
        "suggestions_en": suggestions_en,
    }


def to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def format_money(value: Any) -> str:
    amount = to_float(value)
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    if amount >= 1_000:
        return f"${amount / 1_000:.2f}K"
    if amount > 0:
        return f"${amount:.2f}"
    return "n/a"


def safe_links(meta: Dict[str, Any]) -> List[Dict[str, str]]:
    links = meta.get("links", []) or []
    if not isinstance(links, list):
        return []
    cleaned = []
    for item in links:
        if not isinstance(item, dict):
            continue
        link = item.get("link")
        if isinstance(link, str) and link:
            cleaned.append({"label": str(item.get("label") or "link"), "link": link})
    return cleaned


def flatten_audit_hits(audit: Dict[str, Any]) -> List[str]:
    hits: List[str] = []
    for item in audit.get("riskItems", []) or []:
        if not isinstance(item, dict):
            continue
        for detail in item.get("details", []) or []:
            if isinstance(detail, dict) and detail.get("isHit"):
                title = detail.get("title")
                if isinstance(title, str) and title:
                    hits.append(title)
    return hits


def merge_rankings(rankings: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}
    for rank_name, tokens in rankings.items():
        for index, token in enumerate(tokens, start=1):
            contract = str(token.get("contractAddress") or "").strip().lower()
            if not contract:
                continue
            item = merged.setdefault(
                contract,
                {
                    "contract_address": contract,
                    "symbol": token.get("symbol") or contract,
                    "name": token.get("name") or token.get("symbol") or contract,
                    "token": token,
                    "hits": [],
                    "score": 0.0,
                },
            )
            item["token"] = token
            item["hits"].append({"list": rank_name, "rank": index})
            item["score"] += max(0.0, 30.0 - index)
            if rank_name == "alpha":
                item["score"] += 12
            elif rank_name == "trending":
                item["score"] += 8
            elif rank_name == "top_search":
                item["score"] += 6

    rows = list(merged.values())
    rows.sort(key=lambda item: item["score"], reverse=True)
    return rows


def priority_tier(score: float, lang: str) -> str:
    if score >= 70:
        return dual_text(TEXT["zh"]["tier_s"], TEXT["en"]["tier_s"])
    if score >= 45:
        return dual_text(TEXT["zh"]["tier_a"], TEXT["en"]["tier_a"])
    return dual_text(TEXT["zh"]["tier_b"], TEXT["en"]["tier_b"])


def summarize_fundamentals(token: Dict[str, Any], meta: Dict[str, Any], lang: str) -> str:
    protocol = token.get("protocol") or meta.get("protocol") or dual_text(TEXT["zh"]["unavailable"], TEXT["en"]["unavailable"])
    market_cap = format_money(token.get("marketCap") or token.get("market_cap"))
    holders = int(to_float(token.get("holders")))
    zh = f"{TEXT['zh']['fundamentals_label']}：协议 {protocol}，市值 {market_cap}，持有人 {holders}"
    en = f"{TEXT['en']['fundamentals_label']}: protocol {protocol}, market cap {market_cap}, holders {holders}"
    return dual_block(zh, en)


def summarize_liquidity(token: Dict[str, Any], lang: str) -> str:
    liquidity = format_money(token.get("liquidity"))
    volume = format_money(token.get("volume"))
    price = token.get("price") or "n/a"
    zh = f"{TEXT['zh']['liquidity_label']}：价格 {price}，流动性 {liquidity}，24h成交额 {volume}"
    en = f"{TEXT['en']['liquidity_label']}: price {price}, liquidity {liquidity}, 24h volume {volume}"
    return dual_block(zh, en)


def summarize_risk(audit: Dict[str, Any], meta: Dict[str, Any], lang: str) -> str:
    hits = flatten_audit_hits(audit)
    buy_tax = to_float((audit.get("extraInfo") or {}).get("buyTax"))
    sell_tax = to_float((audit.get("extraInfo") or {}).get("sellTax"))
    verified = (audit.get("extraInfo") or {}).get("isVerified")
    links = safe_links(meta)

    zh_parts = []
    en_parts = []
    if verified is False:
        zh_parts.append("合约未验证")
        en_parts.append("contract unverified")
    if max(buy_tax, sell_tax) > 0:
        zh_parts.append(f"税率 {max(buy_tax, sell_tax):.1f}%")
        en_parts.append(f"tax {max(buy_tax, sell_tax):.1f}%")
    if hits:
        hit_text = "; ".join(hits[:2])
        zh_parts.append(hit_text)
        en_parts.append(hit_text)
    if not links:
        zh_parts.append("缺少公开链接")
        en_parts.append("missing public links")
    if not zh_parts:
        zh_parts.append("未见显著红旗")
        en_parts.append("no major red flags observed")
    zh = f"{TEXT['zh']['risk_label']}：{'；'.join(zh_parts)}"
    en = f"{TEXT['en']['risk_label']}: {'; '.join(en_parts)}"
    return dual_block(zh, en)


def compute_priority_score(candidate: Dict[str, Any], token: Dict[str, Any], audit: Dict[str, Any], meta: Dict[str, Any]) -> float:
    score = float(candidate["score"])
    liquidity = to_float(token.get("liquidity"))
    volume = to_float(token.get("volume"))
    market_cap = to_float(token.get("marketCap"))
    holders = to_float(token.get("holders"))

    if liquidity >= 1_000_000:
        score += 18
    elif liquidity >= 300_000:
        score += 10
    elif liquidity >= 100_000:
        score += 4

    if volume >= 1_000_000:
        score += 10
    elif volume >= 300_000:
        score += 5

    if market_cap >= 50_000_000:
        score += 8
    elif market_cap >= 10_000_000:
        score += 4

    if holders >= 10_000:
        score += 6
    elif holders >= 2_000:
        score += 3

    risk_penalty = 0.0
    if (audit.get("extraInfo") or {}).get("isVerified") is False:
        risk_penalty += 8
    if max(
        to_float((audit.get("extraInfo") or {}).get("buyTax")),
        to_float((audit.get("extraInfo") or {}).get("sellTax")),
    ) > 10:
        risk_penalty += 10
    elif max(
        to_float((audit.get("extraInfo") or {}).get("buyTax")),
        to_float((audit.get("extraInfo") or {}).get("sellTax")),
    ) > 5:
        risk_penalty += 5
    risk_penalty += min(len(flatten_audit_hits(audit)) * 3, 12)

    if not safe_links(meta):
        risk_penalty += 3

    return max(1.0, round(score - risk_penalty, 2))


def build_copy(display_symbol: str, fundamentals: str, liquidity: str, risk: str, lang: str) -> Dict[str, str]:
    tweet_zh = f"{TEXT['zh']['tweet_prefix']} {display_symbol}。\n{fundamentals}\n{liquidity}\n{risk}\n先看量能和承接，再决定是否继续跟踪。"
    tweet_en = f"{TEXT['en']['tweet_prefix']} {display_symbol}.\n{fundamentals}\n{liquidity}\n{risk}\nWatch follow-through before committing more attention."
    group_zh = f"{TEXT['zh']['group_prefix']}｜{display_symbol}\n- {fundamentals}\n- {liquidity}\n- {risk}\n结论：进入今日观察池，等待进一步催化验证。"
    group_en = f"{TEXT['en']['group_prefix']} | {display_symbol}\n- {fundamentals}\n- {liquidity}\n- {risk}\nConclusion: keep on today's watchlist pending catalyst confirmation."
    brief_zh = f"{TEXT['zh']['brief_prefix']}：{display_symbol} 进入今日优先观察名单。\n{fundamentals}\n{liquidity}\n{risk}"
    brief_en = f"{TEXT['en']['brief_prefix']}: {display_symbol} made today's priority watchlist.\n{fundamentals}\n{liquidity}\n{risk}"
    tweet = dual_block(tweet_zh, tweet_en)
    group = dual_block(group_zh, group_en)
    brief = dual_block(brief_zh, brief_en)
    return {"tweet": tweet, "group": group, "brief": brief}


def normalize_candidate(
    candidate: Dict[str, Any],
    token: Dict[str, Any],
    audit: Dict[str, Any],
    meta: Dict[str, Any],
    lang: str,
) -> Dict[str, Any]:
    score = compute_priority_score(candidate, token, audit, meta)
    raw_symbol = str(token.get("symbol") or candidate["symbol"])
    display_symbol = symbol_with_contract(raw_symbol, candidate["contract_address"])
    fundamentals = summarize_fundamentals(token, meta, lang)
    liquidity = summarize_liquidity(token, lang)
    risk = summarize_risk(audit, meta, lang)
    copy = build_copy(display_symbol, fundamentals, liquidity, risk, lang)
    return {
        "symbol": raw_symbol,
        "display_symbol": display_symbol,
        "name": token.get("name") or candidate["name"],
        "contract_address": candidate["contract_address"],
        "priority_score": score,
        "priority_tier": priority_tier(score, lang),
        "fundamentals_summary": fundamentals,
        "liquidity_summary": liquidity,
        "risk_summary": risk,
        "rank_hits": candidate["hits"],
        "links": safe_links(meta),
        "tweet_draft": copy["tweet"],
        "group_draft": copy["group"],
        "brief_draft": copy["brief"],
    }


def render_markdown(report: Dict[str, Any], lang: str) -> str:
    lines = [
        f"# {report['title']}",
        "",
        f"## {dual_text(TEXT['zh']['leaderboard_title'], TEXT['en']['leaderboard_title'])}",
    ]
    for row in report["leaderboard"]:
        lines.append(f"- {row['rank']}. {row['display_symbol']} | {row['priority_tier']} | score {row['priority_score']}")
    lines.extend(["", f"## {dual_text(TEXT['zh']['top_tokens_title'], TEXT['en']['top_tokens_title'])}"])
    for row in report["top_tokens"]:
        lines.append(f"### {row['display_symbol']} ({row['priority_tier']})")
        lines.append(f"- {row['fundamentals_summary']}")
        lines.append(f"- {row['liquidity_summary']}")
        lines.append(f"- {row['risk_summary']}")
        lines.append(f"- 推文草稿 / Tweet Draft: {row['tweet_draft']}")
        lines.append(f"- 群发草稿 / Group Draft: {row['group_draft']}")
        lines.append(f"- 快报草稿 / Brief Draft: {row['brief_draft']}")
        lines.append("")
    lines.append(report["summary"]["disclaimer"])
    return "\n".join(lines)


def maybe_bill(call_name: str, user_ref: str, skip_billing: bool) -> Dict[str, Any]:
    if skip_billing:
        return {
            "ok": True,
            "code": "skipped",
            "message": "Billing skipped",
            "message_zh": "已跳过计费",
            "message_en": "Billing skipped",
        }
    client = build_billing_client()
    amount = os.getenv("SKILLPAY_PRICE_USDT", "0.01").strip() or "0.01"
    result = client.charge(call_name, amount, user_ref, str(uuid4()))
    if not result.ok:
        raise BillingError(f"billing_failed:{result.code}:{result.message}")
    return result.to_dict()


def fetch_top_candidates(client: BinanceWeb3Client, chain_id: str, limit: int) -> List[Dict[str, Any]]:
    rankings = {
        rank_name: client.unified_rank(chain_id=chain_id, rank_type=rank_type, size=max(limit * 3, 10))
        for rank_name, rank_type in RANK_TYPE_ALIASES.items()
    }
    return merge_rankings(rankings)[: max(limit * 2, 10)]


def build_report(
    chain: str,
    lang: str,
    limit: int,
    skip_audit: bool = False,
    client: BinanceWeb3Client | None = None,
    proxy_mode: str = "auto",
    proxies: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    if chain not in CHAIN_ALIASES:
        raise AppError("unsupported_chain")
    if lang not in TEXT:
        raise AppError("unsupported_lang")

    active_client = client or BinanceWeb3Client(proxy_mode=proxy_mode, proxies=proxies)
    chain_id = CHAIN_ALIASES[chain]
    candidates = fetch_top_candidates(active_client, chain_id, limit)
    rows = []

    for candidate in candidates:
        token = candidate["token"]
        contract = candidate["contract_address"]
        try:
            meta = active_client.token_meta(chain_id, contract)
        except BinanceWeb3Error:
            meta = {}
        if skip_audit:
            audit = {}
        else:
            try:
                audit = active_client.token_audit(chain_id, contract)
            except BinanceWeb3Error:
                audit = {}
        rows.append(normalize_candidate(candidate, token, audit, meta, lang))

    rows.sort(key=lambda item: item["priority_score"], reverse=True)
    top_rows = rows[:limit]
    leaderboard = [
        {
            "rank": index,
            "symbol": row["symbol"],
            "display_symbol": row["display_symbol"],
            "priority_score": row["priority_score"],
            "priority_tier": row["priority_tier"],
        }
        for index, row in enumerate(top_rows, start=1)
    ]
    return {
        "title": dual_text(TEXT["zh"]["report_title"], TEXT["en"]["report_title"]),
        "generated_at_utc": utc_now(),
        "chain": chain,
        "leaderboard": leaderboard,
        "top_tokens": top_rows,
        "summary": {
            "candidate_count": len(rows),
            "selected_count": len(top_rows),
            "disclaimer": dual_text(TEXT["zh"]["disclaimer"], TEXT["en"]["disclaimer"]),
            "disclaimer_zh": TEXT["zh"]["disclaimer"],
            "disclaimer_en": TEXT["en"]["disclaimer"],
        },
    }


def run_proxy_check(args: argparse.Namespace) -> Dict[str, Any]:
    proxy_mode, proxies = build_proxy_config(args)
    proxy_inputs = collect_proxy_inputs(args)
    client = BinanceWeb3Client(proxy_mode=proxy_mode, proxies=proxies)
    chain_id = CHAIN_ALIASES[args.chain]
    diagnostics: List[Dict[str, Any]] = []

    def _record(name: str, fn: Any) -> None:
        try:
            result = fn()
            diagnostics.append({"check": name, "ok": True, "result": result})
        except Exception as exc:  # noqa: BLE001
            diagnostics.append({"check": name, "ok": False, "error": str(exc)})

    _record("root", client.ping_root)
    _record(
        "unified_rank",
        lambda: {
            "token_count": len(client.unified_rank(chain_id=chain_id, rank_type=RANK_TYPE_ALIASES["trending"], size=3))
        },
    )

    sample_contract = args.contract or ""
    if not sample_contract:
        try:
            sample_rows = client.unified_rank(chain_id=chain_id, rank_type=RANK_TYPE_ALIASES["trending"], size=1)
            if sample_rows:
                sample_contract = str(sample_rows[0].get("contractAddress") or "")
        except Exception:  # noqa: BLE001
            sample_contract = ""

    if sample_contract:
        _record("token_meta", lambda: {"keys": sorted(client.token_meta(chain_id, sample_contract).keys())[:8]})
        _record(
            "token_audit",
            lambda: {
                "keys": sorted(client.token_audit(chain_id, sample_contract).keys())[:8],
                "contract_address": sample_contract,
            },
        )

    summary = summarize_proxy_diagnostics(diagnostics, proxy_mode=proxy_mode, proxy_inputs=proxy_inputs)
    return {
        "status": "ok",
        "command": "proxy-check",
        "chain": args.chain,
        "proxy_mode": proxy_mode,
        "proxy_inputs": proxy_inputs,
        "custom_proxies_applied": proxies or {},
        "session_trust_env": client.session.trust_env,
        "summary": summary,
        "checks": diagnostics,
    }


def cmd_rank(args: argparse.Namespace) -> None:
    user_ref = args.user_id or os.getenv("SKILLPAY_USER_REF", "anonymous").strip() or "anonymous"
    proxy_mode, proxies = build_proxy_config(args)
    report = build_report(
        chain=args.chain,
        lang=args.lang,
        limit=args.limit,
        skip_audit=args.skip_audit,
        proxy_mode=proxy_mode,
        proxies=proxies,
    )
    billing = maybe_bill("rank", user_ref=user_ref, skip_billing=args.skip_billing)
    payload = {
        **report,
        "billing": billing,
    }
    if args.format == "markdown":
        print(render_markdown(payload, args.lang))
    else:
        _json_print(payload)


def cmd_health(_: argparse.Namespace) -> None:
    _json_print(
        {
            "status": "ok",
            "command": "health",
            "message": "Health check passed",
            "message_zh": "健康检查通过",
            "message_en": "Health check passed",
            "billing_mode": os.getenv("SKILLPAY_BILLING_MODE", "skillpay"),
            "default_price_usdt": os.getenv("SKILLPAY_PRICE_USDT", "0.01"),
            "proxy_mode_default": os.getenv("ALPHA_COPILOT_PROXY_MODE", "auto"),
        }
    )


def cmd_proxy_check(args: argparse.Namespace) -> None:
    _json_print(run_proxy_check(args))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="研究员 Alpha Copilot / Researcher Alpha Copilot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    rank_parser = subparsers.add_parser("rank", help="生成今日优先级报告 / Generate the daily priority report")
    rank_parser.add_argument("--chain", default="bsc", choices=sorted(CHAIN_ALIASES.keys()), help="链名称 / Chain name")
    rank_parser.add_argument("--lang", default="zh", choices=sorted(TEXT.keys()), help="主显示语言 / Primary display language")
    rank_parser.add_argument("--limit", type=int, default=5, help="输出币种数量 / Number of tokens to return")
    rank_parser.add_argument("--format", default="json", choices=("json", "markdown"), help="输出格式 / Output format")
    rank_parser.add_argument("--user-id", default="", help="计费用户标识 / Billing user identifier")
    rank_parser.add_argument("--skip-audit", action="store_true", help="跳过审计补充信息 / Skip audit enrichment")
    rank_parser.add_argument("--skip-billing", action="store_true", help="跳过计费 / Skip billing")
    rank_parser.add_argument(
        "--proxy-mode",
        default=os.getenv("ALPHA_COPILOT_PROXY_MODE", "auto"),
        choices=("auto", "env", "direct", "custom"),
        help="代理模式: 自动/环境变量/直连/自定义 / Proxy mode: auto/env/direct/custom",
    )
    rank_parser.add_argument("--http-proxy", default="", help="自定义 HTTP 代理 / Custom HTTP proxy")
    rank_parser.add_argument("--https-proxy", default="", help="自定义 HTTPS 代理 / Custom HTTPS proxy")
    rank_parser.add_argument("--all-proxy", default="", help="自定义 ALL_PROXY / Custom ALL_PROXY")
    rank_parser.set_defaults(func=cmd_rank)

    health_parser = subparsers.add_parser("health", help="检查运行状态 / Check runtime health")
    health_parser.set_defaults(func=cmd_health)

    proxy_parser = subparsers.add_parser("proxy-check", help="检查代理与上游连通性 / Diagnose proxy and upstream connectivity")
    proxy_parser.add_argument("--chain", default="bsc", choices=sorted(CHAIN_ALIASES.keys()), help="链名称 / Chain name")
    proxy_parser.add_argument(
        "--proxy-mode",
        default=os.getenv("ALPHA_COPILOT_PROXY_MODE", "auto"),
        choices=("auto", "env", "direct", "custom"),
        help="代理模式: 自动/环境变量/直连/自定义 / Proxy mode: auto/env/direct/custom",
    )
    proxy_parser.add_argument("--http-proxy", default="", help="自定义 HTTP 代理 / Custom HTTP proxy")
    proxy_parser.add_argument("--https-proxy", default="", help="自定义 HTTPS 代理 / Custom HTTPS proxy")
    proxy_parser.add_argument("--all-proxy", default="", help="自定义 ALL_PROXY / Custom ALL_PROXY")
    proxy_parser.add_argument("--contract", default="", help="指定测试合约地址 / Specific contract address for testing")
    proxy_parser.set_defaults(func=cmd_proxy_check)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        args.func(args)
        return 0
    except (AppError, BillingError, BinanceWeb3Error) as exc:
        _json_print(
            {
                "status": "error",
                "error": str(exc),
                "error_zh": f"执行失败：{exc}",
                "error_en": f"Execution failed: {exc}",
                "suggestion_zh": "可先运行 proxy-check 检查网络与代理配置。",
                "suggestion_en": "Run proxy-check first to verify network and proxy settings.",
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
