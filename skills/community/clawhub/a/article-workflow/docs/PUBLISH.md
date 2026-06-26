# 📦 发布到 ClawHub

## 发布状态

**当前状态：** ✅ 已发布

**发布时间：** 2026-03-14 12:15

**ClawHub Slug:** article-workflow

**版本:** 1.0.0

**GitHub 仓库:** https://github.com/dongnan/article-workflow

---

## 手动发布步骤

当遇到 GitHub API 限流时，可以稍后重试：

```bash
# 1. 确保已登录
clawhub whoami

# 2. 等待几分钟后重试发布
cd /Users/dongnan/.openclaw/workspace
clawhub publish skills/article-workflow \
  --slug "article-workflow" \
  --name "Article Workflow" \
  --version "1.0.0" \
  --changelog "初始发布 - 文章分析工作流完整功能"

# 3. 验证发布
clawhub search article-workflow
```

---

## 发布配置

### package.json

```json
{
  "name": "article-workflow",
  "version": "1.0.0",
  "description": "文章分析工作流自动化 Skill",
  "author": "dongnan",
  "license": "MIT",
  "keywords": ["article", "workflow", "analysis", "feishu", "bitable"],
  "repository": {
    "type": "git",
    "url": "https://gitlab.idongnan.cn/openclaw/workspace.git",
    "directory": "skills/article-workflow"
  }
}
```

### 发布参数

| 参数 | 值 | 说明 |
|------|-----|------|
| **slug** | article-workflow | Skill 唯一标识 |
| **name** | Article Workflow | 显示名称 |
| **version** | 1.0.0 | 版本号（semver） |
| **changelog** | 初始发布... | 更新日志 |

---

## 发布后验证

### 1. 搜索 Skill

```bash
clawhub search article-workflow
```

### 2. 查看详情

```bash
clawhub inspect article-workflow
```

### 3. 安装测试

```bash
# 在另一个工作区
clawhub install article-workflow
```

---

## 更新发布

当有更新时：

```bash
# 1. 更新版本号（package.json）
# 1.0.0 → 1.0.1

# 2. 发布新版本
clawhub publish skills/article-workflow \
  --slug "article-workflow" \
  --version "1.0.1" \
  --changelog "修复：xxx 问题"

# 3. 验证
clawhub inspect article-workflow@1.0.1
```

---

## 常见问题

### Q: GitHub API 限流

**错误信息：**
```
✖ GitHub API rate limit exceeded — please try again in a few minutes
```

**解决方案：**
- 等待 5-10 分钟后重试
- 或使用已登录的会话（避免重复认证）

### Q: SKILL.md required

**错误信息：**
```
Error: SKILL.md required
```

**解决方案：**
- 确保 SKILL.md 文件存在
- 确保 .gitignore 没有忽略 SKILL.md

### Q: Path must be a folder

**错误信息：**
```
Error: Path must be a folder
```

**解决方案：**
- 确保发布的是目录路径，不是文件
- 使用完整路径：`clawhub publish /path/to/skill`

---

## 发布历史

| 版本 | 发布日期 | 说明 |
|------|---------|------|
| 1.0.0 | 待发布 | 初始版本 |

---

*最后更新：2026-03-14*
