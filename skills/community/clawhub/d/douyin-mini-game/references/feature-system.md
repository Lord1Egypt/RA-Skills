# 系统与生命周期

> 官方文档: 系统 API - 生命周期、系统信息、触摸事件、性能、分包、更新管理

## 生命周期

### tt.onShow(callback) / tt.onHide(callback)

```javascript
// 进入前台
tt.onShow(function(res) {
  console.log("场景值:", res.scene);
  console.log("启动参数:", res.query);
  console.log("启动来源:", res.launch_from);
  // 恢复游戏逻辑、音效等
});

// 进入后台
tt.onHide(function() {
  // 暂停游戏逻辑、音效等，释放临时资源
});

// 取消监听
tt.offShow(callback);
tt.offHide(callback);
```

### tt.getLaunchOptionsSync()

同步获取启动参数。

```javascript
var options = tt.getLaunchOptionsSync();
// options.scene - 场景值（数字）
// options.query - 启动参数对象
// options.referrerInfo - 来源信息
//   .appId - 来源小程序 appId
//   .extraData - 来源小程序传递的数据
```

### tt.restartMiniProgramSync()

重启小游戏，会触发冷启动流程。

### tt.exitMiniProgram(options)

退出小游戏。

```javascript
tt.exitMiniProgram({
  success: function() { console.log("退出成功"); }
});
```

## 系统信息

### tt.getSystemInfoSync()

```javascript
var info = tt.getSystemInfoSync();
// info.brand: 设备品牌 (如 "iPhone", "Xiaomi")
// info.model: 设备型号 (如 "iPhone 14 Pro")
// info.system: 操作系统版本 (如 "iOS 17.0")
// info.platform: 平台 ('ios' | 'android' | 'windows' | 'mac')
// info.screenWidth / info.screenHeight: 屏幕宽高 (px)
// info.windowWidth / info.windowHeight: 可使用窗口宽高
// info.pixelRatio: 设备像素比
// info.SDKVersion: 基础库版本 (如 "3.45.0")
// info.version: 抖音 App 版本
// info.language: 语言 (如 "zh_CN")
// info.statusBarHeight: 状态栏高度
// info.safeArea: { left, right, top, bottom, width, height }
// info.fontSizeSetting: 字体大小设置
// info.benchmarkLevel: 设备性能等级 (-1=未知, 1~50 低端, 51~100 高端)
```

### tt.getSystemInfo(options)

异步获取系统信息。

### tt.getEnvInfoSync()

```javascript
var env = tt.getEnvInfoSync();
// env.microapp.appId: 小游戏 appId
// env.microapp.envVersion: 'develop' | 'trial' | 'release'
```

### tt.canIUse(apiName)

判断 API/参数/返回值是否可用。

```javascript
if (tt.canIUse("tt.createWorker")) { /* 支持 Worker */ }
if (tt.canIUse("requestGamePayment.object.goodType")) { /* 支持道具直购 */ }
if (tt.canIUse("tt.setKeepScreenOn")) { /* 支持保持屏幕常亮 */ }
```

## 触摸事件

### 触摸事件 API

```javascript
// 触摸开始
tt.onTouchStart(function(event) {
  // event.touches: 当前所有触摸点
  // event.changedTouches: 变化的触摸点
  // event.timeStamp: 时间戳
  for (var i = 0; i < event.touches.length; i++) {
    var touch = event.touches[i];
    console.log(touch.identifier); // 唯一标识 (Number)
    console.log(touch.clientX, touch.clientY); // 触摸坐标
    console.log(touch.pageX, touch.pageY);     // 页面坐标
    console.log(touch.force);     // 按压力度 (仅 iOS, 0.0~1.0)
  }
});

tt.onTouchMove(function(event) { /* 触摸移动 */ });
tt.onTouchEnd(function(event) { /* 触摸结束 */ });
tt.onTouchCancel(function(event) { /* 触摸取消(来电等) */ });

// 取消监听
tt.offTouchStart(callback);
tt.offTouchMove(callback);
tt.offTouchEnd(callback);
tt.offTouchCancel(callback);
```

