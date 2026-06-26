# car-cli 平台适配器参考

本文档提供各平台适配器的技术细节，供需要排查问题或扩展功能时参考。

## 目录

1. [懂车帝适配器](#懂车帝适配器-dongchedi)
2. [汽车之家适配器](#汽车之家适配器-che168)
3. [瓜子适配器](#瓜子适配器-guazi)
4. [数据模型](#数据模型)
5. [反爬机制](#反爬机制-httpclient)

---

## 懂车帝适配器 (dongchedi)

### 文件结构

```
scripts/car_cli/client/adapters/dongchedi/
├── client.py        # DongchediClient — URL 构建 + search/detail/list_series
├── parser.py        # __NEXT_DATA__ 和 HTML 解析
├── brands.py        # 品牌名 → 品牌 ID 映射（651 条，含别名）
├── cities.py        # 城市中文名 → adcode 映射
└── font_decoder.py  # PUA 字体数字反混淆
```

### URL 槽位结构

列表页 URL 为 28 段 `-` 分隔的路径：

| 槽位 | 含义 | 示例 |
|------|------|------|
| 0 | 价格范围（万元） | `5,10` |
| 1–18 | 其他筛选 | `x` |
| 19 | 品牌 ID | `4`（宝马） |
| 20 | 车系 ID | `x` |
| 21 | 城市行政区划码 | `110000`（北京） |
| 22 | 页码 | `1` |
| 23–27 | 保留 | `x` |

### PUA 字体反混淆

懂车帝将价格、里程等数字替换为 Unicode Private Use Area 字符，由自定义字体渲染。`font_decoder.py` 中维护 `_CHAR_MAP` 映射表。如果站点更新字体映射，提取结果会出现乱码，需要重新提取映射表。

### 解析策略

- `parser.parse_list()` 优先尝试 `<script id="__NEXT_DATA__">` JSON
- 列表页实际走 HTML 正则回退（车源数据不在 __NEXT_DATA__ 中）
- 详情页数据在 `__NEXT_DATA__` 中

### 品牌 ID 映射 (brands.py)

651 条映射（640 个正式名称 + 11 个别名），从懂车帝 `__NEXT_DATA__` 的 `pageProps.brands` 字段提取（需 Playwright 渲染页面）。品牌 ID 为整数字符串，大部分 1-1000，部分新/小众品牌 10000+。

---

## 汽车之家适配器 (che168)

### 文件结构

```
scripts/car_cli/client/adapters/che168/
├── client.py    # Che168Client — 搜索/详情 + Cookie 反爬
├── parser.py    # HTML 数据属性 + 车辆档案解析
├── brands.py    # 品牌名 → URL slug 映射
└── cities.py    # 城市名 → 拼音 slug 映射
```

### Cookie 挑战

che168 通过 JavaScript 计算设置 Cookie 验证请求合法性，客户端自动解析并重试。

### 车源 ID 格式

汽车之家的 car_id 格式为 `<经销商ID>_<车源ID>`（如 `478339_57621125`），详情页 URL 需要经销商 ID 来构建。

### 车辆档案解析

详情页的"车辆档案"部分使用文本节点 key-value 对，`parser.py` 专门处理这种结构来提取上牌日期、里程、变速箱等字段。

---

## 瓜子适配器 (guazi)

### 文件结构

```
scripts/car_cli/client/adapters/guazi/
├── client.py    # GuaziClient — 搜索/详情 + 验证码检测与重试
├── parser.py    # RSC 数据流解析
└── cities.py    # 城市名 → 拼音缩写映射（bj, sh 等）
```

### RSC 数据解析

瓜子使用 Next.js App Router + React Server Components。数据通过 `self.__next_f.push()` 嵌入 HTML，JSON 经多层转义。

- `parser._strip_rsc_escaping()` 反复解转义直到稳定
- `parser._parse_list_regex()` 通过正则提取字段
- 列表数据在 `initData.carList` 中

### 反爬与验证码

- 使用移动 UA（iPhone Safari）减少验证码触发
- 验证码是 IP 级别的，自动重试最多 3 次
- 详情页被拦截时返回友好提示

### 默认禁用

在 `scripts/car_cli/client/adapters/__init__.py` 的 `ENABLED_PLATFORMS` 中注释掉了 `"guazi"`。启用需取消注释。

---

## 数据模型

### Car（搜索结果）

定义在 `scripts/car_cli/models/car.py`。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | str | 平台内部 ID |
| platform | str | dongchedi / che168 / guazi |
| title | str | 完整车辆标题 |
| price | float | 价格（万元） |
| brand | str | 品牌名 |
| series | str | 车系名 |
| model_year | str | 年款 |
| mileage | float | 里程（万公里） |
| first_reg_date | str | 首次上牌日期 |
| transmission | str | 自动/手动 |
| displacement | str | 排量 |
| city | str | 城市 |
| color | str | 颜色 |
| url | str | 原始链接 |
| tags | list[str] | 标签 |

### CarDetail（详情，继承 Car）

额外字段：description, emission_standard, engine_power, fuel_type, body_type, drive_type, seats, license_plate, transfer_count, annual_inspection, insurance_expiry, images, price_history

### SearchFilter

定义在 `scripts/car_cli/models/filter.py`。

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| city | str | 北京 | 城市中文名 |
| brand | str | "" | 品牌名 |
| series | str | "" | 车系名 |
| min_price / max_price | float? | None | 价格范围（万元） |
| min_mileage / max_mileage | float? | None | 里程范围（万公里） |
| min_year / max_year | int? | None | 年份范围 |
| transmission | str | "" | auto / manual |
| sort_by | str | default | default / price_asc / price_desc / mileage / date |
| page | int | 1 | 页码 |

---

## 反爬机制 (HttpClient)

定义在 `scripts/car_cli/client/http.py`，所有适配器共用。

| 机制 | 说明 |
|------|------|
| 反检测请求头 | Chrome 完整 UA + sec-ch-ua + Sec-Fetch-* |
| 高斯抖动延迟 | 均值 1s，5% 概率 2-5s 长延迟 |
| 突发检测 | 15s/3 次 → +1.2-2.8s，45s/6 次 → +4-7s |
| 指数退避重试 | 429/5xx 最多 3 次，基础 10s，上限 60s |
| 429 自适应 | 遇到 429 时 delay_multiplier ×2（上限 8x） |
