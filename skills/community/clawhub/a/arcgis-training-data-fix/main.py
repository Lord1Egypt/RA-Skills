"""
ArcGIS Pro 训练数据补全脚本 v2.0
通用版本：支持9种元数据格式 × 4种图像格式

元数据格式：
  1. PASCAL_VOC_rectangles (已验证)
  2. KITTI_rectangles
  3. Classified_Tiles
  4. RCNN_Masks (已验证)
  5. Labeled_Tiles
  6. MultiLabeled_Tiles
  7. Exported_Tiles
  8. CycleGAN
  9. Imagenet

图像格式：TIFF(.tif/.tiff)、MRF(.mrf)、JPG(.jpg/.jpeg)、PNG(.png)

用法: python main.py <训练数据目录路径>
例如: python main.py "D:\Deeplearn\Vehicle\sample"
"""

import os
import sys
import json
import struct
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET

# ============================================================
# 支持的图像扩展名
# ============================================================
IMG_EXTS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.mrf'}
WORLD_FILE_MAP = {
    '.jpg': '.jgw', '.jpeg': '.jgw',
    '.png': '.pgw',
    '.tif': '.tfw', '.tiff': '.tfw',
    '.mrf': '.mrfw',
}

# ============================================================
# 元数据格式常量
# ============================================================
FORMAT_PASCAL_VOC = "PASCAL_VOC_rectangles"
FORMAT_KITTI = "KITTI_rectangles"
FORMAT_CLASSIFIED_TILES = "Classified_Tiles"
FORMAT_RCNN_MASKS = "RCNN_Masks"
FORMAT_LABELED_TILES = "Labeled_Tiles"
FORMAT_MULTI_LABELED_TILES = "MultiLabeled_Tiles"
FORMAT_EXPORTED_TILES = "Exported_Tiles"
FORMAT_CYCLEGAN = "CycleGAN"
FORMAT_IMAGENET = "Imagenet"

# 矢量标注格式（有xml/txt标注文件）
VECTOR_FORMATS = {FORMAT_PASCAL_VOC, FORMAT_KITTI}
# 栅格标签格式（标签是tif）
RASTER_TILE_FORMATS = {
    FORMAT_CLASSIFIED_TILES, FORMAT_RCNN_MASKS,
    FORMAT_LABELED_TILES, FORMAT_MULTI_LABELED_TILES, FORMAT_EXPORTED_TILES
}


