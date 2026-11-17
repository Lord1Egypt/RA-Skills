## 0.20.2 · 2026-11-09 · 常驻注入瘦身

- **description 精简**：技能目录注入的 description 压到 ≤45 字，保留原有触发词与「不做什么」边界；SKILL.md 正文与算法口径未变。

## v0.20.0（2026-10-28 · 提速三件套版）

## 0.20.1 · 2026-11-08 · 技能层瘦身与发布完整性

- **SKILL.md 瘦身**：11,701 B → 7,887 B（-32.6%）。触发词、硬规则、能力边界保留在前置段；低频细则外移到 `references/`、`docs/`、`packs/`，按需加载，算法与业务口径不变。
- **发布完整性**：被引用文件随包存在、Python/bash/JSON 语法通过、技能自检 PASS；未实现的检查如实记 SKIP。
- **脱敏**：本机路径、真实项目名与公司资料引用替换为通用示例；平台专用入口只改发布副本。


- **F1 自动分片**：http 直链下载前自动决策——探测 Range + 1MB 样本测速，单连接低于 `http.auto_split_threshold_kbps`（默认 1024kbps）自动按 `http.split_max_concurrency`（默认 4）切分片；`run_curl_split` 重写：并发池（跑完补位，不再 N 段全起）、**分片级复用**（完整 `.partNN` 直接跳过，重跑不浪费）、失败段单独重试 1 次、可选 `http.split_limit_rate` 透传 curl 限速。半成品段整段重下（curl 拒绝 `-C -` 与 `-r` 组合，段内续传不可行）。
- **F2 闲时队列**：`pan idle add|list|delete|run`——队列存 `STATE_DIR/queue/`，`pan idle run` 前台守护在 `http.idle_window`（默认 00:00-08:00，支持跨午夜）内逐个投递（子进程走 `pan get`，单实例锁防重）；`--print-crontab` 只打印条目**不安装**；`PAN_IDLE_FORCE=1` 跳过窗口判断（自测）。Web 设置页新增闲时窗口输入框。
- **F3 换赛道指南**：新增 `references/42-换赛道提速指南.md`（123 云盘 WebDAV / 夸克离线 / PikPak / 分享方换盘四路径对比与接法），SKILL.md 与 Web 教程页各加指针。
- self_test 54 组 / 516 项（新增组 96 F1、组 97 F2）。
- 边界重申：不接第三方解析站、不做进程变速、不自动写系统定时器、不逆向网盘协议、不承诺突破账号级限速。

## v0.19.0（2026-10-28 · 安全加固版）

- **Web API 全面启用 token 鉴权**：`pan serve` 启动即生成随机 token（存配置 0600），所有 `/api/*` 需 `Authorization: Bearer` 或 `?token=`；连败 10 次拉黑 5 分钟。修复此前配合 `--host 0.0.0.0` 可被局域网任意调用的暴露面。
- **on_complete_hook 收紧**：禁止经 Web/API 修改；执行前必须命中 `http.hook_whitelist` 目录白名单（`["-"]` 为显式全放行，不推荐），否则记 HOOK_BLOCKED 拒绝执行。
- `PAN_NOAUTH=1` 仅在回环绑定下允许关闭鉴权；非回环强制开启并红色警告。
- Chrome 扩展新增 API Token 输入项；feishu_bot 支持 `--pan-token` 转发鉴权、`--feishu-verify-token` 回调校验，**非回环监听未配 token 直接拒绝启动**。
- 修复 self_test 缺 `pan.cmd` 崩溃问题：改为分组执行、单项失败不中断（52 组 / 500 项）；补齐 `pan.cmd` 与 `docker/docker-compose.full.yml`（含 cdd-alist）。
- 移除零引用的 `scripts/credentials.py`（其 Windows PowerShell f-string 拼接存在注入面，统一走 engine.py 的 ctypes 凭据后端）。
- `baidu_login` 二维码改写系统临时目录 + 0600 权限（跨平台）；`serve` 帮助文案改为如实描述。

# Changelog


## 0.18.9 (2026-10-21)
- 三平台对齐（cross-platform + i18n overseas）：README.en.md、`--lang en|zh` 主入口、i18n.py、CFI 三平台 workflow 全绿。
- 不改变业务算法/中文模板；平台专用调整只改发布副本。

## 2026-10-18 v0.18.3（修复 /live 页注入风险 + 三平台重新对齐）

- 修复 `/live` 实时页潜在 XSS：表格字段（网盘名/当前步骤/状态徽章/更新时间）统一 HTML 转义；内嵌曲线 JSON 改为 HTML-safe 转义（`&`→`\u0026`、`<`→`\u003c`、`>`→`\u003e`、U+2028/2029）；图表卡片由 `innerHTML` 改为 DOM + `textContent` 渲染，避免安全字段二次解析注入。
- 本次为 SkillHub 安全扫描（sanbu suspicious）定位的真实修复；升级后 GitHub / SkillHub / ClawHub 三平台以 0.18.3 为 latest 重新对齐。
- `scripts/self_test.py` 自检在 482 项基础上新增 `/live` 转义断言；全部 PASS。

