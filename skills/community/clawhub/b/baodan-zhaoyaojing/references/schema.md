# 保单 JSON Schema

保单提取的标准结构化输出格式。

```json
{
  "policy_name": "string - 保单产品名称",
  "insurer": "string - 保险公司名称",
  "version": "string - 版本/年份（如 2024版）",
  "premium_annual": "number - 年缴保费（元）",
  "premium_period": "string - 缴费方式（年缴/月缴/趸交）",
  "coverage_period": "string - 保障期间（1年/终身）",
  "dimensions": {
    "coverage_scope": {
      "accidental_death": {
        "covered": "boolean",
        "amount": "number | null - 保额（元）"
      },
      "accidental_disability": {
        "covered": "boolean",
        "amount": "number | null",
        "grading": "string - 伤残等级赔付规则（如 '1-10级按比例'）"
      },
      "accidental_medical": {
        "covered": "boolean",
        "amount": "number | null - 医疗保额",
        "reimbursement_ratio": "string - 报销比例（如 '100%'、'90%'）",
        "social_insurance_only": "boolean - 是否仅限社保内用药"
      },
      "sudden_death": {
        "covered": "boolean",
        "amount": "number | null"
      },
      "traffic_extra": {
        "aviation": { "covered": "boolean", "amount": "number | null" },
        "rail": { "covered": "boolean", "amount": "number | null" },
        "bus": { "covered": "boolean", "amount": "number | null" },
        "self_driving": { "covered": "boolean", "amount": "number | null" },
        "riding": { "covered": "boolean", "amount": "number | null" }
      },
      "hospital_daily_allowance": {
        "covered": "boolean",
        "amount_per_day": "number | null",
        "max_days": "number | null"
      },
      "ambulance": {
        "covered": "boolean",
        "amount": "number | null"
      },
      "other_coverages": [
        {
          "name": "string - 其他保障名称",
          "amount": "number | null",
          "note": "string - 说明"
        }
      ]
    },
    "deductible_and_waiting": {
      "medical_deductible": "number - 医疗免赔额（元），0表示无免赔",
      "waiting_period_days": "number - 等待期（天），0表示无等待期",
      "single_claim_limit": "number | null - 单次理赔限额",
      "annual_limit": "number | null - 年度理赔限额"
    },
    "exclusions": {
      "high_risk_sports": "boolean - 是否排除高风险运动",
      "high_risk_sports_detail": "string - 具体排除的运动列表",
      "occupation_limit": "string - 职业类别限制（如 '1-3类'、'1-6类'）",
      "pre_existing": "boolean - 是否排除既往症",
      "drunk_driving": "boolean - 是否排除酒驾",
      "war_terrorism": "boolean - 是否排除战争/恐怖主义",
      "specific_regions": ["string - 排除的地区"],
      "other_key_exclusions": ["string - 其他重要除外条款"]
    },
    "claim_conditions": {
      "claim_processing_days": "number | null - 理赔处理时效（工作日）",
      "online_claim": "boolean - 是否支持线上理赔",
      "hospital_scope": "string - 医院范围（如 '二级及以上公立医院'）",
      "required_materials": ["string - 所需理赔材料"],
      "special_notes": ["string - 理赔特别注意事项"]
    },
    "claim_reputation": {
      "search_conducted": "boolean - 是否已执行搜索",
      "data_available": "boolean - 是否搜索到有效数据",
      "avg_claim_days_reported": "number | null - 用户反馈平均理赔到账天数",
      "complaint_volume": "string - 投诉量等级（低/中/高/未知）",
      "complaint_ratio": "string | null - 投诉量/保费收入比描述",
      "common_complaints": ["string - 常见投诉类型（如'拖赔''拒赔''材料反复补充'）"],
      "positive_feedback": ["string - 正面反馈摘要"],
      "regulatory_data": {
        "has_data": "boolean - 监管网站是否有披露数据",
        "avg_processing_days": "number | null - 监管披露的平均理赔时效",
        "settlement_rate": "string | null - 结案率（如 '98.5%'）",
        "source_url": "string | null - 数据来源链接"
      },
      "sources": [
        {
          "platform": "string - 来源平台（微博/小红书/知乎/黑猫投诉/银保监会等）",
          "summary": "string - 搜索结果摘要",
          "sentiment": "positive|neutral|negative|mixed"
        }
      ],
      "overall_assessment": "string - AI综合评估（一段话）",
      "note": "string | null - 若无数据则为'数据不足，建议付费咨询专业保险顾问'"
    }
  },
  "raw_text_excerpt": "string - 保单关键条款原文摘要（500字以内）",
  "confidence": {
    "policy_name": "high|medium|low",
    "premium_annual": "high|medium|low",
    "coverage_scope": "high|medium|low",
    "deductible_and_waiting": "high|medium|low",
    "exclusions": "high|medium|low",
    "claim_conditions": "high|medium|low",
    "claim_reputation": "high|medium|low"
  }
}
```

## 术语白话映射表

用于体检报告视图，将专业术语翻译为普通人语言：

| 专业术语 | 白话解释 |
|---------|---------|
| 被保险人 | 受保的人 |
| 免赔额 | 自己掏腰包的部分，低于这个数不赔 |
| 等待期 | 买完后多久才能生效 |
| 除外责任 | 什么情况不赔 |
| 社保内用药 | 只报销医保目录里的药，进口药自费药不报 |
| 职业类别 | 按工作危险程度分级，4类以上算高风险 |
| 伤残等级表 | 按伤残严重程度1-10级，对应不同赔付比例 |
| 报销比例 | 花了100块，报80块就是80% |
| 猝死 | 突然死亡，很多意外险不保这个！ |
| 住院津贴 | 住院每天给的钱，跟医疗费报销不冲突 |
| 保额 | 最多赔多少 |
| 保费 | 每年交多少钱 |
| 趸交 | 一次性交清 |
| 线上理赔 | 在APP或小程序上提交材料，不用跑柜台 |
| 理赔时效 | 从提交材料到钱到账要多久 |
| 结案率 | 100个理赔申请里有多少最终赔了 |
| 投诉量/保费比 | 收的保费越多投诉理应越多，这个比值能反映真实服务质量 |