# ============================================================
# 格式检测
# ============================================================
def detect_format(base):
    """自动检测元数据格式"""
    img_dir = os.path.join(base, "images")
    lbl_dir = os.path.join(base, "labels")

    # 检查 CycleGAN 结构：images/A/ + images/B/
    if os.path.isdir(os.path.join(img_dir, "A")) and os.path.isdir(os.path.join(img_dir, "B")):
        return FORMAT_CYCLEGAN

    if not os.path.isdir(lbl_dir):
        # 无labels目录，可能是CycleGAN或纯影像
        return FORMAT_CYCLEGAN

    lbl_entries = os.listdir(lbl_dir)

    # 检查是否有 xml 文件 → PASCAL_VOC
    xml_files = [f for f in lbl_entries if f.lower().endswith('.xml')]
    if xml_files:
        return FORMAT_PASCAL_VOC

    # 检查是否有 txt 文件（KITTI格式）
    txt_files = [f for f in lbl_entries if f.lower().endswith('.txt')]
    if txt_files:
        # 确认是KITTI格式（每行有 class x y x y 数据）
        sample_path = os.path.join(lbl_dir, txt_files[0])
        try:
            with open(sample_path, 'r') as f:
                first_line = f.readline().strip()
            parts = first_line.split()
            if len(parts) >= 5:
                # 尝试判断是否是bounding box格式
                float(parts[-4])
                return FORMAT_KITTI
        except (ValueError, IndexError):
            pass

    # 检查子目录结构
    subdirs = [d for d in lbl_entries if os.path.isdir(os.path.join(lbl_dir, d))]

    if subdirs:
        # 有子目录 → 可能是 Classified_Tiles 或 Imagenet
        # 检查子目录中的文件类型
        first_subdir = os.path.join(lbl_dir, subdirs[0])
        subdir_files = os.listdir(first_subdir)
        subdir_img_exts = {os.path.splitext(f)[1].lower() for f in subdir_files if os.path.isfile(os.path.join(first_subdir, f))}

        # 如果子目录中是 tif 文件 → Classified_Tiles
        if '.tif' in subdir_img_exts or '.tiff' in subdir_img_exts:
            return FORMAT_CLASSIFIED_TILES

        # 如果子目录中是 jpg/png → Imagenet（图像分类）
        if subdir_img_exts & {'.jpg', '.jpeg', '.png'}:
            return FORMAT_IMAGENET

    # 检查标签tif文件
    lbl_tifs = [f for f in lbl_entries if f.lower().endswith(('.tif', '.tiff'))]
    if lbl_tifs:
        # 分析标签像素值来判断格式
        sample_label = os.path.join(lbl_dir, lbl_tifs[0])
        try:
            from osgeo import gdal
            ds = gdal.Open(sample_label)
            if ds:
                band = ds.GetRasterBand(1)
                stats = band.GetStatistics(True, True)
                arr = band.ReadAsArray()
                ds = None

                unique_vals = np.unique(arr)
                n_unique = len(unique_vals)

                if n_unique <= 2:
                    # 只有0和另一个值 → RCNN_Masks（二值掩膜）
                    return FORMAT_RCNN_MASKS
                elif n_unique <= 50:
                    # 少量唯一值 → 可能是 Classified_Tiles 或 Labeled_Tiles
                    return FORMAT_CLASSIFIED_TILES
                else:
                    # 多唯一值 → 可能是 MultiLabeled_Tiles 或 Exported_Tiles
                    return FORMAT_LABELED_TILES
        except ImportError:
            # 没有GDAL，用PIL读取
            img = Image.open(sample_label)
            arr = np.array(img)
            unique_vals = np.unique(arr)
            if len(unique_vals) <= 2:
                return FORMAT_RCNN_MASKS
            else:
                return FORMAT_CLASSIFIED_TILES

    # 默认
    return FORMAT_PASCAL_VOC


# ============================================================
# 影像扫描
# ============================================================
def get_image_files(img_dir):
    """获取影像文件列表"""
    if not os.path.isdir(img_dir):
        return []
    return sorted([
        f for f in os.listdir(img_dir)
        if os.path.splitext(f)[1].lower() in IMG_EXTS
    ])


