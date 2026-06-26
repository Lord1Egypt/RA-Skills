# 🚀 DevLoop Agent Pack

**产品驱动开发闭环** — 一个开箱即用的多 Agent 协作系统。

> **6 个专业 Agent** — 覆盖从**产品热点探索**到**开发测试上线**的完整生命周期。

## Quick Start

```bash
/plugin install devloop
```

安装后自动注册所有 Agent 和 Skill，无需额外脚本。

## 包含的 Agent

| Agent | ID | Emoji | 核心职责 | Model |
|-------|-----|-------|----------|-------|
| **Product** | `devloop-product` | 🎯 | 每日 AI 热点探索、产品方向讨论、PRD 生成 | Sonnet |
| **Core Dev** | `devloop-core-dev` | 🧠 | 架构设计（7 维度）、设计文档、Dev 调度 | Opus |
| **Dev** | `devloop-dev` | ⚡ | 精准编码、多实例并行、按设计文档实现 | Sonnet |
| **Test** | `devloop-test` | 🧪 | 测试先行、Bug 趋势追踪、代码审查 | Sonnet |
| **Marketing** | `devloop-marketing` | 📣 | 商业化调研、宣传策略、文案制作 | Sonnet |
| **Research** | `devloop-research` | 🔬 | 深度调研、竞品分析、技术评估 | Sonnet |

## 核心工作流

```
Cron → 🎯 Product（热点探索 + 历史对比）
          ↓ 用户确认方向 + PRD
        ↙          ↘
📣 Marketing    🧠 Core Dev（讨论→设计→调度）
                      ↓
            ⚡ Dev ×N（并行编码）
                      ↓
            🧪 Test（测试先行 + Review）
                  ↓
             合并 main → 📣 Marketing（上线宣传）
```

## Skills

| Skill | 描述 |
|-------|------|
| `devloop-workflow` | 完整的多 Agent 协作工作流定义，含协作协议、Agent 设计背景参考和 9 个工作模板 |

详细内容参见 `skills/devloop-workflow/` 目录：
- `SKILL.md` — 工作流概览、通用规范、模板清单、参考资料索引
- `references/collaboration-protocol.md` — 完整协作协议、消息路由表
- `references/agent-design-background.md` — 各 Agent 设计理念与边缘情况
- `assets/templates/` — 9 个标准化工作模板

## 自定义

- `SOUL.override.md` — 修改 Agent 行为（升级不覆盖）
- `USER.md` — 个人信息与偏好
- `MEMORY.md` — 自定义调研维度

优先级：`SOUL.override.md` > `SOUL.md` > 各 Agent `.md`

## Repository Structure

```
devloop-agent-pack/
├── .claude-plugin/
│   └── plugin.json                         # 插件元数据
├── agents/                                 # 6 个专业 Agent
│   ├── devloop-product.md
│   ├── devloop-core-dev.md
│   ├── devloop-dev.md
│   ├── devloop-test.md
│   ├── devloop-marketing.md
│   └── devloop-research.md
├── skills/                                 # Agent Skills
│   └── devloop-workflow/
│       ├── SKILL.md                        # Skill 主文件（工作流 + 规范）
│       ├── references/                     # 按需加载的参考资料
│       │   ├── collaboration-protocol.md
│       │   └── agent-design-background.md
│       └── assets/                         # 模板文件（Agent 创建文件时使用）
│           └── templates/
│               ├── project-structure.template.md
│               ├── design-doc.template.md
│               ├── design-index.template.md
│               ├── test-spec.template.md
│               ├── daily-report.template.md
│               ├── bug-tracker.template.md
│               ├── review-notes.template.md
│               ├── bug-trend.template.md
│               └── memory-tracking.template.md
└── README.md
```

## Contributing

1. Fork 本仓库
2. 修改 `agents/` 下的 Agent 文件或 `skills/` 下的 Skill 文件
3. Agent 文件使用 YAML frontmatter（`name`, `description`, `model`, `tools`）
4. Skill 文件遵循 Anthropic Agent Skills Specification
5. 更新 `.claude-plugin/plugin.json` 中的版本号
6. 提交 PR

## License

MIT — 详见 `plugin.json` 中的 `license` 字段。
