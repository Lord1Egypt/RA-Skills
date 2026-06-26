# 商品搜索API接口文档

## 接口信息

- **HSF服务**：`com.alibaba.global1688.ai.sel.api.hsf.OppSelectionHsfService`
- **方法名**：`productSearchApi`
- **请求类型**：`ProductSearchApiRequest`
- **响应类型**：`ApiResultModel<ProductSearchApiResponse>`

## 请求参数

### ProductSearchApiRequest

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| keyword | String | 是 | 搜索关键词 | "phone", "yoga pants" |
| platform | String | 是 | 目标平台 | "amazon", "tiktok" |
| region | String | 是 | 目标国家/地区代码 | "US", "UK", "JP", "ID" |
| minPrice | Double | 否 | 最低价格（美元） | 10.0 |
| maxPrice | Double | 否 | 最高价格（美元） | 100.0 |
| minSales | Integer | 否 | 最低30天销量 | 100 |
| maxSales | Integer | 否 | 最高30天销量 | 10000 |
| minRating | Double | 否 | 最低评分（0-5.0） | 4.0 |
| maxRating | Double | 否 | 最高评分（0-5.0） | 5.0 |
| listingTime | String | 否 | 上架时间（天） | "90", "180", "365" |
| count | Integer | 否 | 返回商品数量 | 10（默认），最大100 |

### 平台和区域支持

#### Amazon平台
- 美国 (US)
- 英国 (UK)
- 日本 (JP)
- 德国 (DE)
- 法国 (FR)
- 意大利 (IT)
- 西班牙 (ES)
- 加拿大 (CA)

#### TikTok平台
- 印度尼西亚 (ID)
- 泰国 (TH)
- 越南 (VN)
- 马来西亚 (MY)
- 菲律宾 (PH)

## 响应结果

### ApiResultModel<ProductSearchApiResponse>

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
        "images": [
          "https://example.com/image1.jpg",
          "https://example.com/image2.jpg"
        ],
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
          {
            "name": "Color",
            "value": "Pacific Blue"
          },
          {
            "name": "Storage",
            "value": "256GB"
          }
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

### 响应字段说明

#### ProductDetail（商品详情）

**基本信息**
| 字段 | 类型 | 说明 |
|------|------|------|
| itemId | String | 商品ID |
| title | String | 商品标题 |
| category | String | 商品类目 |
| price | Double | 价格 |
| currency | String | 货币单位 |
| moq | Integer | 最小起订量 |
| stock | Integer | 库存数量 |
| rating | Double | 评分（1-5分） |
| salesVolume | Integer | 30天销量 |
| reviewCount | Integer | 评价数量 |
| images | List<String> | 商品图片URL列表 |

**SupplierInfo（供应商信息）**
| 字段 | 类型 | 说明 |
|------|------|------|
| supplierId | String | 供应商ID |
| supplierName | String | 供应商名称 |
| country | String | 所在国家 |
| city | String | 所在城市 |
| yearsOnPlatform | Integer | 平台经营年限 |
| mainProducts | String | 主营产品 |
| responseRate | Double | 响应率（%） |
| responseTime | String | 响应时间描述 |
| deliveryRate | Double | 发货率（%） |

**Specification（规格参数）**
| 字段 | 类型 | 说明 |
|------|------|------|
| name | String | 参数名 |
| value | String | 参数值 |

**LogisticsOption（物流选项）**
| 字段 | 类型 | 说明 |
|------|------|------|
| method | String | 物流方式 |
| estimatedCost | Double | 预估费用（美元） |
| estimatedTime | String | 预估时间 |
| destination | String | 目的地 |

## 错误码

| 错误码 | HTTP状态码 | 说明 | 解决方案 |
|--------|-----------|------|----------|
| SUCCESS | 200 | 成功 | - |
| KEYWORD_EMPTY | 200 | 关键词为空 | 提供有效的搜索关键词 |
| TARGET_PLATFORM_ILLEGAL | 200 | 平台参数非法 | 使用 amazon 或 tiktok |
| TARGET_COUNTRY_ILLEGAL | 200 | 国家代码非法或平台不支持该国家 | 检查平台与国家的匹配关系 |
| PRODUCT_LISTING_TIME_ERROR | 200 | 上架时间参数错误 | 使用 90/180/365 |
| PRODUCT_FILTER_PARAMS_ERROR | 200 | 筛选参数错误（如价格区间、评分超范围） | 检查参数有效性 |
| PRODUCT_RECALL_EMPTY | 200 | 未搜索到符合条件的商品 | 放宽筛选条件或更换关键词 |
| SYSTEM_ERROR | 200 | 系统错误 | 联系技术支持 |

## 调用示例

### 使用curl

```bash
curl -X POST "http://pre-cbucrm.alibaba-inc.com/api/hsf-test/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "interface": "com.alibaba.global1688.ai.sel.api.hsf.OppSelectionHsfService",
    "method": "productSearchApi",
    "paramTypes": [
      "com.alibaba.global1688.ai.sel.api.hsf.request.ProductSearchApiRequest",
      "java.lang.String"
    ],
    "params": [
      {
        "keyword": "phone",
        "platform": "amazon",
        "region": "US",
        "minPrice": 10.0,
        "maxPrice": 100.0,
        "count": 20
      },
      "123456"
    ]
  }'
```

