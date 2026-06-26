# API Endpoints Reference

PPT生成服务API接口文档

**重要说明**：
- **统一接口地址**：所有操作使用同一个URL
- **通过请求参数区分不同操作**
- **接口地址**: `https://ai.mingyangtek.com/aippt/api/c=15109`

**通用Header**:
```http
Content-Type: application/json
X-Userid: {sender_id}     # 用户标识
X-Sender: {sender}        # 用户名称
X-Chatid: {chat_id}       # 会话ID
X-Channel: {channel}      # 渠道（wecom/feishu/telegram等）
```

**命名规范**：
- **Header字段**：使用小写，如 `X-Userid`, `X-Chatid`
- **Body字段**：使用驼峰命名，如 `mainIdea`, `outLineTree`
- **Response字段**：使用驼峰命名，如 `mainIdea`, `outLineTree`

---

## 1. 生成大纲接口

### 请求
```http
POST https://ai.mingyangtek.com/aippt/api/c=15109
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "mainIdea": "沁园春",  // 必需 - PPT主题/主要想法（驼峰命名）
}
```

### 响应示例
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "id": "9f247d90c8044b10b46dc536bdd724e8",  // 大纲唯一标识
    "userId": null,
    "mainIdea": "沁园春",
    "markdown": "# 水浒传\n## 水浒传的文本与历史渊源\n### 水浒传的历史背景\n...",
    "outLineTree": "{\"children\":[...],\"level\":1,\"title\":\"水浒传\",\"titleBulletsListMap\":{...}}",
    "outputLanguage": "en",
    "depth": 5,
    "modelCode": "Default"
  }
}
```

**重要字段说明**：
- `code`: 状态码，200表示成功
- `message`: 消息，SUCCESS表示成功
- `data.id`: 大纲唯一标识（用于后续操作）
- `data.mainIdea`: PPT主题
- `data.markdown`: Markdown格式的内容
- `data.outLineTree`: JSON字符串格式的大纲树结构，需要解析使用

**outLineTree 解析后的结构**：
```json
{
  "children": [...],
  "level": 1,
  "title": "水浒传",
  "titleBulletsListMap": {
    "水浒传的历史背景_mypptpid_1": {
      "宋江末年农民起义": "宋江末年农民起义",
      "农民起义领袖": "农民起义领袖",
      "被压迫反抗的真实": "被压迫反抗的真实"
    },
    ...
  }
}
```

---

## 2. 编辑大纲接口

### 请求
```http
POST https://ai.mingyangtek.com/aippt/api/c=15110
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "outlineId": "9f247d90c8044b10b46dc536bdd724e8",
  "userId": "1234",
  "markDownStr": "# 水浒传\n## 水浒传的背景与起源\n### 水浒传的历史背景\n- 北宋末年社会动荡\n- 农民起义频发\n..."
}
```

**参数说明**：
- `outlineId`：大纲ID（从生成大纲接口返回的`data.id`）
- `userId`：用户ID
- `markDownStr`：完整的Markdown格式大纲内容

**注意**：
- 接口地址不同于生成大纲：`c=15110`
- 所有参数使用驼峰命名
- `markDownStr`需要包含完整的大纲结构

### 响应示例
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": "编辑成功"
}
```

**响应字段说明**：
- `code`: 状态码，200表示成功
- `message`: 消息，SUCCESS表示成功
- `data`: 返回"编辑成功"字符串

---

## 3. 查询模版列表接口

### 请求
```http
POST https://ai.mingyangtek.com/aippt/api/c=15111
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "keywords": [
    "简约风",
    "蓝色"
  ],
  "userId": "1234"
}
```

**参数说明**：
- `keywords`：标签数组，可以传多个标签（风格标签和颜色标签）
- `userId`：用户ID

**标签范围**：

**风格标签**：
- 简约风、小清新、商务风、中国风、可爱卡通
- 科技风、手绘风格、欧美风、党政风、黑板风

**颜色标签**：
- 蓝色、红色、粉色、黄色、绿色
- 橙色、黑色、白色、灰色、紫色

**注意**：
- keywords可以传多个标签
- 标签可以是风格标签、颜色标签的任意组合
- 建议使用智能标签推荐功能自动生成

### 响应示例
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": [
    {
      "templateId": "template_001",
      "templateName": "商务简约蓝",
      "templateUrl": "https://...",
      "previewUrl": "https://...",
      "keywords": ["简约风", "蓝色"]
    },
    {
      "templateId": "template_002",
      "templateName": "科技蓝调",
      "templateUrl": "https://...",
      "previewUrl": "https://...",
      "keywords": ["科技风", "蓝色"]
    }
  ]
}
```

**响应字段说明**：
- `code`: 200表示成功
- `message`: SUCCESS表示成功
- `data`: 模版列表数组
  - `templateId`: 模版ID
  - `templateName`: 模版名称
  - `templateUrl`: 模版文件URL
  - `previewUrl`: 预览URL
  - `keywords`: 模版标签

---

## 4. 提交创作PPT任务接口（异步）

### 请求
```http
POST https://ai.mingyangtek.com/aippt/api/c=15112
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "templateId": 39,
  "outlineId": "9f247d90c8044b10b46dc536bdd724e8",
  "reporter": "汇报人",
  "userId": "1234"
}
```

**参数说明**：
- `templateId`：模版ID（数字类型，从查询模版列表接口返回）
- `outlineId`：大纲ID（字符串，从生成大纲接口返回）
- `reporter`：汇报人姓名（字符串）
- `userId`：用户ID

**注意**：
- 这是异步接口，提交后会立即返回任务ID
- PPT生成需要一定时间，需要轮询查询状态
- `templateId`是数字类型，不是字符串

### 响应示例
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "id": 2086770
  }
}
```

