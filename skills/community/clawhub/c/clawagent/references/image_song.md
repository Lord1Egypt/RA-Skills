# 照片唱歌

> 调用方式及异步轮询见 SKILL.md「调用方式」「异步任务轮询」

## 参数

```json
{
  "url": "https://cdn.example.com/face.jpg",       // 必填：带人脸的照片，公网URL
  "audio_url": "https://cdn.example.com/song.mp3"  // 必填：歌曲音频，公网URL
}
```

## 关键约束

- 两个 URL 都必填，缺一不可。这是唯一需要两个公网 URL 的工具
