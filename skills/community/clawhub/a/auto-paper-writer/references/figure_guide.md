# 科研配图规范

## 基础设置

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# 高清设置
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9

# 英文衬线字体（论文标准）
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
```

## 三种核心图表

### 1. 模型框架图（Architecture Diagram）

```python
fig, ax = plt.subplots(figsize=(8, 5))

# 背景
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# 模块框
def draw_box(ax, x, y, w, h, label, color='#4472C4'):
    rect = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=10, color='white', weight='bold')

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Input
ax.text(0.5, 3, 'Input', ha='center', va='center', fontsize=11)
draw_arrow(ax, 1, 3, 2, 3)

# Encoder
draw_box(ax, 2, 1.5, 2, 3, 'Encoder')

# Decoder
draw_box(ax, 5, 1.5, 2, 3, 'Decoder')

# Output
draw_arrow(ax, 7, 3, 8, 3)
ax.text(8.5, 3, 'Output', ha='center', va='center', fontsize=11)

# 标注
ax.annotate('Feature\nExtraction', xy=(3, 4.8), fontsize=9, ha='center')
ax.annotate('Cross-Attention', xy=(6, 4.8), fontsize=9, ha='center')

plt.tight_layout()
plt.savefig('figure1_framework.png', bbox_inches='tight', dpi=300)
```

### 2. 方法细节图（Method Detail）

```python
fig, ax = plt.subplots(figsize=(6, 4))

# 核心创新机制可视化
import numpy as np
x = np.linspace(0, 10, 100)

# 对比曲线
ax.plot(x, np.sin(x), 'b-', label='Traditional', linewidth=2)
ax.plot(x, np.sin(x) * 1.2, 'r--', label='Ours', linewidth=2)

ax.set_xlabel('Input Size')
ax.set_ylabel('Performance')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figure2_detail.png', bbox_inches='tight', dpi=300)
```

### 3. 实验结果图（Results）

```python
# 柱状对比图
fig, ax = plt.subplots(figsize=(6, 4))

methods = ['Baseline', 'Method A', 'Method B', 'Ours']
scores = [75.2, 78.5, 80.1, 85.7]
colors = ['#808080', '#4472C4', '#4472C4', '#ED7D31']

bars = ax.bar(methods, scores, color=colors, edgecolor='black', linewidth=1.2)

# 数值标注
for bar, score in zip(bars, scores):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{score:.1f}', ha='center', va='bottom', fontsize=10)

ax.set_ylabel('Accuracy (%)')
ax.set_ylim(0, 100)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('figure3_results.png', bbox_inches='tight', dpi=300)
```

## 通用规范

| 属性 | 要求 |
|------|------|
| 分辨率 | 300 dpi |
| 宽度 | 单栏 3.5in，双栏 7in |
| 格式 | PNG（图表）、PDF（框架图） |
| 颜色 | 避免红绿组合（色盲友好） |
| 字体 | Times New Roman / Arial |
| 线条 | 线条宽度 ≥ 1pt |

## 保存命令

```python
# PNG（照片/图表）
plt.savefig('figure.png', bbox_inches='tight', dpi=300)

# PDF（框架图，矢量放大不失真）
plt.savefig('framework.pdf', bbox_inches='tight')
```
