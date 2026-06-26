#!/usr/bin/env python3
"""
DWG/DXF 图纸遍历和面积/周长计算脚本

支持两种模式：
1. 单个查询：python dxf_handle.py <dwg文件> --query 客厅 --type area
2. 全部查询：python dxf_handle.py <dwg文件> --type area
"""

import sys
import json
import argparse
import csv
from pathlib import Path

try:
    import ezdxf
except ImportError:
    print("错误：需要安装 ezdxf 库")
    print("  pip install ezdxf")
    sys.exit(1)


def load_layer_config(config_path="layers.json"):
    """加载图层配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"配置文件不存在: {config_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误: {e}")
        return None


def calculate_area(polyline):
    """计算闭合多段线的面积"""
    try:
        if hasattr(polyline, 'area'):
            return polyline.area()
        
        points = list(polyline.points())
        if len(points) < 3:
            return 0.0
        
        area = 0.0
        n = len(points)
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        return abs(area) / 2.0
    except Exception as e:
        return 0.0


def calculate_perimeter(polyline):
    """计算多段线的周长"""
    try:
        points = list(polyline.points())
        if len(points) < 2:
            return 0.0
        
        perimeter = 0.0
        n = len(points)
        for i in range(n):
            j = (i + 1) % n
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            perimeter += (dx**2 + dy**2)**0.5
        
        return perimeter
    except Exception as e:
        return 0.0


def is_closed(entity):
    """检查多段线是否闭合"""
    try:
        if hasattr(entity, 'is_closed') and entity.is_closed:
            return True
        
        points = list(entity.points())
        if len(points) < 2:
            return False
        first = points[0]
        last = points[-1]
        return first[0] == last[0] and first[1] == last[1]
    except:
        return False


def query_single_room(dwg_path, config, room_name, calc_type):
    """查询单个房间的面积或周长"""
    
    layers_config = config.get("layers", []) if config else []
    
    # 在配置里找这个房间对应的图层
    target_layer = None
    for item in layers_config:
        if isinstance(item, dict):
            description = item.get("description", "")
            if description == room_name or item.get("layerName", "").find(room_name) >= 0:
                target_layer = item.get("layerName")
                break
    
    if target_layer is None:
        return None, f"没找到{room_name}图层"
    
    # 在 DWG 里查这个图层
    try:
        doc = ezdxf.readfile(dwg_path)
    except IOError as e:
        return None, f"无法打开文件: {e}"
    
    msp = doc.modelspace()
    
    # 检查图层是否存在
    if target_layer not in doc.layers:
        return None, f"没找到{room_name}图层"
    
    # 计算
    count = 0
    total = 0.0
    
    for entity in msp:
        if entity.dxftype() not in ('LWPOLYLINE', 'POLYLINE'):
            continue
        if entity.dxf.layer != target_layer:
            continue
        if not is_closed(entity):
            continue
        
        if calc_type == "area":
            value = calculate_area(entity)
        else:
            value = calculate_perimeter(entity)
        
        count += 1
        total += value
    
    if count == 0:
        return None, f"没找到{room_name}图层"
    
    return {"name": room_name, "layer": target_layer, "count": count, "total": total}, None


def query_all_rooms(dwg_path, config, calc_type):
    """查询所有房间的面积或周长"""
    
    try:
        doc = ezdxf.readfile(dwg_path)
    except IOError as e:
        print(f"无法打开文件: {e}")
        return None
    
    msp = doc.modelspace()
    
    layers_config = config.get("layers", []) if config else []
    
    # 构建图层名 -> 描述 的映射
    layer_map = {}
    for item in layers_config:
        if isinstance(item, dict) and "layerName" in item:
            layer_map[item["layerName"]] = item.get("description", "")
    
    results = {}
    
    # 遍历配置里的每一个图层
    for layer_name, description in layer_map.items():
        
        # 在 DWG 里查找这个图层是否存在
        if layer_name not in doc.layers:
            continue
        
        # 找这个图层里所有的闭合多段线
        count = 0
        total = 0.0
        
        for entity in msp:
            if entity.dxftype() not in ('LWPOLYLINE', 'POLYLINE'):
                continue
            if entity.dxf.layer != layer_name:
                continue
            if not is_closed(entity):
                continue
            
            if calc_type == "area":
                value = calculate_area(entity)
            else:
                value = calculate_perimeter(entity)
            
            count += 1
            total += value
        
        if count > 0:
            results[layer_name] = {
                'layer': layer_name,
                'name': description,
                'count': count,
                'total': total
            }
    
    return results


def main():
    parser = argparse.ArgumentParser(description="DWG 图纸面积和周长计算工具")
    parser.add_argument('dwg_file', help="DWG/DXF 文件路径")
    parser.add_argument('--query', '-q', help="查询单个房间，如：客厅、主卧")
    parser.add_argument('--type', '-t', choices=['area', 'perimeter'], 
                        default='area', help="计算类型: area 或 perimeter")
    parser.add_argument('--output', '-o', help="输出 CSV 文件路径")
    
    args = parser.parse_args()
    
    if not Path(args.dwg_file).exists():
        print(f"文件不存在: {args.dwg_file}")
        sys.exit(1)
    
    # 加载配置
    script_dir = Path(__file__).parent.parent / "references"
    config_path = script_dir / "layers.json"
    config = load_layer_config(str(config_path))
    
    if config is None:
        sys.exit(1)
    
    # 单个查询模式
    if args.query:
        result, error = query_single_room(args.dwg_file, config, args.query, args.type)
        if error:
            print(error)
        else:
            unit = "m²" if args.type == "area" else "m"
            print(f"{result['name']}: {result['total']:.2f} {unit}")
        return
    
    # 全部查询模式
    results = query_all_rooms(args.dwg_file, config, args.type)
    
    if not results:
        print("\n未找到匹配的实体")
        return
    
    print(f"找到 {len(results)} 个图层")
    print("-" * 40)
    
    result_list = sorted(results.values(), key=lambda x: x['layer'])
    unit = "m²" if args.type == "area" else "m"
    
    for r in result_list:
        print(f"{r['name']}: {r['total']:.2f} {unit}")
    
    # 输出 CSV
    if args.output:
        with open(args.output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            type_label = "面积" if args.type == "area" else "周长"
            writer.writerow(['名称', '图层', '数量', type_label])
            for r in result_list:
                writer.writerow([
                    r['name'],
                    r['layer'],
                    r['count'],
                    f"{r['total']:.2f}"
                ])
        print(f"\n已保存到: {args.output}")
    
    print("\n完成!")


if __name__ == "__main__":
    main()
