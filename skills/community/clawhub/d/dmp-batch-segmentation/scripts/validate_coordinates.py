#!/usr/bin/env python3
"""
坐标文件校验模块
功能：校验用户上传的坐标文件格式是否正确
"""

import sys
import json
from pathlib import Path

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

def validate_coordinate_file(file_path):
    """
    校验坐标文件格式
    
    Args:
        file_path: 文件路径
        
    Returns:
        dict: {
            "is_valid": bool,
            "error_msg": str,
            "coordinates": list,
            "total_count": int
        }
    """
    result = {
        "is_valid": False,
        "error_msg": "",
        "coordinates": [],
        "total_count": 0
    }
    
    file_path = Path(file_path)
    
    # 检查文件是否存在
    if not file_path.exists():
        result["error_msg"] = f"文件不存在: {file_path}"
        return result
    
    # 检查文件扩展名
    suffix = file_path.suffix.lower()
    if suffix not in ['.csv', '.xlsx', '.xls']:
        result["error_msg"] = f"不支持的文件格式: {suffix}，仅支持 .csv, .xlsx, .xls"
        return result
    
    if not PANDAS_AVAILABLE:
        result["error_msg"] = "pandas库未安装，无法读取Excel文件"
        return result
    
    try:
        # 读取文件
        if suffix == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # 检查列名
        columns = [col.lower().strip() for col in df.columns]
        
        # 查找经度列
        lng_col = None
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in ['lng', '经度', 'longitude', 'lon']:
                lng_col = col
                break
        
        # 查找纬度列
        lat_col = None
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in ['lat', '纬度', 'latitude']:
                lat_col = col
                break
        
        if lng_col is None or lat_col is None:
            result["error_msg"] = f"文件格式错误：未找到经度(lng)和纬度(lat)列\n当前列名: {list(df.columns)}\n请确保文件包含经度(lng)和纬度(lat)两列"
            return result
        
        # 提取坐标数据
        coordinates = []
        for idx, row in df.iterrows():
            try:
                lng = str(row[lng_col]).strip()
                lat = str(row[lat_col]).strip()
                
                # 验证坐标格式
                lng_float = float(lng)
                lat_float = float(lat)
                
                # 验证坐标范围（中国范围）
                if not (73 <= lng_float <= 135):
                    result["error_msg"] = f"第{idx+2}行经度超出范围: {lng}（应在73-135之间）"
                    return result
                if not (3 <= lat_float <= 54):
                    result["error_msg"] = f"第{idx+2}行纬度超出范围: {lat}（应在3-54之间）"
                    return result
                
                coordinates.append({
                    "lng": lng,
                    "lat": lat
                })
            except (ValueError, TypeError) as e:
                result["error_msg"] = f"第{idx+2}行坐标格式错误: {row[lng_col]}, {row[lat_col]}"
                return result
        
        result["is_valid"] = True
        result["coordinates"] = coordinates
        result["total_count"] = len(coordinates)
        
    except Exception as e:
        result["error_msg"] = f"读取文件失败: {str(e)}"
    
    return result

def print_validation_result(result):
    """打印校验结果"""
    print("\n" + "="*50)
    print("坐标文件校验结果")
    print("="*50)
    
    if result["is_valid"]:
        print(f"✅ 校验通过")
        print(f"   总坐标数: {result['total_count']}个")
        print(f"   预计批次数: {(result['total_count'] + 199) // 200}个（每批200个坐标）")
        print(json.dumps(result["coordinates"][:3], ensure_ascii=False, indent=2))
        if result["total_count"] > 3:
            print(f"   ... 共{result['total_count']}个坐标")
    else:
        print(f"❌ 校验失败")
        print(f"   错误信息: {result['error_msg']}")
    
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python validate_coordinates.py <文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = validate_coordinate_file(file_path)
    print_validation_result(result)
    
    # 输出JSON结果供其他脚本调用
    print("\n---JSON_RESULT---")
    print(json.dumps(result, ensure_ascii=False))
    
    sys.exit(0 if result["is_valid"] else 1)
