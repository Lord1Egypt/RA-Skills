---
name: clawlock-rank
description: >
  ClawLockRank — 基于 ClawLock 2.2.1+ 本地体检结果的排行榜上传技能。
  仅当用户明确要上传安全分、上传体检成绩、提交排行榜结果、同步分数到 ClawLockRank 时触发。
  不要在普通安全体检、安全加固、调试开发、安装依赖或仅浏览榜单时触发。
version: 1.1.0
metadata:
  clawlock:
    version: "1.1.0"
    homepage: "https://github.com/g1at/ClawLock-Rank"
    author: "g1at"
    compatible_with: [openclaw, zeroclaw, claude-code, generic-claw]
    platforms: [linux, macos, windows, android-termux]
    requires:
      python: ">=3.9"
      pip_package: "clawlock>=2.2.1"
      bins:
        - clawlock
      bins_optional:
        - python3
        - python
      config:
        - config.json
---

# ClawLockRank

基于 ClawLock 体检结果构建的排行榜上传技能，面向“本地完成体检后，自愿把成绩同步到 ClawLockRank”的场景。
[English Version → SKILL_EN.md](SKILL_EN.md)

## 安装与使用

```bash
python scripts/submit_score.py
python scripts/submit_score.py --preview-only
```

## 触发边界

仅在用户明确要求上传排行榜成绩时触发。

| 用户意图 | 执行动作 |
|---------|---------|
| 上传安全分 / 上传体检成绩 / 提交排行榜结果 | 启动本 skill |
| 普通安全体检 / 安全加固 / 版本检查 | 交给 ClawLock 主 skill 或直接调用 clawlock CLI |
| 仅浏览榜单 / 介绍项目 / 调试脚本 | 不触发本 skill |

常见触发词：
- 上传安全分
- 上传安全体检分数
- 上传排行榜
- 提交体检成绩
- 把这次体检结果上传到 ClawLockRank
- 同步分数到 ClawLockRank

如果用户只是说“开始安全体检”或“帮我加固”，优先交给 ClawLock 主 skill，而不是本 skill。

## 单一事实来源

- 体检结果以 `clawlock scan --format json` 为唯一事实来源。
- 只使用 ClawLock JSON 里明确给出的字段，不自行补造步骤计数、风险总表或额外结论。
- 对用户的说明分成两层：
  - `ClawLock 结果`：只转述 CLI 已经给出的分数、等级、适配器、版本和 findings。
  - `影响说明`：再用自然语言解释为什么值得上传、哪些字段会公开。
- 如果当前环境里的 `clawlock` 版本低于 `2.2.1`，先提示用户升级，再继续后续动作。

## 隐私与上传范围

默认先在本地执行体检，只有在用户明确确认后才会上传。

允许上传的字段仅包括：
- `tool`
- `clawlock_version`
- `adapter`
- `adapter_version`
- `device_fingerprint`
- `evidence_hash`
- `score`
- `grade`
- `nickname`
- `findings[].scanner`
- `findings[].level`
- `findings[].title`
- `timestamp`

明确不会上传：
- 原始配置文件
- remediation / 修复建议文本
- 本地文件路径或 `location`
- 环境变量
- 完整原始扫描报告
- `scan_history.json`

设备指纹说明：
- 原始 `device_fingerprint` 只发送给排行榜 Worker
- Worker 会在服务端做加盐哈希后再入库
- 前端不会公开展示原始设备指纹

## Claw 场景下的推荐流程

把脚本视作“后台执行器”，对话和确认由模型负责，不要把脚本提示直接当成最终用户体验。

在开始预览前，先输出一行启动提示：

```text
🔍 ClawLockRank 正在准备本地体检结果上传预览，请稍候...
```

推荐顺序：

1. 先运行预览命令：

```bash
python scripts/submit_score.py --preview-only
```

2. 读取预览 JSON，向用户说明：
   - 当前分数和等级
   - 适配器与版本
   - finding 数量
   - 将公开上传的字段
   - 明确不会上传的字段

3. 告知用户排行榜会公开显示一个昵称，并先询问昵称：
   - 留空则使用 `Anonymous`

4. 再询问是否确认上传。

5. 只有在用户明确同意后，才执行：

```bash
python scripts/upload.py --input <payload_path> --nickname "<nickname>" --yes
```

其中 `<payload_path>` 使用预览结果里的 `payload_path`。

如果是终端手动使用，也可以直接运行：

```bash
python scripts/submit_score.py
```

## 兼容性与降级规则

- 当前排行榜面向 OpenClaw 安全体检分数，脚本默认以 `--adapter openclaw` 调用 ClawLock。
- 如需别的适配器，可显式传入 `--adapter` 覆盖默认值。
- 如果 `clawlock scan` 失败，直接把 CLI 的错误返回给用户，不要二次改写成“已通过”。
- 如果用户拒绝上传，明确说明：“已取消上传，本地结果未外传。”
- 如果 Worker 因冷却期、时间戳过旧或频率限制拒绝上传，直接展示 Worker 返回的错误。

## 服务端限制说明

排行榜后端会额外执行以下限制：
- 同一设备默认 `24` 小时冷却
- 只接受最近一段时间内生成的扫描结果
- 同一 IP 有单独的频率限制
- 榜单和安全漏洞热点都只按设备最新一条有效结果统计

## 语言适配

- 面向用户的说明跟随用户当前语言。
- `clawlock scan --format json` 作为结构化输入，不依赖 CLI 文本语言。
- 如用户显式设置 `CLAWLOCK_LANG=zh`，继续按中文对话即可；未设置或使用英文时，使用英文说明。
