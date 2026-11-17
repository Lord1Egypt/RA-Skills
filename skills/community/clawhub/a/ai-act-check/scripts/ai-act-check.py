#!/usr/bin/env python3
"""
EU AI Act Check — 欧盟《人工智能法案》合规检查（免费 skill + 云端合规引擎）

基于 Regulation (EU) 2024/1689（Artificial Intelligence Act，2024 年 8 月 1 日
生效、2026 年 8 月起大规模适用），覆盖 4 大维度、12 项核心检查：高风险 AI 系统
核心要求（风险管理/数据治理/透明度/人工监督/准确性与网络安全）、文档与质量管理
体系、提供者义务（合格评定/提供者全面义务）、透明度与通用目的模型义务（含深度伪造
与 AI 生成内容披露）。

本 skill 免费安装。检查项由 CQDev 云端合规引擎（compliancehub.cn）提供；
评分与额度在云端计算。首次使用请先在 compliancehub.cn 获取免费 API Key
（100 次免费调用）：
  - 打开：https://compliancehub.cn/account.html?skill=ai-act-check
  - 然后通过环境变量提供 Key：export COMPLIANCEHUB_API_KEY=<your-key>
    或保存到：~/.config/compliancehub/ai-act-check.key（mode 0600）

流程：
  1. 加载 API Key（环境变量 COMPLIANCEHUB_API_KEY，或 ~/.config/compliancehub/ai-act-check.key）
  2. 从云端规则库 API 拉取检查项（公开只读，单一事实来源）
  3. 交互式逐项收集合规状态（y=通过 / n=未通过 / na=不适用）
  4. 提交到云端 evaluate 端点，云端评分并返回报告数据
  5. 本地渲染专业报告（含风险等级、证据样例、整改建议与关联执法案例）

没有 API Key？skill 会自动进入匿名试用模式：本地生成随机 anon_id，
每 skill 可获得 5 次真实云端评分（7 天窗口）。额度用尽后引导一键注册，
并携带 anon_id 保证进度不丢失。

仅使用 Python 内置 urllib，零第三方依赖。Key 走 HTTPS + Bearer 传输；
无硬编码、无隐蔽外传。网络访问仅发生在评分运行时：（a）从固定端点拉取
公开检查项规则库（只读，不发送任何作答）；（b）将你的作答与 API Key
（作为 Bearer token）发送到固定 evaluate 端点。--non-interactive /
--non-interactive-json 免费预览完全离线，使用内置 CHECK_ITEMS，绝不联网。
不收集任何凭据；注册在网站（compliancehub.cn/account.html）完成，不在终端。
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
CASES_REF_URL = f"{API_BASE}/api/v1/cases/references/{{ref}}"     # public read: enforcement cases by regulation ref
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
    """Fetch pipl-check items from the cloud rule library (public, no Key needed).

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
    {"id": "risk_management", "name": "Risk Management System (Art. 9)", "desc": "Do you maintain a continuous risk-management system covering the whole lifecycle of your AI system (identifying known and foreseeable risks and applying mitigations)?", "ref": "Art. 9", "category": "A. 高风险 AI 系统核心要求（Art. 9–15）", "recommendation": "建立覆盖设计、开发、部署、运维全生命周期的风险登记与缓解流程，并定期复审。", "severity": "high"},
    {"id": "data_governance", "name": "Data and Data Governance (Art. 10)", "desc": "Do your training, validation and testing datasets meet data-governance requirements (relevance, representativeness, absence of errors, completeness, and bias examination)?", "ref": "Art. 10", "category": "A. 高风险 AI 系统核心要求（Art. 9–15）", "recommendation": "对训练/验证/测试数据进行数据治理审查，处理代表性不足与偏差，记录数据来源与质量评估。", "severity": "critical"},
    {"id": "transparency_deployers", "name": "Transparency and Provision of Information (Art. 13)", "desc": "Do you provide deployers with sufficient transparency information (capabilities, limitations, intended purpose) so they can understand and use the system appropriately?", "ref": "Art. 13", "category": "A. 高风险 AI 系统核心要求（Art. 9–15）", "recommendation": "向部署者提供清晰的能力与局限说明、预期用途与已知约束，便于其正确使用系统。", "severity": "high"},
    {"id": "human_oversight", "name": "Human Oversight (Art. 14)", "desc": "Is your AI system designed to allow effective human oversight, with measures to prevent or minimize risks from automated decisions?", "ref": "Art. 14", "category": "A. 高风险 AI 系统核心要求（Art. 9–15）", "recommendation": "设计可被人有效监督的机制（人工干预入口、中止开关、异常告警），避免完全自动化带来损害。", "severity": "high"},
    {"id": "accuracy_robustness", "name": "Accuracy, Robustness & Cybersecurity (Art. 15)", "desc": "Do you achieve an appropriate level of accuracy, robustness and cybersecurity for your AI system, maintained throughout its lifecycle?", "ref": "Art. 15", "category": "A. 高风险 AI 系统核心要求（Art. 9–15）", "recommendation": "设定准确性指标、做鲁棒性/对抗性测试，并实施网络安全控制与漏洞响应流程。", "severity": "high"},
    {"id": "technical_docs", "name": "Technical Documentation (Art. 11)", "desc": "Have you drawn up and maintained technical documentation demonstrating compliance with the AI Act requirements before the system is placed on the market?", "ref": "Art. 11", "category": "B. 文档与质量管理体系（Art. 11–12, 16）", "recommendation": "编制并持续维护技术文档（设计、开发、性能、合规评估），供主管机关评估。", "severity": "medium"},
    {"id": "record_keeping", "name": "Record-Keeping / Logging (Art. 12)", "desc": "Does your high-risk AI system automatically generate event logs that are traceable and preserved for reproducibility and incident investigation?", "ref": "Art. 12", "category": "B. 文档与质量管理体系（Art. 11–12, 16）", "recommendation": "启用可溯源的自动日志，保证在系统生命周期内可检索、可复现，用于事件排查。", "severity": "medium"},
    {"id": "quality_mgmt", "name": "Quality Management System (Art. 16)", "desc": "Have you established a quality-management system covering the compliance program (design, documentation, change management) for your AI system?", "ref": "Art. 16", "category": "B. 文档与质量管理体系（Art. 11–12, 16）", "recommendation": "建立覆盖合规程序的质量管理体系，明确职责、流程、变更管理与文档控制。", "severity": "medium"},
    {"id": "conformity", "name": "Conformity Assessment & CE Marking (Art. 22)", "desc": "Have you completed the conformity assessment, affixed the CE marking, and registered the high-risk AI system as required?", "ref": "Art. 22", "category": "C. 提供者义务（Art. 22, 26）", "recommendation": "完成合格评定、加贴 CE 标志、在欧盟数据库登记并保存技术文档与日志。", "severity": "high"},
    {"id": "provider_obligations", "name": "Obligations of Providers & Manufacturers (Art. 26)", "desc": "As a provider (or a manufacturer integrating AI into a product/system), do you fulfil all provider compliance obligations under the AI Act?", "ref": "Art. 26", "category": "C. 提供者义务（Art. 22, 26）", "recommendation": "落实提供者的全面合规义务：质量管理体系、技术文档、合格评定、登记、上市后监测与透明度。", "severity": "critical"},
    {"id": "transparency_systems", "name": "Transparency Obligations for Certain AI Systems (Art. 50)", "desc": "For systems that generate synthetic audio/image/video/text, deepfakes, or interact with humans, do you meet the explicit transparency disclosure obligations?", "ref": "Art. 50", "category": "D. 透明度与通用模型义务（Art. 25, 50）", "recommendation": "对合成内容/深度伪造/与人交互的系统履行明确告知义务，标注内容为 AI 生成并避免误导。", "severity": "critical"},
    {"id": "gpai_obligations", "name": "General-Purpose AI Model Obligations (Art. 25)", "desc": "If you provide a general-purpose AI (GPAI) model, do you meet the obligations: technical documentation, training-data summary, copyright policy and systemic-risk evaluation?", "ref": "Art. 25", "category": "D. 透明度与通用模型义务（Art. 25, 50）", "recommendation": "编制技术文档、提供训练数据摘要、落实版权合规政策，并对系统性风险模型做额外评估。", "severity": "high"},
]


