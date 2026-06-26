---
name: alltoken-call
description: Six slash-style AllToken commands — /alltoken-chat, /alltoken-image, /alltoken-video, /alltoken-search, /alltoken-models, /alltoken-cost — recognized in chat and run via stdlib Python recipes. Pair with alltoken for full project bootstrap.
metadata:
  version: 1.0.1
  homepage: https://alltoken.ai
  docs: https://alltoken.ai/docs/apis/overview
  license: MIT
  openclaw:
    compat: ">=0.18"
  companion_skill: ../alltoken/SKILL.md
---

# /alltoken-call — direct AllToken commands

This skill teaches the host agent to recognize **six slash-style invocations** in user prompts and run the corresponding recipe against the user's AllToken API key. Each command is a self-contained Python 3 stdlib script — no external SDK install required.

## When to invoke this skill (vs `alltoken`)

| User wants… | Use |
|---|---|
| "Generate an image of X" / "Translate this with Claude" / "Show available models" | This skill (`alltoken-call`) |
| "Build me an AllToken agent" / "Scaffold a chat app" / "Add AllToken to my project" | `alltoken` instead |
| Both | Load both — they don't conflict |

## Prerequisites

- `ALLTOKEN_API_KEY` exported in the environment the agent shells out to
- `python3` ≥ 3.10 available on `PATH`
- Internet access from the agent's host

> The agent should refuse to invoke any command in this skill if `ALLTOKEN_API_KEY` is unset, and prompt the user to set it first.

## Trigger recognition

Match these patterns **case-insensitively** anywhere in the user's message (a leading `/` is canonical but not required):

