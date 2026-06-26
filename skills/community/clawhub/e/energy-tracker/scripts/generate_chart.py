#!/usr/bin/env python3
"""
能量状态趋势图表生成脚本

功能：读取历史能量状态数据，生成可视化趋势图

依赖: matplotlib
"""

import json
import sys
from typing import Dict, List


def load_data(data_file: str) -> List[Dict]:
    """
    加载能量状态数据

    参数:
        data_file: JSON数据文件路径

    返回:
        数据记录列表，每条记录包含 date, answer, interpretation
    """
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("数据文件格式错误：应为JSON数组")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"数据文件不存在: {data_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析失败: {e}")


def sort_by_date(data: List[Dict]) -> List[Dict]:
    """
    按日期排序数据记录

    参数:
        data: 数据记录列表

    返回:
        按日期升序排列的记录列表
    """
    return sorted(data, key=lambda x: x.get('date', ''))


def map_answer_to_value(answer: str) -> int:
    """
    将答案映射为数值

    参数:
        answer: 答案代码 (A/B/C)

    返回:
        数值 (A=3, B=2, C=1)
    """
    mapping = {
        'A': 3,
        'B': 2,
        'C': 1
    }
    return mapping.get(answer, 2)  # 默认值为2


def setup_chinese_font():
    """
    设置matplotlib中文字体，解决中文显示乱码问题
    """
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    # 字体列表：优先使用系统常用中文字体
    font_list = [
        'SimHei',              # 黑体 (Windows)
        'Microsoft YaHei',     # 微软雅黑 (Windows)
        'PingFang SC',         # 苹方 (macOS)
        'Heiti TC',            # 黑体-繁 (macOS)
        'WenQuanYi Micro Hei', # 文泉驿微米黑 (Linux)
        'DejaVu Sans',         # 通用字体 (备选，可能不支持中文)
    ]

    # 获取系统所有可用字体
    available_fonts = set([f.name for f in fm.fontManager.ttflist])

    # 查找可用的中文字体
    for font_name in font_list:
        if font_name in available_fonts:
            plt.rcParams['font.sans-serif'] = [font_name]
            plt.rcParams['axes.unicode_minus'] = False
            return True

    # 如果找不到中文字体，尝试从字体路径查找
    for font_name in ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'WenQuanYi Micro Hei']:
        try:
            font_path = fm.findfont(font_name)
            if font_path and 'ttf' in font_path.lower():
                plt.rcParams['font.sans-serif'] = [font_name]
                plt.rcParams['axes.unicode_minus'] = False
                return True
        except:
            continue

    # 所有方法都失败，使用英文标签
    return False


def generate_chart(data_file: str, output_file: str):
    """
    生成能量状态趋势图

    参数:
        data_file: JSON数据文件路径
        output_file: 输出图片文件路径

    返回:
        生成结果字典，包含图片路径和统计信息
    """
    try:
        import matplotlib.pyplot as plt

        # 设置中文字体
        chinese_font_available = setup_chinese_font()

        # 加载并排序数据
        data = load_data(data_file)
        if not data:
            raise ValueError("数据文件为空")

        sorted_data = sort_by_date(data)

        # 准备图表数据
        dates = [record.get('date', '') for record in sorted_data]
        # 显示简短日期 (MM-DD)
        short_dates = [d.split('-')[1] + '-' + d.split('-')[2] if '-' in d else d for d in dates]
        values = [map_answer_to_value(record.get('answer', '')) for record in sorted_data]
        labels = [record.get('answer', '') for record in sorted_data]

        # 创建图表
        plt.figure(figsize=(10, 6))

        # 绘制折线图
        plt.plot(short_dates, values, marker='o', linewidth=2, markersize=8, color='#4A90E2')

        # 设置Y轴刻度和标签（根据是否有中文字体决定）
        if chinese_font_available:
            ytick_labels = ['C-不，完全不想动', 'B-勉强可以', 'A-是']
            plt.title('能量状态趋势图', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('日期', fontsize=12)
            plt.ylabel('能量等级', fontsize=12)
            legend_labels = ['高能量', '中能量', '低能量']
        else:
            ytick_labels = ['C-No energy', 'B-Barely', 'A-Yes']
            plt.title('Energy Trend Chart', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Energy Level', fontsize=12)
            legend_labels = ['High', 'Medium', 'Low']

        plt.yticks([1, 2, 3], ytick_labels)
        plt.ylim(0.5, 3.5)

        # 添加网格
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')

        # 标记每个点的标签
        for i, (x, y, label) in enumerate(zip(short_dates, values, labels)):
            plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10, fontweight='bold')

        # 添加颜色背景区域（高/中/低能量）
        plt.axhspan(2.5, 3.5, alpha=0.1, color='green', label=legend_labels[0])
        plt.axhspan(1.5, 2.5, alpha=0.1, color='yellow', label=legend_labels[1])
        plt.axhspan(0.5, 1.5, alpha=0.1, color='red', label=legend_labels[2])

        plt.legend(loc='upper right')
        plt.tight_layout()

        # 保存图片
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()

        # 统计信息
        answer_count = {'A': 0, 'B': 0, 'C': 0}
        for record in sorted_data:
            answer = record.get('answer', '')
            if answer in answer_count:
                answer_count[answer] += 1

        return {
            "success": True,
            "image_path": output_file,
            "total_days": len(sorted_data),
            "answer_count": answer_count,
            "chinese_font": chinese_font_available
        }

    except ImportError as e:
        raise ImportError(f"缺少依赖包: {e}，请安装matplotlib: pip install matplotlib")
    except Exception as e:
        raise Exception(f"生成图表失败: {e}")


def main():
    """
    主函数：处理命令行参数并生成图表
    """
    if len(sys.argv) != 3:
        print(json.dumps({
            "error": "参数错误",
            "usage": "python3 generate_chart.py <data_file.json> <output_file.png>"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    data_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        result = generate_chart(data_file, output_file)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": "生成图表失败",
            "message": str(e)
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
