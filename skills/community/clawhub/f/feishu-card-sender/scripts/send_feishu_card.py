#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import uuid
import mimetypes
from pathlib import Path
from urllib import request, error
from card_snapshot_store import save_snapshot


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "assets" / "templates"
RULES_DIR = ROOT / "assets" / "rules"
OPENCLAW_CONFIG = Path("/root/.openclaw/openclaw.json")


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_kv_pairs(items):
    data = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"Invalid --var '{item}', expected key=value")
        k, v = item.split("=", 1)
        data[k.strip()] = v
    return data


def parse_vars_file(path):
    data = {}
    if not path:
        return data
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"vars file not found: {path}")

    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.lstrip()
    return data


def render_template(text, variables):
    pattern = re.compile(r"\$\{([a-zA-Z0-9_\-\.]+)\}")

    def repl(match):
        key = match.group(1)
        return variables.get(key, match.group(0))

    return pattern.sub(repl, text)


def load_rules(template_name=None):
    if not template_name:
        return []
    p = RULES_DIR / f"{template_name}.rules.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _selector_match(element, selector):
    if not isinstance(element, dict) or not isinstance(selector, dict):
        return False

    tag = selector.get("tag")
    if tag and element.get("tag") != tag:
        return False

    content_contains = selector.get("contentContains")
    if content_contains is not None:
        if content_contains not in str(element.get("content", "")):
            return False

    text_contains = selector.get("textContains")
    if text_contains is not None:
        txt = ""
        text_obj = element.get("text")
        if isinstance(text_obj, dict):
            txt = str(text_obj.get("content", ""))
        if text_contains not in txt:
            return False

    return True


def _is_blankish(value):
    if value is None:
        return True
    s = str(value)
    if not s:
        return True
    # Remove common quotes/symbol wrappers and all unicode whitespaces
    compact = re.sub(r"[\s\"'“”‘’「」『』]+", "", s, flags=re.UNICODE)
    return compact == ""


def apply_rules(template_text, variables, rules):
    try:
        obj = json.loads(template_text)
    except Exception:
        return template_text

    if not rules:
        return template_text

    # pass-1: variable level rules
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        action = rule.get("action")
        field = rule.get("field")

        if action == "default_value":
            if _is_blankish(variables.get(field)):
                variables[field] = str(rule.get("value", ""))

        elif action == "require_non_empty":
            if _is_blankish(variables.get(field)):
                msg = rule.get("message") or f"required field empty: {field}"
                raise ValueError(msg)

    # pass-2: element pruning rules
    body = obj.get("body") if isinstance(obj, dict) else None
    elements = body.get("elements") if isinstance(body, dict) else None
    if not isinstance(elements, list):
        return json.dumps(obj, ensure_ascii=False)

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        action = rule.get("action")
        selector = rule.get("selector") or {}
        field = rule.get("field")

        if action == "remove_when_empty":
            if not _is_blankish(variables.get(field)):
                continue
            elements = [el for el in elements if not _selector_match(el, selector)]

        elif action == "remove_when_missing":
            if variables.get(field):
                continue
            elements = [el for el in elements if not _selector_match(el, selector)]

    body["elements"] = elements
    return json.dumps(obj, ensure_ascii=False)


