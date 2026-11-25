---
slug: cue-sector-etf
name: cue-sector-etf
displayName: 热门赛道与ETF深度投研
Name: 热门赛道与ETF深度投研
description: 用 Cue 一键深度拆解热门赛道与ETF——赛道全景分析、同类ETF横向对比、底层持仓穿透、估值水位研判，告诉你"这条赛道值不值得投、哪只ETF更匹配"。
description_zh: Cue 热门赛道与ETF深度投研：赛道全景+ETF横向对比+持仓穿透+估值研判，选赛道选ETF不再凭感觉。
version: 1.1.5
author: sensedeal
tags: [cue, sector-research, ETF, thematic-investing, 赛道分析, ETF对比, 行业研究, 主题投资, 估值]
---

# 热门赛道与ETF深度投研

> 新能源、AI、半导体、创新药……每个赛道都有十几只 ETF 在追。哪只跟踪得更准？哪只持仓更纯？现在的估值水位贵不贵？让 Cue 帮你把赛道和 ETF 拆开了看，下单之前心里有数。

## 适用范围与场景（先看这个，别用错了）

**可以查：**

| 维度 | 覆盖 |
|------|------|
| 市场 | 全市场 A 股 ETF（股票型、行业/主题型、跨境 ETF）及对应赛道 |
| 赛道类型 | 全行业——新能源/光伏/储能、AI/半导体/算力、医药/创新药、消费/白酒、军工、红利、黄金、跨境等 |
| 分析深度 | 赛道全景、ETF 横向对比、持仓穿透、估值水位、风险扫描 |

**适用场景：**

| 场景 | 解决的问题 |
|------|-----------|
| 赛道选择 | 大家都在说 AI 赛道，它到底包含哪些环节？现在进去贵不贵？ |
| ETF 对比筛选 | 跟踪新能源的 ETF 有十几只，哪只跟踪误差最小、持仓最纯？ |
| 持仓纯度检查 | 买了一只"芯片 ETF"，结果前十大里一半是消费电子——纯度不够 |
| 估值水位研判 | 这个赛道现在的 PE 在历史什么位置？是低估区间还是已经炒高了？ |

**不能查：**

- 具体买卖时点建议（不做择时推荐，只给估值水位参考）
- ETF 实时盘中净值（IOPV）或日内套利策略
- 非上市交易产品（私募基金、场外专户）
- 港/美股 ETF（当前仅覆盖 A 股上市 ETF）

> 简单判断：**这是一条有 A 股 ETF 跟踪的赛道吗？** 是 → 能用。是纯概念、没有 ETF 产品 → 用不了。

### 快速判断：你是否需要这个 Skill？

```
你的需求是？
├─ 我想投一个热门赛道但不知道从哪里下手                    → ✅ 用这个，先看赛道全景
├─ 我已经看好一个赛道，但不知道该选哪只 ETF                 → ✅ 用这个，横向对比
├─ 我持有一只行业 ETF，想看看它底层到底持有什么               → ✅ 用这个，持仓穿透
├─ 我想知道这个赛道现在的估值在历史上是什么水平               → ✅ 用这个，估值水位
├─ 新能源/芯片/医药/白酒/AI，哪个赛道现在性价比最高         → ✅ 用这个，跨赛道对比
├─ 我想知道明天买还是后天买                                 → ❌ 用不了，不做择时
├─ 我想看美股 ETF（如 QQQ/ARKK）的深度分析                  → ❌ 用不了，仅 A 股 ETF
└─ 我想找一只能涨 10 倍的个股                               → ❌ 用不了，去 cue-supply-chain-mining
```

## 试试这样问

**推荐问法（直接对 Agent 说即可触发本 Skill）：**

- "帮我用热门赛道ETF深度投研，分析一下新能源赛道现在值不值得投，哪只 ETF 最好"
- "用 Cue 赛道投研，帮我把市面上跟踪半导体的 ETF 做一个横向对比"
- "帮我研究一下 AI 算力赛道：产业链全景 + 相关 ETF 对比 + 现在的估值水位"
- "我手里有芯片 ETF（159995），帮我穿透持仓看看底层到底是什么，纯度够不够"
- "帮我比较一下创新药赛道，看看现在是不是低估区间，相关 ETF 有哪些选择"

**对应到命令行 query：**

