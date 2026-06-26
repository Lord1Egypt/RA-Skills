# Debate Arena Skill — 辩论流程规范（Publishable）

> Keywords: 辩论 / debate / arena / 对抗 / 投票 / 裁判
> 说明：本 skill 对“使用者（人类）”暴露的是一组**主命令 `debate`（中文别名：`辩论`）**。
> 你在群里输入这些命令即可；背后由主控 Agent 调用脚本 `scripts/debate-arena.js` 维护状态、编排多 Agent 发言、归档与投票。

本 skill 支持：
- **人员选择**：`pros / cons / judge / host`，并可通过 `debate conf` 保存为默认配置
- **飞书显示**： 消息由发言人自动发送到群，更具沉浸感
- **默认五轮次**：开篇立论 / 深化论点 / 交叉辩论 / 关键攻防 / 总结陈词（可配置 1–5）
- **自动推动轮次**：`autonext=true` 默认开启
- **真人投票**：辩论方不可投票；支持多个投票人；默认 sponsor / host / judge（每人总票数=3）
- **发言归档**：辩论观点、裁判点评、打分与结果归档到本地文件
- **辩论质量要求**：对论据数量/质量/表达形式提出硬性要求，并可注入额外提示词（`debate set prompt`）
```
字数：约200字
至少 3 条明确论据，每条论据需具体、可检验或可验证, 有实例最佳 
表达形式：编号/分点输出，避免泛泛而谈
结构：针对性回应对方观点（如果必要） → 核心论点 → 论据展开 → 反驳回应 → 总结
态度：坚定有力，逻辑严密,
```
---

## 一、命令概览（用户在群里直接输入）

主命令：`debate`（中文别名：`辩论`）

- `debate init <话题>`：初始化（**仅此命令作为启动入口**）
- `debate add <pros|cons|judge|host> <agentId>`：设置角色
- `debate add voter <agentId>`：添加投票人（禁止正/反方）
- `debate set rounds <1-5>`：设置轮次
- `debate set autonext <true|false>`：设置自动推进
- `debate set prompt <补充要求>`：设置辩论要求（`clear/none/无` 清空）
- `debate set <pros|cons|judge>.model <alias>`：指定 subagent model
- `debate set <pros|cons|judge>.thinking <mode>`：指定 thinking 模式
- `debate set <pros|cons|judge>.timeout <seconds>`：指定超时秒数
- `debate set <pros|cons|judge>.accountId <id>`：指定发送账号
- `debate conf`：保存为默认配置（可选，仅用于持久化）
- `debate start`：启动辩论（init 后即可；需确保 pros/cons 为真实 agentId）
- `debate next`：手动推进下一轮（仅在 `autonext=false` 时使用）
- `debate status`：查看状态
- `debate stop`：强制结束
- `debate reset`：重置到 IDLE

> `agentId` 是你环境里可用的 Agent 标识（用 `<agentId>` 表示占位）。

---

## 二、核心流程

### 1) 日常使用（最小可用）

```text
辩论 init <新话题>
辩论 start
```

> 若已保存默认配置，init 会自动加载；如需调整，可用 add/set 修改后再 start。
> conf 仅用于把当前配置保存为默认配置（可选）。

### 2) （首次使用）设置角色 + 配置

> ⚠️ 说明：以下为**格式示例**，用于告诉“人类用户”应该怎么输入命令。
> - **不得**把示例当作需要自动执行的指令序列。
> - 程序/助手只能执行用户在群里**明确输入**的那一条命令。

```text
辩论 init <新话题>

debate add host <agentId>
debate add pros <agentId>
debate add cons <agentId>
# 可选：裁判
debate add judge <agentId>

# 可选：加投票人（注意：正/反方禁止投票）
debate add voter <agentId>

# 可选：轮次、推进方式、质量要求
debate set rounds 5
debate set autonext true
debate set prompt <补充发言要求>

# 可选：为正/反/裁判指定模型与超时（按需）
debate set pros.model <alias>
debate set pros.thinking <mode>
debate set pros.timeout <seconds>
debate set pros.accountId <accountId>

# 启动辩论（必须显式执行）
debate start

# （可选）保存为默认配置（仅用于持久化）
debate conf
```

系统会按轮次驱动正反方（以及裁判）发言。

### 发言要求（默认，可通过 set prompt 调整）

默认对每轮发言的质量要求如下（可在 `debate set prompt ...` 中覆盖/追加）：

【发言要求】
- 字数：约200字
- 至少 3 条明确论据，每条论据需具体、可检验或可验证
- 表达形式：编号/分点输出，避免泛泛而谈
- 结构：针对性回应对方观点（如果必要） → 核心论点 → 论据展开 → 反驳回应 → 总结
- 态度：坚定有力，逻辑严密

调整方式：
- `debate set prompt <你的补充要求>`：覆盖/追加发言要求（对正/反/裁判的提示词统一生效）
- `debate set prompt clear`：清空补充要求，恢复默认要求

### 3) 自动 / 手动推进辩论

- 若 `autonext=true`：系统在每轮发言归档后自动推进
- 若 `autonext=false`：每推进一轮需要你输入：

