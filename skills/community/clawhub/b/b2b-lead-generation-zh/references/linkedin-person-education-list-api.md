# LinkedIn人物教育经历列表 API 参考

> 根据人物ID获取某人的教育经历列表，支持游标翻页。
> 接口路径：`POST /agent/search/linkedin/person/education/list`

## python脚本参数

- `--hid`：人物ID（必填），如 `H_67890`
- `--cursor`：分页游标（可选），首次查询不传，翻页时传入上一次响应返回的cursor

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hid | string | 是 | 人物ID |
| cursor | string | 否 | 分页游标，首次请求不传，翻页时传入上一次响应返回的cursor |
| limit | integer | 否 | 每页条数，默认20 |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：教育经历列表数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

- cursor（string）：下一页游标，为空表示无更多数据
- list（array）：教育经历列表

### list 教育经历字段

- hid（string）：人物ID
- sid（string）：学校ID
- startDate（integer）：开始时间（秒级时间戳）
- endDate（integer）：结束时间（秒级时间戳）
- degrees（array[string]）：学业程度列表
- majors（array[string]）：专业列表
- minors（array[string]）：辅修科目列表
- gpa（string）：平均学分绩点
- summary（string）：总结
