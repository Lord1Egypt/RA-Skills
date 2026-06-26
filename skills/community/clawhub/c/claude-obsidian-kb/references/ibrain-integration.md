# Claude-Obsidian × iBrain 整合方案

---

## 架构映射

| Claude-Obsidian | iBrain 对应物 | 说明 |
|----------------|-------------|------|
| Vault | iBrain 数据库 | 持久化知识存储 |
| `raw/` | 来源管理（Sources）| 原始素材 |
| `wiki/` | 卡片库（Cards）| 结构化知识 |
| `output/` | 报告生成 | AI 产出 |
| `CLAUDE.md` | AI行为定义文件 | 角色+规范 |
| `SCHEMA.md` | schema.json | 数据规范 |
| 双向链接 | 实体关系图谱（Neo4j）| 关系建模 |
| 孤儿笔记 | 游离实体 | 无关联的知识碎片 |

---

## 整合优先级

### P0 — 立即可迁移（无需改 iBrain 架构）
- ✅ frontmatter 模板 → iBrain 卡片字段
- ✅ 三层架构 → iBrain 的 Source/Card/Output 分层
- ✅ 命名规范 + 标签体系 → iBrain schema

### P1 — 需要扩展 iBrain
- 🔄 双向链接 → iBrain 实体关系图（Neo4j已有，可对接）
- 🔄 `[!contradiction]` → iBrain 矛盾标记系统
- 🔄 孤儿笔记检测 → 图谱分析查询

### P2 — 深度功能
- 🔄 `/wiki` `/save` 命令 → iBrain CLI 工具
- 🔄 热缓存 → iBrain session memory
- 🔄 `/autoresearch` → iBrain Research Agent

---

## frontmatter → iBrain 卡片字段 映射

```yaml
# Claude-Obsidian frontmatter
title: "神经网络"
type: "concept"
tags: ["AI", "机器学习"]
sources: ["https://arxiv.org/abs/xxx"]
created: "2026-04-21"
updated: "2026-04-21"
summary: "受人脑启发的计算模型"

# iBrain Card (对应)
{
  "title": "神经网络",
  "type": "concept",      // concept | entity | topic
  "tags": ["AI", "机器学习"],
  "sources": [...],       // 来源列表
  "summary": "受人脑启发的计算模型",
  "links": [],            // 关联卡片ID列表（新增）
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 整合路径建议

**阶段1（当前）**：将 Claude-Obsidian 方法论以 skill 形式存在
→ iBrain 开发时作为参考规范

**阶段2（iBrain Phase 3）**：将 wiki 引擎整合进 iBrain
→ Source → AI处理 → Card 自动生成 + 关系建立

**阶段3（未来）**：iBrain 成为 Claude-Obsidian 的完整替代
→ 云端 Vault + 多模型支持 + 自动织网