### 使用Python脚本

```bash
python3 scripts/search.py --keyword "phone" --platform amazon --region US \
  --min-price 10 --max-price 100 --count 20
```

### 使用JavaScript（浏览器Console）

```javascript
fetch("http://pre-cbucrm.alibaba-inc.com/api/hsf-test/invoke", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    interface: "com.alibaba.global1688.ai.sel.api.hsf.OppSelectionHsfService",
    method: "productSearchApi",
    paramTypes: [
      "com.alibaba.global1688.ai.sel.api.hsf.request.ProductSearchApiRequest",
      "java.lang.String"
    ],
    params: [
      {
        keyword: "phone",
        platform: "amazon",
        region: "US",
        minPrice: 10.0,
        maxPrice: 100.0,
        count: 20
      },
      "123456"
    ]
  })
})
.then(res => res.json())
.then(data => console.log(JSON.stringify(data, null, 2)));
```

## 业务逻辑说明

### 搜索流程

1. **参数校验**
   - 验证必填参数（keyword, platform, region）
   - 验证平台和区域的匹配关系
   - 验证筛选条件的有效性

2. **关键词处理**
   - 关键词风控检查
   - 关键词标准化和清洗

3. **商品检索**
   - 根据关键词从商品库检索候选商品
   - 应用筛选条件过滤商品
   - 按相关度或指定规则排序

4. **结果组装**
   - 获取商品详细信息
   - 获取供应商信息
   - 获取物流信息
   - 组装完整响应

### 筛选逻辑

- **价格筛选**：基于目标平台的商品价格（已转换为美元）
- **销量筛选**：基于最近30天的销量数据
- **评分筛选**：基于商品的平台评分（0-5.0星）
- **上架时间筛选**：基于商品在目标平台的上架时间
- **多条件AND逻辑**：所有筛选条件同时满足

### 排序规则

默认按以下优先级排序：
1. 相关度（关键词匹配度）
2. 综合得分（销量、评分、评价数综合计算）
3. 上架时间（新品优先）

## 性能指标

- **平均响应时间**：2-5秒
- **超时时间**：30秒
- **单次最大返回**：100个商品
- **并发支持**：支持高并发查询

## 限制和注意事项

1. **关键词限制**
   - 长度：1-100字符
   - 不支持特殊字符：`<>\"'`
   - 敏感词会被风控拦截

2. **筛选条件限制**
   - 价格：0.01-99999.99美元
   - 销量：0-999999
   - 评分：0-5.0
   - 上架时间：只支持90/180/365天

3. **返回数量限制**
   - 单次最多返回100个商品
   - 建议默认使用10-20个

4. **数据实时性**
   - 商品数据：<24小时延迟
   - 销量数据：每日更新
   - 评分数据：每日更新

5. **平台限制**
   - 平台和区域必须匹配
   - 不支持的组合会返回错误

## 依赖服务

- **商品数据库**：OpenSearch / Lindorm
- **关键词风控**：内部风控服务
- **数据同步**：定时任务同步平台数据

## 常见问题

### Q1: 为什么搜索不到商品？
**A**: 可能原因：
- 关键词不匹配商品库中的数据
- 筛选条件过于严格
- 平台/区域不支持该类商品
- 数据同步延迟

**解决方案**：
- 使用更通用的关键词
- 放宽筛选条件
- 确认平台/区域支持
- 稍后重试

### Q2: 为什么返回403错误？
**A**: HSF白名单未配置。

**解决方案**：
在 Diamond 配置中心添加以下配置到 HsfSafeConfig：
```json
{
  "interfaceWhitelist": [
    "com.alibaba.global1688.ai.sel.api.hsf.OppSelectionHsfService"
  ]
}
```

或方法级白名单：
```json
{
  "methodWhitelist": {
    "com.alibaba.global1688.ai.sel.api.hsf.OppSelectionHsfService": [
      "productSearchApi",
      "keywordSearchApi",
      "newProductReportExecuteApi"
    ]
  }
}
```

### Q3: 价格/销量数据准确吗？
**A**: 数据来源于平台公开数据的定时抓取，可能存在以下情况：
- 价格：实时价格可能有变动，建议以平台实际价格为准
- 销量：基于平台展示的销量估算，仅供参考
- 评分：基于平台的评分数据，每日更新

### Q4: 为什么有些筛选条件不生效？
**A**: 可能原因：
- 参数格式错误（如listingTime必须是字符串）
- 参数值超出有效范围
- 参数逻辑冲突（如minPrice > maxPrice）

**解决方案**：
- 检查参数类型和格式
- 参考API文档的参数说明
- 查看错误码和错误消息

## 测试用例

参考测试计划文档：
- 完整测试用例列表和预期结果
- 异常场景和边界场景测试
- 测试报告模板

## 版本历史

### v1.0 (2026-03-17)
- 初始版本
- 支持关键词搜索
- 支持价格、销量、评分、上架时间筛选
- 支持Amazon和TikTok平台
- 支持多国家/地区
