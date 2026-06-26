---
name: bozo-jiaodu
description: AI图片摄像机角度提示词转换助手。当用户需要将创意描述转换为摄像机角度提示词、提到"生成"、"转换成"、"角度"、"视角"、"镜头"、"特写"、"中景"、"远景"、"侧视"、"俯视"、"仰视"、"左侧"、"右侧"、"前方"、"后方"等与摄像机位置相关的词汇时必须使用此技能。只要涉及到角度或视角，都必须参考96个摄像机位置提示词进行转换，输出以<sks>开头的标准格式。如果输入不涉及摄像机位置转换，则说明这是图片其他修改命令。
---

# 摄像机角度提示词转换助手

## 核心功能

将用户的创意描述转换为标准的摄像机角度提示词。提示词必须以 `<sks>` 开头，并严格遵循96个摄像机位置标准格式。

## 转换规则

### 1. 涉及角度/视角的输入

当用户输入包含以下任何关键词时，必须转换为对应的摄像机提示词：

**方向关键词**：
- 左侧/左边 → `left side view`
- 右侧/右边 → `right side view`
- 前方/正面/前面 → `front view`
- 后方/背面/后面 → `back view`
- 左前侧 → `front-left quarter view`
- 右前侧 → `front-right quarter view`
- 左后侧 → `back-left quarter view`
- 右后侧 → `back-right quarter view`

**高度角度关键词**：
- 低角度/仰视 → `low-angle shot`
- 平视/水平 → `eye-level shot`
- 高角度/俯视 → `elevated shot` 或 `high-angle shot`

**镜头距离关键词**：
- 特写/大特写 → `close-up`
- 中景 → `medium shot`
- 远景/全景 → `wide shot`

### 2. 标准输出格式

输出必须遵循以下格式：

```
<sks> [方向] [高度角度] [镜头距离]
```

**示例**：
- "左侧低角度特写" → `<sks> left side view low-angle shot close-up`
- "正面平视中景" → `<sks> front view eye-level shot medium shot`
- "右后侧高角度远景" → `<sks> back-right quarter view high-angle shot wide shot`

### 3. 不涉及角度的输入

如果用户输入不包含任何角度或视角相关关键词，说明这是**图片其他修改命令**，输出提示：

```
⚠️ 此请求不涉及摄像机角度转换，属于图片其他修改命令。
请使用相应的图片编辑/生成工具进行处理。
```

## 96个摄像机位置标准提示词

### close-up (特写) - 24个

```
<sks> left side view low-angle shot close-up
<sks> front-left quarter view low-angle shot close-up
<sks> front view low-angle shot close-up
<sks> front-right quarter view low-angle shot close-up
<sks> right side view low-angle shot close-up
<sks> back-right quarter view low-angle shot close-up
<sks> back view low-angle shot close-up
<sks> back-left quarter view low-angle shot close-up
<sks> left side view eye-level shot close-up
<sks> front-left quarter view eye-level shot close-up
<sks> front view eye-level shot close-up
<sks> front-right quarter view eye-level shot close-up
<sks> right side view eye-level shot close-up
<sks> back-right quarter view eye-level shot close-up
<sks> back view eye-level shot close-up
<sks> back-left quarter view eye-level shot close-up
<sks> left side view elevated shot close-up
<sks> front-left quarter view elevated shot close-up
<sks> front view elevated shot close-up
<sks> front-right quarter view elevated shot close-up
<sks> right side view elevated shot close-up
<sks> back-right quarter view elevated shot close-up
<sks> back view elevated shot close-up
<sks> back-left quarter view elevated shot close-up
```

### medium shot (中景) - 24个

```
<sks> left side view low-angle shot medium shot
<sks> front-left quarter view low-angle shot medium shot
<sks> front view low-angle shot medium shot
<sks> front-right quarter view low-angle shot medium shot
<sks> right side view low-angle shot medium shot
<sks> back-right quarter view low-angle shot medium shot
<sks> back view low-angle shot medium shot
<sks> back-left quarter view low-angle shot medium shot
<sks> left side view eye-level shot medium shot
<sks> front-left quarter view eye-level shot medium shot
<sks> front view eye-level shot medium shot
<sks> front-right quarter view eye-level shot medium shot
<sks> right side view eye-level shot medium shot
<sks> back-right quarter view eye-level shot medium shot
<sks> back view eye-level shot medium shot
<sks> back-left quarter view eye-level shot medium shot
<sks> left side view elevated shot medium shot
<sks> front-left quarter view elevated shot medium shot
<sks> front view elevated shot medium shot
<sks> front-right quarter view elevated shot medium shot
<sks> right side view elevated shot medium shot
<sks> back-right quarter view elevated shot medium shot
<sks> back view elevated shot medium shot
<sks> back-left quarter view elevated shot medium shot
```

