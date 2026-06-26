# 招聘搜索技能 - 快速开始指南

## 🚀 立即开始

### 1. 安装依赖
```bash
cd C:\Users\yuks\.openclaw\workspace\skills\job-search
pip install requests beautifulsoup4 fake-useragent
```

### 2. 测试功能
```bash
# 测试生产就绪版（推荐）
python test_production.py

# 测试最终版
python test_final.py

# 简单测试
python simple_test.py
```

### 3. 开始搜索
```bash
# 使用生产就绪版（功能最全）
python production_ready.py Python 北京 15
python production_ready.py Java 上海 20
python production_ready.py 前端 广州 10

# 使用最终版
python final_searcher.py Python 北京
python final_searcher.py 测试工程师 深圳 25
```

## 📊 各版本对比

| 版本 | 特点 | 推荐场景 |
|------|------|----------|
| **production_ready.py** | 生产就绪，支持手动添加职位，数据库存储，多种导出格式 | 长期使用，需要积累真实数据 |
| **final_searcher.py** | 最终版，混合搜索策略，保证始终有结果 | 快速使用，需要稳定结果 |
| **practical_searcher.py** | 实用版，简单易用 | 基础需求 |
| **enhanced_searcher.py** | 增强版，更好的反爬处理 | 需要尝试真实搜索 |

## 🔧 在OpenClaw中集成

### 基础集成
```python
# 方法1: 使用生产就绪版（推荐）
import sys
sys.path.append("skills/job-search")
from production_ready import ProductionJobSearcher

searcher = ProductionJobSearcher()
results = searcher.search("Python", "北京", 15)
print(searcher.format_results(results))

# 保存结果
json_file = searcher.export_results(results, 'json')
csv_file = searcher.export_results(results, 'csv')
```

### 创建OpenClaw命令
```python
# 创建自定义命令文件: job_search_command.py
def search_jobs(keyword, city="全国", count=15):
    """OpenClaw招聘搜索命令"""
    from production_ready import ProductionJobSearcher
    searcher = ProductionJobSearcher()
    results = searcher.search(keyword, city, count)
    return searcher.format_results(results)

# 使用
result = search_jobs("Python", "上海", 20)
print(result)
```

### 定时任务
```python
# 创建定时搜索任务
import schedule
import time
from production_ready import ProductionJobSearcher

def daily_job_search():
    searcher = ProductionJobSearcher()
    results = searcher.search("Python", "北京", 20)
    
    # 保存结果
    filename = searcher.export_results(results, 'json')
    print(f"每日搜索完成，结果保存到: {filename}")
    
    # 可以发送通知等

# 每天上午9点执行
schedule.every().day.at("09:00").do(daily_job_search)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 📝 手动添加真实职位

当你在招聘网站看到好职位时，可以手动添加到数据库：

```python
from production_ready import ProductionJobSearcher

searcher = ProductionJobSearcher()

# 准备职位数据
job_data = {
    'platform': 'BOSS直聘',  # 平台名称
    'title': '高级Python开发工程师',  # 职位标题
    'company': '字节跳动',  # 公司名称
    'salary': '30-50K·16薪',  # 薪资
    'location': '北京·海淀区',  # 工作地点
    'experience': '3-5年',  # 经验要求
    'education': '本科',  # 学历要求
    'skills': ['Python', 'Django', 'Redis', '微服务'],  # 技能要求
    'description': '负责核心业务系统开发...',  # 职位描述
    'url': 'https://www.zhipin.com/job_detail/xxx.html',  # 职位链接
    'posted_date': '2024-01-01'  # 发布日期
}

# 添加到数据库
job_id = searcher.add_manual_job(job_data)
print(f"职位添加成功，ID: {job_id}")
```

## 📈 数据导出和分析

### 导出为多种格式
```python
from production_ready import ProductionJobSearcher

searcher = ProductionJobSearcher()
results = searcher.search("Python", "全国", 50)

# 导出为JSON（适合程序处理）
json_file = searcher.export_results(results, 'json')

# 导出为CSV（适合Excel分析）
csv_file = searcher.export_results(results, 'csv')

print(f"JSON文件: {json_file}")
print(f"CSV文件: {csv_file}")
```

### 在Excel中分析
1. 打开导出的CSV文件
2. 使用筛选功能按薪资、地点、经验等条件筛选
3. 使用数据透视表分析各平台职位分布
4. 制作图表展示薪资趋势

## 🔍 高级搜索技巧

### 组合搜索
```python
# 搜索多个关键词
keywords = ["Python", "Java", "前端"]
all_results = []

for keyword in keywords:
    results = searcher.search(keyword, "北京", 10)
    all_results.extend(results)

# 去重
unique_results = list({(job.title, job.company): job for job in all_results}.values())
```

### 薪资筛选
```python
def filter_by_salary(jobs, min_salary=20):
    """筛选薪资高于指定值的职位"""
    filtered = []
    for job in jobs:
        # 提取薪资数字（简单实现）
        import re
        numbers = re.findall(r'\d+', job.salary)
        if numbers:
            max_salary = max(map(int, numbers))
            if max_salary >= min_salary:
                filtered.append(job)
    return filtered
```

## 🛠️ 故障排除

### 常见问题1：导入失败
```bash
# 错误: No module named 'requests'
pip install requests beautifulsoup4 fake-useragent

# 如果pip失败，尝试:
python -m pip install --upgrade pip
pip install requests beautifulsoup4 fake-useragent lxml
```

### 常见问题2：编码问题
```python
# 在脚本开头添加
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### 常见问题3：搜索结果少
```python
# 1. 尝试更多关键词
results1 = searcher.search("Python开发", "北京", 10)
results2 = searcher.search("Python工程师", "北京", 10)
results3 = searcher.search("Python后端", "北京", 10)

# 2. 手动添加真实职位
# 3. 扩大搜索范围（使用"全国"）
```

## 📚 文件说明

### 核心文件
- `production_ready.py` - 生产就绪版（推荐）
- `final_searcher.py` - 最终版
- `practical_searcher.py` - 实用版
- `test_production.py` - 测试脚本

### 数据文件
- `data/jobs_database.json` - 职位数据库
- `data/mock_jobs.json` - 模拟数据模板
- `jobs_export_*.json/csv` - 导出文件

### 文档
- `FINAL_SUMMARY.md` - 完整部署指南
- `DEPLOYMENT_GUIDE.md` - 部署指南
- `README.md` - 详细说明
- `SKILL.md` - 技能说明

## 🎯 下一步建议

### 短期（1周内）
1. 测试各个版本，选择最适合的
2. 手动添加10-20个真实职位到数据库
3. 集成到OpenClaw工作流中

### 中期（1个月内）
1. 定期手动添加新发现的职位
2. 创建定时搜索任务
3. 分析导出数据，了解市场趋势

### 长期（3个月内）
1. 尝试实现真实API搜索（当技术可行时）
2. 添加更多分析功能（薪资预测、技能需求分析等）
3. 扩展到更多招聘平台

## 📞 获取帮助

如果遇到问题：
1. 查看 `FINAL_SUMMARY.md` 中的故障排除部分
2. 检查控制台错误信息
3. 确保网络连接正常
4. 验证Python和依赖库版本

---

**立即开始你的招聘搜索之旅！** 🚀

```bash
# 最简单的开始方式
cd C:\Users\yuks\.openclaw\workspace\skills\job-search
python production_ready.py "你的理想职位" "你的目标城市"
```

祝你找到理想的工作！ 💼