---
name: product
description: 查询和浏览前凌智选平台的产品目录。当用户需要发现产品、按标签搜索或查看产品详情时使用。
version: 0.0.1
license: MIT
---

## 描述

通过 MCP Server 查询和浏览前凌智选 (fore.vip) 平台的产品目录 (KL 集合)。

---

## MCP 工具

**工具名称**: `query_kl`  
**服务器**: `fore-vip-mcp`  
**端点**: `https://api.fore.vip/mcp`

---

## 参数

### 可选参数

| 参数 | 类型 | 默认值 | 说明 | 示例 |
|------|------|--------|------|------|
| `tag` | string | - | 产品标签过滤 (如："推荐", "热门", "新品") | `"推荐"` |
| `limit` | number | `20` | 最大返回结果数 (1-100) | `50` |
| `skip` | number | `0` | 分页跳过的结果数 | `20` |

> **注意**: 所有参数均为可选。如果不提供标签，将返回所有按热度排序的产品。

---

## HTTP API 端点

### 获取工具列表

```bash
curl https://api.fore.vip/mcp/tools/list
```

**响应**:
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "tools": [
      {
        "name": "create_activity",
        "description": "Create offline event for fore.vip platform..."
      },
      {
        "name": "query_kl",
        "description": "Query products (KL collection) by tag. Returns list of products with name, description, images, and metadata.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "tag": {"type": "string", "description": "Product tag to filter (e.g., \"推荐\", \"热门\", \"新品\")"},
            "limit": {"type": "number", "description": "Maximum number of results to return (default: 20, max: 100)"},
            "skip": {"type": "number", "description": "Number of results to skip for pagination (default: 0)"}
          },
          "required": []
        }
      }
    ]
  }
}
```

### 调用工具

```bash
curl -X POST https://api.fore.vip/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "query_kl",
    "arguments": {
      "tag": "推荐",
      "limit": 10,
      "skip": 0
    }
  }'
```

**成功响应**:
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "content": [{
      "type": "text",
      "text": "{\n  \"success\": true,\n  \"total\": 10,\n  \"limit\": 10,\n  \"skip\": 0,\n  \"hasMore\": true,\n  \"data\": [\n    {\n      \"id\": \"kl_xxx\",\n      \"name\": \"产品名称\",\n      \"content\": \"产品描述...\",\n      \"pic\": [\"https://...\"],\n      \"tag\": \"推荐\",\n      \"hot\": 100,\n      \"url\": \"https://example.com\",\n      \"update_date\": 1234567890\n    }\n  ]\n}"
    }],
    "isError": false
  }
}
```

**错误响应**:
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "error": {
    "code": -32000,
    "message": "Tool execution failed"
  }
}
```

---

## 使用示例

### JavaScript (Fetch API)

```javascript
// 按标签查询产品
const result = await fetch('https://api.fore.vip/mcp/tools/call', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'query_kl',
    arguments: {
      tag: '推荐',
      limit: 20,
      skip: 0
    }
  })
})

const response = await result.json()

// 检查错误
if (response.error) {
  console.error('错误:', response.error.message)
} else {
  const data = JSON.parse(response.result.content[0].text)
  if (data.success) {
    console.log(`找到 ${data.total} 个产品`)
    data.data.forEach(product => {
      console.log(`- ${product.name} (${product.tag})`)
    })
  }
}
```

### 分页示例

```javascript
// 获取第一页
const page1 = await queryProducts({ tag: '热门', limit: 20, skip: 0 })

// 获取第二页
if (page1.hasMore) {
  const page2 = await queryProducts({ tag: '热门', limit: 20, skip: 20 })
}
```

### uniCloud (云函数)

```javascript
const mcp = uniCloud.importObject('mcp')

// 查询产品
const result = await mcp.tools_call({
  name: 'query_kl',
  arguments: {
    tag: '新品',
    limit: 50,
    skip: 0
  }
})

