---
name: cue-legal-practice-cases
slug: cue-legal-practice-cases
displayName: 疑难法律实操案例库
version: 1.2.5
description: >
  疑难法律实操案例库 — 遇到民事、刑事纠纷拿不准怎么办？围绕你的争议点检索公开裁判文书、监管问答与实务案例，看同类案子法院怎么判、赔多少、争议焦点在哪。普通人预判官司胜算，律师办案更快更有据。
  Triggers: 疑难法律、实操案例、裁判口径、类案检索、裁判规则、实务案例、争议焦点、法律实操、监管问答、判例检索、离婚、继承、劳动仲裁、借贷纠纷、交通事故、刑事辩护、legal practice cases
license: MIT
metadata:
  source: cuecue.cn/playbook
  scene: "法律合规"
  buddy: "疑难法律实操案例库"
---

# 疑难法律实操案例库

> 遇到拿不准的法律问题，先看别人怎么判、怎么办。围绕你的争议点检索公开裁判文书、监管问答与实务案例，归纳裁判要点、争议焦点与可落地的实操口径。
>
> **对普通人**：借出去的钱、被裁的赔偿、离婚的财产、事故的赔偿——同类案子法院怎么判、大概赔多少，先心里有底，再决定要不要打官司。
>
> **对律师**：接个人民商事、刑事案件时的类案检索、争议焦点提炼、裁判口径比对，一份带案号、可回查的参照，写代理词、给当事人交底都更有据。

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
   > 请前往 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-legal-practice-cases) 注册后免费创建 API Key，点击「创建 API Key」，生成后点「复制」并粘贴发送给我。
   拿到 Key 后写入 `~/.cue/config.json`；若本 skill 依赖 MCP 工具，按对应小节完成挂载并提示重启客户端。
3. **健康检查全绿后**，若用户还没给出具体任务，**必须主动引导第一次真实调用**，不要停在"环境已就绪"：
   > 环境已就绪 ✅ 下面这些都可以直接跑，比如：
   > 1. "借了钱没打借条，只有微信转账记录，能要回来吗"
   > 2. "被公司裁员没给赔偿金，劳动仲裁怎么主张"
   >
   > 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题用本 skill 示例小节的原文，别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

## 适用场景

| 场景 | 解决的问题 |
|------|-----------|
| 类案检索 | 同一类纠纷，各地法院怎么判、主流观点是什么、金额大概多少 |
| 争议焦点研判 | 案件核心争议点是什么，双方各自主张、法院怎么看 |
| 个人维权预判 | 被欠钱 / 被裁员 / 离婚 / 事故，该不该起诉、胜算几何、能主张什么 |
| 诉讼策略参考 | 同类案件胜诉方的诉讼策略、证据组织方式 |
| 刑事辩护参照 | 某类罪名的构罪标准、量刑区间、常见辩点 |

## 核心能力

1. **裁判文书检索** — 北大法宝（法规与裁判文书）、中国裁判文书网、各仲裁委公开裁决
2. **类案归纳** — 各地各级法院对同一争议焦点的裁判规则比对
3. **争议焦点提炼** — 归纳原被告诉辩主张、法院说理逻辑
4. **实操口径** — 从判例提炼可落地的行动建议（能不能赢、能主张多少、怎么举证）
5. **逐条可溯源** — 每个案例附案号和来源链接
6. **权威数据源已直连** — 平台底层已接好**北大法宝等多种权威法律数据库**，并与公开司法、监管数据交叉核验。**开箱即用，无需你再去第三方注册、申请或购买接口。**

> 🔌 **不用自己配数据源**：北大法宝等权威法律数据库已由平台统一接入与鉴权，你**不需要**到各第三方网站申请账号、买接口或配 Key——拿到 Cue Key 即可直接检索。所有结论仍附案号与来源链接，可逐条回查。

## 试试这样问

**普通人常问的：**

