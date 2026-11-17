---
name: bidhunter
slug: bidhunter
displayName: 标讯猎手 BidHunter
version: "2.9.1"
summary: 国央企招投标信息监控与研判：自动采集多平台公告，按资质规则判断可投性，生成研判简报并推送；支持分片全覆盖读标、评分点分值守恒校验、评分点台账（五态状态机+四条必报警）、正向覆盖矩阵（A/B/C 三档）、待补材料清单、零响应检测、合规红线扫描与报价闸门。本地运行，零云成本。
license: MIT-0
description: "国央企招投标信息监控与研判技能。自动采集多平台公告，按资质规则比对可投性（可投/不可投/需确认），生成带研判简报并多通道推送。v1.5 起新增：资质匹配度评分(0-100)、投标日历与开标倒计时、金额/地区/行业多维筛选、零代码规则编辑器、诊断中心、示例模式、集中FAQ、统一命令入口；v2.0 本地AI增强（招标文件AI速读+风险条款识别，零云成本）；v2.5 投标策略建议；v3.0 本地开放API+签名webhook；v3.5 合规红线引擎（31条法定废标红线本地扫描、交标前自查清单、多主体串标隔离，零API成本）；v2.7 报价闸门（品类清算价地板、规模换算线性、单位单价、毛利红线，任一道不过即禁止输出结论金额）。★v2.8 覆盖率重写：修复只读前9000字符导致200页标书95%未读的缺陷，改为结构化分片全覆盖并强制标注覆盖率；修复PDF/DOCX扫描静默失效（此前规则命中恒为0）；新增评分点逐项映射与分值守恒校验、待补材料清单（高危红标签字盖章页缺件）、零响应检测（空洞满足/待补占位/跨项目残留/数字型空洞），无AI key也能出完整简报。触发词：抓招投标、今日哪些能投、标讯监控、标书研判、招投标公告、央企招标、投标资质匹配、AI读标书、投标建议、这份标会不会被废、废标风险、交标前检查、合规红线扫描、多主体投标、会不会被认定串标、报价闸门、这个标报多少、报价复核、出价前检查、这个标值不值得投、报价会不会被废、待补材料清单、还差什么材料、零响应检测、评分点、评分表、评分办法、这个分怎么拿、漏项、丢分、扣分项、待补、待提供、准备什么材料、递交清单、应答表、偏离表、评分台账、评分项跟踪、覆盖矩阵、哪些评分项没写、哪条要求没响应。"
agent_created: true
---

# 标讯猎手 BidHunter

> 采集国央企/公共资源招投标公告 → 资质规则比对可投性 → 生成带研判简报 → 多通道推送 → （v1.5+）评分排序/日历提醒/多维筛选/零代码配规则 → （v2.0+）AI 速读标书与风险识别 → （v2.5+）投标策略建议 → （v3.5+）**交标前法定红线扫描与废标预警**。
> 自包含、已脱敏：不含任何私有主体、个人联系方式、公司档案。使用者按自己的营业执照与业务规则填充配置即可。

## 5 分钟跑通（新用户看这里）

两条路，挑一条：

### A. 先看效果——不用配任何东西

```bash
python3 bidhunter.py paste 你的招标文件.pdf
```

丢一份招标文件进来，直接出**废标风险报告**（31 条法定红线本地扫描）。
不需要 AI key、不需要采集源、离线可跑。

### B. 开始监控——三问生成配置

```bash
python3 bidhunter.py init
```

问三个问题（主体名称 / 主营什么 / 盯哪些地区），自动生成你的资质规则库，
再 `bash pipeline.sh` 开始采集。

> 行业**不设固定选项**——可以直接粘贴营业执照经营范围，自动拆成能力词。
> 想先看看效果不写盘：`python3 bidhunter.py init --preview`

## 卡住了？先跑诊断

任何异常先跑这一条，30 秒定位问题（E001~E005 + W001~W004，每条都带修复建议）：

```bash
python3 bidhunter.py doctor
```

> 最常见的失败原因是 **E002：规则库仍是示例占位符**。装上不等于能用——
> 一条命令解决：`python3 bidhunter.py init`（三问自动生成，约 1 分钟）。

