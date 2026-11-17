---
slug: cue-pre-market-strategy
name: cue-pre-market-strategy
Name: 今日盘前机会
description: 每天开盘前 3 分钟，看懂今天 A 股的机会与风险——自动扫隔夜美股、政策、产业新闻，大白话讲清利好利空，排出今日最值得关注的方向清单。
description_zh: Cue 今日盘前机会：每天开盘前 3 分钟，扫隔夜大事，看懂今天 A 股机会与风险。
version: 1.2.4
author: sensedeal
tags: [cue, pre-market, trading-strategy, 今日盘前机会, 盘前机会, 盘前热点, 盘前掘金, 开盘前必看]
---

# 今日盘前机会

> 每天开盘前，花几分钟看懂隔夜发生了什么、今天 A 股哪些方向有机会、哪些要避开。不用熬夜盯盘，个人投资者也能轻松上手的盘前功课。

## Agent 执行摘要

| 顺序 | 做什么 | 禁止 |
|------|--------|------|
| 1 | **确认 API Key 已配置 + Cue runner 就绪**（未配置先按步骤 0 引导创建） | 禁止跳过 |
| 2 | 告知用户耗时 2-15 分钟 | 禁止中途取消 |
| 3 | 一条命令，`--template-id template_qsweF9` | 禁止连发多条 |
| 4 | `[cue-research] RESULT ok` = 完成 | 禁止编造 |
| 5 | 原样交付报告 | 禁止概括 |
| 6 | 交付时**同时附带 Cue 原始报告链接** | 禁止编造链接 |
| 7 | 遇 `INSUFFICIENT_CREDITS` 按「积分不足专项提示」给出两条路径 | 禁止只丢错误码 |
| 8 | 交付后**用选项弹框**问是否设置定时任务 | 禁止只发文字提醒 / 禁止擅自开启 |

### 步骤 0：接入与装配 + 首任务引导（任何任务之前，必须最先执行）

开跑任何任务前，先确认 API Key 已就绪：

1. **检查 Key**：`~/.cue/config.json` 的 `api_key`（或环境变量 `CUE_API_KEY`）是否有值。
2. **未配置 / 失效**：**停止任务**，由用户本人创建（Agent 不能代生成、无权查看）。按以下话术告知：
   > 请前往 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-pre-market-strategy) 注册后免费创建 API Key，点击「创建 API Key」，生成后点「复制」并粘贴发送给我。
   拿到 Key 后写入 `~/.cue/config.json`；若本 skill 依赖 MCP 工具，按对应小节完成挂载并提示重启客户端。
3. **健康检查全绿后**，若用户还没给出具体任务，**必须主动引导第一次真实调用**，不要停在"环境已就绪"：
   > 环境已就绪 ✅ 下面这些都可以直接跑，比如：
   > 1. "今天盘前有什么值得关注的？"
   > 2. "隔夜美股对今天 A 股有什么影响？"
   >
   > 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题用本 skill 示例小节的原文，别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

## 适用场景

| 场景 | 帮到你什么 |
|------|-----------|
| 每天开盘前 | 几分钟看懂隔夜发生了什么，不用自己熬夜盯美股 |
| 今天关注什么方向 | 直接给你一份「今日机会清单」，哪些板块最可能有行情 |
| 提前避坑 | 隔夜利空会砸到哪些板块，提前知道，避免开盘踩雷 |
| 上班族 | 通勤路上几分钟看完，心中有数再决定今天动不动手 |

## 核心能力

1. **隔夜大事扫描** — 美股、大宗商品、政策、产业新闻，一网打尽
2. **翻译成大白话** — 每件事告诉你「对 A 股意味着什么、利好谁、利空谁」
3. **产业链顺藤摸瓜** — 上游一个消息，帮你推到中下游哪些公司受影响
4. **今日机会排序** — 按「确定性 × 爆发力」排出今天最值得看的方向

## 试试这样问

- "今天盘前有什么值得关注的？"
- "隔夜美股对今天 A 股有什么影响？"
- "今天哪些板块最可能有行情？"
- "开盘前我要避开哪些雷？"
- "帮我看看今天的盘前机会"

