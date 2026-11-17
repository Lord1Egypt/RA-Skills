# 进化燃料 · 信号规范（锻造炉版 v0.4 · 本地安装即开 + 云端上传默认关需显式开启 · 双模态）

> **按需加载**：处理信号采集/上传/被动捕获/云同步相关任务时读取本文件；纯锻造/审视会话不必加载。
> 本文件定义「技能锻造炉」自身的**本地脱敏信号日志**机制（复用扫地僧 v0.4 双模态骨架，按锻造炉语义定制 L1–L7 层码）。
> **两层授权**：①本地记录**安装即开**（安装时默认开启、首次对话提醒、可关）；②云端回传藏经阁·易筋平台**默认关，需显式说"开启云同步"才上传**（零原文零身份、匿名端点、零注册）。不主动开启则永不上传，本地记录不受影响。
> 飞轮转的是「方法层标签」，不是「用户数据」。即使日志意外泄露，也不含任何可还原的内容。
> **幂等键**：每行采集时生成 `signal_id`（UUIDv4），一路带到落库；服务端即便收到两次同 `signal_id` 也只落一条（见 §七 + 服务端 `client_signal_id` 唯一约束）。

## 一、何时记（会话钩子 + 收尾信号块）

**会话结束**（每次锻造/审视/重铸/清晰化会话收尾时，由 SKILL.md A.2 会话钩子执行）：若本地记录已开（安装即开，`.optin` 默认 `on`），向 `signals-log.jsonl` 追加一行 JSONL 方法层信号，并在对话末尾输出**收尾信号块** `[信号] L<层>·<事件>`（off 时输出 `[信号] off`）——收尾块是用户可验证的完成凭证。

**会话开始**（首次交互时静默执行，一条命令）：`scripts/session_hook.py start` —— 内部自动补传（`upload_signals.py`）+ 拉回合并（`download_signals.py pull`，幂等，与定时器重复无害；未开云同步则跳过）+ 缺失检测。

**缺失检测（把沉默变可见）**：若上次会话未留下收尾信号块（`.optin=on` 且曾使用），本次会话开始钩子记录一行 `L0·no_signoff` 信号（`event=no_signoff`，`method_layer=L0`，无 metric）——证明会话发生过但 Agent 未打标签，让"没记"本身成为可见信号（供监控/整改）。首跑（无 `.session_state.json`）不检测防误报；收尾用 `scripts/session_hook.py end --event L<层>:<事件>` 写标准信号并标记已收尾（禁止手写 signals-log JSON）。

- 仅记录**方法层信号**（用了哪层能力、准不准、是否被纠正/放弃）。
- 不记录问答内容、不记录用户身份。
- 用户说「别记了」→ 关闭本地记录，停止写日志。

## 二、记什么（仅方法层标签，零原文 / 零 PII）

```json
{
  "ts": "2026-07-30T03:00:00+08:00",
  "signal_id": "3f1a2b9c-7d4e-4c8a-9b2f-1e6c5d4a3b21",
  "skill_slug": "cjg-skill-forge",
  "skill_version": "2.9.9",
  "method_layer": "L3",
  "event": "helpful",
  "weight": 5,
  "note": "覆盖审计",
  "anon_id": "<本机一次性随机UUID>"
}
```

> **`signal_id` 为必填**：采集时生成（UUIDv4），是端到端去重的幂等键。没有它就无法防重复（见评审 §四问 + §七）。

