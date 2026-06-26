#!/usr/bin/env python3
"""
Batch EDID Validator
Process multiple EDID files and generate summary report
Usage: python3 batch_validate.py <directory>
"""

import sys
import os
import subprocess
import re
from pathlib import Path
from collections import defaultdict

def extract_binary(filepath):
    """Extract binary EDID from decoded file"""
    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()
        
        hex_start = content.find("(hex):")
        if hex_start == -1:
            return None
        hex_start += len("(hex):")
        
        dash_pos = content.find("----------------", hex_start)
        if dash_pos == -1:
            return None
        
        hex_section = content[hex_start:dash_pos]
        hex_pairs = re.findall(r'\b([0-9a-fA-F]{2})\b', hex_section)
        return bytes.fromhex(''.join(hex_pairs))
    except Exception as e:
        return None

def validate_edid(binary):
    """Validate a single EDID binary"""
    result = {
        'valid': False,
        'size': len(binary) if binary else 0,
        'warnings': [],
        'errors': [],
        'manufacturer': None,
        'model': None,
        'max_resolution': None
    }
    
    if not binary:
        result['errors'].append("无法提取二进制数据")
        return result
    
    if len(binary) < 128:
        result['errors'].append(f"文件太小 ({len(binary)} bytes)")
        return result
    
    try:
        proc = subprocess.run(
            ['edid-decode', '-c'],
            input=binary,
            capture_output=True,
            timeout=30
        )
        output = proc.stdout.decode('utf-8', errors='ignore') + proc.stderr.decode('utf-8', errors='ignore')
        
        if proc.returncode != 0:
            result['errors'].append("edid-decode 失败")
        
        if "Fail" in output or "ERROR" in output:
            result['errors'].append("存在失败项")
        
        if "Warning" in output:
            result['warnings'].append("存在警告")
        
        # Extract key info
        m = re.search(r'Manufacturer:\s*(\S+)', output)
        if m:
            result['manufacturer'] = m.group(1)
        
        m = re.search(r'Model:\s*(\S+)', output)
        if m:
            result['model'] = m.group(1)
        
        # Get max resolution from DTD
        m = re.search(r'DTD 1:\s+(\d+)x(\d+)\s+(\d+\.?\d*)\s*Hz', output)
        if m:
            result['max_resolution'] = f"{m.group(1)}x{m.group(2)}@{m.group(3)}"
        
        result['valid'] = len(result['errors']) == 0
        
    except subprocess.TimeoutExpired:
        result['errors'].append("解析超时")
    except Exception as e:
        result['errors'].append(f"异常: {str(e)[:50]}")
    
    return result

def find_edid_files(directory):
    """Find all EDID files in directory"""
    edid_files = []
    
    for root, dirs, files in os.walk(directory):
        for f in files:
            # Skip .bin files, only process source files
            if f.endswith('.bin') or f.endswith('.txt') or f.endswith('_bin.txt'):
                continue
            filepath = os.path.join(root, f)
            # Check if it's a potential EDID file
            try:
                with open(filepath, 'r', errors='ignore') as fp:
                    content = fp.read(100)
                    if '(hex):' in content:
                        edid_files.append(filepath)
            except:
                pass
    
    return edid_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 batch_validate.py <directory>")
        print("Example: python3 batch_validate.py ~/Downloads/edid/test-samples/Digital/")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        sys.exit(1)
    
    print("=" * 60)
    print("        EDID 批量验证 / Batch Validation")
    print("=" * 60)
    print(f"\n扫描目录: {directory}")
    
    # Find all EDID files
    print("\n正在扫描文件...")
    edid_files = find_edid_files(directory)
    print(f"找到 {len(edid_files)} 个 EDID 文件")
    
    if not edid_files:
        print("未找到 EDID 文件")
        sys.exit(1)
    
    # Process files
    print("\n正在验证...")
    results = {
        'valid': [],
        'invalid': [],
        'warnings': []
    }
    
    stats = defaultdict(int)
    
    for i, filepath in enumerate(edid_files):
        if (i + 1) % 100 == 0:
            print(f"  已处理 {i+1}/{len(edid_files)}...")
        
        binary = extract_binary(filepath)
        result = validate_edid(binary)
        
        rel_path = os.path.relpath(filepath, directory)
        
        if result['valid']:
            if result['warnings']:
                results['warnings'].append((rel_path, result))
                stats['warnings'] += 1
            else:
                results['valid'].append((rel_path, result))
                stats['valid'] += 1
        else:
            results['invalid'].append((rel_path, result))
            stats['invalid'] += 1
        
        stats['total'] += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("                    验证结果汇总")
    print("=" * 60)
    print(f"\n总文件数: {stats['total']}")
    print(f"✅ 有效: {stats['valid']}")
    print(f"⚠️  有警告: {stats['warnings']}")
    print(f"❌ 无效: {stats['invalid']}")
    
    # Show invalid files
    if results['invalid']:
        print("\n" + "-" * 40)
        print("❌ 无效文件:")
        for path, result in results['invalid'][:10]:
            print(f"   {path}")
            for err in result['errors']:
                print(f"      - {err}")
        if len(results['invalid']) > 10:
            print(f"   ... 还有 {len(results['invalid']) - 10} 个")
    
    # Show files with warnings
    if results['warnings']:
        print("\n" + "-" * 40)
        print("⚠️  有警告的文件:")
        for path, result in results['warnings'][:10]:
            mfg = result.get('manufacturer', '?')
            model = result.get('model', '?')
            res = result.get('max_resolution', '?')
            print(f"   {path}")
            print(f"      {mfg} {model} | {res}")
            for warn in result['warnings']:
                print(f"      - {warn}")
        if len(results['warnings']) > 10:
            print(f"   ... 还有 {len(results['warnings']) - 10} 个")
    
    # Show manufacturer distribution
    print("\n" + "-" * 40)
    print("📊 制造商分布:")
    mfg_count = defaultdict(int)
    for path, result in results['valid'] + results['warnings']:
        mfg = result.get('manufacturer', 'Unknown')
        mfg_count[mfg] += 1
    
    for mfg, count in sorted(mfg_count.items(), key=lambda x: -x[1])[:10]:
        print(f"   {mfg}: {count}")
    
    print("\n" + "=" * 60)
    print("验证完成 / Validation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()