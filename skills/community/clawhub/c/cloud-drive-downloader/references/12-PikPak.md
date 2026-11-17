# PikPak

## 链接形态

- `https://mypikpak.com/s/xxxx`、`https://pikpak.com/...`。
- 分享可能包含文件、文件夹或磁力/离线任务；地区可用性受账号和网络影响。

## 推荐通道

| 通道 | 适用 | 说明 |
|---|---|---|
| AList PikPak 驱动 | 个人自用 | 用账号登录或授权挂载 |
| PikPak 网页/客户端 | 前置操作 | 分享先保存到自己的 PikPak |
| 官方 API | 有开发者权限时 | 按官方文档申请接入 |

## 登录

1. 在 AList 添加“PikPak”存储，按驱动提示填写账号、密码或 token。
2. 登记 AList：

```bash
python3 scripts/pan.py set --alist-url "http://127.0.0.1:5244"
```

3. 分享保存到自己的 PikPak 后下载：

```bash
python3 scripts/pan.py get "<PikPak分享链接>" --path "/PikPak/目标文件夹" --dry-run
python3 scripts/pan.py get "<PikPak分享链接>" --path "/PikPak/目标文件夹"
```

## 免费 / 会员

- 免费账号：空间、离线次数、速度和并发由 PikPak 决定。
- 会员：`set-drive pikpak --tier vip` 只调整本工具调度并发，不提供任何绕过。

## 常见错误

| 现象 | 处理 |
|---|---|
| 登录失败/区域不可用 | 检查账号所在地区、网络和 AList 驱动版本 |
| 分享保存失败 | 先用网页/客户端保存到自己的 PikPak |
| 下载中断 | 保留任务目录，重新执行利用断点续传 |

## 风险提示

账号密码/token 等同登录态；不要把凭据写入 Git 或聊天记录。
