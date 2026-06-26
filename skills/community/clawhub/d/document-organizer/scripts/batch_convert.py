#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文档整理技能 - 批量转换主脚本
支持 .doc → .md, .xls → .md, .docx → .md, .xlsx → .md, .ppt → .md, .pptx → .md, .pdf → .md

用法:
  python batch_convert.py --source "源目录" --output "输出目录" [--type doc,xls] [--dry-run]
"""

import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import sys
import json

def get_markitdown_command():
    """返回 markitdown 命令路径"""
    try:
        # 尝试在 PATH 中查找 markitdown
        result = subprocess.run(["markitdown", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return "markitdown"
    except FileNotFoundError:
        pass
    
    # 尝试使用 python -m markitdown
    try:
        result = subprocess.run([sys.executable, "-m", "markitdown", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return [sys.executable, "-m", "markitdown"]
    except Exception:
        pass
    
    return None

def find_libreoffice():
    """自动查找 LibreOffice 安装路径"""
    possible_paths = [
        r"D:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"/usr/bin/soffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]
    for path in possible_paths:
        if Path(path).exists():
            return path
    return None

def scan_files(source_dir, file_types):
    """扫描目录中的文件，按类型和目录分组"""
    source = Path(source_dir)
    if not source.exists():
        raise ValueError(f"源目录不存在: {source_dir}")

    all_files = []
    for ft in file_types:
        # 智能匹配：.doc 匹配 .doc 和 .docx；.xls 匹配 .xls 和 .xlsx；.ppt 匹配 .ppt 和 .pptx
        if ft == '.doc':
            all_files.extend(source.rglob('*.doc'))
            all_files.extend(source.rglob('*.docx'))
        elif ft == '.xls':
            all_files.extend(source.rglob('*.xls'))
            all_files.extend(source.rglob('*.xlsx'))
        elif ft == '.ppt':
            all_files.extend(source.rglob('*.ppt'))
            all_files.extend(source.rglob('*.pptx'))
        else:
            all_files.extend(source.rglob(f"*{ft}"))

    # 去重
    all_files = list(set(all_files))

    # 按目录分组
    by_dir = {}
    for f in all_files:
        rel_path = f.relative_to(source)
        parent = str(rel_path.parent)
        if parent not in by_dir:
            by_dir[parent] = []
        by_dir[parent].append(f)

    return by_dir

def convert_docs(by_dir, source_dir, output_dir, soffice_path, temp_root):
    """批量转换 .doc 文件为 .md（LibreOffice 直接）"""
    print(f"\n[步骤 1] Word 文档转换 (.doc → .md)")
    success = 0
    failed = []

    for parent_dir, files in by_dir.items():
        output_subdir = output_dir / parent_dir
        output_subdir.mkdir(parents=True, exist_ok=True)

        # 批量转换（直接使用源文件）
        if files:
            # 构建文件路径列表
            file_paths = [str(f) for f in files]
            # 直接生成 .md 文件到目标目录
            cmd = [soffice_path, "--headless", "--convert-to", "md", "--outdir", str(output_subdir)] + file_paths
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode != 0:
                    failed.append((parent_dir, f"LibreOffice exit: {result.returncode}"))
                else:
                    # 计算成功转换的文件数
                    success_count = len(list(output_subdir.glob("*.md")))
                    success += success_count
                    print(f"  {parent_dir}: {success_count}/{len(files)}")
            except subprocess.TimeoutExpired:
                failed.append((parent_dir, "Timeout"))

    return success, failed

def convert_docx(by_dir, source_dir, output_dir, soffice_path, temp_root):
    """批量转换 .docx 文件为 .md（LibreOffice 直接）"""
    print(f"\n[步骤 2] Word 文档转换 (.docx → .md)")
    success = 0
    failed = []

    for parent_dir, files in by_dir.items():
        output_subdir = output_dir / parent_dir
        output_subdir.mkdir(parents=True, exist_ok=True)

        # 批量转换（直接使用源文件）
        if files:
            # 构建文件路径列表
            file_paths = [str(f) for f in files]
            # 直接生成 .md 文件到目标目录
            cmd = [soffice_path, "--headless", "--convert-to", "md", "--outdir", str(output_subdir)] + file_paths
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode != 0:
                    failed.append((parent_dir, f"LibreOffice exit: {result.returncode}"))
                else:
                    # 计算成功转换的文件数
                    success_count = len(list(output_subdir.glob("*.md")))
                    success += success_count
                    print(f"  {parent_dir}: {success_count}/{len(files)}")
            except subprocess.TimeoutExpired:
                failed.append((parent_dir, "Timeout"))

    return success, failed


def convert_excels(by_dir, source_dir, output_dir, soffice_path, temp_root, all_failed):
    """批量转换 .xls 文件：.xls → .xlsx → .md（使用 convert-markdown 技能）"""
    print(f"\n[步骤 3] Excel 表格转换 (.xls → .xlsx → .md)")
    success = 0
    failed = []

    for parent_dir, files in by_dir.items():
        output_subdir = output_dir / parent_dir
        output_subdir.mkdir(parents=True, exist_ok=True)

        temp_subdir = temp_root / "excels" / parent_dir
        temp_subdir.mkdir(parents=True, exist_ok=True)

        # 复制文件到临时目录
        for src_file in files:
            dest = temp_subdir / src_file.name
            try:
                shutil.copy2(src_file, dest)
            except Exception as e:
                print(f"    [WARN] 复制失败 {src_file.name}: {e}")
                continue

        # 批量转 .xlsx（只对 .xls 文件）
        xls_files = [f for f in temp_subdir.glob("*.xls")]
        if xls_files:
            # 使用通配符方式（LibreOffice 支持自动展开）
            cmd = [soffice_path, "--headless", "--convert-to", "xlsx", "--outdir", str(temp_subdir), str(temp_subdir / "*.xls")]
            try:
                print(f"    [DEBUG] CMD: {' '.join(cmd)}")
                print(f"    [DEBUG] 处理 {len(xls_files)} 个 .xls 文件: {[f.name for f in xls_files]}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 增加超时
                if result.returncode != 0:
                    error_msg = f"LibreOffice exit {result.returncode}: {result.stderr or result.stdout}"
                    print(f"    [ERROR] {error_msg}")
                    failed.append((parent_dir, error_msg))
                    shutil.rmtree(temp_subdir, ignore_errors=True)
                    continue
                else:
                    print(f"    [OK] LibreOffice 完成，输出 {len(list(temp_subdir.glob('*.xlsx')))} 个 .xlsx")
            except subprocess.TimeoutExpired:
                error_msg = "LibreOffice timeout (600s)"
                print(f"    [ERROR] {error_msg}")
                failed.append((parent_dir, error_msg))
                shutil.rmtree(temp_subdir, ignore_errors=True)
                continue

        # 对生成的 .xlsx 使用 convert_modern 处理
        xlsx_files = list(temp_subdir.glob("*.xlsx"))
        if xlsx_files:
            # 创建包含 xlsx 文件的目录结构
            xlsx_by_dir = {parent_dir: xlsx_files}
            # 调用 convert_modern 处理 xlsx
            success += convert_modern(xlsx_by_dir, '.xlsx', 'XLSX', output_dir, all_failed)

        shutil.rmtree(temp_subdir, ignore_errors=True)

    return success, failed

def convert_presentations(by_dir, source_dir, output_dir, soffice_path, temp_root, all_failed):
    """批量转换 .ppt 文件：.ppt → .pptx → .md"""
    print(f"\n[步骤 4] PowerPoint 转换 (.ppt → .pptx → .md)")
    success = 0
    failed = []

    for parent_dir, files in by_dir.items():
        if not files:
            continue
        output_subdir = output_dir / parent_dir
        output_subdir.mkdir(parents=True, exist_ok=True)

        temp_subdir = temp_root / "presentations" / parent_dir
        temp_subdir.mkdir(parents=True, exist_ok=True)

        # 复制文件到临时目录
        for src_file in files:
            dest = temp_subdir / src_file.name
            try:
                shutil.copy2(src_file, dest)
            except Exception as e:
                print(f"    [WARN] 复制失败 {src_file.name}: {e}")
                continue

        # 转 .pptx (只对 .ppt)
        ppt_files = [f for f in temp_subdir.glob("*.ppt")]
        if ppt_files:
            # 使用通配符方式（LibreOffice 支持自动展开）
            cmd = [soffice_path, "--headless", "--convert-to", "pptx", "--outdir", str(temp_subdir), str(temp_subdir / "*.ppt")]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode != 0:
                    failed.append((parent_dir, "LibreOffice failed"))
                    shutil.rmtree(temp_subdir, ignore_errors=True)
                    continue
            except subprocess.TimeoutExpired:
                failed.append((parent_dir, "Timeout"))
                shutil.rmtree(temp_subdir, ignore_errors=True)
                continue

        # 对所有 .pptx 使用 convert_modern 处理
        pptx_files = list(temp_subdir.glob("*.pptx"))
        if pptx_files:
            # 创建包含 pptx 文件的目录结构
            pptx_by_dir = {parent_dir: pptx_files}
            # 调用 convert_modern 处理 pptx
            success += convert_modern(pptx_by_dir, '.pptx', 'PPTX', output_dir, all_failed)

        shutil.rmtree(temp_subdir, ignore_errors=True)

    return success, failed

def convert_modern(by_dir, file_type, label, output_dir, all_failed):
    """使用 markitdown 转换现代格式（.xlsx, .pptx, .docx）"""
    success = 0
    
    markitdown_cmd = get_markitdown_command()
    if not markitdown_cmd:
        print(f"  ⚠️ 未找到 markitdown 命令，请安装: pip install markitdown[docx,xlsx,pdf]")
        return success

    for parent_dir, files in by_dir.items():
        if not files:
            continue
        output_subdir = output_dir / parent_dir
        output_subdir.mkdir(parents=True, exist_ok=True)

        try:
            for src_file in files:
                if src_file.suffix.lower() == file_type:
                    output_file = output_subdir / src_file.with_suffix('.md').name
                    # 构建命令
                    if isinstance(markitdown_cmd, str):
                        cmd = [markitdown_cmd, str(src_file), "-o", str(output_file)]
                    else:
                        cmd = markitdown_cmd + [str(src_file), "-o", str(output_file)]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    if result.returncode == 0:
                        success += 1
                    else:
                        error_msg = f"Exit {result.returncode}: {result.stderr.strip() or result.stdout.strip()}"
                        all_failed.append((str(src_file), file_type, error_msg))
                        print(f"    [DEBUG] {src_file.name} 失败: {error_msg}")

        except Exception as e:
            all_failed.append((parent_dir, file_type, str(e)))

        print(f"  {label} {parent_dir}: {success} 累计成功")

    return success

def convert_pdfs(by_dir, output_dir):
    """批量转换 .pdf 文件 - 使用 markitdown"""
    print(f"\n[步骤 6] PDF 文档转换 (.pdf → .md)")
    success = 0
    failed = []
    
    markitdown_cmd = get_markitdown_command()
    if not markitdown_cmd:
        print(f"  ⚠️ 未找到 markitdown 命令，请安装: pip install markitdown[docx,xlsx,pdf]")
        return success, failed

    for parent_dir, files in by_dir.items():
        if not files:
            continue
        output_subdir = output_dir / parent_dir
        output_subdir.mkdir(parents=True, exist_ok=True)

        for src_file in files:
            try:
                output_file = output_subdir / src_file.with_suffix('.md').name
                # 构建命令
                if isinstance(markitdown_cmd, str):
                    cmd = [markitdown_cmd, str(src_file), "-o", str(output_file)]
                else:
                    cmd = markitdown_cmd + [str(src_file), "-o", str(output_file)]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    success += 1
                else:
                    failed.append((str(src_file), f"Exit {result.returncode}: {result.stderr.strip() or result.stdout.strip()}"))
            except Exception as e:
                failed.append((str(src_file), str(e)))

        print(f"  {parent_dir}: {success} 累计成功")

    return success, failed

def main():
    parser = argparse.ArgumentParser(description="批量文档转换工具")
    parser.add_argument("--source", required=True, help="源目录路径")
    parser.add_argument("--output", default="./output", help="输出目录路径")
    parser.add_argument("--type", default="doc,xls,docx,xlsx,ppt,pptx,pdf", help="处理的文件类型（逗号分隔）")
    parser.add_argument("--soffice-path", help="LibreOffice soffice.exe 路径（自动检测）")
    parser.add_argument("--dry-run", action="store_true", help="仅模拟，不实际转换")
    parser.add_argument("--log-file", default="conversion.log", help="日志文件路径")
    args = parser.parse_args()

    # 初始化
    source_dir = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()
    temp_root = Path("./temp_batch").resolve()

    if temp_root.exists():
        shutil.rmtree(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)

    # 查找 LibreOffice（仅在非 dry-run 模式下）
    soffice_path = None
    if not args.dry_run:
        soffice_path = args.soffice_path or find_libreoffice()
        if not soffice_path or not Path(soffice_path).exists():
            print("❌ 未找到 LibreOffice，请安装或指定路径")
            sys.exit(1)

    print("="*60)
    print("文档批量转换工具")
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print(f"LibreOffice: {soffice_path}")
    print("="*60)

    # 扫描文件
    file_types = [f".{t.strip()}" for t in args.type.split(',')]
    by_dir = scan_files(source_dir, file_types)

    total_files = sum(len(files) for files in by_dir.values())
    print(f"\n扫描结果: {total_files} 个文件，{len(by_dir)} 个子目录")

    if args.dry_run:
        print("\n[Dry Run] 不执行转换，仅显示统计")
        for parent, files in by_dir.items():
            counts = {}
            for f in files:
                ext = f.suffix.lower()
                counts[ext] = counts.get(ext, 0) + 1
            print(f"  {parent}: {counts}")
        return

    # 分离不同类型
    doc_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.doc'] for p, fs in by_dir.items()}
    xls_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.xls'] for p, fs in by_dir.items()}
    docx_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.docx'] for p, fs in by_dir.items()}
    xlsx_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.xlsx'] for p, fs in by_dir.items()}
    ppt_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.ppt'] for p, fs in by_dir.items()}
    pptx_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.pptx'] for p, fs in by_dir.items()}
    pdf_files_by_dir = {p: [f for f in fs if f.suffix.lower() == '.pdf'] for p, fs in by_dir.items()}

    total_success = 0
    all_failed = []

    # 1. 转换 .doc
    if any(doc_files_by_dir.values()):
        success, failed = convert_docs(doc_files_by_dir, source_dir, output_dir, soffice_path, temp_root)
        total_success += success
        all_failed.extend([(f, "doc", err) for f, err in failed])

    # 2. 转换 .docx
    if any(docx_files_by_dir.values()):
        success, failed = convert_docx(docx_files_by_dir, source_dir, output_dir, soffice_path, temp_root)
        total_success += success
        all_failed.extend([(f, "docx", err) for f, err in failed])

    # 3. 转换 .xls
    if any(xls_files_by_dir.values()):
        success, failed = convert_excels(xls_files_by_dir, source_dir, output_dir, soffice_path, temp_root, all_failed)
        total_success += success
        all_failed.extend([(f, "xls", err) for f, err in failed])

    # 4. 转换 .ppt
    if any(ppt_files_by_dir.values()):
        success, failed = convert_presentations(ppt_files_by_dir, source_dir, output_dir, soffice_path, temp_root, all_failed)
        total_success += success
        all_failed.extend([(f, "ppt", err) for f, err in failed])

    # 5. 现代格式（直接 MarkItDown）
    if any(xlsx_files_by_dir.values()):
        success = convert_modern(xlsx_files_by_dir, '.xlsx', "XLSX", output_dir, all_failed)
        total_success += success

    if any(pptx_files_by_dir.values()):
        success = convert_modern(pptx_files_by_dir, '.pptx', "PPTX", output_dir, all_failed)
        total_success += success

    # 5. PDF 转换
    if any(pdf_files_by_dir.values()):
        success, failed = convert_pdfs(pdf_files_by_dir, output_dir)
        total_success += success
        all_failed.extend([(f, "pdf", err) for f, err in failed])

    # 清理
    shutil.rmtree(temp_root, ignore_errors=True)

    # 报告
    print(f"\n" + "="*60)
    print("转换完成")
    print(f"总成功: {total_success}/{total_files}")
    print(f"输出目录: {output_dir}")
    print("="*60)

    # 错误日志
    if all_failed:
        log_path = Path(args.log_file)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n# 转换失败记录 ({datetime.now()})\n")
            for file_path, typ, err in all_failed:
                f.write(f"- [{typ}] {file_path}: {err}\n")
        print(f"失败记录: {log_path}")

if __name__ == '__main__':
    main()
