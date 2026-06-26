# B 站字幕 — 参考与排错

## 官方与工具

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 提取器含 BiliBili。
- B 站接口与风控会变，**优先保持 yt-dlp 最新**。

## 常见错误

### HTTP 412 Precondition Failed

- **原因**：匿名或异常请求被拦；部分网络环境更易触发。
- **处理**：
  1. `yt-dlp -U` 或 `brew upgrade yt-dlp`
  2. `--cookies-from-browser chrome`（或本机常用浏览器）
  3. 使用从浏览器导出的 `cookies.txt` + `--cookies cookies.txt`
  4. 换网络/VPN 再试（若政策允许）

### 没有字幕语言列出

- 该稿件可能确实无字幕；换有「CC」或 UP 注明字幕的稿件测试。

### 只有繁体/英文

- 调整 `--sub-langs`，例如 `zh-Hant,zh-Hans,en`。

## v2 可能扩展（未实现）

- 无字幕时：下载音频 + 本地 Whisper / 已有 `openai-whisper` skill。
- 统一封装 CLI：`bili-subs BVxxx`（若单独开源可再挂 ClawHub）。

## 合规

- 仅处理**用户有权访问**的公开或已授权内容；遵守平台条款与版权。
