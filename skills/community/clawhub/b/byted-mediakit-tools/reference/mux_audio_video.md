# 视频加音频能力

## 功能命名

- `mux_audio_video`

## 作用

- 将视频和音频进行合成，支持保留原音轨及音视频时长对齐策略。

## 参数

| 参数名              | 类型   | 必填 | 说明                                                         |
| ------------------- | ------ | ---- | ------------------------------------------------------------ |
| video_url           | string | ✅   | 待处理视频 URL，支持 `http://` 或 `https://`                 |
| audio_url           | string | ✅   | 待处理音频 URL，支持 `http://` 或 `https://`                 |
| is_audio_reserve    | bool   | ❌   | 是否保留原视频音频，默认 `true`                              |
| is_video_audio_sync | bool   | ❌   | 是否对齐音视频时长，默认 `false`                            |
| sync_mode           | string | ❌   | 对齐模式：`video` \| `audio`，`is_video_audio_sync=true` 时生效 |
| sync_method         | string | ❌   | 对齐方式：`speed` \| `trim`，`is_video_audio_sync=true` 时生效 |

## 返回数据

- task_id(str): 任务查询 id
- requst_id(str): 日志 id
