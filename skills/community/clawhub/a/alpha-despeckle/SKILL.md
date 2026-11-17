---
name: alpha-despeckle
description: "Remove leftover speckle artifacts from transparent-background PNGs produced by matting or keying: semi-transparent haze remnants (alpha below threshold) and isolated island fragments (small connected alpha regions). Use when the user says 'clean up matting residue', 'remove specks on transparent PNG', 'despeckle', 'clear alpha noise', '清理抠像残留', '去透明底杂点', '去碎点'. Defaults to a dry-run report; writes back and auto-creates a byte-level backup only after confirmation."
metadata:
  displayName: "Alpha Despeckle (透明底去杂点)"
  category: "image-processing"
  slug: "alpha-despeckle"
  agent_created: "true"
  description_zh: "清除已完成抠像的透明底 PNG 中残留的细小像素块：半透明雾状残渣（alpha 低于阈值）与孤岛碎块（小面积 alpha 连通域）。当用户要求「清理抠像残留、去除 PNG 上的小碎点/杂点/残渣、despeckle、清透明底噪点」时使用。默认 dry-run 报告，确认后才写回并自动生成字节级备份。"
---

# Alpha Despeckle · 使用入口

> 真工具在 `scripts/alpha_despeckle.py`（零业务依赖，纯 cv2 / numpy / Pillow）。本文件是入口与用法。
> 注：`scripts/` 下的 `peninsula_*` 是 LunaPet 素材目检的项目专用脚本（含硬编码本地路径），**不属于本通用 skill 的发布范围**，本地留用即可，不随本 skill 发布。

## 何时用
已完成抠像的 RGBA 透明底 PNG 残留细小像素块：
- **半透明雾状残渣**（alpha 低于阈值）
- **孤岛碎块**（小面积 alpha 连通域飞溅）
当用户说「清理抠图残留、去透明底杂点、despeckle」时使用。

## 工具：`scripts/alpha_despeckle.py`
三道机制：
- **A 雾状残渣**：`alpha < --alpha-thresh`（默认 8）的像素直接归零。
- **B 孤岛碎块**：`alpha` 连通域面积 `< --min-area`（默认 12 px）整块归零。
- **C 安全阀**：面积前 `--keep-largest`（默认 1）的连通域永不删；删除量超过非透明像素 **30%** 时**拒绝执行**（需 `--force`）。

## 用法
```bash
# 先 dry-run 看报告（默认，不动文件）
python scripts/alpha_despeckle.py 素材.png

# 批量 + 实际写回（写回前自动 .despeckle.bak.png 备份）
python scripts/alpha_despeckle.py frames/*.png --apply

# 另存到目录、调参、看全部明细
python scripts/alpha_despeckle.py 素材.png --out clean/ --alpha-thresh 10 --min-area 20 --verbose
```
- 默认 **dry-run**：只打印报告，不碰文件。
- `--apply` 落盘前生成字节级备份（`.bak`）；`--no-backup` 不建议。
- 非 RGBA 文件自动跳过并告警；支持通配符批量。

## 依赖
`pip install opencv-python numpy pillow`。纯本地，无 AI 模型、无联网。

## 判据（何时该清）
- 边缘灰晕/黑边、发丝旁碎点、抠像后浮尘 → 先 dry-run，看 `removed_list` 的 bbox 与平均 alpha，确认都是残渣再 `--apply`。
- 打印 `refused` 说删除量 >30% → 参数过激，先调 `--alpha-thresh / --min-area`，别直接 `--force`。