## 版本能力一览

| 版本 | 主题 | 关键能力 |
|---|---|---|
| v1.1 | 准 | 边界感知智能匹配、规则健康检查、精华版报告 |
| v1.2 | 达 | 钉钉/企微/邮件多通道推送、配置向导、推送历史与告警 |
| **v1.5** | 易+功能 | 匹配度评分、投标日历、多维筛选、规则编辑器、诊断/示例/FAQ/统一入口 |
| **v2.0** | 智(本地AI) | 招标文件 AI 速读、排他/内定风险识别、业主品类画像（零云成本） |
| **v2.5** | 策 | 投标策略建议生成（仅供参考，不代填报价/资质） |
| **v3.0** | 开(本地) | 本地查询 API + 签名 webhook（云/SaaS 部分因成本约束未启用） |
| **v3.5** | 规 | 合规红线引擎：31 条法定废标红线本地扫描 + 交标前自查清单 + 多主体串标隔离（零 API 成本） |
| **v2.6** | 顺 | **上手转化**：`init` 三问生成配置（行业自由输入）、`paste` 零配置出废标风险报告、本地埋点、平台适配模板 |
| **v2.7** | **价** | **报价闸门**：出价前算式校验（品类清算价地板、规模换算线性、单位单价、毛利红线），任一道不过即禁止输出结论金额；缺参数只交框架与待补清单 |
| **v2.8** | **读全** | ★**覆盖率重写**：分片全覆盖（修掉只读前 9000 字符、200 页标书 95% 未读的缺陷）；PDF/DOCX 扫描静默失效已修（此前规则命中恒为 0）；**评分点逐项映射 + 分值守恒校验**；新增**待补材料清单**与**零响应检测**；无 AI key 也能出完整简报 |
| **v2.9** | **对表** | **评分点台账**（五态状态机 + 四条必报警：分值不守恒/同章节重复锚点/状态回退未确认/临截止仍缺项）；**正向覆盖矩阵**（资格·技术·商务逐条判 A 完全 / B 部分 / C 未覆盖，非布尔）；两表共用 `response_location` 字段；CSV 保底 / xlsx 有库才出 |

## ★ v2.8 为什么是这一版

2026-10-05 复盘发现三个叠加缺陷，**每一个都单独足以让读标结论不可信**：

| # | 缺陷 | 实测影响 | 修复 |
|---|---|---|---|
| 1 | `clause_extractor` / `risk_scanner` / `compliance_scanner` / `bid_advisor` 全部硬编码 `MAX_CHARS=9000` | 200~500 页标书（15~40 万字）**只喂入前 9000 字，约 4~6%**。且截断后照样输出完整 JSON —— **"读了一页就当读完"是最坏的失败模式** | `doc_parser.segment()` 按章节结构切片 + 逐片抽取 + 合并去重；输出强制带 `meta.coverage_pct` |
| 2 | `compliance_scanner` 导入 `doc_parser.parse_document`（该函数不存在），异常被裸 `except` 吞掉 | **喂任何 PDF/DOCX，规则扫描恒为 0 条命中**，却照样打印一份自信的人工清单。B02 实测 0 → 修复后 9 条，其中命中"缺漏项金额超 20% 视为非实质性响应"（该标废标的真实原因） | 改用真实 `parse()`，并把 backend 与 chars_read 写进输出，让静默失败可见 |
| 3 | `bid_advisor` 调 `extract(text)` 拿到的是**元组**，直接 `json.dumps` 传进 prompt | 策略建议基于一个字符串化的元组，**实际一直是坏的** | 接 `(clauses, meta)` 双返回；无 key 时降级出规则版简报而不是 exit 2 |

**修复后实测（B02 保洁真实招标文件 PDF）**：覆盖率 79.9% → **100%**；合规命中 0 → **9 条**；无 AI key 也能出评标办法/截止时间/预算/资格要求/未确认字段。

