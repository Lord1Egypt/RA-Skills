---
name: acceptance-rate-analysis
description: 对承接率下降做阶段式归因分析。适用于“今天/本周承接率为什么下降”“分析承接率下降原因”“看一下承接率环比是否下降及原因”等场景。先定位异常切片，再逐层判断是一级切片结构迁移、资方总量明显减少或分布左移、资产维度异常，还是进一步闭环到敏感资方侧收缩。
---

# 承接率下降归因
对承接率指标进行阶段式的数据变化、取数、归因分析等，每个阶段只做当前层级需要的取数和判断，命中终点后立即停止，不继续下钻。

## 规则优先级
- **计算口径的唯一事实来源是代码**：阈值、门禁公式、命中与候选范围逻辑以 `scripts/acceptance_rate_constants.py` 与 `scripts/acceptance_rate_support.py` / `scripts/acceptance_rate_analysis.py` 为准。**禁止**凭本文件背诵具体百分比、门槛数值或分支细节；若叙述中需要提及规则，只写业务语义，数字与条件以脚本输出字段与表格为准。
- 本 `SKILL.md` 的主职责是：**阶段顺序、终端调用方式、展示字段与顺序、状态块原样输出、对用户可用的业务话术边界（如不暴露内部码）**——不是第二份公式手册。
- `agents/openai.yaml` 只负责运行时默认提示，不应额外定义与本文件冲突的新口径。
- 面向用户输出时，凡脚本已经返回的 `*_display`、`*markdown` 等展示字段，都必须优先直接放入最终回复正文；不要只在思考过程里引用、转述、消化后省略，也不要先写一段新的摘要去替代这些展示块。

## 默认规则
- 用户未指定粒度时，默认按周环比分析。
- 只支持 `day` 和 `week` 两档粒度，`week`周粒度默认以周一为一周起点。
- 用户说“本周和上周”时，默认解释为“本周所在自然周 vs 上周所在自然周”，周边界固定按 `周一~周日`。
- 如果当前时间还没走完整个自然周，但用户要看“本周 / 截至当前 / 截至今天”，必须先提示用户“当前看到的是周内累计口径，不是完整自然周”。
- 用户明确说“本周截至目前 / 截至今天 / 周内累计 / 与上周同期”时，才切回同进度周累计口径。
- 周粒度对话展示优先使用实际分析周段，也就是自然周闭区间 `周一~周日`。
- 用户直接说 `4.13周`、`4.6周` 这类“周标签”时，默认按该日期所在自然周解释。例如 `4.13周 -> 2026-04-13~2026-04-19`，`4.6周 -> 2026-04-06~2026-04-12`。
- 用户说“某日所在周”时，同样按该日期落入的自然周解释。
- 已确定粒度后，不要静默改成其他粒度；若当前粒度下时间窗或数据桶不成立，应先说明原因。

## 快速使用
先从用户问题中明确这 3 个信息：
- `granularity`
- `current_period`
- `baseline_period`

脚本不负责解析自然语言时间，运行前要先把时间窗补齐。

时间参数可以传：
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:MM:SS`

如果只传日期，脚本会自动补成开始时间 `00:00:00` 和结束时间 `23:59:59`。

### 终端里如何调用脚本（Nanobot / exec 受限 workspace 必读）

运行时若开启「命令只能落在允许目录」一类策略，**从 `primary` 到 `funding` 的每一次调用都必须沿用同一种外壳形状**，不要中途改写法。常见故障是：第一轮用了 `cd <skill 根目录> && python scripts/...` 能跑通，后面又改成 `python <绝对路径>/scripts/acceptance_rate_analysis.py`，在当前会话默认工作目录与技能目录不一致时会被守卫拦截，看起来像「前半段正常、后半段突然执行不了脚本」。

**推荐（默认工作目录不在 skill 根目录时）**：每条执行一条命令，且该行只包含「进入 skill 根目录」和「用相对路径跑脚本」，中间用 `&&` 衔接（与后端 `cd … && python …` 白名单一致）：

```bash
cd "<skill 根目录（含本 SKILL.md 的目录）>" && python scripts/acceptance_rate_analysis.py <primary|capital|asset|funding> … --access-token <BIGDATA_ACCESS_TOKEN>
```

- **已在 skill 根目录时**：可直接 `python scripts/acceptance_rate_analysis.py … --access-token <BIGDATA_ACCESS_TOKEN>`。
- **若 exec 工具支持单独传入工作目录**：也可把本次命令的工作目录设为上述 skill 根目录，命令只写 `python scripts/acceptance_rate_analysis.py …`（命令里不要写脚本文件的绝对路径）。
- **不要用**「仅 `python <绝对路径>/scripts/acceptance_rate_analysis.py`」作为受限环境下的默认方式；在未确认部署已把该路径纳入允许范围前，这种方式容易在第二阶段及之后被拒绝。
- **凭证**：持续用 `--access-token` 传入即可。不要把 `export BIGDATA_ACCESS_TOKEN=…`、`$env:BIGDATA_ACCESS_TOKEN='…'` 等写在**同一条** `cd … && python …` 命令的前面（会破坏白名单对「纯 cd + && + python」形式的匹配）。需要先写环境变量时：**单独一条命令**设置，再**单独一条**执行上面的 `cd … && python …`。
- **持久化 token**：仍可按下文「数据访问凭证」用用户级环境变量或 `--access-token`；持久化动作与脚本调用拆开即可。

## 数据访问凭证
本技能需要 `BIGDATA_ACCESS_TOKEN` 用于访问数据查询 API；这个值对应浏览器请求 Cookie 里的 `bigdata_access_token`。凭证处理顺序如下：
1. **运行上下文环境变量**：优先从运行 skill 的上下文中读取 `BIGDATA_ACCESS_TOKEN`。
2. **用户显式提供 token 时立即持久化**：如果用户直接给了 token 值，agent 需要先把它写入当前进程环境变量，并同步写入用户级环境变量，让后续新的终端 / 新的会话也能继续复用。本次调用和后续脚本调用仍继续显式传 `--access-token <BIGDATA_ACCESS_TOKEN>`。脚本在收到显式 `--access-token` 时，也会自动做这一步持久化。
   - 如果上一轮刚刚向用户索要过 token，而用户这一轮只回复了一串单行文本，例如 `manage-xxxx` 这类值，默认直接把这整串视为 `BIGDATA_ACCESS_TOKEN` 本体，不要再次要求用户补“这是 token”或重复解释获取步骤。
3. **当前环境变量复用**：如果用户这次没有再贴 token，但当前终端或用户级环境变量里已经有 `BIGDATA_ACCESS_TOKEN`，直接复用，不要重复向用户索取。
   - 在 Windows 上，不要只检查当前 PowerShell 会话里的 `$env:BIGDATA_ACCESS_TOKEN`；用户级环境变量也算可复用来源。
   - 不要因为一次独立的环境变量探测为空，就在脚本运行前直接判定“缺少 token”；脚本自身也会继续尝试读取用户级环境变量。
4. **浏览器 Cookie 取值**：如果上下文和环境变量都没有，再让用户打开 `https://data.jirongyunke.net/data-pc-bdopr-fe/hoc-inquiry/index`，按 `F12`，在 `Network` 里点开任意一个请求，从 `Cookies` / `Request Cookies` 中复制 `bigdata_access_token` 的值本身，不要传整段 `Cookie:` 请求头。拿到后先按上一条持久化，再执行脚本。

