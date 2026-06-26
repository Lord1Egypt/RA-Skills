#!/usr/bin/env python3
"""
CAD DWG/DXF 图纸专业分析工具集

功能概览:
  info      - 获取图纸基本信息（版本、单位、实体数量等）
  layers    - 列出所有图层及其属性
  entities  - 列出模型空间中的实体（支持按图层/类型过滤）
  blocks    - 列出块定义表（图块模板）
  inserts   - 列出模型空间中的图块引用实例
  texts     - 提取图纸中的所有文本内容
  layer-content  - 提取指定图层上的所有实体详情
  spaces    - 查看空间布局系统（模型空间、布局空间）
  distance  - 计算两个实体之间的距离
  screenshot - 对指定实体/区域进行截图
  audit     - 图纸规范性审核（0层违规检查、图块图层归属分析）
  search    - 按名称/关键字搜索实体
  export-pdf - 将图纸导出为 PDF

依赖: ezdxf, matplotlib
可选依赖: QCAD dwg2bmp (截图功能), ODA File Converter (DWG 读取)

用法: python cad_tools.py <子命令> [参数]
"""

import argparse
import json
import math
import os
import subprocess
import sys
from typing import Optional

# ==================== 依赖检测与路径常量 ====================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(SCRIPT_DIR, "..")
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)
SETUP_MARKER = os.path.join(ASSETS_DIR, ".setup_done")


