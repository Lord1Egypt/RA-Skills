## HarmonyNEXT 步骑行导航 SDK 开发指南

百度地图鸿蒙步骑行导航 SDK 是专为 HarmonyOS NEXT 系统开发的导航服务解决方案，提供步行与骑行场景下的路线规划、导航引导及界面渲染能力。通过 ArkTS 语言实现核心逻辑，支持开发者快速构建符合鸿蒙生态规范的导航功能，覆盖引擎初始化、路径计算、实时导航及状态监听等全流程需求。

---

### 1. 功能介绍

#### 1.1 多模式导航服务
- 支持步行 / 骑行双模式切换，通过 `NaviType` 枚举参数动态配置导航类型（`NaviType.WALK` / `NaviType.RIDE`）
- 提供路线规划、导航启停、偏航重算等核心功能

#### 1.2 智能路线规划
- 支持自定义起终点和途经点坐标（`LatLng` 类型）
- 支持多路线规划与路线切换（`multiRoute` / `switchRoute`）
- 提供路线规划结果可视化展示（`displayRoutePlanResult` 方法）

#### 1.3 生命周期管理
- 导航状态监控：通过 Promise 接口实现异步控制
- 支持 `start()` / `resume()` / `pause()` / `stop()` 完整生命周期操作
- 提供 `isStart()` 状态校验方法
- 支持多实例检测（`isMultiNaviCreated()`）

#### 1.4 默认 UI 组件化
- 内置导航界面组件（`walkRideDefaultUIPage`）
- 支持头部引导区、2D/3D 切换、路线变更、全览/播报按钮、底部 ETA 等交互控件
- 提供退出导航回调（`onExitNav`）等事件绑定

#### 1.5 实时状态监听
- 通过 `IGuideSubStatusListener` 接口实现 7 种导航状态事件回调
- 覆盖偏航预警、目的地接近、室内定位等关键场景
- 通过 `IGuideInfoListener` 接口获取诱导信息、剩余距离/时间、速度等实时数据

#### 1.6 语音播报（TTS）
- 通过 `ITTSPlugin` 接口实现自定义语音播报
- 支持抢占式 / 非抢占式播报模式

#### 1.7 模拟导航
- 通过 `MockLocationPlugin` 实现基于轨迹数据的模拟定位
- 支持自定义模拟速度和轨迹重载

---

### 2. 工程配置

#### 2.1 创建鸿蒙工程

在 DevEco Studio 中创建 HarmonyOS NEXT 工程。

#### 2.2 SDK 引用

在模块目录下的 `oh-package.json5` 文件中声明依赖：

```json5
"dependencies": {
  "@bdmap/map_walkride_search": "2.0.3"
}
```

> **注意**：`@bdmap/map_walkride_search` 是组合包，已包含 `@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util` 的能力。**不允许与独立包（如 `@bdmap/map`）混用**，否则会导致依赖冲突。详见 [包管理规范](package-management.md)。

安装依赖：

```bash
ohpm install
```

#### 2.3 权限配置

在 `module.json5` 文件中配置步骑行 SDK 所需权限：

```json5
{
  "requestPermissions": [
    { "name": "ohos.permission.LOCATION" },
    { "name": "ohos.permission.APPROXIMATELY_LOCATION" },
    { "name": "ohos.permission.LOCATION_IN_BACKGROUND" },
    { "name": "ohos.permission.GET_WIFI_INFO" },
    { "name": "ohos.permission.GET_NETWORK_INFO" },
    { "name": "ohos.permission.GET_BUNDLE_INFO" },
    { "name": "ohos.permission.INTERNET" }
  ]
}
```

| 权限 | 用途 | 是否必须 |
|------|------|----------|
| `ohos.permission.LOCATION` | 精确定位 | 是 |
| `ohos.permission.APPROXIMATELY_LOCATION` | 模糊定位 | 是 |
| `ohos.permission.LOCATION_IN_BACKGROUND` | 后台导航时持续定位 | 后台导航必须 |
| `ohos.permission.GET_WIFI_INFO` | 网络信息获取 | 是 |
| `ohos.permission.GET_NETWORK_INFO` | 网络信息获取 | 是 |
| `ohos.permission.GET_BUNDLE_INFO` | 包信息获取 | 是 |
| `ohos.permission.INTERNET` | 网络请求 | 是 |

---

### 3. 导入与基础类型

使用组合包 `@bdmap/map_walkride_search` 时，所有类型均从该包导入：

