

# 地图初始化与生命周期

> **坐标系说明**: DMap 使用地方平面坐标系，中心点为 `[800000, 600000]`，地图范围为 `[716638.24, 548483.59, 894455.08, 728066.47]`，缩放级别范围为 `7-19`。

## Map 构造函数

创建一个新的 DMap GL 地图实例。

```javascript
var map = new dmapgl.Map(options);
```

### 完整参数

| 参数 | 类型                                | 默认值 | 说明 |
|------|-----------------------------------|--------|------|
| antialias | `boolean`                         | `false` | 是否启用MSAA抗锯齿。默认为false以优化性能 |
| attributionControl | `boolean`                         | `true` | 是否添加归属控件(AttributionControl) |
| bearing | `number`                          | `0` | 初始方位角(旋转角度),从北方逆时针测量(度)。如果未在选项中指定,将从样式对象中查找 |
| bearingSnap | `number`                          | `7` | 方位角吸附阈值(度)。当旋转到北方7度范围内时,地图会自动吸附到正北 |
| bounds | `LngLatBoundsLike`                | `null` | 初始边界。如果指定,将覆盖 center 和 zoom 选项 |
| boxZoom | `boolean`                         | `true` | 是否启用"框选缩放"交互(BoxZoomHandler) |
| center | `LngLatLike`                      | `[0, 0]` | 初始地理中心点 [经度, 纬度]。注意:DMap使用地方平面坐标系 |
| clickTolerance | `number`                          | `3` | 点击期间鼠标可移动的最大像素数,超过则视为拖拽而非点击 |
| collectResourceTiming | `boolean`                         | `false` | 是否收集GeoJSON和矢量瓦片Web Worker的资源时序API信息 |
| config | `Object`                          | `null` | 样式片段的初始配置选项。每个键是片段ID(如 basemap),值是配置对象 |
| container | `HTMLElement / string`            | - | **必需**。HTML容器元素或其字符串ID。指定元素必须无子元素 |
| cooperativeGestures | `boolean`                         | - | 协作手势模式。启用后,滚轮缩放需按住Ctrl/⌘键,触摸平移需双指,触摸俯仰需三指 |
| crossSourceCollisions | `boolean`                         | `true` | 多源符号是否相互碰撞检测。false则各源独立进行碰撞检测 |
| customAttribution | `string / Array<string>`          | `null` | 在归属控件中显示的自定义文本。仅在 attributionControl 为 true 时有效 |
| doubleClickZoom | `boolean`                         | `true` | 是否启用"双击缩放"交互(DoubleClickZoomHandler) |
| dragPan | `boolean / Object`                | `true` | 是否启用"拖拽平移"交互。可传入对象作为 DragPanHandler#enable 的选项 |
| dragRotate | `boolean`                         | `true` | 是否启用"拖拽旋转"交互(DragRotateHandler) |
| fadeDuration | `number`                          | `300` | 标签碰撞淡入/淡出动画持续时间(毫秒)。影响所有符号图层 |
| failIfMajorPerformanceCaveat | `boolean`                         | `false` | 如果性能远低于预期(使用软件渲染),是否让地图创建失败 |
| fitBoundsOptions | `Object`                          | `null` | 仅在适配初始 bounds 时使用的 Map#fitBounds 选项对象 |
| hash | `boolean / string`                | `false` | 是否将地图位置(zoom、center、bearing、pitch)与URL哈希同步。可传入字符串作为自定义参数名 |
| interactive | `boolean`                         | `true` | 是否响应交互。false则不附加任何鼠标、触摸或键盘监听器 |
| keyboard | `boolean`                         | `true` | 是否启用键盘快捷键(KeyboardHandler) |
| language | `"auto" / string / Array<string>` | `null` | BCP 47语言标签,用于地图标签和UI组件。设为 "auto" 时使用浏览器语言 |
| locale | `Object`                          | `null` | UI字符串本地化补丁。映射命名空间UI字符串ID到目标语言的翻译 |
| localFontFamily | `string`                          | `null` | CSS字体族,用于本地覆盖所有字形生成。设置后将忽略样式中的字体设置(除字重外) |
| localIdeographFontFamily | `string`                          | `'sans-serif'` | CSS字体族,用于本地覆盖CJK统一表意文字等范围的字形。设为 false 以使用样式中的字体设置 |
| logoPosition | `string`                          | `'bottom-left'` | 标识位置。可选: `top-left`、`top-right`、`bottom-left`、`bottom-right` |
| maxBounds | `LngLatBoundsLike`                | `null` | 地图约束边界。设置后地图将被限制在此范围内 |
| maxPitch | `number`                          | `85` | 最大俯仰角(0-85度) |
| maxTileCacheSize | `number`                          | `null` | 每个源的最大瓦片缓存数量。省略则根据视口动态调整 |
| maxZoom | `number`                          | `22` | 最大缩放级别(0-24) |
| minPitch | `number`                          | `0` | 最小俯仰角(0-85度) |
| minTileCacheSize | `number`                          | `null` | 每个源的最小瓦片缓存数量。省略则根据视口动态调整 |
| minZoom | `number`                          | `0` | 最小缩放级别(0-24) |
| performanceMetricsCollection | `boolean`                         | `true` | 是否收集和发送性能指标 |
| pitch | `number`                          | `0` | 初始俯仰角(倾斜角),距屏幕平面的角度(0-85度)。如果未指定,将从样式对象中查找 |
| pitchWithRotate | `boolean`                         | `true` | 俯仰是否与旋转联动。false则禁用两指旋转时的俯仰控制 |
| preserveDrawingBuffer | `boolean`                         | `false` | 是否保留绘图缓冲区。true时可使用 canvas.toDataURL() 导出PNG。默认为false以优化性能 |
| refreshExpiredTiles | `boolean`                         | `true` | 是否刷新过期的瓦片 |
| renderWorldCopies | `boolean`                         | `true` | 是否渲染世界副本(横向重复)。false则只显示一个世界 |
| scrollZoom | `boolean / Object`                | `true` | 是否启用"滚轮缩放"交互。可传入对象作为 ScrollZoomHandler#enable 的选项 |
| style | `string / Object`                 | - | **必需**。地图样式URL或样式对象 |
| touchPitch | `boolean / Object`                | `true` | 是否启用"触摸俯仰"交互。可传入对象作为 TouchPitchHandler#enable 的选项 |
| touchZoomRotate | `boolean / Object`                | `true` | 是否启用"触摸缩放旋转"交互。可传入对象作为 TouchZoomRotateHandler#enable 的选项 |
| trackResize | `boolean`                         | `true` | 是否跟踪容器尺寸变化并自动调整地图大小 |
| transformRequest | `Function`                        | `null` | 请求转换函数。可在发送请求前修改URL、headers等。签名: `(url: string, resourceType: string) => RequestParameters` |