| 字段 | 含义 | 取值 |
|------|------|------|
| `ts` | 本地时间戳 | ISO8601 |
| `signal_id` | **幂等键** | UUIDv4，采集时生成 |
| `skill_slug` | 技能标识 | `cjg-skill-forge` |
| `skill_version` | 本次应答时的技能版本号 | 如 `2.9.9`，用于检测发版后完成率骤降 |
| `method_layer` | **层码**（L1–L7，见下表） | 由 agent 直写，不再依赖文件→层码解析 |
| `event` | 会话信号推断的事件类 | 6 类之一（见下表） |
| `weight` | 信号强度 | 1–5 整数 |
| `note` | 触发类 / 主题标签 | 仅方法层类目标签 |
| `anon_id` | 本机一次性随机匿名 ID | UUIDv4，存于 `.anon_id` |
| `accepted` | **采纳标记（P0 闭环）** | `1/0/true/false`，仅 `accept`(=1)/`reject`(=0) 事件填；其余事件 NULL。**前瞻判断，不代表已验证有效**（验证在 P1 回环闭合） |
| `revision_rounds` | **修订轮次（P0 闭环）** | 整数 1–50；accept 时填「该建议最终定稿轮次」（首轮采纳=1），iteration 时填「当前轮次」 |
| `feedback_tag` | **错题分类（P0 闭环）** | 受控枚举：`boundary`/`format`/`desensitivity`/`accuracy`/`other` |
| `recurrence` | **同反馈复发标记** | `1/0/true/false`，同一反馈反复出现时计 |
| `attribution` | **归因（P0 闭环）** | `agent`/`skill`/`harness`/`unknown`（harness=运行时/工具可用性；unknown 交 P1 人审） |
| `attribution_note` | **归因备注** | ≤255 位字符串，服务端强制 `pii_scrub` 脱敏 |
| `action_name` | **动作名（P1-4 动作链遥测）** | 小写 snake_case 白名单标签（≤48 字符），见 §八；零 PII |
| `action_outcome` | **动作结果（P1-4）** | `success` / `fail` / `partial` / `skip` |

### L1–L7 层码（锻造炉语义）

| 层码 | 能力层 | 典型触发 |
|------|--------|----------|
| `L1` | 立项 / 范围（Scoping） | 立项优先、目标用户 / MVP / 边界 / 不做清单 |
| `L2` | 锻造循环（Forge loop） | v1.0 脚手架 → v1.x 反馈轮 → 标杆 / 自审 |
| `L3` | 真实化（Realization） | 覆盖审计 / 外部标杆 / 真机测试（让技能"真能跑、全球最牛"） |
| `L4` | 审视评分（Review rubric） | 10 维加权评分尺、反模式检查 |
| `L5` | 重铸整合（Recast） | 技能库聚类 / 三维打分 / 合并计划 |
| `L6` | 内嵌清晰化（Embedded clarity） | S7 四维（D1–D4）+ 保真红线 |
| `L7` | 发布闸门（Publish gates） | S8 可推广 + 纪律13/17 安全审计 + last-mile 闭环 |

### event 枚举（11 类：6 推断类 + 4 闭环类 + 1 行为遥测类）

> 第 11 类 `action_trace` 为 P1-4 新增的**行为层遥测**（与语义事件「为什么好用」、客观事件「用多少」正交互补），详见 §二·八。

**6 类基础事件（由 Tier 0 对话信号推断）：**

| event | 触发信号 |
|-------|----------|
| `helpful` | 用户采纳了锻造建议 / 顺着做下去了 |
| `unhelpful` | 用户纠正了锻造判断 / 重做了 |
| `confusion` | 用户被锻造指令搞糊涂了（步骤含糊 / 触发飘） |
| `suggestion` | 用户提出了对锻造炉自身的改进建议 |
| `abandoned` | 用户中途放弃本次锻造 / 审视 |
| `misdiagnosis` | 锻造炉给了错误的方法论建议（被指出或事后发现） |

**4 类闭环事件（P0 新增，触发源见 §二·五）：**

| event | 触发信号 | 填哪些 P0 字段 |
|-------|----------|----------------|
| `accept` | 用户**显式「采纳 / 应用」**了 AI 提议的修改（「继续」「执行」等仅表推进已共识方案，**不计**） | `accepted=1` + `revision_rounds` + `attribution`（可 NULL 交 P1 人审） |
| `reject` | 用户**明确驳回** AI 提议的修改，或会话结束未采纳 | `accepted=0` + `feedback_tag`（按驳回原因分类，可 NULL） |
| `iteration` | AI 据用户反馈对**同一修改建议**重新生成 / 修订（进入第 N 轮） | `revision_rounds=N` + `recurrence`（复发计） |
| `edit_capture` | 用户在**任何上下文**手改技能文件（由 `capture_skill_edits.py` 哈希 diff 自动记录，非 AI 主动发） | 无（`note` 记 `<add|modify|delete>:<相对路径>`，`attribution` 恒 NULL） |

### 二·五 迭代闭环信号（P0 · accept/reject/iteration 谁在何时发）

> 权威行为规格（GAP-1 闭合）：见 `skill2loop-p0-review-2026-08-21.md` §2.5。本节为信号侧落文档。

**触发语境（只有"AI 主动提议修改某技能"时才发）：**