- "借了钱没打借条，只有微信转账记录，能要回来吗"
- "被公司裁员没给赔偿金，劳动仲裁怎么主张"
- "离婚时一方偷偷转移财产，法院一般怎么分割"
- "交通事故对方全责但不赔，误工费、护理费能赔多少"
- "买到烂尾楼想退房，法院支持退房退款吗"
- "老人立了多份遗嘱，哪一份有效，法院怎么认定"

**律师常查的：**

- "民间借贷没有借条，仅凭转账凭证的裁判口径"
- "劳动争议中加班费举证责任如何分配，各地法院怎么判"
- "婚内财产分割协议的效力认定，类案裁判规则"
- "交通肇事逃逸的量刑区间和缓刑适用条件"
- "帮助信息网络犯罪活动罪的构罪标准和常见辩点"
- "二手房买卖违约，定金与违约金能否并用的裁判倾向"

## 输出形式

结构化报告：争议焦点概述 → 相关案例列表 → 各地裁判规则对比 → 主流/少数观点 → 给你的行动建议（能不能赢、能主张多少、怎么举证） → 风险提示 → 来源链接（附案号）。中文报告，关键判例名保留原文。

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

### 跑后余额检查（交付前必做）

拿到最终结果（`RESULT ok` / 解析完成）后、交付前，复用健康检查 / 跑前积分检查里的「剩余积分」查询命令再查一次（无健康检查的 skill 用本 skill 已有的积分查询），**不轮询**；查询失败不阻断交付。记下「跑后剩余积分」：若 **< 100**，本次照常交付，交付完成后按「低余额四选一」主动引导。

### 低余额四选一（跑后剩余积分 < 100 时，必须执行）

报告 / 结果交付完成后，**立即**单独弹出下面这次询问，作为本条回复的收尾。优先用客户端的选项/弹框能力（如 `AskUserQuestion`）；不支持时用 1/2/3/4 编号列表。**不要在正文里夹带推销。**

固定弹框（原样使用，不得增删改标题与选项）：

