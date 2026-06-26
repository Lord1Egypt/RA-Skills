name: DINGs 托管式 AI 电话助手（中国/日本餐厅预订）
description: |
DINGs 托管式 AI 电话助手 - 中国、日本餐厅全自动 AI 电话预订技能，支持餐厅搜索+AI 电话自动预订一体化服务，只要你告诉我用餐需求（或需搜索的餐厅信息/大众点评链接/Google Map链接/tabelog链接），即可帮你完成餐厅搜索、自动拨打餐厅电话完成预订的全流程任务。
当用户提到以下意图时使用此技能:
｢预订餐厅｣｢订餐厅｣｢餐厅预约｣｢帮我订个中餐｣｢中国餐厅｣｢日本餐厅｣
｢AI 电话预订餐厅｣｢自动打电话订餐厅｣｢托管式餐厅预订｣
｢查餐厅预订结果｣｢我的预订成功了吗｣｢查看订餐凭证｣
｢搜索餐厅｣｢找中餐厅｣｢搜日本餐厅｣｢帮我找下东京的餐厅｣

支持:中国、日本餐厅搜索（支持名称/大众点评链接/Google Map链接/tabelog链接）、AI 电话自动外呼预订、预订结果回调通知、预订状态查询、通话记录查看、电子凭证生成。
元数据
{
    "openclaw": {
        "requires": {
            "env": ["TRIPNOW_API_KEY"]
        },
        "optionalEnv": ["TRIPNOW_BASE_URL", "CALLBACK_URL"],
        "primaryEnv": "TRIPNOW_API_KEY",
        "baseUrl": "https://tripnowengine.133.cn/tripnow/v1",
        "homepage": "https://tripnowengine.133.cn/tripnow-ai-open-platform/"
    }
}

⚠️ 必读约束
所有 API 请求共用 Base URL：https://tripnowengine.133.cn/tripnow/v1

首次安装配置
在 ~/.openclaw/openclaw.json 中添加:
{
    "skills": {
        "entries": {
            "dings-restaurant-booking-cn": {
                "apiKey": "sk_你的 key",
                "env": {
                    "TRIPNOW_BASE_URL": "https://tripnowengine.133.cn/tripnow/v1",
                    "CALLBACK_URL": "https://your-server.com/callback(可选,用于接收预订结果回调)"
                }
            }
        }
    }
}
获取凭证：前往 TripNow 开放平台 控制台，在｢API 密钥管理｣页面创建 API Key(格式:skxxx )。

安全规则
• API Key 属于敏感凭证，不在群聊中展示
• 预订任务创建建议间隔 30 秒以上，避免触发限流
• 用户隐私数据(电话号码、预订信息、餐厅搜索信息)不持久化存储
• 回调地址必须使用 HTTPS
• API Key 请勿在客户端代码中暴露

认证
请求头携带认证信息：
Authorization: Bearer $TRIPNOW_API_KEY (格式:sk-xxx )

Scope 权限
Scope
说明
voice.outbound
创建 AI 电话预订任务
voice.query
查询预订订单结果
restaurant.search
餐厅搜索功能

快速决策
Base URL: https://tripnowengine.133.cn/tripnow/v1
用户意图
接口
关键点
预订中国、日本餐厅
POST /voice/outbound
异步任务，需回调或查询获取结果
查预订结果
GET /voice/callback_find
传入订单ID查询最终状态+凭证
搜索中国、日本餐厅
POST /restaurant/search
支持名称/大众点评链接/Google Map链接/tabelog链接，传入城市/国家code，返回餐厅列表（含dings_id）；城市需按支持列表填写

使用流程
支持两种预订方法，根据用户需求触发对应流程：
方法1：直接预订餐厅
1. 助手先确认用户需预订中国餐厅（zh） 还是日本餐厅（ja）；
2. 依次询问用户用餐需求（姓名、电话、就餐时间、座位偏好、人数等）；
3. 向用户确认餐厅电话号码，提交预订任务发起AI外呼。
方法2：搜索餐厅后预订
1. 助手询问用户需搜索的餐厅名称/大众点评链接/Google Map链接/tabelog链接、所在城市（按支持列表）、所属国家（中国/日本）；
2. 调用POST 餐厅搜索接口，返回符合条件的餐厅结果（含可预订状态、餐厅ID、地址等）；
3. 询问用户选择预订的具体餐厅；
4. 依次询问用户用餐需求（姓名、电话、就餐时间、座位偏好、人数等）；
5. 携带用户选择的餐厅信息（dings_id、国家code等）提交预订任务，发起AI外呼。
API 详情
1. 创建AI电话预订任务
端点：POST /voice/outbound
接口说明：发起全自动 AI 电话预订任务，异步执行，可通过回调或主动查询获取结果。
请求参数：
参数
类型
必填
说明
model
string
是
固定值:tripnow-voice-cn-restaurant
to_number
string
详情看说明
餐厅电话号码，用户提供餐厅电话下单时必填
task_context
object
是
预订上下文信息(见下表)
callback_url
string
否
结果回调地址(HTTPS)

