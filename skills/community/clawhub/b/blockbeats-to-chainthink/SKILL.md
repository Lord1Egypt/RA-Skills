# BlockBeats to ChainThink Skill

从律动 BlockBeats 抓取文章并自动保存到 ChainThink 后台草稿。

## 使用场景

当用户提供律动 BlockBeats 文章链接（如 `https://www.theblockbeats.info/news/xxxxx`），自动：
1. 提取文章标题、摘要、正文和图片
2. 保存到 ChainThink 后台草稿
3. 返回文章 ID

## 工作流程

1. 打开浏览器访问 BlockBeats 文章页面
2. 从 `window.__NUXT__.data[0].info` 提取文章数据
3. 调用 ChainThink API 保存草稿

## ChainThink API 配置

- **API 地址**: `https://api-v2.chainthink.cn/ccs/v1/admin/content/publish`
- **认证方式**: `x-token` + `x-user-id` headers
- **User ID**: 51
- **Token**: 从 TOOLS.md 读取（需要用户提供）

## 使用方法

用户发送律动文章链接即可，例如：
- "抓取这篇文章：https://www.theblockbeats.info/news/61465"
- "把这个保存到 ChainThink：https://www.theblockbeats.info/news/61461"

## 实现步骤

### 1. 提取文章内容

使用浏览器工具访问 BlockBeats 页面并执行：

```javascript
const data = window.__NUXT__.data[0];
return {
  title: data.info.title,
  abstract: data.info.abstract,
  content: data.info.content
};
```

### 2. 保存到 ChainThink

调用 API：

```bash
curl 'https://api-v2.chainthink.cn/ccs/v1/admin/content/publish' \
  -H 'Content-Type: application/json' \
  -H 'X-App-Id: 101' \
  -H 'x-token: <从TOOLS.md读取>' \
  -H 'x-user-id: 51' \
  --data-raw '{
    "id": "0",
    "is_translate": true,
    "translation": {
      "zh-CN": {
        "title": "<文章标题>",
        "text": "<HTML正文>",
        "abstract": "<摘要>"
      }
    },
    "type": 5,
    "is_public": false,
    "user_id": "3",
    "as_user_id": "3"
  }'
```

### 3. 返回结果

返回保存成功的文章 ID 和状态。

## 注意事项

- 图片链接保留原始 CDN 地址（`https://image.blockbeats.cn/...`）
- 内容格式为 HTML，保留所有标签
- 文章默认保存为草稿（`is_public: false`）
- Token 有效期约 7 天，过期需要重新获取

## Token 配置

在 TOOLS.md 中添加：

```markdown
### ChainThink API Token

x-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
x-user-id: 51
```
