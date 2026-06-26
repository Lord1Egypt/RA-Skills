# ADD v7.17: 任务自动调度修复

**版本**: v7.17.0  
**日期**: 2026-03-13  
**问题**: 第 5 章细纲已完成，为何不继续第 6 章？细纲完成后为何不自动开始正文？  
**范围**: 通用任务调度系统（不只是小说创作）  
**方法**: 第一性原理 + 思维链 + MECE 拆解 + 自我校验

---

## 🎯 第一性原理分析

### 问题本质
```
现象：
- 第 5 章细纲已完成 → 第 6 章未自动开始
- 细纲已完成 → 正文未自动开始

第一性原理：
任务系统 = 任务定义 + 依赖关系 + 状态追踪 + 调度执行

若任务完成后不自动触发后续任务，说明：
1. 任务状态未正确追踪
2. 依赖关系未正确定义
3. 调度器未检测完成状态
4. 无自动触发机制

核心洞察：
好的任务系统 = 任务完成 → 自动触发后续任务
```

### 任务依赖链

```
小说创作任务链：
核心设定 ✅
  ↓
世界观架构 ✅
  ↓
人物体系 ✅
  ↓
情节大纲 ✅
  ↓
章节细纲 (第 1 章✅ → 第 2 章✅ → 第 3 章✅ → 第 4 章✅ → 第 5 章✅ → 第 6 章⏳)
  ↓                                              ↓
正文创作 (第 1 章⏳ ←──────────────────────────────┘

问题：
1. 第 5 章完成 → 第 6 章未自动开始 ❌
2. 第 1 章细纲完成 → 第 1 章正文未自动开始 ❌
```

---

## 📐 MECE 拆解

### 维度 1: 问题来源

| 问题 | 根因 | 影响范围 |
|------|------|----------|
| **任务不自动继续** | 无任务完成检测 | 🔴 通用 |
| **依赖任务不触发** | 无依赖触发机制 | 🔴 通用 |
| **状态未追踪** | 无状态更新机制 | 🔴 通用 |
| **调度器缺失** | 无自动调度器 | 🔴 通用 |

### 维度 2: 通用性分析

| 任务类型 | 任务依赖 | 受影响 |
|----------|----------|--------|
| **小说创作** | 细纲→正文 | 🔴 是 |
| **代码开发** | 设计→编码→测试 | 🔴 是 |
| **数据清洗** | 采集→清洗→分析 | 🔴 是 |
| **市场调研** | 数据→分析→报告 | 🔴 是 |
| **文档编写** | 大纲→编写→审查 | 🔴 是 |

**结论**: ✅ 所有任务类型都受影响

---

### 维度 3: 修复方案

| 组件 | 功能 | 通用性 |
|------|------|--------|
| **任务状态追踪器** | 追踪任务完成状态 | ✅ 通用 |
| **依赖关系管理器** | 定义任务依赖 | ✅ 通用 |
| **自动调度器** | 检测完成并触发后续 | ✅ 通用 |
| **任务队列管理器** | 管理待执行任务 | ✅ 通用 |

---

## 🔍 详细分析

### 问题 1: 任务完成后不继续

**当前流程**:
```
第 5 章细纲完成 → 无检测 → 无触发 → 第 6 章未开始
```

**正确流程**:
```
第 5 章细纲完成 → 状态更新 → 检测依赖 → 触发第 6 章 → 第 6 章开始
```

**根因**: 无任务完成检测和触发机制

---

### 问题 2: 依赖任务不自动触发

**当前流程**:
```
第 1 章细纲完成 → 无检测 → 正文未开始
```

**正确流程**:
```
第 1 章细纲完成 → 状态更新 → 检测依赖 → 触发正文 → 正文开始
```

**根因**: 无依赖关系定义和触发机制

---

### 问题 3: 任务状态未追踪

**当前状态**:
```
任务队列：第 1-5 章✅ 第 6-10 章⏳
但系统不知道✅ 的任务已完成
```

**正确状态**:
```
任务状态库：
{
  "chapter-1-outline": "completed",
  "chapter-2-outline": "completed",
  ...
  "chapter-6-outline": "pending"
}
```

**根因**: 无任务状态库

---

## 🔧 通用修复方案

### 修复 1: 创建任务状态追踪器

**文件**: `skills/agile-workflow/core/task-state-tracker.js`

```javascript
class TaskStateTracker {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
    this.states = this.loadStates();
  }

  // 更新任务状态
  updateTask(taskId, status, metadata = {}) {
    this.states[taskId] = {
      status,  // 'pending' | 'running' | 'completed' | 'failed'
      updatedAt: new Date().toISOString(),
      ...metadata
    };
    this.saveStates();
    
    // ✅ 触发调度器检查
    this.triggerScheduler();
  }

  // 获取任务状态
  getTaskStatus(taskId) {
    return this.states[taskId];
  }

  // 获取所有待执行任务
  getPendingTasks() {
    return Object.entries(this.states)
      .filter(([_, state]) => state.status === 'pending')
      .map(([id, state]) => ({ id, ...state }));
  }

  // 触发调度器
  triggerScheduler() {
    const scheduler = new TaskScheduler(this.projectDir);
    scheduler.checkAndTrigger();
  }
}
```

---

### 修复 2: 创建依赖关系管理器

**文件**: `skills/agile-workflow/core/dependency-manager.js`

