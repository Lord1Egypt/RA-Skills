"""
bricklayer-assistant 材料计算辅助脚本
用途：自动计算砖块、水泥、砂、瓷砖、填缝剂用量
"""

import json
import math
import sys
from typing import Dict, Any


# ============================================================
# 数据定义
# ============================================================

BRICK_TYPES = {
    "standard": {"name": "标准粘土砖", "l": 240, "w": 115, "h": 53, "per_m2_12": 64, "per_m2_24": 128, "per_m2_18": 96, "per_m2_37": 192},
    "perforated": {"name": "多孔砖", "l": 240, "w": 115, "h": 90, "per_m2_12": 43, "per_m2_24": 86, "per_m2_18": 65, "per_m2_37": 129},
    "hollow": {"name": "空心砖", "l": 240, "w": 240, "h": 115, "per_m2_12": 19, "per_m2_24": 38, "per_m2_18": 28.5, "per_m2_37": 57},
    "aac_100": {"name": "加气块(100厚)", "l": 600, "w": 200, "h": 100, "per_m2": 8.3},
    "aac_200": {"name": "加气块(200厚)", "l": 600, "w": 200, "h": 200, "per_m2": 8.3},
    "aac_300": {"name": "加气块(300厚)", "l": 600, "w": 200, "h": 300, "per_m2": 8.3},
}

WALL_TYPES = {
    "12": {"name": "12墙(120mm)", "thickness": 115},
    "18": {"name": "18墙(180mm)", "thickness": 180},
    "24": {"name": "24墙(240mm)", "thickness": 240},
    "37": {"name": "37墙(370mm)", "thickness": 370},
}

MORTAR_RATIOS = {
    "砌筑": {"cement": 1, "sand": 3, "cement_per_m3": 375, "sand_per_m3": 0.75},
    "砌筑高标号": {"cement": 1, "sand": 2.5, "cement_per_m3": 429, "sand_per_m3": 0.714},
    "抹灰底层": {"cement": 1, "sand": 3, "cement_per_m3": 375, "sand_per_m3": 0.75},
    "抹灰面层": {"cement": 1, "sand": 2, "cement_per_m3": 500, "sand_per_m3": 0.667},
}


# ============================================================
# 计算函数
# ============================================================

def calc_brick(wall_area: float, wall_type: str, brick_type: str, wastage: float = 0.03) -> Dict[str, Any]:
    """计算砖块用量"""
    wt = WALL_TYPES.get(wall_type)
    bt = BRICK_TYPES.get(brick_type)

    if not wt or not bt:
        return {"error": f"不支持的墙体类型({wall_type})或砖型({brick_type})"}

    key = f"per_m2_{wall_type}"
    per_m2 = bt.get(key)
    if per_m2 is None:
        key2 = "per_m2"
        per_m2 = bt.get(key2, 0)

    total_bricks = math.ceil(wall_area * per_m2 * (1 + wastage))
    wall_volume = wall_area * wt["thickness"] / 1000

    return {
        "砖型": bt["name"],
        "墙体类型": wt["name"],
        "墙体面积_m2": round(wall_area, 2),
        "每平米砖数": per_m2,
        "砖块用量": total_bricks,
        "损耗率": f"{wastage*100:.0f}%",
        "墙体体积_m3": round(wall_volume, 3),
    }


def calc_mortar(wall_area: float, wall_type: str, brick_type: str, mortar_type: str = "砌筑") -> Dict[str, Any]:
    """计算砂浆用量"""
    wt = WALL_TYPES.get(wall_type)
    bt = BRICK_TYPES.get(brick_type)
    mr = MORTAR_RATIOS.get(mortar_type)

    if not wt or not bt:
        return {"error": f"不支持的墙体类型({wall_type})或砖型({brick_type})"}

    mr = mr or MORTAR_RATIOS["砌筑"]

    wall_volume = wall_area * wt["thickness"] / 1000
    mortar_factors = {
        "standard": 0.056 if wall_type == "12" else 0.11 if wall_type == "24" else 0.08,
        "perforated": 0.05 if wall_type == "12" else 0.10,
        "hollow": 0.07,
    }
    mortar_factor = mortar_factors.get(brick_type, 0.056)
    mortar_volume = wall_area * mortar_factor * 1.3  # 压实系数

    cement_kg = round(mortar_volume * mr["cement_per_m3"], 1)
    cement_bags = math.ceil(cement_kg / 50)
    sand_m3 = round(mortar_volume * mr["sand_per_m3"], 2)

    return {
        "砂浆类型": mortar_type,
        "配比": f"水泥:砂 = {mr['cement']}:{mr['sand']}",
        "砂浆用量_m3": round(mortar_volume, 3),
        "水泥用量_kg": cement_kg,
        "水泥袋数(50kg袋)": cement_bags,
        "砂用量_m3": sand_m3,
        "建议用水量_L": round(cement_kg * 0.4, 0),
    }


