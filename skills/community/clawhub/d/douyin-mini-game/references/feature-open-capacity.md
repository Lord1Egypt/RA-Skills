# 开放能力

> 官方文档: 开放能力 API - 登录、授权、支付、广告、开放数据域、排行榜、Worker 等

## 登录

### tt.login(options)

```javascript
tt.login({
  success: function(res) {
    console.log("code:", res.code);             // 临时登录凭证，有效期 5 分钟
    console.log("anonymousCode:", res.anonymousCode); // 匿名登录凭证
    // 将 code 发送到服务端，换取 openid 和 session_key
  },
  fail: function(err) { console.error("登录失败", err); }
});
```

### tt.checkSession(options)

```javascript
tt.checkSession({
  success: function() { console.log("登录态有效"); },
  fail: function() { console.log("登录态过期，需重新登录"); }
});
```

## 授权与设置

### tt.getSetting(options)

```javascript
tt.getSetting({
  success: function(res) {
    // res.authSetting = { "scope.userInfo": true, "scope.userLocation": false, ... }
  }
});
```

### tt.authorize(options)
```javascript
tt.authorize({ scope: "scope.userInfo" });
```

### tt.openSetting(options)
打开设置页面，让用户手动开启授权。

## 支付

### tt.requestGamePayment(options)

> 基础库 1.0.0+，异步方法。使用前需完成支付能力接入。

```javascript
// 游戏币场景
tt.requestGamePayment({
  mode: "game",             // 支付类型，目前仅支持 "game"
  env: 0,                   // 环境：0=正式
  platform: "android",      // 平台: android / windows
  currencyType: "CNY",      // 币种，目前仅 CNY
  buyQuantity: 600,         // 购买数量：金币数量×单价 = 限定价格等级
  zoneId: "1",              // 游戏服务区 id
  customId: "ORDER_UNIQUE_ID", // 开发者自定义唯一订单号（必填，1.55.0+）
  extraInfo: '{"userId":"123","version":"1.0"}', // 额外信息（≤256字符）
  success: function(res) { console.log("支付发起成功"); },
  fail: function(res) {
    console.error("支付失败:", res.errCode, res.errMsg);
  }
});
```

**限定价格等级（元）**: 1, 3, 6, 8, 12, 18, 25, 30, 40, 45, 50, 60, 68, 73, 78, 88, 98, 108, 118, 128, 148, 168, 188, 198, 328, 648, 998, 1288, 1998, 2998

**道具直购场景** (基础库 3.47.0+):
```javascript
if (tt.canIUse("requestGamePayment.object.goodType")) {
  tt.requestGamePayment({
    goodType: 2,            // 0=默认/游戏币, 1=游戏币, 2=道具直购
    orderAmount: 10,        // 道具现金价格（单位：分）
    goodName: "道具名称",    // ≤10字符
    currencyType: "CNY",
    zoneId: "1",
    customId: "UNIQUE_ORDER_ID",
    mode: "game",
    env: 0,
    platform: "android",
    extraInfo: '{"key":"value"}'
  });
}
```

**支付错误码**:

| errCode | 说明 |
|---------|------|
| -1 | 支付失败 / 内部错误 |
| -2 | 用户取消支付 |
| 3 | 拉起收银台失败 |
| 4 | 网络异常 |
| -15002 | 请求参数不合法 |
| -15006 | app 没有支付权限（需设置游戏币汇率） |
| -15098 | 用户未通过实名认证 |
| -15099 | 累计支付金额超限 |
| -15101 | customId 为空或不唯一 |
| -16000 | 用户未登录 |
| -20002 | 交易存在风险（风控拦截） |
| 21113 | 人脸验证不通过（疑似未成年） |

**注意事项**:
- 需先调用 `tt.checkSession` 确保用户登录态有效
- 建议填入 `customId` 和 `extraInfo`，否则服务端回调无法关联订单
- 可能存在游戏币延迟到账，建议轮询查询余额（间隔3秒，持续约1分钟）
- PC 端仅支持钻石支付
- 真机测试使用真实金额，建议小额测试

## 广告

### 激励视频广告 tt.createRewardedVideoAd(params)

> 基础库 1.3.0+，同步方法。需先开通「流量主」能力并创建广告位。

```javascript
var videoAd = tt.createRewardedVideoAd({
  adUnitId: "your_ad_unit_id",
  multiton: false,           // 是否开启再得广告（仅安卓）
  multitonRewardMsg: [],     // 再得奖励文案数组，单个≤7字符
  multitonRewardTimes: 0,    // 额外观看次数 (1-4)
  progressTip: false         // 是否开启进度提醒
});

// 事件监听（强烈建议始终注册 onError）
videoAd.onLoad(function() { console.log("广告加载成功"); });
videoAd.onError(function(err) { console.error("广告错误:", err); });
videoAd.onClose(function(res) {
  if (res && res.isEnded) {
    // 广告看完，发放奖励
    console.log("发放奖励");
  } else {
    // 广告中途关闭
    console.log("广告未看完");
  }
});

// 展示广告
videoAd.show().catch(function(err) {
  // 未加载完成，先加载再展示
  videoAd.load().then(function() { videoAd.show(); });
});
```

**广告类型**:
- `tt.createRewardedVideoAd()` - 激励视频广告
- `tt.createBannerAd()` - Banner 广告
- `tt.createInterstitialAd()` - 插屏广告
- `tt.createGridGamePanel()` - 网格游戏面板

