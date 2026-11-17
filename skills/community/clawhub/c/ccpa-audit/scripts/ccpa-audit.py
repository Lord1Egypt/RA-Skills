#!/usr/bin/env python3
"""
CCPA Compliance Audit — California Consumer Privacy Act (CCPA, Cal. Civ. Code §1798.100 et seq.) & CPRA amendment

Free skill + CQDev cloud compliance engine (compliancehub.cn).
Scoring and quota are computed in the cloud; before first use, get a free API
Key (100 free calls) at the web account center. Registration is browser-only
because it includes a human/captcha check the terminal cannot perform:
  - Open: https://compliancehub.cn/account.html?skill=ccpa-audit
  - Then hand the Key to this skill via COMPLIANCEHUB_API_KEY or a key file

Flow:
  1. Load API Key (env COMPLIANCEHUB_API_KEY, or ~/.config/compliancehub/<slug>.key)
  2. Fetch check items from the cloud rule-library API (public read)
  3. Collect per-item compliance status (y=pass / n=fail / na=n/a)
  4. Submit to the cloud evaluate endpoint (auth) for cloud scoring
  5. Render a professional report locally

No API Key yet? The skill runs in anonymous trial mode automatically: a local
random anon_id is issued, and you get up to 5 real cloud-scored evaluations per
skill (7-day window). When the trial runs out the skill points you to the
one-click registration page, carrying your anon_id so nothing is lost.


Local persistence: the only file written to disk is a random anon_id at
~/.config/compliancehub/<slug>.anon_id (mode 0600) for the anonymous trial — your answers
are never stored locally and nothing else persists.

Uses only Python built-in urllib — zero third-party dependencies. HTTPS + Bearer
transport for the key; no hardcoding, no covert exfiltration. Outbound network calls are:
(a) fetching the public check-item rule library from the pinned endpoint before any preview/scored
run (read-only, NO answers sent); (b) your scored answers + the API Key (as a Bearer token)
to the pinned evaluate endpoint. The API Key is obtained from the web account center and
supplied via the COMPLIANCEHUB_API_KEY environment variable or ~/.config/compliancehub/<slug>.key;
this skill never collects your email/password or creates accounts. No other data leaves the machine.

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
    return "2.0.1"


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
    """Registration funnel URL carrying the anon_id so the account page can
    keep the visitor's trial context and make registering one-click."""
    url = ACCOUNT_PAGE
    if anon_id:
        url += "&anon_id=" + urllib.parse.quote(anon_id)
    return url


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


