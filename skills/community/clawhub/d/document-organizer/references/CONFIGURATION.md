# 配置指南

本文档说明 `document-organizer` 技能的所有配置选项、环境变量和自定义设置。

---

## 配置层级

配置按优先级从高到低：

1. **命令行参数**（最高）
2. **环境变量**
3. **配置文件**（manifest.json 默认值）
4. **内置默认值**（最低）

---

## 命令行参数

### 必需参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `--source` | `str` | 源目录路径（必需） | `--source "G:\docs"` |

### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--output` | `str` | `./output` | 输出目录路径 |
| `--type` | `str` | `doc,xls,docx,xlsx,ppt,pptx,pdf` | 处理的文件类型（逗号分隔） |
| `--soffice-path` | `str` | 自动检测 | LibreOffice soffice.exe 路径 |
| `--temp-dir` | `str` | `./temp_batch` | 临时文件目录（处理完后自动删除） |
| `--log-file` | `str` | `conversion.log` | 错误日志文件路径 |
| `--dry-run` | `bool` | `false` | 仅扫描统计，不执行转换 |
| `--verbose` | `bool` | `false` | 详细日志输出 |
| `--help` | - | - | 显示帮助信息 |

---

## 环境变量

| 变量 | 覆盖参数 | 说明 | 示例 |
|------|---------|------|------|
| `DO_SOURCE` | `--source` | 源目录 | `export DO_SOURCE="/data/docs"` |
| `DO_OUTPUT` | `--output` | 输出目录 | `set DO_OUTPUT="D:\\md"` |
| `DO_TYPES` | `--type` | 文件类型 | `export DO_TYPES=".doc,.xls"` |
| `SOFFICE_PATH` | `--soffice-path` | LibreOffice 路径 | `set SOFFICE_PATH="C:\\LibreOffice\\soffice.exe"` |
| `DO_TEMP_DIR` | `--temp-dir` | 临时目录 | `set DO_TEMP_DIR="D:\\temp"` |
| `DO_LOG_FILE` | `--log-file` | 日志文件 | `export DO_LOG_FILE="/var/log/do.log"` |

**优先级**: 命令行参数 > 环境变量

---

## 配置文件

技能使用 `manifest.json` 定义默认配置：

```json
{
  "config": {
    "default_source": null,
    "default_output": "./output",
    "default_types": ["doc", "xls", "docx", "xlsx", "ppt", "pptx", "pdf"],
    "temp_dir": "./temp_batch",
    "log_file": "conversion.log",
    "soffice_path": null,
    "recursive": true,
    "keep_structure": true
  }
}
```

### 覆盖配置

可以创建本地配置文件 `config.local.json`（gitignore）：

```json
{
  "soffice_path": "D:\\Custom\\LibreOffice\\soffice.exe",
  "temp_dir": "D:\\fast_ssd\\temp",
  "log_file": "D:\\logs\\conversion.log"
}
```

加载顺序（如果存在）:
1. `config.json`（项目根目录）
2. `config.local.json`（本地覆盖）
3. `manifest.json`（技能自带）

---

## LibreOffice 路径配置

### 自动检测顺序

1. `--soffice-path` 命令行参数
2. `SOFFICE_PATH` 环境变量
3. `manifest.json` 中的 `config.soffice_path`
4. 系统 PATH 中的 `soffice`
5. 默认路径扫描：
   - Windows: `D:\Program Files\LibreOffice\program\soffice.exe`
   - Windows: `C:\Program Files\LibreOffice\program\soffice.exe`
   - Linux: `/usr/bin/soffice`
   - macOS: `/Applications/LibreOffice.app/Contents/MacOS/soffice`

### 自定义路径

```bash
# 命令行指定
npx skills run document-organizer --source "docs" --soffice-path "D:\LibreOffice\soffice.exe"

# 环境变量
set SOFFICE_PATH="D:\LibreOffice\soffice.exe"
npx skills run document-organizer --source "docs"

# 配置文件
{
  "config": {
    "soffice_path": "D:\\LibreOffice\\soffice.exe"
  }
}
```

---

## 临时文件管理

### 临时目录结构

```
temp_batch/
├── docs/                  # Word 临时文件
│   ├── 子目录A/
│   │   ├── file1.doc
│   │   └── file2.doc
├── excels/               # Excel 临时文件
│   ├── 子目录B/
│   │   ├── file1.xls
│   │   └── file1.xlsx   # 转换后
├── presentations/        # PPT 临时文件
└── ... (其他类型)
```

### 配置选项

| 配置项 | 说明 | 推荐值 |
|--------|------|--------|
| `temp_dir` | 临时文件存放位置 | 使用 SSD 快速盘（如 `D:\temp`） |
| `cleanup` | 处理完后是否删除 | `true`（始终清理）|

**性能建议**:
- 将 `temp_dir` 设置在高速 SSD 上
- 确保有足够空间（至少 2x 源文件大小）
- 避免网络驱动器（速度慢）

---

## 日志配置

### 日志文件位置

