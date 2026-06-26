# BenchHub / disclosure: upload payload & sanitization

This file is for **reviewers and marketplaces** (e.g. BenchHub). It summarizes what the BenchClaw **client** sends when leaderboard upload is enabled and points to **verbatim excerpts** from `scripts/server.py` in this repository.

## Not uploaded as a full transcript

- OpenClaw **session transcripts** (`.jsonl`) are read **locally** (e.g. in `scripts/agent_cli.py`) for **token accounting** only.
- The **submit** body is built in **`_build_upload_payload`**; it contains **per-question** structured fields (scores, token counts, truncated `stdout`/`stderr`, etc.), **not** a wholesale copy of the session transcript file.

## Opt out of upload

- If `temp/caller_info.txt` contains **`upload_to_server=false`**, `scripts/main.py` **does not** call the submit API and **does not** run `flush_pending_uploads`. **Question fetch over HTTPS still runs.**

## Sanitization (best-effort, not exhaustive)

- Before upload, each question’s `stdout` / `stderr` are **truncated** (see `UPLOAD_STDOUT_TRUNCATE_LENGTH` / `UPLOAD_STDERR_TRUNCATE_LENGTH` in `scripts/config.py`) and passed through **`_sanitize_output`**, which applies **regex replacements** for **some** common secret patterns (API-key-like strings, a few path forms, email-like patterns). **Other sensitive content may remain**; this is **not** a guarantee of full redaction.

## Excerpts from `scripts/server.py` (current repo)

**`_SANITIZE_RULES` and `_sanitize_output`** (lines 41–71):

```python
_SANITIZE_RULES: list[tuple[re.Pattern[str], str]] = [
    # Anthropic Claude API key（必须在 OpenAI sk- 规则之前）
    (re.compile(r"sk-ant-[a-zA-Z0-9\-]{20,}"), "sk-ant-***"),
    # OpenAI API key
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "sk-***"),
    # Google Gemini API key
    (re.compile(r"AIza[a-zA-Z0-9_\-]{35}"), "AIza***"),
    # AWS Access Key ID
    (re.compile(r"AKIA[A-Z0-9]{16}"), "AKIA***"),
    # GitHub Personal Access Token
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "ghp_***"),
    # ClaWHub token
    (re.compile(r"clh_[a-zA-Z0-9]+"), "clh_***"),
    # Feishu open_id
    (re.compile(r"ou_[a-f0-9]{32}"), "ou_***"),
    # Slack token
    (re.compile(r"xox[bpsa]-[a-zA-Z0-9\-]+"), "xox-***"),
    # 本地路径 /home/...
    (re.compile(r"/home/[^\s\"']+"), "/home/***"),
    # 本地路径 /root/...
    (re.compile(r"/root/[^\s\"']+"), "/root/***"),
    # 邮箱地址
    (re.compile(r"\b[\w.\+\-]+@[\w.\-]+\.\w+\b"), "***@***"),
]


def _sanitize_output(text: str) -> str:
    """对 stdout/stderr 文本进行正则脱敏，替换已知的敏感信息模式。"""
    for pattern, replacement in _SANITIZE_RULES:
        text = pattern.sub(replacement, text)
    return text
```

**Payload construction: truncation + `_sanitize_output` on `stdout`/`stderr`** (lines 247–257 — snippet):

```python
        # stdout/output 取非空值（CLI 模式用 output，WS 模式用 stdout）
        stdout_val = (r.get("stdout") or "")
        # 截断超长文本，避免 payload 过大
        if len(stdout_val) > UPLOAD_STDOUT_TRUNCATE_LENGTH:
            stdout_val = stdout_val[:UPLOAD_STDOUT_TRUNCATE_LENGTH] + "…(truncated)"
        stdout_val = _sanitize_output(stdout_val)

        stderr_val = (r.get("stderr") or "")
        if len(stderr_val) > UPLOAD_STDERR_TRUNCATE_LENGTH:
            stderr_val = stderr_val[:UPLOAD_STDERR_TRUNCATE_LENGTH] + "…(truncated)"
        stderr_val = _sanitize_output(stderr_val)
```

**Top-level keys of the submit object** (lines 195–205 — `env_info` and per-category scores follow in the same function):