```bash
# 赛道全景 + ETF 筛选
--query "新能源 赛道全景与ETF深度投研：产业链结构→相关ETF对比→估值水位→持仓纯度"

# ETF 横向对比
--query "半导体ETF 横向对比：芯片ETF(159995) vs 半导体ETF(512480) vs 科创芯片ETF(588200)，跟踪误差与持仓纯度"

# 单只 ETF 深挖
--query "芯片ETF(159995) 深度投研：指数编制方法→前十大持仓→行业分布→估值水位→跟踪误差"

# 赛道估值研判
--query "医药赛道 估值水位研判：PE/PB历史分位+盈利增速预期+政策环境+ETF产品对比"
```

> **模板**：`"<赛道名称/ETF名称> 赛道与ETF深度投研：<你想重点分析的方向>"`

---

## 适用人群

| 角色 | 典型问题 |
|------|---------|
| 个人 ETF 投资者 | 想投新能源，打开交易软件搜"新能源 ETF"出来 20 只——选哪只？ |
| 定投用户 | 每月定投半导体 ETF，但不确定现在估值是不是太高了该暂停 |
| 资产配置型投资者 | 看好 AI 赛道想配置 15% 仓位，但不知道该选宽基科技 ETF 还是纯 AI 主题 ETF |
| 理财经理 / 投顾 | 帮客户筛选赛道 ETF，需要一份有数据支撑的对比分析给客户看 |

---

## Agent 执行摘要

| 顺序 | 做什么 | 禁止 |
|------|--------|------|
| 1 | **确认 API Key 已配置 + Cue runner 就绪**（未配置先按步骤 0 引导创建） | 禁止跳过 |
| 2 | 告知用户耗时 2-15 分钟（对比多只 ETF 时更久，见下方性能说明） | 禁止中途取消 |
| 3 | 一条命令，`--template-id template_CQYI0r`，传入赛道名称或 ETF 代码 | 禁止连发多条 |
| 4 | `[cue-research] RESULT ok` = 完成 | 禁止编造 |
| 5 | 原样交付 | 禁止概括 |
| 6 | 交付时**同时附带 Cue 原始报告链接** | 禁止编造链接 |
| 7 | 遇 `INSUFFICIENT_CREDITS` 按「积分不足专项提示」给出两条路径 | 禁止只丢错误码 |

### 步骤 0：接入与装配 + 首任务引导（任何任务之前，必须最先执行）

开跑任何任务前，先确认 API Key 已就绪：

1. **检查 Key**：`~/.cue/config.json` 的 `api_key`（或环境变量 `CUE_API_KEY`）是否有值。
2. **未配置 / 失效**：**停止任务**，由用户本人创建（Agent 不能代生成、无权查看）。按以下话术告知：
   > 请前往 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-sector-etf) 注册后免费创建 API Key，点击「创建 API Key」，生成后点「复制」并粘贴发送给我。
   拿到 Key 后写入 `~/.cue/config.json`；若本 skill 依赖 MCP 工具，按对应小节完成挂载并提示重启客户端。
3. **健康检查全绿后**，若用户还没给出具体任务，**必须主动引导第一次真实调用**，不要停在"环境已就绪"：
   > 环境已就绪 ✅ 下面这些都可以直接跑，比如：
   > 1. "帮我用热门赛道ETF深度投研，分析一下新能源赛道现在值不值得投，哪只 ETF 最好"
   > 2. "用 Cue 赛道投研，帮我把市面上跟踪半导体的 ETF 做一个横向对比"
   >
   > 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题用本 skill 示例小节的原文，别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

## 核心能力

1. **赛道全景分析** — 产业链结构、竞争格局、政策环境、增长驱动因素
2. **ETF 横向对比** — 跟踪指数、规模、费率、跟踪误差、流动性、持仓重合度
3. **持仓纯度检查** — 穿透 ETF 底层，判断持仓是否"纯正"——有没有挂着 AI 名头买了一堆消费电子
4. **估值水位研判** — PE/PB 历史分位、盈利增速预期、国内外同业估值对比
5. **风险扫描** — 政策风险、集中度风险、流动性风险、风格漂移风险

## 输出形式

结构化研报：赛道全景（产业链 + 竞争格局 + 政策）→ 相关 ETF 清单 → 横向对比表（规模/费率/跟踪误差/流动性/持仓纯度）→ 持仓穿透分析 → 估值水位图 → 风险提示 → 来源链接。

## 输出示例

