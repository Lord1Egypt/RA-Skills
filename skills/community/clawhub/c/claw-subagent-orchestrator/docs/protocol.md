# Sub-agent 协作协议 — 完整设计

## 背景

主 session 上下文有限（当前模型 1M window），重任务（搜索/分析/写作）会快速膨胀上下文，触发 FIFO 截断丢失关键内容。解决方案：将重任务委派给子 session，子 session 干完即消失（cleanup=delete），主 session 只保留极轻量的 spawn+announce 开销。

设计目标：
- 主 session 不做重活，上下文增长极慢
- 子 session 自给自足（带技能 + 协议），不需要主 session 手把手教
- 崩溃可恢复，信息零损耗
- 技能优化有数据闭环

---

## 协议流程

### 阶段 1：主 session → 子 session

```text
[ROUTINE]
协议: skills/subagent-orchestrator/SKILL.md
技能: <skill-name>
工作空间: workspace/<task-id>/
通知用户: true/false
任务: <一句话任务描述>
```

主 session **不预处理任务内容**，原始需求原样传递。避免：
- 额外的 token 消耗
- 信息传递中的编码损耗
- 主 session 上下文膨胀

### 阶段 2：子 session 启动

子 session 收到任务后，按顺序：
1. 读 `skills/subagent-orchestrator/SKILL.md` → 了解协作协议
2. 读 `skills/<skill-name>/SKILL.md` → 了解怎么干活
3. 初步分析任务 → 拆解出 checklist
4. 在工作空间创建 task.md

### 阶段 3：task.md（checklist）

```text
[start done]
[working done] 步骤1描述
[working done] 步骤2描述
[working] 步骤3描述
[end]
```

- 只在状态切换时写入（步骤开始 / 步骤完成 / 整体结束）
- 中间推理过程不写入 task.md
- 崩溃恢复时：扫到第一个 `[working]` 且没有对应的 `[working done]`，从这里继续

### 阶段 4：step 记录文件

每个 `[working]` 步骤对应一个同名 .md 文件：

```
workspace/task-xxx/
├── task.md               ← checklist only
├── 步骤1描述.md           ← 思考过程 + 工具调用
├── 步骤2描述.md           ← 同上
└── 步骤3描述.md           ← 同上
```

文件名和 `[working]` 行描述完全一致，零 mapping 成本。

写入方式：直接 write 创建新文件（不是 read+edit 插入），节省 token。

### 阶段 5：输出

```
通知用户: true 且渠道可投递时：
  子 session 最后一步：message 直发微信/Telegram等 + assistant reply 摘要
  主 session 收到 announce：确认，不重复发

通知用户: true 但本地直连时：
  渠道为 openclaw-control-ui 等本地终端，无外部投递目标
  子 session 不拿 message 权限
  结果由主 session announce 自然呈现

通知用户: false 时：
  子 session 最后一步：assistant reply 完整结果
  主 session 收到 announce：转发给用户
```

---

## 崩溃恢复流程

### 检测

子 session 完成（或超时/崩溃）后，主 session 收到 announce：
- Status = `failed` / `timed out` → 进入恢复流程
- 检查 task.md 是否有 `[end]` → 没有则视为崩溃

### 恢复

```
旧子 session 崩溃
    │
    ▼
主 session 检查 task.md：
  - 有 [end] → 正常退出，看 retro
  - 无 [end] → 进入恢复
    │
    ▼
主 session spawn 新子 session：
  "[ROUTINE]
  协议: skills/subagent-orchestrator/SKILL.md
  技能: <skill-name>
  工作空间: workspace/<task-id>/
  通知用户: true/false
  动作: 接续
  任务: 从 task.md 第一个未完成的 [working] 继续"
    │
    ▼
新子 session：
  读 task.md → 找到下一个 [working]
  读 步骤N.md → 了解已做的思考过程
  从失败点继续执行
  完成后追加 [working done] 和后续步骤
```

### 恢复成本

```
旧 session A: ~30K（cleanup=delete 消失）
主 session:   检查 task.md → ~0.5K
新 session B: 读 task.md(~0.3K) + 读 步骤N.md(~2K) = ~2.3K
总计:         ~2.8K
```

比主 session 自己理解再重喂（~3.5K）省 20%，且信息零损耗。

---

## 技能优化闭环

正常完成的任务（走到 `[end]`），可 spawn 一个轻量子 session 做回顾分析：

```
回顾子 session：
  → 读工作区所有文件
  → 提取：
    - 各步骤耗时
    - 异常类型和频率
    - 是否需要更新 skill
  → 输出 task-retro.md
```

如果发现同一 skill 的同一步骤多次出现同一类型错误：
- 自动标记 skill 需要更新
- 输出错误模式报告
- 供主 session 判断是否要修改 SKILL.md 或脚本

---

## 约定总结

| 角色 | 职责 | 上下文增长 |
|---|---|---|
| 主 session | 路由、spawn、确认 announce | 低（每次 ~0.5K） |
| 子 session | 干重活、写文件、发微信 | 高（~20-50K），干完消失 |
| 回顾子 session | 复盘、优化分析 | 低（~5K），干完消失 |
