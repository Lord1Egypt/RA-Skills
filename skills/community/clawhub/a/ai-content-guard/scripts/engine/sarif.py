"""SARIF 2.1.0 输出 — 扩展 PITAX 元数据（融合方案 §4.4）。

传统 SAST findings（无 pitax 键）照常输出；PITAX findings 额外生成
tool.driver.rules[]（规则元数据：编号/名称/ATLAS/CVE/参考链接）和
results[].properties.pitax（证据/解码载荷），可被 GitHub Code Scanning、
IDE SARIF 查看器直接消费。
"""
from __future__ import annotations

SARIF_SCHEMA = (
    "https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/schemas/sarif-schema-2.1.0.json"
)
_SEV_LEVEL = {
    "critical": "error", "high": "error", "medium": "warning",
    "low": "note", "info": "none",
}
_PITAX_RULE_FIELDS = (
    "code", "name", "pillar", "aliases", "cwe", "mitre_atlas", "cve", "references",
)


def build_sarif(
    findings: list[dict],
    tool_name: str = "ai-content-guard",
    tool_version: str = "2.0.0",
) -> dict:
    rules: list[dict] = []
    seen_rules: set[str] = set()
    results: list[dict] = []

    for f in findings:
        rid = f.get("type") or f.get("ruleId") or "unknown"
        pitax = f.get("pitax") or {}

        if pitax and rid not in seen_rules:
            props = {k: pitax[k] for k in _PITAX_RULE_FIELDS if pitax.get(k) not in (None, [])}
            rule: dict = {
                "id": rid,
                "name": pitax.get("name", rid),
                "shortDescription": {"text": f"[{rid}] {pitax.get('name', rid)}"},
            }
            if f.get("description"):
                rule["fullDescription"] = {"text": f["description"]}
            if pitax.get("references"):
                rule["help"] = {
                    "text": "References: " + ", ".join(pitax["references"]),
                    "markdown": "\n".join(f"- {r}" for r in pitax["references"]),
                }
            if props:
                rule["properties"] = {"pitax": props}
            rules.append(rule)
            seen_rules.add(rid)

        region = {"startLine": int(f.get("line") or 0)}
        location = {"physicalLocation": {
            "artifactLocation": {"uri": f.get("file", "")},
            "region": region,
        }}
        message = f.get("description", "")
        if pitax.get("decoded_payload"):
            message += f" | decoded payload: {pitax['decoded_payload'][:120]}"
        result: dict = {
            "ruleId": rid,
            "level": _SEV_LEVEL.get(str(f.get("severity", "info")).lower(), "none"),
            "message": {"text": message},
            "locations": [location],
        }
        if pitax:
            rprops = {
                "confidence": str(f.get("confidence", "high")),
                "evidence": pitax.get("evidence", ""),
            }
            if pitax.get("decoded_payload"):
                rprops["decoded_payload"] = pitax["decoded_payload"]
            result["properties"] = {"pitax": rprops}
        results.append(result)

    driver: dict = {
        "name": tool_name,
        "version": tool_version,
        "informationUri": "https://github.com/a9320/tianxi-ai-content-guard",
    }
    if rules:
        driver["rules"] = rules

    return {
        "$schema": SARIF_SCHEMA,
        "version": "2.1.0",
        "runs": [{"tool": {"driver": driver}, "results": results}],
    }