```javascript
class DependencyManager {
  constructor() {
    this.dependencies = new Map();
  }

  // 定义任务依赖
  addDependency(taskId, dependsOn) {
    if (!this.dependencies.has(taskId)) {
      this.dependencies.set(taskId, []);
    }
    this.dependencies.get(taskId).push(dependsOn);
  }

  // 检查依赖是否完成
  areDependenciesMet(taskId) {
    const deps = this.dependencies.get(taskId) || [];
    return deps.every(depId => {
      const state = this.tracker.getTaskStatus(depId);
      return state && state.status === 'completed';
    });
  }

  // 获取可执行任务
  getExecutableTasks() {
    const pending = this.tracker.getPendingTasks();
    return pending.filter(task => this.areDependenciesMet(task.id));
  }
}
```

---

### 修复 3: 创建自动调度器

**文件**: `skills/agile-workflow/core/task-scheduler.js`

```javascript
class TaskScheduler {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.tracker = new TaskStateTracker(projectDir);
    this.deps = new DependencyManager();
  }

  // 检查并触发任务
  async checkAndTrigger() {
    const executable = this.deps.getExecutableTasks();
    
    for (const task of executable) {
      // 检查是否已在运行
      if (this.isRunning(task.id)) {
        continue;
      }
      
      // 触发任务
      await this.triggerTask(task);
    }
  }

  // 触发单个任务
  async triggerTask(task) {
    console.log(`🚀 触发任务：${task.id}`);
    
    // 更新状态为运行中
    this.tracker.updateTask(task.id, 'running');
    
    // 启动 Agent 执行
    await this.startAgent(task);
  }

  // 启动 Agent
  async startAgent(task) {
    const { exec } = require('child_process');
    
    return new Promise((resolve) => {
      exec(`openclaw agent --agent ${task.agent} -m "${task.description}"`, (error) => {
        if (error) {
          this.tracker.updateTask(task.id, 'failed', { error: error.message });
        } else {
          this.tracker.updateTask(task.id, 'completed');
        }
        resolve();
      });
    });
  }
}
```

---

### 修复 4: 定义小说创作任务依赖

**文件**: `skills/agile-workflow/tasks/novel-creation-config.js`

```javascript
// 小说创作任务配置
const NOVEL_TASKS = {
  // 章节细纲任务
  'chapter-1-outline': {
    agent: 'novel_architect',
    description: '创作第 1 章细纲',
    dependsOn: ['plot-outline']  // 依赖情节大纲
  },
  'chapter-2-outline': {
    agent: 'novel_architect',
    description: '创作第 2 章细纲',
    dependsOn: ['chapter-1-outline']  // 依赖第 1 章细纲
  },
  'chapter-3-outline': {
    dependsOn: ['chapter-2-outline']
  },
  // ...
  
  // 正文创作任务
  'chapter-1-writing': {
    agent: 'novel_writer',
    description: '创作第 1 章正文',
    dependsOn: ['chapter-1-outline']  // 依赖第 1 章细纲
  },
  'chapter-2-writing': {
    agent: 'novel_writer',
    description: '创作第 2 章正文',
    dependsOn: ['chapter-2-outline']
  },
  // ...
};
```

---

## ✅ 自我校验

### 校验 1: 任务完成后是否自动继续？

**验证**:
```javascript
// 模拟第 5 章细纲完成
tracker.updateTask('chapter-5-outline', 'completed');

// 调度器应自动触发第 6 章
// 预期：第 6 章自动开始
```

**预期**: ✅ 第 6 章自动开始

---

### 校验 2: 细纲完成后是否触发正文？

**验证**:
```javascript
// 定义依赖
deps.addDependency('chapter-1-writing', 'chapter-1-outline');

// 模拟细纲完成
tracker.updateTask('chapter-1-outline', 'completed');

// 调度器应自动触发正文
// 预期：第 1 章正文自动开始
```

**预期**: ✅ 正文自动开始

---

### 校验 3: 是否通用？

**验证**:
```javascript
// 代码开发任务
const CODE_TASKS = {
  'module-design': { agent: 'code_architect' },
  'module-coding': { 
    agent: 'code_developer',
    dependsOn: ['module-design']
  },
  'module-testing': {
    agent: 'code_tester',
    dependsOn: ['module-coding']
  }
};

// 应该同样工作
```

**预期**: ✅ 通用

---

## 📊 修复前后对比

| 维度 | 修复前 | 修复后 |
|------|--------|--------|
| **任务继续** | 手动触发 | 自动触发 ✅ |
| **依赖触发** | 无 | 自动触发 ✅ |
| **状态追踪** | 无 | 完整追踪 ✅ |
| **调度器** | 无 | 自动调度 ✅ |
| **通用性** | 小说专用 | 通用 ✅ |

---

## 📝 实施步骤

### 已完成（设计）

1. ✅ 设计 TaskStateTracker
2. ✅ 设计 DependencyManager
3. ✅ 设计 TaskScheduler
4. ✅ 设计任务配置格式

### 待完成（实施）

5. ⏳ 实现 TaskStateTracker
6. ⏳ 实现 DependencyManager
7. ⏳ 实现 TaskScheduler
8. ⏳ 定义小说创作任务依赖
9. ⏳ 测试自动触发

---

## ✅ 总结

### 核心问题

**任务调度缺陷**:
1. ❌ 任务完成后不自动继续
2. ❌ 依赖任务不自动触发
3. ❌ 任务状态未追踪
4. ❌ 无自动调度器

### 修复方案

**通用组件** (4 个):
1. ✅ TaskStateTracker（任务状态追踪）
2. ✅ DependencyManager（依赖关系管理）
3. ✅ TaskScheduler（自动调度）
4. ✅ 任务配置格式（通用）

### 核心原则固化

```
任务调度原则：
1. 任务完成自动更新状态 ✅
2. 状态更新触发调度检查 ✅
3. 依赖完成自动触发后续 ✅
4. 调度器通用不依赖任务类型 ✅
```

---

**下一步**: 实现自动调度组件并测试！
