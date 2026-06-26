---
name: cad-editor
author: 王教成 Wang Jiaocheng (波动几何)
description: >
  CAD制图编辑器 — 用自然语言生成工程图纸（建筑平面图/机械零件/电气布置/管道系统/结构详图）。
  支持DXF文件创建、渲染预览、批量导出。触发词：画平面图、CAD、工程图、建筑图、机械图、电气图、
  管道图、结构图、画线/圆/矩形/多边形、尺寸标注、DXF、AutoCAD、施工图、配筋图、齿轮、轴承、
  阀门、弯头、三通、法兰、门窗、楼梯、墙体、梁板柱基础、螺栓螺母弹簧垫圈销钉键槽、
  开关插座灯具配电箱断路器导线组、直管弯头阀门法兰大小头管帽。
---

# CAD Editor Skill

将自然语言指令转换为工程图纸（DXF + PNG/SVG/PDF）。覆盖建筑、机械、电气、管道、结构五大领域，
遵循 GB/T 制图标准。

## 触发条件

当用户要求绘制 CAD 图纸、工程图、施工图、配筋图，或提及以下任一领域时使用本技能：
- 建筑图纸：平面图、立面图、剖面图、门窗、楼梯、墙体、梁板柱基础
- 机械图纸：螺栓、齿轮、轴承、弹簧、垫圈、螺母、销钉、键槽
- 电气图纸：开关、插座、灯具、配电箱、断路器、导线组
- 管道图纸：直管、弯头、三通、法兰、阀门、大小头、管帽
- 结构详图：梁断面、楼板配筋、条形基础、独立基础
- 通用几何：线、圆、弧、矩形、多边形、尺寸标注

## 工作流

### 步骤 1：解析自然语言指令

调用 NL 解析器识别意图并提取参数：

```python
import sys
sys.path.insert(0, 'cad-editor/scripts')

from nl_parser.intent_classifier import IntentClassifier
from nl_parser.param_extractor import ParamExtractor

classifier = IntentClassifier()
intent = classifier.classify(user_input)       # → intent_dict
extractor = ParamExtractor(intent['domain'])
params = extractor.extract(user_input)          # → param_dict
```

`references/intent_templates.json` 包含 52 条预定义意图映射模板，涵盖 6 大类图纸。

### 步骤 2：生成绘图脚本

根据意图类型调用脚本生成器：

```python
from nl_parser.script_generator import ScriptGenerator

gen = ScriptGenerator()
script_code = gen.generate(intent, params)      # → Python str
```

生成器内置 18 套脚本模板，按领域分：
| 领域 | 模板数 | 覆盖组件 |
|---|---|---|
| architectural | 5 | 墙/门/窗/柱/楼梯 |
| mechanical | 4 | 螺栓/齿轮/轴承/弹簧 |
| electrical | 3 | 开关/插座/灯具/导线组 |
| piping | 3 | 直管/弯头/三通/阀门 |
| structural | 3 | 梁断面/楼板/基础 |

### 步骤 3：执行脚本生成 DXF

```python
# 将 script_code 写入临时文件后执行，或直接 exec
exec(script_code)
# 输出：{output_dir}/{name}.dxf
```

### 步骤 4：渲染预览图片

```python
from core.renderer import Renderer
Renderer.render_quick(doc, output_dir='output', name='drawing_name')
# 输出：{output_dir}/drawing_name.png (自动生成)
```

### 步骤 5：交付结果

向用户展示 PNG 预览图，同时提供 DXF 文件路径。

## 直接 API 调用方式（跳过 NL 解析）

当需要精确控制或编程调用时，直接使用 Python API：

```python
import sys
sys.path.insert(0, 'cad-editor/scripts')

from core.document import CADDocument
from core.renderer import Renderer
from layer.manager import LayerManager
from layer.linetypes import Linetypes
from entities import *
from templates.architectural import ArchitecturalTemplates
from dimension import LinearDimension
from layout.paperspace import PaperSpace

doc = CADDocument.new(version='R2010')
msp = doc.modelspace()

Linetypes.load_standard(doc)
LayerManager(doc).setup_template('arch')

ArchitecturalTemplates.wall(msp, [(0,0), (5000,0), (5000,3500), (0,3500)], thickness=240)
ArchitecturalTemplates.door_single(msp, (2500, 0), width=900)
ArchitecturalTemplates.window(msp, (800, 240), (2000, 240))
LinearDimension.chain_horizontal(msp, [(0,-600),(0,0),(5000,0),(5000,-600)], offset=800)
PaperSpace.draw_title_block(msp, (0,0), size='A3', title='图纸标题')

CADDocument.save(doc, 'output/drawing.dxf')
Renderer.render_quick(doc, output_dir='output', name='drawing')
```

## 支持的图纸类型与指令示例

### 建筑制图 (GB/T)
| 指令示例 | 生成内容 |
|---|---|
| `画一个4000x3000的建筑平面图` | 外墙+门+窗+标注+图框 |
| `3600x4800房间开一扇900宽的门两扇1200的窗` | 指定尺寸的户型 |
| `画一个双开门1500mm` | 双扇平开 |
| `12步直跑楼梯宽度1200` | 楼梯平面+折断线+方向箭头 |

