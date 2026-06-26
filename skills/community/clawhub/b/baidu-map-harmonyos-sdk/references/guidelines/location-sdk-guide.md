## Baidu HarmonyOS NEXT 定位 SDK 开发指南（@bdmap/locsdk）

本指南整合了 `SKILL.md` 中关于定位能力（模块：locsdk / `@bdmap/locsdk`）的详细规范，用于实现基础 / 单次 / 后台定位，以及经纬度 / 地址 / POI 等位置信息获取。

> 使用本指南时，需同时遵守 `SKILL.md` 中的「日志 / 注释 / 模块化 / 用户反馈 / 构建检查」等强制要求。

---

### 1. 使用场景与依赖

典型使用场景：

- 前台连续定位（实时位置展示、轨迹采集）
- 单次定位（位置打点、选择当前地址）
- 后台持续定位（安全守护、行程跟踪）
- 获取经纬度 + 精度、地址信息、位置描述、周边 POI

典型触发定位能力业务流程
    ↓
① 隐私协议弹窗 → 不同意 → 提示并阻断
    ↓ 同意
② 申请定位权限 → 拒绝 → 弹出引导弹窗（前往设置）
    ↓ 授予              ↓ UI显示「申请定位权限」按钮（支持重试）
③ 启动定位

依赖安装方式：

- 线下引用（推荐在无外网或内网环境）：
  - 将官网下载的 `locsdk.har` 放到 `entry/libs` 目录；
  - 在 `entry/oh-package.json5` 中配置：

```json
"dependencies": {
  "@bdmap/locsdk": "file:libs/locsdk.har"
}
```

- 线上引用（常规环境）：

```json
"dependencies": {
  "@bdmap/locsdk": "1.1.7"
}
```

规范要求：

- 团队在一个工程内统一 `@bdmap/locsdk` 版本号，避免多模块间版本不一致；
- 依赖安装后，必须在项目根目录执行 `ohpm install` 与构建命令进行自检（见「构建与编码错误自检规范」）。

强制要求：
- 使用 `@bdmap/locsdk` 的 `LocationClient` 进行设备定位时，**必须严格遵循以下初始化顺序和校验规范**，否则极易出现"定位回调无数据"、"坐标始终为 (0,0)"、"定位结果不准确"等难以排查的问题。
- 初始化三步骤（必须按顺序执行，缺一不可）
  **Step 1 — 隐私合规声明**（推荐通过用户隐私协议弹窗形式）：
  ```typescript
  LocationClient.setAgreePrivacy(true);
  ```
  必须在用户同意隐私政策后调用。若遗漏，SDK 内部鉴权流程不会启动，定位回调永远不触发。

  **Step 2 — AK 鉴权校验**（在同意隐私政策后中紧接执行）：
  ```typescript
  LocationClient.checkAuthKey(BAIDU_MAP_AK, this.context, (authResult: string): void => {
    Logger.info('SportHealthMap', JSON.stringify({ action: 'locSdkAuthKey', result: authResult }));
  });
  ```
  鉴权失败时定位 SDK 会静默返回无效坐标（如 `0, 0`），**不会抛异常**，极难排查。建议在回调中记录鉴权结果，便于定位问题。

  **Step 3 — 等待运行时权限授予后再启动定位**（在页面级执行）：
  ```typescript
  private async startLocation(): Promise<void> {
    const context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    const granted: boolean = await PermissionHelper.checkAndRequestLocationPermissions(context);
    if (!granted) {
      // 提示用户并返回，不启动 LocationClient
      return;
    }
    // 权限已授予，安全启动定位
    this.locationClient = new LocationClient(context);
    // ... 注册监听器、配置参数、start()
  }
  ```

  **常见竞态错误**：权限申请是异步的（弹窗等待用户操作），但地图 `onReady` 回调可能在权限弹窗响应之前就触发。如果在 `onReady` 中直接 `new LocationClient().start()` 而不 `await` 权限结果，定位会在权限未授予的状态下启动，导致静默失败。
