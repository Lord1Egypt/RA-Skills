#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recommend_route.py - 根据用户画像推荐个性化游览路线

从 references/attractions/ 加载景区数据，根据画像生成个性化路线

Usage:
    python recommend_route.py --attraction "forbidden-city" --profile "solo-photographer" --time "14:00"
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional
from datetime import datetime

# 处理 Windows 控制台编码
if sys.platform == 'win32':
    import io
    if not isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ============== 支持的景区列表（30 个核心 5A 景区）==============

SUPPORTED_ATTRACTIONS = [
    # 北京 (6)
    "forbidden-city", "great-wall", "summer-palace", "temple-of-heaven",
    "yuanmingyuan", "gongwangfu",
    # 陕西 (3)
    "terracotta-army", "huaqing-palace", "dayan-pagoda",
    # 浙江 (2)
    "west-lake", "qiandao-lake",
    # 西藏 (2)
    "potala-palace", "namtso-lake",
    # 广西 (2)
    "li-river", "detian-waterfall",
    # 湖南 (2)
    "wulingyuan", "phoenix-old-town",
    # 安徽 (2)
    "yellow-mountain", "hongcun",
    # 甘肃 (1)
    "dunhuang-mogao-caves",
    # 四川 (1)
    "jiuzhaigou",
    # 云南 (2)
    "lijiang-old-town", "jade-dragon-snow-mountain",
    # 江苏 (1)
    "suzhou-gardens",
    # 江西 (1)
    "lushan",
    # 福建 (1)
    "wuyi-mountain",
    # 广东 (1)
    "danxia-mountain",
    # 贵州 (1)
    "huangguoshu-waterfall",
    # 新疆 (1)
    "tianchi-lake",
    # 黑龙江 (1)
    "jingpo-lake"
]


# ============== 用户画像模板 ==============

PROFILE_TEMPLATES = {
    "solo-photographer": {
        "companions": "solo",
        "interests": ["photography", "architecture"],
        "pace": "slow",
        "priority": "photo_spots",
        "description": "独自摄影爱好者，追求光影和人少机位"
    },
    "couple-romantic": {
        "companions": "couple",
        "interests": ["romance", "photography", "culture"],
        "pace": "medium",
        "priority": "romantic_spots",
        "description": "情侣出游，注重浪漫场景和合影点"
    },
    "family-kids": {
        "companions": "family",
        "interests": ["interactive", "fun", "education"],
        "pace": "slow",
        "priority": "rest_areas",
        "description": "带娃家庭，需要互动体验和休息点"
    },
    "history-buff": {
        "companions": "solo",
        "interests": ["history", "culture", "architecture"],
        "pace": "medium",
        "priority": "deep_explanation",
        "description": "历史爱好者，追求深度讲解和冷门景点"
    },
    "quick-visit": {
        "companions": "any",
        "interests": ["highlights"],
        "pace": "fast",
        "priority": "efficiency",
        "description": "快速游览，只看精华打卡点"
    }
}


# ============== 景区数据加载 ==============

def get_supported_attractions() -> List[str]:
    """
    获取所有支持的景区列表

    Returns:
        景区英文名列表
    """
    return SUPPORTED_ATTRACTIONS


def load_attraction_data(attraction_name: str) -> Optional[Dict]:
    """
    从 references/attractions/ 加载景区数据

    Args:
        attraction_name: 景区英文名（如 forbidden-city）

    Returns:
        景区数据字典，如加载失败返回 None
    """
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建景区文件路径
    attractions_dir = os.path.join(script_dir, '..', 'references', 'attractions')

    if not os.path.exists(attractions_dir):
        return None

    # 遍历所有省份目录查找景区文件
    for province in os.listdir(attractions_dir):
        province_path = os.path.join(attractions_dir, province)
        if os.path.isdir(province_path):
            file_path = os.path.join(province_path, f"{attraction_name}.md")
            if os.path.exists(file_path):
                return parse_markdown_file(file_path)

    return None