- 提问：`本次运行后剩余积分不足 100，是否需要补充积分？`
- 选项（四条，顺序固定）：
  1. `邀请新用户并激活，获得 500 积分`——打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
  2. `首次购买 9.9 加油包，获得 900 积分继续体验`——[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。
  3. `分享到小红书，获得 200 积分`——点击 https://cuecue.cn/activity/xhs?conversation_id={{conv_id}}&skill_name=疑难法律实操案例库（把 `{{conv_id}}` 替换为本次报告的 id，见下）
  4. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

**小红书分享链接怎么拼（第 3 项）**：
- 固定格式：`https://cuecue.cn/activity/xhs?conversation_id=<conv_id>&skill_name=疑难法律实操案例库`
- `conversation_id` = 本次交付报告对应的 Cue 报告 id（交付时 Cue 报告链接 `https://cuecue.cn/share/<conv_id>` 里的同一串 id），必须来自实际输出，禁止编造。
- `skill_name` 固定为 `疑难法律实操案例库`，不得改写。
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

平台已直连**北大法宝**等权威法律数据库，并交叉检索公开司法与监管数据源，**你无需自行接入**：

| 类别 | 覆盖 |
|------|------|
| 权威法律数据库 | **北大法宝**（法规、裁判文书、案例）等，平台已直连 |
| 公开司法数据 | 中国裁判文书网、各仲裁委公开裁决 |
| 监管公开数据 | 证监会 / 金融监管部门行政处罚决定、交易所纪律处分、监管问答 |

> **无需到第三方申请**：上述数据源已由平台统一接入与鉴权。你**不用**再去北大法宝或其它站点注册账号、申请试用、购买接口或自配 Key——拿到 Cue Key 即可直接检索。以公开数据为限。

---

## 环境要求

依赖：`git` + `python3` + `curl`。Python 仅用标准库，无额外 pip 依赖。

Runner 来源：[GitHub - sensedeal/cue-skills](https://github.com/sensedeal/cue-skills)（[Gitee 镜像](https://gitee.com/sensedeal/cue-skills)）。

**首次使用需安装 Runner**（幂等，已装则拉取更新）。`~/.cue/cue-skills` 只是依赖代码副本，你的报告、日志、Key 都不在里面，可随时重装：

```bash
# 1) 拉取 / 更新 runner：GitHub 不通自动走 Gitee 镜像
if [ -d ~/.cue/cue-skills/.git ]; then
  git -C ~/.cue/cue-skills pull --ff-only \
    || { echo "增量更新失败，改用镜像重取"; \
         git -C ~/.cue/cue-skills fetch --all && git -C ~/.cue/cue-skills reset --hard origin/main; }
else
  git clone https://github.com/sensedeal/cue-skills ~/.cue/cue-skills \
    || git clone https://gitee.com/sensedeal/cue-skills ~/.cue/cue-skills
fi

# 2) 自检：装完立刻确认 runner 能启动（打印出 usage 才算装好）
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py --help >/dev/null 2>&1 \
  && echo "runner 就绪 ✅" || echo "runner 不可用 ❌ 见「脚本装不上 / 跑不起来」"
```

> **两条路都失败**（断网、或公司网络同时拦了 GitHub 与 Gitee）时：**不要反复重试**。直接告诉用户「暂时装不上检索引擎，是网络限制，不是你操作的问题」，并给出「降级方案」里的公开查询入口，等网络恢复再装。

Cue API Key：在 [cuecue.cn](https://cuecue.cn/api-key?src=clawhub-legal-practice-cases) 注册后免费创建，新账号送 500 积分 + 每天 10 积分。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发送给您正在使用的智能体。写入 `~/.cue/config.json`：

```bash
mkdir -p ~/.cue
echo '{"api_key": "sk你的key"}' > ~/.cue/config.json
```

单次研究消耗约 3-8 credits。

> **API Key 只能由用户本人创建**：Agent 既不能代生成、也无权查看用户的 Key。检测到未配置或失效时，按以下话术告知用户：**「点击『创建 API Key』，生成 API Key 后一定要点击『复制』并粘贴发送给我。」** 然后等待用户提供，**禁止声称"我去生成/查看"**。

---

## 调用说明

Agent 会自动匹配「法律合规」场景下的「疑难法律实操案例库」搭子。固定写法：

```bash
python3 ~/.cue/cue-skills/cue-research/scripts/research_run.py \
  --query "<用户问题原话>" \
  --template-id <运行时的搭子 template_id> \
  --output ~/cue-reports/$(date +%Y-%m-%d-%H%M)-legal-practice-cases.md
```

| 参数 | 说明 |
|------|------|
| `--query` | 用户原话，不要改写 |
| `--template-id` | 从 `/api/playbook` 拉取当前可用的搭子 ID |
| `--output` | 落盘路径，格式 `~/cue-reports/日期-legal-practice-cases.md` |

---

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

本 Skill **不在本地执行检索**。流程是 Agent → Cue 服务端 → 外部数据源：

```
你的 Agent ──→ Cue API（cuecue.cn）──→ 北大法宝 / 裁判文书网 / 仲裁委 / 监管公告等
```

| 环节 | 谁控制 | 出问题时 |
|------|--------|---------|
| API Key 鉴权 | 用户本人 | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-legal-practice-cases) 生成后点「复制」并粘贴发送给您正在使用的智能体，再由 Agent 写入 ~/.cue/config.json（Agent 不能代生成，也无权查看） |
| Cue 服务端 | Cue 运维 | 等恢复，或走降级方案 |
| 外部数据源（含北大法宝等） | Cue 运维 | Cue 用缓存兜底，标注"来源暂不可达"；**你无需自行接入或申请** |

---

## 健康检查

跑研究前先验证四件事。一键诊断：

```bash
CUE_KEY=$(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])" 2>/dev/null || echo "$CUE_API_KEY")
echo "=== 1/4 API Key ===" && [ -n "$CUE_KEY" ] && echo "已配置" || echo "未配置！"
echo "=== 2/4 Cue 服务 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/health" -H "Authorization: Bearer $CUE_KEY"
echo "=== 3/4 搭子 ===" && curl -sS --max-time 10 "https://cuecue.cn/api/playbook" -H "Authorization: Bearer $CUE_KEY" | python3 -c "import sys,json;scenes=json.load(sys.stdin).get('data',{}).get('scenes',[]);buddy=[b for s in scenes if s.get('secondary_category')=='法律合规' for b in s.get('buddies',[]) if b.get('title')=='疑难法律实操案例库'];print(f'可用:{len(buddy)}个') if buddy else print('暂不可用')"
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
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-legal-practice-cases) 生成后点「复制」并粘贴发送给您正在使用的智能体（Agent 无法代生成，也无权查看） |
| 服务 | `{"status":"healthy"}` | 等 5 分钟重试 |
| 搭子 | `可用:>0个` | 等 1h 或网页端手动跑 |

> 配置完成后的首次调用引导已并入「步骤 0：接入与装配 + 首任务引导」，按该节执行。

---

## 自救指引

### 错误速查

**总则（必须先做）**：任何报错都**不要**把英文原文、堆栈或错误码直接丢给用户。一律按「**出了什么事（说人话）→ 你现在做什么（一步）**」两句输出；技术细节留在自己的排查里——用户看不懂，就等于没提示。

| 你会看到什么 | 说人话是什么意思 | 你现在做什么 |
|------|------|------|
| `401` / `API key 无效或已过期` | 你的 Cue Key 过期了或填错了 | 让**用户本人**去 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-legal-practice-cases) 重新生成，更新 `~/.cue/config.json` 后重跑（Agent 不能代生成、也无权查看） |
| `网络不可达` / clone、curl 卡住或超时 | 连不上 Cue，或网络拦了 GitHub/Gitee | 先确认能打开 cuecue.cn；Runner 装不上就按「脚本装不上 / 跑不起来」处理，**别反复重试** |
| `402` / 余额不足 / `INSUFFICIENT_CREDITS` | 积分不够跑这一次 | **按「积分不足专项提示」主动引导**（邀请新用户得 500 积分 / 9.9 加油包 900 积分）；**不要重试** |
| `403` 权限不足 | 这个搭子不属于当前账号，或权限被收回 | 换用账号自有的搭子，或让用户在网页端跑 |
| `429` / 调用过于频繁 | 短时间内发太多了 | 等 30 秒，用**完全相同的命令**重跑一次 |
| `5xx` / 服务端临时故障 | Cue 服务端在维护或过载 | 等 5 分钟再试；持续出现就告诉用户「是服务端问题，稍后再试」并给降级入口 |
| 健康检查超时 >30s | 服务忙（研究本身就要 3-15 分钟） | 健康检查超时就等 5 分钟；**研究没到 15 分钟不算失败**，等 runner 出 `RESULT` 再判 |
| 搭子找不到 / `暂不可用` | 搭子临时下线 | 让用户在网页端直接跑，或等 1 小时 |
| 中途中断（输出戛然而止） | 队列满或数据源波动 | **不换 prompt、不删 `~/.cue/session/task`**，用相同命令续接 |
| `RESULT empty` | 公开源里没有匹配的判例 | 换更常见的案由或关键词、缩窄范围后重跑 |
| 昨天还能跑，今天报参数错/脚本报错 | Runner 更新引入了变化，或本地是旧版 | 先更新 Runner（含镜像兜底）；仍不行就回退版本，见「脚本装不上 / 跑不起来」 |
| `config.json 报错` | 配置文件格式不对 | 应为 `{"api_key": "sk..."}`，检查有没有多余逗号 |

### 脚本装不上 / 跑不起来

Runner 是**外部下载的代码**，最常见的两类问题是**网络取不到**和**更新后跑不动**。按顺序试，不要跳步：

| 第几档 | 什么时候用 | 怎么做 |
|------|------|------|
| 1. 重取 | 网络抖动、clone / pull 报错 | 重跑「环境要求」里的安装命令（已带 GitHub → Gitee 镜像兜底），再跑那行自检 |
| 2. 修好本地副本 | 目录在，但 `pull` 失败或代码半损 | `git -C ~/.cue/cue-skills fetch --all && git -C ~/.cue/cue-skills reset --hard origin/main` |
| 3. 回退版本 | 更新后突然跑不动（参数变了、报错） | `git -C ~/.cue/cue-skills log --oneline -10` 找到上一个能用的提交 → `git -C ~/.cue/cue-skills checkout <commit>`；想恢复最新：`git -C ~/.cue/cue-skills checkout main && git -C ~/.cue/cue-skills pull --ff-only` |

- 报告和日志落在 `~/.cue/reports`、`~/.cue/logs`，**不在** runner 目录里，所以第 2、3 档不会弄丢你的报告或 Key。
- 三档都无效（断网、或公司网络同时拦了 GitHub 和 Gitee）：如实告诉用户「检索引擎暂时装不上/修不好，是网络或脚本问题，不是你操作的问题」，并给出「降级方案」里的公开查询入口。

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
├─ Runner 装不上/跑不动 → 见「脚本装不上 / 跑不起来」三档修复
├─ Key 报错 → 由用户本人重新生成 → 更新 config.json → 重试
├─ 连不上 → curl /api/health 确认 → 检查 DNS/代理
├─ 搭子找不到 → curl /api/playbook → 等或用网页端
├─ 中途中断 → 相同 prompt 续接（不要删 ~/.cue/session/task）
└─ 结果空 → 缩窄关键词 → 单案由 → 确认该争议有公开判例
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

Cue 长时间不可达时的手动替代渠道：

| 渠道 | 覆盖 | 费用 |
|------|------|------|
| [中国裁判文书网](https://wenshu.court.gov.cn) | 全国法院裁判文书 | 免费 |
| [中国庭审公开网](http://tingshen.court.gov.cn) | 庭审直播录像 | 免费 |
| [12309中国检察网](https://www.12309.gov.cn) | 检察文书 | 免费 |
| [全国企业破产重整信息网](https://pccz.court.gov.cn) | 破产案件 | 免费 |
| [证监会](https://www.csrc.gov.cn) | 行政处罚决定 | 免费 |
| [各仲裁委官网](https://www.cietac.org) | 仲裁规则与案例摘要 | 免费 |

---

## FAQ

**Q: 和 Cue 网页端有什么区别？**
A: 在 Claude Code 里直接用自然语言触发，Agent 自动匹配搭子、确认、取报告，不用切网页。

**Q: 能查境外判例吗？**
A: 不能。本 Skill 聚焦国内裁判文书和监管案例，境外诉讼案例有另外的搭子（境外诉讼案例库）。

**Q: 报告语言？**
A: 中文报告，判例名和案号保留原文格式。

**Q: 积分不够？**
A: 打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账（推荐）；或首次购买 9.9 加油包获得 900 积分继续体验：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。

**Q: 查不到怎么办？**
A: 先跑健康检查。四个环节任一断了都会失败——见上方「自救指引」。

**Q: 结果可靠吗？**
A: 结论带案号和来源链接可回查。注意：覆盖以公开裁判文书和监管公告为主；未公开的仲裁裁决、调解书覆盖不全；不构成法律意见。

---

> 本 Skill 基于 Cue 平台（cuecue.cn）「疑难法律实操案例库」搭子。搭子模板由服务端动态维护。Skill 本身 MIT 开源。

---

## 参考

- Cue 平台：https://cuecue.cn
- Playbook 页面：https://cuecue.cn/playbook
- API Key 管理：https://cuecue.cn/api-key?src=clawhub-legal-practice-cases
