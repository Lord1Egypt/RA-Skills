---
name: academic-figures
version: 1.5.0
date: 2026-06-17
author: docsor1212
lang: zh
description: >
  论文配图一键生成工具。14种学术图表，6套配色（含Okabe-Ito色盲安全+GLM科技博客风格），
  Kaplan-Meier生存曲线、ROC曲线、堆叠柱状图、双Y轴图、组合图、流程图，
  斜纹填充、比率标注，多格式输出（PNG 600dpi + SVG + PDF + TIFF + EPS）。
metadata:
  clawdbot:
    emoji: "📊"
    category: visualization
requires:
  python: ">=3.8"
  pip: ["matplotlib", "numpy"]
---

# Academic Figures — 论文配图一键生成工具

> 📊 **14种图表 · 6套配色（含色盲安全） · 零配置中文 · 600dpi出版级输出 · PDF/TIFF/SVG全支持**
> 纯本地运行 · 数据不出本机 · Python一条命令搞定

## ✨ 核心亮点

| 特性 | 说明 |
|------|------|
| 📊 **14种学术图表** | 柱状图、水平柱状图、堆叠柱状图、热力图、散点图、折线图、双Y轴图、箱线图、森林图、KM生存曲线、ROC曲线、小提琴图、组合图、流程图 |
| 🎨 **6套配色方案** | **Okabe-Ito色盲安全**（Nature Methods金标准）、Nature、Lancet、保守学术、通用、**GLM科技博客** |
| 🇨🇳 **中文零配置** | 自动检测中文字体，彻底告别乱码，支持中英双语标签 |
| 📈 **统计标注** | 误差棒、显著性标记(p值星号)、趋势线、置信区间 |
| 🔠 **斜纹填充** | `--hatch` 一键添加9种斜纹图案（打印友好，色盲友好） |
| 📊 **比率标注** | `--show-ratio` 自动计算并标注分组间倍数（如"4.96x"） |
| 🌲 **增强森林图** | 权重气泡、I²异质性标注、事件数列、分隔线、效应量标签 |
| 📉 **KM生存曲线** | 阶梯函数、删失标记、Log-rank检验、风险表、中位生存 |
| 📐 **ROC曲线** | AUC值、95%CI、最优截断点、多模型对比 |
| 🧩 **组合图** | 多面板A+B+C，每个面板可放任意图表类型，期刊figure标准布局 |
| 📐 **流程图** | 架构/流程块、箭头、分组标注，CONSORT式研究设计图 |
| 📐 **多格式输出** | PNG 600dpi + SVG + **PDF** + **TIFF** + **EPS** |
| ♿ **无障碍支持** | Okabe-Ito色盲安全配色 + Alt Text撰写指南 |

## 图表类型

| 类型 | 命令 | 核心功能 |
|------|------|---------|
| 柱状图 | `-t bar` | 分组柱状图、误差棒、显著性标记、斜纹填充 |
| 水平柱状图 | `-t hbar` | 横向柱状图、比率标注（"4.96x"） |
| 堆叠柱状图 | `-t stacked_bar` | 构成比、百分比标签、总计标注 |
| 热力图 | `-t heatmap` | 单元格标注、自定义色阶、colorbar |
| 散点图 | `-t scatter` | 趋势线、相关系数、分组着色 |
| 折线图 | `-t line` | 多系列、误差带、标记点 |
| 双Y轴图 | `-t dual_axis` | 左右Y轴、实线+虚线、合并图例 |
| 箱线图 | `-t box` | 箱线图+抖动散点 |
| 森林图 | `-t forest` | CI横线、权重气泡、总效应菱形、I²、事件数 |
| KM生存曲线 | `-t km` | 阶梯函数、删失标记、Log-rank检验、风险表、中位生存 |
| ROC曲线 | `-t roc` | AUC、95%CI、最优截断点、多模型对比 |
| 小提琴图 | `-t violin` | 密度估计、内置均值/中位线 |
| **组合图** | `-t composite` | 多面板A+B+C，每面板任意图表类型，期刊figure布局 |
| **流程图** | `-t diagram` | 架构/流程块、箭头、分组标注，CONSORT式研究设计 |

## 快速开始

