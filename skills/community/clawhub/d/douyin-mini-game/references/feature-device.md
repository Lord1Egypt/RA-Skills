# 设备能力

> 官方文档: 设备 API - 加速度计、陀螺仪、罗盘、振动、扫码、网络状态、屏幕、剪贴板、键盘

## 加速度计

```javascript
// 采样间隔: game(20ms) | ui(60ms) | normal(200ms)
tt.startAccelerometer({ interval: "game" });

tt.onAccelerometerChange(function(res) {
  console.log("x:", res.x, "y:", res.y, "z:", res.z);
  // 单位: m/s², 范围: [-10, 10]
});

tt.stopAccelerometer();
tt.offAccelerometerChange(callback);
```

## 陀螺仪

```javascript
tt.startGyroscope({ interval: "game" });

tt.onGyroscopeChange(function(res) {
  console.log("pitch:", res.x, "roll:", res.y, "yaw:", res.z);
  // 单位: rad/s
});

tt.stopGyroscope();
tt.offGyroscopeChange(callback);
```

## 罗盘

```javascript
tt.startCompass();
tt.onCompassChange(function(res) {
  console.log("方向:", res.direction, "°"); // 0-360, 0=正北
  console.log("精度:", res.accuracy);       // high | medium | low
});
tt.stopCompass();
tt.offCompassChange(callback);
```

## 设备方向

```javascript
tt.startDeviceMotionListening({ interval: "game" });
tt.onDeviceMotionChange(function(res) {
  // res.alpha, res.beta, res.gamma (角度值)
});
tt.stopDeviceMotionListening();
tt.offDeviceMotionChange(callback);
```

## 振动

```javascript
// 短振动 (约 15ms)
tt.vibrateShort({ success: function() {} });
// 长振动 (约 400ms)
tt.vibrateLong({ success: function() {} });
```

## 扫码

```javascript
tt.scanCode({
  onlyFromCamera: false,  // 是否仅允许相机扫码
  scanType: ["qrCode"],   // 扫码类型过滤
  success: function(res) {
    console.log("结果:", res.result);   // 扫码内容
    console.log("类型:", res.scanType); // QR_CODE, AZTEC, CODABAR, CODE_39, CODE_93, CODE_128, DATA_MATRIX, EAN_8, EAN_13, ITF, MAXICODE, PDF_417, RSS_14, RSS_EXPANDED, UPC_A, UPC_E, UPC_EAN_EXTENSION, WX_CODE, CODE_25
    console.log("字符集:", res.charSet);
    console.log("原始数据:", res.rawData);
  },
  fail: function(err) { console.error("扫码失败:", err); }
});
```

## 网络状态

```javascript
// 获取当前网络类型
tt.getNetworkType({
  success: function(res) {
    console.log("网络类型:", res.networkType);
    // wifi | 2g | 3g | 4g | 5g | unknown | none
    console.log("信号强度:", res.signalStrength); // 0~100
    console.log("是否有网络:", res.hasSystemProxy);
  }
});

// 监听网络变化
tt.onNetworkStatusChange(function(res) {
  console.log("变化类型:", res.networkType);
  console.log("是否连接:", res.isConnected);
  // 根据网络状态调整游戏行为（如加载低清资源）
});
tt.offNetworkStatusChange(callback);
```

## 屏幕控制

```javascript
// 保持屏幕常亮
tt.setKeepScreenOn({
  keepScreenOn: true,
  success: function() { console.log("已设置常亮"); }
});

// 获取屏幕亮度 (0-1)
tt.getScreenBrightness({
  success: function(res) { console.log("亮度:", res.value); }
});

// 设置屏幕亮度 (0-1)
tt.setScreenBrightness({
  value: 0.8,
  success: function() { console.log("设置成功"); }
});
```

## 剪贴板

```javascript
tt.getClipboardData({
  success: function(res) { console.log("剪贴板:", res.data); }
});

tt.setClipboardData({
  data: "要复制的内容",
  success: function() { console.log("设置成功"); }
});
```

## 键盘（PC 端）

```javascript
tt.onKeyDown(function(event) {
  // event.key: 按键值 ("a", "Enter", "ArrowLeft")
  // event.code: 物理键位 ("KeyA", "Enter", "ArrowLeft")
  // event.keyCode: 键码 (65)
  // event.ctrlKey/altKey/shiftKey/metaKey: 修饰键状态
  // event.repeat: 是否为长按重复
});
tt.onKeyUp(function(event) { console.log(event.key, "释放"); });
tt.offKeyDown(callback);
tt.offKeyUp(callback);
```

## 滚轮（PC 端）

```javascript
tt.onWheel(function(event) {
  console.log("水平:", event.deltaX, "垂直:", event.deltaY);
  // deltaX/deltaY > 0 表示向右/下滚动
});
tt.offWheel(callback);
```

## 日历

```javascript
tt.addPhoneCalendar({
  title: "游戏活动提醒",
  startTime: Date.now() + 3600000,   // 开始时间（毫秒时间戳）
  allDay: false,                      // 是否全天事件
  description: "记得参加活动！",
  alarm: true,                        // 是否提醒
  alarmOffset: 600,                   // 提醒提前量（秒）
  success: function() { console.log("日历事件添加成功"); },
  fail: function(err) { console.error("添加失败:", err); }
});
```

## 位置

```javascript
// 获取当前位置
tt.getLocation({
  type: "wgs84", // wgs84 (GPS) | gcj02 (国测局坐标)
  altitude: true, // 是否需要海拔
  success: function(res) {
    console.log("纬度:", res.latitude);
    console.log("经度:", res.longitude);
    console.log("速度:", res.speed);
    console.log("精度:", res.accuracy);
    console.log("海拔:", res.altitude);
  }
});

// 打开地图
tt.openLocation({
  latitude: 39.9042,
  longitude: 116.3974,
  scale: 15,        // 缩放级别 (5-18)
  name: "目的地名称",
  address: "详细地址"
});
```
