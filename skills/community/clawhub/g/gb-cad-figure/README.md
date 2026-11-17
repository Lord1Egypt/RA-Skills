# gb-cad-figure · 国标·CAD·图形

**gb-cad-figure = GB(中国国标) + CAD(计算机辅助设计) + figure(图形/图幅)**

一套按中国国家标准 **GB/T** 自动生成正式工程图纸与 CAD 文件的开源工具：从实体图元（平滑回转体 lathe / 圆柱 cyl / 立方体 box）自动选图幅、排图框、生成标题栏、国标尺寸标注、技术说明与图例，并交付 **PDF + DXF + DWG** 三种格式。

本仓库既是**可直接运行的 Python 工具**，也可作为 **AI 技能（skill）** 让模型调用自动出图。

## Features
- GB/T 标准图幅（A0~A4）**自动选幅 + 标准比例**
- 图框 / 标题栏 / 图例 / 技术说明 全参数化自适应布局
- **平滑回转体（lathe）**正等轴测 · 点画中心线贯穿 · 瓶底拱形前缘 · **引线式标注（LDIMS）不穿实体**
- **box 建筑体等轴测 & 全局遮挡去隐藏线**：开口房间/库房墙体（墙厚/内墙角/外墙角线条处理），三灰面填充示例
- **图片描摹 → CAD 转换强模块**：从参考照片/效果图到正式国标工程图的端到端流程（看图提取→尺寸可靠性排序→实体建模→细节线条→轴向标注→三格式交付）
- 标题栏**四行布局**：标签格+填写格分离、填写格宽度按内容长短分配
- 中文字体防方块；出图自动自检（字体 / 线连接闭合 / 遮挡 / 布局）
- **三格式交付**：PDF（查看/打印）+ DXF（可编辑）+ DWG（ODA 转换，默认 ACAD2018）

---

## 一、系统要求
- **Python 3.8+**
- 需安装依赖：`ezdxf`（DXF）、`reportlab`（PDF）、`PyMuPDF`/`fitz`（渲染校验）
- **中文字体**：系统需装有中文字体（如 HarmonyOS Sans、仿宋、思源黑体），否则 PDF/DXF 中文会变方框
- **转 DWG（可选）**：需 `Xvfb`（虚拟显示）；ODA File Converter 首次转换时自动下载，无需手动安装

## 二、安装
```bash
pip install ezdxf reportlab pymupdf

# 仅当你需要产出 DWG 时（无头 Linux 需虚拟显示）
sudo apt-get install -y xvfb   # Debian/Ubuntu
```

## 三、快速开始（命令行）
```bash
# 1) 生成图纸 → 用内置示例直接跑引擎（输出 PDF + DXF）
python3 scripts/gb_figure.py

# 2) 校验 DXF 中文字体（防方块，出图后必跑）
python3 scripts/check_dxf_fonts.py 输出.dxf

# 3) 单个 DXF 转 DWG（首次自动下载 ODA 转换器，约 82MB）
bash scripts/dxf2dwg.sh 输入.dxf 输出目录/
```

## 四、生成自定义图纸（编程式，推荐）
核心入口是 `scripts/gb_figure.py` 的 `generate()` 函数。写一个 Python 脚本调用它即可。

```python
import sys
sys.path.insert(0, "scripts")          # 指向 gb-cad-figure/scripts
from gb_figure import generate

# 主体图元：'lathe' = 回转体，轮廓用 (高度z, 半径r) 折点描述（自动平滑）
ENT = [('lathe', 0, 0, [
    (0, 28.5),   # 瓶底 R28.5 (Ø57)
    (55, 28.5),  # 直壁
    (78, 26.2),  # 腰部凹槽(向内收)
    (134, 28.5),
    (166, 23),   # 肩部下收
    (189, 11),   # 瓶颈 R11
    (200, 13),   # 瓶盖 R13
])]

# 引线式尺寸标注：(文本, 锚点x,y,z, 引出方向dx,dy,dz)
LDIMS = [("Ø57", 28.5,0,90, 46,0,12), ("Ø22", -11,0,184, -38,38,16), ("200", -28.5,0,0, -46,-22,0)]
tech  = ["1  材料: PET(聚对苯二甲酸乙二醇酯)。", "2  壁厚 t=0.3mm。"]
leg   = [("粗实线 — 可见轮廓线", True), ("点画线 — 中心线", False)]

generate("矿泉水瓶", "WB-01", ENT, [], "2026.08.09",
         "/tmp/bottle", tech, leg,
         LDIMS=LDIMS, lathe_ribs=[170,187,200,213,237,250,263,280],
         bot_visible='front', rib_side='front')
# 产出 /tmp/bottle.pdf + /tmp/bottle.dxf
```