## 2026-10-18 v0.18.2（真机验证权限清单 + 依赖声明 + 三平台版本对齐）

- 新增 `references/41-真机验证权限清单.md`：按盘列出最小授权方式（扫码/浏览器登录项、AList 挂载地址、OAuth/WebDAV、分享链接），未授权盘统一标记「待用户提供」，不虚报真机数；本轮授权状态待用户提供。
- 新增 `NOTICE.md`：明确 aria2 / yt-dlp / rclone / AList / BaiduPCS-Go / quark-cli / WebDAV 等为第三方依赖，随包 `tools/pylib/yt_dlp/` 为 yt-dlp 项目源码，发布包不含真实 token/账号。
- `README.md` / `SKILL.md` / `manifest.json` / `references/40-网盘支持矩阵.md` / `references/25-真机验证清单.md` 同步补充权限清单入口与版本号 0.18.2。
- `scripts/self_test.py` 自检由 474 项增至 482 项：新增 NOTICE.md / references/41 权限清单 / 版本一致性断言；全部 PASS。

## 2026-10-18 v0.18.1（支持边界文档补充，功能零改动）

- 新增 `references/40-网盘支持矩阵.md`：以 `scripts/pancli/engine.py` 的 `DRIVES` 注册表为准，列出全部已登记网盘、主域名、默认引擎、可用零客户端桥与参考文档；标注四类非百度路由（官方网页会话桥/浏览器直链桥/AList/OAuth-WebDAV）。
- 明确列出新浪微盘、华为网盘、360 云盘、永硕 E 盘、纳米盘等未接入盘名：一律“不支持/需接入”，不得当成 HTTP 直链抓取分享页。
- README / SKILL.md 增加“支持边界”入口；`scripts/self_test.py` 474 项自检保持全绿。

## 2026-10-16 v0.18.0（100% 优化：10 秒刷新 + 下载请求提速）

- Web UI 任务中心和 `/live` 实时页刷新统一改为每 10 秒；粘贴/输入投递延迟从 50ms/350ms 降到 0ms/120ms，提交后立刻回执「已受理」与本地服务耗时。
- `/api/download` 响应提速：整批只读一次 `load_config()`（原来逐条读盘约 0.4ms/条）；单链接保持同步派发（PID/插件语义不变）；多链接改为后台线程派发，HTTP 响应时间不再随链接数线性增长，实测 50 条链接从 2700ms 降到 10ms。
- 新增响应字段 `accepted`、`queued`、`async`、`accepted_at`、`dispatch_ms`、`live_url`；单链接同时返回顶层 `pid`，Chrome 插件 `data.pid` 语义不变。
- 接收链接阶段仍是纯本机毫秒级检查（登录门禁/路由识别），不发起任何网络请求。
- 自检由 462 项增至 474 项；`manifest.json` / `SKILL.md` 版本同步 `0.18.0`。

## 2026-10-16 v0.17.0（外部引擎日志接入 Web UI）

- 新增 `pan live attach`：把外部 BaiduPCS-Go 进度日志接入 Web UI，显示分享总进度、当前批次百分比、活动分片、速度、ETA、当前文件和绝对下载位置。
- `/live` 增加“总进度”列；外部日志的 0 B/s 如实显示为百度端限速或等待分片，保留断点，不误报速度。
- 修复 `ensure_web_ui()` 复用已有服务时未按预期打开 `/live` 的回归；未注入监控样本时不再用接入前字节计算虚高速度。
- 自检新增外部日志解析、真实 HTTP `/live` 渲染和 `live attach --once` 端到端覆盖，断言由 451 项增至 462 项。

## 2026-10-15 v0.16.0（单实例锁 · 续传安全 · 限速诚实报告）

- 新增 `scripts/pancli/tasklock.py`：按 `(drive, source, target)` 生成单实例锁；同来源重复启动会被拒绝并返回退出码 `9`，陈旧锁可自动接管/清理。
- `scripts/pancli/engine.py`：百度 BaiduPCS 下载步骤和官方网页会话路径自动挂锁；自动移除 `--ow`、补 `--retry 5`；支持 `pan guard` 子命令。
- 新增 `scripts/pancli/guard.py`：双 fork + `setsid` 后台守护、吞吐采样、ETA 预估、统一错误分类与处置建议。
- `scripts/pancli/baidu_login.py`：二维码路径加入时间戳和随机后缀，避免复用同一文件被缓存后扫到旧码。
- 新增 `references/39-单实例与续传安全.md`：记录已验证的扫码→转存→断点续传成功流程，以及多进程抢文件、`--ow` 重下、`nohup` 被回收、限速误判等失败教训。
- 自检覆盖单实例互斥、陈旧锁、`--ow` 剥离、守护进程存活、错误分类和 ETA；版本 `0.16.0`。

