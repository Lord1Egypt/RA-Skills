---
name: cue-deep-research
displayName: Cue 深度研究（通用版）
description: Cue 深度调研通用版——通过 Cue 服务端调用公开数据源完成多维度交叉验证研究。覆盖A股/港股/美股/工商/司法/监管/研报/资金流/招投标等公开数据，每条结论带原链接可回查。仅限公开信息检索，不处理个人数据或非公开信息。支持仿写（mimic），让报告模仿指定文档的写作风格。触发词：深度研究、调研分析、竞品对标、行业趋势、基本面分析
description_zh: Cue 深度研究通用版：470+数据工具、多源交叉验证、100%溯源、支持仿写。覆盖A股/港股/美股/工商/司法/监管/研报/资金流/招投标等公开数据源，仅限公开信息检索。
version: 1.1.4
author: sensedeal
tags: [cue, deep-research, general-purpose, cross-validation, traceability, mimic, 深度研究, 溯源, 仿写, 交叉验证, 通用]
---

# Cue 深度研究（通用版）

> 覆盖 A 股/港股/美股/工商/司法/监管/研报/资金流/招投标等公开数据源。470+ 专业数据工具、多源交叉验证、100% 溯源——每条结论带原链接，不杜撰、可回查。支持仿写，让报告模仿你指定的写作风格。

## 为什么选 Cue 而不是通用 chatbot？

| 你的痛点 | Cue 怎么解决 |
|----------|-------------|
| Chatbot 编造数据、无法溯源 | **100% 溯源**：每条结论附公开来源链接，可回查验证 |
| 单一信源不可靠 | **多源交叉验证**：同一结论从多个独立数据源交叉印证 |
| 手动翻 10 个网站太慢 | **470 个专业 MCP 工具**、20 家数据提供方、56 个工具族，自动调度取证 |
| 通用搜索不会做金融分析 | **58 个工具类别**：主体信息(63)、财务指标(46)、基金(24)、盘面结构(24)、实时行情(23)、宏观经济(22)… |
| 写报告风格不统一 | **仿写（mimic）**：给一篇参考文档，报告按你的风格输出 |

## 数据源全景

**570 个专业 MCP 工具，58 个类别，20 家数据提供方。市场覆盖：**

| 市场 | 工具数 | 典型数据 |
|------|--------|---------|
| A 股 | 213 | 财报/研报/公告/资金流/龙虎榜/股权激励/增减持/质押/大宗交易 |
| 中国大陆（非上市） | 155 | 工商登记/司法涉诉/行政处罚/招投标/动产抵押/高管履历 |
| 全球 | 32 | LEI 主体信息/境外制裁合规(OFAC/MAS/EU)/学术文献 |
| 美股 | 25 | SEC 披露/13F 机构持仓/美股财务/CCASS |
| 港股 | 20 | 港交所披露/CCASS 持股/港股公告 |

**核心类别 TOP 20（按工具数量）：**

| 类别 | 工具数 | 能做什么 |
|------|--------|---------|
| 主体信息（LEI/政采） | 63 | 企业工商登记、统一社会信用代码、招投标中标记录 |
| 股票财务/业绩/指标 | 46 | 三表数据、一致预期、盈利预测明细、经营指标、账龄 |
| 基金 | 24 | 基金净值、持仓、换手率、基金经理、基金风格 |
| 盘面结构 | 24 | 涨停板、板块热度、热榜、K 线图、技术指标 |
| 实时行情/价格 | 23 | 实时股价、涨跌幅、成交量、历史行情 |
| 宏观经济 | 22 | CPI/PPI/PMI/GDP/利率/汇率/货币供应量 |
| 企查查-司法涉诉 | 19 | 破产重整、债权人、司法冻结、失信被执行 |
| 国内监管执法 | 19 | 证监会处罚、交易所问询函、违规处罚、私募登记 |
| 企查查-高管履历/风险 | 36 | 高管任职、历史处罚、个人诉讼、受益所有人 |
| 定期报告阅读 | 18 | 年报/半年报/财报点评、研报观点、公司/行业/宏观观点 |
| 境外制裁/合规 | 15 | OFAC 制裁名单、MAS 监管、EU 金融制裁、FDA 召回 |
| 信用/票据风险 | 14 | 重大诉讼仲裁、票据违约、广告审查 |
| 企查查-经营合规 | 11 | 行政处罚、环保安全、税务违规 |
| 国内信息披露/公告 | 10 | 巨潮公告全文、交易所公告、业绩预告 |
| 股权激励 | 9 | 期权计划、员工持股、高管获授、激励方案要素 |
| 产业链分析 | 7 | 产业链债券、供应链融资、产业债发行人 |
| 资金流向 | 7 | 北向资金、龙虎榜席位、主力资金 |
| 境外披露（SEC/TDnet） | 6 | 美股 SEC Filing、港股披露易、日本 TDnet |
| 公司事件 | 5 | 并购重组、控制权变更、重大资产重组 |
| 融资融券 | 5 | 两融余额、融资买入、融券余量 |