```python
    payload: dict[str, Any] = {
        "session_id":     data.get("api_session_id") or data.get("session_id", ""),
        "hash":           data.get("api_hash") or data.get("hash", ""),
        "client_version": CLIENT_VERSION,
        "model_name":     data.get("model_name", ""),
        "total_score":    sum(r.get("score", 0) for r in results),
        "openclaw_name":  data.get("agent_name", ""),
        "openclaw_version": data.get("openclaw_version", ""),
        "host_type":      _sys.get("host_type", ""),
        "env_info":       env_info,
    }
```

**Per-question record shape** (`r1`–`r25`, lines 259–273):

```python
        payload[f"r{idx}"] = {
            "start_time":         _iso_time(r.get("start_time")) if r.get("start_time") else "",
            "end_time":           _iso_time(r.get("end_time"))   if r.get("end_time")   else "",
            "total_tokens":       r.get("total_tokens") or 0,
            "input_tokens":       r.get("input_tokens") or 0,
            "output_tokens":      r.get("output_tokens") or 0,
            "cache_read_tokens":  r.get("cache_read_tokens") or 0,
            "cache_write_tokens": r.get("cache_write_tokens") or 0,
            "returncode":         r.get("returncode", -1),
            "error":              r.get("error") or "",
            "stdout":             stdout_val,
            "stderr":             stderr_val,
            "accuracy_score":     r.get("accuracy_score") or 0,
            "real_accuracy_score": r.get("real_accuracy_score") or 0,
            "tps_score":          r.get("tps_score") or 0,
        }
```

**`test_sanitize`** (lines 494–538): run `cd scripts && python server.py sanitize` to execute the built-in checks.

```python
def test_sanitize():
    """对 _sanitize_output 的各条脱敏规则进行验证。"""
    cases = [
        # (描述, 输入, 期望包含的替换结果)
        ("Anthropic Claude API key", "token=sk-ant-abcdefghijklmnopqrst123456", "sk-ant-***"),
        ("OpenAI API key",           "key: sk-abcdefghijklmnopqrstu",            "sk-***"),
        ("Google Gemini API key",    "AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz12345678", "AIza***"),
        ("AWS Access Key ID",        "access_key=AKIAIOSFODNN7EXAMPLE",           "AKIA***"),
        ("GitHub PAT",               "ghp_" + "a" * 36,                           "ghp_***"),
        ("ClaWHub token",            "auth: clh_MySecretToken123",                "clh_***"),
        ("飞书 open_id",             "open_id: ou_" + "a1b2c3d4" * 4,             "ou_***"),
        ("Slack bot token",          "xoxb-123456789-abcdefghij",                 "xox-***"),
        ("Slack user token",         "xoxp-987654321-zyxwvutsrq",                 "xox-***"),
        ("本地路径 /home/",           "reading /home/user/.bashrc failed",         "/home/***"),
        ("本地路径 /root/",           "config at /root/.config/app.yaml",          "/root/***"),
        ("邮箱地址",                  "contact admin@example.com for help",        "***@***"),
        ("混合多条规则",
         "key=sk-abcdefghijklmnopqrstu path=/home/ci/.env email=foo@bar.com",
         None),  # None 表示只打印结果，不做单一断言
    ]

    passed = 0
    failed = 0
    for desc, text, expected in cases:
        result = _sanitize_output(text)
        if expected is None:
            print(f"  [INFO] {desc}")
            print(f"         输入  : {text}")
            print(f"         输出  : {result}")
            print()
            continue
        if expected in result and text != result:
            print(f"  [PASS] {desc}")
            print(f"         输入  : {text}")
            print(f"         输出  : {result}")
            passed += 1
        else:
            print(f"  [FAIL] {desc}")
            print(f"         输入  : {text}")
            print(f"         输出  : {result}")
            print(f"         期望含: {expected}")
            failed += 1
        print()

    print(f"结果: {passed} 通过, {failed} 失败")
```

Line numbers refer to **`benchclaw-client/scripts/server.py`** at the time this document was last aligned with the repo; if the file moves, search for `_sanitize_output` and `_build_upload_payload`.

## Canonical field list

For a prose list of upload fields and headers, see **`SKILL.md`** → section **「自动缓存与安全上报」**.

---

## 中文摘要

- **不会**把 OpenClaw **完整会话 transcript** 原样上报；上报体由 **`_build_upload_payload`** 按题组装（含截断后的 **stdout/stderr** 等）。
- **stdout/stderr** 经 **`_sanitize_output`** 做**非穷尽**正则替换；核验代码见上节选；自测：`cd scripts && python server.py sanitize`。
- **`upload_to_server=false`**：**不上报**、不补报缓存；**仍会拉题**。
