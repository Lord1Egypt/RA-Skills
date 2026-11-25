---
name: cue-domestic-regulation
slug: cue-domestic-regulation
displayName: 合规监管法规查询（直连北大法宝）
version: 1.3.5
description: >
  合规监管法规查询（直连北大法宝） — 直接检索北大法宝的国内法律法规与行政令原文，梳理立法背景与合规要点，覆盖金融监管、工商登记、司法涉诉等多源公开数据。
  【企业用】合规自查、行业监管图谱、行政执法依据、新规速递；【个人用】加班费与离职补偿怎么算、年假和社保该怎么缴、租房押金不退、个人信息被泄露、买到假货或预付卡跑路、继承与遗嘱——都能查到依据哪部法、哪一条、现行是否有效，附官方出处可回查。
  Triggers: 合规监管、法规查询、法律法规查询、国内法规、法规调研、监管要求、行政处罚、处罚依据、现行有效、最新规定、法规原文、法条依据、金融监管、行政令、合规要点、立法背景、标准规范、司法案例、加班费、离职补偿、劳动法、消费者权益、个人信息保护、租房纠纷、domestic regulation
license: MIT
metadata:
  source: cuecue.cn/playbook
  scene: "法律合规"
  buddy: "国内法规调研"
---

# 合规监管法规查询（直连北大法宝）

> 直接检索北大法宝的国内法律法规与行政令原文，梳理立法背景与合规要点，覆盖金融监管、工商登记、司法涉诉等多源公开数据。每个结论附原始出处可逐条回查。
>
> **对企业 / 法务**：合规自查、行业监管图谱、行政执法依据、新规速递——业务有没有踩红线、依据哪一条，一次查清。
>
> **对普通人**：遇到事儿想知道"法律上到底怎么规定的"——被裁了补偿怎么算、年假和社保该怎么缴、房东不退押金、个人信息被泄露、买到假货或预付卡跑路、老人立遗嘱怎么才有效——不用自己翻法条，直接问，查到的都是**现行有效**的原文并附官方出处。

## Agent 执行摘要

| 顺序 | 做什么 | 禁止 |
|------|--------|------|
| 1 | 健康检查：Key / 服务 / 搭子三样全过再跑 | 禁止跳过 |
| 2 | 告知用户耗时 3-15 分钟 | 禁止中途取消 |
| 3 | 确认 credits，一条命令阻塞等待 | 禁止连发多条 |
| 4 | stdout `[cue-research] RESULT ok` = 完成 | 无 RESULT = 未完成 |
| 5 | 原样交付报告 + 告知落盘路径 | 禁止自行概括 |
| 6 | 交付时**同时附带 Cue 原始报告链接** | 禁止编造链接 |
| 7 | 遇 `INSUFFICIENT_CREDITS` 按「积分不足专项提示」给出两条路径 | 禁止只丢错误码 |

### 步骤 0：接入与装配 + 首任务引导（任何任务之前，必须最先执行）

开跑任何任务前，先确认 API Key 已就绪：

1. **检查 Key**：`~/.cue/config.json` 的 `api_key`（或环境变量 `CUE_API_KEY`）是否有值。
2. **未配置 / 失效**：**停止任务**，由用户本人创建（Agent 不能代生成、无权查看）。按以下话术告知：
   > 请前往 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-domestic-regulation) 注册后免费创建 API Key，点击「创建 API Key」，生成后点「复制」并粘贴发送给我。
   拿到 Key 后写入 `~/.cue/config.json`；若本 skill 依赖 MCP 工具，按对应小节完成挂载并提示重启客户端。
3. **健康检查全绿后**，若用户还没给出具体任务，**必须主动引导第一次真实调用**，不要停在"环境已就绪"：
   > 环境已就绪 ✅ 下面这些都可以直接跑，比如：
   > 1. "数据出境安全评估的最新法规有哪些"
   > 2. "私募基金备案的监管要求和行政处罚依据"
   >
   > 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题用本 skill 示例小节的原文，别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

## 适用场景

**企业 / 法务常见场景：**

