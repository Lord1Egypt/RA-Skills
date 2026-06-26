#!/usr/bin/env python3
"""
cn-qrcode-reader - 二维码/条形码识别工具
"""
import argparse
import glob
import os
import sys

def try_import_pyzbar():
    """尝试导入pyzbar"""
    try:
        from pyzbar.pyzbar import decode as decode_barcode
        from PIL import Image
        return decode_barcode, Image
    except ImportError:
        return None, None

def read_qrcode(image_path, verbose=False):
    """读取二维码/条形码"""
    decode_barcode, Image = try_import_pyzbar()
    
    if decode_barcode is None:
        print("错误：缺少依赖库")
        print("请安装：pip install Pillow pyzbar")
        print("macOS: brew install zbar")
        print("Ubuntu: sudo apt-get install libzbar0")
        return []
    
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        barcodes = decode_barcode(img)
        results = []
        
        for barcode in barcodes:
            data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            results.append({
                'type': barcode_type,
                'data': data,
                'rect': barcode.rect
            })
            
            if verbose:
                print(f"[{barcode_type}] {data}")
            else:
                print(data)
        
        return results
        
    except Exception as e:
        print(f"读取失败 {image_path}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='二维码/条形码识别工具')
    parser.add_argument('image', nargs='+', help='图片路径（支持glob）')
    parser.add_argument('--verbose', action='store_true', help='显示详细信息')
    parser.add_argument('--save', help='保存结果到文件')
    
    args = parser.parse_args()
    
    # 收集所有图片路径
    image_paths = []
    for pattern in args.image:
        if '*' in pattern or '?' in pattern:
            image_paths.extend(glob.glob(pattern))
        else:
            if os.path.exists(pattern):
                image_paths.append(pattern)
            else:
                print(f"文件不存在: {pattern}")
    
    if not image_paths:
        print("没有找到图片文件")
        return
    
    # 处理每张图片
    all_results = []
    for path in image_paths:
        print(f"\n{'-'*40}")
        print(f"文件: {path}")
        print('-'*40)
        results = read_qrcode(path, args.verbose)
        all_results.extend(results)
    
    # 保存结果
    if args.save and all_results:
        with open(args.save, 'w', encoding='utf-8') as f:
            for r in all_results:
                f.write(f"{r['type']}: {r['data']}\n")
        print(f"\n结果已保存到: {args.save}")

if __name__ == '__main__':
    main()