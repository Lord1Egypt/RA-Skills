# 发布到 ClawHub 指南

## 📦 发布前准备

### 1. 完善技能信息

编辑 `skill.json`，更新以下字段：

```json
{
  "author": "你的 GitHub 用户名",
  "repository": "https://github.com/你的用户名/free-model-finder"
}
```

### 2. 创建 GitHub 仓库（推荐）

```bash
# 在 GitHub 创建新仓库：free-model-finder

# 本地初始化 git
cd C:\Users\sukun\.openclaw\workspace\skills\free-model-finder
git init
git add .
git commit -m "Initial commit: free-model-finder skill"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/free-model-finder.git
git push -u origin main
```

### 3. 测试技能

```bash
# 安装并测试
pip install -e .

# 验证命令
free-model-finder list
free-model-finder status
free-model-finder auto --dry-run
```

---

## 🚀 发布方法

### 方法 A：使用 ClawHub CLI（推荐）

```bash
# 安装 ClawHub CLI
npm install -g clawhub

# 登录 ClawHub
clawhub login

# 发布技能
clawhub publish ./free-model-finder
```

### 方法 B：手动提交到 ClawHub

1. 访问 https://clawhub.ai/submit
2. 填写技能信息：
   - **Name**: free-model-finder
   - **Display Name**: Free Model Finder - 多平台免费模型
   - **Description**: 发现、对比和配置多平台免费/低价 AI 模型。支持 OpenRouter、Groq、Google AI Studio、Ollama、HuggingFace 等平台。
   - **Repository**: 你的 GitHub 仓库地址
   - **Version**: 0.1.0
   - **License**: MIT
3. 提交审核

---

## 📝 发布清单

- [ ] 更新 `skill.json` 中的 author 和 repository
- [ ] 测试所有命令正常工作
- [ ] 编写清晰的 README.md
- [ ] 添加 LICENSE 文件
- [ ] 创建 GitHub 仓库（可选但推荐）
- [ ] 准备技能截图或演示（可选）

---

## 🔍 审核要点

ClawHub 审核团队会检查：

1. ✅ 技能功能正常
2. ✅ 文档清晰完整
3. ✅ 无恶意代码
4. ✅ 权限范围合理
5. ✅ 符合 OpenClaw 技能规范

---

## 📢 发布后

发布成功后，用户可以通过以下命令安装：

```bash
# 通过 ClawHub 安装
npx clawhub@latest install free-model-finder

# 或手动安装
git clone https://github.com/YOUR_USERNAME/free-model-finder.git
cd free-model-finder
pip install -e .
```

---

## 💡 提示

- 保持技能简洁专注
- 提供清晰的安装和使用说明
- 及时响应用户反馈
- 定期更新维护

祝发布顺利！🎉