def _coerce_common_types(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            vv = _coerce_common_types(v)
            if k in ("disabled",) and isinstance(vv, str):
                lv = vv.strip().lower()
                if lv == "true":
                    vv = True
                elif lv == "false":
                    vv = False
            out[k] = vv
        return out
    if isinstance(node, list):
        return [_coerce_common_types(x) for x in node]
    return node


def post_json(url, payload, headers=None):
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except error.HTTPError as ex:
        body = ex.read().decode("utf-8", errors="replace")
        return ex.code, body


def upload_image_bytes(token, image_bytes, filename="poster.jpg"):
    boundary = f"----OpenClawBoundary{uuid.uuid4().hex}"
    crlf = "\r\n"

    file_content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    parts = []
    parts.append((f"--{boundary}{crlf}").encode("utf-8"))
    parts.append((f'Content-Disposition: form-data; name="image_type"{crlf}{crlf}message{crlf}').encode("utf-8"))

    parts.append((f"--{boundary}{crlf}").encode("utf-8"))
    parts.append(
        (
            f'Content-Disposition: form-data; name="image"; filename="{filename}"{crlf}'
            f"Content-Type: {file_content_type}{crlf}{crlf}"
        ).encode("utf-8")
    )
    parts.append(image_bytes)
    parts.append(crlf.encode("utf-8"))
    parts.append((f"--{boundary}--{crlf}").encode("utf-8"))

    body = b"".join(parts)
    req = request.Request("https://open.feishu.cn/open-apis/im/v1/images", data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw)
            if resp.status >= 400 or data.get("code") != 0:
                raise RuntimeError(f"upload image failed: status={resp.status}, body={raw}")
            image_key = ((data.get("data") or {}).get("image_key"))
            if not image_key:
                raise RuntimeError(f"upload image succeeded but image_key missing: body={raw}")
            return image_key
    except error.HTTPError as ex:
        raw = ex.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"upload image failed: status={ex.code}, body={raw}")


def get_tenant_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    status, body = post_json(url, {"app_id": app_id, "app_secret": app_secret})
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise RuntimeError(f"token response is not json, status={status}, body={body[:500]}")

    if status >= 400 or data.get("code") != 0:
        raise RuntimeError(f"get token failed: status={status}, body={body}")

    token = data.get("tenant_access_token")
    if not token:
        raise RuntimeError(f"tenant_access_token missing: body={body}")
    return token


def get_session_account_id():
    """Best-effort read account_id from OpenClaw runtime env."""
    for k in (
        "OPENCLAW_ACCOUNT_ID",
        "OPENCLAW_INBOUND_ACCOUNT_ID",
        "ACCOUNT_ID",
    ):
        v = os.getenv(k)
        if v:
            return v
    return None


def load_openclaw_feishu_credentials(account_id=None, config_path=None):
    cfg_path = Path(config_path) if config_path else OPENCLAW_CONFIG
    if not cfg_path.exists():
        return None, None

    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        accounts = (((cfg.get("channels") or {}).get("feishu") or {}).get("accounts") or [])
    except Exception:
        return None, None

    if not accounts:
        return None, None

    target = None
    if account_id is not None:
        # 1) match by configured account id (e.g. default/dev-bot)
        for a in accounts:
            if str(a.get("id")) == str(account_id):
                target = a
                break
        # 2) if numeric, match by index (inbound account_id is often "0"/"1")
        if target is None and str(account_id).isdigit():
            idx = int(str(account_id))
            if 0 <= idx < len(accounts):
                target = accounts[idx]
    if target is None:
        target = accounts[0]

    return target.get("appId"), target.get("appSecret")


def load_template(template_name=None, template_file=None):
    if template_file:
        p = Path(template_file)
    else:
        p = TEMPLATE_DIR / f"{template_name}.json"

    if not p.exists():
        raise FileNotFoundError(f"template not found: {p}")
    return p.read_text(encoding="utf-8"), p


def list_templates():
    if not TEMPLATE_DIR.exists():
        print("(no templates)")
        return
    files = sorted(TEMPLATE_DIR.glob("*.json"))
    if not files:
        print("(no templates)")
        return
    for f in files:
        print(f.stem)


