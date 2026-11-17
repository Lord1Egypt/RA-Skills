# Dropbox

## 链接形态

- `https://www.dropbox.com/s/xxxx/file.zip`、`https://db.tt/...`，可能是文件或文件夹分享。

## 推荐通道

| 通道 | 适用 | 说明 |
|---|---|---|
| AList Dropbox 驱动 | 个人账号 | OAuth 授权后挂载 |
| rclone Dropbox | 目录同步 | 需要时用 `engine_command` 接入 |
| 浏览器下载 | 公开单文件 | 小文件可先用浏览器验证链接 |

## 登录

1. 在 AList 添加“Dropbox”存储，按驱动提示完成 OAuth。
2. 登记 AList：

```bash
python3 scripts/pan.py set --alist-url "http://127.0.0.1:5244"
```

3. 下载：

```bash
python3 scripts/pan.py get "<Dropbox分享链接>" --path "/Dropbox/目标文件夹" --dry-run
python3 scripts/pan.py get "<Dropbox分享链接>" --path "/Dropbox/目标文件夹"
```

## 免费 / 会员

- 免费账号：容量与流量按 Dropbox 规则；本工具默认单线程、断点续传。
- 会员：`set-drive dropbox --tier vip` 只调整调度并发，不绕过平台限制。

## 常见错误

| 现象 | 处理 |
|---|---|
| OAuth 过期 | 在 AList 重新授权 |
| 分享要求登录 | 先登录 Dropbox 或让分享者开放权限 |
| 目录下载不完整 | 确认使用 rclone/AList 递归，而不是 curl 单文件 |

## 风险提示

OAuth token 等同账号访问权，建议使用独立应用授权和小号。
