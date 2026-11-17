#!/usr/bin/env python3
"""
COPPA Compliance Check — Children's Online Privacy Protection Act (COPPA), 15 U.S.C. §6501 et seq. and the COPPA Rule (16 C.F.R. Part 312)

Free skill + CQDev cloud compliance engine (compliancehub.cn).
Scoring and quota are computed in the cloud; before first use, register for a
free API Key (100 free calls) on the web:

  Open: https://compliancehub.cn/account.html?skill=coppa-check
  Then provide the Key via env COMPLIANCEHUB_API_KEY, or save it to
  ~/.config/compliancehub/coppa-check.key (mode 0600).

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
    {"id": "applicability", "name": "Child-Directed / Actual Knowledge", "ref": "COPPA Rule \u00a7312.2", "category": "A. \u9002\u7528\u6027",
     "desc": "Is your service directed to children under 13, or do you have actual knowledge of collecting PI from under-13 users?", "recommendation": "\u786e\u8ba4\u662f\u5426\u843d\u5165 COPPA \u7ba1\u8f96\uff1b\u82e5\u4ec5\u662f\u901a\u7528\u670d\u52a1\uff0c\u9700\u505a\u5e74\u9f84\u8bc6\u522b\u4e0e\u5206\u6d41\u3002"},
    {"id": "verifiable_consent", "name": "Verifiable Parental Consent", "ref": "\u00a7312.4", "category": "B. \u5bb6\u957f\u540c\u610f",
     "desc": "Do you obtain verifiable parental consent before collecting, using, or disclosing PI from children?", "recommendation": "\u4e0a\u7ebf\u524d\u5b9e\u73b0\u53ef\u9a8c\u8bc1\u5bb6\u957f\u540c\u610f\u673a\u5236\uff08\u4fe1\u7528\u5361\u6821\u9a8c/\u7b7e\u540d\u786e\u8ba4/\u89c6\u9891\u7b49\uff09\u3002"},
    {"id": "direct_notice", "name": "Direct Notice to Parents", "ref": "\u00a7312.4(a)", "category": "B. \u5bb6\u957f\u540c\u610f",
     "desc": "Do you provide direct notice to parents about what PI is collected, how it is used, and with whom it is shared?", "recommendation": "\u5728\u6536\u96c6\u524d\u4ee5\u72ec\u7acb\u901a\u77e5\uff08\u975e\u4ec5\u9690\u79c1\u653f\u7b56\uff09\u544a\u77e5\u5bb6\u957f\u3002"},
    {"id": "collection_limitation", "name": "Collection Limitation", "ref": "\u00a7312.3", "category": "C. \u6536\u96c6\u6700\u5c0f\u5316",
     "desc": "Do you limit collection of children's PI to what is reasonably necessary for the service?", "recommendation": "\u79fb\u9664\u975e\u5fc5\u8981\u5b57\u6bb5\uff1b\u9ed8\u8ba4\u4e0d\u6536\u96c6\u7cbe\u786e\u4f4d\u7f6e/\u8054\u7cfb\u4eba\u7b49\u654f\u611f\u4fe1\u606f\u3002"},
    {"id": "parental_access", "name": "Parental Review & Deletion", "ref": "\u00a7312.4(d)", "category": "D. \u5bb6\u957f\u6743\u5229",
     "desc": "Do you let parents review their child's PI and refuse further use / request deletion?", "recommendation": "\u63d0\u4f9b\u5bb6\u957f\u67e5\u8be2\u3001\u66f4\u6b63\u3001\u5220\u9664\u901a\u9053\u5e76\u6838\u5b9e\u8eab\u4efd\u3002"},
    {"id": "data_security", "name": "Reasonable Data Security", "ref": "\u00a7312.8", "category": "E. \u5b89\u5168",
     "desc": "Do you maintain reasonable security safeguards appropriate to the sensitivity of children's PI?", "recommendation": "\u5bf9\u513f\u7ae5 PI \u52a0\u5bc6\u5b58\u50a8\u3001\u6700\u5c0f\u5316\u7559\u5b58\u3001\u9650\u5236\u5185\u90e8\u8bbf\u95ee\u3002"},
    {"id": "data_retention", "name": "Retention & Deletion", "ref": "\u00a7312.10", "category": "E. \u5b89\u5168",
     "desc": "Do you retain children's PI only as long as necessary to fulfill the service?", "recommendation": "\u8bbe\u5b9a\u81ea\u52a8\u8fc7\u671f\u6e05\u7406\u7b56\u7565\u5e76\u5b9a\u671f\u5ba1\u8ba1\u3002"},
    {"id": "third_party_disclosure", "name": "Third-Party Disclosure", "ref": "\u00a7312.4(a)(2)", "category": "F. \u7b2c\u4e09\u65b9",
     "desc": "Do you disclose the specific third parties (incl. ad/analytics) who receive children's PI?", "recommendation": "\u5217\u660e SDK/\u5e7f\u544a/\u5206\u6790\u5408\u4f5c\u65b9\uff1b\u8bc4\u4f30\u5176\u662f\u5426\u9700\u989d\u5916\u5bb6\u957f\u540c\u610f\u3002"},
    {"id": "safe_harbor", "name": "FTC Safe Harbor (if applicable)", "ref": "\u00a7312.11", "category": "G. \u5408\u89c4\u8ba1\u5212",
     "desc": "If relying on an FTC-approved safe harbor program, are you in compliance with it?", "recommendation": "\u82e5\u52a0\u5165\u5b89\u5168\u6e2f\u8ba1\u5212\uff0c\u9075\u5faa\u5176\u8ba4\u8bc1\u4e0e\u5e74\u5ea6\u5ba1\u8ba1\u8981\u6c42\u3002"},
    {"id": "age_screening", "name": "Age Screening / Age-Gating", "ref": "\u00a7312.2", "category": "A. \u9002\u7528\u6027",
     "desc": "Do you screen for age or age-gate to identify and protect child users?", "recommendation": "\u5bf9\u7591\u4f3c\u672a\u6210\u5e74\u7528\u6237\u505a\u5e74\u9f84\u5206\u6d41\uff0c\u907f\u514d\u5411\u513f\u7ae5\u63a8\u9001\u6210\u4eba\u5185\u5bb9\u3002"},
    {"id": "material_change", "name": "Notice of Material Change", "ref": "\u00a7312.4(a)(4)", "category": "B. \u5bb6\u957f\u540c\u610f",
     "desc": "Do you notify parents of material changes to PI collection/use practices?", "recommendation": "\u53d8\u66f4\u524d\u91cd\u65b0\u53d6\u5f97\u540c\u610f\u6216\u663e\u8457\u901a\u77e5\u3002"},
    {"id": "internal_compliance", "name": "Internal Compliance Program", "ref": "\u00a7312.9", "category": "G. \u5408\u89c4\u8ba1\u5212",
     "desc": "Do you maintain internal compliance (designated contact, workforce training)?", "recommendation": "\u6307\u5b9a COPPA \u5408\u89c4\u8d1f\u8d23\u4eba\u5e76\u5bf9\u56e2\u961f\u57f9\u8bad\u3002"},
]


def collect_responses(items):
    responses = []
    total = len(items)
    print(f"\n📋 COPPA Compliance Check — {total} items")
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
    lines = ["=" * 60, f"  COPPA Compliance Check Report (cloud-scored)" if not s.get("scored_locally") else f"  COPPA Compliance Check Report (local fallback score)",
             f"  Law: Children's Online Privacy Protection Act (COPPA), 15 U.S.C. §6501 et seq. and the COPPA Rule (16 C.F.R. Part 312)", f"  Engine version: {s.get('version', '?')}",
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
<html lang="en"><head><meta charset="UTF-8"><title>COPPA Compliance Check Report</title>
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
<h1>COPPA Compliance Check Report</h1>
<p>Law: Children's Online Privacy Protection Act (COPPA), 15 U.S.C. §6501 et seq. and the COPPA Rule (16 C.F.R. Part 312)</p>
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
    parser = argparse.ArgumentParser(description="COPPA Compliance Check (free skill + cloud engine)")
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
