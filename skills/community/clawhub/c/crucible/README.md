# 🔬 Crucible — 严峻考验式交付管线

> 每个 Stage 是一次考验，每道 Gate 是一次试炼，只有经得起考验的代码才能交付。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Crucible** 是一个 Claude Code Skill 插件，实现多阶段、多角色的产品交付管线。支持从原始需求到可交付产品的全流程编排，内置质量门禁（Gate）和自审循环（Self-Review Loop）。

---

## ✨ 核心特性

- **多阶段管线**：PM → UX → Dev → Test，全流程覆盖
- **Gate 门禁**：每道 Gate 独立审查，PASS 放行 / REJECT 返工
- **Stage 内自审循环**：implement → review → fix → review，质量在阶段内收敛
- **并行 Fan-out**：开发阶段支持 backend / frontend / admin 并行
- **API 契约校验**：Gate 3 自动比对前后端接口一致性
- **遗留项传递**：Gate N 的 leftover 自动注入 Stage N+1
- **6 种使用模式**：完整交付 / 开发+自审 / 并行+契约 / 仅审查 / 自定义

## 📐 架构

```
外层: [Stage 1] → [Gate 1] → [Stage 2] → [Gate 2] → ... → ✅

内层（每个 Stage）:
  implement → self-review → fix → self-review → PASS → 提交 Gate
```

### 完整 8 阶段

```
[PM/PRD ⟳] → [Gate 1] → [UX 设计 ⟳] → [Gate 2]
    → [Dev∥Dev∥Dev ⟳] → [Gate 3]
    → [测试 ⟳] → [Gate 4] → ✅
```

⟳ = Stage 内部的 implement→review→fix 自审循环

---

## 🚀 快速安装

### Linux / macOS

```bash
git clone https://github.com/YvanCheng/crucible.git
cd crucible
bash install.sh
```

### Windows PowerShell

```powershell
git clone https://github.com/YvanCheng/crucible.git
cd crucible
.\install.ps1
```

安装完成后，重启 Claude Code 或运行 `/skills` 刷新，即可看到 `ccg:crucible`。

### 卸载

```bash
# Linux / macOS
bash install.sh --uninstall

# Windows PowerShell
.\install.ps1 -Uninstall
```

---

## 📖 使用方法

| 命令 | 模式 |
|------|------|
| `/ccg:crucible <需求>` | 完整 8 阶段交付 |
| `/ccg:crucible --dev <需求>` | 开发 + 自审（最常用） |
| `/ccg:crucible --dev --review <需求>` | 开发 + Gate 审查 |
| `/ccg:crucible --parallel <需求>` | 并行开发 + API 契约校验 |
| `/ccg:crucible --review-only <path>` | 仅审查现有代码 |
| `/ccg:crucible --stages dev,test <需求>` | 自定义阶段组合 |

---

## 🧬 融合方法论

Crucible 蒸馏了 Claude Code 生态中 5 大顶级 skill 的核心方法论：

| 来源 | 核心价值 |
|------|---------|
| **Ponytail** | 极简编码哲学 (The Ladder)、YAGNI、反过度工程 |
| **Superpowers** | TDD/BDD、子 Agent 编排、理性化防御、验证完成纪律 |
| **ECC** | 6 阶段验证循环、误报过滤、构建修复、10 节安全清单 |
| **OpenSpec** | 约束集驱动、零决策计划、PBT 属性提取 |
| **Codegraph** | 结构化代码智能（推荐 MCP 工具，非必需） |

自包含 — 不要求用户已安装上述任何 skill。

## 🗂️ 文件结构

```
crucible-skill/
├── README.md
├── LICENSE
├── install.sh / install.ps1
├── skill/                              # → ~/.claude/skills/ccg/crucible/
│   ├── SKILL.md                        # 主编排文件
│   ├── roles.md                        # Agent 角色模板
│   ├── gates.md                        # Gate 审查模板
│   ├── references/
│   │   ├── methodology.md              # Ponytail Ladder + 理性化防御
│   │   ├── verification.md             # Pre-Gate 6 阶段验证 + Build 恢复
│   │   ├── security-checklist.md       # 10 节安全清单
│   │   ├── tooling.md                  # Codegraph + OpenSpec 指南
│   │   └── lessons.md                  # 实战经验
│   └── companion/
│       ├── pm-disciplines.md           # PM: brainstorming + pattern grounding
│       ├── dev-disciplines.md          # Dev: Ladder + 双阶段审查 + build-fix
│       ├── test-disciplines.md         # Test: TDD + BDD + 系统调试法
│       └── gate-disciplines.md         # Gate: 误报过滤 + 分支收尾
└── command/                            # → ~/.claude/commands/ccg/
    └── crucible.md
```

---

## 🎯 适用场景

- 从零构建新产品（需要 PM + UX + Dev + Test 全流程）
- 前后端分离项目（需要确保 API 契约一致性）
- 代码质量审计（仅审查模式）
- 需要多角色协作的复杂开发任务
- 希望有质量保障的自动化开发流程

---

## ⚙️ 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `self_review` | `true` | Stage 内是否启用自审循环 |
| `self_review_rounds` | `3` | 自审最大轮次 |
| `gate.enabled` | `true` | Stage 后的 Gate 是否启用 |
| `gate.rounds` | `3` | Gate REJECT→Fix 最大轮次 |
| `parallel` | `false` | Stage 内是否并行 fan-out |
| `model` | `sonnet` | 执行 Agent 的模型 |
| `review_model` | 继承 `model` | 审查 Agent 的模型（建议 ≥ 执行模型） |

---

## 📄 License

MIT © 2026
