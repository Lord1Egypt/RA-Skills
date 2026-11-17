---
name: cue-technical-analysis
description: 用 Cue 对个股做短线走势与技术面分析——从量价关系、资金流向、趋势结构入手，计算波动率与最大回撤，产出可复核的走势分析底稿，辅助判断短线的买卖节奏和关键价位。
description_zh: Cue 短线走势与技术面分析：穿透量价关系/资金流向/趋势结构/支撑压力位，产出可复核的走势底稿。
version: 1.2.4
author: sensedeal
tags: [cue, technical-analysis, short-term-trading, quantity-price, 短线分析, 技术分析, 量价分析, 资金流向, 支撑压力位]
---

# 短线走势与技术面分析

> 围绕个股的历史行情、量价与强弱趋势，计算波动率、最大回撤与趋势结构，产出可复核的走势分析底稿，帮你看清短线的买卖节奏和支撑压力位。

## Agent 执行摘要

| 顺序 | 做什么 | 禁止 |
|------|--------|------|
| 1 | **确认 API Key 已配置 + Cue runner 就绪**（未配置先按步骤 0 引导创建） | 禁止跳过 |
| 2 | 告知用户耗时 2-15 分钟 | 禁止中途取消 |
| 3 | 一条命令，`--template-id template_L1YwFU`，传入目标股票 | 禁止连发多条 |
| 4 | `[cue-research] RESULT ok` = 完成 | 禁止编造 |
| 5 | 原样交付，来源链接不丢失 | 禁止概括/改数字 |
| 6 | 交付时**同时附带 Cue 原始报告链接** | 禁止编造链接 |
| 7 | 遇 `INSUFFICIENT_CREDITS` 按「积分不足专项提示」给出两条路径 | 禁止只丢错误码 |
| 8 | 交付后**用选项弹框**问是否设置定时：每个交易日 16:30（推荐，落在 16:00–17:00 收盘后窗口）/ 自定义时间 / 暂不设置 | 禁止只发文字提醒；禁止未经用户选择擅自开启；禁止错绑标的 |

### 步骤 0：接入与装配 + 首任务引导（任何任务之前，必须最先执行）

开跑任何任务前，先确认 API Key 已就绪：

1. **检查 Key**：`~/.cue/config.json` 的 `api_key`（或环境变量 `CUE_API_KEY`）是否有值。
2. **未配置 / 失效**：**停止任务**，由用户本人创建（Agent 不能代生成、无权查看）。按以下话术告知：
   > 请前往 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-technical-analysis) 注册后免费创建 API Key，点击「创建 API Key」，生成后点「复制」并粘贴发送给我。
   拿到 Key 后写入 `~/.cue/config.json`；若本 skill 依赖 MCP 工具，按对应小节完成挂载并提示重启客户端。
3. **健康检查全绿后**，若用户还没给出具体任务，**必须主动引导第一次真实调用**，不要停在"环境已就绪"：
   > 环境已就绪 ✅ 下面这些都可以直接跑，比如：
   > 1. "帮我分析一下宁德时代短线的量价走势"
   > 2. "比亚迪现在短线能买吗，支撑位在哪？"
   >
   > 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题用本 skill 示例小节的原文，别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

## 适用场景

| 场景 | 解决的问题 |
|------|-----------|
| 短线交易决策 | 判断个股短期的买卖节奏和关键价位 |
| 量价关系分析 | 识别放量突破、缩量回调、量价背离等信号 |
| 技术面复盘 | 复盘个股近期走势的技术结构 |
| 支撑压力判断 | 找出关键支撑位和压力位 |

## 核心能力

1. **量价关系分析** — 成交量与价格走势的配合/背离，识别放量突破、缩量回调
2. **资金流向** — 主力资金进出、筹码分布，判断资金态度
3. **趋势结构** — 均线、趋势线、技术形态，判断当前强弱与趋势方向
4. **波动率与回撤** — 波动率、最大回撤等风险度量，评估短线波动
5. **支撑压力位** — 关键支撑位、压力位，作为买卖参考

## 试试这样问

- "帮我分析一下宁德时代短线的量价走势"
- "比亚迪现在短线能买吗，支撑位在哪？"
- "茅台最近的量价关系怎么样？"
- "这只股票放量了，是突破还是出货？"

## 输出形式

结构化技术面底稿：行情概览 → 量价关系 → 资金流向 → 趋势结构 → 波动率与回撤 → 支撑压力位 → 风险提示 → 来源链接。

## 输出示例