def compute_band_stats(img_dir, img_files, max_samples=200):
    """扫描影像计算波段统计（最多采样max_samples张）"""
    # 如果影像太多，采样计算
    if len(img_files) > max_samples:
        indices = np.linspace(0, len(img_files) - 1, max_samples, dtype=int)
        sample_files = [img_files[i] for i in indices]
    else:
        sample_files = img_files

    try:
        from osgeo import gdal
        use_gdal = True
    except ImportError:
        use_gdal = False

    n_pixels = 0
    sum_vals = None
    sum_sq = None
    global_min = None
    global_max = None
    img_h, img_w, n_bands = 0, 0, 0

    for img_file in sample_files:
        img_path = os.path.join(img_dir, img_file)

        if use_gdal:
            try:
                ds = gdal.Open(img_path)
                if ds is None:
                    continue
                n_bands_file = ds.RasterCount
                w, h = ds.RasterXSize, ds.RasterYSize

                if n_bands_file == 1:
                    band_data = ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
                    img_arr = band_data.reshape(h, w, 1)
                else:
                    # 读取前3个波段
                    bands = []
                    for b in range(min(n_bands_file, 3)):
                        bands.append(ds.GetRasterBand(b + 1).ReadAsArray())
                    img_arr = np.stack(bands, axis=-1).astype(np.float64)
                ds = None
            except Exception:
                continue
        else:
            try:
                img = np.array(Image.open(img_path), dtype=np.float64)
                if img.ndim == 2:
                    img_arr = img.reshape(img.shape[0], img.shape[1], 1)
                else:
                    img_arr = img[:, :, :3]
                h, w = img_arr.shape[:2]
            except Exception:
                continue

        if sum_vals is None:
            n_bands = img_arr.shape[2]
            sum_vals = np.zeros(n_bands, dtype=np.float64)
            sum_sq = np.zeros(n_bands, dtype=np.float64)
            global_min = np.full(n_bands, np.inf)
            global_max = np.full(n_bands, -np.inf)
            img_h, img_w = h, w

        for b in range(min(n_bands, img_arr.shape[2])):
            band_data = img_arr[:, :, b].flatten()
            valid = np.isfinite(band_data)
            if valid.any():
                band_data = band_data[valid]
                global_min[b] = min(global_min[b], float(band_data.min()))
                global_max[b] = max(global_max[b], float(band_data.max()))
                sum_vals[b] += float(band_data.sum())
                sum_sq[b] += float((band_data ** 2).sum())
                n_pixels += len(band_data)

    if n_pixels == 0:
        return {
            'height': 256, 'width': 256, 'n_bands': 3,
            'mins': np.array([0, 0, 0]), 'maxs': np.array([255, 255, 255]),
            'means': np.array([128.0, 128.0, 128.0]),
            'stds': np.array([50.0, 50.0, 50.0])
        }

    # 修复 inf
    for b in range(n_bands):
        if np.isinf(global_min[b]):
            global_min[b] = 0
        if np.isinf(global_max[b]):
            global_max[b] = 255

    band_means = sum_vals / n_pixels
    band_vars = sum_sq / n_pixels - band_means ** 2
    band_stds = np.sqrt(np.maximum(band_vars, 0))

    return {
        'height': img_h, 'width': img_w, 'n_bands': n_bands,
        'mins': global_min, 'maxs': global_max,
        'means': band_means, 'stds': band_stds,
        'total_images': len(img_files)
    }


def get_cell_size(img_dir, img_files):
    """从坐标文件获取像素大小和空间参考"""
    try:
        from osgeo import gdal
        for img_file in img_files[:5]:
            ds = gdal.Open(os.path.join(img_dir, img_file))
            if ds:
                gt = ds.GetGeoTransform()
                cell_x = abs(gt[1])
                cell_y = abs(gt[5])
                srs = ds.GetSpatialRef()
                wkid = 4490  # 默认
                if srs:
                    code = srs.GetAuthorityCode(None)
                    if code:
                        wkid = int(code)
                ds = None
                if cell_x > 0:
                    return round(cell_x, 10), round(cell_y, 10), wkid
    except ImportError:
        pass

    # 从 world file 读取
    for img_file in img_files:
        ext = os.path.splitext(img_file)[1].lower()
        wf_ext = WORLD_FILE_MAP.get(ext, '.jgw')
        wf_path = os.path.join(img_dir, os.path.splitext(img_file)[0] + wf_ext)
        if os.path.exists(wf_path):
            with open(wf_path, 'r') as f:
                lines = f.readlines()
            cell_x = abs(float(lines[0].strip()))
            cell_y = abs(float(lines[3].strip()))
            return cell_x, cell_y, 4490

    return 0.2, 0.2, 4490


# ============================================================
# 标签解析 - 矢量格式
# ============================================================
def parse_pascal_voc(lbl_dir):
    """解析PASCAL VOC格式标签"""
    lbl_files = sorted([f for f in os.listdir(lbl_dir) if f.lower().endswith('.xml')])
    class_stats = {}
    mapping = {}
    features_per_image = []

    for lbl_file in lbl_files:
        stem = os.path.splitext(lbl_file)[0]
        tree = ET.parse(os.path.join(lbl_dir, lbl_file))
        root = tree.getroot()
        n_objs = 0

        for obj in root.findall('object'):
            name = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)
            area = (xmax - xmin) * (ymax - ymin)

            if name not in class_stats:
                class_stats[name] = {"count": 0, "img_set": set(), "areas": []}
            class_stats[name]["count"] += 1
            class_stats[name]["img_set"].add(stem)
            class_stats[name]["areas"].append(area)
            n_objs += 1

        features_per_image.append(n_objs)
        mapping[stem] = lbl_file

    return class_stats, features_per_image, mapping


