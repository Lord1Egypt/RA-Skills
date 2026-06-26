# ADD - 敏捷工作流 v5.0 架构设计文档

**日期**: 2026-03-12  
**版本**: v5.0.0  
**状态**: 设计完成 → 实现中

---

## 1. 架构概述

### 1.1 设计目标

1. **移除旧版本**：清理 v3.6 老旧脚本，统一使用 v4.0+ 引擎
2. **递归拆解**：支持子任务再拆解，直到可执行粒度
3. **智能排序**：根据依赖关系自动排序任务队列
4. **成果组装**：任务完成后统一组装，形成可交付成果

### 1.2 核心原则

```
输入需求 → 递归拆解 → 智能排序 → 执行 → 成果组装 → 交付
    ↓          ↓          ↓        ↓        ↓          ↓
  大任务    粒度评估   依赖分析   Agent    统一整合   可交付
```

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户输入需求                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              递归拆解引擎 (Recursive Decomposer)          │
│  - 任务粒度评估                                          │
│  - 自动再拆解                                            │
│  - 拆解深度限制 (最大 5 层)                                  │
│  - 依赖关系继承                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              智能排序引擎 (Smart Sorter)                 │
│  - 依赖顺序分析                                          │
│  - 优先级计算                                            │
│  - 队列自动插入                                          │
│  - 动态调整                                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              任务执行引擎 (Task Executor)                │
│  - Agent 分配                                             │
│  - 负载均衡                                              │
│  - 状态追踪                                              │
│  - 超时处理                                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              成果组装引擎 (Result Assembler)             │
│  - 结果收集                                              │
│  - 统一整合                                              │
│  - 版本管理                                              │
│  - 交付验证                                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  可交付成果                              │
│  - 完整功能                                              │
│  - 迭代版本                                              │
│  - 文档汇总                                              │
└─────────────────────────────────────────────────────────┘
```

### 2.2 模块划分

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **递归拆解引擎** | 任务拆解到可执行粒度 | 大任务 | 原子任务列表 |
| **智能排序引擎** | 根据依赖排序任务队列 | 原子任务列表 | 排序后的任务队列 |
| **任务执行引擎** | 分配 Agent 执行任务 | 排序后的任务队列 | 任务结果 |
| **成果组装引擎** | 整合所有任务结果 | 任务结果集合 | 可交付成果 |

---

## 3. 核心算法

### 3.1 递归拆解算法

```javascript
async function recursiveDecompose(task, depth = 0) {
  // 1. 检查拆解深度（最大 5 层）
  if (depth >= MAX_DEPTH) {
    return [task]; // 达到最大深度，强制返回
  }

  // 2. 评估任务粒度
  const granularity = evaluateGranularity(task);
  
  // 3. 如果粒度过大，继续拆解
  if (granularity > THRESHOLD) {
    const subtasks = await decomposeTask(task);
    
    // 4. 递归拆解每个子任务
    const atomicTasks = [];
    for (const subtask of subtasks) {
      subtask.parentTask = task.id;
      subtask.depth = depth + 1;
      const result = await recursiveDecompose(subtask, depth + 1);
      atomicTasks.push(...result);
    }
    
    return atomicTasks;
  }
  
  // 5. 任务已足够小，返回
  return [task];
}
```

### 3.2 智能排序算法

```javascript
function smartSort(tasks) {
  // 1. 构建依赖图
  const graph = buildDependencyGraph(tasks);
  
  // 2. 拓扑排序
  const sorted = topologicalSort(graph);
  
  // 3. 计算优先级（考虑深度、依赖数、紧急度）
  for (const task of sorted) {
    task.priority = calculatePriority(task);
  }
  
  // 4. 按优先级排序
  sorted.sort((a, b) => b.priority - a.priority);
  
  return sorted;
}
```

### 3.3 成果组装算法

```javascript
async function assembleResults(taskResults, originalTask) {
  // 1. 收集所有任务结果
  const results = gatherResults(taskResults);
  
  // 2. 按结构组织
  const organized = organizeByStructure(results, originalTask);
  
  // 3. 生成汇总文档
  const summary = generateSummary(organized);
  
  // 4. 打包交付物
  const deliverable = {
    id: generateId(),
    originalTask: originalTask,
    completedAt: Date.now(),
    results: organized,
    summary: summary,
    status: 'deliverable'
  };
  
  // 5. 保存到交付库
  await saveDeliverable(deliverable);
  
  return deliverable;
}
```

---

## 4. 数据结构

### 4.1 任务结构

```json
{
  "id": "task_001",
  "name": "创作第 1 章",
  "type": "chapter_write",
  "parentTask": "project_001",
  "depth": 2,
  "dependsOn": ["chapter_outline_001"],
  "agent": "chapter_writer",
  "status": "pending",
  "priority": 85,
  "granularity": 30,
  "createdAt": 1710288000000,
  "spec": ["规范路径1", "规范路径2"]
}
```

### 4.2 成果结构

```json
{
  "id": "deliverable_001",
  "originalTask": "创作《山海诡秘》第一卷",
  "completedAt": 1710288000000,
  "taskCount": 85,
  "results": {
    "chapters": ["第 1 章", "第 2 章", ...],
    "outlines": ["大纲", "细纲"],
    "settings": ["世界观", "人物"]
  },
  "summary": {
    "totalWords": 250000,
    "chapterCount": 85,
    "quality": "A"
  },
  "status": "deliverable",
  "version": "1.0.0"
}
```

---

## 5. 接口定义

### 5.1 递归拆解接口

```javascript
// 输入
{
  "task": {
    "name": "创作一部小说",
    "type": "novel_creation",
    "requirements": {...}
  },
  "maxDepth": 5
}

