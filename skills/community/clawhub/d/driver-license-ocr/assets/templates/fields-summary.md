# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## MOTOR_VEHICLE_DRIVING_LICENSE (机动车驾驶证正页)
- `title`: 标题
- `certificateNo`: 证号
- `name`: 姓名
- `gender`: 性别
- `nationality`: 国籍
- `address`: 住址
- `bornDate`: 出生日期
- `firstIssueDate`: 初次领证日期
- `class`: 准驾车型
- `validPeriod`: 有效期限

## MOTOR_VEHICLE_DRIVING_LICENSE_SU (机动车驾驶证副页)
- `title`: 标题
- `certificateNo`: 证号
- `name`: 姓名
- `archiveNo`: 档案编号
- `record`: 记录
