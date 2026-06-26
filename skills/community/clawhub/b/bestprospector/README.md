# Prospector

OpenClaw Skill - 潜在客户挖掘器，自动搜索潜在客户并提取联系方式

## 功能特性

- 🔍 **多搜索引擎支持**：Google、DuckDuckGo、Bing、百度、Searx
- 📧 **智能邮箱提取**：官网爬取 + WHOIS查询
- ✅ **邮箱验证**：格式验证 + DNS检查
- 💾 **本地缓存**：自动缓存，避免重复搜索
- 🔄 **智能排重**：跳过已存在的公司
- 🌐 **代理支持**：支持 HTTP/HTTPS 代理
- 📊 **数据统计**：查看累计数据
- 📤 **多格式导出**：JSON / CSV

## 快速开始

### 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 基本使用

```bash
# 搜索客户
python scripts/find_customers.py "软件开发" --region "上海" --limit 20

# 查看统计
python scripts/query_customers.py stats

# 导出数据
python scripts/query_customers.py export --csv customers.csv
```

### 安装到OpenClaw

```bash
# 复制到OpenClaw的skills目录
cp -r . ~/.openclaw/workspace/skills/prospector

# 重启Gateway
openclaw gateway restart
```

## 命令详解

### find_customers.py - 找客户

```bash
# 基本搜索
python scripts/find_customers.py "关键词"

# 指定地区
python scripts/find_customers.py "软件开发" --region "上海"

# 限制数量
python scripts/find_customers.py "软件开发" --limit 50

# 翻页搜索（获取更多不同结果）
python scripts/find_customers.py "软件开发" --page 10

# 导出结果
python scripts/find_customers.py "软件开发" --output results.json --csv results.csv

# 不使用缓存
python scripts/find_customers.py "软件开发" --no-cache

# 不跳过已存在的公司
python scripts/find_customers.py "软件开发" --no-skip

# 查看缓存统计
python scripts/find_customers.py --stats
```

### query_customers.py - 查询客户

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
python scripts/query_customers.py search "阿里"

# 按邮箱搜索
python scripts/query_customers.py email "sales"

# 查看统计
python scripts/query_customers.py stats

# 导出数据
python scripts/query_customers.py export --output export.json --csv export.csv
```

### search_companies.py - 搜索公司

```bash
# 基本搜索
python scripts/search_companies.py "software company"

# 指定地区和数量
python scripts/search_companies.py "软件开发" --region "上海" --limit 50

# 指定搜索引擎
python scripts/search_companies.py "软件开发" --engines google,duckduckgo

# 使用代理
python scripts/search_companies.py "software company" --proxy http://127.0.0.1:7890

# 查看支持的搜索引擎
python scripts/search_companies.py --list-engines

# 导出结果
python scripts/search_companies.py "软件开发" --output search_results.json
```

### extract_emails.py - 提取邮箱

```bash
# 提取单个域名
python scripts/extract_emails.py example.com

# 不使用WHOIS
python scripts/extract_emails.py example.com --no-whois

# 使用代理
python scripts/extract_emails.py example.com --proxy http://127.0.0.1:7890

# 导出结果
python scripts/extract_emails.py example.com --output emails.json
```

### validate_email.py - 验证邮箱

```bash
# 验证单个邮箱
python scripts/validate_email.py test@example.com

# 批量验证
python scripts/validate_email.py --batch emails.json

