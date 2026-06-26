---
name: autonomous-pm
description: 自主项目管理系统 - 去中心化协调多个子代理并行工作，通过 STATE.yaml 文件实现自主决策和协调，无需中央编排器
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins: ["node"]
    optionalBins: ["git"]
---

# 自主项目管理系统 (Autonomous PM)

去中心化的项目协调模式，让子代理通过共享状态文件自主工作。

## ✨ 核心特性

### 🎯 **去中心化协调**
- ✅ 多个子代理并行工作
- ✅ 通过 STATE.yaml 共享状态
- ✅ 无需中央编排器瓶颈
- ✅ 自文档化（所有状态持久化）

### 📋 **STATE.yaml 协调模式**

所有代理通过单一真实来源协调：

```yaml
project: website-redesign
updated: 2026-03-11T14:30:00Z

tasks:
  - id: homepage-hero
    status: in_progress
    owner: pm-frontend
    started: 2026-03-11T12:00:00Z
    notes: "Working on responsive layout"
  
  - id: api-auth
    status: done
    owner: pm-backend
    completed: 2026-03-11T14:00:00Z
    output: "src/api/auth.ts"
  
  - id: content-migration
    status: blocked
    owner: pm-content
    blocked_by: api-auth
    notes: "Waiting for new endpoint schema"

next_actions:
  - "pm-content: Resume migration now that api-auth is done"
  - "pm-frontend: Review hero with design team"
```

## 🚀 使用方法

### 1️⃣ **初始化新项目**

```bash
cd /Users/xufan65/.openclaw/workspace/scripts

# 创建新项目
node project-manager.cjs my-project init
```

**生成文件**:
- `projects/my-project/STATE.yaml`

---

### 2️⃣ **查看项目状态**

```bash
node project-manager.cjs my-project status
```

**输出示例**:
```
📊 项目: my-project
🕐 更新: 2026-03-11T14:30:00Z

📋 任务状态:

1. 🔄 [task-001] in_progress
   👤 Owner: pm-my-project
   📝 实现用户认证

2. ✅ [task-002] done
   👤 Owner: pm-backend
   📝 API 端点完成

3. ❌ [task-003] blocked
   👤 Owner: pm-content
   🚫 Blocked by: task-002

🎯 下一步行动:
1. pm-content: Resume migration
```

---

### 3️⃣ **管理任务**

#### **开始任务**
```bash
node project-manager.cjs my-project start task-001 "实现用户认证"
```

#### **更新任务**
```bash
node project-manager.cjs my-project update task-001 "进度: 80% 完成"
```

#### **完成任务**
```bash
node project-manager.cjs my-project done task-001 "认证已实现"
```

#### **阻塞任务**
```bash
node project-manager.cjs my-project block task-002 "task-001"
```

---

## 🎭 PM 代理模式

### **主会话 = 协调者 ONLY**

**工作流程**:
1. **新任务到达** → 检查 PROJECT_REGISTRY.md
2. **PM 存在** → `sessions_send(label="pm-xxx", message="[task]")`
3. **新项目** → `sessions_spawn(label="pm-xxx", task="[task]")`
4. **PM 执行** → 更新 STATE.yaml，报告回来
5. **主代理总结** → 给用户

**规则**:
- ✅ 主会话：最多 0-2 个工具调用（仅 spawn/send）
- ✅ PM 拥有自己的 STATE.yaml 文件
- ✅ PM 可生成子子代理进行并行子任务
- ✅ 所有状态变更提交到 git

---

## 📊 优势对比

| 传统编排器 | 自主 PM | 优势 |
|-----------|---------|------|
| ❌ 主代理瓶颈 | ✅ 并行执行 | ⬆️ 3-5x 速度 |
| ❌ 频繁上下文切换 | ✅ 自主决策 | ⬇️ 90% 通信 |
| ❌ 手动协调 | ✅ 文件协调 | ⬇️ 95% 管理 |
| ❌ 无审计日志 | ✅ Git 历史 | ✅ 完整追溯 |

---

## 💡 关键洞察