# ─── Interactive collection ──────────────────────────────────────

def collect_responses(items):
    """Collect per-item compliance status interactively (y=pass / n=fail / na=n/a)."""
    responses = []
    total = len(items)
    print(f"\n📋 EU AI Act Compliance Check — {total} items")
    print("   请逐项输入实际状态（y=通过 / n=未通过 / na=不适用）\n")
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


# ─── Enforcement case enrichment ────────────────────────────────

def _collect_case_refs(payload):
    """Collect all related_case_keys from an evaluate response's items."""
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    refs = set()
    for it in (data.get("items") or []):
        for rk in ((it.get("meta") or {}).get("related_case_keys") or []):
            if rk:
                refs.add(rk)
    return sorted(refs)


def fetch_cases_for_refs(refs):
    """Fetch enforcement-case summaries for a set of regulation refs.

    Returns {ref: [summary_line, ...]}. Each line is short and human-readable
    (title + regulator + penalty). Best-effort: any network/parse failure for a
    single ref is swallowed so the report still renders — it degrades gracefully
    and never blocks scoring output. The endpoint is public/read-only (no Key
    needed), same trust model as fetch_rules.
    """
    out = {}
    if not refs:
        return out
    ctx = ssl.create_default_context()
    for ref in refs:
        try:
            url = CASES_REF_URL.format(ref=urllib.parse.quote(ref))
            req = urllib.request.Request(url, headers={"User-Agent": _ua()})
            with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
                if resp.status != 200:
                    continue
                payload = json.loads(resp.read().decode("utf-8"))
            cases = (payload.get("data") or []) if isinstance(payload, dict) else []
            lines = []
            for c in cases[:3]:
                # The case `title` already carries the penalty and authority, so
                # it is used verbatim. (The /cases API returns title/jurisdiction/
                # penalty_amount/etc. but no free-text regulator field.)
                lines.append(c.get("title", ""))
            if lines:
                out[ref] = lines
        except Exception:
            continue
    return out


