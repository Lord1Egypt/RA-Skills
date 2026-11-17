#!/usr/bin/env python3
"""
fn2 — a tiny, dependency-free command-line client for the FN2 API.

FN2 (https://fn2.ai) is an AI research platform for stocks, markets, and the
economy. This CLI wraps the public REST API so an agent (or a human) can:

  * research        ask a grounded, sourced question about markets
  * agents          create / schedule / run / manage research agents
  * runs            read an agent run's outcome and full answer
  * models / usage   list available models and check your quota

It uses only the Python 3 standard library — no pip install required.

Auth:
  Set FN2_API_KEY to a key you create for free at FN2. If it isn't set, the CLI
  prints a sign-up link so a new user can get an account + key in a minute.
  Keys look like:  fn2_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Environment:
  FN2_API_KEY    (required) your fn2_... API key
  FN2_API_BASE   (optional) API base URL, default https://fn2.ai/api/v1

Add --json after any command to print the raw API response (handy for agents),
e.g. `fn2 research "…" --json` or `fn2 agents list --json`.
"""

import argparse
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE = "https://fn2.ai/api/v1"
# FN2_SOURCE tags this build's host integration. It is the ONE value that differs
# between the Hermes and OpenClaw editions of this CLI: it rides along on the
# sign-up link (?ref=) so FN2 can route a new user straight to API-key creation,
# and on the User-Agent for telemetry.
FN2_SOURCE = "openclaw"
SIGNUP_URL = "https://fn2.ai/api-keys?ref=" + FN2_SOURCE
USER_AGENT = "fn2-" + FN2_SOURCE + "/1.0 (+https://github.com/fn2ai)"
# Research can run tools server-side, so give it a generous default timeout.
RESEARCH_TIMEOUT = 240
DEFAULT_TIMEOUT = 60

# Inline citation markers the platform embeds, e.g. "{{cite:<uuid>}}". They are
# rendered as footnotes in the web app; in a terminal they are just noise, so we
# strip them from research output unless --raw is passed.
_CITE_RE = re.compile(r"\{\{cite:[^}]*\}\}")
_MULTISPACE_RE = re.compile(r"[ \t]{2,}")


class Fn2Error(Exception):
    """A clean, user-facing error (printed without a Python traceback)."""


def _base() -> str:
    return os.environ.get("FN2_API_BASE", DEFAULT_BASE).rstrip("/")


def _key() -> str:
    key = os.environ.get("FN2_API_KEY", "").strip()
    if not key:
        raise Fn2Error(
            "You're not connected to FN2 yet.\n\n"
            "FN2 is an AI research platform for stocks, markets, and the economy.\n"
            "Create a free account and API key here (takes a minute):\n\n"
            f"    {SIGNUP_URL}\n\n"
            "Then set your key and you're ready:\n\n"
            "    export FN2_API_KEY=fn2_your_key_here"
        )
    if not key.startswith("fn2_"):
        raise Fn2Error(
            "FN2_API_KEY doesn't look like an FN2 key (it should start with 'fn2_').\n"
            f"Create or copy your key here: {SIGNUP_URL}"
        )
    return key


def _build_request(method, path, body=None, accept="application/json"):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(_base() + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + _key())
    req.add_header("Accept", accept)
    req.add_header("User-Agent", USER_AGENT)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    return req


def _http_error(e: urllib.error.HTTPError) -> "Fn2Error":
    """Turn an HTTPError into a clean Fn2Error (callers `raise` the result)."""
    raw = e.read().decode("utf-8", "replace")
    try:
        payload = json.loads(raw)
        if not isinstance(payload, dict):  # a JSON array/string/number is not a body we can index
            payload = {"error": raw.strip() or e.reason}
    except ValueError:
        payload = {"error": raw.strip() or e.reason}
    return Fn2Error(_http_message(e.code, payload))


def request(method: str, path: str, body=None, params=None, timeout=DEFAULT_TIMEOUT):
    """Make an authenticated request and return (status_code, parsed_json|None)."""
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            path += "?" + urllib.parse.urlencode(clean)

    req = _build_request(method, path, body)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raise _http_error(e)
    except (TimeoutError, socket.timeout):  # socket.timeout is distinct on Python < 3.10
        raise Fn2Error(f"Request timed out after {timeout}s.")
    except urllib.error.URLError as e:
        raise Fn2Error(f"Could not reach the FN2 API at {_base()}: {e.reason}")


