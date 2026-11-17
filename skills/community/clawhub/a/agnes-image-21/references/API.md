# Agnes Image 2.1 Flash API

## 端点

### 图像生成

```
POST https://apihub.agnes-ai.com/v1/images/generations
```

## 请求格式

### 文生图

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",
  "size": "1024x768",
  "extra_body": {
    "response_format": "url"
  }
}
```

### 图生图

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "Transform into a rain-soaked cyberpunk night with neon reflections",
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
  "model": "agnes-image-2.1-flash",
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

## 2.1 版本特性

### 高信息密度优化

2.1 版本专门优化了高信息密度图像的生成：

- **复杂场景**：支持多元素、多层次场景
- **精细细节**：提升纹理和细节表现力
- **构图保留**：编辑时更好地保持原始构图

### 推荐场景

- 精细场景（城市景观、建筑细节）
- 复杂环境（多角色、多物体）
- 丰富构图（多层次、多元素）
- 高信息密度内容（信息图表、复杂设计）