当前环境是 PowerShell 时，可直接复用以下方式：
- 当前会话设置：`$env:BIGDATA_ACCESS_TOKEN='<token>'`
- 持久化到后续新会话：`[System.Environment]::SetEnvironmentVariable('BIGDATA_ACCESS_TOKEN', '<token>', 'User')`
- Linux / macOS 当前终端设置：`export BIGDATA_ACCESS_TOKEN='<token>'`
- Linux / macOS 持久化到后续新会话：将 `export BIGDATA_ACCESS_TOKEN='<token>'` 写入 `~/.bashrc`、`~/.zshrc` 或 `~/.profile`

## 执行顺序
默认严格按“单切片串行”执行，无需打断询问：
1. 先运行 `primary`
2. 第一阶段展示完成后，按 `analysis_sequence` 顺序逐个处理异常切片
3. 对当前切片先运行 `capital`
4. 若当前切片的第二阶段结果显示还需要继续看资产维度，立刻对同一切片运行 `asset`
5. 若当前切片的第三阶段结果显示还需要继续看敏感资方侧，立刻对同一切片的 `qualified_ranges` 逐个运行 `funding`
6. 只有当前切片完整分析到 `stop` 或 `funding` 结束后，才能开始下一个切片
7. 所有需要分析的异常切片都处理完成后，最后统一输出一次“第五阶段：最终总结”

执行约束：
- **终端调用形状一致**：同一对话内所有脚本调用（`primary` / `capital` / `asset` / `funding`）须沿用「快速使用」里约定的同一种路径写法（例如始终 `cd "<skill 根目录>" && python scripts/acceptance_rate_analysis.py …`），禁止中途切换成「仅绝对路径调用脚本」；否则在受限 workspace 下易出现前半段成功、后半段被拦截。
- 每个阶段面向用户输出时，都必须先遵循该阶段自己的“展示要求”完成展示。
- 严禁先把多个切片的 `capital` 全部跑完，再统一进入 `asset` 或 `funding`。
- 第五阶段只允许在全部异常切片都分析完成后输出一次，不要每分析完一个切片就提前插入整体验证结论。
- **【严禁跳切片】** 无论 `analysis_sequence` 里有多少个异常切片，每一个都必须完整走完自己的脚本调用和展示步骤，再处理下一个；禁止以任何理由（"篇幅原因""逻辑类似""不再赘述""以此类推"等）跳过或省略后续切片的分析过程，每个切片必须独立调用脚本并输出对应的展示字段。
- **【严禁提前总结】** 在所有切片全部分析完成之前，禁止输出任何形式的"汇总结论""归因总结""综合来看"等整体性内容；第五阶段总结只能在最后一个切片的展示步骤全部完成后才允许出现。
- **【切片进度全局一致】** 同一 `slice_key` 在 `capital` / `asset` / `funding` 连续调用下，`📍 切片进度：N/M` 必须与一级 `analysis_sequence` 的全局队列一致（脚本根字段 `slice_index` / `slice_total`）；不要用「客群内第几个」「产品线序号」等另一套计数冒充切片进度。

## 状态展示规范（方案A：状态树最小版）
本节是 SKILL 的展示契约，目的是让用户一眼看到"每个切片走到哪、为什么停、还剩几个"。
脚本会在每个阶段产出一行 `status_line` 字符串和一份 `slice_status_summary` 对象，所有可视化文本都已由脚本拼好；Agent 必须**原样追加**，禁止改写、合并或省略，禁止自行拼接状态符号、序号、结论标签。