## 使用流程

通过 Cue runner 提交研究问题后，Cue 服务端自动调度 470+ 工具完成多源取证与交叉验证，预计耗时 3-15 分钟。研究完成后结果写入本地 Markdown 文件，来源链接可逐条回查。

## 适用场景

| 场景 | 解决的问题 |
|------|-----------|
| 公开市场研究 | 一家公司、一个行业、一个事件——基于公开数据源交叉验证 |
| 竞品对标 | 多主体横向对比，数据源一致、口径可比 |
| 投资前摸底 | 快速了解一个公司的基本面/风险/产业链位置 |
| 行业趋势判断 | 从多个数据源交叉验证行业景气度 |
| 监管/合规排查 | 工商/司法/监管处罚/问询函全覆盖 |
| 内容创作 | 用仿写功能让报告按你的风格输出 |

## 核心优势

1. **470 个专业 MCP 工具，58 个类别，20 家数据提供方** — 从聚源（A 股财务/研报/机构）、企查查（工商/司法/高管）、东方财富（行情/资金流）、SEC/港交所（境外披露）、OFAC/MAS（制裁合规）等 20 家数据源取证
2. **多源交叉验证** — 同一结论从多个独立数据源交叉印证，数据冲突时明确标注分歧
3. **100% 溯源，不杜撰** — 每条结论带公开来源链接，可逐条回查验证
4. **仿写（mimic）** — 给一篇参考链接或样本文档，报告自动模仿其写作风格与结构
5. **Agent 原生** — 无需网页端，在自己的 AI agent 里直接跑；支持 Claude Code / Gemini CLI / 各种 agent

## 试试这样问

- "调研一下比亚迪的基本面和近期风险"
- "光伏行业当前景气度如何？哪些环节最受益？"
- "宁德时代和比亚迪的财务健康度对比"
- "最近三个月AI芯片赛道有什么重要进展？"
- "万科的债务结构和偿债压力分析"
- "用这个链接的风格帮我分析特斯拉 Q2 财报"（仿写）

## 输出形式

结构化深度研究报告：核心结论 → 多维度分析 → 数据来源交叉验证 → 风险提示 → 每条结论附原链接。

### 步骤 0：接入与装配 + 首任务引导（任何任务之前，必须最先执行）

开跑任何任务前，先确认 API Key 已就绪：

1. **检查 Key**：`~/.cue/config.json` 的 `api_key`（或环境变量 `CUE_API_KEY`）是否有值。
2. **未配置 / 失效**：**停止任务**，由用户本人创建（Agent 不能代生成、无权查看）。按以下话术告知：
   > 请前往 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-deep-research) 注册后免费创建 API Key，点击「创建 API Key」，生成后点「复制」并粘贴发送给我。
   拿到 Key 后写入 `~/.cue/config.json`；若本 skill 依赖 MCP 工具，按对应小节完成挂载并提示重启客户端。
