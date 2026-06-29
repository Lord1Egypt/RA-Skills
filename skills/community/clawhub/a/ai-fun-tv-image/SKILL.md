---
name: ai-fun-tv-image
description: 当用户要求通过 ai.fun.tv、Fun-GP-image2、GPT-image2、GPT、文生图、生图、海报图、公众号封面图、宣传视觉或提示词生成图片时使用本 Skill。本 Skill 指导 Agent 创建 ai.fun.tv 图片项目、提交文生图任务、轮询结果、保存图片，并管理首次鉴权 token。默认模型必须使用 Fun-GP-image2（`tencent-gpt-img-v2`），并将 `GPT`、`GPT-image2` 视为同一模型别名。
---

# ai.fun.tv 文生图

当用户需要根据提示词生成图片时，使用 ai.fun.tv 文生图接口。优先调用本 Skill 附带的脚本执行真实 API 请求；只有调试接口时才手写 cURL。

## 首次鉴权规则

- 首次使用前，先检查是否已有 token：命令行参数、环境变量 `AI_FUN_TV_AUTHORIZATION`、或当前 Skill 目录下的 `authorization.txt`。
- 如果没有 token，引导用户打开 `https://ai.fun.tv/openclaw` 登录并获取鉴权 token。
- 用户提供 token 后，将 token 保存到当前 Skill 目录下的 `authorization.txt`，后续任务直接读取该文件，不再重复询问。
- 保存 token 时设置文件权限为仅当前用户可读写；不要在回复、日志或产物中展示完整 token。
- 请求头必须写成 `authorization: <JWT>`，不要添加 `Bearer ` 前缀。

## 默认参数

- 基础地址：`https://ai.fun.tv`
- 图片项目 appId：`100100`
- 文生图 tabAppCode：`text2image`
- 默认模型名称：`Fun-GP-image2`
- 默认模型值：`tencent-gpt-img-v2`
- 模型别名：`GPT`、`GPT-image2`、`Fun-GP-image2` 都映射到 `tencent-gpt-img-v2`
- 默认比例：`16:9`
- 默认清晰度：`1K`
- 默认生成数量：`1`

## 可选参数

模型：

- `Fun-GP-image2` / `GPT` / `GPT-image2`：`tencent-gpt-img-v2`
- `Fun-NB pro`：`tencent-gem-banana-pro`
- `Fun-NB 2.0`：`tencent-gem-banana2`
- `即梦 5.0`：`doubao-seedream-5.0`
- `即梦 4.5`：`doubao-seedream-4.5`
- `即梦 4.0`：`doubao-seedream-4.0`
- `Qwen-Image-2.0`：`qwen-image-2.0`
- `Wan 2.7`：`wan2.7-image`
- `Wan 2.6`：`wan2.6-image`

比例：`16:9`、`9:16`、`4:3`、`3:4`、`1:1`。

清晰度：`1K`、`2K`、`4K`。

生成数量：`1` 到 `4`。

## 执行流程

1. 规范化模型名称。用户未指定模型，或写 `GPT`、`GPT-image2`、`Fun-GP-image2` 时，统一使用 `tencent-gpt-img-v2`。
2. 获取 token。优先读取已保存的本地 token；首次缺失时引导用户从 `https://ai.fun.tv/openclaw` 获取并保存。
3. 创建图片项目：`POST /service/workflow/project/appbox/create`，请求体为 `{"appId":100100}`。
4. 提交文生图任务：`POST /service/workflow/project/appbox/image/task`。
5. 轮询结果：`GET /service/workflow/resource/project/{userProjectId}?page=1&pageSize=50&projectId={userProjectId}&tabAppCode=text2image`，直到 `taskStatus` 为 `SUCCESS`。
6. 返回 `data.content[].data.url`，如用户要求保存图片，则下载到目标目录。

## 推荐脚本

首次使用，用户提供 token 后执行：

```bash
python3 scripts/generate_text2image.py "高校 AI 提效训练营主视觉海报，年轻学生干部，清爽科技感，正式活动宣传风格" --authorization "用户提供的JWT" --output-dir ./outputs
```

脚本会自动保存 token。后续使用无需再传 token：

```bash
python3 scripts/generate_text2image.py "提示词" --model GPT-image2 --ratio 3:4 --clarity 2K --count 2 --output-dir ./outputs
```

脚本输出 JSON，包含项目 ID、任务 ID、图片 URL 和本地保存路径。

## 接口请求体

创建项目：

```json
{
  "appId": 100100
}
```

提交文生图任务：

```json
{
  "userProjectId": "PROJECT_ID",
  "tabAppCode": "text2image",
  "aspectRatio": "16:9",
  "model": "tencent-gpt-img-v2",
  "clarity": "1K",
  "prompt": "IMAGE_PROMPT",
  "imageCount": 1
}
```

## 失败处理

- 如果接口返回非 `200` 的 `code`，直接报告完整响应中的 `msg` 和 `requestId`。
- 如果轮询超时，报告最后一次 `taskStatus` 和 `taskMessage`。
- 如果图片下载失败，仍然返回已生成的远程图片 URL。
- 不要编造成功结果或图片地址。