### 状态符号字典（与脚本常量一致）
- `S1` / `S2` / `S3` / `S4` 分别代表一级到四级阶段
- `✅` = 阶段通过（OK）
- `🛑` = 该阶段终止（STOP）
- `🔒` = 已闭环到敏感资方收缩（LOCKED，仅 `S4`）
- `🧩` = 一级结构迁移（SHIFT，仅 `S1` 配 R2）
- `⚠️` = 证据/字段不足（DATA-GAP，对应 R8）
- `⏳` = 尚未到达该阶段（PENDING）

### 状态行格式
脚本按以下统一格式拼好 `status_line`，已带 `> ` 引用前缀：

```text
> 🚀 任务进度：步骤 <1|2>/2 · <步骤名称>
> 📍 切片进度：<index>/<total>
> 🧩 当前切片：<slice_display>
> - 一级·客群入口：✅ 已通过 / 🛑 <终止语义> / 🧩 结构迁移 / ⚠️ 证据不足 / ⏳ 待执行
> - 二级·资方分布：...
> - 三级·资产维度：...
> - 四级·敏感资方闭环：...
```

- 一级阶段状态块只显示：`任务进度(1/2)` + `步骤结论`，不显示切片进度/当前切片，也不展示二~四级细分状态
- 二~四阶段显示任务步骤 `2/2`，并展示切片进度 `N/M` + 当前切片 + 二/三/四级细分状态
- 阶段名统一中文，避免 `S1/S2/S3` 缩写
- 业务展示层不输出 `Rxxx` 内部码；终止原因只展示中文语义
- 结论标签由脚本根据 `terminal_reason` 选择，业务含义统一在「内部终点码速查」中

### 切片进度 N/M（全局一致，以脚本为准）

`📍 切片进度：N/M` 里的 **`M` 永远是一级诊断 `analysis_sequence` 的长度**（跨 `01.惠选客群` + `03.精优客群` 的**全局异常切片队列**）；**`N` 是当前切片 `slice_key` 在该队列里的 1-based 序号**。同一异常切片在 **第二、三、四阶段必须用同一组 N/M**，与脚本返回的 `slice_index` / `slice_total`（以及拼进状态行的文本）一致。

**脚本侧对齐（一次性串行跑命令也必须一致）：**

- **第二阶段**：若未显式传入 `--slice-index` / `--slice-total`，脚本会用 **全客群一级**自动解析 N/M，并与一级 `analysis_sequence` 对齐。
- **第三阶段**：取数仍用「当前切片所属客群」的一级快照（与既有口径一致）；**仅用于状态行的 N/M** 在「未注入一级 JSON、且本轮未传入二阶段 trace」时，脚本会 **再跑一次全客群一级**专门对齐全局队列，避免出现「二阶段 2/5、三阶段误显示 1/4」这类偏差。若在链路中能把上一阶段的 trace（至少含 `slice_index`、`slice_total`）传给脚本接口，可减少重复一级查询。
- **第四阶段**：`slice_index` / `slice_total` 继承第三阶段的 trace（同一 `slice_key` 链路上与二阶段一致）。

**文案约束（Agent）：**

- **禁止**自编「切片2」「精优第几个」等与脚本 `📍 切片进度` **不一致**的进度表述；阶段标题若写「切片」序号，必须与 **`analysis_sequence` 的全局序号**一致（即与 `N` 一致），不得改用客群内局部计数。
- 展示时 **只原样使用脚本生成的 `status_line`**（含 `📍 切片进度`），不要手动改写 N/M。

### 展示位置（必须遵守）
- 一级阶段最开头必须先展示：`workflow_overview_markdown`（总流程导览）+ `stage1_status_block`（一级状态块）
- 二级阶段：`capital_display.summary_markdown` 开头已经前置 `status_line`
- 三级阶段：`asset_display.summary_markdown` 开头已经前置 `status_line`
- 四级阶段：**先展示顶层字段 `status_line`（与 JSON 根上的 `trace["status_line"]` 一致）一次**，再展示 `business_view.summary` 与 `business_view.evidence`；**不要把 `status_line` 再嵌进 `business_view.summary` 造成重复**（脚本不会在 summary 内二次前置状态块）。
- 第五阶段：先输出全局进度行，再输出状态汇总表，最后才进入「逐切片归因结论」（详见第五阶段说明）

### 关键行加粗规则（仅说明，由脚本生成；Agent 不允许自加 `**`）
- 一级 `客群承接率变化` 表：`变化` 列整列加粗
- 一级各客群切片表：`是否下钻=是` 的行，将 `承接率变化` 与 `是否下钻` 单元格加粗
- 二级 `资方桶分布表`：占比变化绝对值最大的桶整行加粗
- 三级 `全部因子总览表`：`是否命中=是` 的行，将 `是否命中` 与 `维度结论` 加粗
- 四级 `business_view.evidence` 列表：放款金额变化主行整行加粗（脚本已用 `**…**` 包裹）

## 第一阶段：一级诊断

向 `primary` 传入粒度、当前期和对比期即可：
- `week` 传实际分析周段的闭区间，例如 `2026-04-20~2026-04-26`（周一~周日）
- `day` 传单日闭区间，例如 `2026-04-26~2026-04-26`
- 每个时间窗都必须落在单个粒度桶内；时间窗跨了两个桶时，先修正再运行
- 用户给的是 `4.13周` 这类周标签时，先翻译成实际分析周段再传脚本

下列 bash 示例假定当前工作目录已为 skill 根目录；若 exec 默认 cwd 不在该目录，请在整条命令外加本文「终端里如何调用脚本」中的 `cd "<skill 根目录>" && …` 外壳，且各阶段保持同一外壳。

```bash
python scripts/acceptance_rate_analysis.py primary --granularity <week|day> --current-start <当前周期开始> --current-end <当前周期结束> --baseline-start <对比周期开始> --baseline-end <对比周期结束> --access-token <BIGDATA_ACCESS_TOKEN>
```

