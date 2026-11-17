# 安装与启动说明（cn-browser-automation）

本 skill 的核心是"接入本机已登录的 Chrome"，因此只需要 Chrome + Playwright 的连接能力，不需要下载额外浏览器。

## 1. 启动带远程调试的 Chrome（保留登录态）

### 方式 A：让脚本自动启动（推荐）
```bash
python scripts/connect_chrome.py <url> --launch
```
脚本会自动找到本机 Chrome，用独立的 `user-data-dir`（默认 `~/.cn-browser-chrome-profile`）启动并打开调试端口。首次会要求你在弹出的浏览器里登录一次，之后登录态保留在该用户目录。

### 方式 B：手动启动（可复用你日常用的 Chrome 配置）
若想直接复用你**日常使用的登录态**（而非独立 profile），关闭所有 Chrome 后，用你平时的用户数据目录启动：

Windows（PowerShell）：
```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="$env:LOCALAPPDATA\Google\Chrome\User Data"
```
macOS：
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome"
```
> ⚠️ 用日常用户目录时，连接后脚本看到的页面/登录态就是你的真实账号；请只对个人授权数据操作。

启动后验证端口：浏览器打开 `http://127.0.0.1:9222/json/version` 能看到 JSON 即成功。

## 2. 安装 Playwright（仅连接能力）

```bash
pip install playwright -i https://mirrors.tencent.com/pypi/simple/
```
`connect_over_cdp` 不需要下载 chromium，但如报缺浏览器，可补：
```bash
playwright install chromium
```

## 3. 受限网络 / 镜像

若 `pip` 官方源超时，统一走腾讯镜像（本机环境实测可用）：
```bash
pip install playwright -i https://mirrors.tencent.com/pypi/simple/
```

## 4. 常见排错

- **端口被占用**：换 `--port 9333` 等，或关掉占用 9222 的 Chrome。
- **连不上**：确认 Chrome 确实带 `--remote-debugging-port` 启动；防火墙一般不影响本机回环地址。
- **登录态没生效**：确认连接的是"已登录那个上下文"（脚本默认用 `browser.contexts[0]`）；若用了独立 profile 首次需手动登录一次。
- **页面空白 / 被反爬挡**：加 `--wait "<选择器>"` 等元素出现；遇滑块先在浏览器人工过一次再让脚本继续。
- **No usable sandbox**：Linux 下可加 `--no-sandbox` 到启动参数（脚本默认未加，必要时自行追加）。
