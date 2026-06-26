# 百度 iOS 定位 SDK（BMKLocationKit）

**边界**：单次/连续/后台/室内定位、地理围栏、鉴权；与地图独立，可单独或与 BaiduMapKit 配合。与地图混用须统一坐标系，见 [utils.md](utils.md)。不含步骑行导航内部定位。

## CocoaPods 集成

Pod 库名：**BMKLocationKit**。在 Podfile 同目录执行 `pod install`，使用生成的 `.xcworkspace` 打开工程。

```ruby
platform :ios, '9.0'
target 'YourProjectTarget' do  # 替换为工程名
  pod 'BMKLocationKit', '2.1.3'
end
```

常用命令：`pod install`、`pod repo update`、`pod update`。若 `pod search` 找不到类库：`pod setup` → 删除 `~/Library/Caches/CocoaPods/search_index.json` → 再执行 `pod search BMKLocationKit`。

## 隐私与初始化（必须遵守）

**必须通过 BMKLocationAuth 的 setAgreePrivacy 在用户同意隐私政策后再进行定位 SDK 的初始化。**

- 首次使用前弹窗让用户阅读并同意隐私政策（隐私政策地址可跳转：https://lbsyun.baidu.com/index.php?title=openprivacy）。
- 用户同意后调用 `[[BMKLocationAuth sharedInstance] setAgreePrivacy:YES]`，**再**初始化定位相关逻辑（如 BMKLocationManager 等）。
- 用户不同意时调用 `setAgreePrivacy:NO`，且不要初始化定位 SDK。
- 与地图 SDK 区分：地图使用 `[BMKMapManager setAgreePrivacy:YES]`；定位使用 **BMKLocationAuth** 的 setAgreePrivacy。

## 鉴权失败排查（无法返回定位/地址时）

若出现 **「鉴权失败导致无法返回定位、地址等信息」**（或错误码 BMKLocationErrorFailureAuth），按下列顺序检查：

| 排查项 | 说明 |
|--------|------|
| **1. setAgreePrivacy 顺序** | 必须在 **BMKLocationManager、BMKGeoFenceManager 等实例化之前** 调用 `[[BMKLocationAuth sharedInstance] setAgreePrivacy:YES]`。顺序：先 setAgreePrivacy(YES) → 再创建/初始化 BMKLocationManager → 再发起定位。若先初始化再设隐私，会导致鉴权失败。 |
| **2. AK（密钥）配置** | 在百度 LBS 控制台申请 **iOS 应用** 的 AK，且 **Bundle Identifier** 必须与当前应用一致。在任意定位 SDK 类初始化前完成 AK 校验/配置（如 BMKLocationAuth 的 checkPermisionWithKey: 等）。多应用需分别申请 AK。 |
| **3. 网络与权限** | 确认设备网络正常；确认已向用户申请并授予定位权限（Info.plist 配置 NSLocationWhenInUseUsageDescription 等）。 |

## 坐标系（与地图 SDK 一致）

**地图 SDK 全局使用 BD09**。**定位 SDK** 通过 **coordinateType**（类型 BMKLocationCoordinateType）设定定位坐标系，**默认为 BMKLocationCoordinateTypeGCJ02**。将定位结果用于地图展示、标注、路线或与地图 API 混用时，必须统一为 BD09：将 **coordinateType 设为 BMKLocationCoordinateTypeBMK09LL**，或使用地图 [utils.md](utils.md) 的 `BMKCoordTrans:fromType:toType:` 将 GCJ02 转为 BD09 后再传给地图。否则会出现偏移或错误。

## 核心类与接口（含默认值，避免与预期不一致）

### BMKLocationAuth

头文件：BMKLocationAuth.h。**初始化 BMKLocationManager 之前必须设置 BMKLocationAuth 中的 APIKey，否则无法正常使用服务。**

| 接口/属性 | 说明 |
|-----------|------|
| `sharedInstance` | 单例 |
| `setAgreePrivacy:` | 设置用户是否同意隐私政策，须在 BMKLocationManager/BMKGeoFenceManager 实例化前调用 |
| `checkPermisionWithKey:...` | AK 校验，须在任意定位 SDK 类使用前调用 |

---

