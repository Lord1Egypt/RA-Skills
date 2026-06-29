# 核心框架

> 基于官方文档: 框架、运行时、模块化、场景值

## 项目文件结构

```
├── game.js               # 小游戏入口文件（必需）
├── game.json             # 小游戏配置文件（必需）
└── project.config.json   # 工程配置文件（必需）
```

## game.json 完整配置

| 属性 | 类型 | 必填 | 默认值 | 描述 | 最低版本 |
|------|------|------|--------|------|---------|
| deviceOrientation | String | 否 | `'landscape'` | 屏幕方向: portrait / landscape | - |
| showStatusBar | Boolean | 否 | `false` | 是否显示状态栏 | - |
| networkTimeout | Object | 否 | - | 网络超时配置（毫秒） | - |
| workers | String | 否 | - | Worker 代码目录路径 | - |
| openDataContext | String | 否 | - | 开放数据域目录 | 1.11.0 |
| subPackages | Object | 否 | - | 分包结构配置 | 1.88.0 |
| menuButtonStyle | String | 否 | - | 更多面板深浅色: light / dark | 3.16.0 |
| enableIOSHighPerformanceMode | Boolean | 否 | `false` | iOS 高性能模式 | 3.43.0 |
| plugins | Object | 否 | - | 插件配置 | 3.65.0 |

### 完整示例

```json
{
  "deviceOrientation": "portrait",
  "showStatusBar": false,
  "networkTimeout": {
    "request": 30000,
    "connectSocket": 30000,
    "uploadFile": 30000,
    "downloadFile": 30000
  },
  "workers": "workers",
  "openDataContext": "openDataContext",
  "subPackages": [
    { "name": "stage1", "root": "stage1/" }
  ],
  "menuButtonStyle": "dark",
  "enableIOSHighPerformanceMode": true,
  "plugins": {
    "myPlugin": { "provider": "ttxxxxxxxx", "version": "1.0.0" }
  }
}
```

## 运行时环境

### 运行环境概述

- **JS 线程**: 执行游戏主逻辑，基于 JavaScript VM
- **Worker 线程**: 通过 `tt.createWorker()` 创建，处理计算密集型任务
- **开放数据域**: 独立 JS 环境，处理关系链数据

小游戏无 BOM 和 DOM API，入口为 `game.js`。

### 运行状态

| 状态 | 触发条件 | 表现 |
|------|---------|------|
| 前台运行 | 游戏正常显示 | JS 逻辑和渲染正常执行 |
| 后台挂起 | 关闭按钮/Home键 | JS 暂停，可短时间维持 |
| 进程终止 | 超时/资源不足 | 进程被系统杀死 |

### 启动类型

- **冷启动**: 首次打开或进程被终止后，需完整加载资源
- **热启动**: 短时间从后台恢复，无需重新加载，JS 上下文保留

### 进程终止条件
- 后台超时（通常几分钟）
- 内存过高触发回收
- iOS 连续内存警告主动终止 → 使用 `tt.onMemoryWarning` 监听

### JS 支持与限制

**严格禁止**:
- `eval()` 函数
- `new Function()` 动态创建函数
- `Proxy` 对象（全版本不可用）

**Polyfill**: 基础库集成 core-js，自动填充缺失的标准 API

**iOS Promise 时序问题** (iOS 15 及以下):
```javascript
// 标准环境: [1,2,3,5,6]
// iOS ≤15:    [1,2,3,6,5]  (setTimeout 模拟 Promise → 宏任务)
var stack = [];
setTimeout(() => stack.push(6), 0);
stack.push(1);
new Promise(r => { stack.push(2); r(); }).then(() => stack.push(5));
stack.push(3);
```

## 全局对象

### tt

小游戏 API 全局对象，承载所有平台能力。

```javascript
tt.createCanvas();
tt.request({ url: "..." });
tt.onShow(function() {});
```

### GameGlobal

替代浏览器的 `window` 对象，所有全局变量都是 GameGlobal 的属性。

```javascript
setTimeout === GameGlobal.setTimeout; // true
GameGlobal === GameGlobal.GameGlobal; // true (循环引用)
```

## 模块化

### require(path)

```javascript
// common.js
module.exports.sayHello = function(name) { console.log(`Hello ${name}`); };
exports.sayGoodbye = function(name) { console.log(`Goodbye ${name}`); };

// game.js
var common = require("./common/common.js"); // 仅支持相对路径
common.sayHello("World");
```

### module / exports

```javascript
module.exports = { fn1: function(){}, fn2: function(){} }; // 替换导出
exports.fn3 = function(){};  // 添加导出（不能赋值 exports = {}）
```

## 场景值

通过 `tt.getLaunchOptionsSync().scene` 获取，标识启动来源（搜索、分享、推荐流等）。

## 包体积限制

| 包类型 | 限制 |
|--------|------|
| 普通小游戏总大小 | ≤ 20MB |
| 整体包（分包后） | ≤ 20MB |
| 单个主包 | ≤ 4MB |
| 单个分包 | ≤ 20MB |
| 开放数据域 | ≤ 4MB |

IDE 不统计: dot 隐藏文件、node_modules、js.map 文件

**支持的文件后缀**: png, jpg, jpeg, gif, svg, json, cer, mp3, aac, m4a, mp4, wav, flac, ape, ogg, wma, midi, ogv, webm, mkv, ttc, ttf, woff, otf, obj, dae, fbx, mtl, stl, 3ds, pvr, plist, fnt, gz, ccz, bmp, atlas, swf, ani, part, proto, bin, sk, mipmaps, txt, zip, tt, map, silk, dbbin, dbmv, etc, lmat, lm, ls, lh, lani, lav, lsani, ltc, xml, pkm, scene, csv, prefab, mesh, astc, wasm, br, heic, ico, cur, wasm.br, dat, dds, glb, gltf, ktx, lmani, lml, skel

## Adapter 适配层

从 H5/Web 游戏迁移到小游戏时，需要用 Adapter 适配 `window`、`document` 等浏览器 API。游戏引擎（Cocos Creator、LayaAir等）导出的版本一般已内置 Adapter。使用 PixiJS、ThreeJS 等时需引入 [tt-adapter](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/framework/runtime/adapter)。

## 无网兼容

平台支持缓存后无网打开，建议游戏逻辑根据网络条件做好兼容。

## API 类型声明

提供 TypeScript 类型声明文件，引入后获得 `tt.*` API 的类型提示。
