# ☕ 飞书长图切割工具 v1.0

> 将飞书长图按 4:3 比例切割成小红书友好的图片，自动去除底部 Logo

**作者：** 咖啡豆 ☕  
**日期：** 2026-03-20

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install Pillow
```

**可选（如果需要 OpenCV 高级功能）：**
```bash
pip install opencv-python numpy
```

### 2️⃣ 使用方法

#### 方式 A：命令行（推荐）

**基础用法：**
```bash
python cropper.py 飞书长图.png
```

**指定起始位置（跳过顶部 200px）：**
```bash
python cropper.py 飞书长图.png --start-y 200
```

**自定义参数：**
```bash
python cropper.py 飞书长图.png \
  --width 1440 \
  --height 1080 \
  --format jpg \
  --logo-height 150
```

**保留 Logo（不去除）：**
```bash
python cropper.py 飞书长图.png --keep-logo
```

#### 方式 B：GUI 界面

```bash
python cropper_gui.py
```

然后：
1. 点击"📁 选择图片"
2. 调整参数（可选）
3. 点击"🚀 开始切割"
4. 完成！

---

## 📐 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入图片路径（必需） | - |
| `-o, --output` | 输出目录 | `./output` |
| `--start-y` | 起始 Y 坐标（跳过顶部） | `0` |
| `--width` | 目标宽度 | `1440px` |
| `--height` | 目标高度 | `1080px` |
| `--format` | 输出格式（png/jpg） | `png` |
| `--keep-logo` | 保留 Logo | `False` |
| `--logo-height` | Logo 区域高度 | `120px` |

---

## 🎯 小红书图片规范

### 推荐尺寸
- **宽度：** 1440px（或 1080px）
- **高度：** 1080px（4:3 比例）
- **格式：** PNG 或 JPG
- **大小：** < 10MB

### 常见比例
| 比例 | 尺寸 | 用途 |
|------|------|------|
| **4:3** | 1440x1080 | 图文笔记（推荐） |
| **3:4** | 1080x1440 | 竖版封面 |
| **1:1** | 1080x1080 | 正方形图片 |
| **9:16** | 1080x1920 | 全屏封面 |

---

## 💡 使用技巧

### 1. 确定起始位置

飞书长图顶部可能有标题栏，建议先预览确定起始位置：

```bash
# 先用图片查看器打开，查看顶部需要跳过多少像素
# 然后用 --start-y 参数跳过
python cropper.py 飞书长图.png --start-y 200
```

### 2. 调整 Logo 高度

如果底部 Logo 去除不干净，调整 `--logo-height`：

```bash
# 增加 Logo 高度（去除更多）
python cropper.py 飞书长图.png --logo-height 150

# 减少 Logo 高度（保留更多内容）
python cropper.py 飞书长图.png --logo-height 80
```

### 3. 批量处理

用脚本批量处理多张图片：

```bash
# Windows PowerShell
Get-ChildItem *.png | ForEach-Object { python cropper.py $_.Name }

# Linux/Mac
for file in *.png; do python cropper.py "$file"; done
```

---

## 📁 输出示例

输入：`飞书文档_20260320.png`（高度 5000px）

输出目录：`./output/`

生成的文件：
```
飞书文档_20260320_20260320_113045_01.png  (1440x1080)
飞书文档_20260320_20260320_113045_02.png  (1440x1080)
飞书文档_20260320_20260320_113045_03.png  (1440x1080)
飞书文档_20260320_20260320_113045_04.png  (1440x1080)
飞书文档_20260320_20260320_113045_05.png  (1440x1080, 自动填充空白)
```

---

## ⚠️ 常见问题

### Q1: Logo 去除不干净
**A:** 调整 `--logo-height` 参数，增加或减少 Logo 区域高度

### Q2: 文字被切断了
**A:** 调整 `--start-y` 参数，或者手动检查切割位置

### Q3: 最后一张图太短
**A:** 工具会自动填充空白，不用担心

### Q4: 图片太模糊
**A:** 检查原图质量，或者调整 `--width` 和 `--height` 参数

### Q5: GUI 界面打不开
**A:** 确保安装了 tkinter（Python 自带，但有些系统需要单独安装）

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install python3-tkinter

# macOS (通常已安装)
brew install python-tk
```

---

## 🔄 更新日志

### v1.0 (2026-03-20)
- ✅ 基础切割功能
- ✅ 自动去除 Logo
- ✅ 空白填充
- ✅ 命令行版本
- ✅ GUI 版本

---

## 📝 TODO

- [ ] 智能检测 Logo 位置（不用手动设置高度）
- [ ] 智能检测文字边界（避免切断）
- [ ] OpenCV Inpaint 高级去水印
- [ ] 预览切割效果
- [ ] 批量处理多张图片
- [ ] 飞书机器人集成

---

## 📄 许可证

MIT License

---

## 🙏 反馈

有问题或建议？联系咖啡豆 ☕
