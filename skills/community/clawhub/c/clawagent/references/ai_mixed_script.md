# 视频混剪

> 调用方式及异步轮询见 SKILL.md「调用方式」「异步任务轮询」

## 参数

```json
{
  "urls": ["https://cdn.example.com/material1.mp4"],  // 必填：素材URL数组，图片或视频
  "text": "今天带大家体验...",                           // 必填：混剪文案
  "voice_type": "营销",                                  // 可选，默认 null：通用 | 角色扮演 | 情感 | 人物模仿 | 特色 | 解说 | 营销 | 客服
  "gender": "男",                                        // 可选，默认 "男"："男" | "女" — 人声性别
  "background_music": true,                              // 可选，默认 true：是否系统推荐背景音乐
  "show_subtitle": true                                  // 可选，默认 true：是否显示文案字幕
}
```

## 关键约束

- `urls` 是**复数数组**，不是单数 `url`
