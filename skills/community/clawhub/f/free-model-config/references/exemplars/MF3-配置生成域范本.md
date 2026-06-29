## MF3 配置生成域范本

### MF3-01 API Key 生成范本

**必选组件**：

1. **平台后台网址**：

| 平台 | 后台网址 | 说明 |
|------|---------|------|
| Agnes AI | https://platform.agnes-ai.com/settings/apiKeys | Sapiens AI 平台 |
| 智谱 BigModel | https://open.bigmodel.cn/apikey/platform | 智谱平台 |
| 商汤 SenseNova | https://platform.sensenova.cn/console/keys | 商汤平台 |
| 小米 MIMO | https://platform.xiaomimimo.com/console/api-keys | 小米平台 |
| 美团 LongCat | https://longcat.chat/platform/api_keys | 美团平台 |

2. **API Key 生成步骤**：

1. 访问平台后台网址：{后台网址}
2. 登录账号
3. 进入 API Key 管理页面
4. 点击"生成 API Key"按钮
5. 复制生成的 API Key

3. **API Key 保存**：

- **保存位置**：`~/.workbuddy/models.json`
- **保存格式**：
  ```json
  {
    "id": "{模型ID}",
    "name": "{模型名称}",
    "vendor": "Custom",
    "url": "{接口地址}",
    "apiKey": "{生成的API Key}",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  }
  ```

**可选组件**：

**API Key 权限设置**：

- {权限设置说明}

**API Key 轮换策略**：

- 建议每 {时间周期} 更换一次 API Key
- 更换时需要更新 `~/.workbuddy/models.json` 中的配置

**组装顺序**：平台登录 → 后台访问 → API Key 生成 → API Key 保存

**约束**：API Key 必须从官方后台网址生成

**格式**：API Key 信息（Markdown）

**输出示例**：

```markdown
## API Key 生成报告

## 平台信息
- 平台名称：Agnes AI
- 后台网址：https://platform.agnes-ai.com/settings/apiKeys

## API Key 生成步骤
1. 访问 https://platform.agnes-ai.com/settings/apiKeys
2. 登录账号
3. 进入 API Key 管理页面
4. 点击"生成 API Key"按钮
5. 复制生成的 API Key

## API Key 保存
- 保存位置：~/.workbuddy/models.json
- 保存格式：
  ```json
  {
    "id": "agnes-2.0-flash",
    "name": "agnes-2.0-flash",
    "vendor": "Custom",
    "url": "https://apihub.agnes-ai.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  }
  ```

## API Key 权限设置
- 建议设置只读权限
- 不要分享给他人

## API Key 轮换策略
- 建议每 3 个月更换一次 API Key
- 更换时需要更新 ~/.workbuddy/models.json 中的配置
```

---

### MF3-02 接口配置范本

**必选组件**：

1. **接口地址**：

| 平台 | 接口地址 | 说明 |
|------|---------|------|
| Agnes AI | https://apihub.agnes-ai.com/v1 | 文本生成接口 |
| 智谱 BigModel | https://open.bigmodel.cn/api/paas/v4/ | 文本生成接口 |
| 商汤 SenseNova | https://token.sensenova.cn/v1 | 文本生成接口 |
| 小米 MIMO | https://token-plan-cn.xiaomimimo.com/v1 | 文本生成接口 |
| 美团 LongCat | https://api.longcat.chat/openai | 文本生成接口 |

2. **接口参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 模型名称 |
| prompt | string | 是 | 输入文本 |
| max_tokens | integer | 否 | 最大生成长度 |
| temperature | float | 否 | 生成随机性 |

3. **接口配置**：

```json
{
  "url": "{接口地址}",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer {API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "{模型名称}",
    "prompt": "{输入文本}",
    "max_tokens": {最大长度},
    "temperature": {随机性}
  }
}
```

**可选组件**：

**接口测试**：

```bash
curl -X POST {接口地址} \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "{模型名称}",
    "prompt": "测试输入",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

**接口验证**：

- [ ] 接口地址可访问
- [ ] API Key 有效
- [ ] 请求参数正确
- [ ] 响应格式正确

**组装顺序**：接口识别 → 参数配置 → 接口配置 → 接口验证

**约束**：接口地址必须准确无误

**格式**：接口配置（JSON）

**输出示例**：

```json
{
  "url": "https://apihub.agnes-ai.com/v1",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer your_api_key_here",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "agnes-2.0-flash",
    "prompt": "测试输入",
    "max_tokens": 100,
    "temperature": 0.7
  }
}
```

---

### MF3-03 模型配置范本

**必选组件**：

1. **模型名称**：

| 平台 | 模型名称 | 说明 |
|------|---------|------|
| Agnes AI | agnes-2.0-flash | 多模态模型 |
| 智谱 BigModel | glm-4.7-flash | 文本生成模型 |
| 商汤 SenseNova | sensenova-6.7-flash-lite | 文本生成模型 |
| 小米 MIMO | mimo-v2.5-pro | 文本生成模型 |
| 美团 LongCat | LongCat-2.0-Preview | 文本生成模型 |

2. **模型配置**：

```json
{
  "id": "{模型ID}",
  "name": "{模型名称}",
  "vendor": "Custom",
  "url": "{接口地址}",
  "apiKey": "{API Key}",
  "supportsToolCall": true,
  "supportsImages": true,
  "supportsReasoning": true,
  "useCustomProtocol": false
}
```

3. **配置文件**：

配置文件位置：`~/.workbuddy/models.json`

**可选组件**：

**配置验证**：

- [ ] 模型 ID 正确
- [ ] 模型名称正确
- [ ] 接口地址可访问
- [ ] API Key 有效

**配置测试**：

```bash
curl -X POST {接口地址} \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "{模型名称}",
    "prompt": "测试输入",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

