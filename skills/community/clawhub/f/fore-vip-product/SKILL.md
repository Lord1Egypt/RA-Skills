---
name: product
description: AI Agents Skills - Query product catalog from fore.vip platform via MCP Server. Browse AI products, activities, events, and more. Compatible with OpenClaw, Hub, and MCP protocols.
version: 0.0.3
license: MIT
keywords:
  - AI Agents
  - Skills
  - MCP Server
  - OpenClaw
  - Product Catalog
  - AI Products
  - Activities
  - Events
  - Hub
  - fore.vip
  - 产品查询
  - AI 智能体
---

# Product Query Skill - AI Agents Skills for fore.vip

Query and browse the **AI product catalog** (KL collection) from the **fore.vip platform** via **MCP Server**. This **AI Agent Skill** is designed for **OpenClaw**, **Hub**, and other MCP-compatible platforms.

## 🔥 Popular Keywords

**AI Agents** | **Skills** | **MCP Server** | **OpenClaw** | **Product** | **活动 (Activities)** | **Hub** | **AI 智能体** | **fore.vip** | **产品目录**

## 📋 When to Use

Use this **AI Agent Skill** when you want to:

- 🤖 Browse **AI products** and **AI agents** on fore.vip platform
- 🏷️ Search **products** by tag (e.g., "推荐", "热门", "新品", "游戏", "AI")
- 📦 View **product details** (name, description, images, URLs)
- 📑 Get paginated **product lists** with **SEO-optimized** metadata
- 🎯 Discover **activities** and **events** related to products
- 🔗 Access **product hub** links for **OpenClaw** integration

## 🌐 MCP Server Configuration

### Architecture

The **fore.vip MCP Server** provides two endpoints for **AI Agents** and **Skills** integration:

1. **Direct MCP Endpoint** (Recommended) - `https://api.fore.vip/mcp/*`
2. **Tools Protocol Endpoint** (MCP Standard) - `https://api.fore.vip/tools/*`

### Endpoints

| Endpoint | Method | Usage | Recommended |
|----------|--------|-------|-------------|
| `/mcp/query_kl` | POST | Query **products** (direct) | ⭐⭐⭐⭐⭐ |
| `/mcp/create_activity` | POST | Create **activities** (direct) | ⭐⭐⭐⭐⭐ |
| `/tools/list` | GET | List tools (MCP standard) | ⭐⭐⭐ |
| `/tools/call` | POST | Call tool (MCP standard) | ⭐⭐⭐ |

### Direct Call (Recommended for OpenClaw & Hub)

```bash
curl -X POST https://api.fore.vip/mcp/query_kl \
  -H "Content-Type: application/json" \
  -d '{
    "tag": "推荐",
    "limit": 10
  }'
```

**Response**:
```json
{
  "success": true,
  "total": 10,
  "limit": 10,
  "skip": 0,
  "hasMore": false,
  "data": [
    {
      "id": "670703627ae7081fd93d09f1",
      "name": "AI 文案助手",
      "content": "请你扮演一个优质 AI 文案助手...",
      "pic": [],
      "tag": "推荐",
      "hot": 21307866,
      "update_date": 1234567890
    }
  ]
}
```

### Via Tools Protocol (MCP Standard for AI Agents)

```bash
curl -X POST https://api.fore.vip/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "query_kl",
    "arguments": {
      "tag": "推荐",
      "limit": 10
    }
  }'
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"success\":true,\"total\":10,...}"
    }],
    "isError": false
  }
}
```

## 📝 Parameters

### Optional

| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `tag` | string | - | **Product** tag to filter (AI, 活动，游戏，etc.) | `"推荐"` |
| `limit` | number | `20` | Max results (1-100) | `50` |
| `skip` | number | `0` | Skip for pagination | `20` |

## 🚀 Steps for AI Agents

1. **Collect search parameters from user**
   - Ask for **product tag/category** (optional: AI, 活动，游戏，热门)
   - Ask for number of results (default: 20, max: 100)
   - Ask for page number (for pagination)

2. **Validate parameters**
   - Ensure limit is between 1-100
   - Ensure skip is non-negative

