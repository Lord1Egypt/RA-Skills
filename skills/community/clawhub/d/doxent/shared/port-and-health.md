# 端口与健康检查规则

## 默认入口与端口回退

- 默认基址：`http://127.0.0.1:46588`
- `doxent_api.py` 先检查请求 URL 的默认端口；默认端口不可达时，再读取 `%APPDATA%/doxent/open_model_config.json` 及跨平台等价路径中的 `port` 重试。
- Windows 下还会隐藏查询当前用户的 `doxent-cli.js --doxent-cli-daemon --port ...` 进程参数，用于兼容旧 CLI 没有把实际端口写回配置的情况；该检查不会弹出 PowerShell 窗口。
- 不要无条件把默认 URL 改写成配置端口：配置可能过期，而默认端口上的当前服务仍可能可用。

## 自动启动与登录

- API 请求发现本地服务不可用时，由 `doxent_api.py` 自动查找并启动当前 Doxent CLI；默认优先使用 `DOXENT_CLI_PATH`，其次查找 Doxent CoreCLI 安装目录。
- Doxent CLI 无参数启动后台 Core；首次启动会按 CLI 自身生命周期打开 Web 登录页，已有会话直接复用。
- `doxent_api.py` 自动发现显式 `DOXENT_NODE`、系统 PATH 或 Codex 缓存中的 Node 运行时并注入 CLI 子进程，不要求用户手工配置。
- skill 启动 CLI、登录、帮助和停止命令时使用隐藏控制台模式；登录只打开浏览器页面，不打开终端窗口。
- 不要手动拼接 `npm run core:cli`、`--background-open-model` 或 Electron 启动命令；安装后的 skill 不应依赖源码仓库。
- 关闭终端不会停止 CLI daemon。仅在用户明确要求停止时运行 `--cli-action stop`。
- 每次真实数据脚本先确保 CLI daemon 已启动，脚本完成后保持其运行，不自动发送停止命令。
- 如果找不到 CLI，先按平台/架构自动下载：Windows 安装到用户级 `Doxent/CoreCLI`，macOS/Linux 将发布文件重命名为 `~/.local/bin/doxent-cli`、赋执行权限并持久化 PATH 与 `DOXENT_CLI_PATH`；下载失败、登录未完成或会话失效时，再提示运行 `--cli-action help` 查看当前版本命令。
- 即使本地服务已健康，也先检查云端 `ETag`、`Last-Modified` 和缓存摘要；版本更高或同版本文件摘要变化时，自动停止旧 daemon、替换用户级 CLI 并重新启动。

## 健康检查映射

- notes → 检查 `/open-model-note/health`
- books → 检查 `/open-model-book/health`
- schedules/tasks → 检查 `/open-model-schedule/health`

健康检查由 `doxent_api.py` 在请求前自动完成；业务模块不应重复检查，也不应把 health 当成写操作成功的证明。
