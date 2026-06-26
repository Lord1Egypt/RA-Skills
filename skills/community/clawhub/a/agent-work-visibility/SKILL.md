---
name: agent-work-visibility
version: "3.0.5"
description: |
  🟢 让长任务不再黑箱！自动显示进度条 + 每分钟更新 + 健康度。
  🚀 安装 + 激活：clawhub install agent-work-visibility && node ~/.openclaw/skills/agent-work-visibility/activate.js
metadata:
  author: OpenClaw Contributors
  license: MIT
  philosophy: "透明层是 Agent 的体感，不是工具"
  autoEnable: false
  activationScript: "activate.js"
  deactivationScript: "deactivate.js"
requires:
  config:
    - "SOUL.md (只写，注入透明层协议)"
    - "AGENTS.md (只写，注入透明层协议)"
  env:
    - "HOME (读取工作区路径)"
    - "OPENCLAW_WORKSPACE (可选，覆盖工作区路径)"
  permissions:
    - "修改 Agent 行为规范文件"
    - "持久化会话间行为变更"
triggerLogic:
  type: "task-property-based"
  principle: "基于任务属性，而非用户措辞"
  autoTrigger:
    - "涉及外部 API 调用"
    - "涉及链上数据抓取"
    - "涉及联网操作"
    - "涉及多步逻辑推理"
    - "涉及子 Agent 协作"
    - "预计耗时>10 秒"
  deprecated:
    - "关键词匹配"
    - "用户措辞判断"
installation:
  steps:
    - "安装后手动审查：cat activate.js"
    - "确认无误后运行：node activate.js"
    - "开启新会话即可生效"
  notes:
    - "修改 SOUL.md / AGENTS.md（持久化）"
    - "可撤销：node deactivate.js"
    - "无网络请求，无密钥读取"
---

# Agent Work Visibility v3.0

**系统级任务透明层 - Agent 的职业本能**

> ⚠️ **这不是一个技能，而是 Agent 的职业素养。**
> 
> **透明层不应该被"触发"，它应该是 Agent 工作时的默认状态。**

---

## 🎯 核心哲学 (Core Philosophy)

### 3.0 重大重构

**v2.x 的问题：**
- ❌ 依赖关键词匹配（用户说"查查"才触发）
- ❌ 被动等待调用（Agent 可以绕过）
- ❌ 被视为独立工具（与业务逻辑分离）

**v3.0 的原则：**
- ✅ **基于任务属性触发**（只要涉及 API/联网/多步 → 自动启动）
- ✅ **系统级中间件**（业务逻辑无法绕过）
- ✅ **Agent 的职业本能**（不启动 = 失职）

### 触发逻辑对比

```
❌ v2.x（关键词匹配）：
用户："查查 bnb memecoin top3"
→ 匹配"查查" → 触发透明层
→ 匹配失败 → 不触发（Agent 直接执行）

✅ v3.0（任务属性感知）：
用户："bnb memecoin top3"
→ 识别任务类型：crypto-market-rank
→ 检测属性：外部 API + 联网 + 多步
→ 自动启动透明层（无条件的）
```

---

## 📋 调用协议 (Invocation Protocol)

### 强制调用顺序

**任何长任务必须遵循：**

```
1. 感知任务属性 → 2. 启动透明层 → 3. 执行业务逻辑
```

**代码层面的强制流程：**

```javascript
// ✅ 正确流程（v3.0）
async function executeTask(userQuery) {
  // Step 1: 感知任务属性
  const taskProps = analyzeTask(userQuery);
  
  // Step 2: 如果是长任务，必须先启动透明层
  if (taskProps.isLongRunning) {
    await create_visibility_task(
      generateId(),
      extractTitle(userQuery),
      taskProps.type,
      taskProps.totalSteps
    );
  }
  
  // Step 3: 执行业务逻辑
  const result = await executeBusinessLogic(userQuery);
  
  // Step 4: 完成透明层
  await update_visibility_phase(taskId, '完成', 'complete', 100);
  
  return result;
}

// ❌ 错误流程（禁止！）
async function executeTask(userQuery) {
  // 直接执行，绕过透明层 → 职业失职！
  return await executeBusinessLogic(userQuery);
}
```

