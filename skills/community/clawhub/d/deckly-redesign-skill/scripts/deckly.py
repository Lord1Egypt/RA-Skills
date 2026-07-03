#!/usr/bin/env python3
"""Deckly deck-redesign client. Standard library only (no pip install)."""
import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

DEFAULT_BASE = os.environ.get("DECKLY_API_BASE", "https://deckly.art").rstrip("/")
TEXT_STYLE_DEFAULT = "text_style:minimalist_corporate"
# Browser-like UA: deckly.art is behind Cloudflare, which 403s default urllib UA.
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

EXTRACT_DONE = {"extracted", "analyzed", "parsed"}
TERMINAL_OK = {"completed", "partial_completed", "preview_completed",
               "preview_partial_completed", "free_previewed_completed",
               "free_previewed_partial_completed"}
TERMINAL_FAIL = {"failed", "cancelled", "preview_failed", "free_previewed_failed"}
PREVIEW_STATES = {"preview_completed", "preview_partial_completed",
                  "free_previewed_completed", "free_previewed_partial_completed"}


class DecklyError(Exception):
    pass


def _config_path():
    return os.environ.get("DECKLY_CONFIG",
                          os.path.join(os.path.expanduser("~"), ".deckly", "credentials"))


def _load_config():
    try:
        with open(_config_path()) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_config(data):
    path = _config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass


def _token(base):
    tok = os.environ.get("DECKLY_TOKEN") or os.environ.get("DECKLY_API_KEY")
    if tok:
        return tok
    cfg = _load_config()
    if cfg.get("api_key"):
        return cfg["api_key"]
    email = os.environ.get("DECKLY_EMAIL")
    password = os.environ.get("DECKLY_PASSWORD")
    if email and password:
        data = _request(base, "POST", "/auth/login",
                        body={"email": email, "password": password}, auth=False)
        return data["access_token"]
    raise DecklyError(
        "No credentials. Run 'signup' + 'verify' to register in-conversation, "
        "or 'login' if you already have a Deckly account. "
        "(Or set DECKLY_TOKEN / DECKLY_API_KEY, or DECKLY_EMAIL + DECKLY_PASSWORD.)")


def _mint_key_from_jwt(base, jwt, email):
    """Create a dk_ API key with a JWT and persist it for future runs."""
    created = _request(base, "POST", "/auth/api-keys",
                       body={"name": "deckly-skill"}, auth=False,
                       headers={"Authorization": "Bearer " + jwt})
    cfg = _load_config()
    cfg["api_key"] = created["api_key"]
    cfg["email"] = email
    cfg["base"] = base
    _save_config(cfg)
    return created["api_key"]


_CACHED_TOKEN = {}


def _auth_header(base):
    if base not in _CACHED_TOKEN:
        _CACHED_TOKEN[base] = _token(base)
    return {"Authorization": "Bearer " + _CACHED_TOKEN[base]}


def _request(base, method, path, body=None, auth=True, raw=False, headers=None):
    url = base + path
    hdrs = {"User-Agent": USER_AGENT}
    hdrs.update(headers or {})
    if auth:
        hdrs.update(_auth_header(base))
    payload = None
    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=payload, method=method, headers=hdrs)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            if raw:
                return content
            if not content:
                return {}
            return json.loads(content)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("detail", detail)
        except Exception:
            pass
        raise DecklyError("HTTP %s on %s %s: %s" % (e.code, method, path, detail))
    except urllib.error.URLError as e:
        raise DecklyError("Network error on %s %s: %s" % (method, path, e.reason))


def _upload(base, project_id, file_path):
    if not os.path.isfile(file_path):
        raise DecklyError("File not found: %s" % file_path)
    boundary = "----deckly" + uuid.uuid4().hex
    fname = os.path.basename(file_path)
    ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
    with open(file_path, "rb") as f:
        data = f.read()
    body = b"".join([
        ("--%s\r\n" % boundary).encode(),
        ('Content-Disposition: form-data; name="file"; filename="%s"\r\n' % fname).encode(),
        ("Content-Type: %s\r\n\r\n" % ctype).encode(),
        data,
        ("\r\n--%s--\r\n" % boundary).encode(),
    ])
    hdrs = {"User-Agent": USER_AGENT}
    hdrs.update(_auth_header(base))
    hdrs["Content-Type"] = "multipart/form-data; boundary=%s" % boundary
    req = urllib.request.Request(base + "/projects/%s/upload" % project_id,
                                 data=body, method="POST", headers=hdrs)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise DecklyError("Upload failed (HTTP %s): %s" %
                          (e.code, e.read().decode("utf-8", "replace")))


