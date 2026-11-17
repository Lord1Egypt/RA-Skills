# 身体化妆：腿脚肤色统一（ComfyUI / z-image-turbo）

针对「真人生成时腿、脚偏黑，局部有褐色块」的两层修复。2026-11-08 实测于 Voiana 套图。

## 为什么会偏黑

1. 角色卡对**裸露腿部没有任何肤色约束**，模型把腿画进阴影里，整体比脸/手臂暗 12–16 个 L*。
2. 原 FACE 段写了 `slight uneven tone`（轻微不均匀），在腿部被放大成灰褐色斑驳。
3. 茶色地面反光 + 腿部处于身体阴影，抬亮前先发灰。

## 第一层：提示词 SKIN 段（治本）

在 FACE 与 COSTUME 之间新增一段，并把 FACE 的 `slight uneven tone` 删掉：

```
SKIN: one even warm light beige skin tone with a soft peach undertone from her face all the
way down to her feet, the neck, shoulders, arms, thighs, knees, shins, ankles and the tops of
her feet all the same healthy tone, softly powdered and evenly toned like a sheer body
foundation, gentle natural shading kept along the calves and knees, smooth clear skin with
fine real texture, the legs warm and softly lit, the same tone as her face, like a cosplayer
who has applied body makeup before the shoot.
```

灯光句再加一句正面暖反弹光：

```
soft warm fill from the right and a soft warm bounce from the front that keeps the legs,
knees and feet evenly lit and the same tone as her face
```

效果：褐斑从源头基本消失、腿脚不再被画进阴影；但单靠提示词会偏苍白偏灰（b* 掉到 3–6），要配第二层补暖。

## 第二层：P7b 身体化妆（兜底，轻量）

`skin_makeup.py`（纯 numpy + Pillow，无 scipy/cv2）：

```
python D:\DSH\workspace\skin_makeup\skin_makeup.py final_01.png deliver\01_xxx.jpg
# 可选：--strength 0.35 --leg-strength 0.85 --debug mask.png
```

只动**腿脚**（y 0.32 以下渐变生效），脸和手臂一个像素都不改：

- 参考肤色取「上胸/手臂」皮肤的中位 L*a*b*，作为腿部目标（比取脸部高光稳定）。
- 曝光：用「皮肤自身的低频亮度」和目标的差做**加法平移**（不是乘法提亮），毛孔与腿型阴影原样保留，不会把斑块衬得更脏。
- 偏色：先在皮肤自身的局部均值上压掉小尺度偏黄/偏红（褐斑、灰斑），再把整体色度拉向参考色；纹身、贴布按色相距离保护，不参与修正。
- 轮廓：修正权重在离皮肤边缘 1–6px 内淡出，贴边像素保持原样 → **不会出现贴着背景的亮边/光晕**。
- 结果：腿脚明度抬 10–14 L，色度回到与手臂一致，且保留毛孔、膝窝阴影与纹身。

### 参数选择

| 情况 | 用法 |
|---|---|
| 默认（推荐） | `--strength 0.35 --leg-strength 0.85` |
| 腿只是略暗 | `--leg-strength 0.60` |
| 腿特别黑（如 final_04） | `--leg-strength 0.95` |
| 想保留更多原始斑驳 | `--leg-strength 0.50` |

上限别超过 1.0：超过就会开始像磨皮。**不要**对同一张图重复跑，参考色会随图变化，越跑越白。

## 实测（1440×2560，皮肤掩码中位数 L* / a* / b*，按人物实际高度归一化分带）

| 图 | 部位 | 修复前 | 修复后 |
|---|---|---|---|
| final_03d | 手臂/胸 | 78.7 / 7.3 / 8.9 | 78.7 / 7.2 / 9.0（不变） |
| final_03d | 大腿 | 62.9 / 8.8 / 5.9 | 73.4 / 9.0 / 7.9 |
| final_03d | 膝 | 63.6 / 10.0 / 7.6 | 74.7 / 9.2 / 9.0 |
| final_03d | 小腿 | 55.5 / 9.5 / 6.5 | 69.3 / 9.2 / 8.4 |
| final_03d | 脚背 | 57.3 / 9.4 / 5.6 | 70.4 / 9.0 / 7.9 |
| final_04 | 手臂/胸 | 77.9 / 7.3 / 7.7 | 77.9 / 7.3 / 7.9（不变） |
| final_04 | 大腿 | 61.3 / 9.9 / 4.7 | 73.6 / 9.3 / 6.8 |
| final_04 | 小腿 | 55.8 / 11.1 / 4.4 | 69.7 / 9.7 / 6.6 |
| final_04 | 脚背 | 55.7 / 11.9 / 6.0 | 68.6 / 9.9 / 7.2 |

腿脚与手臂的明度差从 14–23 压到 4–9（保留「腿在下、光更少」的正常落差），偏红偏黄的斑块色度向手臂靠拢，sd 也明显收敛。

## 已知边界

- 旧图里极顽固的褐色细点只能淡化（约 2–4px，正常观看不可见）；强行抹掉就会变成塑料皮，所以不追求 100% 消失。
- 新图（带 SKIN 段生成）几乎没有这类斑点，P7b 只做轻修，效果最自然。
- 银鞋带、浅色金属已按低彩度排除，但贴边处可能被轻微柔化；小件建议整张重出。
- 深色长袜、网袜不处理（遮罩避开）。
- 纹身会保留形状，颜色可能略被压淡；重色纹身建议出图后贴。

## 文件

- `skin_makeup.py` — 主脚本（`--debug` 导出遮罩）
- `_analyze.py` — 按人物高度归一化的分带 Lab 统计
- `_cmp.py` — before/after 1:1 对照拼图
- `_demo.py` — 全身 + 腿脚裁切的 2×2 验收图
- `demo_before_after.jpg` / `_01` / `_04` — final_03d / 01 / 04 的修复对照
- `draft_skin03.png` / `draft_skin03_fix.jpg` — 新卡（SKIN 段）出图与轻修后效果
