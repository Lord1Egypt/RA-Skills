# Lessons Learned — Codex on WSL2

## 已知坑

### 1. SIGTERM（最常见）
**现象：** Codex 写文件到一半被 kill，退出码 124/143。
**原因：** OpenClaw exec 工具有超时上限，Codex PTY 进程被 SIGTERM。
**解法：** 用 tmux 托管（见 SKILL.md），OpenClaw 只负责 `tmux new-session`，不持有进程。

### 2. 环境变量未继承
**现象：** `codex exec` 报 401 Unauthorized。
**原因：** 非交互 shell 不 source `.bashrc`，OPENAI_BASE_URL 丢失，直连官方 API。
**解法：** 每次显式传 `OPENAI_API_KEY` + `OPENAI_BASE_URL`，或写入 `~/.profile`（登录 shell 继承）。

### 3. TypeScript 模板字符串嵌套
**现象：** `WebchatProvider.ts` 编译报 "Unterminated template literal"。
**原因：** 内嵌 HTML 字符串用了 TS template literal，HTML 里的 JS `${var}` 被误解析。
**解法：** 内嵌 HTML 里的动态部分改成字符串拼接：`'msg ' + type`，而非 `` `msg ${type}` ``。

### 4. @fastify/websocket 版本冲突
**现象：** 启动报 `expected '^4.x' fastify version, '5.x' is installed`。
**原因：** Codex 装了 Fastify v5，但旧版 `@fastify/websocket` 只支持 v4。
**解法：** `npm install @fastify/websocket@latest`，已在 package.json 固定，一次性问题。

### 5. codex exec vs codex interactive
**现象：** `codex exec --skip-git-repo-check` 在非 git 目录报错。
**解法：** 总是在 git repo 内运行，或加 `--skip-git-repo-check`。
**注意：** `codex exec` 适合单次无状态任务；复杂多步任务用 `codex --full-auto`（交互模式）via tmux。

## 模型选择

| 任务 | 模型 |
|------|------|
| 后端逻辑、多文件重构 | `gpt-5.3-codex` |
| 快速测试、验证连通性 | `gpt-4.1-mini` |
| 前端 UI 原型 | `gpt-5.3-codex` + 明确说明组件库 |

## MyClaw 项目上下文

- 路径：`~/MyClaw`
- GitHub：https://github.com/InuyashaYang/MyClaw
- Phase 1 完成：Webchat + LLM streaming（TypeScript + Fastify + Vercel AI SDK）
- Phase 2 待做：工具系统（exec/read/write/web_fetch）+ Memory 注入 + Ask 确认
- Phase 3 待做：Telegram Provider + SQLite 持久化
- Phase 4 待做：Skills 加载器
