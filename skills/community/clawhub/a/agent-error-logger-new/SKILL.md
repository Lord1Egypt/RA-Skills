---
name: agent-error-logger
description: |
  Agent 错误日志工具。记录、检索和分析 Agent 犯过的错误，避免重复踩坑。
  支持自动记录任务失败、手动查询错误模式、生成修正建议。
metadata:
  trigger: 记录错误、查询错误、错误分析、避免踩坑
  author: 苏冠超
  version: 1.0.0
---

# Agent Error Logger

记录 Agent 犯过的错误，避免重复踩坑。

## 功能

- **自动记录**: 任务失败时自动记录错误详情
- **模式识别**: 识别重复出现的错误模式
- **主动提醒**: 新任务前检索相似错误，提前预警
- **统计分析**: 按月/类型统计错误分布

## 文件结构

```
workspace/memory/
├── error-patterns.md       # 错误模式索引（长期）
└── error-log-YYYY-MM.md    # 月度详细日志
```

## 使用方式

### 1. 记录错误

```markdown
用户：记录一个错误，刚才发布小红书失败了

Agent: 好的，请告诉我：
1. 任务是什么？
2. 具体错误是什么？
3. 原因是什么？
4. 怎么修正的？

或者我帮你从对话中提取这些信息？
```

### 2. 查询错误

```markdown
用户：查一下之前发布失败的错误
用户：有没有类似的文件校验错误？
用户：显示所有 #网络超时 的错误
```

### 3. 主动提醒

```markdown
Agent: 等一下，我查一下错误日志...
上次发布小红书失败是因为图片文件不存在。
这次请确认：
✓ 图片文件路径是否正确
✓ 如果是 URL，需要先下载
✓ 文件权限是否可读
```

## 错误记录格式

```markdown
### 错误 #XXX - 简短描述
- **时间**: YYYY-MM-DD HH:MM
- **任务**: 任务描述
- **错误**: 具体错误信息
- **原因**: 根本原因分析
- **修正**: 修正方案
- **模式标签**: #标签 1 #标签 2
- **相似错误**: 关联的错误编号
```

## 模式标签

| 标签 | 描述 | 检查清单 |
|------|------|----------|
| #文件校验 | 文件/路径未校验 | 文件存在、路径正确、权限足够 |
| #网络超时 | 网络请求超时 | 设置 timeout、重试机制、降级方案 |
| #浏览器不可用 | 浏览器工具失败 | 替代方案、合理超时、降级逻辑 |
| #权限不足 | API/文件权限问题 | 检查授权、权限范围 |
| #参数缺失 | 必需参数未提供 | 参数清单、默认值、用户确认 |

## 脚本工具

### record-error.sh

记录新错误：

```bash
cd /path/to/agent-error-logger/scripts
python record_error.py \
  --task "发布内容失败" \
  --error "图片文件不存在" \
  --cause "用户只提供了 URL，未下载" \
  --fix "发布前先下载 URL 图片" \
  --tags "#文件校验 #图片处理"
```

### search-errors.sh

查询错误：

```bash
python search_errors.py --tag "#文件校验" --limit 5
python search_errors.py --keyword "关键词" --limit 10
```

### monthly-report.sh

生成月度报告：

```bash
python monthly_report.py --month YYYY-MM --output markdown
```

## 主动检查清单

在以下场景自动检索错误日志：

| 场景 | 检查内容 |
|------|----------|
| 发布内容前 | 检查 #文件校验 #发布前检查 |
| 网络请求前 | 检查 #网络超时 #降级方案 |
| 浏览器操作前 | 检查 #浏览器不可用 |
| 复杂任务前 | 检查相似任务的错误历史 |

## 最佳实践

1. **及时记录**: 错误发生后立即记录，细节更准确
2. **详细分析**: 不仅记录现象，还要分析根本原因
3. **标签规范**: 使用统一标签，便于检索
4. **定期回顾**: 每月回顾错误模式，更新检查清单
5. **主动提醒**: 新任务前主动检索，避免重复错误

## 扩展建议

- [ ] 自动从对话中提取错误信息
- [ ] 错误相似度计算（向量检索）
- [ ] 错误趋势分析（图表）
- [ ] 集成到 HEARTBEAT 自检
- [ ] 多 Agent 共享错误库

## 相关资源

- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- [CoVE: Chain of Verification](https://arxiv.org/abs/2309.11495)
- [AgentDropoutV2: Dynamic Error Handling](https://github.com/)
