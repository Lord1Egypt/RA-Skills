---
name: cue-hotspot-tracker
slug: cue-hotspot-tracker
displayName: 盘中热点与催化剂追踪
description: 用 Cue 通常 5-10 分钟（最长约 15 分钟）实时扫描今日 A 股热点板块与近 24h 催化资讯，拆解盘中催化逻辑与受益方向；跑完自动生成「看板图」与「报告长图」，报告全文以 Cue 链接交付。
description_zh: Cue 热点追踪：通常 5-10 分钟、最长约 15 分钟，实时扫描今日 A 股热点板块与近24h催化资讯，拆解催化逻辑与受益方向，识别热钱流向，并自动出看板图与报告长图。
version: 1.4.5
author: sensedeal
tags: [cue, hotspot, catalyst, trading, 热点追踪, 题材挖掘, 短线, 催化剂, 看板图, 长图, 报告转图]
---

# 盘中热点与催化剂追踪

> 短线题材捕捉手。通常 5-10 分钟（最长约 15 分钟）实时扫描今日 A 股热点板块，拆解盘中催化逻辑与受益方向，助你紧跟市场热钱流向。

## Agent 执行摘要

| 顺序 | 做什么 | 禁止 |
|------|--------|------|
| 1 | **确认 API Key 已配置 + Cue runner 就绪**（未配置先按步骤 0 引导创建） | 禁止跳过 |
| 2 | 启动后**立即**告知用户：预计 2-15 分钟（多数 5-10 分钟），期间**不要重复提交同一问题**；超过 15 分钟再查进度 | 禁止中途取消；禁止重复提交；禁止只发命令让用户干等 |
| 3 | 一条命令阻塞等待，`--template-id template_maVyo-` | 禁止连发多条 |
| 4 | stdout `[cue-research] RESULT ok` = 完成 | 无 RESULT = 未完成 |
| 5 | **直接出两张图**：报告长图（`scripts/render.py`）+ 看板图（本 agent 先重排成 SOP JSON，再 `scripts/render_dashboard.py`） | 禁止跳过重排直接塞报告原文，禁止编造报告里没有的字段 |
| 6 | 交付**两张图路径 + Cue 原始报告链接**；报告正文**不贴进聊天** | 禁止编造链接，禁止把报告正文大段贴出 |
| 7 | 无 Chrome 时如实降级为 HTML | 禁止谎称出图 |
| 8 | 交付后**用选项弹框**问是否设置定时：每个交易日 10:00（推荐，开盘 30 分钟后）/ 自定义时间 / 暂不设置 | 禁止只发文字提醒；禁止未经用户选择擅自开启 |
| 9 | 遇 `INSUFFICIENT_CREDITS` 按「积分不足专项提示」给出两条路径 | 禁止只丢错误码 |

### 步骤 0：接入与装配 + 首任务引导（任何任务之前，必须最先执行）

开跑任何任务前，先确认 API Key 已就绪：

1. **检查 Key**：`~/.cue/config.json` 的 `api_key`（或环境变量 `CUE_API_KEY`）是否有值。
2. **未配置 / 失效**：**停止任务**，由用户本人创建（Agent 不能代生成、无权查看）。按以下话术告知：
   > 请前往 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-hotspot-tracker) 注册后免费创建 API Key，点击「创建 API Key」，生成后点「复制」并粘贴发送给我。
   拿到 Key 后写入 `~/.cue/config.json`；若本 skill 依赖 MCP 工具，按对应小节完成挂载并提示重启客户端。
3. **健康检查全绿后**，若用户还没给出具体任务，**必须主动引导第一次真实调用**，不要停在"环境已就绪"：
   > 环境已就绪 ✅ 下面这些都可以直接跑，比如：
   > 1. "今天市场有哪些实时热点板块？"
   > 2. "现在哪些板块在领涨？什么逻辑？"
   >
   > 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题用本 skill 示例小节的原文，别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

## 启动告知（必须执行）

发出运行命令后**立即**向用户发一次预期说明，不要等报告生成完才说：

