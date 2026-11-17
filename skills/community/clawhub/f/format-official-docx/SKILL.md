---
name: format-official-docx
description: 将粘贴的中文文本或现有 .docx 文档，转换为符合党政机关公文格式规范的 Word 文档。支持函、请示、报告、通知、批复、意见、纪要、上行文等文种。功能包括红头、发文字号/签发人、密级标注（密级★期限）、主送机关自动补全冒号、--date today 自动填日期、附件说明与附件首页“附件N”标识、发文机关署名居中且成文日期右空四字、版记落偶数页、页码、字体缺失告警，以及保留表格的重排（format-only）模式。附带格式校验脚本。
---

# 党政公文格式化

生成规范的 .docx 文件；不要只给建议而不实际生成。

## 快速流程

1. 判断意图：
   - `format-only`（仅重排）：保留段落文字与顺序，只调整版式与样式。
   - `generate`（生成）：创建公文外壳并撰写简洁正文。
2. 选择文种。若不明确，参考 `references/document-types.md`；否则不必加载。
3. 版式细则参考 `references/format-rules.md`。本地细则优先于通用 GB/T 9704 知识。
4. 用 `scripts/generate_official_docx.py` 生成。
5. 正式公文（请示/函/报告）生成后，尽量运行 `scripts/check_official_docx.py` 做格式校验。
6. 最终文件保存到 `outputs/`。

前置依赖：`python-docx`；若缺失请用 `pip install -r requirements.txt` 安装。

## 核心规则

- 除非用户要求起草或修改，否则保留原文实质内容。
- 不要臆造缺失的元数据；应询问用户，或使用 `XXXX` 等占位符。
- 标题/红头使用方正小标宋简体，正文使用仿宋_GB2312，一级标题使用黑体，二级标题使用楷体_GB2312，数字及拉丁文字使用 Times New Roman。
- 严格的 format-only 模式不得新增结尾、署名、附件或元数据。
- 现有 .docx 的 format-only 重排会保留段落文字与表格（重新套用正文规范字体）；不保留图片、批注、修订痕迹、文本框、复杂页眉。

## 常用命令

生成请示：

```bash
python scripts/generate_official_docx.py --input body.txt --output out.docx --doc-type request --red-header "某单位文件" --outgoing-no "某字〔XXXX〕XX号" --signer "XXX" --title "某单位\n关于XXXX的请示" --recipient "某上级机关：" --issuer "某单位" --date "XXXX年XX月XX日" --add-closing
```

生成函：

```bash
python scripts/generate_official_docx.py --input body.txt --output out.docx --doc-type letter --letterhead "某单位" --outgoing-no "某字〔XXXX〕XX号" --title "关于XXXX的函" --recipient "某单位：" --issuer "某单位" --date "XXXX年XX月XX日" --no-page-number
```

仅重排：

```bash
python scripts/generate_official_docx.py --input source.docx --output formatted.docx --doc-type generic --format-only --promote-first-paragraph-title
```

格式校验：

```bash
python scripts/check_official_docx.py out.docx --doc-type request
python scripts/check_fonts.py
```

## 关键参数

- `--doc-type`：文种，`generic` / `request` / `report` / `letter` / `notice`
- `--format-only`：仅重排模式
- `--red-header`：请示/上行文的红色“发文机关名称+文件”红头
- `--letterhead`：函的红色机关头
- `--letter-special-margins`：仅在明确要求时使用本地函首页页边距（上 5.1 / 下 2.1）
- `--outgoing-no`、`--signer`、`--title`、`--recipient`、`--issuer`、`--date`、`--contact`
- `--attachment`、`--copy-to`、`--print-org`、`--print-date`、`--disclosure-note`
- `--secret-level`：左上角三号黑体密级行，如 `秘密★1年`
- `--add-closing`：仅在缺失时补充标准请示/报告结尾
- `--date today`：自动填入当前日期（也接受 `XXXX年XX月XX日`）
- `--bold-headings`：一级（黑体）标题加粗；默认关闭，遵循三号黑体不加粗规范

## 最终检查

检查标题/红头字体、页边距、行距、首行缩进、标题发文机关行、发文字号/签发人、右对齐的署名与日期、联系人/披露说明、页码、版记。若本机未安装方正小标宋简体或仿宋_GB2312，Word 会替换字体。