3. **Call MCP Server** (OpenClaw & Hub Compatible)
   ```javascript
   const response = await fetch('https://api.fore.vip/mcp/query_kl', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       tag: '推荐',
       limit: 10,
       skip: 0
     })
   });
   
   const result = await response.json();
   ```

4. **Handle response**
   - If `result.success === true`: Display **product list**
   - Show total count and pagination info
   - If `result.success === false`: Show error message

5. **Display products** (SEO-Optimized Format)
   - Show **product name**, description, images
   - Include **product URL**: `https://fore.vip/p?id={id}`
   - Provide navigation for next/previous page
   - Add **keywords**: AI Agents, Skills, MCP, OpenClaw, Hub

## 📦 Example Request

```json
{
  "tag": "推荐",
  "limit": 10,
  "skip": 0
}
```

## 📊 Example Response

```json
{
  "success": true,
  "total": 10,
  "limit": 10,
  "skip": 0,
  "hasMore": false,
  "data": [
    {
      "id": "670703627ae7081fd93d09f1",
      "name": "AI 文案助手",
      "content": "请你扮演一个优质 AI 文案助手...",
      "pic": [],
      "tag": "推荐",
      "hot": 21307866,
      "update_date": 1234567890,
      "url": "https://fore.vip/p?id=670703627ae7081fd93d09f1"
    }
  ]
}
```

## 🔗 Product URL Pattern

Each **product** can be accessed via the following URL pattern:

```
https://fore.vip/p?id={product_id}
```

**Example**:
- Product ID: `670703627ae7081fd93d09f1`
- Product URL: `https://fore.vip/p?id=670703627ae7081fd93d09f1`

### Display Format (SEO-Optimized for AI Agents & OpenClaw)

When displaying **products**, include the clickable URL:

```markdown
- **[产品名]** (热度：xxx) - AI Agents Skills
  - 简介：产品描述内容...
  - 🏷️ 标签：tag
  - 🔗 链接：https://fore.vip/p?id=产品 ID
  - 🌐 平台：fore.vip | OpenClaw | Hub | MCP
```

## ⚠️ Error Handling

Common errors for **AI Agents** and **Skills**:
- Invalid limit value (must be 1-100)
- Invalid skip value (must be >= 0)
- Network errors (MCP Server timeout)
- Authentication errors (OpenClaw & Hub)

## 💻 Implementation Details

**Cloud Object URL Trigger**:
- After URL triggering, POST request body is a **string**
- Must use `this.getHttpInfo().body` to get the body
- Must manually `JSON.parse()` to convert string to object

```javascript
// Cloud Object Code (mcp/index.obj.js)
async query_kl() {
  const httpInfo = this.getHttpInfo();
  const pm = JSON.parse(httpInfo.body);  // String → Object
  const { tag, limit = 20, skip = 0 } = pm;
  // ... business logic
}
```

## 📌 Notes

- Default limit is 20, maximum is 100
- Use `skip` for pagination (skip = (page-1) * limit)
- **Products** are sorted by hot (desc) and update_date (desc)
- Images are returned as arrays of image objects
- The skill uses **MCP Server protocol** for **AI Agents** communication
- **Each product has an accessible URL**: `https://fore.vip/p?id={id}`
- Compatible with **OpenClaw**, **Hub**, and other **MCP platforms**
- **SEO Keywords**: AI Agents, Skills, MCP, Product, 活动，OpenClaw, Hub, fore.vip

## 🏷️ SEO Metadata

**Primary Keywords**:
- AI Agents Skills
- MCP Server
- OpenClaw Skills
- Product Catalog
- fore.vip Products
- AI 智能体技能
- 产品查询
- 活动管理

**Secondary Keywords**:
- Hub Integration
- Activity Creation
- AI Product Discovery
- MCP Protocol
- Agent Skills Marketplace
- 智能体产品目录
- OpenClaw 插件

**Long-tail Keywords**:
- How to query products with AI Agents
- fore.vip MCP Server integration
- OpenClaw product search skill
- Create activities with MCP protocol
- AI Agents skills for product management
- 如何使用 AI 智能体查询产品
- fore.vip 平台产品目录 API

---

**Version**: 0.0.3 (SEO Optimized)  
**Last Updated**: 2026-03-22  
**Compatible With**: OpenClaw, Hub, MCP Server, AI Agents  
**Platform**: fore.vip