**组装顺序**：模型识别 → 配置生成 → 配置文件 → 配置验证

**约束**：配置必须完整准确

**格式**：模型配置文件（JSON）

**输出示例**：

```json
{
  "id": "agnes-2.0-flash",
  "name": "agnes-2.0-flash",
  "vendor": "Custom",
  "url": "https://apihub.agnes-ai.com/v1",
  "apiKey": "your_api_key_here",
  "supportsToolCall": true,
  "supportsImages": true,
  "supportsReasoning": true,
  "useCustomProtocol": false
}
```

---

### MF3-04 WorkBuddy 模板范本

**必选组件**：

1. **模板内容**：

以下是 `%USERPROFILE%\.workbuddy\models.json` 的模板内容：

```json
[
  {
    "id": "agnes-2.0-flash",
    "name": "agnes-2.0-flash",
    "vendor": "Custom",
    "url": "https://apihub.agnes-ai.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "glm-4.7-flash",
    "name": "glm-4.7-flash",
    "vendor": "Custom",
    "url": "https://open.bigmodel.cn/api/paas/v4",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "sensenova-6.7-flash-lite",
    "name": "sensenova-6.7-flash-lite",
    "vendor": "Custom",
    "url": "https://token.sensenova.cn/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "mimo-v2.5-pro",
    "name": "mimo-v2.5-pro",
    "vendor": "Custom",
    "url": "https://token-plan-cn.xiaomimimo.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "LongCat-2.0-Preview",
    "name": "LongCat-2.0-Preview",
    "vendor": "Custom",
    "url": "https://api.longcat.chat/openai",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  }
]
```

2. **使用说明**：

1. 复制上述模板内容
2. 将每个模型的 `your_api_key_here` 替换为从对应平台后台网址生成的 API Key
3. 保存到 `%USERPROFILE%\.workbuddy\models.json`

3. **保存位置**：

配置文件位置：`%USERPROFILE%\.workbuddy\models.json`

**可选组件**：

**模板验证**：

- [ ] 模板格式正确
- [ ] 所有模型配置完整
- [ ] API Key 已替换

**模板测试**：

