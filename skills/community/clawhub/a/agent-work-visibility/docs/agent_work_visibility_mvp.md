# Agent Work Visibility MVP - 设计文档

**项目代号：** `agent_work_visibility_mvp`  
**版本：** v0.1.0  
**日期：** 2026-03-18

---

## 一、问题定义

### 核心痛点

当 Research Agent / Browser Agent 执行 3 分钟以上的长任务时，用户会经历：

1. **焦虑** - 不知道 Agent 是不是卡住了
2. **无助** - 不知道要不要介入、何时介入
3. **黑箱感** - 只有一个 loading 转圈，没有任何进展信息
4. **不可预期** - 不知道还要等多久

### 现有方案的不足

| 方案 | 问题 |
|------|------|
| 纯 Loading 动画 | 用户不知道在做什么、为什么还没完成 |
| 假进度条（37% / 82%） | 数字无意义，无法解释"为什么卡在这里" |
| 原始系统日志 | 技术术语太多，用户看不懂 |
| 复杂 Trace UI | 给开发者看的，不是给 power user 看的 |

---

## 二、目标用户

### 主要用户画像

**重度使用 Agent 的 Power User：**

- 依赖 Agent 做调研、搜索、比较、整理、写初稿
- 不是底层开发者，不想看复杂 trace
- 但又不能接受完全黑箱
- 愿意在必要时介入提供决策

### 典型使用场景

1. **市场调研** - "帮我调研 AI Agent 专用的区块链项目"
2. **竞品分析** - "比较 5 个类似产品的功能和定价"
3. **信息收集** - "收集最近 3 个月关于 X 的新闻和报告"
4. **文档整理** - "从 10 个网页提取关键信息并整理成表格"

---

## 三、核心场景

### 场景 1：正常长任务执行

```
用户启动任务 → Agent 开始执行 → 用户 periodic 查看进度
                                    ↓
                        用户能看到：
                        - 当前在做什么
                        - 为什么还没完成
                        - 是否需要介入
```

### 场景 2：遇到阻塞

```
Agent 遇到 API 超时/信息冲突/缺少输入
            ↓
      自动识别阻塞类型
            ↓
   显示阻塞原因 + 推荐操作
            ↓
   用户决定：等待 / 跳过 / 介入
```

### 场景 3：需要用户决策

```
Agent 发现多个方向都可深入
            ↓
    无法自动判断优先级
            ↓
   主动 Ask Human + 提供选项
            ↓
   用户选择 → Agent 继续执行
```

---

## 四、MVP 范围

### 做什么（In Scope）

| 模块 | 功能 | 优先级 |
|------|------|--------|
| 任务状态管理 | 维护任务状态和阶段状态 | P0 |
| 动作翻译 | 把底层事件翻译成自然语言 | P0 |
| 阻塞检测 | 识别等待、报错、缺输入、需人介入 | P0 |
| 视图渲染 | 生成默认视图和展开视图 | P0 |
| Ask Human | 构造用户介入问题与选项 | P0 |
| 进度计算 | 按阶段加权计算完成度 | P1 |

### 不做什么（Out of Scope）

| 内容 | 原因 |
|------|------|
| 复杂通用平台 | 第一版只聚焦 Research 场景 |
| 多 Agent 依赖图 | V3 再考虑 |
| 开发者级 Tracing UI | 目标用户是 power user，不是开发者 |
| 过度工程化 Schema | 保持简单可扩展 |
| 复杂 Dashboard | 默认视图要极简 |
| 假进度条 | 文字解释优先于百分比 |

---

## 五、状态模型

### 任务整体状态（8 种）

```
pending     → 等待开始
planning    → 规划中
running     → 执行中
waiting     → 等待外部响应（正常）
blocked     → 被阻塞（需要关注）
reviewing   → 复核中
completed   → 已完成
failed      → 失败
```

### 阶段状态（5 种）

```
pending     → 等待中
in_progress → 进行中
completed   → 已完成
blocked     → 被阻塞
skipped     → 已跳过
```

