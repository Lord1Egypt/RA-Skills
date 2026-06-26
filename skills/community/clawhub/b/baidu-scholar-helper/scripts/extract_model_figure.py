#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF模型图智能提取器 V3.0
功能：从PDF中精确定位并提取模型架构图（排除实验图）

核心策略：
1. 提取PDF中的单独图片（不是整个页面）
2. 分析图片的视觉特征
3. 结合图片标题文字判断
4. 智能排除实验结果图
"""

import os
import re
import sys
import subprocess
import tempfile
from PIL import Image
import json

def extract_text_near_image(pdf_path, page_num):
    """提取页面文字用于分析图片标题"""
    try:
        cmd = ["pdftotext", "-f", str(page_num), "-l", str(page_num), "-layout", pdf_path, "-"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.lower()
    except:
        return ""

def analyze_image_features(image):
    """
    分析图片的视觉特征，判断是否是模型图
    
    模型图特征：
    - 横向布局（宽 > 高）
    - 包含矩形框/模块
    - 有明显的颜色边界
    - 通常有箭头/连接线
    
    实验图特征：
    - 曲线图：深色背景+彩色曲线
    - 柱状图：垂直条形
    - 表格：规则网格
    """
    width, height = image.size
    features = {
        "aspect_ratio": width / height if height > 0 else 1,
        "width": width,
        "height": height,
        "is_landscape": width > height,
        "score": 0,
        "type_guess": "unknown"
    }
    
    # 转换为RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 1. 宽高比分析
    aspect_ratio = features["aspect_ratio"]
    if aspect_ratio > 1.5:  # 明显横向
        features["score"] += 25
        features["type_guess"] = "likely_model"
    elif aspect_ratio > 1.2:
        features["score"] += 15
    elif aspect_ratio < 0.8:  # 纵向可能是表格或柱状图
        features["score"] -= 20
        features["type_guess"] = "likely_chart"
    
    # 2. 颜色分析
    colors = image.getcolors(maxcolors=50000)
    if colors:
        unique_colors = len(colors)
        # 模型图：适中颜色数量（框图有填充色）
        if 5 < unique_colors < 500:
            features["score"] += 20
        # 照片/实验图：颜色丰富
        elif unique_colors > 5000:
            features["score"] -= 15
            features["type_guess"] = "likely_photo"
    
    # 3. 边缘检测（简化版：检测是否有明显的矩形区域）
    # 采样分析
    try:
        # 统计水平线和垂直线
        img_gray = image.convert('L')
        pixels = img_gray.load()
        
        horizontal_lines = 0
        vertical_lines = 0
        
        # 采样检测
        for y in range(0, height, max(1, height // 20)):
            same_color_count = 0
            for x in range(1, width):
                if abs(pixels[x, y] - pixels[x-1, y]) < 10:
                    same_color_count += 1
            if same_color_count > width * 0.3:
                horizontal_lines += 1
        
        for x in range(0, width, max(1, width // 20)):
            same_color_count = 0
            for y in range(1, height):
                if abs(pixels[x, y] - pixels[x, y-1]) < 10:
                    same_color_count += 1
            if same_color_count > height * 0.3:
                vertical_lines += 1
        
        # 模型图通常有较多的水平/垂直结构
        if horizontal_lines > 3 and vertical_lines > 3:
            features["score"] += 15
        
    except:
        pass
    
    # 4. 尺寸判断
    if width > 400 and height > 200:
        features["score"] += 10
    
    return features

def check_figure_caption(text, img_index):
    """
    检查图片标题，判断是否是模型图
    
    模型图标题通常包含：
    - Figure 1, Fig. 1（通常第一个图是模型图）
    - architecture, framework, model, overview, pipeline
    - 架构、框架、模型、结构
    
    实验图标题通常包含：
    - accuracy, performance, comparison, results
    - comparison with, ablation study
    - 准确率、对比、消融实验
    """
    score = 0
    
    # 模型图关键词
    model_keywords = [
        'architecture', 'framework', 'model', 'overview', 'pipeline',
        'structure', 'diagram', 'schema', 'system', 'network',
        '架构', '框架', '模型', '结构', '流程', '系统', '网络'
    ]
    
    # 实验图关键词（排除）
    exp_keywords = [
        'accuracy', 'precision', 'recall', 'f1', 'auc',
        'performance', 'comparison', 'ablation', 'results',
        'experiment', 'evaluation', 'baseline',
        '准确率', '精度', '对比', '消融', '实验', '结果'
    ]
    
    text_lower = text.lower()
    
    # 检查模型图关键词
    for kw in model_keywords:
        if kw in text_lower:
            score += 10
    
    # 检查实验图关键词（减分）
    for kw in exp_keywords:
        if kw in text_lower:
            score -= 15
    
    # Figure 1 通常是模型图
    if img_index == 0:
        score += 20
    
    return score

def extract_images_from_pdf_page(pdf_path, page_num, output_dir, prefix):
    """
    从PDF单页中提取所有图片
    使用pdfimages工具
    """
    images = []
    
    try:
        # 使用pdfimages提取图片
        cmd = ["pdfimages", "-png", "-f", str(page_num), "-l", str(page_num), 
               pdf_path, os.path.join(output_dir, f"{prefix}_p{page_num}")]
        subprocess.run(cmd, capture_output=True, timeout=30)
        
        # 找到生成的图片
        for f in os.listdir(output_dir):
            if f.startswith(f"{prefix}_p{page_num}") and f.endswith('.png'):
                img_path = os.path.join(output_dir, f)
                try:
                    # 获取图片编号
                    match = re.search(r'-(\d+)', f)
                    img_index = int(match.group(1)) if match else 0
                    
                    images.append({
                        "path": img_path,
                        "index": img_index,
                        "page": page_num
                    })
                except:
                    pass
    except Exception as e:
        pass
    
    return images

def smart_extract_model_figures(pdf_path, output_dir, max_pages=8, max_figures=3):
    """
    智能提取模型架构图
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        max_pages: 最多检查前N页
        max_figures: 最多提取几张模型图
    
    Returns:
        提取的模型图路径列表
    """
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    candidates = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for page_num in range(1, max_pages + 1):
            # 提取该页的图片
            images = extract_images_from_pdf_page(pdf_path, page_num, tmpdir, pdf_name)
            
            if not images:
                continue
            
            # 获取该页文字（用于分析图片标题）
            page_text = extract_text_near_image(pdf_path, page_num)
            
            for img_info in images:
                try:
                    img = Image.open(img_info["path"])
                    
                    # 分析图片特征
                    features = analyze_image_features(img)
                    
                    # 过滤太小的图片（图标、符号）
                    if features['width'] < 200 or features['height'] < 100:
                        continue
                    
                    # 检查图片标题关键词
                    caption_score = check_figure_caption(page_text, img_info["index"])
                    
                    # 综合得分
                    total_score = features["score"] + caption_score
                    
                    # 只保留得分较高的候选
                    if total_score >= 20:
                        candidates.append({
                            "score": total_score,
                            "path": img_info["path"],
                            "page": page_num,
                            "index": img_info["index"],
                            "features": features,
                            "img": img.copy()
                        })
                        
                except Exception as e:
                    continue
    
    # 按得分排序
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # 保存最佳候选
    saved_paths = []
    for cand in candidates[:max_figures]:
        filename = f"{pdf_name}_p{cand['page']}_fig{cand['index']}_model.png"
        filepath = os.path.join(output_dir, filename)
        
        try:
            cand["img"].save(filepath)
            saved_paths.append(filepath)
            
            width, height = cand["img"].size
            print(f"    🖼️  模型图: {filename}")
            print(f"       得分: {cand['score']} | 尺寸: {width}x{height} | 类型: {cand['features']['type_guess']}")
        except Exception as e:
            print(f"    ⚠️  保存失败: {e}")
    
    return saved_paths


def batch_smart_extract(papers_dir, output_dir=None):
    """
    批量智能提取模型图
    """
    if output_dir is None:
        output_dir = os.path.join(papers_dir, "model_figures")
    
    pdf_files = [f for f in os.listdir(papers_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("未找到PDF文件")
        return
    
    print(f"\n{'='*70}")
    print(f"🔍 智能模型图提取器 V3.0")
    print(f"{'='*70}")
    print(f"\n发现 {len(pdf_files)} 个PDF文件")
    
    total_extracted = 0
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(papers_dir, pdf_file)
        print(f"\n📄 处理: {pdf_file[:50]}...")
        
        figures = smart_extract_model_figures(pdf_path, output_dir)
        total_extracted += len(figures)
    
    print(f"\n{'='*70}")
    print(f"✅ 完成！共提取 {total_extracted} 张模型图")
    print(f"📂 保存位置: {output_dir}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
PDF模型图智能提取器 V3.0

使用方法：
  python extract_model_figure.py <PDF文件或目录>
  python extract_model_figure.py <PDF文件> <输出目录>

示例：
  python extract_model_figure.py paper.pdf
  python extract_model_figure.py ~/Desktop/papers/LLM/

识别策略：
  ┌─────────────────────────────────────────────────────────────┐
  │                    模型图 vs 实验图                          │
  ├─────────────────────────────────────────────────────────────┤
  │ 模型图特征：                                                 │
  │   ✅ 横向布局（宽高比 > 1.2）                                │
  │   ✅ 包含矩形框/模块                                         │
  │   ✅ 标题含 architecture/framework/model                    │
  │   ✅ Figure 1 通常是模型图                                   │
  │   ✅ 适中颜色数量（框图填充）                                 │
  ├─────────────────────────────────────────────────────────────┤
  │ 实验图特征（排除）：                                          │
  │   ❌ 标题含 accuracy/comparison/results                     │
  │   ❌ 纵向布局（可能是柱状图）                                 │
  │   ❌ 颜色过于丰富（照片/曲线图）                              │
  │   ❌ 含 ablation/experiment 关键词                          │
  └─────────────────────────────────────────────────────────────┘

依赖：
  - poppler-utils (pdfimages, pdftotext)
  - Pillow
""")
        sys.exit(1)
    
    target = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None
    
    if os.path.isdir(target):
        batch_smart_extract(target, output_dir)
    elif os.path.isfile(target) and target.lower().endswith('.pdf'):
        if output_dir is None:
            output_dir = os.path.dirname(target) or "."
        smart_extract_model_figures(target, output_dir)
    else:
        print(f"错误: {target} 不是有效的PDF文件或目录")
        sys.exit(1)
