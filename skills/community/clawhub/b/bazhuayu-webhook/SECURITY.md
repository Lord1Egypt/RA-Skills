# 安全指南

本文档说明如何安全地使用八爪鱼 RPA Webhook Skill。

---

## 🔐 安全威胁模型

### 潜在风险

| 风险 | 描述 | 影响 |
|------|------|------|
| 密钥泄露 | config.json 被未授权访问 | 攻击者可触发 RPA 任务 |
| 日志泄露 | 日志包含敏感参数 | 暴露业务数据 |
| 版本控制泄露 | config.json 被提交到 Git | 密钥公开暴露 |
| 文件权限不当 | 其他用户可读取配置 | 本地信息泄露 |

---

## ✅ 安全最佳实践

### 1. 使用环境变量存储敏感信息

**推荐方式：**

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export BAZHUAYU_WEBHOOK_URL="https://api-rpa.bazhuayu.com/..."
export BAZHUAYU_WEBHOOK_KEY="your-secret-key"

# 可选：参数默认值
export BAZHUAYU_PARAM_KEYWORD="默认关键词"
```

**优势：**
- 密钥不存储在磁盘中
- 进程结束后自动清除
- 不会被版本控制追踪

### 2. 保护配置文件

如果必须使用配置文件：

```bash
# 设置正确权限 (仅所有者可读写)
chmod 600 config.json

# 验证权限
ls -la config.json
# 应显示：-rw------- 1 user user ...
```

### 3. 防止版本控制泄露

```bash
# 确保 .gitignore 包含 config.json
cat .gitignore

# 如果已提交，从 Git 历史中移除
git rm --cached config.json
git commit -m "Remove sensitive config"
```

### 4. 日志安全

```bash
# 日志文件也应设置严格权限
chmod 600 *.log

# 定期清理日志
find . -name "*.log" -mtime +30 -delete
```

### 5. 定期安全检查

```bash
# 运行内置安全检查
python3 bazhuayu-webhook.py secure-check
```

---

## 🛡️ 安全配置选项

### 混合模式（推荐）

敏感信息用环境变量，非敏感信息用配置文件：

```bash
# 环境变量
export BAZHUAYU_WEBHOOK_KEY="secret-key"

# config.json (不包含 key)
{
  "url": "https://api-rpa.bazhuayu.com/...",
  "key": "",  # 留空，从环境变量读取
  "paramNames": ["keyword"],
  "defaultParams": {
    "keyword": "默认值"
  }
}
```

### 纯环境变量模式

所有配置都使用环境变量：

```bash
export BAZHUAYU_WEBHOOK_URL="..."
export BAZHUAYU_WEBHOOK_KEY="..."
export BAZHUAYU_PARAM_KEYWORD="..."
```

---

## 🚨 应急响应

### 如果密钥可能已泄露

1. **立即撤销密钥**
   - 登录八爪鱼 RPA 控制台
   - 删除/重置 Webhook 触发器密钥

2. **检查日志**
   - 查看是否有异常调用记录
   - 检查 RPA 任务执行历史

3. **更新配置**
   - 生成新密钥
   - 更新所有配置位置
   - 运行 `secure-check` 验证

### 如果配置文件已提交到 Git

```bash
# 1. 从 Git 历史中移除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config.json" \
  --prune-empty --tag-name-filter cat -- --all

# 2. 推送更改
git push origin --force --all

# 3. 联系 GitHub/GitLab 支持清除缓存 (如已推送到远程)

# 4. 重置密钥 (必须!)
```

---

## 📋 安全检查清单

使用前请确认：

- [ ] config.json 权限为 600
- [ ] config.json 在 .gitignore 中
- [ ] 敏感参数使用环境变量
- [ ] 日志文件权限正确
- [ ] 运行 `secure-check` 无警告

---

## 🔍 审计日志

如需审计调用记录：

```bash
# 启用详细日志
python3 bazhuayu-webhook.py run --dry-run > audit.log 2>&1
chmod 600 audit.log

# 查看日志
cat audit.log
```

---

## 📞 报告安全问题

如发现安全漏洞，请：

1. **不要**公开披露
2. 联系技能作者
3. 等待修复后更新

---

**安全是持续过程，请定期审查和更新配置。**