- 定位结果有效性校验（强制要求）
  **禁止直接使用 `getLatitude()`/`getLongitude()` 的返回值**，必须先校验定位是否成功：

  ```typescript
  onReceiveLocation(bdLocation: BDLocation): void {
    // ① 校验定位是否成功
    if (!bdLocation.isLocSuccess()) {
      const locType: number = bdLocation.getLocType();
      const desc: string = bdLocation.getLocTypeDescription() ?? 'unknown';
      Logger.warn('SportHealthMap', JSON.stringify({
        action: 'locResult', success: false, locType: locType, desc: desc
      }));
      return;  // 不处理失败结果
    }

    // ② 校验坐标有效性（排除 0,0 无效坐标）
    const lat: number = bdLocation.getLatitude();
    const lng: number = bdLocation.getLongitude();
    if (lat === 0 && lng === 0) {
      Logger.warn('SportHealthMap', JSON.stringify({ action: 'locResult', reason: 'invalidCoords' }));
      return;
    }

    // ③ 校验精度半径（可选：超过阈值提示用户）
    const radius: number = bdLocation.getRadius();
    if (radius > 500) {
      Logger.warn('SportHealthMap', JSON.stringify({ action: 'locResult', radius: radius, reason: 'lowAccuracy' }));
      // 根据业务需求决定是否使用该结果
    }

    // ④ 安全使用定位结果
    const addr: string = bdLocation.getAddrStr() ?? '未知地址';
    // ... 业务逻辑
  }
  ```

---

### 2. 隐私合规与 AK 鉴权

#### 2.1 隐私合规（强制）

- 在任何定位 API 调用前，必须先确保用户已阅读并同意隐私政策；
- 必须在代码中显式将隐私同意结果通知给定位 SDK：

```ts
LocationClient.setAgreePrivacy(true); // 用户明确同意后才能为 true
```

- 用户未同意或拒绝时：
  - 必须设置为 `false`；
  - 禁止继续调用任何定位接口。

#### 2.2 权限与 AbilityKit

- 使用定位 SDK 前，必须通过 `@kit.AbilityKit` 获取定位相关运行时权限，推荐统一封装权限助手（如 `LocationPermissionHelper`）：

```ts
import { abilityAccessCtrl, bundleManager, Permissions } from '@kit.AbilityKit';

const LOCATION_PERMISSIONS: Permissions[] = [
  'ohos.permission.LOCATION',
  'ohos.permission.APPROXIMATELY_LOCATION'
];
```
- 权限拒绝后的引导 — 被拒绝时引导用户去系统设置手动开启

示例代码
```ts
 promptAction.showDialog({
    title: '需要定位权限',
    message: 'xxx需要定位权限才能获取xxx的实时位置。\n\n'
      + '请前往「设置 > 应用管理 > 应用名称 > 权限」中开启位置权限。',
    buttons: [
      { text: '暂不开启', color: '#888888' },
      { text: '前往设置', color: '#0288D1' }
    ]
  }).then((result) => {
    if (result.index === 1) {
      // 跳转到应用设置页面
      // 调用封装的context.startAbility方法
    } else {
      Logger.log('SportHealthMap', 'user dismissed permission denied dialog');
    }
  }).catch((err: Error) => {
    Logger.error('SportHealthMap', `permissionDeniedDialog error: ${String(err)}`);
  });
```
- 页面上的权限状态展示 — 让用户清楚看到当前权限状态

规范要求：

- `Permissions` 类型必须从 `@kit.AbilityKit` 正确导入，禁止本地声明 `type Permissions = string`；
- 对 hvigor / ArkTS 编译期报错（如找不到 `@kit.AbilityKit` 类型声明），优先检查工程 SDK 版本与导入路径（应为 `@kit.*` 新范式）。

#### 2.3 定位 SDK 鉴权（AK 校验）

在首次使用定位能力前（通常在应用初始化阶段），调用：

```ts
LocationClient.checkAuthKey(BAIDU_MAP_AK, this.context, (result: string) => {
  console.debug('Baidu Location SDK auth result = ' + result);
});
```

规范建议：

- AK 需通过安全配置管理（如配置文件、服务端下发等），禁止直接写入公开仓库；
- 对鉴权失败结果需要有用户可感知的提示和降级处理（可通过 Toast + 状态文本），并结合 Logger 输出内部日志。

---

### 3. 权限与 appIdentifier 配置

#### 3.1 module.json5 中的定位权限

按需声明定位相关权限（根据业务选择最小集）：

```json
"requestPermissions": [
  {
    "name": "ohos.permission.LOCATION",
    "reason": "$string:permission_location_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "inuse"
    }
  },
  {
    "name": "ohos.permission.LOCATION_IN_BACKGROUND",
    "reason": "$string:permission_location_background_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "always"
    }
  },
  {
    "name": "ohos.permission.APPROXIMATELY_LOCATION",
    "reason": "$string:permission_approx_location_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "inuse"
    }
  },
  {
    "name": "ohos.permission.APP_TRACKING_CONSENT",
    "reason": "$string:permission_app_tracking_consent_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "always"
    }
  },
  {
    "name": "ohos.permission.GET_WIFI_INFO",
    "reason": "$string:permission_get_wifi_info_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "inuse"
    }
  },
  {
    "name": "ohos.permission.GET_NETWORK_INFO",
    "reason": "$string:permission_get_network_info_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "inuse"
    }
  },
  {
    "name": "ohos.permission.INTERNET",
    "reason": "$string:permission_internet_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "always"
    }
  },
  {
    "name": "ohos.permission.KEEP_BACKGROUND_RUNNING",
    "reason": "$string:permission_keep_background_running_reason",
    "usedScene": {
      "abilities": ["EntryAbility"],
      "when": "always"
    }
  }
]
```