### BMKLocationManager（类参考，含属性默认值）

头文件：BMKLocationManager.h。使用前须在 BMKLocationAuth 中设置 APIKey 并 setAgreePrivacy:YES。

#### 属性（含默认值）

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| delegate | id\<BMKLocationManagerDelegate\> | — | 连续定位/错误回调等 |
| distanceFilter | CLLocationDistance | **kCLDistanceFilterNone** | 定位最小更新距离 |
| headingFilter | CLLocationDegrees | **1**（since 2.0.5） | 设备朝向最小更新角度 |
| desiredAccuracy | CLLocationAccuracy | **kCLLocationAccuracyBest** | 定位精度 |
| activityType | CLActivityType | **CLActivityTypeAutomotiveNavigation** | 定位类型 |
| showsBackgroundLocationIndicator | BOOL | **NO**（iOS11+） | 后台定位时状态栏是否显示指示器；“始终授权”下设置有效 |
| coordinateType | BMKLocationCoordinateType | **BMKLocationCoordinateTypeGCJ02** | 定位坐标系类型。与地图混用须设为 BMKLocationCoordinateTypeBMK09LL |
| pausesLocationUpdatesAutomatically | BOOL | **NO** | 定位是否被系统自动暂停 |
| allowsBackgroundLocationUpdates | BOOL | **NO**（iOS9+） | 是否允许后台定位；设为 YES 时须开启 Background Modes → Location updates，且在定位未开始或已停止时修改才生效 |
| locationTimeout | NSInteger | **10**（秒） | 单次定位超时时间，最小 2s；在单次定位请求前设置；从定位权限非 NotDetermined 后开始计时 |
| reGeocodeTimeout | NSInteger | **10**（秒） | 单次逆地理超时时间，最小 2s；单次定位请求前设置 |
| locatingWithReGeocode | BOOL | **YES** | 连续定位是否返回逆地理信息 |
| isNeedNewVersionReGeocode | BOOL | **YES**（1.9 起） | 是否需要最新版逆地理数据（如城市变更实时更新） |
| userID | NSString * | — | 开发者指定用户 ID，便于排查问题 |
| accuracyAuthorization | BMKLAccuracyAuthorization | （只读） | 定位精度等级，iOS14+ 用户可控制；用于适配不同精度下的产品逻辑 |

#### 实例方法

| 方法 | 说明 |
|------|------|
| `requestLocationWithReGeocode:withNetworkState:completionBlock:` | 单次定位。正在连续定位时调用会失败返回 NO。按 desiredAccuracy 获取定位，精度不足会等待至超时后回调精度最高结果。可用 stopUpdatingLocation 取消。参数：withReGeocode 是否带逆地理（需联网），withNetWorkState 是否带移动热点识别（需联网） |
| `startUpdatingLocation` | 开始连续定位；会 cancel 所有单次定位请求 |
| `stopUpdatingLocation` | 停止连续定位；会 cancel 所有单次定位请求，也可用于取消单次定位 |
| `requestNetworkState` | 请求网络状态结果回调 |
| `startUpdatingHeading` | 开始设备朝向事件回调 |
| `stopUpdatingHeading` | 停止设备朝向事件回调 |
| `tryIndoorLocation` | 尝试高精度室内定位（仅室内定位版本生效） |
| `stopIndoorLocation` | 关闭高精度室内定位（仅室内定位版本生效） |
| `authorizationStatus` | 返回当前定位权限（CLAuthorizationStatus） |
| `requestTemporaryFullAccuracyAuthorizationWithPurposeKey:completion:` | 无全量精度权限时临时请求一次全量精度，系统弹框；purposeKey 对应 Info.plist 中 NSLocationTemporaryUsageDescriptionDictionary 的 key（iOS14+） |
| `requestTemporaryFullAccuracyAuthorizationWithPurposeKey:` | 请求一次全量定位精度等级（iOS14+） |

#### BMKLocationManagerDelegate 回调（头文件 BMKLocationManager.h）

| 方法 | 说明 |
|------|------|
| `BMKLocationManager:didUpdateLocation:` | 连续定位位置更新，location 为 BMKLocation |
| `BMKLocationManager:didFailWithError:` | 定位失败，error 含 BMKLocationErrorFailureAuth 等 |
| `BMKLocationManager:didUpdateHeading:` | 设备朝向更新（需先 startUpdatingHeading） |

