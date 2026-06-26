#!/usr/bin/env python3
"""
等时圈生成器：百度坐标 → WGS84 → Mapbox等时圈
用法: python generate_isochrone.py <地址> <百度AK> <MapboxAK> <出行模式> <时间(分钟)> [输出目录]
出行模式: driving / walking / cycling
输出: point.shp(起点) + isochrone.shp(等时圈面) + 预览图.png
"""

import sys
import os
import json
import math
import io
import warnings
warnings.filterwarnings("ignore")

import requests
from coord_convert.transform import bd2wgs
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "WenQuanYi Micro Hei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False


# ============================================================
# 免费 WGS84 底图绘制（Natural Earth + matplotlib）
# ============================================================

try:
    import cartopy
    import cartopy.crs as ccrs
    HAS_CARTOPY = True
except ImportError:
    HAS_CARTOPY = False

try:
    import contextily as ctx
    HAS_CONTEXTILY = True
except ImportError:
    HAS_CONTEXTILY = False


# ============================================================
# 核心函数
# ============================================================

def geocode_baidu(address, ak):
    """调用百度地理编码API，返回第一个结果的 BD-09 坐标 (lng, lat)"""
    url = "https://api.map.baidu.com/geocoding/v3/"
    params = {"address": address, "ak": ak, "output": "json"}
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    if data.get("status") != 0:
        raise ValueError(f"百度地理编码失败: {data.get('msg', data)}")
    result = data.get("result", {})
    location = result.get("location", {})
    lng = location.get("lng")
    lat = location.get("lat")
    if lng is None or lat is None:
        raise ValueError(f"百度地理编码返回结果缺少坐标: {data}")
    return float(lng), float(lat), result.get("precise", 0), result.get("confidence", 0)


def bd09_to_wgs84(bd_lng, bd_lat):
    """百度BD-09坐标转WGS84"""
    return bd2wgs(bd_lng, bd_lat)


def get_mapbox_isochrone(wgs_lng, wgs_lat, mapbox_ak, mode, minutes):
    """调用 Mapbox Isochrone API，返回 GeoJSON FeatureCollection"""
    profiles = {"driving": "mapbox/driving", "walking": "mapbox/walking", "cycling": "mapbox/cycling"}
    profile = profiles.get(mode, "mapbox/driving")
    url = f"https://api.mapbox.com/isochrone/v1/{profile}/{wgs_lng},{wgs_lat}"
    params = {
        "access_token": mapbox_ak,
        "contours_minutes": str(minutes),
        "polygons": "true",
        "denoise": "1",
        "generalize": "0",
    }
    resp = requests.get(url, params=params, timeout=15)
    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 401:
        raise ValueError("Mapbox API 认证失败，请检查 AK 是否正确")
    elif resp.status_code == 422:
        raise ValueError(f"Mapbox API 参数错误 (422): {resp.text}")
    else:
        raise ValueError(f"Mapbox API 请求失败 ({resp.status_code}): {resp.text}")