```typescript
// 地图相关
import {
  MapComponent, MapController, MapOptions, MapStatus,
  CoordUtil, CoordTrans, Event
} from '@bdmap/map_walkride_search';

// 导航核心类
import {
  BDNaviService, NaviType, NaviMode,
  RouteNodeInfo, RoutePlanOption, RoutePlanError,
  MockLocationPlugin, DefaultMsg,
  walkRideDefaultUIPage
} from '@bdmap/map_walkride_search';

// 监听器接口
import {
  IRoutePlanListener, IGuideSubStatusListener,
  IGuideInfoListener, ITTSPlugin, ILocationPlugin
} from '@bdmap/map_walkride_search';

// 检索相关
import {
  PoiSearch, PoiCitySearchOption, PoiCitySearchOptionParams,
  PoiInfo, ERRORNO
} from '@bdmap/map_walkride_search';

// 基础类型
import { LatLng } from '@bdmap/map_walkride_search';

```

---

### 4. 引擎初始化

在使用步骑行导航功能前，需要对引擎进行初始化。初始化成功后方可调用其他功能。

#### 4.1 创建导航服务对象

通过入参选择创建步行或骑行服务：

```typescript
// 创建步行导航服务
let service: BDNaviService = new BDNaviService(NaviType.WALK);

// 或创建骑行导航服务
let service: BDNaviService = new BDNaviService(NaviType.RIDE);
```
> **注意**：
> 如果当前页面同时需要步骑行导航功能，只需创建一个导航服务对象即可，动态切换导航类型 `NaviType` 参数实现。具体参考 4.2 节内容。

#### 4.2 动态切换导航类型

也可在路线规划前修改服务对象的类型：

```typescript
// 切换为骑行模式
service.setNaviType(NaviType.RIDE);

// 切换为步行模式
service.setNaviType(NaviType.WALK);
```

#### 4.3 配置 TTS 语音插件（可选）

若需要语音播报能力，需在引擎初始化前注册 TTS 插件。开发者需实现 `ITTSPlugin` 接口：

```typescript
import { ITTSPlugin } from '@bdmap/map_walkride_search';

@ObservedV2
class DefaultTTSPlugin implements ITTSPlugin {
  @Trace voiceText: string = '';

  init(): void {
    // TTS 引擎初始化，如加载语音合成资源
  }

  unInit(): void {
    // TTS 引擎释放
  }

  /**
   * 播放 TTS 文本。
   * @param speech 播报语音文本
   * @param bPreempt 是否抢占当前播报
   * @returns 播报状态码（0 表示成功）
   */
  playTTSText(speech: string, bPreempt: boolean): number {
    this.voiceText = speech;
    Logger.info('SportHealthMap', { action: 'playTTS', speech: speech, preempt: bPreempt });
    // 实际项目中应调用系统 TTS 或第三方语音合成能力
    return 0;
  }
}
```

在引擎初始化前注册：

```typescript
private ttsPlugin: DefaultTTSPlugin = new DefaultTTSPlugin();

aboutToAppear() {
  this.service.initializer().setTTsPlugin(this.ttsPlugin);
}
```

#### 4.4 配置自定义定位插件（可选）

步骑行导航 SDK 默认使用内置定位能力。若业务已有独立的定位服务（如 `@bdmap/locsdk`），可通过实现 `ILocationPlugin` 接口自定义定位插件，并在引擎初始化前通过 `setLocationPlugin` 注册，使导航引擎使用外部定位数据源。

##### 4.4.1 实现 ILocationPlugin 接口

`ILocationPlugin` 接口定义了定位插件的标准能力，需实现以下方法：

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `init(context: Context)` | `void` | 初始化定位服务 |
| `unInit()` | `void` | 释放定位资源 |
| `startContinuousLocation(callback)` | `Promise<boolean>` | 启动连续定位，通过 callback 持续回传位置 |
| `stopContinuousLocation()` | `Promise<boolean>` | 停止连续定位 |
| `getCurrentLocation()` | `Promise<BMLocation>` | 获取当前位置 |

以下示例基于 `@bdmap/locsdk` 实现自定义定位插件：