3. **健康检查全绿后**，若用户还没给出具体任务，**必须主动引导第一次真实调用**，不要停在"环境已就绪"：
   > 环境已就绪 ✅ 下面这些都可以直接跑，比如：
   > 1. "调研一下比亚迪的基本面和近期风险"
   > 2. "光伏行业当前景气度如何？哪些环节最受益？"
   >
   > 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题用本 skill 示例小节的原文，别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

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
  3. `分享到小红书，获得 200 积分`——点击 https://cuecue.cn/activity/xhs?conversation_id={{conv_id}}&skill_name=Cue 深度研究（通用版）（把 `{{conv_id}}` 替换为本次报告的 id，见下）
  4. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

**小红书分享链接怎么拼（第 3 项）**：
- 固定格式：`https://cuecue.cn/activity/xhs?conversation_id=<conv_id>&skill_name=Cue 深度研究（通用版）`
- `conversation_id` = 本次交付报告对应的 Cue 报告 id（交付时 Cue 报告链接 `https://cuecue.cn/share/<conv_id>` 里的同一串 id），必须来自实际输出，禁止编造。
- `skill_name` 固定为 `Cue 深度研究（通用版）`，不得改写。
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

**首次使用需安装 Runner**（检查依赖 → 克隆 runner → 验证 Key → 测试连通性）：

```bash
if [ -d ~/.cue/cue-skills/.git ]; then
  git -C ~/.cue/cue-skills pull --ff-only
else
  git clone https://github.com/sensedeal/cue-skills ~/.cue/cue-skills \
    || git clone https://gitee.com/sensedeal/cue-skills ~/.cue/cue-skills
fi
```

依赖：`git` + `python3` + `curl`（macOS 自带，Linux `apt install git python3 curl`）。Python 仅用标准库，无额外 pip 依赖。

