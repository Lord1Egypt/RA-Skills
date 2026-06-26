# product 技能 - 产品查询

[![Version](https://img.shields.io/badge/version-0.0.2-blue)](https://github.com/fore-vip/skills/tree/main/product)
[![License](https://img.shields.io/badge/license-MIT-green)](../LICENSE)

通过 MCP Server 查询和浏览 fore.vip 平台的产品目录。

---

## 📋 说明

此技能使 AI 智能体能够查询和浏览 fore.vip 平台的产品。它支持按标签筛选、分页，并返回产品详细信息，包括名称、描述、图片和元数据。

---

## 🚀 安装

```bash
# 从 GitHub 安装
npx skills add fore-vip/skills --skill product

# 从本地路径安装
npx skills add /path/to/skills --skill product
```

---

## 🔧 MCP Server 配置

**端点**: `https://api.fore.vip/mcp/query_kl`  
**方法**: `POST`  
**Content-Type**: `application/json`

---

## 📝 参数

### 可选参数

| 参数 | 类型 | 默认值 | 说明 | 示例 |
|------|------|--------|------|------|
| `tag` | string | - | 产品标签筛选 | `"推荐"` |
| `limit` | number | `20` | 最大结果数 (1-100) | `50` |
| `skip` | number | `0` | 分页跳过数量 | `20` |

---

## 💡 使用示例

### 基础产品查询

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
console.log('产品列表:', result.data);
```

### 分页查询

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
console.log('第', page, '页产品:', result.data);
console.log('更多数据:', result.hasMore);
```

---

## 📊 响应格式

### 成功

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

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 查询成功状态 |
| `total` | number | 返回的产品数量 |
| `limit` | number | 请求的 limit 值 |
| `skip` | number | 请求的 skip 值 |
| `hasMore` | boolean | 是否有更多结果 |
| `data` | array | 产品对象数组 |

### 产品对象

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 产品 ID (_id) |
| `name` | string | 产品名称 |
| `content` | string | 产品描述 |
| `pic` | array | 图片对象数组 |
| `tag` | string | 产品标签 |
| `hot` | number | 热度分数 |
| `update_date` | number | 最后更新时间戳 |

---

## ⚠️ 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Invalid limit value | limit < 1 或 limit > 100 | 使用 1-100 之间的值 |
| Invalid skip value | skip < 0 | 使用非负值 |
| Network error | 连接问题 | 使用指数退避重试 |

---

## 🧪 测试

```bash
# 运行本地测试
cd product
./test_local.sh
```

**测试用例**:
- ✅ 按标签查询产品
- ✅ 分页查询
- ✅ 查询所有产品（无标签）

---

## 📚 相关资源

- **[MCP 规范](https://modelcontextprotocol.io/)** - 协议文档
- **[skills.sh](https://skills.sh/)** - 技能目录
- **[Fore-Vip](https://fore.vip/)** - 平台官网
- **[API 文档](https://api.fore.vip/mcp)** - MCP API

---

## 📝 版本历史

### v0.0.2 (2026-03-22)
- ✅ 更新为 MCP Server 标准
- ✅ 简化 SKILL.md 格式
- ✅ 添加架构文档
- ✅ 更新端点为 `/mcp/query_kl`

### v0.0.1 (2026-03-21)
- ✅ 初始版本

---

## 🤝 贡献

欢迎贡献！请：
1. Fork 仓库
2. 创建特性分支
3. 进行更改
4. 提交 PR

---

## 📄 许可证

MIT License - 详见 [LICENSE](../LICENSE) 文件

---

**维护者**: wise  
**最后更新**: 2026-03-22