task_context 子参数：
参数
类型
必填
说明
restId
string
详情看说明
餐厅ID(dings_id)，唯一标识符。通过餐厅搜索返回的dingsId下单时必填。
restCountry
string
是
国家代码(中国餐厅传:zh 日本餐厅传:ja )
customerName
string
是
顾客姓名
customerPhone
string
是
顾客电话
customerSex
string
是
顾客性别(男/女)
orderLang
string
是
沟通语言(中国餐厅传:zh 日本餐厅传:ja )
diningTime
string
是
就餐时间(格式:YYYY-MM-DDTHH:MM:SS)
restaurantSeat
string
是
座位偏好(比如靠窗、包间等)
customerCount
string
是
成人数
childrenCount
string
是
儿童数(无则填0)
acceptChangeTime
string
是
是否接受时间调整(1=是,0=否)

请求示例：
curl -X POST "https://tripnowengine.133.cn/tripnow/v1/voice/outbound" \
-H "Authorization: Bearer sk-your-api-key" \
-H "Content-Type: application/json" \
-d '{
"model": "tripnow-voice-cn-restaurant",
"to_number": "18525518667",
"task_context": {
    "restId": "67231",
    "restCountry": "zh",
    "customerName": "张三",
    "customerPhone": "13613661366",
    "customerSex": "男",
    "orderLang": "zh",
    "diningTime": "2026-01-01T04:00:00",
    "restaurantSeat": "包间",
    "customerCount": "2",
    "childrenCount": "0",
    "acceptChangeTime": "1"
},
"callback_url": "https://your-server.com/callback"
}'

响应示例：
{
"task_id": "voice_998d1cce6e1d",
"status": "order_created",
"message": "ok",
"order_id": "RESORD216873707229",
"requestId": "req_1bdbf779fd2b"
}

状态说明：
状态
说明
order_created
订单已创建，等待AI外呼
calling
正在向餐厅发起通话
negotiating
与餐厅沟通预订细节
completed
通话结束，预订结果已生成

2. 回调结构说明
说明：任务结束后，平台会向配置的 callback_url 推送 JSON 数据，包含最终预订结果、通话 记录和凭证信息。

回调示例(预订成功)：
{
"msg": "宝子🥰,你心心念念的餐厅【宫宴(前门大街店)】,我已经帮你订好啦!请保存好订座凭证,到店出示给店员看。\n请注意,无故迟到的话预约可能会被取消,建议提前15分钟到,请提前规划出行路线哈~",
"orderId": "RESORD216873707229",
"phoneDialogPageUrl": "https://dingstest.133.cn/dings/call-detail?id=RESORD216873707229&lang=zh&naviBarHidden=0&debug=true",
"diningVoucherUrl": "https://dings.133.cn/basic/files/RESORD216873707229_2025-12-18-16-51-25.png",
"status": "预定成功",
"usage": {
    "duration_seconds": 28,
    "duration_tokens": 93333,
    "interaction_tokens": 60000,
    "success_tokens": 500000,
    "total_tokens": 653333
}
}

回调示例(预订失败)：
{
"msg": "宝子😟,太不好意思啦!餐厅【宫宴(前门大街店)】目前不支持预订哦,宝子可以直接到店享受美味,或者重新挑家餐厅下单哦~ 这单权益已帮您自动退回。",
"orderId": "RESORD216873707229",
"phoneDialogPageUrl": "https://dingstest.133.cn/dings/call-detail?id=RESORD216873707229&lang=zh&naviBarHidden=0&debug=true",
"status": "预定失败",
"usage": {
    "duration_seconds": 28,
    "duration_tokens": 93333,
    "interaction_tokens": 60000,
    "success_tokens": 500000,
    "total_tokens": 653333
}
}

