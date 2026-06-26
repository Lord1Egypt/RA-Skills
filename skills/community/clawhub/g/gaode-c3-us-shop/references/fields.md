# POI 详情页关键字段说明

## middleLayerStrategy 结构

```
data
└── middleLayerStrategy
    ├── baseInfo              # 基础信息
    ├── shopSettlement        # 店铺入驻信息 ⭐
    ├── shopBaseInfo          # 商家基础信息
    ├── shopServiceInfo       # 商家服务信息
    ├── user                  # 用户信息
    ├── notices               # 通知
    ├── brandBanner           # 品牌 banner
    ├── operationMaterial     # 运营素材
    ├── contentContainer      # 内容容器
    ├── adResourceDistribute  # 广告资源分发
    └── ruleConfig            # 规则配置
```

## 核心字段详解

### shopSettlement (店铺入驻信息)

| 字段 | 类型 | 说明 | 可能值 |
|------|------|------|--------|
| `shopId` | String | 商家 ID | 如为空表示 POI 未关联商家 |
| `poiId` | String | POI ID | |
| `poiName` | String | POI 名称 | |
| `productCode` | String | 供给标识 | |
| `visitorInfo` | Object | 访问者信息 | 见下表 |
| `settlementRightInfo` | Object | 入驻权益信息 | **关键字段** |
| `rightGuideInfo` | Object | 权益引导信息 | |
| `operationalInfo` | Object | 经营信息 | |
| `aiInfoToMerchant` | Object | AI 模拟用户数据 | |
| `specExt` | Object | 规格扩展信息 | |

### settlementRightInfo (入驻权益信息)

| 字段 | 类型 | 说明 | 可能值 |
|------|------|------|--------|
| `state` | String | **入驻状态** | `付费` / `点亮` / `潜客` / `未入驻` |
| `saleType` | Integer | 可售类型 | `0`: 可售 / `1`: 不可售 |
| `possibleSettlein` | Integer | 是否可点亮 | `1`: 可点亮 / `0`: 不可点亮 |

**判断逻辑**:
```
if state == "付费" → 商家已购买旺铺
if state == "点亮" → 商家已免费点亮
if state == "潜客" → 有销售跟进
if state == "未入驻" → 未入驻商家
```

### visitorInfo (访问者信息)

| 字段 | 类型 | 说明 |
|------|------|------|
| `uid` | String | 用户 ID |
| `state` | String | 访问者状态 |
| `score` | String | 访问者本人店铺评分 |
| `taskState` | Integer | 任务状态 (0 无/1 有) |
| `messageState` | Integer | 消息状态 (0 无/1 有) |
| `saleType` | Integer | 可售类型 |
| `shopId` | String | 用户商铺 ID |

**state 可能值**:
- `owner` - 店铺 owner
- `旺铺` - 已购买旺铺
- `点亮` - 已点亮
- `浅客` - 浅层访客
- `普通用户` - 普通用户

### operationalInfo (经营信息)

| 字段 | 类型 | 说明 |
|------|------|------|
| `currentSettleinNum` | Integer | 今日开通点亮数量 |
| `currentSettleinpayedNum` | Integer | 今日开通旺铺数量 |
| `traffic` | Long | 累积流量 |
| `transactionNum` | Long | 累积交易数 |
| `storeVisits` | Long | 累积到店数量 |
| `remainingValidDays` | Integer | 旺铺剩余有效天数 |
| `expiredDays` | Integer | 旺铺过期天数 |
| `brandProtectState` | String | 品牌保护状态 |
| `bdProtect` | String | 是否 BD 私海 |
| `pendingOrder` | Object | 待处理订单 |
| `goodNews` | Object | 好消息通知 |

## 常见异常场景

### 场景 1: shopSettlement 为空

**现象**: `middleLayerStrategy.shopSettlement = null`

**可能原因**:
1. POI 未关联任何商家
2. 商家已解绑
3. 该 POI 类型不支持入驻（如学校、医院等）

**排查步骤**:
```sql
-- 查询 POI-Shop 绑定关系
SELECT * FROM poi_shop_relation WHERE poi_id = 'B0LR4UPN4M';
```

### 场景 2: settlementRightInfo.state = "未入驻"

**现象**: 入驻状态为未入驻

**可能原因**:
1. 商家确实未入驻
2. 商家入驻但数据未同步
3. 行业限制（某些行业不支持入驻）

**判断逻辑**:
```java
// ShopSettlementDTO.java L347
private String state; // 入驻状态：付费、点亮、潜客、未入驻
```

### 场景 3: possibleSettlein = 0

**现象**: 不可点亮

**可能原因**:
1. 商家资质不满足
2. 行业不支持点亮
3. 已被其他商家点亮
4. POI 质量分过低

### 场景 4: visitorInfo.state != "owner"

**现象**: 访问者状态不是 owner

**影响**:
- 无法看到经营信息
- 无法操作店铺管理功能

**解决**: 使用 owner 账号访问

## 代码位置参考

| 类名 | 文件路径 | 说明 |
|------|----------|------|
| `ShopSettlementDTO` | `us-platform/src/main/java/com/amap/us/platform/node/model/shop/ShopSettlementDTO.java` | 入驻信息 DTO |
| `SettlementRightInfoDTO` | 同上 (内部类) | 入驻权益信息 |
| `VisitorInfoDTO` | 同上 (内部类) | 访问者信息 |
| `OperationalInfoDTO` | 同上 (内部类) | 经营信息 |
| `ShopSettlementService` | 待搜索 | 入驻服务实现 |
| `ShopSettlementManager` | 待搜索 | 入驻管理类 |

## 相关接口

| 接口路径 | 说明 |
|----------|------|
| `/search_business/process/middleLayer/poiDetail` | POI 详情页主接口 |
| `/search_business/process/middleLayer/shopSettlement` | 单独查询入驻信息 |
| `/search_business/process/middleLayer/shopBaseInfo` | 商家基础信息 |

## AB 实验相关

通过 `testid` 参数控制实验分组：

```
testid=76477_138558_183904_...
```

常见实验 ID:
- `76477` - 基础实验
- `185436` - 新版入驻引导
- `186849` - 经营信息展示优化

---

_最后更新：2026-03-31_
