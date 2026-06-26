# 🎨 萤火虫创意工坊

**广州市萤火虫智能装备技术有限公司（萤火虫空压机）官方创意工具集**

[![Version](https://img.shields.io/badge/版本-2.0.0-green)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/平台-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)]()

---

## 📦 功能一览

| 分类 | 功能 | 依赖 | 模式 |
|------|------|------|------|
| 🖼️ 图片 | AI 背景移除（抠图） | rembg | 脚本模式 |
| 🖼️ 图片 | OCR 铭牌文字识别 | easyocr | 脚本模式 |
| 🖼️ 图片 | 缩放 / 裁剪 / 格式转换 | Pillow | 双模式 |
| 🎬 视频 | 剪切 / 拼接 / 配音合成 | FFmpeg | 脚本模式 |
| 🎤 音频 | AI 语音旁白（中/英文） | edge-tts | 脚本模式 |
| 🖥️ 3D | 互动式三维产品展示 | 无（CDN Three.js） | 原生模式 |
| 📄 网页 | 产品详情页（中英双语） | 无（Claude） | 双模式 |

### 双模式架构

- **模式 A（脚本）**：Python 脚本执行，输出确定，支持批量处理
- **模式 B（原生）**：Claude 直接生成，零依赖，灵活定制

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 必需 Python 包
pip install Pillow pyyaml

# 可选（扩展功能）
pip install rembg easyocr edge-tts

# 可选系统工具（视频功能需要）
# macOS:     brew install ffmpeg
# Linux:     apt install ffmpeg
# Windows:   https://ffmpeg.org/download.html
```

### 2. 环境检测

```bash
python scripts/install_deps.py --check-only
```

### 3. 试试看

```bash
# 从 YAML 配置生成产品详情页
python scripts/generate_detail_page.py -c demo/product-YDV75.yaml -o detail.html

# 产品照片抠图
python scripts/remove_background.py product.jpg -o ./output

# 生成 AI 语音旁白
python scripts/text_to_speech.py --text "萤火虫空压机，专注节能十五年" -o narration.mp3
```

**没有 Python？** 直接用中文告诉 Claude 你的需求就行——详情页和 3D 展示支持原生模式，无需任何依赖。

---

## 📁 文件结构

```
creative-studio/
├── SKILL.md                         # 核心指令集（~170 行）
├── README.md                        # 本文件
├── scripts/                         # Python 脚本
│   ├── install_deps.py              #   环境检测 & 一键安装
│   ├── remove_background.py         #   AI 背景移除（rembg）
│   ├── ocr_image.py                 #   OCR 铭牌识别（easyocr）
│   ├── text_to_speech.py            #   语音合成（edge-tts）
│   ├── video_edit.py                #   视频剪辑（FFmpeg）
│   └── generate_detail_page.py      #   详情页生成（PyYAML）
├── references/                      # 参考文档（按需加载）
│   ├── tools-reference.md           #   FFmpeg/Pillow 命令速查
│   ├── design-guidelines.md         #   品牌设计规范
│   ├── product-templates.md         #   产品 YAML 数据模板
│   └── video-specs.md               #   视频格式标准
└── assets/                          # 模板与资源
    ├── detail-page-template.html    #   详情页 HTML 模板
    ├── 3d-template.html             #   Three.js 3D 展示模板
    └── brand-logo.svg               #   公司 Logo
```

---

## 🎯 典型场景

1. **产品图处理**：去背景 → 统一尺寸 → 输出 Web 适配图片
2. **铭牌 → 详情页**：OCR 识别铭牌参数 → 自动填入产品配置 → 生成 HTML 详情页
3. **产品视频制作**：剪取精华片段 → 生成 AI 旁白配音 → 合成最终成片
4. **3D 产品展示**：从几何体构建交互式三维模型 → 输出可在浏览器直接打开的自包含 HTML
5. **快速生成详情页**：口头提供产品规格 → Claude 直接生成完整的中英双语产品页面

---

## 🏷️ 品牌信息

- **公司**：广州市萤火虫智能装备技术有限公司（萤火虫空压机）
- **官网**：http://www.fireflies.net.cn
- **热线**：13825202084（邹先生）
- **邮箱**：aifirefly@163.com
- **品牌色**：绿 `#1B8C3A` · 蓝 `#1565C0` · 橙 `#F57C00`

---

## 🔗 相关链接

- [ClawHub 发布指南](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
- [AgentSkills 开放标准](https://agentskills.io)
- [萤火虫空压机官网](http://www.fireflies.net.cn)