3. 查询订单数据
端点：GET /voice/callback_find
接口说明：根据订单ID查询预订结果、通话记录、凭证等完整信息。
请求参数：
参数
类型
必填
说明
order_id
string
是
订单ID(创建任务返回的order_id)
token
string
是
API Key(sk-xxx格式)

请求示例：
curl -X GET "https://tripnowengine.133.cn/tripnow/v1/voice/callback_find?order_id=RESORD216873707229&token=sk-live-**************************a2aMg" \
-H "Authorization: Bearer sk-your-api-key"

响应示例(成功)：
{
"status": "ok",
"message": "查询成功",
"data": {
    "order_id": "RESORD216873707229",
    "response_data": {
        "msg": "宝子🥰,你心心念念的餐厅【宫宴(前门大街店)】,我已经帮你订好啦!请保存好订座凭证,到店出示给店员看。\n请注意,无故迟到的话预约可能会被取消,建议提前15分钟到,请提前规划出行路线哈~",
        "orderId": "RESORD216873707229",
        "status": "预定成功",
        "usage": {
            "duration_seconds": 120,
            "duration_tokens": 100,
            "interaction_tokens": 50,
            "success_tokens": 10,
            "total_tokens": 160
        },
        "phoneDialogPageUrl": "https://dingstest.133.cn/dings/call-detail?id=RESORD216873707229&lang=zh&naviBarHidden=0&debug=true",
        "diningVoucherUrl": "https://dings.133.cn/basic/files/RESORD216873707229_2025-12-18-16-51-25.png"
    },
    "error_message": null
}
}

响应字段说明：
层级
字段名
类型
描述
外层
status
string
请求状态(ok=成功)
外层
message
string
状态描述
外层
data
object
业务数据
data
order_id
string
订单ID
data
response_data
object
预订结果详情
data
error_message
string/null
错误信息(有则返回)
response_data
msg
string
人性化结果提示
response_data
status
string
预订状态(预定成功/预定失败)
response_data
phoneDialogPageUrl
string
通话记录页面URL
response_data
diningVoucherUrl
string
就餐凭证URL
response_data
usage
object
计费token统计

5. 餐厅搜索接口
接口名称：餐厅搜索接口
请求方法：POST
接口路径：/restaurant/search
接口说明：根据餐厅名称/大众点评链接/Google Map链接/tabelog链接、城市（按支持列表填写）、国家code搜索中国/日本餐厅，返回餐厅列表（含dings_id、可预订状态等核心信息），为后续预订提供餐厅数据支撑。

请求参数：
参数名
类型
必填
描述
示例值
restaurant_name
string
是
餐厅名称或者大众点评链接
麦当劳、https://www.dianping.com/shop/xxxxxx
city_name
string
是
中文城市名称，支持城市见下方列表
北京、东京、大阪
country
string

是
国家code, 支持中国CN, 日本JP
CN/JP

