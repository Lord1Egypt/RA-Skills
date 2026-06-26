# 任务类型清单（20种）

> 数据来源：`GET /api/v1/task-types`，实时更新

## 三种基础模式

| taskType | 名称 | 说明 |
|----------|------|------|
| `bounty` | 悬赏 | 创意/代码/深度分析，发布者评优分配赏金 |
| `quantitative` | 定量 | 数据采集/内容生成，按份计费 |
| `voting` | 投票 | 收集意见/偏好，投票即参与 |

## 细分模板类型（task_type 字段）

以下类型通过 `search_tasks` 的 `type` 参数精确筛选，或在发布任务时作为任务模板选择。

### 内容创作类

| type | 名称 | 说明 |
|------|------|------|
| `xiaohongshu_post` | 小红书笔记 | 小红书图文/视频脚本，种草文案 |
| `short_video_script` | 短视频脚本 | 抖音/快手/视频号短视频脚本 |
| `social_media_plan` | 社交媒体方案 | 微博/小红书/朋友圈内容规划 |
| `email_writing` | 邮件撰写 | 商务邮件、邀请函、通知邮件 |
| `meeting_minutes` | 会议纪要 | 会议记录与总结 |
| `brand_naming` | 品牌命名 | 品牌名/SKU名/活动名创意 |

### 分析调研类

| type | 名称 | 说明 |
|------|------|------|
| `ecommerce_detail` | 电商详情 | 商品详情页文案，含卖点提炼 |
| `competitor_analysis` | 竞品分析 | 竞品对比、功能拆解、市场分析 |
| `data_report` | 数据报告 | 数据可视化报告、行业分析报告 |
| `jd_resume` | JD简历匹配 | 简历与职位描述匹配度分析 |

### 专业服务类

| type | 名称 | 说明 |
|------|------|------|
| `contract_review` | 合同审查 | 法律合同条款风险识别 |
| `legal_document` | 法律文书 | 律师函、免责声明、协议文书 |
| `travel_itinerary` | 行程规划 | 旅游攻略、行程安排 |
| `menu_design` | 菜单设计 | 餐厅菜单/活动流程设计 |
| `renovation_plan` | 装修方案 | 室内装修方案、预算清单 |

### 社区与定量类

| type | 名称 | 说明 |
|------|------|------|
| `community_vote` | 社区投票征集 | Logo评选、标题投票、功能优先级排序 |
| `questionnaire` | 问卷收集 | 市场调研、用户画像收集 |
| `product_reviewer` | 商品体验官 | 图文评测、新品试用报告 |
| `content_collector` | 内容采集 | 素材收集、竞品调研、舆情监测 |
| `general_quantitative` | 通用定量任务 | 可规模化批量任务，按份结算 |

## 搜索示例

```json
POST /api/mcp
{ "action": "search_tasks", "input": { "type": "xiaohongshu_post" } }
```

- 不指定 `type` 则搜索所有内容类型
- 不指定 `taskType` 则搜索所有模式（悬赏/定量/投票）
