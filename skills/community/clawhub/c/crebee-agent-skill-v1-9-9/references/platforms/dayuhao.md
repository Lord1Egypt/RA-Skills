# 大鱼号发布参数

`platform` 为 `dayuhao`。以下 JSON 是批量发布任务的 `params`；可选字段无值时省略，所有字段均不接受 `null`。

### 视频 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是** | 视频标题；运行时不能为空，最多 60 字。 |
| `desc` | string | **是** | 视频简介；可传空字符串，最多 200 字。 |
| `videoPath` | string | **是** | 本地视频文件路径。 |
| `coverPath` | string | **是** | 横版封面图片路径。 |
| `timing` | number | 否 | 定时发布时间戳；`0` 表示立即发布。 |
| `taskId` | string | 否（建议传） | 用于发布状态回调。 |
| `videoInfo` | object | 否 | 视频信息：`duration`、`width`、`height`、`size` 均为 number，`thumbnail` 为可选 string。 |
| `category` | string | **是** | 视频分类，运行时不能为空；使用客户端内置分类值，当前 HTTP Skill 未暴露分类查询接口。 |
| `tags` | string[] | 否 | 视频标签。 |
| `sourceRemarkType` | `"无需标注"` \| `"AI生成"` \| `"虚构演绎"` \| `"营销信息"` \| `"转载"` \| `"个人观点"` \| `"不适宜未成年人"` | 否 | 内容信息来源声明。 |
| `verticalCoverPath` | string | 否 | 竖版封面图片路径。 |

**最小参数校验示例：**

```json
{
  "title": "大鱼号视频标题",
  "desc": "",
  "videoPath": "/tmp/video.mp4",
  "coverPath": "/tmp/cover.jpg",
  "taskId": "dayuhao-video-1",
  "category": "科技"
}
```

### 文章 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是（运行时）** | 标题长度为 5-50 字。 |
| `content` | string | **是（运行时）** | HTML 正文，去除标签后的文本不能为空。 |
| `covers` | string[] | 否 | schema 支持；当前运行时不支持非空独立封面，封面只能从正文图片选择。 |
| `taskId` | string | 否（建议传） | 用于发布状态回调。 |
| `sourceRemarkType` | `"无需标注"` \| `"AI生成"` \| `"虚构演绎"` \| `"营销信息"` \| `"转载"` \| `"个人观点"` \| `"不适宜未成年人"` | 否 | 信息来源声明；为 `"转载"` 时必须同时提供 `repostLink`。 |
| `repostLink` | string | 否 | 转载原文链接。 |
| `coverMode` | `"none"` \| `"single"` \| `"triple"` | 否 | 横版封面模式。 |
| `coverImageIds` | string[] | 否 | 横版封面使用的正文图片标识。 |
| `verticalCoverImageId` | string | 否 | 竖版封面使用的正文图片标识。 |
| `timing` | number | 否 | 定时发布时间戳；`0` 表示立即发布。 |

**最小参数校验示例：**

```json
{
  "title": "大鱼号文章标题",
  "content": "<p>文章正文</p>",
  "taskId": "dayuhao-article-1"
}
```
