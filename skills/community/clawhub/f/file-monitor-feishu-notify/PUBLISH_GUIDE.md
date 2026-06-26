# 发布指南

## 快速发布

### 发布到 GitHub

```powershell
# 方式 1: 使用脚本（推荐）
powershell -ExecutionPolicy Bypass -File "publish-to-github.ps1"

# 方式 2: 手动执行
cd C:\Users\43900\.openclaw\workspace\skills\file-monitor-feishu-notify
git push -u origin main
```

**仓库地址**: https://github.com/huyoujin-cd/file-monitor-feishu-notify

---

### 发布到 ClawHub

```powershell
# 方式 1: 使用脚本（推荐）
powershell -ExecutionPolicy Bypass -File "publish-to-clawhub.ps1"

# 方式 2: 手动执行
clawhub login
clawhub publish "C:\Users\43900\.openclaw\workspace\skills\file-monitor-feishu-notify" `
    --slug file-monitor-feishu-notify `
    --name "File Monitor Feishu Notify" `
    --version "1.0.0"
```

---

## 手动发布步骤

### GitHub 发布

1. **创建仓库**
   - 访问 https://github.com/new
   - 仓库名：`file-monitor-feishu-notify`
   - 可见性：Public
   - 点击 "Create repository"

2. **推送代码**
   ```powershell
   cd C:\Users\43900\.openclaw\workspace\skills\file-monitor-feishu-notify
   git remote add origin https://github.com/huyoujin-cd/file-monitor-feishu-notify.git
   git branch -M main
   git push -u origin main
   ```

3. **创建 Release**（可选）
   - 访问 https://github.com/huyoujin-cd/file-monitor-feishu-notify/releases/new
   - Tag version: `v1.0.0`
   - Release title: `v1.0.0 - Initial Release`
   - 点击 "Publish release"

---

### ClawHub 发布

1. **登录**
   ```powershell
   clawhub login
   ```

2. **发布**
   ```powershell
   clawhub publish "C:\Users\43900\.openclaw\workspace\skills\file-monitor-feishu-notify" `
       --slug file-monitor-feishu-notify `
       --name "File Monitor Feishu Notify" `
       --version "1.0.0"
   ```

3. **验证**
   ```powershell
   clawhub search file-monitor
   ```

---

## 发布后验证

### GitHub
- [ ] 仓库可访问：https://github.com/huyoujin-cd/file-monitor-feishu-notify
- [ ] 代码已推送
- [ ] README.md 正确显示
- [ ] Release 已创建

### ClawHub
- [ ] Skill 可搜索到
- [ ] 安装测试通过
- [ ] 文档正确显示

---

## 常见问题

### Q: GitHub 推送失败？
A: 检查网络连接，或手动在 GitHub 创建仓库后推送。

### Q: ClawHub 登录失败？
A: 确保已注册 ClawHub 账号，或联系管理员。

### Q: 发布后如何更新？
A: 修改版本号（如 `1.0.1`），重新执行发布命令。

---

## 发布清单

发布前确认：
- [x] config.json 不包含敏感信息（使用 config.example.json）
- [x] .gitignore 已配置
- [x] README.md 完整
- [x] SKILL.md 版本号正确
- [x] 测试通过
- [ ] GitHub 推送成功
- [ ] ClawHub 发布成功

---

**祝发布顺利！** 🚀