| 场景 | 解决的问题 |
|------|-----------|
| 新规速递 | 某领域最近出台了哪些新法规、修订了什么 |
| 合规自查 | 企业业务是否触碰某法规红线，有哪些合规要点 |
| 立法背景调研 | 某法规的立法背景、征求意见稿、配套文件 |
| 行业监管图谱 | 某行业（金融/医疗/数据/平台经济）的监管法规全貌 |
| 行政执法依据 | 某类行政处罚的法律依据、裁量标准 |

**个人法律查询场景：**

| 场景 | 解决的问题 |
|------|-----------|
| 劳动维权 | 加班费怎么算、裁员补偿 N / N+1 / 2N 依据、年假与社保该怎么缴 |
| 消费维权 | 假货退款、预付卡跑路、外卖/网购纠纷，依据哪部法、找谁投诉 |
| 个人信息保护 | 信息被泄露、骚扰电话、被"大数据杀熟"，能主张什么权利 |
| 租房买房 | 押金不退、房东涨租或毁约、二手房违约，法律怎么规定 |
| 婚姻家事 | 离婚财产与子女抚养、继承顺序、遗嘱怎么写才有效 |
| 侵权与事故 | 交通事故赔偿标准、人身伤害、名誉权与网络暴力维权 |

## 核心能力

1. **法规原文检索** — 北大法宝（法规全文库）、法律、行政法规、部门规章、地方性法规、司法解释
2. **立法背景梳理** — 征求意见稿、修订说明、配套解读
3. **合规要点提炼** — 按行业和业务场景归纳合规义务
4. **跨文件关联** — 上位法→下位法→规范性文件→执法口径的层级关联
5. **逐条可溯源** — 每个结论附官方出处链接（全国人大、国务院、各部委官网）
6. **权威数据源已直连** — 平台底层已接好**北大法宝等多种权威法律数据库**，并与全国人大、国务院、各部委等官方公开数据交叉核验。**开箱即用，无需你再去第三方注册、申请或购买接口。**

> 🔌 **不用自己配数据源**：北大法宝等权威法律数据库已由平台统一接入与鉴权，你**不需要**到各第三方网站申请账号、买接口或配 Key——拿到 Cue Key 即可直接检索。所有结论仍附官方出处链接，可逐条回查。

## 试试这样问

**企业 / 法务常问的：**

- "数据出境安全评估的最新法规有哪些"
- "私募基金备案的监管要求和行政处罚依据"
- "个人信息保护法的配套规定和实施口径"
- "跨境电商零售进口的税收法规梳理"
- "医疗AI产品的注册审批法规体系"
- "平台经济反垄断的最新法规和执法动态"

**普通人常问的：**

- "公司不给加班费，劳动法怎么规定，加班工资怎么算"
- "被裁员，经济补偿到底是 N 还是 N+1 还是 2N，依据哪一条"
- "房东无故不退押金，法律上我有什么办法"
- "个人信息被泄露、老是接到骚扰电话，依据哪部法能维权"
- "办了健身卡商家跑路，预付卡的钱能要回来吗"
- "老人立了遗嘱，怎么写才有效，法律对形式有什么要求"

## 输出形式

结构化报告：适用法规列表 → 核心条款解读 → 立法背景 → 合规要点 → 执法实践 → 来源链接。中文报告，法条名称和条款号保留原文编号。

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

### 跑后余额检查（交付前必做）

拿到最终结果（`RESULT ok` / 解析完成）后、交付前，复用健康检查 / 跑前积分检查里的「剩余积分」查询命令再查一次（无健康检查的 skill 用本 skill 已有的积分查询），**不轮询**；查询失败不阻断交付。记下「跑后剩余积分」：若 **< 100**，本次照常交付，交付完成后按「低余额四选一」主动引导。

### 低余额四选一（跑后剩余积分 < 100 时，必须执行）

报告 / 结果交付完成后，**立即**单独弹出下面这次询问，作为本条回复的收尾。优先用客户端的选项/弹框能力（如 `AskUserQuestion`）；不支持时用 1/2/3/4 编号列表。**不要在正文里夹带推销。**