| 事件 | 写点（SkillForge 逻辑内） | 防误发边界 |
|------|---------------------------|------------|
| `accept` | 用户对 AI 提议的修改做**显式「采纳 / 应用」确认后**（AI 随后执行 apply 是其机械后果，不作为判定条件） | 「继续」「执行」「按既定方案推进」等仅表推进已共识方案，**不计为 accept**；纯使用技能、无修改提议 → 不发 |
| `reject` | 用户**明确驳回 / 拒绝** AI 提议后，或会话结束未采纳 | 驳回才发；单纯未提建议不发 |
| `iteration` | AI 收到用户反馈后，对**同一修改建议**重新生成 / 修订（进入第 N 轮） | 不同建议各自独立计轮；`revision_rounds` 填当前轮次 |

**写入通道**：与 `upload_signals.py` 同源的本地 log 写入，向 `<skill_dir>/signals-log.jsonl` append 一行（不新建通道、不新建表）。采集关（`.optin=off`）则上述事件不写。产生 accept/reject/iteration 时沿用 A5 可见标记在对话中告知「本次已记录你的采纳/驳回/修订」。

**JSON 形状（权威示例，与 §二 字段表一致）：**

```json
{"ts":"...","signal_id":"<uuid>","skill_slug":"cjg-skill-forge","skill_version":"<ver>","method_layer":"L2",
 "event":"accept","weight":4,"accepted":1,"revision_rounds":1,"feedback_tag":null,
 "recurrence":0,"attribution":"skill","attribution_note":null,"anon_id":"<本机uuid>"}
```

**语义边界**：`accepted` 记录的是用户「前瞻判断」，不代表改动已被验证有效（验证在 P1 回环闭合：对比采纳前后采纳率）；看板不可把 `accepted=1` 解读为"已证明好用"。`revision_rounds` 语义：accept 时填「该建议最终定稿的轮次」（首轮采纳=1），iteration 时填「当前轮次」。

### 二·六 被动改动捕获（P0 · edit_capture）

> 由 `scripts/capture_skill_edits.py` 自动完成（每日 23:30 上传触发时在 `upload_signals.py` 之后调用）。

- **机制**：维护 `<skill_dir>/.skill_edit_baseline.json`（`{ "<相对路径>": "<sha256 前16位>" }`，范围仅 `SKILL.md` / `references/*` / `scripts/*`）；首跑仅建基线不产信号；后续 diff 出增/改/删 → append 一行 `edit_capture` 信号（`note` = `<add|modify|delete>:<相对路径>`）。
- **默认本地、零云默认**：`edit_capture` 只写本地 `signals-log.jsonl`；是否上行云由既有 `.cloud_optin` 控制（延续双模态），与闭环事件同一通道。
- **只读红线（不可逾越）**：捕获脚本**绝不写入/修改/删除任何技能内容文件**，只读哈希 + 写运行时产物（`.skill_edit_baseline.json` / `signals-log.jsonl`）。P0 阶段只度量、不改动；自动改进写回（loop apply）将在后续版本提供。
- **隐私**：只记相对路径 + kind，不读文件内容、不记绝对路径/用户名（零 PII）。`.skill_edit_baseline.json` 同 `.optin` 等为运行时产物，不进包/不进 git。
- **用户控制**：说「别记了」关本地采集（`.optin=off`）→ 捕获随之停止；`signals.md` 首次启用时透明告知用户。

### 二·七 客观使用事件（G1 · 行业无关客观指标）

> 客观事件回答「用了多少 / 成不成功 / 快不快」——与语义事件（为什么好用）互补，且**不依赖主观判断**（Agent 汇报的是客观事实）。由会话结束「客观使用汇报」`[使用]` 行产生，或由服务网关（如 SmartLib usage_log 插件）批量同步。

- **事件**：`usage_call`（调用）/ `usage_error`（失败）/ `usage_slow`（耗时超标）——3 类共用同一 metric 结构。
- **method_layer 固定 `L0`**（客观层，非 L1–L7 语义层）。
- **metric 结构（行业无关 · 字段白名单 · 零 PII）**：
  ```json
  {
    "calls": 10, "success": 8,
    "errors": {"timeout": 1, "auth": 1},
    "duration_avg_ms": 850,
    "period": "session", "source": "agent"
  }
  ```
  - 白名单字段：`calls / success / errors / duration_avg_ms / period / source`；`errors` 键仅 `timeout/auth/notfound/ratelimit/other`；`period ∈ {session, day}`；`source ∈ {gateway, agent}`。
  - **禁止**：email / user_id / 内容 / 任意字段（字段白名单天然隔离 PII）；行业细节（如端点名）放 `note`。
