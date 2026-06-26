# API 参考文档

本文档详细说明 `document-organizer` 技能的所有公共函数和接口。

---

## 模块结构

```
document-organizer/
├── scripts/
│   └── batch_convert.py    # 主脚本（所有 API 所在）
└── references/
    ├── INDEX.md            # 本文件
    ├── API_REFERENCE.md    # 详细 API 说明
    ├── FORMATS.md         # 格式支持细节
    ├── CONFIGURATION.md   # 配置管理
    ├── TROUBLESHOOTING.md # 故障排除
    ├── PERFORMANCE.md     # 性能调优
    └── EXAMPLES.md        # 示例脚本
```

---

## 核心函数签名

### 1. `find_libreoffice() -> Optional[str]`

**用途**: 自动检测 LibreOffice 安装路径

**返回值**:
- `str`: LibreOffice `soffice.exe` 完整路径
- `None`: 未找到

**搜索顺序**:
1. `D:\Program Files\LibreOffice\program\soffice.exe`
2. `C:\Program Files\LibreOffice\program\soffice.exe`
3. `/usr/bin/soffice` (Linux)
4. `/Applications/LibreOffice.app/Contents/MacOS/soffice` (macOS)

**示例**:
```python
soffice_path = find_libreoffice()
if not soffice_path:
    raise RuntimeError("LibreOffice not found")
```

---

### 2. `scan_files(source_dir: str, file_types: List[str]) -> Dict[str, List[Path]]`

**用途**: 递归扫描目录，按文件类型和子目录分组

**参数**:
- `source_dir`: 源目录路径（字符串或 Path）
- `file_types`: 文件类型列表，如 `['.doc', '.xls', '.pdf']`

**智能匹配**:
- `.doc` 会同时匹配 `.doc` 和 `.docx`
- `.xls` 会同时匹配 `.xls` 和 `.xlsx`
- `.ppt` 会同时匹配 `.ppt` 和 `.pptx`

**返回值**:
```python
{
    "子目录路径1": [Path1, Path2, ...],
    "子目录路径2": [Path3, Path4, ...],
    ...
}
```

**示例**:
```python
by_dir = scan_files("G:\\docs", ['.doc', '.xls'])
for parent, files in by_dir.items():
    print(f"{parent}: {len(files)} files")
```

---

### 3. `convert_docs(by_dir, source_dir, output_dir, soffice_path, temp_root) -> (int, List[Tuple])`

**用途**: 批量转换 `.doc` 文件为 Markdown

**流程**:
1. 为每个子目录创建输出目录
2. 复制 `.doc` 文件到临时目录
3. 批量调用 `soffice --convert-to markdown *.doc`
4. 重命名 `.markdown` 为 `.md`
5. 清理临时文件

**参数**:
- `by_dir`: 按目录分组的文件字典（来自 `scan_files`）
- `source_dir`: 源目录根路径
- `output_dir`: 输出目录根路径
- `soffice_path`: LibreOffice 可执行文件路径
- `temp_root`: 临时文件根目录

**返回值**:
- `success_count`: 成功转换的文件数
- `failed_list`: 失败记录列表 `[(parent_dir, error_msg), ...]`

**注意**:
- 按目录批量转换，不是单个文件
- 每个文件单独处理失败不会中断整体流程

---

### 4. `convert_excels(by_dir, source_dir, output_dir, soffice_path, temp_root, md_converter) -> (int, List[Tuple])`

**用途**: 批量转换 `.xls` 文件为 Markdown（保持表格结构）

**流程**:
1. 复制 `.xls` 到临时目录
2. 调用 LibreOffice 批量转 `.xlsx`
3. 使用 MarkItDown 将 `.xlsx` 转 `.md`
4. 清理临时文件

**参数**:
- `by_dir`: 按目录分组的 `.xls` 文件
- `md_converter`: `MarkItDown()` 实例（已初始化）

**返回值**:
- `success_count`: 成功数量
- `failed_list`: 失败记录 `[(file_path, error_msg), ...]`

**关键代码**:
```python
cmd = [soffice_path, "--headless", "--convert-to", "xlsx", ...]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
for xlsx_file in temp_subdir.glob("*.xlsx"):
    result = md_converter.convert(str(xlsx_file))
    md_file.write_text(result.text_content, encoding='utf-8')
```

---

### 5. `convert_presentations(by_dir, source_dir, output_dir, soffice_path, temp_root, md_converter) -> (int, List[Tuple])`

**用途**: 批量转换 `.ppt` 文件为 Markdown

**流程**: 与 `convert_excels` 相同，但处理的是 PowerPoint

**参数**: 同 `convert_excels`

**返回值**: `(成功数, 失败列表)`

---

### 6. `convert_pdfs(by_dir, output_dir, md_converter) -> (int, List[Tuple])`

**用途**: 批量转换 `.pdf` 文件为 Markdown

**特点**:
- 直接调用 MarkItDown（无需 LibreOffice）
- 支持文本提取和表格保留
- 可选 OCR（需配置 `--ocr`）

**参数**:
- `by_dir`: 按目录分组的 `.pdf` 文件
- `output_dir`: 输出根目录
- `md_converter`: MarkItDown 实例

**返回值**: `(成功数, 失败列表)`

**示例**:
```python
md = MarkItDown()
pdf_files_by_dir = scan_files(source, ['.pdf'])
success, failed = convert_pdfs(pdf_files_by_dir, output_dir, md)
```

