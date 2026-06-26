# Memory System 🧠

> 完整记忆系统 - 四类记忆分类 + Feedback 双向记录

## 安装

```bash
clawhub install memory-system
```

## 核心特性

- 📁 **文件系统存储** - 纯 Markdown，无数据库依赖
- 🔍 **语义搜索** - 支持 Ollama 向量搜索
- ⚡ **自动加载** - 会话启动时自动就位
- 💾 **智能 Flush** - 上下文接近阈值时自动保存
- 📝 **四类记忆** - User / Feedback / Project / Reference
- 🔄 **双向反馈** - 纠正和确认同等重要

## 四类记忆

| 类型 | 作用域 | 用途 |
|------|--------|------|
| User | 私密 | 用户角色、偏好、知识背景 |
| Feedback | 私密/团队 | 用户的纠正和确认 |
| Project | 团队 | 项目进展、目标、决策 |
| Reference | 团队 | 外部系统资源指针 |

## Feedback 双向记录

Feedback 不仅要记录"不要做什么"，也要记录"什么做对了"：

```markdown
### 不要mock数据库
**Type:** negative
**Why:** 上一季度mock测试通过了但生产迁移失败
**How to apply:** 集成测试必须用真实数据库

### 接受单PR而非多个小PR
**Type:** positive
**Why:** 拆分反而造成不必要的开销
**How to apply:** 重构类需求优先合并为大PR
```

## 快速开始

```bash
# 安装
clawhub install memory-system

# 使用
# 了解用户信息 → 保存到 user 类型
# 收到反馈 → 保存到 feedback 类型
# 了解项目动态 → 保存到 project 类型
# 发现外部资源 → 保存到 reference 类型
```

## 文档

- [SKILL.md](./SKILL.md) - 完整技能说明
- [PRODUCT.md](./PRODUCT.md) - 产品说明文档
- [CHANGELOG.md](./CHANGELOG.md) - 更新日志

## 版本

**当前版本**：1.1.0  
**更新内容**：引入四类记忆分类 + Feedback 双向记录

---

**作者**：团宝 (openclaw)
