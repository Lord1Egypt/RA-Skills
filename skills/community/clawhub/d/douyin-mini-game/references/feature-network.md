# 网络通信

> 官方文档: 网络 API - HTTP 请求、文件上传/下载、WebSocket

## HTTP 请求

### tt.request(options)

> 基础库 1.0.0+，异步方法

```javascript
tt.request({
  url: "https://api.example.com/data",
  method: "GET",           // GET | POST | PUT | DELETE | OPTIONS | HEAD | PATCH
  data: { key: "value" },  // Object/String/ArrayBuffer
  header: { "Content-Type": "application/json" },
  dataType: "json",        // json | (其他，默认根据 Content-Type 推断)
  responseType: "text",    // text | arraybuffer
  timeout: 30000,          // 超时 ms（优先级高于 game.json 配置）
  success: function(res) {
    console.log("状态码:", res.statusCode); // Number
    console.log("数据:", res.data);         // String/Object/ArrayBuffer
    console.log("响应头:", res.header);     // Object
    console.log("Cookie:", res.cookies);    // String[]
  },
  fail: function(err) {
    console.error("请求失败:", err.errMsg);
    // 常见 fail: request:fail timeout / request:fail 等
  },
  complete: function() { /* 完成回调（成功或失败都会执行） */ }
});
```

### 响应对象 (success 回调)

| 属性 | 类型 | 说明 |
|------|------|------|
| statusCode | Number | HTTP 状态码 |
| data | String/Object/ArrayBuffer | 返回数据 |
| header | Object | 响应头 |
| cookies | String[] | 返回 Cookie 列表 |
| errMsg | String | 成功时为 "request:ok" |

### 请求参数详细

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| url | String | 是 | - | 开发者服务器地址 |
| method | String | 否 | GET | HTTP 方法 |
| data | Object/String/ArrayBuffer | 否 | - | 请求参数 |
| header | Object | 否 | - | 请求头，Referer 不可设置 |
| dataType | String | 否 | json | 返回数据格式 |
| responseType | String | 否 | text | 响应数据类型 |
| timeout | Number | 否 | 60000 | 超时时间 (ms) |

## 文件上传

### tt.uploadFile(options)

```javascript
tt.uploadFile({
  url: "https://api.example.com/upload",
  filePath: tempFilePath,         // 临时文件路径或本地文件路径
  name: "file",                   // 文件对应的 key
  header: { "Content-Type": "multipart/form-data" },
  formData: { user: "test" },     // 附加表单数据
  timeout: 60000,
  success: function(res) {
    console.log("状态码:", res.statusCode);
    console.log("返回数据:", res.data);
  },
  fail: function(err) { console.error(err); }
});
```

### 上传参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | String | 是 | 上传地址 |
| filePath | String | 是 | 要上传的文件路径 |
| name | String | 是 | 文件对应 key |
| header | Object | 否 | 请求头 |
| formData | Object | 否 | 附加表单数据 |
| timeout | Number | 否 | 超时 (ms) |

## 文件下载

### tt.downloadFile(options)

```javascript
tt.downloadFile({
  url: "https://example.com/resource.zip",
  header: {},
  filePath: "",     // 可选，指定存储路径
  timeout: 60000,
  success: function(res) {
    console.log("临时路径:", res.tempFilePath);  // 下载后的临时路径
    console.log("状态码:", res.statusCode);
    console.log("文件大小:", res.totalBytesWritten);
  },
  fail: function(err) { console.error(err); }
});
```

### 下载参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | String | 是 | 下载地址 |
| header | Object | 否 | 请求头 |
| filePath | String | 否 | 指定存储路径 |
| timeout | Number | 否 | 超时 (ms) |

## WebSocket

### tt.connectSocket(options)

```javascript
var socketTask = tt.connectSocket({
  url: "wss://example.com/ws",
  header: { "Origin": "https://example.com" },
  protocols: ["protocol1"],     // 子协议数组
  tcpNoDelay: false,            // 是否禁用 Nagle 算法
  success: function() { console.log("正在连接..."); },
  fail: function(err) { console.error("连接失败:", err); }
});

// 连接打开
socketTask.onOpen(function(res) {
  console.log("WebSocket 已连接, header:", res.header);
  // 发送消息
  socketTask.send({ data: "hello" });
  socketTask.send({ data: new ArrayBuffer(8) });
});

// 接收消息
socketTask.onMessage(function(res) {
  console.log("收到消息:", res.data); // String | ArrayBuffer
});

// 错误处理
socketTask.onError(function(err) {
  console.error("WebSocket 错误:", err.errMsg);
});

// 连接关闭
socketTask.onClose(function(res) {
  console.log("关闭码:", res.code);   // Number
  console.log("关闭原因:", res.reason); // String
});

// 主动关闭
socketTask.close({
  code: 1000,
  reason: "normal closure",
  success: function() {}
});
```

### SocketTask 完整方法

| 方法 | 说明 |
|------|------|
| send({data}) | 发送文本或二进制消息 |
| close(options) | 关闭连接 |
| onOpen(cb) | 监听连接打开 |
| onMessage(cb) | 监听消息 |
| onError(cb) | 监听错误 |
| onClose(cb) | 监听关闭 |
| offOpen/offMessage/offError/offClose(cb) | 取消对应监听 |

## 全局超时配置 (game.json)

```json
{
  "networkTimeout": {
    "request": 60000,       // tt.request 超时
    "connectSocket": 60000, // tt.connectSocket 超时
    "uploadFile": 60000,    // tt.uploadFile 超时
    "downloadFile": 60000   // tt.downloadFile 超时
  }
}
```

API 调用中的 `timeout` 参数优先级高于 game.json 全局配置。

## 请求域名白名单

所有网络请求的域名必须在**开发者后台**的「开发设置」中配置为 **request 合法域名** 或 **socket 合法域名**。本地开发调试时可在开发者工具中跳过域名校验。
