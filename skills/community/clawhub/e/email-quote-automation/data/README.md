# 数据文件说明 / Data Files Instructions

[中文](#中文说明) | [English](#english-instructions)

---

## 中文说明

本目录用于存放您的业务报价数据文件。

### 初始状态

- `example/` 目录中包含示例数据，您可以参考它来创建自己的数据
- 删除或修改示例文件后放入您的实际数据即可

### 如何准备数据

### 1. 报价规则文件

创建您自己的报价规则说明文档：

```
data/pricing_rules.md
```

在文档中说明您的：
- 材质分类及基础价格
- 尺寸计算规则
- 加工工艺费用
- 折扣政策
- 运输和付款说明

### 2. 材质参数表（可选，如果使用Excel）

如果您希望从Excel读取报价参数，可以放入：

```
data/material_prices.xlsx
```

然后修改 `scripts/quote_calculator.py` 从Excel中读取数据代替硬编码的数据。

### 3. 修改计算逻辑

根据您的实际报价规则，编辑 `scripts/quote_calculator.py` 文件：

- 修改 `MATERIAL_PRICES` 数组填入您的材质和基础价格
- 修改 `SIZE_COEFFICIENTS` 适配您的尺寸分段规则
- 修改 `PROCESS_FEES` 添加您提供的加工工艺和费用
- 修改 `DISCOUNTS` 设置您的批量折扣

### 示例数据说明

`example/pricing_rules_example.md` 是奖牌定制行业的报价规则示例，您可以打开它参考格式。

---

## English Instructions

This directory is for your business pricing data files.

### Initial State

- The `example/` directory contains example data, you can refer to it to create your own data
- After deleting or modifying the example files, put your actual data here

### How to Prepare Your Data

### 1. Pricing Rules Document

Create your own pricing rules documentation:

```
data/pricing_rules.md
```

In the document explain:
- Material categories and base prices
- Size calculation rules
- Processing fees
- Discount policies
- Shipping and payment terms

### 2. Material Parameter Table (optional, if using Excel)

If you want to read pricing parameters from Excel, place it here:

```
data/material_prices.xlsx
```

Then modify `scripts/quote_calculator.py` to read data from Excel instead of hardcoded data.

### 3. Modify Calculation Logic

According to your actual pricing rules, edit the `scripts/quote_calculator.py` file:

- Modify the `MATERIAL_PRICES` array with your materials and base prices
- Modify `SIZE_COEFFICIENTS` to fit your size segmentation rules
- Modify `PROCESS_FEES` to add the processing services and fees you offer
- Modify `DISCOUNTS` to set your volume discounts

### Example Data

`example/pricing_rules_example.md` is an example of pricing rules for the custom medal industry, you can open it for reference formatting.

