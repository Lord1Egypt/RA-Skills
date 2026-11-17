#!/usr/bin/env python3
"""ABS Skill command line: lets an AI agent use ABS (AI Business System) with the user's access token.

No third-party packages; Python 3.8+. Run `python3 abs.py --help`.

Where settings come from (first match wins):
  token     --token, env ABS_TOKEN, the user's config file (written by `login`)
  base URL  --base-url, env ABS_BASE_URL, the user's config file, config.json shipped with this skill
The user's config file is ~/.config/abs-business-system/config.json (Windows: %APPDATA%),
readable only by the user.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

SKILL = "abs-business-system"
VERSION = "1.3.0"
TOKEN_PREFIX = "abs_pat_"
SKILL_DIR = Path(__file__).resolve().parent.parent
CJK = re.compile(r"[㐀-鿿]")
TIMEOUT_FAST, TIMEOUT_SLOW = 60, 180  # plans and diagnoses run AI models on the server
NO_TOKEN = (
    "`search` works without a token. To read whole tool cards, ask ABS, see courses, plan or diagnose, "
    "ask the user to create an access token in ABS → Personal Settings → Access tokens "
    "(个人设置 → 访问令牌), then run `login <token>`."
)


class AbsError(Exception):
    def __init__(self, message: str, code: int = 3):
        super().__init__(message)
        self.code = code


# ---------------------------------------------------------------- settings


def config_path() -> Path:
    if os.name == "nt" and os.environ.get("APPDATA"):
        root = Path(os.environ["APPDATA"])
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return root / SKILL / "config.json"


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_user_config(data: dict[str, Any]) -> Path:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def resolve(args: argparse.Namespace) -> tuple[str, str]:
    """(base_url, token) from flags, environment, the user's config, then the bundled config."""
    user = read_json(config_path())
    bundled = read_json(SKILL_DIR / "config.json")
    base = (
        getattr(args, "base_url", None)
        or os.environ.get("ABS_BASE_URL")
        or user.get("base_url")
        or bundled.get("base_url")
        or ""
    )
    token = getattr(args, "token", None) or os.environ.get("ABS_TOKEN") or user.get("token") or ""
    return base.rstrip("/"), token.strip()


def mask(token: str) -> str:
    return token[: len(TOKEN_PREFIX) + 4] + "…" if token else "(none)"


def pick_lang(flag: str, *texts: str) -> str:
    if flag in ("zh", "en"):
        return flag
    return "zh" if any(CJK.search(t or "") for t in texts) else "en"


# ---------------------------------------------------------------- HTTP


def call(
    base: str,
    token: str,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = TIMEOUT_FAST,
    guest: bool = False,
) -> dict[str, Any]:
    raw = fetch(
        base,
        token,
        method,
        path,
        params=params,
        body=body,
        timeout=timeout,
        accept="application/json",
        guest=guest,
    )
    return json.loads(raw.decode("utf-8") or "{}")


def fetch(
    base: str,
    token: str,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = TIMEOUT_FAST,
    accept: str = "*/*",
    guest: bool = False,
) -> bytes:
    """guest=True: without a token the call goes out anonymously (only `search` allows that)."""
    if not base:
        raise AbsError("No ABS site address. Run `login <token> --base-url https://…`.", 1)
    if not token and not guest:
        raise AbsError(NO_TOKEN, 2)
    url = f"{base}/api/agent/v1{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", accept)
    request.add_header("User-Agent", f"abs-skill/{VERSION}")
    if data is not None:
        request.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise AbsError(explain(exc), 2 if exc.code == 401 else 3) from None
    except urllib.error.URLError as exc:
        raise AbsError(f"Cannot reach ABS at {base}: {exc.reason}") from None


def explain(exc: urllib.error.HTTPError) -> str:
    try:
        detail = json.loads(exc.read().decode("utf-8")).get("detail")
    except (ValueError, AttributeError, OSError):
        detail = None
    hints = {
        401: "The access token is invalid, revoked or expired. Ask the user for a new token "
        "(ABS → Personal Settings → Access tokens) and run `login <token>` again.",
        402: "This ABS account is out of credits for that step. Tell the user what it would cost and let them "
        "top up or upgrade in ABS; do not retry in a loop. Searching has a daily free allowance — "
        "search with intent rather than sweeping the library.",
        403: "This ABS account is not allowed to do that (read-only accounts cannot create plans).",
        404: "Not found in ABS (or not visible to this account).",
        413: "The file is too large for ABS.",
        429: "Too many calls in a short time. Wait a minute and retry. Without a token, searches are also "
        "capped per day: connect an access token to search under the user's own account.",
        503: "The ABS AI model is temporarily unavailable. search, card and courses still work.",
    }
    parts = [f"HTTP {exc.code}", hints.get(exc.code, ""), f"ABS says: {detail}" if detail else ""]
    return " ".join(p for p in parts if p)


