# 🚀 快速发布指南

由于 ClawHub 登录需要浏览器交互验证，请按以下步骤手动完成发布：

---

## 方式一：使用 ClawHub 网页版（推荐）

### 步骤 1: 访问 ClawHub 网站

打开浏览器访问：https://clawhub.com

### 步骤 2: 登录账号

- 点击右上角 "Login"
- 使用 GitHub/Google 账号登录，或注册新账号

### 步骤 3: 进入发布页面

登录后访问：https://clawhub.com/publish

### 步骤 4: 上传技能

**方式 A: 上传 ZIP 文件**

1. 打包技能目录：
   ```bash
   # PowerShell
   Compress-Archive -Path "C:\Users\admin\.openclaw\skills\feishu_process_feedback\*" `
                    -DestinationPath "C:\Users\admin\Desktop\feishu-process-feedback.zip" `
                    -Force
   ```

2. 在网页上选择 "Upload ZIP"
3. 选择刚才创建的 ZIP 文件
4. 填写发布信息：
   - **Slug**: `feishu-process-feedback`
   - **Name**: `Feishu Process Feedback`
   - **Version**: `1.0.0`
   - **Changelog**: `初始版本：基础监听、进度反馈、进程管理、错误重试`

5. 点击 "Publish"

**方式 B: 连接 GitHub 仓库**

1. 将技能推送到 GitHub：
   ```bash
   cd C:\Users\admin\.openclaw\skills\feishu_process_feedback
   git init
   git add .
   git commit -m "Initial release: feishu-process-feedback v1.0.0"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. 在 ClawHub 网页选择 "Connect GitHub"
3. 选择刚才推送的仓库
4. 点击 "Publish"

---

## 方式二：使用 CLI（需要浏览器验证）

### 步骤 1: 登录 ClawHub

```bash
clawhub login
```

这会打开浏览器，按提示完成登录验证。

### 步骤 2: 验证登录

```bash
clawhub whoami
```

成功会显示你的账号信息。

### 步骤 3: 发布技能

```bash
cd C:\Users\admin\.openclaw\skills\feishu_process_feedback

clawhub publish . `
  --slug feishu-process-feedback `
  --name "Feishu Process Feedback" `
  --version 1.0.0 `
  --changelog "初始版本：基础监听、进度反馈、进程管理、错误重试、状态持久化"
```

### 步骤 4: 验证发布

```bash
clawhub search feishu-process-feedback
```

---

## 发布后验证

### 检查技能信息

```bash
clawhub inspect feishu-process-feedback
```

### 测试安装

```bash
# 在新目录测试安装
mkdir C:\temp\test-skill
cd C:\temp\test-skill
clawhub install feishu-process-feedback
```

---

## 常见问题

### Q: 浏览器没有自动打开？

**解决：**
1. 手动访问 `https://clawhub.com/login`
2. 登录后返回 CLI 继续

### Q: 发布失败 "Slug already taken"？

**解决：**
- 使用不同的 slug，如 `feishu-process-feedback-cn`
- 或联系原发布者

### Q: 发布失败 "Invalid skill structure"？

**解决：**
```bash
# 检查必需文件
ls SKILL.md package.json

# 验证 frontmatter
head -10 SKILL.md
```

---

## 发布检查清单

发布前确认：

- [ ] SKILL.md 包含正确的 YAML frontmatter
- [ ] package.json 版本号为 1.0.0
- [ ] 已删除临时文件（.log, .json 状态文件）
- [ ] 已在本地测试所有功能
- [ ] README.md 和 PUBLISH_GUIDE.md 已更新

---

_提示：首次发布建议使用网页版，更直观且容易排查问题。_