> 示例报告待补充，请通过 [cuecue.cn](https://cuecue.cn) 实际运行后获取。

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
如有疑问请关注“感易Cue”官方服务号添加企微客服咨询
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
  3. `分享到小红书，获得 200 积分`——点击 https://cuecue.cn/activity/xhs?conversation_id={{conv_id}}&skill_name=热门赛道与ETF深度投研（把 `{{conv_id}}` 替换为本次报告的 id，见下）
  4. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

**小红书分享链接怎么拼（第 3 项）**：
- 固定格式：`https://cuecue.cn/activity/xhs?conversation_id=<conv_id>&skill_name=热门赛道与ETF深度投研`
- `conversation_id` = 本次交付报告对应的 Cue 报告 id（交付时 Cue 报告链接 `https://cuecue.cn/share/<conv_id>` 里的同一串 id），必须来自实际输出，禁止编造。
- `skill_name` 固定为 `热门赛道与ETF深度投研`，不得改写。
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

## 性能预期

查询耗时取决于分析维度和 Cue 服务端负载：

| 维度 | 预期耗时 | 说明 |
|------|---------|------|
| 单赛道全景 | 3-8 分钟 | 产业链 + 估值 + ETF 清单 |
| 单 ETF 深度穿透 | 2-5 分钟 | 持仓 + 跟踪误差 + 风格分析 |
| ETF 横向对比（3-5 只） | 5-10 分钟 | 多只 ETF 交叉对比 |
| 跨赛道对比（2-3 个赛道） | 8-15 分钟 | 数据量最大 |
| 财报季（1-4月 / 7-8月） | 5-15 分钟 | 基金季报与半年报集中披露 |

> 如果超过 15 分钟没返回，说明可能超时或队列拥堵——**不要取消重试**，跑一下健康检查的四合一诊断（见下文），确认服务状态后再决定是等还是换时段。中途中断时用**相同命令**续接，Cue 会从 session 断点继续，不重复计费。Session 状态存储在 `~/.cue/session/task`，**不要手动删除**。

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

依赖：`git` + `python3` + `curl`（macOS 自带，Linux `apt install git python3 curl`）。Python 仅用标准库，无额外 pip 依赖。

Cue API Key：[cuecue.cn](https://cuecue.cn/api-key?src=clawhub-sector-etf) 注册后免费创建。新账号送 500 积分，每天再免费送 10 分。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发送给您正在使用的智能体。

> **API Key 只能由用户本人创建**：Agent 既不能代生成、也无权查看用户的 Key。检测到未配置或失效时，按以下话术告知用户：**「点击『创建 API Key』，生成 API Key 后一定要点击『复制』并粘贴发送给我。」** 然后等待用户提供，**禁止声称"我去生成/查看"**。

---

## 调用说明

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "新能源 赛道全景与ETF深度投研：产业链结构→相关ETF对比→估值水位→持仓纯度" \
  --template-id template_CQYI0r \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-sector-etf.md
```

| 参数 | 说明 |
|------|------|
| `--query` | 赛道名称或 ETF 代码，**必填**。可指定分析维度（如估值水位、ETF 对比） |
| `--template-id` | 固定为 `template_CQYI0r` |
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

本 Skill **不在本地执行检索**。流程是 Agent → Cue API（cuecue.cn）→ 外部数据源（ETF 发行商公告、指数公司、基金季报/年报）。分析结果的质量和时效取决于 ETF 公开数据的完整性和 Cue 服务端状态。

| 环节 | 谁控制 | 出问题时 |
|------|--------|---------|
| API Key 鉴权 | 用户本人 | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-sector-etf) 生成后点「复制」并粘贴发送给您正在使用的智能体，再由 Agent 写入 ~/.cue/config.json（Agent 不能代生成，也无权查看） |
| Cue 服务端 | Cue 运维 | 等恢复，或走降级方案 |
| ETF 与指数数据源 | 基金公司/指数公司公开披露 | Cue 用缓存兜底，标注"来源暂不可达" |

---

## 健康检查

跑研究前先验证四件事。一键诊断：

```bash
CUE_KEY=$(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])" 2>/dev/null || echo "$CUE_API_KEY")
echo "=== 1/4 API Key ===" && [ -n "$CUE_KEY" ] && echo "已配置" || echo "未配置！"
echo "=== 2/4 Cue 服务 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/health" -H "Authorization: Bearer $CUE_KEY"
echo "=== 3/4 搭子 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/playbook" -H "Authorization: Bearer $CUE_KEY" | python3 -c "import sys,json;scenes=json.load(sys.stdin).get('data',{}).get('scenes',[]);buddy=[b for s in scenes for b in s.get('buddies',[]) if b.get('title')=='热门赛道/ETF深度投研'];print(f'可用:{len(buddy)}个') if buddy else print('暂不可用')"
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
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-sector-etf) 生成后点「复制」并粘贴发送给您正在使用的智能体（Agent 无法代生成，也无权查看） |
| 服务 | `{"status":"healthy"}` | 等 5 分钟重试 |
| 搭子 | `可用:>0个` | 等 1h 或网页端手动跑 |

