---
name: douyin-mini-game
description: Comprehensive skill reference for Douyin (TikTok China) mini-game development framework. Covers frontend JavaScript APIs, framework config (game.json), Canvas rendering, device capabilities, open-platform features (login/payment/ads), and all `tt.*` APIs. Use when developing, debugging, or asking questions about Douyin mini-games — especially when working with tt.createCanvas, game.json, tt.request, touch events, open data domain, tt.login, tt.requestGamePayment, tt.createRewardedVideoAd, Worker, WebSocket, or any tt.* API.
---

> 基于抖音小游戏官方文档生成，生成时间 2026-06-24
> 官方文档: https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/

抖音小游戏是基于 JavaScript 的开放平台游戏框架，运行在抖音 App 内置的 JavaScript VM 中。无 BOM/DOM，仅通过 `tt` 全局对象提供全部平台 API。支持 Canvas 2D/WebGL 渲染、WebAssembly、多线程 Worker、开放数据域等能力。

## 核心框架

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 核心框架 | 项目结构、game.json 完整配置、运行时环境、模块化(require/module/exports)、场景值、Adapter适配、包体积限制 | [core-framework](references/core-framework.md) |
| 渲染系统 | Canvas 创建与 2D/WebGL 上下文、图片(tt.createImage)、字体(tt.loadFont)、帧率控制(requestAnimationFrame)、WebAssembly(TTWebAssembly)、资源压缩 | [core-rendering](references/core-rendering.md) |

## 功能 API

### 平台能力

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 系统与生命周期 | 生命周期(tt.onShow/onHide)、系统信息(tt.getSystemInfoSync)、触摸事件(Touch/touches)、性能监控(tt.onMemoryWarning)、分包加载(tt.loadSubpackage)、更新管理(UpdateManager)、调试日志 | [feature-system](references/feature-system.md) |
| 网络通信 | HTTP 请求(tt.request)、文件上传(tt.uploadFile)/下载(tt.downloadFile)、WebSocket(tt.connectSocket/SocketTask)、全局超时配置 | [feature-network](references/feature-network.md) |
| 存储与文件 | 本地存储(tt.setStorage/tt.getStorage/10MB上限)、文件系统管理(FileSystemManager)、目录操作、临时文件持久化 | [feature-storage](references/feature-storage.md) |
| 设备能力 | 加速度计、陀螺仪、罗盘、设备方向、振动、扫码、网络状态、屏幕亮度、剪贴板、键盘/滚轮(PC端)、日历、位置 | [feature-device](references/feature-device.md) |
| 媒体 | 图片(tt.createImage/Image)、音频(tt.createInnerAudioContext/InnerAudioContext)、视频(tt.createVideo)、录音(tt.getRecorderManager) | [feature-media](references/feature-media.md) |

### 开放能力

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 开放能力 | 登录(tt.login/checkSession)、授权(tt.authorize/getSetting)、支付(tt.requestGamePayment/游戏币/道具直购/错误码)、广告(tt.createRewardedVideoAd/BannerAd/InterstitialAd)、Worker(tt.createWorker)、开放数据域、关系链云存储、排行榜、订阅消息、客服、直播、关注、收藏 | [feature-open-capacity](references/feature-open-capacity.md) |

## 关键概念

### 运行环境

小游戏运行在纯 JavaScript VM 中，**无 BOM 和 DOM**。入口文件 `game.js`，全局对象 `GameGlobal`（非 `window`）。禁止 `eval()` 和 `new Function()`。`Proxy` 全版本不可用。基础库集成 core-js 自动 Polyfill。

### 文件结构

```
├── game.js               # 入口文件（必需）
├── game.json             # 小游戏配置（必需）
└── project.config.json   # 工程配置（必需）
```

### 包体积限制

| 类型 | 限制 |
|------|------|
| 普通小游戏 | 总大小 ≤ 20MB |
| 主包 | ≤ 4MB |
| 单个分包 | ≤ 20MB |
| 开放数据域 | ≤ 4MB |

### 快速代码示例

```javascript
// 创建 Canvas
var canvas = tt.createCanvas();
var ctx = canvas.getContext("2d");
ctx.fillStyle = "#ff0000";
ctx.fillRect(0, 0, 100, 100);

// 触摸事件
tt.onTouchStart(function(event) {
  var touch = event.touches[0];
  console.log("touch at:", touch.clientX, touch.clientY);
});

// 网络请求
tt.request({
  url: "https://api.example.com/data",
  method: "GET",
  success: function(res) { console.log(res.data); }
});

// 生命周期
tt.onShow(function() { console.log("游戏进入前台"); });
tt.onHide(function() { console.log("游戏进入后台"); });

// 模块化
var utils = require("./utils.js");

// 支付
tt.requestGamePayment({
  mode: "game", env: 0, platform: "android",
  currencyType: "CNY", buyQuantity: 10,
  customId: "ORDER_" + Date.now(),
  zoneId: "1"
});

// 广告
var videoAd = tt.createRewardedVideoAd({ adUnitId: "your_ad_unit_id" });
videoAd.onClose(function(res) { if (res.isEnded) { /* 发奖励 */ } });
videoAd.show();
```

### 最佳实践

1. 使用 `tt.createCanvas()` 创建画布，上屏 Canvas 全局唯一
2. 通过 `game.json` 配置屏幕方向、分包结构、网络超时
3. 使用 `requestAnimationFrame` 实现游戏主循环
4. 监听 `tt.onMemoryWarning` 及时释放纹理、缓存等资源
5. 无网/弱网条件下做好体验兼容（平台已支持离线缓存）
6. 使用 `tt.getLaunchOptionsSync()` 获取启动场景值
7. 推荐使用 Cocos Creator、LayaAir 等游戏引擎开发
8. H5 游戏迁移需使用 Adapter 适配层
9. 支付必须使用 `customId` 确保订单唯一性
10. 广告始终注册 `onError` 监听异常情况
