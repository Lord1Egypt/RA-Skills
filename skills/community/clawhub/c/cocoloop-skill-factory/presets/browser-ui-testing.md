# 浏览器自动化与 UI 测试预设

## domain_id

`browser_ui_testing`

## common_jobs

- 页面截图与快照
- 表单与交互验证
- 浏览器流程自动化
- 持久会话 QA
- 本地 Web 或 Electron 调试

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 当前任务是网页登录态流程、本地页面验证，还是持久调试
- 是否必须复用当前浏览器登录态
- 是否接受额外安装 CLI、扩展或 Playwright
- 是否涉及批量抓取、批量发布、社媒互动或账号敏感操作
- 当前有没有 API、导出接口或轻量替代路径

## recommended_execution_planes

- `Skill + OpenCLI`
  适合复用当前浏览器登录态和现成站点命令
- `Skill + agent-browser`
  适合独立浏览器流程、截图、快照、表单验证
- `Skill + Playwright`
  适合本地 Web 或 Electron 调试、持久会话 QA

## risk_and_gates

- 先提示账号、验证码、反爬、平台规则和会话安全风险
- 至少比较两条执行路径
- 如果用户接受额外安装且覆盖面足够，优先 `OpenCLI`
- 批量发布、批量抓取和社媒互动要提高风险等级

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 若进入协议收口，`spec.yaml` 里必须写清 `fallback_policy`
