---
name: ppt-generator
description: PPT自动生成工具，通过调用外部接口实现从主题到完整PPT文件的自动化生成流程。支持大纲生成、大纲修改、模板选择、PPT生成等完整流程。当用户要求生成PPT、制作幻灯片、创建演示文稿、年终总结PPT、项目汇报PPT时使用此skill。
---

# PPT Generator

## ⚠️ 重要：交互式流程说明

**这是一个交互式流程，不是自动化脚本！**

在以下关键步骤必须停止执行，等待用户确认：

1. **Step 4: 大纲确认** - 展示大纲后必须停止，等待用户回复"1"或"2"
2. **Step 8: 选择模版** - 展示模版列表后必须停止，等待用户输入模版编号

**禁止行为**：
- ❌ 不要自动选择大纲确认选项
- ❌ 不要自动选择模版
- ❌ 不要在用户回复前继续下一步

**正确做法**：
- ✅ 展示内容后立即停止
- ✅ 明确告诉用户需要回复什么
- ✅ 等待用户回复后再继续

---

## Overview

通过调用统一API接口实现PPT的自动化生成。完整流程包括：主题输入 → 大纲生成 → 大纲确认/修改 → 模板选择 → PPT生成 → 文件交付。

**统一接口地址**: `https://ai.mingyangtek.com/aippt/api/c=15109`

**重要说明**:
- 所有操作使用同一个URL
- 通过请求参数区分不同操作
- 使用POST方法

---

## Complete Workflow

### Step 1: 用户输入主题

当用户请求生成PPT时，首先确认主题：
```
用户: 帮我生成一个年终总结PPT
用户: 制作一个水浒传赏析的幻灯片
用户: 创建一个产品发布演示文稿
```

**操作**：
1. 从消息上下文中提取用户信息：`sender_id`, `sender`, `chat_id`, `channel`
2. 确认PPT主题（如果用户未明确说明）

### Step 2: 生成大纲

调用统一接口生成大纲：

**Request**:
```http
POST http://ai.mingyangtek.com/aippt/api/c=15109 HTTP/1.1
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "mainIdea": "年终总结"
}
```

**参数说明**：
- `mainIdea`: PPT主题/主要想法（必需）

**Response** (示例):
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "id": "9f247d90c8044b10b46dc536bdd724e8",
    "mainIdea": "年终总结",
    "markdown": "# 年终总结\n## 工作回顾\n...",
    "outLineTree": "{...}"
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

### Step 3: 大纲渲染展示

根据不同渠道，选择不同的渲染方式：

| 渠道 | 推荐格式 | 原因 | 说明 |
|------|---------|---------|------|
| wecom/feishu | emoji | 支持emoji，用户体验好 | 用emoji增强可读性 |
| telegram/discord | markdown | 支持markdown，格式清晰 | 使用标题和列表 |
| slack | simple | 不支持复杂格式 | 使用纯文本编号 |

**格式化函数调用**：
```python
from scripts.ppt_api import format_outline

# 根据渠道自动选择格式
channel = "wecom"
if channel in ["telegram", "discord"]:
    style = "markdown"
elif channel == "slack":
    style = "simple"
else:
    style = "emoji"

formatted_outline = format_outline(result, style=style)
print(formatted_outline)
```

### Step 4: 大纲确认

**⚠️ 重要：必须等待用户确认！展示大纲后必须停止执行，等待用户回复。**

展示大纲后，询问用户是否需要修改：

**选项**：
1. **不修改** - 使用当前大纲
2. **修改大纲** - 调整内容

**必须的操作**：
1. 展示完整大纲内容
2. **停止执行，等待用户回复"1"或"2"**
3. **不要自动选择，不要继续下一步**
4. 根据用户回复执行对应操作

**用户回复**：
- 用户回复 "1" → 确认大纲，继续下一步
- 用户回复 "2" → 进入大纲修改流程

### Step 5: 大纲修改（可选）

如果用户选择修改大纲，调用编辑大纲接口：

**Request**:
```http
POST https://ai.mingyangtek.com/aippt/api/c=15110 HTTP/1.1
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "outlineId": "9f247d90c8044b10b46dc536bdd724e8",
  "markDownStr": "# 年终总结\n## 修改后的内容\n...",
  "userId": "{sender_id}"
}
```

**参数说明**：
- `outlineId`: 大纲ID（必需）
- `markDownStr`: Markdown格式的完整大纲内容（必需）
- `userId`: 用户ID（必需）

**Response** (示例):
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "id": "9f247d90c8044b10b46dc536bdd724e8",
    "mainIdea": "年终总结",
    "markdown": "# 年终总结\n## 修改后的内容\n..."
  }
}
```

### Step 6: 智能标签推荐

根据PPT主题推荐合适的标签：

```python
from scripts.ppt_api import recommend_tags

tags = recommend_tags("年终总结")
# 返回: {"style_tags": ["商务风"], "color_tags": ["蓝色"]}

