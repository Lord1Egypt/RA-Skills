# 示例脚本

本文档提供 `document-organizer` 技能的实用示例代码和典型工作流。

---

## 目录

1. [基本用法](#基本用法)
2. [Python API 调用](#python-api-调用)
3. [自定义工作流](#自定义工作流)
4. [批量参数化](#批量参数化)
5. [错误处理](#错误处理)
6. [与其他工具集成](#与其他工具集成)
7. [生产环境脚本](#生产环境脚本)

---

## 基本用法

### 示例 1: 最简单的命令行调用

```bash
# 转换整个目录（自动处理所有支持的格式）
npx skills run document-organizer --source "G:\docs" --output "D:\md"

# 指定格式
npx skills run document-organizer --source "G:\docs" --type doc,xls
```

---

### 示例 2: 仅 PDF 转换

```bash
npx skills run document-organizer \
  --source "G:\pdf_library" \
  --type pdf \
  --output "D:\pdf_md" \
  --verbose
```

---

### 示例 3: 预览模式（Dry Run）

```bash
# 查看将要转换的文件统计，不实际执行
npx skills run document-organizer --source "G:\docs" --dry-run --verbose

# 输出类似:
# 扫描结果: 2,450 个文件，156 个子目录
# 按类型:
#   - .doc:  800 个
#   - .docx: 300 个
#   - .xls: 1,200 个
#   - .pdf:  150 个
```

---

## Python API 调用

### 示例 4: 脚本化调用（最灵活）

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自定义文档整理脚本
"""

import sys
sys.path.append('d:\\workspace\\pip-packages')

from pathlib import Path
from markitdown import MarkItDown
import subprocess
import shutil
from datetime import datetime

# ==================== 配置 ====================
SOURCE = Path(r"G:\docs")
OUTPUT = Path(r"D:\knowledge")
TEMP = Path(r"D:\fast_ssd\temp")
SOFFICE = r"D:\Program Files\LibreOffice\program\soffice.exe"
# =============================================

def find_libreoffice():
    if Path(SOFFICE).exists():
        return SOFFICE
    # 其他路径...
    return None

def scan_files(source):
    """扫描支持的文件"""
    files = []
    for ext in ['.doc', '.docx', '.xls', '.xlsx', '.pdf']:
        files.extend(source.rglob(f"*{ext}"))
    return files

def convert():
    soffice = find_libreoffice()
    if not soffice:
        raise RuntimeError("LibreOffice not found")

    md = MarkItDown()

    files = scan_files(SOURCE)
    print(f"找到 {len(files)} 个文件")

    # 按类型分组
    docs = [f for f in files if f.suffix.lower() in ['.doc']]
    xlss = [f for f in files if f.suffix.lower() in ['.xls']]
    modern = [f for f in files if f.suffix.lower() in ['.docx', '.xlsx']]
    pdfs = [f for f in files if f.suffix.lower() == '.pdf']

    print(f"  .doc: {len(docs)}")
    print(f"  .xls: {len(xlss)}")
    print(f"  现代 Office: {len(modern)}")
    print(f"  .pdf: {len(pdfs)}")

    # TODO: 实现转换逻辑（参考 batch_convert.py）

if __name__ == "__main__":
    convert()
```

---

### 示例 5: 只转换特定子目录

```python
from pathlib import Path
from document_organizer import scan_files, convert_docs  # 假设已模块化

# 仅处理 "06_需求分析" 子目录
source = Path(r"G:\VSS_SINOCHEM")
target_subdir = source / "流程信息项目" / "06_需求分析"

# 方式 1: 直接按子目录转换
from document_organizer import convert_directory

convert_directory(
    source_dir=target_subdir,
    output_dir=OUTPUT / "06_需求分析",
    types=['.doc', '.xls']
)

# 方式 2: 过滤扫描结果
all_files = scan_files(source, ['.doc', '.xls'])
filtered = {k: v for k, v in all_files.items() if "06_需求分析" in k}
```

---

### 示例 6: 增量转换（跳过已转换）

```python
from pathlib import Path
import json

CHECKPOINT = Path("converted_checkpoint.json")

def load_checkpoint():
    if CHECKPOINT.exists():
        return set(json.loads(CHECKPOINT.read_text()))
    return set()

def save_checkpoint(converted_files):
    CHECKPOINT.write_text(json.dumps(list(converted_files), indent=2))

def convert_incremental():
    checkpoint = load_checkpoint()
    new_files = []

    for file in scan_files(SOURCE, ['.doc', '.xls']):
        if str(file) in checkpoint:
            continue
        new_files.append(file)

    print(f"新文件: {len(new_files)}")
    # 只转换 new_files...

    # 完成后更新 checkpoint
    checkpoint.update(str(f) for f in new_files)
    save_checkpoint(checkpoint)

convert_incremental()
```

---

## 自定义工作流

### 示例 7: 按项目分别输出

```python
projects = {
    "vss_CEB": Path(r"G:\vss_CEB"),
    "VSS_SINOCHEM": Path(r"G:\VSS_SINOCHEM"),
    "新晨科技": Path(r"G:\新晨科技")
}

for name, src in projects.items():
    out = OUTPUT / name
    print(f"\n处理项目: {name}")

    cmd = [
        "npx", "skills", "run", "document-organizer",
        "--source", str(src),
        "--output", str(out),
        "--log-file", f"logs/{name}.log"
    ]
    subprocess.run(cmd)  # 串行，可改为并行
```

---

### 示例 8: 失败文件重试

```python
import re

def parse_failed_from_log(log_file):
    """从日志解析失败文件"""
    failed = []
    for line in Path(log_file).read_text().splitlines():
        if line.startswith("- ["):
            # - [doc] G:\docs\file.doc: error msg
            m = re.search(r'- \[(.*?)\] (.*?):', line)
            if m:
                failed.append(Path(m.group(2)))
    return failed

def retry_failed():
    log = Path("conversion.log")
    if not log.exists():
        print("无日志文件")
        return

    failed_files = parse_failed_from_log(log)
    print(f"失败文件: {len(failed_files)}")

    # 重试（使用更宽松参数）
    for f in failed_files:
        # 手动转换单个文件
        try:
            # 根据后缀选择方法
            if f.suffix == '.doc':
                subprocess.run([SOFFICE, "--convert-to", "markdown", str(f)])
            elif f.suffix in ['.xlsx', '.docx']:
                from markitdown import MarkItDown
                md = MarkItDown()
                result = md.convert(str(f))
                (f.parent / f.with_suffix('.md').name).write_text(result.text_content)
            print(f"  [OK] {f.name}")
        except Exception as e:
            print(f"  [FAIL] {f.name}: {e}")

retry_failed()
```

---

## 批量参数化

### 示例 9: Shell 脚本批量运行

**Windows Batch** (`batch_all.bat`):
```batch
@echo off
set SOURCE_ROOT=G:\projects
set OUTPUT_ROOT=D:\KB

for /d %%P in ("%SOURCE_ROOT%\*") do (
    echo 处理项目: %%~nP
    npx skills run document-organizer ^
      --source "%%P" ^
      --output "%OUTPUT_ROOT%\%%~nP" ^
      --log-file "logs\%%~nP.log"
)
echo 全部完成！
pause
```

**Linux Bash** (`batch_all.sh`):
```bash
#!/bin/bash
SOURCE_ROOT="/mnt/data/projects"
OUTPUT_ROOT="/mnt/kb"

for dir in "$SOURCE_ROOT"/*/; do
    name=$(basename "$dir")
    echo "处理: $name"
    npx skills run document-organizer \
      --source "$dir" \
      --output "$OUTPUT_ROOT/$name" \
      --log-file "logs/$name.log"
done
echo "全部完成！"
```

---

### 示例 10: 按文件大小分批

```python
from pathlib import Path

def batch_by_size(files, max_size_mb=500):
    """按大小分批，每批不超过 max_size_mb"""
    batches = []
    current_batch = []
    current_size = 0

    for f in sorted(files, key=lambda x: x.stat().st_size, reverse=True):
        size_mb = f.stat().st_size / 1024 / 1024
        if current_size + size_mb > max_size_mb and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_size = 0
        current_batch.append(f)
        current_size += size_mb

    if current_batch:
        batches.append(current_batch)

    return batches

# 使用
files = list(Path(r"G:\large_archive").rglob("*.pdf"))
batches = batch_by_size(files, max_size_mb=100)

print(f"分成 {len(batches)} 批，每批 ~100MB")
for i, batch in enumerate(batches, 1):
    print(f"批次 {i}: {len(batch)} 文件，总大小 {sum(f.stat().st_size for f in batch)/1024/1024:.0f} MB")
```

---

## 错误处理

### 示例 11: 自动重试机制

```python
import time
from pathlib import Path

def convert_with_retry(filepath, max_retries=3):
    """单个文件转换带重试"""
    for attempt in range(1, max_retries + 1):
        try:
            if filepath.suffix in ['.doc', '.xls', '.ppt']:
                # 使用 LibreOffice
                subprocess.run([
                    SOFFICE, "--headless", "--convert-to", "markdown",
                    "--outdir", str(filepath.parent),
                    str(filepath)
                ], timeout=300, check=True)
            else:
                # 使用 MarkItDown
                from markitdown import MarkItDown
                md = MarkItDown()
                result = md.convert(str(filepath))
                output = filepath.with_suffix('.md')
                output.write_text(result.text_content, encoding='utf-8')

            print(f"  [OK] {filepath.name}")
            return True

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            print(f"  [RETRY {attempt}/{max_retries}] {filepath.name}: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                print(f"  [FAIL] {filepath.name}: 达到最大重试次数")
                return False

# 批量使用
for file in files:
    convert_with_retry(file)
```

---

### 示例 12: 生成失败报告

```python
from datetime import datetime
import json

def generate_failure_report(failed_list, output_path):
    """生成详细的失败报告"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_failed": len(failed_list),
        "failures": []
    }

    for filepath, error_type, error_msg in failed_list:
        report["failures"].append({
            "file": str(filepath),
            "type": error_type,
            "error": error_msg,
            "size": filepath.stat().st_size if filepath.exists() else None
        })

    # 统计
    by_type = {}
    for f in report["failures"]:
        by_type[f["type"]] = by_type.get(f["type"], 0) + 1

    report["summary"] = {
        "by_type": by_type,
        "most_common": max(by_type.items(), key=lambda x: x[1])[0] if by_type else None
    }

    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"失败报告: {output_path}")

generate_failure_report(all_failed, Path("failure_report.json"))
```

---

## 与其他工具集成

### 示例 13: 与知识库索引集成

```python
from pathlib import Path
import subprocess
import json

def convert_and_reindex(source, output, index_file):
    """转换 + 重建索引"""
    # 1. 转换
    subprocess.run([
        "npx", "skills", "run", "document-organizer",
        "--source", source,
        "--output", output
    ], check=True)

    # 2. 重建索引（假设有 build_index.js）
    subprocess.run([
        "node", "d:\\workspace\\clawd\\knowledge\\build_index.js"
    ], check=True)

    # 3. 验证索引
    index = json.loads(Path(index_file).read_text())
    print(f"索引更新完成: {len(index['files'])} 个文件")

convert_and_reindex(
    source=r"G:\new_batch",
    output=r"d:\workspace\clawd\knowledge\new_batch",
    index_file=r"d:\workspace\clawd\knowledge\INDEX.json"
)
```

---

### 示例 14: 与搜索技能集成

```python
from pathlib import Path
import subprocess
import json

def convert_and_test_search(source, keywords):
    """转换后立即测试搜索"""
    # 转换
    out = Path(r"d:\workspace\clawd\knowledge\test_batch")
    subprocess.run([
        "npx", "skills", "run", "document-organizer",
        "--source", source,
        "--output", str(out)
    ])

    # 使用 search-kb 技能搜索
    for kw in keywords:
        result = subprocess.run(
            ["npx", "skills", "run", "search-kb", "--query", kw],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        print(f"'{kw}' 搜索结果: {len(data['results'])} 条")
```

---

## 生产环境脚本

### 示例 15: 完整的生产就绪脚本

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生产环境文档整理脚本
功能: 扫描、转换、索引、通知
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import json

# ==================== 配置 ====================
CONFIG = {
    "source_roots": [
        r"G:\VSS_SINOCHEM",
        r"G:\vss_CEB",
    ],
    "output_root": Path(r"d:\workspace\clawd\knowledge"),
    "log_dir": Path(r"d:\workspace\clawd\logs"),
    "temp_dir": Path(r"d:\fast_ssd\temp"),
    "index_file": Path(r"d:\workspace\clawd\knowledge\INDEX.json"),
    "notification": {
        "enabled": False,
        "webhook": "https://hooks.slack.com/..."
    }
}
# =============================================

def setup_logging():
    log_file = CONFIG["log_dir"] / f"doc_organizer_{datetime.now():%Y%m%d}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def run_conversion(source, output, log_file):
    """执行转换"""
    logger.info(f"开始转换: {source} → {output}")

    cmd = [
        "npx", "skills", "run", "document-organizer",
        "--source", str(source),
        "--output", str(output),
        "--temp-dir", str(CONFIG["temp_dir"]),
        "--log-file", str(log_file),
        "--verbose"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"转换失败: {result.stderr}")
        raise RuntimeError("Conversion failed")
    logger.info("转换完成")

def rebuild_index():
    """重建知识库索引"""
    logger.info("重建索引...")
    # 假设有重建索引的命令或脚本
    subprocess.run(["node", "build_index.js"], check=True)
    logger.info("索引重建完成")

def send_notification(message):
    """发送通知（可选）"""
    if not CONFIG["notification"]["enabled"]:
        return
    # 实现 Slack/邮件通知
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    logger = setup_logging()

    try:
        total_start = datetime.now()

        for source_dir in CONFIG["source_roots"]:
            source = Path(source_dir)
            if not source.exists():
                logger.warning(f"源目录不存在，跳过: {source}")
                continue

            output = CONFIG["output_root"] / source.name
            log_file = CONFIG["log_dir"] / f"{source.name}.log"

            if args.dry_run:
                logger.info(f"[DRY RUN] 将处理: {source} → {output}")
                continue

            # 转换
            run_conversion(source, output, log_file)

        # 重建索引
        if not args.dry_run:
            rebuild_index()

        # 通知
        elapsed = datetime.now() - total_start
        send_notification(f"✅ 文档整理完成，耗时 {elapsed}")

        logger.info("全部完成！")

    except Exception as e:
        logger.error(f"任务失败: {e}", exc_info=True)
        send_notification(f"❌ 文档整理失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**使用**:
```bash
python production_script.py
python production_script.py --dry-run  # 预览
```

---

## 高级技巧

### 技巧 1: 过滤临时文件

```bash
# 在扫描前先排除临时文件（~$ 开头的）
find . -name "~$*" -delete
# 或在脚本中:
files = [f for f in files if not f.name.startswith('~$')]
```

---

### 技巧 2: 只转换最近修改的文件

```python
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=30)  # 最近 30 天
recent_files = [
    f for f in files
    if datetime.fromtimestamp(f.stat().st_mtime) > cutoff
]
```

---

### 技巧 3: 并发处理多个源目录

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=3) as exec:
    futures = []
    for source in sources:
        futures.append(exec.submit(convert_one_source, source))

    for future in futures:
        future.result()  # 阻塞等待全部完成
```

---

**最后更新**: 2026-03-11  
**版本**: v1.0.0  
**示例库**: 持续更新中...
