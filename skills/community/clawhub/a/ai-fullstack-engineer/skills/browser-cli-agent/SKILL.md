---
name: browser-cli-agent
description: 命令行驱动浏览器做验证：无障碍树快照定位、表单点击断言、会话复用与登录态保持
source:
  type: derived
  repo: vercel-labs/agent-browser
  path: skills/agent-browser/SKILL.md
  updated: 2026-11-03
  url: https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md
metadata:
  category: 浏览器自动化
  platform: Chrome/CDP
  difficulty: 进阶
---

# 浏览器 CLI Agent（给 Agent 用的网页操作通道）

> 适用场景：需要**真在浏览器里把事做完并拿出证据**——验证 PR 的 UI 改动、跑探索式测试、
> 复现一个只有真交互才暴露的 bug、从站点取结构化数据。
> 上游 CLI 是当前生态里信号最强的实现（`vercel-labs/agent-browser`，安装量 1.27M，
> 仓库 4.5 万 stars，持续日更）；本技能描述**通道选型与工作法**，命令细节以 CLI 自带指南为准。

## 能力

- **选型定位**：在 `browser-ops` 的四方案之外，补上"原生 CLI + 无障碍树引用"这条通道
- **工作法**：快照 → 定位元素引用 → 交互 → 再快照验证 的闭环，而不是盲写选择器
- **会话与登录态**：状态持久化、认证保管，避免每次重跑都要人工过登录
- **证据产出**：截图、录屏、控制台与网络日志，直接用于 PR proof 与 issue 复现
- **超出网页的范围**：Electron 桌面应用、Slack 工作区、云浏览器/沙箱执行环境

## 何时用它（与本地既有通道分工）

| 通道 | 何时选 | 现有技能 |
|---|---|---|
| CLI + 无障碍树引用 | 需要稳定元素定位、脚本化闭环、可复跑验证、CI 里执行 | **本技能** |
| 视觉驱动（截图→坐标） | 无选择器、Canvas/图像化 UI、人类视角验收 | [`ai-browser-automation`](../ai-browser-automation/SKILL.md) |
| 选择器/DOM 快照 | 已有稳定测试套件、DOM 语义清晰 | [`browser-devtools`](../browser-devtools/SKILL.md) |
| CDP 直连 | 精细控制网络/性能、拦截请求 | [`browser-devtools`](../browser-devtools/SKILL.md) |
| MCP 浏览器工具 | 宿主已接 MCP、需在工具协议内操作 | [`browser-mcp`](../browser-mcp/SKILL.md) |

> 方案总路由与登录态/文件上传/人工兜底等横切问题，先读
> [`browser-ops`](../browser-ops/SKILL.md)；本技能是那套路由里"CLI Agent 通道"的落地细则。

## 核心工作法：快照 → 引用 → 交互 → 复核

```
1. 打开目标页，拿一次结构化快照（无障碍树优先于 DOM 树：语义更稳、体积更小）
2. 从快照里取元素引用句柄，而不是自己拼 CSS/XPath
3. 用句柄执行动作（点击/输入/提交）
4. 动作后再取一次快照或断言，确认状态真的变了（不要假设成功）
5. 失败时读控制台与网络日志，再决定是重试还是换通道
```

**为什么强调"用快照里的引用"**：手写选择器在 UI 迭代后必坏，且 Agent 经常凭猜测构造选择器。
快照驱动把"元素是否存在"这个问题**提前到执行前**，能省下大量假成功。

## 命令细节以 CLI 下发为准

上游刻意把 `SKILL.md` 做成**发现桩**：它不复制一份可能过期的命令表，
而是让 CLI 自己下发与已安装版本匹配的指导内容（例如先取核心指南，再按其中索引取专题分册；
桌面应用、协作软件、探索式测试、云沙箱等各有专门分册）。

**照抄这一做法的理由**：CLI 迭代快，静态转写必然过期。
所以本技能只固定"何时用、怎么工作、失败怎么判"，具体子命令/参数**运行时向 CLI 要**，
不要从别处复制粘贴一份命令清单长期使用。

## 常见坑

| 坑 | 后果 | 修正 |
|---|---|---|
| 盲写选择器不验证 | 动作静默没生效，却报"已测试" | 交互后必须再快照/断言 |
| 无头环境跑带登录的流程 | 卡在验证码/二次认证 | 会话持久化复用，或留人工兜底一次 |
| 把 CLI 输出当证据 | 评审方无法复现 | 存截图/录屏 + 控制台与网络日志 |
| 冷启动即断 | 页面未 ready 就操作 | 显式等待条件，而非固定 sleep |
| 静态转写上游命令表 | CLI 升级后指令失效 | 运行时向 CLI 取当前版本指南 |
| 本地 `python3` 被 Xcode license 拦 | 脚本类辅助工具直接报错 | 用受管解释器绝对路径，或改走 `node`/`jq` |

## 边界与协作

- 通道总路由、登录态与人工兜底策略 → [`browser-ops`](../browser-ops/SKILL.md)
- 为 PR 产出 BEFORE/AFTER 证据的完整流程 → `skills-repo/open-source-contributor`
  的 [`github-contribution`](https://github.com/skills-repo/open-source-contributor)
- 端到端回归用例编写 → `skills-repo/software-tester` 的 `e2e-testing`
- 网页性能指标与网络面板分析 → [`web-performance`](../web-performance/SKILL.md)