### generate() 主要参数
| 参数 | 含义 |
|---|---|
| `ENT` | 主体图元列表：`lathe`(回转体, [(z,r)])、`cyl`(圆柱, cx,cy,r,z0,z1)、`box`(长方体, cx,cy,a,b,z0,z1) |
| `LDIMS` | 引线式标注 `(文本, ax,ay,az, dx,dy,dz)`，从轮廓点引出、不穿实体 |
| `direction` | `'auto'`（默认，按幅面定横/竖）/ `'vs'` 竖版 / `'hb'` 横版 |
| `lathe_ribs` | 回转体素线角度列表，推荐屏幕等距、左右对称、中间留给中心线 |
| `bot_visible` | `'front'` 画标准正等轴测（长轴水平椭圆底面） |

### 可用图元
- `('lathe', cx, cy, [(z,r),...])`：回转体/瓶/罐/圆锥/轴——轮廓点自动 Catmull-Rom 平滑
- `('cyl', cx, cy, r, z0, z1)`：圆柱
- `('box', cx, cy, a, b, z0, z1)`：长方体（半宽 a、半深 b、z0~z1 高度）

## 五、三格式产出流程
1. **PDF + DXF**：直接由 `generate()` 生成（纯本地，无外部网络依赖）
2. **DWG**：`bash scripts/dxf2dwg.sh x.dxf dir/` → 用 ODA File Converter 转换（首次自动下载 82MB，之后复用）

---

## 六、常见问题（FAQ）
| 问题 | 解决 |
|---|---|
| PDF/DXF 中文显示方框/乱码 | 系统未装中文字体 → 安装 Harmony/仿宋/思源字体；DXF 跑 `check_dxf_fonts.py` 校验 |
| DWG 转换失败 | 确认已安装 `xvfb`；检查网络能否下载 ODA；可手动放转换器到 `scripts/tools/ODAFileConverter.AppImage` |
| 图面/标注出框或重叠 | 引擎会自动选幅；若标注贴框可调 `LDIMS` 引线方向/长度 |
| 标注压到轮廓/素线 | `LDIMS` 锚点避开轮廓点，方向放射引出 |
| 回转体底面不是椭圆 | 需传 `bot_visible='front'` 才会画长轴水平的标准椭圆底面 |

## 目录结构
```
scripts/
  gb_figure.py               # 引擎：生成 PDF + DXF（选幅/标题栏/标注/中心线/拱形底/回转体）
  isometric_occlusion.py     # 等轴测全局遮挡去隐藏线（纯圆柱场景通用工具）
  check_dxf_fonts.py         # 中文字体验证
  dxf2dwg.sh                 # DXF→DWG 转换（首次自动下载 ODA + xvfb-run）
  tools/fetch_oda.sh         # 自动下载 ODAFileConverter.AppImage(~82MB)
  examples/
    stool_iso.py             # 混合 cyl+box 方凳等轴测示例
    gen_storage_A3_fill.py   # 开口库房(墙厚)等轴测 + 三灰面填充完整示例
SKILL.md                # 给 AI/模型 的调用指南
README.md               # 给使用者 的说明（本文档）
```

## Keywords / Topics
`gb` `cad` `figure` `engineering-drawing` `autocad` `isometric` `dimension` `titleblock` `dxf` `dwg` `国标` `工程图` `机械制图` `建筑制图` `CAD图纸` `等轴测` `尺寸标注` `图框` `标题栏`

## Tech Stack
- Python 3 · [ezdxf](https://ezdxf.mozman.at/)（DXF）· ReportLab（PDF）· ODA File Converter（DWG）

## License
MIT（开源建议）
