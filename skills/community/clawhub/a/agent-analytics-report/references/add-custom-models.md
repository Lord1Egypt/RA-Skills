# 以后新加自定义模型：用大白话告诉 Agent 就行

下载时 Agent **通常**会帮你把**当时用过的** `custom-local:*` 模型注入（见 [`on-download-inject.md`](on-download-inject.md)；注入前的授权边界见该文件开头的说明）。这份文件有两重用途：**① 如果当时没注入**（没读到下载 Prompt、或手动装技能），用下面的「一次性补齐所有自定义模型」Prompt 让 Agent 扫描并写入你**全部**自定义模型；**② 以后新加**单个/少量模型时，不用全量扫描，直接说句大白话即可（见「最简单」一节）。

## 如果当时没注入 / 想一次性补齐所有自定义模型

要是下载时 Agent 没自动注入（比如没读到下载 Prompt、或你手动装的技能），直接用下面这段让 Agent **扫描你本机用过的一切自定义模型并全部注入**。无需先去找 `on-download-inject.md`，这一段就够了：

### 先看授权边界：这段 Prompt 会让 Agent 做什么

下面这段 Prompt **不是只读操作**。它明确要求 Agent 做两件会碰文件系统的事，用之前请先确认你接受：

| 动作 | 范围 | 什么时候发生 |
|---|---|---|
| ① **递归扫描（读）** | **仅限 `~/.workbuddy`**（Windows 上即 `C:\Users\<你>\.workbuddy`），用 `grep -rhoE "custom-local:[a-zA-Z0-9._-]+" ~/.workbuddy` 找出你用过的自定义模型名 | 你把下面 Prompt 贴给 Agent、且它开始跑第 1 步时 |
| ② **写配置（写）** | **只写** `（技能目录）/scripts/pricing.local.json` 的 `custom_local` 段（键为去掉 `custom-local:` 前缀、转小写后的底层名），**不碰任何其它文件** | **只有你明确说出每个模型的 RMB 单价数字**（或明确说「按这段提示词执行」）之后才会写 |

三点务必注意：
- **技能不会自动执行这段 Prompt。** 生成报告的默认流程是**只读采集 + 只写报告产物**，既不递归扫 `~/.workbuddy`，也不改任何配置文件；上面的扫描与写入只在你主动使用本文件时发生。
- **你也可以只要清单、先不写入。** 只要你说「先只列出来给我看，不要写文件」，Agent 就应当只回显清单、停在原地等你后续指令。
- **不给单价就不写。** 拿不到单价的模型一律标「待补」跳过；**未得到你对具体条目数字的确认，Agent 不得写入或改动任何条目**（含官方模型条目）。

> 我刚下载了 agent-analytics-report 技能，但我的自定义模型还没写进定价库。请帮我把我在 WorkBuddy 里用过的**所有**自定义模型（custom-local 自建通道）的单价，全部加进这个技能的 pricing.local.json，这样以后报告能算出它们的真实花费。
>
> 请你照下面做：
> 1. 扫描我本机 WorkBuddy 数据目录（一般在 `~/.workbuddy` 下的 `workbuddy.db` 和 traces 文件），找出**所有出现过的 `custom-local:xxx` 模型名**。可以用这个命令发现：`grep -rhoE "custom-local:[a-zA-Z0-9._-]+" ~/.workbuddy 2>/dev/null | sort -u`
> 2. 把找到的自定义模型名列出来给我看。
> 3. 逐个问我每个模型的 RMB 单价：输入多少钱、输出多少钱（单位：元 / 每百万 tokens，按我接口方的实际账单填，比如自建 DeepSeek、自建开源模型的服务方）。
> 4. 把它们在定价文件 `（技能目录）/scripts/pricing.local.json` 的 `custom_local` 段写成：`"底层名(去掉 custom-local: 前缀、小写)": {"input": X, "output": Y}`。
> 5. 只往 `custom_local` 里追加/更新我的模型，**不要改**任何官方模型条目，也不要删其它字段。
> 6. 改完把新增的条目回显给我确认。
> 7. 如果某个模型我一时给不出单价，先跳过、标个「待补」，别卡住。
> 8. **第 4 步真正落盘之前，必须先把「将要写入的条目清单」（模型名 + 输入价 + 输出价）完整回显给我看；只有我回复确认后才允许写入**，否则就停在清单这一步、不要动文件。
>
> 如果第 1 步一个 `custom-local:` 模型都没扫到，说明我还没用过自建接口，直接告诉我"未发现自定义模型"就好，不用写任何东西。