> 报告已开始生成，预计 **2-15 分钟**（多数 5-10 分钟）。这期间**不用重复发同一问题**——重复提交会新建任务、重复消耗积分；完成后我会直接出**看板图 + 报告长图**，并把 Cue 原文链接一起发你。超过 15 分钟还没出来，我帮你查进度。

规则：
- **必须先说再跑**（最晚与运行命令同一轮回复），不得只发命令让用户干等。
- 等待期间用户再次追问**同一问题**时：**不新建任务**，回复当前任务仍在生成并说明已等待时长；超过 15 分钟才按「中途中断」流程查进度或续接。
- 用户换行业、换方向或追问报告细节，属于新问题，可正常受理，不算重复提交。
- 出图在报告完成后进行，**不额外消耗 Cue 积分**；但整体交付会比只有报告多花约 1-2 分钟，等待期间不用催图。

## 适用场景

| 场景 | 解决的问题 |
|------|-----------|
| 盘中实时热点扫描 | 开盘后实时捕捉今日 A 股正在走强的热点板块 |
| 题材催化拆解 | 突发消息的实时催化逻辑与受益方向拆解 |
| 短线选股参考 | 识别受益板块和个股 |
| 风险事件规避 | 识别可能冲击持仓的负面催化剂 |

## 核心能力

1. **今日 A 股实时热点扫描** — 开盘后实时捕捉当前交易日正在走强的热点板块与领涨方向
2. **催化逻辑拆解** — 每条热点/资讯 → 对 A 股的传导路径和影响程度
3. **受益板块识别** — 按催化强度排序受益行业
4. **热钱流向判断** — 结合盘面信号判断资金方向

## 试试这样问

- "今天市场有哪些实时热点板块？"
- "现在哪些板块在领涨？什么逻辑？"
- "今日 A 股热点板块资金在买什么？"
- "盘中有什么突发消息在催化板块？"
- "跑一下今天的盘中热点，出报告和图"

## 输出形式

**两张图 + 一个链接**：看板图（固定版式，适合发布）+ 报告长图（报告原文照搬）；报告全文走 Cue 原始链接，**不贴进聊天**。

## 输出示例