Cue API Key：[cuecue.cn](https://cuecue.cn/api-key?src=clawhub-deep-research) 注册后免费创建。新账号送 500 积分，每天再免费送 10 分。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发送给您正在使用的智能体。

Runner 来源：[GitHub - sensedeal/cue-skills](https://github.com/sensedeal/cue-skills)（[Gitee 镜像](https://gitee.com/sensedeal/cue-skills)）。

> **API Key 只能由用户本人创建**：Agent 既不能代生成、也无权查看用户的 Key。检测到未配置或失效时，按以下话术告知用户：**「点击『创建 API Key』，生成 API Key 后一定要点击『复制』并粘贴发送给我。」** 然后等待用户提供，**禁止声称"我去生成/查看"**。

---

## 调用说明

### 基础用法：自由式深研（最通用）

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "你的研究问题——任意金融/商业/行业问题" \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-deep-research.md
```

### 仿写：让报告模仿指定风格

> ⚠️ **隐私提示**：使用 `--mimic-file` 时，指定的本地文档（PDF/Word/Markdown 等）将被上传至 Cue 服务端进行风格分析。请勿对包含机密、个人、受监管或专有内容的文件使用此参数。仅使用你确认可以发送到 Cue 服务的文档。

```bash
# 方式一：模仿一个链接的风格
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "你的研究问题" \
  --mimic-url "https://example.com/reference-report" \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-mimic.md

# 方式二：模仿本地文档的风格
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "你的研究问题" \
  --mimic-file "~/Documents/reference.pdf" \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-mimic.md
```

| 参数 | 说明 |
|------|------|
| `--query` | 研究问题，**必填**；中英文均可，越具体越好 |
| `--mimic-url` | 参考链接，报告模仿其写作风格 |
| `--mimic-file` | 参考文档，报告模仿其写作风格（PDF/Word/Markdown 等） |
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

本 Skill 检索由 Cue 远程服务完成，流程为 Agent → Cue API（cuecue.cn）→ 外部数据源。本地仅读取 `~/.cue/config.json` 中的 API Key 用于鉴权。使用 `--mimic-file` 时，指定的本地文档将被上传至 Cue 服务端进行风格分析，请勿对敏感或机密文件使用该参数。

| 环节 | 谁控制 | 出问题时 |
|------|--------|---------|
| API Key 鉴权 | 用户本人 | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-deep-research) 生成后点「复制」并粘贴发送给您正在使用的智能体，再由 Agent 写入 ~/.cue/config.json（Agent 不能代生成，也无权查看） |
| Cue 服务端 | Cue 运维 | 等恢复，或走降级方案 |
| 外部数据源 | 公开网站 | Cue 用缓存兜底，标注"来源暂不可达" |

---

## 健康检查

跑研究前先验证四件事。一键诊断：

```bash
echo "=== 1/4 API Key ===" && [ -f "$HOME/.cue/config.json" ] && echo "已配置" || echo "未配置！"
echo "=== 2/4 Cue 服务 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/health"
echo "=== 3/4 搭子 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/playbook" | python3 -c "import sys,json;data=json.load(sys.stdin).get('data',{});scenes=data.get('scenes',[]) if data else [];total=sum(len(s.get('buddies',[])) for s in scenes);print(f'可用:{total}个搭子') if scenes else print('暂不可用')"
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
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-deep-research) 生成后点「复制」并粘贴发送给您正在使用的智能体（Agent 无法代生成，也无权查看） |
| 服务 | `{"status":"healthy"}` | 等 5 分钟重试 |
| 搭子 | `可用:>0个搭子` | 等 1h 或网页端手动跑 |

> 配置完成后的首次调用引导已并入「步骤 0：接入与装配 + 首任务引导」，按该节执行。

---

## 自救指引

### 错误速查

| 现象 | 原因 | 怎么修 |
|------|------|--------|
| 401 / Key 无效 | Key 过期或写错 | 由用户本人重新生成 Key，更新 `~/.cue/config.json` |
| 超时 >30s | 服务维护/过载 | 等 5 分钟，跑诊断；当天内重试 |
| 搭子列表为空 | 服务端维护 | 网页端直接跑，或等 1 小时 |
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

### 常见问题排查

- Key 报错：由用户本人重新生成 Key，更新 config.json，重试
- 服务连不上：检查 DNS/代理，等 5 分钟重试
- 搭子列表为空：等 1 小时或使用网页端
- 中途中断：使用相同 prompt 续接
- 结果空：缩小搜索范围，确认该主题有公开数据

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
| [百度](https://www.baidu.com) | 中文公开信息 | 免费 |
| [Google](https://www.google.com) | 全球公开信息 | 免费 |
| [Wikipedia](https://www.wikipedia.org) | 百科知识 | 免费 |
| 各垂直领域官网 | 专业数据 | 视来源而定 |

## FAQ

**Q: 和场景版 skill（盘前策略/盘后复盘/产业链挖掘等）有什么区别？**
A: 场景版是"预制菜"——固定模板、固定报告结构，适合高频重复场景。通用版是"自助餐"——不绑模板，后台按问题自动规划工具链，适合一次性、探索性研究。

**Q: 数据源具体有哪些？**
A: 470 个 MCP 工具、20 家数据提供方，详见上方"数据源全景"。核心数据方含：聚源（A 股财务/研报/机构调研/一致预期）、企查查（工商/司法/高管/经营合规/资产风险）、东方财富（行情/盘面/资金流）、SEC EDGAR（美股披露）、港交所披露易（港股公告）、OFAC/MAS/EU（制裁合规）、LEI 基金会（全球主体识别）等。

**Q: 仿写能模仿到什么程度？**
A: 模仿写作风格、报告结构、术语习惯、详略节奏——不是复制内容。给一篇研报链接，输出按你的风控/投研/投顾风格来。仅自由式深研支持，有模板的搭子不适用。

**Q: 溯源链接是什么样的？**
A: 每条结论后面跟公开来源 URL，例如 "公司 2025Q3 营收同比增长 23%（[来源](https://...))"，可点击回查原始数据。

**Q: 报告能在网页端看原文吗？**
A: 能。交付时会同时附上 Cue 原始报告链接 `https://cuecue.cn/share/<conv_id>`，可回网页端查看完整原文、继续追问或转发同事。

**Q: 提示积分不足怎么办？**
A: 打开 [cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」，分享给好友注册，当好友激活使用后积分即到账；或首次购买 9.9 加油包获得 900 积分继续体验：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。积分不足不要重试。