def _iter_sse(resp):
    """Yield parsed JSON objects from an SSE response.

    Follows the SSE framing: `data:` lines accumulate and an event is dispatched
    on a blank line (and at end of stream), so a multi-line/pretty-printed JSON
    payload is handled, not just one-object-per-line.
    """
    buf = []

    def flush():
        if not buf:
            return None
        payload = "\n".join(buf).strip()
        buf.clear()
        if not payload:
            return None
        try:
            return json.loads(payload)
        except ValueError:
            return None

    for raw in resp:
        line = raw.decode("utf-8", "replace").rstrip("\n").rstrip("\r")
        if line == "":  # blank line terminates an event
            ev = flush()
            if ev is not None:
                yield ev
        elif line.startswith("data:"):
            buf.append(line[len("data:"):].lstrip())
        # other SSE fields (event:, id:, : comments) are ignored
    ev = flush()  # dispatch a trailing event with no final blank line
    if ev is not None:
        yield ev


def _final_from_history(history) -> str:
    """The last assistant turn with real text — this is the clean final answer.

    Tool-using runs emit intermediate assistant turns with null content (the
    tool calls) plus narration chunks; the persisted final turn is the answer.
    """
    for turn in reversed(history or []):
        if turn.get("role") == "assistant":
            content = turn.get("content")
            if isinstance(content, dict):
                content = content.get("text")
            if isinstance(content, str) and content.strip():
                return content
    return ""


def stream_chat(message: str, model=None, timeout=RESEARCH_TIMEOUT):
    """Run a research query over the streaming endpoint.

    FN2's chat is streaming-first. We POST stream=true and prefer the final
    persisted answer from the `done` event's history (clean, no intermediate
    tool narration), falling back to the accumulated text chunks. Returns
    (answer_text, meta) where meta carries model + usage.
    """
    body = {"message": message, "stream": True}
    if model:
        body["model"] = model
    req = _build_request("POST", "/chat/incognito", body, accept="text/event-stream")

    parts, final, meta = [], "", {}
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for ev in _iter_sse(resp):
                etype = ev.get("type")
                if etype == "streaming_content" and ev.get("content_type") == "text":
                    parts.append(ev.get("content", ""))
                elif etype == "error":
                    raise Fn2Error(ev.get("message") or ev.get("error") or "stream error")
                elif etype == "done":
                    meta = {"model": ev.get("model"), "usage": ev.get("usage"),
                            "status": ev.get("status", "success")}
                    final = _final_from_history(ev.get("history"))
    except urllib.error.HTTPError as e:
        raise _http_error(e)
    except (TimeoutError, socket.timeout):  # socket.timeout is distinct on Python < 3.10
        raise Fn2Error(f"Request timed out after {timeout}s.")
    except urllib.error.URLError as e:
        raise Fn2Error(f"Could not reach the FN2 API at {_base()}: {e.reason}")
    return (final or "".join(parts)), meta


