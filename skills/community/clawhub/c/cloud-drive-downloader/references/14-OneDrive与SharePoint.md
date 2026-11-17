# OneDrive / SharePoint

## 链接形态

- `https://1drv.ms/u/s!xxxx`、`https://onedrive.live.com/...`、`https://*.sharepoint.com/...`。
- 分享链接可能是文件、文件夹或 SharePoint 文档库。

## 推荐通道

| 通道 | 适用 | 说明 |
|---|---|---|
| AList OneDrive 驱动 | 个人 OneDrive | 授权后挂载 |
| AList SharePoint 驱动 | 企业/学校文档库 | 需要租户、站点和授权信息 |
| 浏览器下载 | 临时小文件 | 直接打开分享页，能下载就直接下载 |

## 登录

1. 在 AList 添加“OneDrive”或“SharePoint”存储，按驱动提示完成 OAuth/应用授权。
2. 登记 AList：

```bash
python3 scripts/pan.py set --alist-url "http://127.0.0.1:5244"
```

3. 文件夹递归下载：

```bash
python3 scripts/pan.py get "<OneDrive分享链接>" --path "/OneDrive/目标文件夹" --dry-run
python3 scripts/pan.py get "<OneDrive分享链接>" --path "/OneDrive/目标文件夹"
```

## 免费 / 会员

- 免费账号：受微软个人空间、分享权限和网络影响。
- 企业账号：受租户策略、管理员权限和 DLP 限制；工具不做越权访问。
- `set-drive onedrive --tier vip` 只调整调度并发，不改变微软限制。

## 常见错误

| 现象 | 处理 |
|---|---|
| OAuth 失效 | 在 AList 重新授权 |
| 分享无访问权限 | 让分享者调整权限或先保存到自己账号 |
| SharePoint 站点找不到 | 核对租户域名、站点路径和管理员授权 |

## 风险提示

公司/学校文档受组织策略约束；只下载你有权访问的内容。