Agent 只会在**你逐个确认单价、且确认过待写入条目清单之后**才写 `custom_local` 段，且只追加/更新你自己的模型、保留官方模型不动；未确认单价的模型标「待补」留在清单里，**绝不擅自写入、也绝不改动任何官方模型条目**。写完后重跑报告（见下方「验证 & 注意」）即可看到自定义模型正常计价。

## 最简单：直接说人话（推荐，仅用于新增单个/少量模型）

把下面这句话改改贴给你的 Agent 即可，不用记任何格式：

> 我刚在 WorkBuddy 里新加了个自定义模型，名字叫 `custom-local:deepseek-r1`，自建 DeepSeek 的价格是输入 2 元、输出 8 元（每百万 token）。帮我把它加进 agent-analytics-report 技能的 pricing.local.json 里，以后报告好算它的花费。

Agent 会：① 找到定价文件 `（技能目录）/scripts/pricing.local.json`；② **先把待写入条目回显给你、得到确认后**在 `custom_local` 段加 `"deepseek-r1": {"input": 2.0, "output": 8.0}`（去前缀、转小写）；③ 只追加、不改官方模型；④ 写完再回显最终结果给你核对。（自动的只是「定位文件 + 按格式落值」这一步；**写哪个值、要不要写，仍以你给出的单价和你对回显清单的确认结果为准**。）

一次加多个也行：

> 我新加了俩自定义模型：`custom-local:deepseek-r1`（自建，输入 2 / 输出 8）和 `custom-local:qwen3-235b`（自建 vLLM，输入 1 / 输出 2）。都帮我写进 agent-analytics-report 的 pricing.local.json。

## 如果 Agent 不确定写哪、怎么写（给它的完整指令）

> 请在 agent-analytics-report 技能的 `scripts/pricing.local.json` 里加上我的自定义模型单价。
> - 技能路径：`<你的技能目录，例如 ~/.workbuddy/skills/agent-analytics-report/scripts/pricing.local.json>`
> - 我的模型（单位：元 / 每百万 tokens，输入、输出分开）：
>   - `<模型 A 名，如 custom-local:deepseek-r1>`：输入 `<X>` / 输出 `<Y>`
>   - `<模型 B 名>`：输入 `<X>` / 输出 `<Y>`
>
> 要求：① 先读该 `pricing.local.json` 确认结构（`models` / `timed_free` / `custom_local` / `default_model`）；② 带 `custom-local:` 前缀的写进 `custom_local` 段、键去前缀小写，裸名写进 `models` 段；③ 只在这两个段追加/更新，**不改**官方模型、不删其它字段；④ 用 Edit 工具精准改；⑤ **落盘前先把待写入条目回显给我，得到我确认后才许写入**；⑥ 改完再回显最终结果给我核对。

## 示例（自建 DeepSeek）
WorkBuddy 里把 DeepSeek 配成 OpenAI 兼容端点、模型名 `custom-local:deepseek-r1`，贴给 Agent：

> 请在我的 agent-analytics-report/scripts/pricing.local.json 的 custom_local 段加：`deepseek-r1` 输入 2.0 / 输出 8.0（按我自托管/接口方实际成本填）。

写入后：
```json
"custom_local": {
  "deepseek-r1": {"input": 2.0, "output": 8.0}
}
```

## 验证 & 注意
- 写完后重跑报告：`collect_usage_data.py --period month` → `generate_report.py`，§3.1 / §3.2 里你的自定义模型应正常显示单价与花费，不再标「未配置」。
- 单价按你接口方**实际账单**填（缓存未命中价）；示例的 DeepSeek 数字仅为占位，请以你自托管/接口方实际成本为准。
- `custom_local` 没配时采集器回退到同名官方模型价；无同名官方模型（如自建 `deepseek-r1`）会显示「未配置」——所以务必配上。
- 这些改动只在**你本机下载的副本**的 `pricing.local.json` 里；该文件**不进发布包**，所以 `skillhub upgrade` 升级技能时**不会被覆盖**——你的自定义模型单价自动保留，无需备份或重注入。