def parse_kitti(lbl_dir):
    """解析KITTI格式标签"""
    lbl_files = sorted([f for f in os.listdir(lbl_dir) if f.lower().endswith('.txt')])
    class_stats = {}
    mapping = {}
    features_per_image = []

    for lbl_file in lbl_files:
        stem = os.path.splitext(lbl_file)[0]
        n_objs = 0

        with open(os.path.join(lbl_dir, lbl_file), 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 8:
                    name = parts[0]
                    try:
                        xmin, ymin, xmax, ymax = float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7])
                        area = (xmax - xmin) * (ymax - ymin)
                    except (ValueError, IndexError):
                        continue

                    if name not in class_stats:
                        class_stats[name] = {"count": 0, "img_set": set(), "areas": []}
                    class_stats[name]["count"] += 1
                    class_stats[name]["img_set"].add(stem)
                    class_stats[name]["areas"].append(area)
                    n_objs += 1

        features_per_image.append(n_objs)
        mapping[stem] = lbl_file

    return class_stats, features_per_image, mapping


# ============================================================
# 标签解析 - 栅格格式
# ============================================================
def parse_raster_labels(lbl_dir, label_format):
    """解析栅格标签格式（Classified_Tiles, RCNN_Masks, Labeled_Tiles等）"""
    class_stats = {}
    mapping = {}
    features_per_image = []
    label_classes = {}

    # 检测目录结构
    subdirs = [d for d in os.listdir(lbl_dir) if os.path.isdir(os.path.join(lbl_dir, d))]

    if subdirs:
        # 有子目录 → Classified_Tiles（子目录=类别名）
        for cls_name in subdirs:
            cls_dir = os.path.join(lbl_dir, cls_name)
            cls_files = sorted([
                f for f in os.listdir(cls_dir)
                if os.path.splitext(f)[1].lower() in ('.tif', '.tiff')
                and not f.endswith('.aux.xml')
            ])
            label_classes[cls_name] = cls_files
            class_stats[cls_name] = {
                "count": len(cls_files),
                "img_set": set(),
                "areas": [256 * 256] * len(cls_files)  # 近似
            }

        # 建立mapping：找到每张图片对应的标签
        for cls_name, files in label_classes.items():
            for f in files:
                stem = os.path.splitext(f)[0]
                if stem not in mapping:
                    mapping[stem] = []
                mapping[stem].append(f"labels/{cls_name}/{f}")
                class_stats[cls_name]["img_set"].add(stem)

    else:
        # 无子目录 → 平铺的tif标签
        lbl_tifs = sorted([
            f for f in os.listdir(lbl_dir)
            if os.path.splitext(f)[1].lower() in ('.tif', '.tiff')
            and not f.endswith('.aux.xml')
        ])

        # 扫描唯一像素值来确定类别
        all_unique = set()
        for f in lbl_tifs[:min(20, len(lbl_tifs))]:
            try:
                img = Image.open(os.path.join(lbl_dir, f))
                arr = np.array(img)
                unique_vals = np.unique(arr)
                for v in unique_vals:
                    if v > 0:  # 跳过背景
                        all_unique.add(int(v))
            except Exception:
                continue

        # 分配类别名
        sorted_vals = sorted(all_unique)
        if not sorted_vals:
            sorted_vals = [1]

        for v in sorted_vals:
            cls_name = f"Class_{v}"
            class_stats[cls_name] = {"count": 0, "img_set": set(), "areas": [256 * 256]}

        # 建立mapping
        for f in lbl_tifs:
            stem = os.path.splitext(f)[0]
            mapping[stem] = [f"labels/{f}"]

            # 统计每个类别的标注数
            try:
                img = Image.open(os.path.join(lbl_dir, f))
                arr = np.array(img)
                unique_vals = np.unique(arr)
                for v in unique_vals:
                    if v > 0:
                        cls_name = f"Class_{int(v)}"
                        if cls_name in class_stats:
                            class_stats[cls_name]["count"] += 1
                            class_stats[cls_name]["img_set"].add(stem)
            except Exception:
                pass

        features_per_image = [1] * len(lbl_tifs)
        return class_stats, features_per_image, mapping

    # 对于有子目录的格式，features_per_image按图片统计
    if subdirs:
        all_stems = set()
        for cls_info in class_stats.values():
            all_stems.update(cls_info["img_set"])
        features_per_image = [1] * len(all_stems)

    return class_stats, features_per_image, mapping


