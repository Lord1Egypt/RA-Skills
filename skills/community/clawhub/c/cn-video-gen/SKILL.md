---
name: cn-video-gen
description: 国产AI视频生成技能。支持通义万相（Wan2.6文生视频/图生视频）和可灵（Kling V2）。适合创意视频制作、图生视频、动态内容生成等场景。当用户要求生成视频、将图片生成动态视频、或基于描述生成视频片段时触发。
---

# 国产AI视频生成技能 🎬

## 支持平台

| 平台 | 模型 | 适合场景 | 环境变量 |
|------|------|---------|---------|
| 通义万相 | wan2.6-t2v | 文字→视频 | `DASHSCOPE_API_KEY` |
| 通义万相 | wan2.6-i2v | 图片→视频 | `DASHSCOPE_API_KEY` |
| 可灵 | kling-v2-master | 文字/图片→视频（人物动作好） | `KLING_ACCESS_KEY` + `KLING_SECRET_KEY` |

## 工作流程

### 1. 确认需求
- 文生视频还是图生视频？
- 时长（5/10/15秒）
- 分辨率（720P 省钱 / 1080P 精细）
- 是否需要多镜头叙事（分镜师专用）

### 2. 图生视频：先上传图片到图床
如果是本地图片，必须先上传获取公网URL：
```bash
IMG_URL=$(python3 {baseDir}/scripts/upload_image.py <本地图片路径> | tail -1)
```
图床配置：ImgURL（uid: rrbhyq），credentials 在 TOOLS.md 中。

### 3. 生成视频（异步，需轮询）
调用脚本：`python3 {baseDir}/scripts/generate.py`

### 4. 下载视频并发送到飞书
生成完成后获取 video_url，下载到本地，用 feishu-send-file skill 发送。

## 通义万相 API

**端点：** `https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

**文生视频（T2V）参数：**
```json
{
  "model": "wan2.6-t2v",
  "input": {
    "prompt": "描述文字（中英文均可）",
    "audio_url": "可选：自定义音频URL"
  },
  "parameters": {
    "size": "1280*720",
    "duration": 5,
    "prompt_extend": true,
    "shot_type": "single"
  }
}
```

**图生视频（I2V）参数：**
```json
{
  "model": "wan2.6-i2v",
  "input": {
    "image_url": "图片HTTP URL（非本地路径）",
    "prompt": "描述运动方式"
  },
  "parameters": {
    "size": "1280*720",
    "duration": 5
  }
}
```

**多镜头叙事（分镜师专用）：**
```json
"parameters": {
  "shot_type": "multi",
  "prompt_extend": true
}
```

**查询任务状态：**
`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

**状态说明：**
- `PENDING` → 排队中
- `RUNNING` → 生成中（通常1-5分钟）
- `SUCCEEDED` → 完成，取 `output.video_url`
- `FAILED` → 失败，看 `output.message`

**价格参考（北京地域）：**
- 720P：约0.6元/秒
- 1080P：约1元/秒
- 失败任务不收费

## 可灵 API（Kling V2）

**文档：** https://klingai.kuaishou.com/api/docs

**端点：** `https://api.klingai.com/v1/videos/text2video`

**认证：** 需要 JWT Token（用 Access Key + Secret Key 生成）

**优势：** 人物动作更自然，长视频片段表现好

## 提示词技巧（分镜师专用）

### 描述运动，不只是画面
❌ "海边的日落"
✅ "镜头缓缓推进，海浪拍打礁石，夕阳的橙红色光芒在水面上跳跃"

### 前置主体
模型对提示词前几个词权重更高：
✅ "一个身穿红裙的女孩，在樱花树下旋转，花瓣飞舞"

### 镜头语言
- 推镜：camera slowly pushes in / 镜头缓缓推近
- 拉镜：camera pulls back / 镜头拉远
- 跟拍：tracking shot / 跟拍镜头
- 摇镜：pan left/right / 镜头向左/右摇

### 图生视频注意
- 图片分辨率够高（建议1280x720以上）
- 提前裁剪为目标比例（16:9 or 9:16）
- 图中有隐含动势效果更好（飘动的头发、奔跑姿势）

## 成本控制
1. 先用5秒/720P验证 prompt
2. 满意后再用10-15秒/1080P出成品
3. 生成失败不收费，大胆试
4. 视频 URL 有效期有限，生成后及时下载

## 飞书发送
生成的视频可通过 message tool 直接发送：
```python
# 下载到本地后用 media 参数发送
message(action="send", channel="feishu", media="/path/to/video.mp4", contentType="video/mp4")
```