def fetch_mapbox_map(wgs_lng, wgs_lat, bounds, mapbox_ak, output_path):
    """
    根据 isochrone 的 bbox 范围获取 Mapbox 底图（PNG）。
    bounds: (minx, miny, maxx, maxy) WGS84
    返回底图文件路径（下载失败返回 None）
    """
    minx, miny, maxx, maxy = bounds
    # bbox 字符串: "min_lng,min_lat,max_lng,max_lat"
    bbox_str = f"{minx},{miny},{maxx},{maxy}"

    # Mapbox Static Images API — 底图 + 等时圈 GeoJSON 叠加
    # style: mapbox/streets-v12（街道图）
    base_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v12/static"

    # 等时圈 GeoJSON 直接作为 overlay 传入（Mapbox 会在服务端渲染）
    overlay_part = f"geojson({json.dumps({'type': 'FeatureCollection', 'features': []})})"

    # 使用 bbox 方式，让 Mapbox 自动计算 zoom + center
    static_url = (
        f"{base_url}/"
        f"bbox:{bbox_str}/{800}x{600}@2x"
        f"?access_token={mapbox_ak}"
        f"&天正地图=no"
    )
    # 试 bbox 模式（Mapbox static API 支持）
    # 如失败回退到 center/zoom 模式
    try:
        resp = requests.get(static_url, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(output_path, "wb") as f:
                f.write(resp.content)
            print(f"  ✓ 底图已获取: {output_path} ({len(resp.content)//1024}KB)")
            return output_path
        else:
            print(f"  ⚠ 底图请求异常 ({resp.status_code})，将不使用底图")
            return None
    except Exception as e:
        print(f"  ⚠ 底图获取失败: {e}，将不使用底图")
        return None


def calc_zoom_by_bounds(bounds, img_w=800, img_h=600):
    """根据 bbox 范围估算合适的 Mapbox zoom level"""
    minx, miny, maxx, maxy = bounds
    width_deg = maxx - minx
    height_deg = maxy - miny

    # 每像素经度/纬度
    deg_per_px_x = width_deg / img_w
    deg_per_px_y = height_deg / img_h

    # 使用 EPSG:3857 投影估算（赤道处 1px ≈ 156543/2^zoom 米）
    # 这里直接用 log2 估算
    zoom_x = math.log2(360 / deg_per_px_x / 256) if deg_per_px_x > 0 else 14
    zoom_y = math.log2(180 / deg_per_px_y / 256) if deg_per_px_y > 0 else 14

    zoom = min(zoom_x, zoom_y, 18)  # 不超过 18
    return max(int(zoom), 8)        # 不低于 8


def fetch_mapbox_static_map(wgs_lng, wgs_lat, bounds, mapbox_ak, output_path):
    """
    使用 Mapbox Static Images API 获取底图。
    返回底图文件路径（失败返回 None）。
    """
    minx, miny, maxx, maxy = bounds
    center_lng = (minx + maxx) / 2
    center_lat = (miny + maxy) / 2
    zoom = calc_zoom_by_bounds(bounds)

    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/"
        f"{center_lng},{center_lat},{zoom}/{800}x{600}@2x"
        f"?access_token={mapbox_ak}"
    )
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(output_path, "wb") as f:
                f.write(resp.content)
            print(f"  ✓ 底图已获取 (zoom={zoom}): {output_path} ({len(resp.content)//1024}KB)")
            return output_path
        else:
            print(f"  ⚠ 底图请求失败 ({resp.status_code})，将不使用底图")
            return None
    except Exception as e:
        print(f"  ⚠ 底图获取失败: {e}，将不使用底图")
        return None


def wgs84_to_mercator(lng, lat):
    """WGS84 经纬度 → Web Mercator EPSG:3857 (米)"""
    x = lng * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) * 20037508.34 / math.pi
    return x, y


def mercator_to_wgs84(x, y):
    """Web Mercator EPSG:3857 → WGS84"""
    lng = x / 20037508.34 * 180
    lat = math.atan(math.exp(y / 20037508.34 * math.pi)) * 360 / math.pi - 90
    return lng, lat


def mercator_x_to_lng(x):
    """Mercator X → WGS84 经度"""
    return x / 20037508.34 * 180


def mercator_y_to_lat(y):
    """Mercator Y → WGS84 纬度"""
    return math.atan(math.exp(y / 20037508.34 * math.pi)) * 360 / math.pi - 90


def wgs84_lat_to_tile_y(lat_deg, z):
    """WGS84 纬度 → TMS tile y 坐标 (Google/OSM 标准公式)"""
    n = 2 ** z
    lat_rad = lat_deg * math.pi / 180
    lat_eff = math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad))
    ty = int(math.floor((1 - lat_eff / math.pi) / 2 * n))
    return ty


def tile_y_to_lat(ty, z):
    """TMS tile y 坐标 → WGS84 纬度（上边界的纬度）"""
    n = 2 ** z
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ty / n)))
    return lat_rad * 180 / math.pi


