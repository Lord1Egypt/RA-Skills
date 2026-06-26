# ADD v7.23: 异步质量审核机制

**版本**: v7.23.0  
**日期**: 2026-03-13  
**问题**: 审核是否可以在创作过程中同步进行  
**方案**: 异步并行审核机制  
**方法**: 第一性原理 + 思维链 + MECE 拆解 + 自我校验

---

## 🎯 第一性原理分析

### 审核的本质
```
审核 = 质量检查 + 问题反馈 + 修正建议

核心问题：
1. 审核何时开始？→ 有内容可审时
2. 审核是否阻塞？→ 不应阻塞创作
3. 审核粒度？→ 单章审核 + 批量审核

核心洞察：
审核应该异步并行，而不是串行等待。
创作完成第 N 章 → 立即触发第 N 章审核
审核与创作并行进行
```

### 依赖关系分析
```
传统串行模式：
创作第 1 章 → 创作第 2 章 → ... → 创作第 10 章 → 审核第 1-10 章
总时间：10 章创作 + 10 章审核 = 20 单位时间

异步并行模式：
创作第 1 章 → 创作第 2 章 → ... → 创作第 10 章
    ↓           ↓                    ↓
审核第 1 章   审核第 2 章          审核第 10 章
总时间：max(10 章创作，10 章审核) = 10 单位时间

效率提升：50%
```

---

## 📐 MECE 拆解

### 维度 1: 审核时机

| 审核类型 | 触发条件 | 优点 | 缺点 |
|----------|----------|------|------|
| **单章审核** | 每章正文完成后 | 及时发现问题 | 审核频繁 |
| **批量审核** | 每 N 章完成后 | 减少审核次数 | 问题发现延迟 |
| **混合审核** | 单章 + 批量 | 平衡及时性和效率 | 复杂度较高 |

### 维度 2: 审核内容

| 审核类型 | 检查内容 | 执行 Agent |
|----------|----------|------------|
| **L1 单章审查** | 字数/格式/基础逻辑 | novel_editor |
| **L2 单元审查** | 情节连贯/伏笔 | novel_editor |
| **L3 质量审查** | 整体质量/文笔 | editor_in_chief |

### 维度 3: 依赖关系

| 任务类型 | 依赖 | 是否阻塞 |
|----------|------|----------|
| **单章审核** | 本章正文完成 | ❌ 不阻塞后续创作 |
| **批量审核** | N 章正文完成 | ❌ 不阻塞后续创作 |
| **最终审查** | 全部完成 | ✅ 阻塞发布 |

---

## 🔧 实施方案

### 方案 1: 单章异步审核（推荐）

**触发机制**:
```javascript
// 正文任务完成后
onTaskComplete('chapter-N-writing') {
  // 立即触发单章审核
  triggerTask(`chapter-N-review-l1`);
  
  // 如果是第 10 章，触发批量审核
  if (N % 10 === 0) {
    triggerTask(`chapter-${N-9}-${N}-review-l2`);
  }
}
```

**依赖配置**:
```json
{
  "chapter-1-review-l1": ["chapter-1-writing"],
  "chapter-2-review-l1": ["chapter-2-writing"],
  "chapter-1-10-review-l2": [
    "chapter-1-writing", "chapter-2-writing", ..., "chapter-10-writing"
  ]
}
```

---

### 方案 2: 批量异步审核

**触发机制**:
```javascript
// 每完成 10 章正文
if (completedWritingCount % 10 === 0) {
  const start = completedWritingCount - 9;
  const end = completedWritingCount;
  triggerTask(`chapter-${start}-${end}-review-l2`);
}
```

---

### 方案 3: 混合审核（最优）

**配置**:
```javascript
const REVIEW_CONFIG = {
  // 单章 L1 审核（每章完成后立即进行）
  l1Review: {
    enabled: true,
    trigger: 'per-chapter',
    agent: 'novel_editor'
  },
  
  // 批量 L2 审核（每 10 章进行一次）
  l2Review: {
    enabled: true,
    trigger: 'per-10-chapters',
    agent: 'novel_editor'
  },
  
  // 最终 L3 审核（全部完成后进行）
  l3Review: {
    enabled: true,
    trigger: 'after-all-complete',
    agent: 'editor_in_chief'
  }
};
```

---

## 🔧 实施步骤

### Step 1: 更新任务依赖配置

**文件**: `.task-dependencies.json`

**新增审核任务**:
```json
{
  "chapter-1-review-l1": ["chapter-1-writing"],
  "chapter-2-review-l1": ["chapter-2-writing"],
  ...
  "chapter-1-10-review-l2": [
    "chapter-1-writing", "chapter-2-writing", ..., "chapter-10-writing"
  ],
  "chapter-1-100-review-l3": [
    "chapter-1-writing", ..., "chapter-100-writing"
  ]
}
```

---

### Step 2: 更新任务状态初始化

**文件**: `task-generator.js`