def _poll_status(base, project_id, done_states, fail_states, timeout, interval, label):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        st = _request(base, "GET", "/projects/%s/status" % project_id)
        status = st.get("status")
        if status != last:
            sys.stderr.write("[%s] status=%s\n" % (label, status))
            sys.stderr.flush()
            last = status
        if status in fail_states:
            detail = st.get("error_message")
            if not detail:
                try:
                    errs = [s.get("error_message") for s in
                            _request(base, "GET", "/projects/%s/slides" % project_id)
                            if s.get("error_message")]
                    detail = "; ".join(dict.fromkeys(errs)) if errs else status
                except Exception:
                    detail = status
            raise DecklyError("%s failed: %s" % (label, detail))
        if status in done_states:
            return st
        time.sleep(interval)
    raise DecklyError("%s timed out after %ss (last status=%s)" % (label, timeout, last))


def _slide_record(base, project_id, idx):
    for s in _request(base, "GET", "/projects/%s/slides" % project_id):
        if s.get("index") == idx:
            return s
    return None


def _poll_slide(base, project_id, idx, prev_updated, timeout, interval, label):
    # Partial updates keep project status == "completed", so poll the slide itself.
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        s = _slide_record(base, project_id, idx)
        status = s.get("status") if s else None
        if status != last:
            sys.stderr.write("[%s] slide %s status=%s\n" % (label, idx, status))
            sys.stderr.flush()
            last = status
        if status == "failed":
            raise DecklyError("%s failed on slide %s: %s" %
                              (label, idx, (s or {}).get("error_message") or "unknown"))
        if status == "completed" and s.get("updated_at") != prev_updated:
            return s
        time.sleep(interval)
    raise DecklyError("%s timed out after %ss (last slide status=%s)" % (label, timeout, last))


def _abs_url(base, u):
    if not u:
        return u
    return u if u.startswith("http") else base + u


def cmd_signup(base, args):
    try:
        _request(base, "POST", "/auth/register",
                 body={"email": args.email, "password": args.password}, auth=False)
    except DecklyError as e:
        msg = str(e)
        if "already exists" in msg:
            print(json.dumps({
                "status": "account_exists",
                "email": args.email,
                "message": "An account with this email already exists. It will use your "
                           "EXISTING Deckly account. Provide your password and run: "
                           "login --email %s --password <your password>" % args.email,
            }, indent=2))
            return
        raise
    print(json.dumps({
        "status": "code_sent",
        "email": args.email,
        "message": "A 6-digit verification code was sent to your email. "
                   "Run: verify --email %s --code <code> --password %s" % (args.email, args.password),
    }, indent=2))


def cmd_verify(base, args):
    data = _request(base, "POST", "/auth/verify-email",
                    body={"email": args.email, "code": args.code}, auth=False)
    key = _mint_key_from_jwt(base, data["access_token"], args.email)
    print(json.dumps({
        "status": "registered",
        "email": args.email,
        "api_key_prefix": key[:11],
        "saved_to": _config_path(),
        "message": "Account verified and API key saved. You can now run analyze/redesign directly.",
    }, indent=2))


def cmd_login(base, args):
    data = _request(base, "POST", "/auth/login",
                    body={"email": args.email, "password": args.password}, auth=False)
    key = _mint_key_from_jwt(base, data["access_token"], args.email)
    print(json.dumps({
        "status": "logged_in",
        "email": args.email,
        "api_key_prefix": key[:11],
        "saved_to": _config_path(),
        "message": "Using your existing Deckly account. A new API key was created and saved "
                   "for this agent (manage keys at /auth/api-keys).",
    }, indent=2))


def cmd_me(base, args):
    out = _request(base, "GET", "/auth/me")
    print(json.dumps({
        "email": out.get("email"),
        "credit_balance": out.get("credit_balance"),
        "subscription_credits": out.get("subscription_credits"),
        "top_up_credits": out.get("top_up_credits"),
        "free_preview_available": not out.get("has_used_free_preview"),
    }, indent=2))