## 2026-10-15 v0.15.0（百度零客户端网页会话桥）

- 百度分享默认路由从 `baidupcs` 改为 `baiduweb`；匿名网页会话不阻塞投递，链接内 `pwd` 自动识别。
- 新增 `pancli/webengine.py` 通用网页桥：分享页探测、递归目录、同名目录结构、逐文件任务、`.part` 断点续传、失败重试和实时进度。
- 新增 `pancli/baidu_web.py` 官方网页驱动：只使用官方分享页/接口，进程内 CookieJar，不持久化、不读取浏览器 Cookie、不输出会话字段。
- Web UI 改为投递后自动开始，2 秒任务刷新；任务中心展示文件名、总进度、当前文件、完成/失败数、速度、剩余时间、状态和本地路径。
- 修复 Web 子模块后台启动/重试入口指向 `pancli/web.py` 的问题，并保留提取码在任务控制中的可重试路径。
- 修复百度官方 `/api/sharedownload` 请求体编码：改回官方前端使用的表单编码，避免 JSON 请求导致直链失败。
- 报告与实时状态中的分享提取码统一脱敏为 `pwd=***`。
- 官方接口返回验证码、风控、会员、付费或违规限制时逐项安全失败；不绕过任何平台限制。

## Unreleased（本地迭代 R22：路由与诊断缓存）

- `route_link_payload()` 增加同参数 2 秒短缓存；配置内容或百度本机登录态变化自动失效。
- CLI 新增 `pan route --no-cache`，登录/配置变化后可强制复核。
- `/api/diagnostics` 增加 30 秒缓存；`?refresh=1` 强制刷新，响应带 `cache_hit/cache_ttl_seconds/checked_at`。
- 省 token 方案文档同步更新。
## Unreleased（本地迭代 R21：省 token 路由）

- `pan route --brief` 新增最小 JSON：Agent 只看 `next_action/login_url/missing/target` 等决策字段。
- MCP `pan_route` 默认使用 brief，减少对话 token。
- `load_config()` 增加 mtime/size/inode 缓存；保存后自动刷新缓存。
- 新增开工提示词和省 token 方案文档。
## Unreleased（本地迭代 R20：一次路由提速）

- 新增 `pan route <链接> --json`：识别、登录门禁、依赖、目标目录、提取码、零客户端桥和下一步动作一次返回。
- 新增 `/api/route`，测试页改用一次请求完成预检，不再分多次接口查询。
- MCP 新增 `pan_route`，Agent 收到链接后只调一次即可决定登录/配置/下载。
- 本地路由耗时输出 `latency_ms`；示例百度链接内部路由约 `8ms`，CLI 冷启动约 `0.39s`。
## Unreleased（本地迭代 R19：零客户端引擎桥）

- 新增 `pan engines` / `/api/engines` / `/engines`：统一展示浏览器直链捕获桥、AList 驱动桥、OAuth/WebDAV 桥和本地兼容回退。
- 浏览器插件增加 `chrome.downloads.onCreated` 零客户端捕获模式：用户在官方网页主动触发下载时捕获直链交给网盘通；不读取登录态。
- 插件失败时自动打开 `/login?drive=<网盘>`，并在弹窗提供捕获开关。
- MCP 新增 `pan_auth` 和 `pan_engines`。
- 明确边界：零客户端指不装各家桌面客户端，不是绕过登录、签名、风控、限速或 DRM；官方不给直链时必须失败。
## Unreleased（本地迭代 R18：秒级登录门禁）

- 新增 `pan auth <链接> --json`：收到链接后立即做纯本地登录/授权检查，不联网、不读凭据明文。
- `pan detect` 返回 `auth`，Agent 不用等下载失败才知道需要登录。
- `pan test` 增加登录/授权检查；`/api/test` 返回 `login_required` 和 `/login?drive=<网盘>`。
- Web UI `/api/download` 投递前先做登录门禁；需要登录时立即返回并自动打开统一登录页。
- `/login` 支持 `?drive=<网盘>` 定位提示；规则文档与自检同步。
## Unreleased（本地迭代 R17：登录 / WebUI 回归整改）

- 复盘百度网盘案例：未登录、网页端大文件客户端限制、临时脚本绕开 Web UI 是本次体验失控的根因。
- 新增统一规则 `references/35-登录与WebUI统一流程.md`：所有网盘先走官方扫码/OAuth/浏览器授权，凭据禁止进聊天。
- 新增 WebUI 规范 `references/36-WebUI实时进度规范.md`：任务状态、进度、速度、目标路径必须进入 `/` 和 `/live`，Agent 不做聊天轮询。
- `web.py` 新增 `/login` 统一登录/授权入口，并在导航中接入任务中心。
- `SKILL.md`、`README.md` 补充 `/login` 和统一规则；离线自检覆盖规则文档与关键路由。
## 2026-10-14 v0.14.2（安全扫描整改）