**新增两个纯规则（零 API）模块**：
- `gap scan` 待补材料清单：三态（HAVE / MISSING / CHECK）+ 高危红标（**缺件项落在签字盖章页 = 形式审查直接不通过**）+ 有效期提醒
- `gap zero` 零响应检测：空洞满足 / 借附件 / **待补占位** / 跨项目残留 / 承诺主体不明 / 数字型空洞（"不低于要求"却没数字）

**新增评分点分值守恒校验**：评分项合计 ≠ 100 时报警并要求解释差额——总分对不上通常意味着**漏抄了评分项**，这正是漏分的根因。


## 何时使用

- "抓一下招投标" / "今日哪些能投" / "重新分析一遍标讯"
- "AI 读一下这份标书" / "这份招标文件有什么风险" / "帮我出投标建议"
- "这份标会不会被废" / "交标前帮我过一遍" / "有没有废标风险" / "合规红线扫一下"
- "还差什么材料" / "待补材料清单" / "这些材料要不要盖章"（v2.8 `gap scan`）
- "帮我查查有没有漏项" / "有没有只写完全满足的" / "有没有上个项目的残留"（v2.8 `gap zero`）
- "评分表在哪" / "评分点有几个" / "这个分怎么拿"（v2.8 评分点逐项映射 + 分值守恒校验）
- "我们几家一起投 / 多主体投标会不会被认定串标"（v3.5 先查实施条例第34条）
- "这个标报多少" / "报价复核一下" / "出价前帮我过一遍" / "这个标值不值得投"（v2.7 走报价闸门）
- 需要判断公告可投性、归属投标主体、监控重点平台
- 搭建/优化招投标监控工作流

## 安装与初始化

1. 脚本已随 skill 就位（`~/.workbuddy/skills/bidhunter/scripts/`）。
2. 编辑 `qual_rules.json` 填入你的投标主体与资质能力词：
   - 零代码：运行 `python3 bidhunter.py rules edit` → 浏览器图形化编辑，内置「能源/建筑/IT/市政」行业模板可一键预填
   - 或复制 `scripts/samples/demo_rules.json` 改
   - 校验：`python3 qual_check.py --validate-rules qual_rules.json`
3. （可选）配置推送：`python3 config_wizard.py`（钉钉/企微/邮件）
4. （可选）配置 AI：`~/.config/bidhunter/ai.json` 写入 `{"api_key":"你的MiniMaxKey"}`（v2.0+ 用，仅消耗你的 API 余额，零云成本）。AI 速读 PDF/Word 建议先 `pip install -r requirements.txt`（PyPDF2/python-docx）；未装则自动降级为正则抽取。

> 先看效果再配：直接 `python3 bidhunter.py demo` 跑内置示例。

## 统一命令入口（v1.5 · A9，零命令行门槛）

```bash
python3 bidhunter.py run [--fresh] [--summary] [--calendar]   # 采集+比对+报告(+推送)
python3 bidhunter.py status                                    # 今日状态
python3 bidhunter.py doctor                                    # 一键诊断
python3 bidhunter.py demo                                      # 示例效果
python3 bidhunter.py calendar [--days 7]                        # 投标日历
python3 bidhunter.py faq [关键词]                               # 查常见问题
python3 bidhunter.py rules edit [--port 8080]                  # 图形化配规则
python3 bidhunter.py ai read <标书.pdf>                        # v2.0 AI 速读
python3 bidhunter.py ai advise <标书.pdf>                      # v2.5 投标建议
python3 bidhunter.py api serve [--port 8765]                   # v3.0 本地API
python3 bidhunter.py compliance scan <标书> [--mode tender|bid] # v3.5 合规红线扫描
python3 bidhunter.py compliance checklist                      # v3.5 交标前自查清单
python3 bidhunter.py gap scan <招标文件>                          # v2.8 待补材料清单
python3 bidhunter.py gap zero <投标文件草稿>                      # v2.8 零响应检测
python3 bidhunter.py quote params [--show]                     # v2.7 报价参数库（首次填一次）
python3 bidhunter.py quote check --help                        # v2.7 报价闸门（不过禁止出金额）
python3 bidhunter.py gap scan <招标文件>                        # v2.8 待补材料清单（零 API）
python3 bidhunter.py gap zero <投标文件草稿> [--our-project 名称] # v2.8 零响应检测（零 API）
```

