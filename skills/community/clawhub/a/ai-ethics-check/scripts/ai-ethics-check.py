#!/usr/bin/env python3
"""
AI 科技伦理审查合规检查 — 《人工智能科技伦理审查与服务办法(试行)》（工信部等十部门，工信部联科〔2026〕75号，2026-03-20 施行）

Free skill + complianceHub engine (compliancehub.cn).
Scoring and quota are computed in the cloud; before first use, register for a
free API Key (100 free calls) on the web:

  Open: https://compliancehub.cn/account.html?skill=ai-ethics-check
  Then provide the Key via env COMPLIANCEHUB_API_KEY, or save it to
  ~/.config/compliancehub/ai-ethics-check.key (mode 0600).

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


def _skill_slug():
    """Resolve the skill slug from package.json `name` — NOT from the install
    directory name, which may carry suffixes like `-upload` and would make the
    cloud rule-library URL wrong (404 → the cloud scoring could never be used)."""
    pkg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "package.json")
    try:
        if os.path.isfile(pkg):
            with open(pkg, encoding="utf-8") as f:
                return json.load(f).get("name", "ai-ethics-check")
    except Exception:
        pass
    return "ai-ethics-check"


SKILL_SLUG = _skill_slug()
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
  {
    "id": "ethics_committee",
    "name": "设立科技伦理委员会",
    "ref": "办法§9",
    "category": "A. 委员会",
    "desc": "从事 AI 科技活动是否设立人工智能科技伦理委员会并配备必要资源？",
    "recommendation": "设立独立履职的科技伦理委员会，明确章程与职责。"
  },
  {
    "id": "committee_independent",
    "name": "委员会独立履职",
    "ref": "办法§9",
    "category": "A. 委员会",
    "desc": "伦理委员会是否独立开展审查，不受项目利益相关方不当影响？",
    "recommendation": "保障委员会独立性与回避机制，留存履职记录。"
  },
  {
    "id": "review_apply",
    "name": "活动前申请伦理审查",
    "ref": "办法§12",
    "category": "B. 审查程序",
    "desc": "开展 AI 科技活动前是否按规定申请伦理审查？",
    "recommendation": "在活动启动前提交伦理审查申请，未通过不开展。"
  },
  {
    "id": "review_timeliness",
    "name": "审查决定时限合规",
    "ref": "办法§16",
    "category": "B. 审查程序",
    "desc": "一般程序是否在30日内取得伦理审查决定？应急程序是否依规快速处理？",
    "recommendation": "按程序在法定期限内完成审查，记录决定与时限。"
  },
  {
    "id": "review_focus_fair",
    "name": "审查重点：公平公正",
    "ref": "办法§15",
    "category": "C. 审查重点",
    "desc": "是否就防偏见歧视、防止算法压榨等公平公正要求开展审查？",
    "recommendation": "将公平性纳入审查清单，评估偏见与歧视风险。"
  },
  {
    "id": "review_focus_controllable",
    "name": "审查重点：可控可信可解释",
    "ref": "办法§15",
    "category": "C. 审查重点",
    "desc": "是否审查可控可信、透明可解释、责任可追溯、隐私保护等要点？",
    "recommendation": "评估系统可解释性与责任追溯机制，留存证据。"
  },
  {
    "id": "expert_humanmachine",
    "name": "人机融合系统专家复核",
    "ref": "办法§21-25+附件",
    "category": "D. 专家复核",
    "desc": "研发对人类主观行为/心理情绪/生命健康有较强影响的人机融合系统，是否经初审+专家复核？",
    "recommendation": "列入清单的高风险活动须经专家复核通过后方可开展。"
  },
  {
    "id": "expert_mobilization",
    "name": "舆论动员算法专家复核",
    "ref": "办法附件",
    "category": "D. 专家复核",
    "desc": "研发具有舆论社会动员/意识引导能力的算法模型，是否经专家复核？",
    "recommendation": "舆论动员类算法纳入专家复核清单并严格执行。"
  },
  {
    "id": "expert_auto_decision",
    "name": "高风险自动化决策专家复核",
    "ref": "办法附件",
    "category": "D. 专家复核",
    "desc": "面向安全/人身健康风险场景的高度自主自动化决策系统，是否经专家复核？",
    "recommendation": "高风险自动化决策系统须专家复核并保持人类监督。"
  },
  {
    "id": "registry_tracking",
    "name": "登记与跟踪审查",
    "ref": "办法§19/§30",
    "category": "E. 登记跟踪",
    "desc": "是否在科技伦理管理信息登记平台登记？跟踪审查是否≤12个月、清单内≤6个月？",
    "recommendation": "完成平台登记，按周期开展跟踪审查并留存记录。"
  }
]


def collect_responses(items):
    """Collect y/n/na answers. All prompts go to stderr so that --format json
    keeps stdout clean for machine consumption."""
    responses = []
    total = len(items)
    print(f"\n📋 AI 科技伦理审查合规检查 — {total} 项", file=sys.stderr)
    print("   逐项回答实际合规状态（y=达标 / n=不达标 / na=不适用）\n", file=sys.stderr)
    for i, item in enumerate(items):
        idx = i + 1
        while True:
            sys.stderr.write(f"  [{idx}/{total}] {item['name']} [{item['ref']}]\n"
                             f"        {item['desc']}\n"
                             f"        (y/n/na) > ")
            ans = input().strip().lower()
            if ans in ('y', 'n', 'na'):
                if ans == 'na':
                    responses.append({**item, "status": "na"})
                else:
                    responses.append({**item, "status": "pass" if ans == 'y' else "fail"})
                break
            print("        请输入 y、n 或 na", file=sys.stderr)
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
        # 500 / 502 / 503 等：云端规则库尚未部署或临时不可用 —— 回退本地兜底评分，
        # 保证 skill 在未接入后端时仍可离线产出报告。
        if e.code >= 500:
            return None, "CLOUD_UNAVAILABLE"
        return None, f"cloud error HTTP {e.code}: {detail}"
    except Exception as e:
        return None, "CLOUD_UNAVAILABLE"


def _score_block(data):
    return (f"  合规得分：{data.get('score')}/100\n"
            f"  ✅ 达标 {data.get('passed_count')} ｜ ❌ 不达标 {data.get('failed_count')} ｜ 共 {data.get('total_items')} 项")


def render_text(data, items):
    s = data
    lines = ["=" * 60, "  AI 科技伦理审查合规检查报告 (云端评分)" if not s.get("scored_locally") else "  AI 科技伦理审查合规检查报告 (本地兜底评分)",
             f"  法规：《人工智能科技伦理审查与服务办法(试行)》（工信部等十部门，工信部联科〔2026〕75号，2026-03-20 施行）", f"  引擎版本：{s.get('version', '?')}",
             _score_block(s), "=" * 60]
    current_cat = ""
    for r in items:
        if r.get("category_name") != current_cat:
            current_cat = r.get("category_name", "")
            lines.append(f"\n  ── {current_cat} ──")
        icon = "✅" if r.get("passed") else "❌"
        lines.append(f"\n  {icon} [{r.get('item_key')}] {r.get('name')}")
        if r.get("legal_ref"):
            lines.append(f"    依据：{r.get('legal_ref')}")
        if r.get("recommendation"):
            lines.append(f"    建议：{r.get('recommendation')}")
    lines.append("=" * 60)
    lines.append("\n💡 免责声明：本报告基于你提交的自报信息生成，非监管/审计结论，仅供参考，不构成法律建议。")
    lines.append("   本报告由程序自动生成。")
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
        rec = r.get("recommendation") or "继续保持"
        rows += f"""<tr class="{cls}"><td>{icon}</td><td>{r.get('name')}</td><td>{r.get('legal_ref') or ''}</td><td>{cls.upper()}</td><td>{rec}</td></tr>\n"""
    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8"><title>AI 科技伦理审查合规检查报告</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#333}}
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
<h1>AI 科技伦理审查合规检查报告</h1>
<p>法规：《人工智能科技伦理审查与服务办法(试行)》（工信部等十部门，工信部联科〔2026〕75号，2026-03-20 施行）</p>
<p>引擎版本：{s.get('version','?')}{' ｜ 本地兜底评分（云端规则库尚未开放）' if s.get('scored_locally') else ''}</p>
<div class="score-card"><div class="score">{score}</div><div>合规得分 / 100</div>
<div class="summary"><div>✅ 达标<br><b>{s.get('passed_count')}</b></div><div>❌ 不达标<br><b>{s.get('failed_count')}</b></div><div>共<br><b>{s.get('total_items')}</b></div></div></div>
<table><thead><tr><th></th><th>检查项</th><th>依据</th><th>状态</th><th>建议</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">本报告基于你提交的自报信息生成，非监管/审计结论；由 complianceHub 云端合规引擎自动生成，仅供参考，不构成法律建议。</p>
</body></html>"""


