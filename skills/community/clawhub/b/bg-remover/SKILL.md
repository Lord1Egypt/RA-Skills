---
name: bg-remover
description: "Remove, replace, or blur image backgrounds using AI-powered segmentation (rembg/U2-Net). Use when the user asks to: (1) remove image background / make transparent, (2) replace background with a color or another image, (3) blur background like portrait mode, (4) cut out / extract foreground subject from a photo. Triggers on keywords like 抠图, 去背景, 换背景, 背景模糊, 透明背景, remove background, replace background, blur background, cutout."
---

# bg-remover — 图片背景处理

基于 rembg (U2-Net) 的本地 AI 抠图工具，支持去除背景、替换背景、背景模糊。

## 依赖安装

首次使用前运行安装脚本：

```bash
bash {baseDir}/scripts/install.sh
```

或手动安装：`pip install rembg Pillow numpy onnxruntime`

## 命令

所有操作通过 `{baseDir}/scripts/bg_remove.py` 执行：

### 去除背景（输出透明 PNG）

```bash
python3 {baseDir}/scripts/bg_remove.py remove <input> [-o output.png]
```

### 替换背景

```bash
# 纯色背景（支持 hex、rgb、颜色名）
python3 {baseDir}/scripts/bg_remove.py replace <input> -c "#FF0000" [-o output.png]
python3 {baseDir}/scripts/bg_remove.py replace <input> -c white [-o output.png]

# 图片背景
python3 {baseDir}/scripts/bg_remove.py replace <input> -i bg.jpg [-o output.png]
```

### 背景模糊（人像模式）

```bash
python3 {baseDir}/scripts/bg_remove.py blur <input> [-r 15] [-o output.png]
```

`-r` 控制模糊半径，值越大越模糊，默认 15。

## 输出

- 默认输出路径为原文件名加后缀：`_nobg.png`（去除）、`_newbg.png`（替换）、`_blur.png`（模糊）
- 所有输出均为 PNG 格式
- 使用 `-o` 参数自定义输出路径

## 注意事项

- 首次运行会自动下载 U2-Net 模型（约 170MB），需要网络
- 处理大图可能较慢，建议先缩小再处理
- 抠图效果取决于前景与背景的对比度，简洁背景效果更好