# NOTE: account registration is handled by the web account center
# (https://compliancehub.cn/account.html). This skill only CONSUMES an API Key
# via COMPLIANCEHUB_API_KEY or ~/.config/compliancehub/<slug>.key — it never
# registers accounts or collects credentials in the terminal.


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
    {"id": "right_to_know", "name": "知情权", "desc": "是否支持消费者知晓所收集 PI 的类别与来源/目的？", "ref": "CCPA §1798.100", "category": "A. 消费者权利", "recommendation": "对照法规要求落实并保持证据。", "severity": "high"},
    {"id": "right_to_delete", "name": "删除权", "desc": "是否提供可执行的删除请求通道？", "ref": "CCPA §1798.105", "category": "A. 消费者权利", "recommendation": "对照法规要求落实并保持证据。", "severity": "high"},
    {"id": "right_to_optout", "name": "选择退出权", "desc": "选择退出是否真实生效：提供 Do Not Sell/Share 入口、尊重 GPC，且技术实现确实停止向第三方追踪器出售/共享（opt-out 不要求身份验证）？", "ref": "CCPA §1798.120", "category": "A. 消费者权利", "recommendation": "定期验证 opt-out 技术链路真实停止 sale/share（含第三方标签/追踪器）；部署 GPC 信号识别；opt-out 不得要求登录或身份验证。", "severity": "critical"},
    {"id": "non_discrimination", "name": "非歧视原则", "desc": "是否不因行使权利而歧视消费者？", "ref": "CCPA §1798.125", "category": "A. 消费者权利", "recommendation": "对照法规要求落实并保持证据。", "severity": "high"},
    {"id": "right_to_correct", "name": "更正权", "desc": "是否支持更正不准确 PI？", "ref": "CPRA §1798.106", "category": "A. 消费者权利", "recommendation": "对照法规要求落实并保持证据。", "severity": "high"},
    {"id": "request_verification", "name": "请求验证", "desc": "权利请求的身份核验是否相称：按风险分级、不要求过度信息、不为 opt-out 设置验证障碍、授权代理人可代行？", "ref": "CCPA §1798.145(i)", "category": "A. 消费者权利", "recommendation": "按请求类型分级核验（高风险加强、常规从轻）；opt-out 一律不要求验证；接受授权代理人并核验其授权文件。", "severity": "high"},
    {"id": "authorized_agent", "name": "授权代理人", "desc": "是否接受消费者授权代理人（含注册代理）提出的权利请求，且核验不造成不当负担？", "ref": "CCPA §1798.130(a)(2)", "category": "A. 消费者权利", "recommendation": "明确授权代理人受理流程；允许消费者提供签名授权或注册代理身份；不得要求超出直接请求的额外验证。", "severity": "medium"},
    {"id": "notice_at_collection", "name": "收集通知", "desc": "收集时是否披露类别与目的？", "ref": "CCPA §1798.100(b)", "category": "B. 告知义务", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "pi_categories", "name": "个人信息类别", "desc": "是否完整列示所处理 PI 类别？", "ref": "CCPA §1798.140", "category": "B. 告知义务", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "privacy_policy", "name": "隐私政策", "desc": "隐私政策是否年度更新并列明权利？", "ref": "CCPA §1798.130", "category": "B. 告知义务", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "annual_disclosure", "name": "年度披露", "desc": "是否向员工披露收集的 PI 类别？", "ref": "CCPA §1798.130(a)(5)", "category": "B. 告知义务", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "data_minimization", "name": "数据最小化", "desc": "是否在目的必要范围内收集合规？", "ref": "CPRA §1798.100(b)", "category": "C. 处理原则", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "sensitive_pi", "name": "敏感个人信息(CPRA)", "desc": "敏感 PI（含扩展类别：公民身份/移民状态 AB947、神经数据 SB1223、AI 衍生数据 AB1008）是否限定用途并提供限制权（Limit My Sensitive PI）？", "ref": "CPRA §1798.140(ae)", "category": "C. 处理原则", "recommendation": "盘点全部敏感 PI 类别（含新增）；限定用途为必要目的；提供敏感 PI 限制使用开关并真实生效。", "severity": "high"},
    {"id": "limit_sensitive_use", "name": "限制敏感PI使用", "desc": "是否提供限制敏感 PI 使用的选项？", "ref": "CPRA §1798.121", "category": "C. 处理原则", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "retention_period", "name": "留存期限", "desc": "是否设定 PI 留存期限并到期删除？", "ref": "CPRA §1798.100(a)(3)", "category": "C. 处理原则", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "service_provider", "name": "服务提供商义务", "desc": "与服务提供商合同是否禁止二次使用？", "ref": "CCPA §1798.140(ag)", "category": "D. 第三方", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "third_party_sharing", "name": "第三方共享", "desc": "是否披露共享的第三方类别？", "ref": "CCPA §1798.115", "category": "D. 第三方", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "audit_rights", "name": "合同审计权", "desc": "服务提供商合同是否保留审计权？", "ref": "CCPA §1798.140(ag)(3)", "category": "D. 第三方", "recommendation": "对照法规要求落实并保持证据。", "severity": "medium"},
    {"id": "automated_decisions", "name": "自动化决策", "desc": "使用自动化决策技术（ADMT）做重大决策（录用/信贷/住房/福利等）前，是否提供 pre-use notice、opt-out 与申诉通道（CPPA 2025 ADMT 规则，2027.1.1 生效）？", "ref": "CPRA §1798.185(a)(16)", "category": "E. 问责", "recommendation": "盘点 ADMT 用例；对重大决策提供事前告知 + opt-out（含例外）+ 人工申诉通道；留存影响评估与记录。", "severity": "high"},
    {"id": "minors_data", "name": "未成年人数据", "desc": "是否对未成年人加严同意（含 opt-in）？", "ref": "CCPA §1798.120(c)", "category": "E. 问责", "recommendation": "对照法规要求落实并保持证据。", "severity": "high"},
    {"id": "dark_patterns", "name": "暗模式/选择对称性", "desc": "用户界面是否避免暗模式：cookie 横幅 accept/reject 按钮对称、退出入口与同意入口同等醒目、无误导性默认勾选？", "ref": "CCPA §1798.140(ad)", "category": "E. 问责", "recommendation": "对关键 UI 做暗模式自测（按钮对称性、退出可达性、语言误导、默认勾选）；建立设计评审与 A/B 测试。", "severity": "high"},
    {"id": "hr_data", "name": "员工/求职者数据", "desc": "是否向员工/求职者提供与消费者同等的 CCPA 权利与通知（加州 HR 数据受 CCPA 管辖）？", "ref": "CCPA §1798.100 (HR context)", "category": "E. 问责", "recommendation": "将 HR 数据纳入 CCPA 覆盖：求职者/员工通知、权利受理、opt-out（如 sale/share）、年度披露；纳入隐私审计范围。", "severity": "medium"},
    {"id": "security_obligation", "name": "安全义务", "desc": "是否采取合理安全措施并具备违约救济？", "ref": "CCPA §1798.150(a)(1)", "category": "F. 安全", "recommendation": "对照法规要求落实并保持证据。", "severity": "high"},
    {"id": "risk_assessment", "name": "高风险评估/网络安全审计（前瞻）", "desc": "是否开始为高风险数据处理的年度风险评估与网络安全审计做准备（CPPA 2025 规则，按营收分档 2028-2030 生效）？", "ref": "CPPA 2025 Rules (Risk Assessments / Cyber Audits)", "category": "F. 安全", "recommendation": "识别高风险处理场景；建立风险评估框架与文档存档；按营收档位规划网络安全审计（≥$1亿:2028.4.1 / $0.5-1亿:2029 / <$0.5亿:2030）。", "severity": "medium"},
]


