#!/usr/bin/env python3
"""
CCPA Check — CCPA/CPRA compliance check (free skill + cloud compliance engine)

Based on the California Consumer Privacy Act (CCPA, Cal. Civ. Code §1798.100 et seq.)
and the California Privacy Rights Act (CPRA, effective Jan 1, 2023).
Covers 12 core checks across applicability, consumer rights, opt-out, service
providers, records, and security.

This skill is free to install. Check items are served by the CQDev
cloud compliance engine (compliancehub.cn); scoring and quota are computed in
the cloud. Before first use, get a free API Key (100 free calls) at compliancehub.cn:
  - Open: https://compliancehub.cn/account.html?skill=ccpa-check
    (register in the browser; the Key is shown instantly after registration)
  - Then provide the Key via env: export COMPLIANCEHUB_API_KEY=<your-key>
    or save it to: ~/.config/compliancehub/ccpa-check.key (mode 0600)

Flow:
  1. Load API Key (env COMPLIANCEHUB_API_KEY, or ~/.config/compliancehub/ccpa-check.key)
  2. Fetch check items from the cloud rule-library API (public read, single source)
  3. Interactively collect per-item compliance status (y=pass / n=fail / na=n/a)
  4. Submit to the cloud evaluate endpoint; the cloud scores and returns report data
  5. Render a professional report locally

No API Key yet? The skill runs in anonymous trial mode automatically: a local
random anon_id is issued, and you get up to 5 real cloud-scored evaluations per
skill (7-day window). When the trial runs out the skill points you to the
one-click registration page, carrying your anon_id so nothing is lost.

Uses only Python built-in urllib — zero third-party dependencies. HTTPS + Bearer
transport for the key; no hardcoding, no covert exfiltration. Network access happens ONLY
during a scored run: (a) fetching the public check-item rule library from the pinned endpoint
(read-only, NO answers sent), and (b) your scored answers + the API Key (as a Bearer token) to
the pinned evaluate endpoint. The free --non-interactive / --non-interactive-json previews run
fully OFFLINE using the bundled CHECK_ITEMS and never contact the cloud. No credentials are
collected. No other data leaves the machine; registration is done on the website
(compliancehub.cn/account.html), not in the terminal.
"""
import sys, os, json, argparse, datetime, ssl, uuid
import urllib.request
import urllib.error
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))

# ─── Cloud endpoints ──────────────────────────────────────────────
# API_BASE is PINNED to the operator's official compliance cloud and is
# intentionally NOT overridable via an environment variable. Allowing a
# COMPLIANCEHUB_API_BASE override would let a malicious environment redirect
# users' compliance answers AND their API Key (sent as a Bearer token) to an
# attacker-controlled server — flagged by security scanners as a "redirectable
# cloud endpoint" / credential-exfiltration chain. The destination is fixed.
API_BASE = "https://compliancehub.cn"
SKILL_SLUG = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RULES_URL = f"{API_BASE}/api/v1/rules/{SKILL_SLUG}/rules"        # public read: check items
EVALUATE_URL = f"{API_BASE}/api/v1/rules/{SKILL_SLUG}/evaluate"  # auth: scoring
ACCOUNT_PAGE = f"{API_BASE}/account.html?skill={SKILL_SLUG}&utm_source=skill&utm_medium=agent"      # unified account center (utm for attribution)


def _skill_version():
    pkg = os.path.join(os.path.dirname(__file__), "..", "package.json")
    try:
        if os.path.isfile(pkg):
            with open(pkg, encoding="utf-8") as f:
                return json.load(f).get("version", "2.0.0")
    except Exception:
        pass
    return "2.0.0"


def _ua():
    return f"{SKILL_SLUG}/{_skill_version()}"


# ─── API Key resolution ──────────────────────────────────────────

def _key_path():
    """Private, per-user key store OUTSIDE the skill directory.

    The API Key is written here (mode 0600) rather than inside the skill
    folder, so it is never committed to source control or shared with the
    workspace. This addresses the 'plaintext API key in shared/source-
    controlled workspace' concern raised in security review.
    """
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.key")


