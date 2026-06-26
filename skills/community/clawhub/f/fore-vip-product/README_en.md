# product Skill - Product Query

[![Version](https://img.shields.io/badge/version-0.0.2-blue)](https://github.com/fore-vip/skills/tree/main/product)
[![License](https://img.shields.io/badge/license-MIT-green)](../LICENSE)

Query and browse product catalog from the fore.vip platform via MCP Server.

---

## 📋 Description

This skill enables AI agents to query and browse products from the fore.vip platform. It supports tag-based filtering, pagination, and returns product details including name, description, images, and metadata.

---

## 🚀 Installation

```bash
# Install from GitHub
npx skills add fore-vip/skills --skill product

# Install from local path
npx skills add /path/to/skills --skill product
```

---

## 🔧 MCP Server Configuration

**Endpoint**: `https://api.fore.vip/mcp/query_kl`  
**Method**: `POST`  
**Content-Type**: `application/json`

---

## 📝 Parameters

### Optional

| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `tag` | string | - | Product tag to filter | `"推荐"` |
| `limit` | number | `20` | Max results (1-100) | `50` |
| `skip` | number | `0` | Skip for pagination | `20` |

---

## 💡 Usage Examples

### Basic Product Query

```javascript
const response = await fetch('https://api.fore.vip/mcp/query_kl', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    tag: '推荐',
    limit: 10
  })
});

const result = await response.json();
console.log('Products:', result.data);
```

### With Pagination

```javascript
const page = 2;
const limit = 20;
const skip = (page - 1) * limit;

const response = await fetch('https://api.fore.vip/mcp/query_kl', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    tag: '热门',
    limit: limit,
    skip: skip
  })
});

const result = await response.json();
console.log('Page', page, 'Products:', result.data);
console.log('Has more:', result.hasMore);
```

---

## 📊 Response Format

### Success

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
      "name": "文案助手",
      "content": "请你扮演一个优质文案助手...",
      "pic": [],
      "tag": "推荐",
      "hot": 21307866,
      "update_date": 1234567890
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Query success status |
| `total` | number | Number of products returned |
| `limit` | number | Requested limit |
| `skip` | number | Requested skip |
| `hasMore` | boolean | Whether more results available |
| `data` | array | Array of product objects |

### Product Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Product ID (_id) |
| `name` | string | Product name |
| `content` | string | Product description |
| `pic` | array | Array of image objects |
| `tag` | string | Product tag |
| `hot` | number | Popularity score |
| `update_date` | number | Last update timestamp |

---

## ⚠️ Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid limit value | limit < 1 or limit > 100 | Use value between 1-100 |
| Invalid skip value | skip < 0 | Use non-negative value |
| Network error | Connection issue | Retry with exponential backoff |

---

## 🧪 Testing

```bash
# Run local tests
cd product
./test_local.sh
```

**Test Cases**:
- ✅ Query products by tag
- ✅ Query with pagination
- ✅ Query all products (no tag)

---

## 📚 Related Resources

- **[MCP Specification](https://modelcontextprotocol.io/)** - Protocol docs
- **[skills.sh](https://skills.sh/)** - Skills directory
- **[Fore-Vip](https://fore.vip/)** - Platform website
- **[API Docs](https://api.fore.vip/mcp)** - MCP API

---

## 📝 Version History

### v0.0.2 (2026-03-22)
- ✅ Update to MCP Server standard
- ✅ Simplify SKILL.md format
- ✅ Add architecture documentation
- ✅ Update endpoint to `/mcp/query_kl`

### v0.0.1 (2026-03-21)
- ✅ Initial release

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a PR

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) file.

---

**Maintainer**: wise  
**Last Updated**: 2026-03-22
