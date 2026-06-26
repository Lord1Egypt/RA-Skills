# cfc-disclosure-monitor — 消费金融信披采集 Skill

> **三阶段贯通架构 v4.4 — 2026-04-17**
>
> Phase 1 → Phase 2 → Phase 3 自动流水线，数据从采集到知识图谱不落地二次处理。

---

## 核心概念

```
官网URL
   ↓
[Phase 1] collect.py          采集公告列表 + 下载PDF/附件
   ↓
cfc_raw_data/{公司}/
  ├── announcements.json      原始公告列表 + 正文 + PDF路径
  └── attachments/            PDF文件
   ↓
[Phase 2] phase2_parse.py     解析PDF → 提取合作机构名单
   ↓
cfc_raw_data/{公司}_合作机构_{类型}{日期}.json
   ↓
[Phase 3] phase3_ontology.py   实体入库 → 知识图谱
   ↓
memory/ontology/graph.jsonl    关系型知识图谱
```

---

## 一、架构文件

```
cfc-disclosure-monitor/
├── SKILL.md              ← 本文件（v4.0）
├── companies.json        ← 唯一配置源（30家 URL + 采集方法）
├── collect.py            ← Phase 1 入口：统一调度 collectors.COLLECTORS
├── collectors.py         ← 42个采集方法（v1 函数，list[dict]）
├── collectors_v2.py      ← 5个采集方法（v2 类，BaseCollector）
│                          ← 导入时自动同步到 collectors.COLLECTORS
├── phase1_base.py        ← Announcement + BaseCollector + Builder
│                          ← 统一接口：__call__ 返回 list[dict]
├── core.py               ← 日期/分类/文本提取引擎
├── phase2_parse.py       ← Phase 2：PDF解析 + 合作机构提取
├── phase3_ontology.py     ← Phase 3：知识图谱写入
├── pipeline.py           ← 三阶段统一编排器
└── parsed/               ← Phase 2 中间产物
```

### 架构原则（v1 + v2 并存）

| 层级 | 文件 | 类型 | 返回值 |
|------|------|------|--------|
| v1 | `collectors.py` | 同步/异步函数 | `list[dict]` |
| v2 | `collectors_v2.py` | 异步类（继承 `BaseCollector`） | `list[dict]`（通过 `__call__`） |

两套统一注册到 `collectors.COLLECTORS`，`collect.py` 无需修改。

**新增 v2 collector 步骤：**
1. `collectors_v2.py` 中定义继承 `BaseCollector` 的类
2. `@collector("方法名")` 注册（自动进 `collectors.COLLECTORS`）
3. `companies.json` 中对应公司 `method` 改为 v2 方法名

---

## 二、Pipeline 编排器

**一键贯通运行（推荐）：**

```bash
cd ~/.openclaw/workspace/skills/cfc-disclosure-monitor/

# 全量：P1 → P2 → P3 全部跑完
python3 pipeline.py

# 从指定阶段开始
python3 pipeline.py --phase 2              # 从 P2 开始（全量）
python3 pipeline.py --phase 3 --company 中邮消费金融  # 只 P3 单公司

# 仅查看已采集的公司
python3 pipeline.py --list
```

**分阶段独立运行：**

```bash
# Phase 1：采集列表 + PDF
python3 collect.py --date 2026-04-15
python3 collect.py --company "中邮消费金融" --no-detail  # 仅列表验证

# Phase 2：解析 PDF，提取合作机构（不改动 announcements.json）
python3 phase2_parse.py                    # 全量
python3 phase2_parse.py 中邮消费金融       # 单公司

# Phase 3：写入知识图谱
python3 phase3_ontology.py                 # 全量
python3 phase3_ontology.py 中邮消费金融    # 单公司
```

---

## 三、Phase 1 — 公告列表采集

**目标：** 采集30家消金公司官网所有披露公告，保存正文和附件。

### 输出结构