### wide shot (远景/全景) - 24个

```
<sks> left side view low-angle shot wide shot
<sks> front-left quarter view low-angle shot wide shot
<sks> front view low-angle shot wide shot
<sks> front-right quarter view low-angle shot wide shot
<sks> right side view low-angle shot wide shot
<sks> back-right quarter view low-angle shot wide shot
<sks> back view low-angle shot wide shot
<sks> back-left quarter view low-angle shot wide shot
<sks> left side view eye-level shot wide shot
<sks> front-left quarter view eye-level shot wide shot
<sks> front view eye-level shot wide shot
<sks> front-right quarter view eye-level shot wide shot
<sks> right side view eye-level shot wide shot
<sks> back-right quarter view eye-level shot wide shot
<sks> back view eye-level shot wide shot
<sks> back-left quarter view eye-level shot wide shot
<sks> left side view elevated shot wide shot
<sks> front-left quarter view elevated shot wide shot
<sks> front view elevated shot wide shot
<sks> front-right quarter view elevated shot wide shot
<sks> right side view elevated shot wide shot
<sks> back-right quarter view elevated shot wide shot
<sks> back view elevated shot wide shot
<sks> back-left quarter view elevated shot wide shot
```

### high-angle shot (高角度俯视) - 24个

```
<sks> left side view high-angle shot close-up
<sks> front-left quarter view high-angle shot close-up
<sks> front view high-angle shot close-up
<sks> front-right quarter view high-angle shot close-up
<sks> right side view high-angle shot close-up
<sks> back-right quarter view high-angle shot close-up
<sks> back view high-angle shot close-up
<sks> back-left quarter view high-angle shot close-up
<sks> left side view high-angle shot medium shot
<sks> front-left quarter view high-angle shot medium shot
<sks> front view high-angle shot medium shot
<sks> front-right quarter view high-angle shot medium shot
<sks> right side view high-angle shot medium shot
<sks> back-right quarter view high-angle shot medium shot
<sks> back view high-angle shot medium shot
<sks> back-left quarter view high-angle shot medium shot
<sks> left side view high-angle shot wide shot
<sks> front-left quarter view high-angle shot wide shot
<sks> front view high-angle shot wide shot
<sks> front-right quarter view high-angle shot wide shot
<sks> right side view high-angle shot wide shot
<sks> back-right quarter view high-angle shot wide shot
<sks> back view high-angle shot wide shot
<sks> back-left quarter view high-angle shot wide shot
```

## 转换示例

| 用户输入 | 转换结果 |
|---------|---------|
| 生成一个左侧低角度特写 | `<sks> left side view low-angle shot close-up` |
| 转换成右侧俯视中景 | `<sks> right side view elevated shot medium shot` |
| 正面平视特写 | `<sks> front view eye-level shot close-up` |
| 左前侧仰拍远景 | `<sks> front-left quarter view low-angle shot wide shot` |
| 修改图片颜色 | `⚠️ 此请求不涉及摄像机角度转换，属于图片其他修改命令。` |
| 添加滤镜效果 | `⚠️ 此请求不涉及摄像机角度转换，属于图片其他修改命令。` |

## 使用流程

1. **分析用户输入**：检测是否包含角度/视角相关关键词
2. **匹配标准提示词**：根据关键词组合，从96个标准提示词中找到完全匹配的项
3. **输出结果**：返回以 `<sks>` 开头的标准提示词
4. **非角度请求**：说明这是图片其他修改命令

## 注意事项

- 必须严格使用96个标准提示词之一，不能自行组合或创造
- 关键词识别需要智能匹配（如"左边"、"左侧"、"左面"都应识别为 `left side view`）
- 如果用户描述无法精确匹配96个标准提示词，选择最接近的一个
- 输出格式必须精确，不能有多余空格或换行

---

## BizyAir API 图片角度调整

当用户需要实际执行图片角度调整时，可以使用 BizyAir 的异步 API 进行处理。

### 环境依赖

**必需环境变量**：
```bash
export BIZYAIR_API_KEY="your_actual_api_key_here"
```