def _normalize_answer(ans):
    """Accept both English and Chinese answers so Chinese-first users aren't stuck."""
    a = (ans or "").strip().lower()
    if a in ('y', 'yes', '是', '通过', '符合'):
        return 'pass'
    if a in ('n', 'no', '否', '不通过', '不符合'):
        return 'fail'
    if a in ('na', 'n/a', '不适用', '豁免'):
        return 'na'
    if a in ('?', 'h', '帮助', '建议'):
        return 'help'
    return None


def collect_responses(items):
    responses = []
    total = len(items)

    print(f"\n📋 CCPA Compliance Audit — 共 {total} 项")
    print("   逐项确认实际状态：y=通过 / n=不符合 / na=不适用；输入 ? 可看该项建议\n")

    for i in range(total):
        item = items[i]
        idx = i + 1
        if item.get('category') and (not responses or responses[-1].get('category') != item.get('category')):
            print(f"  ── {item.get('category')} ──")
        pct = round(idx / total * 100)
        while True:
            ans = input(f"  [{idx}/{total} · {pct}%] {item['name']} [{item['ref']}]\n"
                        f"        {item['desc']}\n"
                        f"        (y/n/na/?) > ").strip().lower()
            norm = _normalize_answer(ans)
            if norm == 'help':
                rec = item.get('recommendation') or '对照法规要求落实并保持证据。'
                print(f"        💡 建议：{rec}")
                continue
            if norm is None:
                print("        请输入 y / n / na 或 ?（也可用中文：是 / 否 / 不适用）")
                continue
            responses.append({**item, "status": norm})
            break

    passed = sum(1 for r in responses if r['status'] == 'pass')
    failed = sum(1 for r in responses if r['status'] == 'fail')
    na = sum(1 for r in responses if r['status'] == 'na')
    print(f"\n  ✅ 通过 {passed} ｜ ❌ 不符合 {failed} ｜ ⚪ 不适用 {na} ｜ 共 {total} 项")

    return responses


def build_submission(responses):
    items = []
    for r in responses:
        if r["status"] == "na":
            continue
        items.append({"item_key": r["id"], "passed": r["status"] == "pass", "evidence": None})
    return items


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
            return None, "API Key invalid; get a free Key at %s and set COMPLIANCEHUB_API_KEY" % ACCOUNT_PAGE
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


def _score_block(data):
    return (f"  Compliance score: {data.get('score')}/100\n"
            f"  ✅ Pass {data.get('passed_count')} | ❌ Fail {data.get('failed_count')} | Items {data.get('total_items')}")


def render_text(data, items):
    s = data
    lines = ["=" * 60, "  CCPA Compliance Audit Report (cloud-scored)",
             f"  Law: California Consumer Privacy Act (CCPA, Cal. Civ. Code §1798.100 et seq.) & CPRA amendment", f"  Engine version: {s.get('version', '?')}",
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
<html lang="en"><head><meta charset="UTF-8"><title>CCPA Compliance Audit Report</title>
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
<h1>CCPA Compliance Audit Report</h1>
<p>Law: California Consumer Privacy Act (CCPA, Cal. Civ. Code §1798.100 et seq.) & CPRA amendment</p>
<p>Engine version: {s.get('version','?')}</p>
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
    parser = argparse.ArgumentParser(description="CCPA Compliance Audit (free skill + cloud engine)")
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
        print("🔒 匿名试用模式：本审计将通过 compliancehub.cn 云端引擎真实评分，无需注册可免费试 5 次。")
        print("   你的作答将发送到 compliancehub.cn 云端引擎进行评分，用于生成本次审计报告；详细数据处理见隐私政策 https://compliancehub.cn/privacy.html")
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
    if err:
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