```bash
# 柱状图（色盲安全配色，推荐所有投稿使用）
python3 scripts/gen_figure.py -t bar -d data.json -o figure.png --theme okabe-ito \
  --title "图2 主标题 / Subtitle" --ylabel "准确率 Accuracy (%)"

# 水平柱状图 + 比率标注 + GLM配色（科技博客风格）
python3 scripts/gen_figure.py -t hbar -d throughput.json -o perf.png --theme glm \
  --show-ratio --title "吞吐量提升" --xlabel "归一化吞吐量"

# 柱状图 + 斜纹填充（打印友好，色盲友好）
python3 scripts/gen_figure.py -t bar -d data.json -o hatch.png --theme okabe-ito \
  --hatch --show-values --title "ACR50缓解率"

# Meta分析森林图（PDF输出）
python3 scripts/gen_figure.py -t forest -d forest.json -o forest.pdf --theme okabe-ito

# Kaplan-Meier生存曲线 + Log-rank检验
python3 scripts/gen_figure.py -t km -d survival.json -o km.png --theme okabe-ito \
  --title "图3 Kaplan-Meier生存曲线" --xlabel "时间 (月)" --ylabel "生存概率"

# ROC曲线 + AUC
python3 scripts/gen_figure.py -t roc -d roc.json -o roc.png --theme okabe-ito \
  --title "图4 ROC曲线" --xlabel "1 - 特异度" --ylabel "敏感度"

# 堆叠柱状图（亚组构成比）
python3 scripts/gen_figure.py -t stacked_bar -d subgroups.json -o stacked.png --theme okabe-ito \
  --title "图5 ANCA相关血管炎器官受累"

# 双Y轴图（临床评分+实验室指标）
python3 scripts/gen_figure.py -t dual_axis -d dual.json -o dual.png --theme okabe-ito \
  --title "图6 CRP与DAS28随治疗变化"

# 多面板组合图（Panel A+B+C，期刊figure布局）
python3 scripts/gen_figure.py -t composite -d composite.json -o figure4.png --theme okabe-ito

# 架构/流程图（研究设计，CONSORT式）
python3 scripts/gen_figure.py -t diagram -d flow.json -o flow.png --theme glm --width 12 --height 6

# 热力图（自定义色阶 + 中文）
python3 scripts/gen_figure.py -t heatmap -d data.json -o heatmap.png --cjk \
  --cmap RdBu_r --vmin -20 --vmax 45

# Lancet投稿TIFF格式（照片内容 → 300dpi）
python3 scripts/gen_figure.py -t bar -d data.json -o figure.tiff --dpi 300 --theme lancet
```

## 配色方案

| 方案 | 说明 | 色盲安全 |
|------|------|---------|
| `okabe-ito` | Nature Methods金标准（Wong 2011） | ✅ 是 |
| `nature` | NPG Nature期刊配色 | ❌ |
| `lancet` | Lancet医学配色 | ❌ |
| `conservative` | 保守学术配色 | ❌ |
| `default` | 均衡通用配色 | ❌ |
| `glm` | 柔和优雅科技博客配色（GLM-5.2像素提取） | ✅ 是 |

> **⚠️ 投稿建议**：始终使用 `--theme okabe-ito`。Nature、Science、Cell等主流期刊现已**强制要求**色盲友好图表。红绿配色是常见退稿原因。

### 为什么选 Okabe-Ito？

Okabe-Ito配色是色盲安全学术可视化的金标准：
- **Nature Methods专栏明确推荐**（Wong 2011, Nat Methods 8:441）
- 8种颜色在红色盲、绿色盲、蓝色盲下均可区分
- 视觉鲜明——与传统配色无审美差距

## 输出格式

| 格式 | 扩展名 | DPI | 适用场景 |
|------|--------|-----|----------|
| PNG | `.png` | 600（默认） | 通用、演示文稿 |
| SVG | `.svg` | 矢量 | Web、可编辑图形 |
| **PDF** | `.pdf` | 矢量 | **期刊投稿首选** |
| TIFF | `.tiff` | 600（可 `--dpi 300`） | Nature/Lancet照片要求 |
| EPS | `.eps` | 矢量 | 传统期刊要求 |

> **投稿技巧**：Nature和Science偏好**PDF/EPS矢量**格式用于线稿。使用 `.pdf` 或 `.eps` 扩展名即可。

### DPI标准（2026年）

| 内容类型 | 所需DPI | 用法 |
|----------|---------|------|
| 线稿（图表） | 600-1000+ | 默认600；严格期刊用 `--dpi 1000` |
| 照片/显微图 | 300-600 | 用 `--dpi 300` |
| 混合型 | 600 | 默认 |
| 矢量（PDF/SVG/EPS） | 不适用 | 分辨率无关 |