#### 3.2 获取 appIdentifier（可选）

仅在真机环境有效，用于安全校验等场景：

```ts
public getBundleAppIdentifier() {
  let bundleFlags = bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_SIGNATURE_INFO;
  try {
    return bundleManager.getBundleInfoForSelf(bundleFlags).then((data) => {
      const appIdentifier = data.signatureInfo.appIdentifier;
      console.info('getBundleAppIdentifier successfully. Data: ' + appIdentifier);
    }).catch((error: Error) => {
      console.error('getBundleAppIdentifier failed. Cause: ' + error.message);
    });
  } catch (error) {
    console.error('getBundleAppIdentifier failed:' + (error as Error).message);
  }
}
```

规范建议：

- 只在必要时将 `appIdentifier` 上传服务端，并通过 HTTPS 传输；
- 敏感标识不在控制台日志、埋点中明文输出，上线前注意脱敏或移除。

---

### 4. 定位客户端初始化与监听模式

#### 4.1 推荐初始化顺序（强制）

使用 `LocationClient` 进行定位时，必须严格遵循以下顺序：

1. 在用户同意隐私政策后调用 `LocationClient.setAgreePrivacy(true)`；
2. 在 `EntryAbility.onCreate` 中调用 `LocationClient.checkAuthKey(...)` 完成 AK 鉴权；
3. 在页面级代码中，等待运行时权限授予后再创建 `LocationClient` 并启动定位。

示例（权限检查与启动）：

```ts
private async startLocation(): Promise<void> {
  const context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
  const granted: boolean = await PermissionHelper.checkAndRequestLocationPermissions(context);
  if (!granted) {
    // 提示用户并返回，不启动 LocationClient
    return;
  }
  // 权限已授予，安全启动定位
  this.locationClient = new LocationClient(context);
  // ... 注册监听器、配置参数、start()
}
```

> 常见错误：在地图 `onReady` 回调中直接 `new LocationClient().start()` 而未等待权限结果，导致定位在权限未授予时静默失败。

#### 4.2 监听模式

推荐做法：

- 按页面/业务生命周期管理 `LocationClient`，避免频繁 `new`；
- 使用自定义 `BDLocationListener` 统一处理定位结果，通过状态管理或事件分发传递到各页面。

示例（简化版）：

```ts
class MyLocationListener extends BDLocationListener {
  onReceiveLocation(bdLocation: BDLocation): void {
    const longitude: number = bdLocation.getLongitude();
    const latitude: number = bdLocation.getLatitude();
    const radius: number = bdLocation.getRadius();
    // TODO: 分发给 UI / 数据层，并结合 Logger + Toast 提示定位状态
  }
}
```

规范要求：

- 页面销毁或业务结束时，必须停止定位并注销监听（若 SDK 提供对应接口需调用）；
- 定位状态变化需通过 Toast + 页面状态文本反馈给用户，不得只打日志。

---

### 5. 单次定位使用规范

使用场景：

- 用户主动触发的「获取当前位置」按钮；
- 地址选择 / 打点等只需一次性坐标的场景。

基本调用模式：

```ts
singleLocation() {
  let locClient: LocationClient | null = null;
  try {
    locClient = new LocationClient(this.context);
  } catch (error) {
    return;
  }
  if (!locClient) {
    return;
  }

  const listener: MyLocationListener = new MyLocationListener();
  locClient.registerListener(listener);

  const option = new LocationClientOption();
  option.setCoorType('gcj02');
  option.setIsNeedAddress(true);
  option.setIsNeedLocationDescribe(true);
  option.setIsNeedLocationPoiList(true);
  option.setLocationMode(LocationMode.High_Accuracy);

  locClient.setLocOption(option);
  locClient.requestSingleLocation(); // 触发单次定位
}
```

规范建议：

- 对频繁点击「定位一次」的场景做防抖/节流，避免短时间内多次请求；
- 单次定位完成后可按需复用 / 释放 `LocationClient`，避免泄漏。

---

### 6. 后台持续定位规范

使用场景：

- 儿童安全守护、行程轨迹记录等需要长时间持续位置更新的业务。

前置条件：

- 已获取后台定位和长时任务权限，并在 UI 明确说明用途；
- 在 `module.json5` 的 `abilities` 配置中加入：

