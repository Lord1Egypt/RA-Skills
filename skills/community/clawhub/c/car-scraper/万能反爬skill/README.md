# 万能反爬 Skill - 车辆信息采集工具集

多平台汽车信息采集框架，支持 **大搜车**、**懂车帝**、**汽车之家** 三大平台，采集数据统一格式后供 **OpenClaw** 使用。

## 功能特性

- **三大平台支持**: 大搜车 (souche.com)、懂车帝 (dongchedi.com)、汽车之家 (che168.com)
- **统一数据格式**: 所有平台采集数据转为统一的 `VehicleInfo` 结构
- **OpenClaw 兼容输出**: JSON / JSONL / CSV 多格式导出
- **完整反爬对策**: UA轮换、请求限速、退避策略、Cookie管理、指纹随机化
- **多重解析降级**: API → SSR JSON → HTML 解析，确保数据可得性

## 文件结构

```
万能反爬skill/
├── main.py              # 主入口，命令行启动
├── config.py            # 全局配置（站点URL、请求参数、代理等）
├── data_models.py       # 统一数据模型 VehicleInfo / ScrapeResult
├── anti_detect.py       # 反爬工具集（UA池、限速器、Cookie管理、拦截检测）
├── dasouche_scraper.py  # 大搜车采集器
├── dongchedi_scraper.py # 懂车帝采集器
├── autohome_scraper.py  # 汽车之家采集器
├── openclaw_export.py   # OpenClaw 格式导出
├── requirements.txt     # Python 依赖
├── SKILL.md             # OpenClaw Skill 定义文件
└── output/              # 采集数据输出目录
    └── openclaw/        # OpenClaw 格式数据
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行采集

```bash
# 采集所有平台（每平台2页）
python main.py

# 只采大搜车，5页
python main.py --platform dasouche --pages 5

# 懂车帝 + 按城市过滤
python main.py --platform dongchedi --pages 3 --city 北京

# 汽车之家，输出所有格式
python main.py --platform autohome --format all

# 详细日志
python main.py -v
```

### 3. 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--platform, -p` | 目标平台: dasouche / dongchedi / autohome / all | all |
| `--pages, -n` | 采集页数 | 2 |
| `--city, -c` | 城市过滤（仅懂车帝） | 空 |
| `--format, -f` | 输出格式: json / jsonl / csv / all | json |
| `--output, -o` | 输出目录 | output/openclaw/ |
| `--verbose, -v` | 详细日志 | False |

## 数据模型

采集的每辆车统一为 `VehicleInfo`，主要字段:

| 分类 | 字段 | 说明 |
|------|------|------|
| 基本 | title, brand, series, model, year | 车辆名称/品牌/车系/车型/年款 |
| 价格 | price, original_price | 售价/新车指导价 (万元) |
| 里程 | mileage, mileage_km | 文本里程/公里数 |
| 牌照 | plate_city, plate_date, vin | 上牌城市/日期/VIN |
| 技术 | engine, transmission, fuel_type, drive_type | 发动机/变速箱/燃油/驱动 |
| 电动 | battery_capacity, range_km | 电池容量/续航 |
| 图片 | images, thumbnail | 图片列表/缩略图 |
| 商家 | dealer_name, dealer_phone, dealer_city | 商家信息 |
| 车况 | condition_tags, highlights, description | 标签/亮点/描述 |

## OpenClaw 输出格式

导出的 JSON 文件遵循 OpenClaw 文档结构:

```json
{
  "url": "https://www.dongchedi.com/usedcar/xxx",
  "title": "2023款 宝马3系 325Li",
  "content": "车辆名称: 2023款 宝马3系 325Li\n品牌: 宝马\n车系: 3系\n售价: 25.8万元\n...",
  "source": "car_scraper_dongchedi",
  "timestamp": "2026-03-09T10:30:00",
  "metadata": {
    "source_platform": "dongchedi",
    "brand": "宝马",
    "series": "3系",
    "price_cny_wan": 25.8,
    "mileage": "1.2万公里",
    "fuel_type": "汽油",
    "transmission": "8挡手自一体",
    "images": ["https://..."],
    ...
  }
}
```

## 反爬策略说明

| 策略 | 实现 |
|------|------|
| UA 轮换 | 9 个桌面 + 3 个移动端 UA，每次请求随机选取 |
| 请求限速 | 随机 2~6 秒间隔，被检测后自动退避加倍 |
| 浏览器指纹 | sec-ch-ua、sec-fetch-* 系列头、随机 device fingerprint |
| Cookie 管理 | 自动获取 + 定期刷新，模拟真实会话 |
| 拦截检测 | HTTP 状态码 + 页面关键词双重检测验证码/封禁 |
| 多重解析 | API → 内嵌JSON → HTML 三级降级，保证可得性 |
| 代理支持 | 可配置代理池轮换（config.py 中配置） |

## 配置说明

编辑 `config.py` 可调整:

- **请求间隔**: `REQUEST_DELAY_MIN` / `REQUEST_DELAY_MAX`
- **采集页数**: 各站点 `pages_to_scrape`
- **代理配置**: `PROXY_LIST` 和 `PROXY_ROTATION_ENABLED`
- **输出格式**: `OPENCLAW_OUTPUT_FORMAT`
- **站点URL**: 各 `SiteConfig` 的 URL 模板

## 注意事项

1. 采集频率请保守设置，建议单平台不超过 10 页/次
2. 如遇到验证码/封禁，程序会自动退避并记录日志
3. 代理备选，可在 `config.py` 中配置代理池
4. 各平台页面结构可能更新，解析规则需要根据实际情况调整
5. 数据仅做市场调研和信息参考使用