def parse_imagenet(lbl_dir):
    """解析Imagenet格式（labels/类别名/*.jpg|png）"""
    class_stats = {}
    mapping = {}
    features_per_image = []
    subdirs = [d for d in os.listdir(lbl_dir) if os.path.isdir(os.path.join(lbl_dir, d))]

    for cls_name in subdirs:
        cls_dir = os.path.join(lbl_dir, cls_name)
        cls_files = sorted([
            f for f in os.listdir(cls_dir)
            if os.path.splitext(f)[1].lower() in IMG_EXTS
        ])
        class_stats[cls_name] = {
            "count": len(cls_files),
            "img_set": set(os.path.splitext(f)[0] for f in cls_files),
            "areas": [0]  # Imagenet格式无面积概念
        }
        for f in cls_files:
            stem = os.path.splitext(f)[0]
            mapping[stem] = f"labels/{cls_name}/{f}"

    features_per_image = [1] * sum(cs["count"] for cs in class_stats.values())
    return class_stats, features_per_image, mapping


def parse_cyclegan(base):
    """解析CycleGAN格式（images/A/ + images/B/）"""
    img_a_dir = os.path.join(base, "images", "A")
    img_b_dir = os.path.join(base, "images", "B")

    files_a = get_image_files(img_a_dir)
    files_b = get_image_files(img_b_dir)

    class_stats = {
        "domain_A": {"count": len(files_a), "img_set": set(os.path.splitext(f)[0] for f in files_a), "areas": [0]},
        "domain_B": {"count": len(files_b), "img_set": set(os.path.splitext(f)[0] for f in files_b), "areas": [0]}
    }
    features_per_image = [1] * max(len(files_a), len(files_b))
    mapping = {}
    for f in files_a:
        stem = os.path.splitext(f)[0]
        mapping[stem] = f"images/B/{f}"

    return class_stats, features_per_image, mapping


# ============================================================
# 文件生成
# ============================================================
def generate_map_txt(base, img_dir, img_files, label_format, mapping):
    """生成map.txt"""
    map_path = os.path.join(base, "map.txt")

    with open(map_path, 'w', encoding='utf-8') as f:
        if label_format == FORMAT_CYCLEGAN:
            for img_file in img_files:
                stem = os.path.splitext(img_file)[0]
                # CycleGAN: images/A/xxx → images/B/xxx
                target = os.path.join("images", "B", img_file)
                source = os.path.join("images", "A", img_file)
                f.write(f"{source} {target}\n")
        else:
            for img_file in img_files:
                stem = os.path.splitext(img_file)[0]
                if stem in mapping:
                    lbl = mapping[stem]
                    if isinstance(lbl, list):
                        lbl_str = " ".join(lbl)
                    else:
                        lbl_str = lbl
                    f.write(f"images/{img_file} {lbl_str}\n")

    return map_path


