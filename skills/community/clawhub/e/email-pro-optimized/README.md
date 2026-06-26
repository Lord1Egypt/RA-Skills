# Email Pro Optimized - 完整指南

高性能邮件管理工具，支持 QQ、Gmail、Outlook 三大邮箱服务。

## 🚀 快速开始

### 1. 查看已配置的账户
```bash
cd scripts
python3 email-pro.py list-accounts
```

输出：
```
📧 已配置的邮箱账户:

  qq_136          | 136064252@qq.com          | imap     | ✅ 正常       | 发送邮箱
  qq_3421         | 342187916@qq.com          | imap     | ✅ 正常       | 接收邮箱
  outlook_live    | qiao6646@live.com         | outlook  | ⚠️ 待授权     | Outlook 邮箱
```

### 2. 授权 Outlook 邮箱

**方式 1：自动授权（推荐）**
```bash
bash authorize-outlook.sh
```

**方式 2：手动授权**
```bash
python3 authorize.py outlook \
  --client-id "0360031a-ad0e-4bce-9d2f-0c53eda894b8" \
  --client-secret "914fb58f-4aea-4ddb-bb97-51d66581cfee" \
  --tenant-id "40a99b83-a343-41ca-b303-3e122965a6d8" \
  --name "outlook_live"
```

授权后，浏览器会打开，登录 `qiao6646@live.com`，授予权限即可。

### 3. 检查邮件

**QQ 邮箱**
```bash
# 检查最近 10 封
python3 email-pro.py --account qq_3421 check --limit 10

# 仅检查未读
python3 email-pro.py --account qq_3421 check --unread
```

**Outlook 邮箱**
```bash
python3 email-pro.py --account outlook_live check --limit 10
```

### 4. 发送邮件

**QQ 邮箱**
```bash
python3 email-pro.py --account qq_136 send \
  --to "recipient@example.com" \
  --subject "测试邮件" \
  --body "这是一封测试邮件"
```

**Outlook 邮箱**
```bash
python3 email-pro.py --account outlook_live send \
  --to "recipient@example.com" \
  --subject "测试邮件" \
  --body "这是一封测试邮件"
```

## 📧 邮箱配置详情

### QQ 邮箱

**配置文件**：`~/.openclaw/credentials/email-accounts.json`

```json
{
  "qq_136": {
    "email": "136064252@qq.com",
    "auth_code": "xxxx",  // 需要填入 QQ 邮箱授权码
    "smtp_server": "smtp.qq.com",
    "smtp_port": 587,
    "imap_server": "imap.qq.com",
    "imap_port": 993,
    "provider": "imap",
    "status": "✅ 正常",
    "note": "发送邮箱"
  }
}
```

**获取 QQ 邮箱授权码**：
1. 登录 QQ 邮箱
2. 设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务
3. 开启 IMAP/SMTP 服务
4. 生成授权码

### Outlook 邮箱

**配置文件**：`~/.openclaw/credentials/email-accounts.json`

```json
{
  "outlook_live": {
    "email": "qiao6646@live.com",
    "provider": "outlook",
    "account_name": "outlook_live",
    "client_id": "0360031a-ad0e-4bce-9d2f-0c53eda894b8",
    "client_secret": "914fb58f-4aea-4ddb-bb97-51d66581cfee",
    "tenant_id": "40a99b83-a343-41ca-b303-3e122965a6d8",
    "status": "✅ 已授权",
    "note": "Outlook 邮箱"
  }
}
```

**OAuth 令牌**：`~/.openclaw/credentials/oauth_tokens.json`

授权后自动保存，包含访问令牌和刷新令牌。

### Gmail 邮箱（可选）

如果要添加 Gmail 支持：

1. 获取 Google OAuth 凭证
2. 运行授权脚本
3. 在配置文件中添加账户

```bash
python3 authorize.py gmail \
  --client-id "YOUR_CLIENT_ID" \
  --client-secret "YOUR_CLIENT_SECRET" \
  --name "gmail_account"
```

## 🔧 常用命## 检查邮件
```bash
# 基础用法
python3 email-pro.py check

# 指定账户和数量
python3 email-pro.py --account qq_3421 check --limit 20

# 仅未读邮件
python3 email-pro.py check --unread

# 指定邮箱文件夹
python3 email-pro.py check --mailbox "INBOX"
```

