## MF3 配置生成域范本

### MF3-01 API Key 生成范本

**必选组件**：

1. **平台后台网址**：

| 平台 | 后台网址 | 说明 |
|------|---------|------|
| Agnes AI | https://platform.agnes-ai.com/settings/apiKeys | Sapiens AI 平台 |
| 智谱 BigModel | https://open.bigmodel.cn/apikey/platform | 智谱平台 |
| 商汤 SenseNova | https://platform.sensenova.cn/console/keys | 商汤平台 |
| 小红书 dots | https://dots.ai/platform/apikeys | dots studio |
| 美团 LongCat | https://longcat.chat/platform/api_keys | 美团平台 |
| 小米 MIMO | https://platform.xiaomimimo.com/console/api-keys | 小米平台 |

2. **API Key 生成步骤**：

1. 访问平台后台网址：{后台网址}
2. 登录账号
3. 进入 API Key 管理页面
4. 点击"生成 API Key"按钮
5. 复制生成的 API Key

3. **API Key 保存**：

- **保存位置**：`~/.free-model-config/models.json`
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
- 更换时需要更新 `~/.free-model-config/models.json` 中的配置

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
- 保存位置：~/.free-model-config/models.json
- 保存格式：
  ```json
  {
    "id": "agnes-3.0-flash",
    "name": "agnes-3.0-flash",
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
- 更换时需要更新 ~/.free-model-config/models.json 中的配置
```

---

### MF3-02 接口配置范本

**必选组件**：

1. **接口地址**：

| 平台 | 接口地址 | 说明 |
|------|---------|------|
| Agnes AI | https://apihub.agnes-ai.com/v1 | 文本/图像/视频统一入口 |
| 智谱 BigModel | https://open.bigmodel.cn/api/paas/v4 | 文本生成接口 |
| 商汤 SenseNova | https://token.sensenova.cn/v1 | 文本生成接口 |
| 小红书 dots | https://note3-prev-api.askdiandian.com/v1 | OpenAI 兼容（认证头 api-key） |
| 美团 LongCat | https://api.longcat.chat/openai | 文本生成接口 |
| 小米 MIMO | https://token-plan-cn.xiaomimimo.com/v1 | 文本/语音接口 |

2. **接口参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 模型名称 |
| messages | array | 是 | 对话数组，如 `[{"role":"user","content":"你好"}]` |
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
    "messages": [{"role": "user", "content": "{输入文本}"}],
    "max_tokens": 100,
    "temperature": 0.7
  }
}
```

> 上面 `max_tokens` / `temperature` 为示例值，按实际需求替换（保持 JSON 可解析）。

**可选组件**：

**接口测试**：

```bash
curl -X POST {接口地址} \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "{模型名称}",
    "messages": [{"role": "user", "content": "测试输入"}],
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
    "model": "agnes-3.0-flash",
    "messages": [{"role": "user", "content": "测试输入"}],
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
| Agnes AI | agnes-3.0-flash（推荐）/ agnes-2.5-flash / agnes-image-2.5-flash / agnes-video-2.5-flash | 文本 / 文本轻量 / 图像 / 视频 |
| 智谱 BigModel | glm-4.7-flash（推荐，免费）/ glm-4.6v-flash（免费视觉）/ glm-5.3-flash（付费） | 文本 / 多模态 |
| 商汤 SenseNova | sensenova-6.8-flash（推荐）/ sensenova-6.8-flash-lite / sensenova-u1.5-fast / deepseek-flash / glm-5.2 / kimi-k3 | 多模态对话 / 轻量 / 图像 / 推理 |
| 小红书 dots | dots3-note-prev（推荐） | 512K 长上下文多模态 |
| 美团 LongCat | LongCat-2.5（推荐） | 文本生成 / 视觉理解 |
| 小米 MIMO | mimo-v2.6-pro（推荐）/ mimo-v2.6-flash / mimo-v2.5-asr / mimo-v2.5-tts 系列 | 文本全模态 / 语音识别 / 语音合成 |

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