def cmd_styles(base, args):
    templates = _request(base, "GET", "/templates", auth=False)
    text_styles = _request(base, "GET", "/text-styles", auth=False)
    result = {
        "text_styles": [
            {"style_preset": "text_style:" + s["id"], "name": s.get("name"),
             "description": s.get("description")}
            for s in text_styles
        ],
        "template_themes": [
            {"style_preset": t["id"], "name": t.get("name"),
             "description": t.get("description"),
             "thumbnail_url": _abs_url(base, t.get("thumbnail_url"))}
            for t in templates
        ],
    }
    print(json.dumps(result, indent=2))


def _parse_slides(s):
    if not s:
        return None
    out = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def cmd_analyze(base, args):
    proj = _request(base, "POST", "/projects", body={"name": args.name or os.path.basename(args.file)})
    pid = proj["id"]
    sys.stderr.write("[analyze] project_id=%s\n" % pid)
    _upload(base, pid, args.file)
    _request(base, "POST", "/projects/%s/analyze" % pid)
    _poll_status(base, pid, EXTRACT_DONE, TERMINAL_FAIL, args.timeout, 2, "extract")
    analysis = _request(base, "GET", "/projects/%s/analysis" % pid)
    me = _request(base, "GET", "/auth/me")
    print(json.dumps({
        "project_id": pid,
        "presentation_intent": analysis.get("presentation_intent"),
        "audience": analysis.get("audience"),
        "language": analysis.get("language"),
        "slide_count": len(analysis.get("slides", [])),
        "recommended_slide_indices": analysis.get("recommended_slide_indices"),
        "slides": analysis.get("slides"),
        "free_preview_available": not me.get("has_used_free_preview"),
        "credit_balance": me.get("credit_balance"),
    }, indent=2))


def cmd_quote(base, args):
    out = _request(base, "POST", "/projects/%s/quote" % args.project_id,
                   body={"slide_indices": _parse_slides(args.slides) or []})
    print(json.dumps(out, indent=2))


def _print_slides(base, project_id):
    slides = _request(base, "GET", "/projects/%s/slides" % project_id)
    rows = [{
        "index": s.get("index"),
        "status": s.get("status"),
        "redesigned_url": _abs_url(base, s.get("redesigned_url")),
        "error_message": s.get("error_message"),
    } for s in slides]
    print(json.dumps({"project_id": project_id, "slides": rows}, indent=2))


def cmd_redesign(base, args):
    slides = _parse_slides(args.slides)
    if not slides:
        raise DecklyError("--slides is required (e.g. --slides 1,2,3 or 1-10)")
    body = {
        "slide_indices": slides,
        "style_preset": args.style or TEXT_STYLE_DEFAULT,
        "force_regenerate": args.force,
        "is_partial_update": False,
        "custom_prompt": args.custom,
        "reference_slide_index": args.reference,
        "revert_to_previous": False,
    }
    res = _request(base, "POST", "/projects/%s/redesign" % args.project_id, body=body)
    sys.stderr.write("[redesign] queued: %s\n" % json.dumps(res))
    _poll_status(base, args.project_id, TERMINAL_OK, TERMINAL_FAIL,
                 args.timeout, 5, "redesign")
    _print_slides(base, args.project_id)


def cmd_finetune(base, args):
    body = {
        "slide_indices": [args.slide],
        "style_preset": "modern",
        "force_regenerate": True,
        "is_partial_update": True,
        "custom_prompt": args.instruction,
        "reference_slide_index": args.reference,
        "revert_to_previous": False,
    }
    prev = _slide_record(base, args.project_id, args.slide)
    prev_updated = prev.get("updated_at") if prev else None
    res = _request(base, "POST", "/projects/%s/redesign" % args.project_id, body=body)
    sys.stderr.write("[finetune] queued: %s\n" % json.dumps(res))
    _poll_slide(base, args.project_id, args.slide, prev_updated,
                args.timeout, 5, "finetune")
    _print_slides(base, args.project_id)


