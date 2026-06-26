# 检索服务

**边界**：Sug、地理编码、逆地理、POI、公交等检索；路线算路见 [route.md](route.md)。检索类继承 BMKSearchBase，Option + Delegate 模式；使用前须 `[BMKMapManager setAgreePrivacy:YES]`（见 [SKILL.md](../SKILL.md)）。

## 规范

- 每次检索可新建实例，或复用并重设 delegate
- Option 参数按需设置，city 类参数用于过滤/提高精度
- 回调中先判断 `errorCode == BMK_SEARCH_NO_ERROR` 再处理 result

**常用错误码**（BMKSearchErrorCode）：`BMK_SEARCH_NO_ERROR` 成功；`BMK_SEARCH_AMBIGUOUS_KEYWORD` 关键字歧义；`BMK_SEARCH_NOT_SUPPORT_BUS` 不支持公交；`BMK_SEARCH_NOT_SUPPORT_BUS_2CITY` 不支持跨城公交；`BMK_SEARCH_RESULT_NOT_FOUND` 无结果；`BMK_SEARCH_ST_EN_TOO_NEAR` 起终点过近；其他见头文件 BMKSearchBase.h。

## 地点检索（建议检索 Sug）

> 地点检索使用 BMKSuggestionSearch，参考 EmptyApp/LocationSearchViewController。

### 核心类

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKSuggestionSearch | BMKSuggestionSearch.h | 输入联想/地点检索 |
| BMKSuggestionSearchOption | BMKSuggestionSearchOption.h | 检索参数 |
| BMKSuggestionInfo | BMKSuggestionInfo.h | 单条结果 |
| BMKSuggestionSearchResult | BMKSuggestionSearchResult.h | suggestionList |

### BMKSuggestionSearchOption（参数一览）

| 属性 | 类型/说明 |
|------|-----------|
| keyword | 搜索关键字，**必选** |
| cityname | 城市名或 citycode，**必选** |
| cityLimit | BOOL：NO=全国，YES=仅该城市（海外暂不支持） |
| location | CLLocationCoordinate2D，指定位置，可选 |
| filterDistance | 过滤距离（米），与 location 配合 |
| leftBottom / rightTop | 图区范围（CLLocationCoordinate2D），与 filterDistance 二选一 |
| hotword | 是否仅透出热词 |
| inputLanguageType / languageType | 输入/输出语言类型 |
| serverType | 境内/境外（6.6.6+） |

**方法**：`suggestionSearch:`。**回调**：`onGetSuggestionResult:result:errorCode:`，result.suggestionList 为 BMKSuggestionInfo 数组。

### BMKSuggestionInfo 结果字段

| 属性 | 说明 |
|------|------|
| key | 联想词名称 |
| location | 经纬度坐标 |
| uid | 唯一标识 |
| province / city / district / town | 省/市/区/街道 |
| cityID / townCode / adcode | 编码 |
| address | 地址 |
| tag | 分类 |
| children | 子节点（BMKSuggestionChildrenInfo） |

**子节点展示**：BMKSuggestionChildrenInfo 有 `name`、`showName`、`uid`；展示时**优先用 showName（简称）**，无则用 name。示例：`NSString *displayName = (c.showName.length ? c.showName : c.name) ?: @"";`

**子 POI 选点与坐标**：用户点击子 POI（门、停车场等）时，需用**该子点的坐标**而非主 POI 坐标。做法：用**子 POI 的 uid** 直接发起 **POI 详情检索**（`BMKPoiSearch` 的 `poiDetailSearch:`），`BMKPOIDetailSearchOption.poiUIDs = @[ childUid ]`（即 **childUid**，不是主 POI 的 uid）。回调 `onGetPoiDetailResult` 中 `result.poiInfoList.firstObject` 即为该子点，取其 `pt`、`address` 用于选点回调。

### Sug 结果与无经纬度首条

**注意**：Sug 结果的第一条可能存在**没有经纬度**的情况。该条为输入联想出的**关键词/泛指名称**，不对应任何确切 POI 点。例如输入「肯」，第一条可能为「肯德基」——这是泛指，不会带 location 等字段，无法作为地图选点使用。

**实现建议**：**不要过滤**无经纬度的项，应一并展示。用户**点击**无经纬度项时，将其 **key 当作关键词填入检索框并继续发起 Sug 检索**（相当于用户补全输入后再搜），而非当作选点回调；仅当用户点击带有效经纬度的项时，再回调选点（如 onSelectPlace）。

