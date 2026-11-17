# 商场数据包口径

`GET /ddtclaw/v1/malls/search?q=名称&city=城市` 返回候选，仅用于定位，最多20条；`truncated`为真时补充名称或城市。
`GET /ddtclaw/v1/malls/bundle?mall_id=标识&radius_m=1000` 返回完整包。使用Bearer Key；请求编号在X-Request-Id和成功响应request_id中。

模块：mall商场档案；shops全部场内门店；floors楼层计数和关联门店标识；brands品牌商场覆盖；brand_cooccurrence品牌伴生；city_benchmark城市参照；city_categories同城二级业态；competition相似商场与补位；surroundings指定半径周边楼盘与商场；events已收录活动；opinion缓存舆情；coverage完整性与模块可用情况。

- shops包含设施点位，facility用于识别设施；商场门店总数遵循发布口径，不擅自剔除后仍沿用总数。
- floor_no为负表示地下层，null表示楼层未标注，跨层以floor_span表示。
- hits为浏览热度；heat_index为同城指标综合指数，均不是实际客流、收入或租金。
- avg_price与food_price_median是已有消费价格指标；price为楼盘单价，单位元/平方米；property_fee单位元/平方米/月；households为已有户数，不是实时人口。
- chain_rate、open_rate、各类分位与co_rate为百分数口径。连锁依据已发布商场样本判定；品牌national数量仅代表该样本的商场覆盖，不代表全国所有街边店。
- 坐标使用GCJ-02；周边按直线距离筛选，不等同驾车距离。半径外数据不属于本次完整包。
- similar、gap_l2、gap_brand是相似商场参照下的比较结果，不等同已确认招商需求或空铺。
- 空数组表示本模块没有返回记录；null表示缺失，不能解读为0。opinion_available=false时不可宣称“没有负面舆情”。
- events的match_method区分名称/距离关联与仅距离关联，周边活动不能直接声称由商场主办。
- 完整仅指当前已发布数据和已收录舆情，不保证所有现实门店或所有互联网内容均覆盖。
