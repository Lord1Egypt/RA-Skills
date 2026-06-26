# Figma API 参考

本技能使用Figma REST API v1版本。以下是关键API端点和参数说明。

## 认证

所有API请求都需要在Header中提供个人访问令牌：

```http
X-Figma-Token: <your_personal_access_token>
```

获取个人访问令牌：
1. 登录Figma
2. 进入 Settings → Account
3. 在 Personal access tokens 部分创建新令牌

## 核心API端点

### 1. 获取文件信息
```
GET /v1/files/:key
```

**参数**：
- `key` (必填): Figma文件key或URL中的文件ID
- `version` (可选): 特定版本ID
- `depth` (可选): 返回节点的深度，默认=1

**响应示例**：
```json
{
  "name": "Design System",
  "lastModified": "2024-01-15T10:30:00Z",
  "thumbnailUrl": "https://...",
  "version": "1234567890",
  "document": {...},
  "components": {...},
  "componentSets": {...},
  "styles": {...}
}
```

### 2. 获取图片导出
```
GET /v1/images/:key
```

**查询参数**：
- `ids` (必填): 逗号分隔的节点ID
- `scale` (可选): 缩放比例 (0.01-4)，默认=1
- `format` (可选): 图片格式 (png, jpg, svg, pdf)，默认=png
- `svg_include_id` (可选): SVG是否包含节点ID
- `svg_include_node_data` (可选): SVG是否包含节点数据
- `use_absolute_bounds` (可选): 使用绝对边界

**响应示例**：
```json
{
  "images": {
    "1:23": "https://s3-us-west-2.amazonaws.com/figma-alpha-api/img/..."
  }
}
```

### 3. 获取节点信息
```
GET /v1/files/:key/nodes
```

**查询参数**：
- `ids` (必填): 逗号分隔的节点ID
- `depth` (可选): 节点深度
- `geometry` (可选): 是否返回几何路径

### 4. 获取评论
```
GET /v1/files/:key/comments
```

### 5. 获取版本历史
```
GET /v1/files/:key/versions
```

## 数据结构

### 节点类型
Figma设计中的节点有多种类型：

| 类型 | 描述 | 关键属性 |
|------|------|----------|
| `DOCUMENT` | 文档根节点 | `children` |
| `CANVAS` | 画板/页面 | `backgroundColor`, `children` |
| `FRAME` | 框架/容器 | `absoluteBoundingBox`, `fills`, `strokes`, `children` |
| `GROUP` | 组 | `children` |
| `RECTANGLE` | 矩形 | `absoluteBoundingBox`, `fills`, `cornerRadius` |
| `TEXT` | 文本 | `characters`, `style`, `fills` |
| `COMPONENT` | 组件 | `name`, `description` |
| `INSTANCE` | 组件实例 | `componentId` |
| `VECTOR` | 矢量图形 | `fillGeometry`, `strokeGeometry` |

### 设计属性

#### 颜色 (Fills/Strokes)
```json
{
  "fills": [{
    "type": "SOLID",
    "color": {
      "r": 0.5,    // 0-1范围
      "g": 0.5,
      "b": 0.5,
      "a": 1.0     // 透明度
    }
  }]
}
```

#### 文本样式
```json
{
  "style": {
    "fontFamily": "Inter",
    "fontWeight": 600,
    "fontSize": 16,
    "lineHeightPx": 24,
    "lineHeightPercent": 150,
    "letterSpacing": 0,
    "textCase": "UPPER",
    "textDecoration": "NONE"
  }
}
```

#### 边界框
```json
{
  "absoluteBoundingBox": {
    "x": 100,
    "y": 100,
    "width": 200,
    "height": 100
  }
}
```

## API限制

### 速率限制
- **标准限制**: 2000请求/小时
- **截图限制**: 100张图片/小时
- **建议**: 添加延迟和重试逻辑

### 文件大小限制
- 单个文件: 无明确限制，但建议分页处理大型文件
- 响应大小: 建议使用`depth`参数控制

### 错误码

| 状态码 | 描述 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 请求错误 | 检查参数格式 |
| 401 | 认证失败 | 检查访问令牌 |
| 403 | 权限不足 | 检查文件访问权限 |
| 404 | 资源不存在 | 检查文件/节点ID |
| 429 | 速率限制 | 等待后重试 |
| 500 | 服务器错误 | 稍后重试 |

## 最佳实践

### 1. 错误处理
```javascript
try {
  const response = await axios.get(url, { headers });
  return response.data;
} catch (error) {
  if (error.response?.status === 429) {
    // 速率限制，等待后重试
    await wait(1000);
    return retryRequest();
  }
  throw error;
}
```

### 2. 分页处理大型文件
```javascript
// 使用depth参数控制数据量
const response = await axios.get(
  `https://api.figma.com/v1/files/${fileId}?depth=2`,
  { headers }
);

// 分批处理节点
const batchSize = 50;
for (let i = 0; i < nodeIds.length; i += batchSize) {
  const batch = nodeIds.slice(i, i + batchSize);
  await processBatch(batch);
}
```

### 3. 结果缓存
```javascript
const cache = new Map();

async function getFileInfo(fileId, forceRefresh = false) {
  const cacheKey = `file:${fileId}`;
  
  if (!forceRefresh && cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  
  const data = await fetchFromFigma(fileId);
  cache.set(cacheKey, data);
  return data;
}
```

### 4. 进度指示
```javascript
// 对于长时间操作，提供进度反馈
async function exportMultipleScreenshots(nodeIds) {
  const results = [];
  
  for (let i = 0; i < nodeIds.length; i++) {
    const progress = Math.round((i / nodeIds.length) * 100);
    console.log(`进度: ${progress}% (${i + 1}/${nodeIds.length})`);
    
    const result = await exportScreenshot(nodeIds[i]);
    results.push(result);
  }
  
  return results;
}
```

## 工具函数

### 颜色转换
```javascript
function figmaColorToHex(color) {
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}

function figmaColorToRGBA(color) {
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  return `rgba(${r}, ${g}, ${b}, ${color.a})`;
}
```

### 尺寸计算
```javascript
function calculateNodeSize(node) {
  const bounds = node.absoluteBoundingBox;
  if (!bounds) return null;
  
  return {
    width: bounds.width,
    height: bounds.height,
    area: bounds.width * bounds.height,
    aspectRatio: bounds.width / bounds.height
  };
}
```

## 扩展建议

### 支持的扩展功能
1. **Webhook集成**: 监听文件变更自动同步
2. **增量同步**: 只同步变更的部分
3. **多格式导出**: 支持Sketch、Adobe XD等格式
4. **设计规范检查**: 自动检查设计规范遵循情况
5. **协作分析**: 分析团队协作模式和效率

### 性能优化
- 使用流式处理大文件
- 实现增量加载
- 添加本地缓存
- 并行处理独立任务

## 相关资源
- [官方API文档](https://www.figma.com/developers/api)
- [API Playground](https://www.figma.com/developers/api#playground)
- [社区库和工具](https://www.figma.com/developers/community)
- [Webhook文档](https://www.figma.com/developers/webhooks)