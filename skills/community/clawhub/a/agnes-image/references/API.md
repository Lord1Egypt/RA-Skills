# Agnes Image 2.0 Flash API

## 端点

### 图像生成

```
POST https://apihub.agnes-ai.com/v1/images/generations
```

## 请求格式

### 文生图

```json
{
  "model": "agnes-image-2.0-flash",
  "prompt": "A cat sitting on a windowsill, golden hour lighting, photorealistic",
  "size": "1024x768",
  "extra_body": {
    "response_format": "url"
  }
}
```

### 图生图

```json
{
  "model": "agnes-image-2.0-flash",
  "prompt": "Transform into anime style",
  "size": "1024x768",
  "extra_body": {
    "image": ["https://example.com/photo.jpg"],
    "response_format": "url"
  }
}
```

### 多图合成

```json
{
  "model": "agnes-image-2.0-flash",
  "prompt": "Combine these two characters in a fantasy scene",
  "size": "1024x768",
  "extra_body": {
    "image": ["https://example.com/a.png", "https://example.com/b.png"],
    "response_format": "url"
  }
}
```

## 响应格式

### URL 格式

```json
{
  "data": [
    {
      "url": "https://cdn.example.com/generated-image.png"
    }
  ]
}
```

### Base64 格式

```json
{
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUg..."
    }
  ]
}
```

## 支持尺寸

| 尺寸 | 宽高比 | 适用场景 |
|------|--------|----------|
| 1024x768 | 4:3 | 标准横图 |
| 1024x1024 | 1:1 | 方形 |
| 768x1024 | 3:4 | 标准竖图 |

## 认证

使用 Bearer Token 认证：

```
Authorization: Bearer YOUR_API_KEY
```

## 错误处理

### 常见错误

| 错误码 | 说明 |
|--------|------|
| 401 | API Key 无效或未提供 |
| 400 | 请求格式错误 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

## 最佳实践

1. **提示词质量**：详细描述主体、场景、风格、光照和构图
2. **尺寸选择**：根据使用场景选择合适的宽高比
3. **图生图**：确保输入图像 URL 公开可访问
4. **超时设置**：建议设置 60-360 秒超时
5. **错误重试**：实现指数退避重试机制
