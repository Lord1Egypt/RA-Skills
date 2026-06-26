#!/usr/bin/env python3
"""
照片分析器
提取 EXIF 信息、时间线、地点等
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def analyze_photo(photo_path):
    """分析单张照片的 EXIF 信息"""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
    except ImportError:
        print("Error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        return None
    
    try:
        img = Image.open(photo_path)
        exif = img._getexif()
        
        if not exif:
            return {
                'filename': photo_path.name,
                'size': img.size,
                'format': img.format,
                'exif': None
            }
        
        # 解析 EXIF
        exif_data = {}
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_data[tag] = value
        
        result = {
            'filename': photo_path.name,
            'size': img.size,
            'format': img.format,
            'datetime': exif_data.get('DateTime', ''),
            'datetime_original': exif_data.get('DateTimeOriginal', ''),
            'make': exif_data.get('Make', ''),
            'model': exif_data.get('Model', ''),
        }
        
        # 提取 GPS 信息
        gps_info = exif_data.get('GPSInfo')
        if gps_info:
            lat, lon = extract_gps(gps_info)
            if lat and lon:
                result['gps'] = {'latitude': lat, 'longitude': lon}
        
        return result
        
    except Exception as e:
        print(f"Error analyzing {photo_path}: {e}", file=sys.stderr)
        return None


def extract_gps(gps_info):
    """从 GPSInfo 提取经纬度"""
    def convert_to_degrees(value):
        """将 GPS 坐标转换为度数"""
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    
    try:
        lat = convert_to_degrees(gps_info[2])  # GPSLatitude
        lat_ref = gps_info[1]  # GPSLatitudeRef
        if lat_ref != 'N':
            lat = -lat
        
        lon = convert_to_degrees(gps_info[4])  # GPSLongitude
        lon_ref = gps_info[3]  # GPSLongitudeRef
        if lon_ref != 'E':
            lon = -lon
        
        return lat, lon
    except:
        return None, None


def build_timeline(photos):
    """构建照片时间线"""
    # 按时间排序
    dated_photos = []
    for p in photos:
        dt_str = p.get('datetime_original') or p.get('datetime')
        if dt_str:
            try:
                dt = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
                dated_photos.append((dt, p))
            except:
                pass
    
    dated_photos.sort(key=lambda x: x[0])
    
    # 按年-月分组
    timeline = {}
    for dt, p in dated_photos:
        key = dt.strftime('%Y-%m')
        if key not in timeline:
            timeline[key] = []
        timeline[key].append({
            'date': dt.strftime('%Y-%m-%d'),
            'filename': p['filename'],
            'has_gps': 'gps' in p
        })
    
    return timeline


def extract_locations(photos):
    """提取地点信息"""
    locations = []
    for p in photos:
        if 'gps' in p:
            locations.append({
                'filename': p['filename'],
                'date': p.get('datetime_original', p.get('datetime', '')),
                'gps': p['gps']
            })
    return locations


def main():
    parser = argparse.ArgumentParser(description='分析照片 EXIF 信息')
    parser.add_argument('--dir', required=True, help='照片目录路径')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    photo_dir = Path(args.dir)
    if not photo_dir.exists():
        print(f"Error: Directory not found: {photo_dir}", file=sys.stderr)
        sys.exit(1)
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
    
    # 分析所有照片
    photos = []
    for ext in image_extensions:
        for photo_path in photo_dir.rglob(f'*{ext}'):
            result = analyze_photo(photo_path)
            if result:
                photos.append(result)
    
    # 构建时间线
    timeline = build_timeline(photos)
    
    # 提取地点
    locations = extract_locations(photos)
    
    # 输出
    output = {
        'directory': str(photo_dir),
        'photo_count': len(photos),
        'photos_with_exif': len([p for p in photos if p.get('exif') is not None]),
        'photos_with_gps': len(locations),
        'timeline': timeline,
        'locations': locations,
        'photos': photos[:50]  # 限制输出数量
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"分析完成: {len(photos)} 张照片")
    print(f"  含 EXIF: {output['photos_with_exif']}")
    print(f"  含 GPS: {output['photos_with_gps']}")
    print(f"输出文件: {args.output}")


if __name__ == '__main__':
    main()
