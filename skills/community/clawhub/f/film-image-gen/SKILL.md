# image-gen - 影视概念图生成技能

_通过优创 AIGC API (api.lk888.ai) 生成影视概念图、海报、分镜图、角色设计等视觉内容_

---

## 触发条件

用户要求生成图片、画图、出图、设计概念图/海报/插画/分镜/角色设定等视觉内容时触发。

---

## API 配置

| 配置项 | 值 |
|--------|-----|
| Base URL | `https://api.lk888.ai` |
| Auth Header | `Authorization: Bearer {api_key}` |
| API Key（主） | `sk-790…9616` |
| API Key（备） | `sk-4d6…5fe9` |
| 其他鉴权方式 | `x-api-key` / `x-goog-api-key` / URL 参数 `?key=` |

---

## 调用流程（两步异步 / 同步直返）

### 第 1 步：提交任务

```
POST https://api.lk888.ai/v1/media/generate
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "model": "模型名",
  "params": {
    "prompt": "提示词",
    ...其他参数
  }
}
```

**成功响应分两种**：

**A. 同步直返**（部分参数组合直接返回 URL）：
```json
{"created":1730000000,"data":[{"url":"https://example.com/generated/output.png"}],"usage":{"input_tokens":24,"output_tokens":6144,"total_tokens":6168}}
```

**B. 异步任务**（返回 task_id）：
```json
{"code":200,"data":{"task_id":123456,"成功数量":1},"msg":"任务创建成功"}
```

⚠️ **两种都要处理**：优先检查 `data.url` 或 `data[0].url`，有则直接拿结果；否则走异步轮询。

### 第 2 步：轮询结果（仅异步任务需要）

```
GET https://api.lk888.ai/v1/media/status?task_id={task_id}
Authorization: Bearer {api_key}
```

响应：
```json
{"task_id":123456,"state":"success","status":"已完成","status_group":"已完成","is_final":true,"progress":"100","result_url":"https://cdn.example.com/output.png","result_type":"image","error":"","cost":0.23}
```

**终态判定规则（AI 接入必看）**：
- `is_final === true` → 任务终态，停止轮询
- `state === 'success'` → 成功，从 `result_url` 拿结果
- `state === 'failed'` → 失败（已自动退款）
- `state` 固定 4 档：`pending / running / success / failed`
- `status / status_group` 是中文展示字段，只给人看，**不要用来写业务判断**
- **轮询间隔**：每 3~5 秒一次，图片任务通常 20 秒~2 分钟
- **超时策略**：超过 10 分钟未终态则停止轮询

---

## 可用模型

### 1. gpt-image-2（GPT Image 2）

| 参数 | 类型 | 必填 | 说明 | 选项 |
|------|------|------|------|------|
| prompt | textarea | ✅ | 提示词 | — |
| images | upload | ❌ | 参考图 URL（1-10 张） | URL 字符串或数组 |
| size | select | 推荐 `auto` | 图片尺寸 | `auto` / `1024x1024` / `1024x1536` / `1536x1024` / `960x1280` / `1280x960` / `1088x1920` / `1920x1088` / `2048x2048` / `2048x3072` / `3072x2048` / `1920x2560` / `2560x1920` / `1440x2560` / `2560x1440` / `2880x2880` / `2304x3456` / `3456x2304` / `2400x3200` / `3200x2400` / `2160x3840` / `3840x2160` |
| quality | select | ❌ | 图片质量 | `auto` / `high` / `medium` / `low` |

**特点**：OpenAI 最新一代图像模型，语义理解与细节表现更强，支持文生图与图生图。输入提示：描述画面中的物体、风格及文字排版，注重指令精准与细节还原。推荐 `size: auto` 由模型自动决定。

### 1.5. gpt-image-2-guan（GPT Image 2 官转）

| 参数 | 类型 | 必填 | 说明 | 选项 |
|------|------|------|------|------|
| prompt | textarea | ✅ | 提示词 | — |
| images | upload | ❌ | 参考图 URL（1-10 张） | URL 字符串或数组 |
| size | select | ❌ | 图片尺寸 | 同 gpt-image-2 |
| quality | select | ❌ | 图片质量 | `auto` / `high` / `medium` / `low` |

**特点**：OpenAI 官方直连通道，按 token 精准计费、多退少补；文生图与多图参考编辑兼备，画质与稳定性全面拉满。商业级描述结构：《主体 + 材质 + 场景 + 光影 + 镜头 + 风格》。