- `setup` 不再代跑包管理器；只输出安装建议，由用户复核后手动执行。
- 更新 `--apply` 帮助文本，避免误认为会自动安装依赖。
- 不改变下载调度、凭据与合规边界。

## 2026-10-14 v0.14.1（三平台发布简介与脱敏修订）

- 统一更新发布简介：明确 Agent / MCP / CLI、Web UI、浏览器插件三类入口。
- 明确 macOS / Windows / Linux 支持；`local` 为默认模式，NAS / 服务器 Docker 仅是可选部署。
- 发布摘要去除本机绝对路径，SHA256SUMS 使用相对文件名。
- 保持纯调度层：不新增解析分享页、破解或绕过登录 / 付费 / 限速 / DRM 能力。

## 2026-10-14 v0.14.0（通用下载调度层定位）

- 首屏与 README 从 NAS 优先改为“通用下载调度层”，三类入口统一为 Agent/MCP/CLI、Web UI、浏览器插件。
- 新增 macOS / Windows / Linux 用法：brew/winget/apt/dnf、默认路径和系统凭据库；Web UI 使用占位地址。
- 浏览器插件更名“通用 pan 下载插件”，支持本机/NAS/服务器地址，明确不读取网页登录态。
- MCP 文档补充 `pan_get` / `pan_task` / `pan_get_plan`、通用 MCP 客户端配置和无服务模式。
- setup/doctor 以 local 为默认；NAS/server Docker 只是可选部署模式；本机模式不再检查远程依赖。
- 新增自检：三入口/三系统/占位符、插件一致性、local/nas_docker/server_docker 配置生成；`SELF_TEST_OK checks=375`。

## 2026-10-14 结构优化·之二（拆分 Web 子模块）

- 抽出 `scripts/pancli/web.py`（883 行）：Web/Agent 一站式页面、PWA、实时速度、serve HTTP 服务全部外移。
- `scripts/pancli/engine.py` 从 5985 行降到 5119 行；`pan.py serve`、`pan task` 等通过懒加载调用 web 子模块，行为不变。
- `self_test.py` 离线自检继续通过：`SELF_TEST_OK checks=358`。

## 2026-10-14 结构优化（方案 A：保留全部功能，拆分入口）

- `scripts/pan.py` 改为 CLI 轻入口（约 30 行），实现迁移到 `scripts/pancli/engine.py`。
- 修正 `engine.py` 中的 `SKILL_DIR` 与 `pan_mcp.py` 相对路径，使其在 `scripts/pancli/` 下仍指向技能根目录。
- `self_test.py` 改为直接加载 `pancli/engine.py`，离线自检 358 项通过（SELF_TEST_OK checks=358）。
- `config.example.json` 恢复 `http.live_status: true` 默认值，与新版实时监控自检一致。
- 备份：先前的完整回滚备份与本次修改前备份见 `work/skill-backup-cdd-full-20261013/`。

## 2026-10-13 回滚到旧版（搜索/爬虫/movie/docker）

- 按用户指令回滚到 9:16 功能版：恢复 `pan search`（公开搜索一键下载）、`pan crawl`（网页爬虫）、`pan movie sources/get/x`、`pan docker`（Docker/NAS 一键安装）。
- 恢复 `scripts/pan.py` 旧完整入口、`scripts/self_test.py`、`scripts/pan_mcp.py`、`scripts/pan_web.*`、`scripts/clipboard_monitor.py`、`scripts/feishu_bot.py`。
- 恢复 `references/`（33 篇详细文档）与 `extensions/chrome`。
- 恢复旧 Docker 模板：python:3.11-slim + curl + aria2 + yt-dlp + ffmpeg + ssh，暴露 17890。
- 当前版合规重构已备份到 `work/restore-backup-refactor-20261013/`。

---

## v0.8.0（合规重构）

- **改为纯下载调度层**：不再解析网盘分享页、不提取直链、不猜签名、不抓 Cookie/Token、不做 UA 伪装/IP 轮换、不绕过登录/VIP/限速/验证码/风控/DRM。
- **不再搜索/索引/推荐资源**：输入只来自用户明确提供的 URL/文件 ID/分享链接；删除旧 `search`/`crawl`/`movie`/`x` 逻辑和网页爬虫。
- 新增引擎适配器 `scripts/engines/`：curl / wget / aria2 / rclone / AList（透传用户已配置的命令）。
- 新增命令：`get`、`engines`、`doctor`，全部支持 `--json`。
- `credentials.py`：凭据只从 macOS Keychain / Windows Credential Manager / Linux secret-tool 读取；Cookie 经 0600 临时文件传给工具，用完即删。
- 引擎未安装时只提示安装，不内置替代破解方案；不承诺不限速。
- 测试：`tests/test_pan.py` 只使用公开直链与本机引擎检测。
- 旧实现（含 references / 网盘解析逻辑）已迁出到 `work/legacy-*` 存档，不进本 Skill 目录。

## Unreleased（本地迭代 R16）