## 待补材料清单与零响应检测（v2.8）★

读完标只是第一步，**最容易丢分的是"以为写完了"**。这两条命令专治这件事，纯规则、零 API 成本。

```bash
# 交标前还差什么：资格要求逐条三态判定 + 高危红标
python3 bidhunter.py gap scan 招标文件.pdf
python3 bidhunter.py gap scan 招标文件.pdf --json

# 草稿写完后查零响应：空洞满足 / 借附件 / 待补占位 / 跨项目残留 / 数字型空洞
python3 bidhunter.py gap zero 投标文件草稿.docx
python3 bidhunter.py gap zero 草稿.docx --our-project "XX项目" --other-projects 上一标的项目名
```

**`gap scan` 输出**
```
共 3 项：缺 1 · 待确认 2 · 高风险 1 · 带有效期 2

🔴 [MISSING] 3.3 业绩证明文件（资格评审第 4 项）★须按规定格式提交业绩表…
     ⚠️ 出现在签字盖章页——缺件即形式审查不通过
     标记：需盖章
```

三态含义：
- `HAVE` — 规则库已有证据线索
- `MISSING` — **原文写"必须/应/须"但未找到我方证据 → 最高优先级**
- `CHECK` — 表述含糊，人工确认

**高危判定**：缺件项若涉及合同/业绩/资质/承诺函/人员简历/盖章 → 🔴。因为这些要进签字盖章页，**占位符上会 = 形式审查直接不通过，不用到评标**。

**`gap zero` 检出的六类零响应**
| 类型 | 危险度 | 说明 |
|---|---|---|
| **待补占位**（待补/待提供/【 】/＿＿＿） | 致命 | 评标时等同未提供 |
| **跨项目残留**（别的项目名/甲方名） | 致命 | 复制粘贴未替换 |
| 空洞满足（完全满足/无偏离） | 风险 | 须紧跟具体做法或参数 |
| 借附件（详见附件） | 风险 | 附件里必须真有内容 |
| 数字型空洞（不低于要求/优于标准） | 风险 | 没给数字 = 按无偏离计分 = 零 |
| 承诺主体不明（我司将…） | 提示 | 须落到具体章节与具体承诺 |


## 评分点台账与覆盖矩阵（v2.9）★

`gap` 回答"我还差什么"，**`score` 回答"分丢在哪"**。两张表在交标前互为补充：台账管评分项有没有写，覆盖矩阵管每条要求有没有答。纯规则、零 API 成本。

```bash
# B1 评分点台账：五态跟踪 + 四条必报警
python3 bidhunter.py score ledger 招标文件.pdf
python3 bidhunter.py score ledger 招标文件.pdf --csv 台账.csv --xlsx 台账.xlsx
python3 bidhunter.py score ledger 招标文件.pdf --deadline 2026-10-20

# B2 正向覆盖矩阵：逐条要求判 A/B/C（需同时给投标文件草稿）
python3 bidhunter.py score coverage 招标文件.pdf --response 投标文件草稿.docx

# 两张表一起出 + 机器可读
python3 bidhunter.py score both 招标文件.pdf --response 草稿.docx --json

# 内置自测（11 用例：四个反例 + 三个 L3 回归 + 报警/降级）
python3 bidhunter.py score selftest
```

> ⚠️ **B1 必须配 `--response`**：不给投标文件草稿时，台账只会判「未开始」——
> 定位到评分表只说明这项存在，不代表我方已写。这是 v2.9 修掉的 L1 缺陷
> （此前不给草稿也报"全部已完成"）。
> 用 `--prev-ledger 上版.json` 可激活 A3 状态回退检测。

**B1 五态**（每个评分项在台账里的位置）

| 状态 | 含义 |
|---|---|
| ⚪ 未开始 | 评分项已登记，但没定位到响应内容 |
| 🔵 已写 | 定位到响应位置且有内容 |
| 🔴 材料缺 | 标准要求的材料在材料库零命中 |
| 🟡 待核 | 锚点与材料都到位，等三查通过 |
| ✅ 已完成 | 三查通过（分值归位/锚点唯一/引用可达） |

