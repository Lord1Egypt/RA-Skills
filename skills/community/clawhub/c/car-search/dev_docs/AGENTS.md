# AGENTS.md

## Project overview

car-cli 是一个二手车多平台聚合搜索 CLI 工具，当前已适配懂车帝（dongchedi.com），后续计划接入瓜子、人人车等平台。使用 Python 3.12+，CLI 框架为 Click，终端输出用 Rich，HTTP 请求用 httpx（异步）。

## Setup

**包管理器为 [uv](https://docs.astral.sh/uv/)，不使用 pip/poetry/pdm。** 构建后端为 Hatchling。

```bash
# 安装依赖 & 创建 .venv
uv sync

# 运行 CLI（推荐方式）
uv run car search --city 北京

# 添加新依赖
uv add <package>

# 添加开发依赖
uv add --dev <package>
```

不要手动 `pip install`，也不要修改 `requirements.txt`（不存在该文件）。所有依赖声明在 `pyproject.toml` 的 `[project.dependencies]`，锁文件为 `uv.lock`。

## Project structure

```
car-cli/
├── pyproject.toml              # 项目元数据、依赖、构建配置
├── uv.lock                     # uv 锁文件，提交到仓库
├── car_cli/
│   ├── main.py                 # Click CLI 入口，注册所有子命令
│   ├── logging_config.py       # 统一日志配置（输出到 stderr）
│   ├── commands/               # Click 子命令（search/detail/compare/loan/export）
│   ├── client/
│   │   ├── base.py             # BaseClient 抽象基类
│   │   ├── http.py             # HttpClient：反检测头、抖动延迟、突发限流、指数退避
│   │   └── adapters/
│   │       ├── __init__.py     # 平台注册表 + get_adapters()
│   │       └── dongchedi/      # 懂车帝适配器（自包含包）
│   │           ├── __init__.py # 导出 DongchediClient
│   │           ├── client.py   # DongchediClient 主类（URL 构建 + search/detail 入口）
│   │           ├── parser.py   # HTML / __NEXT_DATA__ 解析逻辑
│   │           ├── brands.py   # 品牌名 → 品牌 ID 映射（懂车帝专属）
│   │           └── font_decoder.py  # PUA 字体数字反混淆（懂车帝专属）
│   ├── models/
│   │   ├── car.py              # Car / CarDetail 数据类
│   │   ├── filter.py           # SearchFilter 数据类
│   │   └── cities.py           # 城市名/adcode 映射表（平台无关）
│   └── utils/                  # 通用工具（平台无关）
├── STEPS.md                    # 开发步骤记录
└── 附-懂车帝数字掩码对照表.md
```

## Code style

- Ruff 为 linter，行宽 100（`pyproject.toml` 已配置）
- Python 3.12+，使用 `list[str]` / `dict[str, str]` / `X | None` 语法，不用 `from __future__ import annotations`（除 logging_config.py 外）
- 数据模型用 `dataclasses`，不使用 Pydantic
- 异步函数限于 `client/` 层（适配器的 `search`/`detail` 方法），命令层通过 `asyncio.run()` 调用
- 日志全部通过 `car_cli.logging_config.get_logger(suffix)` 获取子 logger，输出到 stderr
- 不要在代码中写解释性注释（"这里做了什么"），只写 why 和 non-obvious 的约束

## Architecture: platform adapter pattern

每个二手车平台对应一个适配器，继承 `BaseClient`：

```python
class BaseClient(ABC):
    platform_name: str = ""

    @abstractmethod
    async def search(self, filters: SearchFilter) -> list[Car]: ...

    @abstractmethod
    async def detail(self, car_id: str) -> CarDetail: ...
```

适配器返回统一的 `Car` / `CarDetail` 数据类，上层命令不感知平台差异。

### 添加新平台适配器

1. 在 `client/adapters/` 下新建 `<platform>/` 包目录，包含 `__init__.py`、`client.py` 等
2. 在 `client.py` 中继承 `BaseClient`，实现 `search()` 和 `detail()` 方法，返回 `Car` / `CarDetail`
3. 平台专属的数据映射、反混淆逻辑等放在适配器包内部（参考 `dongchedi/brands.py`、`dongchedi/font_decoder.py`）
4. 在 `client/adapters/__init__.py` 的 `ADAPTER_REGISTRY` 中注册

## Dongchedi adapter specifics

这是目前最复杂的适配器，修改时务必注意：

### URL 槽位结构

列表页 URL 为 28 段 `-` 分隔的路径，常量定义在 `dongchedi.py` 顶部：

| 常量 | 槽位 | 含义 | 示例 |
|------|------|------|------|
| `_SLOT_PRICE` | 0 | 价格范围（万元） | `5,10` |
| `_SLOT_BRAND` | 19 | 品牌 ID | `4`（宝马） |
| `_SLOT_SERIES` | 20 | 车系 ID | `x` |
| `_SLOT_CITY` | 21 | 城市行政区划码 | `110000` |
| `_SLOT_PAGE` | 22 | 页码 | `1` |

这些槽位是通过浏览器实测校准的（见 STEPS.md），网站随时可能调整。如果搜索结果异常，先用 `--debug` 检查生成的 URL，再在浏览器中手动对比。

### 数字反混淆（PUA 字体）

懂车帝将价格、里程等数字替换为 Unicode Private Use Area 字符，由自定义字体渲染。`client/adapters/dongchedi/font_decoder.py` 中维护了一张 `_CHAR_MAP` 映射表。**如果站点更新字体映射，需要重新提取并更新这张表。**

### __NEXT_DATA__ vs HTML 回退

- `parser.parse_list()` 优先尝试从 `<script id="__NEXT_DATA__">` 提取 JSON 数据
- 当前实测发现列表页的车源数据**不在** `__NEXT_DATA__` 中（只有品牌/车系元数据），因此实际走 HTML 正则回退解析
- 详情页的数据在 `__NEXT_DATA__` 中

### 品牌 ID 映射（brands.py）

`client/adapters/dongchedi/brands.py` 中的 `BRAND_IDS` 字典包含 651 条品牌映射（含别名），从懂车帝 `__NEXT_DATA__` 的 `pageProps.brands` 字段提取（需用 Playwright 渲染页面）。更新步骤见 STEPS.md。

### 反爬措施（http.py）

`HttpClient` 内置了以下机制，不要绕过：

- **反检测请求头**：模拟 Chrome 浏览器完整的 `User-Agent` / `sec-ch-ua` / `Sec-Fetch-*` 系列头
- **高斯抖动延迟**：每次请求间加入随机延迟
- **突发检测**：短窗口（15s 内 3 次）和长窗口（45s 内 6 次）触发额外惩罚延迟
- **指数退避重试**：最多 3 次，基础 10s，上限 60s

## Debugging

```bash
# 启用调试日志（输出到 stderr）
uv run car --debug search --city 北京 --brand 宝马

# 同时启用 httpx 流量日志（极冗长）
uv run car --debug --trace-http search --city 北京

# 环境变量方式
CAR_CLI_DEBUG=1 uv run car search --city 北京
CAR_CLI_TRACE_HTTP=1 uv run car search --city 北京
```

Debug 模式会输出：请求 URL、HTTP 状态码、响应长度、解析路径选择（__NEXT_DATA__ / HTML 回退）、提取到的车源条数等。

## Testing

```bash
uv run pytest
```

测试目录为 `tests/`（在 `pyproject.toml` 中配置）。当前测试覆盖较少，添加新功能时应补充对应测试。

## Key conventions

- **所有价格单位为万元**，里程单位为万公里，在 `Car` / `SearchFilter` 数据类中已明确注释
- **城市名使用中文全称**（如"北京"、"上海"），不使用缩写或拼音
- **品牌名使用懂车帝官方中文名**，常用缩写通过 aliases 支持（如"理想" → "理想汽车"）
- **不要直接修改 `uv.lock`**，由 `uv sync` / `uv add` 自动维护
- **不要使用 `pip install`**，所有依赖管理通过 uv
- **Click 子命令**放在 `commands/` 目录下，每个文件一个命令，在 `main.py` 中注册
- **日志只用 `get_logger()`**，不要直接 `print()` 或 `logging.getLogger()`
- **CLI 入口是 `car`**（定义在 `pyproject.toml` 的 `[project.scripts]`）

## Common pitfalls

1. **curl/httpx 直接请求懂车帝可能拿不到 `__NEXT_DATA__`**：服务端对非浏览器请求可能返回精简 HTML。需要完整品牌数据时使用 Playwright
2. **PUA 字体映射是静态的**：如果提取到的价格/里程全是乱码或 `-`，说明字体映射表过期了，需要重新从字体文件提取
3. **URL 槽位可能变动**：懂车帝可能调整路径结构。如果筛选不生效，用浏览器手动点选筛选项观察 URL 变化来重新校准
4. **瓜子反爬严格**：频繁请求会触发验证码（IP 级别封锁）。搜索通常可通过，但详情页容易被拦截。详情被拦截时会返回提示信息引导用户在浏览器中查看

## 瓜子二手车适配器 (guazi/)

### 文件结构

```
client/adapters/guazi/
├── __init__.py       # 导出 GuaziClient
├── client.py         # HTTP 请求、URL 构建、验证码检测与重试
└── parser.py         # RSC 数据提取与解析
```

### RSC 数据解析

瓜子使用 Next.js App Router + React Server Components (RSC)。数据通过 `self.__next_f.push()` 调用嵌入 HTML 中，JSON 经多层转义（`\\\"key\\\"`）。

- `parser._strip_rsc_escaping()` 反复解转义直到稳定
- `parser._parse_list_regex()` 通过正则从 RSC 流中提取 `encryptedClueId`、`title`、`priceString`、`roadHaul` 等字段
- 列表数据位于 `initData.carList` 中，每个 item 包含 `skuBasicArea`（基本信息）和 `priceArea`（价格）

### 反爬与验证码

- 使用移动 UA（iPhone Safari）减少验证码触发
- `GuaziClient._fetch_with_retry()` 检测验证码并自动重试（最多 3 次，递增延迟）
- 验证码是 IP 级别的，重试可能无法绕过
- 详情页被拦截时返回友好提示而不是空数据

### 城市缩写

瓜子 URL 使用拼音缩写（`bj`、`sh`），映射在 `models/cities.py` 的 `CITY_ABBR` 字典中。

4. **城市使用 adcode 而非名称写入 URL 路径**：`models/cities.py` 中的 `CITY_ADCODE` 映射了城市中文名到 6 位行政区划码（平台无关）
5. **品牌 ID 不连续且范围大**：大部分 1-1000，部分新品牌/房车品牌在 10000+。品牌 ID 映射在 `client/adapters/dongchedi/brands.py`（懂车帝专属）