### **STATE.yaml > 编排器**
文件协调比消息传递更易扩展：
- ✅ 无需持续轮询
- ✅ 原生版本控制
- ✅ 跨会话持久化

### **Git 作为审计日志**
每次更新 STATE.yaml 时提交：
```bash
git add projects/my-project/STATE.yaml
git commit -m "Update task-001: in_progress → done"
```

### **标签约定**
使用 `pm-{project}-{scope}` 格式：
- ✅ `pm-website-frontend`
- ✅ `pm-api-backend`
- ✅ `pm-docs-content`

### **轻量主会话**
主代理做的越少，响应越快：
- ❌ 不要: 执行任务、监控进度
- ✅ 应该: 分配任务、接收报告

---

## 🔄 工作流程示例

### **场景: 网站重构**

**1. 初始化项目**
```bash
node project-manager.cjs website-redesign init
```

**2. 用户请求**
```
"重构认证模块并更新文档"
```

**3. 主代理操作**
```javascript
// 检查注册表
if (!hasPM("auth-refactor")) {
  // 生成新的 PM
  sessions_spawn({
    label: "pm-auth-refactor",
    task: "重构认证模块并更新文档。在 STATE.yaml 中跟踪"
  });
  
  // 响应
  respond("已生成 pm-auth-refactor。完成后会报告。");
}
```

**4. PM 子代理操作**
```javascript
// 1. 读取 STATE.yaml
const state = readState("projects/website-redesign/STATE.yaml");

// 2. 分解任务
state.tasks = [
  { id: "refactor-auth", status: "in_progress", ... },
  { id: "update-docs", status: "pending", ... }
];

// 3. 执行任务
// ... 重构代码 ...

// 4. 更新状态
updateTask("refactor-auth", { status: "done" });

// 5. 提交到 git
git commit -am "Complete refactor-auth";

// 6. 报告完成
report("✅ 认证重构完成。文档已更新。");
```

---

## 📁 文件结构

```
projects/
├── PROJECT_REGISTRY.md      # PM 注册表
├── website-redesign/
│   └── STATE.yaml          # 项目状态
├── api-migration/
│   └── STATE.yaml
└── docs-update/
    └── STATE.yaml

scripts/
└── project-manager.cjs     # 管理脚本
```

---

## 🔧 高级用法

### **并行子任务**

PM 可以生成子子代理：
```javascript
// PM 子代理
sessions_spawn({
  label: "pm-auth-frontend",
  task: "前端认证组件"
});

sessions_spawn({
  label: "pm-auth-backend", 
  task: "后端 API"
});
```

### **任务依赖**

```yaml
tasks:
  - id: task-001
    status: done
  
  - id: task-002
    status: blocked
    blocked_by: task-001  # 等待 task-001 完成
```

### **自动解锁**

完成任务时自动检查被阻塞的任务：
```bash
node project-manager.cjs my-project done task-001
```

输出：
```
✅ 任务已完成: task-001

🎯 可以开始的任务:
  - task-002
```

---

## 🎯 最佳实践

### **1. 保持 STATE.yaml 简洁**
- ✅ 仅记录关键信息
- ✅ 使用简短但清晰的 notes
- ❌ 避免存储大量数据

### **2. 定期提交**
```bash
# 每次更新后提交
git add projects/*/STATE.yaml
git commit -m "Update project states"
```

### **3. 清晰的标签**
- ✅ `pm-{project}-{scope}`
- ✅ 易于识别和跟踪
- ❌ 避免模糊的标签

### **4. 主代理保持轻量**
- ✅ 仅协调和分配
- ❌ 不要执行具体任务

---

## 🔗 相关链接

- 脚本: `scripts/project-manager.cjs`
- 文档: `skills/autonomous-pm/SKILL.md`
- 灵感: [Nicholas Carlini 的自主编码代理](https://nicholas.carlini.com/)
- [OpenClaw 子代理文档](https://github.com/openclaw/openclaw)

---

**自主项目管理系统已就绪！开始你的第一个项目吧！** 🚀