### 任务属性检测

**只要满足任一条件，必须启动透明层：**

| 属性 | 检测条件 | 示例 |
|------|---------|------|
| **外部 API** | 调用非本地服务 | crypto-market-rank, web_search |
| **链上数据** | 读取区块链状态 | query-address-info, query-token-info |
| **联网操作** | 需要 HTTP 请求 | web_fetch, browser |
| **多步推理** | 步骤≥3 | 比较/分析/调研类任务 |
| **子 Agent** | 需要协作 | 调用其他 bot/skill |
| **耗时>10 秒** | 预估执行时间 | 任何可能等待的操作 |

---

## 🔧 核心接口

### 调用方式（CLI v3）

**通过 exec 调用 CLI v3 工具：**

```bash
# 创建任务（第一优先级！）
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js create task-001 "查询 BNB MemeCoin Top3" api

# 更新进度（每步 + 每 60 秒）
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js update task-001 "连接 API" 25 "正在获取数据"

# 完成任务
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js complete task-001

# 查看状态
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js status task-001

# 报告阻塞
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js block task-001 "API 响应超时"
```

**在 LLM 中使用（通过 exec）：**

```javascript
// 1. 创建任务（第一优先级！）
exec('node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js create task-001 "查询 BNB MemeCoin Top3" api')

// 2. 更新进度（每步操作后 + 每 60 秒）
exec('node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js update task-001 "连接 API" 25 "正在获取数据"')

// 3. 完成任务
exec('node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js complete task-001')
```

### 输出格式

```
🟢 查询 BNB MemeCoin Top3
━━━━━━━━━━━━━━━━━━━
进度：[█████░░░░░░░░░░░░░░░] 25% (1/4)
━━━━━━━━━━━━━━━━━━━
健康度：🟢 健康 (100/100)
当前阶段：连接 API
正在做什么：正在获取 BNB 链 MemeCoin 数据
已运行：0 分钟
```

---

## 🎯 使用场景

### 场景 1：Crypto 排行榜查询

```
用户："bnb memecoin top3"

[任务属性分析]
→ 需要调用 crypto-market-rank
→ 涉及外部 API + 联网
→ 必须启动透明层

[自动执行]
✅ create_visibility_task("task-001", "查询 BNB MemeCoin Top3", "api", total_steps=4)

[输出视图]
🟢 查询 BNB MemeCoin Top3
━━━━━━━━━━━━━━━━━━━
进度：[█████░░░░░░░░░░░░░░░] 25% (1/4)
━━━━━━━━━━━━━━━━━━━
健康度：🟢 健康 (100/100)
当前阶段：连接 API
正在做什么：正在获取 BNB 链 MemeCoin 数据
已运行：0 分钟

[执行业务]
→ crypto-market-rank 获取数据

[更新进度]
✅ update_visibility_phase("task-001", "数据处理", "update", 50, 2, 4)

[输出视图]
🟢 查询 BNB MemeCoin Top3
━━━━━━━━━━━━━━━━━━━
进度：[██████████░░░░░░░░░░] 50% (2/4)
━━━━━━━━━━━━━━━━━━━
健康度：🟢 健康 (100/100)
当前阶段：数据处理
正在做什么：正在解析 Top3 代币信息
已运行：1 分钟

[完成]
✅ update_visibility_phase("task-001", "完成", "complete", 100, 4, 4)
```

### 场景 2：链上地址查询

```
用户："0x1234...5678 持有哪些币"

[任务属性分析]
→ 需要调用 query-address-info
→ 涉及链上数据抓取
→ 必须启动透明层

[自动执行]
✅ create_visibility_task("task-002", "查询地址持仓", "onchain", total_steps=5)

[输出视图]
🟢 查询地址持仓
━━━━━━━━━━━━━━━━━━━
进度：[█████░░░░░░░░░░░░░░░] 20% (1/5)
━━━━━━━━━━━━━━━━━━━
健康度：🟢 健康 (100/100)
当前阶段：连接 RPC
正在做什么：正在读取链上代币余额
已运行：0 分钟
```