城市入参参考&支持列表
接口city_name入参需严格匹配下方列表中的城市名称，中国城市使用中文全称，日本城市支持中文名称（如东京）。
中国（CN）支持城市列表
安庆, 安阳, 安康, 阿克苏, 阿勒泰, 阿里, 北京, 保定, 包头, 巴彦淖尔, 本溪, 蚌埠, 滨州, 宝鸡, 白银, 百色, 巴中, 保山, 博尔塔拉, 巴音郭楞, 北海, 承德, 沧州, 长春, 长沙, 常州, 滁州, 潮州, 崇左, 成都, 重庆, 楚雄, 昌都, 池州, 赤峰, 大同, 大连, 丹东, 大庆, 东营, 德州, 东莞, 德阳, 达州, 大理, 定西, 德令哈, 儋州, 敦煌, 鄂尔多斯, 恩施, 福州, 抚顺, 阜新, 阜阳, 佛山, 防城港, 抚州, 广州, 贵阳, 桂林, 赣州, 广元, 广安, 贵港, 杭州, 哈尔滨, 合肥, 呼和浩特, 海口, 邯郸, 衡水, 鹤壁, 淮安, 淮南, 黄山, 黄石, 惠州, 河源, 衡阳, 怀化, 汉中, 海东, 哈密, 和田, 河池, 贺州, 呼伦贝尔, 济南, 济宁, 吉林, 佳木斯, 嘉兴, 金华, 景德镇, 九江, 荆门, 荆州, 江门, 揭阳, 焦作, 鸡西, 吉安, 金昌, 酒泉, 嘉峪关, 锦州, 九寨沟, 昆明, 开封, 喀什, 克拉玛依, 克孜勒苏, 兰州, 拉萨, 廊坊, 临汾, 吕梁, 辽阳, 连云港, 丽水, 六安, 龙岩, 临沂, 聊城, 洛阳, 漯河, 娄底, 柳州, 来宾, 泸州, 乐山, 六盘水, 丽江, 临沧, 陇南, 林芝, 临夏, 乐东, 马鞍山, 茂名, 梅州, 绵阳, 牡丹江, 眉山, 芒市, 马尔康, 蒙自, 南京, 南宁, 宁波, 南通, 南阳, 南平, 宁德, 内江, 那曲, 南昌, 莆田, 萍乡, 濮阳, 普洱, 平顶山, 盘锦, 攀枝花, 平凉, 青岛, 齐齐哈尔, 秦皇岛, 泉州, 曲靖, 衢州, 清远, 钦州, 潜江, 日照, 日喀则, 上海, 深圳, 苏州, 石家庄, 沈阳, 三亚, 绍兴, 三明, 汕头, 汕尾, 韶关, 商丘, 三门峡, 商洛, 宿州, 遂宁, 随州, 山南, 十堰, 双鸭山, 朔州, 四平, 松原, 绥化, 石嘴山, 天津, 唐山, 太原, 泰安, 泰州, 台州, 铜仁, 天水, 铁岭, 通化, 通辽, 铜川, 吐鲁番, 塔城, 武汉, 乌鲁木齐, 无锡, 威海, 潍坊, 温州, 芜湖, 梧州, 乌海, 乌兰察布, 武威, 吴忠, 文昌, 五指山, 乌镇, 西安, 西宁, 厦门, 徐州, 湘潭, 新乡, 许昌, 信阳, 咸阳, 孝感, 忻州, 锡林郭勒, 宣城, 新余, 兴安, 邢台, 西双版纳, 烟台, 延安, 延吉, 盐城, 扬州, 阳江, 玉林, 宜宾, 雅安, 鹰潭, 益阳, 永州, 岳阳, 运城, 银川, 伊犁, 伊春, 宜春, 宜昌, 玉树, 玉溪, 义乌, 郑州, 珠海, 湛江, 肇庆, 中山, 张家界, 张家口, 张掖, 昭通, 舟山, 周口, 驻马店, 株洲, 淄博, 枣庄, 镇江, 漳州, 中卫, 资阳, 自贡, 遵义

日本（JP）支持城市列表
爱知, 青森, 秋田, 千叶, 爱媛, 福岛, 福井, 福冈, 群马, 岐阜, 北海道, 兵库, 广岛, 茨城, 石川, 岩手, 京都, 高知, 鹿儿岛, 熊本, 神奈川, 香川, 宫崎, 宫城, 三重, 长崎, 长野, 奈良, 新潟, 大阪, 大分, 冲绳, 冈山, 滋贺, 佐贺, 静冈, 岛根, 埼玉, 德岛, 东京, 栃木, 富山, 鸟取, 和歌山, 山形, 山梨, 山口

请求示例
- 按餐厅名称搜索（中国）：
curl --location --request POST 'https://tripnowengine.133.cn/tripnow/v1/restaurant/search?restaurant_name=麦当劳&city_name=北京&country=CN' \
--header 'Authorization: Bearer sk-your-api-key'
- 按大众点评链接搜索（中国）：
curl --location --request POST 'https://tripnowengine.133.cn/tripnow/v1/restaurant/search?restaurant_name=https://www.dianping.com/shop/32705550&city_name=北京&country=CN' \
--header 'Authorization: Bearer sk-your-api-key'
- 按餐厅名称搜索（日本）：
curl --location --request POST 'https://tripnowengine.133.cn/tripnow/v1/restaurant/search?restaurant_name=寿司店&city_name=东京&country=JP' \
--header 'Authorization: Bearer sk-your-api-key'