**B1 四条必报警**（不报警即算实现错误）
| 编号 | 触发条件 |
|---|---|
| A1 | 评分项分值合计 ≠ 声明总分（缺省 100）——**差额必须解释，不得直接采信** |
| A2 | 同一评分项在**同一文件同一章节**出现 ≥2 个锚点 |
| A3 | 状态回退未经人工确认（需显式 `--confirm-regress`） |
| A4 | 距投标截止 ≤3 天仍有「未开始」项 |

**B2 覆盖三档**（非布尔——中间那档才是有用的信息）

| 档 | 判定 |
|---|---|
| ✅ A 完全覆盖 | 定位到响应 ＋ 硬要素（数字/规格/名单/年限）齐全 ＋ 有承诺动词 |
| 🟡 B 部分覆盖 | 有定位但硬要素缺失，**或**仅空声明（"完全满足"无支撑） |
| 🔴 C 未覆盖 | 响应文件中定位不到对应内容 |

**B2 关键用法**：`--response` **必须给投标文件草稿**。不给时全部降为 C 并提示"未提供草稿，无法判定（不猜）"——因为拿招标文件自己的措辞去比对毫无意义，硬要素天然"齐全"，会刷出假的 A。

> 三条铁律同 v2.8：**不猜不编**（分值为空留空，不填 0）、**指不到页码标"待人工核实"**、**检测器不是裁判**（A/B/C 是规则判断，人工结论仍归人）。
> `openpyxl` 非必需依赖：缺失时自动降级 CSV 并打印原因，CSV 是保底输出。


## 标准流程

### 1. 采集 + 比对 + 报告
```bash
bash pipeline.sh                  # 全流程（缓存优先）
bash pipeline.sh --fresh         # 强制重采当天
bash pipeline.sh --calendar      # 生成后额外打印投标日历
# A4 多维筛选（后过滤）
bash pipeline.sh --budget-min 500000 --budget-max 20000000 --region 天津 --industry 智能设备
```
报告：`bid_reports/report_YYYY-MM-DD.txt`（文字，适配 IM）、`report_YYYY-MM-DD.html`（浏览器）。

### 2. 多通道推送（v1.2）
首次 `python3 config_wizard.py` 配置；`pipeline.sh` 生成报告后自动推送。`push_manager.py` 支持 `test/history/stats/health-check/retry-failed`。关闭用 `pipeline.sh --no-push`。

### 3. v1.5 新能力
- **匹配度评分（A1）**：可投标按 0-100 分排序，等级 强烈推荐/建议跟/可投一般。报告直接显示分数。
- **投标日历（A2）**：`python3 calendar.py <qual文件> --days 30` 看开标/截止日；`--remind` 对临近截止（默认48h）自动推送提醒。
- **多维筛选（A4）**：规则库设 `region_priority.high` / `industry_categories`+`industry_priority` / `budget_priority`，运行时用 `--region/--industry/--budget-min/--budget-max` 过滤。
- **规则编辑器（可视化）**：`python3 bidhunter.py rules edit` → http://localhost:8080，选行业模板、填能力词、实时试标、保存。
- **诊断中心（A6）**：`python3 doctor.py` 输出带错误码（E001~E005 / W001~W004）的诊断与下一步。
- **示例模式（A7）**：`python3 demo.py [--summary] [--calendar]` 用内置示例看完整效果。
- **集中 FAQ（A8）**：`python3 faq.py <关键词>` 检索常见问题。
- **平台扩展（A5）**：内置 3 适配器（cnooc/cebpubservice/ccgp）+ 自定义数据源 `sources.json`（json/rss/html 三种模式，零代码接入任意公开平台）。