### 推荐用法：Sug + POI 组合

- **输入过程中**：以 **Sug 检索**为入口，边输入边出联想/热词，响应快、体验好。
- **输入结束后**：若 Sug 仍未给出满意结果（列表为空或用户继续输入完整关键词），可再用 **POI 检索**（如 `BMKPOISearch` + `BMKPOICitySearchOption`，以当前关键字为 `keyword`）继续搜索，补足 POI 列表。

组合流程：用户输入 → Sug 防抖请求 → 有结果则展示（无经纬度项点击后当作关键词继续检索）；无结果或用户确认「搜不到」时，再发起 POI 城市检索。

### 地点检索 UI 实现要点

见 [ui-standards.md](ui-standards.md)（防抖、关键字长度、结果展示、检索框与列表对齐、行前 pin 图标）。**隐私检查**：检索前检查 `setAgreePrivacy`，未同意时提示并引导。**选择回调**：`onSelectLocation(BMKSuggestionInfo *)`，取消时传 nil。

**性能优化**：防抖约 0.25s；`becomeFirstResponder` 用 `dispatch_async` 延后至下一 RunLoop，避免与页面转场同时进行导致卡顿；避免在 `viewDidAppear` 中自定义 searchBar 内部结构（如 leftView），易引发布局卡顿。

```objc
// 检索
BMKSuggestionSearch *sug = [[BMKSuggestionSearch alloc] init];
sug.delegate = self;
BMKSuggestionSearchOption *opt = [[BMKSuggestionSearchOption alloc] init];
opt.keyword = keyword;
opt.cityname = @"北京市";
opt.cityLimit = YES;
[sug suggestionSearch:opt];

// 回调
- (void)onGetSuggestionResult:(BMKSuggestionSearch *)searcher result:(BMKSuggestionSearchResult *)result errorCode:(BMKSearchErrorCode)error {
    if (error != BMK_SEARCH_NO_ERROR) { /* 清空列表 */ return; }
    NSArray *list = result.suggestionList ?: @[];
    // 刷新 UITableView
}
```

## 地理编码

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKGeoCodeSearch | BMKGeoCodeSearch.h | 地理编码/逆地理编码 |
| BMKGeoCodeSearchOption | BMKGeoCodeSearchOption.h | address、city |
| BMKReverseGeoCodeSearchOption | BMKReverseGeoCodeSearchOption.h | 逆地理参数 |

**BMKGeoCodeSearchOption**：`address`（必填）、`city`（可选，多城市同名时过滤）。支持「*路与*路交叉口」描述。**方法**：`geoCode:`. **回调**：`onGetGeoCodeResult:result:errorCode:`，result 含 location、level、precise 等。

**BMKReverseGeoCodeSearchOption（逆地理参数一览）**：

| 属性 | 说明 |
|------|------|
| location | CLLocationCoordinate2D，**必填** |
| isLatestAdmin | 是否返回最新行政区划，建议 YES |
| pageNum / pageSize | POI 列表分页 |
| radius | 召回半径（米） |
| languageType | 输出语言 |
| extensionsRoad | 是否扩展道路信息 |
| entirePoi | 是否返回全量 POI |
| sortStrategy | 排序策略 |
| tags | 过滤标签 |

**逆地理（地图选点）**：设置 `location`（如 mapView.centerCoordinate）、`isLatestAdmin = YES`。**回调**：`onGetReverseGeoCodeResult:result:errorCode:`。`BMKReverseGeoCodeSearchResult` 含 `address`、`sematicDescription`、`poiList`（BMKPoiInfo）、`poiRegions`、addressComponent 等。选点场景：regionDidChange 时对中心点做逆地理，第一行展示 address，后续行展示 poiList；选中 POI 可 `setCenterCoordinate:animated:`。

## POI 检索

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKPOISearch | BMKPOISearch.h | POI 检索，delegate 接收结果 |
| BMKPOICitySearchOption | BMKPoiSearchOption.h | 城市内检索 |
| BMKPOINearbySearchOption | BMKPoiSearchOption.h | 周边检索 |
| BMKPOIBoundSearchOption | BMKPoiSearchOption.h | 矩形范围内检索 |
| BMKPOIDetailSearchOption | BMKPoiSearchOption.h | POI 详情（按 UID） |
| BMKPOIIndoorSearchOption | BMKPoiSearchOption.h | 室内 POI |

