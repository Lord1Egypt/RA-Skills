# 数据源说明

## 数据源概览

| 数据源 | 数据类型 | 需登录 | 自动化 | 数据质量 |
|--------|----------|--------|--------|----------|
| 天眼查 | 工商、股权、诉讼 | ✅ 付费会员 | ✅ Playwright | ⭐⭐⭐⭐⭐ |
| 企查查 | 工商、股权、诉讼 | ✅ 付费会员 | ✅ Playwright | ⭐⭐⭐⭐⭐ |
| 巨潮资讯 | 上市公司公告 | ❌ | ✅ HTTP | ⭐⭐⭐⭐⭐ |
| 上交所 | 公司详细信息 | ❌ | ✅ HTTP | ⭐⭐⭐⭐ |
| 深交所 | 公司详细信息 | ❌ | ✅ HTTP | ⭐⭐⭐⭐ |
| 裁判文书网 | 诉讼判决 | ❌ | ⚠️ 验证码 | ⭐⭐⭐⭐ |
| 执行信息公开网 | 失信记录 | ❌ | ⚠️ 验证码 | ⭐⭐⭐⭐ |
| 国家企业信用网 | 工商信息 | ❌ | ❌ 反爬严格 | ⭐⭐⭐ |
| 百度搜索 | 舆情信息 | ❌ | ✅ HTTP | ⭐⭐⭐ |

---

## 一、天眼查

### 网址
https://www.tianyancha.com/

### 数据内容
- ✅ 工商信息（注册资本、法人、成立时间等）
- ✅ 股东结构（股东穿透图）
- ✅ 关联企业（集团关系图谱）
- ✅ 诉讼记录
- ✅ 失信信息
- ✅ 行政处罚
- ✅ 知识产权
- ✅ 招投标
- ✅ 财务数据（部分）

### 登录要求
- **免费版**: 每日查询次数有限，部分信息不可见
- **VIP会员**: ¥ 366/年，完整信息
- **企业版**: ¥ 1998/年，API 接口

### Playwright 自动化

```python
from playwright.sync_api import sync_playwright

def login_tianyancha(page, username, password):
    """天眼查登录"""
    page.goto("https://www.tianyancha.com/login")
    
    # 切换到密码登录
    page.click("text=密码登录")
    
    # 输入账号密码
    page.fill('input[placeholder="请输入手机号"]', username)
    page.fill('input[placeholder="请输入密码"]', password)
    
    # 点击登录
    page.click("button:has-text('登录')")
    
    # 等待登录成功
    page.wait_for_url("**/company/**", timeout=30000)

def query_company(page, company_name):
    """查询公司信息"""
    # 搜索公司
    page.fill('input[placeholder="请输入公司名、人名等"]', company_name)
    page.press('input[placeholder="请输入公司名、人名等"]', 'Enter')
    
    # 点击第一个结果
    page.click('.search-result-item:first-child a')
    
    # 等待页面加载
    page.wait_for_selector('.company-info')
    
    # 提取数据
    data = {
        'name': page.text_content('.company-name'),
        'legal_person': page.text_content('.legal-person'),
        'capital': page.text_content('.capital'),
        # ... 更多字段
    }
    
    return data
```

### 反爬策略
- 验证码（登录时）
- 请求频率限制
- IP 黑名单

### 应对方案
- 使用 Playwright 模拟真人操作
- 随机延迟（2-5秒）
- 代理 IP 池

---

## 二、企查查

### 网址
https://www.qcc.com/

### 数据内容
- ✅ 工商信息
- ✅ 股东结构
- ✅ 关联企业
- ✅ 诉讼记录
- ✅ 失信信息
- ✅ 行政处罚
- ✅ 财务数据（更详细）
- ✅ 招聘信息

### 登录要求
- **免费版**: 基础信息
- **VIP会员**: ¥ 298/年
- **SVIP会员**: ¥ 598/年

### Playwright 自动化

```python
def login_qichacha(page, username, password):
    """企查查登录"""
    page.goto("https://www.qcc.com/")
    
    # 点击登录按钮
    page.click("text=登录")
    
    # 切换到账号密码登录
    page.click("text=密码登录")
    
    # 输入账号密码
    page.fill('input[placeholder="手机号/用户名"]', username)
    page.fill('input[placeholder="密码"]', password)
    
    # 点击登录
    page.click("button:has-text('登录')")
    
    # 等待登录成功
    page.wait_for_selector('.user-info', timeout=30000)
```

---

## 三、巨潮资讯网

### 网址
http://www.cninfo.com.cn/

### 数据内容
- ✅ 上市公司公告（年报、季报、临时公告）
- ✅ 公司基本信息
- ✅ 股东变动
- ✅ 财务报告

### 登录要求
- ❌ 无需登录

### HTTP 自动化

