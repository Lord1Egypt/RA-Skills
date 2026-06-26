#!/usr/bin/env python3
"""
decompile.py - APK 反编译脚本
用法: python3 decompile.py <apk_file> [output_dir] [--java]

功能:
  - 反编译 DEX 到 Smali
  - 解码资源文件
  - 可选: 转换 DEX 到 JAR (Java 源码)
"""

import argparse
import os
import subprocess
import sys
import shutil
from pathlib import Path

TOOLS_DIR = os.environ.get('TOOLS_DIR', os.path.expanduser('~/.apk-tools'))

def check_tools():
    """检查必要工具是否存在"""
    required = ['baksmali.jar', 'apktool.jar']
    missing = []
    
    for tool in required:
        if not os.path.exists(os.path.join(TOOLS_DIR, tool)):
            missing.append(tool)
    
    if missing:
        print(f"❌ 缺少工具: {', '.join(missing)}")
        print("请先运行: ./setup_tools.sh")
        return False
    return True

def decompile_dex(apk_path: str, output_dir: str) -> bool:
    """反编译 DEX 到 Smali"""
    print("📦 反编译 DEX 到 Smali...")
    
    # 解压 APK 获取 classes.dex
    apk_name = Path(apk_path).stem
    extracted_dir = os.path.join(output_dir, 'extracted')
    os.makedirs(extracted_dir, exist_ok=True)
    
    # 使用 unzip 解压
    result = subprocess.run(
        ['unzip', '-o', apk_path, '-d', extracted_dir],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"⚠️ 解压 APK 失败: {result.stderr}")
        return False
    
    # 找到所有 DEX 文件
    dex_files = list(Path(extracted_dir).glob('*.dex'))
    
    if not dex_files:
        print("❌ 未找到 DEX 文件")
        return False
    
    smali_dir = os.path.join(output_dir, 'smali-out')
    
    for i, dex_file in enumerate(dex_files):
        suffix = '' if len(dex_files) == 1 else f'_{i}'
        out_dir = f"{smali_dir}{suffix}" if suffix else smali_dir
        
        print(f"  处理: {dex_file.name}")
        
        result = subprocess.run(
            ['java', '-jar', os.path.join(TOOLS_DIR, 'baksmali.jar'),
             'd', str(dex_file), '-o', out_dir],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print(f"  ⚠️ 反编译失败: {result.stderr}")
        else:
            print(f"  ✅ 输出: {out_dir}")
    
    return True

def decode_resources(apk_path: str, output_dir: str) -> bool:
    """使用 apktool 解码资源"""
    print("📄 解码资源文件...")
    
    result = subprocess.run(
        ['java', '-jar', os.path.join(TOOLS_DIR, 'apktool.jar'),
         'd', apk_path, '-o', os.path.join(output_dir, 'apktool-out'),
         '-f', '-s'],  # -f 强制覆盖, -s 不反编译源码
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"⚠️ apktool 警告: {result.stderr[:200]}")
        # apktool 有时会有警告但仍成功
    
    print(f"  ✅ 输出: {output_dir}/apktool-out")
    return True

def dex_to_jar(apk_path: str, output_dir: str) -> bool:
    """转换 DEX 到 JAR"""
    print("☕ 转换 DEX 到 JAR...")
    
    dex2jar_dir = os.path.join(TOOLS_DIR, 'dex2jar')
    if not os.path.exists(dex2jar_dir):
        print("❌ dex2jar 未安装，请运行 setup_tools.sh")
        return False
    
    # 找到 dex2jar 脚本
    d2j_cmd = os.path.join(dex2jar_dir, 'd2j-dex2jar.sh')
    if not os.path.exists(d2j_cmd):
        # Windows
        d2j_cmd = os.path.join(dex2jar_dir, 'd2j-dex2jar.bat')
    
    jar_output = os.path.join(output_dir, f'{Path(apk_path).stem}-dex2jar.jar')
    
    result = subprocess.run(
        [d2j_cmd, apk_path, '-o', jar_output, '--force'],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"⚠️ dex2jar 警告: {result.stderr[:200]}")
    else:
        print(f"  ✅ 输出: {jar_output}")
        print("  💡 使用 jadx 或 jd-gui 查看 Java 源码")
    
    return True

def analyze_apk(apk_path: str) -> dict:
    """分析 APK 基本信息"""
    info = {
        'file': apk_path,
        'size': os.path.getsize(apk_path) / 1024 / 1024,
    }
    
    # 解压获取基本信息
    result = subprocess.run(
        ['unzip', '-l', apk_path],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        info['file_count'] = len(lines) - 3  # 减去头部和尾部
        
        # 找 DEX 文件
        dex_count = sum(1 for l in lines if '.dex' in l)
        info['dex_count'] = dex_count
    
    return info

def main():
    parser = argparse.ArgumentParser(
        description='APK 反编译工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s app.apk                    # 反编译到 ./app-decompiled/
  %(prog)s app.apk ./output           # 反编译到 ./output/
  %(prog)s app.apk --java             # 同时转换 DEX 到 JAR
        """
    )
    
    parser.add_argument('apk', help='APK 文件路径')
    parser.add_argument('output', nargs='?', help='输出目录（默认: APK名-decompiled）')
    parser.add_argument('--java', action='store_true', help='同时转换 DEX 到 JAR')
    parser.add_argument('--resources-only', action='store_true', help='只解码资源')
    parser.add_argument('--smali-only', action='store_true', help='只反编译 Smali')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.apk):
        print(f"❌ 文件不存在: {args.apk}")
        sys.exit(1)
    
    # 检查工具
    if not check_tools():
        sys.exit(1)
    
    # 确定输出目录
    apk_name = Path(args.apk).stem
    output_dir = args.output or f'{apk_name}-decompiled'
    
    print(f"\n🔍 分析 APK: {args.apk}")
    info = analyze_apk(args.apk)
    print(f"   大小: {info['size']:.2f} MB")
    print(f"   DEX 文件: {info.get('dex_count', '?')}")
    print(f"   输出目录: {output_dir}")
    print()
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 反编译
    if not args.resources_only:
        decompile_dex(args.apk, output_dir)
    
    if not args.smali_only:
        decode_resources(args.apk, output_dir)
    
    if args.java:
        dex_to_jar(args.apk, output_dir)
    
    print(f"\n✅ 反编译完成！输出目录: {output_dir}")
    print("\n📁 输出结构:")
    print(f"   {output_dir}/")
    print("   ├── smali-out/      # Smali 源码")
    print("   ├── apktool-out/    # 解码的资源文件")
    if args.java:
        print("   ├── *-dex2jar.jar   # JAR 文件（可用 jadx 查看）")
    print("   └── extracted/      # 原始 APK 内容")

if __name__ == '__main__':
    main()
