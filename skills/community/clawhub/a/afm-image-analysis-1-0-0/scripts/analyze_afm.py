#!/usr/bin/env python3
"""
AFM Image Analysis Tool
支持: 表面粗糙度、纳米颗粒统计、线轮廓、3D可视化、批量处理
Author: Labclaw 🦎  |  2026-04-06
"""

import sys
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LightSource
from scipy import ndimage, signal
from scipy.stats import skew, kurtosis
import cv2
import os
import glob
import csv
import json
from datetime import datetime

# ── 颜色主题 ──────────────────────────────────────────────
C_FG   = '#E8EAF6'   # 前景
C_BG   = '#0D1117'   # 背景
C_ACC  = '#7C4DFF'   # 紫色强调
C_WARN = '#FFB300'   # 警告黄
C_ERR  = '#EF5350'   # 错误红
C_OK   = '#66BB6A'   # 绿色

# ── 粗糙度参数 ─────────────────────────────────────────────
def calc_roughness(z_data, unit='nm'):
    """计算AFM粗糙度参数"""
    z_flat = z_data.flatten()
    # 去除平缓倾斜（plane fit）
    ny, nx = z_data.shape
    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y)
    # 一阶平面拟合
    A = np.c_[X.ravel(), Y.ravel(), np.ones(nx*ny)]
    z_fit = np.linalg.lstsq(A, z_flat, rcond=None)[0]
    z_plane = (A @ z_fit).reshape(ny, nx)
    z_plane_fit = z_data - z_plane

    Ra  = np.mean(np.abs(z_plane_fit))
    Rq  = np.sqrt(np.mean(z_plane_fit**2))
    Rpv = np.max(z_plane_fit) - np.min(z_plane_fit)
    Rsk = skew(z_plane_fit.flatten())
    Rku = kurtosis(z_plane_fit.flatten())

    # 高斯滤波粗糙度（可选）
    z_smooth = ndimage.gaussian_filter(z_plane_fit, sigma=3)
    Ra_g = np.mean(np.abs(z_plane_fit - z_smooth))

    return {
        'Ra(nm)':   round(Ra,  4),
        'Rq(nm)':   round(Rq,  4),
        'Rpv(nm)':  round(Rpv, 4),
        'Rsk':      round(Rsk, 4),
        'Rku':      round(Rku, 4),
        'Ra_g(nm)': round(Ra_g, 4),
        'z_min(nm)': round(float(z_plane_fit.min()), 4),
        'z_max(nm)': round(float(z_plane_fit.max()), 4),
    }

def detect_particles(z_data, threshold_pct=0.2, min_size_px=10):
    """检测纳米颗粒/突起"""
    # Otsu自动阈值
    z_flat = z_data.flatten()
    try:
        _, thresh = cv2.threshold(
            z_flat.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    except:
        thresh = int(np.percentile(z_flat, 70))

    z_norm = (z_data - z_data.min()) / (z_data.max() - z_data.min() + 1e-10)
    mask = (z_norm > threshold_pct).astype(np.uint8)

    # 连通域分析
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    h_img, w_img = z_data.shape

    particles = []
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < min_size_px:
            continue
        component = (labels == i).astype(np.uint8)
        # 等效圆直径 (nm假设 1px=1nm)
        eq_diameter = 2 * np.sqrt(area / np.pi)
        # 高度统计
        heights = z_data[component > 0]
        particles.append({
            'id': i,
            'area_px': area,
            'eq_diameter_nm': round(eq_diameter, 2),
            'height_mean_nm': round(float(np.mean(heights)), 3),
            'height_max_nm':  round(float(np.max(heights)),  3),
            'height_min_nm':  round(float(np.min(heights)),  3),
            'cx': round(float(centroids[i, 0]), 1),
            'cy': round(float(centroids[i, 1]), 1),
        })

    return particles

def extract_line_profile(z_data, p1, p2, num_points=500):
    """提取线轮廓"""
    x0, y0 = int(p1[0]), int(p1[1])
    x1, y1 = int(p2[0]), int(p2[1])
    # Bresenham线
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= y < z_data.shape[0] and 0 <= x < z_data.shape[1]:
            points.append((x, y, z_data[y, x]))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy; x += sx
        if e2 < dx:
            err += dx; y += sy
        if len(points) > 2000:
            break
    return np.array(points)

# ── 绘图函数 ──────────────────────────────────────────────
def plot_afm_heatmap(z_data, title, output_path, z_unit='nm'):
    """绘制AFM高度图热图"""
    fig, ax = plt.subplots(figsize=(8, 6.5), facecolor=C_BG)
    ax.set_facecolor(C_BG)
    im = ax.imshow(z_data, cmap='terrain', aspect='equal')
    cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label(f'Height ({z_unit})', color=C_FG, fontsize=11)
    cbar.ax.yaxis.set_tick_params(color=C_FG)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=C_FG)
    ax.set_title(title, color=C_FG, fontsize=13, pad=10)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=C_BG, bbox_inches='tight')
    plt.close()