### Touch 对象

| 属性 | 类型 | 说明 |
|------|------|------|
| identifier | Number | 触摸点唯一标识（手指不变） |
| clientX | Number | 距离 Canvas 左侧距离 |
| clientY | Number | 距离 Canvas 顶部距离 |
| pageX/pageY | Number | 距离页面左侧/顶部距离 |
| force | Number | 按压力度（仅 iOS，0~1） |

## 性能监控

### tt.getPerformance()

获取当前游戏性能数据。

```javascript
var perf = tt.getPerformance();
// 可用于测量帧率、内存等指标
```

### tt.onMemoryWarning(callback)

监听内存告警。

```javascript
tt.onMemoryWarning(function(res) {
  // res.level: 5 (告警) | 10 (严重告警)
  if (res.level >= 10) {
    // 紧急释放非必要资源：纹理缓存、音频、对象池等
    clearTextureCache();
    clearAudioPool();
  }
});
```

### tt.triggerGC()

主动触发 JS 垃圾回收。**仅建议在开发调试时使用**，正式版不建议频繁调用。

## 更新管理 (UpdateManager)

### tt.getUpdateManager()

```javascript
var updateManager = tt.getUpdateManager();

// 检查更新
updateManager.onCheckForUpdate(function(res) {
  console.log("有新版本:", res.hasUpdate);
});

// 新版本下载完成
updateManager.onUpdateReady(function() {
  tt.showModal({
    title: "更新提示",
    content: "新版本已准备好，是否重启？",
    success: function(res) {
      if (res.confirm) updateManager.applyUpdate();
    }
  });
});

// 更新失败
updateManager.onUpdateFailed(function(err) {
  console.error("更新失败:", err);
});
```

## 分包加载

### tt.loadSubpackage(options)

```javascript
var task = tt.loadSubpackage({
  name: "stage1",
  success: function() { console.log("分包加载完成"); },
  fail: function(err) { console.error(err); }
});

// 监听进度
task.onProgressUpdate(function(res) {
  console.log("进度: " + res.progress + "%");
  console.log("已下载:", res.totalBytesWritten);
  console.log("总大小:", res.totalBytesExpectedToWrite);
});

// 中断加载
// task.abort();
```

### game.json 分包配置
```json
{
  "subPackages": [
    { "name": "stage1", "root": "stage1/" },
    { "name": "stage2", "root": "stage2/" }
  ]
}
```

## 全局错误

### tt.onError(callback)

```javascript
tt.onError(function(error) {
  console.error("全局错误:", error.message);
  console.error("错误堆栈:", error.stack);
});
```

## 调试

```javascript
// 日志管理器（写入文件）
var logger = tt.getLogManager();
logger.log("普通日志");
logger.info("信息日志");
logger.warn("警告日志");
logger.debug("调试日志");

// 实时日志管理器（上传到后台）
var rtLogger = tt.getRealtimeLogManager();
rtLogger.info("实时信息");
rtLogger.warn("实时警告");
rtLogger.error("实时错误");
rtLogger.setFilterMsg("keyword"); // 添加过滤关键词
```

## 键盘事件（PC 端）

```javascript
tt.onKeyDown(function(event) {
  // event.key: 按键值 (如 "a", "ArrowLeft")
  // event.code: 物理键位 (如 "KeyA", "ArrowLeft")
  // event.repeat: 是否为长按重复
  // event.keyCode: 键码
});
tt.onKeyUp(function(event) { /* ... */ });
tt.offKeyDown(callback);
tt.offKeyUp(callback);
```

## 滚轮事件（PC 端）

```javascript
tt.onWheel(function(event) {
  console.log(event.deltaX, event.deltaY); // 滚轮滚动量
});
tt.offWheel(callback);
```
