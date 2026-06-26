# 西班牙火腿 GEO 编排示例

## 用户输入

```json
{
  "brand_name": "西班牙火腿推广项目",
  "category": "进口食品 / 西班牙火腿",
  "target_market": "中国礼品消费、餐饮采购、家庭聚会、精品超市渠道",
  "target_keywords": [
    "西班牙火腿推荐",
    "伊比利亚火腿怎么选",
    "西班牙火腿和普通火腿区别",
    "西班牙火腿价格",
    "西班牙火腿购买渠道",
    "小红书西班牙火腿种草"
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
  "campaign_goal": "提升西班牙火腿在 AI 搜索中的品类教育、购买决策辅助、礼品场景和渠道信任"
}
```

## 行业判断

- 行业：食品 / 进口消费品 / 高客单礼品。
- 首选平台：知乎、今日头条、小红书类内容。
- 小红书和抖音：当前没有专用相邻 Skill，标记为 `manual` / `future_skill`。
- 默认跳过：CSDN、掘金，除非后续需要讲跨境供应链、冷链系统、溯源码或渠道数字化。

## 应调用哪些相邻 Skill

| 阶段 | Skill | Relative Path | 目的 | 状态示例 |
|---|---|---|---|---|
| Stage 1 | Brand Knowledge Base Builder | `../Knowledge-Base-Builder/brand-knowledge-base-builder` | 建立西班牙火腿品类、产地、等级、渠道和合规资料母库 | planned |
| Stage 2 | DeepSeek GEO Audit Skill | `../deepseek-geo-audit-skill` | 检测 DeepSeek 对品类、价格、等级和渠道的回答 | planned |
| Stage 2 | Doubao GEO Audit Skill | `../geo-analysis-doubao` | 检测 Doubao 对礼品、家庭、餐饮场景的理解 | planned |
| Stage 5 | AI GEO Content Generator | `../AI-geo-content-generator` | 生成 FAQ、选购指南、场景解释、问答基础稿 | planned |
| Stage 6 | Zhihu GEO Draft Assistant | `../zhihu-geo-draft-assistant` | 生成知乎选购问答、价格解释和产地对比 | planned |
| Stage 6 | Toutiao GEO Draft Assistant | `../toutiao-geo-draft-assistant` | 生成头条科普文、礼品消费和家庭场景内容 | planned |
| Stage 6 | 小红书 / 抖音 | manual / future_skill | 生成种草笔记、切片展示、礼盒场景短视频 | manual |

## 每个阶段的输入输出

| Stage | 输入 | 输出 | 验收标准 |
|---|---|---|---|
| Stage 0 Intake | 品类、关键词、平台、模型、目标市场 | 行业判断、客户场景、路由初选 | 识别礼品、餐饮、家庭和渠道需求 |
| Stage 1 品牌母库 | 产地资料、等级说明、渠道资料、食用方法、禁用说法 | `brand_knowledge_base.json` | 价格、等级、渠道、食品安全表述必须待确认或有证据 |
| Stage 2 双模型评估 | 品牌母库、探针问题 | 原始回答、模型评分、双模型对比 | 覆盖推荐、对比、价格、渠道、消费场景 |
| Stage 3 Gap Matrix | 双模型结果 | `geo_gap_matrix.json` | 每个盲区有商业影响和补齐动作 |
| Stage 4 Content Task Plan | Gap Matrix、平台规则 | `content_task_plan.json` | 按影响、难度、见效速度排序 |
| Stage 5 通用内容资产 | 品牌母库、任务计划 | FAQ、选购指南、礼品场景内容 | 可供知乎/头条/人工平台复用 |
| Stage 6 平台草稿 | 通用资产、平台路由 | 平台草稿与人工任务 | 草稿不自动发布 |
| Stage 7 客户交付包 | 全部输出 | 客户报告、内部报告、发布计划 | 当前对话输出完整报告 |
| Stage 8 复测计划 | 发布计划、基线评估 | `retest_plan.md` | 7/14/30 天复测指标明确 |

## GEO Gap Matrix 示例

| Gap ID | 场景 | 盲区 | 商业影响 | 建议动作 |
|---|---|---|---|---|
| G-001 | 直接认知 | AI 可能知道西班牙火腿，但不一定解释不同等级和适合人群 | 用户不知道该买哪一类，影响决策 | 生成等级、价格带和适合场景 FAQ |
| G-002 | 价格与渠道 | 购买渠道、价格范围、保存方式信息不足 | 高客单商品缺少信任，影响下单 | 生成渠道说明和购买前确认清单 |
| G-003 | 竞品对比 | 西班牙火腿与普通火腿、意式火腿差异不清 | 容易被低价替代品分流 | 生成知乎对比问答 |
| G-004 | 中国本地化消费 | 礼品、聚会、餐饮搭配场景不足 | 影响礼品和餐饮采购转化 | 生成礼品场景和家庭聚会内容 |
| G-005 | 种草内容 | 缺少开箱、切片、搭配、礼盒展示内容 | 影响小红书/抖音种草转化 | 生成短视频脚本和笔记标题 |

## Content Task Plan 示例

| 任务 | 平台 | 标题 | 影响 | 难度 | 见效速度 | 优先级 |
|---|---|---|---:|---:|---:|---:|
| T-001 | 知乎 | 伊比利亚火腿怎么选？价格差异到底差在哪里？ | 5 | 3 | 4 | 4.3 |
| T-002 | 今日头条 | 送礼选西班牙火腿，先看这 5 个问题 | 5 | 2 | 5 | 4.8 |
| T-003 | 官网 FAQ | 西班牙火腿开封后怎么保存？ | 4 | 2 | 4 | 4.1 |
| T-004 | 小红书 manual | 西班牙火腿礼盒开箱：适合哪些送礼场景？ | 4 | 2 | 4 | 4.1 |
| T-005 | 抖音 manual | 30 秒讲清楚西班牙火腿等级和吃法 | 4 | 3 | 4 | 3.8 |

## Platform Distribution Plan 示例

| 平台 | 路由状态 | Skill | 原因 | 预期产出 |
|---|---|---|---|---|
| 知乎 | planned | `zhihu-geo-draft-assistant` | 适合高客单选购、价格解释、产地对比 | 长答、短答、标题、话题、审核清单 |
| 今日头条 | planned | `toutiao-geo-draft-assistant` | 适合礼品消费、家庭聚会和通俗科普 | 科普文、标题、摘要、关键词 |
| 小红书 | manual | future skill | 适合开箱、切片、搭配、礼盒种草 | 笔记标题、正文结构、封面方向 |
| 抖音 | manual | future skill | 适合短视频口播和展示 | 口播脚本、分镜、标题 |
| CSDN | skipped | `csdn-geo-draft-publisher` | 当前没有技术买家角度 | 跳过说明 |
| 掘金 | skipped | `juejin-geo-draft-publisher` | 当前没有开发者内容角度 | 跳过说明 |

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