- 新增通用 HTTP/HTTPS 直链下载模块 `scripts/http_downloader/`：
  - 新命令 `pan direct <直链>`：只接受 http/https 直链，支持 Range 并发分片、断点续传、重试、超时、SHA-256/MD5 校验、`--to`、`--json`。
  - `pan get --generic-direct` 与 `pan movie get --generic-direct`：把 http/https 直链切换到通用模块，非交互必须 `--confirm-own-use`。
  - 合规边界：不解析网盘分享链接、不绕过登录/验证码/防盗链/会员、不搜索盗版资源；下载前强制确认用户对该文件拥有授权或公开许可。
  - 本机与 NAS 容器均已部署；容器内 `python3 -m http_downloader.self_test` 通过（单流/并发分片/拒绝非 http）。

## Unreleased（本地迭代 R15）

- v0.13 新增 `pan crawl` 网络爬虫能力：
  - 新增 `pan crawl <网页URL>`：抓取网页/目录页里可直接下载的媒体、文件、magnet、torrent 候选，支持 `--kind movie|video|music|file`、`--limit`、`--timeout`、`--depth`（同域分页跟进最多 5 个子页）、`--json`。
  - 一键下载：`pan crawl "<URL>" --pick 1 [--kind movie] [--remote nas] [--to 目录] [--dry-run]`，复用现有下载管线；网页候选默认需 `--assume-own` 确认有权访问，`--dry-run` 预览不受限。
  - 自动识别并优先排序 torrent/video/movie 候选；支持相对链接归一化和磁力/BT 种子识别。
  - 搜索与爬虫共用同一套“选中即下载”逻辑（`dispatch_chosen_download`），行为保持一致。
  - 离线自测增至 358 项，覆盖单页提取、相对链接、磁力/BT、分类过滤、授权确认与 dry-run。

## Unreleased（本地迭代 R14）

- v0.12 解决搜索与 Docker 验证遗留风险：
  - 新增 `pan search "关键词" --check`：离线/真机逐个测试搜索源连通性（archive.org / DuckDuckGo / yt-dlp），JSON 给 Agent 解析；沙箱外网受限时本机用它确认。
  - 网页搜索候选增加授权确认：`--pick` 网页候选默认禁止直接下载，须加 `--assume-own` 或 `--force`（`--dry-run` 预览不受限），避免误下未授权内容。
  - 新增 `pan docker check`：检测本机 docker/podman 与生成文件完整性；无 Docker 的主机也能静态校验并得到明确的 NAS 部署指引。
  - 离线自测增至 340 项，覆盖搜索连通性检测、网页候选授权确认与 docker check。

## Unreleased（本地迭代 R13）

- v0.11 一键搜索下载 + Docker/NAS 部署：
  - 新增 `pan search "关键词"`：聚合搜索公开/官方资源（archive.org 公版电影音频、DuckDuckGo 网页候选、yt-dlp 公开视频搜索），支持 `--kind movie|video|music|file`、`--limit`、`--json`、`--list-providers`。
  - 一键下载：`pan search "关键词" --pick 1` 选中候选直接走现有下载管线；支持 `--remote nas`、`--to`、`--dry-run`、`--split`、`--live`。
  - 搜索对齐合规边界：只列公开/公版/你有权下载的内容，不破解会员、验证码、限速或风控；网页搜索结果需自行确认授权。
  - 新增 `pan docker` 子命令：在技能根 `docker/`（或自定义 `--out`）生成 `Dockerfile`、`docker-compose.yml`、`install.sh`、`README-Docker.md`；镜像内置 python+curl+aria2+yt-dlp+ffmpeg+ssh，容器里 serve 默认监听 `0.0.0.0:17890`。
  - Docker 部署到 NAS 场景：群晖 Container Manager / 威联通、飞牛、TrueNAS 等装好 Docker 后执行 `bash install.sh`，`state/` 与 `download/` 用卷挂载持久化；容器不包含本机 config/cookie/token。
  - 离线自测增至 322 项，覆盖 search 候选解析与 Docker 文件生成。

## Unreleased（本地迭代 R12）

- v0.10 免费电影 / NAS 下载 / X(推特) 视频：
  - 新增 `pan movie sources`：列出公开/公版/官方免费电影入口（Internet Archive、Public Domain Torrents、archive.org 磁力、官方公开资源）；只列你有权下载的内容，不搬运盗版源，不破解会员/验证码/风控。
  - 新增 `pan movie get <url> [--candidates url2,url3]`：多候选直链真实测速，自动选最快源再下载；支持 `--remote <nas>`、`--to`、`--tier`、`--dry-run`、`--split` 分片并发。
  - 新增 `pan movie x <url>`：下载 X（原推特）推文视频，识别 `x.com/i/status`、`twitter.com/...`、`mobile.twitter.com/...`，走内置 yt-dlp 多分段下载；登录/私密推文请配置 `ytdlp.cookies_from_browser`。
  - `detect_drive` 已将 twitter/x.com 归入 stream（yt-dlp），无需额外客户端。
  - NAS 场景：`movie get`/`movie x` 都支持 `--remote nas`，先测速选最快，再交给远程设备下载。
  - 离线自测新增 movie sources / X 识别 / movie get 最快候选 / movie x dry-run 用例。

