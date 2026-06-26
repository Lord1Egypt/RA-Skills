# Agent Work Visibility - 示例输出

## 场景：调研 AI Agent 专用区块链

### 默认视图（Default View）

```
任务：调研 AI Agent 专用区块链
状态：运行中
当前阶段：分析与比较

当前在做什么：
正在比较 3 个重点项目的定位与差异。

为什么还没完成：
其中 2 个项目资料不一致，正在交叉验证。

下一步：
输出一页结论摘要。

是否需要你：
暂时不需要。
```

---

### 展开视图（Full View）

```
任务：调研 AI Agent 专用区块链
状态：运行中
当前阶段：分析与比较

当前在做什么：
正在比较 3 个重点项目的定位与差异。

为什么还没完成：
其中 2 个项目资料不一致，正在交叉验证。

下一步：
输出一页结论摘要。

是否需要你：
暂时不需要。

━━━━━━━━━━━━━━━━━━━━━━━━
【展开详情】

【总体进度】
███████░░░ 65%
预计剩余：约 3 分钟

【阶段进度】
✓ 理解任务
✓ 制定搜索计划
✓ 收集信息
⟳ 分析与比较 - 60%
○ 形成输出

【最近动作】
• 正在比较 3 个重点项目
• 已提取 12 个候选项目
• 第一次请求超时，已自动重试
• 正在读取第 3 个网页
• 已明确搜索范围
• 开始制定执行计划
• 任务已启动：调研 AI Agent 专用区块链

【阻塞状态】
无阻塞

【时间信息】
开始：03-18 10:30
更新：03-18 10:45
```

---

## 场景：遇到阻塞

### 默认视图（阻塞状态）

```
任务：调研 AI Agent 专用区块链
状态：已阻塞
当前阶段：收集信息

当前在做什么：
等待外部 API 响应。

为什么还没完成：
外部 API 响应超时（已持续 2 分钟）

下一步：
继续等待或跳过此数据源。

是否需要你：
暂时不需要。
```

### 展开视图（阻塞详情）

```
...（默认视图内容）

━━━━━━━━━━━━━━━━━━━━━━━━
【展开详情】

【总体进度】
████░░░░░░ 40%
预计剩余：约 8 分钟

【阶段进度】
✓ 理解任务
✓ 制定搜索计划
⟳ 收集信息 - 30%
○ 分析与比较
○ 形成输出

【最近动作】
⚠ 外部 API 响应超时
↻ 第 2 次重试：API 请求
• 正在读取第 5 个网页
• 已提取 8 个候选项目

【阻塞状态】
级别：low
原因：外部 API 响应超时
持续：2 分钟
建议：可继续等待，系统会自动重试

【重试记录】
✗ API 请求 - 第 1 次：超时
↻ API 请求 - 第 2 次：超时

【时间信息】
开始：03-18 10:30
更新：03-18 10:35
```

---

## 场景：需要用户介入

### 默认视图（需要用户决策）

```
任务：调研 AI Agent 专用区块链
状态：等待中
当前阶段：分析与比较

当前在做什么：
等待用户选择深入方向。

为什么还没完成：
等待用户输入

下一步：
根据用户选择继续分析。

是否需要你：
⚠️ 需要！

问题：发现 3 个方向都可继续深入，你要优先看哪一个？
选项：
  - A: 技术架构
  - B: 商业模式
  - C: 团队背景
```

---

## 场景：任务完成

### 默认视图（完成状态）

```
任务：调研 AI Agent 专用区块链
状态：已完成
当前阶段：形成输出

当前在做什么：
任务已完成。

为什么还没完成：
任务正在正常执行中

下一步：
查看输出结果。

是否需要你：
暂时不需要。
```

### 展开视图（完成详情）