### 4. v2.0 本地 AI 增强（零云成本）
```bash
python3 bidhunter.py ai read 招标文件.pdf     # 解析+结构化抽取+风险扫描
python3 bidhunter.py ai read 招标文件.pdf --llm   # 加 LLM 风险扫描
python3 ai/analytics.py --days 30              # 本地业主/品类画像
```
调用你自己的 MiniMax API（仅耗余额），不外传数据到任何 BidHunter 云端（我们无云端）。

### 5. v2.5 投标策略建议
```bash
python3 bidhunter.py ai advise 招标文件.pdf    # 资质自检+评分得分点+报价策略+时间节点
```
**合规边界**：只建议不代劳——不自动填报价、不伪造资质、不写技术方案。所有建议标注"仅供参考，人工确认"。

### 6. v3.0 本地开放能力（零云成本子集）
```bash
python3 api_server.py --port 8765             # 本地查询 API（127.0.0.1，无云端）
python3 webhook_publish.py qual_xxx.jsonl     # 把标讯签名推送到你自己的系统
```
> v3.0 原规划的云/SaaS 部分（多租户、第三方插件市场、数据市场、Salesforce/金蝶连接器）因涉及付费云基础设施，按成本约束未启用。本机 API + 签名 webhook 是其零成本替代。

### 7. v3.5 合规红线引擎（零 API 成本）★

找到标只是第一步，**交了标不被废**才是最后一公里。v3.5 把《招标投标法》《实施条例》《评标委员会和评标方法暂行规定》（12号令）蒸馏成机器可读的 **31 条法定红线**，本地扫描，**不调用任何 LLM，零 API 成本**。

```bash
# 扫招标文件：找出文件里埋了哪些"雷"（实质性要求、违规条款、致命形式要件）
python3 bidhunter.py compliance scan 招标文件.pdf --mode tender

# 扫投标文件：交标前最后一检，找自己文件里的致命项
python3 bidhunter.py compliance scan 投标文件.pdf --mode bid

# 交标前自查清单（31 条，逐条打勾）
python3 bidhunter.py compliance checklist

# 输出 JSON（供其他系统消费）/ 追加 LLM 深度扫描（耗 MiniMax 余额）
python3 bidhunter.py compliance scan 招标文件.pdf --json
python3 bidhunter.py compliance scan 招标文件.pdf --llm
```

**红线分类（31 条）**

| 类 | 名称 | 条数 | 发生阶段 | 决定方 | 后果 |
|---|---|---|---|---|---|
| A | 拒收/不予受理 | 4 | 交标现场 | 招标人/代理机构 | 当场拒收，进不了评标 |
| B | 否决投标 | 14 | 评标阶段 | 评标委员会 | 该份投标出局 |
| C | 投标无效 | 4 | 全程 | 无需认定 | 相关投标**均**无效 |
| D | 反向保护条款（盾牌） | 3 | 维权 | 投标人主张 | 可据此质疑/投诉 |
| E | 多主体串标隔离 | 6 | 评审/调查 | 评标委员会/行政监督 | 视为串通，中标无效 |

**三条最值钱的认知**（其余详见 `compliance/redlines.json`）：

1. **多主体投同一标段，先查《实施条例》第34条**（C02）：单位负责人为同一人、或存在控股/管理关系的不同单位**不得**参加同一标段投标，违反则相关投标均无效。这是**资格硬禁止**，无需任何串通证据，且优先于一切串标推定。
2. **细微偏差不影响投标有效性**（D02，12号令第26条）：个别漏项只会被要求补正，招标文件没规定量化标准的**不得扣分**。与"重大偏差=否决"严格区分——这条能救命。
3. **标底不能作为否决依据**（D01，实施条例第50条）：招标文件若写"报价超出标底±X%作废标处理"，该条款**本身违法**，可据此质疑投诉。扫描器会自动识别此类违规条款并标为"盾牌"。

**合规边界（与 v2.5 一致）**：
- ✅ 做：法条索引、风险提示、自查清单、违规条款识别
- ❌ 不做：法律意见、胜诉承诺、代填报价、伪造资质
- ⚠️ 扫描结果**不构成法律意见**，最终判定以招标文件、评标委员会认定及有权机关解释为准。法规未给出量化标准的（如"低于成本"），本引擎**不设阈值**

