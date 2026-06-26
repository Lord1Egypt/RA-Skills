# GitHub 仓库设置指南

## 🚀 快速开始

### 1. 创建 GitHub 仓库

访问 https://github.com/new 创建新仓库：

- **Repository name:** `china-install-skills`
- **Description:** 中国大陆专用 ClawHub 技能安装工具 - 绕过 API 限流
- **Visibility:** ✅ Public（公开）
- **Initialize:** ❌ 不要勾选（我们已有本地代码）

### 2. 推送代码到 GitHub

```bash
# 进入仓库目录
cd /tmp/china-install-skills-repo

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/5145852587/china-install-skills.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 3. 配置 ClawHub Token

1. 获取 ClawHub Token：
   ```bash
   clawhub login
   clawhub whoami
   ```

2. 在 GitHub 仓库设置中添加 Secret：
   - 访问：https://github.com/5145852587/china-install-skills/settings/secrets/actions
   - 点击 "New repository secret"
   - **Name:** `CLAWHUB_TOKEN`
   - **Value:** (粘贴你的 ClawHub token)

### 4. 发布第一个版本

```bash
# 创建版本标签
git tag v1.0.0

# 推送标签（触发自动发布）
git push origin v1.0.0
```

### 5. 验证发布

- **GitHub Actions:** https://github.com/5145852587/china-install-skills/actions
- **ClawHub 页面:** https://clawhub.com/skills?q=china-install-skills

---

## 📋 检查清单

- [ ] 创建 GitHub 仓库
- [ ] 推送代码
- [ ] 配置 CLAWHUB_TOKEN Secret
- [ ] 推送 v1.0.0 标签
- [ ] 验证 GitHub Actions 执行成功
- [ ] 验证 ClawHub 上可以看到技能

---

## 🔧 常见问题

### Q: 如何获取 ClawHub Token？

```bash
clawhub login
# 浏览器会打开进行 GitHub 授权
# 授权后 token 会自动保存
```

### Q: GitHub Actions 失败怎么办？

1. 检查 Secret 配置是否正确
2. 查看 Actions 日志了解详细错误
3. 常见错误：
   - `Not logged in` → 检查 CLAWHUB_TOKEN
   - `Version already exists` → 使用新版本号
   - `SKILL.md required` → 检查文件格式

### Q: 如何更新版本？

```bash
# 1. 修改代码
# 2. 更新 _meta.json 版本号
# 3. 提交
git add .
git commit -m "chore: bump version to 1.0.1"

# 4. 推送新标签
git tag v1.0.1
git push origin v1.0.1
```

---

**设置完成后，每次推送 v* 标签都会自动发布到 ClawHub！** 🎉
