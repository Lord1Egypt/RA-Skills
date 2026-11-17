# ecommerce-board-graphics · 电商UV荧光板产品图技能包

把「一张角色原图 / PSD」变成「可直接发给客户的 A5 板宣传图」的完整工作流。
规则来自真实生产环境的多轮迭代，已固化为可复用的脚本 + 文档。

## 快速开始

```bash
# 1. 紫光效果（单卡）
python scripts/uv_from_cut.py <png> <psd>          # 输出紫光效果图

# 2. 包边板子（A5内包边，横竖自适应）
python scripts/make_boards_v2.py

# 3. 宣传册（全部卡片 → 一册长图）
python scripts/make_catalog.py [ROOT] [OUT] [BORDER] [DIA] [COVER] [QR] [UVDEMO]
```

## 目录结构

```
project-01-电商产品图技能包/
├── SKILL.md                # 技能包主文档（规则清单 + 踩坑记录）
├── README.md               # 本文件
├── references/
│   ├── board-rule.md       # 包边规则（内包边 / 横竖版 / 高定钻石边 / 双面不包边）
│   └── uv-rule.md          # 紫光效果参数（光晕紧贴抠图，禁止发散）
├── scripts/
│   ├── psd_cutout.py       # PSD最上方可见非背景图层抠图
│   ├── uv_from_cut.py      # 抠图紫光效果（核心）
│   ├── uv_effect2.py       # 整图紫光效果（无PSD时回退）
│   ├── make_boards_v2.py   # 包边A5板子生成
│   └── make_catalog.py     # 宣传册生成（封面/分类/UV演示/二维码）
└── assets/
    └── uv_verify.png       # 紫光效果验证图
```

## 核心规则（详见 references/）

| 环节 | 关键规则 |
|------|---------|
| 抠图 | 读 PSD 最上方可见非"背景"图层；组的跳过、不可见的跳过 |
| 紫光 | 光晕高斯模糊 2.5px **紧贴抠图形状**；主体 ×1.45 + 紫偏移；核心区 ×1.55 |
| 包边 | **内包边不留白**；竖版 1052×1494，横版 1494×1052（边框旋转90°） |
| 高定 | 钻石包边素材 |
| 高位双面 | 不包边，正反两张左右并排 |
| 宣传册 | 分类花边框架；缎带标题；渐变底色；封面+UV演示+二维码；单册 <10MB |

## 踩坑清单（改版前必看）

1. 紫光发散 → 没用抠图 alpha 做蒙版。必须走 `uv_from_cut`。
2. 包边只显示两边 → 横版没旋转边框素材，或图片没铺满画布。
3. 竖版被压扁 → 横竖判断反了（`宽>高` 才是横版）。
4. 抠图位置偏移 → 抠图图层与原图尺寸不一致，必须 resize 到同一尺寸。
5. 宣传册 >10MB → 用降尺寸救急会糊；正确做法是压缩编码质量。
6. makima/3 特殊处理 → 不从文件夹 png 走，直接从其 PSD 提取原图合成。

## 依赖

- Python 3.10+
- Pillow, numpy, psd-tools
- Windows 字体（georgia / bahnschrift / msyh），缺失时回退默认字体

## 发布到 AI Agent 生态（OpenClaw / Claude Code）

1. 把 `SKILL.md` 放到 `skills/ecommerce-board-graphics/` 目录
2. 连同 `references/`、`scripts/` 一起作为 skill 包分发
3. 在 SKILL.md 头部保持 `name` / `description` 字段（已符合 OpenClaw skill 规范）
4. 可选：打包为 `.zip` 上传 ClawHub 技能市场
