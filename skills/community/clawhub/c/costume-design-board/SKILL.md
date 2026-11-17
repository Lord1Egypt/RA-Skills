---
slug: costume-design-board
name: costume-design-board
skill: costume-design-board
displayName: 舞台服装设计板
description: 为舞台服装设计生成标准化、专业级设计板拼合图与PDF。当用户要求将服装效果图/参考图拼合成设计板、生成服装设计板、做角色服装设计参考板、或需要统一多个角色服装方案的版式时触发。
version: 1.0.0
author: 衣述
metadata: {"openclaw": {"requires": {"python3": true, "pillow": true}, "install": ["pip install pillow"]}}
tags: [costume, design-board, fashion, stage, pdf, layout, image-collage, 服装设计, 舞台服装]
---

# 舞台服装设计板生成技能（本地版）

## 快速入口

- 脚本：`scripts/build_design_board.py`（以 skill 目录为基准）
- 参数表：`references/v9.1-layout-spec.md`

## 标准布局（V9.1 验证版）

- 画布：6528×3100 px（高清打印级）
- 左侧：3 张全身图横排（正/背/侧），保持原始比例，不裁切不变形
- 右侧：信息面板 + 2×3 特写网格
- 顶部：角色名 + 版本号 + 项目/角色/色调/面料关键词
- 底部：3 行设计说明
- 背景：纯黑 #0c0c0c

## 执行命令

```bash
python scripts/build_design_board.py \
  --src "generated-images/V6/jimeng-2026-07-06-4485" \
  --out "generated-images/V6/board" \
  --character "关盼盼" \
  --version "9.1" \
  --project "《浮生若梦》" \
  --role "盛唐情感巅峰 · 执念与体面" \
  --color "深绯红 · 古金 · 墨黑" \
  --fabric "织锦缎 / 暗纹提花"
```

## 输入文件命名约定

每个角色目录下准备 9 张图：
- `front*` 或 `01_*` — 正面全身
- `back*` 或 `02_*` — 背面全身
- `side*` 或 `03_*` — 侧面全身
- `chest*` 或 `04_*` — 胸口特写
- `back_opening*` 或 `05_*` — 背部开口特写
- `sleeve*` 或 `06_*` — 广袖特写
- `waist*` 或 `07_*` — 腰封特写
- `skirt*` 或 `08_*` — 裙摆特写
- `hair*` 或 `09_*` — 头饰特写

## 核心参数（已验证）

```python
MARGIN = 80
HEADER_HEIGHT = 280
FOOTER_HEIGHT = 260
SECTION_GAP = 90
FB_GAP = 44
DETAIL_GAP = 28
INFO_PANEL_HEIGHT = 260
INFO_TO_GRID_GAP = 40
FULL_BODY_TARGET_HEIGHT = 2400

BG_COLOR = (12, 12, 12)
DARK_PANEL = (32, 32, 32)
TEXT_WHITE = (255, 255, 255)
TEXT_GRAY = (190, 190, 190)
TEXT_GOLD = (210, 175, 120)
LINE_COLOR = (60, 60, 60)
```

## 踩坑提醒

- 标题 y=50，副标题 y=160，间距 ≥ 80，避免重叠
- 底部说明 y = canvas_height - FOOTER_HEIGHT + 30，避免贴边
- 字体优先 `simhei.ttf`，逐级回退到 `msyhbd.ttc` / `msyh.ttc` / `simsun.ttc`
- 全身图与特写色调不一致是生图模型局限，排版阶段用统一黑底尽量减少差异

## 项目上下文

- 当前项目：《浮生若梦》，新国风舞蹈餐秀，非历史复原
- 已完成角色：关盼盼
- 待推进角色：彭祖、项羽、虞姬、张天骥