示例 1：按周分析"本周 vs 上周"

```bash
python scripts/acceptance_rate_analysis.py primary --granularity week --current-start 2026-04-20 --current-end 2026-04-26 --baseline-start 2026-04-13 --baseline-end 2026-04-19 --access-token <BIGDATA_ACCESS_TOKEN>
```

示例 2：用户明确要"本周截至目前 vs 上周同期"时，使用同进度周累计

```bash
python scripts/acceptance_rate_analysis.py primary --granularity week --current-start 2026-04-27 --current-end 2026-04-27 --baseline-start 2026-04-20 --baseline-end 2026-04-20 --access-token <BIGDATA_ACCESS_TOKEN>
```

示例 3：按日分析昨天 vs 上周同日

```bash
python scripts/acceptance_rate_analysis.py primary --granularity day --current-start 2026-04-26 --current-end 2026-04-26 --baseline-start 2026-04-19 --baseline-end 2026-04-19 --access-token <BIGDATA_ACCESS_TOKEN>
```

示例 4：用户说"分析 4.13周 相较于 4.6周"，先把周标签换成实际分析周段

```bash
python scripts/acceptance_rate_analysis.py primary --granularity week --current-start 2026-04-13 --current-end 2026-04-19 --baseline-start 2026-04-06 --baseline-end 2026-04-12 --access-token <BIGDATA_ACCESS_TOKEN>
```

内部路由重点看（不对用户直出）：
- `terminal_reason`
- `next_action`
- `analysis_sequence`
- `primary_display`
- `customer_group_summary_text`

一级判定与停止：
- 若 `terminal_reason = R1`，大盘承接率未下降，直接结束，不进入后续任何阶段（含第五阶段）。
- 若 `terminal_reason = R2`，大盘下降以结构迁移为主导，展示 `primary_display.structural_decomposition` 中的结构分解结论（含 `structural_effect`、`performance_effect`、`structural_ratio`、`top_movers` 字段）后，**跳过第二至四阶段，直接进入第五阶段总结**；R2 路径下不展示惠选/精优客群切片表，不进入资方诊断链路。
- 若 `terminal_reason = R9` 或 `R10`，目标客群未触及继续下钻条件，用一句话说明原因后直接结束，不进入后续任何阶段（含第五阶段）。
- 否则，按 `analysis_sequence` 顺序逐个切片进入第二阶段。

展示要求（适用于大盘下降且有异常切片的正常下钻路径；R1/R9/R10 直接结束，R2 仅展示结构分解后跳至第五阶段）：
- 优先直接原样复制 `primary_display.stage1_verbatim_markdown` 整段作为第一阶段正文；若必须拆分展示，也只能按下面 5 步顺序逐字复制。
- 以下 5 个展示步骤必须按顺序直接进入最终回复正文，不可省略，也不允许只停留在思考过程里：
  1. 首先原样展示大盘情况字段 `primary_display.overall_summary_markdown`；该块必须先展示“### 大盘情况”，再展示“### 客群承接率变化”。其中大盘情况优先说明整体承接率与路由金额变化，客群承接率变化表头固定为 `客群 / 对比期 / 当前期 / 变化`。
  2. 接着原样展示两类客群继续分析条件判断字段 `customer_group_summary_text`；该块用于说明两个客群分别是否命中继续分析条件，以及是否已经形成可继续下钻的异常切片。
  3. 然后原样展示继续分析口径字段 `primary_display.drill_down_scope_markdown`；该块内的客群门槛与明显下降阈值以 **`acceptance_rate_constants` 的 `CUSTOMER_GROUP_ACCEPTANCE_THRESHOLDS`、`PRIMARY_CUSTOMER_GROUP_DECLINE_THRESHOLD`** 及脚本生成文案为准（上文出现的百分比仅为与展示字段对齐，**禁止**凭记忆改写数值）；异常切片入口为命中客群后，承接率较对比期下降的 `客群 + cp_dj_new` 切片继续下钻（`acceptance_rate_delta` 为负，以实现为准）。
  4. 然后原样展示惠选客群切片表 `primary_display.huixuan_group_markdown`；该表必须展示 `01.惠选客群` 下的全部切片，而不只是进入第二阶段的切片，表头固定为 `cp_dj_new / 对比期承接率 / 当前期承接率 / 承接率变化 / 对比期路由金额 / 当前期路由金额 / 是否下钻`。
  5. 最后原样展示精优客群切片表 `primary_display.jingyou_group_markdown`；该表必须展示 `03.精优客群` 下的全部切片，而不只是进入第二阶段的切片，表头固定为 `cp_dj_new / 对比期承接率 / 当前期承接率 / 承接率变化 / 对比期路由金额 / 当前期路由金额 / 是否下钻`。
- **【绝对禁止】** 跳过流程导览和一级状态块；第一阶段正文必须先输出 `workflow_overview_markdown`，再输出 `stage1_status_block`，再进入大盘与客群表格。
- **【口径防幻觉】** “明显下降”阈值仅适用于**客群入口**，不等于切片下钻门槛；切片下钻以 `primary_display` 各表 **`是否下钻`** 与 `select_primary_drill_down_candidates` 实现为准，严禁改写成“切片下降须达到某固定百分点才下钻”。
- **【数量一致性】** 客群分表标题里的“其中 X 个承接率下降继续下钻”必须与该表“是否下钻=是”的行数一致；若不一致，以分表内逐行“是否下钻”结果为准并修正文案，不得自行重算或另起口径。
- 5 个字段全部展示完毕后，才可以写过渡句进入第二阶段，且过渡句不得再次汇总切片总数。
- 禁止在正文另行汇总“共识别到 X 个异常切片”作为开场白；切片数量已包含在 `customer_group_summary_text` 和各客群分表标题里，不要重复另起一行总计。
- **第一阶段不再展示切片队列。** 必须保留 `primary_display.status_line`（已在 `stage1_status_block` 中），并保持其位于第一阶段开头展示。


