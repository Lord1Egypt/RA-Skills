#!/usr/bin/env python3
"""
坐标转换工具 - Coordinate Transformation Tool
支持 GeoJSON 和 WKT 格式的坐标系统转换
支持：中国坐标系(CGCS2000)、WGS84、火星坐标系(GCJ-02)、百度坐标系(BD-09)
"""

import sys
import json
import argparse
import math
import re
from pathlib import Path

try:
    from pyproj import Transformer, CRS
except ImportError:
    print("ERROR: pyproj not installed. Run: apt-get install python3-pyproj")
    sys.exit(1)


# ============== 坐标系定义 ==============
CRS_DEFINITIONS = {
    # 中国常用坐标系
    "4326": "EPSG:4326",   # WGS84 (GPS标准)
    "4490": "EPSG:4490",   # CGCS2000 (国家2000坐标系)
    "4547": "EPSG:4547",   # CGCS2000 / 3-degree Gauss-Kruger zone 39
    "4548": "EPSG:4548",   # CGCS2000 / 3-degree Gauss-Kruger zone 40
    "4549": "EPSG:4549",   # CGCS2000 / 3-degree Gauss-Kruger zone 41
    "4552": "EPSG:4552",   # CGCS2000 / 3-degree Gauss-Kruger CM 117E
    "4553": "EPSG:4553",   # CGCS2000 / 3-degree Gauss-Kruger CM 120E
    "4554": "EPSG:4554",   # CGCS2000 / 3-degree Gauss-Kruger CM 123E
    "4555": "EPSG:4555",   # CGCS2000 / 3-degree Gauss-Kruger CM 126E
    "4556": "EPSG:4556",   # CGCS2000 / 3-degree Gauss-Kruger CM 129E
    "3857": "EPSG:3857",   # Web Mercator (互联网地图常用)
    "4214": "EPSG:4214",   # Beijing 1954
    "2433": "EPSG:2433",   # Beijing 1954 / 3-degree Gauss-Kruger zone 39
    "2434": "EPSG:2434",   # Beijing 1954 / 3-degree Gauss-Kruger zone 40
    "2435": "EPSG:2435",   # Beijing 1954 / 3-degree Gauss-Kruger zone 41
    # 国际常用
    "32648": "EPSG:32648", # WGS 84 / UTM zone 48N
    "32649": "EPSG:32649", # WGS 84 / UTM zone 49N
    "32650": "EPSG:32650", # WGS 84 / UTM zone 50N
}

# 火星坐标系和百度坐标系的特殊标记
GCJ02 = "gcj02"   # 火星坐标系 (高德、腾讯地图使用)
BD09 = "bd09"     # 百度坐标系


# ============== 火星坐标系/百度坐标系转换算法 ==============

# WGS84转GCJ02的偏差参数
GCJ02_PARS = {
    'a': 6378245.0,
    'ee': 0.00669342162296594723,
}

def out_of_china(lng, lat):
    """判断坐标是否在中国境外"""
    return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)

def transform_lat(x, y):
    """计算纬度偏移"""
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret

def transform_lng(x, y):
    """计算经度偏移"""
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