### 阻塞级别（4 级）

```
none   → 无阻塞
low    → 轻微阻塞（可自动恢复）
medium → 中等阻塞（可能需要用户关注）
high   → 严重阻塞（需要用户介入）
```

---

## 六、数据结构

### 任务状态对象

```javascript
{
  // 基础信息
  task_id: string,
  task_title: string,
  task_type: 'research' | 'browser',
  
  // 整体状态
  overall_status: OverallStatus,
  current_phase: string | null,
  progress_percent: number,
  
  // 阻塞状态
  blocker_status: BlockerLevel,
  blocker_reason: string | null,
  blocker_type: BlockerType | null,
  blocker_since: ISO-8601 | null,
  
  // 用户介入
  needs_user_input: boolean,
  user_input_type: UserInputType | null,
  user_question: string | null,
  user_options: string[],
  
  // 行动指引
  current_action: string | null,      // 当前在做什么
  why_not_done: string | null,        // 为什么还没完成
  next_action: string | null,         // 下一步做什么
  recommended_user_action: string | null,
  
  // 时间戳
  started_at: ISO-8601,
  updated_at: ISO-8601,
  completed_at: ISO-8601 | null,
  
  // 阶段列表
  phases: Phase[],
  
  // 动作日志（最近 10 条）
  action_log: LogEntry[],
  
  // 重试记录
  retry_log: RetryEntry[]
}
```

### Research 固定 5 阶段

| 阶段 | 权重 | 说明 |
|------|------|------|
| 理解任务 | 10% | 解析用户需求，明确任务目标 |
| 制定搜索计划 | 15% | 设计搜索策略，确定关键词 |
| 收集信息 | 30% | 执行搜索，抓取网页，提取数据 |
| 分析与比较 | 30% | 整理信息，交叉验证，对比分析 |
| 形成输出 | 15% | 生成结论，撰写报告 |

---

## 七、交互原则

### 渐进披露

**默认视图（第一层）- 3 秒看懂：**

- 任务标题
- 当前状态
- 当前阶段
- 当前在做什么
- 为什么还没完成
- 下一步
- 是否需要你

**展开视图（第二层）- 主动查看：**

- 阶段列表（5 阶段进度）
- 最近动作日志
- 重试记录
- 阻塞详情

### 文字优先

```
❌ 进度：37%
✅ 正在比较 3 个重点项目的定位与差异

❌ 阻塞：API_TIMEOUT
✅ 外部 API 响应超时（已持续 2 分钟）

❌ blocked: true
✅ 需要用户决策：请选择优先深入的方向
```

### 阻塞必须 Actionable

不能只说 "blocked"，要告诉用户：
- 阻塞原因是什么
- 已经持续多久
- 推荐用户做什么

---

## 八、对外接口

### 核心 API

```javascript
// 任务创建
create_task(task_title, task_type="research")

// 阶段管理
start_phase(task_id, phase_name)
update_phase_progress(task_id, phase_name, progress)
complete_phase(task_id, phase_name)
complete_task(task_id)

// 日志与事件
log_raw_event(task_id, event)
add_human_readable_action(task_id, message)

// 阻塞管理
mark_blocked(task_id, reason, level)

// 用户介入
request_user_input(task_id, question, options)
resolve_user_input(task_id, answer)

// 视图获取
get_user_snapshot(task_id)       // 默认视图
get_expanded_snapshot(task_id)   // 展开视图
```

---

## 九、成功标准

### 产品效果验收

- [x] 用户能在 3 秒内看懂 Agent 当前在干什么
- [x] 用户能知道为什么还没完成
- [x] 用户能明确分辨"正常等待"和"真的卡住"
- [x] 用户知道何时需要自己介入
- [x] 默认视图信息不过载
- [x] 在 Research 长任务场景中明显优于"只有一个转圈 loading"

### 技术验收