- **落库**：`signals.metric_json`（TEXT 存 JSON，服务端校验后写入）；旧数据为 NULL 不受影响。
- **客户端产生**（会话结束 `[使用]` 行）：`event=usage_call` + metric 对象 → `upload_signals.py` 透传 → 服务端校验落库。
- **服务网关产生**（插件式，SmartLib usage_log 为范例）：网关每日聚合 → 同步（剥 email/user_id，只留聚合指标）→ 同上校验落库。

### 二·八 动作链遥测（P1-4 · action_trace）

> 回答「用户触发了哪个关键动作、成没成」——**行为层遥测**，与语义事件（为什么好用）/ 客观事件（用多少）正交互补。守体验铁律：匿名 + 方法层 + opt-in + 零 PII。

- **事件**：`action_trace`（行为层，method_layer 固定 `L0`）。
- **字段**：`action_name`（白名单，见 §八）+ `action_outcome`（`success` / `fail` / `partial` / `skip`）。
- **触发**：Agent 在用户完成 / 尝试一个白名单动作后调用 `scripts/session_hook.py action <name> <outcome>`（本地记录开时写入，关时跳过）。
- **零 PII**：`action_name` 只允许 §八 白名单内的方法层标签，**绝不允许任意用户自由文本**——从源头杜绝 PII 泄漏（服务端 + 客户端双重校验）。
- **云端**：与 `usage_call` 同通道（`.cloud_optin` 控上传）；Body 白名单见 §七。

```json
{"ts":"...","signal_id":"<uuid>","client_signal_id":"<uuid>","skill_slug":"cjg-skill-forge",
 "skill_version":"<ver>","method_layer":"L0","event":"action_trace","weight":1,
 "anon_id":"<本机uuid>","action_name":"publish","action_outcome":"success"}
```

## 三、两层授权模型（本地安装即开 / 云端上传默认关需显式开启）

### 第一层：本地记录（安装即开）

- **安装即开**。技能安装时 `.optin` 即设为 `on`，无需用户额外操作——进化飞轮零摩擦启动。
- 首次对话时按 SKILL.md §零 **口头提醒一次**（透明告知，不是请求许可）。
- 用户说「别记了」/「关掉」→ 写 `.optin=off`，停止记录。可随时说「再开」恢复。
- 与旧版区别：v0.1 opt-in 默认关 → v0.2 首次告知后开 → **v0.3 安装即开**（零摩擦、安装时即告知、可关）。

### 第二层：云端回传（默认关，需显式开启）

- **默认关**。`.cloud_optin` 安装时设为 `off`；只有用户明确说「开启云同步」才写 `on` 开始上传——**绝不默认上传**。本机日志只传方法层标签（零原文零身份），云端上传走匿名端点（包零密钥、仅含公网 URL），终端用户零注册、零配置、透明使用。
- 首次对话按 SKILL.md §零 **口头提醒一次**（告知云端默认关、可随时「开启云同步」）。
- 用户说「开启云同步」→ 写 `.cloud_optin=on`，开始回传（并仅在此时安装每日上传定时任务）。
- 说「别传了」→ 写 `.cloud_optin=off`，停止回传并卸载定时任务，**本地记录不受影响**。
- 说「再传」→ 写 `.cloud_optin=on`，恢复回传。
- **两层独立**：`.optin` 控本地、`.cloud_optin` 控云端；关云端不影响本地；关本地则云端也无信号可传（本地不记 = 云端无源）。

## 四、落盘实现（采集 one-liner · 末步硬纪律）

> **这是采集环节的唯一确定性机制**：把"写信号"从"可选散文提醒"升级为"每次应答必须执行的最后一步"，执行成本降到一行命令。

**末步硬规则**：七层应答（锻造 / 审视 / 重铸 / 清晰化）结束前，必须执行下方信号追加 one-liner；除非用户说「别记了」。

```bash
# 末步执行：追加一行方法层信号（缺字段留空即可，失败静默）
printf '%s\n' "$(python -c "import json,uuid,datetime; print(json.dumps({'ts':datetime.datetime.now().astimezone().isoformat(),'signal_id':str(uuid.uuid4()),'skill_slug':'cjg-skill-forge','skill_version':'2.9.9','method_layer':'<L1..L7>','event':'<helpful|unhelpful|confusion|suggestion|abandoned|misdiagnosis>','weight':<1-5>,'note':'<触发类标签>','anon_id':open('<dir>/.anon_id').read().strip() if __import__('os').path.exists('<dir>/.anon_id') else ''},ensure_ascii=False))")" >> "<dir>/signals-log.jsonl"
```