// 输出
{
  "atomicTasks": [...],
  "dependencyGraph": {...},
  "estimatedTime": 3600000
}
```

### 5.2 成果组装接口

```javascript
// 输入
{
  "taskId": "project_001",
  "taskResults": [...],
  "outputFormat": "complete_novel"
}

// 输出
{
  "deliverableId": "deliverable_001",
  "status": "assembled",
  "outputPath": "/path/to/deliverable",
  "quality": "A"
}
```

---

## 6. 旧版本移除计划

### 6.1 需要移除的文件

| 文件/目录 | 路径 | 状态 |
|----------|------|------|
| 旧脚本 | `/skills/agile-workflow/scripts/*.sh` | 待移除 |
| 旧配置 | `/skills/agile-workflow/config/` | 待移除 |
| 旧文档 | `/skills/agile-workflow/README.md` | 待更新 |

### 6.2 移除步骤

1. 备份旧版本代码
2. 停止所有旧版本进程
3. 删除旧脚本文件
4. 更新配置文件
5. 验证新版本功能

---

## 7. 测试计划

### 7.1 功能测试

| 测试项 | 输入 | 期望输出 | 状态 |
|--------|------|---------|------|
| 递归拆解 | 大任务 | 原子任务列表 | ⏳ |
| 智能排序 | 无序任务 | 有序队列 | ⏳ |
| 成果组装 | 分散结果 | 统一成果 | ⏳ |
| 旧版移除 | 旧版本 | 完全清理 | ⏳ |

### 7.2 性能测试

| 指标 | 目标值 | 实测值 | 状态 |
|------|--------|--------|------|
| 拆解速度 | < 5 秒/任务 | - | ⏳ |
| 排序速度 | < 1 秒/100 任务 | - | ⏳ |
| 组装速度 | < 10 秒/成果 | - | ⏳ |

---

## 8. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 递归过深 | 中 | 高 | 限制最大深度 5 层 |
| 循环依赖 | 低 | 高 | 检测并报错 |
| 成果丢失 | 低 | 高 | 实时备份 |
| 性能下降 | 中 | 中 | 性能监控 |

---

## 9. 实施计划

### Phase 1: 核心引擎开发 (已完成)
- [x] 递归拆解引擎
- [x] 智能排序引擎
- [x] 成果组装引擎

### Phase 2: 旧版本移除 (进行中)
- [ ] 备份旧代码
- [ ] 停止旧进程
- [ ] 删除旧文件

### Phase 3: 集成测试 (待开始)
- [ ] 功能测试
- [ ] 性能测试
- [ ] 回归测试

### Phase 4: 部署上线 (待开始)
- [ ] 生产环境部署
- [ ] 监控配置
- [ ] 文档更新

---

**ADD 设计完成，准备实施！** 🚀