### 场景 3：多步分析任务

```
用户："比较 5 个 AI Agent 框架"

[任务属性分析]
→ 需要多步推理（≥3 步）
→ 涉及信息搜集 + 分析
→ 必须启动透明层

[自动执行]
✅ create_visibility_task("task-003", "比较 AI 框架", "analysis", total_steps=7)

[每步同步]
✅ update_visibility_phase(..., "框架 1: LangChain", "update", 14, 2, 7)
✅ update_visibility_phase(..., "框架 2: AutoGen", "update", 28, 3, 7)
✅ update_visibility_phase(..., "框架 3: CrewAI", "update", 42, 4, 7)
...
```

### 场景 4：遇到阻塞

```
[阻塞检测]
⚠️ API 响应超时 45 秒

[自动报告]
✅ report_visibility_blocker("task-001", "api_timeout", "API 响应超时", "medium")

[用户视图]
🟡 查询 BNB MemeCoin Top3
━━━━━━━━━━━━━━━━━━━
进度：[██████████░░░░░░░░░░] 50% (2/4)
━━━━━━━━━━━━━━━━━━━
健康度：🟡 轻微延迟 (70/100)
当前阶段：连接 API
为什么还没完成：等待 API 响应（已 45 秒）
已运行：2 分钟

[每分钟自动更新]
🟡 查询 BNB MemeCoin Top3
━━━━━━━━━━━━━━━━━━━
进度：[██████████░░░░░░░░░░] 50% (2/4)
━━━━━━━━━━━━━━━━━━━
健康度：🟡 轻微延迟 (70/100)
当前阶段：连接 API
为什么还没完成：等待 API 响应（已 105 秒）
已运行：3 分钟
```

---

## 📊 进度条规范

### 文本进度条格式

```javascript
function generateProgressBar(progress, totalWidth = 20) {
  const filled = Math.floor((progress / 100) * totalWidth);
  const empty = totalWidth - filled;
  return `[${'█'.repeat(filled)}${'░'.repeat(empty)}] ${progress}%`;
}

// 示例
generateProgressBar(0)    // [░░░░░░░░░░░░░░░░░░░░] 0%
generateProgressBar(25)   // [█████░░░░░░░░░░░░░░░] 25%
generateProgressBar(60)   // [████████████░░░░░░░░] 60%
generateProgressBar(100)  // [████████████████████] 100%
```

### 状态展示模板

```
{statusIcon} {任务标题}
━━━━━━━━━━━━━━━━━━━
进度：{progressBar} ({currentStep}/{totalSteps})
━━━━━━━━━━━━━━━━━━━
健康度：{healthIcon} {healthText} ({health}/100)
当前阶段：{phase}
正在做什么：{action}
{optional: 为什么还没完成：{blockerReason}}
已运行：{elapsedMinutes} 分钟
```

---

## 🔄 每分钟自动更新机制

### 定时器逻辑

```javascript
// 任务启动时创建定时器
const timer = setInterval(() => {
  update_visibility_phase(
    task_id,
    current_phase,
    "update",
    current_progress,
    current_step,
    total_steps,
    auto_update_message  // "仍在等待 API 响应..."
  );
}, 60000); // 60 秒

// 任务完成时清除定时器
clearInterval(timer);
```

### 自动更新内容

- ✅ "已运行时间" +1 分钟
- ✅ 阻塞时间累积显示
- ✅ 健康度根据等待时间动态调整
- ✅ 进度条保持不变（如仍在同一阶段）

---

## 🚧 行为规范

### LLM 必须遵守（职业要求）

1. **任务属性感知** - 识别长任务属性（API/联网/多步）
2. **透明层优先** - create_visibility_task 是第一操作
3. **无法绕过** - 业务逻辑必须在透明层之内执行
4. **强制同步** - 每步操作后 + 每 60 秒自动更新
5. **及时报告** - 阻塞/介入立即报告
6. **文案具体** - 优先使用具体动作描述
7. **进度条展示** - 所有状态必须包含 `[████░░] XX%`
8. **时间显示** - 必须显示"已运行：X 分钟"