## 第二阶段：资方分布诊断

```bash
python scripts/acceptance_rate_analysis.py capital --granularity <week|day> --current-start <沿用 primary> --current-end <沿用 primary> --baseline-start <沿用 primary> --baseline-end <沿用 primary> --slice-key "<analysis_sequence[i].slice_key 原值>" --access-token <BIGDATA_ACCESS_TOKEN>
```

> `--slice-key` 的值必须直接从 `analysis_sequence[i].slice_key` 字段逐字复制，禁止自行拼接 `if_irr`、`cp_dj_new` 字段值构造。
> `--slice-index` / `--slice-total`（可选）：不传时脚本会按一级全局队列自动解析 N/M，并与下文「切片进度 N/M」一节对齐；仅在需要手工覆盖时传入（须与 `analysis_sequence` 一致）。

内部路由重点看（不对用户直出）：
- `terminal_reason`
- `next_action`
- `capital_total_judgement`
- `distribution_judgement`
- `capital_display`
- `stage2_signal`：`left_shift` / `no_shift`（由脚本根据 4-CDF 路由信号写入根字段与 `capital_display.stage2_signal`）

二级判定与停止（**路由信号层 ≠ 最终归因**）：
- **语义分层**：第二阶段的数值（加权均值、分布与 CDF 相关指标）统一理解为 **辅助结论 + 路由判断**。`distribution_judgement.is_left_shift` / `stage2_signal` **仅表示脚本给出的路由信号**，用于与后续资产形态、第四阶段共同解读；**不等于**已完成最终归因。
- **左移/分布的具体条件与阈值**：以实现为准（见 `acceptance_rate_analysis.py` 中 capital 阶段对 `distribution_judgement`、`capital_total_judgement` 的写入逻辑）；**不要用本 SKILL 复述百分比或条数**，需要解释时引用脚本返回的字段文案或表格单元格。
- 准入资方加权均值在第二阶段只作辅助结论，**不再作为分叉节点**；当前版本在完成第二阶段后**仍会进入第三阶段**（与脚本一致）；`stage2_signal = no_shift` 时须在叙述中标明这是**路由信号**，不等于排除资方因素。
- `terminal_reason = R4a` / `R8` 等：以返回 JSON 的 `terminal_reason`、`root_cause` 为准，业务展示只译中文语义。

展示要求：
- 以下 3 个展示步骤必须按顺序直接进入最终回复正文，不可省略，也不允许只在思考过程里消化后另写摘要：
  1. 首先展示对准入资方个数总量估算的判断结果 `capital_display.summary_markdown`；
  2. 其次在总量判断未命中的情况下，完整展示资方桶分布的表格 `capital_display.bucket_table_markdown`；
  3. 最后给出对准入资方个数分布的判断结果 `capital_display.distribution_detail_markdown`。
- 在这 3 个字段写入最终回复正文之前，不要先写"第二阶段结果""资方分布左移""继续进入第三阶段"这类摘要或过渡话术。
- `capital_display.summary_markdown` 开头的状态块 **已由脚本拼好**，必须原样输出；禁止移到阶段末尾。

## 第三阶段：资产维度诊断

```bash
python scripts/acceptance_rate_analysis.py asset --granularity <week|day> --current-start <沿用 primary> --current-end <沿用 primary> --baseline-start <沿用 primary> --baseline-end <沿用 primary> --slice-key "<analysis_sequence[i].slice_key 原值>" --access-token <BIGDATA_ACCESS_TOKEN>
```

> `--slice-index` / `--slice-total`（可选）：不传时脚本会用一级全局队列对齐状态行 N/M（见「切片进度 N/M」）；与 `capital` 同一切片链路保持一致。

> **为何「只有某一切片」三阶段 R8、二阶段却正常？** 二阶段 `capital` 只按 `if_irr + cp_dj_new` 向数仓取**桶级分布**，**不要求**该切片出现在一级 `analysis_sequence` 里；三阶段 `asset` 必须先拿到一级给出的**切片承接率/路由快照**（与一级下钻队列同源）。个别切片可能卡在「一级边界判定未入选」或「单客群重跑一级与先前不一致」，而桶查询仍有数——因而只见该片 asset 失败。**脚本已在快照缺失时自动补跑全客群一级再查找**；仍失败时请核对时间窗、token 与 `--slice-key` 是否与一级 `slice_key` 逐字同源。
>
> **仅跑 `asset` 时（未注入一级 JSON）**：脚本会再跑与当前 `slice_key` 同客群的一级做快照；并已保留 `analysis_sequence_lookup`、R2 清空路由队列时仍可 lookup。**推荐**：同一会话内先 `primary` 再按序 `capital`→`asset`。
>
> **承接率占位符**：缺失与常见占位符在脚本内统一经 `to_float` 处理；细节以实现为准。**对用户复述时仍可出现 `-`**，与内部数值不必逐字对齐。