# ---------------------------------------------------------------- output


def tags(item: dict[str, Any]) -> str:
    """出处标签：非丹纳赫件、规则的口径类别。回答里按它标注，不要一律写「已知」。"""
    found = [str(t) for t in (item.get("provenance_label"), item.get("status_label")) if t]
    return f" [{' · '.join(found)}]" if found else ""


def sources_block(sources: list[dict[str, Any]], lang: str) -> str:
    if not sources:
        return ""
    head = "来源" if lang == "zh" else "Sources"
    lines = [
        f"[{s.get('ref') or i}] {s.get('title')}{tags(s)} — {s.get('url')}" for i, s in enumerate(sources, 1)
    ]
    return f"\n\n{head}:\n" + "\n".join(lines)


def pages_block(pages: list[dict[str, Any]], lang: str) -> list[str]:
    """能取原页核对的地方；用 `page <pdf> <n>` 取图。"""
    out = []
    for g in pages or []:
        check = f" · {g.get('check')}" if g.get("check") else ""
        topic = f" — {g.get('topic')}" if g.get("topic") else ""
        out.append(f"- {g.get('pdf')} p{g.get('pages')}{topic}{check}")
    return out


def show(result: dict[str, Any], args: argparse.Namespace, text: str) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else text)


# ---------------------------------------------------------------- commands


def cmd_login(args: argparse.Namespace) -> None:
    token = args.token_value.strip()
    if not token.startswith(TOKEN_PREFIX):
        raise AbsError(
            f"That does not look like an ABS access token (it should start with {TOKEN_PREFIX}).", 1
        )
    base, _ = resolve(args)
    me = call(base, token, "GET", "/me")
    path = save_user_config({"base_url": base, "token": token})
    user = me.get("user") or {}
    print(
        f"Connected to {me.get('site') or base} as {user.get('display_name')} ({user.get('role')}). "
        f"Token {mask(token)} saved to {path} (only you can read it)."
    )


def cmd_logout(args: argparse.Namespace) -> None:
    data = read_json(config_path())
    data.pop("token", None)
    save_user_config(data)
    print(
        "Token removed from this computer. To disable it everywhere, "
        "revoke it in ABS → Personal Settings → Access tokens."
    )