def wgs84_to_web_mercator_tile(lng, lat, z):
    """WGS84 经纬度 → Web Mercator TMS tile (tx, ty, z)"""
    n = 2 ** z
    tx = int(math.floor((lng + 180) / 360 * n))
    ty = wgs84_lat_to_tile_y(lat, z)
    return tx, ty


def tile_to_mercator_bounds(tx, ty, z):
    """Tile (tx,ty,z) → Web Mercator EPSG:3857 bounds (xmin, ymin, xmax, ymax) 米"""
    n = 2 ** z
    xmin = tx / n * 20037508.34 * 2 - 20037508.34
    xmax = (tx + 1) / n * 20037508.34 * 2 - 20037508.34
    lat_max_deg = tile_y_to_lat(ty, z)
    lat_min_deg = tile_y_to_lat(ty + 1, z)
    _, ymin = wgs84_to_mercator(0, lat_min_deg)
    _, ymax = wgs84_to_mercator(0, lat_max_deg)
    return xmin, ymin, xmax, ymax


def calc_zoom_by_mercator_bounds(bounds_wgs, tile_size_px=256, target_tiles=4):
    """
    根据 WGS84 bounds 计算最佳 zoom level。
    target_tiles: 期望覆盖整个区域需要的瓦片数量（长宽方向各几个）
    """
    import numpy as np
    minx, miny, maxx, maxy = bounds_wgs
    width_deg = maxx - minx
    height_deg = maxy - miny
    mid_lat = (miny + maxy) / 2
    m_per_deg_lng = 111320 * math.cos(mid_lat * math.pi / 180)
    m_per_deg_lat = 110540
    width_m = width_deg * m_per_deg_lng
    height_m = height_deg * m_per_deg_lat
    for z in range(8, 18):
        n = 2 ** z
        m_per_tile_lng = 20037508.34 * 2 / n
        tiles_x = width_m / m_per_tile_lng
        tiles_y = height_m / m_per_tile_lng
        # 找到 tiles 在 target_tiles 附近的最小 zoom（至少覆盖 target_tiles/2，最多 target_tiles*2 个瓦片）
        if tiles_x >= 0.5 and tiles_y >= 0.5:
            return z
    return 14