# ─── Report rendering ────────────────────────────────────────────

def render_text(data, items, cases_by_ref=None):
    s = data
    cases_by_ref = cases_by_ref or {}
    lines = [
        "=" * 60,
        "  EU AI Act Compliance Check Report (cloud-scored)",
        "  Law: Regulation (EU) 2024/1689 (Artificial Intelligence Act)",
        f"  Engine version: {s.get('version', '?')}",
        f"  Compliance score: {s.get('score')}/100",
        "=" * 60,
        f"  Overview: {s.get('total_items')} items counted | ✅ Pass {s.get('passed_count')} | ❌ Fail {s.get('failed_count')} | Free quota left {s.get('quota_remaining')}",
        "=" * 60,
    ]
    sev_label = {"critical": "🔴 严重", "high": "🟠 高", "medium": "🟡 中", "low": "🟢 低"}
    current_cat = ""
    for r in items:
        if r.get("category") != current_cat:
            current_cat = r.get("category", "")
            lines.append(f"\n  ── {current_cat} ──")
        icon = "✅" if r.get("passed") else "❌"
        sev = r.get("severity") or ""
        sev_txt = f"  [风险等级：{sev_label.get(sev, sev)}]" if sev else ""
        lines.append(f"\n  {icon} [{r.get('item_key')}] {r.get('name')}{sev_txt}")
        lines.append(f"    Status: {'Pass' if r.get('passed') else 'Fail'}")
        if r.get("legal_ref"):
            lines.append(f"    Authority: {r.get('legal_ref')}")
        if not r.get("passed"):
            meta = r.get("meta") or {}
            rt = meta.get("remediation_template")
            if rt:
                lines.append(f"    🔧 整改建议: {rt.get('summary', '')}")
                for step in (rt.get("steps") or [])[:3]:
                    lines.append(f"       · {step}")
            lt = meta.get("legal_text")
            if lt and lt.get("snippet"):
                lines.append(f"    📜 法条依据: {lt.get('snippet', '')}")
        if r.get("recommendation"):
            lines.append(f"    Recommendation: {r.get('recommendation')}")
        case_keys = (r.get("meta") or {}).get("related_case_keys") or []
        if case_keys and cases_by_ref:
            shown = 0
            block = []
            for ck in case_keys:
                for line in cases_by_ref.get(ck, []):
                    block.append(f"       · {line}")
                    shown += 1
                    if shown >= 3:
                        break
                if shown >= 3:
                    break
            if block:
                lines.append("    📚 关联执法案例:")
                lines.extend(block)
    lines.append("=" * 60)
    lines.append("\n💡 Disclaimer: This report is generated by the CQDev cloud compliance engine for reference only and does not constitute legal advice.")
    return "\n".join(lines)