[查看完整报告](https://cuecue.cn/share/buddy-test-81a83d14ba86)

> 上例中的 token 是示例，**不可复制到实际交付中**。

## 交付规范（必须执行）

把最终报告发送给用户时，**必须同时附带 Cue 原始报告链接**，方便用户回到网页端查看完整原文、继续追问或转发同事。

**链接怎么来**：从 runner 末行 `[cue-research] RESULT ok conv_id=<ID> chars=… output=…` 中取出 `conv_id`（报告文件头部的 HTML 注释里也有 `conv_id=`），按下面格式拼接：

```
https://cuecue.cn/share/<conv_id>
```

交付模板（照此结构输出）：

```
报告已完成 ✅

<报告正文……>

---
**Cue 原始报告**：https://cuecue.cn/share/<conv_id>
**本地副本**：~/cue-reports/<文件名>.md
```

规则：
- `conv_id` 必须取自实际输出，**禁止编造**或使用文档示例里的 id。
- 末行为 `RESULT empty`（无 conv_id 或报告为空）时**不要拼链接**，如实告知未取到报告并给后续建议。
- 用户明确说不要链接时可不附。

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
  3. `分享到小红书，获得 200 积分`——点击 https://cuecue.cn/activity/xhs?conversation_id={{conv_id}}&skill_name=个股短线走势与技术面分析（把 `{{conv_id}}` 替换为本次报告的 id，见下）
  4. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

**小红书分享链接怎么拼（第 3 项）**：
- 固定格式：`https://cuecue.cn/activity/xhs?conversation_id=<conv_id>&skill_name=个股短线走势与技术面分析`
- `conversation_id` = 本次交付报告对应的 Cue 报告 id（交付时 Cue 报告链接 `https://cuecue.cn/share/<conv_id>` 里的同一串 id），必须来自实际输出，禁止编造。
- `skill_name` 固定为 `个股短线走势与技术面分析`，不得改写。
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

## 定时任务（交付后必做：弹框询问）

技术面分析是**个股**维度，适合每个交易日收盘后固定跑一次，次日开盘前直接看结论。**交付报告后，不要只发一句"建议定时跑"的文字提醒，必须直接弹出选项让用户点选。**

### 弹框内容（必须三选一）

优先用运行环境自带的选项弹框能力（如 Claude Code 的 `AskUserQuestion`）。环境不支持弹框时，把同样的三个选项以编号形式写在正文末尾，等用户回复编号。

> **要不要把这只股票的短线分析设成定时任务，每个交易日收盘后自动生成？**
>
> 1. **每个交易日 16:30（推荐）** — 15:00 收盘后日线、量价与资金数据已落地，处于 16:00–17:00 推荐窗口，晚上就能看
> 2. **自定义时间** — 自己指定几点、每周哪几天（建议仍落在 16:00–17:00）
> 3. **暂不设置** — 这次先看报告，以后需要随时说

选「自定义时间」时，必须追问**几点跑、每周哪几天**；并提醒用户：**早于 16:00 跑，当天日线与资金数据可能还没补齐**，建议仍在 16:00–17:00 之间。

### 定时的是哪只股票（必须确认）

本 skill 一次只分析一只股票，定时任务必须绑定明确标的：

- 默认按**本次刚分析的股票**建任务；
- 用户要定时看多只时，逐只确认标的，每只单独一条任务；**每只每次运行都消耗一份 Cue 积分**，建任务前先把标的总数和预计积分说清楚。

### 铁律

- **禁止擅自开启**：用户没有明确选择时间之前，不得创建任何定时任务、cron、launchd。
- **禁止只发文字**：文字提醒不算完成，必须给出可点选的选项。
- **禁止错绑标的**：用户没确认标的时不得建任务，禁止拿示例股票或上一只股票顶替。
- **每次交付问一次**：用户配置成功或明确选「暂不设置」后，后续交付不再重复打扰。
- **禁止谎称已设**：当前客户端不支持定时任务时，给出时点清单让用户自行设提醒，并说明未配置。

### 用户选定后怎么配

统一用同一套命令跑（把 `<目标股票>` 换成用户确认的标的）：

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "<目标股票> 短线量价与技术面分析：量价关系 + 资金流向 + 趋势结构 + 支撑压力位" \
  --template-id template_L1YwFU \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-technical-analysis.md
```

按运行环境选一种落地方式：

| 环境 | 配置方式 |
|------|---------|
| Claude Code | 用 `CronCreate`，cron 表达式 `30 16 * * 1-5`（自定义时间按用户所选取 分 时 日 月 周） |
| macOS | 建 `~/Library/LaunchAgents/com.cue.technical-analysis.plist`，`StartCalendarInterval` 设 `Weekday` 1–5、`Hour` 16、`Minute` 30，再 `launchctl load` |
| Linux | `crontab -e` 追加 `30 16 * * 1-5 <上面的命令>` |

配完必须回报三件事：**触发时间、绑定标的、如何关掉**（Claude Code 删任务 / `launchctl unload` / `crontab -e` 删除对应行）。

### 必须提前告知的两个坑

- **每次运行都会消耗 Cue 积分**，盯多只股票按任务数叠加，余额不足时当天会失败，需按「积分不足专项提示」补充积分，不会自动跳过。
- **定时任务不会自动推送**：报告只落盘 `~/cue-reports/*.md`，需要自己打开看；看板可在次日交互时基于已落盘的 `.md` 补生成（纯本地操作，不消耗积分）。

---

## 环境要求

**首次使用运行 skill 自带的一键安装脚本**（检查依赖 → 克隆 runner → 验证 Key → 测试连通性）：

```bash
```

依赖：`git` + `python3` + `curl`。Python 仅用标准库，无额外 pip 依赖。

Cue API Key：[cuecue.cn](https://cuecue.cn/api-key?src=clawhub-technical-analysis) 注册后免费创建。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发送给您正在使用的智能体。

- **积分赠送**：新注用户赠送 500 积分；每邀请 1 位新用户注册再送 500 积分——打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
- **积分不足**：按「积分不足专项提示」给出两条路径（邀请新用户得 500 积分 / 9.9 加油包 900 积分）。

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

> **API Key 只能由用户本人创建**：Agent 既不能代生成、也无权查看用户的 Key。检测到未配置或失效时，按以下话术告知用户：**「点击『创建 API Key』，生成 API Key 后一定要点击『复制』并粘贴发送给我。」** 然后等待用户提供，**禁止声称"我去生成/查看"**。

---

## 调用说明

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "目标股票 短线量价与技术面分析：量价关系 + 资金流向 + 趋势结构 + 支撑压力位" \
  --template-id template_L1YwFU \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-technical-analysis.md
```

| 参数 | 说明 |
|------|------|
| `--query` | 目标股票 + 关注角度，**必填** |
| `--template-id` | 固定为 `template_L1YwFU` |
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
| API Key 鉴权 | 用户本人 | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-technical-analysis) 生成后点「复制」并粘贴发送给您正在使用的智能体，再由 Agent 写入 ~/.cue/config.json（Agent 不能代生成，也无权查看） |
| Cue 服务端 | Cue 运维 | 等恢复，或走降级方案 |
| 外部数据源 | 公开网站 | Cue 用缓存兜底，标注"来源暂不可达" |

---

## 健康检查

跑研究前先验证四件事。一键诊断：

```bash
CUE_KEY=$(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])" 2>/dev/null || echo "$CUE_API_KEY")
echo "=== 1/4 API Key ===" && [ -n "$CUE_KEY" ] && echo "已配置" || echo "未配置！"
echo "=== 2/4 Cue 服务 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/health" -H "Authorization: Bearer $CUE_KEY"
echo "=== 3/4 搭子 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/playbook" -H "Authorization: Bearer $CUE_KEY" | python3 -c "import sys,json;scenes=json.load(sys.stdin).get('data',{}).get('scenes',[]);buddy=[b for s in scenes if s.get('secondary_category')=='短线盘面' for b in s.get('buddies',[]) if b.get('title')=='短线资金量价与技术面分析'];print(f'可用:{len(buddy)}个') if buddy else print('暂不可用')"
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
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-technical-analysis) 生成后点「复制」并粘贴发送给您正在使用的智能体（Agent 无法代生成，也无权查看） |
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
| 交易日盘中/盘后 | 正常使用（数据最新鲜） |
| 夜间/周末 | 可能有维护，跑前先诊断 |
| 新 Key | 必须先诊断确认生效 |
| 连续失败 | 停 15 分钟再试，不要反复重试 |

---

## 降级方案

Cue 长时间不可达时的手动替代渠道：

| 渠道 | 覆盖 | 费用 |
|------|------|------|
| [同花顺](https://www.10jqka.com.cn) | 个股行情、技术指标、资金流向 | 免费 |
| [东方财富](https://www.eastmoney.com) | 行情数据、资金流向、技术指标 | 免费 |
| [雪球](https://xueqiu.com) | 个股讨论、资金面观点 | 免费 |
| [TradingView](https://www.tradingview.com) | 图表、技术分析工具 | 免费版 |

---

## FAQ

**Q: 能给出具体买卖点吗？**
A: 报告给出支撑压力位、量价信号和趋势判断，不喊具体买卖指令，决策在你。

**Q: 适合什么周期的短线？**
A: 以日线为主，可在 query 中指定时间窗口（如"近 20 个交易日"）调整。

**Q: 和技术指标类工具（如 MACD/KDJ）有什么区别？**
A: 这个搭子不止看单一指标，而是把量价、资金、趋势、波动回撤放在一起交叉看，输出一份可复核的底稿，而非单个指标信号。

**Q: 报告能在网页端看原文吗？**
A: 可以。交付时会同时附上 Cue 原始报告链接 `https://cuecue.cn/share/<conv_id>`，点开即可回到网页端查看完整原文、继续追问或转发同事。

**Q: 提示积分不足怎么办？**
A: 打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账（推荐）；或首次购买 9.9 加油包获得 900 积分继续体验：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。

## 参考

- Cue 平台首页：https://cuecue.cn
- API Key 管理：https://cuecue.cn/api-key?src=clawhub-technical-analysis
- 付费订阅页面：https://cuecue.cn/pay
