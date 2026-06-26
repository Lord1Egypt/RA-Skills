# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## GENERAL_MACHINE_INVOICE (通用机打发票)
- `title`: 标题
- `invoiceCode`: 发票代码
- `invoiceNo`: 发票号码
- `invoiceDate`: 开票日期
- `checkCode`: 验证码
- `buyerName`: 购方名称
- `buyerCode`: 购方纳税人识别号
- `buyerAddressAndPhone`: 购方地址及电话
- `buyerBankAndAccount`: 购方开户行及账号
- `sellerName`: 销售方名称
- `sellerCode`: 销售方纳税人识别号
- `sellerAddressAndPhone`: 销售方地址及电话
- `sellerBankAndAccount`: 销售方开户行及账号
- `preTaxTotalAmount`: 税前合计金额
- `totalTaxAmount`: 合计税额
- `totalAmountUpper`: 价税合计(大写)
- `totalAmountLower`: 价税合计(小写)
- `remarks`: 备注
- `payee`: 收款人
- `checker`: 复核
- `drawer`: 开票人
- `goodsDetails`: 发票商品明细
  - `goodsName`: 货物服务名称
  - `specification`: 规格型号
  - `unit`: 单位
  - `quantity`: 数量
  - `unitPrice`: 单价
  - `itemAmount`: 金额
  - `taxRate`: 税率
  - `taxAmount`: 税额
