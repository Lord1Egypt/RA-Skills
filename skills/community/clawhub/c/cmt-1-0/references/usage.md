# 敏感词检测工具 - 使用指南

## 安装依赖

```bash
pip install python-docx openpyxl pypdf2 pymupdf
```

## 使用方法

### 使用内置词库（推荐，无需额外文件）

```bash
python sensitive_word_checker.py --input <待检测文件>
```

### 使用外部词库文件

```bash
python sensitive_word_checker.py --words <敏感词库.docx> --input <待检测文件>
```

### 示例

```bash
# 使用内置词库检测Word文档（最简用法）
python sensitive_word_checker.py --input "合同.docx"

# 使用内置词库检测PDF
python sensitive_word_checker.py --input "文档.pdf"

# 使用内置词库检测Excel
python sensitive_word_checker.py --input "表格.xlsx"

# 指定输出目录
python sensitive_word_checker.py --input "文档.pdf" --output "D:/输出"

# 使用外部词库文件
python sensitive_word_checker.py --words "敏感词库.docx" --input "合同.docx"
```

## 参数说明

| 参数 | 说明 | 是否必填 |
|------|------|----------|
| `--input` | 待检测文件路径 | **必填** |
| `--words` | 外部敏感词库文件路径 (.docx) | 可选，不填则用内置词库 |
| `--output` | 输出目录（默认桌面） | 可选 |

## 内置敏感词库

内置9类65个敏感词，涵盖：高规格名号、会议名称、评奖活动、企业专题、名称包含、报社文本、茶歇宴会、收费合同、其他。

## 输出说明

- Word (.docx): 黄色高亮文本（仅敏感词本身标黄）
- Excel (.xlsx/.xls): 黄色背景单元格
- PDF: 黄色高亮注释（需要pymupdf）
- 默认输出到桌面

## 注意事项

1. 敏感词匹配不区分大小写
2. 支持部分匹配 (如"广告"会匹配"广告投放")
3. 输出文件默认保存到桌面
4. PDF高亮需要安装pymupdf库
5. 如需更新内置词库，编辑脚本顶部的 BUILTIN_WORDS 列表