def wgs84_to_gcj02(lng, lat):
    """WGS84转火星坐标系(GCJ-02)"""
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - GCJ02_PARS['ee'] * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((GCJ02_PARS['a'] * (1 - GCJ02_PARS['ee'])) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (GCJ02_PARS['a'] / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return mglng, mglat

def gcj02_to_wgs84(lng, lat):
    """火星坐标系(GCJ-02)转WGS84"""
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - GCJ02_PARS['ee'] * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((GCJ02_PARS['a'] * (1 - GCJ02_PARS['ee'])) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (GCJ02_PARS['a'] / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat - dlat
    mglng = lng - dlng
    return mglng, mglat

def gcj02_to_bd09(lng, lat):
    """火星坐标系(GCJ-02)转百度坐标系(BD-09)"""
    x = lng
    y = lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * math.pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * math.pi)
    bdlng = z * math.cos(theta) + 0.0065
    bdlat = z * math.sin(theta) + 0.006
    return bdlng, bdlat

def bd09_to_gcj02(lng, lat):
    """百度坐标系(BD-09)转火星坐标系(GCJ-02)"""
    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * math.pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * math.pi)
    gcjlng = z * math.cos(theta)
    gcjlat = z * math.sin(theta)
    return gcjlng, gcjlat

def wgs84_to_bd09(lng, lat):
    """WGS84直接转百度坐标系(BD-09)"""
    gLng, gLat = wgs84_to_gcj02(lng, lat)
    return gcj02_to_bd09(gLng, gLat)

def bd09_to_wgs84(lng, lat):
    """百度坐标系(BD-09)直接转WGS84"""
    gLng, gLat = bd09_to_gcj02(lng, lat)
    return gcj02_to_wgs84(gLng, gLat)


# ============== 坐标转换调度器 ==============

class CoordTransformer:
    """坐标转换器，支持多种坐标系之间的转换"""
    
    def __init__(self, src_crs, dst_crs):
        self.src_crs = src_crs.upper() if isinstance(src_crs, str) else src_crs
        self.dst_crs = dst_crs.upper() if isinstance(dst_crs, str) else dst_crs
        
        # 标准化CRS
        self.src_type = self._get_crs_type(self.src_crs)
        self.dst_type = self._get_crs_type(self.dst_crs)
        
        # 如果都是EPSG坐标系，创建pyproj转换器
        if self.src_type == 'epsg' and self.dst_type == 'epsg':
            src_epsg = resolve_crs(str(self.src_crs))
            dst_epsg = resolve_crs(str(self.dst_crs))
            self.transformer = Transformer.from_crs(src_epsg, dst_epsg, always_xy=True)
        else:
            self.transformer = None
    
    def _get_crs_type(self, crs):
        """判断CRS类型"""
        crs_str = str(crs).upper()
        if crs_str in (GCJ02.upper(), 'GCJ02', 'MARS'):
            return 'gcj02'
        elif crs_str in (BD09.upper(), 'BD09', 'BAIDU'):
            return 'bd09'
        elif 'EPSG:' in crs_str or crs_str.isdigit():
            return 'epsg'
        else:
            return 'epsg'  # 默认按EPSG处理
    
    def transform_point(self, x, y):
        """转换单个点坐标"""
        if self.transformer:
            return self.transformer.transform(x, y)
        
        # 使用中国坐标转换算法
        return self._transform_chinese(x, y)
    
    def _transform_chinese(self, lng, lat):
        """中国坐标系统之间的转换"""
        src = self.src_type
        dst = self.dst_type
        
        # WGS84 <-> GCJ02
        if src == 'epsg' and dst == 'gcj02':
            return wgs84_to_gcj02(lng, lat)
        elif src == 'gcj02' and dst == 'epsg':
            return gcj02_to_wgs84(lng, lat)
        
        # WGS84 <-> BD09
        elif src == 'epsg' and dst == 'bd09':
            return wgs84_to_bd09(lng, lat)
        elif src == 'bd09' and dst == 'epsg':
            return bd09_to_wgs84(lng, lat)
        
        # GCJ02 <-> BD09
        elif src == 'gcj02' and dst == 'bd09':
            return gcj02_to_bd09(lng, lat)
        elif src == 'bd09' and dst == 'gcj02':
            return bd09_to_gcj02(lng, lat)
        
        # 相同坐标系
        elif src == dst:
            return lng, lat
        
        else:
            raise ValueError(f"不支持的坐标转换: {self.src_crs} -> {self.dst_crs}")


# ============== 辅助函数 ==============

def resolve_crs(crs_str: str) -> str:
    """解析坐标系字符串，支持EPSG代码或完整WKT"""
    if not crs_str:
        raise ValueError("坐标系不能为空")

    crs_str = str(crs_str).strip().upper()

    # 已经是完整EPSG格式
    if crs_str.startswith("EPSG:"):
        return crs_str

    # 火星/百度坐标系
    if crs_str in (GCJ02.upper(), 'MARS'):
        return GCJ02
    if crs_str in (BD09.upper(), 'BAIDU'):
        return BD09

    # 尝试直接作为EPSG代码
    if crs_str.isdigit():
        if crs_str in CRS_DEFINITIONS:
            return CRS_DEFINITIONS[crs_str]
        return f"EPSG:{crs_str}"

    # 尝试在预定义中匹配
    if crs_str.upper() in CRS_DEFINITIONS:
        return CRS_DEFINITIONS[crs_str.upper()]

    return crs_str


def transform_coords(coords, transformer):
    """递归转换坐标数组（处理嵌套结构）"""
    if isinstance(coords, list) and len(coords) > 0:
        if isinstance(coords[0], (int, float)):
            # 点坐标 [x, y] 或 [lon, lat]
            return list(transformer.transform_point(coords[0], coords[1]))
        else:
            # 嵌套坐标数组（多边形、线等）
            return [transform_coords(c, transformer) for c in coords]
    return coords


def transform_wkt_geometry(wkt_str: str, transformer) -> str:
    """
    转换WKT几何体中的所有坐标
    使用状态机解析WKT字符串，只转换坐标数字对
    """
    num_pattern = r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
    
    result = []
    i = 0
    n = len(wkt_str)
    
    while i < n:
        c = wkt_str[i]
        
        if c.isdigit() or c in '.-+':
            match = re.match(num_pattern, wkt_str[i:])
            if match:
                num_str = match.group(0)
                j = i + len(num_str)
                # 跳过空白
                while j < n and wkt_str[j] in ' \t\n\r':
                    j += 1
                if j < n:
                    next_c = wkt_str[j]
                    if next_c.isdigit() or next_c in '.-+':
                        match2 = re.match(num_pattern, wkt_str[j:])
                        if match2:
                            x = float(num_str)
                            y = float(match2.group(0))
                            tx, ty = transformer.transform_point(x, y)
                            result.append(f"{tx} {ty}")
                            i = j + len(match2.group(0))
                            continue
                    else:
                        result.append(num_str)
                        i = j
                        continue
                else:
                    result.append(num_str)
                    i = j
                continue
            else:
                result.append(c)
                i += 1
                continue
        
        result.append(c)
        i += 1
    
    return ''.join(result)


def transform_geojson(geojson_data: dict, transformer) -> dict:
    """转换GeoJSON中的所有坐标"""
    result = json.loads(json.dumps(geojson_data))  # 深拷贝

    def transform_geometry(geom):
        if not geom or "coordinates" not in geom:
            return
        geom["coordinates"] = transform_coords(geom["coordinates"], transformer)

    geom = result.get("geometry", {})

    # 处理FeatureCollection
    if "type" in result and result["type"] == "FeatureCollection":
        for feature in result.get("features", []):
            transform_geometry(feature.get("geometry", {}))

    # 处理单独Feature
    elif "type" in result and result["type"] == "Feature":
        transform_geometry(geom)

    # 处理直接的几何对象
    elif "type" in result and result.get("geometry") is None and "coordinates" in result:
        transform_geometry(result)

    return result


# ============== WKT <-> GeoJSON 转换 ==============

def wkt_to_geojson(wkt_str: str) -> dict:
    """将WKT转换为GeoJSON"""
    wkt_str = wkt_str.strip().upper()
    
    # 提取几何类型和坐标内容
    if wkt_str.startswith('POINT'):
        match = re.search(r'POINT\s*\((.+)\)', wkt_str)
        if match:
            coords = [float(x) for x in match.group(1).split()]
            return {"type": "Point", "coordinates": coords}
    
    elif wkt_str.startswith('LINESTRING'):
        match = re.search(r'LINESTRING\s*\((.+)\)', wkt_str)
        if match:
            coords = [[float(x) for x in pair.split()] for pair in match.group(1).split(',')]
            return {"type": "LineString", "coordinates": coords}
    
    elif wkt_str.startswith('POLYGON'):
        match = re.search(r'POLYGON\s*\((.+)\)', wkt_str)
        if match:
            rings_str = match.group(1)
            rings = []
            for ring in rings_str.split('),'):
                ring = ring.strip('(').strip(')')
                coords = [[float(x) for x in pair.split()] for pair in ring.split(',')]
                rings.append(coords)
            return {"type": "Polygon", "coordinates": rings}
    
    elif wkt_str.startswith('MULTIPOINT'):
        match = re.search(r'MULTIPOINT\s*\((.+)\)', wkt_str)
        if match:
            coords = [[float(x) for x in pair.split()] for pair in match.group(1).split(',')]
            return {"type": "MultiPoint", "coordinates": coords}
    
    elif wkt_str.startswith('MULTILINESTRING'):
        match = re.search(r'MULTILINESTRING\s*\((.+)\)', wkt_str)
        if match:
            lines_str = match.group(1)
            lines = []
            for line in lines_str.split('),'):
                line = line.strip('(').strip(')')
                coords = [[float(x) for x in pair.split()] for pair in line.split(',')]
                lines.append(coords)
            return {"type": "MultiLineString", "coordinates": lines}
    
    elif wkt_str.startswith('MULTIPOLYGON'):
        match = re.search(r'MULTIPOLYGON\s*\((.+)\)', wkt_str)
        if match:
            polygons_str = match.group(1)
            polygons = []
            for polygon in polygons_str.split(')),'):
                polygon = polygon.strip('(').strip(')')
                rings = []
                for ring in polygon.split('),('):
                    ring = ring.strip('(').strip(')')
                    coords = [[float(x) for x in pair.split()] for pair in ring.split(',')]
                    rings.append(coords)
                polygons.append(rings)
            return {"type": "MultiPolygon", "coordinates": polygons}
    
    raise ValueError(f"不支持的WKT类型: {wkt_str[:50]}")


def geojson_to_wkt(geojson_data: dict) -> str:
    """将GeoJSON转换为WKT"""
    geom = geojson_data.get("geometry", geojson_data)
    geom_type = geom.get("type", "").upper()
    coords = geom.get("coordinates", [])
    
    if geom_type == "POINT":
        return f"POINT({coords[0]} {coords[1]})"
    
    elif geom_type == "LINESTRING":
        coord_strs = [f"{c[0]} {c[1]}" for c in coords]
        return f"LINESTRING({','.join(coord_strs)})"
    
    elif geom_type == "POLYGON":
        ring_strs = []
        for ring in coords:
            coord_strs = [f"{c[0]} {c[1]}" for c in ring]
            ring_strs.append(f"({','.join(coord_strs)})")
        return f"POLYGON(({','.join(ring_strs)}))"
    
    elif geom_type == "MULTIPOINT":
        coord_strs = [f"{c[0]} {c[1]}" for c in coords]
        return f"MULTIPOINT({','.join(coord_strs)})"
    
    elif geom_type == "MULTILINESTRING":
        line_strs = []
        for line in coords:
            coord_strs = [f"{c[0]} {c[1]}" for c in line]
            line_strs.append(f"({','.join(coord_strs)})")
        return f"MULTILINESTRING({','.join(line_strs)})"
    
    elif geom_type == "MULTIPOLYGON":
        poly_strs = []
        for polygon in coords:
            ring_strs = []
            for ring in polygon:
                coord_strs = [f"{c[0]} {c[1]}" for c in ring]
                ring_strs.append(f"({','.join(coord_strs)})")
            poly_strs.append(f"(({','.join(ring_strs)}))")
        return f"MULTIPOLYGON({','.join(poly_strs)})"
    
    elif geom_type == "GEOMETRYCOLLECTION":
        geoms = geom.get("geometries", [])
        geom_strs = [geojson_to_wkt(g) for g in geoms]
        return f"GEOMETRYCOLLECTION({','.join(geom_strs)})"
    
    raise ValueError(f"不支持的GeoJSON类型: {geom_type}")


def load_input(input_spec: str) -> tuple:
    """加载输入数据，返回 (data, input_format)"""
    path = Path(input_spec)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    else:
        content = input_spec.strip()

    if content.startswith('{') or content.startswith('['):
        try:
            data = json.loads(content)
            if isinstance(data, dict) and ("type" in data or "geometry" in data or "features" in data):
                return data, "geojson"
            return data, "geojson"
        except json.JSONDecodeError:
            pass

    return content, "wkt"


# ============== 主程序 ==============

def run(args=None):
    parser = argparse.ArgumentParser(
        description="坐标转换工具 - 支持 GeoJSON/WKT 格式互转，支持中国常用坐标系",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # WKT转GeoJSON
  python3 coord_convert.py --wkt "POINT(113 23)" --from 4326 --to 4490 --format geojson

  # GeoJSON转WKT
  python3 coord_convert.py --input data.geojson --from 4490 --to 4326 --format wkt

  # 坐标系统转换 (4490 -> 4547)
  python3 coord_convert.py --wkt "POINT(113 23)" --from 4490 --to 4547

  # 火星坐标系转换 (WGS84 -> GCJ02)
  python3 coord_convert.py --wkt "POINT(113 23)" --from 4326 --to gcj02

  # 百度坐标系转换 (GCJ02 -> BD09)
  python3 coord_convert.py --wkt "POINT(113 23)" --from gcj02 --to bd09

支持的坐标系:
  EPSG代码: 4326(WGS84), 4490(CGCS2000), 4547-4556(3度分带), 3857(Web墨卡托), 4214(北京54)
  中国专属: gcj02(火星坐标系), bd09(百度坐标系)
        """
    )

    parser.add_argument("--input", "-i", help="输入文件路径或GeoJSON/WKT字符串")
    parser.add_argument("--wkt", help="直接指定WKT字符串（覆盖--input）")
    parser.add_argument("--from", "-f", dest="src_crs",
                        help="源坐标系 (如 4490, 4326, gcj02, bd09)")
    parser.add_argument("--to", "-t", dest="dst_crs",
                        help="目标坐标系 (如 4490, 4326, gcj02, bd09)")
    parser.add_argument("--output", "-o", help="输出文件路径 (不指定则输出到stdout)")
    parser.add_argument("--format", "-F", choices=["geojson", "wkt", "auto"], default="auto",
                        help="输出格式 (默认自动推断)")
    parser.add_argument("--list-crs", action="store_true",
                        help="列出所有支持的坐标系代码")

    parsed = parser.parse_args(args)

    if parsed.list_crs:
        print("支持的坐标系代码:")
        print("\nEPSG 坐标系:")
        for code, definition in sorted(CRS_DEFINITIONS.items()):
            print(f"  {code:6s} -> {definition}")
        print("\n中国专属坐标系:")
        print(f"  gcj02  -> 火星坐标系 (高德、腾讯地图使用)")
        print(f"  bd09   -> 百度坐标系")
        return 0

    if not parsed.src_crs or not parsed.dst_crs:
        parser.error("必须指定 --from/-f 和 --to/-t")

    # 确定输入
    if parsed.wkt:
        input_data, input_format = parsed.wkt, "wkt"
    elif parsed.input:
        input_data, input_format = load_input(parsed.input)
    else:
        parser.error("必须指定 --input 或 --wkt")

    # 确定输出格式
    if parsed.format != "auto":
        output_format = parsed.format
    else:
        output_format = "geojson" if input_format == "wkt" else "wkt"

    # 创建转换器
    transformer = CoordTransformer(parsed.src_crs, parsed.dst_crs)

    # 执行转换
    try:
        # 如果需要格式转换
        if input_format == "wkt" and output_format == "geojson":
            # WKT -> GeoJSON（同时转换坐标）
            geojson = wkt_to_geojson(input_data)
            result = transform_geojson({"type": "Feature", "geometry": geojson, "properties": {}}, transformer)
            result = result["geometry"]
        elif input_format == "geojson" and output_format == "wkt":
            # GeoJSON -> WKT（同时转换坐标）
            transformed = transform_geojson(input_data if isinstance(input_data, dict) else {"type": "Feature", "geometry": input_data, "properties": {}}, transformer)
            result = geojson_to_wkt(transformed)
        elif input_format == "wkt":
            # WKT，保持WKT格式
            result = transform_wkt_geometry(input_data, transformer)
        else:
            # GeoJSON，保持GeoJSON格式
            result = transform_geojson(input_data, transformer)
    except Exception as e:
        print(f"转换错误: {e}", file=sys.stderr)
        return 1

    # 输出结果
    if output_format == "geojson" and isinstance(result, dict):
        output_json = json.dumps(result, ensure_ascii=False, indent=2)
        if parsed.output:
            with open(parsed.output, 'w', encoding='utf-8') as f:
                f.write(output_json)
            print(f"✅ 转换完成，输出文件: {parsed.output}")
        else:
            print(output_json)
    else:
        output_str = str(result)
        if parsed.output:
            with open(parsed.output, 'w', encoding='utf-8') as f:
                f.write(output_str)
            print(f"✅ 转换完成，输出文件: {parsed.output}")
        else:
            print(output_str)

    return 0


if __name__ == "__main__":
    sys.exit(run())
