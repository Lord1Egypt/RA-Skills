---
name: memory-curator
description: "记忆整理技能 — 审查结构化记忆，提取洞察，更新 MEMORY.md，清理过期条目。"
homepage: https://github.com/jobzhao15/openclaw-enhance
metadata: { "openclaw": { "emoji": "🧠", "requires": { "bins": [] } } }
---

# 记忆整理 (Memory Curator)

定期整理和优化结构化记忆系统。

## 使用时机

✅ **使用此技能当：**
- "整理一下记忆"、"清理过期记忆"
- 定期维护（建议每周一次）
- 记忆条目数量过多需要精简
- 需要从记忆中提取总结更新到 MEMORY.md

## 整理流程

### 1. 审查当前状态
```
调用 enhance_memory_review action=stats 查看各类别统计
调用 enhance_memory_review action=recent limit=30 查看最近记忆
```

### 2. 清理过期/无效记忆
检查每条记忆是否仍然有效：
- **project 类**: 项目状态可能已变化，验证后决定保留或删除
- **feedback 类**: 用户反馈通常长期有效，谨慎删除
- **user 类**: 用户信息通常稳定，少量更新
- **reference 类**: 链接/资源可能已过期，检查后决定
- **decision 类**: 决策通常长期有效，除非被推翻

```
调用 enhance_memory_review action=delete id=<过期记忆ID>
```

### 3. 合并重复记忆
如果多条记忆说的是同一件事：
1. 创建一条更完整的合并记忆
2. 删除旧的重复条目

### 4. 同步到 MEMORY.md
将最重要的结构化记忆摘要写入 MEMORY.md：
- 只写长期有效、高重要性的内容
- 按类别组织
- 保持简洁

### 5. 输出整理报告

```
## 记忆整理报告

### 统计
- 整理前: XX 条
- 删除: X 条（原因: ...）
- 合并: X 条 → X 条
- 新增: X 条
- 整理后: XX 条

### 操作记录
1. 删除 #12: 过期的项目截止日期
2. 合并 #15 + #18 → #23: 用户偏好
3. ...

### MEMORY.md 更新
[是否更新了 MEMORY.md，更新了什么]
```

## 核心原则
- **保守删除** — 不确定就保留，宁多勿少
- **feedback 最珍贵** — 用户反馈是最难重新获取的记忆类型
- **验证后再删** — 对 project 类记忆，先确认项目状态再决定
- **MEMORY.md 是精华** — 只把最重要的同步过去，不要全量复制