def plot_roughness_bar(params, output_path):
    """粗糙度参数柱状图"""
    labels = [k.split('(')[0] for k in params.keys()]
    values = list(params.values())
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=C_BG)
    ax.set_facecolor(C_BG)
    colors = [C_ACC] * len(labels)
    bars = ax.bar(labels, values, color=colors, edgecolor='none', width=0.6)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.4g}', ha='center', va='bottom', color=C_FG, fontsize=9)
    ax.tick_params(colors=C_FG)
    ax.spines[:].set_color('#3A3F5C')
    ax.set_title('Surface Roughness Parameters', color=C_FG, fontsize=13)
    ax.set_ylabel('Value (nm)', color=C_FG, fontsize=11)
    plt.xticks(rotation=30, ha='right', color=C_FG)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=C_BG, bbox_inches='tight')
    plt.close()

def plot_particle_hist(particles, output_path):
    """颗粒直径分布直方图"""
    if not particles:
        return None
    diameters = [p['eq_diameter_nm'] for p in particles]
    heights   = [p['height_max_nm']  for p in particles]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), facecolor=C_BG)
    for ax in axes:
        ax.set_facecolor(C_BG)
        ax.spines[:].set_color('#3A3F5C')
        ax.tick_params(colors=C_FG)

    axes[0].hist(diameters, bins=min(30, max(5, len(diameters)//3)),
                 color=C_ACC, edgecolor='none', alpha=0.85)
    axes[0].set_title('Particle Equivalent Diameter', color=C_FG, fontsize=11)
    axes[0].set_xlabel('Diameter (nm)', color=C_FG)
    axes[0].set_ylabel('Count', color=C_FG)
    axes[0].axvline(np.mean(diameters), color=C_WARN, lw=1.5, label=f'Mean={np.mean(diameters):.1f}nm')
    axes[0].legend(labelcolor=C_FG, fontsize=9)

    axes[1].hist(heights, bins=min(30, max(5, len(heights)//3)),
                 color='#FF7043', edgecolor='none', alpha=0.85)
    axes[1].set_title('Particle Height Distribution', color=C_FG, fontsize=11)
    axes[1].set_xlabel('Max Height (nm)', color=C_FG)
    axes[1].set_ylabel('Count', color=C_FG)
    axes[1].axvline(np.mean(heights), color=C_WARN, lw=1.5, label=f'Mean={np.mean(heights):.1f}nm')
    axes[1].legend(labelcolor=C_FG, fontsize=9)

    plt.suptitle('Nanoparticle Statistics', color=C_FG, fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=C_BG, bbox_inches='tight')
    plt.close()
    return output_path

def plot_3d_surface(z_data, title, output_path):
    """3D表面渲染"""
    fig = plt.figure(figsize=(9, 7), facecolor=C_BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=C_BG)
    ny, nx = z_data.shape
    x = np.linspace(0, nx-1, min(nx, 300))
    y = np.linspace(0, ny-1, min(ny, 300))
    X, Y = np.meshgrid(x, y)
    Z = z_data[:len(y), :len(x)]
    ls = LightSource(azdeg=315, altdeg=45)
    colors = ls.shade(Z, cmap=plt.cm.terrain, blend_mode='soft', vert_exag=2)
    ax.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1, linewidth=0)
    ax.set_title(title, color=C_FG, fontsize=12, pad=10)
    ax.set_xlabel('X (nm)', color=C_FG, fontsize=9)
    ax.set_ylabel('Y (nm)', color=C_FG, fontsize=9)
    ax.set_zlabel('Z (nm)', color=C_FG, fontsize=9)
    ax.tick_params(colors=C_FG)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=C_BG, bbox_inches='tight')
    plt.close()

def plot_line_profile(points, output_path):
    """线轮廓截面图"""
    if len(points) == 0:
        return None
    distances = np.arange(len(points))
    heights = points[:, 2]
    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor=C_BG)
    ax.set_facecolor(C_BG)
    ax.plot(distances, heights, color=C_ACC, lw=1.5, alpha=0.9)
    ax.fill_between(distances, heights, alpha=0.2, color=C_ACC)
    ax.axhline(np.mean(heights), color=C_WARN, lw=1.2, ls='--', label=f'Mean: {np.mean(heights):.3f} nm')
    ax.axhline(np.max(heights), color=C_ERR,  lw=1.0, ls=':', label=f'Max: {np.max(heights):.3f} nm')
    ax.axhline(np.min(heights), color=C_OK,   lw=1.0, ls=':', label=f'Min: {np.min(heights):.3f} nm')
    ax.spines[:].set_color('#3A3F5C')
    ax.tick_params(colors=C_FG)
    ax.set_xlabel('Distance along profile (px)', color=C_FG)
    ax.set_ylabel('Height (nm)', color=C_FG)
    ax.set_title('Line Profile Cross-Section', color=C_FG, fontsize=12)
    ax.legend(labelcolor=C_FG, fontsize=9)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=C_BG, bbox_inches='tight')
    plt.close()
    return output_path

