# Example: Decision-Oriented Conclusion Document

**Date**: 2026-05-21
**Topic**: 圆桌讨论内置 Web 查让没有自定义 channel 的用户也能查看讨论详情
**Participants**: 饼哥(产品), 像素姐(设计), 码飞(开发), coordinator
**Rounds**: 3
**Discussion ID**: rt_xxxxxxxx

## Key Pattern: Decision-Oriented Conclusion

For product/design/dev discussions aimed at making build decisions, the conclusion doc should go beyond listing consensus/disagreement — it should be a **ready-to-execute specification** with:

1. **MVP Feature Checklist** — numbered, with clear scope (P0 = do, P1 = later)
2. **Technical Architecture** — ASCII diagram + file structure + API table
3. **Acceptance Criteria** — measurable, with specific numbers (≤3s, ≥20 concurrent)
4. **Risk Table** — risk + mitigation, one row each
5. **Design Deliverables** — what the designer needs to hand off
6. **Timeline with Milestones** — who does what, when, with buffer

## Example Conclusion Structure

```markdown
# 圆桌讨论结论：[主题]

## 摘要
- **参与者**：角色1（职位）、角色2（职位）、角色3（职位）
- **轮次**：N 轮
- **日期**：YYYY-MM-DD
- **讨论 ID**：rt_xxxxxxxx

## 共识点
1. [Point 1]
2. [Point 2]

## 分歧点
无阻塞性分歧。[或 list specific disagreements]

## 决策

### MVP 功能清单（P0）

| # | 功能 | 说明 |
|---|------|------|
| 1 | [Feature] | [Brief description] |
| 2 | ... | ... |

### 技术架构
```
[ASCII architecture diagram]
```

### 文件结构
```
[project tree]
```

### API 接口（if applicable）

| 路径 | 方法 | 说明 |
|------|------|------|
| ... | ... | ... |

### 验收标准

| 项目 | 标准 |
|------|------|
| 性能 | ≤ Xs / ≥ Y concurrent |
| 兼容性 | [specific browsers/devices] |
| 安全 | [specific requirements] |

### 风险提示

1. **[风险名]**：[缓解措施]
2. ...

### 设计交付物（if designer involved）

1. CSS 变量表
2. 状态原型 × N
3. 组件规范
4. ...

## 行动项

1. **[角色]**：[任务] — [工期]
2. ...

## 详细讨论记录
完整讨论记录见圆桌讨论系统（ID: rt_xxxxxxxx）
```

## Tips

- Write the conclusion doc BEFORE calling `roundtable_end`
- Use `roundtable_summarize` to get structured data, but the doc should be BETTER than raw data
- Include the discussion_id so readers can find the full transcript
- For technical discussions, include actual code snippets and architecture diagrams from the discussion
- Make acceptance criteria measurable — avoid vague "should be fast"