def cmd_revert(base, args):
    body = {
        "slide_indices": [args.slide],
        "style_preset": "modern",
        "force_regenerate": True,
        "is_partial_update": True,
        "custom_prompt": None,
        "reference_slide_index": None,
        "revert_to_previous": True,
    }
    prev = _slide_record(base, args.project_id, args.slide)
    prev_updated = prev.get("updated_at") if prev else None
    res = _request(base, "POST", "/projects/%s/redesign" % args.project_id, body=body)
    sys.stderr.write("[revert] queued: %s\n" % json.dumps(res))
    _poll_slide(base, args.project_id, args.slide, prev_updated,
                args.timeout, 5, "revert")
    _print_slides(base, args.project_id)


def cmd_versions(base, args):
    out = _request(base, "GET", "/projects/%s/slides/%s/versions" % (args.project_id, args.slide))
    if isinstance(out, dict) and "versions" in out:
        for v in out["versions"]:
            v["url"] = _abs_url(base, v.get("url"))
    print(json.dumps(out, indent=2))


def cmd_select(base, args):
    out = _request(base, "POST", "/projects/%s/slides/%s/versions/select" %
                   (args.project_id, args.slide), body={"path": args.path})
    print(json.dumps(out, indent=2))


def cmd_continue(base, args):
    res = _request(base, "POST", "/projects/%s/continue" % args.project_id)
    sys.stderr.write("[continue] queued: %s\n" % json.dumps(res))
    _poll_status(base, args.project_id, TERMINAL_OK, TERMINAL_FAIL,
                 args.timeout, 5, "continue")
    _print_slides(base, args.project_id)


def cmd_status(base, args):
    print(json.dumps(_request(base, "GET", "/projects/%s/status" % args.project_id), indent=2, default=str))


def cmd_slides(base, args):
    _print_slides(base, args.project_id)


def cmd_download(base, args):
    content = _request(base, "GET", "/projects/%s/download" % args.project_id, raw=True)
    out = args.output or ("deckly_%s.pptx" % args.project_id)
    with open(out, "wb") as f:
        f.write(content)
    print(json.dumps({"saved": os.path.abspath(out), "bytes": len(content)}, indent=2))


def cmd_oneshot(base, args):
    proj = _request(base, "POST", "/projects", body={"name": args.name or os.path.basename(args.file)})
    pid = proj["id"]
    sys.stderr.write("[oneshot] project_id=%s\n" % pid)
    _upload(base, pid, args.file)
    _request(base, "POST", "/projects/%s/analyze" % pid)
    _poll_status(base, pid, EXTRACT_DONE, TERMINAL_FAIL, args.timeout, 2, "extract")
    analysis = _request(base, "GET", "/projects/%s/analysis" % pid)

    slides = _parse_slides(args.slides)
    if not slides:
        slides = analysis.get("recommended_slide_indices") or \
            [s["index"] for s in analysis.get("slides", [])]
    slides = slides[:60]

    body = {
        "slide_indices": slides,
        "style_preset": args.style or TEXT_STYLE_DEFAULT,
        "force_regenerate": False,
        "is_partial_update": False,
        "custom_prompt": args.custom,
        "reference_slide_index": None,
        "revert_to_previous": False,
    }
    res = _request(base, "POST", "/projects/%s/redesign" % pid, body=body)
    sys.stderr.write("[oneshot] redesign queued: %s\n" % json.dumps(res))
    st = _poll_status(base, pid, TERMINAL_OK, TERMINAL_FAIL, args.timeout, 5, "redesign")

    if st.get("status") in PREVIEW_STATES:
        slides_out = _request(base, "GET", "/projects/%s/slides" % pid)
        preview = [{"index": s.get("index"), "status": s.get("status"),
                    "redesigned_url": _abs_url(base, s.get("redesigned_url"))}
                   for s in slides_out]
        if args.preview_only:
            print(json.dumps({"project_id": pid, "preview_only": True,
                              "message": "Free preview ready (3 slides, 0 credits). "
                              "Buy credits, then run: continue <pid> && download <pid>.",
                              "slides": preview}, indent=2))
            return
        quote = _request(base, "POST", "/projects/%s/quote" % pid,
                         body={"slide_indices": slides})
        if not quote.get("can_afford"):
            print(json.dumps({"project_id": pid, "preview_only": True,
                              "needs_credits": quote.get("cost_credits"),
                              "user_balance": quote.get("user_balance"),
                              "message": "Free preview ready (3 slides, 0 credits). "
                              "Full deck needs %s credits but balance is %s. "
                              "Buy credits, then run: continue <pid> && download <pid>."
                              % (quote.get("cost_credits"), quote.get("user_balance")),
                              "slides": preview}, indent=2))
            return
        sys.stderr.write("[oneshot] preview done; paying %s credits to render full deck...\n"
                         % quote.get("cost_credits"))
        _request(base, "POST", "/projects/%s/continue" % pid)
        _poll_status(base, pid, TERMINAL_OK, TERMINAL_FAIL, args.timeout, 5, "continue")

    content = _request(base, "GET", "/projects/%s/download" % pid, raw=True)
    out = args.output or ("deckly_%s.pptx" % pid)
    with open(out, "wb") as f:
        f.write(content)
    print(json.dumps({"project_id": pid, "saved": os.path.abspath(out),
                      "bytes": len(content), "slides": slides}, indent=2))