```
cfc_raw_data/{公司名}/                ← 按公司分目录
├── announcements.json                 ← 公告列表（含正文摘要）
│   [{
│     "title": "中邮消费金融有限公司催收合作机构信息公示",
│     "date": "2026-02-28",
│     "url": "https://www.youcash.com/xxgg/77802.html",
│     "category": "合作机构",
│     "text": "尊敬的客户：...",      ← HTML正文
│     "_content_type": "html|vue|pdf|image",
│     "_attachments": [{"filename":"xxx.pdf","path":"...","type":"pdf"}]
│   }]
└── attachments/                       ← Phase 2 需要的原始文件
    └── *.pdf
```

### 采集方法映射（companies.json）

| 架构 | 方法 | 代表公司 |
|------|------|----------|
| 静态列表 | `html_dom` | 蚂蚁、中信、宁银（老）、河北 |
| JSON API（v2） | `cfcbnb_v2` | **宁银**（Vue data.json，47条） |
| 详情遍历（v2） | `mengshang_v2` | **蒙商**（HTML详情，86家） |
| layui分页 | `zhongyin_layui` | 中银（13页） |
| Vue SPA | `vue_pagination` | 招联 |
| AJAX翻页 | `multi_page` | 湖北（3 Tab） |
| 首页滚动 | `homepage_scroll` | 平安、金美信 |
| 双栏翻页 | `jinshang_two_col` | 晋商 |
| Vue Tab | `suyinkaiji_vue` | 苏银凯基 |
| CDP截图 | `cdp3.py` | 长银五八 |

---

## 四、Phase 2 — PDF解析与实体提取

**目标：** 扫描 announcements.json → 下载PDF → pdftotext提取 → 保存结构化合作机构名单。

### 支持的披露类型

| 披露类型 | 识别关键词 | 输出文件 |
|----------|-----------|---------|
| 催收合作机构 | `催收` | `{公司}_合作机构_催收合作机构_{日期}.json` |
| 增信服务机构 | `增信`、`担保` | `{公司}_合作机构_互联网贷款增信服务机构_{日期}.json` |
| 平台运营机构 | `平台`、`运营机构` | `{公司}_合作机构_互联网贷款平台运营机构_{日期}.json` |
| 关联交易 | `关联交易` | 同上模式 |
| 不良资产 | `不良资产` | 同上模式 |

### 输出 JSON 格式

```json
[
  {"name": "和君纵达数据科技股份有限公司", "phone": "18855123966"},
  {"name": "众焱普惠科技有限公司", "phone": "028-85567577"}
]
```

### 提取规则

- 公司名识别：`{4-20汉字}(有限公司|股份有限公司|有限责任公司|集团|事务所)`
- 电话识别：`0\d{2,3}[-\s]\d{7,8}` 或 `1[3-9]\d{9}` 或 `95\d{3,5}` 或 `400\d{7}`
- 自动修复：换行断裂的公司名（拼接相邻行）

---

## 五、Phase 3 — 知识图谱写入

**目标：** 将结构化数据写入 `memory/ontology/graph.jsonl`，建立跨公司关联。

### 实体类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `Company` | 合作机构/公司 | 蚂蚁智信、和君纵达 |
| `DisclosureList` | 披露清单 | 中邮催收合作机构2026(101家) |
| `DisclosureDocument` | 具体披露文档 | 中邮消金催收公示PDF |
| `CooperationRelation` | 合作关系（通过 relation 表达） | |

### Relation 类型

| Relation | 从 | 到 | 说明 |
|----------|----|----|------|
| `cooperates_with` | Company | Company(消金) | 合作机构 ↔ 消金公司 |
| `publishes_disclosure` | Company(消金) | DisclosureList | 消金发布披露清单 |
| `includes_company` | DisclosureList | Company | 清单包含合作机构 |
| `disclosed_by` | DisclosureDocument | Company(消金) | 文档由消金发布 |
| `appears_in_document` | Company | DisclosureDocument | 合作机构出现在文档正文 |

