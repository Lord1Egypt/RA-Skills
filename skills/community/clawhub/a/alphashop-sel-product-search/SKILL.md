---
name: alphashop-sel-product-search
category: official-1688
description: >-
  商品搜索API SKILL：通过关键词搜索发现Amazon/TikTok平台商品。
  支持价格、销量、评分、上架时间等多维度筛选条件。
  通过 AlphaShop REST API 调用遨虾AI选品系统的商品搜索服务。
metadata:
  version: 1.0.1
  label: AI商品搜索
  author: 1688官方技术团队
  openclaw:
    primaryEnv: none
    requires:
      env: []
---

## 配置

### 环境变量

需要配置 AlphaShop API 凭证。在 OpenClaw config 中设置：

```json5
{
  skills: {
    entries: {
      "alphashop-sel-newproduct": {
        env: {
          ALPHASHOP_ACCESS_KEY: "你的AccessKey",
          ALPHASHOP_SECRET_KEY: "你的SecretKey"
        }
      }
    }
  }
}
```

### 如何获取 API Key

#### 获取途径

本 skill 使用 AlphaShop/遨虾平台的 API 服务，需要申请以下凭证：
- `ALPHASHOP_ACCESS_KEY` - API 访问密钥
- `ALPHASHOP_SECRET_KEY` - API 密钥

#### 申请步骤

1. **联系平台方**
   - 如果您是 1688 或阿里内部用户，请联系 AlphaShop/遨虾 平台管理员
   - 平台可能需要您提供：
     - 公司信息
     - 使用场景说明
     - 预期调用量

2. **获取凭证**
   - 平台审核通过后会提供：
     - Access Key（访问密钥）
     - Secret Key（密钥）

3. **配置到环境**
   - 按照上面的配置方式设置环境变量

#### 缺少凭证时的提示

如果运行 skill 时未配置凭证，会看到详细的配置指南：

```
🔐 需要 AlphaShop API 凭证

本 skill 需要以下凭证才能使用：
  • ALPHASHOP_ACCESS_KEY  - API 访问密钥
  • ALPHASHOP_SECRET_KEY  - API 密钥

📋 如何获取凭证：
1. 联系 AlphaShop/遨虾 平台获取 API 凭证
2. 配置环境变量或 OpenClaw 配置
3. 重新运行命令
```


# 商品搜索API SKILL

通过 AlphaShop REST API 调用1688遨虾AI选品系统的商品搜索服务，支持**关键词搜索**，覆盖Amazon和TikTok平台。


**CRITICAL: 参数收集策略**

当用户请求搜索但未提供必需参数（`platform` 和 `region`）时，**必须**使用 `AskUserQuestion` 工具引导用户选择。**禁止使用任何默认值**。

### 必需参数检查

**关键词搜索** (`scripts/search.py`)：
- `--keyword`: 必填（从用户输入提取）
- `--platform`: 必填 ⚠️ **如果缺失→询问用户**
- `--region`: 必填 ⚠️ **如果缺失→询问用户**

### 参数询问流程

**Step 1: 询问平台**（如果用户未指定 `platform`）

使用 `AskUserQuestion` 提供选项：
- **Amazon** - 描述：覆盖美国、英国、日本、德国、法国、意大利、西班牙、加拿大8个市场
- **TikTok** - 描述：覆盖西班牙、菲律宾、法国、印尼、墨西哥、越南、德国、日本、泰国、新加坡、巴西、意大利、美国、英国、马来西亚15个市场

**Step 2: 询问区域**（如果用户未指定 `region`）

根据选择的平台，使用 `AskUserQuestion` 提供对应区域选项：

**Amazon 区域**：
- US - 美国
- UK - 英国
- JP - 日本
- DE - 德国
- FR - 法国
- IT - 意大利
- ES - 西班牙
- CA - 加拿大

**TikTok 区域**：
- ES - 西班牙
- PH - 菲律宾
- FR - 法国
- ID - 印尼
- MX - 墨西哥
- VN - 越南
- DE - 德国
- JP - 日本
- TH - 泰国
- SG - 新加坡
- BR - 巴西
- IT - 意大利
- US - 美国
- GB - 英国
- MY - 马来西亚

**Step 3: 执行搜索**

收集完所有必需参数后，构建完整命令执行。

### 执行示例

#### ❌ 错误示例
```
用户: "搜索 yoga pants"
Claude: 直接执行 python3 scripts/search.py --keyword "yoga pants" --platform amazon --region US
问题: 未询问用户，擅自使用默认值
```