def generate_report(payload, format="text"):
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    items = data.get("items", [])
    if format == "json":
        payload = dict(payload)
        payload["disclaimer"] = "本报告基于你提交的自报信息生成，非监管/审计结论，仅供参考，不构成法律建议；由程序自动生成。"
        return json.dumps(payload, ensure_ascii=False, indent=2)
    elif format == "html":
        return render_html(data, items)
    return render_text(data, items)


def main():
    parser = argparse.ArgumentParser(description="AI 科技伦理审查合规检查 (free skill + cloud engine)")
    parser.add_argument("--non-interactive", action="store_true", help="免费预览模式（列出检查项，不评分）")
    parser.add_argument("--non-interactive-json", action="store_true", help="免费预览 JSON 模式")
    parser.add_argument("--format", "-f", choices=["text", "json", "html"], default="text")
    parser.add_argument("--output", "-o", help="报告输出文件路径")
    args = parser.parse_args()

    if args.non_interactive_json:
        # 预览模式：纯本地内置检查项，完全离线，不发起任何网络请求
        items = CHECK_ITEMS
        preview_data = [{"id": it["id"], "name": it["name"], "desc": it["desc"], "ref": it["ref"], "category": it["category"]} for it in items]
        print(json.dumps({"preview": True, "total_items": len(items), "free": True, "needs_api_key": True,
                          "register_page": ACCOUNT_PAGE, "message": "免费 skill；评分运行于 complianceHub 云端引擎（免费 API Key）。",
                          "preview_items": preview_data}, ensure_ascii=False, indent=2))
        return

    if args.non_interactive:
        # 预览模式：纯本地内置检查项，完全离线
        items = CHECK_ITEMS
        print(f"\n🔍 免费预览模式 — {len(items)} 项；评分需免费 API Key\n")
        current_cat = ""
        for it in items:
            if it.get("category") != current_cat:
                current_cat = it.get("category", "")
                print(f"\n  ── {current_cat} ──")
            print(f"  • [{it['id']}] {it['name']}  [{it['ref']}]")
            print(f"      {it['desc']}")
        print(f"\n💡 评分运行于云端引擎。获取免费 API Key：{ACCOUNT_PAGE}")
        return

    # 评分模式：拉取云端最新检查项（单一数据源）；云端不可用时回退本地内置
    items = fetch_rules() or CHECK_ITEMS

    key = load_api_key()
    anon_id = None
    if not key:
        anon_id = load_or_create_anon_id()
        print("🔒 匿名试用模式：本检查将通过 compliancehub.cn 云端引擎真实评分，无需注册可免费试 5 次。", file=sys.stderr)
        print("   你的作答将发送到 compliancehub.cn 云端引擎进行评分，用于生成本次合规报告；详细数据处理见隐私政策 https://compliancehub.cn/privacy.html", file=sys.stderr)
    responses = collect_responses(items)
    submission = build_submission(responses)
    if not submission:
        print("❌ 无可统计项（全部标记为不适用）。", file=sys.stderr)
        sys.exit(1)

    print("\n⏳ 正在提交至云端合规引擎评分……", file=sys.stderr)
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
    elif err in ("RULE_LIB_NOT_OPEN", "CLOUD_UNAVAILABLE"):
        print("⚠️ 云端规则库暂不可用 —— 使用本地兜底评分（相同题目，本地计算）。", file=sys.stderr)
        data = compute_local_score(submission, items)
        payload = {"data": data}
    elif err:
        print(f"❌ {err}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(payload, format=args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已保存至：{args.output}", file=sys.stderr)
    else:
        print(report)
    data_out = payload.get("data") or {}
    if anon_id:
        tl = data_out.get("trials_left")
        if tl is not None:
            print(f"\n💡 匿名试用剩余次数：{tl}/5（注册后每把 Key 含 100 次免费额度）。", file=sys.stderr)
    else:
        rem = data_out.get("quota_remaining")
        if rem is not None:
            print(f"\n💡 本 Key 剩余免费额度：{rem} 次。", file=sys.stderr)


if __name__ == "__main__":
    main()
