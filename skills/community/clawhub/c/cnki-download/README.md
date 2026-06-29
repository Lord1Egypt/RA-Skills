# CNKI 知网下载

- 平台支持：Windows（需要可视化登录）
- 入口：首次运行会要求用户提供知网搜索页面的 URL，保存到 `scripts/user_config.json`，后续直接复用
- 依赖：Node.js（用 openclaw 说明你已有）+ Microsoft Edge（agent 自检）
- 脚本：Node.js（Playwright + 系统 Edge）
- 使用：直接说"知网下载"，AI 会引导后续流程
- 首次登录以后可能会有些问题，再试一次应该就可以了