**新增审核任务生成**:
```javascript
// 生成审核任务
for (let i = 1; i <= totalChapters; i++) {
  // L1 单章审核
  state[`chapter-${i}-review-l1`] = {
    status: 'pending',
    agent: agents.editor || 'novel_editor',
    description: `第${i}章 L1 审查（字数/格式/基础逻辑）`,
    dependsOn: [`chapter-${i}-writing`]
  };
  
  // L2 批量审核（每 10 章）
  if (i % 10 === 0) {
    const start = i - 9;
    state[`chapter-${start}-${i}-review-l2`] = {
      status: 'pending',
      agent: agents.editor || 'novel_editor',
      description: `第${start}-${i}章 L2 审查（情节连贯/伏笔）`,
      dependsOn: Array.from({length: 10}, (_, j) => `chapter-${start+j}-writing`)
    };
  }
}

// L3 最终审查
state[`chapter-1-${totalChapters}-review-l3`] = {
  status: 'pending',
  agent: agents.chiefEditor || 'editor_in_chief',
  description: `全书 L3 审查（整体质量/文笔）`,
  dependsOn: Array.from({length: totalChapters}, (_, i) => `chapter-${i+1}-writing`)
};
```

---

### Step 3: 更新调度器支持审核触发

**文件**: `task-scheduler.js`

**新增审核触发逻辑**:
```javascript
async triggerTask(task) {
  // ... 原有逻辑 ...
  
  // 如果是正文任务完成，触发审核
  if (task.id.includes('-writing') && status === 'completed') {
    const chapterNum = extractChapterNum(task.id);
    
    // 触发 L1 审核
    const l1TaskId = `chapter-${chapterNum}-review-l1`;
    if (this.tracker.getTaskStatus(l1TaskId)?.status === 'pending') {
      await this.triggerTask({ id: l1TaskId, agent: 'novel_editor' });
    }
    
    // 如果是第 10/20/30...章，触发 L2 审核
    if (chapterNum % 10 === 0) {
      const start = chapterNum - 9;
      const l2TaskId = `chapter-${start}-${chapterNum}-review-l2`;
      if (this.tracker.getTaskStatus(l2TaskId)?.status === 'pending') {
        await this.triggerTask({ id: l2TaskId, agent: 'novel_editor' });
      }
    }
  }
}
```

---

## ✅ 自我校验

### 校验 1: 审核是否异步？

**验证**:
```javascript
// 创作和审核并行
创作第 1 章 → 创作第 2 章 → 创作第 3 章
    ↓           ↓           ↓
审核第 1 章   审核第 2 章   审核第 3 章

// 时间线
T0: 开始创作第 1 章
T1: 第 1 章完成 → 开始创作第 2 章 → 开始审核第 1 章
T2: 第 2 章完成 → 开始创作第 3 章 → 开始审核第 2 章
...

// 审核不阻塞创作 ✅
```

---

### 校验 2: 审核依赖是否正确？

**验证**:
```javascript
// L1 审核依赖本章正文
chapter-1-review-l1 dependsOn: [chapter-1-writing] ✅

// L2 审核依赖 10 章正文
chapter-1-10-review-l2 dependsOn: [chapter-1-writing, ..., chapter-10-writing] ✅

// L3 审核依赖全部正文
chapter-1-100-review-l3 dependsOn: [chapter-1-writing, ..., chapter-100-writing] ✅
```

---

### 校验 3: 审核是否自动触发？

**验证**:
```javascript
// 正文完成后
onTaskComplete('chapter-1-writing') {
  // 自动触发 L1 审核
  triggerTask('chapter-1-review-l1'); ✅
  
  // 如果是第 10 章，触发 L2 审核
  if (chapterNum % 10 === 0) {
    triggerTask('chapter-1-10-review-l2'); ✅
  }
}
```

---

## 📊 效率对比

| 模式 | 创作时间 | 审核时间 | 总时间 | 效率 |
|------|----------|----------|--------|------|
| **串行审核** | 10 小时 | 10 小时 | 20 小时 | 50% |
| **异步审核** | 10 小时 | 10 小时 | 10 小时 | 100% |

**效率提升**: **50%**

---

## 📝 实施步骤

### 立即执行（P0）

1. ✅ 更新 .task-dependencies.json（添加审核依赖）
2. ✅ 更新 task-generator.js（生成审核任务）
3. ✅ 更新 task-scheduler.js（自动触发审核）
4. ⏳ 重启调度器

### 短期优化（P1）

5. ⏳ 添加审核进度展示
6. ⏳ 添加审核问题追踪
7. ⏳ 添加审核报告生成

---

## ✅ 总结

### 核心改进

**异步审核机制**:
1. ✅ 单章 L1 审核（每章完成后立即进行）
2. ✅ 批量 L2 审核（每 10 章进行一次）
3. ✅ 最终 L3 审核（全部完成后进行）
4. ✅ 审核与创作并行进行

### 效率提升

**时间节省**:
- 串行审核：20 小时
- 异步审核：10 小时
- **节省**: 50%

### 核心原则固化

```
审核原则：
1. 审核不阻塞创作 ✅
2. 单章审核立即触发 ✅
3. 批量审核定期进行 ✅
4. 最终审核保证质量 ✅
```

---

**下一步**: 立即实施异步审核机制！