```typescript
import { Context } from "@ohos.abilityAccessCtrl";
import { BDLocation, BDLocationListener } from "@bdmap/locsdk";
import { ILocationPlugin, BMLocation as WalkRideLocation } from "@bdmap/map_walkride_search";

export class WalkRideLocPlugin implements ILocationPlugin {
  private continuousCallback: ((location: WalkRideLocation) => void) | null = null;
  private locListener: BDLocationListener | null = new BDLocationListener();
  private initialized = false;
  private currentLoc: WalkRideLocation | null = null;
  private locationClient: LocationClient;

  constructor(loc: LocationClient) {
    this.locationClient = loc;
  }

  init(context: Context): void {
    if (!this.initialized) {
      // 初始化定位服务
      this.locListener = new BDLocationListener();
      this.initialized = true;
    }
  }

  unInit(): void {
    if (this.initialized) {
      try {
        this.stopContinuousLocation()
          .then(() => {
            this.locListener = null;
            this.initialized = false;
          });
      } catch (err) {
        console.error("Failed to stop location during unInit", err);
        throw new Error(`Failed to uninitialize: ${err.message}`);
      }
    }
  }

  /**
   * 将 locsdk 的 BMLocation 转换为步骑行 SDK 的 BMLocation。
   * 需映射经纬度、海拔、速度、方向等字段，并设置定位精度。
   */
  private convertToWalkRideLocation(source: BDLocation | undefined): WalkRideLocation {
    const target = new WalkRideLocation();
    if (source) {
      target.setLongitude(source.getLongitude());
      target.setLatitude(source.getLatitude());
      target.setAltitude(source.getAltitude());
      target.setSpeed(source.getSpeed());
      target.setDirection(source.getDirection());
    } else {
      target.setLongitude(0);
      target.setLatitude(0);
      target.setAltitude(0);
      target.setSpeed(0);
      target.setDirection(0);
    }
    target.setRadius(10);
    this.currentLoc = target;
    return target;
  }

  async startContinuousLocation(callback: (location: WalkRideLocation) => void): Promise<boolean> {
    this.continuousCallback = callback;

    if (this.locListener) {
      // 将 locsdk 的定位回调转换后传递给导航引擎
      this.locListener.onReceiveLocationBlock = (value: BDLocation) => {
        if (this.continuousCallback) {
          this.continuousCallback(this.convertToWalkRideLocation(value));
        }
      };

      this.locationClient.registerLocationListener(this.locListener);
    }

    return true;
  }

  async stopContinuousLocation(): Promise<boolean> {
    if (this.continuousCallback && this.locListener) {
      this.locationClient.unRegisterLocationListener(this.locListener);
      this.continuousCallback = null;
      return Promise.resolve(true);
    } else {
      return Promise.reject(false);
    }
  }

  async getCurrentLocation(): Promise<WalkRideLocation> {
    return Promise.resolve(this.convertToWalkRideLocation(this.currentLoc));
  }
}
```

##### 4.4.2 注册自定义定位插件

在引擎初始化前，通过 `setLocationPlugin` 将自定义插件注册到导航服务：

```typescript
import { WalkRideLocPlugin } from './WalkRideLocPlugin';

// 假设 locationClient 为已初始化的定位服务客户端
private locPlugin: WalkRideLocPlugin = new WalkRideLocPlugin(this.locationClient);

aboutToAppear() {
  // 注册自定义定位插件（需在 init() 之前调用）
  this.service.initializer().setLocationPlugin(this.locPlugin);

  // 注册 TTS 插件（可选）
  this.service.initializer().setTTsPlugin(this.ttsPlugin);
}
```

> **注意**：
> - `setLocationPlugin` 必须在 `init()` 之前调用，否则不生效。
> - 自定义定位插件与模拟定位插件（`MockLocationPlugin`）互斥，注册新插件会替换当前插件。
> - 退出导航时若需恢复默认定位，应调用 `resetLocationPlugin()`。

#### 4.5 初始化导航引擎

引擎初始化需传入上下文和地图控制器，必须在 `MapComponent.onReady` 回调中执行：

```typescript
MapComponent({
  onReady: (err: Error | null, map: MapController) => {
    if (map) {
      this.mapController = map;

      // 初始化导航引擎（需传入 UIAbility 上下文和 MapController）
      this.service.initializer()
        .init(getContext(this) as common.UIAbilityContext, this.mapController)
        .then(() => {
          Logger.info('SportHealthMap', { action: 'naviEngineInit', status: 'success' });
          promptAction.showToast({ message: '导航引擎初始化成功', duration: 2000 });
        })
        .catch((reason: string) => {
          Logger.error('SportHealthMap', { action: 'naviEngineInit', error: reason });
          promptAction.showToast({ message: '导航引擎初始化失败：' + reason, duration: 3000 });
        });
    }
  },
  mapOptions: this.mapOptions
}).width('100%').height('100%')
```

#### 4.6 隐藏底图默认控件（可选）

导航场景下通常不需要默认的缩放和比例尺控件，可在地图就绪后关闭：

```typescript
import { Event } from '@bdmap/map_walkride_search';
import { emitter } from '@kit.BasicServicesKit';

// 隐藏缩放控件
emitter.emit({ eventId: Event.ZoomCom }, {
  data: { show: false, mapViewId: this.mapController?.mapViewId }
});
// 隐藏比例尺控件
emitter.emit({ eventId: Event.ScaleCom }, {
  data: { show: false, mapViewId: this.mapController?.mapViewId }
});
```