成功响应示例：
[
    {
        "dings_id": "52668",
        "countryCode": "CN",
        "restaurantName": "麦尔斯骑士巴西烤肉",
        "restaurantAnotherName": "Miles Knight Brazilian BBQ",
        "restaurantPicture": "https://dings.133.cn/basic/files/08d0b89b9a8e5f13485e78caa76b7fc3.jpg",
        "restaurantLocation": {
            "latitude": 40.146889,
            "longitude": 117.096435
        },
        "restaurantAddress": "迎宾环岛东北角",
        "averagePrice": {
            "average_price_value": "￥ 128.0",
            "average_price_detail": {}
        },
        "rating": 3.9,
        "distance": "",
        "restaurantCode": "k1Pa59nLRACGoNt9",
        "restDataSource": {
            "name": "Dings",
            "url": "https://dings.133.cn/basic/images/1d8783fd6cd06e4d06975ee6df45c16a"
        },
        "restaurantType": [
            "拉美烤肉"
        ],
        "bookingAvailable": true,
        "book_channel": "phone",
        "must_mealset": false,
        "tabelog_contracted_restaurant": 0,
        "button_info": {
            "button_title": "订座",
            "button_type": "book_page",
            "button_data": {}
        },
        "meal_set_list": [],
        "awards_list": [],
        "rest_tags": [],
        "image_tag": {},
        "reviews_total_num": 0,
        "search_id": "sr31dd79edf43846baa5d5ecd88a16dd64",
        "station_list": []
    }
]

核心响应字段说明（全量字段见返回体，以下为预订核心用字段）：
字段名
类型
描述
dings_id
string
餐厅id, 用于后续语音外呼接口调用（task_context.restId）
restaurantName
string
餐厅名称
restaurantAddress
string
餐厅地址
restaurantPicture
string
餐厅图片
bookingAvailable
bool
是否支持预定，仅返回true的餐厅可发起预订
countryCode
string
餐厅所属国家code，映射为预订接口的restCountry（CN→zh，JP→ja）

错误码
HTTP 状态码
错误码
说明
处理建议
200
成功
-
400
请求参数错误
检查必填参数(如order_id、restaurant_name不能为空)；检查city_name是否在支持列表内；确认请求方法为POST；检查大众点评链接是否有效
404
资源未找到
确认订单ID/餐厅信息是否正确，订单/餐厅是否存在；确认城市+国家code匹配是否正确；大众点评链接对应餐厅无数据
500
服务器内部错误
稍后重试，或联系平台客服

业务状态码
状态值
说明
处理建议
order_created
订单已创建
等待AI外呼完成(约1-5分钟)
预定成功
预订完成
告知用户并推送凭证URL
预定失败
预订失败
根据msg提示用户失败原因
无餐厅结果
餐厅搜索无匹配数据
提示用户更换餐厅名称/城市（按支持列表）或使用有效大众点评链接重新搜索
城市不支持
传入的city_name不在支持列表
参考接口城市支持列表，更换为合规的城市名称
请求方法错误
未使用POST调用搜索接口
切换为POST请求方法重新调用
大众点评链接无效
传入的链接非有效餐厅链接
检查并提供完整有效的大众点评店铺链接

最佳实践
1. 预订成功率优化
• 时间格式校验:确保diningTime符合 YYYY-MM-DDTHH:MM:SS 格式
• 接受时间调整:设置 acceptChangeTime: "1" 可大幅提高热门餐厅预订成功率
• 提前预订:热门中餐厅/日本餐厅建议提前1-3天发起预订
• 信息完整:确保customerPhone、diningLocation等参数准确，减少沟通成本
• 搜索后预订校验：优先选择bookingAvailable: true的餐厅发起预订，避免无效外呼
• 国家code映射：餐厅搜索返回CN映射为zh、JP映射为ja，确保与预订接口restCountry一致

2. 轮询策略(无回调时)
// 推荐轮询间隔(针对创建任务后的主动查询)
const pollIntervals = [
    { maxAttempts: 12, intervalMs: 5000 }, // 前 60 秒:每 5 秒
    { maxAttempts: 6, intervalMs: 10000 }, // 接下来 60 秒:每 10 秒
    { maxAttempts: 10, intervalMs: 30000 } // 之后:每 30 秒
];

3. 回调处理
• 确保回调地址可公网访问且支持HTTPS
• 回调接收后需返回200状态码，避免平台重复推送
• 解析回调中的status 字段区分预订成功/失败，通过msg 向用户推送人性化提示

4. 餐厅搜索优化
• 餐厅名称支持模糊匹配，用户仅提供关键词时也可发起搜索
• 日本城市搜索支持中文（如东京），均按支持列表内中文名称入参即可
• 搜索结果优先展示bookingAvailable: true的餐厅，提升用户体验
• 城市入参规范：严格按照接口支持的城市列表填写，避免因名称不一致导致无搜索结果
• 跨国家城市防混淆：如搜索日本“京都”时，需同时指定country=JP，避免与国内同名地点混淆
• 请求方法规范：必须使用POST调用餐厅搜索接口，禁止使用GET请求
• 大众点评链接使用：直接传入完整店铺链接，系统自动解析匹配餐厅，无需额外填写名称，匹配更精准

