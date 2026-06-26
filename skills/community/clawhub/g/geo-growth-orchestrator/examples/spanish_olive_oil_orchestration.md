# 西班牙橄榄油 GEO 编排示例

## 用户输入

```json
{
  "brand_name": "西班牙橄榄油推广项目",
  "category": "进口食品 / 橄榄油",
  "target_market": "中国家庭消费、礼品消费、餐饮采购",
  "target_keywords": [
    "西班牙橄榄油推荐",
    "橄榄油怎么选",
    "西班牙橄榄油和意大利橄榄油哪个好",
    "适合中餐的橄榄油",
    "进口橄榄油购买渠道",
    "小红书橄榄油种草"
  ],
  "target_models": [
    "DeepSeek",
    "Doubao"
  ],
  "target_platforms": [
    "知乎",
    "今日头条",
    "小红书",
    "抖音"
  ],
  "campaign_goal": "提升西班牙橄榄油在 AI 搜索和中文内容平台中的品类认知、购买决策辅助和本地化消费场景覆盖"
}
```

## 行业判断

- 行业：消费品 / 食品 / 进口品类。
- 首选平台：知乎、今日头条、小红书类内容。
- 小红书与抖音：当前没有专用相邻 Skill，标记为 `manual` / `future_skill`，由 Orchestrator 生成选题、脚本方向和人工发布清单。
- 默认跳过：CSDN、掘金，除非后续加入供应链数字化、食品溯源系统或跨境电商技术内容。

## 应调用哪些相邻 Skill

| 阶段 | Skill | Relative Path | 目的 | 状态示例 |
|---|---|---|---|---|
| Stage 1 | Brand Knowledge Base Builder | `../Knowledge-Base-Builder/brand-knowledge-base-builder` | 建立西班牙橄榄油品类与品牌资料母库 | planned |
| Stage 2 | DeepSeek GEO Audit Skill | `../deepseek-geo-audit-skill` | 检测 DeepSeek 对品类、产地、渠道和中餐场景的回答 | planned |
| Stage 2 | Doubao GEO Audit Skill | `../geo-analysis-doubao` | 检测 Doubao 对中文消费场景的理解 | planned |
| Stage 5 | AI GEO Content Generator | `../AI-geo-content-generator` | 生成 FAQ、选购指南、问答基础稿和句库 | planned |
| Stage 6 | Zhihu GEO Draft Assistant | `../zhihu-geo-draft-assistant` | 生成知乎问答、对比文、选购指南 | planned |
| Stage 6 | Toutiao GEO Draft Assistant | `../toutiao-geo-draft-assistant` | 生成头条科普文和家庭消费内容 | planned |
| Stage 6 | 小红书 / 抖音 | manual / future_skill | 生成种草笔记和短视频脚本方向 | manual |

## 每个阶段的输入输出

| Stage | 输入 | 输出 | 验收标准 |
|---|---|---|---|
| Stage 0 Intake | 用户输入、关键词、平台、模型 | 行业判断、目标市场、路由初选 | 品类、市场、平台、模型明确 |
| Stage 1 品牌母库 | 品类资料、产地资料、渠道资料、合规边界 | `brand_knowledge_base.json` | 不编造产地、价格、渠道和认证 |
| Stage 2 双模型评估 | 品牌母库、探针问题 | 原始回答、模型评分、双模型对比 | 覆盖推荐、对比、选购、本地化场景 |
| Stage 3 Gap Matrix | 双模型结果 | `geo_gap_matrix.json` | 每个盲区有商业影响 |
| Stage 4 Content Task Plan | Gap Matrix、平台规则 | `content_task_plan.json` | 每个任务有优先级和发布前确认项 |
| Stage 5 通用内容资产 | 品牌母库、任务计划 | FAQ、问答基础稿、句库 | 对应盲区，人工审核 |
| Stage 6 平台草稿 | 通用资产、平台规则 | 知乎/头条草稿，小红书/抖音人工任务 | 平台适配清楚 |
| Stage 7 客户交付包 | 全部输出 | 客户报告、内部报告、发布计划 | 当前对话输出完整报告 |
| Stage 8 复测计划 | 基线评估、发布计划 | `retest_plan.md` | 7/14/30 天指标明确 |