**注意事项**:
- 广告全屏展示，iOS 端播放/关闭会触发 onShow/onHide，安卓不会
- 广告播放期间游戏逻辑和渲染均被暂停
- 激励视频目前支持竖屏展示，横屏游戏展示时会先切竖屏
- 录屏分享激励能力：当广告返回 1004 错误时，自动拉起录屏分享替代（基础库 2.20+）

### RewardedVideoAd 实例方法

| 方法 | 说明 |
|------|------|
| show() | 展示广告，返回 Promise |
| load() | 加载广告，返回 Promise |
| onLoad(cb) | 监听广告加载成功 |
| onError(cb) | 监听广告错误 |
| onClose(cb) | 监听广告关闭，res.isEnded 判断是否看完 |
| offLoad/offError/offClose | 取消监听 |
| destroy() | 销毁广告实例 |

## Worker 多线程

### tt.createWorker(workerPath)

创建 Worker 线程。

```javascript
// 主线程
var worker = tt.createWorker("workers/worker.js");

// 向 Worker 发送消息
worker.postMessage({ type: "compute", data: largeArray });

// 监听 Worker 消息
worker.onMessage(function(res) {
  console.log("Worker 返回:", res.data);
});

// 终止 Worker
worker.terminate();
```

### Worker 对象（Worker 线程内）

| 属性/方法 | 说明 |
|-----------|------|
| postMessage(data) | 向主线程发送消息 |
| onMessage(callback) | 监听主线程消息 |
| terminate() | 结束当前 Worker（仅主线程调用） |

**注意事项**:
- Worker 代码目录需在 game.json 的 `workers` 字段中配置
- Worker 线程中也支持 `TTWebAssembly` 对象（基础库 ≥ 3.7.0）

## 开放数据域

```javascript
// 获取开放数据域上下文
var openDataContext = tt.getOpenDataContext();
openDataContext.postMessage({ type: "updateScore", score: 999 });

// 监听开放数据域消息
tt.onMessage(function(data) {
  console.log("来自开放数据域:", data);
});
```

### 开放数据域内 API
```javascript
// 在 openDataContext/index.js 中
wx.onMessage(function(data) { /* ... */ });
wx.getSharedCanvas();        // 获取共享 Canvas
wx.setUserCloudStorage({ KVDataList: [...] });
wx.getUserCloudStorage({ keyList: [...] });
wx.getCloudStorageByRelation({ keyList: [...] });
```

## 关系链云存储

```javascript
tt.setUserCloudStorage({
  KVDataList: [{ key: "score", value: "9999" }, { key: "level", value: "50" }]
});
tt.getUserCloudStorage({ keyList: ["score", "level"] });
tt.getCloudStorageByRelation({ keyList: ["score"] });
tt.removeUserCloudStorage({ keyList: ["tempData"] });
```

## 游戏排行榜

```javascript
tt.setImRankData({ score: 9999 });          // 设置排行
tt.getImRankList({ rankType: 0 });          // 获取排行榜
tt.getImRankData();                          // 获取自己的排行
tt.setImRankDataInOpenContext({ score: 0 }); // 开放域设置排行
```

## 订阅消息

```javascript
tt.requestSubscribeMessage({
  tmplIds: ["template_id_1"],
  success: function(res) { /* res[templateId] = "accept" | "reject" */ }
});
```

## 客服消息

```javascript
tt.openCustomerServiceConversation({
  showMessageCard: true,
  sendMessageTitle: "问题反馈",
  sendMessagePath: "pages/index/index"
});

var button = tt.createContactButton({
  type: "text", text: "联系客服",
  style: { left: 10, top: 10, width: 120, height: 40 }
});
```

## 侧边栏与场景

```javascript
tt.navigateToScene({ scene: "xxx" }); // 跳转到抖音场景
tt.checkScene({ scene: "xxx" });      // 检查场景是否可用
```

## 添加到桌面

```javascript
tt.addShortcut();                       // 提示添加到桌面
tt.checkShortcut({ success: function(res) { console.log(res.status); }});
```

## 直播能力

```javascript
var liveManager = tt.getLiveManager();
liveManager.getLiveStatus();     // 获取直播状态
liveManager.navigateToLive({ roomId: "xxx" }); // 跳转直播间
liveManager.onXScreenSizeChange(function(res) { /* 异形屏尺寸变化 */ });
```

## 关注

```javascript
tt.checkFollowAwemeState();           // 检查抖音号关注状态
tt.openAwemeUserProfile({ secUid: "xxx" }); // 打开抖音号主页
tt.createFollowButton({ type: "text", text: "关注", style: {...} });
tt.checkFollowState();               // 检查关注状态
```

## 收藏与复访

```javascript
tt.showFavoriteGuide();                       // 显示收藏引导
tt.onFavoriteStateChange(function(res) { });  // 监听收藏状态
tt.showRevisitGuide();                        // 显示复访引导
```

## 公会群

```javascript
tt.getUnionGroupInfo();
tt.bindUnionGroup({ groupId: "xxx" });
tt.joinUnionGroup({ groupId: "xxx" });
```

## 推荐流

```javascript
tt.requestFeedSubscribe();
tt.checkFeedSubscribeStatus();
tt.onFeedStatusChange(callback);
```

## 数据分析

```javascript
tt.reportAnalytics("event_name", { key: "value" });
tt.reportScene({ sceneId: "xxx" });
```
