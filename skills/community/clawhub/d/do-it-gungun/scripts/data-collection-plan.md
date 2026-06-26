# do-it 数据采集与更新方案

**版本：** 1.0.0  
**创建日期：** 2026-03-15  
**用途：** 指导数据采集、清洗、更新流程

---

## 🕷️ 数据采集方案

### 1. 职业数据抓取

#### 薪资数据源

| 网站 | 数据类型 | 抓取方式 | 频率 |
|------|----------|----------|------|
| 拉勾网 | 互联网行业薪资 | API/爬虫 | 周 |
| Boss 直聘 | 全行业薪资 | API/爬虫 | 周 |
| 猎聘网 | 中高端职位 | API/爬虫 | 周 |
| 脉脉 | 职场爆料薪资 | 爬虫 | 月 |
| LinkedIn | 外企/海外薪资 | API | 月 |

#### 抓取脚本示例

```python
# scripts/crawl_salary.py
import requests
from bs4 import BeautifulSoup
import json

def crawl_lagou_salary(keyword, city):
    """抓取拉勾网薪资数据"""
    url = "https://www.lagou.com/jobs/list_{keyword}?city={city}"
    # 实现抓取逻辑
    pass

def crawl_boss_salary(keyword, city):
    """抓取 Boss 直聘薪资数据"""
    # 实现抓取逻辑
    pass

def aggregate_salary_data():
    """聚合多源薪资数据"""
    # 去重、清洗、计算中位数
    pass
```

---

### 2. 城市数据抓取

#### 数据来源

| 数据项 | 来源 | 网址 |
|--------|------|------|
| GDP 数据 | 国家统计局 | stats.gov.cn |
| 人口流入 | 各城市统计局 | - |
| 房价数据 | 安居客/链家 | anjuke.com |
| 生活成本 | Numbeo | numbeo.com |
| 教育质量 | 教育部/学校排名 | - |
| 医疗资源 | 卫健委 | nhc.gov.cn |

#### 抓取脚本示例

```python
# scripts/crawl_city_data.py
def crawl_gdp_data():
    """抓取各城市 GDP 数据"""
    pass

def crawl_housing_price(cities):
    """抓取各城市房价"""
    pass

def crawl_living_cost(cities):
    """抓取生活成本数据"""
    pass
```

---

### 3. 行业趋势数据

#### 数据来源

| 来源 | 类型 | 网址 |
|------|------|------|
| 36 氪 | 行业新闻 | 36kr.com |
| 艾瑞咨询 | 行业报告 | iresearch.com.cn |
| 易观分析 | 行业分析 | analysys.cn |
| 券商研报 | 深度分析 | 慧博/东方财富 |

#### 抓取脚本示例

```python
# scripts/crawl_industry_trends.py
def crawl_36kr_industry(industry):
    """抓取 36 氪行业新闻"""
    pass

def crawl_research_reports(industry):
    """抓取行业研究报告"""
    pass
```

---

## 🧹 数据清洗流程

### 清洗规则

```python
# scripts/clean_data.py

def clean_salary_data(raw_data):
    """清洗薪资数据"""
    # 1. 去除异常值 (过高/过低)
    # 2. 统一薪资单位 (统一为月薪/年薪)
    # 3. 去除重复数据
    # 4. 填补缺失值
    # 5. 计算统计值 (min/median/max/avg)
    pass

def validate_data_quality(data):
    """验证数据质量"""
    # 1. 样本数量检查 (>100)
    # 2. 数据时效性检查 (<6 个月)
    # 3. 数据一致性检查 (多源对比)
    # 4. 异常值检测
    pass
```

### 质量要求

| 指标 | 要求 |
|------|------|
| 样本数量 | ≥100 条/城市/职位 |
| 数据时效 | ≤6 个月 |
| 多源一致性 | 偏差<20% |
| 异常值比例 | <5% |

---

## 🔄 数据更新机制

### 定时任务配置

```yaml
# config/cron_jobs.yaml

daily:
  - task: update_stock_returns
    time: "02:00"
    
weekly:
  - task: update_salary_data
    time: "03:00"
    day: "Monday"
    
monthly:
  - task: update_city_data
    time: "04:00"
    day: 1
    
quarterly:
  - task: update_industry_reports
    time: "05:00"
    day: 1
    month: [1, 4, 7, 10]
```

### 更新脚本