### 2. gemini-3-pro-image-preview（Nano Banana Pro）

| 参数 | 类型 | 必填 | 说明 | 选项 |
|------|------|------|------|------|
| prompt | textarea | ✅ | 提示词 | — |
| images | upload | ❌ | 参考图 URL（1-14 张） | URL 字符串或数组 |
| aspectRatio | select | ✅ | 宽高比 | `1:1` / `2:3` / `3:2` / `3:4` / `4:3` / `4:5` / `5:4` / `9:16` / `16:9` / `21:9` |
| imageSize | select | ✅ | 分辨率 | `1K` / `2K` / `4K` |

**特点**：谷歌 2025 年最新超高清图像模型，拥有目前最强的文字渲染能力，擅长生成 8K 分辨率的微距摄影、皮肤质感与复杂排版设计。支持同步/流式 Gemini 官方接口格式。

### 3. gemini-3.1-flash-image-preview（Nano Banana 2）

| 参数 | 类型 | 必填 | 说明 | 选项 |
|------|------|------|------|------|
| prompt | textarea | ✅ | 提示词 | — |
| images | upload | ❌ | 参考图 URL（1-14 张） | URL 字符串或数组 |
| aspectRatio | select | ✅ | 宽高比 | `1:1` / `2:3` / `3:2` / `3:4` / `4:3` / `4:5` / `5:4` / `9:16` / `16:9` / `21:9` / `1:4` / `4:1` / `1:8` / `8:1` |
| imageSize | select | ✅ | 分辨率 | `0.5K` / `1K` / `2K` / `4K` |
| thinkingLevel | select | ❌ | 思考等级 | `minimal` / `high` |
| web_search | switch | ❌ | 联网搜索 | `true` / `false` |

**特点**：Nano Banana Pro 高速版，针对速度和高用量场景优化。支持联网搜索生图、Google 图片搜索接地、512px 快速预览，新增 1:4/4:1/1:8/8:1 超宽比例。

### 4. mj_imagine（Midjourney）

| 参数 | 类型 | 必填 | 说明 | 选项 |
|------|------|------|------|------|
| prompt | textarea | ✅ | 提示词 | 可加 MJ 参数如 `--ar 16:9 --v 6.0 --style raw` |
| images | upload | ❌ | 参考图 URL（1-4 张） | URL 字符串或数组 |
| botType | select | ✅ | 模型风格 | `MID_JOURNEY` / `NIJI_JOURNEY` |
| aspectRatio | select | ✅ | 图片比例 | `1:1` / `16:9` / `9:16` / `4:3` / `3:4` / `3:2` / `2:3` / `4:5` / `5:4` / `21:9` |
| quality | select | ❌ | 质量 | `0.25` / `0.5` / `1` / `2` |
| stylize | select | ❌ | 风格化强度 | `0`（写实）→ `1000`（极度艺术化） |
| chaos | select | ❌ | 变化多样性 | `0`（稳定一致）→ `100`（差异很大） |
| style | select | ❌ | 风格模式 | ``（默认）/ `raw` |

**特点**：全球最火的 AI 图像生成模型，以极高的艺术性和美感著称。擅长电影级概念艺术、插画、海报、氛围图。支持 MJ 和 Niji 双模式。

### 5. grok-4.1-image（xAI）

| 参数 | 类型 | 必填 | 说明 | 选项 |
|------|------|------|------|------|
| prompt | textarea | ✅ | 提示词 | — |
| images | upload | ❌ | 参考图 URL（最多 1 张） | URL 字符串 |
| size | select | ✅ | 图片尺寸 | `1024x1024` / `1080x1080` / `1200x1200` / `2048x2048` / `2160x2160` / `1280x720` / `1366x768` / `1600x900` / `1920x1080` / `2048x1152` / `2560x1440` / `1024x768` / `1280x960` / `2048x1536` / `720x1280` / `768x1366` / `900x1600` / `1080x1920` / `1440x2560` |

**特点**：xAI 旗下图像模型，基于 Grok 4.1 架构，支持文生图和图片编辑，每次生成固定返回 2 张图片，19 种尺寸覆盖正方形、横版、竖版。

---

## 模型选择建议

