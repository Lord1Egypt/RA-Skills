# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## BANK_CHECK (银行支票)
- `title`: 标题
- `bankName`: 银行名称
- `billNo`: 票据号码
- `issueDate`: 出票日期
- `payingBankName`: 付款行名称
- `payeeName`: 收款人
- `drawerAccount`: 出票人账号
- `amountUpper`: 大写金额
- `amountLower`: 小写金额
- `usage`: 用途
- `password`: 密码
- `bankCode`: 行号