def cmd_whoami(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    if not token:
        # 没有令牌不算出错：检索照样能用，告诉 Agent 能做什么、还差什么
        show(
            {"site": base, "signed_in": False, "can": {"search": True}},
            args,
            f"ABS site: {base}\nNot connected to an ABS account yet (no access token).\n{NO_TOKEN}",
        )
        return
    me = call(base, token, "GET", "/me")
    user, info, can = me.get("user") or {}, me.get("token") or {}, me.get("can") or {}
    allowed = ", ".join(k for k, v in can.items() if v)
    text = (
        f"ABS site: {me.get('site') or base}\n"
        f"Account: {user.get('display_name')} ({user.get('username')}, {user.get('role')})"
        + (f", account expires {user.get('expires_at')}" if user.get("expires_at") else "")
        + f"\nToken: {info.get('name')} {info.get('prefix')}…, expires {info.get('expires_at') or 'never'}"
        + f"\nCan: {allowed}"
    )
    show(me, args, text)


def cmd_search(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang, args.query)
    out = call(
        base, token, "GET", "/search", params={"q": args.query, "limit": args.limit, "lang": lang}, guest=True
    )
    rows = out.get("results") or []
    if not rows:
        text = (
            "ABS 知识库里没有找到相关内容。"
            if lang == "zh"
            else "Nothing relevant in the ABS knowledge base."
        )
    else:
        text = "\n".join(
            f"{i}. [{r.get('kind')}] {r.get('title')}{tags(r)} — {r.get('url')}\n   {r.get('excerpt')}"
            for i, r in enumerate(rows, 1)
        )
    if out.get("note"):
        text += f"\n\n{out['note']}"
    show(out, args, text)


def cmd_ask(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang, args.question)
    out = call(
        base, token, "POST", "/ask", body={"question": args.question, "lang": lang}, timeout=TIMEOUT_SLOW
    )
    show(out, args, (out.get("answer") or "") + sources_block(out.get("sources") or [], lang))


def cmd_card(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang)
    out = call(base, token, "GET", f"/cards/{urllib.parse.quote(args.card_id)}", params={"lang": lang})
    zh = lang == "zh"
    parts = [f"# {out.get('name')}{tags(out)}", str(out.get("url"))]
    if out.get("sources"):
        parts.append("\n## " + ("原件出处" if zh else "Original sources"))
        for s in out["sources"]:
            pages = f" p{s['pages']}" if s.get("pages") else ""
            note = f" — {s['note']}" if s.get("note") else ""
            parts.append(f"- {s.get('file')}{pages}{note}")
    if out.get("rules"):
        parts.append("\n## " + ("规则参数与口径类别" if zh else "Rule parameters and their basis"))
        for r in out["rules"]:
            note = f" — {r['note']}" if r.get("note") else ""
            parts.append(
                f"- `{r.get('key')}` = {r.get('value')} [{r.get('status_label') or r.get('status')}]{note}"
            )
    if out.get("pages"):
        parts.append(
            "\n## " + ("可取原页核对（page 命令）" if zh else "Original pages you can fetch (page command)")
        )
        parts += pages_block(out["pages"], lang)
    parts.append("\n" + str(out.get("markdown") or ""))
    show(out, args, "\n".join(parts))


def cmd_courses(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang)
    out = call(base, token, "GET", "/courses", params={"lang": lang})
    lines = []
    for c in out.get("courses") or []:
        progress = c.get("progress") or {}
        lines.append(
            f"- {c.get('title')} (`{c.get('id')}`) — {c.get('lessons')} lessons, "
            f"{progress.get('done', 0)}/{progress.get('total', 0)} done — {c.get('url')}"
        )
    show(out, args, "\n".join(lines))


def cmd_course(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang)
    out = call(base, token, "GET", f"/courses/{urllib.parse.quote(args.course_id)}", params={"lang": lang})
    parts = [f"# {out.get('title')}", str(out.get("url")), str(out.get("summary") or "")]
    for i, lesson in enumerate(out.get("lessons") or [], 1):
        parts.append(f"\n## {i}. {lesson.get('title')} — {lesson.get('url')}")
        if lesson.get("objective"):
            parts.append(f"Objective / 目标: {lesson['objective']}")
        parts += [f"- {p}" for p in lesson.get("points") or []]
        if lesson.get("task"):
            parts.append(f"Task / 任务: {lesson['task']}")
        if lesson.get("pages"):
            parts.append(("原页：" if lang == "zh" else "Original pages:"))
            parts += pages_block(lesson["pages"], lang)
        check = lesson.get("check") or {}
        if check.get("question"):
            options = " | ".join(str(o) for o in check.get("options") or [])
            parts.append(f"Check / 检验: {check['question']}" + (f" ({options})" if options else ""))
    show(out, args, "\n".join(parts))


def cmd_plan(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang, args.request)
    body = {"question": args.request, "lang": lang, "start_date": args.start}
    out = call(base, token, "POST", "/plans", body=body, timeout=TIMEOUT_SLOW)
    show(out, args, plan_text(out, lang))


def cmd_plan_get(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    out = call(base, token, "GET", f"/plans/{urllib.parse.quote(args.code)}")
    show(out, args, plan_text(out, pick_lang(args.lang, out.get("question") or "")))


def cmd_plan_list(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang)
    out = call(base, token, "GET", "/plans", params={"limit": args.limit})
    lines = [
        f"- {p.get('code')} · {p.get('status')} · {p.get('proposed_at') or ''} · {p.get('question')} — {p.get('url')}"
        for p in out.get("plans") or []
    ]
    empty = "还没有规划。" if lang == "zh" else "No plans yet."
    show(out, args, "\n".join(lines) or empty)


def plan_text(out: dict[str, Any], lang: str) -> str:
    link = out.get("url")
    note = (
        f"\n\n规划书链接：{link}（草稿：在 ABS 里确认提交后才会建项目和任务）"
        if lang == "zh"
        else f"\n\nPlan link: {link} (a draft: review and submit it in ABS to create projects and tasks)"
    )
    if out.get("markdown"):
        return f"{out['markdown']}{note}"
    reason = out.get("no_flow_reason") or ""
    return f"{reason}{note}"


def cmd_diagnose(args: argparse.Namespace) -> None:
    base, token = resolve(args)
    lang = pick_lang(args.lang, args.question)
    body: dict[str, Any] = {
        "question": args.question,
        "company": args.company or "",
        "lang": lang,
        "save": args.save,
    }
    if args.file:
        path = Path(args.file)
        try:
            body["filename"] = path.name
            body["content_base64"] = base64.b64encode(path.read_bytes()).decode("ascii")
        except OSError as exc:
            raise AbsError(f"Cannot read {path}: {exc}", 1) from None
    out = call(base, token, "POST", "/diagnoses", body=body, timeout=TIMEOUT_SLOW)
    text = (out.get("answer") or "") + sources_block(out.get("sources") or [], lang)
    if out.get("url"):
        text += f"\n\n{'已保存到诊断记录' if lang == 'zh' else 'Saved to diagnosis records'}: {out['url']}"
    show(out, args, text)


def cmd_page(args: argparse.Namespace) -> None:
    """原件的一页（图片），用来核对 ABS 给的出处。只给单页；每分钟有上限。"""
    base, token = resolve(args)
    data = fetch(base, token, "GET", f"/pages/{urllib.parse.quote(args.pdf)}/{args.page}", accept="image/png")
    target = Path(args.out or f"abs-page-{Path(args.pdf).stem}-p{args.page}.png")
    target.write_bytes(data)
    print(
        f"Saved page {args.page} of {args.pdf} to {target.resolve()} ({len(data)} bytes). Open it to check."
    )


# ---------------------------------------------------------------- entry


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="abs.py", description="Use ABS (AI Business System) from an AI agent.")
    p.add_argument("--version", action="version", version=f"{SKILL} {VERSION}")
    sub = p.add_subparsers(dest="command", required=True)

    def add(name: str, handler, help_text: str, *, lang: bool = True) -> argparse.ArgumentParser:
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("--base-url", dest="base_url", help="ABS site address, e.g. https://www.ucai.net")
        sp.add_argument("--token", help="use this token instead of the saved one")
        sp.add_argument("--json", action="store_true", help="print the raw JSON response")
        if lang:
            sp.add_argument("--lang", choices=("auto", "zh", "en"), default="auto")
        sp.set_defaults(handler=handler)
        return sp

    add("login", cmd_login, "check an access token and save it for this user", lang=False).add_argument(
        "token_value", metavar="TOKEN"
    )
    add("logout", cmd_logout, "remove the saved token from this computer", lang=False)
    add("whoami", cmd_whoami, "show the connected site, account and what it can do", lang=False)
    add("search", cmd_search, "search the ABS knowledge base").add_argument("query")
    sub.choices["search"].add_argument("--limit", type=int, default=8)
    add("ask", cmd_ask, "ask ABS; the answer cites ABS sources").add_argument("question")
    add("card", cmd_card, "read a whole tool card").add_argument("card_id")
    add("courses", cmd_courses, "list ABS courses and your progress")
    add("course", cmd_course, "read a course: lessons, objectives, tasks, checks").add_argument("course_id")
    plan = add("plan", cmd_plan, "turn one sentence into a scheduled plan (saved as a draft)")
    plan.add_argument("request")
    plan.add_argument("--start", help="start date YYYY-MM-DD (default: next Monday or a date in the request)")
    add("plan-get", cmd_plan_get, "read a plan you created").add_argument("code")
    add("plan-list", cmd_plan_list, "list the plans you created, newest first").add_argument(
        "--limit", type=int, default=20
    )
    page = add("page", cmd_page, "save one original source page as an image, to check a citation", lang=False)
    page.add_argument("pdf", help="the pdf name from a card's or lesson's pages list")
    page.add_argument("page", type=int)
    page.add_argument("--out", help="where to save the PNG (default: ./abs-page-<name>-p<n>.png)")
    diag = add("diagnose", cmd_diagnose, "diagnose a question, operations data, a document or a photo")
    diag.add_argument("question", nargs="?", default="")
    diag.add_argument("--file", help="xlsx, csv, pdf, docx, txt, md or an image (up to 5 MB)")
    diag.add_argument("--company", help="company or scene, e.g. 'Assembly line 1'")
    diag.add_argument("--save", action="store_true", help="keep it in the user's diagnosis records")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        args.handler(args)
    except AbsError as exc:
        print(f"ABS: {exc}", file=sys.stderr)
        return exc.code
    return 0


if __name__ == "__main__":
    sys.exit(main())
