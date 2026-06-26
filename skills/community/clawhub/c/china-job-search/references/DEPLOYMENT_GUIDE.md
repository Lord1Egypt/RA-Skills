# 招聘搜索技能部署指南

## 概述

本技能已创建完整框架，支持BOSS直聘、智联招聘、前程无忧三大平台。要使技能实际工作，需要根据各网站当前结构进行调整。

## 当前状态

✅ **已完成**：
- 完整的技能框架和代码结构
- 多平台支持架构
- 数据模型和格式化输出
- OpenClaw集成接口
- 反爬处理基础框架

⚠️ **需要调整**：
- 各网站的实际HTML/CSS选择器
- API请求参数（如果网站有变化）
- 反爬绕过策略

## 部署步骤

### 第一步：环境准备

```bash
# 1. 进入技能目录
cd C:\Users\yuks\.openclaw\workspace\skills\job-search

# 2. 安装依赖
pip install -r requirements.txt

# 3. 验证安装
python -c "import requests; from bs4 import BeautifulSoup; print('依赖安装成功')"
```

### 第二步：测试各网站当前结构

#### 方法1：手动查看网页结构

1. **打开浏览器**，访问招聘网站
2. **搜索一个职位**，如"Python 北京"
3. **右键检查**，查看HTML结构
4. **记录关键选择器**：
   - 职位列表容器
   - 职位标题元素
   - 公司名称元素
   - 薪资信息元素
   - 地点和经验要求

#### 方法2：使用测试脚本

创建测试脚本查看实际HTML：

```python
# test_page_structure.py
import requests
from bs4 import BeautifulSoup

url = "https://www.zhipin.com/web/geek/job?query=Python&city=101010100"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 保存HTML供分析
with open('boss_structure.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print("HTML已保存，请查看页面结构")
```

### 第三步：更新解析器选择器

根据实际页面结构，更新对应的解析器文件：

#### 1. BOSS直聘 (`boss_parser.py`)

```python
# 更新选择器示例
def _parse_html_results(self, html: str):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 根据实际页面结构调整这些选择器
    job_items = soup.select('.job-list li')  # 需要验证
    # 或: job_items = soup.select('.job-card-wrapper')
    # 或: job_items = soup.select('[class*="job-item"]')
    
    for item in job_items:
        # 提取信息
        title_elem = item.select_one('.job-title')  # 需要验证
        company_elem = item.select_one('.company-name')  # 需要验证
        # ... 其他元素
```

#### 2. 智联招聘 (`zhilian_parser.py`)

```python
def _parse_html_results(self, html: str):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 智联招聘可能的选择器
    job_items = soup.select('.joblist__item')  # 需要验证
    # 或: job_items = soup.select('.contentpile__content__wrapper')
    
    for item in job_items:
        # 提取信息
        title_elem = item.select_one('.joblist__item__title')  # 需要验证
        # ... 其他元素
```

#### 3. 前程无忧 (`qiancheng_parser.py`)

```python
def _parse_html_results(self, html: str):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 前程无忧可能的选择器
    job_items = soup.select('.j_joblist .e')  # 需要验证
    # 或: job_items = soup.select('.dw_table .el')
    
    for item in job_items:
        # 提取信息
        title_elem = item.select_one('.jname')  # 需要验证
        # ... 其他元素
```

### 第四步：处理反爬机制

#### 策略1：请求头伪装

```python
# 在解析器中添加
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.zhipin.com/',
    'Cache-Control': 'max-age=0',
}
```

#### 策略2：添加延迟

```python
import time
import random

def _add_delay(self):
    """随机延迟1-3秒"""
    delay = random.uniform(1.0, 3.0)
    time.sleep(delay)
```

#### 策略3：使用会话和Cookie

```python
self.session = requests.Session()
self.session.headers.update(headers)

# 可以预先访问首页获取Cookie
home_response = self.session.get('https://www.zhipin.com/', timeout=10)
```

#### 策略4：代理支持（如果需要）

```python
proxies = {
    'http': 'http://your-proxy:port',
    'https': 'http://your-proxy:port',
}

response = self.session.get(url, proxies=proxies, timeout=15)
```

### 第五步：测试和验证

#### 创建测试脚本

```python
# test_platforms.py
from enhanced_searcher import EnhancedJobSearcher

searcher = EnhancedJobSearcher()

# 测试各平台
test_cases = [
    ('BOSS直聘', 'Python', '北京'),
    ('智联招聘', 'Java', '上海'),
    ('前程无忧', '前端', '广州'),
]

for platform_name, keyword, city in test_cases:
    print(f"\n测试 {platform_name}: {keyword} - {city}")
    
    if platform_name == 'BOSS直聘':
        jobs = searcher.search_boss(keyword, city, 5)
    elif platform_name == '智联招聘':
        jobs = searcher.search_zhilian(keyword, city, 5)
    # ... 其他平台
    
    print(f"找到 {len(jobs)} 个岗位")
    for job in jobs[:3]:
        print(f"  - {job.title} | {job.company} | {job.salary}")
```