def _check_python_deps():
    """检查 Python 依赖是否已安装，缺失时给出明确提示但不自动安装"""
    missing = []
    for pkg in ("ezdxf", "matplotlib"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(json.dumps({
            "status": "error",
            "message": f"缺少必需的 Python 依赖: {', '.join(missing)}",
            "fix_command": f"pip install {' '.join(missing)}",
            "hint": "请手动安装后重试，或运行 setup 命令: python3 {} setup --confirm".format(
                os.path.join(SCRIPT_DIR, "cad_tools.py"))
        }, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


def _read_setup_config() -> dict:
    """读取 setup.sh 生成的配置标记文件"""
    config = {}
    if os.path.exists(SETUP_MARKER):
        with open(SETUP_MARKER, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, val = line.split("=", 1)
                    config[key] = val
    return config


# 检查 Python 依赖（仅检测，不自动安装）
_check_python_deps()

import ezdxf
from ezdxf.addons import odafc
from ezdxf.document import Drawing


# ==================== 通用工具函数 ====================

def _find_oda_wrapper() -> Optional[str]:
    """按优先级查找 ODA wrapper 脚本"""
    candidates = [
        os.path.join(ASSETS_DIR, "oda_wrapper.sh"),
    ]
    # 从 setup 配置中读取
    config = _read_setup_config()
    if config.get("oda_wrapper"):
        candidates.insert(0, config["oda_wrapper"])

    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def _find_qcad_tool(user_path: Optional[str] = None) -> Optional[str]:
    """按优先级查找 QCAD dwg2bmp 工具"""
    candidates = [
        user_path,
        os.environ.get("QCAD_DWG2BMP_PATH"),
    ]
    # 从 setup 配置中读取（skill 内置安装的 QCAD）
    config = _read_setup_config()
    if config.get("qcad_path"):
        candidates.append(config["qcad_path"])

    # 常见安装位置
    candidates.extend([
        os.path.join(ASSETS_DIR, "qcad", "dwg2bmp"),
        "/usr/local/bin/dwg2bmp",
        "/opt/qcad/dwg2bmp",
    ])

    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def _load_dwg(filepath: str) -> Drawing:
    """加载 DWG 或 DXF 文件，返回 ezdxf Document 对象"""
    if not os.path.exists(filepath):
        print(json.dumps({
            "status": "error",
            "message": f"文件不存在: {filepath}"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()

    # 自动配置 ODA wrapper
    oda_wrapper = _find_oda_wrapper()
    if oda_wrapper:
        ezdxf.options.oda_file_converter = oda_wrapper

    try:
        if ext == ".dwg":
            if not oda_wrapper:
                print(json.dumps({
                    "status": "error",
                    "message": "读取 DWG 文件需要 ODA File Converter，但未检测到。请运行环境配置: bash {}/setup.sh".format(SCRIPT_DIR),
                    "hint": "如果您有 ODA RPM 安装包，可以运行: bash {}/setup.sh --oda-rpm /path/to/ODA.rpm".format(SCRIPT_DIR)
                }, ensure_ascii=False), file=sys.stderr)
                sys.exit(1)
            doc = odafc.readfile(filepath)
        elif ext in (".dxf",):
            doc = ezdxf.readfile(filepath)
        else:
            print(json.dumps({
                "status": "error",
                "message": f"不支持的文件格式 '{ext}'，仅支持 .dwg 和 .dxf"
            }, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        return doc
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"加载文件失败: {str(e)}"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


UNIT_MAPPING = {
    0: "无单位 (Unitless)",
    1: "英寸 (Inches)",
    2: "英尺 (Feet)",
    4: "毫米 (Millimeters)",
    5: "厘米 (Centimeters)",
    6: "米 (Meters)",
    14: "分米 (Decimeters)",
}


def _get_unit_name(doc: Drawing) -> str:
    insunits = doc.header.get('$INSUNITS', 0)
    return UNIT_MAPPING.get(insunits, f"其他 (代码: {insunits})")


def _get_unit_code(doc: Drawing) -> int:
    return doc.header.get('$INSUNITS', 0)


def _entity_to_dict(entity, include_details=True) -> dict:
    """将实体转换为可序列化的字典"""
    result = {
        "type": entity.dxftype(),
        "layer": entity.dxf.layer,
        "handle": entity.dxf.handle,
    }

    if hasattr(entity.dxf, 'color'):
        result["color"] = entity.dxf.color

    etype = entity.dxftype()

    if etype == "INSERT":
        result["block_name"] = entity.dxf.name
        result["position"] = {
            "x": round(entity.dxf.insert.x, 4),
            "y": round(entity.dxf.insert.y, 4),
            "z": round(entity.dxf.insert.z, 4),
        }
        result["rotation"] = entity.dxf.rotation
        if hasattr(entity.dxf, 'xscale'):
            result["scale"] = {
                "x": entity.dxf.xscale,
                "y": entity.dxf.yscale,
                "z": getattr(entity.dxf, 'zscale', 1.0),
            }
        # 提取属性
        if entity.attribs:
            result["attributes"] = {
                attrib.dxf.tag: attrib.dxf.text for attrib in entity.attribs
            }

    elif etype == "LINE" and include_details:
        result["start"] = {
            "x": round(entity.dxf.start.x, 4),
            "y": round(entity.dxf.start.y, 4),
        }
        result["end"] = {
            "x": round(entity.dxf.end.x, 4),
            "y": round(entity.dxf.end.y, 4),
        }
        result["length"] = round(
            math.hypot(
                entity.dxf.end.x - entity.dxf.start.x,
                entity.dxf.end.y - entity.dxf.start.y,
            ),
            4,
        )

    elif etype == "LWPOLYLINE" and include_details:
        vertices = entity.get_points("xy")
        result["vertex_count"] = len(vertices)
        result["is_closed"] = entity.closed
        if len(vertices) <= 20:
            result["vertices"] = [
                {"x": round(v[0], 4), "y": round(v[1], 4)} for v in vertices
            ]

    elif etype == "CIRCLE" and include_details:
        result["center"] = {
            "x": round(entity.dxf.center.x, 4),
            "y": round(entity.dxf.center.y, 4),
        }
        result["radius"] = round(entity.dxf.radius, 4)

    elif etype == "ARC" and include_details:
        result["center"] = {
            "x": round(entity.dxf.center.x, 4),
            "y": round(entity.dxf.center.y, 4),
        }
        result["radius"] = round(entity.dxf.radius, 4)
        result["start_angle"] = entity.dxf.start_angle
        result["end_angle"] = entity.dxf.end_angle

    elif etype in ("TEXT",) and include_details:
        result["text"] = entity.dxf.text
        if hasattr(entity.dxf, 'insert'):
            result["position"] = {
                "x": round(entity.dxf.insert.x, 4),
                "y": round(entity.dxf.insert.y, 4),
            }
        result["height"] = getattr(entity.dxf, 'height', None)

    elif etype in ("MTEXT",) and include_details:
        result["text"] = entity.text
        if hasattr(entity.dxf, 'insert'):
            result["position"] = {
                "x": round(entity.dxf.insert.x, 4),
                "y": round(entity.dxf.insert.y, 4),
            }
        result["height"] = getattr(entity.dxf, 'char_height', None)

    elif etype == "DIMENSION" and include_details:
        result["dimension_type"] = "标注"
        if hasattr(entity.dxf, 'text'):
            result["text_override"] = entity.dxf.text

    elif etype == "HATCH" and include_details:
        result["pattern_name"] = getattr(entity.dxf, 'pattern_name', 'SOLID')

    return result


# ==================== 子命令实现 ====================


def cmd_info(args):
    """获取图纸基本信息"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()

    # 统计各类型实体数量
    type_counts = {}
    for entity in msp:
        t = entity.dxftype()
        type_counts[t] = type_counts.get(t, 0) + 1

    info = {
        "file": os.path.abspath(args.file),
        "dxf_version": doc.dxfversion,
        "unit": _get_unit_name(doc),
        "unit_code": _get_unit_code(doc),
        "total_layers": len(list(doc.layers)),
        "total_blocks": len(list(b for b in doc.blocks if b.is_block_layout and not b.name.startswith("*"))),
        "modelspace_entity_count": len(msp),
        "entity_type_summary": type_counts,
        "layout_count": len(list(doc.layouts)),
    }

    # 尝试获取更多 header 信息
    try:
        if '$TDCREATE' in doc.header:
            info["created"] = str(doc.header['$TDCREATE'])
        if '$TDUPDATE' in doc.header:
            info["last_modified"] = str(doc.header['$TDUPDATE'])
        if '$LASTSAVEDBY' in doc.header:
            info["last_saved_by"] = doc.header['$LASTSAVEDBY']
    except Exception:
        pass

    print(json.dumps(info, ensure_ascii=False, indent=2))


def cmd_layers(args):
    """列出所有图层"""
    doc = _load_dwg(args.file)
    layers = []
    for layer in doc.layers:
        name = layer.dxf.name
        if name.startswith("*"):
            continue
        layer_info = {
            "name": name,
            "color_index": layer.dxf.color,
            "linetype": layer.dxf.linetype,
            "is_on": layer.is_on(),
            "is_locked": layer.is_locked(),
            "is_frozen": layer.is_frozen(),
        }
        # 如需统计实体数量
        if args.count_entities:
            msp = doc.modelspace()
            count = len(msp.query(f'*[layer=="{name}"]'))
            layer_info["entity_count"] = count
        layers.append(layer_info)

    if args.sort_by == "name":
        layers.sort(key=lambda x: x["name"])
    elif args.sort_by == "color":
        layers.sort(key=lambda x: x["color_index"])

    print(json.dumps(layers, ensure_ascii=False, indent=2))


def cmd_entities(args):
    """列出模型空间中的实体"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()

    # 构建查询字符串
    if args.type and args.layer:
        query = f'{args.type}[layer=="{args.layer}"]'
    elif args.type:
        query = args.type
    elif args.layer:
        query = f'*[layer=="{args.layer}"]'
    else:
        query = "*"

    entities = msp.query(query)
    total = len(entities)

    result_entities = []
    limit = args.limit or total
    for i, entity in enumerate(entities):
        if i >= limit:
            break
        result_entities.append(_entity_to_dict(entity, include_details=True))

    output = {
        "total_matched": total,
        "returned": len(result_entities),
        "entities": result_entities,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_blocks(args):
    """列出块定义表"""
    doc = _load_dwg(args.file)
    blocks = []
    for block_def in doc.blocks:
        name = block_def.name
        if block_def.is_block_layout and not name.startswith("*"):
            entity_count = len(block_def)

            # 统计各类型
            type_counts = {}
            for e in block_def:
                t = e.dxftype()
                type_counts[t] = type_counts.get(t, 0) + 1

            block_info = {
                "name": name,
                "entity_count": entity_count,
                "entity_types": type_counts,
            }

            if args.name_filter and args.name_filter.lower() not in name.lower():
                continue

            blocks.append(block_info)

    print(json.dumps(blocks, ensure_ascii=False, indent=2))


def cmd_inserts(args):
    """列出模型空间中的图块引用实例"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()

    inserts = []
    for entity in msp.query("INSERT"):
        name = entity.dxf.name
        if args.name_filter and args.name_filter.lower() not in name.lower():
            continue

        insert_info = _entity_to_dict(entity, include_details=True)

        # 分析内部图层
        if args.analyze_layers:
            block_def = doc.blocks.get(name)
            if block_def:
                internal_layers = set()
                for internal_entity in block_def:
                    internal_layers.add(internal_entity.dxf.layer)
                insert_info["internal_layers"] = list(internal_layers)

        inserts.append(insert_info)

    limit = args.limit or len(inserts)
    output = {
        "total": len(inserts),
        "returned": min(limit, len(inserts)),
        "inserts": inserts[:limit],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_texts(args):
    """提取图纸中的所有文本"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()

    texts = []

    # 提取 TEXT 实体
    for entity in msp.query("TEXT"):
        text_info = {
            "type": "TEXT",
            "content": entity.dxf.text,
            "layer": entity.dxf.layer,
        }
        if hasattr(entity.dxf, 'insert'):
            text_info["position"] = {
                "x": round(entity.dxf.insert.x, 4),
                "y": round(entity.dxf.insert.y, 4),
            }
        text_info["height"] = getattr(entity.dxf, 'height', None)
        texts.append(text_info)

    # 提取 MTEXT 实体
    for entity in msp.query("MTEXT"):
        text_info = {
            "type": "MTEXT",
            "content": entity.text.replace("\\P", "\n"),
            "layer": entity.dxf.layer,
        }
        if hasattr(entity.dxf, 'insert'):
            text_info["position"] = {
                "x": round(entity.dxf.insert.x, 4),
                "y": round(entity.dxf.insert.y, 4),
            }
        text_info["height"] = getattr(entity.dxf, 'char_height', None)
        texts.append(text_info)

    # 提取 INSERT 中的属性文字
    for entity in msp.query("INSERT"):
        if entity.attribs:
            for attrib in entity.attribs:
                texts.append({
                    "type": "ATTRIB",
                    "content": attrib.dxf.text,
                    "tag": attrib.dxf.tag,
                    "layer": attrib.dxf.layer,
                    "parent_block": entity.dxf.name,
                })

    # 过滤关键字
    if args.keyword:
        kw = args.keyword.lower()
        texts = [t for t in texts if kw in t.get("content", "").lower()]

    limit = args.limit or len(texts)
    output = {
        "total": len(texts),
        "returned": min(limit, len(texts)),
        "texts": texts[:limit],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_layer_content(args):
    """提取指定图层上的所有实体详情"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()

    query_string = f'*[layer=="{args.layer_name}"]'
    entities = msp.query(query_string)

    result_entities = []
    limit = args.limit or len(entities)
    for i, entity in enumerate(entities):
        if i >= limit:
            break
        result_entities.append(_entity_to_dict(entity, include_details=True))

    output = {
        "layer_name": args.layer_name,
        "total_entities": len(entities),
        "returned": len(result_entities),
        "entities": result_entities,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_spaces(args):
    """查看空间布局系统"""
    doc = _load_dwg(args.file)

    spaces = []
    for layout in doc.layouts:
        space_info = {
            "name": layout.name,
            "entity_count": len(layout),
        }
        if layout.is_modelspace:
            space_info["type"] = "模型空间 (Model Space)"
        elif layout.is_any_paperspace:
            space_info["type"] = "布局空间 (Paper Space)"
            # 提取布局空间的图块和视口信息
            if args.detail:
                inserts = layout.query("INSERT")
                space_info["insert_count"] = len(inserts)
                viewports = layout.query("VIEWPORT")
                vp_list = []
                for vp in viewports:
                    vp_info = {
                        "id": vp.dxf.id,
                        "center": {"x": round(vp.dxf.center.x, 2), "y": round(vp.dxf.center.y, 2)},
                        "width": round(vp.dxf.width, 2),
                        "height": round(vp.dxf.height, 2),
                    }
                    vp_list.append(vp_info)
                space_info["viewports"] = vp_list
        else:
            space_info["type"] = "块定义空间 (Block Definition)"

        spaces.append(space_info)

    print(json.dumps(spaces, ensure_ascii=False, indent=2))


def cmd_distance(args):
    """计算两个实体之间的距离"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()

    def _find_entity_position(identifier: str) -> Optional[tuple]:
        """通过 handle 或 block_name 查找实体位置"""
        # 先尝试按 handle 查找
        try:
            entity = doc.entitydb.get(identifier)
            if entity:
                return _get_entity_center(entity)
        except Exception:
            pass

        # 再按 block name 查找 INSERT
        for entity in msp.query("INSERT"):
            if entity.dxf.name == identifier:
                return (entity.dxf.insert.x, entity.dxf.insert.y, entity.dxf.insert.z)

        return None

    def _get_entity_center(entity) -> tuple:
        """获取实体的中心/位置坐标"""
        etype = entity.dxftype()
        if etype == "INSERT":
            return (entity.dxf.insert.x, entity.dxf.insert.y, entity.dxf.insert.z)
        elif etype == "LINE":
            mx = (entity.dxf.start.x + entity.dxf.end.x) / 2
            my = (entity.dxf.start.y + entity.dxf.end.y) / 2
            return (mx, my, 0)
        elif etype in ("CIRCLE", "ARC"):
            return (entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z)
        elif etype in ("TEXT",):
            if hasattr(entity.dxf, 'insert'):
                return (entity.dxf.insert.x, entity.dxf.insert.y, 0)
        elif etype in ("MTEXT",):
            if hasattr(entity.dxf, 'insert'):
                return (entity.dxf.insert.x, entity.dxf.insert.y, 0)
        elif etype == "LWPOLYLINE":
            pts = entity.get_points("xy")
            if pts:
                cx = sum(p[0] for p in pts) / len(pts)
                cy = sum(p[1] for p in pts) / len(pts)
                return (cx, cy, 0)
        return None

    # 支持直接坐标或实体标识符
    pos1 = None
    pos2 = None

    if args.coord1:
        parts = [float(x) for x in args.coord1.split(",")]
        pos1 = tuple(parts + [0] * (3 - len(parts)))
    else:
        pos1 = _find_entity_position(args.entity1)

    if args.coord2:
        parts = [float(x) for x in args.coord2.split(",")]
        pos2 = tuple(parts + [0] * (3 - len(parts)))
    else:
        pos2 = _find_entity_position(args.entity2)

    if pos1 is None:
        print(f"错误: 无法找到第一个实体/坐标 '{args.entity1 or args.coord1}'", file=sys.stderr)
        sys.exit(1)
    if pos2 is None:
        print(f"错误: 无法找到第二个实体/坐标 '{args.entity2 or args.coord2}'", file=sys.stderr)
        sys.exit(1)

    # 计算距离
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2] if len(pos1) > 2 and len(pos2) > 2 else 0

    dist_2d = math.hypot(dx, dy)
    dist_3d = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    unit_name = _get_unit_name(doc)

    result = {
        "point1": {"x": round(pos1[0], 4), "y": round(pos1[1], 4), "z": round(pos1[2], 4) if len(pos1) > 2 else 0},
        "point2": {"x": round(pos2[0], 4), "y": round(pos2[1], 4), "z": round(pos2[2], 4) if len(pos2) > 2 else 0},
        "distance_2d": round(dist_2d, 4),
        "distance_3d": round(dist_3d, 4),
        "delta_x": round(dx, 4),
        "delta_y": round(dy, 4),
        "delta_z": round(dz, 4),
        "unit": unit_name,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_screenshot(args):
    """对指定实体/区域进行截图"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()
    abs_dwg = os.path.abspath(args.file)

    # 确定截图区域
    start_x = start_y = width = height = None

    if args.region:
        # 直接指定区域 "x,y,w,h"
        parts = [float(x) for x in args.region.split(",")]
        if len(parts) != 4:
            print("错误: --region 格式应为 'x,y,w,h'", file=sys.stderr)
            sys.exit(1)
        start_x, start_y, width, height = parts

    elif args.block_name:
        # 按块名查找
        target_entity = None
        for entity in msp.query("INSERT"):
            if entity.dxf.name == args.block_name:
                target_entity = entity
                break
        if not target_entity:
            print(f"错误: 未找到名为 '{args.block_name}' 的图块", file=sys.stderr)
            sys.exit(1)
        insert_pt = target_entity.dxf.insert
        view_radius = args.radius or 5000
        start_x = insert_pt.x - view_radius
        start_y = insert_pt.y - view_radius
        width = view_radius * 2
        height = view_radius * 2

    elif args.handle:
        # 按 handle 查找
        try:
            entity = doc.entitydb.get(args.handle)
            if entity and entity.dxftype() == "INSERT":
                insert_pt = entity.dxf.insert
                view_radius = args.radius or 5000
                start_x = insert_pt.x - view_radius
                start_y = insert_pt.y - view_radius
                width = view_radius * 2
                height = view_radius * 2
        except Exception:
            print(f"错误: 无法通过 handle '{args.handle}' 找到实体", file=sys.stderr)
            sys.exit(1)

    elif args.layer_name:
        # 截取整个图层内容的 bounding box
        entities_on_layer = msp.query(f'*[layer=="{args.layer_name}"]')
        if len(entities_on_layer) == 0:
            print(f"错误: 图层 '{args.layer_name}' 上没有实体", file=sys.stderr)
            sys.exit(1)
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        for e in entities_on_layer:
            try:
                if e.dxftype() == "INSERT":
                    px, py = e.dxf.insert.x, e.dxf.insert.y
                    min_x, min_y = min(min_x, px), min(min_y, py)
                    max_x, max_y = max(max_x, px), max(max_y, py)
                elif e.dxftype() == "LINE":
                    for pt in (e.dxf.start, e.dxf.end):
                        min_x, min_y = min(min_x, pt.x), min(min_y, pt.y)
                        max_x, max_y = max(max_x, pt.x), max(max_y, pt.y)
                elif e.dxftype() in ("CIRCLE", "ARC"):
                    c = e.dxf.center
                    r = e.dxf.radius
                    min_x, min_y = min(min_x, c.x - r), min(min_y, c.y - r)
                    max_x, max_y = max(max_x, c.x + r), max(max_y, c.y + r)
            except Exception:
                continue
        if min_x == float('inf'):
            print("错误: 无法计算图层的边界框", file=sys.stderr)
            sys.exit(1)
        padding = args.radius or 2000
        start_x = min_x - padding
        start_y = min_y - padding
        width = (max_x - min_x) + padding * 2
        height = (max_y - min_y) + padding * 2

    else:
        # 全图截图：不指定窗口
        pass

    output_path = os.path.abspath(args.output or "cad_screenshot.png")
    pixel_size = args.pixel_size or 3000

    # 优先尝试 QCAD dwg2bmp
    qcad_tool = _find_qcad_tool(args.qcad_path)

    if qcad_tool:
        _screenshot_qcad(abs_dwg, output_path, qcad_tool, start_x, start_y, width, height, pixel_size, args.background or "black")
    else:
        # 回退到 matplotlib 渲染
        _screenshot_matplotlib(doc, output_path, start_x, start_y, width, height, pixel_size)


def _screenshot_qcad(dwg_path, output_path, qcad_tool, start_x, start_y, width, height, pixel_size, background):
    """使用 QCAD dwg2bmp 进行截图"""
    command = ["xvfb-run", "-a", qcad_tool, "-f", "-b", background]

    if start_x is not None:
        window_param = f"{start_x},{start_y},{width},{height}"
        command.extend(["-w", window_param])

    command.extend(["-width", str(pixel_size), "-height", str(pixel_size)])
    command.extend(["-o", output_path, dwg_path])

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(json.dumps({
                "status": "success",
                "output": output_path,
                "file_size_kb": round(file_size, 1),
                "resolution": f"{pixel_size}x{pixel_size}",
                "method": "qcad",
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({
                "status": "error",
                "message": f"截图文件未生成: {result.stderr.strip()}"
            }, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print(json.dumps({"status": "error", "message": "截图超时 (120秒)"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


def _screenshot_matplotlib(doc, output_path, start_x, start_y, width, height, pixel_size):
    """使用 matplotlib 渲染截图（回退方案）"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    except ImportError:
        print(json.dumps({
            "status": "error",
            "message": "matplotlib 未安装，无法使用回退截图方案。请安装: pip install matplotlib"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    msp = doc.modelspace()
    fig_size = pixel_size / 100  # dpi=100
    fig = plt.figure(figsize=(fig_size, fig_size))
    ax = fig.add_axes([0, 0, 1, 1])

    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    out.set_background("#FFFFFF")

    frontend = Frontend(ctx, out)
    frontend.draw_layout(msp, finalize=True)

    if start_x is not None:
        ax.set_xlim(start_x, start_x + width)
        ax.set_ylim(start_y, start_y + height)

    # 根据扩展名保存
    ext = os.path.splitext(output_path)[1].lower()
    fmt = "png"
    if ext == ".pdf":
        fmt = "pdf"
    elif ext == ".svg":
        fmt = "svg"

    fig.savefig(output_path, format=fmt, dpi=100)
    plt.close(fig)

    file_size = os.path.getsize(output_path) / 1024
    print(json.dumps({
        "status": "success",
        "output": output_path,
        "file_size_kb": round(file_size, 1),
        "method": "matplotlib",
    }, ensure_ascii=False, indent=2))


def cmd_audit(args):
    """图纸规范性审核"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()

    issues = []

    # 1. 检查 0 层违规的 INSERT
    for entity in msp.query("INSERT"):
        if entity.dxf.layer == "0":
            issues.append({
                "severity": "error",
                "rule": "zero_layer_insert",
                "message": f"图块 '{entity.dxf.name}' 被放置于默认 0 层，应分配至专业图层",
                "entity_handle": entity.dxf.handle,
                "position": {
                    "x": round(entity.dxf.insert.x, 2),
                    "y": round(entity.dxf.insert.y, 2),
                },
            })

    # 2. 检查图块内部图层规范性
    for entity in msp.query("INSERT"):
        block_name = entity.dxf.name
        block_def = doc.blocks.get(block_name)
        if block_def:
            internal_layers = set()
            for internal_entity in block_def:
                internal_layers.add(internal_entity.dxf.layer)
            if "0" not in internal_layers or len(internal_layers) > 1:
                issues.append({
                    "severity": "warning",
                    "rule": "block_layer_mixed",
                    "message": f"图块 '{block_name}' 内部使用了多个图层: {list(internal_layers)}",
                    "entity_handle": entity.dxf.handle,
                    "insert_layer": entity.dxf.layer,
                    "internal_layers": list(internal_layers),
                })

    # 3. 检查空图层
    for layer in doc.layers:
        name = layer.dxf.name
        if name.startswith("*"):
            continue
        count = len(msp.query(f'*[layer=="{name}"]'))
        if count == 0:
            issues.append({
                "severity": "info",
                "rule": "empty_layer",
                "message": f"图层 '{name}' 在模型空间中没有任何实体，可能为冗余图层",
            })

    # 4. 检查是否存在 DEFPOINTS 层上的实体（不应出现）
    defpoints_count = len(msp.query('*[layer=="DEFPOINTS"]'))
    if defpoints_count > 0:
        issues.append({
            "severity": "warning",
            "rule": "defpoints_entities",
            "message": f"DEFPOINTS 图层上存在 {defpoints_count} 个实体，这些实体不会被打印",
        })

    # 去重相同 block_name 的 block_layer_mixed 警告
    seen_block_warnings = set()
    deduped_issues = []
    for issue in issues:
        if issue["rule"] == "block_layer_mixed":
            bn = issue["message"].split("'")[1]
            if bn in seen_block_warnings:
                continue
            seen_block_warnings.add(bn)
        deduped_issues.append(issue)

    summary = {
        "total_issues": len(deduped_issues),
        "errors": len([i for i in deduped_issues if i["severity"] == "error"]),
        "warnings": len([i for i in deduped_issues if i["severity"] == "warning"]),
        "info": len([i for i in deduped_issues if i["severity"] == "info"]),
        "issues": deduped_issues,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def cmd_search(args):
    """按名称/关键字搜索实体"""
    doc = _load_dwg(args.file)
    msp = doc.modelspace()
    keyword = args.keyword.lower()

    results = []

    for entity in msp:
        matched = False
        match_reason = ""

        etype = entity.dxftype()

        if etype == "INSERT" and keyword in entity.dxf.name.lower():
            matched = True
            match_reason = f"图块名称匹配: '{entity.dxf.name}'"

        elif etype == "TEXT" and keyword in entity.dxf.text.lower():
            matched = True
            match_reason = f"文本内容匹配: '{entity.dxf.text}'"

        elif etype == "MTEXT" and keyword in entity.text.lower():
            matched = True
            match_reason = f"多行文本匹配: '{entity.text[:80]}'"

        elif keyword in entity.dxf.layer.lower():
            matched = True
            match_reason = f"图层名称匹配: '{entity.dxf.layer}'"

        if matched:
            result = _entity_to_dict(entity, include_details=True)
            result["match_reason"] = match_reason
            results.append(result)

    limit = args.limit or len(results)
    output = {
        "keyword": args.keyword,
        "total_matches": len(results),
        "returned": min(limit, len(results)),
        "results": results[:limit],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_export_pdf(args):
    """将图纸导出为 PDF"""
    doc = _load_dwg(args.file)
    output_path = os.path.abspath(args.output or "cad_export.pdf")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    except ImportError:
        print(json.dumps({
            "status": "error",
            "message": "matplotlib 未安装。请安装: pip install matplotlib"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    msp = doc.modelspace()
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_axes([0, 0, 1, 1])

    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    bg = args.background or "#FFFFFF"
    out.set_background(bg)

    frontend = Frontend(ctx, out)
    frontend.draw_layout(msp, finalize=True)

    fig.savefig(output_path, format="pdf")
    plt.close(fig)

    file_size = os.path.getsize(output_path) / 1024
    print(json.dumps({
        "status": "success",
        "output": output_path,
        "file_size_kb": round(file_size, 1),
    }, ensure_ascii=False, indent=2))


def cmd_check_env(args):
    """检查当前环境的依赖配置状态"""
    status = {}

    # Python 依赖
    for pkg in ("ezdxf", "matplotlib"):
        try:
            mod = __import__(pkg)
            ver = getattr(mod, "version", getattr(mod, "__version__", "unknown"))
            status[pkg] = {"installed": True, "version": str(ver)}
        except ImportError:
            status[pkg] = {"installed": False}

    # xvfb
    xvfb_ok = subprocess.run(["which", "xvfb-run"], capture_output=True).returncode == 0
    status["xvfb"] = {"installed": xvfb_ok}

    # ODA
    oda = _find_oda_wrapper()
    status["oda_file_converter"] = {
        "installed": oda is not None,
        "path": oda,
        "capability": "读取 DWG 文件并转换为 DXF 格式",
    }

    # QCAD
    qcad = _find_qcad_tool()
    status["qcad_dwg2bmp"] = {
        "installed": qcad is not None,
        "path": qcad,
        "capability": "高质量 CAD 图纸截图渲染",
    }

    # 总结
    all_ok = all([
        status["ezdxf"]["installed"],
        status["matplotlib"]["installed"],
        status["oda_file_converter"]["installed"],
        status["qcad_dwg2bmp"]["installed"],
    ])

    output = {
        "environment_ready": all_ok,
        "dependencies": status,
        "setup_script": os.path.join(SCRIPT_DIR, "setup.sh"),
    }

    if not all_ok:
        missing = []
        if not status["oda_file_converter"]["installed"]:
            missing.append("ODA File Converter (用于 DWG 读取)")
        if not status["qcad_dwg2bmp"]["installed"]:
            missing.append("QCAD dwg2bmp (用于高质量截图)")
        if not status["ezdxf"]["installed"]:
            missing.append("ezdxf (Python CAD 库)")
        if not status["matplotlib"]["installed"]:
            missing.append("matplotlib (回退截图引擎)")
        output["missing"] = missing
        output["fix_command"] = f"bash {os.path.join(SCRIPT_DIR, 'setup.sh')}"

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_setup(args):
    """运行环境配置脚本"""
    setup_script = os.path.join(SCRIPT_DIR, "setup.sh")
    if not os.path.exists(setup_script):
        print(json.dumps({
            "status": "error",
            "message": f"setup.sh 不存在: {setup_script}"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    cmd = ["bash", setup_script]
    if args.confirm:
        cmd.append("--confirm")
    if args.skip_oda:
        cmd.append("--skip-oda")
    if args.skip_qcad:
        cmd.append("--skip-qcad")
    if args.oda_rpm:
        cmd.extend(["--oda-rpm", args.oda_rpm])
    if args.qcad_tar:
        cmd.extend(["--qcad-tar", args.qcad_tar])

    result = subprocess.run(cmd, cwd=SCRIPT_DIR)
    sys.exit(result.returncode)


# ==================== 主入口 ====================

def main():
    parser = argparse.ArgumentParser(
        description="CAD DWG/DXF 图纸专业分析工具集",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # info
    p = subparsers.add_parser("info", help="获取图纸基本信息")
    p.add_argument("file", help="DWG/DXF 文件路径")

    # layers
    p = subparsers.add_parser("layers", help="列出所有图层")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--count-entities", action="store_true", help="统计每个图层上的实体数量")
    p.add_argument("--sort-by", choices=["name", "color"], default="name", help="排序方式")

    # entities
    p = subparsers.add_parser("entities", help="列出模型空间中的实体")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--type", help="按类型过滤 (INSERT/LINE/CIRCLE/TEXT/MTEXT/LWPOLYLINE 等)")
    p.add_argument("--layer", help="按图层过滤")
    p.add_argument("--limit", type=int, help="限制返回数量")

    # blocks
    p = subparsers.add_parser("blocks", help="列出块定义表")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--name-filter", help="按名称过滤（模糊匹配）")

    # inserts
    p = subparsers.add_parser("inserts", help="列出图块引用实例")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--name-filter", help="按图块名称过滤（模糊匹配）")
    p.add_argument("--analyze-layers", action="store_true", help="分析图块内部图层分布")
    p.add_argument("--limit", type=int, help="限制返回数量")

    # texts
    p = subparsers.add_parser("texts", help="提取图纸中的所有文本")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--keyword", help="按关键字过滤")
    p.add_argument("--limit", type=int, help="限制返回数量")

    # layer-content
    p = subparsers.add_parser("layer-content", help="提取指定图层的实体详情")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("layer_name", help="目标图层名称")
    p.add_argument("--limit", type=int, help="限制返回数量")

    # spaces
    p = subparsers.add_parser("spaces", help="查看空间布局系统")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--detail", action="store_true", help="显示详细布局信息")

    # distance
    p = subparsers.add_parser("distance", help="计算两点/实体间的距离")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--entity1", help="第一个实体标识 (handle 或 block_name)")
    p.add_argument("--entity2", help="第二个实体标识 (handle 或 block_name)")
    p.add_argument("--coord1", help="第一个坐标 'x,y' 或 'x,y,z'")
    p.add_argument("--coord2", help="第二个坐标 'x,y' 或 'x,y,z'")

    # screenshot
    p = subparsers.add_parser("screenshot", help="对指定实体/区域截图")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--block-name", help="按图块名称定位截图区域")
    p.add_argument("--handle", help="按实体 handle 定位截图区域")
    p.add_argument("--layer-name", help="截取整个图层内容的区域")
    p.add_argument("--region", help="直接指定截图区域 'x,y,w,h'")
    p.add_argument("--radius", type=float, default=5000, help="实体截图时向四周扩展的半径 (默认: 5000)")
    p.add_argument("--output", "-o", help="输出文件路径 (默认: cad_screenshot.png)")
    p.add_argument("--pixel-size", type=int, default=3000, help="输出图片像素尺寸 (默认: 3000)")
    p.add_argument("--background", default="black", help="背景颜色 (默认: black)")
    p.add_argument("--qcad-path", help="QCAD dwg2bmp 工具路径")

    # audit
    p = subparsers.add_parser("audit", help="图纸规范性审核")
    p.add_argument("file", help="DWG/DXF 文件路径")

    # search
    p = subparsers.add_parser("search", help="按关键字搜索实体")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("keyword", help="搜索关键字")
    p.add_argument("--limit", type=int, help="限制返回数量")

    # export-pdf
    p = subparsers.add_parser("export-pdf", help="导出图纸为 PDF")
    p.add_argument("file", help="DWG/DXF 文件路径")
    p.add_argument("--output", "-o", help="输出 PDF 路径 (默认: cad_export.pdf)")
    p.add_argument("--background", default="#FFFFFF", help="背景颜色 (默认: 白色)")

    # check-env
    p = subparsers.add_parser("check-env", help="检查环境依赖配置状态")

    # setup
    p = subparsers.add_parser("setup", help="运行环境配置脚本（安装 ODA/QCAD 等依赖）")
    p.add_argument("--confirm", action="store_true", help="确认执行自动安装（必须显式指定）")
    p.add_argument("--skip-oda", action="store_true", help="跳过 ODA File Converter 安装")
    p.add_argument("--skip-qcad", action="store_true", help="跳过 QCAD 安装")
    p.add_argument("--oda-rpm", help="指定本地 ODA RPM/DEB 安装包路径")
    p.add_argument("--qcad-tar", help="指定本地 QCAD tar.gz 安装包路径")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "info": cmd_info,
        "layers": cmd_layers,
        "entities": cmd_entities,
        "blocks": cmd_blocks,
        "inserts": cmd_inserts,
        "texts": cmd_texts,
        "layer-content": cmd_layer_content,
        "spaces": cmd_spaces,
        "distance": cmd_distance,
        "screenshot": cmd_screenshot,
        "audit": cmd_audit,
        "search": cmd_search,
        "export-pdf": cmd_export_pdf,
        "check-env": cmd_check_env,
        "setup": cmd_setup,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