| Trigger | Command |
|---|---|
| `/alltoken-chat`, `alltoken chat`, "ask alltoken with model X" | [Command 1](#1-alltoken-chat) |
| `/alltoken-image`, `alltoken image`, "generate an image via alltoken", "draw with alltoken" | [Command 2](#2-alltoken-image) |
| `/alltoken-video`, `alltoken video`, "make a video on alltoken" | [Command 3](#3-alltoken-video) |
| `/alltoken-search`, `alltoken search`, "use alltoken web search", "find with alltoken" | [Command 4](#4-alltoken-search) |
| `/alltoken-models`, `alltoken models`, "what alltoken models are available" | [Command 5](#5-alltoken-models) |
| `/alltoken-cost`, `alltoken cost`, "how much did that cost" (when last response was an AllToken call) | [Command 6](#6-alltoken-cost) |

## Production constraints baked into the recipes

These were verified live on 2026-05-12 — they're not optional:

1. **Image results are one-shot.** Persist `b64_json` on the first `completed` read; re-polling returns `410 image_already_retrieved`.
2. **`enable_search: true` only works on DeepSeek and Qwen.** OpenAI returns 503, Claude/GLM/Kimi/Minimax silently drop it. The `/alltoken-search` recipe defaults to `deepseek-v4-pro` for this reason.
3. **Streaming `usage` requires opt-in.** Add `stream_options: {"include_usage": True}` or it'll be null.
4. **The API key reaches `/v1/*` only.** `/api-account/user/balance`, `/usage`, `/billing` return 401 with the Bearer token — they need a web session. Do not attempt them.
5. **Errors are envelope-shaped:** `{"error": {"code": "<slug>", "type": "<group>", "message": "...", "param": null, "request_id": "..."}}`. Always surface `code` and `request_id` to the user on failure.

---

## 1. `/alltoken-chat`

**Syntax**

```
/alltoken-chat <model> <prompt>
/alltoken-chat <prompt>                       # uses default: gpt-5.4-mini
```

**Parameters**

- `model` (optional) — any ID from `/v1/models`. Common choices: `gpt-5.4-mini`, `gpt-5.4`, `claude-sonnet-4-6`, `claude-opus-4-7`, `deepseek-v4-pro`, `gemini-3.1-pro-preview`. Cheap defaults: `gpt-5.4-nano`, `claude-haiku-4-5`, `gemini-3-flash-preview`.
- `prompt` (required) — free-form text.

**Recipe** — save as `/tmp/at_chat.py`, run with `python3 /tmp/at_chat.py <model> <prompt...>`:

```python
import os, sys, json, urllib.request
args = sys.argv[1:]
if not args:
    print("usage: at_chat.py [model] <prompt...>"); sys.exit(2)
# Heuristic: first arg is model only if it has no spaces AND looks like an ID
first = args[0]
if len(args) >= 2 and "-" in first and " " not in first and "." in first or first.startswith(("gpt-","claude-","gemini-","deepseek-","glm-","qwen","kimi-","minimax-")):
    model, prompt = first, " ".join(args[1:])
else:
    model, prompt = "gpt-5.4-mini", " ".join(args)
body = json.dumps({
    "model": model,
    "messages": [{"role":"user","content": prompt}],
    "stream": True,
    "stream_options": {"include_usage": True},
}).encode()
req = urllib.request.Request("https://api.alltoken.ai/v1/chat/completions",
    data=body, method="POST",
    headers={"Authorization": f"Bearer {os.environ['ALLTOKEN_API_KEY']}", "Content-Type":"application/json"})
try:
    r = urllib.request.urlopen(req, timeout=120)
except urllib.error.HTTPError as e:
    err = json.loads(e.read()).get("error", {})
    print(f"\n[error {e.code}] {err.get('code')}/{err.get('type')}: {err.get('message')}  req={err.get('request_id')}")
    sys.exit(1)
usage = None
for raw in iter(r.readline, b""):
    line = raw.decode("utf-8","replace").rstrip("\n")
    if not line or line.startswith(":"): continue
    if line.startswith("data: "):
        data = line[6:]
        if data == "[DONE]": break
        obj = json.loads(data)
        if obj.get("usage"): usage = obj["usage"]
        for ch in obj.get("choices", []):
            c = ch.get("delta", {}).get("content")
            if c: sys.stdout.write(c); sys.stdout.flush()
print()
if usage:
    print(f"\n[usage] prompt={usage['prompt_tokens']} completion={usage['completion_tokens']} total={usage['total_tokens']} model={model}")
```

**Agent presentation** — after running, show the streamed text to the user and, in a separate line, surface the token usage (`prompt + completion = total`). If the user follows up with `/alltoken-cost`, that line is what gets multiplied by per-token prices.

---

## 2. `/alltoken-image`

**Syntax**

```
/alltoken-image <prompt> [--size=1024x1024] [--quality=low|medium|high] [--out=PATH]
```

**Parameters**

- `prompt` (required)
- `--size` — `1024x1024` (default), `1536x1024`, `1024x1536`, `auto`
- `--quality` — `low` (default for speed), `medium`, `high`, `auto`
- `--out` — output path (default: `./alltoken-image-<8charhex>.png` in `cwd`)

**Recipe** — save as `/tmp/at_image.py`:

```python
import os, sys, json, time, base64, uuid, argparse, urllib.request
ap = argparse.ArgumentParser()
ap.add_argument("prompt", nargs="+")
ap.add_argument("--size", default="1024x1024")
ap.add_argument("--quality", default="low", choices=["low","medium","high","auto"])
ap.add_argument("--out", default=None)
a = ap.parse_args()
prompt = " ".join(a.prompt)
out = a.out or f"alltoken-image-{uuid.uuid4().hex[:8]}.png"
H = {"Authorization": f"Bearer {os.environ['ALLTOKEN_API_KEY']}", "Content-Type":"application/json"}
body = json.dumps({"model":"gpt-image-2","prompt":prompt,"size":a.size,"quality":a.quality}).encode()
req = urllib.request.Request("https://api.alltoken.ai/v1/images/generations/async",
    data=body, method="POST", headers={**H, "Idempotency-Key": str(uuid.uuid4())})
try:
    created = json.loads(urllib.request.urlopen(req, timeout=60).read())
except urllib.error.HTTPError as e:
    print(f"[error] submit failed: {e.code} {e.read().decode()[:300]}"); sys.exit(1)
task_id = created["id"]; t0 = time.time()
print(f"submitted {task_id} (size={a.size} quality={a.quality})", flush=True)
while True:
    time.sleep(2)
    req = urllib.request.Request(f"https://api.alltoken.ai/v1/images/generations/{task_id}", headers=H)
    s = json.loads(urllib.request.urlopen(req, timeout=30).read())
    print(f"  [{time.time()-t0:.0f}s] {s['status']}", flush=True)
    if s["status"] == "completed":
        # ONE-SHOT: write immediately, never re-poll
        with open(out, "wb") as f: f.write(base64.b64decode(s["data"][0]["b64_json"]))
        print(f"saved {out} ({os.path.getsize(out)} bytes) in {time.time()-t0:.1f}s")
        u = s.get("usage", {}); print(f"[usage] input={u.get('input_tokens')} output={u.get('output_tokens')} total={u.get('total_tokens')}")
        break
    if s["status"] in ("failed","cancelled"):
        print(f"[error] task ended: {s.get('error')}"); sys.exit(1)
```

**Agent presentation** — confirm the file path, embed/preview the image if the host supports it, and warn the user that the result is gone from the server after retrieval. If the user asks for a variation, run a *new* `/alltoken-image` rather than re-polling the old task.

---

## 3. `/alltoken-video`

**Syntax**

```
/alltoken-video <prompt> [--model=seedance-1.5-pro] [--duration=5] [--ratio=16:9] [--resolution=480p|720p|1080p]
```

**Parameters**

- `prompt` (required)
- `--model` — `seedance-1.5-pro` (default), `seedance-2.0`, `happyhorse-1.0-t2v`, `happyhorse-1.0-i2v`. Check `/v1/videos/models` for the full list.
- `--duration` — seconds, default `5`
- `--ratio` — `16:9` (default), `9:16`, `4:3`, `3:4`, `21:9`, `1:1`, `adaptive`
- `--resolution` — `480p` (default), `720p`, `1080p`

**Recipe** — save as `/tmp/at_video.py`:

```python
import os, sys, json, time, argparse, urllib.request
ap = argparse.ArgumentParser()
ap.add_argument("prompt", nargs="+")
ap.add_argument("--model", default="seedance-1.5-pro")
ap.add_argument("--duration", type=int, default=5)
ap.add_argument("--ratio", default="16:9")
ap.add_argument("--resolution", default="480p", choices=["480p","720p","1080p"])
a = ap.parse_args()
H = {"Authorization": f"Bearer {os.environ['ALLTOKEN_API_KEY']}", "Content-Type":"application/json"}
body = json.dumps({"model":a.model,"prompt":" ".join(a.prompt),"duration":a.duration,"ratio":a.ratio,"resolution":a.resolution}).encode()
req = urllib.request.Request("https://api.alltoken.ai/v1/videos/generations", data=body, method="POST", headers=H)
try:
    created = json.loads(urllib.request.urlopen(req, timeout=60).read())
except urllib.error.HTTPError as e:
    print(f"[error] {e.code} {e.read().decode()[:300]}"); sys.exit(1)
vid = created["id"]; t0 = time.time()
print(f"submitted {vid}", flush=True)
while True:
    time.sleep(3)
    req = urllib.request.Request(f"https://api.alltoken.ai/v1/videos/generations/{vid}", headers=H)
    s = json.loads(urllib.request.urlopen(req, timeout=30).read())
    print(f"  [{time.time()-t0:.0f}s] {s['status']}", flush=True)
    if s["status"] == "completed":
        url = s.get("video_url")
        ttl = s.get("video_url_ttl", "?")
        print(f"video_url ({ttl}s TTL): {url}")
        print(f"resolution={s.get('resolution')} ratio={s.get('ratio')} fps={s.get('fps')}")
        break
    if s["status"] in ("failed","cancelled","expired"):
        print(f"[error] task ended: {s.get('error')}"); sys.exit(1)
```

**Agent presentation** — give the `video_url` (presigned, expires in `video_url_ttl` seconds) and remind the user to download promptly. If they want to cancel mid-generation, `POST /v1/videos/generations/{id}/cancel`.

---

## 4. `/alltoken-search`

**Syntax**

```
/alltoken-search <query>
/alltoken-search --model=qwen3.6-flash <query>
```

**Parameters**

- `query` (required) — natural-language question
- `--model` — defaults to `deepseek-v4-pro`. Only DeepSeek and Qwen models honor `enable_search:true`; choose one of: `deepseek-v4-pro`, `deepseek-v3.2`, `qwen3.6-flash`, `qwen3.6-max-preview`. If you pass any other model the recipe will refuse and tell the user why.

**Recipe** — save as `/tmp/at_search.py`:

```python
import os, sys, json, argparse, urllib.request
SEARCH_OK = {"deepseek-v4-pro","deepseek-v3.2","qwen3.6-flash","qwen3.6-max-preview","qwen3.6-plus","qwen3.6-27b"}
ap = argparse.ArgumentParser()
ap.add_argument("query", nargs="+")
ap.add_argument("--model", default="deepseek-v4-pro")
a = ap.parse_args()
if a.model not in SEARCH_OK:
    print(f"[refuse] {a.model} does NOT honor enable_search on AllToken today.")
    print(f"        Use one of: {', '.join(sorted(SEARCH_OK))}")
    sys.exit(2)
body = json.dumps({
    "model": a.model,
    "messages": [{"role":"user","content":" ".join(a.query)}],
    "enable_search": True,
    "max_tokens": 600,
}).encode()
req = urllib.request.Request("https://api.alltoken.ai/v1/chat/completions",
    data=body, method="POST",
    headers={"Authorization": f"Bearer {os.environ['ALLTOKEN_API_KEY']}", "Content-Type":"application/json"})
try:
    r = urllib.request.urlopen(req, timeout=120)
except urllib.error.HTTPError as e:
    err = json.loads(e.read()).get("error", {})
    print(f"[error {e.code}] {err.get('code')}/{err.get('type')}: {err.get('message')}  req={err.get('request_id')}"); sys.exit(1)
j = json.loads(r.read())
m = j["choices"][0]["message"]
print(m.get("content","").strip())
u = j.get("usage", {})
print(f"\n[usage] prompt={u.get('prompt_tokens')} completion={u.get('completion_tokens')} total={u.get('total_tokens')} model={a.model}")
```

**Agent presentation** — the response should look like a search-grounded answer (current dates, specific numbers). If the model says "I don't have web search" anyway, the family is honoring the flag but the underlying provider failed — re-run with a different model.

---

## 5. `/alltoken-models`

**Syntax**

```
/alltoken-models
/alltoken-models --type=chat        # chat (default), image, video
/alltoken-models --filter=claude    # substring filter on ID
```

**Recipe** — save as `/tmp/at_models.py`:

```python
import os, sys, json, argparse, urllib.request
ap = argparse.ArgumentParser()
ap.add_argument("--type", default="chat", choices=["chat","image","video"])
ap.add_argument("--filter", default="")
a = ap.parse_args()
path = {"chat":"/v1/models","image":"/v1/images/models","video":"/v1/videos/models"}[a.type]
req = urllib.request.Request(f"https://api.alltoken.ai{path}",
    headers={"Authorization": f"Bearer {os.environ['ALLTOKEN_API_KEY']}"})
j = json.loads(urllib.request.urlopen(req, timeout=30).read())
ids = [m["id"] for m in j["data"]]
if a.filter: ids = [i for i in ids if a.filter.lower() in i.lower()]
print(f"{a.type}: {len(ids)} model(s)" + (f" matching '{a.filter}'" if a.filter else ""))
for i in ids: print(f"  {i}")
```

**Agent presentation** — list IDs in a code block. If the user asks "which is cheapest / fastest / best for code", cross-reference the verified-working table in `alltoken/SKILL.md` `## Discovering models`.

---

## 6. `/alltoken-cost`

Compute the cost of a chat call from its `usage` block + per-million prices from the catalog. Useful right after `/alltoken-chat` or `/alltoken-search`.

**Syntax**

```
/alltoken-cost <model> <prompt_tokens> <completion_tokens>
```

**Recipe** — save as `/tmp/at_cost.py`:

```python
import os, sys, json, urllib.request
if len(sys.argv) != 4:
    print("usage: at_cost.py <model> <prompt_tokens> <completion_tokens>"); sys.exit(2)
model, pt, ct = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
# Public catalog — no auth required
req = urllib.request.Request(f"https://api.alltoken.ai/api-account/models/{model}")
try:
    j = json.loads(urllib.request.urlopen(req, timeout=30).read())
except urllib.error.HTTPError as e:
    print(f"[error] catalog lookup failed: {e.code}"); sys.exit(1)
# Pricing fields vary; try common keys
data = j.get("data", j)
p_in  = float(data.get("input_price")  or data.get("prompt_price")     or 0)
p_out = float(data.get("output_price") or data.get("completion_price") or 0)
# Convention: prices are per 1M tokens
cost = (pt / 1_000_000) * p_in + (ct / 1_000_000) * p_out
print(f"model:            {model}")
print(f"prompt tokens:    {pt:>10,}")
print(f"completion tokens:{ct:>10,}")
print(f"input  $/1M:      ${p_in:.4f}")
print(f"output $/1M:      ${p_out:.4f}")
print(f"───")
print(f"total cost:       ${cost:.6f}")
```

**Agent presentation** — surface the total in $ to 6 decimal places; for streaming chat, prefer reading the exact figure from the after-`[DONE]` SSE comment line (which is the authoritative per-request cost from AllToken's gateway). Use this recipe as a fallback when that comment line wasn't captured.

> Tip: pricing fields in the catalog response have evolved — if `input_price`/`output_price` aren't populated, fall back to inspecting `data` keys: `curl https://api.alltoken.ai/api-account/models/<model> | jq 'keys'`.

---

## Error handling (shared across all commands)

When any recipe hits a non-2xx response, the AllToken envelope is `{"error": {"code", "type", "message", "param", "request_id"}}`. The agent should:

1. Show the user `code` and `message`.
2. Include `request_id` in any support communication.
3. For specific slugs, take action without prompting:
   - `invalid_api_key` (401): tell the user the key is bad; do not retry.
   - `image_already_retrieved` (410): tell the user to re-run; the result is gone.
   - `all_providers_failed` (503): try a different model from the same family, then a different family.
   - `rate_limited` / HTTP 429: read `Retry-After` (integer seconds), sleep, retry once.
   - `insufficient_balance` (402): tell the user to top up in Settings → Billing.

## Companion skill

If the user wants to *build* something instead of one-shot calls, hand off to `alltoken`:

> "If you want me to scaffold a whole agent project around this, load `skills/alltoken/SKILL.md`."

## Resources

- AllToken docs: https://alltoken.ai/docs/apis/overview
- Live model list: `GET https://api.alltoken.ai/v1/models` (Bearer auth)
- Public catalog: `GET https://api.alltoken.ai/api-account/models` (no auth)
- Companion bootstrap skill: [`../alltoken/SKILL.md`](../alltoken/SKILL.md)
- Companion usage manual: [`../alltoken/USAGE.md`](../alltoken/USAGE.md)
