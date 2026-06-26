# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目说明

clawmoney-skill 是 ClawMoney 平台的 OpenClaw/ClawHub skill，供 AI agent 安装后自动注册、浏览任务、赚取奖励。

## API Base URL

**必须使用 `api.bnbot.ai`，不是 `api.clawmoney.ai`**（后者无法解析）。

所有 SKILL.md 和 scripts 中的 API 调用都走 `https://api.bnbot.ai`。

## 发布

```bash
npx clawhub publish /Users/jacklee/Projects/clawmoney-skill \
  --slug clawmoney --name clawmoney --version <ver> --changelog "<text>"
```

## 同步

修改 SKILL.md 后，**必须同步更新三个文件并发布**：

1. **本文件** `clawmoney-skill/SKILL.md` → git push + `npx clawhub publish`
2. **项目内部 skill** `/Users/jacklee/Projects/clawmoney-web/.claude/skills/clawmoney/SKILL.md` → git push
3. **网站 skill** `/Users/jacklee/Projects/clawmoney-web/public/skill.md` → git push

三者内容保持一致。每次更新都要 clawhub publish 新版本。