> 配置完成后的首次调用引导已并入「步骤 0：接入与装配 + 首任务引导」，按该节执行。

---

## 自救指引

### 错误速查

Cue 返回结构化错误，包含 `code`（错误码）、`retryable`（是否可重试）、`user_action`（操作建议）。

| 错误码 | 现象 | 可重试？ | 处理 |
|--------|------|---------|------|
| `AUTH_FAILED` | 401 / Key 无效 | ❌ | 由用户本人重新生成 Key，更新 `~/.cue/config.json` |
| `TIMEOUT` | 超时 >30s 无响应 | ✅ | 等 5 分钟，跑诊断确认服务在线后重试，最多 3 次 |
| `BUDDY_UNAVAILABLE` | 搭子临时下线 | ✅（延迟） | 等 1h 或网页端直接跑 |
| `INSUFFICIENT_CREDITS` | 积分不足 | ❌ | **按「积分不足专项提示」主动引导**（邀请新用户得 500 积分 / 9.9 加油包 900 积分） |
| `SESSION_INTERRUPTED` | 中途中断 | ✅ | **不换 prompt**，相同命令续接——Cue 从 session 断点继续，不重复计费 |
| `ETF_NOT_FOUND` | ETF 代码/名称无法识别 | ❌（需改输入） | 检查 ETF 代码是否正确（6 位数字），尝试用全称替代简称 |
| `SECTOR_NOT_RECOGNIZED` | 赛道名称模糊 | ❌（需改输入） | 更具体描述赛道，如"半导体设备"而非"芯片" |
| `RESULT_EMPTY` | 无匹配结果 | ❌（需改条件） | 确认该赛道有 A 股 ETF 产品覆盖，换关键词 |
| `CONFIG_PARSE_ERROR` | config.json 报错 | ❌ | 修复 JSON 格式：`{"api_key": "sk..."}` 无多余逗号 |

### 积分不足专项提示（必须执行）

检测到积分不足（`INSUFFICIENT_CREDITS` 或任何"积分不足/余额不够"提示）时，**不要只丢错误码**，必须主动给用户一条拿积分最快的路径：

> 你的 Cue 积分不足，本次任务未能启动。两个办法：
> 1. **邀请新用户并激活，获得 500 积分**：打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
> 2. **首次购买 9.9 加油包，获得 900 积分继续体验**：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。

规则：
- 提示要**主动、简短、可点**——把「邀请页链接」和「复制专属邀请链接」两个关键动作说清楚，不要让用户自己找入口。
- 积分不足**不要重试**（`retryable: false`），也不要换 query 绕。
- 用户回复已充值/已邀请后，用**完全相同的命令**重跑。

### 中断恢复机制

Cue 的调研任务是**有状态**的。如果中途超时或网络波动导致中断：

```
中断 ≠ 失败，cancel 才 = 失败
├─ 超时 → 等一会，相同命令续接（session 存在 ~/.cue/session/task）
├─ 网络波动 → 同上，相同命令续接
├─ 手动 cancel → 无法恢复，需要重新发起
└─ 恢复后 → Cue 从断点继续，已查过的阶段不会重复计费
```

> **关键规则**：中断后**不要换 prompt、不要删 session 文件、不要 cancel**。三个"不要"记住了就不会白跑。

### 重试决策