### API 参数

- **web_app_id**: `43531` (图片角度调整工作流)
- **输入参数**:
  - `41:LoadImage.image`: 原始图片 URL
  - `112:TextEncodeQwenImageEditPlus.prompt`: 摄像机角度提示词（以 `<sks>` 开头）

### 使用脚本

项目提供了两个 Shell 脚本用于 API 调用：

#### 1. 创建角度调整任务

```bash
bash scripts/create_angle_task.sh <图片URL> <摄像机提示词> [web_app_id]
```

**示例**：
```bash
bash scripts/create_angle_task.sh \
  "https://example.com/image.png" \
  "<sks> left side view low-angle shot close-up"
```

**返回**：
```
📤 正在创建摄像机角度调整任务...
📷 图片 URL: https://example.com/image.png
🎬 摄像机提示词: <sks> left side view low-angle shot close-up

✅ 任务创建成功！

🔖 任务 ID: ca339473-aec3-469d-8ee6-a6657c38cd1c

⏳ 图片正在后台处理中...
💡 使用以下命令查询结果:
   bash scripts/get_task_outputs.sh ca339473-aec3-469d-8ee6-a6657c38cd1c
```

#### 2. 获取任务结果

```bash
bash scripts/get_task_outputs.sh <requestId> [轮询间隔]
```

**示例**：
```bash
bash scripts/get_task_outputs.sh ca339473-aec3-469d-8ee6-a6657c38cd1c
```

**返回**：
```
🔍 查询任务结果...
🔖 任务 ID: ca339473-aec3-469d-8ee6-a6657c38cd1c
⏱️ 轮询间隔: 5 秒

⏳ 任务进行中... (Processing)
💡 等待 5 秒后重新查询...

✅ 任务完成！

📊 任务详情:

### 🎨 摄像机角度调整结果

> 🔖 任务 ID: `ca339473-aec3-469d-8ee6-a6657c38cd1c`
> ⏱️ 生成耗时: ~12.5 秒
> 🔄 共 1 张图片

| 序号 | 预览 | 图片 URL |
| --- | --- | --- |
| 1 | ![图片1](https://storage.bizyair.cn/outputs/xxx.png) | https://storage.bizyair.cn/outputs/xxx.png |

> 📥 如需下载图片，请提供保存路径
```

### 直接 API 调用

如果不使用脚本，可以直接使用 curl 调用 API：

**创建任务**：
```bash
curl -X POST "https://api.bizyair.cn/w/v1/webapp/task/openapi/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${BIZYAIR_API_KEY}" \
  -d '{
  "web_app_id": 43531,
  "suppress_preview_output": false,
  "input_values": {
    "41:LoadImage.image": "https://example.com/image.png",
    "112:TextEncodeQwenImageEditPlus.prompt": "<sks> back-right quarter view high-angle shot medium shot\n"
  }
}'
```

**查询结果**：
```bash
curl -X GET "https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs?requestId=<requestId>" \
  -H "Authorization: Bearer ${BIZYAIR_API_KEY}"
```

### API 响应格式

**创建任务成功响应**：
```json
{
  "requestId": "ca339473-aec3-469d-8ee6-a6657c38cd1c"
}
```

**查询结果成功响应**：
```json
{
  "code": 20000,
  "message": "Ok",
  "data": {
    "request_id": "29f53793-12d3-4dd3-b2a8-4d9848e0c7da",
    "status": "Success",
    "outputs": [
      {
        "object_url": "https://storage.bizyair.cn/outputs/xxx.png",
        "output_ext": ".png",
        "cost_time": 10775,
        "audit_status": 2,
        "error_type": "NOT_ERROR"
      }
    ]
  }
}
```

### 错误处理

**任务创建失败**：
```
❌ 任务创建失败

💡 可能原因：
• BIZYAIR_API_KEY 无效或过期
• 网络连接不稳定
• 图片 URL 无法访问
• 请求参数格式错误

建议您：
1. 检查环境变量 BIZYAIR_API_KEY 是否正确设置
2. 确认摄像机提示词格式正确（以 <sks> 开头）
3. 稍后重试
```

**任务执行失败**：
```
⚠️ 图片角度调整任务执行失败

🔖 任务 ID: xxx
❌ 错误信息: xxx

💡 建议：
• 检查摄像机提示词是否属于96个标准提示词之一
• 确认原始图片 URL 可访问
• 稍后使用相同参数重试
```