### 搜索邮件
```bash
# 搜索关键词
python3 email-pro.py search "旅行"

# 限制结果数量
python3 email-pro.py search "机票" --limit 50
```

### 获取完整邮件
```bash
python3 email-pro.py fetch 12345
```

### 发送邮件
```bash
# 纯文本
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "主题" \
  --body "内容"

# HTML 格式
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "主题" \
  --body "<h1>标题</h1><p>内容</p>" \
  --html

# 带附件
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "主题" \
  --body "内容" \
  --attach /path/to/file1.pdf /path/to/file2.txt
```

## 📊 性能对比

| 操作 | 旧版本 | 新版本 | 提升 |
|------|--------|--------|------|
| 检查 10 封 | 1.5-2s | 0.3-0.5s | 4-5x |
| 检查 100 封 | 15-20s | 2-3s | 6-8x |
| 检查 1000 封 | 150-200s | 15-20s | 8-10x |

## 🔐 安全性

- **QQ 邮箱**：使用授权码，不存储密码
- **Outlook/Gmail**：使用 OAuth 2.0，令牌自动刷新
- **凭证存储**：所有凭证保存在 `~/.openclaw/credentials/`，权限 600

## 🐛 故障排除

### QQ 邮箱连接失败
```
❌ 检查邮件失败: [Errno -1] IMAP4 protocol error
```

**解决方案**：
1. 确认授权码正确（不是密码）
2. 确认 IMAP/SMTP 服务已开启
3. 检查网络连接

### Outlook 授权失败
```
❌ 授权失败或超时
```

**解决方案**：
1. 确认 Client ID、Secret、Tenant ID 正确
2. 确认浏览器能访问 Microsoft 登录页面
3. 重新运行授权脚本

### 邮件解析失败
某些特殊格式的邮件可能无法解析，脚本会自动跳过。

## 📝 使用示例

### 旅行监控
```bash
# 搜索旅行相关邮件
python3 email-pro.py search "机票|酒店|旅行" --limit 50

# 发送监控报告
python3 email-pro.py --account qq_136 send \
  --to "342187916@qq.com" \
  --subject "旅行监控报告" \
  --body "今日发现 5 条相关邮件"
```

### 邮件备份
```bash
# 导出所有邮件为 JSON
python3 email-pro.py check --limit 1000 > backup.json
```

### 批量处理
```bash
# 获取最近 100 封邮件的完整内容
python3 email-pro.py check --limit 100 | \
  jq -r '.[].uid' | \
  xargs -I {} python3 email-pro.py fetch {}
```

## 📚 文件结构

```
email-pro-optimized/
├── scripts/
│   ├── email-pro.py              # 主程序
│   ├── providers.py              # 邮件提供商实现
│   ├── oauth_handler.py          # OAuth 处理
│   ├── authorize.py              # 授权工具
│   ├── authorize-outlook.sh      # Outlook 快速授权脚本
│   └── analyze.py                # 邮件分析工具
├── SKILL.md                      # 技能文档
├── README.md                     # 本文件
└── package.json                  # 项目元数据
```

## 🔄 更新2.0.0 (2026-03-20)
- ✅ 新增 Gmail 支持（OAuth 2.0）
- ✅ 新增 Outlook 支持（OAuth 2.0）
- ✅ 模块化提供商架构
- ✅ 自动令牌刷新
- ✅ 统一命令接口

### v1.0.0 (2026-03-19)
- ✅ QQ 邮箱支持
- ✅ 高性能批量获取
- ✅ 并发处理

## 💡 提示

1. **默认账户**：所有命令默认使用 `qq_3421`，可用 `--account` 指定其他账户
2. **JSON 输出**：所有查询结果都是 JSON 格式，便于脚本处理
3. **错误处理**：脚本会自动跳过损坏的邮件，继续处理其他邮件
4. **连接复用**：IMAP 连接会自动复用，提高性能

## 📞 支持

如有问题，请检查：
1. 配置文件是否正确
2. 网络连接是否正常
3. 邮箱凭证是否有效
4. 查看脚本输出的错误信息