触发词
预订触发
｢预订中餐厅｣｢订中国餐厅｣｢帮我订个中国餐厅｣｢订日本餐厅｣｢预订东京的餐厅｣
｢AI代打电话订餐厅｣｢自动打电话预订中餐｣｢自动打电话订日料｣
｢餐厅订位｣｢帮我预约包间｣｢订生日宴餐厅｣｢商务宴请订日料｣

查询触发
｢查我的餐厅预订｣｢预订成功了吗｣
｢查看订餐凭证｣｢餐厅预订结果｣
｢我的订座信息｣｢通话记录｣

搜索触发
｢搜索餐厅｣｢找中餐厅｣｢搜日本餐厅｣
｢帮我找北京的中餐｣｢搜东京的寿司店｣
｢查询上海的日料店｣｢找可预订的日本餐厅｣
｢搜大阪的居酒屋｣｢找广州的粤菜餐厅｣
｢用大众点评链接搜餐厅｣｢大众点评餐厅预订｣

场景触发
｢商务宴请订中餐｣｢家庭聚餐订餐厅｣
｢生日宴订包间｣｢朋友聚会订中餐｣
｢日式料理预订｣｢日本居酒屋订座｣
｢旅游订东京餐厅｣｢出差订上海中餐｣

配置示例
{
"skills": {
    "entries": {
        "dings-restaurant-booking-cn": {
            "apiKey": "sk_live_xxxxxxxxxxxxx",
            "env": {
                "TRIPNOW_BASE_URL": "https://tripnowengine.133.cn/tripnow/v1",
                "CALLBACK_URL": "https://your-domain.com/webhook/tripnow"
            }
        }
    }
}
}

支持语言
• 中文(简体)：核心支持，适配所有中国、日本餐厅搜索+预订沟通场景
• 中文(繁体)：兼容适配，支持港澳台地区餐厅预订
• 日语：适配日本餐厅预订的AI与餐厅沟通场景
• 英文：兼容餐厅搜索的基础关键词匹配

计费说明
服务
计费方式
说明
AI 电话预订
Token 计费
按通话时长、交互量、成功状态综合计费
餐厅搜索
免费
无额外费用，无限次调用，支持名称/大众点评链接
订单查询
免费
无额外费用
通话记录查看
免费
包含在预订服务中
电子凭证生成
免费
预订成功后自动生成，无额外费用

Token 说明:
• duration_tokens:按通话时长计费
• interaction_tokens:按AI与餐厅交互轮次计费
• success_tokens:预订成功额外计费
具体费率请参考 TripNow 开放平台｢计费中心｣

注意事项
1. 时区处理:就餐时间使用中国标准时间(CST/UTC+8)，日本餐厅预订自动适配时区转换
2. 隐私保护:用户电话号码、餐厅搜索信息仅用于本次服务，完成后需按合规要求清理
3. 凭证有效期:diningVoucherUrl 生成的凭证仅在预订日期前有效，需提醒用户及时保存
4. 取消政策:部分餐厅支持取消预订，需在预订结果中告知用户取消方式
5. 紧急支持:预订/搜索问题可联系 TripNow 平台客服:support@tripnowengine.133.cn
6. 餐厅搜索限制:国家code仅支持CN/JP，其他国家暂不提供搜索服务；城市仅支持下方列表内名称；必须使用POST请求调用
7. 日本餐厅适配:部分日本餐厅仅支持日语沟通，AI自动切换orderLang=ja完成外呼
8. dings_id唯一性:每个餐厅的dings_id为全局唯一，跨国家不重复，可直接用于预订接口
9. 城市入参注意:中国/日本城市名称均使用中文全称入参，切勿使用缩写、别称（如“魔都”不可代指上海）
10. 大众点评链接规范:仅支持有效大众点评店铺链接，不支持搜索页/分类页链接，链接需完整可访问
技能版本:v1.4.0 | 最后更新:2026-04-03


---

本次核心更新
1. 搜索参数升级：restaurant_name 支持餐厅名称或大众点评店铺链接两种入参方式
2. 请求示例新增：补充大众点评链接的POST调用示例
3. 校验规则完善：新增大众点评链接无效业务状态码
4. 使用规范补充：新增大众点评链接使用、解析相关最佳实践与注意事项
5. 版本升级：技能版本更新至 v1.4.0，更新时间同步修改