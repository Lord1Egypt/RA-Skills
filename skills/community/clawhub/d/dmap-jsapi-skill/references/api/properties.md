

# Properties - 全局属性和工具函数

dmapgl命名空间下的全局属性、工具函数和浏览器检测。

## 后台服务地址

指定后台服务地址。

### 设置

```javascript
// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';
```


## version - 版本号

获取DMap GL的版本号。

```javascript
console.log('DMap GL版本:', dmapgl.version);
// 例如: "1.0.0"
```

## supported - 浏览器支持检测

检测浏览器是否支持DMap GL。

### 基本检测

```javascript
if (!dmapgl.supported()) {
  alert('您的浏览器不支持DMap GL');
}
```

### 详细检测

```javascript
const support = dmapgl.supported({ failIfMajorPerformanceCaveat: true });

if (!support) {
  console.error('浏览器不支持WebGL或性能不足');
}
```

### 配置选项

```javascript
dmapgl.supported({
  failIfMajorPerformanceCaveat: false  // 默认false
});
```

## getRTLTextPlugin - 获取RTL文本插件

获取从右到左文本渲染插件的状态。

```javascript
const pluginUrl = dmapgl.getRTLTextPlugin();
console.log('RTL插件URL:', pluginUrl);
```

## setRTLTextPlugin - 设置RTL文本插件

设置从右到左文本（阿拉伯语、希伯来语等）渲染插件。

### 配置

```javascript
dmapgl.setRTLTextPlugin(
  'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.3/mapbox-gl-rtl-text.js',
  (error) => {
    if (error) {
      console.error('RTL插件加载失败:', error);
    } else {
      console.log('RTL插件加载成功');
    }
  },
  false  // lazy加载
);
```

### 参数说明

- **url**: 插件URL
- **callback**: 加载完成回调
- **lazy**: 是否延迟加载（默认false）


## clearStorage - 清除浏览器存储

清除库使用的浏览器存储,包括瓦片缓存。

```javascript
dmapgl.clearStorage((error) => {
  if (error) {
    console.error('清除存储失败:', error);
  } else {
    console.log('存储已清除');
  }
});
```

**注意**: 仅在支持 Cache API 的浏览器中可用(需要HTTPS)。

## clearPrewarmedResources - 清除预热资源

清除由 prewarm() 创建的资源。

```javascript
// 通常在不需要再使用地图时调用
dmapgl.clearPrewarmedResources();
```

## config - 全局配置

配置全局选项。

```javascript
dmapgl.config = {
  API_URL: 'https://api.dmap.com',
  MAX_PARALLEL_IMAGE_REQUESTS: 16
};
```

## WorkerCount - Worker数量

设置Web Worker数量。

```javascript
// 默认值为navigator.hardwareConcurrency或2
console.log('Worker数量:', dmapgl.workerCount);

// 自定义（必须在创建Map之前设置）
dmapgl.workerCount = 4;
```

## AnimationOptions - 动画选项

控制地图动画的通用选项。

### 属性

- `animate` - 是否启用动画 (默认 true)
- `duration` - 动画持续时间(毫秒)
- `easing` - 缓动函数
- `essential` - 是否为必要动画(不受 prefers-reduced-motion 影响)
- `curve` - 缩放曲线值
- `speed` - 平均速度
- `screenSpeed` - 屏幕速度
- `minZoom` - 最小缩放级别
- `maxDuration` - 最大持续时间
- `offset` - 目标中心偏移量
- `preloadOnly` - 仅预加载瓦片

### 示例

```javascript
map.flyTo({
  center: [800000, 600000],
  zoom: 14,
  duration: 5000,
  essential: true,
  curve: 1.42
});
```

## CameraOptions - 相机选项

控制相机位置、缩放、旋转和俯仰的选项。

### 属性

- `center` - 中心点坐标
- `zoom` - 缩放级别
- `bearing` - 旋转角度
- `pitch` - 俯仰角
- `padding` - 填充选项
- `around` - 变换原点
- `retainPadding` - 是否保留填充 (默认 true)

### 示例

```javascript
// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';
var map = new dmapgl.Map({
  container: 'map',
  style: dmapgl.serviceUrl + '/map/vector/standard/styles/style.json',
  center: [800000, 600000],
  pitch: 60,
  bearing: -60,
  zoom: 11
});
```

## CustomLayerInterface - 自定义图层接口

自定义样式图层的接口规范。

### 属性

- `id` - 唯一图层ID
- `type` - 类型 (必须为 "custom")
- `renderingMode` - 渲染模式 ("2d" 或 "3d")
- `wrapTileId` - 是否包装瓦片ID

### 必需方法

- `render(gl, matrix)` - 渲染方法
- `prerender(gl, matrix)` - 预渲染方法(可选)
- `onAdd(map, gl)` - 添加时调用(可选)
- `onRemove()` - 移除时调用(可选)

## 工具函数

### LngLat转换

```javascript
// 转换为LngLat对象
const coord = dmapgl.LngLat.convert([800000, 600000]);
console.log(coord.lng, coord.lat);
```

### LngLatBounds转换

```javascript
// 转换为边界对象
const bounds = dmapgl.LngLatBounds.convert([
  [716638.24, 548483.59],
  [894455.08, 728066.47]
]);
```

### Point转换

```javascript
// 创建Point对象
const point = new dmapgl.Point(100, 200);
```

## 浏览器检测

### Browser对象

```javascript
// 检测浏览器特性
console.log('支持WebGL:', dmapgl.browser.webglSupported);
console.log('支持触控:', dmapgl.browser.touchSupport);
console.log('设备像素比:', dmapgl.browser.devicePixelRatio);
```

## 实用示例

### 完整的初始化检查

```javascript
function initializeMap() {
  // 1. 检查浏览器支持
  if (!dmapgl.supported()) {
    showError('您的浏览器不支持DMap GL');
    return;
  }
  
  // 2. 指定后台服务地址
  dmapgl.serviceUrl = 'http://172.26.64.84/api';

  
  // 3. 创建地图
  var map = new dmapgl.Map({
    container: 'map',
    style: dmapgl.serviceUrl + '/map/vector/standard/styles/style.json',
    center: [800000, 600000],
    zoom: 11
  });
  
  return map;
}
```

### 清除缓存刷新

```javascript
function refreshMap() {
  dmapgl.clearData((error) => {
    if (error) {
      console.error('清除缓存失败:', error);
      return;
    }
    
    // 重新加载页面
    window.location.reload();
  });
}
```

### 环境检测

```javascript
function detectEnvironment() {
  const env = {
    supported: dmapgl.supported(),
    version: dmapgl.version,
    webgl: dmapgl.browser.webglSupported,
    touch: dmapgl.browser.touchSupport,
    pixelRatio: dmapgl.browser.devicePixelRatio,
    workers: dmapgl.workerCount
  };
  
  console.log('环境信息:', env);
  return env;
}

detectEnvironment();
```

## 注意事项

1. **后台服务地址**: 请确保后台服务地址正确
2. **supported**: 在创建Map前检查浏览器支持
3. **clearData**: 清除操作不可逆
4. **RTL插件**: 仅在需要时加载
5. **Worker数量**: 根据设备性能调整
6. **版本兼容**: 注意API版本变化