固定弹框（原样使用，不得增删改标题与选项）：

- 提问：`本次运行后剩余积分不足 100，是否需要补充积分？`
- 选项（四条，顺序固定）：
  1. `邀请新用户并激活，获得 500 积分`——打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
  2. `首次购买 9.9 加油包，获得 900 积分继续体验`——[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。
  3. `分享到小红书，获得 200 积分`——点击 https://cuecue.cn/activity/xhs?conversation_id={{conv_id}}&skill_name=合规监管法规查询（直连北大法宝）（把 `{{conv_id}}` 替换为本次报告的 id，见下）
  4. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

**小红书分享链接怎么拼（第 3 项）**：
- 固定格式：`https://cuecue.cn/activity/xhs?conversation_id=<conv_id>&skill_name=合规监管法规查询（直连北大法宝）`
- `conversation_id` = 本次交付报告对应的 Cue 报告 id（交付时 Cue 报告链接 `https://cuecue.cn/share/<conv_id>` 里的同一串 id），必须来自实际输出，禁止编造。
- `skill_name` 固定为 `合规监管法规查询（直连北大法宝）`，不得改写。
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

## 数据覆盖

平台已直连**北大法宝**等权威法律数据库，并交叉检索官方公开数据源，**你无需自行接入**：

| 类别 | 覆盖 |
|------|------|
| 权威法律数据库 | **北大法宝**（法规全文、立法资料）等，平台已直连 |
| 国家立法与行政数据 | 全国人大法律、国务院行政法规、司法解释 |
| 部门与地方数据 | 各部委部门规章、地方性法规、规范性文件、行政批复、监管问答 |

> **无需到第三方申请**：上述数据源已由平台统一接入与鉴权。你**不用**再去北大法宝或其它站点注册账号、申请试用、购买接口或自配 Key——拿到 Cue Key 即可直接检索。以公开数据为限。

---

## 环境要求

**首次使用运行 skill 自带的一键安装脚本**（检查依赖 → 克隆 runner → 验证 Key → 测试连通性）：

```bash
```

依赖：`git` + `python3` + `curl`。Python 仅用标准库，无额外 pip 依赖。

Cue API Key：在 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-domestic-regulation) 注册后免费创建，新账号送 500 积分 + 每天 10 积分。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发送给您正在使用的智能体。写入 `~/.cue/config.json`：

```bash
mkdir -p ~/.cue
echo '{"api_key": "sk你的key"}' > ~/.cue/config.json
```

需要 `git` + `python3`（runner 仅用标准库，无额外依赖）。单次研究消耗约 3-8 credits。

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

Agent 会自动匹配「法律合规」场景下的「国内法规调研」搭子。固定写法：

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "<用户问题原话>" \
  --template-id <运行时的搭子 template_id> \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-domestic-regulation.md