def render_html(data, items, cases_by_ref=None):
    s = data
    cases_by_ref = cases_by_ref or {}
    score = s.get("score", 0)
    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 60 else "#f44336"
    rows = ""
    sev_cls = {"critical": "#dc2626", "high": "#ea580c", "medium": "#ca8a04", "low": "#16a34a"}
    sev_label = {"critical": "严重", "high": "高", "medium": "中", "low": "低"}
    current_cat = ""
    for r in items:
        if r.get("category") != current_cat:
            current_cat = r.get("category", "")
            rows += f'<tr class="category-row"><td colspan="6">{current_cat}</td></tr>\n'
        icon = "✅" if r.get("passed") else "❌"
        cls = "pass" if r.get("passed") else "fail"
        sev = r.get("severity") or ""
        sev_badge = ""
        if sev:
            color = sev_cls.get(sev, "#64748b")
            sev_badge = f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:10px;font-size:.75rem">{sev_label.get(sev, sev)}</span>'
        rec = r.get("recommendation") or "Keep it up"
        meta = r.get("meta") or {}
        rt = meta.get("remediation_template")
        if not r.get("passed") and rt:
            rec = f"🔧 {rt.get('summary', '')}（整改期限约 {rt.get('deadline_days', '')} 天）"
        case_html = ""
        case_keys = (r.get("meta") or {}).get("related_case_keys") or []
        if case_keys and cases_by_ref:
            shown = 0
            li = []
            for ck in case_keys:
                for line in cases_by_ref.get(ck, []):
                    li.append(f"<li>{line}</li>")
                    shown += 1
                    if shown >= 3:
                        break
                if shown >= 3:
                    break
            if li:
                case_html = f'<div class="cases"><b>📚 关联执法案例</b><ul>{"".join(li)}</ul></div>'
        rows += f"""<tr class="{cls}"><td>{icon}</td><td>{r.get('name')}</td><td>{r.get('legal_ref') or ''}</td><td>{sev_badge}</td><td>{cls.upper()}</td><td>{rec}{case_html}</td></tr>\n"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>EU AI Act 合规检查报告</title>
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
.cases{{margin-top:4px;font-size:.8rem;color:#475569}}
.cases ul{{margin:2px 0 0;padding-left:16px}}
.cases li{{margin:1px 0}}
.note{{color:#94a3b8;margin-top:2rem;font-size:.85rem}}
</style></head>
<body>
<h1>EU AI Act 合规检查报告</h1>
<p>Law: Regulation (EU) 2024/1689 (Artificial Intelligence Act)</p>
<p>Engine version: {s.get('version','?')} ｜ Free quota left: {s.get('quota_remaining')}</p>
<div class="score-card"><div class="score">{score}</div><div>合规评分 / 100</div>
<div class="summary"><div>✅ 通过<br><b>{s.get('passed_count')}</b></div><div>❌ 未通过<br><b>{s.get('failed_count')}</b></div><div>检查项<br><b>{s.get('total_items')}</b></div></div></div>
<table><thead><tr><th></th><th>检查项</th><th>法条</th><th>风险等级</th><th>状态</th><th>整改建议</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">本报告由 CQDev 云端合规引擎生成，仅供参考，不构成法律意见。</p>
</body></html>"""


def generate_report(payload, format="text", cases_by_ref=None):
    """Render report from cloud response. payload is the full evaluate JSON."""
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    items = data.get("items", [])
    if format == "json":
        return json.dumps(payload, ensure_ascii=False, indent=2)
    elif format == "html":
        return render_html(data, items, cases_by_ref=cases_by_ref)
    return render_text(data, items, cases_by_ref=cases_by_ref)


# ─── Main entry ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="EU AI Act compliance check (free skill + cloud engine)")
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

    report = generate_report(payload, format=args.format, cases_by_ref=fetch_cases_for_refs(_collect_case_refs(payload)))
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
