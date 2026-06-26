#!/usr/bin/env python3
"""Render a Markdown report from collected OpenClaw audit artefacts.

The renderer is intentionally tolerant:
- reads capture files produced by collect_openclaw_audit.sh
- extracts JSON from CLI captures when possible
- merges audit findings from regular + deep runs
- enriches findings with assets/openclaw_checkid_map.json
- fills in environment clues from targeted config-get captures

Usage:
  python3 "{baseDir}/scripts/render_report.py" --input ./openclaw-audit --output ./openclaw-security-report.md
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4, "unknown": 9}
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


@dataclass
class Capture:
    name: str
    path: Path
    raw: str
    body: str


def strip_cmd_banner(text: str) -> str:
    text = ANSI_RE.sub("", text)
    lines = text.splitlines()
    if lines and lines[0].startswith("$ "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def load_capture(path: Path) -> Optional[Capture]:
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8", errors="replace")
    return Capture(name=path.stem, path=path, raw=raw, body=strip_cmd_banner(raw))


def newest_audit_folder(root: Path) -> Path:
    if root.is_dir():
        kids = [p for p in root.iterdir() if p.is_dir() and p.name.startswith("openclaw-audit-")]
        if kids:
            return sorted(kids, key=lambda p: p.name)[-1]
    return root


def clean_scalar_text(text: str) -> str:
    lines: List[str] = []
    for line in text.splitlines():
        if line.startswith("[warn]") or line.startswith("[info]"):
            continue
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def load_json_text(txt: str) -> Any:
    body = clean_scalar_text(txt)
    candidate_starts = [i for ch in ("{", "[") for i in [body.find(ch)] if i != -1]
    for idx in sorted(candidate_starts):
        try:
            return json.loads(body[idx:])
        except Exception:
            continue
    return None


def load_json_capture(path: Path) -> Any:
    capture = load_capture(path)
    if capture is None:
        return None
    return load_json_text(capture.body)


def load_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def normalise_sev(raw: str) -> str:
    s = (raw or "").strip().lower()
    if not s:
        return "unknown"
    if "/" in s:
        parts = [p.strip() for p in s.split("/") if p.strip()]
        if "critical" in parts:
            return "critical"
        if "high" in parts:
            return "high"
        if "warn" in parts or "warning" in parts or "medium" in parts:
            return "medium"
        if "low" in parts:
            return "low"
        if "info" in parts:
            return "info"
        return parts[0] if parts else "unknown"
    if s in ("warn", "warning"):
        return "medium"
    if s == "crit":
        return "critical"
    return s if s in SEV_ORDER else s


def extract_findings(obj: Any) -> List[Dict[str, Any]]:
    if obj is None:
        return []
    if isinstance(obj, dict):
        for key in ("findings", "checks", "results", "issues"):
            value = obj.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        if obj and all(isinstance(v, dict) for v in obj.values()):
            out: List[Dict[str, Any]] = []
            for key, value in obj.items():
                item = dict(value)
                item.setdefault("checkId", key)
                out.append(item)
            return out
    if isinstance(obj, list):
        return [item for item in obj if isinstance(item, dict)]
    return []


def pick_text(finding: Dict[str, Any]) -> str:
    for key in ("title", "summary", "message", "description"):
        value = finding.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "(no summary provided)"


def dedupe_findings(findings: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen: set[Tuple[str, str, str]] = set()
    out: List[Dict[str, Any]] = []
    for finding in findings:
        check_id = str(finding.get("checkId") or finding.get("id") or "").strip()
        summary = pick_text(finding)
        sev = normalise_sev(str(finding.get("severity") or finding.get("level") or finding.get("risk") or ""))
        key = (check_id, summary, sev)
        if key in seen:
            continue
        seen.add(key)
        out.append(finding)
    return out


def sort_key(finding: Dict[str, Any]) -> Tuple[int, str, str]:
    sev = normalise_sev(str(finding.get("severity") or finding.get("level") or finding.get("risk") or "unknown"))
    order = SEV_ORDER.get(sev, 8)
    check_id = str(finding.get("checkId") or finding.get("id") or "")
    return (order, check_id, pick_text(finding))


def severity_counts(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for finding in findings:
        sev = normalise_sev(str(finding.get("severity") or finding.get("level") or finding.get("risk") or "unknown"))
        counts[sev] = counts.get(sev, 0) + 1
    return counts


def load_checkid_map(skill_root: Path) -> Dict[str, Any]:
    path = skill_root / "assets" / "openclaw_checkid_map.json"
    if path.exists():
        obj = load_json_file(path)
        if isinstance(obj, dict):
            return obj
    return {}


def read_capture_body(in_dir: Path, stem: str) -> str:
    capture = load_capture(in_dir / f"{stem}.txt")
    if capture is None:
        return ""
    return clean_scalar_text(capture.body)


def read_config_value(in_dir: Path, stem: str) -> Optional[Any]:
    body = read_capture_body(in_dir, stem)
    if not body:
        return None
    try:
        return json.loads(body)
    except Exception:
        lowered = body.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if lowered == "null":
            return None
        return body


def one_line(value: Any) -> str:
    if value is None:
        return "(unset)"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        value = value.strip()
        return value or "(empty)"
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def detect_os(in_dir: Path) -> str:
    sw_vers = read_capture_body(in_dir, "host_sw_vers")
    if sw_vers:
        product_name = ""
        product_version = ""
        for line in sw_vers.splitlines():
            if ":" not in line:
                continue
            key, value = [part.strip() for part in line.split(":", 1)]
            if key == "ProductName":
                product_name = value
            elif key == "ProductVersion":
                product_version = value
        if product_name or product_version:
            return " ".join(part for part in (product_name, product_version) if part).strip()

    os_release = read_capture_body(in_dir, "host_os_release")
    if os_release:
        for line in os_release.splitlines():
            if line.startswith("PRETTY_NAME="):
                return line.split("=", 1)[1].strip().strip('"')
        for line in os_release.splitlines():
            if line.startswith("NAME="):
                return line.split("=", 1)[1].strip().strip('"')

    uname = read_capture_body(in_dir, "host_uname")
    return uname or "(unknown)"


def parse_version(in_dir: Path) -> str:
    body = read_capture_body(in_dir, "openclaw_version")
    if not body:
        return "(unknown)"
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    return lines[-1] if lines else "(unknown)"


def parse_gateway_runtime(in_dir: Path) -> str:
    body = read_capture_body(in_dir, "openclaw_gateway_status")
    if not body:
        return "(not collected)"
    runtime = ""
    rpc = ""
    for line in body.splitlines():
        line = line.strip()
        if line.lower().startswith("runtime:"):
            runtime = line.split(":", 1)[1].strip()
        elif line.lower().startswith("rpc probe:"):
            rpc = line.split(":", 1)[1].strip()
    if runtime and rpc:
        return f"Runtime: {runtime}; RPC probe: {rpc}"
    if runtime:
        return f"Runtime: {runtime}"
    return body.splitlines()[0].strip()


def build_environment_rows(in_dir: Path) -> List[Tuple[str, str]]:
    rows = [
        ("OS", detect_os(in_dir)),
        ("OpenClaw version", parse_version(in_dir)),
        ("Gateway status", parse_gateway_runtime(in_dir)),
        ("Gateway bind", one_line(read_config_value(in_dir, "openclaw_config_gateway_bind"))),
        ("Gateway auth mode", one_line(read_config_value(in_dir, "openclaw_config_gateway_auth_mode"))),
        ("Gateway auth.allowTailscale", one_line(read_config_value(in_dir, "openclaw_config_gateway_auth_allow_tailscale"))),
        ("Control UI allowed origins", one_line(read_config_value(in_dir, "openclaw_config_gateway_controlui_allowed_origins"))),
        ("Trusted proxies", one_line(read_config_value(in_dir, "openclaw_config_gateway_trusted_proxies"))),
        ("allowRealIpFallback", one_line(read_config_value(in_dir, "openclaw_config_gateway_allow_real_ip_fallback"))),
        ("Discovery mDNS mode", one_line(read_config_value(in_dir, "openclaw_config_discovery_mdns_mode"))),
        ("Session dmScope", one_line(read_config_value(in_dir, "openclaw_config_session_dm_scope"))),
        ("Default DM policy", one_line(read_config_value(in_dir, "openclaw_config_channels_defaults_dm_policy"))),
        ("Default group policy", one_line(read_config_value(in_dir, "openclaw_config_channels_defaults_group_policy"))),
        ("Tools profile", one_line(read_config_value(in_dir, "openclaw_config_tools_profile"))),
        ("FS workspaceOnly", one_line(read_config_value(in_dir, "openclaw_config_tools_fs_workspace_only"))),
        ("Exec security", one_line(read_config_value(in_dir, "openclaw_config_tools_exec_security"))),
        ("Elevated tools enabled", one_line(read_config_value(in_dir, "openclaw_config_tools_elevated_enabled"))),
        ("Logging redactSensitive", one_line(read_config_value(in_dir, "openclaw_config_logging_redact_sensitive"))),
    ]
    docker_ps = read_capture_body(in_dir, "docker_ps")
    if docker_ps:
        rows.append(("Docker present", "yes"))
    return rows


def overall_risk(counts: Dict[str, int]) -> str:
    if counts.get("critical"):
        return "Critical"
    if counts.get("high"):
        return "High"
    if counts.get("medium"):
        return "Moderate"
    if counts.get("low"):
        return "Low"
    if counts.get("info") or counts.get("unknown"):
        return "Informational"
    return "No parsed findings"


def likely_verification_for(check_id: str) -> str:
    if check_id.startswith("gateway.") or check_id.startswith("security.exposure.") or check_id.startswith("discovery."):
        return "`openclaw security audit --deep --json`, `openclaw gateway probe --json`, `openclaw channels status --probe`"
    if check_id.startswith("fs.") or check_id.startswith("logging."):
        return "`openclaw security audit --json` and re-check filesystem permissions"
    if check_id.startswith("sandbox.") or check_id.startswith("tools."):
        return "`openclaw security audit --deep --json` plus targeted `openclaw config get ...`"
    return "`openclaw security audit --deep --json`"


def markdown_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a Markdown report from OpenClaw audit artefacts.")
    parser.add_argument("--input", required=True, help="Audit folder or parent folder produced by collect_openclaw_audit.sh")
    parser.add_argument("--output", required=True, help="Output Markdown file")
    args = parser.parse_args()

    in_path = Path(args.input)
    in_dir = newest_audit_folder(in_path)
    out_path = Path(args.output)

    if not in_dir.exists() or not in_dir.is_dir():
        raise SystemExit(f"Input directory not found: {in_dir}")

    skill_root = Path(__file__).resolve().parents[1]
    check_map = load_checkid_map(skill_root)

    audit_sources = [
        in_dir / "openclaw_security_audit_deep_json.txt",
        in_dir / "openclaw_security_audit_json.txt",
    ]
    findings: List[Dict[str, Any]] = []
    parsed_files: List[str] = []
    for path in audit_sources:
        obj = load_json_capture(path)
        if obj is not None:
            parsed_files.append(path.name)
            findings.extend(extract_findings(obj))

    findings = dedupe_findings(findings)
    findings_sorted = sorted(findings, key=sort_key)
    counts = severity_counts(findings_sorted)
    env_rows = build_environment_rows(in_dir)

    report: List[str] = []
    report.append("# OpenClaw Security Audit Report\n\n")
    report.append("## Executive summary\n\n")
    report.append(f"- **Overall risk rating:** {overall_risk(counts)}\n")
    report.append(f"- **OpenClaw version:** {parse_version(in_dir)}\n")
    report.append(f"- **Audit artefacts folder:** `{in_dir}`\n")
    if parsed_files:
        report.append(f"- **Parsed audit files:** {', '.join(f'`{name}`' for name in parsed_files)}\n")
    else:
        report.append("- **Parsed audit files:** none (review raw artefacts manually)\n")

    if findings_sorted:
        report.append("- **Most urgent issues:**\n")
        for finding in findings_sorted[:3]:
            check_id = str(finding.get("checkId") or finding.get("id") or "(unknown)")
            summary = pick_text(finding)
            sev = normalise_sev(str(finding.get("severity") or finding.get("level") or finding.get("risk") or "unknown"))
            report.append(f"  - `{check_id}` ({sev}): {summary}\n")
    else:
        report.append("- **Most urgent issues:** none parsed automatically; inspect raw audit outputs.\n")
    report.append("\n")

    report.append("## Environment overview\n\n")
    for key, value in env_rows:
        report.append(f"- **{key}:** {value}\n")
    report.append("\n")

    report.append("## Finding counts\n\n")
    if counts:
        for sev in ("critical", "high", "medium", "low", "info", "unknown"):
            if sev in counts:
                report.append(f"- **{sev}:** {counts[sev]}\n")
    else:
        report.append("- No findings parsed.\n")
    report.append("\n")

    report.append("## Findings\n\n")
    if not findings_sorted:
        report.append("No findings were parsed from the collected JSON. Review these files manually:\n\n")
        for path in audit_sources:
            report.append(f"- `{path.name}`\n")
        report.append("\n")
    else:
        report.append("| Severity | Check ID | Summary | Why it matters | Likely fix area | Auto-fix | Verification |\n")
        report.append("|---|---|---|---|---|---:|---|\n")
        for finding in findings_sorted[:400]:
            sev = normalise_sev(str(finding.get("severity") or finding.get("level") or finding.get("risk") or "unknown"))
            check_id = str(finding.get("checkId") or finding.get("id") or "").strip() or "(unknown)"
            summary = markdown_escape(pick_text(finding))
            enrich = check_map.get(check_id, {}) if isinstance(check_map, dict) else {}

            why = ""
            likely_fix = ""
            auto_fix = ""

            if isinstance(enrich, dict):
                why = str(enrich.get("why") or "")
                likely_fix = str(enrich.get("primary_fix") or "")
                if "auto_fix" in enrich:
                    auto_fix = "yes" if enrich.get("auto_fix") else "no"

            for key in ("why", "reason"):
                value = finding.get(key)
                if isinstance(value, str) and value.strip():
                    why = value.strip()
                    break

            for key in ("primaryFix", "fix", "path", "configPath"):
                value = finding.get(key)
                if isinstance(value, str) and value.strip():
                    likely_fix = value.strip()
                    break
                if isinstance(value, dict):
                    maybe_path = value.get("path")
                    if isinstance(maybe_path, str) and maybe_path.strip():
                        likely_fix = maybe_path.strip()
                        break

            if isinstance(finding.get("autoFix"), bool):
                auto_fix = "yes" if finding.get("autoFix") else "no"

            report.append(
                "| {sev} | {check_id} | {summary} | {why} | {fix} | {auto_fix} | {verify} |\n".format(
                    sev=sev,
                    check_id=markdown_escape(check_id),
                    summary=summary,
                    why=markdown_escape(why or "(see finding detail)"),
                    fix=markdown_escape(likely_fix or "(see config / finding detail)"),
                    auto_fix=auto_fix or "",
                    verify=markdown_escape(likely_verification_for(check_id)),
                )
            )
        report.append("\n")

    report.append("## Remediation plan\n\n")
    report.append("### Phase 1 — Stop the bleeding (same day)\n\n")
    report.append("1. Fix any public exposure, missing auth, or open groups combined with dangerous tools.\n")
    report.append("2. Back up the current state before invasive changes: `openclaw backup create --verify`.\n")
    report.append("3. Remove insecure Control UI / reverse-proxy settings and lock down DM/group access.\n\n")

    report.append("### Phase 2 — Reduce blast radius (this week)\n\n")
    report.append("1. Move inbox-facing agents to a conservative tool profile and deny unnecessary groups.\n")
    report.append("2. Tighten workspace, exec, sandbox, node, and plugin trust settings.\n")
    report.append("3. Review writable paths, local skill/plugin sources, transcript retention, and log redaction.\n\n")

    report.append("### Phase 3 — Operationalise (ongoing)\n\n")
    report.append("- Keep OpenClaw and the host OS updated.\n")
    report.append("- Rotate gateway credentials after any suspected leakage.\n")
    report.append("- Re-run `openclaw security audit --deep --json` after major config changes.\n")
    report.append("- Keep an intentional backup/restore routine for config, state, and workspace.\n\n")

    report.append("## Key raw artefacts\n\n")
    for stem in (
        "openclaw_status_all",
        "openclaw_status_deep",
        "openclaw_gateway_status",
        "openclaw_gateway_probe_json",
        "openclaw_channels_status_probe",
        "openclaw_security_audit_json",
        "openclaw_security_audit_deep_json",
        "openclaw_health_json",
    ):
        path = in_dir / f"{stem}.txt"
        if path.exists():
            report.append(f"- `{path.name}`\n")
    report.append("\n")

    report.append("## Residual risk notes\n\n")
    report.append(
        "Even after hardening, any agent that can read untrusted content and call tools carries prompt-injection and social-engineering risk. "
        "Document which surfaces are intentionally open, which tools remain enabled, and what the recovery path is if the Gateway host or credentials are compromised.\n"
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
