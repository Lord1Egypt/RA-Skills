# POI 详情页模块 - sourceId 映射表

> 从代码库 `gaode.search/us-business-service` 的 `ShopNodeNameEnum` 枚举类提取

**文件路径**: `us-platform/src/main/java/com/amap/us/platform/enums/ShopNodeNameEnum.java`  
**总计**: 58 个 sourceId  
**最后更新**: 2026-03-31

---

## 使用说明

在查询日志和复现请求时，使用 `sourceId` 可以精准定位目标模块数据。

**查询模板**:
```bash
# 日志查询
LOG_QUERY="<gsid> AND pageIndex=2 AND \"<sourceId>\" AND /search_business/process/middleLayer/poiDetail"

# 响应路径
data.<sourceId>
```

---

## 完整映射表

### 🏪 基础模块 (4)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 店铺商业化分发 | `shopDistribute` | `data.shopDistribute` |
| 店铺基础信息 | `shopBaseInfo` | `data.shopBaseInfo` |
| 房产行业数据 | `shopBaseData` | `data.shopBaseData` |
| 店铺复合信息 | `shopInfo` | `data.shopInfo` |

### 📦 聚合模块 (2)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 店铺装修聚合 Node | `shopDecorationAggregated` | `data.shopDecorationAggregated` |
| 店铺装修详情聚合 Node | `shopDecorationDetailAggregated` | `data.shopDecorationDetailAggregated` |

### 📋 列表模块 (5)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 商家新鲜事 | `shopFreshNews` | `data.shopFreshNews` |
| 店铺动态 | `shopNews` | `data.shopNews` |
| 商家相册 | `media` | `data.media` |
| 商家相册 (别名) | `shopMedia` | `data.shopMedia` |
| 店铺通知 | `notices` | `data.notices` |

### 🎁 营销模块 (3)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 预约礼 | `gifts` | `data.gifts` |
| 商家留资活动 | `discountActivity` | `data.discountActivity` |
| 聚合 Banner | `shopMergeBanner` | `data.shopMergeBanner` |

### 👤 内容模块 (6)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| **人物列表** | `contentPerson` | `data.contentPerson.data.personInfos` |
| 人物信息 | `persons` | `data.persons` |
| **案例列表** | `contentCaseBook` | `data.contentCaseBook` |
| 案例集 | `caseBooks` | `data.caseBooks` |
| 案例详情 | `caseInfo` | `data.caseInfo` |
| 人物详情 | `personInfo` | `data.personInfo` |

### 🛍️ 功能模块 (11)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 新品橱窗 | `freshGoodsWindow` | `data.freshGoodsWindow` |
| 品牌故事 | `brandStory` | `data.brandStory` |
| 品牌信息 | `brandInfo` | `data.brandInfo` |
| 课程 | `shopCourse` | `data.shopCourse` |
| 产品服务/店内服务 | `shopProductService` | `data.shopProductService` |
| 商铺活动 | `shopBaseActivity` | `data.shopBaseActivity` |
| 店铺活动 | `shopActivity` | `data.shopActivity` |
| 装修内容活动 | `shopDecorationContentActivity` | `data.shopDecorationContentActivity` |
| 店铺位置引导 | `shopLocGuide` | `data.shopLocGuide` |
| 特色服务列表 | `shopBrandServices` | `data.shopBrandServices` |
| 结构化货架 | `structShelf` | `data.structShelf` |

### 📞 通讯模块 (5)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 电话信息 | `telInfo` | `data.telInfo` |
| IM 信息 | `shopIm` | `data.shopIm` |
| IM 信息 (别名) | `imInfo` | `data.imInfo` |
| 店铺问题库 | `shopQuestions` | `data.shopQuestions` |
| 问题库 | `questions` | `data.questions` |

### 🏷️ 入驻模块 (1)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 好人卡 (入驻信息) | `shopSettlement` | `data.shopSettlement` |

### 🤖 AI 模块 (2)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| AI 客服服务 | `shopAiCustomer` | `data.shopAiCustomer` |
| Agent 首次响应策略 | `agentFirstResponsePolicy` | `data.agentFirstResponsePolicy` |

