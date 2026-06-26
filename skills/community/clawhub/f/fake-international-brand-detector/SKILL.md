# ✅ Fake International Brand Detector - Enhanced v2.0 [已激活]

## 📢 技能状态
- **🟢 激活状态**: ✅ 已启用（默认自动运行）
- **🎯 触发条件**: 检测到用户询问"假国际品牌"、"品牌真实性"、"保健品品牌"等关键词时自动调用
- **⚙️ 默认参数**: `--brand {品牌名} --mode quick`
- **📁 文件路径**: `/home/admin/.openclaw/workspace/skills/fake-international-brand-detector/`

一个用于检测"假国际品牌"的智能 Agent 技能（增强版）。

## 📋 功能说明

通过**七项维度**验证品牌的国际化真实性（基于 NYO3 验证经验优化）：

### 原有四项（核心维度）
1. **海外官网** - 检查是否存在成熟的多语言海外官方网站
2. **海外销售渠道** - 验证线下/线上海外零售渠道
3. **跨境电商记录** - 在亚马逊等平台的全球销售历史
4. **海外媒体曝光** - 国际媒体报道和广告记录

### 新增三项（识别假国际特征）
5. **WHOIS 注册地核查** - 检查域名 registrant_country 是否为品牌宣称的本土国家
6. **商标注册时间线分析** - 对比中国市场/海外市场的商标注册时间先后
7. **销售渠道运营者国籍** - 检查 Amazon.de/.co.uk店铺运营者所在国家（非店铺名称）

## 🎯 判定规则（更新版）

| 有效高质量项数量 | 品牌类型 |
|-----------|---------|
| ≥5 项高质量内容 | ✅ 真国际品牌 |
| 3-4 项/混合质量 | ⚠️ 存疑品牌 |
| ≤2 项或假国际特征明显 | ❌ 假国际品牌 |

**"有质量的内容"标准**（优化版）：

| 验证项 | 真国际品牌标准 | 假国际品牌特征 |
|--|-|-|
| **官网 WHOIS** | registrant_country=本土国家 + 多语言 + 正规备案 | CN/中国邮箱 (@qq.com) + 机器翻译内容 |
| **销售渠道** | 至少 2 家欧洲本土连锁药房直营/授权 | 仅 Amazon.de/.co.uk店铺，无Boots/Holland&Barrett等 |
| **销售记录** | ≥4 个国际站点持续销售≥6 个月 | 0-1 个站点或仅 Amazon.cn + 新注册店铺 |
| **媒体报道** | Reuters/Forbes/WebMD/BBC报道≥5 篇 | 无权威媒体，仅有博客/软文/中文内容 |
| **WHOIS 核查** | registrant_country=本土国家 | CN/中国邮箱/地址（即使域名是.com）|
| **商标时间线** | 海外注册时间早于或与中国同期 | 中国市场先注册，海外后申请 |
| **运营者国籍** | 欧洲店铺由欧洲公司运营 | Amazon.de/.co.uk店铺由中国卖家运营 |

## 🔧 使用方法

### 命令行调用

```bash
# 快速检查（约 30 秒）
python /home/admin/.openclaw/workspace/skills/fake-international-brand-detector/scripts/detect_brand.py --brand "品牌名称" --mode quick

# 深度检查（约 5-10 分钟，更准确）
python /home/admin/.openclaw/workspace/skills/fake-international-brand-detector/scripts/detect_brand.py --brand "品牌名称" --mode deep

# 输出 JSON 格式（便于 API 集成）
python /home/admin/.openclaw/workspace/skills/fake-international-brand-detector/scripts/detect_brand.py --brand "NYO3" --output json
```

### API 调用示例

```python
import requests

response = requests.post(
    "http://localhost:8080/api/detect",
    json={"brand": "Nike", "mode": "quick"},
    headers={"Content-Type": "application/json"}
)
print(response.json())
```

## 📦 输出示例（NYO3 验证结果）

```json
{
  "brand": "NYO3",
  "timestamp": "2026-03-17T16:59:00+08:00",
  "verifications": {
    "official_website": {
      "found": true,
      "url": "https://nyomega.com",
      "age_years": 8.5,
      "languages": ["en", "de"],
      "quality_score": 1.5,
      "issues": [
        "WHOIS registrant_country=CN",
        "邮箱地址@qq.com",
        "仅英文+德语，无挪威语/瑞典语"
      ]
    },
    "sales_channels": {
      "found": true,
      "channels": {
        "physical_stores": 0,
        "online_partners": [
          {"platform": "amazon.de", "seller_location": "CN"},
          {"platform": "amazon.co.uk", "seller_location": "CN"}
        ]
      },
      "quality_score": 2.0,
      "issues": [
        "无Boots UK授权",
        "欧洲店铺由中国卖家运营"
      ]
    },
    "cross_border_sales": {
      "found": true,
      "platforms": ["amazon.com", "amazon.de"],
      "order_count_estimate": ">100",
      "duration_months": 3,
      "quality_score": 1.5,
      "issues": [
        "店铺注册时间晚，销量低"
      ]
    },
    "media_exposure": {
      "found": false,
      "sources_checked": ["Reuters", "Forbes", "WebMD"],
      "articles_found": 0,
      "quality_score": 0.5,
      "issues": [
        "无权威媒体报道，仅有博客软文"
      ]
    },
    "whois_registration_country": {
      "registrant_country": "CN",
      "expected_country": "NO",
      "match": false,
      "email_domain": "@qq.com",
      "quality_score": 0
    },
    "trademark_timeline": {
      "china_registration_date": "201X",
      "norway_registration_date": "20XX（晚于中国）",
      "earlier_market": "China",
      "suspicious_pattern": true,
      "quality_score": 0
    },
    "amazon_seller_location": {
      "amazon_de_seller_country": "CN",
      "amazon_uk_seller_country": "CN",
      "expected_countries": ["DE", "UK"],
      "match": false,
      "quality_score": 0
    }
  },
  "score_summary": {
    "total_items": 7,
    "high_quality_count": 0,
    "valid_count": 2,
    "false_international_flags": [
      "WHOIS显示中国注册",
      "商标时间线：中国市场早于海外",
      "亚马逊欧洲店铺为中国卖家运营"
    ]
  },
  "total_quality_score": 2.0,
  "verdict": "🚩 假国际品牌",
  "confidence": 0.95,
  "recommendation": "建议避免购买或进一步调查，该品牌由中国青岛逢时科技注册和运营"
}
```