def _http_message(code: int, payload) -> str:
    payload = payload if isinstance(payload, dict) else {}
    error = payload.get("error")
    message = payload.get("message")
    # Quota responses use `error` as a machine code and `message` as the useful
    # plan-specific explanation. Other endpoints traditionally put prose in
    # `error`, so preserve that ordering everywhere else.
    msg = (message if code == 429 else error) or message or error or "request failed"
    detail = str(msg).rstrip()
    if not detail.endswith((".", "!", "?")):
        detail += "."
    if code == 401:
        return (f"Your FN2 API key was rejected (401): {msg}. Check it's valid and active "
                f"— create or manage keys at {SIGNUP_URL}")
    if code == 403:
        result = f"Forbidden (403): {detail}"
        if "scope" in str(msg).lower():
            result += " Your API key may be missing a required scope (chat / agents / models)."
        return result
    if code == 429:
        return f"Quota exceeded (429): {detail} See your plan limits with `fn2 usage`."
    if code == 404:
        return f"Not found (404): {msg}."
    return f"API error ({code}): {msg}"


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def emit_json(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def _clean_answer(text: str, raw: bool) -> str:
    if raw or not text:
        return text or ""
    text = _CITE_RE.sub("", text)
    text = _MULTISPACE_RE.sub(" ", text)
    # Tidy any " ." or " ," left behind by removing a marker.
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    return text.strip()


def _fmt_schedule(sched) -> str:
    if not sched:
        return "one-off"
    if sched.get("cron"):
        tz = sched.get("timezone") or "UTC"
        return f"cron '{sched['cron']}' ({tz})"
    if sched.get("run_at"):
        return f"once at {sched['run_at']}"
    if sched.get("frequency"):
        return str(sched["frequency"])
    return "scheduled"


def print_agent(a: dict) -> None:
    line = f"  {a.get('id')}  {a.get('name') or '(unnamed)'}"
    print(line)
    bits = [
        f"status={a.get('status')}",
        f"schedule={_fmt_schedule(a.get('schedule'))}",
        f"runs={a.get('run_count', 0)}",
    ]
    if a.get("model"):
        bits.append(f"model={a['model']}")
    print("    " + "  ".join(bits))
    if a.get("prompt"):
        prompt = a["prompt"].replace("\n", " ")
        print("    prompt: " + (prompt[:120] + ("…" if len(prompt) > 120 else "")))


def print_run(r: dict, show_result: bool = False) -> None:
    print(f"  run {r.get('run_id')}  status={r.get('status')}")
    meta = []
    if r.get("created_at"):
        meta.append(f"created={r['created_at']}")
    if r.get("duration_seconds") is not None:
        meta.append(f"duration={r['duration_seconds']}s")
    usage = r.get("usage") or {}
    if usage.get("total_tokens"):
        meta.append(f"tokens={usage['total_tokens']}")
    if meta:
        print("    " + "  ".join(meta))
    if r.get("error"):
        print(f"    error[{r['error'].get('code')}]: {r['error'].get('message')}")
    if show_result and (r.get("result") or {}).get("text"):
        print("\n" + r["result"]["text"].strip() + "\n")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_research(args) -> int:
    text, meta = stream_chat(args.question, args.model)
    status = meta.get("status", "success")
    if args.json:
        emit_json({
            "response": text,
            "status": status,
            "model": meta.get("model"),
            "usage": meta.get("usage"),
        })
    else:
        print(_clean_answer(text, args.raw) or "(no answer returned)")
    # Non-zero exit when the run didn't finish cleanly or produced nothing, so a
    # caller/agent keying off the exit code can tell success from failure.
    return 0 if (status == "success" and text.strip()) else 2


def cmd_models(args) -> int:
    _, data = request("GET", "/models")
    if args.json:
        emit_json(data)
        return 0
    models = data or []
    if not models:
        print("No models available.")
        return 0
    print("Available models (★ = your default, 🔒 = needs a higher plan):")
    for m in models:
        mark = "★" if m.get("is_default") else (" 🔒" if m.get("locked") else "  ")
        model_id = m.get("model_id") or "?"
        name = m.get("display_name") or model_id
        print(f"  {mark} {model_id:<28} {name}  [{m.get('model_class')}]")
    return 0


def _int(value, default=0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def cmd_usage(args) -> int:
    _, data = request("GET", "/usage")
    if args.json:
        emit_json(data)
        return 0
    data = data or {}
    tokens = data.get("tokens") or {}
    used, limit, remaining = _int(tokens.get("used")), _int(tokens.get("limit")), _int(tokens.get("remaining"))
    print(f"Plan: {data.get('plan', 'unknown')}")
    if tokens.get("unlimited"):
        print(f"Tokens: {used:,} used (unlimited plan)")
    else:
        print(f"Tokens: {used:,} used / {limit:,} limit ({remaining:,} remaining)")
    if tokens.get("resets_at"):
        print(f"Resets: {tokens['resets_at']}")
    if data.get("api_key"):
        k = data["api_key"]
        print(f"API key '{k.get('name')}': {_int(k.get('total_requests'))} requests")
    return 0


def _build_schedule(args):
    """Translate CLI scheduling flags into the API's `schedule` object, or None."""
    if args.cron:
        return {
            "frequency": "custom",
            "cron": args.cron,
            "timezone": args.timezone or "UTC",
            "ends_at": args.ends,
        }
    if args.every:
        return {"frequency": args.every, "timezone": args.timezone or "UTC", "ends_at": args.ends}
    if args.at:
        return {"run_at": args.at, "timezone": args.timezone or "UTC"}
    return None


def cmd_agents_list(args) -> int:
    _, data = request("GET", "/agents", params={"status": args.status, "limit": args.limit})
    if args.json:
        emit_json(data)
        return 0
    agents = (data or {}).get("agents", [])
    total = (data or {}).get("total", len(agents))
    if not agents:
        print("No agents yet. Create one with `fn2 agents create --prompt \"…\"`.")
        return 0
    print(f"Agents ({len(agents)} of {total}):")
    for a in agents:
        print_agent(a)
    return 0


def cmd_agents_get(args) -> int:
    _, data = request("GET", f"/agents/{args.id}")
    if args.json:
        emit_json(data)
        return 0
    print_agent(data or {})
    return 0


def cmd_agents_create(args) -> int:
    body = {"prompt": args.prompt}
    if args.name:
        body["name"] = args.name
    if args.model:
        body["model"] = args.model
    if args.label:
        body["labels"] = args.label
    schedule = _build_schedule(args)
    if schedule:
        body["schedule"] = {k: v for k, v in schedule.items() if v is not None}
    _, data = request("POST", "/agents", body=body)
    if args.json:
        emit_json(data)
        return 0
    print("Created agent:")
    print_agent(data or {})
    if not schedule:
        print("  (no schedule given — it is running once now; check `fn2 runs list <id>`)")
    return 0


def cmd_agents_update(args) -> int:
    body = {}
    for field in ("name", "prompt", "model"):
        val = getattr(args, field)
        if val is not None:
            body[field] = val
    if args.label is not None:
        body["labels"] = args.label
    if not body:
        raise Fn2Error("Nothing to update. Pass --name / --prompt / --model / --label.")
    _, data = request("PATCH", f"/agents/{args.id}", body=body)
    if args.json:
        emit_json(data)
        return 0
    print("Updated agent:")
    print_agent(data or {})
    return 0


def _set_status(agent_id: str, status: str, as_json: bool) -> int:
    _, data = request("PATCH", f"/agents/{agent_id}", body={"status": status})
    if as_json:
        emit_json(data)
        return 0
    print(f"Agent {agent_id} is now {(data or {}).get('status', status)}.")
    return 0


def cmd_agents_pause(args) -> int:
    return _set_status(args.id, "paused", args.json)


def cmd_agents_resume(args) -> int:
    return _set_status(args.id, "active", args.json)


def cmd_agents_run(args) -> int:
    _, data = request("POST", f"/agents/{args.id}/run")
    if args.json:
        emit_json(data)
        return 0
    print(f"Started run {(data or {}).get('run_id')} (status={(data or {}).get('status')}).")
    print(f"Read the result with: fn2 runs get {args.id} {(data or {}).get('run_id')}")
    return 0


def cmd_agents_delete(args) -> int:
    request("DELETE", f"/agents/{args.id}")
    if args.json:
        emit_json({"deleted": True, "id": args.id})
        return 0
    print(f"Deleted agent {args.id}.")
    return 0


def cmd_runs_list(args) -> int:
    _, data = request("GET", f"/agents/{args.agent_id}/runs", params={"limit": args.limit})
    if args.json:
        emit_json(data)
        return 0
    runs = (data or {}).get("runs", [])
    if not runs:
        print("No runs yet.")
        return 0
    print(f"Runs for agent {args.agent_id}:")
    for r in runs:
        print_run(r)
    return 0


def cmd_runs_get(args) -> int:
    _, data = request("GET", f"/agents/{args.agent_id}/runs/{args.run_id}")
    if args.json:
        emit_json(data)
        return 0
    print_run(data or {}, show_result=True)
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    # `--json` is shared by every command via this parent parser, so it is
    # accepted *after* the subcommand (e.g. `fn2 research "…" --json`).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="print the raw JSON API response")

    p = argparse.ArgumentParser(
        prog="fn2",
        description="Command-line client for the FN2 market-research API (https://fn2.ai).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  fn2 research \"How did NVDA do this week and why?\"\n"
            "  fn2 agents create --prompt \"Daily macro brief\" --every weekdays\n"
            "  fn2 agents create --prompt \"Weekly tech recap\" --cron \"0 9 * * 1\"\n"
            "  fn2 runs list <agent-id>\n"
            "  fn2 models\n"
            "\nAdd --json to any command for raw JSON output.\n"
        ),
    )
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("research", parents=[common], help="ask FN2 a grounded, sourced market question")
    r.add_argument("question", help="the question to research")
    r.add_argument("--model", help="model_id to use (see `fn2 models`)")
    r.add_argument("--raw", action="store_true", help="keep inline citation markers")
    r.set_defaults(func=cmd_research)

    sub.add_parser("models", parents=[common], help="list models you can use").set_defaults(func=cmd_models)
    sub.add_parser("usage", parents=[common], help="show your plan and token usage").set_defaults(func=cmd_usage)

    # agents
    ag = sub.add_parser("agents", help="create and manage research agents")
    agsub = ag.add_subparsers(dest="agents_command", required=True)

    al = agsub.add_parser("list", parents=[common], help="list your agents")
    al.add_argument("--status", help="filter by status (active, paused, …)")
    al.add_argument("--limit", type=int, default=50, help="max agents to return (default 50)")
    al.set_defaults(func=cmd_agents_list)

    agg = agsub.add_parser("get", parents=[common], help="show one agent")
    agg.add_argument("id")
    agg.set_defaults(func=cmd_agents_get)

    ac = agsub.add_parser("create", parents=[common], help="create an agent (one-off or scheduled)")
    ac.add_argument("--prompt", required=True, help="what the agent should research")
    ac.add_argument("--name", help="a friendly name")
    ac.add_argument("--model", help="model_id (see `fn2 models`)")
    ac.add_argument("--label", action="append", help="a label (repeatable)")
    grp = ac.add_argument_group("scheduling (pick one; omit all for a one-off run now)")
    grp.add_argument("--every", help="recurring frequency: daily, weekdays, hourly, weekly, …")
    grp.add_argument("--cron", help="a cron expression, e.g. \"0 9 * * 1\" (Mon 9am)")
    grp.add_argument("--at", help="run once at an ISO datetime, e.g. 2026-07-01T09:00:00")
    grp.add_argument("--timezone", help="IANA timezone for the schedule (default UTC)")
    grp.add_argument("--ends", help="stop recurring after this date (YYYY-MM-DD)")
    ac.set_defaults(func=cmd_agents_create)

    au = agsub.add_parser("update", parents=[common], help="change an agent's settings")
    au.add_argument("id")
    au.add_argument("--name")
    au.add_argument("--prompt")
    au.add_argument("--model")
    au.add_argument("--label", action="append", help="replace labels (repeatable)")
    au.set_defaults(func=cmd_agents_update)

    ap_ = agsub.add_parser("pause", parents=[common], help="pause a scheduled agent")
    ap_.add_argument("id")
    ap_.set_defaults(func=cmd_agents_pause)

    ar = agsub.add_parser("resume", parents=[common], help="resume a paused agent")
    ar.add_argument("id")
    ar.set_defaults(func=cmd_agents_resume)

    arun = agsub.add_parser("run", parents=[common], help="run an agent now")
    arun.add_argument("id")
    arun.set_defaults(func=cmd_agents_run)

    ad = agsub.add_parser("delete", parents=[common], help="delete an agent and its history")
    ad.add_argument("id")
    ad.set_defaults(func=cmd_agents_delete)

    # runs
    rn = sub.add_parser("runs", help="inspect agent runs and their answers")
    rnsub = rn.add_subparsers(dest="runs_command", required=True)

    rl = rnsub.add_parser("list", parents=[common], help="list an agent's runs")
    rl.add_argument("agent_id")
    rl.add_argument("--limit", type=int, default=20, help="max runs (default 20)")
    rl.set_defaults(func=cmd_runs_list)

    rg = rnsub.add_parser("get", parents=[common], help="show one run, including its full answer")
    rg.add_argument("agent_id")
    rg.add_argument("run_id")
    rg.set_defaults(func=cmd_runs_get)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except Fn2Error as e:
        print(f"fn2: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
