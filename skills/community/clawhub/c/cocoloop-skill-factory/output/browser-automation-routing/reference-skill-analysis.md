# Browser Automation Routing - 参考 Skill 本地分析

## 分析对象

- `/Users/tanshow/.codex/skills/opencli/SKILL.md`
- `/Users/tanshow/.codex/skills/playwright-interactive/SKILL.md`
- `/Users/tanshow/.codex/.tmp/plugins/plugins/vercel/skills/agent-browser/SKILL.md`
- `/Users/tanshow/.codex/.tmp/plugins/plugins/vercel/skills/agent-browser-verify/SKILL.md`

本次同时核对了官方公开来源：

- `jackwener/OpenCLI`
- `vercel-labs/agent-browser`

## 1. opencli

### 值得复用的能力

- 已有站点命令、真实浏览器控制、适配器生成三条路径
- 强调复用 Chrome 或 Chromium 已登录状态
- `opencli doctor` 提供统一验收入口

### 设计要点

- 更像统一执行面，而不是单次浏览器脚本
- 适合账号态业务和多站点统一命令入口
- 需要把 Browser Bridge 扩展安装说明交给用户

### 不适合直接当默认答案的情况

- 目标站点明显不在支持面里
- 用户不能接受扩展安装
- 任务更偏本地调试而不是网页登录态流程

## 2. agent-browser

### 值得复用的能力

- 独立浏览器自动化 CLI
- 截图、快照、等待、表单操作直接成型
- 适合本地页面验证和页面回归

### 设计要点

- 官方安装方式清楚，支持 `npm`、`brew`、`cargo`
- 首次使用必须执行 `agent-browser install`
- 更适合作为受控自动化执行面

### 不适合直接当默认答案的情况

- 用户必须复用当前个人浏览器登录态
- 业务已经被 `OpenCLI` 的现成命令和浏览器能力覆盖

## 3. playwright-interactive

### 值得复用的能力

- 持久 Playwright 会话
- 本地 Web 与 Electron 的功能 QA 和视觉 QA
- 改代码后继续复测的调试节奏

### 设计要点

- 依赖 `js_repl`
- 需要安装 `playwright`
- 环境准备成本明显更高

### 不适合直接当默认答案的情况

- 任务只是网页登录态自动化
- 用户要的是简单安装和直接上手

## 汇总结论

这三条路径各自解决的重点不同，所以 `skill-factory` 需要把它们作为路线比较对象。

推荐顺序如下：

1. 用户接受安装，且业务被 `OpenCLI` 覆盖时，优先 `OpenCLI`
2. 页面验证、结构化快照、独立浏览器自动化更重要时，优先 `agent-browser`
3. 本地调试、持久会话 QA、Electron 场景更重要时，优先 `playwright-interactive`