- `<dir>` = 本技能目录绝对路径（即 `~/.workbuddy/skills/skill-forge`）。
- `<L1..L7>` / `<event>` / `<weight>` / `<note>` 由 agent 按本轮实际判断填充（见 §二 表）。
- `signal_id` 由命令当场生成；`.anon_id` 缺失时命令自动留空（上传脚本 bootstrap 会补）。
- 该命令**失败静默**：即便 `python` 不存在或写文件失败，也绝不阻塞用户。
- **上传不是在这里做**——上传由 WorkBuddy cron 每日 23:30 跑 `scripts/upload_signals.py` 确定性批量完成（见 §七）。本 one-liner 只负责"可靠地写本地日志"。

- **采集时显性标记（A5 · 透明落到采集发生点）**：本轮 one-liner 成功写入 `signal_id` 后，AI 在应答末追加**一行轻量可见光标**（例：`> 📊 已记录 1 条进化信号 · 方法层 L3 · 有用 — 说"查看我的信号"看全部`）。规则：仅产生信号的回合标、无信号不标；首次附一句「只记方法名，绝不记你说了什么」；用户说"别提示了"可关、说"再提示"恢复；关本地（别记了）自然无标记。标记纯文本、失败静默、不碰后端。

## 五、隐私红线（不可逾越）

- **绝不记**：问题原文、回答原文、文件名/路径、用户身份、任何 PII、任何可还原内容。
- 本地信号**仅留本机**；上行云端（藏经阁·易筋平台）需 `.cloud_optin=on`（第二层授权），且仍只上行上述方法层标签。
- `signals-log.jsonl` 与 `.optin` / `.cloud_optin` / `.anon_id` / `.uploaded_ids.txt` 是**运行时产物，不进 git、不进打包 zip、不分发**。

## 六、两层授权边界总结

| 层级 | 控制文件 | 默认 | 触发方式 | 作用域 |
|------|----------|------|----------|--------|
| 第一层：本地记录 | `.optin` | **开** | 安装即开，首次提醒，可关 | 本机 `signals-log.jsonl` |
| 第二层：云端回传 | `.cloud_optin` | **关** | 默认关，需显式说"开启云同步"才上传、可关 | 上行藏经阁·易筋平台 |

- **本地开 ≠ 云端开**：本地记录安装即开，云端回传默认关（需显式开启、可关），二者独立可控。
- **云端依赖本地**：本地关 → 云端无源可传，自动降级不可用。
- **各自独立可关**：「别记了」关本地；「别传了」关云端，互不影响对方已设状态（但关本地会使云端实际不可用）。

## 七、本地 → 云端信号格式映射（上传时转换 · 由 upload_signals.py 完成）

> 上传由共享脚本 `scripts/upload_signals.py`（经 cron 每日触发）确定性完成，与"智能体是否记得 POST"彻底解耦。本机采集只写本地 JSONL；脚本负责转换 + 上传 + 幂等确认。

本地 `signals-log.jsonl` 的字段经**标准映射**转成云端白名单：

| 本地字段 | 云端字段 | 转换规则 |
|----------|----------|----------|
| `skill_slug` | `slug` | 直接映射（改名） |
| `method_layer` | `method_layer` | **直接透传**（agent 已直写层码，如 `"L3"`） |
| `event` | `event` | 直接透传 |
| `weight` | `weight` | 直接透传 |
| `note` | `note` | 直接放入 note 字段（PII 安全：仅触发类标签） |
| `skill_version` | `skill_version` | 直接透传 |
| `anon_id` | `anon_id` | 直接透传 |
| `signal_id` | `client_signal_id` | **直接透传（幂等键）**——服务端 UNIQUE 约束去重 |
| —（固定） | `mode` | 固定 `"cloud"` |
| `ts` | — | 丢弃（云端用服务端时间戳） |

### 幂等双保险

- **客户端**：`.uploaded_ids.txt`（append-only 副索引）记录已成功上传的 `signal_id`；cron 重跑 / 正常重试都先跳过已传行。
- **服务端**：`signals` 表 `client_signal_id VARCHAR(40)` + `UNIQUE KEY`；匿名 INSERT 用 `INSERT IGNORE`，重复 `client_signal_id` 直接忽略，不新增行。
- 二者缺一不可：客户端防"cron 跑两次 / 正常业务重试"，服务端防"网络边界重试（服务端已 200 落库、客户端读超时误判失败而重试）"。

