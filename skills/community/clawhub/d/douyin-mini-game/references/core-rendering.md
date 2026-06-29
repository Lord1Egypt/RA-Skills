# 渲染系统

> 官方文档: 渲染 API - Canvas、图片、字体、帧率、WebAssembly、资源压缩

## Canvas 画布

### tt.createCanvas()

> 基础库 1.0.0+，同步方法

创建 Canvas 对象。**首次调用获取上屏 Canvas**，该 Canvas 已显示在屏幕上且与屏幕等宽等高。小游戏运行期间**有且仅有 1 个**上屏 Canvas。

```javascript
var canvas = tt.createCanvas();
console.log(canvas.width, canvas.height); // 屏幕宽高
```

### Canvas.getContext(contextType)

> 基础库 1.0.0+

```javascript
var ctx = canvas.getContext("2d");   // 2D 渲染上下文
var gl = canvas.getContext("webgl"); // WebGL 渲染上下文
```

### Canvas.toTempFilePath(options)

将 Canvas 内容导出为临时图片文件。

```javascript
canvas.toTempFilePath({
  x: 0, y: 0,
  width: 200, height: 200,
  destWidth: 400, destHeight: 400, // 输出尺寸（可缩放）
  fileType: "png",                  // png | jpg
  quality: 1,                       // jpg 质量 (0-1)
  success: function(res) {
    console.log(res.tempFilePath);   // 临时文件路径
  }
});
```

### Canvas.toTempFilePathSync(options)

> 基础库 2.82.0+，同步版本

### Canvas.requestFocus()

> 基础库 3.16.0+

使 Canvas 获取焦点，用于键盘事件接收。

## 图片

### tt.createImage()

> 基础库 1.31.0+，同步方法

```javascript
var img = tt.createImage();

// 支持多种 src 格式：网络地址、本地 ttfile://、base64、ArrayBuffer
img.src = "assets/character.png";

// 方式 1: onload/onerror
img.onload = function() {
  console.log("图片宽高:", img.width, img.height);
  ctx.drawImage(img, 0, 0);
};
img.onerror = function(err) { console.error("加载失败", err); };

// 方式 2: addEventListener
img.addEventListener("load", function(e) {
  console.log("加载成功, width:", e.target.width);
});
img.addEventListener("error", function(e) {
  console.error("加载失败:", e);
});
```

### Image 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| src | String/ArrayBuffer | 图片源（URL / base64 / ArrayBuffer） |
| width | Number | 图片真实宽度（加载完成后） |
| height | Number | 图片真实高度（加载完成后） |
| onload | Function | 加载成功回调 |
| onerror | Function | 加载失败回调 |

### 注意事项
1. 通过 `tt.createImage()` 直接显示**不需要配置图片白名单**
2. 开放数据域中只能显示与 `tt.getUserInfo()` 返回的 avatarUrl 同主机的图片
3. 使用游戏引擎时，部分引擎需要先下载图片（需配置白名单），可通过改写引擎图片能力解决

**Cocos Creator 适配示例** (避免白名单配置):
```javascript
// 注册自定义图片加载器
cc.assetManager.downloader.register(".head", (url, options, onComplete) => {
  onComplete(null, url);
});
cc.assetManager.parser.register(".head", (url, options, onComplete) => {
  var img = new Image();
  img.onload = () => onComplete(null, img);
  img.src = url;
});
```

## 2D 渲染

```javascript
var ctx = canvas.getContext("2d");

// 矩形
ctx.fillStyle = "#ff00ff";
ctx.fillRect(0, 0, 100, 100);
ctx.strokeStyle = "#000000";
ctx.strokeRect(10, 10, 80, 80);

// 文本
ctx.font = "20px Arial";
ctx.fillStyle = "#000";
ctx.fillText("Hello 抖音小游戏", 10, 50);

// 图片绘制
var img = tt.createImage();
img.src = "assets/sprite.png";
img.onload = function() {
  ctx.drawImage(img, 0, 0);
  ctx.drawImage(img, 16, 0, 16, 16, 100, 100, 32, 32); // 裁剪绘制
};

// 变换
ctx.save();
ctx.translate(150, 150);
ctx.rotate(Math.PI / 4);
ctx.fillRect(-50, -50, 100, 100);
ctx.restore();
```

## 字体

### tt.loadFont(options)

> 基础库 2.0.0+

```javascript
tt.loadFont({
  family: "MyCustomFont",        // 自定义字体名称
  source: "assets/font.ttf",     // 字体文件路径（支持 ttf/otf/woff）
  desc: { style: "normal", weight: "normal" },
  success: function() {
    ctx.font = "20px MyCustomFont";
    ctx.fillText("自定义字体", 10, 50);
  },
  fail: function(err) { console.error("字体加载失败", err); }
});
```

## 帧率控制

### tt.setPreferredFramesPerSecond(fps)

> 基础库 1.0.0+

设置游戏期望帧率。实际帧率受设备性能和屏幕刷新率限制。

```javascript
tt.setPreferredFramesPerSecond(60); // 期望 60fps
```

### requestAnimationFrame(callback) / cancelAnimationFrame(id)

```javascript
function gameLoop(timestamp) {
  // timestamp: DOMHighResTimeStamp
  updateLogic();
  render();
  requestAnimationFrame(gameLoop);
}
requestAnimationFrame(gameLoop);
```

## WebAssembly

> 基础库 ≥ 3.7.0.0，JS 线程和 Worker 线程均支持

### TTWebAssembly.compile(path)

```javascript
TTWebAssembly.compile("assets/module.wasm.br")
  .then(function(module) { /* TTWebAssembly.Module */ });
```

### TTWebAssembly.instantiate(path, importObject)

```javascript
var mem = new TTWebAssembly.Memory({ initial: 256 });
TTWebAssembly.instantiate("assets/module.wasm.br", {
  env: { memory: mem, table: new TTWebAssembly.Table({ initial: 0, element: "anyfunc" }) }
}).then(function(result) {
  result.instance.exports.main();
});
```

### 核心类

| 类 | 说明 |
|---|------|
| TTWebAssembly.Module | 编译后模块 |
| TTWebAssembly.Instance | 模块实例 |
| TTWebAssembly.Memory | 共享内存 |
| TTWebAssembly.Table | 动态链接表 |
| TTWebAssembly.Global | 全局变量传递 |

**限制**: iOS 不支持 SIMD 特性；仅支持 brotli 压缩（`*.wasm.br`）

## 资源压缩

### tt.inflate(options)

解压 deflate 压缩的数据。

```javascript
tt.inflate({
  data: compressedBuffer, // ArrayBuffer
  success: function(res) { console.log("解压后:", res.data); }
});
```

### tt.createBuffer(size)

创建 Buffer 对象。

```javascript
var buffer = tt.createBuffer(4096);
```

## 鼠标/指针样式（PC 端）

```javascript
tt.setCursor({ value: "pointer" });
// 值: default | pointer | text | crosshair | move | not-allowed | grab | ...
tt.requestPointerLock();    // 锁定指针
tt.exitPointerLock();       // 退出锁定
tt.isPointerLocked();       // 是否已锁定
```
