# DeepSeek Harness — Windows 部署避坑 Skill

给 **agent** 看的一份实战指南：如何在 **Windows** 上把 DeepSeek Harness
（`deepseek-ai/deepseek-harness`）源码安装、构建、启动、并配好工作区，跳过所有已踩过的坑。

> 这是 **Agent Skills** 格式的技能包（核心是 `SKILL.md`），由 WorkBuddy / OpenClaw 等支持
> Agent Skills 标准的 agent 自动加载；不是给人直接执行的脚本。

## 适用范围与边界（先读）

本技能**只**覆盖在 Windows 上安装 / 构建 / 启动 / 排错 DeepSeek Harness 本身：

- 不覆盖搭建新项目脚手架、跨平台桌面应用开发、Electron / Tauri 打包——这些由独立的
  `deepseek-harness-desktop-shell` 技能负责。
- 不覆盖任何与 Harness 部署无关的环境改动。
- 高影响步骤（清空 `NODE_OPTIONS`、结束端口 3080 进程、删除 `~/.dsh` 下的文件）执行前需先向用户说明并确认；
  给出的模式只适用于 Harness 排错，不得套用到其他场景。
- 若任务只是"做个桌面应用""打包成 exe"，应交给桌面套壳技能，而不是本技能。

## 这个 skill 解决什么

- pnpm / corepack 在 Windows + 托管 Node 下路径损坏 → 用 PowerShell 直调 `corepack.js`。
- WorkBuddy 沙箱注入的 `genie-safe-delete` 钩子导致 Harness 写盘失败 → 启动加 `NODE_OPTIONS=""`。
- 迁移后 `EPERM` 目录符号链接、端口 3080 残留占用。
- 工作区持久化位置（`~/.dsh/storages/workspace.json`）与"选不中工作区"的排查。

## 兼容性

本技能遵循开放的 **Agent Skills 标准**（`SKILL.md` + frontmatter），任何支持该标准的 agent 都能加载。

- **已确认适用**：WorkBuddy、OpenClaw（技能生态 100% 兼容，ClawHub 市场可一键安装）。
- **格式兼容、待官方确认**：Claude / Claude Code、Cursor、Windsurf、Codex（OpenAI）等——
  若实现 Agent Skills 标准即可直接加载；是否原生加载请以各产品官方文档为准。
- **需单独确认**：Hermes（独立 agent 产品，运行时加载机制以官方为准）。
- **操作系统**：Windows 10 / 11。
- **说明**：除标注的"WorkBuddy / CodeBuddy 沙箱特有"坑外，其余坑（pnpm、端口、EPERM 符号链接、
  工作区语义）对所有在 Windows 部署 Harness 的 agent 都有参考价值。

## 目录结构

```
deepseek-harness-windows-deploy/
├── SKILL.md                      # 给 agent 的主指令（核心结论、启动命令、兼容性、安全边界）
├── README.md                     # 本文件（给人看）
└── references/
    └── deploy-pitfalls.md        # 详细避坑清单（成因 + 解法）
```

## 如何使用（agent 侧）

- **自动**：安装到 `~/.workbuddy/skills/`（或 OpenClaw 对应 skills 目录）后，agent 在相关
  任务（部署 / 构建 / 启动 / 排错 DeepSeek Harness on Windows）时自动触发。
- **手动**：把本目录整体放进 agent 的 skills 目录即可。

## 版本更新

- **v1.0.4**（2026-08-14）：新增 `README.en.md`（人读英文版），结构与本中文 README 一致，便于英文用户直接阅读。无技能行为变更。
- **v1.0.3**（2026-08-14）：回应 ClawHub 安全扫描（skillspector）的多条意见，做针对性加固——
  - 新增「适用范围与边界」小节，明确不覆盖桌面套壳 / 脚手架，并声明高影响步骤需先向用户确认、模式不得外溢（对应 SQP-1）。
  - 强化「安全与防护边界」：`NODE_OPTIONS=""` 明确为**仅作用于 dsh web 单个进程**、非全局关闭，并加"执行前需用户确认"；常驻服务声明为用户可控（对应 RA2 / TM1 / persistence_privilege）。
  - 全文去除 emoji，清理中英文混杂的表达，并将命令中的个人路径改为占位符。
- **v1.0.2**（2026-08-14）：从 skill 中移除「桌面套壳（可选）」整节及 `references/desktop-shell-prompt.md`（该主题将独立成 skill / 项目）。纯文档清理，无行为变更。
- **v1.0.1**（2026-08-14）：回应 ClawHub 平台 LLM 审核意见，在 `SKILL.md` 新增「安全与防护边界（重要）」小节。
  - 明确 `NODE_OPTIONS=""` **仅用于启动 `dsh web` 这一条命令**，目的是绕过沙箱注入的 `genie-safe-delete` 钩子，并非关闭系统/文件系统安全机制，不应套用到其他命令或长期环境。
  - 明确 `fs.rmSync(path,{recursive:true,force:true})` **只针对** `~/.dsh/profiles/node_modules/@deepseek-ai/dsh-goal-round-driver` 这一个失效的目录符号链接，可重建、路径精确、不触及任何用户数据。
- **v1.0.0**（2026-08-14）：首发，覆盖 Windows + 托管 Node 环境下部署 DeepSeek Harness 的全部已知坑与已验证命令。

## 许可

MIT
