---
name: skillscan-wrapper
description: 使用 auto、native 或 external 引擎审计待安装的 skill 包或归档，并可选启用 LLM 语义分析。
license: MIT-0
author: CMIC Skill Scanner
---

# Skill Scan Wrapper

当你要在安装一个本地 skill、归档或 release bundle 前做一次快速安全检查时，使用这个 skill。

## ⚠️ Security Notice

This tool scans locally by default and requires user trust in the binary you run. Native LLM review sends a bounded text packet to a user-configured endpoint; external LLM review follows the external scanner's data policy. **Always verify the checksum after downloading**. For maximum security, build from source (recommended).

## Reference Package (No Binary)

This package contains only documentation. Pre-built binaries are hosted on **Gitee Releases** (open source, verifiable).

**Download from Gitee Releases:**
https://gitee.com/random_player/cmic-skill-scanner/releases

**Verify checksums before running:**
See https://gitee.com/random_player/cmic-skill-scanner/raw/main/releases/v0.11.1/SHA256SUMS

**Build from source (recommended for maximum security):**
```bash
git clone https://gitee.com/random_player/cmic-skill-scanner.git
cd cmic-skill-scanner && cargo build --release
```


## 前置条件

- 默认 `auto` 模式会优先尝试本地可解析的 external scanner；没有可用 scanner 时回退到内置 native 引擎
- 不安装 external scanner 也可以使用：单二进制会回退到 native
- `--upload-url` 和 `--use-llm` 功能**默认禁用**，仅在用户显式配置时启用

## 信任模型

This is an **open-source (MIT-0) package**. The binary (bundled or downloaded) is a **convenience only** — it does not grant any additional trust.

**Your options:**

| Approach | Trust Requirement | Verification |
|----------|------------------|--------------|
| Build from source | None (you control everything) | Manual code review |
| Bundled/downloaded binary | You trust the release host | SHA-256 checksum |

**Default behavior and trust boundaries:**
- CMIC does NOT upload reports unless you configure `--upload-url`
- CMIC does NOT configure an LLM endpoint unless you set `--use-llm`
- `auto` may execute a locally resolved external scanner; use `--engine native` to prevent that
- Does NOT access credentials or SSH configs as scan targets unless they are under the path you explicitly scan

## 工作流程

1. 调用 skillscan：

```bash
skillscan review /path/to/target --format markdown
skillscan review /path/to/skills --output-dir /tmp/skillscan-out
```

2. 阅读输出中的：输入类型、完整度、engine 执行状态、findings

## 网络上传功能 (默认禁用)

**⚠️ This feature is completely optional and disabled by default.** It requires explicit user configuration via `--upload-url`.

This applies to report upload only. LLM review is a separate, explicit network feature; a resolved external scanner has its own dependency and network behavior.

**What gets sent** (only when you configure `--upload-url`):
- A structured JSON report containing detection findings
- An instance identifier you supply via `--instance-id`
- **No skill source code, credentials, or system configuration is ever transmitted**

## Optional LLM Review

**⚠️ This feature is completely optional and disabled by default.** It requires explicit `--use-llm` and works with `native`, `external`, and `auto`.

```bash
skillscan review /path/to/target --engine native --use-llm   --llm-endpoint http://localhost:11434/v1   --llm-model your-model
```

With `native`, the endpoint receives static-finding summaries and up to 24 text files from the target package (up to 8 KiB each and 64 KiB total). Lines named `api_key`, `token`, `password`, `secret`, or `authorization` are redacted at a basic level. This is not a guarantee that all sensitive text is removed: use only a trusted endpoint and confirm the data-handling policy.

With a Cisco-compatible `external` engine, CMIC adds `--use-llm` and passes endpoint, model, and optional key to the child process through `SKILL_SCANNER_LLM_*` variables; the external scanner controls its own packet, redaction, and failure behavior. `auto` tries that external LLM first and falls back to native if the external process fails. API keys are never written to the scan command or report.

If the native LLM request fails, the native static result is still returned and `engine.fallback_reason` records the reason.

## 外部引擎集成

Default `auto` mode tries a locally resolved external scanner first and falls back to native when it is unavailable or fails. Use `--engine external` to require the external result, or `--engine native` to run only the built-in engine.

CMIC passes the target path to a user-configured local tool. The tool runs with the current user's process permissions; trust the external tool and its configuration separately. CMIC only configures the external LLM endpoint when `--use-llm` is explicitly set; the tool may otherwise bootstrap dependencies or use its own network configuration.

## Permissions Required

| Scope | Reason |
|-------|--------|
| Read files in target path | To analyze skill source code for patterns |
| Write to `--output-dir` | To save scan reports locally |
| Execute binary / external tool | To run the selected scanner engine; `auto` may invoke a locally resolved external scanner |
| Network (optional) | `--upload-url` sends a JSON report; native `--use-llm` sends a bounded text packet; external `--use-llm` follows the external tool's data policy |