def parse_markdown_file(file_path: str) -> Dict:
    """
    解析 Markdown 文件，提取景区信息

    Args:
        file_path: Markdown 文件路径

    Returns:
        景区数据字典
    """
    data = {
        "name": "",
        "basic_info": {},
        "spots": []
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 提取景区名称
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                data["name"] = line.replace('# ', '').split('(')[0].strip()
                break

        # 提取景点列表（查找主要景点表格）
        in_spots_table = False
        for line in lines:
            line = line.strip()

            # 检测景点表格开始
            if '| 序号 | 景点 |' in line or '| 1 |' in line:
                in_spots_table = True
                continue

            # 检测表格结束
            if in_spots_table and (line.startswith('---') or line.startswith('###') or line.startswith('## ')):
                in_spots_table = False
                continue

            # 提取景点数据
            if in_spots_table and '|' in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    try:
                        # 跳过表头
                        if '景点' in parts[2] or '序号' in parts[1]:
                            continue

                        spot_name = parts[2].strip()
                        if spot_name and len(spot_name) > 1:
                            stay_time = parts[3].strip() if len(parts) > 3 else "30 分钟"
                            highlight = parts[4].strip() if len(parts) > 4 else "景区亮点"

                            data["spots"].append({
                                "name": spot_name,
                                "stay_time": stay_time,
                                "highlight": highlight
                            })
                    except Exception:
                        pass

        # 如果没有提取到景点，使用默认值
        if not data["spots"]:
            data["spots"] = get_default_spots(data["name"])

        return data

    except Exception as e:
        print(f"Error parsing file: {e}", file=sys.stderr)
        return data


def get_default_spots(name: str) -> List[Dict]:
    """获取默认景点列表"""
    if '故宫' in name or 'Forbidden' in name:
        return [
            {"name": "午门", "stay_time": "30 分钟", "highlight": "紫禁城正门"},
            {"name": "太和殿", "stay_time": "40 分钟", "highlight": "皇帝登基大殿"},
            {"name": "中和殿", "stay_time": "20 分钟", "highlight": "皇帝休息处"},
            {"name": "保和殿", "stay_time": "25 分钟", "highlight": "科举殿试场所"},
            {"name": "乾清宫", "stay_time": "30 分钟", "highlight": "皇帝寝宫"}
        ]
    elif '长城' in name or 'Great Wall' in name:
        return [
            {"name": "关城", "stay_time": "30 分钟", "highlight": "长城起点"},
            {"name": "北一楼", "stay_time": "20 分钟", "highlight": "俯瞰关城"},
            {"name": "北四楼", "stay_time": "30 分钟", "highlight": "好汉坡"},
            {"name": "北八楼", "stay_time": "30 分钟", "highlight": "最高点"}
        ]
    elif '西湖' in name or 'West Lake' in name:
        return [
            {"name": "断桥", "stay_time": "30 分钟", "highlight": "白蛇传发生地"},
            {"name": "白堤", "stay_time": "40 分钟", "highlight": "白居易修建"},
            {"name": "平湖秋月", "stay_time": "30 分钟", "highlight": "中秋赏月"},
            {"name": "苏堤", "stay_time": "60 分钟", "highlight": "苏轼修建"}
        ]
    else:
        return [
            {"name": "核心景点 A", "stay_time": "30 分钟", "highlight": "景区亮点"},
            {"name": "核心景点 B", "stay_time": "30 分钟", "highlight": "必打卡点"},
            {"name": "核心景点 C", "stay_time": "30 分钟", "highlight": "拍照胜地"}
        ]


# ============== 路线推荐逻辑 ==============

def recommend_route(attraction_data: Dict, profile_type: str, current_time: str = "14:00") -> Dict:
    """
    根据画像推荐个性化路线

    Args:
        attraction_data: 景区数据
        profile_type: 画像类型
        current_time: 当前时间

    Returns:
        推荐路线字典
    """
    # 获取画像信息
    profile = PROFILE_TEMPLATES.get(profile_type, PROFILE_TEMPLATES["quick-visit"])

    # 获取景点列表
    spots = attraction_data.get("spots", [])

    # 根据画像类型筛选和排序景点
    if profile_type == "solo-photographer":
        # 摄影爱好者：选择拍照好的景点，时间充裕
        recommended_spots = spots[:5] if len(spots) >= 5 else spots
        stay_multiplier = 1.2
    elif profile_type == "family-kids":
        # 家庭亲子：选择有趣的景点，增加休息
        recommended_spots = spots[:4] if len(spots) >= 4 else spots
        stay_multiplier = 0.8
    elif profile_type == "history-buff":
        # 历史爱好者：选择有历史价值的景点，深度讲解
        recommended_spots = spots[:6] if len(spots) >= 6 else spots
        stay_multiplier = 1.5
    elif profile_type == "quick-visit":
        # 快速游览：只去核心景点
        recommended_spots = spots[:3] if len(spots) >= 3 else spots
        stay_multiplier = 0.6
    else:
        # 默认
        recommended_spots = spots[:5] if len(spots) >= 5 else spots
        stay_multiplier = 1.0

    # 构建路线
    route = []
    for spot in recommended_spots:
        # 解析停留时间
        stay_time_str = spot.get("stay_time", "30 分钟")
        try:
            # 提取数字
            numbers = re.findall(r'\d+', stay_time_str)
            stay_minutes = int(numbers[0]) if numbers else 30
        except:
            stay_minutes = 30

        route.append({
            "spot": spot.get("name", "景点"),
            "stay_minutes": int(stay_minutes * stay_multiplier),
            "photo_tip": f"{spot.get('highlight', '拍照点')}，根据光线调整角度",
            "culture_highlight": spot.get("highlight", "景区亮点"),
            "next_direction": "继续下一站"
        })

    # 计算总时长
    total_minutes = sum(int(stop["stay_minutes"]) for stop in route)

    return {
        "attraction": attraction_data.get("name", "景区"),
        "profile": profile,
        "route": route,
        "total_duration_minutes": total_minutes,
        "current_time": current_time,
        "summary": f"为您定制{profile['description']}路线，共{len(route)}站，预计{total_minutes}分钟"
    }


def format_output(result: Dict) -> str:
    """格式化输出为人类可读格式"""
    if not result or "error" in result:
        return "抱歉，暂时找不到该景区数据\n支持景区：forbidden-city, great-wall, west-lake 等"

    output = []
    output.append(f"{result['attraction']} 个性化路线推荐")
    output.append("")
    output.append(f"画像：{result['profile']['description']}")
    output.append(f"总时长：{result['total_duration_minutes']} 分钟")
    output.append(f"共 {len(result['route'])} 站")
    output.append("")
    output.append("=" * 40)
    output.append("")

    for i, stop in enumerate(result['route'], 1):
        output.append(f"【第{i}站】{stop['spot']}")
        output.append(f"  建议停留：{int(stop['stay_minutes'])} 分钟")
        output.append(f"  拍照：{stop['photo_tip']}")
        output.append(f"  亮点：{stop['culture_highlight']}")
        output.append(f"  方向：{stop['next_direction']}")
        output.append("")

    output.append("=" * 40)
    output.append("")
    output.append("准备好出发了吗？")
    output.append("1. 开始导览")
    output.append("2. 调整路线")
    output.append("3. 查看拍照机位")
    output.append("")
    output.append('> 直接回复数字即可（如回复"1"）')

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="景区个性化路线推荐")
    parser.add_argument("--attraction", type=str, help="景区英文名（如 forbidden-city）")
    parser.add_argument("--profile", type=str, default="quick-visit",
                       help="用户画像类型：solo-photographer/couple-romantic/family-kids/history-buff/quick-visit")
    parser.add_argument("--time", type=str, default="14:00", help="当前时间")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--list", action="store_true", help="列出所有支持的景区")

    args = parser.parse_args()

    # 验证参数
    if not args.list and not args.attraction:
        print("错误：必须指定 --attraction 或使用 --list")
        print("使用 --list 查看所有支持的景区")
        return

    # 列出所有支持的景区
    if args.list:
        print("ChinaTour 支持的景区：")
        print("=" * 50)
        for i, attraction in enumerate(SUPPORTED_ATTRACTIONS, 1):
            print(f"{i:2d}. {attraction}")
        print("=" * 50)
        print(f"总计：{len(SUPPORTED_ATTRACTIONS)} 个景区")
        return

    # 加载景区数据
    attraction_data = load_attraction_data(args.attraction)

    if not attraction_data:
        print(f"抱歉，找不到景区 '{args.attraction}' 的数据")
        print(f"支持的景区({len(SUPPORTED_ATTRACTIONS)}个): {', '.join(SUPPORTED_ATTRACTIONS[:10])} ...")
        print("使用 --list 参数查看所有支持的景区")
        return

    # 推荐路线
    result = recommend_route(attraction_data, args.profile, args.time)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()