def load_api_key():
    """Resolve API Key precedence:
      1) env COMPLIANCEHUB_API_KEY (ephemeral, safest)
      2) private store ~/.config/compliancehub/<slug>.key (mode 0600)
    """
    env_key = os.environ.get("COMPLIANCEHUB_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    p = _key_path()
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                s = f.read().strip()
                if s:
                    return s
        except Exception:
            pass
    return None


def _anon_id_path():
    """Per-user anonymous trial id store (mode 0600), outside the skill dir."""
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.anon_id")


def load_or_create_anon_id():
    """Return the persistent anonymous trial id, creating a fresh uuid on first run.

    The anon_id lets the cloud engine keep a 7-day, up-to-5-use anonymous quota
    per skill WITHOUT requiring registration first. It is a plain random uuid and
    carries no personal data; it is only used to continue the anonymous trial
    and to pre-fill the registration page when the trial runs out.
    """
    p = _anon_id_path()
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                s = f.read().strip()
                if s and len(s) <= 64:
                    return s
        except Exception:
            pass
    aid = str(uuid.uuid4())
    try:
        with open(p, "w", encoding="utf-8") as f:
            f.write(aid)
        os.chmod(p, 0o600)
    except Exception:
        pass
    return aid


def _register_page(anon_id=None):
    """Registration funnel URL. The anon_id is passed through so the account page
    can keep the visitor's trial context and make registering a one-click jump."""
    url = ACCOUNT_PAGE
    if anon_id:
        url += "&anon_id=" + urllib.parse.quote(anon_id)
    return url


# ─── Rule data source (cloud rule-library API, public read) ──────

def fetch_rules():
    """Fetch ccpa-check items from the cloud rule library (public, no Key needed).

    Returns a mapped item list (id=item_key / name / desc / ref / category /
    recommendation); returns None on any error so the caller falls back to the
    built-in CHECK_ITEMS.
    """
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(RULES_URL, headers={"User-Agent": _ua()})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            if resp.status != 200:
                return None
            payload = json.loads(resp.read().decode("utf-8"))
        if not payload.get("success"):
            return None
        raw_items = payload.get("items") or []
        if not raw_items:
            return None
        items = []
        for it in raw_items:
            items.append({
                "id": it.get("item_key"),
                "name": it.get("name"),
                "desc": it.get("question") or it.get("description") or "",
                "ref": it.get("legal_ref") or "",
                "category": it.get("category_name") or "",
                "recommendation": it.get("recommendation") or "",
            })
        return items
    except Exception:
        return None


# ─── Check items (fallback data source) ─────────────────────────

CHECK_ITEMS = [
    {"id": "applicability_business", "name": "Business Applicability", "desc": "Does your business meet the CCPA 'business' threshold (revenue > $25M; buys/sells/shares PI of ≥100k consumers; or ≥50% revenue from selling/sharing PI)?", "ref": "CCPA §1798.140(d)", "category": "A. Applicability & Notice"},
    {"id": "notice_disclosure", "name": "Privacy Notice at Collection", "desc": "At or before collection, do you disclose categories of PI collected and purposes of use?", "ref": "CCPA §1798.100(b)", "category": "A. Applicability & Notice"},
    {"id": "consumer_rights", "name": "Consumer Rights Fulfillment", "desc": "Do you support know/delete/correct rights with working request channels?", "ref": "CCPA §1798.100/105/106", "category": "B. Consumer Rights"},
    {"id": "identity_verification", "name": "Identity Verification", "desc": "Do you verify the consumer's identity for rights requests without undue burden?", "ref": "CCPA §1798.145(i)", "category": "B. Consumer Rights"},
    {"id": "response_timeliness", "name": "Response Timeliness", "desc": "Do you respond to verifiable requests within 45 calendar days (or one permitted extension)?", "ref": "CCPA §1798.130(a)(2)", "category": "B. Consumer Rights"},
    {"id": "non_discrimination", "name": "Non-Discrimination", "desc": "Do you refrain from discriminating against consumers who exercise their rights?", "ref": "CCPA §1798.125", "category": "B. Consumer Rights"},
    {"id": "opt_out_mechanism", "name": "Right to Opt-Out", "desc": "Do you provide a 'Do Not Sell or Share' link and honor opt-out (incl. GPC signals)?", "ref": "CCPA §1798.120", "category": "C. Opt-Out & Data Control"},
    {"id": "sensitive_pi_handling", "name": "Sensitive PI Handling", "desc": "For sensitive PI, do you limit use to permitted purposes and offer a right to limit use?", "ref": "CPRA §1798.121", "category": "C. Opt-Out & Data Control"},
    {"id": "data_sale_management", "name": "Sale/Sharing of PI", "desc": "If you sell/share PI, is it disclosed with opt-out and bounded by contract?", "ref": "CCPA §1798.140(t)/115", "category": "C. Opt-Out & Data Control"},
    {"id": "service_provider_mgmt", "name": "Service Provider Contracts", "desc": "Do contracts with service providers/contractors prohibit secondary use of PI?", "ref": "CCPA §1798.140(ag)", "category": "D. Service Providers & Records"},
    {"id": "record_keeping", "name": "Record Keeping", "desc": "Do you keep records of consumer requests and how they were handled (≥24 months)?", "ref": "CCPA §1798.130(a)", "category": "D. Service Providers & Records"},
    {"id": "data_security_measures", "name": "Reasonable Security", "desc": "Do you maintain reasonable security procedures appropriate to the nature of the PI?", "ref": "CCPA §1798.81.5", "category": "E. Data Security"},
]


# ─── Interactive collection ──────────────────────────────────────

def collect_responses(items):
    """Collect per-item compliance status interactively (y=pass / n=fail / na=n/a)."""
    responses = []
    total = len(items)
    print(f"\n📋 CCPA/CPRA Compliance Check — {total} items")
    print("   Answer each item's actual status (y=pass / n=fail / na=not applicable)\n")
    for i, item in enumerate(items):
        idx = i + 1
        while True:
            ans = input(f"  [{idx}/{total}] {item['name']} [{item['ref']}]\n"
                        f"        {item['desc']}\n"
                        f"        (y/n/na) > ").strip().lower()
            if ans in ('y', 'n', 'na'):
                if ans == 'na':
                    responses.append({**item, "status": "na"})
                else:
                    responses.append({**item, "status": "pass" if ans == 'y' else "fail"})
                break
            print("        please enter y, n or na")
    return responses


def build_submission(responses):
    """Convert interactive results to cloud evaluate request items (na excluded)."""
    items = []
    for r in responses:
        if r["status"] == "na":
            continue
        items.append({
            "item_key": r["id"],
            "passed": r["status"] == "pass",
            "evidence": None,
        })
    return items


# ─── Cloud scoring ───────────────────────────────────────────────

def call_evaluate(key, submission, anon_id=None):
    """Call the cloud evaluate endpoint; returns (data, error)."""
    payload = {"items": submission, "context": None}
    if anon_id:
        payload["anon_id"] = anon_id
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": _ua()}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(
        EVALUATE_URL,
        data=body,
        headers=headers,
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            if resp.status != 200:
                return None, f"cloud returned HTTP {resp.status}"
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = json.loads(e.read().decode("utf-8", "ignore")).get("detail", "")
        except Exception:
            pass
        if e.code == 401:
            return None, "API Key invalid or unauthorized; get a new one at %s (then set COMPLIANCEHUB_API_KEY or save to the key file)" % ACCOUNT_PAGE
        if e.code == 403:
            if anon_id:
                # Anonymous trial exhausted -> the caller routes to registration.
                return None, "ANON_QUOTA_EXHAUSTED"
            return None, f"free quota exhausted: {detail} (get a new key at %s)" % ACCOUNT_PAGE
        if e.code == 404:
            return None, f"rule library not open: {detail}"
        return None, f"cloud error HTTP {e.code}: {detail}"
    except Exception as e:
        return None, f"cloud call failed: {e}"


# ─── Report rendering ────────────────────────────────────────────

def render_text(data, items):
    s = data
    lines = [
        "=" * 60,
        "  CCPA/CPRA Compliance Check Report (cloud-scored)",
        "  Law: California Consumer Privacy Act (CCPA) & CPRA amendment",
        f"  Engine version: {s.get('version', '?')}",
        f"  Compliance score: {s.get('score')}/100",
        "=" * 60,
        f"  Overview: {s.get('total_items')} items counted | ✅ Pass {s.get('passed_count')} | ❌ Fail {s.get('failed_count')} | Free quota left {s.get('quota_remaining')}",
        "=" * 60,
    ]
    current_cat = ""
    for r in items:
        if r.get("category") != current_cat:
            current_cat = r.get("category", "")
            lines.append(f"\n  ── {current_cat} ──")
        icon = "✅" if r.get("passed") else "❌"
        lines.append(f"\n  {icon} [{r.get('item_key')}] {r.get('name')}")
        lines.append(f"    Status: {'Pass' if r.get('passed') else 'Fail'}")
        if r.get("legal_ref"):
            lines.append(f"    Authority: {r.get('legal_ref')}")
        if r.get("recommendation"):
            lines.append(f"    Recommendation: {r.get('recommendation')}")
    lines.append("=" * 60)
    lines.append("\n💡 Disclaimer: This report is generated by the CQDev cloud compliance engine for reference only and does not constitute legal advice.")
    return "\n".join(lines)


def render_html(data, items):
    s = data
    score = s.get("score", 0)
    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 60 else "#f44336"
    rows = ""
    current_cat = ""
    for r in items:
        if r.get("category") != current_cat:
            current_cat = r.get("category", "")
            rows += f'<tr class="category-row"><td colspan="5">{current_cat}</td></tr>\n'
        icon = "✅" if r.get("passed") else "❌"
        cls = "pass" if r.get("passed") else "fail"
        rec = r.get("recommendation") or "Keep it up"
        rows += f"""<tr class="{cls}"><td>{icon}</td><td>{r.get('name')}</td><td>{r.get('legal_ref') or ''}</td><td>{cls.upper()}</td><td>{rec}</td></tr>\n"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>CCPA/CPRA Compliance Check Report</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#333}}
h1{{border-bottom:2px solid #2563eb;padding-bottom:.5rem}}
.score-card{{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;padding:2rem;border-radius:12px;text-align:center;margin:1.5rem 0}}
.score{{font-size:4rem;font-weight:700}}
.summary{{display:flex;gap:2rem;justify-content:center;margin-top:1rem}}
.summary div{{text-align:center;font-size:1.2rem}}
table{{width:100%;border-collapse:collapse;margin-top:1.5rem}}
th{{background:#f1f5f9;text-align:left;padding:.75rem;border-bottom:2px solid #e2e8f0}}
td{{padding:.75rem;border-bottom:1px solid #e2e8f0}}
tr.pass td:first-child{{color:#4caf50}}
tr.fail td:first-child{{color:#f44336}}
tr.category-row td{{background:#dbeafe;font-weight:600;color:#1d4ed8}}
.note{{color:#94a3b8;margin-top:2rem;font-size:.85rem}}
</style></head>
<body>
<h1>CCPA/CPRA Compliance Check Report</h1>
<p>Law: California Consumer Privacy Act (CCPA) &amp; California Privacy Rights Act (CPRA)</p>
<p>Engine version: {s.get('version','?')} ｜ Free quota left: {s.get('quota_remaining')}</p>
<div class="score-card"><div class="score">{score}</div><div>Compliance score / 100</div>
<div class="summary"><div>✅ Pass<br><b>{s.get('passed_count')}</b></div><div>❌ Fail<br><b>{s.get('failed_count')}</b></div><div>Items<br><b>{s.get('total_items')}</b></div></div></div>
<table><thead><tr><th></th><th>Check</th><th>Authority</th><th>Status</th><th>Recommendation</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">This report is generated by the CQDev cloud compliance engine for reference only and does not constitute legal advice.</p>
</body></html>"""


def generate_report(payload, format="text"):
    """Render report from cloud response. payload is the full evaluate JSON."""
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    items = data.get("items", [])
    if format == "json":
        return json.dumps(payload, ensure_ascii=False, indent=2)
    elif format == "html":
        return render_html(data, items)
    return render_text(data, items)


# ─── Main entry ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CCPA/CPRA compliance check (free skill + cloud engine)")
    parser.add_argument("--non-interactive", action="store_true", help="free preview mode (list items, no scoring)")
    parser.add_argument("--non-interactive-json", action="store_true", help="free preview JSON mode (for sandbox case generation)")
    parser.add_argument("--format", "-f", choices=["text", "json", "html"], default="text")
    parser.add_argument("--output", "-o", help="report output file path")
    args = parser.parse_args()

    # ── free previews run OFFLINE using the bundled CHECK_ITEMS (no network) ──
    if args.non_interactive or args.non_interactive_json:
        items = CHECK_ITEMS
        if args.non_interactive_json:
            preview_data = [{
                "id": item["id"], "name": item["name"],
                "desc": item["desc"], "ref": item["ref"], "category": item["category"],
            } for item in items]
            print(json.dumps({
                "preview": True,
                "total_items": len(items),
                "free": True,
                "needs_api_key": True,
                "offline": True,
                "register_page": ACCOUNT_PAGE,
                "message": "This check is free, but scoring runs on the CQDev cloud engine and needs a free API Key.",
                "preview_items": preview_data,
            }, ensure_ascii=False, indent=2))
            return

        # ── free preview (list items, no scoring, no Key) ──
        print(f"\n🔍 Free preview mode — {len(items)} items (offline, bundled); scoring needs a free API Key\n")
        current_cat = ""
        for it in items:
            if it.get("category") != current_cat:
                current_cat = it.get("category", "")
                print(f"\n  ── {current_cat} ──")
            print(f"  • [{it['id']}] {it['name']}  [{it['ref']}]")
            print(f"      {it['desc']}")
        print(f"\n💡 Scoring runs on the cloud engine. Get a free API Key: {ACCOUNT_PAGE}")
        return

    # ── full check: registered Key, or anonymous trial when no Key ──
    key = load_api_key()
    anon_id = None
    if not key:
        anon_id = load_or_create_anon_id()
        print("🔒 匿名试用模式：本检查将通过 compliancehub.cn 云端引擎真实评分，无需注册可免费试 5 次。")
        print("   你的作答将发送到 compliancehub.cn 云端引擎进行评分，用于生成本次合规报告；详细数据处理见隐私政策 https://compliancehub.cn/privacy.html")
    # Check items come from the cloud rule library; fall back to built-in CHECK_ITEMS on failure
    items = fetch_rules() or CHECK_ITEMS
    responses = collect_responses(items)
    submission = build_submission(responses)
    if not submission:
        print("❌ No countable items (all marked not applicable).")
        sys.exit(1)

    print("\n⏳ Submitting to cloud compliance engine for scoring…")
    payload, err = call_evaluate(key, submission, anon_id)
    if err == "ANON_QUOTA_EXHAUSTED":
        reg = _register_page(anon_id)
        if args.format == "json":
            print(json.dumps({"error": "anon_quota_exhausted",
                              "message": "匿名试用额度已用尽（每 skill 5 次），请注册后继续使用",
                              "get_key_page": reg}, ensure_ascii=False, indent=2))
        else:
            print("❌ 匿名试用的 5 次额度已用尽。")
            print("💡 注册即可继续使用（免费 API Key 含 100 次额度）。")
            print(f"👉 打开注册页（已带入你的试用进度）：{reg}")
        sys.exit(2)
    elif err:
        print(f"❌ {err}")
        sys.exit(1)

    report = generate_report(payload, format=args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Report saved to: {args.output}")
    else:
        print(report)
    data_out = payload.get("data") or {}
    if anon_id:
        tl = data_out.get("trials_left")
        if tl is not None:
            print(f"\n💡 匿名试用剩余次数：{tl}/5（注册后每把 Key 含 100 次免费额度）。")
    else:
        rem = data_out.get("quota_remaining")
        if rem is not None:
            print(f"\n💡 This Key's remaining free quota: {rem} calls.")


if __name__ == "__main__":
    main()
