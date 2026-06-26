---
name: data-harvester
description: 智能数据采集器 - 自动化数据采集、处理和导出工具。支持Web抓取、API调用、数据库查询、文件读取，导出JSON/CSV/Excel/PDF。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - CLAWHUB_SITE
    primaryEnv: CLAWHUB_SITE
    emoji: "📊"
    homepage: https://openclawx.asia
    install:
      - kind: uv
        package: -r requirements.txt
---

# 智能数据采集器 - Smart Data Harvester

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT--0-green)

专为OpenClaw设计的自动化数据采集工具。从网页、API、数据库、文件中采集数据，智能清洗处理后导出为你需要的格式。

## 🚀 核心功能

- **多数据源适配器**：Web抓取、API调用、数据库查询、文件读取
- **智能数据处理管道**：数据清洗、转换、聚合、分析
- **多种导出格式**：JSON、CSV、Excel、SQLite、PDF报告
- **定时任务调度**：支持定时自动执行数据采集任务
- **OpenClaw无缝集成**：原生OpenClaw技能，一键安装使用
- **全中文支持**：中文界面和文档，专为中国用户设计

## 📦 安装

```bash
clawhub install data-harvester
```

或手动安装：
```bash
git clone https://gitee.com/du-xuegong/openclaw-wealth-guide.git
cd openclaw-wealth-guide
uv pip install -r requirements.txt
```

## 🛠️ 快速使用

### 在OpenClaw中
```
/技能 数据采集器
采集网页 https://example.com 保存为 data.json
定时采集 https://api.example.com/data 每天 09:00
导出数据为 Excel 报表
```

### Python API
```python
from data_harvester import DataHarvester

harvester = DataHarvester()
result = harvester.harvest({
    "sources": [{"type": "web", "url": "https://example.com"}],
    "export": {"format": "json", "path": "output.json"}
})
print(f"采集完成：{result['stats']['total_records']}条记录")
```

## ⚙️ 配置

支持数据源类型：
- **Web适配器**：CSS选择器、XPath抓取
- **API适配器**：REST API，支持认证
- **数据库适配器**：MySQL/PostgreSQL/SQLite
- **文件适配器**：CSV、Excel、JSON

## ❓ 常见问题

**Q: 安装后怎么激活？**  
A: 在OpenClaw对话中使用 `/技能 数据采集器` 激活。

**Q: 支持哪些数据源？**  
A: Web页面、API接口、数据库、文件四种类型。

**Q: 需要定制开发或部署咨询？**  
A: 访问 https://openclawx.asia 获取企业级支持服务。

## 📄 许可证

MIT-0 — 免费使用，无需署名。

## 📞 联系

- **作者**：dxg
- **邮箱**：852621787@qq.com
- **GitHub**：https://github.com/dxg852621787
- **企业服务**：https://openclawx.asia