### 📊 价目表模块 (4)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 价目表列表 | `quotationList` | `data.quotationList` |
| 价目表 | `quotationTable` | `data.quotationTable` |
| 价目表项详情 | `quotationTableItem` | `data.quotationTableItem` |
| 价目表详情 | `quotationDetail` | `data.quotationDetail` |

### 🍽️ 菜品模块 (2)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 推荐菜 | `shopMenu` | `data.shopMenu` |
| 推荐菜项详情 | `shopMenuItem` | `data.shopMenuItem` |

### 🏢 其他模块 (13)

| 描述 | sourceId | 响应路径 |
|------|----------|----------|
| 店铺小程序 | `shopMiniApps` | `data.shopMiniApps` |
| 店铺服务信息 | `shopServiceInfo` | `data.shopServiceInfo` |
| 联系方式配置 | `contact` | `data.contact` |
| IM 发送项 | `imSendItems` | `data.imSendItems` |
| 城市限行通知 | `cityRestrictionNotice` | `data.cityRestrictionNotice` |
| 店铺腰封 | `brandBanner` | `data.brandBanner` |
| 品牌服务项详情 | `brandServiceItem` | `data.brandServiceItem` |
| 商场事件 | `shoppingMallEvent` | `data.shoppingMallEvent` |
| 商场事件扩展 | `shoppingMallEventExt` | `data.shoppingMallEventExt` |
| 服务门店 | `serviceShop` | `data.serviceShop` |
| 业务线 | `businessLine` | `data.businessLine` |
| 商家私域渠道 | `privateSphereChannel` | `data.privateSphereChannel` |
| KA 店铺服务 | `kaShopService` | `data.kaShopService` |

---

## 常用模块快速查询

### 🎯 手艺人模块排查

```bash
# sourceId: contentPerson
# 响应路径：data.contentPerson.data.personInfos

# 日志查询
LOG_QUERY="<gsid> AND pageIndex=2 AND \"contentPerson\" AND /poiDetail"

# 字段说明
- personId: 手艺人 ID
- basicInfo.name: 姓名
- basicInfo.photo: 头像
- certifications: 认证信息
- introduction: 简介
```

### 🏪 店铺入驻排查

```bash
# sourceId: shopSettlement
# 响应路径：data.shopSettlement

# 日志查询
LOG_QUERY="<gsid> AND \"shopSettlement\" AND /poiDetail"

# 字段说明
- shopId: 商家 ID
- settlementRightInfo.state: 入驻状态 (付费/点亮/潜客/未入驻)
- operationalInfo: 经营信息
```

### 📞 IM 模块排查

```bash
# sourceId: shopIm
# 响应路径：data.shopIm

# 日志查询
LOG_QUERY="<gsid> AND \"shopIm\" AND /poiDetail"
```

### 🤖 AI 客服排查

```bash
# sourceId: shopAiCustomer
# 响应路径：data.shopAiCustomer

# 日志查询
LOG_QUERY="<gsid> AND \"shopAiCustomer\" AND /poiDetail"
```

---

## 日志查询模板

### 基础模板

```bash
aone-kit call-tool loghouse-mcp::query_log '{
  "app_name": "lse2-us-business-service",
  "log_name": "nginx_uni",
  "query": "<GSID> AND pageIndex=<PAGE_INDEX> AND \"<SOURCE_ID>\" AND /search_business/process/middleLayer/poiDetail",
  "start_time": "1h ago",
  "end_time": "now",
  "size": 10,
  "reverse": true,
  "emp_id": "501280"
}'
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `GSID` | 用户会话 ID | `09011095227079177495792911000044285436331` |
| `PAGE_INDEX` | 分页索引 (默认 2) | `2` |
| `SOURCE_ID` | 模块 sourceId | `contentPerson` |
| `timeRange` | 时间范围 | `1h ago`, `30m ago`, `4h ago` |

---

## 枚举类信息

**类名**: `com.amap.us.platform.enums.ShopNodeNameEnum`  
**文件路径**: `us-platform/src/main/java/com/amap/us/platform/enums/ShopNodeNameEnum.java`  
**用途**: 统一管理 Node 别名，避免硬编码  
**枚举数量**: 58 个

---

_数据来源：代码库 `gaode.search/us-business-service` master 分支_  
_提取时间：2026-03-31_
