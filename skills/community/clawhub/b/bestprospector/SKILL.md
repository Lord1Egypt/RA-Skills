---
name: prospector
description: |
  根据关键词自动搜索潜在客户公司，提取联系方式（邮箱），输出结构化客户列表。
  
  适用场景：
  - 用户需要寻找潜在客户时
  - 用户需要获取公司联系方式时
  - 用户提到"找客户"、"获客"、"销售线索"、"潜在客户"等关键词
  - 用户需要查询已收集的客户数据
  
  功能：
  1. 根据关键词和地区搜索潜在客户公司
  2. 访问公司官网提取邮箱地址
  3. 通过WHOIS查询域名注册邮箱
  4. 验证邮箱格式有效性
  5. 输出结构化的客户列表（JSON/CSV格式）
  6. 自动缓存结果，避免重复搜索
  7. 自动排重，跳过已存在的公司
  8. 查询已收集的客户数据（简单查询）
  
  注意：此Skill只负责"找客户"和"简单查询"，不负责"发邮件"和"客户管理"。发送邮件请使用其他邮件相关Skill，复杂客户管理请使用专门的客户管理工具。

user-invocable: true
metadata:
  openclaw:
    emoji: "⛏️"
    requires:
      bins: ["python3", "curl"]
    install:
      - id: pip
        kind: pip
        package: requests,beautifulsoup4,python-whois,dnspython
        label: "Install Python dependencies"
---

# Prospector - 潜在客户挖掘器

## 快速开始

用户只需描述目标客户，即可自动搜索并提取联系方式：

```
用户：帮我找上海地区的软件外包公司
用户：搜索北京的人工智能企业，需要50家
用户：找一些外贸公司，规模大一点的
用户：继续找更多软件公司（翻页搜索）
用户：查看已收集的客户列表
用户：搜索包含"阿里"的客户
```

## 工作流程

### 找客户流程

#### Step 1: 解析需求
- 提取关键词：行业、产品、服务类型
- 提取地区：城市、省份、国家
- 提取数量：需要多少家

#### Step 2: 检查缓存
- 检查是否有相同关键词的缓存结果
- 缓存有效期：7天
- 如果有缓存，直接返回，避免重复搜索

#### Step 3: 搜索公司
- 调用 scripts/search_companies.py
- 使用多搜索引擎：Google、DuckDuckGo、Bing、百度、Searx
- 支持代理访问（Google等需要代理）
- 返回公司名称、域名、简介

#### Step 4: 排重处理
- 检查公司是否已存在于数据库
- 跳过已处理的公司
- 只处理新公司

#### Step 5: 提取邮箱
- 调用 scripts/extract_emails.py
- 爬取官网页面提取邮箱
- WHOIS查询域名注册信息
- 缓存邮箱结果

#### Step 6: 输出结果
- 结构化JSON格式
- 可选CSV导出
- 统计汇总信息

### 查询客户流程

#### Step 1: 解析查询意图
- 列表查询：列出已收集的客户
- 关键词搜索：按公司名搜索
- 邮箱搜索：按邮箱关键词搜索
- 统计查询：查看数据统计

#### Step 2: 从缓存读取
- 从本地缓存读取客户数据
- 支持多种筛选条件

#### Step 3: 返回结果
- 表格或JSON格式
- 支持导出

## 使用示例

### 找客户示例

#### 示例1：首次搜索
```
用户：帮我找10家上海的SaaS公司

执行：
1. 搜索 "上海 SaaS公司"
2. 提取邮箱
3. 缓存结果
4. 返回结果

输出：
📊 搜索结果
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 找到公司：10家
✅ 有效邮箱：7个

📈 累计数据：
   总公司数：10
   总邮箱数：7
```

#### 示例2：再次搜索相同关键词
```
用户：帮我找上海的SaaS公司

执行：
1. 检查缓存 → 发现缓存
2. 使用缓存结果
3. 跳过已存在的公司

输出：
📦 使用缓存结果 (10 家公司)
⏭️ 跳过 10 家已存在的公司
✅ 待处理 0 家公司
```

#### 示例3：翻页搜索更多
```
用户：继续找更多上海的SaaS公司

执行：
1. 翻页偏移：跳过前10条
2. 搜索新的结果
3. 跳过已存在的公司
4. 返回新公司

输出：
🔍 搜索: 上海 SaaS公司
   翻页偏移: 10
⏭️ 跳过 3 家已存在的公司
✅ 待处理 7 家公司
```

### 查询客户示例

#### 示例4：列出所有客户
```
用户：查看已收集的客户列表

执行：
python scripts/query_customers.py list --limit 20

输出：
📋 客户列表 (共 50 家)

序号  公司名称                          域名                       邮箱                            
────────────────────────────────────────────────────────────────────────────────────────
1     XX科技有限公司                     xx.com                     contact@xx.com, sales@xx.com
2     YY信息技术有限公司                   yy.com                     info@yy.com
...
```

#### 示例5：按关键词搜索客户
```
用户：搜索包含"阿里"的客户

执行：
python scripts/query_customers.py search "阿里"

输出：
🔍 搜索结果: 阿里 (共 3 家)

• 阿里巴巴科技有限公司
  邮箱: contact@alibaba.com

• 阿里云智能有限公司
  邮箱: support@aliyun.com
```

