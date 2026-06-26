# ByteTech API Reference

> 通过 Chrome DevTools MCP 抓包发现的完整 API 文档。

## 核心文章 API

### POST /proxy_tech_api/v1/article/detail

获取文章完整详情。

**Request:**
```json
{"article_id": "7619471842051620907", "id_type": 8}
```

**Response 关键字段:**
```json
{
  "err_no": 0,
  "data": {
    "article_info": {
      "title": "万字长文|从Spec Coding到Harness：...",
      "en_title": "From Spec Coding to Harness: ...",
      "summary": "摘要内容",
      "lark_doc_token": "MQJsdhQMhovxhHxiTCAcc4cqn6d",
      "lark_doc_url": "https://bytedance.larkoffice.com/docx/MQJsdhQMhovxhHxiTCAcc4cqn6d",
      "view_cnt": 10670,
      "dig_cnt": 470,
      "collect_cnt": 379,
      "coin_cnt": 201,
      "comment_count": 11,
      "labels": [{"id": 2434, "name": "AI组织与公司", "en_name": "AI Organization"}],
      "content_type": 2000
    },
    "auther": {
      "name": "杜沁园",
      "full_name": "杜沁园",
      "email": "duqinyuan@bytedance.com",
      "department_name": "产品研发和工程架构-Dev Infra-...",
      "avatar": "https://...",
      "leader": {"name": "王铭"}
    }
  }
}
```

### POST /proxy_tech_api/v1/article/recommend

获取推荐文章。

**Request:**
```json
{"article_id": "7619471842051620907", "id_type": 8, "limit": 10}
```

### POST /proxy_tech_api/v2/content/team_account/item_include_info

获取文章所属团队目录和关联文章列表。

**Request:**
```json
{"item_id": "7619471842051620907", "id_type": 8}
```

**Response:** 返回团队树结构，包含 `root.sub[].items[]` 完整目录。

### POST /proxy_tech_api/v1/content/team_account/rank/item

获取团队热门文章排行。

**Request:**
```json
{"team_id": "7358737962923851787", "limit": 10}
```

### POST /proxy_tech_api/v1/content/item_detail_inclusion

文章详细关联信息。

### POST /proxy_tech_api/v2/label/tree

获取标签树（全量）。

### GET /proxy_tech_api/v2/search/hotwords

获取热搜关键词。

### POST /proxy_tech_api/v1/login

登录态检查（返回当前用户信息）。

## 辅助 API

### POST /api/v1/lark/component_auth

飞书组件鉴权，用于嵌入飞书文档。

### GET /tech.bytedance.net/api/ping

健康检查，返回 204。

## OAuth

- Client ID: `cli_9ea9078075791102`
- Redirect: `https://bytetech.info/oauth2/callback`

## Cookie

```
gateway_sid=xxx; bytetech=bytetech-user; csrf_session_id=xxx
```

## 页面结构

- 文章元信息：SSR 渲染（title、meta og:description）
- 文章正文：飞书文档 iframe（跨域，通过 `<tt-docs-component>` web component）
- 飞书文档 token：来自 API `article_info.lark_doc_token` 或 URL hash

## 内容获取路径

```
bytetech URL → article/detail API → 获取 lark_doc_token → lark-cli docs +fetch → 完整正文
```