---

### 5. 坐标转换

步骑行 SDK 内部使用百度坐标系（BD09ll）。如果外部数据源使用 WGS84 或 GCJ-02 坐标，需在传入前进行转换：

```typescript
import { CoordTrans } from '@bdmap/map_walkride_search';

// WGS84 → 百度坐标
let wgsLatLng: LatLng = new LatLng(40.048241, 116.296165);
let bdLatLng: LatLng | null = CoordTrans.wgsToBaidu(wgsLatLng);

// GCJ-02 → 百度坐标
let gcjLatLng: LatLng = new LatLng(40.048241, 116.296165);
let bdLatLng2: LatLng | null = CoordTrans.gcjToBaidu(gcjLatLng);

// 百度坐标 → GCJ-02
let bdBack: LatLng | null = CoordTrans.baiduToGcj(bdLatLng!);
```

> **注意**：转换后需进行空值检查，`CoordTrans` 方法在参数异常时会返回 `null`。

---

### 6. 路线规划

#### 6.1 构造起终点

使用 `RouteNodeInfo` 描述起终点位置：

```typescript
let startLocation: RouteNodeInfo = new RouteNodeInfo();
startLocation.location = new LatLng(40.048241, 116.296165);

let endLocation: RouteNodeInfo = new RouteNodeInfo();
endLocation.location = new LatLng(40.04721, 116.316372);
```

#### 6.2 构造路线规划参数

使用 `RoutePlanOption` 的链式调用设置参数：

```typescript
let param: RoutePlanOption = new RoutePlanOption()
  .startNodeInfo(startLocation)
  .endNodeInfo(endLocation)
  .extraNaviMode(NaviMode.RealNavi);  // 设置为真实导航模式
```

**NaviMode 取值说明：**

| 模式 | 值 | 说明 |
|------|---|------|
| `NaviMode.Invalid` | 0 | 无效 |
| `NaviMode.RealNavi` | 1 | 真实导航（使用实际 GPS 定位） |
| `NaviMode.DemoNavi` | 2 | 模拟导航 |
| `NaviMode.TrackNavi` | 3 | 轨迹文件导航 |

#### 6.3 计算起终点距离（可选）

可在规划前使用 `CoordUtil` 计算两点间距离：

```typescript
import { CoordUtil } from '@bdmap/map_walkride_search';

let distance: number = CoordUtil.getDistanceByLL(startLocation.location!, endLocation.location!);
Logger.info('SportHealthMap', { action: 'calcDistance', distance: distance });
// distance 单位为米，返回 -1 表示计算失败
```

#### 6.4 发起路线规划

通过 `routePlanService().routePlanWithRouteNode()` 发起规划，并通过 `IRoutePlanListener` 回调处理结果：

```typescript
/** 路线规划回调 */
private routePlanListener: IRoutePlanListener = new Object({
  /** 路线规划开始 */
  onRoutePlanStart: (): void => {
    Logger.info('SportHealthMap', { action: 'routePlanStart' });
  },
  /** 路线规划成功 */
  onRoutePlanSuccess: (): void => {
    Logger.info('SportHealthMap', { action: 'routePlanSuccess' });
    // 在地图上展示规划路线
    this.service.routePlanService().displayRoutePlanResult();
    promptAction.showToast({ message: '路线规划成功', duration: 2000 });
  },
  /** 路线规划失败 */
  onRoutePlanFail: (error: RoutePlanError): void => {
    let errorMsg: string = this.routeSearchError(error);
    Logger.error('SportHealthMap', { action: 'routePlanFail', error: errorMsg });
    promptAction.showToast({ message: '路线规划失败：' + errorMsg, duration: 3000 });
  }
}) as IRoutePlanListener;

// 注册导航状态监听（建议在路线规划前完成）
this.service.navigationService()
  .info()
  .routeGuidanceInfo()
  .addRGSubStatusListener(this.guideSubStatusListener);

// 发起路线规划
this.service.routePlanService().routePlanWithRouteNode(param, this.routePlanListener);
```

#### 6.5 路线展示与控制

```typescript
// 展示路线规划结果（多路线场景可传入 MultiRouteDisplayOption 自定义样式）
this.service.routePlanService().displayRoutePlanResult();

// 隐藏/清除路线展示
this.service.routePlanService().cancelRoutePlanDisplay();

// 切换到指定路线（多路线场景，routeIndex 从 0 开始）
this.service.routePlanService().switchRoute(routeIndex)
  .then((success: boolean) => {
    Logger.info('SportHealthMap', { action: 'switchRoute', index: routeIndex, success: success });
  });
```

