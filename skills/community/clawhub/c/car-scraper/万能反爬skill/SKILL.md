---
description: "车辆信息采集反爬 Skill - 从大搜车、懂车帝、汽车之家采集二手车/新车数据，输出 OpenClaw 兼容格式。USE FOR: 采集车辆列表、车辆详情、价格行情、商家信息。支持反爬对策: UA轮换、限速退避、Cookie管理、指纹伪装。"
---

# 万能反爬 Skill

## 能力

1. **大搜车采集** (`dasouche_scraper.py`): 采集 souche.com 二手车列表和详情
2. **懂车帝采集** (`dongchedi_scraper.py`): 采集 dongchedi.com 二手车数据（API + SSR 双模式）
3. **汽车之家采集** (`autohome_scraper.py`): 采集 che168.com 二手车数据（含字体反爬处理）
4. **OpenClaw 导出** (`openclaw_export.py`): 统一格式输出 JSON/JSONL/CSV

## 使用方式

```python
# 单平台采集
from dasouche_scraper import DasoucheScraper
scraper = DasoucheScraper()
result = scraper.scrape(pages=3)

# OpenClaw 导出
from openclaw_export import export_scrape_result
files = export_scrape_result(result, output_format="json")
```

## 数据模型

所有车辆数据统一为 `VehicleInfo` (见 `data_models.py`)，包含:
- 品牌/车系/车型/年款
- 价格/里程/上牌信息
- 发动机/变速箱/驱动/排放等技术参数
- 图片/商家/车况描述

## 反爬配置

编辑 `config.py` 调整请求间隔、代理池、目标页数等参数。
