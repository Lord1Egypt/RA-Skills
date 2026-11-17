# format-official-docx（党政公文格式化）

将纯文本或现有 Word 文档，按党政机关公文格式规范，生成/重排为规范的 `.docx`。
支持 **请示、报告、函、通知、批复、意见、纪要** 等文种，以及密级标注、红头、附件、版记、页码等要素。

> 本技能默认遵循「三号仿宋_GB2312 正文、方正小标宋简体标题、版记落偶数页」等常见规范；
> 具体以你单位印发的格式细则为准。文中示例均使用 `某单位` 等占位名称，请按实际替换。

## 特性

- 生成（generate）与重排（format-only）两种工作流
- 文种：请示 / 报告 / 函 / 通知，校验亦支持 批复 / 意见 / 纪要
- 红头（发文机关+文件）、发文字号、签发人、密级（左上角 三号黑体 `密级★期限`）
- 主送机关自动补全中文冒号；成文日期支持 `--date today` 自动填
- 附件说明（首行缩进）+ 附件首页「附件N」标识
- 发文机关署名居中、成文日期右空四字
- 版记（抄送 / 印发机关 / 印发日期）强制落偶数页
- 字体缺失时主动告警（避免 Word 静默替换导致排版漂移）
- `--bold-headings` 可选：一级黑体标题加粗

## 安装

```bash
pip install -r requirements.txt
```

依赖：`python-docx>=1.2.0`。

## 快速开始

生成一份请示：

```bash
python scripts/generate_official_docx.py \
  --input body.txt --output out.docx --doc-type request \
  --red-header "某单位文件" --outgoing-no "某字〔2026〕1号" --signer "XXX" \
  --title "某单位\n关于某事项的请示" --recipient "某上级机关" \
  --issuer "某单位" --date today --add-closing \
  --attachment "关于某事项的说明" --copy-to "某机关" \
  --print-org "某办公室" --print-date "2026年7月9日" \
  --contact "(联系人：XXX，联系方式：XXXXXXXX)" --secret-level "秘密★1年"
```

将已有 `.docx` 重排为规范格式（**保留表格**）：

```bash
python scripts/generate_official_docx.py \
  --input source.docx --output formatted.docx --doc-type generic \
  --format-only --promote-first-paragraph-title
```

校验格式信号：

```bash
python scripts/check_official_docx.py out.docx --doc-type request
python scripts/check_fonts.py
```

## 常用参数

| 参数 | 说明 |
|---|---|
| `--doc-type` | `generic` / `request` / `report` / `letter` / `notice` |
| `--format-only` | 仅改版式与字体，不新增结尾、署名、附件等要素 |
| `--red-header` | 请示/上行文红头，如 `某单位文件` |
| `--letterhead` | 函的红头机关名称 |
| `--secret-level` | 左上角密级，如 `秘密★1年` |
| `--attachment` | 可多次，附件名称 |
| `--copy-to` | 抄送机关 |
| `--print-org` / `--print-date` | 印发机关 / 印发日期 |
| `--date today` | 自动填入当前日期 |
| `--add-closing` | 请示/报告自动补结尾（仅在缺失时） |
| `--bold-headings` | 一级黑体标题加粗（默认不加粗） |

## 字体说明

生成脚本写入的字体名为规范名称：`方正小标宋简体`、`仿宋_GB2312`、`楷体_GB2312`、
`黑体`、`宋体`、`Times New Roman`。若本机未安装对应字体，Word 打开时会替换渲染，
脚本会在生成时向 stderr 告警。装好字体即可获得与打印一致的规范排版。

## 文种速查

详见 `references/document-types.md`；版式细则见 `references/format-rules.md`。

## License

MIT-0