**深度审查联动**：本地扫描是"浅层快速筛"，需要逐条法理分析和举证策略时，联动蒸馏姊妹 skill（需另行安装）：`bid-rejection-guard`（25条红线深度审查）、`bid-price-redline`（低于成本举证自救）、`multi-entity-bid-isolation`（多主体串标隔离 10 条清单）。

## 报价闸门（v2.7）—— 出价前必须过的四道算式卡

找到标、保住标之后，**最贵的教训在报价上**：沿用旧价没换算规模、单价算错量级、毛利倒挂——错的数字会被下游当成可信基数一路沿用。

```bash
# 第一次填一次参数库（最低工资 / 毛利红线 / 容差），只写本机，不上传
python3 bidhunter.py quote params
python3 bidhunter.py quote params --show      # 查看 + 过期提醒（默认 90 天）

# 跑闸门：给什么算什么，缺什么列什么
python3 bidhunter.py quote check --labor --heads 7 --months 12 --cost 200000 --quote 260000
python3 bidhunter.py quote check --prior-amount 600000 --prior-scale 300 --new-scale 60 --quote 120000
python3 bidhunter.py quote check --help
python3 bidhunter.py quote --selftest
```

**四道算式卡**（任一道不过 → **禁止输出结论金额**）：

| 卡 | 名称 | 判据 |
|---|---|---|
| C-1 | 品类清算价筛查 | 对手地板价 ≈ 当地月最低工资 × 人数 × 月数 × (1.10~1.25)。我方合规成本 ≥ 地板价下限 → 判「结构性陪跑」，直接不投 |
| C2 | 规模换算（线性校验） | 新金额 ≈ 旧金额 × 新规模 ÷ 旧规模，偏差超容差即卡住——防的就是沿用旧价没换算 |
| C3 | 单位单价校验 | 单价 = 总价 ÷ 数量，越出品类单价带即卡住 |
| M1 | 毛利红线 | 毛利率 = (总价 − 成本) ÷ 总价，低于红线不得出价 |

外加 5 项**算式扫不出来、必须人工确认**的核对卡：条款逐字读完、市场价带反推、服务模式逐项加减、敏感性分析覆盖全部变量、成本口径与服务口径配套。

**闸门铁律**：
- 结论只有三种：`已过闸门` / `禁止出价` / `参数待补`
- **只有「已过闸门」才回显金额**；另外两种只给"卡在哪 + 缺什么参数"
- 缺参数时**只允许交成本模型框架与参数待补清单，不得交带金额的报价函**
- 参数库在 `~/.config/bidhunter/quote_params.json`（权限 600）；最低工资随年度调整，超期会自动提醒

**边界**：闸门只做算式校验与清单提示，**不产生报价意见、不替代人工判断**，也不联网取数。

## 系统组件（位于 `scripts/`）

