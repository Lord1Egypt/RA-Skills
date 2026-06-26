# Classics Text Cache

为提升检索速度，三本经典使用预抽取的 UTF-8 文本文件作为主读取源：

- `A_滴天髓.txt`
- `B_渊海子平.txt`
- `C_穷通宝鉴.txt`

## 当前覆盖缺口（需补全）

| 文件 | 缺失内容 | 影响 |
|------|----------|------|
| `B_渊海子平.txt` | 格局论核心章节（成格/破格/从格/化格判断规则）完全缺失，当前仅含基础命理/十神/神煞/六亲入门内容 | Step 2「结构优先」无文本支撑，必须从源 PDF 重新提取完整版 |
| `C_穷通宝鉴.txt` | 乙木完整版、丁火、戊土、己土、庚金、辛金、癸水调候章节缺失，当前约覆盖 60% 天干 | Step 3「调候校正」对缺失天干无法给出调候依据 |
| `A_滴天髓.txt` | 整体覆盖较完整，暂无已知缺口 | — |

**在补全前，涉及缺失内容的分析结论不得标注对应来源标签；应在输出中注明"当前文本节选，[B-结构]/[C-调候] 依据不完整"。**

## Regenerate

在项目根目录执行（需先准备好 PDF 源文件，通过 `--pdf-a/b/c` 参数指定路径）：

```bash
python scripts/extract_classics_text.py \
  --pdf-a /path/to/滴天髓.pdf \
  --pdf-b /path/to/渊海子平.pdf \
  --pdf-c /path/to/穷通宝鉴.pdf \
  --output-dir references/classics
```

如需同时生成 markdown 文件：

```bash
python scripts/extract_classics_text.py \
  --pdf-a /path/to/滴天髓.pdf \
  --pdf-b /path/to/渊海子平.pdf \
  --pdf-c /path/to/穷通宝鉴.pdf \
  --output-dir references/classics \
  --md
```

## Source PDFs

PDF 源文件需由使用者自行提供，不随 skill 包分发。运行脚本时通过参数传入路径（见上方命令）。
