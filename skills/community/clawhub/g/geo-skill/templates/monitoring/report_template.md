# {{PARK_NAME}} GEO监控报告

> 报告周期：{{REPORT_START_DATE}} 至 {{REPORT_END_DATE}}
> 报告生成时间：{{REPORT_GENERATION_TIME}}
> 报告编号：{{REPORT_ID}}

---

## 📊 一、整体健康度评分

| 评估维度 | 得分 | 状态 | 环比变化 |
|----------|------|------|----------|
| AI引用率 | {{AI_CITATION_SCORE}}/100 | {{AI_CITATION_STATUS}} | {{AI_CITATION_TREND}} |
| 信息准确率 | {{ACCURACY_SCORE}}/100 | {{ACCURACY_STATUS}} | {{ACCURACY_TREND}} |
| 排名稳定性 | {{RANK_STABILITY_SCORE}}/100 | {{RANK_STABILITY_STATUS}} | {{RANK_STABILITY_TREND}} |
| 内容覆盖度 | {{COVERAGE_SCORE}}/100 | {{COVERAGE_STATUS}} | {{COVERAGE_TREND}} |
| **综合评分** | **{{TOTAL_SCORE}}/100** | **{{TOTAL_STATUS}}** | {{TOTAL_TREND}} |

### 评分说明

- 🟢 绿：80-100分，优秀
- 🟡 黄：60-79分，良好
- 🟠 橙：40-59分，需改进
- 🔴 红：0-39分，紧急处理

---

## 🔍 二、AI引用情况

### 核心关键词排名

| 关键词 | DeepSeek | 豆包 | Kimi | 平均排名 | 目标排名 | 差距 |
|--------|----------|------|------|----------|----------|------|
| {{KEYWORD_1}} | #{{RANK_DS_1}} | #{{RANK_DB_1}} | #{{RANK_KIMI_1}} | #{{AVG_RANK_1}} | #{{TARGET_RANK}} | {{GAP_1}} |
| {{KEYWORD_2}} | #{{RANK_DS_2}} | #{{RANK_DB_2}} | #{{RANK_KIMI_2}} | #{{AVG_RANK_2}} | #{{TARGET_RANK}} | {{GAP_2}} |
| {{KEYWORD_3}} | #{{RANK_DS_3}} | #{{RANK_DB_3}} | #{{RANK_KIMI_3}} | #{{AVG_RANK_3}} | #{{TARGET_RANK}} | {{GAP_3}} |
| {{KEYWORD_4}} | #{{RANK_DS_4}} | #{{RANK_DB_4}} | #{{RANK_KIMI_4}} | #{{AVG_RANK_4}} | #{{TARGET_RANK}} | {{GAP_4}} |
| {{KEYWORD_5}} | #{{RANK_DS_5}} | #{{RANK_DB_5}} | #{{RANK_KIMI_5}} | #{{AVG_RANK_5}} | #{{TARGET_RANK}} | {{GAP_5}} |

### AI答案引用分析

| 问题类型 | 被引用次数 | 引用率 | 信息准确率 |
|----------|------------|--------|------------|
| 基础认知 | {{CITATION_BASIC}} | {{CITATION_RATE_BASIC}}% | {{ACCURACY_BASIC}}% |
| 招商入驻 | {{CITATION_INVEST}} | {{CITATION_RATE_INVEST}}% | {{ACCURACY_INVEST}}% |
| 政策优惠 | {{CITATION_POLICY}} | {{CITATION_RATE_POLICY}}% | {{ACCURACY_POLICY}}% |
| 配套设施 | {{CITATION_FACILITY}} | {{CITATION_RATE_FACILITY}}% | {{ACCURACY_FACILITY}}% |

### 本周新增引用

- 🔖 {{NEW_CITATION_1}}
- 🔖 {{NEW_CITATION_2}}
- 🔖 {{NEW_CITATION_3}}

---

## 📱 三、内容表现数据

### 平台发布统计

| 平台 | 本周发布 | 累计发布 | 阅读量 | 互动量 | 转化数 |
|------|----------|----------|--------|--------|--------|
| 知乎 | {{ZH_PUBLISH_COUNT}} | {{ZH_TOTAL_COUNT}} | {{ZH_VIEWS}} | {{ZH_ENGAGEMENT}} | {{ZH_CONVERSION}} |
| 百家号 | {{BJH_PUBLISH_COUNT}} | {{BJH_TOTAL_COUNT}} | {{BJH_VIEWS}} | {{BJH_ENGAGEMENT}} | {{BJH_CONVERSION}} |
| 公众号 | {{WXG_PUBLISH_COUNT}} | {{WXG_TOTAL_COUNT}} | {{WXG_VIEWS}} | {{WXG_ENGAGEMENT}} | {{WXG_CONVERSION}} |
| CSDN | {{CSDN_PUBLISH_COUNT}} | {{CSDN_TOTAL_COUNT}} | {{CSDN_VIEWS}} | {{CSDN_ENGAGEMENT}} | {{CSDN_CONVERSION}} |
| 36氪 | {{36KR_PUBLISH_COUNT}} | {{36KR_TOTAL_COUNT}} | {{36KR_VIEWS}} | {{36KR_ENGAGEMENT}} | {{36KR_CONVERSION}} |

### 内容类型分布

```
{{PIECHART_DATA}}
```

