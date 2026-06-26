#!/usr/bin/env python3
"""
轴承型号搜索脚本
用法: python search_model.py <型号>
示例: python search_model.py 6204
"""

import json
import sys
import os
from pathlib import Path


def get_data_dir():
    """获取数据目录路径"""
    # 如果在 skill 目录中运行，向上找到项目根目录
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    project_dir = skill_dir.parent.parent.parent
    return project_dir / "data"


def load_all_models():
    """加载所有型号数据"""
    data_dir = get_data_dir()
    models_dir = data_dir / "models"

    all_models = []
    if models_dir.exists():
        for json_file in models_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'models' in data:
                        all_models.extend(data['models'])
            except Exception as e:
                print(f"Warning: Failed to load {json_file}: {e}")

    return all_models


def search_model(model_number):
    """搜索特定型号"""
    model_number = model_number.upper().strip()
    models = load_all_models()

    # 精确匹配
    for model in models:
        if model['model'] == model_number:
            return model

    # 基础型号匹配（去掉后缀）
    base_model = model_number.split('-')[0].split('.')[0]
    for model in models:
        if model['model'] == base_model:
            result = model.copy()
            result['queried_model'] = model_number
            result['base_model'] = base_model
            return result

    return None


def parse_model_number(model_number):
    """解析型号编码"""
    model = model_number.upper().strip()

    # 基本型号提取
    parts = {
        'original': model,
        'base': '',
        'suffixes': []
    }

    # 分离后缀
    if '-' in model:
        base, *suffixes = model.split('-')
        parts['base'] = base
        parts['suffixes'] = suffixes
    else:
        parts['base'] = model

    # 解析基础型号（针对深沟球轴承）
    base = parts['base']
    if len(base) >= 4 and base[0] in ['6', '7', '3']:
        parts['bearing_type'] = base[0]
        parts['diameter_series'] = base[1]
        parts['bore_code'] = base[2:4]

        # 计算内径
        bore_code = base[2:4]
        if bore_code == '00':
            parts['inner_diameter'] = 10
        elif bore_code == '01':
            parts['inner_diameter'] = 12
        elif bore_code == '02':
            parts['inner_diameter'] = 15
        elif bore_code == '03':
            parts['inner_diameter'] = 17
        else:
            try:
                parts['inner_diameter'] = int(bore_code) * 5
            except ValueError:
                parts['inner_diameter'] = None

    return parts


def format_model_info(model):
    """格式化输出型号信息"""
    if not model:
        return "未找到该型号信息"

    lines = []
    lines.append(f"\n{'='*50}")
    lines.append(f"轴承型号: {model.get('model', 'N/A')}")
    if 'queried_model' in model:
        lines.append(f"查询型号: {model['queried_model']}")
    lines.append(f"类型: {model.get('type_name', model.get('type', 'N/A'))}")
    lines.append(f"{'='*50}\n")

    # 尺寸
    dims = model.get('dimensions', {})
    lines.append("【尺寸参数】")
    lines.append(f"  内径 (d): {dims.get('d', 'N/A')} mm")
    lines.append(f"  外径 (D): {dims.get('D', 'N/A')} mm")
    lines.append(f"  宽度 (B): {dims.get('B', 'N/A')} mm")
    lines.append("")

    # 载荷
    loads = model.get('load_ratings', {})
    lines.append("【载荷能力】")
    lines.append(f"  基本额定动载荷 (C): {loads.get('C', 'N/A')} N")
    lines.append(f"  基本额定静载荷 (C0): {loads.get('C0', 'N/A')} N")
    lines.append("")

    # 转速
    speeds = model.get('speed_limits', {})
    lines.append("【极限转速】")
    lines.append(f"  脂润滑: {speeds.get('grease', 'N/A')} rpm")
    lines.append(f"  油润滑: {speeds.get('oil', 'N/A')} rpm")
    lines.append("")

    # 其他
    lines.append("【其他参数】")
    if 'weight' in model:
        lines.append(f"  重量: {model['weight']} kg")

    # 品牌对照
    cross = model.get('cross_reference', {})
    if cross:
        lines.append("")
        lines.append("【品牌型号对照】")
        for brand, model_num in cross.items():
            lines.append(f"  {brand}: {model_num}")

    lines.append(f"\n{'='*50}\n")
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python search_model.py <型号>")
        print("示例: python search_model.py 6204")
        print("      python search_model.py 6204-2RS")
        sys.exit(1)

    model_number = sys.argv[1]

    # 解析型号
    print(f"\n正在搜索: {model_number}")
    parsed = parse_model_number(model_number)
    print(f"基础型号: {parsed['base']}")

    # 搜索
    result = search_model(model_number)
    print(format_model_info(result))


if __name__ == "__main__":
    main()