默认: `conversion.log`（当前工作目录）

可配置:
```bash
--log-file "D:\logs\conversion-2026-03-11.log"
```

### 日志格式

```
# 转换失败记录 (2026-03-11 13:00:00)

## LibreOffice 转换失败
- G:\docs\bad.doc: Exit code: 1, stderr: ...

## MarkItDown 转换失败
- G:\docs\corrupt.xlsx: Traceback...
```

### 日志轮转

建议使用日志管理工具（如 `logrotate` 或 Windows 事件查看器）自动轮转。

---

## 性能调优配置

### 批量大小

按目录分组批量转换的优势：
- 减少 LibreOffice 启动开销
- 默认已优化，无需调整

### 超时设置

```python
# 在 batch_convert.py 中修改
timeout = 300  # 秒，默认 5 分钟

# 对于大文件，可以增加
timeout_large = 600  # 10 分钟
```

### 并行处理（高级）

当前版本是串行处理（按目录顺序）。如需并行：

```python
# 修改 convert_docs 函数
from concurrent.futures import ThreadPoolExecutor

def convert_docs_parallel(by_dir, ...):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for parent_dir, files in by_dir.items():
            futures.append(executor.submit(convert_single_dir, parent_dir, files, ...))
        # 收集结果
```

**警告**: 并行可能增加内存压力，建议先测试。

---

## 高级配置示例

### 场景 1: 企业级批量处理

```bash
npx skills run document-organizer \
  --source "\\fileserver\projects\archive" \
  --output "D:\KnowledgeBase\Archive" \
  --type doc,xls,pdf \
  --soffice-path "D:\Program Files\LibreOffice\program\soffice.exe" \
  --temp-dir "D:\NVMe_SSD\temp" \
  --log-file "D:\logs\conversion-%Y%m%d.log" \
  --verbose
```

### 场景 2: 内存受限环境

```bash
# 使用小临时目录，限制并发（修改脚本）
--temp-dir "/dev/shm/temp"  # Linux RAM disk
# 或修改脚本: max_workers=1
```

### 场景 3: 开发测试

```bash
# Dry run 检查文件列表
npx skills run document-organizer --source "G:\new_docs" --dry-run --verbose

# 仅转换 10 个文件测试
npx skills run document-organizer --source "G:\new_docs" --limit 10
# （需修改脚本支持 --limit）
```

---

## 自定义依赖

### 最小依赖（仅现代格式）

```json
{
  "dependencies": {
    "pip_packages": [
      "markitdown[docx,xlsx]>=0.1.5"
    ]
  }
}
```

### 完整依赖（含 PDF OCR）

```json
{
  "dependencies": {
    "pip_packages": [
      "markitdown[docx,xlsx,pdf]>=0.1.5",
      "pillow>=10.0.0",
      "pytesseract>=0.3.10"
    ],
    "external_tools": [
      {
        "name": "Tesseract OCR",
        "required": false,
        "download_url": "https://github.com/tesseract-ocr/tesseract"
      }
    ]
  }
}
```

---

## 配置文件验证

使用 Python 验证配置：

```python
import json
from pathlib import Path

def validate_config(config_path):
    with open(config_path) as f:
        config = json.load(f)

    required = ['source', 'output', 'type']
    for key in required:
        if key not in config:
            raise ValueError(f"Missing required config: {key}")

    # 验证路径存在
    if not Path(config['source']).exists():
        raise FileNotFoundError(f"Source not found: {config['source']}")

    print("配置验证通过")

validate_config("config.json")
```

---

## 故障排除配置问题

### 问题 1: "Cannot find LibreOffice"

**解决**:
```bash
# 1. 确认 LibreOffice 安装
where soffice  # Windows
which soffice  # Linux/macOS

# 2. 显式指定路径
--soffice-path "C:\Program Files\LibreOffice\program\soffice.exe"
```

### 问题 2: 权限错误

**解决**:
- 确保对源目录有读取权限
- 确保对输出目录有写入权限
- 使用管理员权限（Windows）或 `sudo`（Linux）

### 问题 3: 磁盘空间不足

**解决**:
```bash
# 检查空间
df -h  # Linux/macOS
dir D:\  # Windows

# 清理临时目录
--temp-dir "D:\fast_ssd\temp"  # 使用大容量快速盘
```

### 问题 4: 内存不足

**解决**:
- 减少 `--type` 指定 fewer formats
- 使用 `--dry-run` 先评估规模
- 分批处理（分目录多次运行）

---

## 配置检查清单

发布前检查：

- [ ] `--source` 路径正确且有权限
- [ ] `--output` 目录可写（或自动创建）
- [ ] `--soffice-path` 正确（如需）
- [ ] `--temp-dir` 在快速盘且有足够空间
- [ ] `--log-file` 路径可写
- [ ] `--type` 包含所有需要处理的格式
- [ ] `--dry-run` 先验证文件统计

---

**最后更新**: 2026-03-11  
**对应版本**: document-organizer v1.0.0  
**配置示例**: 见 `examples/` 目录