### 高性能内容TOP5

| 排名 | 标题 | 平台 | 阅读量 | 转化 |
|------|------|------|--------|------|
| 1 | {{TOP_CONTENT_1}} | {{TOP_PLATFORM_1}} | {{TOP_VIEWS_1}} | {{TOP_CONV_1}} |
| 2 | {{TOP_CONTENT_2}} | {{TOP_PLATFORM_2}} | {{TOP_VIEWS_2}} | {{TOP_CONV_2}} |
| 3 | {{TOP_CONTENT_3}} | {{TOP_PLATFORM_3}} | {{TOP_VIEWS_3}} | {{TOP_CONV_3}} |
| 4 | {{TOP_CONTENT_4}} | {{TOP_PLATFORM_4}} | {{TOP_VIEWS_4}} | {{TOP_CONV_4}} |
| 5 | {{TOP_CONTENT_5}} | {{TOP_PLATFORM_5}} | {{TOP_VIEWS_5}} | {{TOP_CONV_5}} |

---

## ⚠️ 四、问题预警

### 🔴 紧急问题

| 问题 | 严重程度 | 发现时间 | 处理状态 |
|------|----------|----------|----------|
| {{URGENT_ISSUE_1}} | 紧急 | {{URGENT_TIME_1}} | {{URGENT_STATUS_1}} |
| {{URGENT_ISSUE_2}} | 紧急 | {{URGENT_TIME_2}} | {{URGENT_STATUS_2}} |

### 🟠 重要问题

| 问题 | 严重程度 | 发现时间 | 处理状态 |
|------|----------|----------|----------|
| {{IMPORTANT_ISSUE_1}} | 重要 | {{IMPORTANT_TIME_1}} | {{IMPORTANT_STATUS_1}} |
| {{IMPORTANT_ISSUE_2}} | 重要 | {{IMPORTANT_TIME_2}} | {{IMPORTANT_STATUS_2}} |

### 🟡 一般问题

| 问题 | 建议 | 处理期限 |
|------|------|----------|
| {{NORMAL_ISSUE_1}} | {{NORMAL_SUGGESTION_1}} | {{NORMAL_DEADLINE_1}} |
| {{NORMAL_ISSUE_2}} | {{NORMAL_SUGGESTION_2}} | {{NORMAL_DEADLINE_2}} |

---

## 🔄 五、修复进度

### 上周问题处理

| 问题 | 处理措施 | 处理结果 |
|------|----------|----------|
| {{FIXED_ISSUE_1}} | {{FIX_ACTION_1}} | ✅ 已解决 |
| {{FIXED_ISSUE_2}} | {{FIX_ACTION_2}} | ✅ 已解决 |
| {{FIXED_ISSUE_3}} | {{FIX_ACTION_3}} | ⚠️ 部分解决 |

### 本周新发现问题

| 问题 | 负责团队 | 计划完成日期 |
|------|----------|--------------|
| {{NEW_ISSUE_1}} | {{TEAM_1}} | {{DUE_DATE_1}} |
| {{NEW_ISSUE_2}} | {{TEAM_2}} | {{DUE_DATE_2}} |

---

## 📈 六、竞品监控

### 竞品AI曝光度对比

| 竞品名称 | AI提及次数 | 正面率 | 曝光趋势 |
|----------|------------|--------|----------|
| {{COMPETITOR_1}} | {{MENTION_1}} | {{POSITIVE_RATE_1}}% | {{TREND_1}} |
| {{COMPETITOR_2}} | {{MENTION_2}} | {{POSITIVE_RATE_2}}% | {{TREND_2}} |
| {{COMPETITOR_3}} | {{MENTION_3}} | {{POSITIVE_RATE_3}}% | {{TREND_3}} |
| **{{PARK_NAME}}** | **{{MY_MENTION}}** | **{{MY_POSITIVE_RATE}}%** | **{{MY_TREND}}** |

### 竞品动态

- 📢 {{COMPETITOR_NEWS_1}}
- 📢 {{COMPETITOR_NEWS_2}}

---

## 💡 七、优化建议

### 短期建议（本周）

1. {{SHORT_TERM_1}}
2. {{SHORT_TERM_2}}
3. {{SHORT_TERM_3}}

### 中期建议（本月）

1. {{MID_TERM_1}}
2. {{MID_TERM_2}}

### 长期建议（季度）

1. {{LONG_TERM_1}}
2. {{LONG_TERM_2}}

---

## 📋 八、下周计划

- [ ] {{TODO_1}}
- [ ] {{TODO_2}}
- [ ] {{TODO_3}}
- [ ] {{TODO_4}}
- [ ] {{TODO_5}}

---

## 📎 九、附件

- 附件1：[详细数据表格链接]
- 附件2：[AI对话截图]
- 附件3：[内容分发截图]

---

## 📝 报告审批

| 角色 | 姓名 | 日期 | 签字 |
|------|------|------|------|
| 报告人 | {{REPORTER}} | {{REPORT_DATE}} | ________ |
| 审核人 | {{REVIEWER}} | {{REVIEW_DATE}} | ________ |
| 批准人 | {{APPROVER}} | {{APPROVE_DATE}} | ________ |

---

*报告由GEO.SKILL监控模块自动生成*
*如有问题请联系：{{CONTACT_EMAIL}}*