def generate_emd(base, stats, class_stats, label_format, cell_x, cell_y, wkid, img_files):
    """生成esri_model_definition.emd"""
    emd_path = os.path.join(base, "esri_model_definition.emd")

    classes = []
    for i, cls_name in enumerate(sorted(class_stats.keys())):
        classes.append({
            "Value": i + 1,
            "Name": cls_name,
            "Color": [0, 0, 0]
        })

    all_tiles_stats = []
    for b in range(stats['n_bands']):
        all_tiles_stats.append({
            "Min": round(float(stats['mins'][b]), 2),
            "Max": round(float(stats['maxs'][b]), 2),
            "Mean": round(float(stats['means'][b]), 2),
            "StdDev": round(float(stats['stds'][b]), 2)
        })

    band_names = [f"Band_{i+1}" for i in range(stats['n_bands'])]

    emd = {
        "ImageHeight": stats['height'],
        "ImageWidth": stats['width'],
        "MetaDataMode": label_format,
        "BlackenAroundFeature": False,
        "IsMultidimensional": False,
        "CropTileMode": "Fixed size",
        "MinCellSize": {
            "x": cell_x, "y": cell_y,
            "spatialReference": {"wkid": wkid, "latestWkid": wkid}
        },
        "MaxCellSize": {
            "x": cell_x, "y": cell_y,
            "spatialReference": {"wkid": wkid, "latestWkid": wkid}
        },
        "ImageSpaceUsed": "MAP_SPACE",
        "Classes": classes,
        "InputRastersProps": {
            "RasterCount": len(img_files),
            "SensorName": "",
            "BandNames": band_names
        },
        "AllTilesStats": all_tiles_stats,
        "ExtractBands": list(range(stats['n_bands']))
    }

    with open(emd_path, 'w', encoding='utf-8') as f:
        json.dump(emd, f, indent=4, ensure_ascii=False)

    return emd_path


