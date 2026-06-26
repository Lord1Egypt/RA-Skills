# Auth Guard 发布指南

## 发布到 GitHub

### 1. 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库（不初始化）
# 仓库名：auth-guard-skill
# 可见性：Public
# 描述：Authorization protection skill for OpenClaw
```

### 2. 添加远程仓库

```bash
cd auth-guard
git remote add origin https://github.com/YOUR_USERNAME/auth-guard-skill.git
git branch -M main
git push -u origin main
```

### 3. 创建 Release

```bash
# 在 GitHub 上创建 Release
# Tag: v1.0.0
# Title: Auth Guard v1.0.0 - Initial Release
# Description: 初始版本发布
```

### 4. 更新远程

```bash
# 如果有人 fork 或 clone
git push origin main
```

## 发布到 ClawHub

### 方式 1: 使用 clawhub CLI

```bash
# 登录 ClawHub
clawhub login

# 发布技能
cd auth-guard
clawhub publish
```

### 方式 2: 手动上传

1. 访问 https://clawhub.com
2. 登录账号
3. 点击 "Publish Skill"
4. 填写信息：
   - Name: auth-guard
   - Version: 1.0.0
   - Description: 授权保护技能 - 所有外部 API 操作必须经过用户明确授权
   - Repository: https://github.com/YOUR_USERNAME/auth-guard-skill.git
   - License: MIT
   - Tags: security, authorization, protection, audit
5. 上传 clawhub.yaml
6. 提交审核

## 发布后检查

### GitHub

- [ ] 仓库可见性为 Public
- [ ] README.md 显示正确
- [ ] License 文件存在
- [ ] Release 已创建
- [ ] 所有文件都已推送

### ClawHub

- [ ] Skill 已发布
- [ ] 描述和标签正确
- [ ] 安装说明完整
- [ ] 示例代码可运行
- [ ] 版本号为 1.0.0

## 更新版本

### 语义化版本

- **MAJOR.MINOR.PATCH** (例如：1.0.0)
- MAJOR: 不兼容的 API 变更
- MINOR: 向后兼容的功能新增
- PATCH: 向后兼容的问题修复

### 发布新版本

```bash
# 1. 更新版本号
# 编辑 _meta.json 和 clawhub.yaml

# 2. 提交更改
git add .
git commit -m "Bump version to 1.1.0"
git tag v1.1.0
git push origin main --tags

# 3. 发布到 ClawHub
clawhub publish --version 1.1.0

# 4. 创建 GitHub Release
# 在 GitHub 上基于 tag 创建 Release
```

## 推广

### 社交媒体

- Twitter/X: 发布技能链接和特性介绍
- Discord: OpenClaw 社区频道
- Reddit: r/opensource, r/automation

### 文档

- 更新 SKILL.md 使用例
- 添加视频教程（可选）
- 编写博客文章

## 维护

### 定期任务

- 每月检查依赖更新
- 每季度审查安全配置
- 响应用户问题和 PR
- 更新文档和示例

### 收集反馈

- GitHub Issues
- ClawHub 评论
- 社区反馈

---

*发布愉快！* 🚀
