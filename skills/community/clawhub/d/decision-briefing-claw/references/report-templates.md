# 简报模板库

## 模板选择

| 模板名 | 适用场景 | 长度 |
|--------|----------|------|
| `minimal` | 快速浏览，仅核心数据 | ~200 字 |
| `standard` | 日常使用，数据+对比+异常 | ~500 字 |
| `detailed` | 深度分析，含趋势图表 | ~1000 字 |
| `executive` | 高管版，战略指标+解读 | ~800 字 |

## 模板占位符

所有模板使用 `{变量名}` 占位符，自动填充数据：

- `{date}` - 报告日期
- `{metric_name}` - 指标名称
- `{value}` - 当前值
- `{prev_value}` - 前值（昨日/上周/上月）
- `{change_pct}` - 变化百分比
- `{change_abs}` - 变化绝对值
- `{trend}` - 趋势符号（↑↓→）
- `{alert}` - 异常标记（⚠️ 或空）

## 极简版模板 (minimal)

```markdown
# {date} 经营简报

**核心数据**
- 订单数：{orders_count} {orders_trend}
- GMV：¥{gmv} {gmv_trend}
- 新增用户：{new_users} {new_users_trend}

{alerts}
```

## 标准版模板 (standard)

```markdown
# {date} 经营简报

## 核心数据

| 指标 | 昨日 | 前日 | 变化 |
|------|------|------|------|
| 订单数 | {orders_count} | {orders_prev} | {orders_change} {orders_trend} |
| GMV | ¥{gmv} | ¥{gmv_prev} | {gmv_change} {gmv_trend} |
| 客单价 | ¥{avg_order} | ¥{avg_order_prev} | {avg_order_change} {avg_order_trend} |
| 新增用户 | {new_users} | {new_users_prev} | {new_users_change} {new_users_trend} |
| 活跃用户 | {dau} | {dau_prev} | {dau_change} {dau_trend} |

## 财务数据

| 指标 | 昨日 | 前日 | 变化 |
|------|------|------|------|
| 收入 | ¥{revenue} | ¥{revenue_prev} | {revenue_change} {revenue_trend} |
| 成本 | ¥{cost} | ¥{cost_prev} | {cost_change} {cost_trend} |
| 利润 | ¥{profit} | ¥{profit_prev} | {profit_change} {profit_trend} |

## 异常提醒

{alerts}

---
*数据来源：{data_sources} | 生成时间：{generated_at}*
```

## 详细版模板 (detailed)

在标准版基础上增加：
- 近 7 天趋势图（ASCII 图表或图片链接）
- 同比数据（去年同期对比）
- 分类明细（按品类/渠道/地区拆解）

## 高管版模板 (executive)

```markdown
# {date} 经营简报（高管版）

## 战略指标

**增长**
- GMV：¥{gmv}（{gmv_yoy_change}）
- 用户规模：{total_users}（{total_users_yoy_change}）

**盈利**
- 毛利率：{gross_margin}%（{gross_margin_change}）
- 净利率：{net_margin}%（{net_margin_change}）

**效率**
- 获客成本：¥{cac}（{cac_change}）
- 用户生命周期价值：¥{ltv}（{ltv_change}）

## 关键洞察

{insights}

## 需要关注

{alerts}
```

## 输出格式

- **Markdown**：默认格式，适合飞书/企业微信
- **HTML**：邮件推送使用，自动转换表格和样式
- **纯文本**：短信/钉钉等纯文本渠道