#### 6.6 路线规划错误码

`RoutePlanError` 枚举定义了完整的错误码体系：

| 错误码 | 枚举值 | 说明 |
|--------|--------|------|
| 1000 | `SERVER_UNUSUAL` | 服务器异常 |
| 1001 | `PARSE_FAIL` | 数据解析失败 |
| 1002 | `NET_ERR` | 网络错误 |
| 1010 | `FORWARD_AK_ERROR` | AK 鉴权失败 |
| 1011 | `INVAILD_PERMISSION` | 权限未开通 |
| 2000 | `PARAM_ERROR` | 参数错误 |
| 2001 | `DISTANCE_LESS_THAN_30M` | 起终点距离小于 30 米 |
| 2002 | `DISTANCE_MORE_THAN_50KM` | 起终点距离大于 50 公里 |
| 2003 | `DISTANCE_TOO_CLOSE` | 起终点距离过近 |
| 2004 | `DISTANCE_MORE_THAN` | 起终点距离过远 |
| 2005 | `ROUTE_DIS_SAME` | 起终点相同 |
| 3000 | `IS_NOT_SUPPORT_INDOOR_NAVI` | 不支持室内导航 |
| 3001 | `IS_NOT_SUPPORT_AR_NAVI` | API 级别不支持 AR 步行导航 |
| 4000 | `ENGINE_STATUS_ERROR` | 引擎状态错误 |
| 4001 | `NAVI_STATUS_ERROR` | 导航状态错误 |
| 5000 | `SDK_NOT_INITIALIZED` | SDK 未初始化 |
| 5001 | `REQUEST_TIMEOUT` | 请求超时 |
| 5002 | `ENGINE_SEARCH_ERROR` | 引擎检索错误 |
| 5003 | `INTERRUPTED` | 请求被中断 |

建议封装错误码解码方法，为用户提供友好的错误提示：

```typescript
/**
 * 将路线规划错误码转换为用户友好的提示信息。
 * @param error 路线规划错误枚举
 * @returns 中文错误提示
 */
routeSearchError(error: RoutePlanError): string {
  const errorMap: Record<string, string> = {
    [RoutePlanError.SERVER_UNUSUAL.toString()]: '服务器异常，请稍后重试',
    [RoutePlanError.PARSE_FAIL.toString()]: '数据解析失败',
    [RoutePlanError.NET_ERR.toString()]: '网络错误，请检查网络连接',
    [RoutePlanError.FORWARD_AK_ERROR.toString()]: '鉴权失败，请检查 AK 配置',
    [RoutePlanError.INVAILD_PERMISSION.toString()]: '权限未开通',
    [RoutePlanError.PARAM_ERROR.toString()]: '参数错误',
    [RoutePlanError.DISTANCE_LESS_THAN_30M.toString()]: '起终点距离太近（小于 30 米）',
    [RoutePlanError.DISTANCE_MORE_THAN_50KM.toString()]: '起终点距离太远（超过 50 公里）',
    [RoutePlanError.DISTANCE_TOO_CLOSE.toString()]: '起终点距离过近',
    [RoutePlanError.DISTANCE_MORE_THAN.toString()]: '起终点距离过远',
    [RoutePlanError.ROUTE_DIS_SAME.toString()]: '起终点位置相同',
    [RoutePlanError.IS_NOT_SUPPORT_INDOOR_NAVI.toString()]: '不支持该室内导航',
    [RoutePlanError.IS_NOT_SUPPORT_AR_NAVI.toString()]: 'API 级别不支持 AR 步行导航',
    [RoutePlanError.ENGINE_STATUS_ERROR.toString()]: '引擎状态错误',
    [RoutePlanError.SDK_NOT_INITIALIZED.toString()]: 'SDK 未初始化',
    [RoutePlanError.REQUEST_TIMEOUT.toString()]: '请求超时，请检查网络',
    [RoutePlanError.ENGINE_SEARCH_ERROR.toString()]: '引擎检索错误',
  };
  return errorMap[error.toString()] ?? '未知错误';
}
```

---

### 7. 导航控制

#### 7.1 开始真实导航

开始导航前必须先清除路线展示，再启动导航生命周期：