```
...（默认视图内容）

━━━━━━━━━━━━━━━━━━━━━━━━
【展开详情】

【总体进度】
██████████ 100%
预计剩余：已完成

【阶段进度】
✓ 理解任务
✓ 制定搜索计划
✓ 收集信息
✓ 分析与比较
✓ 形成输出

【最近动作】
• 任务已完成
• 已生成报告：5 页
• 输出已完成
• 完成最终复核
• 正在生成输出

【阻塞状态】
无阻塞

【时间信息】
开始：03-18 10:30
更新：03-18 11:15
完成：03-18 11:15
```

---

## JSON 输出示例

```json
{
  "task_id": "uuid-12345",
  "task_title": "调研 AI Agent 专用区块链",
  "task_type": "research",
  "overall_status": "running",
  "current_phase": "分析与比较",
  "progress_percent": 65,
  "current_action": "正在比较 3 个重点项目的定位与差异",
  "why_not_done": "其中 2 个项目资料不一致，正在交叉验证",
  "next_action": "输出一页结论摘要",
  "needs_user_input": false,
  "user_question": null,
  "user_options": [],
  "started_at": "2026-03-18T10:30:00.000Z",
  "updated_at": "2026-03-18T10:45:00.000Z",
  "phases": [
    {
      "name": "理解任务",
      "status": "completed",
      "progress": 100,
      "weight": 10,
      "completed": true
    },
    {
      "name": "制定搜索计划",
      "status": "completed",
      "progress": 100,
      "weight": 15,
      "completed": true
    },
    {
      "name": "收集信息",
      "status": "completed",
      "progress": 100,
      "weight": 30,
      "completed": true
    },
    {
      "name": "分析与比较",
      "status": "in_progress",
      "progress": 60,
      "weight": 30,
      "completed": false
    },
    {
      "name": "形成输出",
      "status": "pending",
      "progress": 0,
      "weight": 15,
      "completed": false
    }
  ],
  "action_log": [
    {
      "timestamp": "2026-03-18T10:45:00.000Z",
      "message": "正在比较 3 个重点项目",
      "level": "info"
    },
    {
      "timestamp": "2026-03-18T10:42:00.000Z",
      "message": "已提取 12 个候选项目",
      "level": "info"
    }
  ],
  "blocker": {
    "has_blocker": false
  }
}
```

---

## 使用示例代码

```javascript
const { TaskVisibilityManager, BLOCKER_TYPE, USER_INPUT_TYPE } = require('./src/index');

// 创建管理器
const manager = new TaskVisibilityManager();

// 创建任务
manager.createTask('task-001', '调研 AI Agent 专用区块链', 'research');

// 开始第一阶段
manager.startPhase('task-001', '理解任务');
manager.setNextAction('task-001', '明确搜索关键词');

// 记录动作
manager.log('task-001', '已明确搜索范围：AI + 区块链 + Agent');
manager.event('task-001', 'search_query_defined', { query: 'AI Agent blockchain' });

// 完成第一阶段，自动进入下一阶段
manager.completePhase('task-001', '理解任务', '已明确任务目标');

// 开始收集信息阶段
manager.startPhase('task-001', '收集信息');
manager.event('task-001', 'search_started');

// 记录网页读取
manager.event('task-001', 'page_fetch_started', { url: 'https://example.com', pageNumber: 1 });
manager.event('task-001', 'page_fetch_completed', { pageNumber: 3 });

// 更新阶段进度
manager.updatePhaseProgress('task-001', '收集信息', 50, '正在读取第 5 个网页');

// 遇到阻塞
manager.block('task-001', BLOCKER_TYPE.API_TIMEOUT, '外部 API 响应超时');

// 请求用户介入
manager.ask('task-001', USER_INPUT_TYPE.DIRECTION_CHOICE, 
  '发现 3 个方向都可继续深入，你要优先看哪一个？',
  ['A: 技术架构', 'B: 商业模式', 'C: 团队背景']
);

// 获取视图
console.log(manager.getDefaultView('task-001'));  // 默认视图
console.log(manager.getFullView('task-001'));     // 展开视图
console.log(manager.getStatusJSON('task-001', true));  // JSON
```
