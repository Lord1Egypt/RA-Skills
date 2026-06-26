# Cognitive Flexibility Skill 手动发布指南

**版本:** v2.1.0  
**创建时间:** 2026-04-05  
**状态:** ⚠️ 需要手动完成浏览器认证

---

## ⚠️ 发布说明

ClawHub 发布需要浏览器认证，由于当前环境无法打开浏览器，需要您手动完成以下步骤：

---

## 🚀 发布步骤

### 步骤 1: 打开 PowerShell

```powershell
# 进入发布目录
cd C:\Users\www31\.openclaw\workspace-optimizer\skills\cognitive-flexibility-release
```

### 步骤 2: 登录 ClawHub

```powershell
# 执行登录命令
clawhub login
```

**此时会：**
1. 自动打开默认浏览器
2. 跳转到 ClawHub 认证页面
3. 登录您的 ClawHub 账号
4. 授权 CLI 访问
5. 自动返回命令行

### 步骤 3: 验证登录

```powershell
# 检查登录状态
clawhub whoami
```

**预期输出:**
```
Logged in as: [your-username]
```

### 步骤 4: 发布 Skill

```powershell
# 发布到 ClawHub
clawhub publish . --slug cognitive-flexibility --version 2.1.0
```

**预期输出:**
```
Publishing cognitive-flexibility v2.1.0...
✓ Skill published successfully
URL: https://clawhub.com/skills/cognitive-flexibility
```

### 步骤 5: 验证发布

打开浏览器访问：
```
https://clawhub.com/skills/cognitive-flexibility
```

**检查:**
- [ ] Skill 页面正常显示
- [ ] 版本号为 2.1.0
- [ ] 文档完整
- [ ] 安装命令正确

---

## 🔑 备选方案：使用 Token 登录

如果浏览器认证失败，可以使用 Token 方式：

### 1. 获取 Token

1. 访问 https://clawhub.com/settings/tokens
2. 创建新的 CLI Token
3. 复制 Token

### 2. 使用 Token 登录

```powershell
# 方式 1: 命令行输入
clawhub auth token

# 方式 2: 环境变量
$env:CLAWHUB_TOKEN="your-token-here"
clawhub whoami
```

### 3. 发布 Skill

```powershell
clawhub publish . --slug cognitive-flexibility --version 2.1.0
```

---

## 📋 发布后验证

### 1. 检查 Skill 页面

```
https://clawhub.com/skills/cognitive-flexibility
```

**检查项:**
- [ ] 标题正确
- [ ] 版本号 2.1.0
- [ ] 描述完整
- [ ] 标签正确
- [ ] 安装命令正确

### 2. 测试安装

```powershell
# 在新目录测试安装
cd C:\temp
clawhub install cognitive-flexibility
cd cognitive-flexibility
python tests/test_cognitive_skills.py
```

**预期:** 测试通过率 100%

### 3. 分享社区

**分享渠道:**
- [ ] Discord #skills-release 频道
- [ ] GitHub Issues
- [ ] 邮件列表
- [ ] 社交媒体

---

## 📊 发布后监控

### 每日检查

```powershell
# 查看下载量（如果支持）
clawhub inspect cognitive-flexibility

# 查看评论
# 访问 https://clawhub.com/skills/cognitive-flexibility#comments
```

### 每周报告

**检查:**
- 下载量统计
- 用户评论
- GitHub Issues
- 使用监控数据

**更新:** `feedback/FEEDBACK-TRACKER.md`

---

## 🔗 相关链接

| 链接 | 说明 |
|------|------|
| **Skill 页面** | https://clawhub.com/skills/cognitive-flexibility |
| **ClawHub 设置** | https://clawhub.com/settings |
| **Token 管理** | https://clawhub.com/settings/tokens |
| **发布文档** | https://clawhub.com/docs/publishing |

---

## 📧 问题支持

如遇到问题：

1. **ClawHub 文档:** https://clawhub.com/docs
2. **GitHub Issues:** https://github.com/clawhub/cli/issues
3. **Discord 社区:** #support 频道

---

## ✅ 发布检查清单

- [ ] 打开 PowerShell
- [ ] 进入发布目录
- [ ] 执行 `clawhub login`
- [ ] 完成浏览器认证
- [ ] 验证登录 `clawhub whoami`
- [ ] 发布 Skill `clawhub publish . --slug cognitive-flexibility --version 2.1.0`
- [ ] 验证 Skill 页面
- [ ] 测试安装
- [ ] 分享到社区
- [ ] 设置反馈监控

---

_道师出品 · Cognitive Flexibility Skill 手动发布指南 v2.1_

**创建时间:** 2026-04-05  
**状态:** ⚠️ 等待用户手动完成浏览器认证
