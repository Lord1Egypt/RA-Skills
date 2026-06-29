# 媒体

> 官方文档: 媒体 API - 图片、音频、视频、录音

## 图片 (Image)

### tt.createImage()

> 基础库 1.31.0+，同步方法

```javascript
var img = tt.createImage();

// src 支持：网络 URL、本地 ttfile://协议、base64、ArrayBuffer
img.src = "assets/character.png";

// 事件监听（两种方式等价）
img.onload = function() {
  console.log(img.width, img.height);
  ctx.drawImage(img, 0, 0);
};
img.onerror = function(err) { console.error("加载失败", err); };

// 或使用 addEventListener
img.addEventListener("load", function(e) {
  console.log("width:", e.target.width);
});
```

### Image 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| src | String/ArrayBuffer | 图片资源地址 |
| width | Number | 图片真实宽度（只读，加载后） |
| height | Number | 图片真实高度（只读，加载后） |
| onload | Function | 加载成功回调 |
| onerror | Function | 加载失败回调 |

**注意**: 通过 `tt.createImage()` 加载的图片不需要配置白名单。

## 音频

### tt.createInnerAudioContext()

> 基础库 1.0.0+

创建内部音频实例，支持包内路径和网络 URL。同时最多 10 个实例。

```javascript
var audio = tt.createInnerAudioContext();
audio.src = "assets/bgm.mp3"; // 或 https://example.com/music.mp3
audio.autoplay = false;
audio.loop = true;
audio.volume = 0.8;           // 0.0 ~ 1.0
audio.playbackRate = 1.0;     // 0.5 ~ 2.0

// 事件监听
audio.onCanplay(function() {
  console.log("可播放, 时长:", audio.duration, "秒");
  audio.play();
});
audio.onPlay(function() { console.log("开始播放"); });
audio.onPause(function() { console.log("暂停"); });
audio.onStop(function() { console.log("停止"); });
audio.onEnded(function() {
  console.log("播放结束");
  // audio.destroy(); // 不再使用时销毁
});
audio.onError(function(err) { console.error("音频错误:", err); });
audio.onTimeUpdate(function() { console.log("进度:", audio.currentTime); });
audio.onWaiting(function() { console.log("加载中..."); });
audio.onSeeking(function() { console.log("跳转中..."); });
audio.onSeeked(function() { console.log("跳转完成"); });

// 播放控制
audio.play();
audio.pause();
audio.stop();      // 停止后再次 play 会从头播放
audio.seek(30);    // 跳转到 30 秒
audio.destroy();   // 销毁实例释放资源
```

### InnerAudioContext 属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| src | String | - | 音频地址（包内路径/网络URL/ttfile://） |
| autoplay | Boolean | false | 是否自动播放 |
| loop | Boolean | false | 是否循环 |
| volume | Number | 1 | 音量 (0-1) |
| playbackRate | Number | 1 | 播放速率 (0.5-2.0) |
| startTime | Number | 0 | 开始播放位置（秒） |
| duration | Number | 0 | 音频总长度（只读） |
| currentTime | Number | 0 | 当前播放位置（只读） |
| paused | Boolean | true | 是否暂停（只读） |
| obeyMuteSwitch | Boolean | true | 是否遵循静音开关（iOS） |

### 支持的音频格式

mp3, aac, m4a, wav, flac, ape, ogg, wma, midi

## 视频

### tt.createVideo(options)

> 基础库 1.0.0+

```javascript
var video = tt.createVideo({
  src: "https://example.com/video.mp4",
  controls: true,
  autoplay: false,
  loop: false,
  muted: false,
  initialTime: 0,
  width: 300, height: 200,
  x: 0, y: 0,
  showProgress: true,     // 是否显示进度条
  showCenterPlayBtn: true // 是否显示居中播放按钮
});

// 事件
video.onPlay(function() {});
video.onPause(function() {});
video.onEnded(function() {});
video.onError(function(err) { console.error(err); });
video.onTimeUpdate(function() { console.log(video.currentTime); });

// 控制
video.play();
video.pause();
video.stop();
video.seek(30);
video.requestFullScreen();
video.exitFullScreen();
video.destroy();
```

### Video 属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| src | String | - | 视频地址 |
| controls | Boolean | true | 显示默认控件 |
| autoplay | Boolean | false | 自动播放 |
| loop | Boolean | false | 循环播放 |
| muted | Boolean | false | 静音 |
| width/height | Number | 300/150 | 尺寸 |
| x/y | Number | 0/0 | 位置 |
| playbackRate | Number | 1 | 播放速率 (0.5-2.0) |

## 录音

### tt.getRecorderManager()

```javascript
var recorder = tt.getRecorderManager();

recorder.onStart(function() { console.log("录音开始"); });
recorder.onPause(function() { console.log("录音暂停"); });
recorder.onResume(function() { console.log("录音恢复"); });
recorder.onStop(function(res) {
  console.log("临时文件:", res.tempFilePath);
  console.log("时长:", res.duration, "ms");
  console.log("文件大小:", res.fileSize);
});
recorder.onError(function(err) { console.error(err); });
recorder.onFrameRecorded(function(res) {
  console.log("帧数据:", res.frameBuffer);
});

// 开始录音
recorder.start({
  duration: 60000,          // 最长录音 (ms)，默认 60000
  sampleRate: 44100,        // 采样率: 8000/16000/44100
  numberOfChannels: 1,      // 声道: 1 或 2
  encodeBitRate: 192000,    // 编码码率
  format: "mp3",            // mp3 | aac | wav
  frameSize: 50             // 帧大小 (KB)
});

recorder.pause();  // 暂停
recorder.resume(); // 继续
recorder.stop();   // 停止
```