### 查询示例（grep graph.jsonl）

```bash
# 查哪家消金跟河北银海有合作
grep "河北银海" memory/ontology/graph.jsonl

# 查中邮消金所有合作机构
grep "co_zhongyou" memory/ontology/graph.jsonl

# 查所有增信服务机构
grep "GuaranteeAgency" memory/ontology/graph.jsonl
```

---

## 六、Ontology Schema 扩展

已为消金监控扩展 ontology schema：

```yaml
types:
  Company:
    required: [name]
    properties:
      name: string
      company_type: string   # LawFirm|TechCompany|CollectionBPO|GuaranteeCompany...
      disclosure_type: string
      source_company: string
      phone: string

  DisclosureList:
    required: [name, company, disclosure_type, count, date]
    properties:
      name: string
      company: string
      disclosure_type: string
      count: integer
      date: string
      source_url: string

  DisclosureDocument:
    required: [title, date, source_company]
    properties:
      title: string
      date: string
      url: string
      category: string
      disclosure_type: string
      source_company: string
```

---

## 七、使用示例

### 场景：查询"哪家消金跟河北银海融资担保有合作"

**旧方式（手动搜索）：**
1. 回忆之前的分析文档
2. 搜索关键词
3. 翻聊天记录
4. 无法确认 → 返回"没找到"

**新方式（ontology查询）：**
```bash
grep "河北银海" memory/ontology/graph.jsonl
```
→ 立即得到：co_zhongyou ← cooperates_with ← co_yinhai_guarantee

### 场景：添加新公司信披采集

1. 在 `companies.json` 添加公司 URL 和方法
2. `python3 pipeline.py --phase 1 --company "XX消费金融"`
3. `python3 pipeline.py --phase 2 --company "XX消费金融"`
4. `python3 pipeline.py --phase 3 --company "XX消费金融"`
5. 自动入库 → 可直接查询

### 场景：批量补充历史 PDF

```bash
# 假设已采集 announcements.json，但 PDF 未下载
python3 phase2_parse.py    # 自动扫描所有 PDF 链接并下载
python3 phase3_ontology.py # 自动提取并写入 ontology
```

---

## 八、目录结构总览

```
~/.openclaw/workspace/
├── cfc_raw_data/                         ← 原始数据湖
│   ├── 中邮消费金融/
│   │   ├── announcements.json            ← Phase 1 产出
│   │   ├── 中邮消费金融_合作机构_催收合作机构_2026-02-28.json  ← Phase 2 产出
│   │   ├── 中邮消费金融_合作机构_互联网贷款增信服务机构_2026-03-31.json
│   │   └── attachments/                 ← PDF/图片
│   ├── 兴业消费金融/
│   │   └── ...
│   └── ...
├── memory/ontology/
│   └── graph.jsonl                       ← Phase 3 产出（全公司知识图谱）
└── skills/cfc-disclosure-monitor/
    ├── pipeline.py                       ← 统一编排器
    ├── phase2_parse.py                   ← Phase 2
    ├── phase3_ontology.py                ← Phase 3
    └── ...
```

---

## 九、更新日志

| 日期 | 版本 | 内容 |
|------|------|------|
| 2026-04-15 | v4.0 | 深度重构：phase1_base.py去除重复方法+死代码（325行，原474行）；collectors.py末尾死函数collect_mengshang已删除（2240行，原2253行）；v1+v2统一COLLECTORS注册表；Announcement dict兼容层保持；cfcbnb_v2/mengshang_v2验证通过（47条/宁银） |
| 2026-04-15 | v3.0 | 三阶段贯通：Phase 1→2→3 pipeline，新增phase2_parse.py/phase3_ontology.py/pipeline.py， ontology graph.jsonl 为统一出口 |
| 2026-04-15 | v2.0 | Phase 1+2 合并，详情页同步获取，PDF探测改进 |
| 2026-04-05 | v1.0 | 初版，30家列表确认，html_dom方法建立 |
