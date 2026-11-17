# 邮箱查询总结 — 配置说明

本技能通过 IMAP 协议拉取邮件。使用前需在 skill 根目录配置 `accounts.json`。

---

## 一、说明

目前常用配置示例为**阿里企业邮箱**和 **QQ 邮箱**；任意支持 IMAP 的邮箱均可配置（填写对应 `host` / `port` / `folders` 即可）。

使用前需获取邮箱的**三方客户端授权码**（不是登录密码），写入 `accounts.json` 后方可查询与总结邮件。

---

## 二、阿里企业邮箱 — 获取授权码

1. 登录邮箱：https://work.aliyun.com/alimail/
2. 进入 **设置 → 查看更多设置**
3. 进入 **账号与安全 → 账户安全 → 三方客户端安全管理 → 生成新密码**
4. 输入验证码，复制保存生成的授权码（即客户端专用密码）

**IMAP 参考参数：**

| 字段 | 值 |
| --- | --- |
| host | `imap.mxhichina.com` |
| port | `993` |
| folders | `["INBOX", "Sent Messages", "已发送"]` |

---

## 三、QQ 邮箱 — 获取授权码

1. 登录邮箱：https://mail.qq.com/
2. 进入 **设置 → 账号与安全**
3. 进入 **安全设置 → 生成授权码**
4. 完成短信验证，复制保存授权码

**IMAP 参考参数：**

| 字段 | 值 |
| --- | --- |
| host | `imap.qq.com` |
| port | `993` |
| folders | `["INBOX", "Sent Messages", "已发送"]` |

---

## 四、写入 accounts.json

配置文件路径：`<skill根目录>/accounts.json`

`username` 或 `password` 为空的账户会被自动跳过。`password` 填授权码，**不要填登录密码**。

```json
{
  "_comment": "邮箱账户配置。username 或 password 为空时该账户会被自动跳过。",
  "accounts": [
    {
      "label": "阿里企业邮箱",
      "host": "imap.mxhichina.com",
      "port": 993,
      "username": "your@company.com",
      "password": "你的授权码",
      "folders": ["INBOX", "Sent Messages", "已发送"]
    },
    {
      "label": "QQ邮箱",
      "host": "imap.qq.com",
      "port": 993,
      "username": "your@qq.com",
      "password": "你的授权码",
      "folders": ["INBOX", "Sent Messages", "已发送"]
    }
  ]
}
```

### 字段说明

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `label` | 是 | 账户显示名称，会出现在邮件总结中 |
| `host` | 是 | IMAP 服务器地址 |
| `port` | 是 | IMAP 端口，SSL 通常为 `993` |
| `username` | 是 | 完整邮箱地址 |
| `password` | 是 | 三方客户端授权码 |
| `folders` | 是 | 要扫描的文件夹列表；收件箱 + 已发送文件夹 |

可配置多个账户，脚本会依次拉取并合并结果。
