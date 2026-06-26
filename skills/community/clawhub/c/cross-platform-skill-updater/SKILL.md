---
name: skill-updater
description: 用于检查或更新通过 git 工作树、或通过 .skill-lock.json 这类锁文件方式安装的本地 skills。适用于用户提到“查 skill 更新”“更新 skill”“检查 skills”“同步 skills”“GitHub skill 更新”“OpenClaw skills 更新”“全局 skills 状态”“只看风险项”“输出 JSON”这类需求。
---

# Skill Updater

用于统一检测并更新跨平台安装的 skills。

## 适用范围

- 支持 git 工作树型安装
- 支持 `.skill-lock.json` 型安装
- 默认扫描当前项目和常见全局目录
- 支持 OpenClaw 的 `~/.openclaw/skills` 与 `~/.openclaw/workspace/skills`
- 默认只做手动 `check` / `update`

## 推荐命令

```bash
sh skills/skill-updater/scripts/skill-updater check
sh skills/skill-updater/scripts/skill-updater update
sh skills/skill-updater/scripts/skill-updater check --source pbakaus/impeccable --json
sh skills/skill-updater/scripts/skill-updater update --path ~/.agents
sh skills/skill-updater/scripts/skill-updater check --path ~/.openclaw/workspace
```

## 自然语言触发示例

- 查 skill 更新
- 更新 skill
- 检查 skills
- 同步 skills
- 看看哪些 skill 要更新
- 更新 GitHub 装的 skills
- 检查 OpenClaw skills
- 检查全局 skills
- 只看有风险的 skill
- 输出 skill 状态 JSON
- 检查 `pbakaus/impeccable`

## 安全规则

- 遇到 git `dirty` / `ahead` / `diverged` 默认跳过
- 遇到锁文件来源异常、本地目录缺失或本地内容漂移默认跳过
- 更新前会为锁文件型安装做备份
