# PDF / 富文档来源归档

PDF 的提取、清洗、翻译、富元素识别和完整性验证由
`trans-doc-to-md >=3.0.0,<4.0.0` 负责。本 Skill 只准备来源和归档上下文。

## 乐享内 PDF

```bash
python3 scripts/lexiang_pdf_parse.py <entry_id> \
  --download-pdf \
  --out-dir <work-dir>
```

桥接产物包括原 PDF、不可变 `source.md`、图片清单和含 `parent_id` 的元信息。将这些输入交给
`trans-doc-to-md`，由其按 PDF 模式生成标准 Prepared Markdown Package。

## 本地/公网 PDF

1. 下载并保留原始 PDF。
2. 建立 `meta.json`，至少填写标准字段。
3. 调用 `trans-doc-to-md` 完成全文提取、图片/图表裁剪、双语翻译、富元素标注
   和完整性验证。
4. 保留不可变 `source.md`，最终文件命名为原文标题。

## 上传

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" upload \
  "<work-dir>/<原文标题>.md" \
  --parent-id "<meta.parent_id 或目标目录ID>" \
  --name "<原文标题>" \
  --pin \
  --json
```

`upload-markdown-to-lexiang >=1.1.0,<2.0.0` 直接渲染
`trans-doc-to-md` 的 callout、表格、图片和其他富元素标注。正常流程不再由
本 Skill 使用 MCP 做二次渲染。

## 异常维护

上传后若仅需修复少量错误，可使用 block 工具做人工增量维护。要求：

1. 修改前读取当前线上状态。
2. 只改目标块。
3. 每项修改同步回本地最终 Markdown。
4. 若问题可复现，应归因到 trans-doc-to-md 或 uploader，并在对应公共 Skill
   修复；不要把渲染逻辑复制回本 Skill。

## 自检

- `source.md` 未修改。
- trans-doc-to-md 完整性验证通过。
- 最终 Markdown 中本地图片全部存在。
- uploader `verified == true`。
- uploader `local_images == remote_images`。
- 未执行常规 MCP 二次渲染。
