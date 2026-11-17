---
name: browser-ops
description: 浏览器操作方案路由：按场景在视觉驱动/选择器快照/CDP/MCP 四方案间选型，含登录态、文件上传、人机验证人工兜底等横切决策
source:
  type: original
  repo: skills-repo/ai-fullstack-engineer
  path: skills/browser-ops/SKILL.md
  version: 1.0.0
  updated: 2026-10-28
metadata:
  category: 浏览器自动化
  platform: Web
  difficulty: 进阶
---

# 浏览器操作方案路由（Browser Ops）

> 一个入口回答「这个浏览器任务该用哪个方案」：先给选型决策表与三问决策法，再路由到对应子技能或 MCP 形态；横切关注点（登录态 / 文件上传 / 人机验证 / 合规）统一收敛到 playbook。

## 能力

- 四方案路由决策表：视觉驱动 / 选择器快照 / CDP / MCP，每格含「何时不用」反指示
- 三问决策法：定位可否结构化 → 登录态要求 → 消费方形态
- 横切关注点路由：登录态三模式、文件上传最小授权、人机验证人工兜底、平台 ToS 合规边界
- 复杂动态表单（电商发布页类）的内容包驱动填充策略

## 使用方式

在 Claude Code 中使用 `/browser-ops` 调用。

```
/browser-ops 我要在淘宝发布页自动填表，类目树是自研组件、属性随类目动态渲染
/browser-ops 把浏览器操作能力接给 MCP 客户端做常驻自动化
/browser-ops 这两个浏览器方案该选哪个？页面会改版，登录态要保住
```

## 方案路由表（核心）

| # | 场景特征 | 方案 | 加载 | 何时不用 |
|---|---------|------|------|---------|
| A | 选择器不稳定、动态渲染表单、只有截图、Canvas/富交互 | **视觉驱动** | [ai-browser-automation](../ai-browser-automation/SKILL.md) | 结构稳定且要进 CI 的正式断言（用 B） |
| B | 页面结构稳定、要可复现脚本 / CI 用例、快照 ref 可靠 | **选择器快照** | `software-tester` 的 [e2e-testing](https://github.com/skills-repo/software-tester) | 动态表单硬写选择器，改版即坏（换 A） |
| C | 调试诊断、性能审计、接管已打开的真实浏览器 | **CDP** | [browser-devtools](../browser-devtools/SKILL.md) | 只是批量填表（用 A/B 更直接） |
| D | 消费方是 MCP Client / 平台型 Agent，需工具化常驻复用 | **MCP** | [browser-mcp](../browser-mcp/SKILL.md) | 一次性任务直接用 A/B/C 更轻 |

**横切关注点**（登录态三模式、文件上传、验证码人工兜底、ToS 合规、动态表单内容包）一律先读
[references/browser-ops-playbook.md](references/browser-ops-playbook.md)（随本技能安装，单装自包含）—— 方案怎么选完都要过这五关。

## 三问决策法

1. **元素定位**：无障碍快照里能稳定拿到 ref 吗？能 → B / C；不能（自研组件、随数据动态渲染）→ A
2. **登录态**：需要保持登录吗？临时任务 → 各方案自带 session；长期复用 → CDP 接管真实浏览器或持久 profile（选型见 playbook）
3. **消费方**：人 / 脚本手动触发 → A / B / C 走 CLI；要挂给 Agent / MCP Client 常驻调用 → D（MCP 内部仍是 B 的快照定位）

## 工作流

1. 用三问决策法定位方案编号
2. 查路由表，加载对应子技能（动态表单先准备**内容包**：结构化 JSON 逐字段对应表单项）
3. 按子技能工作流执行；涉及登录态 / 上传 / 验证码时回 playbook 查 SOP
4. 执行后按子技能方式验证（截图 / 断言 / 快照）
5. 失败按 playbook 降级路径处理（视觉兜选择器、人工按内容包手填）

## 红线（违反即停）

- 遇到滑块 / 验证码 → **人工兜底**：暂停、交给人操作、截图确认后继续；绝不自动绕过，不编写风控对抗代码
- 登录态操作只做用户明确授权的动作，敏感值不进任务总结与 shell 历史
- 平台 ToS 风险如实告知：低频、拟人节奏、真实内容；不做批量铺货式群控

## 适用场景

- 电商 / 后台复杂动态表单自动化（选 A + playbook 内容包策略）
- 把浏览器操作做成 Agent 可复用工具、多客户端共享（选 D）
- 团队内统一浏览器自动化选型口径，避免「上来就写选择器脚本」

## 限制

- 本技能是路由与决策层，不含具体命令（在各子技能与 playbook 中）
- 不覆盖移动端 App 自动化（Midscene android/ios 切片不在组织范围）
- 社区 stealth / anti-detect / 风控对抗类技能**明确不纳入**（合规红线）
