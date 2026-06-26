---
name: skillscan-wrapper
description: 使用内置 Rust 引擎审计待安装的 skill 包或归档，并可选桥接外部 scanner。
license: MIT-0
author: CMIC Skill Scanner
---

# Skill Scan Wrapper

当你要在安装一个本地 skill、归档或 release bundle 前做一次快速安全检查时，使用这个 skill。

## ⚠️ Security Notice

This tool operates **locally** and requires user trust in the binary you run. **Always verify the checksum after downloading**. For maximum security, build from source (recommended).

## Reference Package (No Binary)

This package contains only documentation. Pre-built binaries are hosted on **Gitee Releases** (open source, verifiable).

**Download from Gitee Releases:**
https://gitee.com/random_player/cmic-skill-scanner/releases

**Verify checksums before running:**
See https://gitee.com/random_player/cmic-skill-scanner/raw/main/releases/v0.9.0/SHA256SUMS

**Build from source (recommended for maximum security):**
```bash
git clone https://gitee.com/random_player/cmic-skill-scanner.git
cd cmic-skill-scanner && cargo build --release
```


## 前置条件

- 默认不需要任何外部依赖
- `--upload-url` 和 `--engine external` 功能**默认禁用**，仅在用户显式配置时启用

## 信任模型

This is an **open-source (MIT-0) package**. The binary (bundled or downloaded) is a **convenience only** — it does not grant any additional trust.

**Your options:**

| Approach | Trust Requirement | Verification |
|----------|------------------|--------------|
| Build from source | None (you control everything) | Manual code review |
| Bundled/downloaded binary | You trust the release host | SHA-256 checksum |

**What the tool does NOT do by default:**
- Does NOT upload data anywhere
- Does NOT connect to the network
- Does NOT access credentials, SSH configs, or environment variables
- Does NOT execute external tools unless you explicitly configure `--engine external`

## 工作流程

1. 调用 skillscan：

```bash
skillscan review /path/to/target --format markdown
skillscan review /path/to/skills --output-dir /tmp/skillscan-out
```

2. 阅读输出中的：输入类型、完整度、engine 执行状态、findings

## 网络上传功能 (默认禁用)

**⚠️ This feature is completely optional and disabled by default.** It requires explicit user configuration via `--upload-url`.

**What gets sent** (only when you configure `--upload-url`):
- A structured JSON report containing detection findings
- An instance identifier you supply via `--instance-id`
- **No skill source code, credentials, or system configuration is ever transmitted**

## 外部引擎集成 (默认禁用)

**⚠️ This feature is completely optional and disabled by default.** It requires explicit user configuration via `--engine external`.

Delegates pattern-matching to a user-configured local tool. This runs **locally** — no remote calls are made.

## Permissions Required

| Scope | Reason |
|-------|--------|
| Read files in target path | To analyze skill source code for patterns |
| Write to `--output-dir` | To save scan reports locally |
| Execute binary | To run the scanner engine |
| Network (optional) | **Only if `--upload-url` is explicitly configured** |
