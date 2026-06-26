---
name: 1password-browser-login
description: |
  从 1Password 取出账号密码，用无头浏览器自动登录目标网站，然后根据用户需求操作页面。
  适用场景：用户说"帮我登录 xxx 然后做 yyy"、"用 1Password 登录 xxx"、"从 1Password 取 xxx 的账号登录并下载数据/截图/抓取内容"等。
  前提：系统已安装 1Password CLI（op），且 OP_SERVICE_ACCOUNT_TOKEN 已配置在 ~/.zshrc 中。
---

# 1Password Browser Login

从 1Password 取凭证，无头浏览器自动登录，执行用户指定任务。

## 前提检查

```bash
source ~/.zshrc 2>/dev/null && op whoami 2>&1
```

若失败，提示用户配置 `OP_SERVICE_ACCOUNT_TOKEN`。

## 执行流程

### Step 1：解析意图

从用户消息提取：
- `ITEM_NAME`：1Password 中的 item 名称
- `TASK`：登录后要做什么

`ITEM_NAME` 不明确时，列出所有可用 item 让用户选：
```bash
source ~/.zshrc 2>/dev/null && op item list --format json 2>&1
```

### Step 2：取凭证

服务账户必须指定 vault，先列出：
```bash
source ~/.zshrc 2>/dev/null && op vault list --format json 2>&1
```

取 item 详情：
```bash
source ~/.zshrc 2>/dev/null && op item get "<ITEM_NAME>" --vault "<VAULT_NAME>" --format json 2>&1
```

从 JSON 中提取：
- `fields[]` 中 `purpose=USERNAME` 的 `value` → username
- `fields[]` 中 `purpose=PASSWORD` 的 `value` → password
- `urls[0].href` → 登录页 URL

⚠️ 安全规则：
- 禁止将 password 打印到回复或日志
- 禁止将凭证写入任何文件
- 回复用户只说"已从 1Password 取得凭证"

### Step 3：浏览器登录

```
browser open url=<登录页URL>
browser snapshot → 找用户名输入框、密码输入框、登录按钮的 ref
browser act kind=type ref=<用户名框> text=<username>
browser act kind=type ref=<密码框> text=<password>
browser act kind=click loadState=networkidle ref=<登录按钮>
browser snapshot → 确认已离开登录页（登录成功）
```

### Step 4：执行任务

| 任务类型 | 操作 |
|---------|------|
| 截图 | `browser screenshot` → 保存到 `./downloads/` → `MEDIA:./downloads/文件名` 发给用户 |
| 抓页面数据 | `browser snapshot` → 解析内容 → 整理回复 |
| 下载文件 | `browser act kind=click` 触发下载 → `exec` 找到文件移到 workspace → `MEDIA:` 发送 |
| 导航后操作 | `browser navigate url=<目标页>` → 再截图/抓数据/下载 |

结果文件保存路径：`./downloads/YYYY-MM-DD_<网站名>_<描述>.<扩展名>`

## 错误处理

| 错误 | 处理 |
|------|------|
| item 不存在 | 列出所有 item，让用户确认名称 |
| vault 无权限 | 提示在 1Password 后台给服务账户授权该 vault |
| 登录失败（密码错误） | 截图当前页，告知用户 |
| 需要 2FA | 告知不支持，需用户手动处理 |
| CAPTCHA | 截图，告知用户需手动完成验证 |
| 找不到输入框 | 截图，让用户描述表单位置 |

## 示例

**用户：** 帮我登录 MyApp 然后截个首页截图
1. ITEM_NAME="MyApp"，TASK="截首页截图"
2. 取凭证 → browser 登录 → screenshot → 发给用户

**用户：** 用 1Password 登录 GitHub 下载最新 release
1. ITEM_NAME="GitHub"，TASK="下载最新 release"
2. 取凭证 → 登录 → 导航到 releases 页 → 点击下载 → 发文件
