# 部署详细文档

## 一、依赖项

### Python 虚拟环境

推荐使用 `uv` 创建：

```bash
uv venv /tmp/douyin_transcribe --python 3.12
source /tmp/douyin_transcribe/bin/activate
pip install faster-whisper yt-dlp python-docx requests
```

或直接运行 `setup_douyin_daily_report.sh` 自动完成。

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `SMTP_USER` | ✅ | QQ 邮箱地址 |
| `SMTP_PASS` | ✅ | QQ 邮箱 SMTP 授权码（不是密码）|
| `SMTP_HOST` | | 默认 `smtp.qq.com` |
| `SMTP_PORT` | | 默认 `587` |
| `DOUYIN_EMAIL_RECIPIENTS` | ✅ | 收件人，逗号分隔 |
| `DOUYIN_DIGEST_LIMIT` | | 默认 `15` |
| `DOUYIN_VENV_PY` | | 默认 `/tmp/douyin_transcribe/venv/bin/python3` |

### TikHub API Token

在 `~/.openclaw/config.json` 中配置：

```json
{
  "tikhub_api_token": "tk_live_xxxxxxxxxxxx"
}
```

注册地址：https://user.tikhub.io

## 二、获取 QQ 邮箱授权码

1. 登录 QQ 邮箱 → 设置 → 账户
2. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
3. 开启"SMTP服务"→ 获取授权码（16位）
4. 将授权码填入 `SMTP_PASS`

## 三、Cron 定时任务

手动设置：

```bash
# 每天 08:00 和 16:00 执行
0 8,16 * * *  bash /root/.openclaw/workspace/skills/douyin-daily-report/scripts/cron_daily_digest_wrapper.sh 15 >> /tmp/douyin_cron.log 2>&1
```

## 四、故障排查

### 邮件发送失败
- 检查 `SMTP_USER` 和 `SMTP_PASS` 是否正确
- 确认 QQ 邮箱授权码未过期

### TikHub API 失败
- 确认 `tikhub_api_token` 已写入 `~/.openclaw/config.json`
- 确认 Token 未过期（tk_live_ 开头为正式版）

### DOCX 附件显示 .bin
- 当前已修复，使用 `EmailMessage.add_attachment()` 自动处理文件名编码
- 如仍有问题，检查邮件客户端是否支持 RFC 5987

### LLM 分析失败
- 确认 OpenClaw Gateway 运行中（`openclaw gateway status`）
- 确认 session key 有效：`agent:main:lightclawbot:direct:100012167891`

### 日报只有 3 条内容
- 检查日报文件大小，超过 500 字符邮件正文不会被截断
- 可能是 TikHub 返回数据不足（免费版限制）

## 五、卸载

```bash
# 删除 Cron
crontab -l | grep -v "douyin_daily_digest" | crontab -

# 删除虚拟环境
rm -rf /tmp/douyin_transcribe

# 删除输出文件
rm -rf ~/Documents/douyin_analysis

# 删除技能目录
rm -rf /root/.openclaw/workspace/skills/douyin-daily-report
```
