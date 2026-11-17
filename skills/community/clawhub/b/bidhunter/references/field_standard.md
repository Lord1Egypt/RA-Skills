# 标讯字段标准化 Schema

## 核心字段定义

| 字段名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| `bid_id` | string | 标讯唯一标识（平台+原始ID） | `cnooc_12345` |
| `source_platform` | string | 来源平台编码 | `cnooc` |
| `source_url` | string | 原始链接 | `https://...` |
| `title` | string | 项目名称 | `渤海某油田FPSO工程EPC总包` |
| `content_text` | string | 正文纯文本（前5000字） | `...` |
| `content_html` | string | 原始HTML（存档） | `...` |
| `publish_time` | string | 公告发布时间（ISO 8601） | `2024-03-01T10:00:00+08:00` |
| `deadline_time` | string | 投标截止时间 | `2024-03-15T09:00:00+08:00` |
| `bid_open_time` | string | 开标时间 | `2024-03-15T09:30:00+08:00` |
| `budget_amount` | number | 预算金额（元，标准化） | `420000000` |
| `budget_amount_raw` | string | 原始金额字符串 | `4.2亿元` |
| `currency` | string | 币种 | `CNY` |
| `purchaser_name` | string | 采购单位名称（标准化） | `某某有限公司天津分公司` |
| `purchaser_address` | string | 采购单位地址 | `天津市滨海新区...` |
| `purchaser_contact` | string | 联系人及方式 | `张三 022-XXXX` |
| `agency_name` | string | 招标代理机构 | `某某招标有限公司` |
| `bid_type` | string | 项目类型编码 | `engineering` / `goods` / `service` |
| `bid_method` | string | 采购方式编码 | `public_tender` / `invitation` / `inquiry` |
| `region_code` | string | 地区编码（国家统计局6位码） | `120116` |
| `industry_code` | string | 行业编码 | `B07` |
| `qualification_requirements` | array | 资质要求 | `["一级资质", "安全生产许可证"]` |
| `attachment_list` | array | 附件清单 | `[{"name": "招标文件.pdf", "size": 10240000, "url": "..."}]` |
| `status` | string | 标讯状态 | `new` / `updated` / `expired` / `opened` / `cancelled` |
| `crawl_time` | string | 采集时间 | `2024-03-01T10:05:00+08:00` |
| `crawl_version` | string | 解析规则版本 | `1.0` |

## 判定结果字段

| 字段名 | 类型 | 说明 | 取值 |
|---|---|---|---|
| `verdict` | string | 资质判定结果 | `investable` / `not_investable` / `needs_review` / `skip` |
| `reason` | string | 判定原因 | `主体能力匹配：广告, 活动` / `红色预警：建筑施工` |
| `assigned_entity` | string | 归属投标主体 | `entity_a` / `entity_b` |
| `assigned_entity_name` | string | 归属投标主体名称 | `主体A（传媒/活动类）` |
| `matched_capabilities` | array | 匹配到的能力词 | `["广告", "活动策划"]` |
| `region_info` | object | 地区信息 | `{"is_priority": true, "region": "天津"}` |

## 金额标准化规则

原始金额字符串 → 标准化元数值：

| 原始格式 | 标准化结果 |
|---|---|
| `4.2亿元` | `420000000` |
| `500万元` | `5000000` |
| `300万` | `3000000` |
| `1.2亿` | `120000000` |
| `未填写` / 空 | `null` |

## 地区编码

使用国家统计局 6 位行政区划编码：

| 编码 | 地区 |
|---|---|
| `110000` | 北京市 |
| `120000` | 天津市 |
| `310000` | 上海市 |
| `440000` | 广东省 |
| `510000` | 四川省 |
| ... | ... |

完整编码表参考国家统计局最新版行政区划代码。

## 行业分类编码

采用 GB/T 4754《国民经济行业分类》：

| 编码 | 行业 |
|---|---|
| `B07` | 石油和天然气开采业 |
| `B08` | 黑色金属矿采选业 |
| `E48` | 土木工程建筑业 |
| `I63` | 电信、广播电视和卫星传输服务 |
| ... | ... |