```typescript
startNavi(): void {
  // 必须先清除路线展示覆盖物
  this.service.routePlanService().cancelRoutePlanDisplay();

  // 启动导航
  this.service.navigationService()
    .lifecycle()
    .start()
    .then(() => {
      this.serviceState = true;
      Logger.info('SportHealthMap', { action: 'naviStart', status: 'success' });
      promptAction.showToast({ message: '导航已开始', duration: 2000 });

      // 检测多实例状态（可选）
      const multiResult = this.service.navigationService()
        .lifecycle()
        .isMultiNaviCreated();
      if (multiResult?.code !== 0) {
        promptAction.showToast({ message: multiResult?.message, duration: 2000 });
      }
    })
    .catch((reason: string) => {
      Logger.error('SportHealthMap', { action: 'naviStart', error: reason });
      promptAction.showToast({ message: '导航启动失败：' + reason, duration: 3000 });
    });
}
```

#### 7.2 模拟导航

使用 `MockLocationPlugin` 可基于预置的 GPS 轨迹数据模拟导航过程，适用于开发调试阶段：

```typescript
// WGS84坐标类型数据
interface GPSPoint {
  type: string; // 坐标类型，必填项，默认 2，代表  "wgs84"。当前仅支持 "wgs84" 坐标类型
  longitude: number; // 必须
  latitude: number; // 必须
  altitude: number; // 高度， 默认 0
  direction: number; // 方向范围 0~360，0为正北，顺时针方向
  speed: number; // 速度，默认 0
  timestamp: string; // 时间戳，格式为 'yyyy-MM-dd HH:mm:ss'
  unknownFlag: number; // 未知标识， 默认 0
  timeIncrement: number; // 轨迹点时间增量，默认 1000
}
const trackPoints: GPSPoint[] = [
  // 轨迹点数据
];
const trackData = trackPoints.map(gpsPoint=>{
  return `${gpsPoint.type},${gpsPoint.longitude},${gpsPoint.latitude},${gpsPoint.altitude},${gpsPoint.direction},${gpsPoint.speed},${gpsPoint.timestamp},${gpsPoint.unknownFlag},${gpsPoint.timeIncrement}`;
}).join('\n')

startMockNavi(): void {
  // 创建模拟定位插件（传入轨迹字符串和模拟速度）
  let mockPlugin: MockLocationPlugin = new MockLocationPlugin(trackData,
    100  // 模拟速度，值越小移动越快
  );

  // 注册模拟定位插件
  this.service.initializer().setLocationPlugin(mockPlugin);
  this.mockPlugin = mockPlugin;

  // 启动导航（流程同真实导航）
  this.startNavi();
}
```

> **注意**：模拟导航结束或退出时，必须重置定位插件并释放资源：

```typescript
exitNavi(): void {
  if (this.mockPlugin) {
    this.service.initializer().resetLocationPlugin();
    this.mockPlugin = null;
  }
  this.serviceState = false;
}
```

#### 7.3 导航生命周期方法

`navigationService().lifecycle()` 提供以下生命周期方法：

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `start()` | `Promise<void>` | 开始导航 |
| `resume()` | `void` | 恢复导航（从暂停状态恢复） |
| `pause()` | `void` | 暂停导航 |
| `stop()` | `void` | 停止导航 |
| `isStart()` | `boolean` | 判断是否已开始导航 |
| `isMultiNaviCreated()` | `IMultiNaviCallbackResult` | 检测是否存在多实例 |

---

### 8. 导航状态监听

#### 8.1 导航子状态监听（IGuideSubStatusListener）

通过 `IGuideSubStatusListener` 接口监听导航过程中的关键状态变化：

```typescript
private guideSubStatusListener: IGuideSubStatusListener = new Object({
  /** 已开始偏航 */
  onRouteFarAway: (msg: DefaultMsg): void => {
    Logger.info('SportHealthMap', { action: 'onRouteFarAway', msg: msg });
    promptAction.showToast({ message: '您已偏离路线，正在重新规划', duration: 2000 });
  },
  /** 偏航规划中 */
  onRoutePlanYawing: (msg: DefaultMsg): void => {
    Logger.info('SportHealthMap', { action: 'onRoutePlanYawing', msg: msg });
  },
  /** 偏航规划结束 */
  onReRouteComplete: (msg: DefaultMsg): void => {
    Logger.info('SportHealthMap', { action: 'onReRouteComplete', msg: msg });
    promptAction.showToast({ message: '路线已重新规划', duration: 2000 });
  },
  /** 接近目的地 */
  onArriveDestNear: (msg: DefaultMsg): void => {
    Logger.info('SportHealthMap', { action: 'onArriveDestNear', msg: msg });
    promptAction.showToast({ message: '即将到达目的地', duration: 2000 });
  },
  /** 到达目的地 */
  onArriveDest: (msg: DefaultMsg): void => {
    Logger.info('SportHealthMap', { action: 'onArriveDest', msg: msg });
  },
  /** 到达室内目的地 */
  onIndoorEnd: (msg: DefaultMsg): void => {
    Logger.info('SportHealthMap', { action: 'onIndoorEnd', msg: msg });
  },
  /** 到达最终目的地 */
  onFinalEnd: (msg: DefaultMsg): void => {
    Logger.info('SportHealthMap', { action: 'onFinalEnd', msg: msg });
    promptAction.showToast({ message: '已到达目的地', duration: 2000 });
    // 到达后自动停止导航
    this.stopNavi();
  }
}) as IGuideSubStatusListener;
```