**BMKPOICitySearchOption**：keyword、city（必填）、pageIndex、pageSize、scope、tags、type、filter、filterDistance、location、leftBottom/rightTop、isCityLimit、isBoundLimit、addressResult、homonym、extensionsChildPoi、extensionsAdcode、inputLanguageType、languageType、serverType、isLightVersion、showPhotos。

**BMKPOINearbySearchOption**：keywords（数组）、location、radius、pageIndex、pageSize、scope、tags、type、filter、isRadiusLimit、addressResult、homonym、extensionsChildPoi、extensionsAdcode、inputLanguageType、languageType、serverType、isLightVersion、showPhotos。

**BMKPOIBoundSearchOption**：keywords、leftBottom、rightTop、pageIndex、pageSize、scope、tags、type、filter、addressResult、homonym、extensionsChildPoi、extensionsAdcode、inputLanguageType、languageType、serverType、isLightVersion、showPhotos。

**BMKPOIDetailSearchOption**：poiUIDs（POI 唯一标识数组，必填）、scope、languageType、extensionsAdcode、serverType、showPhotos。**子 POI**：可直接传入**子 POI 的 uid**（如 Sug 结果中 BMKSuggestionChildrenInfo.uid），接口会返回该子点的详情（pt、address 等），无需传主 POI uid 再在 detailInfo.children 中匹配。

**POI 详情/列表返回图片（photos）**：接口默认不返回图片；需同时满足：(1) **scope = BMK_POI_SCOPE_DETAIL_INFORMATION**；(2) **showPhotos = YES**。POI 图片为高级字段，AK 需在控制台申请对应权限，否则仍可能无图。城市/周边/详情检索的 Option 均有 showPhotos，仅当 scope 为详情时生效。

```objc
BMKPOIDetailSearchOption *opt = [BMKPOIDetailSearchOption new];
opt.poiUIDs = @[poiUid];
opt.scope = BMK_POI_SCOPE_DETAIL_INFORMATION;
opt.showPhotos = YES;
[self.poiSearch poiDetailSearch:opt];
```

**BMKPOIIndoorSearchOption**：indoorID、keyword、floor、pageIndex、pageSize。

**方法**：`poiSearchInCity:`、`poiSearchNearBy:`、`poiSearchInbounds:`、`poiDetailSearch:`、`poiIndoorSearch:`。**回调**：`onGetPoiResult:result:errorCode:type:`（城市/周边/矩形）、`onGetPoiDetailResult:result:errorCode:`、`onGetPoiIndoorResult:result:errorCode:`。结果中 poiInfoList / poiIndoorInfoList 为 BMKPoiInfo 数组；详情为 BMKPOIDetailSearchResult，含 BMKPOIDetailInfo（含 name、address、location、photos、openingHours、price、overallRating 等）。

## 公交

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKBusLineSearch | BMKBusLineSearch.h | 公交线路详情（按线路 UID） |

**BMKBusLineSearchOption**：线路 UID（从 POI 或路线结果获取）、city、languageType、pageIndex、pageSize 等。**方法**：按 UID 查询线路站点与走向。**回调**：`onGetBusDetailResult:result:errorCode:`。与路线规划中的「公交路线」为不同能力：此处查单条线路详情，路线规划用 BMKRouteSearch 的 transitSearch / busRoutePlanSearch。

## 其他检索

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKDistrictSearch | BMKDistrictSearch.h | 行政区域（省市区边界等） |
| BMKAOISearch | BMKAOISearch.h | AOI 检索（面状区域） |
| BMKBuildingSearch | BMKBuildingSearch.h | 建筑物检索（高级） |
| BMKGeoCodeBatchSearch / 逆地理批量 | 见 SDK 头文件 | 批量地理编码/逆地理（若有需求） |

---

## 按需方案

| 需求 | 推荐检索 | 说明 |
|------|----------|------|
| 起终点/地点选点 | BMKSuggestionSearch | keyword+city，返回 location、key、address，见 LocationSearchViewController |
| 地图拖拽选点 | BMKPointAnnotation/BMKIconMarker + BMKGeoCodeSearch | 固定屏幕标注 + 逆地理。标注见 [annotations.md](annotations.md)，regionDidChange 时 reverseGeoCode。布局见 [ui-standards.md](ui-standards.md) |
| 地址→坐标 | BMKGeoCodeSearch | address+city，结构化地址精度更高 |
| 坐标→地址 | BMKReverseGeoCodeSearch | 逆地理 |
| 城市内 POI | BMKPOISearch + BMKPOICitySearchOption | 关键字+城市 |
| 公交线路详情 | BMKBusLineSearch | 需线路 UID |