## ⚙️ 配置选项

```bash
# 运行模式
--mode quick       # 快速检查（默认，约 30 秒）
--mode deep        # 深度检查（约 5-10 分钟，更准确）

# 输出格式
--output json      # JSON 格式
--output markdown  # Markdown 报告

# API 源配置
--tavily-api-key KEY
--whois-domain tools.domaintools.com
--trademark-office CNIPA:USPTO:EUIPO
```

## 📂 文件结构

```
fake-international-brand-detector/
├── SKILL.md                    # 技能定义文档（此文件）
├── scripts/
│   └── detect_brand.py         # 核心检测脚本（待更新）
├── reference/
│   ├── apis.md                 # API 和搜索引擎列表
│   ├── quality-standards.md    # 内容质量标准说明
│   └── brand-examples.json     # 已知品牌示例数据库（新增：NYO3案例）
└── sample/
    └── test_brands.json        # 测试用例数据
```

## 📚 引用资源

### 🔑 API 配置
```bash
# Tavily Web Search - 已默认配置✅
export TAVILY_API_KEY="your-key-here"

# 可选：其他 API（按需配置）
export GOOGLE_CSE_API_KEY="..."
export GOOGLE_CSE_ID="..."
```

### 海外信息源

- **WHOIS 查询**：whois.domaintools.com / whois命令
- **商标数据库**：
  - CNIPA（中国国家知识产权局）
  - USPTO（美国专利商标局）
  - EUIPO（欧盟知识产权局）
  - WIPO（世界知识产权组织）
- **Wayback Machine**：web.archive.org (官网历史快照) 
- **Google News**：news.google.com (国际新闻搜索)
- **亚马逊全球搜索**：amazon.com/gp/search/
- **NewsAPI**：newsapi.org (新闻媒体聚合)
- **Shopify 商店查询**：shopify.store/ (电商目录)
- **Amazon Seller API（需登录）**：查看店铺运营者位置

### 判定标准文档

详见 `reference/apis.md` 和 `reference/quality-standards.md`

## 🏆 已知品牌示例数据库（NYO3案例）

```json
{
  "brand": "NOW",
  "origin": "United States",
  "founded": 1968,
  "whois_country": "US",
  "amazon_platforms": ["amazon.com", "amazon.co.uk", "amazon.de"],
  "media_coverage": true,
  "verdict": "✅ 真国际品牌"
}

{
  "brand": "Swisse",
  "origin": "Australia",
  "founded": 1987,
  "whois_country": "AU",
  "amazon_platforms": ["amazon.com", "amazon.co.uk", "amazon.de", "amazon.fr"],
  "media_coverage": true,
  "verdict": "✅ 真国际品牌"
}

{
  "brand": "NYO3",
  "origin": "China (青岛逢时科技)",
  "claimed_origin": "Norway（宣称挪威，实为假）",
  "whois_country": "CN",
  "trademark_timeline": {
    "china_first": true,
    "norway_later": true
  },
  "amazon_seller_location": {"de": "CN", "uk": "CN"},
  "media_coverage": false,
  "verdict": "🚩 假国际品牌"
}

{
  "brand": "LOEON",
  "origin": "China",
  "founded": <5年，
  "whois_country": "CN",
  "amazon_platforms": ["amazon.cn"],
  "media_coverage": false,
  "verdict": "🚩 假国际品牌"
}
```

## ⚠️ 注意事项

1. **隐私合规**：只公开查询品牌信息，不抓取用户数据
2. **API 限流**：遵守各平台 robots.txt 和使用条款
3. **误判风险**：小品牌可能因资料少被误判，可指定--mode deep 复测
4. **时效性**：建议每 6 个月重新验证一次结论
5. **中文处理**：对于"国货出海的假国际品牌"（如假 Nike）也能准确识别
6. **NYO3案例学习**：
   - ✅ WHOIS显示中国注册 → 中国品牌
   - ✅ 商标时间线中国市场早于海外 → 先做品牌后出海
   - ✅ Amazon.de/.co.uk店铺为中国卖家 → 无本土运营
   - ✅ 无权威媒体报道 → 仅国内内容/软文
7. **判定逻辑**：
   - 真国际品牌需要≥5项高质量验证（至少3项高分+2项有效）
   - 假国际品牌会触发多项红旗特征（如 WHOIS=CN、商标时间线异常等）

## 🔄 维护日志

| 日期 | 版本 | 更新内容 |
|------|------|------|
| 2026-03-17 | v2.0 | 新增 WHOIS 注册地、商标时间线、卖家国籍三项检查，基于 NYO3 案例优化 |
| 2026-04-16 | v2.1 | 优化大型集团品牌（如 Reckitt/MegaRed）的识别逻辑，增加集团品牌白名单验证，防止因缺乏独立官网而被误判为存疑品牌 |

## 📄 License

MIT License - 自由用于商业和学术研究