注册监听（建议在路线规划前完成）：

```typescript
this.service.navigationService()
  .info()
  .routeGuidanceInfo()
  .addRGSubStatusListener(this.guideSubStatusListener);
```

#### 8.2 诱导信息监听（IGuideInfoListener）

通过 `IGuideInfoListener` 获取导航过程中的实时诱导信息：

```typescript
private guideInfoListener: IGuideInfoListener = new Object({
  /** 简易诱导信息更新（如"前方 200 米左转"） */
  onSimpleGuideInfoUpdate: (info: BWNaviSimpleMapInfo): void => {
    Logger.info('SportHealthMap', { action: 'guideInfoUpdate', info: info });
  },
  /** 剩余距离和时间更新 */
  onRemainInfoUpdate: (record: Record<string, BMObject>): void => {
    Logger.info('SportHealthMap', { action: 'remainInfoUpdate' });
  },
  /** 速度和行驶距离更新 */
  onSpeedUpdate: (travelData: BWNaviTravelData): void => {
    Logger.info('SportHealthMap', { action: 'speedUpdate' });
  },
  /** 定位匹配路线信息 */
  onMatchRouteInfo: (record: Record<string, BMObject>): void => {
    Logger.info('SportHealthMap', { action: 'matchRouteInfo' });
  },
  /** 红绿灯状态变化 */
  onTrafficLightUpdate: (json: string): void => {
    Logger.info('SportHealthMap', { action: 'trafficLightUpdate', data: json });
  },
  /** 外部路线图层信息 */
  onOutNaviInfo: (record: Record<string, BMObject>): void => {
    Logger.info('SportHealthMap', { action: 'outNaviInfo' });
  }
}) as IGuideInfoListener;
```

---

### 9. 界面渲染

#### 9.1 默认导航 UI

导航开始后，可渲染步骑行导航默认 UI。`walkRideDefaultUIPage` 是内置组件，提供完整的导航界面：

```typescript
if (this.serviceState) {
  walkRideDefaultUIPage({
    service: this.service,
    walkRideUIPageOption: {
      isAutoStop: true,                // 到达终点后自动停止导航
      onExitNav: () => { this.exitNavi(); },  // 退出导航回调
      // 以下均为可选参数，默认全部显示
      headerGuideShow: true,           // 头部诱导区
      twoDThreeDToggleShow: true,      // 2D/3D 切换按钮
      transRouteBtnShow: true,         // 路线朝向变更按钮
      voiceViewChangeShow: true,       // 全览、播报按钮
      naviETAShow: true                // 底部 ETA 信息
    }
  })
    .hitTestBehavior(HitTestMode.None)  // 确保默认 UI 不拦截底图手势
}
```

**UI 控件说明：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `isAutoStop` | `boolean` | - | 到达终点后是否自动停止导航 |
| `onExitNav` | `() => void` | - | 用户退出导航时的回调 |
| `headerGuideShow` | `boolean` | `true` | 头部诱导引导区 |
| `twoDThreeDToggleShow` | `boolean` | `true` | 2D/3D 视图切换按钮 |
| `transRouteBtnShow` | `boolean` | `true` | 路线朝向变更按钮 |
| `voiceViewChangeShow` | `boolean` | `true` | 全览/语音播报按钮 |
| `naviETAShow` | `boolean` | `true` | 底部预计到达时间 |

> **重要**：必须设置 `.hitTestBehavior(HitTestMode.None)`，否则默认 UI 会拦截底图的手势事件。

---

### 10. POI 检索（设置起终点）

步骑行场景中，通常通过 POI 检索让用户搜索并选择起终点。组合包已内置检索能力：

