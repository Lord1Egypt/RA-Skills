#!/usr/bin/env python3
"""
analyze.py - APK 分析脚本
用法: python3 analyze.py <apk_file> [--manifest] [--permissions] [--activities] [--strings]

功能:
  - 提取 AndroidManifest 信息
  - 分析权限
  - 列出 Activities/Services/Receivers
  - 提取字符串常量
"""

import argparse
import os
import subprocess
import sys
import zipfile
from pathlib import Path
import struct

def extract_manifest_info(apk_path: str) -> dict:
    """从 APK 中提取 AndroidManifest 信息"""
    info = {
        'package': None,
        'version_name': None,
        'version_code': None,
        'min_sdk': None,
        'target_sdk': None,
        'permissions': [],
        'activities': [],
        'services': [],
        'receivers': [],
        'providers': [],
    }
    
    # 解析 DEX 文件提取字符串
    with zipfile.ZipFile(apk_path, 'r') as z:
        # 检查是否有 classes.dex
        dex_files = [f for f in z.namelist() if f.endswith('.dex')]
        
        for dex_name in dex_files:
            with z.open(dex_name) as f:
                data = f.read()
                strings = extract_strings_from_dex(data)
                
                # 提取权限
                for s in strings:
                    if s.startswith('android.permission.'):
                        if s not in info['permissions']:
                            info['permissions'].append(s)
                    
                    # 提取 Activities
                    if 'Activity' in s and '.' in s and s.count('.') >= 2:
                        if s not in info['activities'] and not s.startswith('android.'):
                            info['activities'].append(s)
    
    return info

def extract_strings_from_dex(data: bytes) -> list:
    """从 DEX 文件提取字符串"""
    strings = []
    
    try:
        # DEX 文件头
        if data[:4] != b'dex\n':
            return strings
        
        # 读取字符串数量和偏移
        string_ids_size = struct.unpack('<I', data[56:60])[0]
        string_ids_off = struct.unpack('<I', data[60:64])[0]
        
        # 读取字符串
        for i in range(min(string_ids_size, 10000)):  # 限制数量
            try:
                string_data_off = struct.unpack('<I', 
                    data[string_ids_off + i*4:string_ids_off + i*4 + 4])[0]
                
                # 读取 ULEB128 长度
                idx = string_data_off
                length = 0
                shift = 0
                while True:
                    b = data[idx]
                    idx += 1
                    length |= (b & 0x7f) << shift
                    if not (b & 0x80):
                        break
                    shift += 7
                
                # 读取字符串 (MUTF-8)
                s = ''
                for j in range(min(length, 1000)):  # 限制长度
                    c = data[idx + j]
                    if c < 0x80:
                        s += chr(c)
                    else:
                        break
                
                if s and len(s) > 2:
                    strings.append(s)
            except:
                continue
    except Exception as e:
        pass
    
    return strings

def list_dex_classes(smali_dir: str) -> list:
    """从 Smali 目录列出类"""
    classes = []
    
    for root, dirs, files in os.walk(smali_dir):
        for f in files:
            if f.endswith('.smali'):
                # 从路径提取类名
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, smali_dir)
                class_name = rel_path.replace('.smali', '').replace(os.sep, '.')
                
                # 过滤掉系统类
                if not class_name.startswith('android.') and \
                   not class_name.startswith('kotlin.') and \
                   not class_name.startswith('java.'):
                    classes.append(class_name)
    
    return sorted(classes)

def analyze_apk(apk_path: str, smali_dir: str = None) -> dict:
    """全面分析 APK"""
    result = {
        'file': apk_path,
        'size_mb': os.path.getsize(apk_path) / 1024 / 1024,
        'manifest': {},
        'classes': [],
        'assets': [],
        'native_libs': [],
    }
    
    # 从 APK 提取信息
    with zipfile.ZipFile(apk_path, 'r') as z:
        files = z.namelist()
        
        # 资源文件
        result['assets'] = [f for f in files if f.startswith('assets/')]
        
        # Native 库
        result['native_libs'] = [f for f in files if f.startswith('lib/') and f.endswith('.so')]
        
        # DEX 文件数量
        result['dex_count'] = sum(1 for f in files if f.endswith('.dex'))
    
    # 提取 Manifest 信息
    result['manifest'] = extract_manifest_info(apk_path)
    
    # 从 Smali 提取类列表
    if smali_dir and os.path.exists(smali_dir):
        result['classes'] = list_dex_classes(smali_dir)
    
    return result

def main():
    parser = argparse.ArgumentParser(
        description='APK 分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s app.apk                    # 基本分析
  %(prog)s app.apk --smali ./smali-out  # 包含 Smali 类分析
  %(prog)s app.apk --permissions      # 只显示权限
        """
    )
    
    parser.add_argument('apk', help='APK 文件路径')
    parser.add_argument('--smali', help='Smali 源码目录')
    parser.add_argument('--permissions', action='store_true', help='只显示权限')
    parser.add_argument('--activities', action='store_true', help='只显示 Activities')
    parser.add_argument('--classes', action='store_true', help='显示应用类列表')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.apk):
        print(f"❌ 文件不存在: {args.apk}")
        sys.exit(1)
    
    print(f"🔍 分析 APK: {args.apk}\n")
    
    result = analyze_apk(args.apk, args.smali)
    
    if args.permissions:
        print("📋 权限列表:")
        for p in result['manifest']['permissions']:
            print(f"   • {p}")
        return
    
    if args.activities:
        print("📱 Activities:")
        for a in result['manifest']['activities'][:30]:
            print(f"   • {a}")
        if len(result['manifest']['activities']) > 30:
            print(f"   ... 还有 {len(result['manifest']['activities']) - 30} 个")
        return
    
    if args.classes:
        if not args.smali:
            print("❌ 需要指定 --smali 参数")
            sys.exit(1)
        print("📦 应用类:")
        for c in result['classes'][:50]:
            print(f"   • {c}")
        if len(result['classes']) > 50:
            print(f"   ... 还有 {len(result['classes']) - 50} 个")
        return
    
    # 完整分析
    print("📊 基本信息:")
    print(f"   文件大小: {result['size_mb']:.2f} MB")
    print(f"   DEX 文件: {result['dex_count']} 个")
    print(f"   资源文件: {len(result['assets'])} 个")
    print(f"   Native 库: {len(result['native_libs'])} 个")
    
    if result['manifest']['permissions']:
        print("\n📋 权限:")
        for p in result['manifest']['permissions']:
            print(f"   • {p}")
    
    if result['manifest']['activities']:
        print("\n📱 Activities:")
        for a in result['manifest']['activities'][:20]:
            print(f"   • {a}")
    
    if result['classes']:
        print(f"\n📦 应用类: {len(result['classes'])} 个")

if __name__ == '__main__':
    main()