```python
import requests
from bs4 import BeautifulSoup

def search_listed_company(keyword):
    """搜索上市公司"""
    url = "http://www.cninfo.com.cn/new/fulltextSearch"
    
    params = {
        'searchtype': 'company',
        'keyword': keyword,
        'sdate': '',
        'edate': '',
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    companies = []
    for item in soup.select('.company-item'):
        companies.append({
            'name': item.select_one('.company-name').text,
            'code': item.select_one('.stock-code').text,
            'url': item.select_one('a')['href']
        })
    
    return companies

def get_announcements(stock_code, page=1):
    """获取公告列表"""
    url = "http://www.cninfo.com.cn/new/hisAnnouncementQuery"
    
    data = {
        'stock': f'{stock_code},',
        'tabName': 'fulltext',
        'pageSize': 30,
        'pageNum': page,
    }
    
    response = requests.post(url, data=data)
    result = response.json()
    
    return result.get('announcements', [])
```

---

## 四、中国裁判文书网

### 网址
http://wenshu.court.gov.cn/

### 数据内容
- ✅ 诉讼判决书
- ✅ 裁定书
- ✅ 调解书

### 登录要求
- ❌ 无需登录，但有验证码

### 自动化难点
- 验证码（图片+滑动）
- 请求加密
- 反爬严格

### 推荐方案
```python
# 方案1: 使用第三方 API（付费）
# 方案2: 手动查询 + 自动化记录
# 方案3: OCR 识别验证码（成功率一般）

def get_court_cases(company_name):
    """获取诉讼查询指引"""
    return {
        'url': 'http://wenshu.court.gov.cn/',
        'search_keywords': [
            company_name,
            f'"{company_name}"',
            f'被告:{company_name}',
            f'原告:{company_name}',
        ],
        'tips': [
            '1. 访问裁判文书网',
            '2. 输入验证码',
            '3. 在当事人栏输入公司名称',
            '4. 按时间倒序排列查看最新案件',
        ]
    }
```

---

## 五、中国执行信息公开网

### 网址
http://zxgk.court.gov.cn/

### 数据内容
- ✅ 被执行人信息
- ✅ 失信被执行人信息
- ✅ 限制消费人员信息
- ✅ 终结本次执行案件

### 登录要求
- ❌ 无需登录，但有验证码

### 查询入口

```
综合查询: http://zxgk.court.gov.cn/
失信被执行人: http://zxgk.court.gov.cn/shixin/
被执行人: http://zxgk.court.gov.cn/zhixing/
限制消费: http://zxgk.court.gov.cn/xiaofei/
```

---

## 六、国家企业信用信息公示系统

### 网址
http://www.gsxt.gov.cn/

### 数据内容
- ✅ 工商登记信息
- ✅ 行政处罚
- ✅ 经营异常
- ✅ 严重违法

### 自动化难度
- ⚠️ 反爬非常严格
- ⚠️ 需要滑动验证码
- ⚠️ 频繁 IP 封禁

### 推荐
- 使用天眼查/企查查代替
- 或手动查询

---

## 七、百度搜索

### 网址
https://www.baidu.com/

### 数据内容
- ✅ 新闻报道
- ✅ 舆情信息
- ✅ 负面新闻

### 自动化

```python
import requests
from bs4 import BeautifulSoup

def search_news(company_name, keywords=None):
    """搜索舆情信息"""
    query = company_name
    if keywords:
        query += ' ' + ' '.join(keywords)
    
    url = "https://www.baidu.com/s"
    params = {
        'wd': query,
        'tn': 'news',
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news = []
    for item in soup.select('.result'):
        news.append({
            'title': item.select_one('h3 a').text,
            'url': item.select_one('h3 a')['href'],
            'source': item.select_one('.c-showurl').text,
            'date': item.select_one('.c-color-gray').text,
        })
    
    return news
```

---

## 付费 API 推荐

如需完全自动化，建议使用以下付费 API：

### 天眼查 API
- 网址: https://open.tianyancha.com/
- 价格: 按次计费，约 0.01-0.1 元/次
- 优势: 数据全面、稳定可靠

### 企查查 API
- 网址: https://openapi.qcc.com/
- 价格: 按次计费，约 0.01-0.1 元/次
- 优势: 数据全面、API 文档完善

### 启信宝 API
- 网址: https://openapi.qixin.com/
- 价格: 按次计费
- 优势: 数据质量高

---

## 数据源选择建议

| 场景 | 推荐数据源 |
|------|------------|
| 上市公司尽调 | 巨潮资讯 + 天眼查/企查查 |
| 非上市公司尽调 | 天眼查/企查查（付费） |
| 快速风险排查 | 裁判文书网 + 执行信息公开网 |
| 批量查询 | 天眼查/企查查 API |
| 成本敏感 | 公开数据源 + 手动补充 |
