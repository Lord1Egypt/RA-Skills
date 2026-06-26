---
name: check-user-fraud
description: Query MySQL database to analyze user fraud/shuadan behavior. Use when user asks to check if a user is engaging in fraudulent task completion. Analyzes time intervals, publisher concentration, task duplication, and top refresh status to identify suspicious patterns.
---

# 用户刷单查询

根据userId查询MySQL数据库，分析用户做单行为是否涉嫌刷单。

## 使用场景

当需要查询用户是否存在刷单行为时，使用此技能：
- 用户举报某账号刷单
- 风控系统标记异常账号
- 定期抽查用户行为
- 分析做单模式

## 查询流程

### 1. 执行查询脚本

```bash
python3 scripts/check_fraud.py <userId>
```

### 2. 分析维度

脚本会自动分析以下指标：

#### 时间间隔分析
- 报名到提交的时间间隔
- 完成时间 < 5分钟: 高度可疑
- 完成时间 5-10分钟: 中度可疑

#### 发单人集中度
- 频繁接取同一发单人的任务
- 同一发单人 > 10次: 高度可疑
- 同一发单人 5-10次: 中度可疑

#### 任务重复度
- 多次接取相同任务
- 重复任务 > 2次: 可疑

#### 置顶刷新状态
- 接取时任务是否有置顶
- 未置顶任务比例 > 70%: 可疑（可能通过非正规渠道获取）

### 3. 风险等级评估

- **高风险**: 2个及以上高风险指标，或完成时间<5分钟占比>50%
- **中风险**: 1个高风险或2个中风险指标
- **低风险**: 无明显异常

## 数据库配置

- **Host**: rr-wz97dxha81orq30j0eo.mysql.rds.aliyuncs.com
- **Port**: 3389
- **User**: oc_gw
- **Password**: m83KkZVLQp2Wg7HgDVb5cRjQ

## SQL查询参考

详细SQL语句见 `references/` 目录：
- `query_user_records.sql` - 查询用户做单记录
- `query_top_refresh.sql` - 查询任务置顶状态
- `fraud_analysis_guide.md` - 刷单分析指标说明

## 输出格式

```json
{
  "userId": "用户ID",
  "total_records": 记录总数,
  "records": [...],  // 详细记录
  "fraud_indicators": [  // 可疑指标
    {
      "type": "指标类型",
      "level": "high/medium/low",
      "description": "描述"
    }
  ],
  "summary": {
    "risk_level": "high/medium/low",
    "conclusion": "结论",
    "indicators_count": 指标数量,
    "high_risk_count": 高风险数量,
    "medium_risk_count": 中风险数量
  }
}
```

## 注意事项

1. 需要安装pymysql: `pip install pymysql`
2. 数据库名需要确认后填入脚本
3. 查询结果包含敏感信息，注意保密