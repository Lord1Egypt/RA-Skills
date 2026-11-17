# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## COMMERCIAL_INVOICE (商业发票)
- `invoiceNo`: 发票号码
- `invoiceDate`: 发票日期
- `totalAmount`: 发票金额
- `issuerName`: 发票开具方名称
- `issuerAddress`: 发票开具方地址
- `lcNumber`: 信用证编号
- `lcDate`: 信用证开证日期
- `contractNumber`: 合同号
- `priceTerm`: 成交方式

