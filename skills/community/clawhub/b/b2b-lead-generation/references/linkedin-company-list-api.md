# 领英找公司列表搜索 API 参考

> 数据来源已由接口固定为 `linkedin`（领英），调用方无需传入 `sourceNames`。
> 接口路径：`POST /agent/search/linkedin/company/list`

## python脚本参数
- `--params`: API业务参数（JSON字符串）
- `--task_id`：任务ID；用于继续之前的任务或断点续传
- `--query_count`：期望获取的总记录数；默认20；范围20~1000
- params、task_id 必须指定其一，不能同时指定

## params API业务参数

### 关键词搜索
- keywords（数组）：关键词匹配列表（涉及：公司名、公司行业、公司简介、经营范围、公司产品、公司标签）
- companyNames（数组）：公司名关键词列表
- companyNamesFilter（数组）：公司名不包含的关键词列表

### 行业与规模
- industries（数组）：行业列表
- industriesFilter（数组）：不包含的行业列表
- industriesIdFilter（整数数组）：不包含的行业 ID 列表
- companySizes（数组）：公司规模（0-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10001+）

### 成立时间
- minCompanyFounded（整数）：最早成立年（包含当前值）
- maxCompanyFounded（整数）：最近成立年（不包含当前值）

### 地理筛选
- countryCodes（数组）：国家代码列表（ISO 3166-1 alpha-2）
- countryCodesFilter（数组）：不包含的国家代码

### 联系方式筛选
- existPhone：0=全部，1=存在，2=不存在
- existWhatsApp：0=全部，1=存在，2=不存在
- existEmail：0=全部，1=存在，2=不存在
- existWebsite：0=全部，1=存在，2=不存在
- existSocial：0=全部，1=存在，2=不存在
- existValidPhone：0=全部，1=存在，2=不存在（是否有有效电话）
- existValidEmail：0=全部，1=存在，2=不存在（是否有有效邮箱）
- existValidWebsite：0=全部，1=存在，2=不存在（是否有有效官网）
- existPersonContact：0=全部，1=存在，2=不存在（是否存在核心成员联系方式）

### 排序与匹配
- sort（整数）：0=匹配度排序，1=综合排序
- isExact（布尔值）：true=精确匹配，false=模糊匹配（默认 false）

### 游标与 PIT
- cursor（字符串）：查询游标；首次请求不传
- usePit（布尔值）：是否启用 PIT 模式（大数据量翻页时更稳定）
- pitId（字符串）：PIT 游标 ID；启用 PIT 后由首次响应返回，后续请求回传

## 响应数据

### 外层结构
- code（整数）：响应码，0 表示成功
- msg（字符串）：响应消息
- data：公司列表数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段
- cursor（字符串）：下一页查询游标
- pitId（字符串）：PIT 游标 ID（启用 PIT 时返回）
- list（数组）：公司列表

### list 公司字段
- pid：公司 ID
- company_name：公司名称
- company_names：公司曾用名列表
- country_code：国家二字码
- employee：员工范围
- employee_num：员工数量
- entity_type：公司实体类型
- incorp_date：公司成立时间戳（秒级）
- revenue_usd：营收（单位千美元）
- status：公司状态 ID（1=在业，2=注销，3=吊销，4=迁出，5=经营异常）
- industries：行业描述列表
- addresses：公司地址列表（含 address 详细地址、postal_code 邮编、country_code、province_en、city_en、street、address_type_id 等）
- stock_codes：股票代码列表
- logos：公司 logo 信息
- products：产品名称列表
- tags：公司标签
- product_alias：产品近似词列表
- product_downstream：产品下游词列表
- product_superordinate：产品上游词列表
- person_contact_show：展示一条存在的员工联系方式
- phone_num：电话数量
- email_num：邮箱数量
- website_num：网址数量
- social_num：社媒数量
- ws_num：WhatsApp 数量
- rate：数据评分
- es_score：es 匹配评分
