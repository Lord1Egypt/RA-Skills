# Boss 直聘职位沟通自动化 Skill

## 📋 概述

这是一个完整的 Boss 直聘职位沟通自动化技能，能够：
- 自动滚动浏览职位列表
- 点击职位查看详情
- 截取职位描述区域
- 使用 OCR 识别技术关键词
- 智能匹配技术栈（≥60% 方向占比 + ≥2/3 技术栈匹配）
- 生成沟通话术
- 自动发送消息

## 🚀 快速开始

### 安装依赖

```bash
# Python 依赖
pip install -r requirements.txt

# Node.js OCR 依赖
cd skills/ocr-local
npm install
```

### 运行自动化

#### 自动循环模式

```bash
python main.py
```

#### CLI 命令行

```bash
python cli.py start          # 开始自动处理
python cli.py scroll         # 滚动一次
python cli.py click          # 点击职位
python cli.py screenshot     # 截图
python cli.py ocr <image>    # OCR 识别
python cli.py chat           # 执行沟通
python cli.py config         # 显示配置
```

## 📊 技术匹配策略

### 匹配标准

```
技术方向占比 >= 60%  AND  技术栈匹配数 >= 2/3
```

### 技术方向分类

| 方向 | 关键词示例 |
|------|---------|
| **前端** | 前端/页面/界面/Vue/React/Angular/HTML/CSS/TypeScript |
| **后端** | 后端/API/RESTful/Spring/Django/Flask/Go/Kubernetes/Docker |
| **数据** | 数据/数据库/SQL/NoSQL/Pandas/Spark/Hadoop/Flink/Redis |
| **算法** | 算法/模型/PyTorch/TensorFlow/Scikit-learn/OpenCV/ONNX/LLM/NLP/CV |
| **全栈** | 全栈/全端/MERN/MEAN/Next.js/NestJS/GraphQL |

### 技术栈关键词

| 类别 | 关键词 |
|------|--------|
| **语言** | Python/Java/Go/Rust/JavaScript/TypeScript/C++/C# |
| **框架** | PyTorch/TensorFlow/Spring/Django/FastAPI/Express/NestJS |
| **模型** | LLM/GPT/BERT/Transformers/Stable Diffusion/YOLO/OpenCV |

## 💬 话术生成策略

### 生成规则

1. **说明符合要求的内容** - 直接提及匹配的技术点
2. **技术方面适当夸大** - 了解→熟悉，不熟悉→了解
3. **模仿人类语言习惯** - 自然流畅的中文表达
4. **表达强烈应聘希望** - 体现求职诚意
5. **字数控制** - 40-60 字

## ⚙️ 配置说明

编辑 `config.json` 自定义：
- 目标分辨率（默认 2560x1440）
- 坐标缩放倍数
- 滚动参数
- 匹配阈值
- 话术模板

## 📁 文件结构

```
boss-automation/
├── SKILL.md                    # 本技能文档
├── README.md                   # 快速指南
├── requirements.txt            # Python 依赖
├── config.json                 # 主配置文件
├── chat_template.txt           # 话术模板
├── main.py                     # 主流程脚本
├── cli.py                      # CLI 命令行接口
└── boss_automation.py          # pyautogui 自动化函数
```

## 🐛 故障排除

### OCR 无法识别

- 确保 `skills/ocr-local` 已安装依赖：`npm install`
- 检查图像路径是否正确
- 确认 `tesseract.js` 已安装

### 中文话术乱码

- 使用 `pyperclip` 复制（已在代码中自动处理）
- 确保文件编码为 UTF-8

### 坐标偏移

- 在 `config.json` 中调整坐标值
- 或使用 `scale_multiplier` 自动缩放
- 运行 `python cli.py test` 查看缩放结果

## 📜 License

MIT License
