# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## BUS_TICKET (汽车票)
- `title`: 标题
- `invoiceCode`: 发票代码
- `invoiceNo`: 发票号码
- `invoiceDate`: 开票日期
- `departureDate`: 开车日期
- `departureTime`: 开车时间
- `departStation`: 起始站
- `destinationStation`: 终止站
- `totalAmountLower`: 合计金额(小写)
- `passengerName`: 旅客姓名