#### 验证数据准确性

1. **手动对比**：与网站实际显示对比
2. **检查完整性**：确保所有字段都有数据
3. **测试边界情况**：空结果、特殊字符等

### 第六步：集成到OpenClaw

#### 方法1：直接调用

```python
# 在OpenClaw工作区创建脚本
from skills.job_search.enhanced_searcher import EnhancedJobSearcher

searcher = EnhancedJobSearcher()
results = searcher.search_all_platforms('Python', '北京', 20)
print(searcher.format_results(results))
```

#### 方法2：创建OpenClaw命令

```python
# 创建自定义命令
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'skills', 'job-search'))

def search_jobs(keyword, city='北京', platforms='all'):
    from enhanced_searcher import EnhancedJobSearcher
    searcher = EnhancedJobSearcher()
    
    if platforms == 'all':
        results = searcher.search_all_platforms(keyword, city, 20)
    else:
        # 处理指定平台
        pass
    
    return searcher.format_results(results)

# 在OpenClaw中注册这个函数
```

#### 方法3：定时任务

```python
# 创建定时搜索任务
import schedule
import time

def daily_job_search():
    searcher = EnhancedJobSearcher()
    results = searcher.search_all_platforms('Python', '北京', 30)
    
    # 保存或发送结果
    with open('daily_jobs.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(searcher.format_results(results))
    
    print("每日搜索完成")

# 每天上午9点执行
schedule.every().day.at("09:00").do(daily_job_search)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 故障排除

### 问题1：返回空结果
**可能原因**：
- 选择器不正确
- 网站结构已更新
- 触发了反爬机制

**解决方案**：
1. 重新检查页面结构
2. 更新选择器
3. 添加更好的请求头伪装
4. 增加延迟

### 问题2：被网站屏蔽
**可能原因**：
- 请求频率过高
- User-Agent被识别
- IP被限制

**解决方案**：
1. 增加请求间隔
2. 轮换User-Agent
3. 使用代理IP
4. 使用Selenium浏览器自动化

### 问题3：数据解析错误
**可能原因**：
- HTML结构变化
- 编码问题
- 数据格式不一致

**解决方案**：
1. 添加异常处理
2. 验证数据格式
3. 使用更宽松的选择器

## 高级功能扩展

### 1. 数据持久化
```python
import sqlite3

def save_to_database(jobs):
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            platform TEXT,
            title TEXT,
            company TEXT,
            salary TEXT,
            location TEXT,
            experience TEXT,
            education TEXT,
            skills TEXT,
            url TEXT,
            publish_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    for job in jobs:
        cursor.execute('''
            INSERT INTO jobs (platform, title, company, salary, location, 
                            experience, education, skills, url, publish_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (job.platform, job.title, job.company, job.salary, job.location,
              job.experience, job.education, ','.join(job.skills), job.url, job.publish_time))
    
    conn.commit()
    conn.close()
```

### 2. 邮件通知
```python
import smtplib
from email.mime.text import MIMEText

def send_email_notification(jobs, recipient):
    # 构建邮件内容
    content = "发现新岗位:\n\n"
    for job in jobs:
        content += f"- {job.title} | {job.company} | {job.salary}\n"
    
    # 发送邮件
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = '招聘岗位更新通知'
    msg['From'] = 'your-email@example.com'
    msg['To'] = recipient
    
    # 配置SMTP发送
    # ...
```

### 3. 数据分析和可视化
```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_jobs(jobs):
    # 转换为DataFrame
    df = pd.DataFrame([{
        'platform': job.platform,
        'title': job.title,
        'company': job.company,
        'salary_min': extract_min_salary(job.salary),
        'salary_max': extract_max_salary(job.salary),
        'location': job.location,
        'experience': job.experience
    } for job in jobs])
    
    # 分析薪资分布
    plt.figure(figsize=(10, 6))
    df.groupby('platform')['salary_avg'].mean().plot(kind='bar')
    plt.title('各平台平均薪资对比')
    plt.savefig('salary_comparison.png')
```

## 维护建议

1. **定期检查**：每月检查一次网站结构
2. **监控日志**：记录搜索成功率和错误
3. **备份配置**：保存可用的选择器配置
4. **社区更新**：关注相关开源项目的更新

## 获取帮助

如果遇到问题：
1. 查看各解析器的错误日志
2. 手动测试网站访问
3. 检查网络连接和代理设置
4. 参考requests和BeautifulSoup文档

---

**最后更新**: 2024-01-01  
**版本**: 1.0.0  
**维护者**: OpenClaw技能库