def calc_tile(area: float, tile_l: int, tile_w: int, layout: str = "正铺", gap: float = 2.0) -> Dict[str, Any]:
    """计算瓷砖用量"""
    wastage_map = {"正铺": 0.05, "直铺": 0.05, "工字铺": 0.08, "三七分": 0.10, "二八分": 0.10, "菱形铺": 0.15, "斜铺": 0.15, "人字铺": 0.18, "鱼骨拼": 0.20}
    wastage = wastage_map.get(layout, 0.05)

    tile_area = (tile_l * tile_w) / 1_000_000  # mm² to m²
    tile_count = math.ceil(area / tile_area)
    total_count = math.ceil(tile_count * (1 + wastage))

    # 瓷砖胶计算（薄贴法）
    adhesive_per_m2 = 4.0 if max(tile_l, tile_w) >= 800 else 3.5
    adhesive_total = math.ceil(area * adhesive_per_m2 / 20)  # 20kg/袋

    # 填缝剂计算
    grout = round((tile_l + tile_w) * gap * 3 * 1.6 / (tile_l * tile_w) * 1.5, 2)

    return {
        "瓷砖规格": f"{tile_l}×{tile_w}mm",
        "铺贴方式": layout,
        "铺贴面积_m2": round(area, 2),
        "理论片数": tile_count,
        "含损耗片数": total_count,
        "损耗率": f"{wastage*100:.0f}%",
        "瓷砖胶(20kg袋)": adhesive_total,
        "填缝剂_kg_per_m2": grout,
        "填缝剂总量_kg": round(grout * area, 1),
    }


def calc_plaster(wall_area: float, thickness: float = 15.0) -> Dict[str, Any]:
    """计算抹灰材料用量"""
    mortar_volume = wall_area * thickness / 1000 * 1.15  # ±15%损耗

    cement_kg = round(mortar_volume * 375, 1)  # 1:3 配比
    cement_bags = math.ceil(cement_kg / 50)
    sand_m3 = round(mortar_volume * 0.75, 2)

    return {
        "抹灰面积_m2": round(wall_area, 2),
        "抹灰厚度_mm": thickness,
        "砂浆用量_m3": round(mortar_volume, 3),
        "水泥用量_kg": cement_kg,
        "水泥袋数(50kg袋)": cement_bags,
        "砂用量_m3": sand_m3,
    }


def calc_full_report(params: Dict[str, Any]) -> Dict[str, Any]:
    """生成完整材料计算报告"""
    result = {}

    # 砌墙计算
    if params.get("wall_area") and params.get("wall_type"):
        result["砌墙"] = calc_brick(
            params["wall_area"],
            params.get("wall_type", "24"),
            params.get("brick_type", "standard"),
            params.get("wastage", 0.03),
        )
        result["砌筑砂浆"] = calc_mortar(
            params["wall_area"],
            params.get("wall_type", "24"),
            params.get("brick_type", "standard"),
            params.get("mortar_type", "砌筑"),
        )

    # 瓷砖计算
    if params.get("tile_area") and params.get("tile_l") and params.get("tile_w"):
        result["贴砖"] = calc_tile(
            params["tile_area"],
            params["tile_l"],
            params["tile_w"],
            params.get("tile_layout", "正铺"),
            params.get("tile_gap", 2.0),
        )

    # 抹灰计算
    if params.get("plaster_area"):
        result["抹灰"] = calc_plaster(
            params["plaster_area"],
            params.get("plaster_thickness", 15.0),
        )

    return result


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
使用方法:
  python bricklayer_calc.py <json_params>

参数示例(JSON):
  {
    "wall_area": 12.5,     # 墙体面积(m²)
    "wall_type": "24",     # 12/18/24/37
    "brick_type": "standard",  # standard/perforated/hollow/aac_100/aac_200/aac_300
    "tile_area": 25,       # 铺贴面积(m²)
    "tile_l": 800,         # 瓷砖长度(mm)
    "tile_w": 800,         # 瓷砖宽度(mm)
    "tile_layout": "正铺",  # 正铺/工字铺/三七分/菱形铺/人字铺/鱼骨拼
    "plaster_area": 30     # 抹灰面积(m²)
  }
        """)
        sys.exit(0)

    if len(sys.argv) < 2:
        # 默认示例
        params = {
            "wall_area": 10,
            "wall_type": "24",
            "brick_type": "standard",
            "tile_area": 20,
            "tile_l": 800,
            "tile_w": 800,
            "tile_layout": "正铺",
            "plaster_area": 25,
        }
    else:
        params = json.loads(sys.argv[1])

    report = calc_full_report(params)
    print(json.dumps(report, ensure_ascii=False, indent=2))
