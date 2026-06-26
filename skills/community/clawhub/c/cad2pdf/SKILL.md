---
name: cad2pdf
description: CAD图纸转矢量PDF - 支持DWG/DXF，自动按图框拆页，完整渲染中文、标注、填充
version: 2.0.0
author: 老狗
tags: [cad, dxf, dwg, pdf, 矢量, 工程图纸, 建筑, 造价]
license: MIT
---

# CAD2PDF v2 - CAD图纸转矢量PDF

## 一句话介绍
CAD图纸发过来，一条命令出多页矢量PDF——自动按图框拆页、完整渲染填充/标注/中文。

## 解决什么问题？
- CAD图纸发微信：对方没CAD软件？→ 转PDF直接看
- 多图框图纸：一张DWG里有N个大样？→ 自动拆成N页PDF
- 中文乱码：天正CAD文字显示不全？→ MBCS编码自动解码
- HATCH填充丢失：转PDF后材质看不出来？→ ezdxf原生渲染，完整保留

## 核心特性
- 📐 **ezdxf原生渲染引擎** - HATCH填充/尺寸标注/块引用完整渲染
- ✂️ **自动拆页** - 检测粉紫色图框，每框一页
- 🔍 **大样图检测** - 自动检测图框外实体聚集区域，独立页面
- 🈶 **天正MBCS解码** - `\M+5CDE2` → "外"，中文不乱码
- 📏 **DIMENSION修复** - 标注insert在原点时自动移到实际位置
- 🔢 **索引圆圈编号补全** - ODA转换丢失的SHX编号自动补绘
- 🎨 **黑白输出** - 适配打印，不同材质用不同灰度区分

## 依赖安装

### Python依赖
```bash
pip install ezdxf matplotlib --break-system-packages
```

### 系统依赖（DWG转DXF才需要）
```bash
# ODA File Converter
wget "https://www.opendesign.com/guestfiles/get?filename=ODAFileConverter_QT6_lnxX64_8.3dll_27.1.deb" -O /tmp/ODAFileConverter.deb
sudo dpkg -i /tmp/ODAFileConverter.deb
sudo apt-get install -y libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xkb1

# 中文字体
sudo apt-get install -y fonts-noto-cjk
```

## 使用方法

### 基本用法
```bash
# DXF转PDF
python3 scripts/dxf2pdf.py 图纸.dxf 输出.pdf

# 指定纸张和DPI
python3 scripts/dxf2pdf.py 图纸.dxf 输出.pdf --paper A3 --dpi 300

# DWG文件（自动先转DXF）
bash cad2pdf.sh 图纸.dwg 输出.pdf
```

### Shell封装
```bash
bash cad2pdf.sh 图纸.dxf                    # 自动命名输出
bash cad2pdf.sh 图纸.dxf 输出.pdf --paper A2
```

### 命令行参数
- `--paper SIZE` - 纸张大小：A0/A1/A2/A3/A4（默认A3，宽度固定，高度按图框比例自适应）
- `--dpi N` - 输出分辨率（默认300）

## 技术架构

```
输入DXF
  ↓
[预处理]
  ├─ MBCS解码: \M+XXXXX → GBK中文
  ├─ Unicode解码: \U+XXXX → 字符
  ├─ %%编码: %%c→Ø, %%d→°, %%p→±
  ├─ DIMENSION修复: insert(0,0) → 实际位置
  ├─ 字体替换: STXIHEI.SHX → Noto Sans CJK
  └─ 圆圈编号补全: 空圆圈 → 自动编号
  ↓
[页面检测]
  ├─ 粉紫色图框(颜色6) → 主图页
  └─ 实体聚集区域聚类 → 大样图页
  ↓
[ezdxf原生渲染]
  ├─ HATCH填充(完整保留)
  ├─ DIMENSION标注
  ├─ TEXT/MTEXT文字
  ├─ LINE/ARC/CIRCLE
  └─ INSERT块引用
  ↓
[多页PDF输出]
  ├─ 宽度固定A3
  ├─ 高度按图框比例自适应
  └─ 视图裁剪到图框范围
```

## 已知限制
- 大样图检测基于网格聚类，极分散的实体可能误判
- 天正自定义HATCH图案名（`\M+`编码）无法显示为中文名
- 需要STXIHEI.TTF等原版字体才能完美显示天正标注样式

## 文件结构
```
cad2pdf/
├── SKILL.md              # 本文档
├── cad2pdf.sh            # Shell封装（支持DWG/DXF）
└── scripts/
    └── dxf2pdf.py        # 核心Python脚本
```
