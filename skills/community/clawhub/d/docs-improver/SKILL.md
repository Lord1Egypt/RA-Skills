---
name: docs-improver
description: 专业技术文档提升工具。评估文档质量（完整性、准确性、清晰度、结构化、可维护性），自动生成缺失文档（README、API 文档），检查文档与代码一致性，提供可执行的改进建议。使用场景：文档质量审计、缺失文档生成、文档一致性检查、文档改进规划、新项目文档搭建、发布前检查。支持所有编程语言。
---

# Docs Improver - 技术文档专家

专业的技术文档分析、生成和改进工具。

## 快速开始

```bash
# 完整流程：分析 + 生成 + 检查 + 改进
python3 scripts/docs-improver.py --path /path/to/project --mode all --report report.md

# 仅质量评估
python3 scripts/analyze.py --path /path/to/project --output quality.md

# 仅文档生成
python3 scripts/generate.py --path /path/to/project --type readme

# 仅一致性检查
python3 scripts/consistency-check.py --path /path/to/project --output issues.md

# 仅改进建议
python3 scripts/improve.py --path /path/to/project --output plan.md
```

## 核心功能

### 📊 文档质量评估

| 维度 | 说明 |
|------|------|
| **完整性** | 覆盖关键内容（30% 权重） |
| **清晰度** | 易读易懂（25% 权重） |
| **结构化** | 组织清晰（20% 权重） |
| **可维护性** | 易于更新（15% 权重） |
| **准确性** | 与代码一致（10% 权重） |

### 📝 文档生成

| 文档类型 | 说明 |
|----------|------|
| **README.md** | 项目概述和快速开始 |
| **API.md** | API 接口文档 |
| **ARCHITECTURE.md** | 架构设计文档 |
| **INSTALL.md** | 安装部署指南 |
| **CONTRIBUTING.md** | 贡献指南 |
| **CHANGELOG.md** | 变更日志 |

### 🔍 一致性检查

- API 文档 vs 实际接口
- 示例代码 vs 实际代码
- 架构图 vs 实际架构
- 配置说明 vs 实际配置
- 链接有效性检查

### 💡 改进建议

| 优先级 | 时间 | 说明 |
|--------|------|------|
| **快速获胜** | 几小时 | 立即可改的小问题 |
| **短期** | 几天 | 需要一定工作量 |
| **长期** | 几周 | 系统性改进 |

## 输出示例

### 质量评估报告

```markdown
# 文档质量评估报告

## 总体评分：88/100 ✅

| 维度 | 评分 | 状态 |
|------|------|------|
| 完整性 | 80/100 | ✅ 良好 |
| 清晰度 | 100/100 | ✅ 优秀 |
| 结构化 | 85/100 | ✅ 良好 |
| 可维护性 | 100/100 | ✅ 优秀 |

## 改进建议

### 快速获胜（几小时）
- [ ] 添加项目描述和徽章
- [ ] 添加代码示例

### 短期（几天）
- [ ] 创建 API 文档
- [ ] 添加架构图

### 长期（几周）
- [ ] 建立自动化文档生成
- [ ] 建立文档审查流程
```

### 一致性问题

```markdown
# 一致性检查报告

## 发现问题：5 个

### 严重 (1)
1. API 端点 /api/users 存在于代码但未文档化

### 主要 (2)
1. README 中的示例代码使用了过时的 API
2. 架构图缺少新增的微服务

### 次要 (2)
1. 3 个外部链接失效
2. 术语不统一（用户/客户混用）
```

## 使用场景

### 1. 文档质量审计
```bash
python3 scripts/analyze.py --path . --output audit.md
```

**适用：**
- 接手新项目
- 准备发布
- 季度文档审查

### 2. 生成缺失文档
```bash
python3 scripts/generate.py --path . --output ./docs
```

**适用：**
- 新项目启动
- 准备开源
- 新成员入职

### 3. 发布前检查
```bash
python3 scripts/consistency-check.py --path . --output check.md
```

**适用：**
- 重大发布前
- 大重构后
- API 变更后

### 4. 完整文档 overhaul
```bash
python3 scripts/docs-improver.py --path . --mode all --output ./docs --report report.md
```

**适用：**
- 文档严重过时
- 新项目文档搭建
- 技术债务冲刺

## 文档模板

包含 6+ 专业模板：

- README.md 模板
- API.md 模板
- ARCHITECTURE.md 模板
- CONTRIBUTING.md 模板
- CHANGELOG.md 模板
- ADR（架构决策记录）模板

## Mermaid 图表模板

包含 10+ 图表模板：

- 系统架构图
- 微服务架构
- 分层架构
- 事件驱动架构
- 流程图
- 序列图
- 类图
- 状态图
- ER 图
- 甘特图

## 与 AI 助手配合

**Claude/Codex:**
```
"评估我们的文档质量并提出改进建议"
```

AI 会：
1. 运行 docs-improver
2. 解读质量报告
3. 生成具体改进计划
4. 帮助实施建议

## 最佳实践

详见 [references/best-practices.md](references/best-practices.md)：
- 文档写作风格指南
- 技术文档最佳实践
- 模板使用指南
- 图表绘制规范

## 参见

- [文档模板](scripts/templates/)
- [Mermaid 图表](assets/diagrams/)
- [OpenClaw 文档](https://docs.openclaw.ai)