配置文件位置：`~/.free-model-config/models.json`

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
    "messages": [{"role": "user", "content": "测试输入"}],
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
  "id": "agnes-3.0-flash",
  "name": "agnes-3.0-flash",
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

### MF3-04 通用配置模板范本

**必选组件**：

1. **环境变量模板**（推荐，任何调用方可用）：

```bash
# 按需填写，调用方或脚本从环境变量读取
export AGNES_API_KEY="sk-..."
export ZHIPU_API_KEY="..."
export SENSENOVA_API_KEY="..."
export DOTS_API_KEY="..."
export LONGCAT_API_KEY="..."
export MIMO_API_KEY="..."

# 可选：自定义通用台账路径（默认 ~/.free-model-config/models.json）
export FREE_MODEL_CONFIG="$HOME/.free-model-config/models.json"
```

> Windows 下用 `$env:AGNES_API_KEY="..."`（PowerShell）或 `set AGNES_API_KEY=...`（cmd）；需要持久化可写入用户环境变量。

2. **通用 JSON 台账**（字段可裁剪，按目标格式映射）：

以下是 `%USERPROFILE%\.free-model-config\models.json` 的模板内容：

```json
[
  {
    "id": "agnes-3.0-flash",
    "name": "agnes-3.0-flash",
    "vendor": "Custom",
    "url": "https://apihub.agnes-ai.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "agnes-2.5-flash",
    "name": "agnes-2.5-flash",
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
    "id": "glm-4.6v-flash",
    "name": "glm-4.6v-flash",
    "vendor": "Custom",
    "url": "https://open.bigmodel.cn/api/paas/v4",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "glm-5.3-flash",
    "name": "glm-5.3-flash",
    "vendor": "Custom",
    "url": "https://open.bigmodel.cn/api/paas/v4",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "sensenova-6.8-flash",
    "name": "sensenova-6.8-flash",
    "vendor": "Custom",
    "url": "https://token.sensenova.cn/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "sensenova-6.8-flash-lite",
    "name": "sensenova-6.8-flash-lite",
    "vendor": "Custom",
    "url": "https://token.sensenova.cn/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "sensenova-u1.5-fast",
    "name": "sensenova-u1.5-fast",
    "vendor": "Custom",
    "url": "https://token.sensenova.cn/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": false,
    "supportsImages": true,
    "supportsReasoning": false,
    "useCustomProtocol": false
  },
  {
    "id": "deepseek-flash",
    "name": "deepseek-flash",
    "vendor": "Custom",
    "url": "https://token.sensenova.cn/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "glm-5.2",
    "name": "glm-5.2",
    "vendor": "Custom",
    "url": "https://token.sensenova.cn/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": false,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "kimi-k3",
    "name": "kimi-k3",
    "vendor": "Custom",
    "url": "https://token.sensenova.cn/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "dots3-note-prev",
    "name": "dots3-note-prev",
    "vendor": "Custom",
    "url": "https://note3-prev-api.askdiandian.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "LongCat-2.5",
    "name": "LongCat-2.5",
    "vendor": "Custom",
    "url": "https://api.longcat.chat/openai",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "mimo-v2.6-pro",
    "name": "mimo-v2.6-pro",
    "vendor": "Custom",
    "url": "https://token-plan-cn.xiaomimimo.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "mimo-v2.6-flash",
    "name": "mimo-v2.6-flash",
    "vendor": "Custom",
    "url": "https://token-plan-cn.xiaomimimo.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": true,
    "supportsImages": true,
    "supportsReasoning": true,
    "useCustomProtocol": false
  },
  {
    "id": "mimo-v2.5-asr",
    "name": "mimo-v2.5-asr",
    "vendor": "Custom",
    "url": "https://token-plan-cn.xiaomimimo.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": false,
    "supportsImages": false,
    "supportsReasoning": false,
    "useCustomProtocol": false
  },
  {
    "id": "mimo-v2.5-tts",
    "name": "mimo-v2.5-tts",
    "vendor": "Custom",
    "url": "https://token-plan-cn.xiaomimimo.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": false,
    "supportsImages": false,
    "supportsReasoning": false,
    "useCustomProtocol": false
  },
  {
    "id": "mimo-v2.5-tts-voiceclone",
    "name": "mimo-v2.5-tts-voiceclone",
    "vendor": "Custom",
    "url": "https://token-plan-cn.xiaomimimo.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": false,
    "supportsImages": false,
    "supportsReasoning": false,
    "useCustomProtocol": false
  },
  {
    "id": "mimo-v2.5-tts-voicedesign",
    "name": "mimo-v2.5-tts-voicedesign",
    "vendor": "Custom",
    "url": "https://token-plan-cn.xiaomimimo.com/v1",
    "apiKey": "your_api_key_here",
    "supportsToolCall": false,
    "supportsImages": false,
    "supportsReasoning": false,
    "useCustomProtocol": false
  }
]
```

