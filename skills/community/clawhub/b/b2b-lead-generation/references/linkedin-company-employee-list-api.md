# 领英员工列表 API 参考

> 数据来源已由接口固定为 `linkedin`（领英），调用方无需传入 `sourceNames`。
> 接口路径：`POST /agent/search/linkedin/company/employee/list`

## python脚本参数

- `--pid`：公司ID（必填），如 `US_12345`
- `--cursor`：分页游标（可选），首次查询不传，翻页时传入上一次响应返回的cursor

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pid | string | 是 | 公司ID |
| cursor | string | 否 | 分页游标，首次请求传空串，翻页时传入上一次响应返回的cursor |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：员工列表数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

- cursor（string）：下一页游标，为空表示无更多数据
- list（array）：员工列表

### list 员工字段

- pid（string）：公司ID
- hid（string）：人物ID
- titleNames（array[string]）：职位名称列表（如 ["CEO", "Founder"]）