def build_parser():
    p = argparse.ArgumentParser(prog="deckly", description="Deckly deck redesign client")
    p.add_argument("--base", default=DEFAULT_BASE, help="API base URL (default: %s)" % DEFAULT_BASE)
    p.add_argument("--timeout", type=int, default=1800, help="poll timeout seconds (default 1800)")
    sub = p.add_subparsers(dest="cmd", required=True)

    su = sub.add_parser("signup")
    su.add_argument("--email", required=True)
    su.add_argument("--password", required=True)
    su.set_defaults(func=cmd_signup)

    vf = sub.add_parser("verify")
    vf.add_argument("--email", required=True)
    vf.add_argument("--code", required=True)
    vf.add_argument("--password")
    vf.set_defaults(func=cmd_verify)

    lg = sub.add_parser("login")
    lg.add_argument("--email", required=True)
    lg.add_argument("--password", required=True)
    lg.set_defaults(func=cmd_login)

    sub.add_parser("me").set_defaults(func=cmd_me)
    sub.add_parser("styles").set_defaults(func=cmd_styles)

    a = sub.add_parser("analyze")
    a.add_argument("file")
    a.add_argument("--name")
    a.set_defaults(func=cmd_analyze)

    q = sub.add_parser("quote")
    q.add_argument("project_id")
    q.add_argument("--slides", required=True)
    q.set_defaults(func=cmd_quote)

    r = sub.add_parser("redesign")
    r.add_argument("project_id")
    r.add_argument("--slides", required=True)
    r.add_argument("--style")
    r.add_argument("--custom")
    r.add_argument("--reference", type=int)
    r.add_argument("--force", action="store_true")
    r.set_defaults(func=cmd_redesign)

    f = sub.add_parser("finetune")
    f.add_argument("project_id")
    f.add_argument("--slide", type=int, required=True)
    f.add_argument("--instruction", required=True)
    f.add_argument("--reference", type=int)
    f.set_defaults(func=cmd_finetune)

    rv = sub.add_parser("revert")
    rv.add_argument("project_id")
    rv.add_argument("--slide", type=int, required=True)
    rv.set_defaults(func=cmd_revert)

    v = sub.add_parser("versions")
    v.add_argument("project_id")
    v.add_argument("--slide", type=int, required=True)
    v.set_defaults(func=cmd_versions)

    sl = sub.add_parser("select")
    sl.add_argument("project_id")
    sl.add_argument("--slide", type=int, required=True)
    sl.add_argument("--path", required=True)
    sl.set_defaults(func=cmd_select)

    c = sub.add_parser("continue")
    c.add_argument("project_id")
    c.set_defaults(func=cmd_continue)

    st = sub.add_parser("status")
    st.add_argument("project_id")
    st.set_defaults(func=cmd_status)

    s = sub.add_parser("slides")
    s.add_argument("project_id")
    s.set_defaults(func=cmd_slides)

    d = sub.add_parser("download")
    d.add_argument("project_id")
    d.add_argument("-o", "--output")
    d.set_defaults(func=cmd_download)

    o = sub.add_parser("oneshot")
    o.add_argument("file")
    o.add_argument("--slides")
    o.add_argument("--style")
    o.add_argument("--custom")
    o.add_argument("--name")
    o.add_argument("-o", "--output")
    o.add_argument("--preview-only", action="store_true")
    o.set_defaults(func=cmd_oneshot)

    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args.base.rstrip("/"), args)
    except DecklyError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()