> ⚠️ `dots3-note-prev` 只接受请求头 `api-key: KEY`，不认 `Authorization: Bearer`。若调用方只发 Bearer，会返回 401，需在请求头里补 `api-key`，或改用支持自定义头的调用方式。该模型为 512K 上下文、预览期限时免费。

**字段映射**（台账字段与通用含义一一对应，按目标格式映射即可）：

| 通用含义 | 台账字段 | 说明 |
|----------|---------|------|
| 模型 ID | `id` / `name` | 填写模型名时用同值 |
| 接口地址 | `url` | 即 base_url |
| 密钥 | `apiKey` | 等价于 api_key |
| 能力开关 | `supportsToolCall` / `supportsImages` / `supportsReasoning` | 不支持可省略或置 false |

3. **使用说明**：

1. 选一种形态：写入环境变量，或复制 JSON 台账
2. 将 `your_api_key_here` 替换为从对应平台后台网址生成的 API Key（或让脚本从环境变量读取）
3. 台账保存到 `~/.free-model-config/models.json`（Windows 为 `%USERPROFILE%\.free-model-config\models.json`）

4. **保存位置**：

默认位置：`~/.free-model-config/models.json`，可用 `FREE_MODEL_CONFIG` 覆盖。

5. **写入既有配置文件**：

用 `scripts/apply_config.py` 把台账写入目标文件；默认预演，`--write` 才落盘（自动备份 + 回读校验）：

```bash
# 同构 JSON 数组
python scripts/apply_config.py --path /path/to/target.json
python scripts/apply_config.py --path /path/to/target.json --write

# 数组在对象内、字段名不同
python scripts/apply_config.py --path /path/to/target.json --root models \
  --map url=base_url,apiKey=api_key,id=model --key model --write
```

- 合并策略：按 `id` 命中即字段级合并（保留未知字段），未命中追加；`--mode replace` 才整段替换
- 目标不存在时按 `--root` 结构新建；格式支持 `json` 与 `yaml`（yaml 需 pyyaml）

**可选组件**：

**模板验证**：

- [ ] 模板格式正确
- [ ] 所有模型配置完整
- [ ] API Key 已替换

**模板测试**：