| 场景 | 推荐模型 |
|------|----------|
| 含文字的图（海报/排版/LOGO） | gemini-3-pro-image-preview |
| 写实/产品/商业图 | gpt-image-2 |
| 艺术感/概念艺术/插画 | mj_imagine |
| 快速出图/超宽比例 | gemini-3.1-flash-image-preview |
| 需要联网搜索实时信息 | gemini-3.1-flash-image-preview |
| 最高画质（4K 微距/皮肤质感） | gemini-3-pro-image-preview |
| 精准计费/稳定性优先 | gpt-image-2-guan |

### 影视概念图推荐

| 场景 | 推荐模型 | 推荐参数 |
|------|----------|----------|
| 角色概念设计 | gpt-image-2 | size: `1024x1536`（竖构图）, quality: `high` |
| 场景/环境概念图 | gemini-3-pro-image-preview | aspectRatio: `16:9`, imageSize: `2K` |
| 分镜/故事板 | gemini-3.1-flash-image-preview | aspectRatio: `16:9`, imageSize: `1K`（快速） |
| 电影海报 | gemini-3-pro-image-preview | aspectRatio: `2:3`, imageSize: `4K` |
| 道具/服装设计 | gpt-image-2 | size: `1024x1024`, quality: `high` |
| 氛围/Mood Board | gemini-3-pro-image-preview | aspectRatio: `21:9`, imageSize: `2K` |
| 概念艺术/插画 | mj_imagine | aspectRatio: `16:9`, quality: `1`, stylize: `250` |

---

## 默认参数策略

用户未指定参数时，使用以下默认值：

| 参数 | gpt-image-2 | gemini-3-pro | gemini-3.1-flash |
|------|-------------|--------------|------------------|
| size/aspectRatio | `auto` | `1:1` | `1:1` |
| quality | `auto` | — | — |
| imageSize | — | `2K` | `2K` |

---

## 执行步骤

1. **理解需求**：解析用户想要的画面内容、风格、尺寸
2. **选择模型**：根据场景选择最合适的模型（或询问用户）
3. **构建请求**：组装 prompt 和 params，必填参数必须包含
4. **提交任务**：调用 POST `/v1/media/generate`，获取 task_id 或直接返回 URL
5. **处理响应**：
   - 如果响应包含 `data.url` 或 `data[0].url` → 直接拿结果
   - 如果响应包含 `data.task_id` → 走异步轮询
6. **轮询结果**（异步）：每 3~5 秒调用 GET `/v1/media/status`，直到 `is_final=true`
7. **返回图片**：将 result_url 发送给用户，同时告知花费和耗时

---

## Prompt 编写技巧

- **结构**：《主体 + 材质 + 场景 + 光影 + 镜头 + 风格》
- **含文字的图**用 gemini-3-pro，用引号包裹要渲染的文字
- 中文 prompt 效果良好，但英文对 OpenAI 模型更稳定
- 越具体的描述效果越好，避免模糊词

### 影视概念图 Prompt 模板

```
[主体描述]，[材质/服装细节]，[场景环境]，[光影氛围]，[镜头角度/景别]，[艺术风格/参考导演]，cinematic lighting, 8k resolution, concept art
```

**示例**：
```
一位中年男侦探站在雨夜的上海弄堂口，穿着深灰色风衣，手里拿着怀表，霓虹灯映照在水洼中反射出紫色和橙色的光，侧面45度中景，赛博朋克风格，电影级光影，概念艺术
```

---

## 错误处理

- **任务失败**（`state === 'failed'` 或 error 非空）→ 告知用户错误信息，询问是否重试（已自动退款）
- **超时**：超过 10 分钟未终态 → 提示用户稍后用 task_id 手动查询
- **API Key 失效**：提示用户更新 API Key
- **401 Unauthorized**：主 Key 失败自动切换备用 Key

---

## 辅助脚本

使用 `scripts/generate-image.ps1` 执行 API 调用和轮询。

用法：
```powershell
# 基础用法
.\generate-image.ps1 -Prompt "描述"

# 指定模型
.\generate-image.ps1 -Prompt "描述" -Model "gpt-image-2"

# 指定尺寸/比例
.\generate-image.ps1 -Prompt "描述" -Size "1024x1536"
.\generate-image.ps1 -Prompt "描述" -AspectRatio "16:9" -ImageSize "2K"

# 带参考图
.\generate-image.ps1 -Prompt "描述" -ImageUrl "https://..."
```

---

_版本：2.0.0 | API: 优创 AIGC (api.lk888.ai) | 更新：2026-06-07_
