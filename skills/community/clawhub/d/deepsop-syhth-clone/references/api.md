# Voice Clone API 详细文档

## 基础信息

**Base URL:** `https://ai.deepsop.com/prod-api`

**认证方式:** 所有请求需要在 Header 中携带 `x-api-key: <your_api_key>`

**API Key 获取:**
- **已有账号** → 前往 [https://ai.deepsop.com/login?source=4](https://ai.deepsop.com/login?source=4) 登录获取
- **没有账号** → 前往 [https://ai.deepsop.com/register?source=4](https://ai.deepsop.com/register?source=4) 注册后获取
登录后在复制您的 API Key（`sk-` 开头）。

---

## 1. 查询音色列表

获取当前用户可用的所有音色。

### 请求

```http
GET /ai/voice/clone/list?pageNum=1&pageSize=10
x-api-key: sk-your_api_key_here
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNum | int | 否 | 页码，默认 1 |
| pageSize | int | 否 | 每页数量，默认 10 |

### 响应示例

```json
{
  "total": 3,
  "rows": [
    {
      "id": 10,
      "deleted": 0,
      "createUser": "1",
      "createTime": "2026-03-16 20:17:34",
      "updateUser": "1",
      "updateTime": "2026-03-16 20:17:40",
      "userId": 1,
      "deptId": 100,
      "name": "蔡总的音色",
      "voiceId": "cosyvoice-v3.5-plus-deepsop-2689c5e102004891ac158340547fa44a",
      "targetModel": "cosyvoice-v3.5-plus",
      "prefix": "DeepSop",
      "audioUrl": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/timbre/100/1773663443610_c8733ade.mp3",
      "status": "OK",
      "remark": null
    }
  ],
  "code": 200,
  "msg": "查询成功"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 音色 ID，用于语音合成 |
| name | string | 音色名称 |
| voiceId | string | 声音唯一标识 |
| targetModel | string | 使用的模型，如 cosyvoice-v3.5-plus |
| prefix | string | 前缀标识 |
| audioUrl | string | 音色样本音频 URL |
| status | string | 状态：OK=可用，DEPLOYING=部署中 |
| createTime | string | 创建时间 |

### 状态码

| 状态 | 说明 |
|------|------|
| OK | 音色可用，可用于语音合成 |
| DEPLOYING | 音色正在部署，暂不可用 |
| 其他 | 音色不可用 |

---

## 2. 创建新音色

上传音频文件创建新的音色克隆。

### 请求

```http
POST /ai/voice/clone/sync/create
x-api-key: sk-your_api_key_here
Content-Type: application/json
```

### 请求体

```json
{
  "name": "测试音色",
  "prefix": "DeepSop",
  "audioUrl": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/timbre/100/xxx.mp3",
  "remark": null
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 音色名称 |
| prefix | string | 否 | 前缀标识，默认 "DeepSop" |
| audioUrl | string | 是 | 音频文件 OSS URL |
| remark | string | 否 | 备注信息 |

### 响应示例

```json
{
  "msg": "操作成功",
  "code": 200,
  "data": {
    "id": 12,
    "deleted": 0,
    "createUser": "1",
    "createTime": "2026-04-02 13:59:44",
    "updateUser": "1",
    "updateTime": "2026-04-02 13:59:50",
    "userId": 1,
    "deptId": 100,
    "name": "测试 11",
    "voiceId": "cosyvoice-v3.5-plus-deepsop-19ce1b6d3dce43ceabae661e6c3ead0e",
    "targetModel": "cosyvoice-v3.5-plus",
    "prefix": "DeepSop",
    "audioUrl": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/timbre/100/1775109577087_813ce67c.mp3",
    "status": "OK",
    "remark": null
  }
}
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 新创建的音色 ID |
| voiceId | string | 声音唯一标识 |
| status | string | 初始状态，通常为 OK 或 DEPLOYING |

---

## 3. 语音合成

使用指定音色合成语音。

### 请求

```http
POST /ai/voice/clone/synthesize
x-api-key: sk-your_api_key_here
Content-Type: application/json
```

### 请求体

```json
{
  "text": "大家好啊，我是库阔 AI 的销售经理王志勇",
  "id": 10
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 要合成的文本内容 |
| id | int | 是 | 音色 ID（从音色列表获取） |

### 响应示例

```json
{
  "msg": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/voice_clone/1/3c48a33a-8bdb-4272-81c4-b5607a19928c.mp3",
  "code": 200
}
```

### 响应说明

- `msg` 字段包含合成后的音频文件 URL
- 可直接访问该 URL 播放或下载音频

---

## 4. 文件上传

将本地文件上传到 OSS 获取可访问 URL。

### 请求

```http
POST /system/fileUpload/upload
x-api-key: sk-your_api_key_here
Content-Type: multipart/form-data
```

### 请求体 (form-data)

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 要上传的文件 |

### cURL 示例

```bash
curl --location --request POST 'https://ai.deepsop.com/prod-api/system/fileUpload/upload' \
--header 'x-api-key: sk-your_api_key_here' \
--form 'file=@"C:\Users\admin\Downloads\voice.mp3"'
```

### 响应示例

```json
{
  "msg": "操作成功",
  "fileName": "1773660081867_f4eec03c.mp3",
  "code": 200,
  "url": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/material/100/6f5a70ba-cb60-4474-a579-ef5326037b5c.mp3"
}
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| fileName | string | 上传后的文件名 |
| url | string | OSS 可访问 URL |

---

## 错误码说明

| code | 说明 |
|------|------|
| 200 | 操作成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败（API Key 无效） |
| 403 | 权限不足 |
| 500 | 服务器内部错误 |

---

## 最佳实践

### 1. 音色选择

- 优先选择 `status: "OK"` 的音色
- 避免使用 `DEPLOYING` 状态的音色（可能失败）

### 2. 音频上传

- 推荐 MP3 格式
- 时长建议 10-60 秒
- 清晰的人声录音效果最佳

### 3. 文本合成

- 文本长度控制在 500 字以内
- 支持中文、英文混合
- 标点符号会影响停顿

### 4. 错误处理

- 检查响应 `code` 是否为 200
- 音色创建后可能需要等待部署完成
- 网络超时建议重试机制
