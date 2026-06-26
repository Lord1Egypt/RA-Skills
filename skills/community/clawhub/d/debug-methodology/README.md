# 🔍 Debug Methodology

[![ClawHub](https://img.shields.io/badge/ClawHub-debug--methodology-blue?style=flat-square)](https://clawhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Agent_Skill-orange?style=flat-square)](https://github.com/openclaw/openclaw)

**系统化调试方法论** — 适用于 AI Agent 和开发者的通用调试规范。

> 从真实生产事故中提炼，结合 Nicole Tietz、Brendan Gregg、Julia Evans 等业界顶级工程师的方法论。

## 为什么需要这个？

AI Agent 在调试时容易陷入以下陷阱：
- 🚨 **醉汉反模式** — 随机改代码直到问题消失
- 🚨 **路灯反模式** — 只在熟悉的地方找，而不是问题真正在的地方
- 🚨 **补丁链** — 每次报新错就修那个错，越改越乱
- 🚨 **忽略用户** — 用户说"改了X就坏了"，却继续自己猜

这套方法论提供了一个**强制性的调试流程**，避免这些常见错误。

## 核心流程

```
Phase 1: STOP    → 动手前先搞清现状（进程、环境、启动命令）
Phase 2: THINK   → 形成一个假设（优先查自己改了什么）
Phase 3: TEST    → 一次改一个，验证后再继续
Phase 4: DETECT  → 改了2次没好？全部回退，重新来
```

## 快速决策树

```
Error appears
  ├─ Was I just editing? → DIFF my changes → REVERT if suspect
  ├─ Service won't start? → CHECK startup command + environment
  ├─ New error after fix? → STOP (patch chain!) → Revert all → Phase 1
  ├─ User reports regression? → DIFF before/after their last known-good
  └─ Intermittent? → CHECK logs + external dependencies + timing
```

## 作为 OpenClaw Skill 使用

将 `SKILL.md` 放入你的 skills 目录：

```bash
mkdir -p ~/.agents/skills/debug-methodology
cp SKILL.md ~/.agents/skills/debug-methodology/
```

重启 OpenClaw 后，所有 session 遇到调试场景会自动加载这套方法论。

## 完整规范

详见 [SKILL.md](SKILL.md) — 包含：

- **4阶段调试流程**（STOP → Hypothesize → Test → Patch-Chain Detection）
- **4大反模式警告**（醉汉/路灯/货物崇拜/忽略用户）
- **环境检查清单**（runtime/deps/config/process manager/logs/backup）
- **部署安全流程**（拉取→备份→修改→测试→部署→验证）
- **快速决策树**

## 起源

这套方法论源自一次真实的生产事故：

修复一个简单的超时问题（2步就能搞定），却因为重启服务时没用虚拟环境，走了10步弯路。事后复盘发现，如果一开始跑一句 `ps -p <PID> -o command=` 就能避免所有问题。

由此总结出这套通用调试规范，并结合业界最佳实践形成了完整的方法论。

## Install

```bash
clawhub install debug-methodology
```

## Wiki

更详细的案例分析和扩展内容请查看 [Wiki](../../wiki)。

## 🔗 Part of the AI Dev Quality Suite

| Skill | Purpose | Install |
|-------|---------|---------|
| [bug-audit](https://github.com/abczsl520/bug-audit-skill) | Dynamic bug hunting, 200+ pitfall patterns | `clawhub install bug-audit` |
| [codex-review](https://github.com/abczsl520/codex-review) | Three-tier code review with adversarial testing | `clawhub install codex-review` |
| **debug-methodology** (this) | Root-cause debugging, prevents patch-chaining | `clawhub install debug-methodology` |
| [nodejs-project-arch](https://github.com/abczsl520/nodejs-project-arch) | AI-friendly architecture, 70-93% token savings | `clawhub install nodejs-project-arch` |
| [game-quality-gates](https://github.com/abczsl520/game-quality-gates) | 12 universal game dev quality checks | `clawhub install game-quality-gates` |

## License

MIT