```

| 参数 | 说明 |
|------|------|
| `--query` | 用户原话，不要改写 |
| `--template-id` | 从 `/api/playbook` 拉取当前可用的搭子 ID |
| `--output` | 落盘路径，格式 `~/cue-reports/日期-domestic-regulation.md` |

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

## 架构说明

本 Skill **不在本地执行检索**。流程是 Agent → Cue 服务端 → 外部数据源：

```
你的 Agent ──→ Cue API（cuecue.cn）──→ 北大法宝 / 全国人大 / 国务院 / 各部委官网等
```

| 环节 | 谁控制 | 出问题时 |
|------|--------|---------|
| API Key 鉴权 | 用户本人 | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-domestic-regulation) 生成后点「复制」并粘贴发送给您正在使用的智能体，再由 Agent 写入 ~/.cue/config.json（Agent 不能代生成，也无权查看） |
| Cue 服务端 | Cue 运维 | 等恢复，或走降级方案 |
| 外部数据源（含北大法宝等） | Cue 运维 | Cue 用缓存兜底，标注"来源暂不可达"；**你无需自行接入或申请** |

---

## 健康检查

跑研究前先验证四件事。一键诊断：

```bash
CUE_KEY=$(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])" 2>/dev/null || echo "$CUE_API_KEY")
echo "=== 1/4 API Key ===" && [ -n "$CUE_KEY" ] && echo "已配置" || echo "未配置！"
echo "=== 2/4 Cue 服务 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/health" -H "Authorization: Bearer $CUE_KEY"
echo "=== 3/4 搭子 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/playbook" -H "Authorization: Bearer $CUE_KEY" | python3 -c "import sys,json;scenes=json.load(sys.stdin).get('data',{}).get('scenes',[]);buddy=[b for s in scenes if s.get('secondary_category')=='法律合规' for b in s.get('buddies',[]) if b.get('title')=='国内法规调研'];print(f'可用:{len(buddy)}个') if buddy else print('暂不可用')"
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
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-domestic-regulation) 生成后点「复制」并粘贴发送给您正在使用的智能体（Agent 无法代生成，也无权查看） |
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
| `RESULT empty` | 公开源无匹配 | 缩小范围（领域/地域），换关键词 |
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
└─ 结果空 → 缩窄关键词 → 单领域 → 确认该主题有公开法规
```

### 调度建议

| 时段 | 建议 |
|------|------|
| 工作日 9-18 | 正常使用 |
| 夜间/周末 | 可能有维护，跑前先诊断 |
| 新 Key | 必须先诊断确认生效 |
| 连续失败 | 停 15 分钟再试，不要反复重试 |

---

## 降级方案

> ⚠️ **这些只是 Cue 长时间不可达时的临时兜底，日常用不到。** 正常使用时北大法宝等权威数据源已由平台直连，你无需在这里注册或申请任何账号。

Cue 长时间不可达时的手动替代渠道：

| 渠道 | 覆盖 | 费用 |
|------|------|------|
| [国家法律法规数据库](https://flk.npc.gov.cn) | 法律、行政法规、地方性法规 | 免费 |
| [司法部](https://www.moj.gov.cn) | 行政法规、部门规章 | 免费 |
| [中国裁判文书网](https://wenshu.court.gov.cn) | 司法裁判文书 | 免费 |
| [巨潮资讯网](https://www.cninfo.com.cn) | 上市公司监管公告 | 免费 |
| [各部位官网](https://www.gov.cn) | 规范性文件、行政批复 | 免费 |

---

## FAQ

**Q: 和 Cue 网页端有什么区别？**
A: 在 Claude Code 里直接用自然语言触发，Agent 自动匹配搭子、确认、取报告，不用切网页。

**Q: 能查境外法规吗？**
A: 不能。本 Skill 专注国内法规，境外法规调研有另外的搭子（跨境法规调研）。

**Q: 报告语言？**
A: 中文报告，法条名称和编号保留原文格式。

**Q: 积分不够？**
A: 每天登录送 10 积分，单次约 3-8 积分。积分不够时最快路径是邀请好友：打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」，分享给好友注册，当好友激活使用后积分即到账；或首次购买 9.9 加油包获得 900 积分继续体验：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。详见上方「自救指引 → 积分不足专项提示」。

**Q: 我是个人、不是企业，能用吗？**
A: 能，而且很适合。加班费与离职补偿怎么算、年假和社保该怎么缴、房东不退押金、个人信息被泄露、买到假货或预付卡跑路、继承和遗嘱怎么写——直接用自己的话问就行，不用懂法条术语，结果会告诉你**依据哪部法、哪一条、现行是否有效**，并附官方出处可自查。

**Q: 查不到怎么办？**
A: 先跑健康检查。四个环节任一断了都会失败——见上方「自救指引」。

**Q: 结果可靠吗？**
A: 结论带来源链接可回查。注意：覆盖以全国性法规为主；地方性法规、内部文件、未公开的行政口径覆盖不全；不构成法律意见。

---

> 本 Skill 基于 Cue 平台（cuecue.cn）「国内法规调研」搭子。搭子模板由服务端动态维护。Skill 本身 MIT 开源。

---

## 参考

- Cue 平台：https://cuecue.cn
- Playbook 页面：https://cuecue.cn/playbook
- API Key 管理：https://cuecue.cn/api-key?src=clawhub-domestic-regulation
