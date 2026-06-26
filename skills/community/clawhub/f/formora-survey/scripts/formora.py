#!/usr/bin/env python3
"""Formora AI Survey CLI client.

Core workflow:
  create -> preview questions -> edit until confirmed -> publish -> broadcast

Broadcast channels:
- QR code: always available
- Telegram: auto-send when FORMORA_TELEGRAM_BOT_TOKEN + FORMORA_TELEGRAM_CHAT_IDS are set
- Email: auto-send when himalaya is installed and FORMORA_EMAIL_TO (or --email-to) is set
- X: auto-post when FORMORA_X_API_KEY / _SECRET / _ACCESS_TOKEN / _ACCESS_TOKEN_SECRET are set

Paid ads channels:
- Google Ads: plan + guarded launch flow
- Meta Ads: plan + guarded launch flow

Safety defaults:
- ads-plan is safe and does not spend money
- ads-launch requires explicit budgets and respects shared caps across Google + Meta
- ads-launch creates campaigns in paused mode by default
- destination URLs must stay under formora.dev unless explicitly reconfigured via env
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API_BASE = "https://api.formora.dev"
APP_BASE = "https://formora.dev"
API_KEY = os.environ.get("FORMORA_API_KEY", "")

SAFE_ALLOWED_DOMAINS = [x.strip().lower() for x in os.environ.get("FORMORA_ADS_ALLOWED_DOMAINS", "formora.dev").split(",") if x.strip()]
SAFE_DAILY_CAP_CNY = float(os.environ.get("FORMORA_ADS_SHARED_DAILY_CAP_CNY", "50"))
SAFE_WEEKLY_CAP_CNY = float(os.environ.get("FORMORA_ADS_SHARED_WEEKLY_CAP_CNY", "100"))
SAFE_REQUIRE_PAUSED = os.environ.get("FORMORA_ADS_REQUIRE_PAUSED_CREATE", "true").lower() in {"1", "true", "yes", "on"}
ADS_ENABLED = os.environ.get("FORMORA_ADS_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
ADS_STATE_PATH = Path(os.environ.get("FORMORA_ADS_STATE_PATH", str(Path(__file__).resolve().parents[1] / "data" / "ads_state.json")))

TYPE_LABELS = {
    "single_choice": "single choice",
    "multiple_choice": "multiple choice",
    "dropdown": "dropdown",
    "text_short": "short text",
    "text_long": "long text",
    "rating": "rating",
    "scale": "scale",
    "nps": "NPS",
    "slider": "slider",
}


def infer_language(text: str, explicit: str | None = None) -> str:
    """Infer survey language from user text unless explicitly provided.

    Heuristic:
    - Any CJK chars -> zh-CN
    - Otherwise -> en
    """
    if explicit and explicit.lower() not in {"auto", ""}:
        return explicit
    for ch in text:
        code = ord(ch)
        if (
            0x4E00 <= code <= 0x9FFF or
            0x3400 <= code <= 0x4DBF or
            0x3040 <= code <= 0x30FF or
            0xAC00 <= code <= 0xD7AF
        ):
            return "zh-CN"
    return "en"


def request(method, path, data=None, binary=False):
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Mozilla/5.0 (compatible; FormoraClient/1.0)",
        "Accept": "application/json",
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read() if binary else json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return json.loads(raw)
        except Exception:
            return {"success": False, "error": {"code": str(e.code), "message": raw.decode(errors="replace")}}


def http_json(method, url, headers=None, data=None):
    headers = headers or {}
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
        if not raw:
            return {}
        return json.loads(raw)


def now_utc_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_ads_state():
    if ADS_STATE_PATH.exists():
        try:
            return json.loads(ADS_STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"campaigns": [], "spend": []}


def save_ads_state(state):
    ADS_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ADS_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def get_spend_summary(state, now=None):
    now = now or datetime.now(timezone.utc)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = day_start - timedelta(days=day_start.weekday())
    daily = 0.0
    weekly = 0.0
    for item in state.get("spend", []):
        try:
            ts = datetime.fromisoformat(item["ts"])
            amount = float(item["amount_cny"])
        except Exception:
            continue
        if ts >= day_start:
            daily += amount
        if ts >= week_start:
            weekly += amount
    return {
        "daily_spent_cny": round(daily, 2),
        "weekly_spent_cny": round(weekly, 2),
        "daily_remaining_cny": round(max(0.0, SAFE_DAILY_CAP_CNY - daily), 2),
        "weekly_remaining_cny": round(max(0.0, SAFE_WEEKLY_CAP_CNY - weekly), 2),
        "shared_daily_cap_cny": SAFE_DAILY_CAP_CNY,
        "shared_weekly_cap_cny": SAFE_WEEKLY_CAP_CNY,
    }


def validate_ads_budget(daily_budget_cny, weekly_budget_cny, state):
    errors = []
    if daily_budget_cny is None or weekly_budget_cny is None:
        errors.append("Both --daily-budget-cny and --weekly-budget-cny are required for ads-launch.")
        return errors
    if daily_budget_cny <= 0 or weekly_budget_cny <= 0:
        errors.append("Budgets must be positive.")
    if daily_budget_cny > SAFE_DAILY_CAP_CNY:
        errors.append(f"Requested daily budget {daily_budget_cny} exceeds shared daily cap {SAFE_DAILY_CAP_CNY} CNY.")
    if weekly_budget_cny > SAFE_WEEKLY_CAP_CNY:
        errors.append(f"Requested weekly budget {weekly_budget_cny} exceeds shared weekly cap {SAFE_WEEKLY_CAP_CNY} CNY.")
    summary = get_spend_summary(state)
    if daily_budget_cny > summary["daily_remaining_cny"]:
        errors.append(f"Requested daily budget {daily_budget_cny} exceeds remaining shared daily budget {summary['daily_remaining_cny']} CNY.")
    if weekly_budget_cny > summary["weekly_remaining_cny"]:
        errors.append(f"Requested weekly budget {weekly_budget_cny} exceeds remaining shared weekly budget {summary['weekly_remaining_cny']} CNY.")
    return errors


def ensure_allowed_ads_url(url):
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if not host:
        return False, "Missing hostname in destination URL."
    if any(host == d or host.endswith("." + d) for d in SAFE_ALLOWED_DOMAINS):
        return True, None
    return False, f"Destination host '{host}' is not allowed. Allowed domains: {', '.join(SAFE_ALLOWED_DOMAINS)}"


def platform_list(value):
    items = [x.strip().lower() for x in value.split(",") if x.strip()]
    allowed = {"google", "meta"}
    unknown = [x for x in items if x not in allowed]
    if unknown:
        raise SystemExit(f"Unsupported platforms: {', '.join(unknown)}")
    return items or ["google", "meta"]


def budget_split(platforms, daily_budget_cny, weekly_budget_cny):
    count = max(1, len(platforms))
    daily_each = round(daily_budget_cny / count, 2)
    weekly_each = round(weekly_budget_cny / count, 2)
    split = {}
    for idx, platform in enumerate(platforms):
        # put rounding remainder on last platform
        if idx == count - 1:
            split[platform] = {
                "daily_budget_cny": round(daily_budget_cny - sum(v["daily_budget_cny"] for v in split.values()), 2),
                "weekly_budget_cny": round(weekly_budget_cny - sum(v["weekly_budget_cny"] for v in split.values()), 2),
            }
        else:
            split[platform] = {"daily_budget_cny": daily_each, "weekly_budget_cny": weekly_each}
    return split


def build_ads_copy(title, url, language="en"):
    zh = str(language).lower().startswith("zh")
    if zh:
        return {
            "headline": title[:30],
            "description": f"参与这份简短问卷，帮助我们获得真实用户反馈。预计 2 分钟完成。 {url}",
            "short_primary": f"欢迎填写问卷《{title}》，约 2 分钟完成。",
            "keywords": [title, "问卷", "调研", "用户反馈", "市场研究"],
            "interests": ["technology", "mobile apps", "product feedback", "market research"],
        }
    return {
        "headline": title[:30],
        "description": f"Take this short survey and help us collect real user feedback. About 2 minutes. {url}",
        "short_primary": f"Take the survey: {title}. It takes about 2 minutes.",
        "keywords": [title, "survey", "user feedback", "market research", "questionnaire"],
        "interests": ["technology", "mobile apps", "product feedback", "market research"],
    }


def get_published_info(survey_id):
    result = request("GET", f"/openapi/v1/surveys/{survey_id}/status")
    if not result.get("success"):
        print(f"Error: unable to fetch survey status: {result}")
        sys.exit(1)
    d = result["data"]
    pub = d.get("public_url")
    if not pub:
        print("Error: survey is not published yet. Run publish first.")
        sys.exit(1)
    return {
        "survey_id": survey_id,
        "title": d.get("title", survey_id),
        "url": f"{APP_BASE}{pub}",
        "response_count": d.get("response_count", 0),
    }


def print_questions(survey_id, indent=""):
    result = request("GET", f"/openapi/v1/surveys/{survey_id}/questions")
    if not result.get("success"):
        print(f"{indent}Warning: unable to fetch questions: {result}")
        return result
    d = result["data"]
    print(f"\n{indent}Preview: {d['title']}")
    if d.get("description"):
        print(f"{indent}   {d['description']}")
    print(f"{indent}   Questions: {len(d['questions'])}  Status: {d['status']}\n")
    for i, q in enumerate(d["questions"], 1):
        qtype = TYPE_LABELS.get(q["type"], q["type"])
        req_mark = "✱" if q.get("required") else "○"
        print(f"{indent}  Q{i}. [{qtype}] {req_mark} {q['text']}")
        opts = q.get("options", {})
        for c in opts.get("choices", []) or []:
            text = c.get("text") or c.get("value", "")
            if text:
                print(f"{indent}       • {text}")
        if q.get("description"):
            print(f"{indent}       ↳ {q['description']}")
    print()
    return result


def build_copy(title, url, language="en"):
    zh = str(language).lower().startswith("zh")
    if zh:
        telegram = f"📊 {title}\n\n正在做一份简短调研，想听听你的真实想法。\n🕐 约 2 分钟\n🔗 {url}"
        email_subject = f"问卷邀请：{title}"
        email_body = f"你好，\n\n想邀请你填写这份简短问卷：{title}\n问卷链接：{url}\n预计耗时：约 2 分钟\n\n感谢你的帮助。"
        x_text = f"正在进行一份简短问卷：{title}\n欢迎填写，约 2 分钟完成 👇\n{url}"
    else:
        telegram = f"📊 {title}\n\nI’m running a short survey and would love your input.\n🕐 About 2 minutes\n🔗 {url}"
        email_subject = f"Survey Invitation: {title}"
        email_body = f"Hello,\n\nI'd like to invite you to take this short survey: {title}.\nSurvey link: {url}\nEstimated time: about 2 minutes.\n\nThank you for your help."
        x_text = f"I’m running a short survey: {title}\nWould love your input — takes about 2 minutes 👇\n{url}"
    iframe = f'<iframe src="{url}" width="100%" height="600" frameborder="0"></iframe>'
    markdown = f"[{title}]({url})"
    return {
        "telegram": telegram,
        "email_subject": email_subject,
        "email_body": email_body,
        "x_text": x_text,
        "iframe": iframe,
        "markdown": markdown,
    }


def generate_qr(url, out_path):
    try:
        import qrcode
        img = qrcode.make(url)
        img.save(out_path)
        return out_path
    except Exception:
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(url)}"
        req = urllib.request.Request(qr_api, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(out_path, "wb") as f:
            f.write(resp.read())
        return out_path


def send_telegram(text, qr_path=None):
    token = os.environ.get("FORMORA_TELEGRAM_BOT_TOKEN")
    chat_ids = [x.strip() for x in os.environ.get("FORMORA_TELEGRAM_CHAT_IDS", "").split(",") if x.strip()]
    if not token or not chat_ids:
        return {"sent": False, "reason": "FORMORA_TELEGRAM_BOT_TOKEN / FORMORA_TELEGRAM_CHAT_IDS not configured"}

    results = []
    for chat_id in chat_ids:
        try:
            if qr_path and Path(qr_path).exists():
                boundary = f"----Formora{secrets.token_hex(8)}"
                with open(qr_path, "rb") as f:
                    img = f.read()
                parts = []
                def add_field(name, value):
                    parts.extend([
                        f"--{boundary}\r\n".encode(),
                        f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                        str(value).encode(), b"\r\n"
                    ])
                add_field("chat_id", chat_id)
                add_field("caption", text)
                parts.extend([
                    f"--{boundary}\r\n".encode(),
                    b'Content-Disposition: form-data; name="photo"; filename="survey_qr.png"\r\n',
                    b"Content-Type: image/png\r\n\r\n",
                    img, b"\r\n",
                    f"--{boundary}--\r\n".encode(),
                ])
                req = urllib.request.Request(
                    f"https://api.telegram.org/bot{token}/sendPhoto",
                    data=b"".join(parts),
                    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
                    method="POST",
                )
                with urllib.request.urlopen(req) as resp:
                    results.append(json.loads(resp.read()))
            else:
                results.append(http_json(
                    "POST",
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    headers={"Content-Type": "application/json"},
                    data={"chat_id": chat_id, "text": text},
                ))
        except Exception as e:
            results.append({"ok": False, "chat_id": chat_id, "error": str(e)})
    return {"sent": True, "results": results}


def send_email(subject, body, email_to=None):
    recipients = email_to or os.environ.get("FORMORA_EMAIL_TO", "")
    recipients = [x.strip() for x in recipients.split(",") if x.strip()]
    if not recipients:
        return {"sent": False, "reason": "No recipients specified (FORMORA_EMAIL_TO or --email-to)"}
    if not shutil.which("himalaya"):
        return {"sent": False, "reason": "himalaya is not installed"}

    msg = f"Subject: {subject}\nTo: {', '.join(recipients)}\n\n{body}\n"
    try:
        proc = subprocess.run(
            ["himalaya", "template", "send"],
            input=msg.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return {
            "sent": proc.returncode == 0,
            "stdout": proc.stdout.decode(errors="replace"),
            "stderr": proc.stderr.decode(errors="replace"),
        }
    except Exception as e:
        return {"sent": False, "reason": str(e)}


def _oauth1_header(method, url, consumer_key, consumer_secret, token, token_secret):
    oauth = {
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": token,
        "oauth_version": "1.0",
    }
    encoded = sorted((urllib.parse.quote(k, safe="~"), urllib.parse.quote(v, safe="~")) for k, v in oauth.items())
    param_str = "&".join(f"{k}={v}" for k, v in encoded)
    base_elems = [method.upper(), urllib.parse.quote(url, safe="~"), urllib.parse.quote(param_str, safe="~")]
    base_string = "&".join(base_elems)
    signing_key = f"{urllib.parse.quote(consumer_secret, safe='~')}&{urllib.parse.quote(token_secret, safe='~')}"
    signature = base64.b64encode(hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()).decode()
    oauth["oauth_signature"] = signature
    header = "OAuth " + ", ".join(
        f'{urllib.parse.quote(k, safe="~") }="{urllib.parse.quote(v, safe="~")}"'.replace(' ', '') for k, v in sorted(oauth.items())
    )
    return header


def send_x_post(text):
    ck = os.environ.get("FORMORA_X_API_KEY")
    cs = os.environ.get("FORMORA_X_API_SECRET")
    at = os.environ.get("FORMORA_X_ACCESS_TOKEN")
    ats = os.environ.get("FORMORA_X_ACCESS_TOKEN_SECRET")
    if not all([ck, cs, at, ats]):
        return {"sent": False, "reason": "FORMORA_X_* credentials are not fully configured"}
    url = "https://api.twitter.com/2/tweets"
    auth = _oauth1_header("POST", url, ck, cs, at, ats)
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps({"text": text[:280]}).encode("utf-8"),
            headers={
                "Authorization": auth,
                "Content-Type": "application/json",
                "User-Agent": "FormoraSurveySkill/1.0",
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return {"sent": True, "response": json.loads(resp.read())}
    except urllib.error.HTTPError as e:
        return {"sent": False, "reason": e.read().decode(errors="replace")}
    except Exception as e:
        return {"sent": False, "reason": str(e)}


def google_ads_ready(live=False):
    needed = [
        "FORMORA_GOOGLE_ADS_CUSTOMER_ID",
        "FORMORA_GOOGLE_ADS_DEVELOPER_TOKEN",
        "FORMORA_GOOGLE_ADS_CLIENT_ID",
        "FORMORA_GOOGLE_ADS_CLIENT_SECRET",
        "FORMORA_GOOGLE_ADS_REFRESH_TOKEN",
    ]
    missing = [k for k in needed if not os.environ.get(k)]
    return {"ready": not missing, "missing": missing}


def google_ads_api_version():
    return os.environ.get("FORMORA_GOOGLE_ADS_API_VERSION", "v19")


def google_ads_get_token():
    """Exchange refresh token for a short-lived access token."""
    data = urllib.parse.urlencode({
        "client_id": os.environ["FORMORA_GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["FORMORA_GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["FORMORA_GOOGLE_ADS_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]


def google_ads_mutate(customer_id, resource, operations, access_token):
    """Call GoogleAds REST mutate endpoint."""
    dev_token = os.environ["FORMORA_GOOGLE_ADS_DEVELOPER_TOKEN"]
    version = google_ads_api_version()
    url = f"https://googleads.googleapis.com/{version}/customers/{customer_id}/{resource}:mutate"
    body = json.dumps({"operations": operations}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "developer-token": dev_token,
            "Content-Type": "application/json",
            "User-Agent": "FormoraSurveySkill/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def google_ads_mutate_resource(customer_id, resource, resource_name, patch, access_token):
    """PATCH a single resource via mutate (used for pause/enable)."""
    dev_token = os.environ["FORMORA_GOOGLE_ADS_DEVELOPER_TOKEN"]
    version = google_ads_api_version()
    url = f"https://googleads.googleapis.com/{version}/customers/{customer_id}/{resource}:mutate"
    op = {"update": {"resourceName": resource_name, **patch}, "updateMask": ",".join(patch.keys())}
    body = json.dumps({"operations": [op]}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "developer-token": dev_token,
            "Content-Type": "application/json",
            "User-Agent": "FormoraSurveySkill/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def geo_to_google_location_ids(geo):
    """Map geo string to Google Ads geo target constant IDs.

    Common mappings (canonical subset). Full list: https://developers.google.com/google-ads/api/reference/data/geotargets
    For unsupported codes the caller falls back to no geo targeting.
    """
    GEO_MAP = {
        "US": "2840", "CA": "2124", "GB": "2826", "AU": "2036",
        "CN": "2156", "JP": "2392", "KR": "2410", "DE": "2276",
        "FR": "2250", "IN": "2356", "BR": "2076", "MX": "2484",
        "SG": "2702", "HK": "2344", "TW": "2158", "TH": "2764",
        "ID": "2360", "PH": "2608", "VN": "2704", "MY": "2458",
    }
    if not geo or geo.lower() == "global":
        return []
    codes = [x.strip().upper() for x in geo.split(",") if x.strip() and len(x.strip()) == 2]
    return [GEO_MAP[c] for c in codes if c in GEO_MAP]


def google_create_live_campaign(info, plan, survey_id, paused=True):
    readiness = google_ads_ready(live=True)
    if not readiness["ready"]:
        return {
            "platform": "google",
            "status": "blocked",
            "live_api_called": False,
            "reason": "Missing required Google Ads configuration.",
            "config_ready": readiness,
        }
    customer_id = os.environ["FORMORA_GOOGLE_ADS_CUSTOMER_ID"].replace("-", "")
    campaign_name = f"formora-{survey_id[:8]}-google"
    status = "PAUSED" if paused else "ENABLED"
    # daily budget in micros (1 CNY = 1,000,000 micros)
    daily_micros = int(plan["budget"]["daily_budget_cny"] * 1_000_000)
    copy = plan.get("creative", {})
    keywords = plan.get("keywords", [])
    geo_ids = geo_to_google_location_ids(plan.get("geo", ""))

    try:
        access_token = google_ads_get_token()

        # 1) Campaign budget
        budget_resp = google_ads_mutate(customer_id, "campaignBudgets", [{
            "create": {
                "name": f"{campaign_name}-budget",
                "amountMicros": str(daily_micros),
                "deliveryMethod": "STANDARD",
            }
        }], access_token)
        budget_rn = budget_resp["results"][0]["resourceName"]

        # 2) Campaign
        campaign_body = {
            "name": campaign_name,
            "advertisingChannelType": "SEARCH",
            "status": status,
            "campaignBudget": budget_rn,
            "networkSettings": {
                "targetGoogleSearch": True,
                "targetSearchNetwork": True,
                "targetContentNetwork": False,
            },
        }
        if geo_ids:
            campaign_body["geoTargetTypeSetting"] = {"positiveGeoTargetType": "PRESENCE_OR_INTEREST"}
        campaign_resp = google_ads_mutate(customer_id, "campaigns", [{"create": campaign_body}], access_token)
        campaign_rn = campaign_resp["results"][0]["resourceName"]

        # 3) Geo targets
        if geo_ids:
            geo_ops = [
                {"create": {"campaign": campaign_rn, "location": {"geoTargetConstant": f"geoTargetConstants/{gid}"}}}
                for gid in geo_ids
            ]
            google_ads_mutate(customer_id, "campaignCriteria", geo_ops, access_token)

        # 4) Ad group
        adgroup_resp = google_ads_mutate(customer_id, "adGroups", [{
            "create": {
                "name": f"{campaign_name}-adgroup",
                "campaign": campaign_rn,
                "type": "SEARCH_STANDARD",
                "status": status,
                "cpcBidMicros": "1000000",  # 1 CNY default CPC
            }
        }], access_token)
        adgroup_rn = adgroup_resp["results"][0]["resourceName"]

        # 5) Keywords (up to 5)
        if keywords:
            kw_ops = [
                {
                    "create": {
                        "adGroup": adgroup_rn,
                        "status": status,
                        "keyword": {"text": kw[:80], "matchType": "BROAD"},
                    }
                }
                for kw in keywords[:5]
            ]
            google_ads_mutate(customer_id, "adGroupCriteria", kw_ops, access_token)

        # 6) Responsive Search Ad
        headline_text = (copy.get("headline") or info["title"])[:30]
        desc_text = (copy.get("description") or info["title"])[:90]
        ad_resp = google_ads_mutate(customer_id, "adGroupAds", [{
            "create": {
                "adGroup": adgroup_rn,
                "status": status,
                "ad": {
                    "responsiveSearchAd": {
                        "headlines": [{"text": headline_text}, {"text": info["title"][:30]}],
                        "descriptions": [{"text": desc_text}, {"text": "Take our short survey. About 2 minutes."}],
                    },
                    "finalUrls": [info["url"]],
                },
            }
        }], access_token)
        ad_rn = ad_resp["results"][0]["resourceName"]

        return {
            "platform": "google",
            "status": "paused" if paused else "active",
            "live_api_called": True,
            "config_ready": readiness,
            "target_url": info["url"],
            "campaign_name": campaign_name,
            "budget": plan["budget"],
            "created_at": now_utc_iso(),
            "budget_resource_name": budget_rn,
            "campaign_resource_name": campaign_rn,
            "adgroup_resource_name": adgroup_rn,
            "ad_resource_name": ad_rn,
            "geo_ids": geo_ids,
        }
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        return {
            "platform": "google",
            "status": "error",
            "live_api_called": True,
            "config_ready": readiness,
            "reason": body,
            "target_url": info["url"],
            "campaign_name": campaign_name,
            "budget": plan["budget"],
            "created_at": now_utc_iso(),
        }
    except Exception as e:
        return {
            "platform": "google",
            "status": "error",
            "live_api_called": False,
            "config_ready": readiness,
            "reason": str(e),
            "target_url": info["url"],
            "campaign_name": campaign_name,
            "budget": plan["budget"],
            "created_at": now_utc_iso(),
        }


def google_pause_live_campaign(record):
    readiness = google_ads_ready(live=True)
    if not readiness["ready"]:
        return {"ok": False, "reason": "Missing Google Ads configuration.", "config_ready": readiness}
    customer_id = os.environ["FORMORA_GOOGLE_ADS_CUSTOMER_ID"].replace("-", "")
    try:
        access_token = google_ads_get_token()
        paused = []
        if record.get("campaign_resource_name"):
            paused.append({"campaign": google_ads_mutate_resource(
                customer_id, "campaigns",
                record["campaign_resource_name"],
                {"status": "PAUSED"},
                access_token,
            )})
        if record.get("adgroup_resource_name"):
            paused.append({"adGroup": google_ads_mutate_resource(
                customer_id, "adGroups",
                record["adgroup_resource_name"],
                {"status": "PAUSED"},
                access_token,
            )})
        return {"ok": True, "paused": paused}
    except urllib.error.HTTPError as e:
        return {"ok": False, "reason": e.read().decode(errors="replace")}
    except Exception as e:
        return {"ok": False, "reason": str(e)}


def meta_ads_ready(live=False):
    needed = [
        "FORMORA_META_AD_ACCOUNT_ID",
        "FORMORA_META_ACCESS_TOKEN",
    ]
    if live:
        needed += [
            "FORMORA_META_PAGE_ID",
        ]
    missing = [k for k in needed if not os.environ.get(k)]
    return {"ready": not missing, "missing": missing}


def meta_api_version():
    return os.environ.get("FORMORA_META_API_VERSION", "v22.0")


def meta_graph_post(path, data):
    token = os.environ.get("FORMORA_META_ACCESS_TOKEN", "")
    version = meta_api_version()
    url = f"https://graph.facebook.com/{version}/{path.lstrip('/')}"
    payload = dict(data)
    payload["access_token"] = token
    encoded = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "FormoraSurveySkill/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else {}


def parse_geo_countries(geo):
    if not geo or geo.lower() == "global":
        return []
    items = [x.strip().upper() for x in geo.split(",") if x.strip()]
    countries = [x for x in items if len(x) == 2 and x.isalpha()]
    return countries


def meta_create_live_campaign(info, plan, survey_id, paused=True):
    readiness = meta_ads_ready(live=True)
    if not readiness["ready"]:
        return {
            "platform": "meta",
            "status": "blocked",
            "live_api_called": False,
            "reason": "Missing required Meta live-submit configuration.",
            "config_ready": readiness,
        }

    countries = parse_geo_countries(plan.get("geo", ""))
    if not countries:
        return {
            "platform": "meta",
            "status": "blocked",
            "live_api_called": False,
            "reason": "Meta live submit requires --geo with comma-separated ISO country codes, e.g. US,CA or CN.",
            "config_ready": readiness,
        }

    account_id = os.environ["FORMORA_META_AD_ACCOUNT_ID"]
    page_id = os.environ["FORMORA_META_PAGE_ID"]
    status = "PAUSED" if paused else "ACTIVE"
    budget_fen = int(round(float(plan["budget"]["daily_budget_cny"]) * 100))
    creative = plan["creative"]
    campaign_name = f"formora-{survey_id[:8]}-meta"

    try:
        campaign = meta_graph_post(f"act_{account_id}/campaigns", {
            "name": campaign_name,
            "objective": "OUTCOME_TRAFFIC",
            "status": status,
            "special_ad_categories": "[]",
        })
        campaign_id = campaign.get("id")
        if not campaign_id:
            raise RuntimeError(f"Meta campaign creation returned no id: {campaign}")

        adset = meta_graph_post(f"act_{account_id}/adsets", {
            "name": f"{campaign_name}-adset",
            "campaign_id": campaign_id,
            "daily_budget": str(budget_fen),
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "LINK_CLICKS",
            "destination_type": "WEBSITE",
            "status": status,
            "targeting": json.dumps({"geo_locations": {"countries": countries}}),
            "promoted_object": json.dumps({"page_id": page_id}),
        })
        adset_id = adset.get("id")
        if not adset_id:
            raise RuntimeError(f"Meta ad set creation returned no id: {adset}")

        adcreative = meta_graph_post(f"act_{account_id}/adcreatives", {
            "name": f"{campaign_name}-creative",
            "object_story_spec": json.dumps({
                "page_id": page_id,
                "link_data": {
                    "link": info["url"],
                    "message": creative.get("primary_text") or creative.get("description") or info["title"],
                    "name": creative.get("headline") or info["title"],
                    "description": creative.get("description") or "",
                    "call_to_action": {"type": "LEARN_MORE"},
                },
            }),
        })
        creative_id = adcreative.get("id")
        if not creative_id:
            raise RuntimeError(f"Meta ad creative creation returned no id: {adcreative}")

        ad = meta_graph_post(f"act_{account_id}/ads", {
            "name": f"{campaign_name}-ad",
            "adset_id": adset_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": status,
        })
        ad_id = ad.get("id")
        if not ad_id:
            raise RuntimeError(f"Meta ad creation returned no id: {ad}")

        return {
            "platform": "meta",
            "status": "paused" if paused else "active",
            "live_api_called": True,
            "config_ready": readiness,
            "target_url": info["url"],
            "campaign_name": campaign_name,
            "budget": plan["budget"],
            "created_at": now_utc_iso(),
            "campaign_id": campaign_id,
            "adset_id": adset_id,
            "creative_id": creative_id,
            "ad_id": ad_id,
            "geo_countries": countries,
        }
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        return {
            "platform": "meta",
            "status": "error",
            "live_api_called": True,
            "config_ready": readiness,
            "reason": body,
            "target_url": info["url"],
            "campaign_name": campaign_name,
            "budget": plan["budget"],
            "created_at": now_utc_iso(),
        }
    except Exception as e:
        return {
            "platform": "meta",
            "status": "error",
            "live_api_called": False,
            "config_ready": readiness,
            "reason": str(e),
            "target_url": info["url"],
            "campaign_name": campaign_name,
            "budget": plan["budget"],
            "created_at": now_utc_iso(),
        }


def create_google_ads_plan(info, language, daily_budget_cny, weekly_budget_cny, geo):
    copy = build_ads_copy(info["title"], info["url"], language)
    return {
        "platform": "google",
        "mode": "plan",
        "campaign_type": "search",
        "objective": "website_traffic",
        "status_on_create": "PAUSED",
        "target_url": info["url"],
        "language": language,
        "geo": geo,
        "budget": {"daily_budget_cny": daily_budget_cny, "weekly_budget_cny": weekly_budget_cny},
        "creative": {
            "headline": copy["headline"],
            "description": copy["description"],
        },
        "keywords": copy["keywords"],
        "config_ready": google_ads_ready(),
    }


def create_meta_ads_plan(info, language, daily_budget_cny, weekly_budget_cny, geo):
    copy = build_ads_copy(info["title"], info["url"], language)
    return {
        "platform": "meta",
        "mode": "plan",
        "campaign_type": "traffic",
        "objective": "OUTCOME_TRAFFIC",
        "status_on_create": "PAUSED",
        "target_url": info["url"],
        "language": language,
        "geo": geo,
        "budget": {"daily_budget_cny": daily_budget_cny, "weekly_budget_cny": weekly_budget_cny},
        "creative": {
            "headline": copy["headline"],
            "primary_text": copy["short_primary"],
            "description": copy["description"],
        },
        "interests": copy["interests"],
        "config_ready": meta_ads_ready(),
    }


def create_google_launch_record(info, plan, paused=True):
    readiness = google_ads_ready()
    return {
        "platform": "google",
        "status": "paused" if paused else "pending_enable",
        "live_api_called": False,
        "reason": "Google Ads credentials not configured; launch prepared but not submitted." if not readiness["ready"] else "Google Ads live submit requires all 5 credentials (CUSTOMER_ID, DEVELOPER_TOKEN, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN).",
        "config_ready": readiness,
        "target_url": info["url"],
        "campaign_name": f"formora-{info['survey_id'][:8]}-google",
        "budget": plan["budget"],
        "created_at": now_utc_iso(),
    }


def create_meta_launch_record(info, plan, paused=True):
    readiness = meta_ads_ready()
    return {
        "platform": "meta",
        "status": "paused" if paused else "pending_enable",
        "live_api_called": False,
        "reason": "Meta Ads credentials not configured; launch prepared but not submitted." if not readiness["ready"] else "Meta Ads live submit is available when FORMORA_META_PAGE_ID is also configured.",
        "config_ready": readiness,
        "target_url": info["url"],
        "campaign_name": f"formora-{info['survey_id'][:8]}-meta",
        "budget": plan["budget"],
        "created_at": now_utc_iso(),
    }


def meta_pause_live_campaign(record):
    readiness = meta_ads_ready(live=True)
    if not readiness["ready"]:
        return {"ok": False, "reason": "Missing Meta live-submit configuration.", "config_ready": readiness}
    paused = []
    try:
        if record.get("campaign_id"):
            paused.append({"campaign": meta_graph_post(record["campaign_id"], {"status": "PAUSED"})})
        if record.get("adset_id"):
            paused.append({"adset": meta_graph_post(record["adset_id"], {"status": "PAUSED"})})
        if record.get("ad_id"):
            paused.append({"ad": meta_graph_post(record["ad_id"], {"status": "PAUSED"})})
        return {"ok": True, "paused": paused}
    except urllib.error.HTTPError as e:
        return {"ok": False, "reason": e.read().decode(errors="replace")}
    except Exception as e:
        return {"ok": False, "reason": str(e)}


def cmd_create(args):
    language = infer_language(args.instruction, args.language)
    payload = {"instruction": args.instruction, "language": language, "question_count": args.count}
    if args.audience:
        payload["target_audience"] = args.audience
    result = request("POST", "/openapi/v1/surveys", payload)
    if not result.get("success"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    d = result["data"]
    survey_id = d["survey_id"]
    print(f"Draft created: {survey_id}  ({d.get('title', '')})")
    print_questions(survey_id)
    print(f"survey_id: {survey_id}")


def cmd_questions(args):
    print_questions(args.survey_id)


def cmd_edit(args):
    result = request("PUT", f"/openapi/v1/surveys/{args.survey_id}", {"instruction": args.instruction})
    if not result.get("success"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    print(f"Updated: {result['data'].get('message', '')}")
    print_questions(args.survey_id)
    print(f"survey_id: {args.survey_id}")


def cmd_status(args):
    result = request("GET", f"/openapi/v1/surveys/{args.survey_id}/status")
    if result.get("success"):
        d = result["data"]
        pub = d.get("public_url")
        url = f"{APP_BASE}{pub}" if pub else None
        print(json.dumps({
            "survey_id": d["survey_id"],
            "title": d.get("title", ""),
            "status": d["status"],
            "response_count": d.get("response_count", 0),
            "public_url": url,
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_publish(args):
    result = request("POST", f"/openapi/v1/surveys/{args.survey_id}/publish")
    if not result.get("success"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    d = result["data"]
    pub = d.get("public_url", "")
    full_url = f"{APP_BASE}{pub}"
    print(f"Published!\n   Title: {d.get('title', args.survey_id)}\n   URL: {full_url}\nsurvey_id: {args.survey_id}\nurl: {full_url}")


def cmd_distribute(args):
    info = get_published_info(args.survey_id)
    language = infer_language(info["title"], args.language)
    copy = build_copy(info["title"], info["url"], language)
    qr_path = None
    if args.qr:
        qr_path = args.qr if args.qr != "auto" else f"survey_qr_{args.survey_id[:8]}.png"
        generate_qr(info["url"], qr_path)

    print(f"\nDistribution kit: {info['title']}")
    print("─" * 50)
    print(f"Direct URL:  {info['url']}")
    print(f"\nTelegram copy:\n{copy['telegram']}")
    print(f"\nEmail subject:\n{copy['email_subject']}")
    print(f"\nEmail body:\n{copy['email_body']}")
    print(f"\nX post copy:\n{copy['x_text']}")
    print(f"\nWeb embed code:\n{copy['iframe']}")
    print(f"\nMarkdown link:\n{copy['markdown']}")
    if qr_path:
        print(f"\nQR code saved to: {qr_path}")


def cmd_broadcast(args):
    info = get_published_info(args.survey_id)
    language = infer_language(info["title"], args.language)
    copy = build_copy(info["title"], info["url"], language)
    out_dir = Path(args.out_dir or f"broadcast_{args.survey_id[:8]}")
    out_dir.mkdir(parents=True, exist_ok=True)
    qr_path = str(out_dir / f"qr_{args.survey_id[:8]}.png")
    generate_qr(info["url"], qr_path)

    results = {
        "survey_id": args.survey_id,
        "title": info["title"],
        "url": info["url"],
        "language": language,
        "qr": qr_path,
        "channels": {}
    }

    results["channels"]["telegram"] = send_telegram(copy["telegram"], qr_path if args.telegram_with_qr else None)
    results["channels"]["email"] = send_email(copy["email_subject"], copy["email_body"], args.email_to)
    results["channels"]["x"] = send_x_post(copy["x_text"])
    (out_dir / "telegram.txt").write_text(copy["telegram"], encoding="utf-8")
    (out_dir / "email_subject.txt").write_text(copy["email_subject"], encoding="utf-8")
    (out_dir / "email_body.txt").write_text(copy["email_body"], encoding="utf-8")
    (out_dir / "x.txt").write_text(copy["x_text"], encoding="utf-8")
    (out_dir / "iframe.html").write_text(copy["iframe"], encoding="utf-8")
    (out_dir / "link.md").write_text(copy["markdown"], encoding="utf-8")

    print(json.dumps(results, ensure_ascii=False, indent=2))


def cmd_ads_plan(args):
    info = get_published_info(args.survey_id)
    ok, reason = ensure_allowed_ads_url(info["url"])
    if not ok:
        print(json.dumps({"ok": False, "error": reason}, ensure_ascii=False, indent=2))
        sys.exit(1)
    language = infer_language(info["title"], args.language)
    platforms = platform_list(args.platforms)
    daily_budget_cny = float(args.daily_budget_cny or SAFE_DAILY_CAP_CNY)
    weekly_budget_cny = float(args.weekly_budget_cny or SAFE_WEEKLY_CAP_CNY)
    if daily_budget_cny > SAFE_DAILY_CAP_CNY:
        daily_budget_cny = SAFE_DAILY_CAP_CNY
    if weekly_budget_cny > SAFE_WEEKLY_CAP_CNY:
        weekly_budget_cny = SAFE_WEEKLY_CAP_CNY
    split = budget_split(platforms, daily_budget_cny, weekly_budget_cny)
    state = load_ads_state()
    result = {
        "survey_id": args.survey_id,
        "title": info["title"],
        "url": info["url"],
        "language": language,
        "geo": args.geo,
        "platforms": platforms,
        "mode": "plan",
        "requires_manual_confirmation": True,
        "shared_budget": {
            "requested_daily_budget_cny": daily_budget_cny,
            "requested_weekly_budget_cny": weekly_budget_cny,
            **get_spend_summary(state),
        },
        "safety": {
            "ads_enabled": ADS_ENABLED,
            "require_paused_create": SAFE_REQUIRE_PAUSED,
            "allowed_domains": SAFE_ALLOWED_DOMAINS,
        },
        "plans": {},
    }
    if "google" in platforms:
        result["plans"]["google"] = create_google_ads_plan(info, language, split["google"]["daily_budget_cny"], split["google"]["weekly_budget_cny"], args.geo)
    if "meta" in platforms:
        result["plans"]["meta"] = create_meta_ads_plan(info, language, split["meta"]["daily_budget_cny"], split["meta"]["weekly_budget_cny"], args.geo)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_ads_launch(args):
    info = get_published_info(args.survey_id)
    ok, reason = ensure_allowed_ads_url(info["url"])
    if not ok:
        print(json.dumps({"ok": False, "error": reason}, ensure_ascii=False, indent=2))
        sys.exit(1)
    if not ADS_ENABLED:
        print(json.dumps({
            "ok": False,
            "error": "FORMORA_ADS_ENABLED is not true. Live ads launch is disabled.",
            "hint": "Set FORMORA_ADS_ENABLED=true after reviewing credentials and budget policy.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    state = load_ads_state()
    daily_budget_cny = float(args.daily_budget_cny)
    weekly_budget_cny = float(args.weekly_budget_cny)
    errors = validate_ads_budget(daily_budget_cny, weekly_budget_cny, state)
    if errors:
        print(json.dumps({"ok": False, "errors": errors, "budget": get_spend_summary(state)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    language = infer_language(info["title"], args.language)
    platforms = platform_list(args.platforms)
    split = budget_split(platforms, daily_budget_cny, weekly_budget_cny)
    paused = True if SAFE_REQUIRE_PAUSED else args.paused
    campaign_group_id = f"adsgrp_{args.survey_id[:8]}_{int(time.time())}"
    result = {
        "ok": True,
        "mode": "launch",
        "live_submitted": False,
        "campaign_group_id": campaign_group_id,
        "survey_id": args.survey_id,
        "url": info["url"],
        "language": language,
        "paused": paused,
        "shared_budget": {
            "daily_budget_cny": daily_budget_cny,
            "weekly_budget_cny": weekly_budget_cny,
            **get_spend_summary(state),
        },
        "platforms": {},
        "note": "Campaigns are recorded as paused launch intents. This environment enforces plan-first and does not auto-enable spend.",
    }

    if "google" in platforms:
        plan = create_google_ads_plan(info, language, split["google"]["daily_budget_cny"], split["google"]["weekly_budget_cny"], args.geo)
        if google_ads_ready(live=True)["ready"]:
            record = google_create_live_campaign(info, plan, args.survey_id, paused=paused)
        else:
            record = create_google_launch_record(info, plan, paused=paused)
        result["platforms"]["google"] = record
        state["campaigns"].append({
            "campaign_group_id": campaign_group_id,
            **record,
            "survey_id": args.survey_id,
            "platform_budget_cny": plan["budget"],
        })

    if "meta" in platforms:
        plan = create_meta_ads_plan(info, language, split["meta"]["daily_budget_cny"], split["meta"]["weekly_budget_cny"], args.geo)
        if meta_ads_ready(live=True)["ready"]:
            record = meta_create_live_campaign(info, plan, args.survey_id, paused=paused)
        else:
            record = create_meta_launch_record(info, plan, paused=paused)
        result["platforms"]["meta"] = record
        state["campaigns"].append({
            "campaign_group_id": campaign_group_id,
            **record,
            "survey_id": args.survey_id,
            "platform_budget_cny": plan["budget"],
        })

    result["live_submitted"] = any(v.get("live_api_called") for v in result["platforms"].values())
    save_ads_state(state)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_ads_status(args):
    state = load_ads_state()
    summary = get_spend_summary(state)
    campaigns = state.get("campaigns", [])
    if args.survey_id:
        campaigns = [c for c in campaigns if c.get("survey_id") == args.survey_id]
    if args.campaign_group_id:
        campaigns = [c for c in campaigns if c.get("campaign_group_id") == args.campaign_group_id]
    print(json.dumps({
        "ok": True,
        "budget": summary,
        "campaign_count": len(campaigns),
        "campaigns": campaigns,
    }, ensure_ascii=False, indent=2))


def cmd_ads_stop(args):
    state = load_ads_state()
    changed = []
    for campaign in state.get("campaigns", []):
        if args.campaign_group_id and campaign.get("campaign_group_id") != args.campaign_group_id:
            continue
        if args.survey_id and campaign.get("survey_id") != args.survey_id:
            continue
        if args.platform and campaign.get("platform") != args.platform:
            continue
        if campaign.get("platform") == "meta" and campaign.get("live_api_called"):
            campaign["stop_result"] = meta_pause_live_campaign(campaign)
        elif campaign.get("platform") == "google" and campaign.get("live_api_called"):
            campaign["stop_result"] = google_pause_live_campaign(campaign)
        campaign["status"] = "stopped"
        campaign["stopped_at"] = now_utc_iso()
        changed.append(campaign)
    save_ads_state(state)
    print(json.dumps({
        "ok": True,
        "stopped_count": len(changed),
        "campaigns": changed,
    }, ensure_ascii=False, indent=2))


def cmd_responses(args):
    path = f"/openapi/v1/surveys/{args.survey_id}/responses?page={args.page}&per_page={args.per_page}"
    if args.status:
        path += f"&status={args.status}"
    print(json.dumps(request("GET", path), ensure_ascii=False, indent=2))


def cmd_export(args):
    path = f"/openapi/v1/surveys/{args.survey_id}/export?format={args.format}"
    data = request("GET", path, binary=True)
    out = args.output or f"responses.{args.format}"
    with open(out, "wb") as f:
        f.write(data)
    print(f"Exported to {out}  ({len(data):,} bytes)")


def cmd_wizard(args):
    print(f"\nFormora wizard mode\n{'─'*40}")
    language = infer_language(args.topic, args.language)
    payload = {"instruction": args.topic, "language": language, "question_count": args.count}
    if args.audience:
        payload["target_audience"] = args.audience
    result = request("POST", "/openapi/v1/surveys", payload)
    if not result.get("success"):
        print(f"Create failed: {result}")
        sys.exit(1)
    survey_id = result["data"]["survey_id"]
    print_questions(survey_id)
    while True:
        print("Please confirm the draft:\n  [y] confirm and publish\n  [n] keep as draft\n  [e] edit with a new instruction")
        choice = input(">>> ").strip().lower()
        if choice == "y":
            pub = request("POST", f"/openapi/v1/surveys/{survey_id}/publish")
            if not pub.get("success"):
                print(f"Publish failed: {pub}")
                sys.exit(1)
            print(f"\nPublished!\n   URL: {APP_BASE}{pub['data']['public_url']}\n   survey_id: {survey_id}")
            break
        if choice == "n":
            print(f"\nDraft kept. survey_id: {survey_id}")
            break
        if choice == "e":
            instruction = input("Edit instruction >>> ").strip()
            if instruction:
                edit_result = request("PUT", f"/openapi/v1/surveys/{survey_id}", {"instruction": instruction})
                if edit_result.get("success"):
                    print_questions(survey_id)
                else:
                    print(f"Edit failed: {edit_result}")
        else:
            print("Please enter y / n / e")


def main():
    if not API_KEY:
        print("ERROR: FORMORA_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Formora AI Survey CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("create", help="Create a draft and preview questions")
    p.add_argument("instruction")
    p.add_argument("--audience")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--language", default="auto")
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("questions", help="Show survey questions")
    p.add_argument("survey_id")
    p.set_defaults(func=cmd_questions)

    p = sub.add_parser("edit", help="Edit the survey and preview again")
    p.add_argument("survey_id")
    p.add_argument("instruction")
    p.set_defaults(func=cmd_edit)

    p = sub.add_parser("status", help="Show survey status")
    p.add_argument("survey_id")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("publish", help="Publish the survey")
    p.add_argument("survey_id")
    p.set_defaults(func=cmd_publish)

    p = sub.add_parser("distribute", help="Generate channel copy, QR code, and embed assets")
    p.add_argument("survey_id")
    p.add_argument("--language", default="auto")
    p.add_argument("--qr", nargs="?", const="auto", default=None)
    p.set_defaults(func=cmd_distribute)

    p = sub.add_parser("broadcast", help="Broadcast to as many available channels as possible: Telegram / Email / QR / X")
    p.add_argument("survey_id")
    p.add_argument("--language", default="auto")
    p.add_argument("--email-to", default="")
    p.add_argument("--out-dir", default="")
    p.add_argument("--telegram-with-qr", action="store_true")
    p.set_defaults(func=cmd_broadcast)

    p = sub.add_parser("ads-plan", help="Generate a safe paid ads plan for Google Ads / Meta Ads")
    p.add_argument("survey_id")
    p.add_argument("--platforms", default="google,meta")
    p.add_argument("--language", default="auto")
    p.add_argument("--geo", default="global")
    p.add_argument("--daily-budget-cny", type=float, default=None)
    p.add_argument("--weekly-budget-cny", type=float, default=None)
    p.set_defaults(func=cmd_ads_plan)

    p = sub.add_parser("ads-launch", help="Create guarded paid ads launch intents for Google Ads / Meta Ads")
    p.add_argument("survey_id")
    p.add_argument("--platforms", default="google,meta")
    p.add_argument("--language", default="auto")
    p.add_argument("--geo", default="global")
    p.add_argument("--daily-budget-cny", type=float, required=True)
    p.add_argument("--weekly-budget-cny", type=float, required=True)
    p.add_argument("--paused", action="store_true")
    p.set_defaults(func=cmd_ads_launch)

    p = sub.add_parser("ads-status", help="Show paid ads budget usage and tracked campaign state")
    p.add_argument("--survey-id", default="")
    p.add_argument("--campaign-group-id", default="")
    p.set_defaults(func=cmd_ads_status)

    p = sub.add_parser("ads-stop", help="Stop tracked paid ads campaign intents")
    p.add_argument("--survey-id", default="")
    p.add_argument("--campaign-group-id", default="")
    p.add_argument("--platform", choices=["google", "meta"], default="")
    p.set_defaults(func=cmd_ads_stop)

    p = sub.add_parser("responses", help="Fetch survey responses as JSON")
    p.add_argument("survey_id")
    p.add_argument("--status", default="completed")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--per_page", type=int, default=50)
    p.set_defaults(func=cmd_responses)

    p = sub.add_parser("export", help="Export responses as CSV or Excel")
    p.add_argument("survey_id")
    p.add_argument("--format", choices=["csv", "xlsx"], default="csv")
    p.add_argument("--output")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("wizard", help="Interactive flow: generate -> preview -> confirm/edit -> publish")
    p.add_argument("topic")
    p.add_argument("--audience")
    p.add_argument("--count", type=int, default=6)
    p.add_argument("--language", default="auto")
    p.set_defaults(func=cmd_wizard)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