内部路由重点看（不对用户直出）：
- `terminal_reason`
- `next_action`
- `qualified_ranges`
- `asset_display`
- `asset_dimension_pattern` / `asset_dimension_pattern_label`：编码仅存 trace（`concentrated` / `broad_based` / `mixed_pattern` / `no_clear_signal` / `all_factors_raw_volume_decline`（R12 全维原始桶普降）），展示正文用 `asset_dimension_pattern_label` 白话句，**不等于最终归因**（正文不必复述英文编码）。
- `stage2_signal`（若在链路中传入第二阶段结果则会携带）：与形态字段共同用于第五阶段路径回放
- `root_cause`（R8、R12 等终止时可能带类型说明；R4b/R5 等同上）
- `raw_volume_gate_summaries`：五因子**原始桶**体积规则逐维摘要（含 **本维原始桶普降** 是否成立）；R12 与走深链路时均有，便于对照
- `asset_deep_chain_factor_keys`：**仅**会继续跑归一化深链路的因子键列表（= 原始桶门禁**未**判「普降」的维度）
- `factor_results`（R12 路径下常为空列表，表示未跑「归一化桶 + 单桶门槛」深链路；深链路时**仅含**上述「未普降」因子）
- `business_view`（本阶段脚本字段：仅 R8 早退路径存在，R4b/R5/成功路径不输出；与第四阶段脚本的同名字段含义独立，勿混用）

三级判定与停止（**先门禁，再深链路；细节以代码为准**）：
- **原始桶体积门禁**：实现为 `acceptance_rate_support.compute_asset_raw_volume_gate` / `analyze_raw_volume_single_factor`；可调阈值见 `acceptance_rate_constants` 中 `ASSET_RAW_GATE_*`。门禁在**取数原始桶键**上计算（高龄等分列，不归一成「55+」）；五维**同时**满足时脚本返回 R12 并停止深链路（见 `run_asset_stage`）。
- **未过门禁的维度**：仅这些维度进入归一化深链路（`_build_factor_results` 按 `asset_deep_chain_factor_keys` 过滤）；已过门禁的维度不再重复深链路。摘要表里「本维原始桶普降」与下方因子总览（可能出现 `55+`）属于两套桶键，属预期差异。
- **深链路**（单桶门槛、因子内普降形态、`broad_perf_decline`、候选范围组合与排序）：见 `_build_factor_results`、`_build_range_results`、`_filter_minimal_qualified_ranges`；门槛常量见 `ASSET_BUCKET_*`、`ASSET_RANGE_ROUTE_*`。**勿自拟门槛数值或公式**。
- **目标桶白名单**：`FACTOR_TARGET_BUCKETS`（身份证仅无效桶命中高龄等为产品设计；复述时用脚本表格中的「是否命中」列）。
- **复制 `range_key`**：进入第四阶段时 `--range-key` **必须**从 `asset_display.range_detail_markdown` 表格逐字复制，禁止拼凑。
- **终止语义**：`terminal_reason` / `root_cause` 以 JSON 为准；对用户只译中文（R12 / R4b / R5 / R8 等不在正文暴露）。R12 时沿用 `asset_display.summary_markdown` 已拼好的说明块，**勿**写成「已完成资金闭环」。

展示要求：
- 以下 3 个展示步骤必须按顺序直接进入最终回复正文，不可省略，也不允许只在思考过程里引用后省略：
  1. 首先完整展示第三阶段结论 `asset_display.summary_markdown`（含「#### 五维原始桶体积门禁摘要」表——其中有 **本维原始桶普降** 列；R12 另有「#### 五维体积规则摘要」「#### 形态与业务结论（画像≠定责）」等；内部终端码仅存 JSON，**面向用户复述时不要出现 R 码**；形态编码仅存 JSON trace，**先于**最强桶叙事，避免把广谱普降误写成单桶主导）；
  2. 其次完整展示 `asset_display.factor_detail_markdown`：**非 R12** 时为因子总览表（若仅部分维度未过门禁，标题为「未通过原始桶门禁的维度」且行数少于 5）；**R12** 时为精简版「各维度桶级摘录（节选）」（每维至多少量示例桶），仍须整段原样输出；
  3. 最后完整展示 `asset_display.range_detail_markdown`（**R12** 下为「敏感资方与资金明细：本分支说明」短文，仍须原样输出；不对用户复述内部码）；
- 不要先在正文写一段新的自由摘要去替代上面 3 个展示块；如果需要补充业务串联，必须放在这 3 个展示块之后。
- `asset_display.summary_markdown` 开头的状态块 **已由脚本拼好**，必须原样输出；禁止删除或重写。

**深链路补充说明（未 R12 时由脚本执行；勿背公式）**：
- 单桶影响、因子内普降 `broad_perf_decline`、候选范围是否进入下一阶段：均以 `_build_factor_results` / `_build_range_results` 及常量为准；展示层只看表格中的门槛列与「是否进入下一阶段」。
- `qualified_ranges` 的去重与排序由 `_filter_minimal_qualified_ranges` 与脚本排序逻辑完成；第四阶段优先使用表中靠前的 `range_key`。

## 第四阶段：敏感资方闭环
第四阶段仍通过资金项目映射数据做敏感资方侧闭环。`--range-key` 参数沿用第三阶段已确定的值，即从 `asset_display.range_detail_markdown` 表格中的 `range_key（传给第四阶段脚本）` 列逐字复制，与第三阶段判定说明保持一致；`range_id` 只用于阅读顺序，不要把它当成跨阶段稳定主键。

第四阶段 funding：**维度列表、过滤条件、项目聚合方式**以实现 `acceptance_rate_analysis.py` 中 `run_funding_stage` 及 funding 查询构造为准；高龄与 `range_key` 原始桶字符串须与第三阶段输出一致。**不支持因子 / R8 / `business_view`**：只复述脚本已生成的 `business_view` 与证据列表，勿自拟失败原因。

