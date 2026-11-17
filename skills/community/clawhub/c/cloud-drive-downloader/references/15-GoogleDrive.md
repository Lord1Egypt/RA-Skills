# Google Drive

## 链接形态

- `https://drive.google.com/file/d/xxxx/view`、文件夹链接、Google Docs/Sheets/Slides 链接。
- Google 域名在部分地区通常需要可用的网络环境；本技能不提供代理。

## 推荐通道

| 通道 | 适用 | 说明 |
|---|---|---|
| AList Google Drive 驱动 | 个人/团队盘 | OAuth 或服务账号授权 |
| rclone Google Drive | 大规模目录 | 用 rclone 配置后可作为自定义通道 |
| 浏览器导出 | 少量公开文件 | 公开分享文件可直接下载 |

## 登录

1. 按 AList Google Drive 驱动提示创建 OAuth 凭据或服务账号。
2. 在 AList 添加 Google Drive 存储并完成授权。
3. 登记 AList：

```bash
python3 scripts/pan.py set --alist-url "http://127.0.0.1:5244"
```

4. 下载：

```bash
python3 scripts/pan.py get "<GoogleDrive分享链接>" --path "/GoogleDrive/目标文件夹" --dry-run
python3 scripts/pan.py get "<GoogleDrive分享链接>" --path "/GoogleDrive/目标文件夹"
```

## 免费 / 会员

- 免费账号：15 GB 共享空间；下载速度受网络和 Google 限制。
- Google One/Workspace：容量和权限由对应套餐/管理员决定；工具不做任何绕过。
- `set-drive googledrive --tier vip` 只调整调度并发。

## 常见错误

| 现象 | 处理 |
|---|---|
| 无法连接 | 检查网络环境；技能不提供代理 |
| 403/配额不足 | 检查 API 配额、共享盘权限或服务账号权限 |
| OAuth 失效 | 在 AList 重新授权 |

## 风险提示

不要把 Google 应用密钥或服务账号 JSON 放进 Git/聊天记录。
