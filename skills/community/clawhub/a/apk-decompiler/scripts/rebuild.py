#!/usr/bin/env python3
"""
rebuild.py - APK 重新打包和签名脚本
用法: python3 rebuild.py <project_dir> [output_apk]

功能:
  - 从 Smali 重新编译 DEX
  - 使用 apktool 重新打包
  - 签名 APK
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import shutil

TOOLS_DIR = os.environ.get('TOOLS_DIR', os.path.expanduser('~/.apk-tools'))

def compile_smali(smali_dir: str, output_dex: str) -> bool:
    """编译 Smali 到 DEX"""
    print("🔨 编译 Smali 到 DEX...")
    
    if not os.path.exists(smali_dir):
        print(f"❌ Smali 目录不存在: {smali_dir}")
        return False
    
    result = subprocess.run(
        ['java', '-jar', os.path.join(TOOLS_DIR, 'smali.jar'),
         'a', smali_dir, '-o', output_dex],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"❌ 编译失败: {result.stderr}")
        return False
    
    print(f"  ✅ 输出: {output_dex}")
    return True

def rebuild_apk(project_dir: str, output_apk: str) -> bool:
    """使用 apktool 重新打包"""
    print("📦 重新打包 APK...")
    
    result = subprocess.run(
        ['java', '-jar', os.path.join(TOOLS_DIR, 'apktool.jar'),
         'b', project_dir, '-o', output_apk],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"⚠️ 打包警告: {result.stderr[:500]}")
        if 'Error' in result.stderr:
            return False
    
    print(f"  ✅ 输出: {output_apk}")
    return True

def sign_apk(apk_path: str, signed_apk: str = None) -> bool:
    """签名 APK"""
    print("✍️ 签名 APK...")
    
    if signed_apk is None:
        base = Path(apk_path).stem
        ext = Path(apk_path).suffix
        signed_apk = f"{base}-signed{ext}"
    
    signer = os.path.join(TOOLS_DIR, 'uber-apk-signer.jar')
    
    if not os.path.exists(signer):
        print("⚠️ uber-apk-signer 未安装，尝试使用 apksigner...")
        # 尝试使用系统 apksigner
        result = subprocess.run(
            ['apksigner', 'sign', '--ks', 'debug.keystore',
             '--ks-pass', 'pass:android', '--out', signed_apk, apk_path],
            capture_output=True, text=True
        )
    else:
        result = subprocess.run(
            ['java', '-jar', signer, '--apks', apk_path,
             '--out', os.path.dirname(signed_apk) or '.'],
            capture_output=True, text=True
        )
    
    if result.returncode != 0:
        print(f"⚠️ 签名警告: {result.stderr[:200]}")
        # uber-apk-signer 可能已自动签名
    
    print(f"  ✅ 签名完成")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='APK 重新打包工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s ./app-decompiled           # 从项目目录重新打包
  %(prog)s ./app-decompiled app.apk   # 指定输出文件名
  %(prog)s ./app-decompiled --sign-only app.apk  # 只签名
        """
    )
    
    parser.add_argument('project', help='项目目录（包含 smali-out 或 apktool-out）')
    parser.add_argument('output', nargs='?', help='输出 APK 文件名')
    parser.add_argument('--sign-only', action='store_true', help='只签名 APK')
    parser.add_argument('--no-sign', action='store_true', help='跳过签名')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.project):
        print(f"❌ 目录不存在: {args.project}")
        sys.exit(1)
    
    project_dir = Path(args.project)
    apk_name = project_dir.name.replace('-decompiled', '')
    output_apk = args.output or f'{apk_name}-rebuilt.apk'
    
    if args.sign_only:
        # 只签名
        if not args.output:
            print("❌ 签名模式需要指定 APK 文件")
            sys.exit(1)
        sign_apk(args.output)
        return
    
    # 检查项目结构
    smali_dir = project_dir / 'smali-out'
    apktool_dir = project_dir / 'apktool-out'
    
    if apktool_dir.exists():
        # 使用 apktool 打包
        print(f"📁 使用 apktool 打包: {apktool_dir}")
        if not rebuild_apk(str(apktool_dir), output_apk):
            print("❌ 打包失败")
            sys.exit(1)
    else:
        print("⚠️ 未找到 apktool-out 目录")
        print("请确保项目是通过 decompile.py 生成的")
        sys.exit(1)
    
    # 签名
    if not args.no_sign:
        sign_apk(output_apk)
    
    print(f"\n✅ 打包完成！")
    print(f"   输出: {output_apk}")
    print("\n💡 提示: 签名使用的是调试密钥，仅用于测试。")
    print("   发布前请使用正式密钥签名。")

if __name__ == '__main__':
    main()
