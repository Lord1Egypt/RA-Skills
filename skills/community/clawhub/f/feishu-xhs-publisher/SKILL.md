---
name: xhs-publisher
description: >
  将飞书文档/Wiki 转换为小红书图文帖子，生成竖版图片（1242×1660）并打包成新飞书文档供用户直接发布。
  支持深色科技风格（代码块高亮、macOS 窗口样式）和知识卡片风格。
  触发词：发布到小红书、转小红书格式、生成小红书图片、小红书排版、xhs-publisher。
  输入：飞书文档链接（docx）或 Wiki 链接（wiki）。
  输出：包含图片+正文摘要+标题备选+话题标签的新飞书文档链接。
---

# XHS Publisher

将飞书文档转换为小红书图文帖，全流程半自动化，用户收工直接发布。

## 工作流程（5步，每步与用户确认）

### Step 1：读取飞书文档

- **docx 链接**：直接提取 `doc_token`，用飞书 SDK `docx.document.rawContent` 读取内容
- **wiki 链接**：先用 `wiki.space.getNode` 获取 `obj_token`，再读文档内容
- Wiki token 提取：`https://xxx.feishu.cn/wiki/ABC123` → token = `ABC123`

```js
// 飞书 SDK（在 ~/.openclaw/extensions/feishu/ 目录下运行）
const client = new Lark.Client({ appId: '...', appSecret: '...' });

// wiki → obj_token
const node = await client.wiki.space.getNode({ params: { token: wikiToken } });
const objToken = node.node.obj_token;

// 读取内容
const content = await client.docx.document.rawContent({
  path: { document_id: objToken }, params: { lang: 0 }
});
```

### Step 2：润色成小红书风格（AI 改写）

将原文改写为小红书风格，**与用户确认文案**后再进行图片渲染。

改写原则：
- 长段落 → 拆成 2-3 行短句，每段加 emoji 开头
- 标题层级 → `🔥 小节标题` 风格
- 列表 → `👉 要点一`
- 代码块 → **保留原文**，另做代码截图卡
- 表格 → 提炼关键信息转成对比句
- 超链接 → 去掉 URL，保留链接文字

图片分组建议（按内容长度）：
- 短文（<1000字）：5-7 张
- 中等（1000-2500字）：7-10 张
- 长文（>2500字）：10-12 张，可分多篇发布

每个代码块额外生成 1 张代码截图卡（深色背景 + macOS 窗口样式）。

### Step 3：生成 HTML 图片并渲染

在工作目录创建 `cards/` 子目录，每张图一个 HTML 文件（命名按序号：`01_xxx.html`）。

**图片规格**：1242×1660px（3:4 小红书推荐比例）

渲染命令：
```bash
python3 ~/.openclaw/workspace/skills/xhs-publisher/scripts/render_images.py \
  <cards_dir> <output_dir>
```

需要 Playwright：`pip3 install playwright && playwright install chromium`

**设计风格参考**：见 `references/design-styles.md`，默认使用「科技蓝·深空」风格。
**内容卡模板参考**：见 `assets/templates/example_cover.html`。

渲染完成后**打开图片供用户确认**效果再继续。

### Step 4：生成正文摘要 + 标题

**与用户确认**以下内容再进入 Step 5：

1. **正文摘要**（500-800字，小红书风格，含 emoji）
2. **标题备选**（3 个，20字以内，带钩子）
3. **话题标签**（8-10 个 `#xxx` 格式）

### Step 5：上传到飞书文档

飞书 SDK 所在目录：`~/.openclaw/extensions/feishu/`（含 `@larksuiteoapi/node-sdk`）

上传脚本：
```bash
cd ~/.openclaw/extensions/feishu
node ~/.openclaw/workspace/skills/xhs-publisher/scripts/upload_to_feishu.cjs \
  <output_dir> <doc_title> [summary_md_file]
```

图片上传**三步法**（顺序不能错）：
1. 创建空图片块（`documentBlockChildren.create`，`block_type: 27`）
2. 用**图片块 blockId** 作为 `parent_node` 上传图片（⚠️ 不是 docId）
3. `patch` 图片块填入 `file_token`

```js
// ⚠️ 关键：parent_node 用 imageBlockId，不是 docId
const insertRes = await client.docx.documentBlockChildren.create({...});
const imageBlockId = insertRes.data.children[0].block_id;  // 注意是 .data.children

const uploadRes = await client.drive.media.uploadAll({
  data: { parent_type: 'docx_image', parent_node: imageBlockId, ... }
});

await client.docx.documentBlock.patch({
  path: { document_id: docId, block_id: imageBlockId },
  data: { replace_image: { token: uploadRes.file_token } }
});
```

文字内容写入用 Markdown 转换法：
```js
const convertRes = await client.docx.document.convert({
  data: { content_type: 'markdown', content: markdownText }
});
await client.docx.documentBlockDescendant.create({
  path: { document_id: docId, block_id: docId },
  data: {
    children_id: convertRes.data.first_level_block_ids,
    descendants: convertRes.data.blocks,
    index: -1
  }
});
```

完成后发送飞书文档链接给用户。

## 飞书 SDK 配置

SDK 位于 `~/.openclaw/extensions/feishu/`，所有脚本在此目录运行：

```js
const Lark = require('./node_modules/@larksuiteoapi/node-sdk');
const client = new Lark.Client({
  appId: 'cli_a9249001d9f8dcc9',
  appSecret: 'IcxmMHOYNVUGWsuI4Ikp2fjtouXEwDUf',
  domain: Lark.Domain.Feishu,
});
```

文档所有者 open_id：`ou_966010364ecf08ba373bf29bf198a04a`

## 常见问题

| 问题 | 原因 | 解法 |
|------|------|------|
| `relation mismatch` | upload 时 parent_node 用了 docId | 改用 imageBlockId |
| `children is undefined` | 取 `insertRes.children` | 改用 `insertRes.data.children` |
| 图片不显示 | patch 未执行 | 确保三步法完整执行 |
| 文本块写入失败 | 直接用 batchUpdate 创建文本块 | 改用 `document.convert` + `documentBlockDescendant.create` |
