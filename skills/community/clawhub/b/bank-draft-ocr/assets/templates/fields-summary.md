# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## BANK_DRAFT (银行汇票)
- `title`: 标题
- `billCode`: 票据代码
- `billNo`: 票据号码
- `issueDate`: 出票日期
- `agentPayingBank`: 代理付款行
- `agentPayingBankNo`: 代理付款行行号
- `payeeName`: 收款人名称
- `issueAmountUpper`: 出票金额(大写)
- `issueAmountLower`: 出票金额(小写)
- `settleAmountUpper`: 实际结算金额(大写)
- `settleAmountLower`: 实际结算金额(小写)
- `applicantName`: 申请人名称
- `applicantAccount`: 申请人账号
- `issueBank`: 出票行
- `issueBankNo`: 出票行行号
- `remark`: 备注
- `cipherCode`: 密押
- `surplusAmount`: 多余金额