- [x] 成功输出 current_state
- [x] 成功输出 why_not_done
- [x] 成功识别 blocked
- [x] 成功生成 ask-human 请求
- [x] 成功生成 next_action
- [x] 每次都能输出 user-readable snapshot
- [x] 15 项基础测试全部通过

---

## 十、默认视图格式

### 正常运行状态

```
任务：调研 AI Agent 专用区块链
状态：运行中
当前阶段：分析与比较

当前在做什么：
正在比较 3 个重点项目。

为什么还没完成：
还有 2 个项目的信息需要交叉验证。

下一步：
形成一页结论摘要。

是否需要你：
暂时不需要。
```

### 阻塞状态

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

### 需要用户介入

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

问题：请选择优先深入的方向
选项：
  - [A] 底层链设计
  - [B] Agent 通信协议
  - [C] 代币机制与激励
```

---

## 十一、文件结构

```
agent-work-visibility/
├── SKILL.md                      # 技能入口文档
├── README.md                     # 使用指南
├── docs/
│   └── agent_work_visibility_mvp.md  # 设计文档（本文件）
├── src/
│   ├── schema.js                 # 状态 Schema 定义
│   ├── phases.js                 # 阶段模型（5 阶段）
│   ├── logger.js                 # 动作日志 + 事件翻译
│   ├── blocker.js                # 阻塞识别
│   ├── ask-human.js              # 用户介入队列
│   ├── progress.js               # 进度计算
│   ├── renderer.js               # 视图渲染
│   └── index.js                  # 统一 API 入口
├── examples/
│   └── sample-output.md          # 示例输出
├── demos/
│   ├── demo1_normal.js           # 正常 research 流程
│   ├── demo2_blocked.js          # 阻塞 + 用户介入
│   └── demo3_retry.js            # 超时重试（可选）
└── tests/
    └── basic.test.js             # 基础测试
```

---

## 十二、Roadmap

### V2（下一步）

| 功能 | 说明 |
|------|------|
| Confidence Score | 证据完整性评分，帮助用户判断结果可信度 |
| 更丰富的任务类型 | Browser Agent、Data Processing 等专用阶段模型 |
| 更好的 ETA | 基于历史数据的剩余时间预估 |
| 通知机制 | 阻塞/完成时主动推送通知到 Telegram/微信 |

### V3（多 Agent）

| 功能 | 说明 |
|------|------|
| 多 Agent 任务树 | 展示多个子任务的依赖关系 |
| Agent 依赖关系 | 识别哪些任务在等哪些任务 |
| Bottleneck 识别 | 自动发现拖慢整体进度的 Agent |
| Manager 面板 | 总览所有 Agent 的工作状态 |

### V4（开发者工具）

| 功能 | 说明 |
|------|------|
| Developer Trace Mode | 展开视图显示原始事件和 trace |
| Observability Integration | 对接 Datadog、Sentry 等监控平台 |
| SDK / Protocol 化 | 提供标准协议，让其他 Agent 框架接入 |

---

## 十三、边界声明

### 第一版明确边界

- ✅ 只服务 research / browser 长任务
- ✅ 只服务单 Agent 主流程
- ✅ 只做默认视图 + 展开视图
- ✅ 只做最必要的 ask-human 机制
- ❌ 不做大而全平台
- ❌ 不做多 Agent 协作
- ❌ 不做开发者级 tracing

### 设计原则

**宁可简单，不要过度设计。**

第一版的目标是验证"工作透明层"的价值，而不是构建通用平台。如果 MVP 证明用户确实更安心、更愿意使用长任务功能，再考虑扩展到 V2/V3。

---

## 十四、版本历史

| 版本 | 日期 | 内容 |
|------|------|------|
| v0.1.0 | 2026-03-18 | MVP 初始版本，Research 场景 |

---

## 十五、参考

- 产品需求文档：用户原始需求描述
- 技能文档：`SKILL.md`
- 使用指南：`README.md`
- 示例输出：`examples/sample-output.md`
