# 全球企业库找人列表搜索 API 参考

> 数据来源已由接口固定为 `depth_company`（全球企业库），调用方无需传入 `sourceNames`。
> 接口路径：`POST /agent/search/depth_company/person/list`

## python脚本参数
- `--params`: API业务参数（JSON字符串）
- `--task_id`：任务ID；用于继续之前的任务或断点续传
- `--query_count`：期望获取的总记录数；默认20；范围20~1000
- params、task_id 必须指定其一，不能同时指定

## params API业务参数

### 关键词搜索
- keywords（数组）：关键词匹配列表（涉及：人名、公司名、人物行业、公司行业、人物简介、职位、角色、职级、学位、兴趣爱好、技能字段）
- humanNames（数组）：人物名关键词列表
- humanNamesFilter（数组）：人物名不包含的关键词列表
- companyNames（数组）：公司名关键词列表
- companyNamesFilter（数组）：公司名不包含的关键词列表
- humanUrls（数组）：人物链接（官网、领英）列表

### 行业筛选
- humanIndustries（数组）：人物行业列表
- humanIndustriesFilter（数组）：不包含的人物行业列表
- companyIndustries（数组）：公司行业列表
- companyIndustriesFilter（数组）：不包含的公司行业列表

### 地理筛选
- countryCodes（数组）：国家代码列表（ISO 3166-1 alpha-2）
- countryCodesFilter（数组）：不包含的国家代码

### 联系方式筛选
- existPhone：0=全部，1=存在，2=不存在
- existWhatsApp：0=全部，1=存在，2=不存在
- existEmail：0=全部，1=存在，2=不存在
- existWebsite：0=全部，1=存在，2=不存在
- existSocial：0=全部，1=存在，2=不存在

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
- data：人物列表数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段
- cursor（字符串）：下一页查询游标
- pitId（字符串）：PIT 游标 ID（启用 PIT 时返回）
- list（数组）：人物列表

### list 人物字段
- hid：人物唯一标识
- pid：公司唯一标识
- human_name：人物名称
- company_name：公司名称
- country_code：人物所属国家 ISO 代码
- title_names：职位名称列表
- title_levels：职位级别列表
- employee：公司员工人数范围
- experience_num：工作经历次数
- human_industries：人物行业描述列表
- company_industries：公司行业描述列表
- gender：性别（F=女性，M=男性）
- human_type：人物类型（0=未检测，1=个人，2=公司，3=不确定）
- phone_num：电话数量
- email_num：邮箱数量
- website_num：网址数量
- social_num：社媒数量
- ws_num：WhatsApp 数量
- exist_company_website：是否有公司官网（1=存在，2=不存在）
- rate：数据评分
- es_score：es 匹配评分