```text
debate next
```

---

## 三、投票阶段（规则与用法）

### 规则（强制）

- 默认投票人：sponsor / host / judge（也可 `debate add voter ...` 增加）
- **辩论方不可投票**（正方/反方禁止投票）
- 每位投票人 **总票数必须=3**（例如 `2-1`、`3-0`）

### sponsor（出题用户）如何投票

在群里直接发：
- `2-1` 或
- `投票 2-1`

Host 会解析并记录。

> 说明：host/judge 的票通常由系统自动完成；你只需要投 sponsor 的票即可（除非你们配置成多人都手工投票）。

---

## 四、群聊上下文（context，init 自动绑定）

- 你在**哪个群**里 `debate init`，辩论消息就只会回到这个群。
- `debate init` 时会自动绑定当前群聊上下文（无需手工设置）。

---

## 五、调用方式（脚本/API）

脚本入口：`scripts/debate-arena.js`

说明：该脚本提供的是一组 **API 函数（cmdInit/cmdStart/cmdNextRound/…）**，属于 Node.js 模块（`module.exports = { ... }`），不是一个“直接执行就能解析参数”的 CLI。

> 推荐做法：在脚本所在目录，用 `node -e` 调用导出的 cmd* 方法进行本地验证/调试。

### 1) 最小调用：reset / init / status

```bash
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdReset());"

# init 的第二个参数是群上下文；本地测试可填 dummy 值
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdInit('AI 会取代大多数工作吗', {channel:'feishu', target:'chat:oc_xxx', chatType:'group'}));"

node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdStatus());"
```

### 2) 配置角色并开始

> 注意：`pros/cons` 必须设置为真实 `agentId`（用 `<agentId>` 表示占位），否则 `cmdStart()` 会拒绝启动。

```bash
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('host','<agentId>'));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('pros','<agentId>'));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('cons','<agentId>'));"

# 可选：裁判
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('judge','<agentId>'));"

# 启动辩论（返回 nextAction/hostPrompt，以及 speaker 的 spawn spec）
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdStart());"

# （可选）保存为默认配置
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdConf());"
```

### 3) 推进下一轮

```bash
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdNextRound());"
```

### 4) 修改配置：轮次 / autonext / prompt

```bash
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdSet('rounds', 3));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdSet('autonext', false));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdSet('prompt', '每轮至少3条可验证论据，分点编号输出'));"
```

---

## 六、约束与容错

### 角色约束

- **最低配置**：正方 + 反方 + 主持人（3 个不同 agent），裁判可选
- **agent 唯一性**：同一 agent 不能担任多个角色（正方≠反方≠裁判≠主持人）
- **主持人独立性**：主持人不能同时担任辩手
- **agentId 须真实**：`pros/cons/host` 必须设置为环境中可用的 agentId

### 群聊约束

- **自动绑定**：`debate init` 自动获取当前群聊上下文（channel/target/chatType），无需手动配置
- **单群绑定**：init 后 context 锁定，所有消息发送到同一群
- **群聊类型不限**：飞书/微信/Slack/Telegram 等均可

### 容错策略

- **缺 judge**：裁判点评/投票会跳过，投票人集合自动调整。
- **归档失败**：通常为目录权限或路径错误；检查 `DEBATE_ARENA_ARCHIVE_DIR` 与写权限。
- **投票失败**：票数校验不通过或重复投票会返回 error；按提示重新提交正确票数。

---

## 七、日志与文件位置

默认路径（可通过环境变量覆盖）：
- Data dir: `~/.openclaw/debate-arena/`
- Default config: `~/.openclaw/debate-arena/default-config.json`
- State: `~/.openclaw/debate-arena/debate-state.json`
- Archive dir: `~/.openclaw/debate-arena/archives/`
- Log: `~/.openclaw/debate-arena/debate-state.log`

说明：
- `default-config.json` 仅在执行 `debate conf` 后生成/写入。
- 若需要清理为“真·首次使用”，可删除该文件：`rm ~/.openclaw/debate-arena/default-config.json`。

环境变量：
- `DEBATE_ARENA_STATE_FILE`（同时影响 log 所在目录）
- `DEBATE_ARENA_ARCHIVE_DIR`

---

## 版本

- v2.8：新增角色约束（agent 唯一性 + 最低 3 人 + 主持人独立），SKILL.md 约束章节
- v2.7：发言结构升级（新增"针对性回应对方观点"第一步）
- v2.6：辩论历史传递修复（正反方+裁判可见全部发言）
- v2.5：安全修复，移除参与方本地命令归档方式，改为主持人回传正文归档。
- v2.4：文档收敛（去除重复入口描述）、归档说明合并到日志章节、群消息发送约束更明确、默认参与者更泛化。
- v2.3：默认配置持久化（default-config）、多投票人（voters/votes）、裁判点评归档、文档完善。
- v2.2：新增 context（init 自动绑定）与 spawn 配置、完善容错说明。
- v2.1：轮次可配置、autonext、投票严格校验、裁判点评与投票分离。