def fetch_esri_tiles_and_reproject_wgs84(bounds_wgs, output_path, n_tiles_target=4, request_timeout=10):
    """
    从 ESRI World Imagery 获取瓦片（EPSG:3857），拼图后用 rasterio 重投影为 WGS84。
    返回 (WGS84底图文件路径, WGS84 extent [west, south, east, north])
    """
    import numpy as np
    from PIL import Image
    import io
    import rasterio
    from rasterio.warp import calculate_default_transform, reproject, Resampling

    z = calc_zoom_by_mercator_bounds(bounds_wgs, target_tiles=n_tiles_target)
    print(f"  自动选择 zoom={z}（约 {n_tiles_target} 瓦片覆盖区域）")

    # WGS84 范围
    west, south, east, north = bounds_wgs

    # 计算 WGS84 → Mercator tile 坐标（使用模块级正确函数）
    tx_w, ty_n = wgs84_to_web_mercator_tile(west, north, z)   # 西北角 tile
    tx_e, ty_s = wgs84_to_web_mercator_tile(east, south, z)   # 东南角 tile
    # 取 bounding box 范围（可能 tx_w>tx_e 或 ty_s>ty_n，因为 WGS84 经纬度方向与 TMS y 方向不同）
    tx_min = min(tx_w, tx_e)
    tx_max = max(tx_w, tx_e)
    ty_min = min(ty_n, ty_s)
    ty_max = max(ty_n, ty_s)
    # 确保至少 1 tile
    tx_max = max(tx_max, tx_min)
    ty_max = max(ty_max, ty_min)
    print(f"  瓦片范围: x=[{tx_min},{tx_max}] y=[{ty_min},{ty_max}] 共 {(tx_max-tx_min+1)*(ty_max-ty_min+1)} 张")

    # 拼合 EPSG:3857 大图
    all_tiles = []
    tiles_arrays = []
    for ty in range(ty_min, ty_max + 1):  # ty_min=北(小), ty_max=南(大)
        row_tiles = []
        for tx in range(tx_min, tx_max + 1):
            url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{ty}/{tx}"
            r = requests.get(url, timeout=request_timeout)
            if r.status_code == 200 and len(r.content) > 1000:
                img = Image.open(io.BytesIO(r.content)).convert("RGB")
            else:
                img = Image.new("RGB", (256, 256), (128, 128, 128))
            row_tiles.append(np.array(img))
        tiles_arrays.append(np.hstack(row_tiles))
    mosaic = np.vstack(tiles_arrays)  # (height, width, 3)

    # 对应 Mercator bounds（使用模块级正确函数）
    xmin0, ymin0, xmax0, ymax0 = tile_to_mercator_bounds(tx_min, ty_max, z)
    xmin1, ymin1, xmax1, ymax1 = tile_to_mercator_bounds(tx_max, ty_min, z)
    merc_x_min = min(xmin0, xmin1)
    merc_x_max = max(xmax0, xmax1)
    merc_y_min = min(ymin0, ymin1)
    merc_y_max = max(ymax0, ymax1)
    merc_bounds = (merc_x_min, merc_y_min, merc_x_max, merc_y_max)
    print(f"  EPSG:3857 底图范围: x=[{merc_x_min:.0f},{merc_x_max:.0f}] y=[{merc_y_min:.0f},{merc_y_max:.0f}]")

    # 用 rasterio 将 EPSG:3857 Mosaic → WGS84 (EPSG:4326) GeoTIFF
    from rasterio.transform import from_bounds
    h, w = mosaic.shape[:2]
    src_transform = from_bounds(*merc_bounds, w, h)

    with rasterio.io.MemoryFile() as mem_3857:
        with mem_3857.open(
            driver="GTiff", height=h, width=w, count=3,
            dtype=np.uint8, crs="EPSG:3857",
            transform=src_transform
        ) as dst:
            dst.write(mosaic.transpose(2, 0, 1))

        with mem_3857.open() as src:
            transform, width, height = calculate_default_transform(
                src.crs, "EPSG:4326", w, h, *src.bounds
            )
            with rasterio.io.MemoryFile() as mem_wgs84:
                with mem_wgs84.open(
                    driver="GTiff", height=height, width=width, count=3,
                    dtype=np.uint8, crs="EPSG:4326", transform=transform
                ) as dst:
                    reproject(
                        source=rasterio.band(src, [1, 2, 3]),
                        destination=rasterio.band(dst, [1, 2, 3]),
                        src_transform=src.transform,
                        dst_transform=transform,
                        src_crs=src.crs,
                        dst_crs="EPSG:4326",
                        resampling=Resampling.bilinear
                    )
                mem_wgs84.seek(0)
                with open(output_path, "wb") as f:
                    f.write(mem_wgs84.read())

    # 计算 WGS84 extent
    with rasterio.open(output_path) as src:
        wgs84_bounds = src.bounds  # (west, south, east, north)
    print(f"  WGS84 底图已输出: {output_path}")
    print(f"  WGS84 extent: {wgs84_bounds}")
    return output_path, wgs84_bounds


def bounds_to_mercator(bounds):
    """将 WGS84 bounds 转为 Mercator bounds (xmin, ymin, xmax, ymax)"""
    minx, miny, maxx, maxy = bounds
    x1, y1 = wgs84_to_mercator(minx, miny)
    x2, y2 = wgs84_to_mercator(maxx, maxy)
    return x1, y1, x2, y2


def polygon_to_mercator(gdf):
    """将 GeoDataFrame 的几何体从 WGS84 转换为 EPSG:3857 (Mercator)"""
    gdf_copy = gdf.to_crs(epsg=3857)
    return gdf_copy