#### ✅ 正确示例
```
用户: "搜索 yoga pants"
Claude: 使用 AskUserQuestion 询问平台 (Amazon/TikTok)
用户: 选择 Amazon
Claude: 使用 AskUserQuestion 询问区域 (US/UK/JP...)
用户: 选择 US
Claude: 执行 python3 scripts/search.py --keyword "yoga pants" --platform amazon --region US
```

#### ✅ 部分参数已提供
```
用户: "在 Amazon 搜索 phone"
Claude: 识别到 platform=amazon，使用 AskUserQuestion 询问区域
用户: 选择 JP
Claude: 执行 python3 scripts/search.py --keyword "phone" --platform amazon --region JP
```

#### ✅ 所有参数齐全
```
用户: "在 Amazon 美国市场搜索 phone"
Claude: 识别到所有必需参数，直接执行搜索
Claude: python3 scripts/search.py --keyword "phone" --platform amazon --region US
```

---

## 功能说明

### 核心功能

#### 关键词搜索 (`scripts/search.py`)
- **关键词搜索**：根据关键词搜索目标平台的商品
- **多维度筛选**：支持价格、销量、评分、上架时间等筛选条件
- **多平台支持**：Amazon（美国、英国、日本等）、TikTok（印尼、泰国等）
- **丰富商品信息**：返回商品详情、供应商信息、规格参数、物流选项等

### 支持的平台和区域

**Amazon平台**：
- 美国 (US)
- 英国 (UK)
- 日本 (JP)
- 德国 (DE)
- 法国 (FR)
- 意大利 (IT)
- 西班牙 (ES)
- 加拿大 (CA)

**TikTok平台**：
- 西班牙 (ES)
- 菲律宾 (PH)
- 法国 (FR)
- 印度尼西亚 (ID)
- 墨西哥 (MX)
- 越南 (VN)
- 德国 (DE)
- 日本 (JP)
- 泰国 (TH)
- 新加坡 (SG)
- 巴西 (BR)
- 意大利 (IT)
- 美国 (US)
- 英国 (GB)
- 马来西亚 (MY)

## 使用方法

### 基础搜索

```bash
# 搜索Amazon美国市场的手机
python3 scripts/search.py --keyword "phone" --platform amazon --region US

# 搜索TikTok印尼市场的瑜伽裤
python3 scripts/search.py --keyword "yoga pants" --platform tiktok --region ID
```

### 价格筛选

```bash
# 搜索价格在10-100美元的商品
python3 scripts/search.py --keyword "phone" --platform amazon --region US --min-price 10 --max-price 100
```

### 销量筛选

```bash
# 搜索月销量在100-10000的商品
python3 scripts/search.py --keyword "phone" --platform amazon --region US --min-sales 100 --max-sales 10000
```

### 评分筛选

```bash
# 搜索评分4.0-5.0的高评分商品
python3 scripts/search.py --keyword "phone" --platform amazon --region US --min-rating 4.0 --max-rating 5.0
```

### 上架时间筛选

```bash
# 搜索90天内上架的新品
python3 scripts/search.py --keyword "phone" --platform amazon --region US --listing-time 90

# listing-time 支持：90, 180, 365
```

### 综合筛选

```bash
# 组合多个筛选条件
python3 scripts/search.py \
  --keyword "phone" \
  --platform amazon \
  --region US \
  --min-price 10 \
  --max-price 100 \
  --min-sales 100 \
  --min-rating 4.0 \
  --listing-time 90 \
  --count 20
```

### 指定返回数量

```bash
# 返回最多50个商品（默认10个）
python3 scripts/search.py --keyword "phone" --platform amazon --region US --count 50
```

## 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--keyword` | 是 | 搜索关键词 | "phone", "yoga pants" |
| `--platform` | 是 | 目标平台 | amazon, tiktok |
| `--region` | 是 | 目标国家/地区代码 | US, UK, JP, ID, TH, ES, PH, FR, MX, VN, DE, SG, BR, IT, GB, MY |
| `--min-price` | 否 | 最低价格（美元） | 10.0 |
| `--max-price` | 否 | 最高价格（美元） | 100.0 |
| `--min-sales` | 否 | 最低30天销量 | 100 |
| `--max-sales` | 否 | 最高30天销量 | 10000 |
| `--min-rating` | 否 | 最低评分（0-5.0） | 4.0 |
| `--max-rating` | 否 | 最高评分（0-5.0） | 5.0 |
| `--listing-time` | 否 | 上架时间（天）| 90, 180, 365 |
| `--count` | 否 | 返回商品数量（默认10） | 20 |
| `--user-id` | 否 | 用户ID（默认"123456"） | "your_user_id" |

## 返回数据结构

