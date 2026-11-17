---
name: download-youtube-with-firefox
description: "Download YouTube videos up to 4K using yt-dlp, FFmpeg, and Firefox cookies. Bypasses Windows App-Bound encryption and bot checks with JS challenge solving."
user-invocable: true
---

# Download YouTube Videos with Firefox Cookies (YouTube 4K 高画质下载器)

使用 `yt-dlp`、`FFmpeg` 与 Firefox 浏览器免密提取 Cookie，全自动下载最高清晰度（最高可达 4K/8K）及最高音质（Opus）的 YouTube 视频，并自动合并为 MKV/MP4 格式。

本 Skill 专为解决现代 YouTube 严苛风控以及 Windows 操作系统底层浏览器加密难题而设计：
1. **天然绕过 Windows App-Bound Encryption（应用绑定加密）**：无需关闭浏览器，无需安装复杂扩展，直接安全读取 Firefox Cookie，彻底告别 Edge/Chrome 的 DPAPI 解密拦截报错。
2. **集成 JavaScript 挑战求解器（`--js-runtimes node`）**：解决 YouTube 最新播放器 `n challenge` 签名解密失败、格式缺失、强制降至 360p 或报人机验证的问题。
3. **支持 OpenClaw 分布式架构（Gateway 与 Node Host 协同）**：无论 OpenClaw 跑在云端 VPS 还是本地，均能智能将下载任务调度至持有 Firefox 登录态的物理节点。

---

## 快速使用 (Usage)

### 1. 聊天调用 (Chat Commands)
在与 OpenClaw 聊天时，直接输入命令或自然语言链接：
- `/download-youtube-with-firefox https://www.youtube.com/watch?v=XXXXXX`
- `/download-youtube https://www.youtube.com/watch?v=XXXXXX`
- 或直接发送：“帮我把这个视频下载到电脑：https://www.youtube.com/watch?v=XXXXXX”

### 2. 手动命令行直接执行 (Manual CLI Examples)
若要在本地终端手动执行下载，可参考以下标准化命令：

**Windows (PowerShell):**
```powershell
yt-dlp --cookies-from-browser firefox --js-runtimes node -f "bv*+ba/b" --merge-output-format mkv -o "$HOME\Downloads\%(title).200B [%(id)s].%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Linux / macOS (Bash / Zsh):**
```bash
yt-dlp --cookies-from-browser firefox --js-runtimes node -f "bv*+ba/b" --merge-output-format mkv -o "$HOME/Downloads/%(title).200B [%(id)s].%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

---

## 前置环境要求 (Prerequisites)

为了保证视频能正常以最高清晰度合成落地，宿主机（或执行下载任务的 Node 电脑）上需安装以下 4 项依赖：

1. **Firefox 浏览器**：
   - 安装并在 Firefox 中登录一次您的 YouTube 账号。
   - 保持登录状态即可，下载时无需刻意关闭 Firefox。
2. **yt-dlp**：
   - 推荐保持最新版（建议 2024.10 或更新版本）：
     - Windows: `winget install yt-dlp` 或 `yt-dlp --update`
     - macOS: `brew install yt-dlp`
     - Linux: `sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp && sudo chmod a+rx /usr/local/bin/yt-dlp`
3. **FFmpeg**：
   - 用于将分离的最高画质视频流与最高音质音频流无损合成为单一文件：
     - Windows: `winget install Gyan.FFmpeg`
     - macOS: `brew install ffmpeg`
     - Linux: `sudo apt install ffmpeg`
4. **Node.js 或 Deno (JavaScript 运行时)**：
   - 用于运行 YouTube 最新的客户端 JS challenge 求解器：
     - Windows: `winget install OpenJS.NodeJS`
     - macOS: `brew install node`
     - Linux: `sudo apt install nodejs`

---

## 技术原理与避坑指南 (Technical Insights)

### 为什么选择 Firefox，而不是 Edge 或 Chrome？
- **Chromium 的 App-Bound 加密壁垒**：从 Chromium 127 开始，Google Chrome 和 Microsoft Edge 在 Windows 上启用了系统特权服务级的应用绑定加密（App-Bound Encryption）。Cookie 数据库密钥被操作系统服务锁定，**只有官方数字签名的 `chrome.exe` 或 `msedge.exe` 自身进程有权解密**。任何外部命令行（包括 `yt-dlp`）去读取时都会报 `Failed to decrypt with DPAPI`；若浏览器正在运行，还会报文件被锁定占用。
- **Firefox 的纯净标准存储**：Firefox 没有加入该专有封锁机制，其 SQLite Cookie 存储标准透明，外部授权工具可安全直读，不需要手动频繁导出 `cookies.txt`，实现全自动无感调用。

### 为什么必须携带 `--js-runtimes node`？
- 现代 YouTube 会定期轮换播放器算法并注入复杂的混淆 JavaScript 挑战（`n challenge`）。
- 如果 `yt-dlp` 无法调用本地 JS 引擎解析该算法，YouTube 就会降级甚至拒绝提供 1080p、2K、4K、8K 的音画分离流清单（提示 `n challenge solving failed`），导致只能下载 360p 或直接报 `Requested format is not available`。

---

## AI Agent 执行流程 (Agent Procedure)

当作为 OpenClaw Agent 执行该 Skill 时，必须严格遵循以下执行规程：

1. **请求与 URL 校验**：
   - 提取并校验输入的 YouTube 链接（支持 `youtube.com/watch?v=...`、`youtu.be/...`、`youtube.com/shorts/...`）。
   - 严禁绕过付费墙或违规 DRM 内容。
2. **确定执行目标宿主 (Host Routing)**：
   - 检查用户环境：若用户的浏览器登录态和本地文件位于已配对的 Node 节点（如家用 Windows/Mac），必须通过 `host=node` 将命令路由到该节点执行，绝不可在没有凭据的云端 Gateway 盲目执行。
3. **依赖与环境前置探测**：
   - 依次检查节点上的 `yt-dlp`、`ffmpeg`、`node`（或 `deno`）以及 Firefox 可用性。
   - 若在 Windows 节点上通过 `exec` 执行，不要用 Unix 分号 `;` 拼接多条命令，避免参数解析错误。
4. **执行下载与音画合成**：
   - 默认选择最佳画质与最佳音质（`bv*+ba/b`），容器格式优先选择兼容性极佳的 `mkv`。
   - 检查磁盘剩余空间，确保目标磁盘（如大容量存储盘）有充足空间承载 4K 大文件。
   - 运行标准命令，严密监控传输进度：
     ```bash
     yt-dlp --cookies-from-browser firefox --js-runtimes node -f "bv*+ba/b" --merge-output-format mkv -o "$OUTPUT_DIR/%(title).200B [%(id)s].%(ext)s" -- "$URL"
     ```
5. **验证产物与安全保护**：
   - 校验输出文件是否存在且大小正常（通常大于 0 字节）。
   - 向用户清晰汇报下载完成的文件名、保存绝对路径与文件大小。
   - **安全铁律**：严禁在任何会话历史、屏幕回显、日志输出中打印、传输或暴露 Cookie 的具体内容与凭据明文。
