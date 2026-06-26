# 音、视频剪切能力

## 功能命名

- `trim_media_duration`

## 作用

- 按时间范围裁剪音频或视频,`end_time` 必须大于 `start_time`。

## 参数

| 参数名     | 类型   | 必填 | 说明                                              |
| ---------- | ------ | ---- | ------------------------------------------------- |
| type       | string | ✅   | 媒体类型：`audio` \| `video`                      |
| source     | string | ✅   | 待剪切资源 URL，支持 `http://` 或 `https://`      |
| start_time | float  | ❌   | 裁剪开始时间，默认 0，最多 2 位小数，单位秒       |
| end_time   | float  | ❌   | 裁剪结束时间，默认片源结尾，最多 2 位小数，单位秒 |

## 返回数据

- task_id(str): 任务查询 id
- requst_id(str): 日志 id
