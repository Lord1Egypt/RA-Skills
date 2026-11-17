# 网盘通（cloud-drive-downloader）
**[English](./README.en.md) | [中文](./README.md)**


通用下载调度层。用户链接可从 Agent / MCP / CLI、Web UI 或浏览器插件进入 pan 调度层，再交由本机、NAS Docker、服务器 Docker 或远程引擎执行。
支持 macOS / Windows / Linux；默认本机 Agent / CLI 下载，NAS 不是前置条件。

## 三类入口

- **Agent / MCP / CLI**：`scripts/pan.py route --brief` 一次完成链接识别/登录门禁/预检并省 token，`scripts/pan.py get` 执行下载；无服务模式可直接调用，也可通过 `scripts/pan_mcp.py` 接入 Codex 或通用 MCP 客户端。
- **Web UI**：`bash scripts/pan.sh serve` 后访问 `http://127.0.0.1:<port>`；登录/授权走 `/login`，零客户端桥走 `/engines`，进度走 `/live`；NAS/服务器模式访问 `http://<nas>:<port>` 或 `http://<server>:<port>`。
- **浏览器插件**：加载 `extensions/chrome/`，支持 Chrome 与 Edge，可投递到本机、NAS 或服务器地址。

## 能力

- 识别网盘、直链、磁力、种子、网页视频；已知网盘先做纯本地登录/授权门禁，再优先走官方网页会话桥、浏览器直链桥、AList、OAuth/WebDAV；BaiduPCS-Go / quark-cli 等只作显式兼容回退。
- 公开搜索与网页候选：`search` / `crawl` / `movie` / `movie x`，只处理你有权访问的内容。
- 可选部署：`docker` 生成 Dockerfile、compose 与 install.sh；NAS 或服务器均可运行。
- 远程模式：`remote` 把任务交给你自己的 SSH 主机、挂载盘或私有存储。

配置优先级：`CLI 参数 > 环境变量 > config.json > 内置默认值`。示例占位符：`<api-url>`、`<download-dir>`、`<port>`、`<pan-root>`。

快速开始与三系统用法见 `SKILL.md`；Docker 属于可选部署，详见 `references/33-Docker部署与一键搜索.md`。

合规说明：只走官方网页会话、官方接口、用户在官方网页触发的下载 URL 和通用直链；不破解、不伪造登录态，不绕过验证码/风控/限速/会员/DRM；插件不读取网页登录态；凭据只放系统凭据库；用户对下载内容合法性负责。

## 单实例、续传与失败诊断（v0.16.0）

- 同一 `(网盘, 来源, 目标目录)` 只允许一个下载进程；抢不到锁会直接返回退出码 `9`，不会继续覆盖断点。
- 查看/清理锁：`bash scripts/pan.sh guard status`、`bash scripts/pan.sh guard clean`。
- 续传不要加 `--ow`；计划构建阶段会自动剥离，并补 `--retry 5`。
- 后台任务使用双 fork：`bash scripts/pan.sh guard daemon --cmd '<命令>' --log <日志路径>`，不要用 `nohup ... &`。
- 低速度先用 `bash scripts/pan.sh guard speed --target <目录> --seconds 20` 采样；低于 200 KB/s 会提示网盘侧限速/免费账号特征，不混同登录失败。
- 错误先用 `bash scripts/pan.sh guard error --text '<原始错误>'` 归类，再按返回的 `remediation` 处理。


## 支持边界（v0.20.1）

- 非百度路由：浏览器直链捕获桥通用于所有官方网页登录；AList 驱动桥覆盖绝大多数已登记盘（阿里/夸克/天翼/迅雷/115/123/移动/联通/UC/PikPak/OneDrive/Google/Dropbox/微云/蓝奏等）；OAuth/WebDAV 桥覆盖官方开放平台与 WebDAV 盘（坚果云等）。
- 明确“不支持/需接入”的盘名与判定规则见 `references/40-网盘支持矩阵.md`；未接入盘不得当作 HTTP 直链抓取分享页，必须标“不支持/需接入”。
- 各盘真机验证的最小授权方式见 `references/41-真机验证权限清单.md`；未授权前对应盘标记“待用户提供”，不虚报真机数。第三方依赖说明见 `NOTICE.md`。