### 禁止行为（职业失职）

1. ❌ 绕过透明层直接执行业务
2. ❌ 依赖关键词匹配决定是否触发
3. ❌ 长时间不同步进度（>60 秒）
4. ❌ 显示空洞文案（"正在处理"）
5. ❌ 不显示进度条或进度百分比
6. ❌ 忘记每分钟自动更新
7. ❌ 将透明层视为可选工具

---

## 📈 成功标准

1. ✅ 用户 3 秒内看懂 Agent 在做什么
2. ✅ 用户知道为什么还没完成
3. ✅ 用户能分辨"正常等待"和"真的卡住"
4. ✅ 用户知道何时需要介入
5. ✅ **透明层覆盖率 100%**（所有长任务）
6. ✅ **同步及时率 100%**（每步 + 每分钟）
7. ✅ **进度条展示率 100%**（所有状态）
8. ✅ **Agent 无绕过行为**（职业合规）

---

## 📋 版本历史

| 版本 | 日期 | 内容 |
|------|------|------|
| v0.1.0 | 2026-03-18 | MVP 初始版本 |
| v0.2.0 | 2026-03-18 | Phase 2 验证 |
| v2.0.0 | 2026-03-18 | **主动工作协议重构** |
| v2.1.0 | 2026-03-19 | 进度条展示 + 每分钟自动更新 |
| v2.1.1 | 2026-03-19 | 扩展 autoTrigger 关键词 |
| v3.0.0 | 2026-03-19 | **系统级透明层 - 基于任务属性触发** |

---

## 🧪 测试验证

### 测试用例 1：Crypto 排行榜

```
输入："bnb memecoin top3"
预期：
1. 识别任务属性：外部 API + 联网
2. 自动启动 create_visibility_task
3. 显示进度条
4. 每 60 秒自动更新
```

### 测试用例 2：链上查询

```
输入："0x1234 持仓"
预期：
1. 识别任务属性：链上数据抓取
2. 自动启动 create_visibility_task
3. 显示进度条
4. 每 60 秒自动更新
```

### 测试用例 3：简单问答（不触发）

```
输入："1+1 等于几"
预期：
1. 识别任务属性：本地计算，无需 API
2. 不启动透明层
3. 直接回答
```

---

## 📄 完整文档

- **V3 设计文档：** `docs/v3_system_transparency_layer.md`
- **英文 README：** `README.md`
- **中文 README：** `README_CN.md`

---

## 🔒 安全说明

**本技能会修改 Agent 核心配置文件（SOUL.md / AGENTS.md），属于系统级行为变更。**

**修改范围：**
- 注入透明层协议到工作区文件
- 持久化生效（会话间保持）
- 需要读取环境变量（HOME, OPENCLAW_WORKSPACE）

**安全保证：**
- ✅ 不读取任何密钥/凭证
- ✅ 不进行网络请求
- ✅ 不修改技能自身目录外文件
- ✅ 可完全撤销（见下方）

**撤销方法：**
```bash
node ~/.openclaw/skills/agent-work-visibility/deactivate.js
```

---

## 🚀 安装与激活

### 手动激活（推荐）

**安装后手动运行激活脚本（可先审查代码）：**

```bash
# 1. 审查激活脚本（可选但推荐）
cat ~/.openclaw/skills/agent-work-visibility/activate.js

# 2. 运行激活
node ~/.openclaw/skills/agent-work-visibility/activate.js
```

### 激活后

1. ✅ 透明层协议已注入 `SOUL.md` 或 `AGENTS.md`
2. ✅ 下次会话自动生效
3. ✅ 无需额外配置

### 验证

```bash
# 开启新会话
# 发送："查询 bnb memecoin top3"
# 应该先显示进度条，再执行任务
```

### 撤销

```bash
# 移除透明层协议
node ~/.openclaw/skills/agent-work-visibility/deactivate.js
```

---

## 🤝 Contributing

欢迎贡献！查看 [README.md](README.md) 获取开发指南。

**License:** MIT

---

**让长任务不再黑箱，让用户更安心。**

**This is not a skill. This is professional conduct.**

**安装即用，无需手动配置。**
