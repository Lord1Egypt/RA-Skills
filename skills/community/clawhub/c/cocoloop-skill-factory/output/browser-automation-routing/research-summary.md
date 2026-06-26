# Browser Automation Routing - 研究摘要

## 目标

把“强需求浏览器自动化时必须比较路线、`OpenCLI` 满足覆盖条件时优先、附带扩展安装说明”收口成正式研究结论。

## 本次核实对象

- 本地 Skill：`opencli`、`playwright-interactive`
- 本地临时插件 Skill：`agent-browser`、`agent-browser-verify`
- 官方仓库：`jackwener/OpenCLI`、`vercel-labs/agent-browser`
- 本机运行状态：`opencli --version`、`opencli doctor`、`agent-browser --version`

## 核实结果

### 1. `agent-browser` 是真实可用能力

- 官方仓库：`vercel-labs/agent-browser`
- CLI 包名：`agent-browser`
- 当前核实版本：`0.25.4`
- 官方安装方式：`npm install -g agent-browser`、`brew install agent-browser`、`cargo install agent-browser`
- 首次使用前置动作：`agent-browser install`

### 2. `OpenCLI` 的浏览器能力依赖 Browser Bridge 扩展

- 官方仓库：`jackwener/OpenCLI`
- npm 包名：`@jackwener/opencli`
- 当前核实版本：`1.7.4`
- 官方安装基线：安装 CLI、从 Releases 下载 `opencli-extension-v{version}.zip`、在 `chrome://extensions` 中 `Load unpacked`
- 官方验收命令：`opencli doctor`

### 3. 本机环境已具备两条执行面

- `opencli --version` 返回 `1.7.4`
- `opencli doctor` 返回 daemon 正常、extension 已连接、connectivity 正常
- `agent-browser --version` 返回 `0.25.4`

### 4. 三条路线的定位已经足够清楚

- `opencli`：优先解决复用当前 Chrome 或 Chromium 登录态、现成站点命令、浏览器内实时操作和适配器生成
- `agent-browser`：优先解决独立浏览器自动化、页面截图、结构化快照、表单与页面验证
- `playwright-interactive`：优先解决本地 Web 或 Electron 调试、持久会话 QA 和反复迭代验证

## 研究结论

后续 `skill-factory` 在处理强需求浏览器自动化任务时，需要把浏览器自动化视为路线选择问题，而不是单一工具推荐问题。

默认规则如下：

- 至少比较 2 条方向
- 如果用户接受额外安装，且业务被 `OpenCLI` 支持面覆盖，优先推荐 `OpenCLI`
- 推荐 `OpenCLI` 时，必须附带 Browser Bridge 扩展安装与 `opencli doctor` 验证说明
- 如果 `OpenCLI` 覆盖不足，继续保留 `agent-browser` 或 `playwright-interactive` 作为替代路径