| 文件 | 作用 | 版本 |
|---|---|---|
| `bid_monitor.sh` | 采集（含自定义数据源加载） | base+A5 |
| `qual_rules.json` | 资质规则库（**必须自定义**） | base+A4字段 |
| `qual_check.py` | 比对引擎 + A1 评分/预算/行业提取 | v1.5 |
| `report_text.py` / `report_html.py` | 文字/HTML 简报（含评分展示） | v1.5 |
| `push_manager.py` / `config_wizard.py` | 推送+配置向导 | v1.2 |
| `calendar.py` | A2 投标日历/倒计时提醒 | v1.5 |
| `filter_multi.py` | A4 多维筛选 | v1.5 |
| `rule_editor.py` | 零代码规则编辑器（HTTP） | v1.5 |
| `doctor.py` | A6 诊断中心 | v1.5 |
| `demo.py` + `samples/` | A7 示例模式 | v1.5 |
| `faq.py` + `docs/FAQ.md` | A8 集中 FAQ | v1.5 |
| `bidhunter.py` | A9 统一命令入口 | v1.5 |
| `custom_source.py` + `sources.example.json` | A5 自定义数据源 | v1.5 |
| `ai/minimax_client.py` | MiniMax 客户端（urllib，零依赖） | v2.0 |
| `ai/doc_parser.py` | B1 标书解析 + **v2.8 结构感知分片 segment() + 覆盖率统计** | v2.0/v2.8 |
| `ai/clause_extractor.py` | B1 条款抽取（**v2.8 分片全覆盖 + 规则引擎兜底 + 评分点逐项映射 + 分值守恒校验**） | v2.0/v2.8 |
| `ai/risk_scanner.py` | B2 风险条款识别 | v2.0 |
| `ai/doc_reader.py` | B1 总装：AI 速读 | v2.0 |
| `ai/analytics.py` | A3 业主/品类画像 | v2.0 |
| `ai/bid_advisor.py` | v2.5 投标策略建议（**v2.8 修 tuple 传参 bug + 无 key 降级**） | v2.5/v2.8 |
| `api_server.py` / `webhook_publish.py` | v3.0 本地开放能力 | v3.0 |
| `compliance/redlines.json` | C1 法定红线规则库（31条：A4/B14/C4/D3/E6） | v3.5 |
| `compliance/compliance_scanner.py` | C1 合规红线扫描引擎（**v2.8 修 PDF/DOCX 静默失效 + LLM 分片**） | v3.5/v2.8 |
| `quote_gate.py` | v2.7 报价闸门引擎（四道算式卡 + 5 项人工核对卡，零依赖零联网） | v2.7 |
| `quote/gate.json` | v2.7 闸门规则与阈值（阈值数据化，改阈值不必改代码） | v2.7 |
| `material_gap.py` | **v2.8 待补材料清单（G1）+ 零响应检测（G2），纯规则零 API** | v2.8 |

## 已知坑点

- **IM 发文件失败**：个人 IM 不支持发文件，只能文字。可视化网页供电脑浏览器看。
- **list API 无截止日**：部分平台返回仅 id/title，截止日需 detail 接口（常 401），故只采集当天近似；日历日期从标题解析，未含明确日期的标归入"待核实截止日"。
- **IP 限流**：连发约 20 次后可能 401/403，翻页 sleep 2s + 失败重试冷却 10s。
- **匹配边界**：边界感知规则会挡掉词中误匹配（如"电气设备"里的"电气"因前有 CJK 被挡属正常防误匹配）。能力词尽量让其出现在词首边界可稳定命中。
- **AI 依赖**：v2.0/v2.5 需配置 MiniMax API Key；未配置时 AI 功能自动跳过。**v2.8 起不配置也能出完整简报**（规则引擎兜底），只损失策略建议的文字部分。
- **标书解析**：最佳效果需 `pip install PyPDF2 python-docx`（可选）；未装时 PDF 走正则降级、DOCX 可能解析不全。
- **纯扫描件无文字层**：v2.8 起会明确报错并提示需 OCR，**不再静默降级为"读了但其实没读"**。
- **覆盖率标注**：v2.8 起所有读标输出都带 `coverage_pct`。**若显示覆盖率明显低于 100%（例如文件解析后只剩零散片段），结论不可信，须换解析后端或先 OCR。**

## 反馈（零成本，30 秒）

| 方式 | 怎么用 | 说明 |
|---|---|---|
| **快速反馈** | `python3 bidhunter.py feedback` | 交互式问三句 → 自动格式化 → 写进剪贴板 → 打开平台评论页，粘贴即可 |
| SkillHub 评论区 | <https://skillhub.cn/skills/user_7a89592b/bidhunter> | 公开讨论，作者可见 |
| ClawHub 评论区 | <https://clawhub.ai/419597334-sudo/bidhunter> | 公开讨论，作者可见 |

> 反馈模块**不上传任何数据**：全程只在本机生成文本、写剪贴板、唤起你的浏览器，无任何后端与网络请求。

## 参考文档

- `references/platforms.md`：支持平台清单、自定义数据源指南
- `references/filter_rules.md`：筛选规则结构
- `references/field_standard.md`：标讯字段标准
- `docs/FAQ.md`：常见问题（`faq.py` 检索）
- `samples/`：示例规则与模板（demo / 行业模板）