```python
# scripts/update_all_data.py
import schedule
import time

def daily_update():
    """每日更新任务"""
    update_stock_returns()
    update_exchange_rates()

def weekly_update():
    """每周更新任务"""
    crawl_salary_data()
    clean_and_aggregate()

def monthly_update():
    """每月更新任务"""
    crawl_city_data()
    update_industry_trends()

# 调度任务
schedule.every().day.at("02:00").do(daily_update)
schedule.every().monday.at("03:00").do(weekly_update)
schedule.every().month.do(monthly_update)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

---

## 📊 数据存储方案

### 数据库选择

| 数据类型 | 存储方案 | 说明 |
|----------|----------|------|
| 结构化数据 | PostgreSQL | 薪资/城市/案例数据 |
| 文档数据 | MongoDB | 行业报告/研究论文 |
| 缓存数据 | Redis | 热点数据/会话缓存 |
| 文件存储 | OSS/S3 | 原始数据备份 |

### 数据表设计

```sql
-- 薪资数据表
CREATE TABLE industry_salary (
    id SERIAL PRIMARY KEY,
    industry VARCHAR(100),
    role VARCHAR(100),
    city VARCHAR(50),
    experience_years INTEGER,
    salary_min DECIMAL(10,2),
    salary_median DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    sample_size INTEGER,
    data_source VARCHAR(100),
    updated_at TIMESTAMP
);

-- 案例记录表
CREATE TABLE case_records (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(50) UNIQUE,
    user_profile JSONB,
    problem_type VARCHAR(50),
    options JSONB,
    recommendation VARCHAR(500),
    reasoning TEXT,
    decision_date DATE,
    outcome TEXT,
    satisfaction_score INTEGER,
    created_at TIMESTAMP
);
```

---

## 🔐 数据使用规范

### API 接口设计

```python
# api/decision_support.py

@app.get("/api/salary/query")
def query_salary(industry: str, role: str, city: str, experience: int):
    """查询薪资数据"""
    pass

@app.get("/api/city/compare")
def compare_cities(cities: list, factors: list):
    """城市对比"""
    pass

@app.post("/api/career/analyze")
def analyze_career_options(user_profile: dict, options: list):
    """职业选择分析"""
    pass

@app.post("/api/case/submit")
def submit_case_feedback(case_id: str, outcome: str, satisfaction: int):
    """提交案例反馈"""
    pass
```

### 数据权限

| 角色 | 权限 |
|------|------|
| 普通用户 | 查询公开数据 |
| 付费用户 | 深度分析 + 历史数据 |
| 管理员 | 全部权限 |
| API 调用 | 限流 + 鉴权 |

---

## 📈 数据质量监控

### 监控指标

```python
# scripts/monitor_data_quality.py

def monitor_data_freshness():
    """监控数据时效性"""
    # 检查各数据表最后更新时间
    # 超过阈值告警
    pass

def monitor_data_accuracy():
    """监控数据准确性"""
    # 多源数据对比
    # 异常值检测
    pass

def monitor_api_usage():
    """监控 API 使用情况"""
    # 调用次数
    # 响应时间
    # 错误率
    pass
```

### 告警规则

| 指标 | 阈值 | 告警方式 |
|------|------|----------|
| 数据过期 | >30 天未更新 | 邮件 + 钉钉 |
| API 错误率 | >5% | 钉钉 |
| 响应时间 | >2 秒 | 邮件 |
| 数据异常 | 偏差>50% | 邮件 + 钉钉 |

---

## 🎯 实施路线图

### 第 1 阶段：基础数据 (2 周)
- [ ] 搭建数据库
- [ ] 抓取主要城市薪资数据
- [ ] 抓取一线城市生活成本
- [ ] 建立基础 API

### 第 2 阶段：自动化 (2 周)
- [ ] 定时抓取脚本
- [ ] 数据清洗流程
- [ ] 质量监控告警

### 第 3 阶段：产品化 (4 周)
- [ ] Web 界面开发
- [ ] 用户反馈系统
- [ ] 案例积累功能

### 第 4 阶段：优化迭代 (持续)
- [ ] 根据反馈优化数据
- [ ] 扩展数据源
- [ ] 提升判断准确率

---

## 💡 注意事项

### 法律合规
- [ ] 遵守网站 robots.txt
- [ ] 数据使用授权
- [ ] 用户隐私保护
- [ ] 数据脱敏处理

### 技术风险
- [ ] 反爬机制应对
- [ ] 数据备份策略
- [ ] 容灾恢复方案
- [ ] API 限流保护

### 运营风险
- [ ] 数据准确性验证
- [ ] 用户期望管理
- [ ] 免责声明明确
- [ ] 持续投入保障

---

**创建人：** 滚滚 & 地球人  
**创建时间：** 2026-03-15  
**状态：** 🚀 方案完成，等待实施
