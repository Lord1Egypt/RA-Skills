# FlyClaw - 航班信息聚合查询 CLI 工具

**FlyClaw** 是一个轻量级命令行工具，基于多源聚合架构，通过开源库及免费公开 API 获取数据，在终端中聚合查询航班信息（航班动态、价格、时刻等），原生支持中英文查询，原生OpenClaw技能，覆盖中国国内及国际航班。轻量化python实现，非浏览器模拟的复杂和低效方式。

**FlyClaw** is a lightweight command-line tool that aggregates flight information (dynamics, prices, schedules, etc.) using a multi-source aggregation architecture powered by open-source libraries and free public APIs, with native Chinese/English query support and native OpenClaw skill integration, covering both Chinese domestic and international flights. Lightweight Python implementation — no browser automation, no complexity, no overhead.

核心价值：单一来源不稳定、不完整、覆盖有限 -- FlyClaw 的目标是**聚合、去重、补齐、呈现**。

Core value: A single data source is unreliable, incomplete, and limited in coverage -- FlyClaw's value lies in **aggregation, deduplication, gap-filling, and presentation**.

[English Readme](README_EN.md)

**作者**：nuaa02@gmail.com 小红书@深度连接
**GitHub**：[https://github.com/AI4MSE/FlyClaw](https://github.com/AI4MSE/FlyClaw)
**许可证**：[Apache-2.0](LICENSE)

## 功能特性

- **零 API Key 依赖**：无需注册账号，开箱即用，安全，同时规避浏览器模拟等复杂、不可靠和低速问题
- **多数据源聚合**：飞猪(Fliggy)、Google Flights、Skiplagged、FR24、Airplanes.live 五大数据源并发查询，通过开源库及免费公开 API 获取航班动态、价格、实时位置。**插件式架构，支持无限扩展**——每个数据源为独立模块（`sources/` 目录下一个文件）。特别感谢以上公开数据源为公益和大众需求提供的便利！
- **多源价格互补**：飞猪 + Google Flights + Skiplagged 三源并发查价，支持往返搜索、多旅客、舱位选择、经停控制
- **统一货币输出**：默认输出人民币（CNY），可用 `--currency usd` 切换为美元，每条记录含 `currency` 字段标注
- **城市级智能搜索**：中英文城市名 / IATA 代码混合输入，自动展开至所有机场（"上海"→PVG+SHA），自动过滤已关闭/货运专用机场
- **7000+ 个机场缓存**：覆盖全球 99% 有 IATA 代码的机场，含中英文名称及别名（AI 翻译，如有错误欢迎纠正）
- **智能重试 & 快速返回**：瞬态错误自动重试，有结果后提前返回不等慢源
- **共享代码去重**：自动识别并合并 Codeshare 航班，默认仅显示主运营航班

## 快速开始



### 安装（OpenClaw）

技能文件 SKILL.md (中文）  SKILL_EN.md(英文）
技能市场安装

```bash
clawclub install flyclaw
```
或告知小龙虾本github地址让它帮忙自动安装

- 安装说明

<img src="img/OpenClaw_Install_Instruction_CHS.jpg" width="350"/>

安装完成后建议先让小龙虾阅读技能文档再使用：

- Debug调试说明（偶发问题）

<img src="img/OpenClaw_Install_Debug1_CHS.jpg" width="350"/> <img src="img/OpenClaw_Install_Debug2_CHS.jpg" width="350"/>

- 实际使用示例示意（查航班、查动态等，更多等你挖掘！）

<img src="img/OpenClaw_Demo1_CHS.jpg" width="350"/> <img src="img/OpenClaw_Demo2_CHS.jpg" width="350"/>


### 安装（非OpenClaw方式）

```bash
# 创建 conda 环境
conda create -n flyclaw python=3.11 -y
conda activate flyclaw

# 安装核心依赖
pip install requests pyyaml curl_cffi flights
```
### 环境要求

- Python 3.11+
- conda 环境（推荐）

### 配置

默认配置文件 `config.yaml` 已包含推荐值，通常无需修改即可使用：

```yaml
sources:
  fr24:
    enabled: true
    priority: 1
    timeout: 10
  google_flights:
    enabled: true
    priority: 2
    timeout: 15
    serpapi_key: ""  # 留空则跳过 SerpAPI；填入则自动启用
    retry: 2           # 空结果时智能重试次数（0 = 禁用）
    retry_delay: 0.5   # 初始重试等待秒数
    retry_backoff: 2.0  # 重试等待倍数（0.5 → 1.0 → 2.0s）
  skiplagged:
    enabled: true
    priority: 2
    timeout: 12
    retry: 4           # 空结果时智能重试次数（0 = 禁用）
    retry_delay: 0.5   # 初始重试等待秒数
    retry_backoff: 2.0  # 重试等待倍数（0.5 → 1.0 → 2.0s）
    mcp_enabled: false  # MCP 实验性后端（默认关闭）；true = 优先尝试 MCP，失败则回退 REST
    mcp_url: "https://mcp.skiplagged.com/mcp"  # MCP 服务器地址
  airplanes_live:
    enabled: true
    priority: 3
    timeout: 6
  fliggy_mcp:
    enabled: true
    priority: 2
    timeout: 10
    api_key: ""          # 留空使用内置默认 key
    sign_secret: ""      # 留空使用内置默认 secret
  fast_flights:
    enabled: false  # 可选：仅在 --compare 模式下启用
    timeout: 15
cache:
  dir: cache
  airport_update_days: 99999  # 默认禁用自动更新（使用内置预建数据）；0 = 禁用，30 = 每月更新
  airport_update_url: ""   # 自定义更新地址；留空则使用内置默认地址
query:
  timeout: 20      # 全局查询超时秒数（各数据源超时仍独立生效）
  return_time: 12   # 智能返回：有结果后提前返回（秒）；0 = 禁用
  filter_inactive_airports: true  # 多机场查询时自动过滤已关闭/非商用机场
  route_relay: true           # 启用航线中继：发现航班航线后自动查询价格源
  relay_timeout: 8            # 中继专用超时秒数（快速失败）
  relay_engines:              # 航线中继价格查询使用的引擎
    google_flights: true
    skiplagged: true
price_priority:            # 价格优先级（独立于数据字段优先级）
  - fliggy_mcp
  - google_flights
  - skiplagged
output:
  format: json  # table / json
  language: both  # cn / en / both
  currency: cny  # cny / usd / original（默认 CNY 统一输出）
  exchange_rate_cny_usd: 7.25  # CNY↔USD 汇率
```

### 使用示例

```bash
# 按航班号查询（多源并发）
conda run -n flyclaw python flyclaw.py query --flight CA981

# 按航班号查询，过滤指定日期
conda run -n flyclaw python flyclaw.py query --flight CA981 --date 2026-04-01

# 按航线搜索（含价格）——城市级搜索自动覆盖所有机场
conda run -n flyclaw python flyclaw.py search --from 上海 --to 纽约 --date 2026-04-01
# 上海(PVG+SHA) → 纽约(JFK+EWR+LGA) 所有机场组合

# 往返搜索
conda run -n flyclaw python flyclaw.py search --from PVG --to LAX --date 2026-04-15 --return 2026-04-25

# 商务舱 + 2 人
conda run -n flyclaw python flyclaw.py search --from PVG --to JFK --date 2026-04-15 --cabin business -a 2

# 直飞 + 按价格排序 + JSON 输出
conda run -n flyclaw python flyclaw.py search --from PVG --to NRT --date 2026-04-15 --stops 0 --sort cheapest -o json

# 包含经停航班
conda run -n flyclaw python flyclaw.py search --from PVG --to JFK --date 2026-04-15 --stops any

# 关闭绕行查价
conda run -n flyclaw python flyclaw.py query --flight CA981 --no-relay

# 英文输入同样支持
conda run -n flyclaw python flyclaw.py search --from Shanghai --to "New York" --date 2026-04-01

# 切换为美元输出
conda run -n flyclaw python flyclaw.py search --from 上海 --to 北京 --date 2026-04-15 --currency usd

# 详细模式（显示数据来源和舱位）
conda run -n flyclaw python flyclaw.py query --flight CA981 -v

# 自定义超时
conda run -n flyclaw python flyclaw.py query --flight CA981 --timeout 10 --return-time 5

# 更新机场数据
conda run -n flyclaw python flyclaw.py update-airports --url http://example.com/airports.json
```

### 搜索参数

| 参数 | 短标志 | 默认值 | 说明 |
|------|--------|-------|------|
| `--from` | — | （必填） | 出发地（IATA/中文/英文） |
| `--to` | — | （必填） | 目的地 |
| `--date` | `-d` | — | 出行日期 YYYY-MM-DD |
| `--return` | `-r` | — | 返程日期（启用往返搜索） |
| `--adults` | `-a` | 1 | 成人旅客数 |
| `--children` | — | 0 | 儿童旅客数 |
| `--infants` | — | 0 | 婴儿旅客数 |
| `--cabin` | `-C` | economy | 舱位：economy/premium/business/first |
| `--limit` | `-l` | 不限制 | 最大结果数（默认返回全部，指定后截断） |
| `--sort` | `-s` | — | 排序：cheapest/fastest/departure/arrival |
| `--stops` | — | 0 | 经停控制：0=直飞/1/2/any=不限 |
| `--currency` | — | cny | 输出货币：cny/usd/original |
### 调试功能（开发者用，普通用户无需关注）

以下功能仅用于开发调试，需安装额外可选依赖，普通用户无需安装。**OpenClaw 技能用户不要安装** mcp、fast-flights、playwright 等调试依赖。

**MCP 后端**为实验功能，默认关闭（`mcp_enabled: false`），有额外握手延迟，普通用户无需开启。

**交叉验证**：`--compare` 标志，用 fast-flights v3 对比 fli 的查询结果，支持航班号匹配：

```bash
# 需安装: pip install fast-flights>=3.0rc0
conda run -n flyclaw python flyclaw.py search --from PVG --to CAN --date 2026-04-01 --compare
```

**浏览器基准验证**：`--browser` 配合 `--compare`，启动 Playwright 浏览器三方独立验证：

```bash
# 需安装: pip install playwright && playwright install chromium
conda run -n flyclaw python flyclaw.py search --from PVG --to CAN --date 2026-04-01 --compare --browser
```

未安装 fast-flights / playwright 时，`--compare` / `--browser` 会提示安装方法，不影响正常使用。

### 输出示例

```
  CA981  (Air China)
  北京(PEK) → 纽约(JFK)
  Departure: 2026-04-01 13:00    Arrival: 2026-04-01 14:30
  Price: $856 | Stops: 0 | Duration: 840min
```

往返搜索输出：
```
  CA981  (Air China)
  上海(PVG) → 洛杉矶(LAX)
  Departure: 2026-04-15 10:00    Arrival: 2026-04-15 14:00
  Price: $2400 (round-trip) | Stops: 0 | Duration: 840min
  ── Return ──
  CA982  (Air China)
  Departure: 2026-04-25 18:00    Arrival: 2026-04-26 22:00
  Stops: 0 | Duration: 900min
```

## 数据来源

FlyClaw 基于多源聚合架构，通过开源库及免费公开 API 获取数据。无需注册账号或提供 API Key。使用相关数据请遵守当地法律和规定。


## 依赖及许可证

| 依赖 | 版本要求 | 许可证 | 用途 |
|------|----------|--------|------|
| requests | >=2.28.0 | Apache-2.0 | HTTP 请求 |
| pyyaml | >=6.0 | MIT | YAML 配置解析 |
| curl_cffi | >=0.5.0 | MIT | Skiplagged API 请求 |
| flights (fli) | latest | MIT | Google Flights 查询（必需，GF 默认启用） |
| mcp | >=1.26.0 | MIT | Skiplagged MCP 后端（实验功能，默认关闭，普通用户无需安装） |
| fast-flights | >=3.0rc0 | MIT | --compare 交叉验证（可选，调试用） |
| playwright | latest | Apache-2.0 | --compare --browser 浏览器验证（可选，调试用） |

Python 版本要求：3.11+


## 免责声明

- 本工具基于多源聚合架构，通过开源库及免费公开 API 获取数据
- **无需注册账号或提供任何 API Key** 即可使用全部核心功能
- 本工具仅供学习研究用途，请遵守当地法律法规
- Google Flights 在部分地区（如中国大陆）可能不可用
- 价格数据来自多个数据源（飞猪、Google Flights、Skiplagged），不同来源的价格可能存在差异（含税/不含税、舱位差异、货币汇率等），仅供参考
- 程序不收集、不存储、不传输任何用户个人信息

## License

[Apache-2.0](LICENSE) |  nuaa02@gmail.com