def annotate_particles(z_data, particles, output_path):
    """标注颗粒的AFM图像"""
    fig, ax = plt.subplots(figsize=(9, 8), facecolor=C_BG)
    ax.set_facecolor(C_BG)
    im = ax.imshow(z_data, cmap='terrain', aspect='equal')
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Height (nm)', color=C_FG)
    for p in particles:
        cx, cy = p['cx'], p['cy']
        d = p['eq_diameter_nm']
        circle = plt.Circle((cx, cy), d/2, fill=False,
                             edgecolor=C_ERR, lw=1.2, ls='-')
        ax.add_patch(circle)
        ax.annotate(f"#{p['id']}\nØ={d:.1f}nm\nh={p['height_max_nm']:.1f}nm",
                    (cx, cy), color=C_FG, fontsize=7,
                    ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=C_BG,
                              edgecolor='#3A3F5C', alpha=0.8))
    ax.set_title(f'Particle Detection ({len(particles)} found)', color=C_FG, fontsize=12)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=C_BG, bbox_inches='tight')
    plt.close()

# ── 主分析函数 ──────────────────────────────────────────────
def analyze_afm_image(filepath, args):
    fname = os.path.splitext(os.path.basename(filepath))[0]
    out_dir = os.path.join(args.output, fname)
    os.makedirs(out_dir, exist_ok=True)

    # 读取数据
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.txt', '.csv', '.asc', '.dat']:
        # 文本格式（常见于AFM导出）
        z_data = np.loadtxt(filepath)
    elif ext in ['.npy', '.npz']:
        z_data = np.load(filepath)
        if isinstance(z_data, np.lib.npyio.NpzFile):
            z_data = z_data[list(z_data.files)[0]]
    else:
        # 图像格式 → 高度映射
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"  ⚠ 无法读取: {filepath}")
            return None
        # 8-bit: 0-255 → nm (默认scale, 用户可通过--scale覆盖)
        scale = args.scale or 1.0  # nm per gray level
        z_data = img.astype(float) * scale

    if z_data.ndim != 2:
        print(f"  ⚠ 跳过(非2D): {filepath}")
        return None

    print(f"\n📊 分析: {fname}  shape={z_data.shape}")
    results = {'file': filepath, 'timestamp': datetime.now().isoformat()}

    # 1. 粗糙度
    rough = calc_roughness(z_data)
    results['roughness'] = rough
    print(f"  Ra={rough['Ra(nm)']:.4f}nm  Rq={rough['Rq(nm)']:.4f}nm  Rpv={rough['Rpv(nm)']:.4f}nm")
    plot_roughness_bar(rough, os.path.join(out_dir, 'roughness.png'))
    plot_afm_heatmap(z_data, f'AFM Height Map — {fname}', os.path.join(out_dir, 'afm_heatmap.png'))

    # 2. 3D视图
    if not args.no_3d:
        plot_3d_surface(z_data, f'3D Surface — {fname}', os.path.join(out_dir, 'afm_3d.png'))

    # 3. 颗粒检测
    threshold_pct = args.threshold / 100.0
    particles = detect_particles(z_data, threshold_pct=threshold_pct, min_size_px=args.min_size)
    results['particles'] = particles
    print(f"  检测到 {len(particles)} 个颗粒")
    if particles:
        plot_particle_hist(particles, os.path.join(out_dir, 'particle_hist.png'))
        annotate_particles(z_data, particles, os.path.join(out_dir, 'particles_annotated.png'))

    # 4. 线轮廓
    if args.profile:
        try:
            pts = args.profile.split(',')
            p1 = float(pts[0]), float(pts[1])
            p2 = float(pts[2]), float(pts[3])
            line_pts = extract_line_profile(z_data, p1, p2)
            results['line_profile'] = {
                'p1': p1, 'p2': p2,
                'n_points': len(line_pts),
                'z_mean': round(float(np.mean(line_pts[:,2])), 4),
                'z_max':  round(float(np.max(line_pts[:,2])),  4),
                'z_min':  round(float(np.min(line_pts[:,2])),  4),
            }
            plot_line_profile(line_pts, os.path.join(out_dir, 'line_profile.png'))
            print(f"  轮廓: {len(line_pts)} 点, Z范围 [{results['line_profile']['z_min']}, {results['line_profile']['z_max']}] nm")
        except Exception as e:
            print(f"  ⚠ 轮廓提取失败: {e}")

    # 5. 保存CSV报告
    report_csv = os.path.join(out_dir, 'roughness.csv')
    with open(report_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Parameter', 'Value', 'Unit'])
        for k, v in rough.items():
            unit = k.split('(')[1].rstrip(')') if '(' in k else '-'
            w.writerow([k.split('(')[0], v, unit])
    if particles:
        p_csv = os.path.join(out_dir, 'particles.csv')
        with open(p_csv, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=particles[0].keys())
            w.writeheader()
            w.writerows(particles)

    # 6. JSON摘要
    with open(os.path.join(out_dir, 'report.json'), 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"  ✅ 输出: {out_dir}/")
    return results

# ── CLI ──────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(
        description='🦎 AFM图像分析工具 — 粗糙度/颗粒/轮廓/3D/批量',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument('files', nargs='+', help='AFM图像文件或包含.npy/.txt的目录')
    p.add_argument('-o', '--output', default='./afm_output',
                   help='输出目录 (默认: ./afm_output)')
    p.add_argument('--threshold', type=float, default=20,
                   help='颗粒检测高度阈值(%%) (默认: 20)')
    p.add_argument('--min-size', type=int, default=10,
                   help='最小颗粒面积(px) (默认: 10)')
    p.add_argument('--scale', type=float, default=None,
                   help='灰度→nm 比例因子 (默认: 从文件读取或1.0)')
    p.add_argument('--profile', type=str, default=None,
                   help='线轮廓坐标: x1,y1,x2,y2 (单位:px)')
    p.add_argument('--no-3d', action='store_true', help='跳过3D渲染')
    p.add_argument('--recursive', '-r', action='store_true', help='递归扫描子目录')
    args = p.parse_args()

    files = []
    for f in args.files:
        if os.path.isdir(f):
            pattern = os.path.join(f, '**') if args.recursive else os.path.join(f, '*')
            for ext in ('*.npy', '*.npz', '*.txt', '*.csv', '*.asc', '*.dat',
                        '*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff'):
                files.extend(glob.glob(os.path.join(f, pattern, ext) if args.recursive
                                        else os.path.join(f, ext)))
        elif os.path.isfile(f):
            files.append(f)
    files = sorted(set(files))
    if not files:
        print("❌ 未找到文件")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)
    print(f"🦎 AFM分析工具 | 文件数: {len(files)} | 输出: {args.output}")

    all_results = []
    for fp in files:
        r = analyze_afm_image(fp, args)
        if r:
            all_results.append(r)

    # 汇总
    summary_path = os.path.join(args.output, 'summary.csv')
    with open(summary_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['File', 'Ra(nm)', 'Rq(nm)', 'Rpv(nm)', 'Rsk', 'Rku', 'N_Particles'])
        for r in all_results:
            rough = r.get('roughness', {})
            w.writerow([
                os.path.basename(r['file']),
                rough.get('Ra(nm)', ''),
                rough.get('Rq(nm)', ''),
                rough.get('Rpv(nm)', ''),
                rough.get('Rsk', ''),
                rough.get('Rku', ''),
                len(r.get('particles', [])),
            ])
    print(f"\n✅ 完成！汇总: {summary_path}")
    print(f"   分析了 {len(all_results)} 个文件")

if __name__ == '__main__':
    main()