## Unreleased（本地迭代 R11）

- v0.9 统一入口 + 最快下载体验：
  - 新增网页视频/HLS/流媒体识别（YouTube、bilibili、vimeo、twitch 等），自动走 yt-dlp 多分段下载。
  - 新增内置 `pan probe` 命令：对多个候选直链逐源真实测速（默认各采样前 200KB），按速度排序并推荐最快链接。
  - 新增技能自带便携引擎：`tools/pylib` 预装 yt-dlp（已在本机装载）；`find_engine_binary` 自动在 `tools/bin、tools/pylib/bin、tools/aria2/bin` 查找，无需用户逐个装客户端。
  - 配置新增 `ytdlp.format / concurrent_fragments / cookies_from_browser`（对流媒体多站可用性）与 `engines.yt-dlp`。
  - 新增 `rank_fastest_urls` 测速函数与 `DRIVES.stream`。
  - 离线自测增至 300 项。

## Unreleased（本地迭代 R10）

- 多协议下载扩展（HTTP/FTP/BT/磁力）：
  - 新增 `ftp://`、`ftps://` 直链识别，自动走 curl/aria2 断点续传。
  - 新增 `magnet:` 磁力链接与 `.torrent` 种子识别，自动路由到 aria2（DHT → P2P + tracker）。
  - aria2 分支新增多连接并发（HTTP/FTP 用 `-x/-s`，免费默认 4、会员 16，可在 `bt.connections_free/vip` 调整）与磁力/BT 专属参数（`--enable-dht`、`--bt-save-metadata`、`--bt-max-peers`、`--seed-time`、`--bt-tracker`）。
  - 新增配置段 `bt`（trackers / seed_time / enable_dht / dht_listen_port / bt_max_peers / connections_free / connections_vip），`config.example.json` 同步。
  - 新增 `is_magnet_url`、`is_torrent_path`、`is_ftp_url` 识别助手。
  - 离线自测新增 ftp/ftps/磁力/.torrent 识别与计划拼接用例。

## Unreleased（本地迭代 R8）

- 发布后小白上手：
  - 新增 `references/29-小白快速上手指南.md`：面向完全没碰过代码的用户，步骤式说明装 Python、拿工具、一键配置、网页下载、找文件、常见问题与安全提醒。
  - 新增 `scripts/pan_web.ps1`：Windows 一键网页下载助手（启动 serve + 剪贴板监听 + 打开 Web UI），与 `pan_web.sh` 对齐。
  - 离线自测从 272 增至 274 项，覆盖 Windows 一键脚本与小白指南存在性。

## Unreleased（本地迭代 R7）

- 第 3 步·飞书机器人（桥接层）：
  - `notify` 新增 `feishu` 通道：群机器人 Webhook 文本消息 `{"msg_type":"text","content":{"text":...}}`，支持 `pan notify --channel feishu`；默认配置与 `config.example.json` 同步加入 `notify.feishu_secret`。
  - 新增 `scripts/feishu_bot.py`：飞书事件回调桥（`url_verification` challenge 应答、自动抽取 http(s) 链接与“提取码/密码/pwd”后的 4-6 位码、POST 到 `serve` 的 `/api/download`），纯标准库、支持 `--check` 离线自检、`--host/--port/--target`。
  - 新增 `references/28-飞书机器人.md`：说明群机器人 Webhook 只能发通知、自建应用事件订阅才能收消息；给出事件回调地址配置与 SSH 反向隧道/VPS 公网方案；秘钥走系统凭据库，不写 config/Git。
  - 离线自测从 258 增至 272 项，覆盖飞书 notify payload、桥接脚本存在性与自检、回调消息转发。

## Unreleased（本地迭代 R6）

- 第 2 步：远程 NAS 常驻 + 网页控制。
  - `remote deploy <name> --web-port <端口> [--web-host <0.0.0.0|127.0.0.1>] [--web-reports-dir <目录>]`：部署后通过 SSH nohup 在远程设备后台启动 `scripts/pan.py serve`，Web 页面通过 `--reports-dir` 指向远程 root，自动扫描任务中心/实时速度/历史报告。
  - 新增 `remote web <name>` 帮助命令：打印远程 Web 地址、SSH 反向隧道命令与本地访问地址（不实际连接）。
  - 部署计划/JSON 输出新增 `web_port/web_host/web_url/web_guide` 字段，供 Agent 与 Web 控制使用。
  - `serve` 新增本机任务投递回跳字段（`live_url/home_url`）与远程报告目录兼容；离线自测从 244 增至 256 项，覆盖远程 Web 命令拼装与 0.0.0.0 直连 URL。
  - 远程 Web 安全提示：默认监听 127.0.0.1，需局域网直连才用 0.0.0.0 并确认防火墙；推荐 SSH 反向隧道访问，不直接暴露公网。