**响应字段说明**：
- `code`: 200表示成功
- `message`: SUCCESS表示成功
- `data.id`: PPT任务ID（数字类型，用于查询生成状态）

**注意**：返回的是`id`字段，用于后续查询任务状态

---

## 5. 查询PPT生成结果接口

### 请求
```http
POST https://ai.mingyangtek.com/aippt/api/c=15113
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "pptId": 2086770,
  "userId": "1234"
}
```

**参数说明**：
- `pptId`：PPT任务ID（数字类型，从提交任务接口返回的`data.id`）
- `userId`：用户ID

**注意**：
- PPT生成需要一定时间，需要轮询查询
- 建议5-10秒查询一次
- 最多查询60次（约10分钟）

### 响应示例

**生成中**：
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "fileurl": "",
    "status": 0
  }
}
```

**生成完成**：
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "fileurl": "https://aipptus.oss-us-west-1.aliyuncs.com/worksdate/20260310/16198169/T2031281446055038976/1773130263007.pptx",
    "status": 1
  }
}
```

**响应字段说明**：
- `code`: 200表示成功
- `message`: SUCCESS表示成功
- `data.fileurl`: PPT文件下载链接（OSS直链）
- `data.status`: 任务状态
  - `0`: 生成中
  - `1`: 生成完成

**使用说明**：
1. 提交PPT任务后，获取`id`
2. 使用该`id`轮询查询状态
3. 当`status=1`时，返回`fileurl`下载链接
4. 用户可直接点击下载链接获取PPT

---

## 用户信息字段说明

### sender_id (X-Userid)
- **来源**: 从消息上下文的 `sender_id` 字段获取
- **格式**: 字符串，例如 `openclaw-control-ui`
- **用途**: 用户唯一标识，用于限流和用户追踪
- **传递方式**: 通过Header `X-Userid` 传递

### sender (X-Sender)
- **来源**: 从消息上下文的 `Sender.label` 字段获取
- **格式**: 字符串，例如 `openclaw-control-ui`
- **用途**: 用户显示名称
- **传递方式**: 通过Header `X-Sender` 传递

### chat_id (X-Chatid)
- **来源**: 从消息上下文的 `chat_id` 字段获取
- **格式**: 字符串，例如 `wecom:JiaJunHao`
- **用途**: 会话标识，区分不同对话
- **传递方式**: 通过Header `X-Chatid` 传递

### channel (X-Channel)
- **来源**: 从消息上下文的 `channel` 字段获取
- **格式**: 字符串，枚举值：`wecom`, `feishu`, `telegram`, `discord`, `slack` 等
- **用途**: 标识用户来自哪个渠道
- **传递方式**: 通过Header `X-Channel` 传递

**重要**：所有字段名使用小写，不使用驼峰

---

## 错误响应格式

所有接口在出错时返回统一的错误格式：

```json
{
  "timestamp": 1773975110447,
  "status": 404,
  "error": "Not Found",
  "path": "/aippt/api/c=15109"
}
```

### 常见错误码：
- `200` - 成功
- `400 Bad Request` - 参数错误
- `404 Not Found` - 资源不存在
- `429 Too Many Requests` - 请求频率超限
- `500 Internal Server Error` - 服务器内部错误

---

## 接口调用示例

### 示例：生成大纲
```bash
curl -X POST https://ai.mingyangtek.com/aippt/api/c=15109 \
  -H "Content-Type: application/json" \
  -H "X-Userid: openclaw-control-ui" \
  -H "X-Sender: openclaw-control-ui" \
  -H "X-Chatid: wecom:JiaJunHao" \
  -H "X-Channel: wecom" \
  -d '{"mainIdea":"沁园春"}'
```

---

## 待确认事项

以下事项需要后端开发时确认：

1. **修改大纲接口** - 请求参数格式
2. **获取模板列表接口** - 请求参数格式
3. **生成PPT接口** - 请求参数格式
4. **认证方式** - 是否需要额外的API Key或Token？
5. **异步处理** - PPT生成是否需要异步处理？
6. **OSS配置**:
   - Bucket名称和地址
   - 链接有效期（建议24小时）
   - 是否需要CDN加速？
7. **限流策略**：具体的限流规则
8. **预览页面**：模板预览页面的实现方式

---

此文档会根据后端实现情况持续更新。