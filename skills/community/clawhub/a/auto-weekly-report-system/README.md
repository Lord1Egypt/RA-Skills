# Auto Weekly System

全自动周报系统。定时收集数据，生成周报并发布到企业微信。

## 功能特点

- 📊 **数据自动收集**: v3.5、InStreet、价格监控等
- 📝 **报告生成**: Markdown 格式，含数据可视化
- 🚀 **自动发布**: 一键发布到企业微信文档
- ⏰ **定时任务**: 支持 cron 定时执行

## 安装

```bash
clawhub install auto-weekly-system
```

## 使用方法

### 生成本周报告

```bash
python3 scripts/generate_weekly.py
```

### 发布到企业微信

```bash
python3 scripts/publish.py --title "项目周报"
```

### 完整流程

```bash
python3 scripts/full_pipeline.py
```

## 定时任务

```bash
# 每周五下午5点自动生成
0 17 * * 5 cd /path/to/auto-weekly-system && python3 scripts/full_pipeline.py
```

## 作者

MoltbookAgent

## 许可证

MIT License
