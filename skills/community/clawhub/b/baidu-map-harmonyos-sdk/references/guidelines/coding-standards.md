## Baidu Map HarmonyOS SDK 代码规范

本文件补充 `SKILL.md` 中的「强制要求」部分，对日志、注释、模块化以及图片资源使用做出更细致的约定。

### 1. 日志输出规范（Logger）

- **统一入口**
  - 必须使用统一的 `Logger` 工具类封装原生 `console`。
  - 第一个参数固定使用场景名：`"SportHealthMap"`。
  - 第二个参数统一使用 `string | object`，推荐直接传入对象，由 `Logger` 负责 JSON 序列化。
- **禁止行为**
  - 禁止在业务代码中直接调用 `console.info / console.error / console.warn / console.debug`。
  - 禁止输出包含敏感信息（如完整经纬度、appIdentifier 等）的明文日志，上线前需脱敏。

示例（推荐写法）：

```ts
// ✅ 推荐：统一使用 Logger，输出结构化 JSON
Logger.info('SportHealthMap', {
  action: 'mapReady',
  mapType: 'normal',
  sdkVersion: '2.0.3'
});

// ❌ 禁止：直接使用 console
console.info('map ready');
```

> 提示：在回答中给出示例代码时，同样应遵守以上规范，避免出现直接使用 `console` 的示例。

### 2. 代码注释规范

- **必须注释的内容**
  - 关键业务方法（例如初始化 SDK、发起路线规划、创建地图覆盖物）。
  - 非直观的参数或返回值含义。
  - 对性能、内存或安全有重要影响的逻辑。
- **注释风格**
  - 使用简洁的中文说明，必要时补充英文术语。
  - 避免无意义注释（如 `// 调用接口`）。
  - 建议使用 JSDoc/TS 注释格式，让 IDE 能展示提示。

示例：

```ts
/**
 * 初始化百度地图 SDK。
 * @param context Ability 上下文，用于创建 MapComponent 和 LocationClient。
 * @param ak 百度地图开放平台申请到的 AK，不应硬编码在代码中。
 */
initBaiduMapSdk(context: common.UIAbilityContext, ak: string): void {
  // ...
}
```

### 3. 模块化规范

- **必须模块化的内容**
  - 通用工具类：如 Logger、权限助手、坐标转换工具等。
  - 可复用的 UI 组件：如轨迹回放控制条、地图状态面板等。
  - 与具体页面解耦的业务能力：如路线规划服务、定位服务封装等。
- **禁止行为**
  - 禁止在页面组件内部内联定义通用类（如在单个页面里定义 `class Logger` 或大段工具方法）。
  - 禁止在多个页面拷贝粘贴相同逻辑而不抽取公共模块。

建议结构示例：

```text
entry/src/main/ets/
  common/
    Logger.ts
    PermissionHelper.ts
    CoordinateUtil.ts
  service/
    RoutePlanService.ts
    LocationService.ts
  feature/
    track/
      TrackPlayer.ts
```

### 4. 图片资源使用规范

本 Skill 提供了一套约定好的图片资源，位于仓库内 `references/assets.md` 与 `references/assets/images/` 目录，用于轨迹、路况、起终点等常见场景。

- **命名与用途约定**
  - 轨迹小车优先使用：`track_car@2x.png` / `track_car@3x.png`。
  - 路况线条优先使用：`traffic_texture_*` 系列纹理。
  - 起点终点图标：`icon_start@*x.png` / `icon_end@*x.png`。
  - 当前位置：`location@*x.png`。
- **拷贝与引用要求（强制）**
  - 需要将本仓库的图片文件**主动拷贝**到当前 HarmonyOS 工程的模块资源目录：
    - 通用示例：`entry/src/main/resources/rawfile/`
    - 或业务模块下：`<module>/src/main/resources/rawfile/`
  - 在代码中通过 `rawfile://` 形式引用，例如：

```ts
// 将 track_car@2x.png 拷贝到 resources/rawfile/ 后
const carImage = new ImageEntity('rawfile://track_car@2x.png');
```

- **回答时的提醒要求**
  - 当示例代码中使用到图片时，必须在文字说明中提醒：
    - 需要从本仓库的 `assets/images/` 目录**主动拷贝**到工程的 `resources/rawfile/`。
    - 若未拷贝，运行时地图覆盖物会因为找不到资源而不显示或报错。

