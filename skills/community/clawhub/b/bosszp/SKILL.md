---
name: bosszp
description: BOSS直聘岗位数据爬虫 + 可视化分析工具。使用 Scrapy 爬取职位数据，存入 MySQL，用 Flask + Highcharts 生成可视化报告。当用户需要批量采集 BOSS直聘 职位数据、分析薪资分布、公司分布、岗位要求，或需要生成可视化报告时触发。
---

# BOSS直聘 数据爬虫分析 (bosszp)

## 环境要求

- Python 3.x
- MySQL
- Scrapy
- Pandas + SQLAlchemy
- Flask + Highcharts

## 安装依赖

```bash
pip install scrapy
pip install flask pandas sqlalchemy pymysql
pip install flash
```

## 数据采集

### 1. 创建 Scrapy 项目

```bash
scrapy startproject bosszp
cd bosszp
scrapy genspider boss zhipin.com
```

### 2. 配置 Cookie 和请求头

编辑 `settings.py`：

```python
COOKIES_ENABLED = True
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    ...
]

# 爬取延迟（避免被封）
DOWNLOAD_DELAY = 2
```

### 3. 运行爬虫

```bash
scrapy crawl boss -o output.csv
```

## 数据导出

### CSV 格式

岗位名称,岗位地区,薪资,公司名称,公司类型,公司规模,融资阶段,工作年限,学历,福利标签

### 导入 MySQL

```bash
python clean_data.py   # 数据清洗 + 导入 MySQL
```

## 可视化看板

```bash
cd web
export FLASK_APP=run.py
flask run
# 访问 http://127.0.0.1:8080/
```

看板包含：
- **饼图**: 公司融资阶段分布
- **柱状图**: 薪资分布 Top10
- **词云**: 岗位福利标签词云
- **表格**: 公司排名 Top10（按岗位数量）

## 字段说明

| 字段 | 说明 |
|------|------|
| job_name | 岗位名称 |
| job_area | 工作地区 |
| job_salary | 薪资范围 |
| com_name | 公司名称 |
| com_type | 公司类型（国企/民营等） |
| com_size | 公司规模 |
| finance_stage | 融资阶段 |
| work_year | 工作年限要求 |
| education | 学历要求 |
| job_benefits | 福利标签 |