[查看完整报告](https://cuecue.cn/share/cO1M8Hcv?i=G522KBT7)

> 上例中的 token 是示例，**不可复制到实际交付中**。

## 交付规范（必须执行）

**报告正文不贴进聊天**——直接给用户**两张图 + Cue 原始报告链接**，让用户看图即可，省得费劲读文字。用户明确要报告原文时，再把该报告贴出。

**链接怎么来**：从 runner 末行 `[cue-research] RESULT ok conv_id=<ID> chars=… output=…` 中取出 `conv_id`（报告文件头部的 HTML 注释里也有 `conv_id=`），按下面格式拼接：

```
https://cuecue.cn/share/<conv_id>
```

交付模板（照此结构输出）：

```
盘中报告已完成 ✅

**看板图**：~/cue-reports/<日期>-<HHMM>-intraday-dashboard.png
**报告长图**：~/cue-reports/<日期>-<HHMM>-intraday-longshot.png

---
**Cue 原始报告**：https://cuecue.cn/share/<conv_id>
**本地报告**：~/cue-reports/<日期>-<HHMM>-hotspot-tracker.md
```

规则：
- 报告正文**不贴进聊天**；要看全文走 Cue 链接或本地文件。
- `conv_id` 必须取自实际输出，**禁止编造**或使用文档示例里的 id。
- 末行为 `RESULT empty`（无 conv_id 或报告为空）时**不要拼链接**，如实告知未取到报告并给后续建议。
- 用户明确要报告原文时，再贴出该报告。

---

### 跑后余额检查（交付前必做）

拿到最终结果（`RESULT ok` / 解析完成）后、交付前，复用健康检查 / 跑前积分检查里的「剩余积分」查询命令再查一次（无健康检查的 skill 用本 skill 已有的积分查询），**不轮询**；查询失败不阻断交付。记下「跑后剩余积分」：若 **< 100**，本次照常交付，交付完成后按「低余额四选一」主动引导。

### 低余额四选一（跑后剩余积分 < 100 时，必须执行）

报告 / 结果交付完成后，**立即**单独弹出下面这次询问，作为本条回复的收尾。优先用客户端的选项/弹框能力（如 `AskUserQuestion`）；不支持时用 1/2/3/4 编号列表。**不要在正文里夹带推销。**

固定弹框（原样使用，不得增删改标题与选项）：

- 提问：`本次运行后剩余积分不足 100，是否需要补充积分？`
- 选项（四条，顺序固定）：
  1. `邀请新用户并激活，获得 500 积分`——打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
  2. `首次购买 9.9 加油包，获得 900 积分继续体验`——[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。
  3. `分享到小红书，获得 200 积分`——点击 https://cuecue.cn/activity/xhs?conversation_id={{conv_id}}&skill_name=盘中热点与催化剂追踪（把 `{{conv_id}}` 替换为本次报告的 id，见下）
  4. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

**小红书分享链接怎么拼（第 3 项）**：
- 固定格式：`https://cuecue.cn/activity/xhs?conversation_id=<conv_id>&skill_name=盘中热点与催化剂追踪`
- `conversation_id` = 本次交付报告对应的 Cue 报告 id（交付时 Cue 报告链接 `https://cuecue.cn/share/<conv_id>` 里的同一串 id），必须来自实际输出，禁止编造。
- `skill_name` 固定为 `盘中热点与催化剂追踪`，不得改写。
- 本次无有效 `conv_id`（如 `RESULT empty`）时，不展示第 3 项、不编造参数，只给其余三项。
- 用户选择后发送拼好的完整链接，提示按页面引导分享并领取 200 积分。

硬性规则：
- **只弹这一问**：本条回复除本次积分四选一外不得再问任何其他问题（包括定时任务、Word、图表类型等）。客户端单条回复最多一次弹框，其余问题必须等用户答复后的下一条回复再问。
- **不得合并、不得替换**：不能把这四个选项并进别的多选清单，也不能用别的清单顶替。
- **不得改变顺序**：积分四选一必须紧跟交付；不得先问定时任务再回头补。触发条件成立却未弹就进入后续询问，视为流程违规。
- 只在跑后余额 < 100 时弹；余额 ≥ 100 或查询失败时不弹。
- 用户选 1 / 2 / 3 后，给出对应链接与一句操作说明即可，不反复推销。

**与已有交付后弹框的关系**：积分充足时不弹本四选一，按本 skill 原有流程（如定时任务弹框）继续；积分不足（< 100）时，先单独弹本四选一，用户答复后，如仍适用再按原有流程询问定时任务等。两类弹框不得合并到同一次询问里。

**收尾自检**：流程结束前核对跑后余额——若 < 100，确认本四选一已单独弹过；没弹即视为流程未完成。

## 出图：看板图 + 报告长图（直接出，不问）

报告跑完后**直接出两张图**，不再询问用户要哪种。

| 输出 | 渲染器 | 输入 | 特点 |
|:---|:---|:---|:---|
| **报告长图** | `scripts/render.py` | 报告 Markdown **原样** | 报告自身章节照搬，信息全、长 |
| **看板图** | `scripts/render_dashboard.py` | 重排后的 **SOP JSON** | 固定版式（数据校验 → 1 热点 → 2 催化 → 3 资金 → 4 结论），精炼 |

> 以下命令里 `scripts/...` 相对 **skill 根目录**；若当前工作目录不是 skill 根，请用 skill 的绝对路径。

### 报告长图（一步）

```bash
python3 scripts/render.py <报告md> -o ~/cue-reports/<日期>-<HHMM>-intraday-longshot.png
```

### 看板图（两步，中间一步必须由本 agent 做）

看板图**不能直接吃报告**——中间必须有一层「重排」：本 agent 读报告 → 按 `references/sop-schema.md` 把内容填进 SOP JSON → 再渲染。样例见 `assets/intraday-sample.json`。

1. 重排成 JSON，落盘 `~/cue-reports/<日期>-<HHMM>-intraday.json`。
2. 渲染：

```bash
python3 scripts/render_dashboard.py ~/cue-reports/<日期>-<HHMM>-intraday.json -o ~/cue-reports/<日期>-<HHMM>-intraday-dashboard.png
```

### 出图硬规则

- **只做盘中**：本 skill 仅服务**盘中**，看板 / 长图的标题、页脚、数据校验一律「盘中」口径，**禁止**出现「盘后」「收盘复盘」等字样。
- **时间一律取「报告生成时间」**：看板「数据校验 → 数据时间」由 agent 填、长图标题下的时间行由 `render.py` 自动提取——两者同源，都取报告头部 HTML 注释的 `| YYYY-MM-DD HH:MM`（长图渲染成「YYYY-MM-DD 盘中（报告生成 HH:MM）」）。**不要**用正文「数据截至 …」那类收盘模版字段（长图仅在报告无注释时才退回它）。
- **合规弱化版**：看板内**不得**出现 `市场评级`、`关注强度上限`、`看多 / 谨慎 / 防守条件`、`今日不做`、`可加码` 等带买卖倾向字段；第 4 块只留客观的「一句话结论 + 盘面主线 + 风险提示」。
- 图内**必须**含「不构成任何投资建议」（两个渲染器已内置）。
- 重排字段（数据校验 / 强度 / 结论 / 标签）报告里**没有现成值**，由模型归纳，**不得谎称是报告原文**；报告没有的标「报告中未提及」，**禁止编造**。
- 依赖 headless Chrome / Chromium / Edge：**有则 PNG**；找不到浏览器时脚本会**自动用默认浏览器打开 HTML** 让你直接看到成品（终端也打印路径）——仍**不得谎称出了图**。
- 交付目录 `~/cue-reports/` **只留 PNG**，命名 `<日期>-<HHMM>-intraday-{dashboard|longshot}.png`；中间产物 HTML 收在**同级 `<图名>.src/` 子目录**里（调样式用，不交付给用户）。

---

## 最佳用法（交付后必做：弹框询问定时任务）

本 skill 的核心价值在**盘中实时**——9:30 开盘后热点板块才逐步成形，手动跑容易错过早盘强势题材。最佳用法是**设置定时任务，每个交易日 10:00 自动跑一次**（开盘 30 分钟后，早盘热点已初步明朗）。

**交付报告后，不要只发一句"建议定时跑"的文字提醒，必须直接弹出选项让用户点选。**

### 弹框内容（必须三选一）

优先用运行环境自带的选项弹框能力（如 Claude Code 的 `AskUserQuestion`）。环境不支持弹框时，把同样的三个选项以编号形式写在正文末尾，等用户回复编号。

> **要不要把盘中热点追踪设成定时任务，每个交易日盘中自动跑？**
>
> 1. **每个交易日 10:00（推荐）** — 开盘 30 分钟后，早盘热点与催化逻辑已初步明朗
> 2. **自定义时间** — 自己指定几点、每周哪几天（可设多个时点，如 10:00 和 14:00 各跑一次）
> 3. **暂不设置** — 这次先看报告，以后需要随时说

选「自定义时间」时，必须追问**几点跑、每周哪几天**。并提醒用户：**盘中热点只在 9:30–11:30 / 13:00–15:00 交易时段内有意义**；下午再跑一次能捕捉午后新题材，但**每多跑一次就多消耗一份 Cue 积分**。

### 铁律

- **禁止擅自开启**：用户没有明确选择时间之前，不得创建任何定时任务、cron、launchd。
- **禁止只发文字**：文字提醒不算完成，必须给出可点选的选项。
- **每次交付问一次**：用户配置成功或明确选「暂不设置」后，后续交付不再重复打扰。
- **禁止谎称已设**：当前客户端不支持定时任务时，给出时点清单让用户自行设提醒，并说明未配置。

### 用户选定后怎么配

统一用同一套命令跑（`<skill根目录>` 换成该 skill 的实际安装路径）：

```bash
TS=$(date +%Y-%m-%d-%H%M)
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "今日A股实时热点板块扫描与催化逻辑分析" \
  --template-id template_maVyo- \
  --output ~/cue-reports/$TS-hotspot-tracker.md \
&& python3 <skill根目录>/scripts/render.py ~/cue-reports/$TS-hotspot-tracker.md \
  -o ~/cue-reports/$TS-intraday-longshot.png
```

按运行环境选一种落地方式：

| 环境 | 配置方式 |
|------|---------|
| Claude Code | 用 `CronCreate`，cron 表达式 `0 10 * * 1-5`（自定义时间按用户所选取 分 时 日 月 周）；触发时由 agent 完整执行「跑研究 → 出两张图 → 交付」，与手动跑一致 |
| macOS | 建 `~/Library/LaunchAgents/com.cue.hotspot-tracker.plist`，`StartCalendarInterval` 设 `Weekday` 1–5、`Hour` 10、`Minute` 0，再 `launchctl load`；只跑上面这条 shell 链路（报告 + 长图） |
| Linux | `crontab -e` 追加 `0 10 * * 1-5 <上面的脚本>` |

配完必须回报三件事：**触发时间、输出目录、如何关掉**（Claude Code 删任务 / `launchctl unload` / `crontab -e` 删除对应行）。

### 必须提前告知的三个坑

- **每次运行都会消耗 Cue 积分**；设多个时点按次数叠加，余额不足时当天会失败，需按「积分不足专项提示」补充积分，不会自动跳过。
- **无界面跑批出不全两张图**：launchd / crontab 只能自动出报告 md + 报告长图；看板图需要 agent 先重排 SOP JSON，须下次交互时基于已落盘的 `.md` 补生成。Claude Code 的 `CronCreate` 触发时会叫醒 agent，可完整出两张图。
- **法定节假日仍会触发**：cron 只认周一到周五；节假日可能返回空结果或沿用前一交易日数据，属正常现象。报告与图片只落盘 `~/cue-reports/`，不会推送，需要自己打开看。

---

## 环境要求

Runner 来源：[GitHub - sensedeal/cue-skills](https://github.com/sensedeal/cue-skills)（[Gitee 镜像](https://gitee.com/sensedeal/cue-skills)）。

首次使用需安装 Runner（幂等，已装则拉取更新）：

```bash
if [ -d ~/.cue/cue-skills/.git ]; then
  git -C ~/.cue/cue-skills pull --ff-only
else
  git clone https://github.com/sensedeal/cue-skills ~/.cue/cue-skills \
    || git clone https://gitee.com/sensedeal/cue-skills ~/.cue/cue-skills
fi
```

依赖：`git` + `python3` + `curl`。Python 仅用标准库，无额外 pip 依赖。

Cue API Key：在 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-hotspot-tracker) 注册后免费创建 API Key，`cue login` 写入 `~/.cue/config.json`。新账号送 500 积分。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发送给您正在使用的智能体。

> **API Key 只能由用户本人创建**：Agent 既不能代生成、也无权查看用户的 Key。检测到未配置或失效时，按以下话术告知用户：**「点击『创建 API Key』，生成 API Key 后一定要点击『复制』并粘贴发送给我。」** 然后等待用户提供，**禁止声称"我去生成/查看"**。

---

## 调用说明

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "今日A股实时热点板块扫描与催化逻辑分析" \
  --template-id template_maVyo- \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-hotspot-tracker.md
```

| 参数 | 说明 |
|------|------|
| `--query` | 研究问题。可选加行业/方向限定 |
| `--template-id` | 固定为 `template_maVyo-` |
| `--output` | 落盘路径 |

---

## 格式转换

Cue 输出 Markdown。安装 pandoc 后可转换为 Word 或 PDF：

```bash
# .md → .docx（Word）
pandoc report.md -o report.docx

# .md → .pdf
pandoc report.md -o report.pdf --pdf-engine=xelatex
```

输出文件与输入同目录、同名、不同后缀。

### 依赖安装

| 目标格式 | 依赖 | macOS | Ubuntu |
|----------|------|-------|--------|
| Word (.docx) | pandoc | `brew install pandoc` | `sudo apt install pandoc` |
| PDF (.pdf) | pandoc + LaTeX | `brew install --cask basictex` | `sudo apt install texlive-xetex` |

---

## 架构说明

本 Skill **不在本地执行检索**。流程是 Agent → Cue API（cuecue.cn）→ 外部数据源。解析结果的质量和时效取决于 Cue 服务端和外部数据源的状态。

| 环节 | 谁控制 | 出问题时 |
|------|--------|---------|
| API Key 鉴权 | 用户本人 | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-hotspot-tracker) 生成后点「复制」并粘贴发送给您正在使用的智能体，再由 Agent 写入 ~/.cue/config.json（Agent 不能代生成，也无权查看） |
| Cue 服务端 | Cue 运维 | 等恢复，或走降级方案 |
| 外部数据源 | 公开网站 | Cue 用缓存兜底，标注"来源暂不可达" |

---

## 健康检查

跑研究前先验证四件事。一键诊断：

```bash
CUE_KEY=$(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])" 2>/dev/null || echo "$CUE_API_KEY")
echo "=== 1/4 API Key ===" && [ -n "$CUE_KEY" ] && echo "已配置" || echo "未配置！"
echo "=== 2/4 Cue 服务 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/health" -H "Authorization: Bearer $CUE_KEY"
echo "=== 3/4 搭子 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/playbook" -H "Authorization: Bearer $CUE_KEY" | python3 -c "import sys,json;scenes=json.load(sys.stdin).get('data',{}).get('scenes',[]);buddy=[b for s in scenes if s.get('secondary_category')=='短线盘面' for b in s.get('buddies',[]) if b.get('title')=='24h热点与催化剂追踪'];print(f'可用:{len(buddy)}个') if buddy else print('暂不可用')"
echo "=== 4/4 剩余积分 ===" && python3 -c "
import json, urllib.request, os
p = os.path.expanduser('~/.cue/config.json')
k = (json.load(open(p)).get('api_key') if os.path.exists(p) else '') or os.environ.get('CUE_API_KEY', '')
req = urllib.request.Request('https://cuecue.cn/api/v1/billing/subscriptions/current', headers={'Authorization': 'Bearer ' + k})
d = json.load(urllib.request.urlopen(req, timeout=10)) or {}
d = d.get('data', d) or {}
a = d.get('available_credits') or 0; q = d.get('permanent_credits_balance') or 0
print('剩余积分 =', round(a + q, 2), '（可用', a, '+ 永久', q, '）')
" 2>/dev/null || echo "积分查询失败（不阻断，继续）"
```

> **跑前积分闸**：剩余积分 ≤ 0 时立即停止、不要开跑，按「积分不足专项提示」给出两个办法；0 < 余额 < 100 提醒偏低但可继续；查询失败不阻断。

| 检查 | 预期 | 异常处理 |
|------|------|---------|
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-hotspot-tracker) 生成后点「复制」并粘贴发送给您正在使用的智能体（Agent 无法代生成，也无权查看） |
| 服务 | `{"status":"healthy"}` | 等 5 分钟重试 |
| 搭子 | `可用:>0个` | 等 1h 或网页端手动跑 |

> 配置完成后的首次调用引导已并入「步骤 0：接入与装配 + 首任务引导」，按该节执行。

---

## 自救指引

### 错误速查

| 现象 | 原因 | 怎么修 |
|------|------|--------|
| 401 / Key 无效 | Key 过期或写错 | 由用户本人重新生成 Key，更新 `~/.cue/config.json` |
| 超时 >30s | 服务维护/过载 | 等 5 分钟，跑诊断；当天内重试 |
| 搭子不可用 | 临时下线 | 网页端直接跑，或等 1 小时 |
| 积分不足 | 余额 < 消耗 | **按「积分不足专项提示」主动引导**（邀请新用户得 500 积分 / 9.9 加油包 900 积分） |
| 中途中断 | 队列满/数据源波动 | **不换 prompt**，相同命令续接 |
| `RESULT empty` | 公开源无匹配 | 缩小范围，换关键词 |
| config.json 报错 | JSON 格式不对 | `{"api_key": "sk..."}` 无多余逗号 |

### 积分不足专项提示（必须执行）

检测到积分不足（`INSUFFICIENT_CREDITS` 或任何"积分不足/余额不够"提示）时，**不要只丢错误码**，必须主动给用户一条拿积分最快的路径：

> 你的 Cue 积分不足，本次任务未能启动。两个办法：
> 1. **邀请新用户并激活，获得 500 积分**：打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
> 2. **首次购买 9.9 加油包，获得 900 积分继续体验**：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。

规则：
- 提示要**主动、简短、可点**——把「邀请页链接」和「复制专属邀请链接」两个关键动作说清楚，不要让用户自己找入口。
- 积分不足**不要重试**（`retryable: false`），也不要换 query 绕。
- 用户回复已充值/已邀请后，用**完全相同的命令**重跑。

### 决策树

```
出问题？
├─ Key 报错 → 由用户本人重新生成 → 更新 config.json → 重试
├─ 连不上 → curl /api/health 确认 → 检查 DNS/代理
├─ 搭子找不到 → curl /api/playbook → 等或用网页端
├─ 中途中断 → 相同 prompt 续接（不要删 ~/.cue/session/task）
└─ 结果空 → 缩窄关键词 → 确认该主题有公开数据
```

### 调度建议

| 时段 | 建议 |
|------|------|
| 交易日 10:00 | 定时跑的最佳时点（开盘 30 分钟后早盘热点已明朗） |
| 工作日 9-18 | 正常使用 |
| 夜间/周末 | 可能有维护，跑前先诊断 |
| 新 Key | 必须先诊断确认生效 |
| 连续失败 | 停 15 分钟再试，不要反复重试 |

---

## 降级方案

Cue 长时间不可达时的手动替代渠道：

| 渠道 | 覆盖 | 费用 |
|------|------|------|
| [东方财富](https://www.eastmoney.com) | A股资讯、公告 | 免费 |
| [华尔街见闻](https://wallstreetcn.com) | 全球财经快讯 | 免费 |
| [财联社](https://www.cls.cn) | 电报式财经资讯 | 免费 |
| [Reuters](https://www.reuters.com) | 国际财经新闻 | 免费 |

---

## FAQ

**Q: 和投顾早盘简报有什么区别？**
A: 早盘简报面向理财师生成客户沟通素材；热点追踪面向交易员做催化剂拆解和板块映射。

**Q: 能指定关注的行业吗？**
A: 可以，在 `--query` 中说明，例如"重点关注新能源和半导体方向"。

**Q: 报告能在网页端看原文吗？**
A: 能。交付时会附 `https://cuecue.cn/share/<conv_id>`，点开即可在网页端查看完整原文、继续追问或转发同事。

**Q: 等了几分钟没动静，要不要再发一次？**
A: 不要。同一问题重复提交会新建任务、重复消耗积分。报告通常 2-15 分钟出结果（多数 5-10 分钟），之后还要出看板图和报告长图；超过 15 分钟再让我查进度，我会沿用原任务续接，不改 prompt。

**Q: 提示积分不足怎么办？**
A: 打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账（推荐）；或首次购买 9.9 加油包获得 900 积分继续体验：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。

## 参考

- Cue 平台首页：https://cuecue.cn
- API Key 管理：https://cuecue.cn/api-key?src=clawhub-hotspot-tracker
- 付费订阅页面：https://cuecue.cn/pay

出图相关文件：

- `scripts/render.py` —— 报告长图渲染器（Markdown → 长图）
- `scripts/render_dashboard.py` —— 看板图渲染器（SOP JSON → 看板长图）
- `references/sop-schema.md` —— 看板字段说明 + 「报告重排成 SOP JSON」指引
- `assets/intraday-sample.json` —— 盘中 SOP 样例