def save_shapefile(gdf, filepath):
    """保存 GeoDataFrame 为 Shapefile"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    gdf.to_file(filepath, encoding="utf-8")
    print(f"  ✓ 已保存: {filepath}")


def generate_preview(point_gdf, isochrone_gdf, address_name, mode, minutes,
                     output_path, mapbox_ak=None, base_map_path=None,
                     wgs84_extent=None):
    global os
    """
    生成等时圈预览图：
    - 有 WGS84 GeoTIFF 底图：ESRI 卫星影像重投影 → 最佳效果
    - 无底图时：matplotlib 绘制简洁 WGS84 网格背景（无外部依赖，极小文件）
    等时圈透明度: alpha=0.38（面）
    """
    fig, ax = plt.subplots(figsize=(10, 9))
    mode_labels = {"driving": "驾车", "walking": "步行", "cycling": "骑行"}
    mode_cn = mode_labels.get(mode, mode)

    if not isochrone_gdf.empty:
        bounds_wgs = isochrone_gdf.total_bounds
    else:
        bounds_wgs = None

    # ===== 路径A：WGS84 GeoTIFF 底图（卫星影像）======
    if wgs84_extent and base_map_path and os.path.exists(base_map_path):
        try:
            import rasterio
            with rasterio.open(base_map_path) as src:
                img_wgs84 = src.read()
                extent_wgs84 = src.bounds
            west, south, east, north = extent_wgs84
            ax.set_xlim(west, east)
            ax.set_ylim(south, north)
            ax.imshow(img_wgs84.transpose(1, 2, 0),
                      extent=[west, east, south, north],
                      origin="upper", aspect="auto", zorder=0)
            isochrone_gdf.plot(ax=ax, color="#4A90E2", alpha=0.35,
                               edgecolor="#1A5EB8", linewidth=2,
                               label="等时圈范围", zorder=2)
            if not point_gdf.empty:
                pt = point_gdf.geometry.iloc[0]
                ax.scatter(pt.x, pt.y, color="#E74C3C", s=150, marker="*",
                          edgecolor="white", linewidth=1.5, zorder=5)
                ax.annotate(
                    f"{address_name}\n({pt.x:.5f}, {pt.y:.5f})",
                    xy=(pt.x, pt.y), xytext=(8, 8),
                    textcoords="offset points", fontsize=9, color="#222222",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                              alpha=0.85, edgecolor="#999"), zorder=6)
            ax.set_xlabel("经度 (WGS84)", fontsize=9)
            ax.set_ylabel("纬度 (WGS84)", fontsize=9)
            ax.grid(True, linestyle="--", alpha=0.3, color="white")
            ax.set_title(f"等时圈预览 — {address_name}\n{mode_cn} {minutes}分钟",
                         fontsize=13, fontweight="bold")
            ax.set_aspect("equal")
            plt.tight_layout()
            # 先保存 PNG，再用 PIL 转为 JPG（控制文件大小）
            # 先保存 PNG，再用 PIL 转为 JPG（支持 quality 参数控制文件大小）
            png_tmp = output_path + '_tmp.png'
            plt.savefig(png_tmp, dpi=130, bbox_inches='tight', format='png')
            plt.close()
            img = Image.open(png_tmp).convert('RGB')
            img.save(output_path, 'JPEG', quality=82, optimize=True)
            __import__('os').remove(png_tmp)
            size = __import__('os').path.getsize(output_path) // 1024
            print(f"  ✓ 已保存预览图（WGS84底图，JPG压缩{size}KB）: {output_path}")
            return
        except Exception as e:
            print(f"  ⚠ WGS84底图渲染失败: {e}，使用简洁背景模式")

    # ===== 路径B：简洁WGS84网格背景（matplotlib原生，无外部依赖）======
    if bounds_wgs is not None:
        pad = (bounds_wgs[2] - bounds_wgs[0]) * 0.12
        xlim = (bounds_wgs[0] - pad, bounds_wgs[2] + pad)
        ylim = (bounds_wgs[1] - pad, bounds_wgs[3] + pad)
    else:
        xlim = None; ylim = None

    ax.set_facecolor("#EEF2F7")
    if xlim and ylim:
        ax.set_xlim(xlim); ax.set_ylim(ylim)

    if xlim and ylim:
        ax.grid(True, which="major", linestyle="-", alpha=0.4, color="#FFFFFF", linewidth=0.7)
        ax.grid(True, which="minor", linestyle=":", alpha=0.2, color="#FFFFFF", linewidth=0.3)
        ax.set_xlabel("经度 (WGS84)", fontsize=9, color="#444")
        ax.set_ylabel("纬度 (WGS84)", fontsize=9, color="#444")
        N = 5
        x_fracs = np.linspace(0, 1, N)
        x_ticks = [xlim[0] + f * (xlim[1] - xlim[0]) for f in x_fracs]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f"{v:.3f}°" for v in x_ticks], fontsize=7.5, color="#555")
        y_fracs = np.linspace(0, 1, N)
        y_ticks = [ylim[0] + f * (ylim[1] - ylim[0]) for f in y_fracs]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([f"{v:.3f}°" for v in y_ticks], fontsize=7.5, color="#555")

    if not isochrone_gdf.empty:
        isochrone_gdf.plot(ax=ax, color="#4A90E2", alpha=0.38,
                           edgecolor="#1A5EB8", linewidth=2, label="等时圈范围", zorder=2)

    if not point_gdf.empty:
        point_gdf.plot(ax=ax, color="#E74C3C", markersize=130, marker="*",
                       edgecolor="white", linewidth=1.8, zorder=5, label="起点")
        pt = point_gdf.geometry.iloc[0]
        ax.annotate(
            f"{address_name}\n({pt.x:.5f}, {pt.y:.5f})",
            xy=(pt.x, pt.y), xytext=(10, 10),
            textcoords="offset points", fontsize=9, color="#1A1A1A",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      alpha=0.88, edgecolor="#AAA"), zorder=6)

    ax.set_title(f"等时圈预览 — {address_name}\n{mode_cn} {minutes}分钟",
                 fontsize=13, fontweight="bold", color="#222")
    ax.set_aspect("equal")
    plt.tight_layout()
    png_tmp = output_path + "_tmp.png"
    plt.savefig(png_tmp, dpi=80, bbox_inches="tight", format="png")
    plt.close()
    img = Image.open(png_tmp).convert("RGB")
    img.save(output_path, "JPEG", quality=75, optimize=True)
    __import__("os").remove(png_tmp)
    size_kb = __import__("os").path.getsize(output_path) // 1024
    print(f"  ✓ 已保存预览图（简洁WGS84网格背景，{size_kb}KB）: {output_path}")

    """
    生成等时圈预览图：
    - 有 WGS84 底图（推荐）：ESRI 卫星影像重投影 + 等时圈(WGS84)，完美匹配
    - 有 PNG 底图（旧）：EPSG:3857 底图 + 等时圈(3857)，手动轴标签修正
    - 无底图：纯 matplotlib（WGS84 坐标）
    等时圈透明度: alpha=0.35（面）
    """
    fig, ax = plt.subplots(figsize=(10, 9))

    mode_labels = {"driving": "驾车", "walking": "步行", "cycling": "骑行"}
    mode_cn = mode_labels.get(mode, mode)

    # isochrone extent（WGS84）
    if not isochrone_gdf.empty:
        bounds_wgs = isochrone_gdf.total_bounds  # [minx, miny, maxx, maxy]
    else:
        bounds_wgs = None


# [ORPHANED OLD CODE REMOVED]

def main():
    if len(sys.argv) < 6:
        print("用法: python generate_isochrone.py <地址> <百度AK> <MapboxAK> <出行模式> <时间(分钟)> [输出目录]")
        sys.exit(1)

    address = sys.argv[1]
    baidu_ak = sys.argv[2]
    mapbox_ak = sys.argv[3]
    mode = sys.argv[4].lower()
    minutes = int(sys.argv[5])
    output_dir = sys.argv[6] if len(sys.argv) > 6 else "/root/.openclaw/workspace/isochrone_output"

    if mode not in ("driving", "walking", "cycling"):
        raise ValueError("出行模式仅支持: driving / walking / cycling")

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"等时圈生成器")
    print(f"{'='*50}")
    print(f"地址: {address}")
    print(f"出行模式: {mode} / {minutes}分钟")
    print(f"输出目录: {output_dir}")

    # Step 1: 百度地理编码 (BD-09)
    print(f"\n[Step 1] 百度地理编码...")
    bd_lng, bd_lat, precise, confidence = geocode_baidu(address, baidu_ak)
    print(f"  BD-09 坐标: ({bd_lng:.6f}, {bd_lat:.6f})")
    print(f"  精确度: {precise} | 置信度: {confidence}")

    # Step 2: BD-09 → WGS84
    print(f"\n[Step 2] 坐标转换 (BD-09 → WGS84)...")
    wgs_lng, wgs_lat = bd09_to_wgs84(bd_lng, bd_lat)
    print(f"  WGS84 坐标: ({wgs_lng:.6f}, {wgs_lat:.6f})")

    # Step 3: Mapbox 等时圈
    print(f"\n[Step 3] 请求 Mapbox 等时圈...")
    isochrone_geojson = get_mapbox_isochrone(wgs_lng, wgs_lat, mapbox_ak, mode, minutes)
    feature_count = len(isochrone_geojson.get("features", []))
    print(f"  等时圈面数量: {feature_count}")

    # Step 4: 保存 Shapefile
    print(f"\n[Step 4] 保存 Shapefile...")

    point_gdf = gpd.GeoDataFrame(
        {"name": [address], "lat_wgs": [wgs_lat], "lng_wgs": [wgs_lng],
         "lat_bd": [bd_lat], "lng_bd": [bd_lng]},
        geometry=[Point(wgs_lng, wgs_lat)],
        crs="EPSG:4326"
    )
    point_shp = os.path.join(output_dir, "point.shp")
    save_shapefile(point_gdf, point_shp)

    isochrone_gdf = gpd.GeoDataFrame.from_features(isochrone_geojson["features"], crs="EPSG:4326")
    if "isochrone" in isochrone_gdf.columns:
        isochrone_gdf = isochrone_gdf.rename(columns={"isochrone": "mode"})
    isochrone_gdf["mode"] = mode
    isochrone_gdf["minutes"] = minutes
    isochrone_shp = os.path.join(output_dir, "isochrone.shp")
    save_shapefile(isochrone_gdf, isochrone_shp)

    # Step 5: 获取 WGS84 底图（ESRI 卫星影像 → rasterio 重投影）
    bounds_wgs = tuple(isochrone_gdf.total_bounds) if not isochrone_gdf.empty else None
    base_map_path = os.path.join(output_dir, "base_map_wgs84.tif")
    wgs84_extent = None
    if bounds_wgs is not None:
        print(f"\n[Step 5] 获取 WGS84 底图（ESRI 影像 → 重投影）...")
        try:
            result = fetch_esri_tiles_and_reproject_wgs84(bounds_wgs, base_map_path, n_tiles_target=4)
            base_map_path, wgs84_extent = result
        except Exception as e:
            print(f"  ⚠ WGS84 底图获取失败: {e}，将不使用底图")
            base_map_path = None
    else:
        base_map_path = None

    # Step 6: 生成预览图
    print(f"\n[Step 6] 生成预览图...")
    preview_path = os.path.join(output_dir, "isochrone_preview.jpg")
    generate_preview(
        point_gdf, isochrone_gdf, address, mode, minutes,
        preview_path, mapbox_ak=mapbox_ak, base_map_path=base_map_path,
        wgs84_extent=wgs84_extent
    )

    # 结果汇总
    print(f"\n{'='*50}")
    print(f"生成完成！")
    print(f"  起点 SHP: {point_shp}")
    print(f"  等时圈 SHP: {isochrone_shp}")
    print(f"  预览图: {preview_path}")
    print(f"{'='*50}\n")

    print("RESULT_JSON:")
    print(json.dumps({
        "address": address,
        "bd09": {"lng": bd_lng, "lat": bd_lat},
        "wgs84": {"lng": wgs_lng, "lat": wgs_lat},
        "mode": mode,
        "minutes": minutes,
        "output_dir": output_dir,
        "files": {
            "point_shp": point_shp,
            "isochrone_shp": isochrone_shp,
            "preview_png": preview_path,
        }
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