## 输出形式

一份「今日盘前机会清单」：隔夜大事 → 对 A 股意味着什么 → 利好/利空哪些板块 → 今日机会排序 → 风险提示 → 来源链接。

## 输出示例

[查看完整报告](https://cuecue.cn/share/jwhaQSVxNzzWYOvHmt-jO)

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
- 报告交付完**必须紧接着弹出定时任务选项**（见「定时任务（交付后必做）」一节），但**只有用户明确选择时间后才配置**。

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
  3. `分享到小红书，获得 200 积分`——点击 https://cuecue.cn/activity/xhs?conversation_id={{conv_id}}&skill_name=今日盘前机会（把 `{{conv_id}}` 替换为本次报告的 id，见下）
  4. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

**小红书分享链接怎么拼（第 3 项）**：
- 固定格式：`https://cuecue.cn/activity/xhs?conversation_id=<conv_id>&skill_name=今日盘前机会`
- `conversation_id` = 本次交付报告对应的 Cue 报告 id（交付时 Cue 报告链接 `https://cuecue.cn/share/<conv_id>` 里的同一串 id），必须来自实际输出，禁止编造。
- `skill_name` 固定为 `今日盘前机会`，不得改写。
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

## 环境要求

**三步装好（一次性，约 1 分钟）：**

```bash
# 1. 克隆 runner 到 ~/.cue/cue-skills
if [ -d ~/.cue/cue-skills/.git ]; then
  git -C ~/.cue/cue-skills pull --ff-only
else
  git clone https://github.com/sensedeal/cue-skills ~/.cue/cue-skills \
    || git clone https://gitee.com/sensedeal/cue-skills ~/.cue/cue-skills
fi
#   国内网络慢可换 Gitee 镜像：
#   git clone https://gitee.com/sensedeal/cue-skills ~/.cue/cue-skills

# 2. 写入 API Key（在 https://cuecue.cn/api-key?src=clawhub-pre-market-strategy 创建后复制）
mkdir -p ~/.cue && echo '{"api_key":"sk..."}' > ~/.cue/config.json

# 3. 验证连通（返回 200 即成功）
curl -sS --max-time 10 "https://cuecue.cn/api/templates" \
  -H "Authorization: Bearer $(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])")"
```

依赖：`git` + `python3` + `curl`（macOS 自带，Linux `apt install git python3 curl`）。Python 仅用标准库，无额外 pip 依赖。

Runner 来源：[GitHub - sensedeal/cue-skills](https://github.com/sensedeal/cue-skills)（[Gitee 镜像](https://gitee.com/sensedeal/cue-skills)）。

Cue API Key：[cuecue.cn](https://cuecue.cn/api-key?src=clawhub-pre-market-strategy) 注册后免费创建。新账号送 500 积分，每天再免费送 10 分。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发送给您正在使用的智能体。

- **积分赠送**：新注用户赠送 500 积分；每邀请 1 位新用户注册再送 500 积分——打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
- **积分不足**：按「积分不足专项提示」给出两条路径（邀请新用户得 500 积分 / 9.9 加油包 900 积分）。

> **API Key 只能由用户本人创建**：Agent 既不能代生成、也无权查看用户的 Key。检测到未配置或失效时，按以下话术告知用户：**「点击『创建 API Key』，生成 API Key 后一定要点击『复制』并粘贴发送给我。」** 然后等待用户提供，**禁止声称"我去生成/查看"**。

---

## 调用说明

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "今日盘前策略：隔夜全球事件→A股映射→产业链传导→爆发力主题" \
  --template-id template_qsweF9 \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-pre-market.md
```

| 参数 | 说明 |
|------|------|
| `--query` | 可加行业偏好或风险关注点 |
| `--template-id` | 固定为 `template_qsweF9` |
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

## 定时任务（交付后必做）

盘前报告的价值在「每天开盘前都有」。**交付报告后，不要只发一句"建议你定时跑"的文字提醒，必须直接弹出选项让用户点选。**

### 弹框内容（必须三选一）

优先用运行环境自带的选项弹框能力（如 Claude Code 的 `AskUserQuestion`）。环境不支持弹框时，把同样的三个选项以编号形式写在正文末尾，等用户回复编号。

> **要不要把这份盘前机会设成定时任务，每个交易日早上自动生成？**
>
> 1. **每个交易日 08:00（推荐）** — 周一至周五每天 08:00 自动跑，开盘前拿到今日机会清单
> 2. **自定义时间** — 自己指定几点、哪几天
> 3. **暂不设置** — 这次先只看报告，以后需要随时说

选择 `2` 时再追问一句：**几点跑？周一到周五，还是也要周末？**（默认周一到周五；建议 07:30–08:30，隔夜信息已沉淀且距开盘还有决策时间）。用户回答后再确认一次具体时间，例如「每周一至周五 08:00，确认吗？」

### 铁律

- **禁止擅自开启**：用户没选时间之前，不得创建任何定时任务、cron、launchd。
- **禁止只发文字**：文字提醒不算完成，必须给出可点选的选项。
- **禁止重复打扰**：用户本次已选过（配置成功或明确选"暂不设置"）就不要再问。
- **每次只问一次**：交付后问一次即可，不要追问"真的不要吗"。

### 用户选定后怎么配

统一用同一套命令跑（与手工调用完全一致）：

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "今日盘前策略：隔夜全球事件→A股映射→产业链传导→爆发力主题" \
  --template-id template_qsweF9 \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-pre-market.md
```

按运行环境选一种落地方式：

| 环境 | 配置方式 |
|------|---------|
| Claude Code | 用 `CronCreate`，cron 表达式 `0 8 * * 1-5`（自定义时间按用户所选取 分 时 日 月 周） |
| macOS | 建 `~/Library/LaunchAgents/com.cue.pre-market.plist`，`StartCalendarInterval` 设 `Weekday` 1–5、`Hour` 8、`Minute` 0，再 `launchctl load` |
| Linux | `crontab -e` 追加 `0 8 * * 1-5 <上面的命令>` |

配完必须回报三件事：**触发时间、输出目录、如何关掉**（Claude Code 删任务 / `launchctl unload` / `crontab -e` 删除对应行）。

### 必须提前告知的两个坑

- **每次运行都会消耗 Cue 积分**，余额不足时当天会失败，需按「积分不足专项提示」补充积分，不会自动跳过。
- **不会自动推送**：报告只落在 `~/cue-reports/`，需要自己打开看；想要消息推送要另外接通知渠道。

---

## 架构说明

本 Skill **不在本地执行检索**。流程是 Agent → Cue API（cuecue.cn）→ 外部数据源。解析结果的质量和时效取决于 Cue 服务端和外部数据源的状态。

| 环节 | 谁控制 | 出问题时 |
|------|--------|---------|
| API Key 鉴权 | 用户本人 | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-pre-market-strategy) 生成后点「复制」并粘贴发送给您正在使用的智能体，再由 Agent 写入 ~/.cue/config.json（Agent 不能代生成，也无权查看） |
| Cue 服务端 | Cue 运维 | 等恢复，或走降级方案 |
| 外部数据源 | 公开网站 | Cue 用缓存兜底，标注"来源暂不可达" |

**能力边界（先说清楚，别期望过高）：**

- 结果是**基于公开信息的推断**，不构成投资建议，也不保证涨跌。
- 报告质量与时效**取决于 Cue 服务端和外部数据源当天状态**——数据源波动时可能延迟或标注"来源暂不可达"。
- 不提供实时行情、资金流、买卖点；这些去券商 App。

---

## 健康检查

跑研究前先验证四件事。一键诊断：

```bash
CUE_KEY=$(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])" 2>/dev/null || echo "$CUE_API_KEY")
echo "=== 1/4 API Key ===" && [ -n "$CUE_KEY" ] && echo "已配置" || echo "未配置！"
echo "=== 2/4 Cue 服务 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/health" -H "Authorization: Bearer $CUE_KEY"
echo "=== 3/4 搭子 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/playbook" -H "Authorization: Bearer $CUE_KEY" | python3 -c "import sys,json;scenes=json.load(sys.stdin).get('data',{}).get('scenes',[]);buddy=[b for s in scenes if s.get('secondary_category')=='短线盘面' for b in s.get('buddies',[]) if b.get('title')=='深度盘前策略内参'];print(f'可用:{len(buddy)}个') if buddy else print('暂不可用')"
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
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-pre-market-strategy) 生成后点「复制」并粘贴发送给您正在使用的智能体（Agent 无法代生成，也无权查看） |
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

### 输入不对时会怎样、怎么改

| 你的输入 | 结果 | 正确做法 |
|---------|------|---------|
| 空 query，或没写清时间/主题 | 结果空或跑偏 | 明确"今天/近几天的盘前"，说清关注方向 |
| 问实时行情、买卖点、K 线 | 无法回答 | 这类去券商 App；本工具只做隔夜事件→A股影响的推断 |
| 隔夜无大事，硬要"今天机会" | `RESULT empty` | 正常，说明当天无强信号，别硬凑 |
| 只写一个行业（如"半导体"） | 结果过窄 | 可直接用，也可加"及相关产业链"扩大覆盖面 |

### 决策树

```
出问题？
├─ Key 报错 → 由用户本人重新生成 → 更新 config.json → 重试
├─ 连不上 → curl /api/health 确认 → 检查 DNS/代理
├─ 搭子找不到 → curl /api/playbook → 等或用网页端
├─ 中途中断 → 相同 prompt 续接（不要删 ~/.cue/session/task）
└─ 结果空 → 缩窄关键词 → 确认该主题有公开数据
```

### 中断恢复与重试模型

> `research_run.py` 采用 fire-and-retrieve + replay 兜底：后台跑完自动取报告，取不到会自动回放 DB 拿完整报告（**不重复扣费**）。但**网络/鉴权类失败不会自动重试**——按上方决策树手动重试（最多 3 次）。
> 想要自动重试，可在外层包循环：
> ```bash
> for i in 1 2 3; do
>   python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
>     --query "今日盘前策略：隔夜全球事件→A股映射→产业链传导→爆发力主题" \
>     --template-id template_qsweF9 && break
>   sleep 300
> done
> ```

中断 ≠ 失败：中途超时/断网，用**相同命令**续接（Cue 从断点继续，不重复计费）；只有手动 cancel 才无法恢复。

### 调度建议

| 时段 | 建议 |
|------|------|
| 工作日 9-18 | 正常使用 |
| 夜间/周末 | 可能有维护，跑前先诊断 |
| 新 Key | 必须先诊断确认生效 |
| 连续失败 | 停 15 分钟再试，不要反复重试 |

---

## 降级方案

Cue 长时间不可达时的手动替代渠道：

| 渠道 | 覆盖 | 费用 |
|------|------|------|
| [东方财富](https://www.eastmoney.com) | A股盘前资讯 | 免费 |
| [财联社](https://www.cls.cn) | 隔夜要闻 | 免费 |
| [华尔街见闻](https://wallstreetcn.com) | 全球市场动态 | 免费 |
| [新浪财经](https://finance.sina.com.cn) | 盘前公告汇总 | 免费 |

---

## FAQ

**Q: 和投顾早盘简报、24h热点追踪有什么区别？**
A: 早盘简报是理财师发给客户的素材；热点追踪讲「发生了什么」；今日盘前机会更进一步，讲「对 A 股意味着什么、今天该关注哪些板块」，并给出机会排序。深度依次递增，这个最接近「今天该怎么看盘」。

**Q: 最佳跑的时间？**
A: 建议 8:00-8:30 跑，隔夜信息已充分沉淀，距开盘（9:30）还有充足决策时间。上班族通勤路上就能跑完。交付报告后 Agent 会直接问你要不要设成定时任务，选「每个交易日 08:00」即可每天自动生成。

**Q: 报告能在网页端看原文吗？**
A: 可以。交付时会同时附上 Cue 原始报告链接 `https://cuecue.cn/share/<conv_id>`，点开即可回到网页端查看完整原文、继续追问或转发同事。

**Q: 提示积分不足怎么办？**
A: 打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账（推荐）；或首次购买 9.9 加油包获得 900 积分继续体验：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。
