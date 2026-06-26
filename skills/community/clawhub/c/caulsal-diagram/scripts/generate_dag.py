#!/usr/bin/env python3
"""
因果图（DAG）生成脚本

使用 Pillow 生成因果图图片，支持自定义节点、边和布局。

示例用法：
    python3 generate_dag.py \
        --output diagram.png \
        --title "止痛药与心脏病风险" \
        --nodes "年龄,疼痛程度,止痛药使用,心脏病风险" \
        --edges "年龄->疼痛程度,疼痛程度->止痛药使用,止痛药使用->心脏病风险"
"""

import argparse
import os
import math
from PIL import Image, ImageDraw, ImageFont

# 尝试加载中文字体
def get_font(size):
    fonts_to_try = [
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for font_path in fonts_to_try:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    return ImageFont.load_default()


def parse_nodes(nodes_str):
    """解析节点字符串"""
    return [n.strip() for n in nodes_str.split(',')]


def parse_edges(edges_str):
    """解析边字符串，返回 (from, to) 列表"""
    edges = []
    for edge in edges_str.split(','):
        if '->' in edge:
            parts = edge.strip().split('->')
            if len(parts) == 2:
                edges.append((parts[0].strip(), parts[1].strip()))
    return edges


def calculate_positions(nodes, edges, layout='tb', width=600, height=400, margin=80):
    """计算节点位置，根据因果结构智能分层"""
    n = len(nodes)
    if n == 0:
        return {}
    
    # 计算每个节点的入度（有多少条边指向它）
    in_degree = {node: 0 for node in nodes}
    for from_node, to_node in edges:
        if to_node in in_degree:
            in_degree[to_node] += 1
    
    # 按入度分层：入度为0的是原因（第一层），入度>0的是结果（后面层）
    layer0 = [node for node in nodes if in_degree[node] == 0]  # 原因层
    layer1 = [node for node in nodes if in_degree[node] > 0]    # 结果层
    
    positions = {}
    
    if layout == 'lr':
        # 左右布局：原因在左，结果在右
        # 第一层（原因）
        for i, node in enumerate(layer0):
            x = margin
            y = margin + i * (height - 2 * margin) // max(1, len(layer0) - 1) if len(layer0) > 1 else height // 2
            positions[node] = (x, y)
        # 第二层（结果）
        for i, node in enumerate(layer1):
            x = width - margin
            y = margin + i * (height - 2 * margin) // max(1, len(layer1) - 1) if len(layer1) > 1 else height // 2
            positions[node] = (x, y)
    else:
        # 上下布局（默认）：原因在上，结果在下
        # 第一层（原因）
        for i, node in enumerate(layer0):
            x = margin + i * (width - 2 * margin) // max(1, len(layer0) - 1) if len(layer0) > 1 else width // 2
            y = margin
            positions[node] = (x, y)
        # 第二层（结果）
        for i, node in enumerate(layer1):
            x = margin + i * (width - 2 * margin) // max(1, len(layer1) - 1) if len(layer1) > 1 else width // 2
            y = height - margin
            positions[node] = (x, y)
    
    return positions


def draw_arrow(draw, start, end, color='#333333', width=2, start_node_size=None, end_node_size=None):
    """绘制箭头，支持根据节点实际大小调整偏移"""
    # 计算方向
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    if length < 1:
        return
    
    # 归一化
    ndx = dx / length
    ndy = dy / length
    
    # 根据方向和节点框大小计算偏移量
    def node_offset(node_size, ndx, ndy):
        if node_size is None:
            return 50
        half_w, half_h = node_size
        # 射线与矩形边框的交点距离
        candidates = []
        if abs(ndx) > 1e-6:
            t = half_w / abs(ndx)
            candidates.append(t)
        if abs(ndy) > 1e-6:
            t = half_h / abs(ndy)
            candidates.append(t)
        return min(candidates) if candidates else 50
    
    start_offset = node_offset(start_node_size, ndx, ndy)
    end_offset = node_offset(end_node_size, ndx, ndy)

    # 调整起点和终点，避免穿过节点
    adjusted_start = (start[0] + ndx * start_offset, start[1] + ndy * start_offset)
    adjusted_end = (end[0] - ndx * end_offset, end[1] - ndy * end_offset)
    
    # 绘制线
    draw.line([adjusted_start, adjusted_end], fill=color, width=width)
    
    # 箭头头部
    arrow_len = 12
    arrow_angle = 0.4
    ax1 = adjusted_end[0] - arrow_len * (ndx * math.cos(arrow_angle) + ndy * math.sin(arrow_angle))
    ay1 = adjusted_end[1] - arrow_len * (ndy * math.cos(arrow_angle) - ndx * math.sin(arrow_angle))
    ax2 = adjusted_end[0] - arrow_len * (ndx * math.cos(arrow_angle) - ndy * math.sin(arrow_angle))
    ay2 = adjusted_end[1] - arrow_len * (ndy * math.cos(arrow_angle) + ndx * math.sin(arrow_angle))
    draw.polygon([adjusted_end, (ax1, ay1), (ax2, ay2)], fill=color)


def draw_node(draw, pos, text, font, box_width=None, box_height=40, padding_x=20, padding_y=12):
    """绘制节点，框大小根据文字宽度自适应"""
    # 动态计算框宽度
    if box_width is None:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        box_width = text_w + padding_x * 2
    # 动态计算框高度
    bbox = draw.textbbox((0, 0), text, font=font)
    text_h = bbox[3] - bbox[1]
    box_height = text_h + padding_y * 2

    x, y = pos
    x1 = x - box_width // 2
    y1 = y - box_height // 2
    x2 = x + box_width // 2
    y2 = y + box_height // 2
    
    # 绘制背景（圆角矩形简化为普通矩形）
    draw.rectangle((x1, y1, x2, y2), fill='#E3F2FD', outline='#1976D2', width=2)
    
    # 绘制文字
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x - text_width // 2
    text_y = y - text_height // 2
    draw.text((text_x, text_y), text, fill='#1565C0', font=font)
    
    # 返回节点框的半宽半高，供箭头计算用
    return (box_width // 2, box_height // 2)


def generate_dag(output, title, nodes_str, edges_str, layout='tb', width=600, height=400):
    """生成因果图"""
    nodes = parse_nodes(nodes_str)
    edges = parse_edges(edges_str)
    
    if not nodes:
        print("错误：未提供节点")
        return False
    
    # 字体
    font = get_font(16)
    title_font = get_font(20)
    
    # 先用临时图片计算文字尺寸
    tmp_img = Image.new('RGB', (1, 1), 'white')
    tmp_draw = ImageDraw.Draw(tmp_img)
    
    # 计算节点框大小
    padding_x, padding_y = 20, 12
    node_sizes = {}  # {node: (half_w, half_h)}
    for node in nodes:
        bbox = tmp_draw.textbbox((0, 0), node, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        node_sizes[node] = ((text_w + padding_x * 2) // 2, (text_h + padding_y * 2) // 2)
    
    # 计算入度分层
    in_degree = {node: 0 for node in nodes}
    for from_node, to_node in edges:
        if to_node in in_degree:
            in_degree[to_node] += 1
    layer0 = [node for node in nodes if in_degree[node] == 0]
    layer1 = [node for node in nodes if in_degree[node] > 0]
    
    # 根据节点框尺寸动态计算画布大小
    # 每层最大半宽和半高
    layer0_max_hw = max((node_sizes[n][0] for n in layer0), default=40)
    layer1_max_hw = max((node_sizes[n][0] for n in layer1), default=40)
    layer0_max_hh = max((node_sizes[n][1] for n in layer0), default=20)
    layer1_max_hh = max((node_sizes[n][1] for n in layer1), default=20)
    
    # 每层节点间距：至少节点框宽度 + 间隔
    layer0_total_w = sum(node_sizes[n][0] * 2 + 30 for n in layer0)
    layer1_total_w = sum(node_sizes[n][0] * 2 + 30 for n in layer1)
    min_width = max(layer0_total_w, layer1_total_w, 400) + 80  # 80 = 左右padding
    
    title_height = 50 if title else 30
    min_height = max(layer0_max_hh, layer1_max_hh) * 2 + 120 + title_height  # 上下层 + 层间距 + padding
    
    width = max(width, min_width)
    height = max(height, min_height)
    
    # 创建正式图片
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 绘制标题
    if title:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        draw.text(((width - title_width) // 2, 15), title, fill='#333333', font=title_font)
    
    # 计算节点位置（margin 确保节点框不超出画布）
    safe_margin_x = max(layer0_max_hw, layer1_max_hw) + 20
    safe_margin_y = max(layer0_max_hh, layer1_max_hh) + 10
    positions = calculate_positions(nodes, edges, layout, width, height - title_height,
                                     margin=max(safe_margin_x, safe_margin_y, 60))
    
    # 调整位置（下移，给标题留空间）
    positions = {k: (v[0], v[1] + title_height) for k, v in positions.items()}
    
    # 绘制边（先画，在节点下方）
    for from_node, to_node in edges:
        if from_node in positions and to_node in positions:
            draw_arrow(draw, positions[from_node], positions[to_node],
                       start_node_size=node_sizes.get(from_node),
                       end_node_size=node_sizes.get(to_node))
    
    # 绘制节点（后画，覆盖箭头与节点框重叠的部分）
    for node in nodes:
        if node in positions:
            draw_node(draw, positions[node], node, font)
    
    # 保存图片
    img.save(output, 'PNG')
    print(f'✅ 因果图已生成: {output}')
    return True


def main():
    parser = argparse.ArgumentParser(description='生成因果图（DAG）')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--title', default='', help='图表标题')
    parser.add_argument('--nodes', required=True, help='节点列表，逗号分隔')
    parser.add_argument('--edges', default='', help='边列表，逗号分隔，格式：A->B,B->C')
    parser.add_argument('--layout', default='tb', choices=['tb', 'lr'], help='布局方式')
    
    args = parser.parse_args()
    
    generate_dag(
        output=args.output,
        title=args.title,
        nodes_str=args.nodes,
        edges_str=args.edges,
        layout=args.layout
    )


if __name__ == '__main__':
    main()