### 成功响应

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "成功",
  "data": {
    "totalCount": 50,
    "productList": [
      {
        "itemId": "B08N5WRWNW",
        "title": "Apple iPhone 12 Pro Max",
        "category": "Cell Phones",
        "price": 899.99,
        "currency": "USD",
        "moq": 1,
        "stock": 500,
        "rating": 4.8,
        "salesVolume": 5000,
        "reviewCount": 1234,
        "images": ["https://..."],
        "supplier": {
          "supplierId": "AXXXXX",
          "supplierName": "Apple Store",
          "country": "US",
          "city": "Cupertino",
          "yearsOnPlatform": 10,
          "mainProducts": "Electronics",
          "responseRate": 98.5,
          "responseTime": "within 2 hours",
          "deliveryRate": 99.0
        },
        "specifications": [
          {"name": "Color", "value": "Pacific Blue"},
          {"name": "Storage", "value": "256GB"}
        ],
        "logisticsOptions": [
          {
            "method": "Standard Shipping",
            "estimatedCost": 5.99,
            "estimatedTime": "3-5 business days",
            "destination": "US"
          }
        ],
        "advantages": [
          "Fast shipping",
          "High quality",
          "Verified supplier"
        ]
      }
    ]
  }
}
```

### 错误响应

```json
{
  "success": false,
  "code": "KEYWORD_EMPTY",
  "message": "搜索关键词不能为空",
  "data": null
}
```

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `KEYWORD_EMPTY` | 关键词为空 | 提供有效的搜索关键词 |
| `TARGET_PLATFORM_ILLEGAL` | 平台参数非法 | 使用 amazon 或 tiktok |
| `TARGET_COUNTRY_ILLEGAL` | 国家代码非法或平台不支持 | 检查平台与国家的匹配关系 |
| `PRODUCT_LISTING_TIME_ERROR` | 上架时间参数错误 | 使用 90/180/365 |
| `PRODUCT_FILTER_PARAMS_ERROR` | 筛选参数错误 | 检查价格/销量/评分区间 |
| `PRODUCT_RECALL_EMPTY` | 未搜索到符合条件的商品 | 放宽筛选条件 |

## 接口信息

### 商品搜索 API

- **接口地址**：`POST https://api.alphashop.cn/ai.sel.global1688.productSearchApi/1.0`
- **环境**：生产环境（Production）
- **认证方式**：JWT Token (HS256)
- **请求格式**：JSON
- **响应格式**：JSON
- **超时时间**：建议 30-60 秒

### 认证配置

需要配置 AlphaShop API 凭证：

**环境变量：**
```bash
export ALPHASHOP_ACCESS_KEY='your-access-key'
export ALPHASHOP_SECRET_KEY='your-secret-key'
```

**OpenClaw 配置：**
```json
{
  "skills": {
    "entries": {
      "alphashop-sel-product-search": {
        "env": {
          "ALPHASHOP_ACCESS_KEY": "your-access-key",
          "ALPHASHOP_SECRET_KEY": "your-secret-key"
        }
      }
    }
  }
}
```

**凭证获取途径**：https://www.alphashop.cn/seller-center/apikey-management

## 注意事项

1. **关键词风控**：某些敏感关键词可能被风控系统拦截
2. **数据实时性**：商品信息可能存在延迟（通常<24小时）
3. **筛选条件**：过于严格的筛选可能导致无结果
4. **性能考虑**：复杂查询可能耗时较长（通常<5秒）
5. **平台限制**：确保平台和国家组合在支持列表中
6. **评分范围**：评分必须在 0-5.0 之间
7. **价格单位**：所有价格以美元计价

## 使用场景

### 1. 市场调研
找出目标市场的热门商品和价格区间

```bash
python3 scripts/search.py --keyword "yoga mat" --platform amazon --region US --count 50
```

### 2. 选品分析
筛选高评分、高销量的优质商品

```bash
python3 scripts/search.py --keyword "fitness equipment" --platform amazon --region US \
  --min-rating 4.5 --min-sales 500 --count 30
```

### 3. 新品发现
寻找90天内上架的新品

```bash
python3 scripts/search.py --keyword "smart watch" --platform amazon --region US \
  --listing-time 90 --count 20
```

### 4. 价格竞争分析
分析特定价格区间的商品分布

```bash
python3 scripts/search.py --keyword "headphone" --platform amazon --region US \
  --min-price 20 --max-price 50 --count 40
```

## 技术支持

- **问题反馈**：提交 Issue 到 global-skill 仓库
- **文档更新**：参考 `references/api.md`
- **测试计划**：参考项目中的测试用例

## 版本历史

- **v1.0** (2026-03-17)
  - 初始版本
  - 支持基础关键词搜索
  - 支持多维度筛选（价格、销量、评分、上架时间）
  - 支持 Amazon 和 TikTok 平台