```bash
python scripts/acceptance_rate_analysis.py funding --granularity <week|day> --current-start <沿用 primary> --current-end <沿用 primary> --baseline-start <沿用 primary> --baseline-end <沿用 primary> --slice-key "<analysis_sequence[i].slice_key 原值>" --range-key "<qualified_ranges[i].range_key 原值>" --access-token <BIGDATA_ACCESS_TOKEN>
```

> `--slice-index` / `--slice-total`（可选）：一般与第三/二阶段 JSON 中 `slice_index` / `slice_total` 一致；不传时由脚本在拉取资产阶段结果后继承，保持 N/M 与全局队列一致。

内部路由重点看（不对用户直出）：
- `terminal_reason`
- `business_view`（摘要开头已由脚本前置 **归因定级** 段落：`final_attribution_level` / `final_attribution_rationale`）
- `final_attribution_level` / `final_attribution_rationale` / `final_attribution_meta`：结合第三阶段形态与第四阶段闭环（R6/R7/R8）给出的中文定级，业务展示层只复述中文标签与证据，不暴露内部码
- `matched_projects`
- `funding_amount_delta`
- `project_count_delta`
- `root_cause`

四级判定与停止：
- 若 `terminal_reason = R7`，停在第四阶段，解释为"已经闭环到敏感资方收缩"；要明确带出敏感资方相关项目放款金额变化、项目数变化和关键项目证据。
- 若 `terminal_reason = R6`，停在第四阶段，解释为"资产维度组合成立，但敏感资方侧没有观察到同步收缩"，因此当前不能把原因直接落到敏感资方变化。
- 若 `terminal_reason = R8`，停在第四阶段，并结合 `root_cause` 与脚本已输出的 `business_view` 说明为什么不能闭环，例如：没有 `qualified_ranges`、范围引用不一致、资金项目查询失败、没有匹配到敏感资方相关项目。
- **范围包含暂不支持的因子（如风险评级 `reloan_price_tag`）**：脚本会给出 `root_cause.type = unsupported_funding_factors` 及专项 `business_view`（标题与摘要已区分「自动闭环失败」与「资产侧结论仍可参考」）。Agent 须**原样放入** `business_view.headline`、`business_view.summary`、`business_view.evidence`，并在展示之后用一两句业务话串联：先概括「该切片承接率下降在资产维度上仍倾向于由本候选范围解释」，再说明「敏感资方侧需按指引手工核对」——不得省略摘要里的倾向性结论，也不得用「根据 SKILL 规则直接返回 R8」替代正文。
- 第四阶段是最终阶段，不再继续下钻。

展示要求：
- 以下 3 个展示步骤必须按顺序直接进入最终回复正文，不可省略，也不允许只在思考过程里做判断后在正文缩成一句"已闭环"或"未闭环"：
  1. 首先将 `business_view.headline` 作为结论标题、`business_view.summary` 作为摘要说明，直接写入正文（摘要已含 **【归因定级】** 与业务 rationale，须一并原样输出）；
  2. 其次逐条展示 `business_view.evidence` 中的项目级放款金额变化证据；
  3. 最后结合 `project_count_delta` 说明项目数变化，并明确给出"是否观察到敏感资方相关项目数量或放款金额同步下降"的判断。
- 在这 3 个步骤写入最终回复正文之前，不要先写"第四阶段结果""已闭环""未闭环"这类摘要或过渡话术。
- 第四阶段状态块只展示一次：先展示顶层 `status_line`，再展示 `business_view.summary` 与 `business_view.evidence`；禁止在 `summary` 和 `evidence` 内重复插入状态块。

## 第五阶段：最终总结
不再运行新脚本，直接基于各阶段已有结果做统一总结。

**视觉呈现增强（仅改样式，不改内容）**
- 标题分级固定为：`# 第五阶段` → `## 部分标题` → `### 子标题`；每个切片用 `## 切片N：<slice_display>` 起段。
- 每个切片前加分隔线 `---`，降低连续文本疲劳。
- 每个切片核心判断必须放引用块：`> **切片结论：** ...`；阶段核心判断同理可用 `> **资方分布结论：** ...`、`> **资产维度结论：** ...`。
- 关键状态句前加标签（不改原结论）：`**【已闭环】**`、`**【需手工验证】**`、`**【证据不足】**`、`**【弱信号】**`。
- 负向变化仅做 markdown 强调，不改数值：例如 `**-3.2%**`、`**-1.22万**`。重点字段：承接率变化、路由金额变化、占比变化、放款金额变化、降幅。
- 表格保持 markdown 形态；异常行通过关键单元格加粗体现（如 `是否下钻=是`、`是否命中=是`、`是否闭环=是`）。

**第零部分：全局进度行 + 状态汇总表（必须最先输出）**
- 先输出一行全局进度行，模板固定为：

  ```text
  > 📊 已完成 N/N 个切片：闭环 X · 结构迁移 Y · 证据不足 Z · 常规终止 W
  ```

  字段计数口径：`闭环 = LOCKED`、`结构迁移 = SHIFT`、`证据不足 = DATA-GAP`、`常规终止 = STOP`；分母 N 取 `analysis_sequence` 长度，分子 N 取已展示完成的切片数。

- 再输出一张状态汇总表，列固定为：`切片 | 终点阶段 | 状态 | 结论标签 | 是否闭环`。每一行直接来源于该切片各阶段的 `slice_status_summary`：
  - `切片` = `slice_status_summary.slice_display`
  - `终点阶段` = `slice_status_summary.end_stage_label`（例如「二级·资方分布」）
  - `状态` = `slice_status_summary.status_symbol` + 空格 + `slice_status_summary.status`（例如「⛔ STOP」「🔒 LOCKED」「🧩 SHIFT」「⚠ DATA-GAP」）
  - `结论标签` = `slice_status_summary.conclusion_tag`
  - `是否闭环` = `slice_status_summary.is_locked` 为 true 时填 `是`，否则 `否`

  该表是第五阶段唯一允许聚合所有切片的位置；禁止在表外再用列表形式重述切片状态。

