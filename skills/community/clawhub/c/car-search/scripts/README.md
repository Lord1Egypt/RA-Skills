# 🚗 car-cli — 二手车多平台聚合搜索 CLI

从多个二手车平台聚合搜索、查看详情、对比车源，所有操作都在终端完成。

## 支持平台

| 平台 | 标识 | 搜索 | 详情 | 车系查询 |
|------|------|:----:|:----:|:--------:|
| [懂车帝](https://www.dongchedi.com) | `dongchedi` | ✅ | ✅ | ✅ |
| [汽车之家二手车](https://www.che168.com) | `che168` | ✅ | ✅ | ✅ |
| [瓜子二手车](https://www.guazi.com) | `guazi` | ✅ | ✅ | ❌ |
| [优信拍](https://www.youxinpai.com) | `youxinpai` | ✅ | ✅ | ✅ |

---

## 环境要求

- **Python** 3.12+
- **[uv](https://docs.astral.sh/uv/)** — 包管理器（不使用 pip/poetry）

## 安装

```bash
# 安装依赖并创建虚拟环境
uv sync
```

安装完成后，`car` 命令即可使用：

```bash
uv run car --help
```

---

## 快速开始

```bash
# 全平台搜索宝马，10 万以内
uv run car search --brand 宝马 --max-price 10

# 查看某辆车的详情
uv run car detail dongchedi:22805067

# 对比两辆车
uv run car compare dongchedi:22805067 che168:478339_57621125

# 查看宝马有哪些车系
uv run car series 宝马

# 贷款计算
uv run car loan --total 15 --down-payment 0.3 --years 3
```

---

## 命令详解

### 全局选项

所有子命令前均可使用：

```
car [全局选项] <子命令> [命令选项]
```

| 选项 | 说明 |
|------|------|
| `--debug` / `-d` | 启用调试日志（输出到 stderr），显示请求 URL、解析步骤等 |
| `--trace-http` | 启用 httpx 流量级日志（极其冗长），自动开启 `--debug` |
| `--version` | 显示版本号 |
| `--help` | 显示帮助 |

也可通过环境变量启用：

```bash
CAR_CLI_DEBUG=1 uv run car search --brand 丰田
CAR_CLI_TRACE_HTTP=1 uv run car search --brand 丰田
```

---

### `car search` — 搜索二手车

聚合搜索多个平台的二手车源，以表格形式展示结果。

```bash
uv run car search [选项]
```

#### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--city` | `全国` | 城市名称（中文），如 `北京`、`上海`、`广州` |
| `--brand` | 无 | 品牌名称，如 `宝马`、`丰田`、`比亚迪` |
| `--series` | 无 | 车系名称，如 `3系`、`卡罗拉`（需配合 `--brand` 使用） |
| `--min-price` | 无 | 最低价格（万元） |
| `--max-price` | 无 | 最高价格（万元） |
| `--min-mileage` | 无 | 最低里程（万公里） |
| `--max-mileage` | 无 | 最高里程（万公里） |
| `--min-year` | 无 | 最早年份，如 `2020` |
| `--max-year` | 无 | 最晚年份，如 `2024` |
| `--transmission` | 无 | 变速箱类型：`auto` / `manual` |
| `--platform` | `all` | 指定平台：`dongchedi`、`guazi`、`che168`、`youxinpai`、`all` |
| `--sort` | `default` | 排序方式：`price_asc`、`price_desc`、`mileage`、`date` |
| `--output` | `table` | 输出格式：`table`、`json`、`yaml` |
| `--page` | `1` | 页码 |

#### 示例

```bash
# 北京地区 5-10 万的宝马
uv run car search --city 北京 --brand 宝马 --min-price 5 --max-price 10

# 只搜懂车帝，按价格升序排列
uv run car search --brand 丰田 --platform dongchedi --sort price_asc

# 按车系筛选（懂车帝 / che168）
uv run car search --brand 宝马 --series 3系 --platform che168

# 优信拍：搜索拍卖车源
uv run car search --city 上海 --platform youxinpai

# 优信拍：品牌 + 车系筛选（动态从平台 API 获取车系 ID）
uv run car search --brand 宝马 --series 3系 --platform youxinpai

# 输出为 JSON
uv run car search --brand 比亚迪 --output json
```

> **提示**：搜索结果会自动缓存，可用 `car export` 导出。

---

### `car detail` — 查看车源详情

根据搜索结果中的车源 ID 查看详细信息。

```bash
uv run car detail <platform:id> [选项]
```

#### 参数

- `CAR_ID`：车源 ID，格式为 `平台:ID`，从搜索结果的 ID 列获取。

#### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--output` | `table` | 输出格式：`table`、`json`、`yaml` |

#### 示例

```bash
# 懂车帝详情
uv run car detail dongchedi:22805067

# 汽车之家详情（ID 包含经销商前缀）
uv run car detail che168:478339_57621125

# 优信拍详情（ID 格式为 auctionId_crykey，从搜索结果复制）
uv run car detail youxinpai:8224454_182f89

# 输出为 YAML
uv run car detail dongchedi:22805067 --output yaml
```

#### 展示字段

标题、价格、品牌、车系、年款、里程、首次上牌、变速箱、排量、燃料类型、车身类型、驱动方式、排放标准、颜色、车源城市、过户次数、链接。

---

### `car compare` — 对比两辆车

并排对比两辆车的关键参数，支持跨平台对比。

```bash
uv run car compare <platform:id1> <platform:id2> [选项]
```

#### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--output` | `table` | 输出格式：`table`、`json`、`yaml` |

#### 示例

```bash
# 跨平台对比
uv run car compare dongchedi:22805067 che168:478339_57621125

# 同平台对比
uv run car compare dongchedi:22805067 dongchedi:23150603
```

---

### `car series` — 查询品牌车系

查询某个品牌下可用的车系列表，方便使用 `--series` 进行精确筛选。

```bash
uv run car series <品牌名> [选项]
```

#### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--platform` | `dongchedi` | 指定平台（当前懂车帝、che168、优信拍支持车系查询） |

#### 示例

```bash
# 查看宝马的所有车系
uv run car series 宝马

# 查看比亚迪的车系
uv run car series 比亚迪

# 然后按车系筛选搜索
uv run car search --brand 宝马 --series 3系
```

---

### `car loan` — 车贷计算器

支持等额本息和等额本金两种还款方式。

```bash
uv run car loan [选项]
```

#### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--total` | 必填 | 车辆总价（万元） |
| `--down-payment` | `0.3` | 首付比例（0-1） |
| `--years` | `3` | 贷款年限 |
| `--rate` | `4.0` | 年利率（%） |
| `--method` | `equal_principal_interest` | 还款方式：`equal_principal_interest`（等额本息）/ `equal_principal`（等额本金） |

#### 示例

```bash
# 15 万的车，首付 30%，3 年期
uv run car loan --total 15 --down-payment 0.3 --years 3

# 等额本金，自定义利率
uv run car loan --total 20 --method equal_principal --rate 3.5 --years 5
```

---

### `car export` — 导出搜索结果

将上一次 `car search` 的结果导出为 CSV 或 JSON 文件。

```bash
uv run car export [选项]
```

#### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--format` | `csv` | 导出格式：`csv` / `json` |
| `-o` / `--output` | stdout | 输出文件路径，留空则输出到终端 |

#### 示例

```bash
# 先搜索
uv run car search --brand 丰田 --city 北京

# 导出为 CSV 文件
uv run car export --format csv -o result.csv

# 导出为 JSON 到终端
uv run car export --format json
```

---

## 平台管理

### 启用 / 禁用平台

编辑 `car_cli/client/adapters/__init__.py` 中的 `ENABLED_PLATFORMS` 列表：

```python
ENABLED_PLATFORMS: list[str] = [
    "dongchedi",
    # "guazi",       # ← 注释掉 = 禁用
    "che168",
    "youxinpai",
]
```

`--platform all` 时只搜索 `ENABLED_PLATFORMS` 中未注释的平台。指定具体平台名称时不受此限制。

---

## 调试指南

```bash
# 启用调试日志
uv run car --debug search --city 北京 --brand 宝马

# 同时启用 HTTP 流量日志
uv run car --debug --trace-http search --city 北京
```

调试日志输出到 stderr，包含：

- 请求构建的完整 URL
- HTTP 状态码和响应长度
- 解析路径选择（__NEXT_DATA__ / HTML 回退 / 车辆档案）
- 提取结果数量
- 品牌/车系 ID 匹配过程

---

## 项目结构

```
car-cli/
├── pyproject.toml                  # 项目配置、依赖、构建
├── uv.lock                         # uv 锁文件
├── car_cli/
│   ├── main.py                     # CLI 入口，注册所有子命令
│   ├── logging_config.py           # 统一日志配置
│   ├── commands/                   # CLI 子命令
│   │   ├── search.py               # 多平台聚合搜索
│   │   ├── detail.py               # 车源详情
│   │   ├── compare.py              # 车源对比
│   │   ├── series.py               # 品牌车系查询
│   │   ├── loan.py                 # 车贷计算器
│   │   └── export.py               # 导出搜索结果
│   ├── client/
│   │   ├── base.py                 # BaseClient 抽象基类
│   │   ├── http.py                 # HttpClient（反检测、限流、重试）
│   │   └── adapters/
│   │       ├── __init__.py         # 平台注册表 + ENABLED_PLATFORMS
│   │       ├── dongchedi/          # 懂车帝适配器
│   │       │   ├── client.py       # 搜索/详情/车系查询
│   │       │   ├── parser.py       # __NEXT_DATA__ + HTML 解析
│   │       │   ├── brands.py       # 品牌 ID 映射（651 条）
│   │       │   ├── cities.py       # 城市 adcode 映射
│   │       │   └── font_decoder.py # PUA 字体数字反混淆
│   │       ├── che168/             # 汽车之家适配器
│   │       │   ├── client.py       # 搜索/详情 + Cookie 反爬
│   │       │   ├── parser.py       # HTML 数据属性 + 车辆档案解析
│   │       │   ├── brands.py       # 品牌 URL slug 映射
│   │       │   └── cities.py       # 城市拼音 slug 映射
│   │       ├── guazi/              # 瓜子适配器
│   │       │   ├── client.py       # 搜索/详情 + 验证码检测
│   │       │   ├── parser.py       # RSC 数据流解析
│   │       │   └── cities.py       # 城市拼音缩写映射
│   │       └── youxinpai/          # 优信拍适配器
│   │           ├── client.py       # 搜索/详情 + Session 初始化
│   │           ├── parser.py       # JSON API + HTML 详情解析
│   │           ├── cities.py       # 城市 ID 映射（动态加载）
│   │           └── city_list.json  # 优信拍城市数据（560 城）
│   └── models/
│       ├── car.py                  # Car / CarDetail 数据类
│       ├── filter.py               # SearchFilter 数据类
│       └── cities.py               # 通用城市名列表
```

---

## 注意事项

1. **反爬限制**：各平台均有反爬措施。工具内置了请求头伪装、随机延迟、突发限流和指数退避机制，请勿频繁调用。
2. **瓜子验证码**：瓜子反爬较严格，IP 级别封锁。搜索通常可通过，详情页容易被拦截。
3. **懂车帝数字混淆**：价格/里程使用 PUA 字体渲染，`font_decoder.py` 维护映射表。如提取结果异常（全是乱码），可能需要更新映射。
4. **汽车之家 Cookie 挑战**：站点通过 JS 计算设置 Cookie，客户端会自动解析并重试。车系筛选通过动态解析品牌页的拼音 slug 选项实现。
5. **优信拍 Session 认证**：API 需要先访问交易页面获取 `csrfToken` / `jwt_token` Cookie，客户端会自动完成此步骤（每次搜索多一次 GET 请求）。`car_id` 格式为 `auctionId_crykey`，两者缺一不可。车系筛选通过平台品牌 API 动态查询（无需预先第三方映射表）。详情页读取价格、里程、颗色、上牌日期、过户次数、车辆描述等字段。
6. **价格单位**：统一为**万元**，里程单位为**万公里**。

---

## License

MIT