---

### 7. `convert_modern(by_dir, suffix, converter, label) -> int`

**用途**: 通用现代格式转换（`.docx`, `.xlsx`, `.pptx`）

**参数**:
- `by_dir`: 按目录分组的文件
- `suffix`: 文件扩展名（用于日志显示）
- `converter`: MarkItDown 实例
- `label`: 类型标签（如 "DOCX"）

**返回值**: 成功转换的文件数

**内部调用**:
```python
result = converter.convert(str(src_file))
md_file.write_text(result.text_content, encoding='utf-8')
```

---

### 8. `main() -> None`

**用途**: 命令行入口点

**命令行参数**:
```bash
python batch_convert.py \
  --source "源目录" \
  --output "输出目录" \
  --type "doc,xls,docx,xlsx,ppt,pptx,pdf" \
  --soffice-path "自动检测" \
  --temp-dir "./temp_batch" \
  --log-file "conversion.log" \
  --dry-run
```

**执行流程**:
1. 初始化（检测 LibreOffice）
2. 扫描文件（`scan_files`）
3. 分离类型（`doc_files_by_dir`, `xls_files_by_dir`, ...）
4. 按顺序转换：
   - `convert_docs()` → 旧版 Word
   - `convert_excels()` → 旧版 Excel
   - `convert_presentations()` → 旧版 PPT
   - `convert_modern()` → 新版 Office
   - `convert_pdfs()` → PDF
5. 清理临时文件
6. 输出统计报告
7. 写入错误日志（如有）

---

## 数据模型

### 按目录分组结构 (`by_dir`)

```python
{
    "相对路径/子目录A": [
        Path("G:/docs/子目录A/file1.doc"),
        Path("G:/docs/子目录A/file2.doc"),
    ],
    "相对路径/子目录B": [
        Path("G:/docs/子目录B/file3.xls"),
    ]
}
```

**用途**: 保持目录结构，批量处理优化

---

### 错误记录格式

```python
all_failed = [
    (file_path, file_type, error_message),
    # 例如:
    ("G:/docs/bad.doc", "doc", "LibreOffice timeout"),
    ("G:/docs/corrupt.xls", "xls", "MarkItDown failed: ..."),
]
```

**日志输出** (追加到 `conversion.log`):
```markdown
# 转换失败记录 (2026-03-11 13:00:00)
- [doc] G:/docs/bad.doc: LibreOffice timeout
- [xls] G:/docs/corrupt.xls: MarkItDown failed: ...
```

---

## 配置接口

### 环境变量

| 变量 | 说明 | 默认 |
|------|------|------|
| `SOFFICE_PATH` | LibreOffice 路径 | 自动检测 |
| `MARKITDOWN_OPTS` | MarkItDown 选项 | `{}` |

### 配置文件

技能支持 `manifest.json` 中定义的配置项，可通过 CLI 参数覆盖。

---

## 扩展点

### 添加新格式支持

1. **在 `scan_files` 中扩展类型匹配**
```python
if ft == '.newformat':
    all_files.extend(source.rglob('*.newformat'))
    all_files.extend(source.rglob('*.newformatx'))  # 智能匹配
```

2. **实现转换函数**
```python
def convert_newformat(by_dir, output_dir, converter):
    # 类似 convert_pdfs
    pass
```

3. **在 `main()` 中调用**
```python
new_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.newformat'] for p, fs in by_dir.items()}
if any(new_files_by_dir.values()):
    convert_newformat(new_files_by_dir, output_dir, md_converter)
```

---

## 异常处理

所有转换函数都使用 `try-except` 捕获异常，确保：
- 单个文件失败不影响其他文件
- 失败记录写入日志
- 临时文件始终清理（`finally` 或在 `except` 中）

**超时处理**:
```python
except subprocess.TimeoutExpired:
    failed.append((parent_dir, "Timeout"))
    shutil.rmtree(temp_subdir, ignore_errors=True)
    continue
```

---

## 类型提示（Type Hints）

完整类型提示（Python 3.10+）:
```python
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def scan_files(source_dir: str, file_types: List[str]) -> Dict[str, List[Path]]:
    ...

def convert_docs(
    by_dir: Dict[str, List[Path]],
    source_dir: Path,
    output_dir: Path,
    soffice_path: str,
    temp_root: Path
) -> Tuple[int, List[Tuple[str, str]]]:
    ...
```

---

## 性能相关

### 临时文件清理

所有转换函数都确保：
```python
shutil.rmtree(temp_subdir, ignore_errors=True)  # 每个子目录处理完后
# 最后
shutil.rmtree(TEMP_ROOT, ignore_errors=True)    # 总体清理
```

### 超时设置

LibreOffice 转换: `timeout=300` (5分钟)  
MarkItDown 转换: 无超时（依赖库内部处理）

---

## 测试示例

```python
# 测试扫描功能
by_dir = scan_files("test_docs", ['.doc', '.xls'])
assert len(by_dir) > 0
print(f"找到 {sum(len(v) for v in by_dir.values())} 个文件")

# 测试转换（小批量）
from markitdown import MarkItDown
md = MarkItDown()
success, failed = convert_docs(by_dir, Path("test_docs"), Path("output"), soffice_path, Path("./temp"))
print(f"成功: {success}, 失败: {len(failed)}")
```

---

**最后更新**: 2026-03-11  
**模块**: `scripts/batch_convert.py`  
**版本**: 1.0.0