**第一部分：承接率变化分层展示**
按两层顺序展示，直接复用第一阶段已输出的字段，不要重新拼写：
1. 整体承接率变化（来自 `primary_display.overall_summary_markdown`）
2. 惠选 / 精优客群承接率变化（来自 `primary_display.huixuan_group_markdown` / `jingyou_group_markdown`）

**第二部分：逐切片归因结论（路径回放 + 定级 + 数字证据）**
按客群（惠选 / 精优）分组，逐个切片给出归因；每个切片须按 **决策链路顺序** 叙述，避免跳结论：
- **路径回放（精简要版）**：**第二阶段路由信号**（`stage2_signal` / 是否左移）→ **第三阶段形态**（`asset_dimension_pattern_label`）→ **第四阶段闭环结果**（`business_view.headline` / `terminal_reason` 对应的中文语义）→ **`final_attribution_level` 定级**。
- **承接率快照（每个切片先写）**：先给出该切片的对比期承接率、当前期承接率、承接率变化（pp）；该三项直接引用第一阶段客群切片表对应行，不重新计算、不改口径。
- **资方准入分布**：总量是否下降；全桶分布路由信号（左移 / 未左移）；配上「资方分布关键数」。
- **资产维度**（若进入第三阶段）：优先引用形态判别结论，再补充命中因子（高龄 / 风险评级 / 身份证有效性 / 特殊区域）与关键桶数字。
- **敏感资方闭环**（若进入第四阶段）：已定位到 XXX 范围；同步复述脚本给出的 **归因定级**（`final_attribution_level`）及放款/项目数证据。
- **切片结论**：在路径回放与定级之后，用一句话收束「当前最可能解释」，注明已闭环 / 待验证 / 证据不足。

**逐切片写作要求（第五阶段）**
- 每个切片在“切片结论”前，必须先给出可复核数字，不可只写“偏高/偏低/有变化”这类抽象判断。
- 数字证据至少包含：
  1. `承接率快照`：对比期承接率 / 当前期承接率 / 变化（pp）；
  2. `资方分布关键数`：引用第二阶段返回字段/表格中的数值（勿凭记忆填写 CDF 比例或阈值）；
  3. `资产命中桶数字`（若进入第三阶段）：引用脚本表格中的桶标签与数值；高龄以脚本输出的原始 `age_rand` 为准；
  4. `资方闭环数字`（若进入第四阶段）：敏感资方放款金额变化、项目数变化。
- 若某切片缺少上述某类数字，需明确写“该项数字暂缺 + 原因”（如字段未接入、阶段未进入）。
- 参考写法：`年龄（示例「7.>55」）客群承接率：当前 XX%，对比期 YY%，变化 ZZ pp；新疆/西藏客群承接率：当前 AA%，对比期 BB%，变化 CC pp。`（桶名以脚本输出的原始 `age_rand` 为准。）

复用各切片的 `business_view.headline / summary` 作为归因内容主体，不要重新拼话。切片停在第一阶段（R2/R9/R10）的也要单独列出并说明停止原因。

**第三部分：建议与数据缺口**
- 提炼跨切片共性：多个切片指向同一问题时合并成一条结论，不要逐条堆砂。
- 给出优先建议：已闭环的联系资方确认；分布未左移的排查规则/授用信通过率；资金侧无法自动闭环的给出手工核查指引。
- 说明数据缺口：授用信通过率未接入、规则变更需手工核查、高龄/风险评级暂不支持自动闭环等。

输出约束：
- 用业务语言呈现，不暴露内部终止码（R2/R3/R4a/R4b/R11 等）、`root_cause`、`next_action` 等内部词。
- 若 R2 触发，说明结构迁移的业务含义（哪些切片占比在增加/减少），解释为什么不进入资方诊断。
- 禁止只给抽象判断（如“偏低”“偏高”“有变化”）；凡能从阶段表格或 `business_view.evidence` 取得的数字，必须在第五阶段逐切片结论中落字。

## 内部终点码速查（**仅供对照 JSON**；业务叙述用中文、不念码。具体是否触发以脚本返回为准。）
- `R1`：大盘未下降
- `R2`：一级结构迁移（路由份额主导大盘降幅；不进资方诊断）
- `R3`：准入资方总量明显减少（历史码；现仅辅助，不作二阶段终止）
- `R4a`：资方分布未见整体下行（规则/通过率另核），停在第二阶段
- `R4b`：资产侧停在第三阶段（弱信号未达桶门槛 / 无达门槛异常桶等，见 `root_cause`）
- `R5`：有异常桶但未锁定达门槛的最小因子范围（范围路由金额阈值见 `ASSET_RANGE_*` 常量），停在第三阶段
- `R12`：五维原始桶门禁均通过（R12 展示由脚本生成）；停在第三阶段，不自动跑资金项目
- `R6`：最小因子范围成立但敏感资方未同步收缩，停在第四阶段
- `R7`：敏感资方收缩（已闭环），停在第四阶段
- `R8`：证据或字段不足，停在各阶段
- `R9`：目标客群未达继续分析门槛，停在第一阶段
- `R10`：目标客群无可下钻切片，停在第一阶段
- `R11`：准入资方总量未下降（历史码；现仅辅助）
