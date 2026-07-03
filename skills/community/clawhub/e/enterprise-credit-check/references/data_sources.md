# 数据源配置

## 一、四大官方数据源

| 数据源 | 官网 | 查询内容 | 权威性 |
|--------|------|----------|--------|
| 中国人民银行征信中心 | https://www.pbccrc.org.cn | 企业信用报告、信贷记录 | ★★★★★ |
| 国家企业信用信息公示系统 | https://www.gsxt.gov.cn | 经营异常、行政处罚 | ★★★★★ |
| 中国执行信息公开网 | http://zxgk.court.gov.cn | 失信被执行人、限高 | ★★★★★ |
| 裁判文书网 | https://wenshu.court.gov.cn | 诉讼记录 | ★★★★☆ |

## 二、数据源详情

### 1. 人行征信中心
- **网址**: https://www.pbccrc.org.cn
- **主要查询**: 企业信用报告
- **数据内容**:
  - 信贷记录汇总
  - 逾期及违约信息
  - 担保信息
  - 公共信息（欠税、民事判决等）

### 2. 信用公示系统
- **网址**: https://www.gsxt.gov.cn
- **主要查询**: 企业基础信息
- **数据内容**:
  - 经营异常名录
  - 严重违法失信企业名单
  - 行政处罚信息
  - 股权冻结信息
  - 年报信息

### 3. 执行信息公开网
- **网址**: http://zxgk.court.gov.cn
- **主要查询**: 司法执行信息
- **数据内容**:
  - 失信被执行人名单
  - 被执行人信息
  - 限制高消费人员

### 4. 裁判文书网
- **网址**: https://wenshu.court.gov.cn
- **主要查询**: 诉讼记录
- **数据内容**:
  - 民事判决书
  - 刑事判决书
  - 行政判决书
  - 知识产权诉讼

## 三、数据格式规范

### 人行征信报告格式
```json
{
  "source": "pbc_credit_report",
  "enterprise_name": "xxx",
  "credit_score": "正常/关注/次级/可疑/损失",
  "loan_records": [],
  "guarantee_records": [],
  "public_records": []
}
```

### 信用公示系统格式
```json
{
  "source": "business_anomaly",
  "enterprise_name": "xxx",
  "unified_social_credit_code": "xxx",
  "business_status": "存续/吊销/注销",
  "abnormal_records": [],
  "illegal_records": []
}
```

### 执行信息公开网格式
```json
{
  "source": "dishonest_execution",
  "enterprise_name": "xxx",
  "unified_social_credit_code": "xxx",
  "dishonest_records": [],
  "execution_subjects": [],
  "consumption_restrictions": []
}
```

### 裁判文书网格式
```json
{
  "source": "litigation_records",
  "enterprise_name": "xxx",
  "total_cases": 0,
  "cases": [],
  "ip_disputes": 0
}
```