if (result.error) {
  console.error(result.error.message)
} else {
  const data = JSON.parse(result.result.content[0].text)
  console.log('产品列表:', data.data)
}
```

---

## 响应格式

### 成功响应结构

```json
{
  "success": true,
  "total": 20,
  "limit": 20,
  "skip": 0,
  "hasMore": true,
  "data": [
    {
      "id": "kl_xxx",
      "name": "产品名称",
      "content": "产品描述文本...",
      "pic": ["https://example.com/img1.jpg", "https://example.com/img2.jpg"],
      "tag": "推荐",
      "hot": 150,
      "url": "https://example.com/product",
      "update_date": 1711094400000
    }
  ]
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 查询成功状态 |
| `total` | number | 本次响应返回的产品数量 |
| `limit` | number | 请求的 limit 值 |
| `skip` | number | 请求的 skip 值 |
| `hasMore` | boolean | 是否有更多结果 |
| `data` | array | 产品对象数组 |

### 产品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 产品 ID (kl 集合 _id) |
| `name` | string | 产品名称 |
| `content` | string | 产品描述 |
| `pic` | array | 图片 URL 数组 |
| `tag` | string | 产品标签/分类 |
| `hot` | number | 热度分数 |
| `url` | string | 外部链接 URL |
| `update_date` | number | 最后更新时间戳 (毫秒) |

---

## 错误码

| 代码 | 错误 | 原因 | 解决方案 |
|------|------|------|----------|
| -32602 | `Missing required parameter: name` | 请求中未提供 name 字段 | 在请求体中包含 `name` 字段 |
| -32602 | `Unknown tool: xxx` | 无效的工具名称 | 使用 `query_kl` |
| -32000 | `Tool execution failed` | 数据库查询错误 | 检查服务器日志 |

---

## 前端集成 (产品目录页面)

### Vue 3 组件示例

```vue
<template>
  <view class="product-catalog">
    <!-- 标签筛选 -->
    <o-tab-tag 
      :tags="['全部', '推荐', '热门', '新品']"
      :current="currentTag"
      @change="onTagChange"
    />
    
    <!-- 产品列表 -->
    <scroll-view 
      scroll-y 
      class="product-list"
      @scrolltolower="loadMore"
    >
      <o-card 
        v-for="product in products" 
        :key="product.id"
        :title="product.name"
        :content="product.content"
        :bg="product.pic[0]"
        clickable
        @click="goToProduct(product.id)"
      />
      
      <!-- 无更多提示 -->
      <o-nomore v-if="!hasMore && products.length > 0" />
      
      <!-- 空状态 -->
      <view v-if="products.length === 0" class="empty">
        <text>暂无产品</text>
      </view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      currentTag: '全部',
      products: [],
      skip: 0,
      limit: 20,
      hasMore: true,
      loading: false
    }
  },
  
  onLoad() {
    this.loadProducts()
  },
  
  methods: {
    async loadProducts() {
      if (this.loading) return
      
      this.loading = true
      
      try {
        const response = await fetch('https://api.fore.vip/mcp/tools/call', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: 'query_kl',
            arguments: {
              tag: this.currentTag === '全部' ? '' : this.currentTag,
              limit: this.limit,
              skip: this.skip
            }
          })
        })
        
        const result = await response.json()
        
        if (result.error) {
          uni.showToast({ title: result.error.message, icon: 'none' })
          return
        }
        
        const data = JSON.parse(result.result.content[0].text)
        
        if (data.success) {
          if (this.skip === 0) {
            this.products = data.data
          } else {
            this.products = [...this.products, ...data.data]
          }
          
          this.hasMore = data.hasMore
          this.skip += data.data.length
        }
      } catch (e) {
        console.error(e)
        uni.showToast({ title: '加载失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
    
    onTagChange(tag) {
      this.currentTag = tag
      this.skip = 0
      this.products = []
      this.hasMore = true
      this.loadProducts()
    },
    
    loadMore() {
      if (this.hasMore && !this.loading) {
        this.loadProducts()
      }
    },
    
    goToProduct(id) {
      uni.navigateTo({
        url: `/ai/s?id=${id}`
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.product-catalog {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.product-list {
  flex: 1;
  padding: 20rpx;
}

.empty {
  text-align: center;
  padding: 100rpx 0;
  color: #999;
}
</style>
```

---

## 注意事项

1. **标签筛选**: 如果不提供标签或标签为"全部"，将返回所有产品
2. **分页**: 使用 `skip` 和 `limit` 进行分页。检查 `hasMore` 判断是否有更多结果
3. **排序**: 结果按 `hot` (降序) 然后 `update_date` (降序) 排序
4. **图片 URL**: `pic` 字段是图片 URL 数组，使用 `pic[0]` 作为缩略图
5. **产品详情**: 使用产品 `id` 跳转到详情页：`/ai/s?id=${id}`

---

## 相关文件

| 文件 | 路径 |
|------|------|
| MCP 云函数 | `/Users/codes/git/ai/fore/uniCloud-aliyun/cloudfunctions/mcp/index.obj.js` |
| 技能定义 | `/Users/codes/git/ai/skills/product/SKILL.md` |
| 产品详情页 | `/Users/codes/git/ai/fore/ai/s.vue` |

---

**版本**: 0.0.1  
**更新**: 2026-03-21  
**MCP 规范**: https://modelcontextprotocol.io/  
**API**: https://api.fore.vip/mcp  
**平台**: https://fore.vip