#### 示例6：按邮箱搜索
```
用户：查找包含"sales"的邮箱

执行：
python scripts/query_customers.py email sales

输出：
📧 邮箱搜索: sales (共 15 家)

• XX科技有限公司
  匹配: sales@xx.com
```

#### 示例7：查看数据统计
```
用户：查看已收集的客户数据统计

执行：
python scripts/query_customers.py stats

输出：
📊 数据统计
========================================
总公司数: 50
总邮箱数: 35
搜索次数: 5
有邮箱公司: 30
邮箱覆盖率: 60.0%
```

#### 示例8：导出数据
```
用户：导出所有客户数据

执行：
python scripts/query_customers.py export --output customers.json --csv customers.csv

输出：
✅ 已导出 50 条数据到 customers.json
✅ 已导出 50 条数据到 customers.csv
```

## 缓存机制

### 缓存内容
- 搜索结果缓存（按关键词+地区）
- 公司信息缓存（按域名）
- 邮箱缓存（按域名）

### 缓存有效期
- 搜索缓存：7天
- 公司信息：永久
- 邮箱信息：永久

### 缓存位置
```
AutoFindCustomer/
└── cache/
    ├── companies.json    # 公司数据库
    ├── searches.json     # 搜索缓存
    └── emails.json       # 邮箱缓存
```

## 命令行参数

### 找客户命令

```bash
# 基本搜索
python scripts/find_customers.py "软件开发" --region "上海" --limit 20

# 不使用缓存
python scripts/find_customers.py "软件开发" --no-cache

# 不跳过已存在的公司
python scripts/find_customers.py "软件开发" --no-skip

# 翻页搜索（获取更多不同结果）
python scripts/find_customers.py "软件开发" --page 10

# 查看缓存统计
python scripts/find_customers.py --stats

# 导出结果
python scripts/find_customers.py "软件开发" --output results.json --csv results.csv
```

### 查询客户命令

```bash
# 列出客户
python scripts/query_customers.py list --limit 20

# 只显示有邮箱的客户
python scripts/query_customers.py list --has-email

# 只显示无邮箱的客户
python scripts/query_customers.py list --no-email

# JSON格式输出
python scripts/query_customers.py list --json

# 按关键词搜索
python scripts/query_customers.py search "关键词" --region "上海"

# 按邮箱搜索
python scripts/query_customers.py email "sales"

# 查看统计
python scripts/query_customers.py stats

# 导出数据
python scripts/query_customers.py export --output export.json --csv export.csv
```

## 输出格式

### JSON格式
```json
{
  "query": "上海 软件公司",
  "total_companies": 50,
  "total_emails": 35,
  "email_coverage": "70.0%",
  "results": [
    {
      "name": "XX科技有限公司",
      "domain": "xx.com",
      "url": "https://xx.com",
      "emails": ["contact@xx.com", "sales@xx.com"],
      "description": "专业软件开发服务"
    }
  ]
}
```

### CSV格式
```
公司名称,域名,邮箱,网址,简介
XX科技有限公司,xx.com,contact@xx.com,https://xx.com,专业软件开发服务
YY信息技术有限公司,yy.com,sales@yy.com,https://yy.com,IT解决方案
```

## 职责边界

### ✅ 负责
- 搜索潜在客户
- 提取联系方式
- 验证邮箱格式
- 简单查询客户数据
- 导出客户数据
- 数据统计

### ❌ 不负责
- 发送邮件（由其他Skill处理）
- 复杂客户管理（标签、分类、跟进状态）
- 客户备注记录
- 发送历史追踪
- 回复状态管理

## 与其他Skill配合

找到客户后，可以使用其他Skill进行后续操作：

```
用户：帮我找上海的外贸公司，然后给每家公司发一封开发信

Agent会：
1. 调用 auto-find-customer Skill 找客户
2. 调用 send-email Skill 发邮件
```

复杂客户管理建议使用专门的CRM工具或独立的customer-manager Skill。

## 注意事项

1. 搜索速度受网络影响，建议控制并发
2. 部分网站可能无法访问，会自动跳过
3. 邮箱提取成功率约60-70%
4. 建议搜索后人工复核关键客户
5. 缓存数据会累积，形成客户资产
6. 使用 --page 参数可以获取更多不同结果
7. 简单查询功能在此Skill内，复杂管理建议使用CRM系统

## 搜索引擎说明

### 支持的搜索引擎

| 引擎 | 代理需求 | 地区限制 | 说明 |
|------|----------|----------|------|
| Google | ✅ 需要 | 中国、伊朗、朝鲜、俄罗斯 | 结果质量最高 |
| DuckDuckGo | ❌ 无需 | 无 | 推荐使用 |
| Bing | ❌ 无需 | 中国 | 结果质量较好 |
| 百度 | ❌ 无需 | 无 | 适合中文搜索 |
| Searx | ❌ 无需 | 无 | 开源元搜索引擎 |

### 代理设置

如果用户在中国大陆等需要代理的地区，需要设置代理：

```bash
# 环境变量方式
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890

# 或命令行参数
python scripts/search_companies.py "software company" --proxy http://127.0.0.1:7890
```

### 地区推荐

- **中国大陆**：使用百度、DuckDuckGo、Searx（无需代理）
- **海外**：可使用所有搜索引擎，Google 效果最佳
- **俄罗斯**：使用 DuckDuckGo、Bing、Searx（Google 被屏蔽）