## GEO Gap Matrix 示例

| Gap ID | 场景 | 盲区 | 商业影响 | 建议动作 |
|---|---|---|---|---|
| G-001 | 自发推荐 | AI 容易泛泛推荐橄榄油产地，但不一定解释西班牙橄榄油的差异化价值 | 用户无法形成清晰购买理由 | 生成“西班牙橄榄油为什么适合中国家庭”的解释文 |
| G-002 | 竞品对比 | 西班牙与意大利、希腊橄榄油对比信息不足 | 容易被竞品产地占据心智 | 生成产地对比 FAQ 和知乎对比问答 |
| G-003 | 选购指南 | 酸度、等级、压榨、适合烹饪方式等选购信息分散 | 影响用户下单信心 | 生成结构化选购指南 |
| G-004 | 中国本地化消费 | 缺少中餐、凉拌、煎炒、礼品等场景 | 影响家庭消费和礼品转化 | 生成中式厨房使用场景内容 |
| G-005 | 种草内容 | 缺少小红书/抖音体验型内容 | 影响种草转化和年轻用户触达 | 生成笔记标题、口播脚本和封面方向 |

## Content Task Plan 示例

| 任务 | 平台 | 标题 | 影响 | 难度 | 见效速度 | 优先级 |
|---|---|---|---:|---:|---:|---:|
| T-001 | 知乎 | 西班牙橄榄油值得买吗？和意大利橄榄油有什么区别？ | 5 | 3 | 4 | 4.3 |
| T-002 | 今日头条 | 家里做中餐，橄榄油到底怎么用？ | 5 | 2 | 5 | 4.8 |
| T-003 | 小红书 manual | 3 个适合厨房新手的西班牙橄榄油用法 | 4 | 2 | 4 | 4.1 |
| T-004 | 抖音 manual | 30 秒讲清楚橄榄油等级和适合场景 | 4 | 3 | 4 | 3.8 |
| T-005 | 官网 FAQ | 西班牙橄榄油怎么选？ | 5 | 2 | 3 | 4.2 |

## Platform Distribution Plan 示例

| 平台 | 路由状态 | Skill | 原因 | 预期产出 |
|---|---|---|---|---|
| 知乎 | planned | `zhihu-geo-draft-assistant` | 决策型问答和产地对比适合知乎 | 长答、短答、标题、话题、审核清单 |
| 今日头条 | planned | `toutiao-geo-draft-assistant` | 家庭消费和通俗科普适合头条 | 科普文、标题、摘要、关键词 |
| 小红书 | manual | future skill | 种草内容重要但当前无专用 Skill | 笔记标题、正文结构、封面方向 |
| 抖音 | manual | future skill | 适合做选购和厨房场景短视频 | 口播脚本、分镜、标题 |
| CSDN | skipped | `csdn-geo-draft-publisher` | 食品消费场景不优先 | 跳过说明 |
| 掘金 | skipped | `juejin-geo-draft-publisher` | 无开发者内容角度 | 跳过说明 |

## 最终客户交付包结构

```text
geo_orchestrator_v2/
├── final_report.md
├── summary.md
├── client_delivery_report.md
├── internal_audit_report.md
├── content_asset_summary.md
├── publish_plan_client.md
├── retest_plan.md
├── orchestrator_run_summary.md
├── raw_answers/
│   ├── deepseek/
│   └── doubao/
├── model_scores/
│   ├── deepseek.json
│   └── doubao.json
├── dual_model_comparison.json
├── brand_knowledge_base.json
├── geo_gap_matrix.json
├── content_task_plan.json
├── platform_distribution_plan.json
└── publish_plan.json
```
