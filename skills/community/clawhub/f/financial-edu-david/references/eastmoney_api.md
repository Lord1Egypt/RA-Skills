# 东方财富 F10 数据接口

## 用途

用于核对从年报PDF提取的财务数据与官方公开数据是否一致。

## F10 页面

```
https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=sh600903&color=b#/cwfx
```

上交所：`sh{code}`，深交所：`sz{code}`

## 数据接口

基础 URL：`https://datacenter-web.eastmoney.com/api/data/v1/get`

### 利润表（报告期）
```
reportName=RPT_F10_FINANCE_GINCOMEQC
filter=(SECURITY_CODE="{code}")
sortColumns=REPORT_DATE
sortTypes=-1
pageSize=5
```

### 资产负债表
```
reportName=RPT_F10_FINANCE_GBALANCE
filter=(SECURITY_CODE="{code}")
```

### 现金流量表
```
reportName=RPT_F10_FINANCE_GCASHFLOW
filter=(SECURITY_CODE="{code}")
```

## 关键核对科目

| 分类 | 科目名 | 东方财富字段 |
|------|--------|-------------|
| 资产负债表 | 资产总计 | TOTAL_ASSETS |
| 资产负债表 | 负债合计 | TOTAL_LIABILITIES |
| 资产负债表 | 所有者权益合计 | TOTAL_EQUITY |
| 利润表 | 营业收入 | OPERATE_INCOME |
| 利润表 | 净利润 | NET_PROFIT |
| 现金流量表 | 经营现金流净额 | NETCASH_OPERATE |
| 现金流量表 | 投资现金流净额 | NETCASH_INVEST |
| 现金流量表 | 筹资现金流净额 | NETCASH_FINANCE |

## 核对标准

- 资产总计、负债合计、所有者权益合计 → 100%一致（2位小数）
- 经营/投资/筹资现金流净额 → 100%一致
- 利润表科目允许因PDF解析跨行问题有微小误差（<5%）
