#!/usr/bin/env python3
"""
GDPR Compliance Check — General Data Protection Regulation (EU) 2016/679 (GDPR)

Free skill + CQDev cloud compliance engine (compliancehub.cn).
Scoring and quota are computed in the cloud; before first use, register for a
free API Key (100 free calls) on the web:

  Open: https://compliancehub.cn/account.html?skill=gdpr-check
  Then provide the Key via env COMPLIANCEHUB_API_KEY, or save it to
  ~/.config/compliancehub/gdpr-check.key (mode 0600).

Flow:
  1. Load API Key (env COMPLIANCEHUB_API_KEY, or ~/.config/compliancehub/<slug>.key)
  2. Fetch check items from the cloud rule-library API (public read)
  3. Collect per-item compliance status (y=pass / n=fail / na=n/a)
  4. Submit to the cloud evaluate endpoint (auth) OR score locally on 404
  5. Render a professional report locally

No API Key yet? The skill runs in anonymous trial mode automatically: a local
random anon_id is issued, and you get up to 5 real cloud-scored evaluations per
skill (7-day window). When the trial runs out the skill points you to the
one-click registration page, carrying your anon_id so nothing is lost.

Uses only Python built-in urllib — zero third-party dependencies. HTTPS + Bearer
transport for the key; no hardcoding, no covert exfiltration. Account creation and
API Key issuance happen on the website (compliancehub.cn), not in this skill. Outbound
network calls are: (a) fetching the public check-item rule library from the pinned endpoint
before any preview/scored run (read-only, NO answers sent); and (b) your scored answers + the
API Key (as a Bearer token) to the pinned evaluate endpoint. No other data leaves the machine.

Language: bilingual (中文/English). Item names, categories and recommendations are
presented in Chinese by default for Chinese-speaking compliance teams; legal/regulatory
references keep English originals. Users may request English output at any time.
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
                return json.load(f).get("version", "1.0.0")
    except Exception:
        pass
    return "1.0.0"


def _ua():
    return f"{SKILL_SLUG}/{_skill_version()}"


def _key_path():
    """Private, per-user key store OUTSIDE the skill directory.
    The API Key is written here (mode 0600) rather than inside the skill
    folder, so it is never bundled with or leaked by the skill package.
    """
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.key")


def load_api_key():
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


def fetch_rules():
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


CHECK_ITEMS = [
    {"id": "applicability", "name": "Material & Territorial Scope", "ref": "Art. 3", "category": "A. \u9002\u7528\u6027",
     "desc": "Does GDPR apply (establishment in EU, or offering goods/services / monitoring to EU data subjects)?", "recommendation": "\u786e\u8ba4\u9002\u7528\u6027\u8fb9\u754c\u4e0e\u6240\u5904\u7406\u6570\u636e\u4e3b\u4f53\u8303\u56f4\u3002"},
    {"id": "legal_basis", "name": "Lawful Basis for Processing", "ref": "Art. 6", "category": "B. \u5904\u7406\u5408\u6cd5\u6027",
     "desc": "Do all processing activities have a documented lawful basis (consent/contract/legal obligation/etc.)?", "recommendation": "\u9010\u6d3b\u52a8\u6620\u5c04\u5408\u6cd5\u4f9d\u636e\u5e76\u5b58\u6863\u3002"},
    {"id": "consent", "name": "Valid Consent", "ref": "Art. 7", "category": "B. \u5904\u7406\u5408\u6cd5\u6027",
     "desc": "Where relying on consent, is it freely given, specific, informed, unambiguous, and withdrawable?", "recommendation": "\u540c\u610f\u673a\u5236\u53ef\u64a4\u56de\u3001\u7559\u75d5\uff0c\u4e0d\u4e0e\u670d\u52a1\u6346\u7ed1\u3002"},
    {"id": "transparency", "name": "Transparency & Privacy Notice", "ref": "Art. 13-14", "category": "C. \u900f\u660e\u5ea6",
     "desc": "Do you provide clear information at collection (identity, purposes, rights, transfers)?", "recommendation": "\u9690\u79c1\u58f0\u660e\u8986\u76d6 Art.13/14 \u5168\u90e8\u8981\u7d20\u3002"},
    {"id": "data_subject_rights", "name": "Data Subject Rights", "ref": "Art. 15-17", "category": "D. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "Do you support access, rectification, and erasure in practice?", "recommendation": "\u5efa\u7acb\u6743\u5229\u8bf7\u6c42\u53d7\u7406\u4e0e\u54cd\u5e94\u6d41\u7a0b\uff08\u22641 \u4e2a\u6708\uff09\u3002"},
    {"id": "automated_decision", "name": "Automated Decision-Making", "ref": "Art. 22", "category": "D. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "Do you provide human oversight / safeguards for solely automated decisions with legal effects?", "recommendation": "\u9ad8\u98ce\u9669\u81ea\u52a8\u51b3\u7b56\u63d0\u4f9b\u7533\u8bc9\u4e0e\u4eba\u5ba1\u3002"},
    {"id": "dpia", "name": "Data Protection Impact Assessment", "ref": "Art. 35", "category": "E. \u95ee\u8d23",
     "desc": "Do you conduct a DPIA for high-risk processing?", "recommendation": "\u9ad8\u98ce\u9669\u5904\u7406\uff08\u753b\u50cf/\u5927\u89c4\u6a21\u654f\u611f\u6570\u636e\uff09\u505a DPIA\u3002"},
    {"id": "breach_notification", "name": "Breach Notification", "ref": "Art. 33-34", "category": "F. \u8fdd\u7ea6\u901a\u77e5",
     "desc": "Can you notify the supervisory authority within 72 hours of a breach?", "recommendation": "\u8fdd\u7ea6\u5206\u7ea7\u4e0e 72 \u5c0f\u65f6\u4e0a\u62a5\u6d41\u7a0b\u5c31\u7eea\u3002"},
    {"id": "cross_border_transfer", "name": "International Transfers", "ref": "Art. 44-49", "category": "G. \u8de8\u5883\u4f20\u8f93",
     "desc": "Do transfers outside the EEA rely on adequacy decisions / SCCs / BCRs?", "recommendation": "\u8de8\u5883\u4f20\u8f93\u8d70 SCC \u6216\u5145\u5206\u6027\u8ba4\u5b9a\u3002"},
    {"id": "security", "name": "Security of Processing", "ref": "Art. 32", "category": "H. \u5b89\u5168",
     "desc": "Is security appropriate to risk (pseudonymisation, encryption, resilience)?", "recommendation": "\u6280\u672f\u4e0e\u7ba1\u7406\u63aa\u65bd\u5339\u914d\u98ce\u9669\u7b49\u7ea7\u3002"},
    {"id": "processor_mgmt", "name": "Processor Agreements", "ref": "Art. 28", "category": "I. \u5904\u7406\u8005\u7ba1\u7406",
     "desc": "Do contracts with processors meet Art. 28 (instructions, security, audit)?", "recommendation": "\u4e0e\u5904\u7406\u8005\u7b7e\u7f72\u7b26\u5408 Art.28 \u7684 DPA\u3002"},
    {"id": "dpo", "name": "Data Protection Officer", "ref": "Art. 37-39", "category": "E. \u95ee\u8d23",
     "desc": "If required, have you appointed a DPO with the necessary resources and independence?", "recommendation": "\u5f3a\u5236\u60c5\u5f62\u4efb\u547d DPO \u5e76\u516c\u793a\u8054\u7cfb\u65b9\u5f0f\u3002"},
]


def collect_responses(items):
    responses = []
    total = len(items)
    print(f"\n📋 GDPR Compliance Check — {total} items")
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
    items = []
    for r in responses:
        if r["status"] == "na":
            continue
        items.append({"item_key": r["id"], "passed": r["status"] == "pass", "evidence": None})
    return items


def compute_local_score(submission, items):
    """Fallback scoring when cloud rule library is not yet open (404)."""
    meta = {it["id"]: it for it in items}
    total = len(submission)
    passed = sum(1 for s in submission if s["passed"])
    score = round(passed / total * 100) if total else 0
    out_items = []
    for s in submission:
        it = meta.get(s["item_key"], {}) or {}
        out_items.append({
            "item_key": s["item_key"], "name": it.get("name", s["item_key"]),
            "passed": s["passed"], "legal_ref": it.get("ref", ""),
            "recommendation": it.get("recommendation", ""), "category_name": it.get("category", ""),
        })
    return {
        "version": _skill_version(), "score": score,
        "passed_count": passed, "failed_count": total - passed, "total_items": total,
        "quota_remaining": None, "scored_locally": True, "items": out_items,
    }


def call_evaluate(key, submission, anon_id=None):
    payload = {"items": submission, "context": None}
    if anon_id:
        payload["anon_id"] = anon_id
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": _ua()}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(EVALUATE_URL, data=body, headers=headers, method="POST")
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
            return None, f"free quota exhausted: {detail}"
        if e.code == 404:
            return None, "RULE_LIB_NOT_OPEN"
        return None, f"cloud error HTTP {e.code}: {detail}"
    except Exception as e:
        return None, f"cloud call failed: {e}"


def _score_block(data):
    return (f"  Compliance score: {data.get('score')}/100\n"
            f"  ✅ Pass {data.get('passed_count')} | ❌ Fail {data.get('failed_count')} | Items {data.get('total_items')}")


def render_text(data, items):
    s = data
    lines = ["=" * 60, f"  GDPR Compliance Check Report (cloud-scored)" if not s.get("scored_locally") else f"  GDPR Compliance Check Report (local fallback score)",
             f"  Law: General Data Protection Regulation (EU) 2016/679 (GDPR)", f"  Engine version: {s.get('version', '?')}",
             _score_block(s), "=" * 60]
    current_cat = ""
    for r in items:
        if r.get("category_name") != current_cat:
            current_cat = r.get("category_name", "")
            lines.append(f"\n  ── {current_cat} ──")
        icon = "✅" if r.get("passed") else "❌"
        lines.append(f"\n  {icon} [{r.get('item_key')}] {r.get('name')}")
        if r.get("legal_ref"):
            lines.append(f"    Authority: {r.get('legal_ref')}")
        if r.get("recommendation"):
            lines.append(f"    Recommendation: {r.get('recommendation')}")
    lines.append("=" * 60)
    lines.append("\n💡 Disclaimer: reference only, not legal advice.")
    return "\n".join(lines)


def render_html(data, items):
    s = data
    score = s.get("score", 0)
    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 60 else "#f44336"
    rows = ""
    current_cat = ""
    for r in items:
        if r.get("category_name") != current_cat:
            current_cat = r.get("category_name", "")
            rows += f'<tr class="category-row"><td colspan="5">{current_cat}</td></tr>\n'
        icon = "✅" if r.get("passed") else "❌"
        cls = "pass" if r.get("passed") else "fail"
        rec = r.get("recommendation") or "Keep it up"
        rows += f"""<tr class="{cls}"><td>{icon}</td><td>{r.get('name')}</td><td>{r.get('legal_ref') or ''}</td><td>{cls.upper()}</td><td>{rec}</td></tr>\n"""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>GDPR Compliance Check Report</title>
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
</style></head><body>
<h1>GDPR Compliance Check Report</h1>
<p>Law: General Data Protection Regulation (EU) 2016/679 (GDPR)</p>
<p>Engine version: {s.get('version','?')}{' ｜ Local fallback score (cloud rule library not open yet)' if s.get('scored_locally') else ''}</p>
<div class="score-card"><div class="score">{score}</div><div>Compliance score / 100</div>
<div class="summary"><div>✅ Pass<br><b>{s.get('passed_count')}</b></div><div>❌ Fail<br><b>{s.get('failed_count')}</b></div><div>Items<br><b>{s.get('total_items')}</b></div></div></div>
<table><thead><tr><th></th><th>Check</th><th>Authority</th><th>Status</th><th>Recommendation</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">This report is generated by the CQDev cloud compliance engine for reference only and does not constitute legal advice.</p>
</body></html>"""