```bash
## 测试 Agnes AI 模型
curl -X POST https://apihub.agnes-ai.com/v1 \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-2.0-flash",
    "prompt": "测试输入",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

**组装顺序**：模板准备 → 内容填充 → 使用说明 → 保存验证

**约束**：模板必须完整准确，API Key 必须脱敏

**格式**：JSON 模板文件

**输出示例**：

```json
[
  {
    "id": "agnes-2.0-flash",
    "name": "agnes-2.0-flash",
    "vendor": "Custom",
    "url": "https://apihub.agnes-ai.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  }
]
```

---

### MF3-05 API 配置规范范本

**必选组件**：

1. **API 端点**：

| 平台 | 模型 | 端点 | 说明 |
|------|------|------|------|
| Agnes AI | agnes-image-2.0-flash | POST https://apihub.agnes-ai.com/v1/images/generations | 图像生成 |
| Agnes AI | agnes-video-v2.0 | POST https://apihub.agnes-ai.com/v1/videos | 视频生成 |
| 智谱 BigModel | glm-4.7-flash | POST https://open.bigmodel.cn/api/paas/v4/chat/completions | 文本生成 |
| 商汤 SenseNova | sensenova-6.7-flash-lite | POST https://token.sensenova.cn/v1/chat/completions | 文本生成 |
| 小米 MIMO | mimo-v2.5-pro | POST https://token-plan-cn.xiaomimimo.com/v1/chat/completions | 文本生成 |
| 美团 LongCat | LongCat-2.0-Preview | POST https://api.longcat.chat/openai/chat/completions | 文本生成 |

2. **请求参数**：

**Agnes AI 图像生成**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 固定值 `agnes-image-2.0-flash` |
| prompt | string | 是 | 图像描述文本 |
| size | string | 否 | 分辨率，如 `1024x768`、`1024x1024` |
| extra_body | object | 否 | 附加参数容器 |
| extra_body.image | string[] | 否 | 输入图片 URL 或 Data URI 数组 |
| extra_body.response_format | string | 否 | `url` 或 `b64_json`，**禁止放顶层** |

**Agnes AI 视频生成**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | `agnes-video-v2.0` |
| prompt | string | 是 | 视频描述文本 |
| image | string | 图生视频时是 | 单张图片 URL |
| width | integer | 否 | 视频宽度，默认 1152 |
| height | integer | 否 | 视频高度，默认 768 |
| num_frames | integer | 否 | 总帧数，按分辨率受限（见下方帧数限制表），需满足 8n+1，默认 121 |
| frame_rate | integer | 否 | 帧率 1-60，默认 24 |

**视频生成帧数限制（按分辨率）**：

| 分辨率 | 最大帧数 | 24fps 时长 |
|--------|---------|-----------|
| 1080p (所有宽高比) | 169 帧 | ~7 秒 |
| 720p (所有宽高比) | 409 帧 | ~17 秒 |
| 480p (所有宽高比) | 961 帧 | ~40 秒 |

3. **约束条件**：

**Agnes AI 图像生成**：
- response_format 必须放在 extra_body 中，放顶层会 400 错误
- 图生图不需要传 tags
- URL 必须是公网可访问的 HTTPS 地址

**Agnes AI 视频生成**：
- num_frames 按分辨率受限：1080p ≤169、720p ≤409、480p ≤961，需满足 8n+1
- frame_rate 范围 1-60
- 视频生成为异步任务，需轮询查询结果
- **轮询使用 `task_id`**（格式 `task_xxx`），**不要使用** API 返回的 `video_id`（litellm 包装 ID，无法用于轮询）
- 图生视频时 `image` 参数必须是公网可访问的 URL，本地文件需先上传到文件托管服务（脚本已内置自动上传逻辑）
- 创建任务建议超时 600 秒，轮询超时 30 秒并自动重试
- 推荐轮询间隔 10 秒，生成通常需要 3-10 分钟

**可选组件**：

**调用示例**：

**Agnes AI 图像生成**：

```bash
curl -X POST https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "prompt": "A glass cube on white background, soft shadows, high detail",
    "size": "1024x768",
    "extra_body": {
      "response_format": "url"
    }
  }'
```

**Agnes AI 视频生成**：

```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "Astronaut walking on red desert, cinematic tracking shot",
    "width": 1152,
    "height": 768,
    "num_frames": 121,
    "frame_rate": 24
  }'
```

**错误处理**：

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 400 | 请求参数错误 | 检查参数格式，确保 response_format 放在 extra_body 中 |
| 401 | 未授权 | 检查 API Key 是否有效 |
| 404 | 资源不存在 | 检查接口地址是否正确 |
| 500 | 服务器错误 | 稍后重试或联系技术支持 |

**组装顺序**：API 识别 → 参数配置 → 约束设置 → 验证测试

**约束**：API 配置必须准确无误，约束条件必须明确

**格式**：API 配置文档（Markdown）

**输出示例**：

```markdown
## Agnes AI API 配置规范

## 图像生成 API
- 端点：POST https://apihub.agnes-ai.com/v1/images/generations
- 模型：agnes-image-2.0-flash
- 约束：response_format 必须放在 extra_body 中

## 视频生成 API
- 端点：POST https://apihub.agnes-ai.com/v1/videos
- 模型：agnes-video-v2.0
- 约束：num_frames 必须 ≤ 441 且满足 8n+1
```