## Unreleased（本地迭代 R2）

- 新增一键安装+配置向导 `pan setup`：创建/刷新 config，检测系统包管理器（brew/apt/dnf/winget），列出缺失依赖的安装命令；`--apply` 实际执行；`--root` 可同时设定下载目录；`--json` 供 agent 使用。
- 新增任务控制（真实落地 v2）：`get` 实际下载前登记 `任务控制.json`（目标/链接/引擎/档次/PID/状态/当前步骤），提供 `pan task list|show|pause|resume|delete|retry <id>` 子命令。
- 暂停/继续实现为「进程级真实暂停」，对当前引擎子进程发送 SIGSTOP/SIGCONT；取消发送 SIGTERM 后兜底 SIGKILL，不依赖轮询猜状态。
- `serve` 首页升级到任务中心 v2：表格增加「操作」列，运行中可暂停/取消，暂停中可继续/删除，已结束可重试/删除；新增 `GET /api/task/action?task=<id>&action=pause|resume|delete|retry` 接口。
- `serve_unified_tasks` / `serve_task_controls` 递归收集 任务控制.json（覆盖任务目录、live_dir、report_dir），暂停/取消状态在任务中心正确显示。
- 重试基于任务控制记录自动重新拉起 `get` 子进程（不保存提取码明文；有提取码的任务会提示补充 `--pwd`）。
- 离线自测从 161 增至 170 项，覆盖任务登记、状态机、递归合并与控制动作。
- 新增智能默认 + 自动重试：`smart.auto_classify` 与 `get --classify` 按扩展名自动归档（影视/音乐/文档/图片/压缩包/其他）；默认重试 3 次 + 断点续传已有能力对齐说明。
- 新增 Web UI PWA：`/manifest.webmanifest`、`/sw.js`、动态 PNG 图标路由，网页可安装为独立窗口。
- 离线自测增至 213 项，覆盖内容分类、分类目录、PWA 清单/图标/页面注入。

- Web UI 重新美化：任务中心首页与实时速度页从朴素表格改为深色卡片式界面（运行中/已完成/失败/全部统计卡、状态徽章、速度高亮、圆角按钮、移动端两列自适应）。
- 修复 Web UI 打不开：任务中心首页模板中 `width:100%` 里的 `%` 被 Python `%` 格式化误当占位符，导致首页 `ValueError: unsupported format character '}'` 返回空响应；已改为 `width:100%%` 并把首页渲染抽成 `serve_home_html(tasks)`，离线自测新增回归项，checks 从 191 增至 199。

- 新增浏览器扩展 + 剪贴板监听（`extensions/chrome/`，Manifest V3）：右键「发送 网盘链接 到 pan 下载」、复制/选区自动识别链接、popup 手动提交，接入 `POST /api/download` 后台启动下载；扩展仅允许访问 `http://127.0.0.1:17890/*`，不读取网盘页面登录态。
- `serve` 新增 `POST /api/download`（url/pwd/to/engine/tier/path）供扩展与 Agent 直接投递下载任务；URL 为空或启动失败返回人话错误。
- 离线自测增至 191 项：覆盖 `_spawn_download_task` 参数拼装/空链接/启动异常、Chrome 扩展清单 manifest_version=3 且 host_permissions 仅本机端口、扩展文件完整性与 JS 语法检查（node --check，无 node 退化为括号平衡校验）。

- 新增任务中心 Web UI v1：`serve` 首页从只读状态页升级为「跨网盘任务中心」，实时任务与历史报告统一成一张表（任务ID/网盘/当前步骤/实时与平均速度/状态/更新时间）；新增 `/api/tasks` 与 `?state=` 筛选接口。
- 新增实时速度监控：`get --live`（或配置 `http.live_status=true`）在下载期间周期性采样目标目录字节增量，写入 `下载速度.live.json`（含实时/平均速度 KB/s、已下载字节、当前步骤、状态）；`serve` 页面新增 `/live` 自动刷新视图与 `/api/live` 接口。
- 新增 R9：常见错误人话提示。`get` 失败时终端和 `下载报告.json` 的 `steps[].hint` 输出中文动作建议（超时/依赖缺失/连接失败/非 2xx/WebDAV/百度/夸克），无法判断时保留原文退出码不猜测。
- 新增下载统计与可观测性：实际下载完成后在目标目录生成 `下载报告.json`（起始/结束时间、耗时、逐步骤退出码/耗时、缺失与警告）。
- 新增 `get --events`：实际下载过程输出逐步 JSON 事件（NDJSON），便于 Agent 与上层可视化消费，凭据仍全部打码。
- 新增配置项 `http.report_dir` 与 `http.on_complete_hook`：支持自定义报告目录和在下载成功后执行本地完成钩子（如 rsync 到远端）。
- 新增 R6-R8：
  - `init --wizard` 环境检测向导、`doctor` JSON/文本给出安装建议命令；
  - `mcp guide` 输出 Codex `[mcp_servers]` 注册片段；新增 OpenAPI 稳定接口文档 `references/26-OpenAPI.md`；
  - `notify` 扩展 telegram/discord；新增 `serve` 只读本地状态页（127.0.0.1:17890，/、/api/reports、/api/status）。