def generate_report(payload, format="text"):
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    items = data.get("items", [])
    if format == "json":
        return json.dumps(payload, ensure_ascii=False, indent=2)
    elif format == "html":
        return render_html(data, items)
    return render_text(data, items)


def main():
    parser = argparse.ArgumentParser(description="GDPR Compliance Check (free skill + cloud engine)")
    parser.add_argument("--non-interactive", action="store_true", help="free preview mode (list items, no scoring)")
    parser.add_argument("--non-interactive-json", action="store_true", help="free preview JSON mode")
    parser.add_argument("--format", "-f", choices=["text", "json", "html"], default="text")
    parser.add_argument("--output", "-o", help="report output file path")
    args = parser.parse_args()

    items = fetch_rules() or CHECK_ITEMS

    if args.non_interactive_json:
        preview_data = [{"id": it["id"], "name": it["name"], "desc": it["desc"], "ref": it["ref"], "category": it["category"]} for it in items]
        print(json.dumps({"preview": True, "total_items": len(items), "free": True, "needs_api_key": True,
                          "register_page": ACCOUNT_PAGE, "message": "Free skill; scoring runs on the CQDev cloud engine (free API Key).",
                          "preview_items": preview_data}, ensure_ascii=False, indent=2))
        return

    if args.non_interactive:
        print(f"\n🔍 Free preview mode — {len(items)} items; scoring needs a free API Key\n")
        current_cat = ""
        for it in items:
            if it.get("category") != current_cat:
                current_cat = it.get("category", "")
                print(f"\n  ── {current_cat} ──")
            print(f"  • [{it['id']}] {it['name']}  [{it['ref']}]")
            print(f"      {it['desc']}")
        print(f"\n💡 Scoring runs on the cloud engine. Get a free API Key: {ACCOUNT_PAGE}")
        return

    key = load_api_key()
    anon_id = None
    if not key:
        anon_id = load_or_create_anon_id()
        print("🔒 匿名试用模式：本检查将通过 compliancehub.cn 云端引擎真实评分，无需注册可免费试 5 次。")
        print("   你的作答将发送到 compliancehub.cn 云端引擎进行评分，用于生成本次合规报告；详细数据处理见隐私政策 https://compliancehub.cn/privacy.html")
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
    elif err == "RULE_LIB_NOT_OPEN":
        print("⚠️ Cloud rule library not open yet — using local fallback score (same questions, local computation).")
        data = compute_local_score(submission, items)
        payload = {"data": data}
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
