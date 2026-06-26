# 智能数据采集器 - Smart Data Harvester

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 🚀 功能特性

智能数据采集器是一个为OpenClaw生态系统设计的自动化数据采集、处理和导出工具。支持多种数据源和导出格式，专为中国市场优化。

### 核心功能
- **多数据源适配器**：Web抓取、API调用、数据库查询、文件读取
- **智能数据处理管道**：数据清洗、转换、聚合、分析
- **多种导出格式**：JSON、CSV、Excel、SQLite、PDF报告
- **定时任务调度**：支持定时自动执行数据采集任务
- **OpenClaw无缝集成**：原生OpenClaw技能，可通过ClawHub安装
- **中文界面和文档**：全中文支持，适合中国用户

## 📦 安装

### 通过ClawHub安装（推荐）
```bash
npx clawhub install data-harvester
```

### 手动安装
1. 克隆仓库：
```bash
git clone https://gitee.com/du-xuegong/openclaw-wealth-guide.git
cd openclaw-wealth-guide
```

2. 安装依赖：
```bash
uv pip install -r requirements.txt
```

3. 在OpenClaw中配置技能

## 🛠️ 快速开始

### 基本使用
```python
from data_harvester import DataHarvester

# 创建数据采集器实例
harvester = DataHarvester()

# 配置数据源
config = {
    "sources": [
        {
            "type": "web",
            "url": "https://example.com/data",
            "extract_rules": {
                "title": "h1",
                "content": ".main-content"
            }
        }
    ],
    "processing": {
        "clean_html": True,
        "remove_duplicates": True
    },
    "export": {
        "format": "json",
        "path": "output/data.json"
    }
}

# 执行数据采集
result = harvester.harvest(config)
print(f"采集完成：{result['stats']['total_records']}条记录")
```

### OpenClaw技能使用
```bash
# 在OpenClaw对话中
/技能 数据采集器

# 示例命令
采集网页 https://example.com 保存为 data.json
定时采集 https://api.example.com/data 每天 09:00
导出数据为 Excel 报表
```

## 📁 项目结构
```
openclaw-wealth-guide/
├── src/data_harvester/
│   ├── adapters/          # 数据源适配器
│   ├── processors/        # 数据处理器
│   ├── exporters/         # 数据导出器
│   ├── scheduler/         # 任务调度器
│   └── openclaw_integration/  # OpenClaw集成
├── tests/                 # 测试套件
├── examples/              # 使用示例
├── skill.json            # OpenClaw技能清单
└── requirements.txt      # Python依赖
```

## 🔧 配置选项

### 数据源配置
支持多种数据源类型：
- **Web适配器**：网页抓取，支持CSS选择器、XPath
- **API适配器**：REST API调用，支持认证和参数
- **数据库适配器**：MySQL、PostgreSQL、SQLite查询
- **文件适配器**：CSV、Excel、JSON文件读取

### 处理器配置
- 数据清洗：去重、过滤、格式化
- 数据转换：类型转换、计算字段
- 数据聚合：分组统计、汇总计算
- 数据验证：规则验证、质量检查

### 导出器配置
- JSON导出：结构化数据输出
- CSV导出：表格数据输出
- Excel导出：多工作表Excel文件
- SQLite导出：本地数据库存储
- PDF报告：格式化报告生成

## ⏰ 定时任务

支持APScheduler定时任务调度：
```python
from data_harvester.scheduler import Scheduler

scheduler = Scheduler()
scheduler.add_job(
    "daily_report",
    "cron",
    hour=9,
    minute=0,
    config={
        "sources": [...],
        "export": {"format": "excel", "path": "reports/daily.xlsx"}
    }
)
scheduler.start()
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 📞 联系

- **作者**：dxg
- **邮箱**：852621787@qq.com
- **Gitee**：https://gitee.com/du-xuegong
- **GitHub**：https://github.com/dxg852621787

## 💰 定价

### 版本和定价
- **基础版**：¥299 - 基础数据采集功能
- **专业版**：¥899 - 高级功能+定时任务+技术支持
- **企业版**：¥2,999 - 定制开发+优先支持+培训服务

### 购买方式
1. 通过ClawHub技能商店购买
2. 联系作者直接购买
3. 企业定制服务咨询

---

**智能数据采集器 - 让数据采集变得简单高效！** 🚀