- 新增 R5：`notify send`（Bark/企业微信，webhook 存系统凭据库，默认 dry-run）+ 真机验证脚本 `scripts/verify_real_env.py` 与 `references/25-真机验证清单.md`（覆盖 Range 分片、rclone 转存、MCP 注册、通知发送）。
- 新增 R4：`transfer` / `sync` 子命令（rclone 跨盘转存/增量同步，默认 dry-run）、公司目录红线默认拒绝、`sync` 需显式 `--delete + --apply`；新增 `references/24-跨盘转存与同步.md`。
- 新增 R3：CLI JSON 覆盖补齐（`detect/dirs --json`）+ 最小 stdio MCP 服务器 `scripts/pan_mcp.py`（纯 Python），暴露 `pan_doctor/pan_detect/pan_dirs/pan_get_plan`；新增 `references/23-MCP与Agent接口.md`。注册到 Codex 的 `[mcp_servers]` 需在本机配置，本 skill 原版不含平台配置。
- 新增 R2：http 直链单文件 Range 分片（`get --split N` / `http.range_split`），服务端不支持时自动回退整文件；分片结果进 `下载报告.json`。
- 保持 v0.6.0 的既有铁律不变：不绕过限速/风控，凭据不落盘不输出。

## Unreleased（本地迭代 R3）

- 新增「测试连接」入口 `pan test <url>`：只读验证一条链接能否下载（识别网盘、依赖/配置是否齐备、目标目录是否可写、是否提供提取码），不下载不写盘；`--json` 供 Agent 使用。
- `pan login <盘名> --open`：用默认程序打开对应网盘的授权教程，降低找登录步骤的成本（仍不绕过平台验证码/风控）。
- Web UI 新增独立「测试连接」页 `/test`：粘贴链接/提取码即可调用 `/api/test` 显示人话检查结果；任务中心导航与 PWA 缓存已包含该页。
- `serve` 新增 `GET /api/test?url=...`，Web UI/扩展可直接使用测试连接能力。
- MCP 新增 `pan_test` 工具：返回一条链接的测试连接 JSON。
- 离线自测新增第 30 项，checks 从 221 增至 227。

## Unreleased（本地迭代 R4）

- 新增下载后处理链样板 `scripts/hooks/post_media.sh`：下载完成自动解压 ZIP/TGZ，预留 Jellyfin/Emby/Plex 媒体库扫描命令位；默认 AUTO=0 只预览，改 1 生效。
- 浏览器扩展弹窗新增「测试连接」区块：粘贴链接（可选提取码）直接调用 `/api/test` 显示人话检查结果，不真正下载。
- 提取码智能提示：百度/夸克/蓝奏/123/微云等常见分享盘未传 `--pwd` 时提前 output 提示，避免下载失败后无头绪。
- 新增定时/低峰下载骨架：`get --at HH:MM` 或 `http.schedule_at`，到点再开始；dry-run/JSON 不阻塞。
- 离线自测新增第 32 项，checks 从 232 增至 238。

## Unreleased（本地迭代 R5：网页/Agent 一站式）

- 首页新增「粘贴链接开始下载」表单：提交后自动跳转 `/live` 看实时进度；修复首页 `width:100%%` 转义回归。
- `POST /api/download` 新增返回 `live_url` / `home_url`，让 Agent/扩展直接把实时进度链接给用户。
- 新增全局剪贴板监听 `scripts/clipboard_monitor.py`（macOS `pbpaste` / Linux `xclip/xsel` / Windows PowerShell）：剪贴板出现网盘链接自动投递本机 serve，去重 10 分钟，`--once` 支持单检。
- 新增一键脚本 `scripts/pan_web.sh`：启动 serve + 剪贴板监听 + 自动打开 Web UI。
- 离线自测新增第 33 项，checks 从 238 增至 244。

# Changelog

## 0.6.0 - 2026-09-27

- 新增 `README.md` 概述，明确本 Skill 的功能、支持网盘、远程存储、账号等级、凭据保护和合规边界。
- 补充市场定位：与 rclone、AList、单网盘工具及 Skill 市场的关系和差异化。
- 完善发布元数据：新增 `manifest.json`、`LICENSE.md`，同步 `agents/openai.yaml` 展示说明。
- 保持核心下载逻辑不变，继续通过离线自测和发布合规检查。

## 0.5.0 - 2026-09-27

- 增加 Windows 启动包装器、系统凭据库后端和远程 NAS/私人存储能力。
- 扩展网盘覆盖和本地/远程引擎适配。

## 0.1.0 - 2026-09-24

- 首个可用版本：统一识别、目录规划、下载引擎适配、免费账号策略和凭据安全边界。
