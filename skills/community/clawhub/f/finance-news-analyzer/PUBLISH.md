# ClawHub Skill 发布配置

## 发布信息

- **Skill Slug**: `finance-news-analyzer`
- **Skill Name**: `财经新闻分析器`
- **Version**: `1.0.0`
- **Description**: 专业的财经新闻深度分析技能，支持 28+ 新闻源、10+ LLM 模型，提供情感分析、影响评估、图表生成、数据持久化等完整功能

## 发布步骤

### 1. 登录 ClawHub

```bash
clawhub login
```

这会打开浏览器让你登录 clawhub.com 账号。

### 2. 验证登录

```bash
clawhub whoami
```

### 3. 发布 Skill

```bash
cd skills/finance-news-analyzer
clawhub publish . --slug finance-news-analyzer --name "财经新闻分析器" --version 1.0.0 --changelog "初始版本：新闻抓取、情感分析、图表生成、数据持久化、定时任务"
```

### 4. 验证发布

```bash
clawhub inspect finance-news-analyzer
```

### 5. 更新版本（后续）

```bash
# 修改版本号后重新发布
clawhub publish . --slug finance-news-analyzer --version 1.1.0 --changelog "新增 XX 功能，优化 XX"
```

---

## 发布前检查清单

- [x] SKILL.md 文件存在且格式正确
- [x] name 和 description 字段完整
- [x] scripts/ 目录包含所有必要脚本
- [x] references/ 目录包含参考文档
- [x] templates/ 目录包含模板文件
- [x] requirements.txt 包含所有依赖
- [x] README.md 快速入门文档
- [x] 测试脚本可运行
- [ ] 已登录 ClawHub
- [ ] 已通过测试

---

## 手动发布命令

```bash
# 完整发布命令
clawhub publish ./skills/finance-news-analyzer \
  --slug finance-news-analyzer \
  --name "财经新闻分析器" \
  --version 1.0.0 \
  --changelog "初始版本：支持 28+ 新闻源、10+ LLM 模型、情感分析、图表生成、数据持久化、定时任务"
```

---

## 发布后

### 安装链接
```
https://clawhub.com/skills/finance-news-analyzer
```

### 安装命令
```bash
clawhub install finance-news-analyzer
```

### 更新命令
```bash
clawhub update finance-news-analyzer
```

---

## 注意事项

1. **版本号规范**: 遵循语义化版本 (SemVer)
   - `1.0.0` - 初始版本
   - `1.0.1` - Bug 修复
   - `1.1.0` - 新功能
   - `2.0.0` - 重大更新

2. **Changelog 写法**: 简洁描述变更内容
   - 新增功能用"新增"
   - 修复问题用"修复"
   - 性能优化用"优化"

3. **更新频率**: 建议定期更新
   - Bug 修复及时发布
   - 新功能累积到一定数量发布
   - 重大更新单独发布大版本

---

## 故障排查

### 问题 1: 发布失败 - 权限不足
```bash
# 重新登录
clawhub logout
clawhub login
```

### 问题 2: Slug 已被占用
```bash
# 检查是否已发布
clawhub inspect finance-news-analyzer

# 如果已被占用，使用不同的 slug
clawhub publish . --slug finance-news-analyzer-pro
```

### 问题 3: 文件大小超限
```bash
# 检查文件大小
ls -lh reports/
# 删除大文件
rm reports/*.png
```

---

**准备就绪后执行发布命令即可！** 🚀