```typescript
import {
  PoiSearch, PoiCitySearchOption, PoiCitySearchOptionParams,
  PoiInfo, ERRORNO
} from '@bdmap/map_walkride_search';

/**
 * 在指定城市内搜索 POI。
 * @param keyword 搜索关键词
 * @param city 城市名称
 */
async searchAddress(keyword: string, city: string): Promise<void> {
  let search: PoiSearch = PoiSearch.newInstance();
  let optionParams: PoiCitySearchOptionParams = {
    keyword: keyword,
    city: city
  };
  let option: PoiCitySearchOption = new PoiCitySearchOption(optionParams);
  let searchResult = await search.searchInCity(option);

  if (searchResult.error === ERRORNO.NO_ERROR && searchResult.arrayPoiInfo !== undefined) {
    // 检索成功，展示结果列表
    this.addressList = searchResult.arrayPoiInfo;
    Logger.info('SportHealthMap', { action: 'poiSearch', count: this.addressList.length });
  } else {
    // 检索失败，提示用户
    Logger.error('SportHealthMap', { action: 'poiSearch', error: searchResult.error });
    promptAction.showToast({ message: '搜索失败，请稍后重试', duration: 2000 });
  }
}
```

用户选择结果后，将 `PoiInfo.location` 用作路线规划的起点或终点。

---

### 11. 资源释放

#### 11.1 退出导航

退出导航时需重置状态并释放模拟插件（如有）：

```typescript
exitNavi(): void {
  // 释放模拟定位插件
  if (this.mockPlugin) {
    this.service.initializer().resetLocationPlugin();
    this.mockPlugin = null;
  }
  // 重置业务状态
  this.serviceState = false;
}
```

#### 11.2 停止导航

导航自动结束（到达目的地）或手动停止时：

```typescript
stopNavi(): void {
  this.service.navigationService().lifecycle().stop();
  this.exitNavi();
}
```

#### 11.3 销毁导航引擎

页面销毁时必须释放导航实例，避免内存泄漏：

```typescript
aboutToDisappear(): void {
  this.service.initializer()
    .unInit()
    .then(() => {
      Logger.info('SportHealthMap', { action: 'naviEngineDestroy', status: 'success' });
    })
    .catch(() => {
      Logger.error('SportHealthMap', { action: 'naviEngineDestroy', status: 'fail' });
    });
}
```

---

### 12. 完整开发流程总结

以下是步骑行导航的典型开发流程：

```
1. 工程配置
   └─ oh-package.json5 添加 @bdmap/map_walkride_search
   └─ module.json5 配置权限

2. 页面初始化
   └─ aboutToAppear: 注册 TTS 插件、坐标转换
   └─ MapComponent.onReady: 获取 MapController → 初始化导航引擎

3. 路线规划
   └─ 用户选择起终点（POI 检索 / 地图选点 / 手动输入）
   └─ 构造 RoutePlanOption → routePlanWithRouteNode()
   └─ onRoutePlanSuccess → displayRoutePlanResult() 展示路线

4. 开始导航
   └─ cancelRoutePlanDisplay() 清除路线展示
   └─ lifecycle().start() 启动导航
   └─ 渲染 walkRideDefaultUIPage 默认 UI

5. 导航中
   └─ IGuideSubStatusListener 监听偏航 / 到达等状态
   └─ IGuideInfoListener 获取诱导 / 剩余距离等信息
   └─ ITTSPlugin 处理语音播报

6. 导航结束
   └─ lifecycle().stop() 停止导航
   └─ resetLocationPlugin() 释放模拟插件
   └─ initializer().unInit() 销毁引擎

7. 页面销毁
   └─ aboutToDisappear: unInit() 释放所有资源
```

---

### 13. 注意事项

1. **引擎初始化时序**：`init()` 必须在 `MapComponent.onReady` 中获取 `MapController` 后调用，不可在页面构造阶段提前调用。
2. **导航前清除路线**：调用 `start()` 前必须先执行 `cancelRoutePlanDisplay()`，否则路线展示覆盖物会与导航覆盖物冲突。
3. **坐标系一致性**：SDK 使用百度坐标系（BD09ll），外部 WGS84/GCJ-02 数据必须通过 `CoordTrans` 转换后再传入。
4. **模拟导航退出**：使用 `MockLocationPlugin` 后，退出导航时必须调用 `resetLocationPlugin()` 重置为默认定位插件。
5. **引擎销毁**：页面 `aboutToDisappear` 中必须调用 `unInit()` 释放引擎资源，否则会导致内存泄漏。
6. **默认 UI 手势穿透**：`walkRideDefaultUIPage` 必须设置 `.hitTestBehavior(HitTestMode.None)`，否则会拦截底图手势。
7. **组合包互斥**：`@bdmap/map_walkride_search` 与独立包（`@bdmap/map` 等）不可混用，详见 [包管理规范](package-management.md)。
8. **构建自检**：每次完成代码改动后，需在工程根目录执行 `ohpm install` 和 `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon` 进行构建自检，详见 [构建与编码错误自检规范](build-and-test.md)。
