# POI 检索与地理编码

## 通用规则

- **监听先于请求**：先 `setOnGetPoiSearchResultListener` 或 `setOnGetGeoCodeResultListener`，再调用检索方法，否则可能收不到回调。
- 用完后调用 `destroy()` 释放 PoiSearch / GeoCoder 实例。

---

## POI 检索

### 实例与监听

- `PoiSearch mPoiSearch = PoiSearch.newInstance();`
- `OnGetPoiSearchResultListener` 实现：`onGetPoiResult(PoiResult)`、`onGetPoiDetailResult(PoiDetailSearchResult)`、`onGetPoiIndoorResult(PoiIndoorResult)`（按需）。先 `mPoiSearch.setOnGetPoiSearchResultListener(listener)`，再发起检索。

### 城市内检索（关键字）

- `mPoiSearch.searchInCity(new PoiCitySearchOption().city("北京").keyword("美食").pageNum(0));` city 与 keyword 必填。
- PoiCitySearchOption 其它常用：pageNum、pageCapacity、tag、scope（1 或空为基本信息，2 为详情）、cityLimit（是否限制在城市内）、poiFilter、isExtendAdcode、serverType（如 PoiServerType.POI_SERVER_TYPE_ABROAD 海外）。

### POI 结果错误码（result.error）

- PoiResult 有 **result.error** 字段（类型 `SearchResult.ERRORNO`）：
  - `result.error == SearchResult.ERRORNO.NO_ERROR`：成功，用 `result.getAllPoi()`、`result.getPoiResult()` 等。
  - `result.error == SearchResult.ERRORNO.RESULT_NOT_FOUND`：未找到结果。
  - `result.error == SearchResult.ERRORNO.AMBIGUOUS_KEYWORD`：关键字在本市无结果但在其他城市有，可 `result.getSuggestCityList()` 提示用户。

### POI 详情

- 从 PoiResult 取 PoiInfo，用 uid：`mPoiSearch.searchPoiDetail(new PoiDetailSearchOption().poiUids(poi.uid));` 最多 10 个 uid，逗号分隔。结果在 `onGetPoiDetailResult(PoiDetailSearchResult)`。自 V5.2.0 起废弃 onGetPoiDetailResult(PoiDetailResult)，改用 PoiDetailSearchResult。

### 周边检索

- `mPoiSearch.searchNearby(new PoiNearbySearchOption().location(centerLatLng).radius(radius).keyword("餐厅").pageNum(0));` 多关键字用 `$` 分隔，最多 10 个。

### 区域检索（矩形）

- `LatLngBounds searchBounds = new LatLngBounds.Builder().include(sw).include(ne).build();`
- `mPoiSearch.searchInBound(new PoiBoundSearchOption().bound(searchBounds).keyword("餐厅"));`

### 检索结果展示

- 可使用开源 PoiOverlay（overlayutil 包）：`PoiOverlay overlay = new PoiOverlay(mBaiduMap); overlay.setData(poiResult); overlay.addToMap(); overlay.zoomToSpan();`
- 有底部面板时可用 `overlay.zoomToSpanPaddingBounds(padding, padding, padding, bottomPadding)` 使 POI 落在可视区内。

### 注意

- Android 7.5.2+ 支持 adCode；PoiCitySearchOption.isExtendAdcode(true) 时结果含 adCode。

---

## 地理编码（地址 → 坐标）

- `GeoCoder mCoder = GeoCoder.newInstance();`
- `OnGetGeoCoderResultListener` 实现 `onGetGeoCodeResult(GeoCodeResult)` 与 `onGetReverseGeoCodeResult(ReverseGeoCodeResult)`。
- `mCoder.setOnGetGeoCodeResultListener(listener);`
- 发起：`mCoder.geocode(new GeoCodeOption().city("北京").address("北京上地十街10号"));` city 与 address 必填。
- 结果：`geoCodeResult.getLocation()` 得 LatLng，需判 error 是否为 NO_ERROR。

---

## 逆地理编码（坐标 → 地址）

- 同一 GeoCoder 与 listener，在 `onGetReverseGeoCodeResult(ReverseGeoCodeResult)` 中处理。
- 发起：`mCoder.reverseGeoCode(new ReverseGeoCodeOption().location(latLng).newVersion(1).radius(500));` newVersion 0 不返回新版，1 返回；radius 为 POI 召回半径 0–1000 米。
- 结果：`getAddress()`、`getAdcode()`（新版用 getAdcode，与旧版 cityCode 不同）；周边 POI 用 `getPoiList()`。
- V4.5.2+ 通过 ReverseGeoCodeOption.newVersion(1) 获取新版数据。