## 常用参数

| 参数 | 说明 |
|------|------|
| `--title "文字"` | 图表标题 |
| `--xlabel`, `--ylabel` | 坐标轴标签 |
| `--width N`, `--height N` | 图表尺寸（英寸） |
| `--format F` | 强制输出格式：png, svg, pdf, tiff, eps |
| `--dpi N` | 覆盖DPI设置 |
| `--show-values` | 柱状图显示数值标签 |
| `--show-ratio` | 显示分组间比率标注（如"4.96x"） |
| `--ratio-base N` | 比率计算的基准系列索引（默认0） |
| `--hatch` | 添加斜纹图案（打印友好，9种图案循环） |
| `--no-trend` | 隐藏散点趋势线 |
| `--no-legend` | 隐藏图例 |
| `--cmap NAME` | 热力图色阶 |
| `--vmin`, `--vmax` | 热力图数值范围 |
| `--cjk` | 自动加载中文字体 |

## ♿ 无障碍 & Alt Text

投稿时需为每个图表提供**Alt Text**描述。示例：
> "柱状图显示治疗组（均值75，标准差3）与对照组（均值68，标准差2）的比较。误差棒表示标准差。星号表示统计学显著性（p < 0.001）。"

Springer Nature、NSF等主要出版商均要求Alt Text以符合无障碍标准。

## 数据输入

JSON（完整功能）或 CSV（基础功能）。详见 `references/data-formats.md`。

**JSON柱状图示例:**
```json
{
  "labels": ["对照组", "实验组"],
  "series": {"治疗前": [75, 82], "治疗后": [68, 70]},
  "errors": {"治疗前": [3, 2], "治疗后": [2, 1]},
  "significance": {"治疗前:0": "***", "治疗后:1": "NS"}
}
```

**KM生存曲线示例:**
```json
{
  "groups": {
    "治疗组": [[12,1],[24,1],[36,0],[48,1],[60,0],[72,0]],
    "对照组": [[6,1],[10,1],[18,1],[30,1],[42,0],[48,1]]
  },
  "log_rank": {"p": 0.032, "method": "Log-rank"},
  "risk_table": {
    "times": [0, 12, 24, 36, 48],
    "治疗组": [50, 42, 35, 28, 20],
    "对照组": [50, 38, 25, 15, 8]
  }
}
```

**ROC曲线示例:**
```json
{
  "fpr": [0.0, 0.05, 0.10, 0.15, 0.30, 0.50, 1.0],
  "tpr": [0.0, 0.45, 0.68, 0.82, 0.92, 0.96, 1.0],
  "auc": 0.912,
  "ci": {"low": 0.854, "high": 0.958},
  "cutoff": {"fpr": 0.15, "tpr": 0.88, "threshold": 2.35}
}
```

## 版本历史

- **v1.5.0** (2026-06-17) — 新增3种图表：水平柱状图（hbar，含比率标注"4.96x"）、多面板组合图（composite，GridSpec布局，每面板任意图表类型）、架构/流程图（diagram，色块+箭头+分组标注）；新增GLM配色方案（GLM-5.2像素提取柔和配色：`#70A0D0`蓝+`#D09050`橙）；新增斜纹填充功能（`--hatch`，9种图案，打印友好）；新增 `--hatch`、`--show-ratio`、`--ratio-base`、`--horizontal` CLI参数；强制白底输出（出版标准）
- **v1.4.0** (2026-05-17) — 新增4种图表：Kaplan-Meier生存曲线（Log-rank检验、风险表、中位生存、删失标记）、ROC曲线（AUC、95%CI、最优截断点、多模型对比）、堆叠柱状图（构成比、百分比标签）、双Y轴折线图（临床评分+实验室指标同图展示）；扩展数据校验
- **v1.3.0** (2026-05-17) — 新增Okabe-Ito色盲安全配色（Nature Methods金标准）；DPI升级300→600线稿默认；新增PDF/TIFF/EPS输出；增强森林图（权重气泡、I²异质性、事件数列、分隔线）；无障碍Alt Text指南；智能DPI分场景
- **v1.2.0** (2026-05-16) — 新增版本元数据、依赖声明、负触发词、文件结构文档
- **v1.1.0** — 新增中文自动检测、CSV长格式自动转换、空数据校验
- **v1.0.0** — 初始版本：7种图表、4套配色、中文支持、统计标注
