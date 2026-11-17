# 视频分析

> 调用方式见 SKILL.md「调用方式」
> ⚠️ 此工具超时 5 分钟，比普通工具长

## 参数

```json
{
  "url": "https://cdn.example.com/ref_video.mp4"  // 必填：待分析视频，公网URL或本地路径（抖音分享链接先用 get_raw_url 解析）
}
```

## 返回值

分析结果含结构化脚本（style、scene、运镜、灯光等），可直接作为 `ai_clone_video` 的 `script` 参数使用。

## 关键约束

- **双层判断**：`code=0` 且 `data.success=true` 才算分析成功。`code=0` 但 `success=false` 是可能的（视频无法分析时）
- 超时 5 分钟，比普通工具长
- 抖音分享链接需先用 `get_raw_url` 解析，见 [get_raw_url.md](get_raw_url.md)
