# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## GENERAL (通用文字)
- `width`: 图像宽度（像素）
- `height`: 图像高度（像素）
- `angle`: 图像旋转角度（度）
- `text`: 文字块数组，每个块包含：
  - `text`: 文字内容
  - `pos`: 四边形坐标 [[左上], [右上], [右下], [左下]]
  - `x`, `y`, `width`, `height`: 文本块位置和尺寸
  - `text_class`: 文本类别（1竖向，2横向）
  - `confidences`, `chars` 等

## ID_CARD (大陆身份证)
- `name`: 姓名
- `gender`: 性别
- `nation`: 民族
- `bornDate`: 出生日期
- `address`: 住址
- `IDNumber`: 公民身份号码
- `issueInstitution`: 签发机关
- `validityPeriod`: 有效期

## BANK_CARD (银行卡)
- `bankName`: 银行名称
- `cardNumber`: 卡号
- `validThru`: 有效期
- `cardHolder`: 持卡人

## BUSINESS_LICENSE (营业执照)
- `title`: 标题
- `socialCreditCode`: 统一社会信用代码
- `name`: 名称
- `capital`: 注册资本
- `type`: 类型
- `date`: 成立日期
- `directorType`: 负责人类型
- `director`: 负责人
- `businessTerm`: 营业期限
- `businessScope`: 经营范围
- `address`: 住所

## VAT_INVOICE (增值税发票)
- `title`: 发票名称
- `invoiceCode`: 发票代码
- `invoiceNo`: 发票号码
- `invoiceDate`: 开票日期
- `buyerName`: 购方名称
- `buyerCode`: 购方税号
- `sellerName`: 销方名称
- `sellerCode`: 销方税号
- `totalAmountLower`: 价税合计（小写）
- `totalAmountUpper`: 价税合计（大写）
- `preTaxTotalAmount`: 税前合计
- `totalTaxAmount`: 合计税额
- `goodsDetails`: 商品明细数组
- ... 等

## VAT_ROLL_INVOICE (增值税卷票)
- `invoiceCode`: 发票代码
- `invoiceNo`: 发票号码
- `printedNo`: 机打号码
- `invoiceDate`: 开票日期
- `buyerName`: 购方名称
- `buyerCode`: 购方税号
- `sellerName`: 销方名称
- `sellerCode`: 销方税号
- `totalAmountUpper`: 价税合计大写
- `totalAmountLower`: 价税合计小写
- `checkCode`: 校验码

## TAXI_INVOICE (出租车发票)
- `title`: 发票标题
- `invoiceCode`: 发票代码
- `invoiceNo`: 发票号码
- `vehicleNo`: 车号
- `certificateNo`: 证号
- `date`: 日期
- `boardingTime`: 上车时间
- `alightingTime`: 下车时间
- `amount`: 金额
- `actualAmount`: 实收金额

## TRAIN_TICKET (火车票)
- `ticketNo`: 车票编号
- `departStation`: 出发站
- `destinationStation`: 到达站
- `trainNo`: 车次
- `departDate`: 出发日期
- `departTime`: 出发时间
- `seatPostion`: 座位号
- `seatNo`: 座次等级
- `ticketPrice`: 票价
- `passengerName`: 旅客姓名
- `identifyIdTag`: 是否有身份证号
- `invoiceNo`: 发票号码
- `invoiceDate`: 开票日期
- ... 等

## AIRPORT_TICKET (航空行程单)
- `title`: 标题
- `passengerName`: 旅客姓名
- `identifyIdNo`: 身份证号
- `ticketPrice`: 票价
- `fuleDischarge`: 燃油附加费
- `civilAviationFund`: 民航发展基金
- `taxAmount`: 增值税税额
- `totalAmount`: 合计金额
- `issueUnit`: 填开单位
- `issueDate`: 填开日期
- `airTransportRoutes`: 行程数组

## VEHICLE_SALE_INVOICE (机动车销售统一发票)
- `title`: 发票名称
- `invoiceCode`: 发票代码
- `invoiceNo`: 发票号码
- `issueDate`: 开票日期
- `buyerName`: 购方名称
- `buyerTaxId`: 购方税号
- `vehicleType`: 车辆类型
- `brandModel`: 厂牌型号
- `engineNo`: 发动机号
- `vehicleIdentificationNo`: 车辆识别代号
- `totalAmountUpper`: 价税合计大写
- `totalAmountLower`: 价税合计小写
- `sellerName`: 销方名称
- ... 等