# 跳过DNS验证
python scripts/validate_email.py test@example.com --no-dns
```

## 输出格式

### JSON格式

```json
{
  "query": "软件开发",
  "region": "上海",
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

```csv
公司名称,域名,邮箱,网址,简介
XX科技有限公司,xx.com,contact@xx.com,https://xx.com,专业软件开发服务
YY信息技术有限公司,yy.com,sales@yy.com,https://yy.com,IT解决方案
```

## 缓存机制

### 缓存内容

| 缓存类型 | 文件 | 有效期 | 说明 |
|----------|------|--------|------|
| 搜索缓存 | `cache/searches.json` | 7天 | 按关键词+地区缓存搜索结果 |
| 公司缓存 | `cache/companies.json` | 永久 | 已收集的公司信息 |
| 邮箱缓存 | `cache/emails.json` | 永久 | 已提取的邮箱地址 |

### 缓存管理

```bash
# 查看缓存统计
python scripts/query_customers.py stats

# 清理过期缓存
python scripts/cache_manager.py clear

# 导出所有缓存数据
python scripts/cache_manager.py export
```

## 在OpenClaw中使用

### 找客户

```
用户：帮我找上海地区的软件外包公司
用户：搜索北京的人工智能企业，需要50家
用户：继续找更多软件公司
```

### 查询客户

```
用户：查看已收集的客户列表
用户：搜索包含"阿里"的客户
用户：查找包含"sales"的邮箱
用户：查看数据统计
用户：导出所有客户数据
```

### 配合其他Skill

```
用户：帮我找上海的外贸公司，然后给每家公司发一封开发信

Agent会：
1. 调用 prospector Skill 找客户
2. 调用 send-email Skill 发邮件
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

## 搜索引擎

### 支持的搜索引擎

| 引擎 | 代理需求 | 地区限制 | 说明 |
|------|----------|----------|------|
| **Google** | ✅ 需要 | 中国、伊朗、朝鲜、俄罗斯 | 全球最大搜索引擎，结果质量最高 |
| **DuckDuckGo** | ❌ 无需 | 无 | 注重隐私的搜索引擎，推荐使用 |
| **Bing** | ❌ 无需 | 中国 | 微软搜索引擎，结果质量较好 |
| **百度** | ❌ 无需 | 无 | 中国最大搜索引擎，适合中文搜索 |
| **Searx** | ❌ 无需 | 无 | 开源元搜索引擎，聚合多个结果 |

### 查看支持的搜索引擎

```bash
python scripts/search_companies.py --list-engines
```

### 指定搜索引擎

```bash
# 使用所有搜索引擎（默认）
python scripts/search_companies.py "软件开发"

# 只使用特定搜索引擎
python scripts/search_companies.py "软件开发" --engines google,duckduckgo

# 只用国内可用的搜索引擎
python scripts/search_companies.py "软件开发" --engines baidu,duckduckgo
```

### 代理设置

Google 等搜索引擎在某些地区需要代理访问：

```bash
# 方式1：命令行参数
python scripts/search_companies.py "software company" --proxy http://127.0.0.1:7890

# 方式2：环境变量
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
python scripts/search_companies.py "software company"

# 方式3：ALL_PROXY 环境变量
export ALL_PROXY=http://127.0.0.1:7890
python scripts/search_companies.py "software company"
```

### 地区使用建议

| 地区 | 推荐引擎 | 说明 |
|------|----------|------|
| 中国大陆 | 百度、DuckDuckGo、Searx | 无需代理，DuckDuckGo 结果更国际化 |
| 中国香港/台湾 | Google、DuckDuckGo、Bing | 可直接访问 Google |
| 美国/欧洲 | Google、DuckDuckGo、Bing | 所有引擎均可使用 |
| 俄罗斯 | DuckDuckGo、Bing、Searx | Google 被屏蔽 |
| 伊朗/朝鲜 | DuckDuckGo、Searx | 大部分搜索引擎被屏蔽 |

### 邮箱提取

| 来源 | 说明 |
|------|------|
| 官网首页 | 提取页面中的邮箱 |
| 联系页面 | 访问/contact等页面 |
| WHOIS | 查询域名注册信息 |

### 邮箱验证

- 格式验证：正则匹配
- 域名验证：MX记录检查
- 一次性邮箱：黑名单过滤

## 注意事项

1. **搜索速度**：受网络影响，建议控制并发
2. **网站访问**：部分网站可能无法访问，会自动跳过
3. **邮箱准确率**：约60-70%，建议人工复核
4. **缓存数据**：会累积形成客户资产
5. **翻页搜索**：使用 `--page` 参数获取更多不同结果
6. **合规使用**：数据来源于公开信息，请遵守当地法规

## 项目结构

```
prospector/
├── SKILL.md                      # OpenClaw Skill配置
├── README.md                     # 本文档
├── scripts/
│   ├── find_customers.py         # 找客户（主入口）
│   ├── query_customers.py        # 查询客户
│   ├── search_companies.py       # 搜索公司
│   ├── extract_emails.py         # 提取邮箱
│   ├── validate_email.py         # 验证邮箱
│   ├── cache_manager.py          # 缓存管理
│   └── requirements.txt          # Python依赖
└── cache/                        # 缓存数据（自动生成）
    ├── companies.json            # 公司数据库
    ├── searches.json             # 搜索缓存
    └── emails.json               # 邮箱缓存
```

## 依赖说明

| 包名 | 版本 | 用途 |
|------|------|------|
| requests | >=2.28.0 | HTTP请求 |
| beautifulsoup4 | >=4.11.0 | HTML解析 |
| python-whois | >=0.8.0 | WHOIS查询 |
| dnspython | >=2.3.0 | DNS验证 |

## 更新日志

### v1.1.0 (2026-03-09)

- 新增 Google 搜索引擎支持
- 新增 Searx 元搜索引擎支持
- 新增代理支持（HTTP/HTTPS/ALL_PROXY）
- 新增 `--list-engines` 命令查看支持的搜索引擎
- 新增 `--engines` 参数指定搜索引擎
- 新增 `--proxy` 参数设置代理
- 优化搜索引擎选择逻辑，按顺序尝试多个引擎
- 添加地区限制和代理需求说明

### v1.0.0 (2026-03-09)

- 初始版本
- 支持多搜索引擎搜索
- 支持邮箱提取和验证
- 支持本地缓存和排重
- 支持查询和导出功能

## License

MIT
