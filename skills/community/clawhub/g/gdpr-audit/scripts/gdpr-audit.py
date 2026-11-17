#!/usr/bin/env python3
"""
GDPR Compliance Audit — General Data Protection Regulation (EU) 2016/679 (GDPR)

Free skill + CQDev cloud compliance engine (compliancehub.cn).
Scoring and quota are computed in the cloud; before first use, get a free API
Key (100 free calls) at the web account center. Registration is browser-only
because it includes a human/captcha check the terminal cannot perform:
  - Open: https://compliancehub.cn/account.html?skill=gdpr-audit
  - Then hand the Key to this skill via COMPLIANCEHUB_API_KEY or a key file

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
transport for the key; no hardcoding, no covert exfiltration. Outbound network calls are: (a) fetching the public check-item rule library from the pinned endpoint before any preview/scored run (read-only, NO answers sent); (b) your scored answers + the API Key (as a Bearer token) to the pinned evaluate endpoint. The API Key is obtained from the web account center and supplied via the COMPLIANCEHUB_API_KEY environment variable or ~/.config/compliancehub/<slug>.key; this skill never collects your email/password or creates accounts. No other data leaves the machine.
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


def require_key():
    key = load_api_key()
    if key:
        return key
    if sys.stdin.isatty():
        # Human at an interactive terminal: print friendly guidance, not raw JSON.
        print("\n🔑 生成评分报告需要一把免费的 API Key（每个 Key 含 100 次免费调用）。")
        print("   两步即可开通：")
        print(f"   1) 打开网页注册并领取 Key：{ACCOUNT_PAGE}")
        print("   2) 把 Key 交给本工具（任选其一）：")
        print("        export COMPLIANCEHUB_API_KEY=<网页显示的 Key>")
        print(f"        mkdir -p ~/.config/compliancehub && echo '<网页显示的 Key>' > ~/.config/compliancehub/{SKILL_SLUG}.key")
        print("   若只想先看题目、暂不评分，可运行："
              f"python3 scripts/{os.path.basename(__file__)} --non-interactive")
    else:
        # Non-interactive (agent / piped): keep machine-readable JSON for the caller.
        msg = {
            "error": "missing_api_key",
            "message": "This skill calls the CQDev cloud compliance engine and needs a free API Key.",
            "get_key_page": ACCOUNT_PAGE,
            "option_env": "export COMPLIANCEHUB_API_KEY=sk_live_xxx",
            "option_file": f"mkdir -p ~/.config/compliancehub && echo 'sk_live_xxx' > ~/.config/compliancehub/{SKILL_SLUG}.key",
        }
        print(json.dumps(msg, ensure_ascii=False, indent=2))
    sys.exit(2)


def _api_json(method, url, payload=None, token=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json", "User-Agent": _ua()}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "ignore"))
        except Exception:
            return e.code, {}
    except Exception:
        return 0, {}




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
    {"id": "scope_applicability", "name": "\u9002\u7528\u8303\u56f4", "ref": "Art. 3", "category": "A. \u9002\u7528\u8303\u56f4",
     "desc": "\u662f\u5426\u660e\u786e GDPR \u9002\u7528\u8fb9\u754c\u4e0e\u6240\u5904\u7406\u6570\u636e\u4e3b\u4f53\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "principles", "name": "\u5904\u7406\u539f\u5219", "ref": "Art. 5", "category": "B. \u57fa\u672c\u539f\u5219",
     "desc": "\u662f\u5426\u7b26\u5408\u5408\u6cd5\u3001\u516c\u5e73\u3001\u900f\u660e\u3001\u76ee\u7684\u9650\u5b9a\u3001\u6700\u5c0f\u5316\u7b49\u539f\u5219\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "legal_basis", "name": "\u5408\u6cd5\u4f9d\u636e", "ref": "Art. 6", "category": "C. \u5408\u6cd5\u6027",
     "desc": "\u5404\u5904\u7406\u6d3b\u52a8\u662f\u5426\u6620\u5c04\u5e76\u8bb0\u5f55\u5408\u6cd5\u4f9d\u636e\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "consent", "name": "\u540c\u610f", "ref": "Art. 7", "category": "C. \u5408\u6cd5\u6027",
     "desc": "\u540c\u610f\u662f\u5426\u6709\u6548\u3001\u53ef\u64a4\u56de\u3001\u7559\u75d5\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "special_categories", "name": "\u7279\u6b8a\u7c7b\u522b\u6570\u636e", "ref": "Art. 9", "category": "C. \u5408\u6cd5\u6027",
     "desc": "\u654f\u611f\u6570\u636e\u662f\u5426\u6709 Art.9 \u4f8b\u5916\u6216\u660e\u793a\u540c\u610f\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "transparent_info", "name": "\u900f\u660e\u544a\u77e5", "ref": "Art. 12", "category": "D. \u900f\u660e\u5ea6",
     "desc": "\u544a\u77e5\u662f\u5426\u6613\u61c2\u3001\u53ca\u65f6\u3001\u514d\u8d39\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "info_at_collection", "name": "\u6536\u96c6\u65f6\u4fe1\u606f", "ref": "Art. 13-14", "category": "D. \u900f\u660e\u5ea6",
     "desc": "\u662f\u5426\u8986\u76d6\u8eab\u4efd\u3001\u76ee\u7684\u3001\u6743\u5229\u3001\u63a5\u6536\u65b9\u3001\u8de8\u5883\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "right_access", "name": "\u8bbf\u95ee\u6743", "ref": "Art. 15", "category": "E. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "\u662f\u5426\u652f\u6301\u67e5\u9605\u5e76\u590d\u5236\u4e2a\u4eba\u6570\u636e\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "right_rectification", "name": "\u66f4\u6b63\u6743", "ref": "Art. 16", "category": "E. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "\u662f\u5426\u652f\u6301\u66f4\u6b63\u4e0d\u51c6\u786e\u6570\u636e\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "right_erasure", "name": "\u5220\u9664\u6743", "ref": "Art. 17", "category": "E. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "\u662f\u5426\u652f\u6301\u88ab\u9057\u5fd8\u6743\uff08\u542b\u64e6\u9664\u94fe\u8def\uff09\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "right_restriction", "name": "\u9650\u5236\u5904\u7406\u6743", "ref": "Art. 18", "category": "E. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "\u662f\u5426\u652f\u6301\u5728\u4e89\u8bae\u671f\u9650\u5236\u5904\u7406\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "right_portability", "name": "\u53ef\u643a\u6743", "ref": "Art. 20", "category": "E. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "\u662f\u5426\u652f\u6301\u7ed3\u6784\u5316\u6570\u636e\u5bfc\u51fa\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "right_objection", "name": "\u53cd\u5bf9\u6743", "ref": "Art. 21", "category": "E. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "\u662f\u5426\u652f\u6301\u57fa\u4e8e\u516c\u5171\u5229\u76ca/\u753b\u50cf\u7684\u53cd\u5bf9\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "automated_decisions", "name": "\u81ea\u52a8\u51b3\u7b56", "ref": "Art. 22", "category": "E. \u6570\u636e\u4e3b\u4f53\u6743\u5229",
     "desc": "\u662f\u5426\u63d0\u4f9b\u4eba\u5ba1\u4e0e\u5f02\u8bae\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "accountability", "name": "\u95ee\u8d23", "ref": "Art. 24", "category": "F. \u95ee\u8d23",
     "desc": "\u662f\u5426\u5efa\u7acb\u95ee\u8d23\u5236\u5ea6\u4e0e\u5904\u7406\u8bb0\u5f55\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "privacy_by_design", "name": "\u8bbe\u8ba1\u4e0e\u9ed8\u8ba4\u4fdd\u62a4", "ref": "Art. 25", "category": "F. \u95ee\u8d23",
     "desc": "\u662f\u5426\u5728\u7cfb\u7edf\u8bbe\u8ba1\u4e2d\u5d4c\u5165\u6570\u636e\u4fdd\u62a4\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "processor", "name": "\u5904\u7406\u8005\u7ba1\u7406", "ref": "Art. 28", "category": "G. \u5904\u7406\u8005",
     "desc": "DPA \u662f\u5426\u6ee1\u8db3 Art.28 \u8981\u6c42\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "records", "name": "\u5904\u7406\u6d3b\u52a8\u8bb0\u5f55", "ref": "Art. 30", "category": "F. \u95ee\u8d23",
     "desc": "\u662f\u5426\u7ef4\u62a4 ROPA \u8bb0\u5f55\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "security", "name": "\u5904\u7406\u5b89\u5168", "ref": "Art. 32", "category": "H. \u5b89\u5168",
     "desc": "\u5b89\u5168\u63aa\u65bd\u662f\u5426\u5339\u914d\u98ce\u9669\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "breach_authority", "name": "\u5411\u76d1\u7ba1\u901a\u62a5\u8fdd\u7ea6", "ref": "Art. 33", "category": "I. \u8fdd\u7ea6\u901a\u77e5",
     "desc": "\u662f\u5426\u80fd\u5728 72 \u5c0f\u65f6\u5185\u901a\u62a5\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "breach_subject", "name": "\u5411\u6570\u636e\u4e3b\u4f53\u901a\u62a5", "ref": "Art. 34", "category": "I. \u8fdd\u7ea6\u901a\u77e5",
     "desc": "\u9ad8\u98ce\u9669\u8fdd\u7ea6\u662f\u5426\u901a\u77e5\u4e3b\u4f53\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "dpia", "name": "\u6570\u636e\u4fdd\u62a4\u5f71\u54cd\u8bc4\u4f30", "ref": "Art. 35", "category": "F. \u95ee\u8d23",
     "desc": "\u9ad8\u98ce\u9669\u5904\u7406\u662f\u5426\u505a DPIA\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "prior_consultation", "name": "\u4e8b\u524d\u534f\u5546", "ref": "Art. 36", "category": "F. \u95ee\u8d23",
     "desc": "DPIA \u4ecd\u9ad8\u98ce\u9669\u662f\u5426\u62a5\u76d1\u7ba1\u534f\u5546\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "dpo", "name": "\u6570\u636e\u4fdd\u62a4\u5b98", "ref": "Art. 37-39", "category": "F. \u95ee\u8d23",
     "desc": "\u5f3a\u5236\u60c5\u5f62\u662f\u5426\u4efb\u547d DPO\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
    {"id": "international_transfer", "name": "\u56fd\u9645\u4f20\u8f93", "ref": "Art. 44-49", "category": "J. \u8de8\u5883\u4f20\u8f93",
     "desc": "\u51fa\u5883\u662f\u5426\u4f9d\u8d56\u5145\u5206\u6027/SCC/BCR\uff1f", "recommendation": "\u5bf9\u7167\u6cd5\u89c4\u8981\u6c42\u843d\u5b9e\u5e76\u4fdd\u6301\u8bc1\u636e\u3002"},
]


def _draft_path():
    """Per-user audit draft, stored OUTSIDE the skill folder (never bundled)."""
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.audit.draft.json")


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


def _save_draft(path, answers):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(answers, f, ensure_ascii=False)
    except Exception:
        pass


def _load_draft(path):
    try:
        if os.path.isfile(path):
            with open(path, encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return None


def collect_responses(items):
    responses = []
    total = len(items)
    draft_path = _draft_path()

    # Resume an unfinished draft (interactive terminals only).
    if sys.stdin.isatty():
        draft = _load_draft(draft_path)
        if draft:
            print(f"\n📝 检测到上次未完成的审计草稿（{len(draft)}/{total} 项已作答）。")
            r = input("   继续作答 (y) 还是重新开始 (n)？[y] > ").strip().lower()
            if r != 'n':
                responses = list(draft)
            try:
                os.remove(draft_path)
            except Exception:
                pass

    print(f"\n📋 GDPR Compliance Audit — 共 {total} 项")
    print("   逐项确认实际状态：y=通过 / n=不符合 / na=不适用；输入 ? 可看该项建议\n")

    for i in range(len(responses), total):
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
        # Autosave so a long audit isn't lost on interruption.
        if sys.stdin.isatty():
            _save_draft(draft_path, responses)

    passed = sum(1 for r in responses if r['status'] == 'pass')
    failed = sum(1 for r in responses if r['status'] == 'fail')
    na = sum(1 for r in responses if r['status'] == 'na')
    print(f"\n  ✅ 通过 {passed} ｜ ❌ 不符合 {failed} ｜ ⚪ 不适用 {na} ｜ 共 {total} 项")

    try:
        os.remove(draft_path)
    except Exception:
        pass
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
            return None, "API Key invalid; get a free Key at " + ACCOUNT_PAGE
        if e.code == 403:
            if anon_id:
                # Anonymous trial exhausted -> the caller routes to registration.
                return None, "ANON_QUOTA_EXHAUSTED"
            return None, f"free quota exhausted: {detail} (get a new key at %s)" % ACCOUNT_PAGE
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
    lines = ["=" * 60, f"  GDPR Compliance Audit Report (cloud-scored)" if not s.get("scored_locally") else f"  GDPR Compliance Audit Report (local fallback score)",
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
<html lang="en"><head><meta charset="UTF-8"><title>GDPR Compliance Audit Report</title>
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
<h1>GDPR Compliance Audit Report</h1>
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
    parser = argparse.ArgumentParser(description="GDPR Compliance Audit (free skill + cloud engine)")
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
    if err == "RULE_LIB_NOT_OPEN":
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
