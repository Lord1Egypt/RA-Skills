# 碎片元数据字段说明

## 必填字段

| 字段 | 说明 | 示例 |
|-----|------|------|
| created | 创建时间ISO格式 | 2024-01-15T10:30:00 |
| source | 来源类型 | wechat/webchat/doc/meeting/manual |
| tags | 主题标签列表 | ["AI", "产品", "增长"] |

## 可选字段

| 字段 | 说明 | 示例 |
|-----|------|------|
| title | 碎片标题 | "AI安全的三个层次" |
| author | 作者/发言人 | "张三" or "Sam Altman" |
| related | 关联碎片ID列表 | ["2024-01-10-xxx", "2024-01-12-yyy"] |
| status | 处理状态 | new/reviewed/connected/archived |

## 碎片文件命名规范

```
YYYY-MM-DD-[hash8]-[主题].md
示例: 2024-01-15-a1b2c3d4-AI安全.md
```

## 连接笔记模板

```markdown
---
type: connection
created: 2024-01-15T10:30:00
source_frag: 2024-01-15-a1b2c3d4-AI安全.md
related_frags:
  - 2024-01-10-e5f6g7h8-模型对齐.md
  - 2024-01-12-i9j0k1l2-AGI.md
connection_type: concept_similar
---

# 知识连接

## 关联点
[说明这条碎片和已有知识的关联]

## 原文摘录
> 相关原文摘录
```

## 大纲草案模板

```markdown
---
type: outline
theme: [主题名称]
fragments_count: 5
created: 2024-01-15T10:30:00
---

# [主题名称] 大纲草案

## 已收集要点
1. [要点1 - 来源]
2. [要点2 - 来源]

## 建议结构

### 第一章: [章节名]
- 核心观点
- 支撑素材

### 第二章: [章节名]
- 核心观点
- 支撑素材

## 待补充信息
- [ ] 缺失的关键信息1
- [ ] 缺失的关键信息2

## 下一步行动
- [ ] 补充XX素材
- [ ] 与XX讨论确认
```