### 示例

```javascript
// 基础初始化
// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';
var map = new dmapgl.Map({
  container: 'map',
  style: dmapgl.serviceUrl + '/map/vector/standard/styles/style.json',
  center: [800000, 600000], // 地方平面坐标
  zoom: 11,
  minZoom: 7,
  maxZoom: 19,
  maxBounds: [
    [716638.2414098255, 548483.5939021005],
    [894455.0756895209, 728066.4667000007]
  ]
});

// 高级配置
var map = new dmapgl.Map({
  container: 'map',
  style: dmapgl.serviceUrl + '/map/vector/standard/styles/style.json',
  center: [800000, 600000],
  zoom: 13,
  pitch: 60,
  bearing: -17.6,
  antialias: true,
  minZoom: 7,
  maxZoom: 19
});
```

## 地图事件

### load

地图样式加载完成时触发。

```javascript
map.on('load', () => {
  console.log('地图加载完成');
  // 在此添加图层、数据源等
});
```

### render

地图渲染帧时触发(高频)。

```javascript
map.on('render', () => {
  // 用于动画或持续更新
});
```

### error

发生错误时触发。

```javascript
map.on('error', (e) => {
  console.error('地图错误:', e.error);
});
```

## 地图销毁

组件卸载时必须调用,释放WebGL资源。

```javascript
// 方法1: remove() - 移除地图并清理
map.remove();

// 方法2: destroy() - 仅清理内部状态
map.destroy();
```

## 等待地图就绪

### 使用 load 事件

```javascript
map.on('load', () => {
  // 安全地添加图层和数据源
  map.addSource('points', {
    type: 'geojson',
    data: features
  });
});
```

### 检查 loaded 状态

```javascript
if (map.loaded()) {
  // 地图已完全加载
  map.addLayer({ /* ... */ });
} else {
  map.on('load', () => {
    map.addLayer({ /* ... */ });
  });
}
```

## 样式切换

动态切换地图样式。

```javascript
// 切换样式
map.setStyle('zyzx://vector/black/styles/style.json');

// 监听样式加载完成
map.on('style.load', () => {
  console.log('新样式加载完成');
  // 重新添加自定义图层
});
```

## 完整示例

```javascript

// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';

// 创建地图
var map = new dmapgl.Map({
  container: 'map-container',
  style: dmapgl.serviceUrl + '/map/vector/standard/styles/style.json',
  center: [800000, 600000],
  zoom: 11,
  pitch: 45,
  minZoom: 7,
  maxZoom: 19,
  antialias: true
});

// 等待加载
map.on('load', () => {
  console.log('地图就绪');
  
  // 添加控件
  map.addControl(new dmapgl.NavigationControl());
  map.addControl(new dmapgl.ScaleControl());
});

// 错误处理
map.on('error', (e) => {
  console.error('地图错误:', e.error);
});

// 清理函数
function cleanup() {
  map.remove();
}
```

## 注意事项

1. **容器要求**: 容器元素必须存在且无子元素
2. **CSS尺寸**: 确保容器有明确的宽高
3. **异步加载**: 所有图层操作应在 `load` 事件后进行
4. **资源清理**: 务必在组件销毁时调用 `remove()`
