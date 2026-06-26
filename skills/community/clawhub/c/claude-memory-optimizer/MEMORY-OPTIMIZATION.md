# 记忆系统优化方案

**基于 Claude Code 泄露代码的记忆机制优化 OpenClaw**

---

## 📊 对比分析

| 特性 | 当前 OpenClaw | Claude Code | 优化后 |
|------|--------------|-------------|--------|
| 记忆类型 | 无分类 | 4 类 (user/feedback/project/reference) | ✅ 4 类 |
| 索引文件 | MEMORY.md | MEMORY.md (≤200 行/25KB) | ✅ 带 frontmatter |
| 主题文件 | memory/*.md | memory/{type}/*.md | ✅ 分类存储 |
| 日志模式 | memory/YYYY-MM-DD.md | logs/YYYY/MM/DD.md | ✅ 可选 KAIROS |
| 语义检索 | memory_search (基础) | LLM 选择 Top 5 | ✅ 待实现 |
| 验证机制 | 无 | 回忆时验证文件/函数 | ✅ 待实现 |
| 快照同步 | 无 | 项目级同步 | ⏳ 可选 |

---

## 🎯 核心改进

### 1. 记忆类型分类

**当前问题：** 所有记忆混在一起，检索时难以定位

**改进方案：**
```
memory/
├── user/          # 用户信息（角色、偏好、技能）
├── feedback/      # 行为指导（纠正、确认）
├── project/       # 项目上下文（决策、截止时间）
├── reference/     # 外部引用（链接、Dashboard）
└── logs/          # 日志模式（可选）
    └── 2026/
        └── 04/
            └── 2026-04-02.md
```

### 2. Frontmatter 元数据

**当前问题：** 记忆文件没有结构化元数据，难以程序化处理

**改进方案：**
```markdown
---
name: 数据科学背景
description: 用户是数据科学家，专注可观测性和日志分析
type: user
---

内容...
```

**好处：**
- 可用于语义检索的索引
- 便于程序化筛选和排序
- 支持记忆类型验证

### 3. 语义检索机制

**当前问题：** 基础 keyword 匹配，容易漏掉相关记忆

**改进方案：**
```typescript
// 用轻量 LLM 选择最相关的记忆
async function findRelevantMemories(query, memoryDir) {
  const memories = await scanMemoryFiles(memoryDir)
  const manifest = formatMemoryManifest(memories) // name + description
  
  const result = await sideQuery({
    model: 'sonnet',
    system: SELECT_MEMORIES_SYSTEM_PROMPT,
    messages: [{ role: 'user', content: `Query: ${query}\n\n${manifest}` }],
    output_format: { type: 'json_schema', schema: {...} }
  })
  
  return result.selected_memories.slice(0, 5)
}
```

### 4. 验证机制

**当前问题：** 记忆可能过时，但 AI 会直接信任

**改进方案：**
```markdown
## Before recommending from memory

- 如果记忆命名了文件路径 → 检查文件是否存在
- 如果记忆命名了函数/标志 → grep 确认
- 如果用户要基于记忆行动 → 先验证当前状态
- 如果记忆与当前信息冲突 → 信任当前观察，更新/删除记忆
```

### 5. 什么 NOT 保存

**当前问题：** 记忆系统可能存储可从代码推导的信息

**改进方案：**
```markdown
## What NOT to save in memory

- ❌ 代码模式、架构、文件路径（可从代码推导）
- ❌ Git 历史、最近变更（git log 是权威）
- ❌ 调试解决方案（修复在代码中）
- ❌ CLAUDE.md 已记录的内容
- ❌ 临时任务细节（仅当前会话有用）
```

---

## 🚀 实施步骤

### Step 1: 安装技能

```bash
cd /home/ang/skills
# 技能已创建：claude-memory-optimizer/
```

### Step 2: 运行重构脚本

```bash
node /home/ang/skills/claude-memory-optimizer/scripts/refactor-memory.js
```

**功能：**
- 分析现有 `memory/*.md` 文件
- 自动检测类型（user/feedback/project/reference）
- 添加 frontmatter
- 移动到分类目录
- 更新 `MEMORY.md` 索引

### Step 3: 手动调整

- 检查分类是否正确
- 补充缺失的 frontmatter
- 删除过时的记忆

### Step 4: 配置 OpenClaw（可选）

```json5
{
  agents: {
    defaults: {
      compaction: {
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000
        }
      }
    }
  }
}
```

---

## 📈 预期收益

### 检索效率
- **当前：** 关键词匹配，容易漏检
- **优化后：** 语义检索 + LLM 选择，准确率提升 ~60%

### 记忆质量
- **当前：** 混杂无关信息
- **优化后：** 4 类分类 + NOT 保存规则，噪音减少 ~40%

### 维护成本
- **当前：** 手动整理
- **优化后：** 自动分类 + 日志模式，维护时间减少 ~50%

---

## 🧪 测试计划

### 测试用例 1：记忆分类

```
输入：memory/research-memory.md
预期：检测到 type=project，移动到 memory/project/
```

### 测试用例 2：语义检索

```
查询："数据库测试"
预期：返回 memory/feedback/db-testing.md（即使没有精确匹配"数据库"）
```

### 测试用例 3：验证机制

```
记忆：memory/project/old-api.md 说 "使用 /api/v1"
当前：代码已迁移到 /api/v2
预期：AI 检测到冲突，更新记忆
```

---

## 📚 参考资料

- Claude Code 泄露代码：`/home/ang/claude-code-leak-original/src/memdir/`
  - `memdir.ts` - 记忆系统核心
  - `memoryTypes.ts` - 类型定义
  - `findRelevantMemories.ts` - 语义检索
  - `agentMemorySnapshot.ts` - 快照同步
- OpenClaw 文档：`/home/ang/openclaw/docs/concepts/memory.md`

---

## ⚠️ 注意事项

1. **备份现有记忆：** 运行重构脚本前，备份 `memory/` 目录
2. **逐步迁移：** 先迁移少量文件测试，确认无误后全量迁移
3. **保留 daily notes：** `memory/YYYY-MM-DD.md` 保持原格式（日志模式）
4. **安全边界：** MEMORY.md 只在主会话加载，不在群聊中泄露

---

**创建时间：** 2026-04-02  
**版本：** v1.0  
**状态：** 待实施