```bash
## 测试 Agnes AI 模型
curl -X POST https://apihub.agnes-ai.com/v1/chat/completions \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-3.0-flash",
    "messages": [{"role": "user", "content": "测试输入"}],
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
    "id": "agnes-3.0-flash",
    "name": "agnes-3.0-flash",
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
| Agnes AI | agnes-3.0-flash / agnes-2.5-flash | POST https://apihub.agnes-ai.com/v1/chat/completions | 文本生成 |
| Agnes AI | agnes-image-2.5-flash | POST https://apihub.agnes-ai.com/v1/images/generations | 图像生成 / 编辑 |
| Agnes AI | agnes-video-2.5 / -flash | POST https://apihub.agnes-ai.com/v1/videos | 视频生成（异步） |
| Agnes AI | agnes-video-2.5 | GET https://apihub.agnes-ai.com/agnesapi?video_id=&model_name= | 视频结果轮询 |
| 智谱 BigModel | glm-4.7-flash / glm-5.3-flash | POST https://open.bigmodel.cn/api/paas/v4/chat/completions | 文本生成 |
| 智谱 BigModel | cogview-3-flash | POST https://open.bigmodel.cn/api/paas/v4/images/generations | 图像生成 |
| 智谱 BigModel | cogvideox-flash | POST https://open.bigmodel.cn/api/paas/v4/videos/generations | 视频生成 |
| 商汤 SenseNova | sensenova-6.8-flash | POST https://token.sensenova.cn/v1/chat/completions | 多模态对话 |
| 商汤 SenseNova | sensenova-u1.5-fast | POST https://token.sensenova.cn/v1/images/generations | 图像生成/编辑 |
| 商汤 SenseNova | deepseek-flash / glm-5.2 / kimi-k3 | POST https://token.sensenova.cn/v1/chat/completions | 对话推理 |
| 小红书 dots | dots3-note-prev | POST https://note3-prev-api.askdiandian.com/v1/chat/completions | 长上下文对话（头 `api-key`） |
| 美团 LongCat | LongCat-2.5 | POST https://api.longcat.chat/openai/chat/completions | 文本生成 |
| 小米 MIMO | mimo-v2.6-pro / mimo-v2.6-flash | POST https://token-plan-cn.xiaomimimo.com/v1/chat/completions | 文本/全模态 |
| 小米 MIMO | mimo-v2.5-asr | POST https://token-plan-cn.xiaomimimo.com/v1/audio/transcriptions | 语音识别 |
| 小米 MIMO | mimo-v2.5-tts / -voiceclone / -voicedesign | POST https://token-plan-cn.xiaomimimo.com/v1/audio/speech | 语音合成 |

2. **请求参数**：

**Agnes AI 图像生成**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 固定值 `agnes-image-2.5-flash` |
| prompt | string | 是 | 图像描述文本 |
| size | string | 是 | 输出档位 `1K` / `2K` / `3K` / `4K`；旧式像素值兼容但可能被归一化 |
| ratio | string | 否 | `1:1`、`3:4`、`4:3`、`16:9`、`9:16`、`2:3`、`3:2`、`21:9` |
| extra_body.image | string[] | 否 | 输入图片 URL 或 Data URI 数组（图生图/多图合成） |
| extra_body.response_format | string | 否 | `url` 或 `b64_json`，**禁止放顶层** |
| return_base64 | boolean | 否 | 文生图需要返回 Base64 时置 true |

**Agnes AI 视频生成**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | `agnes-video-2.5` 或 `agnes-video-2.5-flash` |
| prompt | string | 是 | 视频描述文本；reference 模式用 `<Picture 1>`/`<Audio 1>`/`<Video 1>` 指代素材 |
| mode | string | 是 | `text` / `keyframe` / `reference` |
| seconds | string | 否 | 时长 `"4"`–`"12"`，默认 `"5"` |
| size | string | 否 | `720P` / `1080P` / `1K` / `2K`；不接受像素值 |
| aspect_ratio | string | 否 | 默认 `16:9`；不支持 `auto` |
| seed | integer | 否 | 随机种子 |
| first_frame / last_frame | string | 否 | keyframe 模式的首/尾帧公网 URL |
| images / audios / videos[] | array | 否 | reference 模式；视频用 `videos[].url` |
| n | integer | 否 | 仅支持 1 |

**视频分辨率档位与计费（agnes-video-2.5）**：

| 档位 | 单价（list） | 说明 |
|------|------------|------|
| 720P | $0.025 / 秒 | flash 版当前限时 $0 |
| 1080P | $0.040 / 秒 | |
| 1K | $0.040 / 秒 | |
| 2K | $0.055 / 秒 | |

**已废弃参数**：`width`、`height`、`fps`、`num_frames`、`quality`、`num_inference_steps` 传入即 400；旧的「帧数上限 / 8n+1」规则不再适用。

3. **约束条件**：

**Agnes AI 图像生成**：
- `response_format` 必须放在 `extra_body` 中，放顶层会 400 错误
- 图生图不需要传 `tags`
- URL 必须是公网可访问的 HTTPS 地址
- 要精确画幅用 `size` 档位 + `ratio`，不要传 1920×1080 这类像素值（会被归一化）

**Agnes AI 视频生成**：
- `seconds` 取 `"4"`–`"12"`（字符串），`size` 只接受 720P/1080P/1K/2K
- 视频生成为异步任务：先 `POST /v1/videos`，再轮询 `GET /agnesapi?video_id=<ID>&model_name=<模型>`
- 创建返回的 `id` / `task_id` 是任务号，`video_id` 才是查询凭证
- keyframe / reference 模式轮询**必须带** `model_name`；text 模式可省略
- 图生视频用 `mode=keyframe` + `first_frame`（或 `last_frame`），图片必须是公网 URL
- `mode` 与媒体字段必须匹配，否则 400（如 reference 模式却只传 first_frame）
- 创建任务超时 600 秒，轮询超时 30 秒并重试；轮询间隔 1–2 秒，生成通常 1–5 分钟

**可选组件**：

**调用示例**：

**Agnes AI 图像生成**：

```bash
curl -X POST https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.5-flash",
    "prompt": "A glass cube on white background, soft shadows, high detail",
    "size": "2K",
    "ratio": "16:9",
    "extra_body": {
      "response_format": "url"
    }
  }'
