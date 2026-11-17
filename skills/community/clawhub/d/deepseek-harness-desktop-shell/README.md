# DeepSeek Harness — 桌面套壳（Electron）Skill

给 **agent** 看的一份实战指南：如何把**已经在本地跑起来的** DeepSeek Harness Web UI
（默认 `http://127.0.0.1:3080`），用 Electron 包装成一个桌面应用（exe / app），开箱即用，
且完整保留 Harness 自身的功能与插件体系。

> 这是 **Agent Skills** 格式的技能包（核心是 `SKILL.md`），由 WorkBuddy / OpenClaw 等支持
> Agent Skills 标准的 agent 自动加载；不是给人直接执行的脚本。

## 适用范围与边界（先读）

- 本技能**只**覆盖桌面套壳本身：用 Electron 包住本地已运行的 Harness Web UI。
- DeepSeek Harness 的安装 / 构建 / 启动 / 排错，由独立的 `deepseek-harness-windows-deploy`
  技能负责；本技能只消费它跑起来的 Web UI。
- 高影响步骤（安装依赖、执行打包 / 分发、在用户目录新建或修改工程文件）执行前需先向用户说明并确认。

## 这个 skill 解决什么

- 不想每次都开浏览器、手输 `http://127.0.0.1:3080`——包成桌面窗口，打开即用。
- 给出**最小可运行**的 Electron 壳，以及完整的工程脚手架 / 打包任务提示词。
- 关键约束：壳只做"容器"，不内嵌业务代码；完整保留 Harness 的页面逻辑与插件/扩展能力。

## 兼容性

- 实测环境：Windows 10 / 11。Electron 本身跨平台，macOS / Linux 同理。
- 前置：已装 Node + npm 且能联网；纯 webview 壳**无需** Visual Studio 编译工具。
- 与 `deepseek-harness-windows-deploy` 配合：先按它把 `dsh web` 跑起来，本技能再包壳。

## 目录结构

```
deepseek-harness-desktop-shell/
├── SKILL.md                           # 给 agent 的主指令（范围、核心思路、安全注意）
├── README.md                          # 本文件（给人看）
└── references/
    └── desktop-shell-prompt.md        # 完整工程脚手架 / 打包 / 插件保留策略的任务提示词
```

## 如何使用（agent 侧）

- **自动**：安装到 `~/.workbuddy/skills/`（或 OpenClaw 对应 skills 目录）后，agent 在相关
  任务（把本地 Harness Web UI 包成桌面应用）时自动触发。
- **手动**：把本目录整体放进 agent 的 skills 目录即可。

## 版本更新

- **v1.0.0**（2026-08-14）：首发。从 `deepseek-harness-windows-deploy` 中拆分出来，独立承担
  "桌面套壳（Electron 包装本地 Harness Web UI）"这一主题，满足 ClawHub 安全扫描关于技能范围
  收敛的建议（SDI-1）。

## 许可

MIT
