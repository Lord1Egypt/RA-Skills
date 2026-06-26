# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## BUSINESS_LICENSE (营业执照)
- `title`: 标题
- `socialCreditCode`: 统一社会信用代码
- `name`: 名称
- `capital`: 注册资本
- `type`: 类型
- `date`: 成立日期
- `directorType`: 负责人类型
- `director`: 负责人
- `businessTerm`: 有效日期至
- `businessScope`: 经营范围
- `address`: 住所

## SOCIAL_ORG_REG (社会团体法人登记证书)
- `title`: 标题
- `name`: 名称
- `directorType`: 负责人类型
- `director`: 负责人
- `scope`: 业务范围
- `regionAct`: 活动地域
- `capital`: 注册资金
- `address`: 住所
- `businessUnit`: 业务主管单位
- `code`: 统一社会信用代码
- `due`: 有效期限
- `issueUnit`: 发证机关
- `issueDate`: 发证日期

## TRADE_UNION_REG (工会法人资格证书)
- `title`: 标题
- `name`: 工会名称
- `address`: 住所
- `directorType`: 负责人类型
- `director`: 负责人
- `issueUnit`: 发证机关
- `due`: 有效期
- `code`: 社会统一信用代码
- `issueDate`: 发证日期

## RELIGIOUS_ACTIVITY_REG (宗教活动场所登记证)
- `title`: 标题
- `name`: 名称
- `religion`: 教别
- `orgNature`: 类别
- `directorType`: 负责人类型
- `director`: 负责人
- `address`: 地址
- `code`: 统一社会信用代码
- `religionNo`: 宗场证字
- `issueUnit`: 发证机关
- `issueDate`: 发证日期

## PRIVATE_NON_ENTERPRISE_REG (民办非企业单位登记证书)
- `title`: 标题
- `name`: 名称
- `directorType`: 负责人类型
- `director`: 法定代表人
- `address`: 住所
- `capital`: 开办资金
- `scope`: 业务范围
- `businessUnit`: 业务主管单位
- `code`: 统一社会信用代码
- `due`: 有效期限
- `issueUnit`: 发证机关
- `issueDate`: 发证日期

## INSTITUTION_LEGAL_REG (事业单位法人证书)
- `title`: 标题
- `name`: 名称
- `directorType`: 负责人类型
- `director`: 法定代表人
- `scope`: 宗旨和业务范围
- `resource`: 经费来源
- `capital`: 开办资金
- `address`: 住所
- `organizer`: 举办单位
- `code`: 统一社会信用代码
- `due`: 有效期

## UNIFIED_SOCIAL_CREDIT_REG (统一社会信用代码证书)
- `title`: 标题
- `name`: 机构名称
- `orgNature`: 机构性质
- `address`: 机构地址
- `directorType`: 负责人类型
- `director`: 负责人
- `code`: 统一社会信用代码
- `due`: 有效期至
- `issueDate`: 颁发日期