def main():
    parser = argparse.ArgumentParser(description="Send Feishu interactive card from template")
    parser.add_argument("--template", help="template name in assets/templates, without .json")
    parser.add_argument("--template-file", help="absolute/relative path to template json")
    parser.add_argument("--list-templates", action="store_true", help="list built-in templates")

    parser.add_argument("--receive-id", help="open_id/user_id/chat_id")
    parser.add_argument("--receive-id-type", default="open_id", choices=["open_id", "user_id", "chat_id", "union_id"], help="default: open_id")

    parser.add_argument("--vars-file", help="env-like KEY=VALUE file")
    parser.add_argument("--var", action="append", help="inline variable key=value, repeatable")
    parser.add_argument("--poster-url", help="download image from URL, upload to Feishu, and fill poster_img_key")
    parser.add_argument("--poster-file", help="read local image file, upload to Feishu, and fill poster_img_key")

    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID"))
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET"))
    parser.add_argument("--account-id", help="OpenClaw feishu account id; use 'current' to auto-read from session context")
    parser.add_argument("--config", help="OpenClaw config path (default: /root/.openclaw/openclaw.json)")
    parser.add_argument("--dry-run", action="store_true", help="render and validate only, do not send")

    args = parser.parse_args()

    if args.list_templates:
        list_templates()
        return 0

    if not args.template and not args.template_file:
        eprint("ERROR: --template or --template-file is required")
        return 2

    if not args.receive_id:
        eprint("ERROR: --receive-id is required")
        return 2

    app_id, app_secret = args.app_id, args.app_secret
    account_id = args.account_id
    if account_id == "current":
        account_id = get_session_account_id()

    if not app_id or not app_secret:
        cfg_app_id, cfg_app_secret = load_openclaw_feishu_credentials(account_id, args.config)
        app_id = app_id or cfg_app_id
        app_secret = app_secret or cfg_app_secret

    if not app_id or not app_secret:
        eprint("ERROR: app credentials missing; set FEISHU_APP_ID/FEISHU_APP_SECRET, pass --app-id/--app-secret, or use --account-id with OpenClaw config")
        return 2

    try:
        raw_template, template_path = load_template(args.template, args.template_file)
        file_vars = parse_vars_file(args.vars_file)
        cli_vars = parse_kv_pairs(args.var)
        variables = {**file_vars, **cli_vars}
        if not (variables.get("card_key") or "").strip():
            variables["card_key"] = uuid.uuid4().hex

        token = get_tenant_token(app_id, app_secret)

        # Optional: upload poster first and inject poster_img_key
        if args.poster_url or args.poster_file:
            if args.poster_url:
                req = request.Request(args.poster_url, headers={"User-Agent": "Mozilla/5.0 OpenClaw/feishu-card-sender"})
                with request.urlopen(req, timeout=30) as resp:
                    image_bytes = resp.read()
                filename = Path(args.poster_url.split("?")[0]).name or "poster.jpg"
            else:
                p = Path(args.poster_file)
                if not p.exists():
                    raise FileNotFoundError(f"poster file not found: {args.poster_file}")
                image_bytes = p.read_bytes()
                filename = p.name

            image_key = upload_image_bytes(token, image_bytes, filename=filename)
            variables["poster_img_key"] = image_key

        rules = load_rules(args.template)
        ruled_template = apply_rules(raw_template, variables, rules)
        rendered = render_template(ruled_template, variables)

        # validate + normalize common types (e.g. "disabled": "false" -> false)
        rendered_obj = json.loads(rendered)
        rendered_obj = _coerce_common_types(rendered_obj)
        rendered = json.dumps(rendered_obj, ensure_ascii=False)

        if args.dry_run:
            print(f"template: {template_path}")
            print("dry_run: true")
            print(f"rendered_size: {len(rendered)}")
            print(rendered)
            return 0

        send_url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={args.receive_id_type}"
        payload = {
            "receive_id": args.receive_id,
            "msg_type": "interactive",
            "content": rendered,
        }
        status, body = post_json(send_url, payload, headers={"Authorization": f"Bearer {token}"})

        print(f"template: {template_path}")
        print(f"status: {status}")
        print(f"response: {body}")

        data = json.loads(body)
        if variables.get("poster_img_key"):
            print(f"poster_img_key: {variables.get('poster_img_key')}")
        if status >= 400 or data.get("code") != 0:
            return 1
        msg_id = (data.get("data") or {}).get("message_id")
        if msg_id:
            print(f"message_id: {msg_id}")

        # snapshot for delayed card update workflow
        try:
            save_snapshot(
                card_key=variables.get("card_key"),
                message_id=msg_id,
                receive_id=args.receive_id,
                account_id=str(account_id) if account_id is not None else None,
                media_type=variables.get("media_type"),
                tmdb_id=str(variables.get("tmdb_id")) if variables.get("tmdb_id") is not None else None,
                title=variables.get("title"),
                raw_card_json=rendered,
            )
        except Exception:
            pass
        return 0
    except Exception as ex:
        eprint(f"ERROR: {ex}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
