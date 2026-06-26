# Auto Report Generator Skill

## 功能
上传数据（CSV/Excel）→ AI自动分析 → 生成专业报表（图表+文字分析+格式），一键搞定月报/周报。

## 核心文件
- `SKILL.md` - 本文件，技能说明
- `scripts/generator.py` - 主生成器脚本（CLI入口）
- `core/parser.py` - 数据解析（pandas）
- `core/charts.py` - 图表生成（matplotlib/xlsxwriter）
- `core/ai_analyzer.py` - AI分析（OpenAI兼容接口）
- `core/report_builder.py` - 报表构建（多sheet Excel）
- `core/quota.py` - 额度管理（免费5次绝对计数）
- `core/templates.py` - 模板系统
- `scripts/quick_report.sh` - 快捷生成脚本

## 安装依赖
```bash
pip install pandas openpyxl xlsxwriter matplotlib pillow -q
```

## 使用方式
通过 Skill 系统调用 `scripts/generator.py`，传入参数：
- `--file` 数据文件路径
- `--template` 模板类型（月报/财务/销售/对比/自定义）
- `--ai-provider` AI提供商（openai/deepseek）
- `--ai-model` AI模型
- `--tier` 套餐等级（FREE/STD/PRO/MAX）
- `--output` 输出路径

## 套餐说明
- FREE: 5次绝对计数，1图表
- STD: ¥9.9/月，50次/月，3图表
- PRO: ¥29.9/月，200次/月，不限图表，PDF导出
- MAX: ¥99/月，不限次数，自定义模板

## Token前缀
REPORT-FREE / REPORT-STD / REPORT-PRO / REPORT-MAX
