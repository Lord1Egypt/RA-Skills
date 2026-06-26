---
name: feishu-doc-skill
description: 当用户提供飞书 wiki、docx、知识库页面链接，并希望读取、总结、比对、抽取内容、把结果写回飞书文档，或把本地图片插入飞书文档时使用。这个技能会先从链接中提取文档标识，优先通过飞书 OpenAPI 读取正文；做需求分析时优先输出 Markdown，调试接口结构时再输出 JSON。
---

# 飞书文档读写

当用户要求你“读取飞书文档”“总结飞书 wiki”“比较两个飞书页面”“抽取页面中的表格、接口定义、需求说明”“把内容写回飞书文档”“把本地截图插入飞书文档”等内容时，使用这个技能。

## 默认策略

1. 先判断任务类型。
   - 读取正文
   - 输出 Markdown / JSON
   - 写回文档
   - 插入本地图片

2. 优先走 API。
   - 如果已经有 `FEISHU_USER_ACCESS_TOKEN`，优先使用用户身份读取和写入。
   - 如果没有用户 token，可以直接运行 `scripts/feishu_oauth_server.js`，再在 `http://127.0.0.1:3333` 页面里填写 `App ID / App Secret` 发起授权。
   - 也可以继续沿用环境变量方式启动 `scripts/feishu_oauth_server.js`。

3. 读取正文时：
   - 默认直接运行 `node scripts/read_feishu_url_md.js <飞书链接>`，不要先手动提取 token，脚本会自己处理链接和 token。
   - 如果用户只想调试结构化返回，运行 `node scripts/read_feishu_url.js <飞书链接>`。
   - 只有在需要看原始接口结构时，再运行 `node scripts/read_feishu_doc.js <doc_or_wiki_token>`。
   - 如果本地已经有 `.feishu-user-token.json`，读取脚本会自动复用，不要求用户重复手填 `FEISHU_USER_ACCESS_TOKEN`。

4. 插入图片时：
   - 只支持“本地图片路径”，不直接复用聊天里的图片附件。
   - 运行 `node scripts/insert_feishu_local_image.js <飞书文档链接或 token> <本地图片绝对路径>`。
   - 如果需要说明文字，再加 `--caption '说明文字'`。

## 输出要求

读取成功后，输出应包含：
- 文档标题
- 来源链接
- 简洁总结
- 用户要求的重点信息

写入或插图成功后，输出应包含：
- 目标文档
- 实际写入结果
- 如失败，明确说明是权限问题、路径问题还是文档类型问题

## 常见限制

- 聊天中的图片附件目前不能稳定当作原始文件直接上传到飞书。
- 如果用户要插图，要求对方提供本地图片绝对路径。
- 如果没有读到正文或写入失败，不要假装成功，要明确说明阻塞点。

## 使用脚本

- 提取 token：`node scripts/extract_feishu_doc_id.js`
- 本地 OAuth 回调：`scripts/feishu_oauth_server.js`
- 读取正文：`node scripts/read_feishu_doc.js`
- 一键读取与摘要：`node scripts/read_feishu_url.js`
- 一键读取为 Markdown：`node scripts/read_feishu_url_md.js`
- 插入本地图片：`node scripts/insert_feishu_local_image.js`

如果是 `wiki` 链接，先提取链接中的 token。读取和插图脚本都会优先尝试把 `wiki token` 解析成实际文档 `obj_token`，再继续操作 docx 内容。