### 机械制图 (GB/T)
| 指令示例 | 生成内容 |
|---|---|
| `M16六角螺栓头俯视图` | 六角头+内切圆+中心十字线 |
| `20齿齿轮端面视图D100` | 齿顶圆+齿根圆+轴孔+径向齿形线 |
| `轴承6205侧面图` | 内外圈+滚动体 |
| `压缩弹簧线径2外径16有效圈数6` | 锯齿形侧视图 |

### 电气制图
| 指令示例 | 生成内容 |
|---|---|
| `单极开关符号垂直放置` | 圆触点+倾斜动触杆+引线 |
| `三孔电源插座` | 半圆弧+底边+孔位 |
| `吸顶灯符号` | 圆形灯具标记 |
| `三相导线组间距30mm` | 三条平行导线 |

### 管道/暖通
| 指令示例 | 生成内容 |
|---|---|
| `DN50直管段带中心线` | 双线管+轴线 |
| `90度弯头R100 DN50东北走向` | 双线圆弧弯头 |
| `闸阀DN50` | 阀体+手轮 |
| `三通DN50/DN30` | 主管+支管接头 |

### 结构详图
| 指令示例 | 生成内容 |
|---|---|
| `250x500梁断面配3根16底部钢筋` | 截面轮廓+箍筋+纵筋+混凝土填充 |
| `楼板120厚双向配筋12@150/10@200` | 板轮廓+钢筋线+弯钩+标注 |
| `500x500柱下独立基础2000x2000深600` | 台阶式基础+受力筋+分布筋+标注 |

### 通用几何
| 指令示例 | 生成内容 |
|---|---|
| `画一个矩形400x300` | 矩形 |
| `正六边形外接圆半径100` | 正多边形 |
| `圆心(0,0)半径50的圆和直径80的同心圆` | 同心圆组 |

## 输出格式

| 格式 | 用途 |
|---|---|
| `.dxf` | 主输出，可导入 AutoCAD / FreeCAD / 中望CAD |
| `.png` | 快速预览（自动生成） |
| `.svg` | 矢量可缩放预览 |
| `.pdf` | 打印/交付文档 |

## 依赖库

| 库 | 用途 | 安装 |
|---|---|---|
| `ezdxf` | DXF 读写引擎 | 必须 |
| `matplotlib` | PNG/SVG/PDF 渲染后端 | 必须 |
| `numpy` | 数值计算 | 必须 |

安装命令：`pip install ezdxf matplotlib numpy`

## 架构与文件组织

```
cad-editor/
├── SKILL.md                        # 本文件（技能说明书）
├── scripts/                        # 可执行代码
│   ├── nl_parser/                  # 自然语言解析器
│   │   ├── intent_classifier.py    #   意图分类（19 种规则）
│   │   ├── param_extractor.py     #   参数提取（5 大领域）
│   │   └── script_generator.py    #   脚本生成（18 套模板）
│   ├── core/                      #   文档创建 / 单位管理 / 渲染引擎
│   ├── entities/                  #   基础实体（线/圆/弧/多段线/文字）
│   ├── layer/                     #   图层管理 / 线型加载 / 行业图层模板
│   ├── dimension/                 #   标注（线性/径向/角度/引线）
│   ├── block/                     #   图块定义与插入
│   ├── hatch/                     #   图案填充（混凝土/砖/金属等）
│   ├── tools/                     #   编辑工具（偏移/裁剪/阵列/镜像/圆角倒角/测量）
│   ├── layout/                    #   图纸空间 / 视口 / 图框标题栏
│   ├── export/                    #   批量导出 SVG/PDF/PNG
│   └── templates/                 #   行业图库组件
│       ├── architectural.py       #     建筑（墙/门/窗/柱/楼梯/阳台）
│       ├── mechanical.py          #     机械（螺栓/齿轮/轴承/弹簧/键槽/垫圈/螺母/销）
│       ├── electrical.py          #     电气（开关/插座/灯具/导线/配电箱/断路器）
│       ├── piping.py              #     管道（直管/弯头/三通/阀门/法兰/大小头/管帽）
│       └── structural.py           #     结构（梁断面/楼板配筋/条基/独立基础）
├── references/                     # 参考文档（按需加载）
│   ├── color_index.md             #   ACI 颜色表(256色) + 行业配色规范
│   ├── layer_standards.md         #   GB/T 图层命名规范
│   ├── dxf_entity_codes.md        #   DXF 组码速查 + ezdxf API 映射
│   └── intent_templates.json      #   52 条 NL→参数映射模板
└── assets/                         # 输出资源（不加载到上下文）
    ├── fonts/                     #   CAD 字体文件
    ├── hatch_patterns/            #   自定义填充图案
    ├── linetypes/                 #   线型定义
    └── title_blocks/              #   图框标题栏模板（A0-A4）
```

## 参考文档索引

| 文档 | 内容 | 加载时机 |
|---|---|---|
| `references/color_index.md` | ACI 256 色表 + 建筑/机械/电气/管道/结构配色方案 | 需要设置颜色时 |
| `references/layer_standards.md` | GB/T 17825 图层命名规范，含 5 大行业预设 | 创建文档/设置图层时 |
| `references/dxf_entity_codes.md` | DXF 组码速查表 + ezdxf Python API 对照 | 操作底层实体时 |
| `references/intent_templates.json` | 52 条意图模板（NL 正则匹配→参数提取规则）| NL 解析阶段自动读取 |
