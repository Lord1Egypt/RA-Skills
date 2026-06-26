---
name: ecommerce-data-analyzer
description: 电商数据分析工具，支持CSV销售数据上传、生成销售趋势图/产品排名/渠道收入占比/利润率分析/库存预警，一键生成PDF报告，集成SkillPay支付接口。适用于电商卖家分析销售业绩、生成业务报告。
license: MIT
---

# 电商数据分析工具

## 功能概述
1. 上传CSV格式的销售数据文件
2. 自动生成以下分析图表和报表：
   - 日销/周销/月销趋势折线图
   - 各产品销售数量/金额排名
   - 各销售渠道（Amazon/Shopify/独立站）收入占比饼图
   - 利润率分析（需手动填入成本数据）
   - 库存预警：基于销售速度预测断货时间
3. 一键导出完整分析报告为PDF文件
4. 全中文界面支持

## 支付说明
每次调用本工具将收取0.001 USDT，支付接口由SkillPay.me提供，API Key：`sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e`

## 使用流程
1. 上传销售数据CSV文件，CSV需包含以下字段：
   - 订单日期
   - 产品名称
   - 销售数量
   - 销售金额
   - 销售渠道
   - 库存数量
2. 填写成本数据（用于利润率分析）
3. 系统自动生成分析图表和报告
4. 下载PDF报告

## 依赖要求
- Python 3.8+
- pandas: 数据处理
- matplotlib: 图表生成
- reportlab: PDF生成
- flask: 网页界面（可选）

## 部署说明
1. 克隆或下载本技能目录
2. 安装依赖：`pip install pandas matplotlib reportlab flask`
3. 运行启动脚本：`python scripts/app.py`
4. 访问本地地址即可使用工具