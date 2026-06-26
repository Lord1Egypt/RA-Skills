# 自动发布配置指南

## 支持平台

| 平台 | 工具 | 认证方式 |
|------|------|----------|
| `bilibili` | biliup | 扫码登录 |
| `youtube` | Google API | OAuth 2.0 |
| `tiktok` | Cookie | 浏览器 Cookie |
| `xiaohongshu` | Cookie | 浏览器 Cookie |

## 配置目录

```bash
mkdir -p ~/.fcpx-assistant/publish
chmod 700 ~/.fcpx-assistant/publish
```

## B 站配置

**安装 biliup：**
```bash
pip3 install --break-system-packages biliup
biliup login  # 扫码登录
```

**配置文件** `~/.fcpx-assistant/publish/bilibili.json`：
```json
{
  "cookie": "登录后复制的 cookie（推荐）",
  "upload_source": 1
}
```

获取 Cookie：登录 bilibili.com → F12 开发者工具 → 复制请求头 Cookie

## YouTube 配置

**配置文件** `~/.fcpx-assistant/publish/youtube.json`：
```json
{
  "client_secrets": "/path/to/client_secret.json",
  "token": "/path/to/token.json"
}
```

获取凭证：Google Cloud Console → 创建项目 → 启用 YouTube Data API → OAuth 2.0 凭证

## 抖音 / 小红书配置

**配置文件** `~/.fcpx-assistant/publish/<platform>.json`：
```json
{
  "cookie": "登录后复制的 cookie"
}
```

- 抖音：登录 creator.douyin.com → F12 复制 Cookie
- 小红书：同理

## 安全提示

```bash
chmod 600 ~/.fcpx-assistant/publish/*.json  # 限制权限
```

- 使用 Cookie 而非密码
- 不要提交到 Git
- 定期更新 Cookie（有过期时间，B站约180天）

## 使用示例

```bash
# 上传到 B 站
bash scripts/auto-publish.sh \
    --video final.mp4 --platform bilibili \
    --title "我的视频" --tags "vlog，日常"

# 初始化配置
bash scripts/auto-publish.sh --config

# 故障排查
biliup renew   # 检查登录状态
biliup login   # 重新登录
```