tags = recommend_tags("春天")
# 返回: {"style_tags": ["中国风"], "color_tags": ["绿色"]}
```

**标签范围**：
- 风格标签：简约风、小清新、商务风、中国风、可爱卡通、科技风、手绘风格、欧美风、党政风、黑板风
- 颜色标签：蓝色、红色、粉色、黄色、绿色、橙色、黑色、白色、灰色、紫色

### Step 7: 查询模版列表

**Request**:
```http
POST https://ai.mingyangtek.com/aippt/api/c=15111 HTTP/1.1
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "keywords": ["商务风", "蓝色"],
  "userId": "{sender_id}"
}
```

**参数说明**：
- `keywords`: 标签数组（必需）- 可以传多个标签
- `userId`: 用户ID（必需）

**Response** (示例):
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": [
    {
      "templateId": 39,
      "fileName": "简约蓝色商务汇报PPT模版.pptx",
      "preview": "https://aipptx.oss-cn-shanghai.aliyuncs.com/templates/39/view_xxx.pptx"
    }
  ]
}
```

**模版列表展示**：
```python
from scripts.ppt_api import format_templates

# 格式化模版列表（简单列表格式，不显示ID和预览）
formatted = format_templates(templates, channel="wecom")
# 输出：
# 找到 5 个模版：
#
# 1. 简约蓝色商务汇报PPT模版.pptx
# 2. 绿色简约校园通用PPT.pptx
# ...
#
# 请选择模版编号（1-5）：
```

### Step 8: 选择模版

**⚠️ 重要：必须等待用户选择！展示模版列表后必须停止执行，等待用户输入模版编号。**

展示模版列表后，询问用户选择模版：

**必须的操作**：
1. 展示模版列表（使用format_templates函数）
2. **停止执行，等待用户输入模版编号（如"1"、"2"等）**
3. **不要自动选择模版，不要继续下一步**
4. 根据用户输入的编号，提取对应的templateId

**用户选择模版编号后**，提取对应的 templateId：

```python
# 用户选择编号 1
selected_template_id = templates[0]['templateId']  # 39
```

### Step 9: 提交PPT任务

**Request**:
```http
POST https://ai.mingyangtek.com/aippt/api/c=15112 HTTP/1.1
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "templateId": 39,
  "outlineId": "9f247d90c8044b10b46dc536bdd724e8",
  "reporter": "贾俊豪"
}
```

**参数说明**：
- `templateId`: 模版ID（必需）- 数字类型
- `outlineId`: 大纲ID（必需）
- `reporter`: 汇报人/作者名称（可选）

**Response** (示例):
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "id": 2086770
  }
}
```

**重要**：返回的是 `id` 字段（数字类型），不是 `taskId`

### Step 10: 查询PPT生成结果

PPT生成是异步的，需要轮询查询状态：

**Request**:
```http
POST https://ai.mingyangtek.com/aippt/api/c=15113 HTTP/1.1
Content-Type: application/json
X-Userid: {sender_id}
X-Sender: {sender}
X-Chatid: {chat_id}
X-Channel: {channel}

{
  "pptId": 2086770,
  "userId": "{sender_id}"
}
```

**参数说明**：
- `pptId`: PPT任务ID（必需）- 数字类型
- `userId`: 用户ID（必需）

**Response - 生成中**:
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "id": 2086770,
    "status": 0,
    "fileurl": null
  }
}
```

**Response - 生成完成**:
```json
{
  "code": 200,
  "message": "SUCCESS",
  "data": {
    "id": 2086770,
    "status": 1,
    "fileurl": "https://aipptx.oss-cn-shanghai.aliyuncs.com/worksdate/xxx.pptx"
  }
}
```

**状态说明**：
- `status=0`: 生成中
- `status=1`: 生成完成

**轮询策略**：
```python
# 使用 wait_for_ppt 函数自动轮询
result = client.wait_for_ppt(ppt_id, max_attempts=60, interval=5)
# 每5秒查询一次，最多查询60次（约5分钟）
```

### Step 11: 交付PPT文件

**格式化输出**：
```python
from scripts.ppt_api import format_ppt_result

# 格式化PPT生成结果（包含推广文案）
output = format_ppt_result(
    theme="年终总结",
    ppt_id="2086770",
    download_url="https://aipptx.oss-cn-shanghai.aliyuncs.com/worksdate/xxx.pptx",
    channel="wecom"
)

print(output)
```

**输出格式**：
```markdown
## ✅ PPT生成成功！

### 📋 生成信息：

- **主题**: 年终总结
- **PPT ID**: `2086770`

---

### 📥 PPT下载链接：

```
https://aipptx.oss-cn-shanghai.aliyuncs.com/worksdate/xxx.pptx
```

**点击链接即可下载PPT文件！**

---

## 🎉 PPT生成完成！

---

**本功能由名阳信息技术有限公司提供**  
如需使用完整功能，请下载APP应用或访问网站：
- 📱 APP：各大应用商店搜索"mindppt"
- 🌐 网站：https://mindppt.net
```
---

## User Information Passing

所有API调用都需要携带用户信息：

### Header字段
`http
X-Userid: {user_id}       # 用户唯一标识（必需）
X-Sender: {sender}        # 用户名称
X-Chatid: {chat_id}       # 会话ID
X-Channel: {channel}      # 渠道（wecom/feishu/telegram等）
`

### 获取方式
从消息上下文中获取：
- sender_id - 从消息上下文获取
- sender - 从 Sender.label 获取
- chat_id - 从 inbound_meta.chat_id 获取
- channel - 从 inbound_meta.channel 获取

---

## Error Handling

### 常见错误

1. **网络连接失败** - 检查网络连通性
2. **请求频率超限（429）** - 等待后重试
3. **资源不存在（404）** - 检查ID是否正确
4. **服务器错误（5xx）** - 等待后重试

---

## References

- API接口文档：
eferences/api-endpoints.md
- Python客户端：scripts/ppt_api.py