### 四问机制（对应评审四问）

| 问题 | 处理 | 落点 |
|---|---|---|
| ① 离线 | 采集纯本地追加（不联网、不阻塞）；上传失联/超时不写 `.uploaded_ids.txt`，行留本地，下个 cron 续传 | §四 本地采集 + 脚本失败不标记 |
| ② 首次开启 / 历史回填 | `.cloud_optin` 默认 `off` → 用户说"开启云同步"后首次 cron 把 `signals-log.jsonl` 所有历史未上传行一次性回填；若仍 `off` 则不回填 | §三 bootstrap + 脚本全量扫描未上传 |
| ③ 断点续传 | 逐行原子确认：每条 200 后立即把 `signal_id` 追加进 `.uploaded_ids.txt` 并 flush；中途被杀 → 已确认跳过、未确认下轮续；遇 429 立即停本轮、下轮续 | §七 脚本逐行确认 + 副索引 |
| ④ 防重复 | 客户端 `.uploaded_ids.txt` 跳过已传 + 服务端 `UNIQUE(client_signal_id)` 幂等忽略 | 本 § 双保险 + 服务端改动 E |

### 云端 API 规范

- **端点**：`cloud_config.json` 的 `ingest_url` + `/ingest/anon`（随包分发，仅公网 URL、零密钥；**代码零硬编码**，端点完全来自外部配置，缺失则跳过云端上传）。
- **鉴权**：**无**（匿名端点免鉴权）。首次上报可不带 `anon_id`，由服务端 HMAC 签发并返回；后续携带复用同一限流身份。
- **Body 白名单**：`{slug, method_layer, event, weight, note, anon_id, mode, skill_version, client_signal_id, accepted, revision_rounds, feedback_tag, recurrence, attribution, attribution_note, action_name, action_outcome}`（P0 闭环 6 字段 + P1-4 动作链 2 字段全部可选，缺失落 NULL）。
- **method_layer**：须为 **L1–L7 层码**。
- **event 枚举**：`confusion` / `helpful` / `unhelpful` / `suggestion` / `misdiagnosis` / `abandoned` / `accept` / `reject` / `iteration` / `edit_capture` / `action_trace`。
- **weight 范围**：1–5 整数。
- **限流**：per-anon_id 100 次/小时 + 全局护栏 10000 次/小时；超限返回 429（脚本收到 429 立即停本轮，下轮续）。
- **零 PII 校验**：云端 `signal_validate` 强制白名单 + note 脱敏扫描，超出字段直接拒绝。

## 八、动作名白名单（P1-4 · action_name 取值）

> `action_name` 只接受下列方法层标签（snake_case，零 PII）；任意不在表的名称服务端 + 客户端双重拒绝。产出技能由 `forge-signal-kit.py` 注入各自专属白名单（覆盖本表）。

| action_name | 含义 |
|-------------|------|
| `forge_new` | 新建技能（模式 A 进入） |
| `upgrade` | 升级既有技能 |
| `review` | 审视 / 审计技能（模式 B） |
| `recast` | 重铸整合技能库（模式 C） |
| `clarify` | 内嵌清晰化（模式 D / S7） |
| `register_skill` | 注册技能到藏经阁（forge-register） |
| `open_cloud_sync` | 开启云同步（开启云同步） |
| `close_cloud_sync` | 关闭云同步（别传了） |
| `turn_off_log` | 关闭本地记录（别记了） |
| `publish` | 四平台发布（forge-publish） |
| `joint_test` | 三侧三方联合测试（S9） |
| `self_check` | 全量自测（selfcheck） |
| `inject_signal_kit` | 注入信号套件（S0） |
| `run_pipeline` | 工作流编排（forge_pipeline） |
| `view_signals` | 查看我的信号 |
| `view_growth` | 我的技能成长 |
| `delete_signals` | 删除我的信号 |
| `download_proposals` | 同步 / 查看提案 |
| `apply_proposal` | 应用提案 |

> 本文件与扫地僧 `references/signals.md` 同源（v0.4 双模态）；差异仅在 L1–L7 层码语义（锻造炉按锻造能力分层）与不含 `coverage_gap`（锻造炉自身缺口上报走 `event=suggestion` + `note`）。