```json
"backgroundModes": ["location"]
```

启动后台定位示例（简化）：

```ts
const wantAgentInfo: wantAgent.WantAgentInfo = {
  wants: [
    {
      bundleName: '您的包名',
      abilityName: '您的Ability名'
    }
  ],
  operationType: wantAgent.OperationType.START_ABILITY,
  requestCode: 0,
  wantAgentFlags: [wantAgent.WantAgentFlags.UPDATE_PRESENT_FLAG]
};

wantAgent.getWantAgent(wantAgentInfo).then((wantAgentObj: WantAgent) => {
  if (this.client != null) {
    this.client.enableLocInBackground(wantAgentObj);
  }
});
```

关闭后台定位：

```ts
if (this.client != null) {
  this.client.disableLocInBackground();
}
```

规范要求：

- 后台定位必须有明确的结束条件（如守护任务结束、超时等），禁止无限期运行；
- 用户可在设置页显式关闭后台定位，并在关闭时同步调用 `disableLocInBackground`；
- 业务逻辑要对前台 / 后台状态切换进行处理（如降低频率、合并上报）。

---

### 7. 坐标系、经纬度与精度

#### 7.1 坐标系支持

- `gcj02`：国测局坐标（默认）；
- `bd09ll`：百度经纬度坐标（在百度地图上标注时推荐）；
- `bd09`：百度墨卡托坐标。

配置示例：

```ts
const option = new LocationClientOption();
option.setCoorType('bd09ll'); // 在百度地图展示时推荐
```

解析位置：

```ts
const longitude: number = bdLocation.getLongitude();
const latitude: number = bdLocation.getLatitude();
const radius: number = bdLocation.getRadius(); // 定位精度（米）
const coorType: string = bdLocation.getCoorType();
```

规范建议：

- 工程内统一约定主用坐标系（例如地图展示统一使用 `bd09ll`），避免混用；
- 对精度较大的定位结果（radius 过大）在界面和业务上做降级处理，如提示“定位不精确，请稍后重试”。

---

### 8. 地址、位置描述与周边 POI

地址信息（需显式开启）：

```ts
const option = new LocationClientOption();
option.setIsNeedAddress(true);
```

在回调中获取：

```ts
const addr: string | null = bdLocation.getAddrStr();
const country: string | null = bdLocation.getCountry();
const province: string | null = bdLocation.getProvince();
const city: string | null = bdLocation.getCity();
const district: string | null = bdLocation.getDistrict();
const street: string | null = bdLocation.getStreet();
const adcode: string | null = bdLocation.getAdCode();
const town: string | null = bdLocation.getTown();
```

位置描述（需显式开启）：

```ts
option.setIsNeedLocationDescribe(true);
const locationDescribe: string | null = bdLocation.getLocationDescribe();
```

周边 POI（需显式开启）：

```ts
option.setIsNeedLocationPoiList(true);

const poi: Poi | undefined = bdLocation.getPoiList().pop();
if (poi) {
  const poiName: string = poi.getName();
  const poiTags: string = poi.getTags();
  const poiAddr: string = poi.getAddr();
}

const poiRegion: PoiRegion | null = bdLocation.getPoiRegion();
if (poiRegion != null) {
  const poiDirectionDesc: string = poiRegion.getDirectionDesc();
  const poiRegionName: string = poiRegion.getName();
  const poiRegionTags: string = poiRegion.getTags();
}
```

规范要求：

- 各字段可能为空，业务逻辑中必须进行空值和长度判断；
- POI 列表数量可能较多，需在前端或服务端做数量 / 频率控制；
- 对 POI 类型（`tags`）可在产品层面进行归类统一展示。

---

### 9. 错误处理、性能与合规要求

- 错误处理：
  - 对 `LocationClient` 初始化失败、权限不足、定位失败、网络异常等情况，必须：
    - 使用 Logger 记录内部错误详情（`action` + `error` 对象）；
    - 使用 Toast / 状态文本给出用户可理解的错误原因和解决建议；
    - 区分「编码问题」与「环境问题」，编码问题需要修复后重新执行构建命令。
- 性能与功耗：
  - 对连续定位合理设置时间 / 距离间隔，避免高频请求导致耗电过快；
  - 后台定位需设置最大持续时长或依据业务状态自动停止。
- 安全与隐私：
  - 经纬度 / 地址 / POI 等均视为敏感信息，传输必须通过 HTTPS；
  - 日志 / 埋点中避免输出用户具体坐标，必要时做精度裁剪或模糊化；
  - 应用设置中需提供显式定位开关和后台定位开关，用户可随时撤销授权。

