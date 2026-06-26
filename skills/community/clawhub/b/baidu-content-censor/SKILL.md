# 百度内容审核 (baidu-content-censor)

## 概述

本 Skill 提供文本审核和图像审核两个 API 接口，用于内容安全检测。

## 触发方式

当用户请求以下操作时，自动调用此 Skill：
- 文本审核 / 内容审核 / 文字审核
- 图片审核 / 图像审核 / 图片检测
- 内容安全检测
- 敏感词检测 / 违规内容检测
- 审核这段文字 / 审核这张图片
- "帮我审核..." / "请审核..." / "检测一下..."

## 执行指令

当触发此 Skill 时：
1. 识别用户是要审核**文本**还是**图片**
2. 如果是文本审核：调用 `api_client.text_censor(text="...")`
3. 如果是图片审核：
   - 如果用户提供的是本地图片路径，调用 `api_client.image_censor(image="/path/to/image.jpg")`
   - 如果用户提供的是图片 URL，调用 `api_client.image_censor(img_url="https://...")`
4. 解析返回的 JSON 结果，以友好的方式展示给用户
5. access_token 会自动从 AK/SK 获取并缓存，无需手动处理

## 接口地址

- 文本审核: `https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined`
- 图像审核: `https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined`

---

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| BCE_SINAN_AK | 是 | 百度云 API Key |
| BCE_SINAN_SK | 是 | 百度云 Secret Key |

设置方式：
```bash
export BCE_SINAN_AK="你的AK"
export BCE_SINAN_SK="你的SK"
```

---

## Token 缓存机制

- Access Token 会自动从百度云 API 获取
- 缓存文件位置：`~/.claude/skills/baidu-content-censor/token_cache.json`
- 缓存过期时间：提前 5 分钟自动刷新
- 如果 API 返回 110（access_token 无效）或 111（access_token 过期），会自动刷新并重试

---

## API 使用方法

### 1. 文本审核

```python
from baidu-content-censor import text_censor

# 审核文本
result = text_censor(text="待审核的文本内容")

# 也可以指定 appid
result = text_censor(text="待审核的文本内容", appid=123456)
```

### 2. 图像审核

```python
from baidu-content-censor import image_censor

# 方式一：通过图片 URL 审核
result = image_censor(img_url="https://example.com/image.jpg")

# 方式二：通过本地图片路径审核（自动转为 Base64）
result = image_censor(image="/path/to/image.jpg")

# 也可以指定 appid
result = image_censor(img_url="https://example.com/image.jpg", appid=123456)
```

### 3. 通用接口（自动识别类型）

```python
from baidu-content-censor import censor

# 自动识别为文本
result = censor("待审核的文本内容")

# 自动识别为图片（URL）
result = censor("https://example.com/image.jpg")

# 自动识别为图片（本地路径）
result = censor("/path/to/image.jpg")

# 手动指定类型
result = censor("待审核的文本内容", content_type="text")
result = censor("/path/to/image.jpg", content_type="image")
```

### 4. 强制刷新 Token

```python
from baidu-content-censor import refresh_access_token

# 强制刷新 access_token（清除缓存并重新获取）
new_token = refresh_access_token()
```

---

## 返回结果

接口返回完整的 JSON 审核结果，包含以下常见字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| logId | long | 请求唯一标识 |
| conclusion | string | 审核结论（如：合规、不合规、疑似） |
| conclusionType | int | 结论类型（1:合规, 2:不合规, 3:疑似, 4:审核失败） |
| data | array | 详细审核数据 |

---

## 注意事项

1. `image` 和 `img_url` 只能传其中一个，不能同时传递
2. 文本审核内容不能超过 2 万字节
3. 所有请求都会自动添加 `isFromSkill=true` 参数用于埋点
4. 本地图片路径会自动转换为 Base64，无需手动处理
5. Access Token 缓存机制确保性能最优，不会频繁请求百度云获取 token