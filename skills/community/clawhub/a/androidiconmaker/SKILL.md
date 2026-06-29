---
version: 1.0.0
name: androidiconmaker
description: 将任意图片（JPG/PNG）转换为 Android 应用图标（mipmap 格式），自动裁剪为圆形并生成 mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi 全套分辨率。触发场景：用户发了一张图片并说「做成 App 图标」「把这个设为应用图标」「生成安卓图标」「做个图标吧」「图片转图标」「安卓图标生成器」；或英文「make this an app icon」「generate android icon」「convert to android icon」「android icon maker」。
---

# 安卓图标生成器 / Android Icon Maker

将用户发来的图片转换为 Android mipmap 图标，圆形裁剪，自动输出全套分辨率。

## 使用方式

用户发图片 + 说「做成 App 图标」/ "make this an app icon" 等 → 调用脚本处理。

## 脚本用法

```bash
python3 scripts/make_round_icon.py <图片路径> <输出目录> [基准尺寸]
```

- **图片路径**：JPG 或 PNG 文件完整路径
- **输出目录**：生成图标的目录（默认 `android_icons`）
- **基准尺寸**：mdpi 对应 dp 值（默认 48）

**示例**：
```bash
python3 scripts/make_round_icon.py /path/to/photo.jpg /path/to/output
```

生成文件：
```
android_icons/
├── icon_mdpi.png    (48x48)
├── icon_hdpi.png    (72x72)
├── icon_xhdpi.png   (96x96)
├── icon_xxhdpi.png  (144x144)
└── icon_xxxhdpi.png (192x192)
```

## 依赖（必须先安装）

使用前必须安装 Pillow，否则脚本报错。

```bash
# 检查是否已安装
python3 -c "from PIL import Image; print('Pillow 已安装')"

# 安装（Linux/macOS/Windows 均适用）
pip install pillow

# 如果提示权限不足，加 --break-system-packages（Linux）
pip install pillow --break-system-packages
```

**安装失败时的错误信息**：`ModuleNotFoundError: No module named 'PIL'`

## 注意事项

- 图片会自动居中裁剪为正方形
- LANCZOS 算法缩放，质量优先
- 透明通道保留，支持圆形蒙版
- **默认输出位置**：当前目录下的 `android_icons/` 子目录（如不指定输出目录）
- **可指定输出目录**：第二个参数可自由指定任意路径
- **输出到 Android 项目**：如果要将图标直接复制到 Android 项目的 `mipmap-*` 目录，必须先询问用户要放到哪个项目，或者直接把生成的图片发给用户，避免覆盖错误项目的图标
