# Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

项目采用 [语义化版本](https://semver.org/lang/zh-CN/)。

> **版本间导航**：远端目前只有 `v0.2.0` 一个 tag，`0.1.0` 没有对应 tag。compare 链接需要「上一版本」与「当前版本」两个真实 tag 才能构成，因此本文件**不提供 compare 链接**——不编造起点。补打 `v0.1.0` 需要能定位到当时发布的 commit，属独立决策。

## [0.2.0] - 2026-10-11

> **一句话概括**：这版给 skill 划清了**能力边界**——只做文件下载，不做搜索、不拉 magnet 内容、不下网盘文件、不破解反爬；同时新增代理兜底链与文件名冲突检查。**需要你注意一处不兼容**：magnet 链接从「用 aria2c 试图下载」改为「报告 `suggested_tool=none`，由你用 BT 客户端处理」；`install_hint` 字段结构也变了（见下方 Changed / Breaking 段）。

### Added

- **SKILL.md**：新增"能力边界"章节（skill 不做什么：搜索资源 / magnet 内容拉取 / 网盘下载 / JS 反爬破解）。
- **SKILL.md**：新增 Phase 2.5 代理兜底章节（直连失败 → 按链顺序重试）。
- **SKILL.md**：新增 Phase 3.0 文件名冲突检查（追加序号，不覆盖）。
- **SKILL.md**：新增"网盘链接处理"章节（kind=cloud_drive 识别但不下载）。
- **SKILL.md**：新增"Magnet 链接处理"章节（kind=magnet 报告客户端处理）。
- **SKILL.md**：新增"平台视频失败应对"章节（按症状查表）。
- **scripts/check_tools.py**：工具可用性检查（curl / yt-dlp / aria2c）。stdlib only，零网络。
- **scripts/proxy_chain.py**：代理链解析（env → ~/.downrc → builtin）。stdlib only，零网络。
- **references/commands-windows.md**：PowerShell 命令模板（curl.exe / & 调用 / 反引号行续符）。
- **docs/PLAN-v0.2.md**：v0.2 开发计划（11 条决策 + 8 个 Phase + 6 层稳定性保障）。
- **detect.py**：新增 `cloud_drive` kind（10 个网盘 host：百度/夸克/阿里/115/天翼/微云/文库）。
- **detect.py**：JSON 契约新增 `user_action` / `reason` 字段（skill 不处理时给用户的指引）。
- **detect.py**：`dest_name` 加完整路径净化（防路径穿越 + shell 注入 + 控制字符 + 超长截断）。
- **AGENTS.md**：加"能力边界"章节（v0.2 新增）+ 4 条元规则（加"辅助脚本也只读"）。

### Changed

- **detect.py**：`.torrent` 从 aria2c 改为 curl（只下种子文件本体，用户手动下内容）。
- **detect.py**：magnet 从 aria2c 改为 none（skill 不处理，报告用户用客户端）。
- **detect.py**：`install_hint` 字段结构统一（`install_by_platform: {windows, linux, macos}`）。
- **detect.py**：删掉 dead imports（mimetypes, shlex）。
- **SKILL.md**：kind 从 5 种扩展到 6 种（加 cloud_drive）；suggested_tool 从 3 种改为 3 种（含 none）。
- **references/tool-matrix.md**：加"代理参数速查"章节；加"何时不询问安装"章节；torrent→curl；magnet→none。
- **references/commands.md**：torrent 从 aria2c 改为 curl；加 magnet/cloud_drive 回复模板；加代理兜底提示。
- **references/detectors.md**：加 CLOUD_DRIVE_SITES 白名单章节；加 sanitize_filename 规则说明；测试覆盖 15→28。
- **README.md**：加 PLAN-v0.2.md 到目录树；修 "clarify 问路径" → "三级优先级"。
- **CHANGELOG.md**：清 [Unreleased] stale 段；修 evals 用例数 11→17；加 docs/USAGE.md 条目。

### Fixed

- README 快速上手与 SKILL.md 语义冲突（"clarify 问保存路径" → "三级优先级"）。
- README "保存路径强制询问"与三级优先级冲突（改为"三级优先级，不询问"）。
- README 目录树与文件系统不一致（缺 USAGE.md / PLAN-v0.2.md）。
- CHANGELOG v0.1.0 段落与 [Unreleased] 状态矛盾（[Unreleased] 清空，保留为 v0.2 占位）。
- `detect.py` dead imports（mimetypes, shlex）——v0.1.0 加入但从未使用。

### Design notes

- **skill 定位清晰**：只做文件下载，不做搜索、不做网盘下载、不拉 magnet 内容、不破解反爬。见 SKILL.md 的"能力边界"章节。
- **代理链解析不发网络**：延续 detect.py 零网络原则。`proxy_chain.py` 只做配置解析，不探测端口。真正验证代理可用性靠重试下载（一个代理可能活着但不通目标站）。
- **`.torrent` 用 curl 而非 aria2c**：只下种子文件本体（几 KB 到几 MB 的小文件），用户手动用 BT 客户端下内容。依赖简化，用户明确"只给我链接就好"。
- **magnet 报告 none 而非 aria2c**：magnet 是元数据 URI，需要 BT 客户端解析。skill 定位是文件下载，不是 BT 内容下载。
- **cloud_drive 报告 none 而非尝试下载**：每个网盘 API 都不同，稳定性不可能保证；每个网盘都要 cookie/登录态，违反"不静默认证"红线。
- **dest_name 净化**：防路径穿越（`../../passwd` → `download`）+ 防 shell 注入（`foo$bar` → `foo_bar`）+ 控制字符 strip + 200 字符截断。10 个边界用例全过。
- **Windows 只补文档**：`references/commands-windows.md` 只写命令模板，代码不动（POSIX + Windows 共享 detect.py/check_tools.py/proxy_chain.py）。
- **~/.downrc 用 JSON 而非 TOML**：stdlib `json` 全版本支持（Python 3.9+）；TOML 支持留待 v0.3（3.11+ 用 tomllib）。
- **内置默认代理链 3 个**：7897（Hermes 验证）→ 7890（Clash 默认）→ 192.168.31.135:7890（LAN 兜底）。

### Known limitations

- 反爬站点（Nitroflare / Alfafile 等）无法通过 CLI 绕过——这是**特性**不是 bug，skill 会如实报告。
- 无 headless 浏览器驱动——不尝试破解 JS 挑战（RandHash2 / Cloudflare turnstile 等）。
- 不下载 magnet 内容 / 网盘内容——需要 BT 客户端 / 账号登录，skill 只报告。

### Migration notes（from v0.1.0）

- **`.torrent` 处理**：v0.1.0 用 aria2c 下载 .torrent 文件（并尝试拉 BT 内容）。v0.2.0 改用 curl 只下种子文件本体，用户手动用 BT 客户端下内容。**如果你的脚本依赖 v0.1.0 的 aria2c 行为，请更新**。
- **magnet 处理**：v0.1.0 用 aria2c 尝试下载 magnet 内容。v0.2.0 报告 `suggested_tool=none`，用户手动用 BT 客户端。**如果你的脚本依赖 v0.1.0 的 aria2c 行为，请更新**。
- **JSON 契约**：新增 `user_action` 和 `reason` 字段（v0.1.0 客户端忽略这两个字段即可）。
- **install_hint 字段**：`install_windows`/`install_linux`/`install_macos` 改为 `install_by_platform: {windows, linux, macos}`。v0.1.0 客户端如果读旧字段会拿到 `None`。

## [0.1.0] - 2026-10-10

> **一句话概括**：首次发布——一个「扔 URL 进来、用最少工具步骤下载到本地」的 skill。**你不需要做任何事**，按 `SKILL.md` 的 Phase 流程使用即可；需要 yt-dlp / curl 等工具时按提示自行安装（skill 不会静默安装）。

### Added

- **SKILL.md**：主入口，含三条元规则（不静默安装 / 最小步骤 / 验证才算完成）、5 Phase 工作流、Pitfalls 清单（来自实战：X `--no-playlist`、`hls-*` vs `http-*`、Nitroflare 硬墙、Windows `python -c` 反引号陷阱等）。
- **scripts/detect.py**：URL 探测器。stdlib only，零网络请求。分类：`platform_video` / `direct_file` / `torrent` / `magnet` / `unknown`。
- **references/tool-matrix.md**：curl / yt-dlp / aria2c 能力边界与选择规则。
- **references/detectors.md**：detect.py 字段契约与判定优先级。
- **references/commands.md**：各 kind 的命令配方（含验证命令）。
- **references/anti-bot.md**：Nitroflare / Alfafile / CGPersia 类站点的识别与降级。
- **AGENTS.md**：本仓库编码约定（3 条元规则 + 提交规约 + 自检命令）。
- **README.md**：快速上手与目录结构。
- **docs/USAGE.md**：用户视角的使用文档（常见问题 + 开发者上手）。
- **evals/test_detect.py**：detect.py 单元测试（stdlib unittest，17 个用例覆盖所有 kind 与边界）。

### Design notes

- **skill 不硬编码任何默认路径**：路径解析走三级优先级——用户显式指定 → 环境偏好（Hermes memory / `~/.downrc` / `DOWN_DEFAULT_DIR`）→ 临时目录兜底。skill 逻辑与用户本机偏好解耦：本机偏好是环境层配置，不是 skill 逻辑。
- **强制询问工具安装**：不静默 `uv tool install` 或 `winget install`。
- **探测器不发网络**：URL 探测阶段无副作用，避免误触反爬与泄露 Referer。
- **工具矩阵优先级**：curl → yt-dlp → aria2c，能用更轻量的解决就不用更重的。

### Known limitations

- 反爬站点（Nitroflare / Alfafile 等）无法通过 CLI 绕过——这是**特性**不是 bug，skill 会如实报告。
- 仅支持 POSIX shell 命令配方（`references/commands.md`）；PowerShell 版本留待 v0.2。
- 无 headless 浏览器驱动——不尝试破解 JS 挑战（RandHash2 / Cloudflare turnstile 等）。
