English | [中文](README_CN.md)

# feishu-sheet-links

从公开的飞书多维表格中提取所有超链接——覆盖**所有 Sheet 标签页**——并可批量下载链接指向的文章，转为 Markdown 文件。

## 为什么做这个

飞书多维表格采用懒加载机制：每个 Sheet 的数据模型只有在浏览器中被激活后才会加载。常规爬虫只能抓到第一个 Sheet 的数据，其余全部遗漏。

这个工具通过 Chrome DevTools Protocol（CDP）逐一激活每个 Sheet，等待其内部 JavaScript 数据模型加载完成，再从飞书的两种链接存储格式（`url-type` 和 `mention-type`）中提取超链接。

**零 npm 依赖。** 不需要 `npm install`，只依赖 Bun 运行时和 Chrome 浏览器。

## 环境要求

- [Bun](https://bun.sh) 运行时
- Google Chrome 或 Chromium

## 作为 Claude Code Skill 使用

将整个仓库复制到 Claude Code 的 skills 目录：

```bash
cp -r feishu-sheet-links ~/.claude/skills/
```

然后在 Claude Code 中调用：

```
/feishu-sheet-links https://your-feishu-doc.feishu.cn/wiki/...
```

完整的 Skill 接口说明见 [SKILL.md](SKILL.md)。

## 作为独立脚本使用

**第一步 — 提取所有 Sheet 的链接：**

```bash
npx -y bun scripts/main.ts "https://your-feishu-doc.feishu.cn/wiki/..." -o links.json
```

**第二步 — 批量下载链接文章为 Markdown：**

```bash
npx -y bun scripts/download.ts links.json -o ./articles -c 5
```

## 使用说明

### main.ts — 提取链接

```
bun scripts/main.ts <spreadsheet-url> [-o output.json]
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `<spreadsheet-url>` | — | 公开的飞书 wiki 或多维表格 URL |
| `-o <file>` | `feishu-sheet-links.json` | 输出 JSON 文件路径 |

**输出格式：**

```json
{
  "1月": [{ "text": "文章标题", "url": "https://..." }],
  "2月": [...]
}
```

### download.ts — 批量下载文章

```
bun scripts/download.ts <links.json> [-o output-dir] [-c concurrency] [--max-wait ms]
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-o <dir>` | `./feishu-articles` | 输出目录 |
| `-c <n>` | `5` | 并发下载数 |
| `--max-wait <ms>` | `20000` | 每个 URL 的最长等待时间 |

**断点续传：** 每成功下载一个 URL 后保存进度，重新运行会自动跳过已下载的文件。

## 工作原理

1. 优先复用已运行的 Chrome 实例（检测端口 64023、9222、9229），否则自动启动一个新实例
2. 打开多维表格，从 `spreadApp.collaborativeSpread._spread.sheetIdToIndexMap` 读取所有 Sheet ID
3. 对每个 Sheet，单独打开一个 `?sheet=<id>` 标签页，调用 `setActiveSheetIndex()` 触发懒加载，等待 `sheet._dataModel.contentModel` 填充完成
4. 从两种链接存储格式中提取超链接：
   - **url-type：** `contentModel.link.idToRef._map`（整格超链接）
   - **mention-type：** `contentModel.segmentModel.table`（富文本内嵌链接）

## 环境变量

| 变量 | 说明 |
|------|------|
| `FEISHU_CHROME_PATH` | 自定义 Chrome 可执行文件路径 |
| `FEISHU_CHROME_PROFILE` | 自定义 Chrome Profile 目录 |

## 注意事项

- 仅支持**公开**飞书文档，无需登录
- 每个 Sheet 标签页加载约需 8–15 秒，超时时间设置较宽松
- Chrome Profile 与系统默认 Profile 隔离：`~/Library/Application Support/feishu-sheet-links/chrome-profile`（macOS）

## License

MIT