单次定位结果在 `requestLocationWithReGeocode:...completionBlock:` 的 block 中返回。

#### 类方法

| 方法 | 说明 |
|------|------|
| `+ headingAvailable` | 设备是否支持朝向事件回调 |
| `+ BMKLocationCoordinateConvert:SrcType:DesType:` | 坐标转换。参数：coordinate 待转换经纬度，srctype 源坐标系类型，destype 目标百度坐标系类型（bd09ll、bd09mc）。返回目标百度坐标系经纬度 |
| `+ BMKLocationDataAvailableForCoordinate:withCoorType:` | 判断经纬度是否在大陆及港、澳地区。参数：coordinate 待判断经纬度，coortype 该经纬度的坐标系类型。返回 YES 表示境内 |

### BMKGeoFenceManager

地理围栏：创建、查询、删除围栏等，须在 setAgreePrivacy:YES 之后实例化。

**国内外/境内判断**：使用 `[BMKLocationManager BMKLocationDataAvailableForCoordinate:withCoorType:]`，coortype 传 `BMKLocationCoordinateTypeBMK09LL`，返回 YES 表示国内。与地图配合见 [utils.md](utils.md)。

## 获取位置信息（能力与对应方式）

| 能力 | 说明 |
|------|------|
| 单次定位 | BMKLocationManager 的 requestLocationWithReGeocode: completionBlock: |
| 连续定位 | startUpdatingLocation，通过 BMKLocationManagerDelegate 回调 |
| 后台定位 | allowsBackgroundLocationUpdates = YES，UIBackgroundModes 含 location，并配置 Info.plist 定位相关说明 |
| 室内定位 | 使用室内定位相关 API（具体见 BMKLocationKit 头文件） |

## 辅助功能（能力与对应类/接口）

| 能力 | 说明 |
|------|------|
| 地理围栏 | BMKGeoFenceManager，创建/删除围栏、状态回调 |
| 移动热点识别 | 定位 SDK 提供的热点相关接口 |
| 国内外位置判断 | BMKLocationManager 的 BMKLocationDataAvailableForCoordinate:withCoorType: |
| 坐标转换 | 定位 SDK 内坐标类型配置（coordinateType）或配合地图 utils 的 BMKCoordTrans |
| 防作弊 | 定位 SDK 提供的防作弊相关接口 |

错误码（如 BMKLocationErrorFailureAuth）、iOS 14 适配、提交 App Store 注意事项、HTTPS 等请查阅百度 LBS 开放平台 iOS 定位 SDK 文档。

## 与地图 SDK 的关系

- **仅需定位**：只集成 BMKLocationKit 即可。
- **地图 + 定位**：同时集成 BaiduMapKit 与 BMKLocationKit；地图上「我的位置」、定位图层等见 [mapview.md](mapview.md)（LocationViewAPI）；坐标转换、国内外判断等见 [utils.md](utils.md)。
- **隐私**：定位 SDK 必须通过 **BMKLocationAuth** 的 **setAgreePrivacy** 在用户同意后再初始化；地图 SDK 使用 BMKMapManager 的 setAgreePrivacy。详见上文「隐私与初始化」。

---

## 按需方案

| 需求 | 说明 |
|------|------|
| 仅需定位、无地图 | BMKLocationKit，BMKLocationAuth setAgreePrivacy → BMKLocationManager，coordinateType 按需设置 |
| 地图上显示我的位置 | BaiduMapKit + BMKLocationKit，mapview 的 showsUserLocation / userTrackingMode / updateLocationData；定位结果 coordinateType 建议 BMK09LL |
| 国内外/境内判断 | BMKLocationManager 的 BMKLocationDataAvailableForCoordinate:withCoorType:，见 [utils.md](utils.md) |
| 单次/连续/后台/室内定位 | BMKLocationManager requestLocationWithReGeocode、startUpdatingLocation、allowsBackgroundLocationUpdates 等 |
| 地理围栏/热点/坐标转换/防作弊 | BMKGeoFenceManager、coordinateType、及 SDK 对应辅助接口 |