def generate_accumulated_stats(base, stats, class_stats, features_per_image, label_format, cell_x, cell_y, wkid, img_files):
    """生成esri_accumulated_stats.json"""
    json_path = os.path.join(base, "esri_accumulated_stats.json")

    classes = []
    for i, cls_name in enumerate(sorted(class_stats.keys())):
        classes.append({"Value": i + 1, "Name": cls_name, "Color": [0, 0, 0]})

    band_stats_state = []
    for b in range(stats['n_bands']):
        band_stats_state.append({
            "Min": round(float(stats['mins'][b]), 2),
            "Max": round(float(stats['maxs'][b]), 2),
            "Mean": round(float(stats['means'][b]), 2),
            "StdDev": round(float(stats['stds'][b]), 2)
        })

    band_names = [f"Band_{i+1}" for i in range(stats['n_bands'])]

    total_tiles = len(img_files)

    # FeatureStats
    total_objects = sum(cs["count"] for cs in class_stats.values())
    num_features_per_class = {}
    num_images_per_class = {}
    feature_area_per_class = {}
    for i, cls_name in enumerate(sorted(class_stats.keys())):
        key = i + 1
        cs = class_stats[cls_name]
        num_features_per_class[key] = cs["count"]
        num_images_per_class[key] = len(cs["img_set"])
        if cs["areas"] and cs["areas"][0] > 0:
            areas = cs["areas"]
            feature_area_per_class[key] = {
                "min": round(min(areas), 2),
                "max": round(max(areas), 2),
                "avg": round(float(np.mean(areas)), 2),
                "sum": round(sum(areas), 2),
                "count": len(areas)
            }

    fpia = np.array(features_per_image) if features_per_image else np.array([0])

    accumulated_stats = {
        "Version": "3.0",
        "MetaDataMode": label_format,
        "FeatureStats": {
            "NumImagesTotal": total_tiles,
            "NumFeaturesTotal": total_objects,
            "NumImagesPerClass": num_images_per_class,
            "NumFeaturesPerClass": num_features_per_class,
            "NumFeaturesPerImage": {
                "min": int(fpia.min()) if len(fpia) > 0 else 0,
                "max": int(fpia.max()) if len(fpia) > 0 else 0,
                "avg": round(float(fpia.mean()), 2) if len(fpia) > 0 else 0,
                "sum": int(fpia.sum()) if len(fpia) > 0 else 0,
                "count": len(fpia)
            },
            "FeatureAreaPerClass": feature_area_per_class
        },
        "BandStatsState": band_stats_state,
        # Pro validate.py 需要的额外字段
        "NumBands": stats['n_bands'],
        "TileHeight": stats['height'],
        "TileWidth": stats['width'],
        "TotalTiles": total_tiles,
        "EmptyTiles": 0,
        "ImageHeight": stats['height'],
        "ImageWidth": stats['width'],
        "TileSizeX": stats['width'],
        "TileSizeY": stats['height'],
        "NumClasses": len(class_stats),
        "CellSizeX": cell_x,
        "CellSizeY": cell_y,
        "InputRastersProps": {
            "RasterCount": len(img_files),
            "SensorName": "",
            "BandNames": band_names
        }
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(accumulated_stats, f, indent=4, ensure_ascii=False)

    return json_path


def generate_stats_txt(base, stats, class_stats, features_per_image, label_format):
    """生成stats.txt"""
    stats_path = os.path.join(base, "stats.txt")

    total_objects = sum(cs["count"] for cs in class_stats.values())
    fpia = np.array(features_per_image) if features_per_image else np.array([0])

    lines = []
    lines.append(f"images: {stats.get('total_images', len(features_per_image))}, bands: {stats['n_bands']}, width: {stats['width']}, height: {stats['height']}")
    lines.append(f"features: {total_objects}")
    if len(fpia) > 0 and fpia.sum() > 0:
        lines.append(f"features per image: min={int(fpia.min())}, avg={round(float(fpia.mean()), 2)}, max={int(fpia.max())}")
    lines.append(f"classes: {len(class_stats)}")

    for i, cls_name in enumerate(sorted(class_stats.keys())):
        cs = class_stats[cls_name]
        if cs["areas"] and cs["areas"][0] > 0:
            areas = cs["areas"]
            lines.append(
                f"class: {cls_name}, images: {len(cs['img_set'])}, "
                f"features: {cs['count']}, "
                f"min_size: {round(min(areas), 2)}, "
                f"avg_size: {round(float(np.mean(areas)), 2)}, "
                f"max_size: {round(max(areas), 2)}"
            )
        else:
            lines.append(f"class: {cls_name}, images: {len(cs['img_set'])}, features: {cs['count']}")

    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")

    return stats_path


# ============================================================
# 主流程
# ============================================================
def main():
    if len(sys.argv) < 2:
        print("用法: python main.py <训练数据目录路径>")
        print('例如: python main.py "D:\\Deeplearn\\Vehicle\\sample"')
        sys.exit(1)

    base = sys.argv[1]
    if not os.path.isdir(base):
        print(f"错误: 目录不存在 - {base}")
        sys.exit(1)

    img_dir = os.path.join(base, "images")
    lbl_dir = os.path.join(base, "labels")

    # CycleGAN 特殊处理
    is_cyclegan = os.path.isdir(os.path.join(img_dir, "A")) and os.path.isdir(os.path.join(img_dir, "B"))

    if not is_cyclegan:
        if not os.path.isdir(img_dir):
            print(f"错误: images/ 目录不存在")
            sys.exit(1)

    print("=" * 50)
    print("ArcGIS Pro 训练数据补全 v2.0 (通用版)")
    print("=" * 50)
    print(f"目录: {base}")

    # 1. 检测格式
    print("\n[1/8] 检测元数据格式...")
    label_format = detect_format(base)
    print(f"  检测到格式: {label_format}")

    # 2. 扫描影像
    print("\n[2/8] 扫描影像文件...")
    if is_cyclegan:
        img_files_a = get_image_files(os.path.join(img_dir, "A"))
        img_files_b = get_image_files(os.path.join(img_dir, "B"))
        img_files = img_files_a
        print(f"  Domain A: {len(img_files_a)} 张, Domain B: {len(img_files_b)} 张")
    else:
        img_files = get_image_files(img_dir)
        print(f"  找到 {len(img_files)} 个影像文件")
        # 统计图像格式
        exts = {}
        for f in img_files:
            ext = os.path.splitext(f)[1].lower()
            exts[ext] = exts.get(ext, 0) + 1
        print(f"  格式: {exts}")

    if not img_files:
        print("错误: 未找到任何影像文件")
        sys.exit(1)

    # 3. 计算波段统计
    print("\n[3/8] 计算波段统计...")
    if is_cyclegan:
        scan_dir = os.path.join(img_dir, "A")
    else:
        scan_dir = img_dir
    stats = compute_band_stats(scan_dir, img_files)
    stats['total_images'] = len(img_files)
    print(f"  尺寸: {stats['width']}x{stats['height']}, 波段: {stats['n_bands']}")
    for b in range(stats['n_bands']):
        print(f"  Band {b+1}: Min={stats['mins'][b]:.2f}, Max={stats['maxs'][b]:.2f}, "
              f"Mean={stats['means'][b]:.2f}, StdDev={stats['stds'][b]:.2f}")

    # 4. 解析标签
    print("\n[4/8] 解析标签...")
    if label_format == FORMAT_PASCAL_VOC:
        class_stats, features_per_image, mapping = parse_pascal_voc(lbl_dir)
    elif label_format == FORMAT_KITTI:
        class_stats, features_per_image, mapping = parse_kitti(lbl_dir)
    elif label_format == FORMAT_IMAGENET:
        class_stats, features_per_image, mapping = parse_imagenet(lbl_dir)
    elif label_format == FORMAT_CYCLEGAN:
        class_stats, features_per_image, mapping = parse_cyclegan(base)
    elif label_format in RASTER_TILE_FORMATS:
        class_stats, features_per_image, mapping = parse_raster_labels(lbl_dir, label_format)
    else:
        class_stats, features_per_image, mapping = {}, [], {}

    total_objects = sum(cs["count"] for cs in class_stats.values())
    class_names = sorted(class_stats.keys())
    print(f"  类别: {class_names}")
    print(f"  总标注对象: {total_objects}")
    for cls in class_names:
        cs = class_stats[cls]
        print(f"  {cls}: {cs['count']} objects in {len(cs['img_set'])} images")

    # 5. 获取坐标信息
    print("\n[5/8] 获取坐标信息...")
    cell_x, cell_y, wkid = get_cell_size(scan_dir, img_files)
    print(f"  像素大小: {cell_x} x {cell_y}, WKID: {wkid}")

    # 6. 生成文件
    print("\n[6/8] 生成标准文件...")

    map_path = generate_map_txt(base, scan_dir, img_files, label_format, mapping)
    print(f"  [OK] map.txt")

    emd_path = generate_emd(base, stats, class_stats, label_format, cell_x, cell_y, wkid, img_files)
    print(f"  [OK] esri_model_definition.emd")

    json_path = generate_accumulated_stats(base, stats, class_stats, features_per_image, label_format, cell_x, cell_y, wkid, img_files)
    print(f"  [OK] esri_accumulated_stats.json")

    stats_path = generate_stats_txt(base, stats, class_stats, features_per_image, label_format)
    print(f"  [OK] stats.txt")

    # 7. 清理旧文件
    print("\n[7/8] 清理非标准命名文件...")
    removed = []
    for f in os.listdir(base):
        fp = os.path.join(base, f)
        if not os.path.isfile(fp):
            continue
        if f.endswith('.emd') and f != 'esri_model_definition.emd':
            os.remove(fp)
            removed.append(f)
        elif f.endswith('.json') and f != 'esri_accumulated_stats.json':
            os.remove(fp)
            removed.append(f)
    if removed:
        for f in removed:
            print(f"  删除: {f}")
    else:
        print("  无需清理")

    # 8. 验证
    print("\n[8/8] 最终验证 ===")
    required_files = ["esri_model_definition.emd", "esri_accumulated_stats.json", "map.txt", "stats.txt"]
    all_ok = True
    for f in sorted(os.listdir(base)):
        fp = os.path.join(base, f)
        if os.path.isfile(fp):
            is_required = f in required_files
            prefix = "[OK]" if is_required else "    "
            print(f"  {prefix} {f} ({os.path.getsize(fp)} bytes)")
            if is_required:
                required_files.remove(f)

    for f in required_files:
        print(f"  [MISSING] {f}")
        all_ok = False

    print(f"\n{'=' * 50}")
    if all_ok:
        print("补全完成!")
        print(f"  格式: {label_format}")
        print(f"  在Pro中使用:")
        print(f"    工具: Train Deep Learning Model")
        print(f"    Input Training Data: {base}")
    else:
        print("部分文件缺失，请检查错误信息")


if __name__ == "__main__":
    main()
