---
name: changelog-draft-gen
description: 更新日志草稿生成器 — 发版手写 CHANGELOG 漏三漏四，conventional-changelog 全家桶又太重，只想按规范出个草稿（零依赖，确定性输出，rc=0/1/2，--json 机器可读） 适用场景：当需要更新日志草稿生成器能力时使用本技能；触发词：changelog-draft-gen。
slug: changelog-draft-gen
title: changelog-draft-gen
version: 1.0.1
display_name: 更新日志草稿生成器
display_name_en: Changelog Generator
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
category: 工程方法
platforms: [claude, codex, cursor, windsurf, cli]
copyright: SynomosAI
description_zh: "更新日志草稿生成器 — 发版手写 CHANGELOG 漏三漏四，conventional-changelog 全家桶又太重，只想按规范出个草稿（零依赖，确定性输出，rc=0/1/2，--json 机器可读）"
description_en: "Generate a spec-compliant CHANGELOG draft from commit history without the heavyweight toolchain (zero-dependency, deterministic output, --json)."
read_when:
  - 快速生成符合 Conventional Commits 的 CHANGELOG 草稿
  - 要零依赖、确定性、可机器解析的发布日志（CI 集成/脚本调用）
  - 仅针对特定版本号做预发布说明，无需完整自动化流水线
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [changelog-draft-gen, 工程方法]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/changelog_gen.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: repo
    type: string
    description: git 仓库路径默认.
    required: false
  - name: from
    type: string
    description: 起始 ref
    required: false
  - name: to
    type: string
    description: 结束 ref 默认 HEAD
    required: false
  - name: version
    type: string
    description: 版本标签如 v1.2.0
    required: false
  - name: out
    type: string
    description: 写入文件（原子替换）
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: conventional commits 生成的 CHANGELOG 草稿
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - changelog
  - git
  - documentation
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
- Quickly generate a Conventional-Commits-compliant CHANGELOG draft without hand-writing or configuring heavyweight tools (e.g. conventional-changelog).
- Want zero-dependency, deterministic, machine-parseable release notes for CI integration or scripts.
- Pre-release notes for a specific version (rc=0/1/2) without a full automation pipeline.

### Usage
- Command: `changelog_gen.py`.
- Key params: `--version` (e.g. v1.0.0-rc2), `--mode` (rc=0/1/2 release mode).
- Output: Markdown by default; `--json` for machine-readable stream.

### Flow
1. Ensure local Git history is tidy; base CHANGELOG directory exists.
2. Invoke with version info (e.g. v1.0.0-rc1).
3. Run the script; choose Markdown or JSON output.
4. Review the generated draft; verify links and format.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
- 当你需要快速生成符合 Conventional Commits 规范的 CHANGELOG 草稿，但手动维护或配置重型工具（如 conventional-changelog）耗时过长时。
- 当你希望获得零依赖、确定性高、且可机器解析的发布日志格式时，用于 CI 集成或脚本调用。
- 当你仅需针对特定版本号（rc=0/1/2）进行预发布说明生成，无需完整自动化流水线介入时。

### 用法
- 调用命令：`changelog_gen.py`。
- 关键参数说明：`--version`（指定目标版本号，如 v1.0.0-rc2）、`--mode`（选择 rc=0/1/2 发布模式）。
- 输出格式说明：默认生成 Markdown 文件至当前目录，可通过 `--json` 参数直接获取 JSON 格式数据流。

### 流程
1. 确保本地 Git 历史记录已整理完毕，且变更日志基础目录结构存在。
2. 调用技能时携带输入版本信息参数，如 `v1.0.0-rc1` 以明确发布类型。
3. 执行脚本解析并生成，根据需求选择 Markdown 或 JSON 格式输出。
4. 检查生成的变更日志草稿内容，验证链接与格式是否符合预期规范。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
