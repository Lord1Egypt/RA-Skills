#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

# ── 路径配置 (符合 Skill 手册 Kebab-case 规范 [cite: 178-181]) ──────────────────

# 获取当前脚本所在目录 (scripts/) 的父目录，即 Skill 根目录 [cite: 151-155]
BASE_DIR = Path(__file__).resolve().parent.parent
# 优先指向 Skill 内部 tools 目录下的绿色版 ODA [cite: 53-54]
INTERNAL_ODA = BASE_DIR / "tools" / "oda" / "ODAFileConverter.exe"

# Windows 系统下的常见备选路径 [cite: 608-614]
EXTERNAL_ODA_PATHS = [
    r"C:\Program Files\ODA\ODAFileConverter\ODAFileConverter.exe",
    r"C:\Program Files (x86)\ODA\ODAFileConverter\ODAFileConverter.exe",
]

def find_oda_engine():
    """查找可用的 ODA 转换引擎，实现环境自愈 """
    # 1. 优先使用 Skill 内部自带的绿色版
    if INTERNAL_ODA.exists():
        return str(INTERNAL_ODA)
    
    # 2. 搜索 Windows 常用安装目录
    for path in EXTERNAL_ODA_PATHS:
        if os.path.exists(path):
            return path
            
    # 3. 尝试从系统环境变量查找
    found = shutil.which("ODAFileConverter.exe") or shutil.which("ODAFileConverter")
    return found

def convert(input_path_str, output_dir_str):
    """
    执行 DWG 到 DXF 的静默转换。
    使用临时目录策略规避中文字符路径和权限问题 [cite: 215-219, 295-301]。
    """
    oda_exe = find_oda_engine()
    if not oda_exe:
        print("【错误】未检测到 ODA 转换引擎。")
        print("请确保 ODAFileConverter.exe 位于 tools/oda/ 目录下或已安装在系统默认路径。")
        print("下载地址: https://www.opendesign.com/guestfiles/oda_file_converter")
        sys.exit(1)

    input_path = Path(input_path_str).absolute()
    output_dir = Path(output_dir_str).absolute()
    output_dir.mkdir(parents=True, exist_ok=True)

    # 判定是单文件还是目录批量转换 [cite: 111-119]
    if input_path.is_dir():
        input_folder = input_path
        filter_str = "*.dwg"
        print(f"模式: 批量转换文件夹 -> {input_folder}")
    else:
        input_folder = input_path.parent
        filter_str = input_path.name
        print(f"模式: 单文件转换 -> {filter_str}")

    # 使用系统临时目录作为中转，彻底解决 Windows 中文路径乱码问题 
    with tempfile.TemporaryDirectory(prefix="oda_conv_") as tmp_work_dir:
        tmp_path = Path(tmp_work_dir)
        
        # 如果是单文件，先拷贝到纯净的临时目录
        if not input_path.is_dir():
            shutil.copy2(input_path, tmp_path / filter_str)
            actual_in = tmp_path
        else:
            actual_in = input_folder

        # ODA 命令行参数 (ACAD2013 是解析库 ezdxf 兼容性最好的版本)
        cmd = [
            oda_exe,
            str(actual_in),
            str(tmp_path), # 先输出到临时目录
            "ACAD2013",
            "DXF",
            "0", # 不递归
            "1", # 审计修复
            filter_str
        ]

        print(f"正在转换，请稍候... (引擎: {Path(oda_exe).name})")
        
        try:
            # 开启创建标志以在 Windows 后台静默运行，不弹出窗口 
            creation_flags = 0x08000000 if os.name == 'nt' else 0 # CREATE_NO_WINDOW
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                creationflags=creation_flags,
                timeout=180 # 防止大型图纸卡死 
            )
            
            # 将转换好的 DXF 移动到最终目标目录
            success_count = 0
            for dxf_file in tmp_path.glob("*.dxf"):
                shutil.move(str(dxf_file), str(output_dir / dxf_file.name))
                success_count += 1
            
            if success_count > 0:
                print(f"【成功】已生成 {success_count} 个 DXF 文件至: {output_dir}")
            else:
                print("【警告】转换任务结束，但未发现生成的 DXF 文件。")
                
        except subprocess.TimeoutExpired:
            print("【错误】转换超时，图纸文件可能过大或已损坏。")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"【错误】ODA 引擎执行失败 (Exit Code: {e.returncode})")
            print(f"错误日志: {e.stderr}")
            sys.exit(1)

if __name__ == "__main__":
    # 严格校验命令行参数 [cite: 615-616]
    if len(sys.argv) < 3:
        print("用法: python dwg_to_dxf.py <输入路径(文件或目录)> <输出目录>")
        sys.exit(1)
        
    convert(sys.argv[1], sys.argv[2])