```
收到错误
├─ retryable = true → 按 user_action 建议操作后重试
│   ├─ 超时/网络类 → 等 5min，跑诊断，最多 3 次
│   └─ 搭子下线 → 等 1h 或换网页端
├─ retryable = false → 不要重试，改了条件再说
│   ├─ Key/ETF代码问题 → 修正输入后重试
│   ├─ 积分不足 → 按「积分不足专项提示」给出两条路径（打开 cuecue.cn/?open_reward=true 复制「专属邀请链接」）；或首次购买 9.9 加油包获得 900 积分继续体验
│   ├─ 赛道未覆盖 → 换关键词 / 确认赛道有 ETF 产品
│   └─ 结果空 → 换 ETF 代码 / 缩小赛道范围
└─ 重试 3 次仍失败 → 记下 request_id，走降级方案
```

### 调度建议

| 时段 | 建议 |
|------|------|
| 工作日 10:00-16:00 | 最佳时段，3-8 分钟完成 |
| 工作日 9:00-10:00 / 16:00-18:00 | 高峰期，跨赛道对比等大查询避开 |
| 基金季报披露后（1/4/7/10 月下旬） | ETF 持仓数据最新鲜，适合做持仓纯度检查 |
| 夜间/周末 | 可能有维护，跑前先诊断 |
| 连续失败 ≥2 次 | 停 15 分钟，记下 request_id 后重试 |

---

## 降级方案

Cue 长时间不可达时的手动替代渠道：

| 渠道 | 覆盖 | 费用 |
|------|------|------|
| [天天基金](https://fund.eastmoney.com) | ETF 持仓 + 跟踪误差 + 规模 | 免费 |
| [东方财富](https://www.eastmoney.com) | 行业板块估值 + ETF 列表 | 免费 |
| [中证指数公司](https://www.csindex.com.cn) | 指数编制方法 + 成分股 | 免费 |
| [理杏仁](https://www.lixinger.com) | 行业/指数历史 PE/PB 分位 | 部分免费 |

---

## FAQ

**Q: ETF 分析和赛道分析的区别是什么？**
A: 赛道分析是"面"——这个行业的结构、景气度、估值水位、政策环境。ETF 分析是"点"——跟踪这条赛道的具体产品，谁的跟踪误差最小、谁的持仓最纯、谁的流动性最好。本搭子两个都做：先看赛道值不值得投，再看哪只 ETF 最合适。

**Q: 怎么知道该用这个还是 cue-supply-chain-mining？**
A: 本搭子焦点是 ETF 产品对比和赛道估值，解决"选哪只 ETF、现在贵不贵"。cue-supply-chain-mining 焦点是产业链里找个股，解决"这条链上哪家公司最有弹性"。如果你最终想买个股，先跑本搭子看赛道方向 → 再跑 supply-chain-mining 找标的。

**Q: 能分析港美股 ETF 吗？**
A: 当前仅覆盖 A 股上市 ETF（含跨境 ETF，如纳指 ETF、恒生 ETF 等在 A 股上市的品种）。港/美股本地 ETF（如 QQQ、ARKK）不在覆盖范围。

**Q: 持仓纯度是什么意思？**
A: 比如一只叫"AI 人工智能 ETF"的产品，前十大重仓里却有海康威视（安防）、立讯精密（消费电子代工）这些跟 AI 核心环节关联没那么直接的公司——这就是纯度不够。Cue 会穿透持仓，告诉你在"AI"这个主题上的实际暴露程度。

**Q: 估值水位怎么看？**
A: PE/PB 在当前时间点在历史（过去 3-5 年）中所处的百分位。比如 PE 处于历史 85% 分位，说明比过去 85% 的时间都贵，属于偏高区间；处于 15% 分位则相反。不是买卖信号，是风险提示——"现在入场，安全边际是多少"。

**Q: ETF 对比只比跟踪误差吗？**
A: 不止。Cue 会从跟踪指数、规模、管理费率、日均成交额、跟踪误差、持仓重合度、前十大集中度、成立时间等多个维度做对比，给出综合评价。

**Q: 分析完了我该怎么做？**
A: 本搭子帮你做赛道和 ETF 的选择决策。定了之后，可以用 cue-asset-allocation 确认这条赛道在你的整体配置里占多少比例合适，用 cue-deep-research 对 ETF 里的核心持仓股做深度尽调。

**Q: 报告能在网页端看原文吗？**
A: 可以。交付时会同时附上 Cue 原始报告链接 `https://cuecue.cn/share/<conv_id>`，点开即可回到网页端查看完整原文、继续追问或转发同事。

**Q: 提示积分不足怎么办？**
A: 打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账（推荐）；或首次购买 9.9 加油包获得 900 积分继续体验：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。