```

**Agnes AI 视频生成**：

```bash
# 1) 创建任务
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-2.5",
    "prompt": "Astronaut walking on red desert, cinematic tracking shot",
    "mode": "text",
    "seconds": "5",
    "size": "720P",
    "aspect_ratio": "16:9"
  }'

# 2) 轮询结果（keyframe/reference 模式必须带 model_name）
curl "https://apihub.agnes-ai.com/agnesapi?video_id=video_xxx&model_name=agnes-video-2.5" \
  -H "Authorization: Bearer {API_KEY}"
```

**小红书 dots 文本生成**（注意认证头）：

```bash
curl -X POST https://note3-prev-api.askdiandian.com/v1/chat/completions \
  -H "api-key: {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dots3-note-prev",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 512,
    "stream": false
  }'
```

**错误处理**：

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 400 | 请求参数错误 | 检查是否传了废弃参数（width/height/num_frames），response_format 是否在 extra_body 内，mode 与媒体字段是否匹配 |
| 401 | 未授权 | 检查 API Key；dots 平台需用 `api-key` 头而非 Bearer |
| 404 | 资源不存在 | 视频查询用 `video_id`（不是 task_id）；模型 ID 是否已停用 |
| 429 | 限流 | 指数退避重试 |
| 500 | 服务器错误 | 稍后重试或联系技术支持 |

**组装顺序**：API 识别 → 参数配置 → 约束设置 → 验证测试

**约束**：API 配置必须准确无误，约束条件必须明确

**格式**：API 配置文档（Markdown）

**输出示例**：

```markdown
## Agnes AI API 配置规范

## 图像生成 API
- 端点：POST https://apihub.agnes-ai.com/v1/images/generations
- 模型：agnes-image-2.5-flash
- 约束：response_format 必须放在 extra_body 中

## 视频生成 API
- 端点：POST https://apihub.agnes-ai.com/v1/videos
- 模型：agnes-video-2.5 / agnes-video-2.5-flash
- 约束：seconds 4–12 秒；size 仅 720P/1080P/1K/2K；width/height/num_frames 已废弃
- 轮询：GET /agnesapi?video_id=<ID>&model_name=<模型>

## 长上下文对话 API
- 端点：POST https://note3-prev-api.askdiandian.com/v1/chat/completions
- 模型：dots3-note-prev
- 约束：认证头 `api-key`；输入 + max_tokens ≤ 524288
```
