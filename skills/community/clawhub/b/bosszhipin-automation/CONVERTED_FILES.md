# Boss Automation - 已转换的文件清单

## 📋 转换说明

以下文件已从 `boss-anti-assemble` 目录完整转换为标准 OpenClaw skill 格式：

## ✅ 已转换的文件

| 文件名 | 说明 | 状态 |
|--------|------|------|
| **README.md** | 技能文档 | ✅ 已转换 |
| **SKILL.md** | 主技能说明文档 | ✅ 已转换 |
| **config.json** | 配置文件（含所有参数） | ✅ 已转换 |
| **chat_template.txt** | 话术模板 | ✅ 已转换 |
| **main.py** | 主流程脚本（函数式接口） | ✅ 已转换 |
| **cli.py** | CLI 命令行接口 | ✅ 已转换 |
| **boss_automation.py** | pyautogui 自动化核心函数 | ✅ 已转换 |
| **requirements.txt** | Python 依赖 | ✅ 已转换 |
| **.gitignore** | Git 忽略文件 | ✅ 已转换 |
| **CONVERTED_FILES.md** | 此说明文档 | ✅ 新创 |

## 🔄 依赖关系

以下文件作为依赖引用，**未直接转换**（位于其他技能目录）：

- `skills/ocr-local/scripts/ocr.js` - OCR 识别脚本
- `skills/ocr-local/package.json` - OCR 依赖

## 📊 核心功能

该技能包含以下功能模块：

### 1. 浏览自动化
- 自动滚动职位列表
- 自动点击职位
- 浏览器前后操作

### 2. 截图与 OCR
- 截取职位描述区域
- 调用 ocr-local 进行识别
- 提取技术关键词

### 3. 智能匹配
- 技术方向占比分析（≥60%）
- 技术栈匹配（≥2/3）
- 核心技能关键词匹配

### 4. 话术生成
- 说明符合要求的内容
- 技术方面适当夸大
- 模仿人类语言习惯
- 表达强烈应聘希望

### 5. 沟通流程
- 点击沟通按钮
- 粘贴话术
- 发送消息
- 失败重试机制

### 6. 配置管理
- 多分辨率适配
- 坐标自动缩放
- 话术模板自定义
- 匹配阈值调整

## 🚀 使用方式

### 自动循环模式

```bash
python main.py
```

### CLI 命令行

```bash
python cli.py start          # 开始自动处理
python cli.py scroll         # 滚动一次
python cli.py click          # 点击职位
python cli.py screenshot     # 截图
python cli.py ocr <image>    # OCR 识别
python cli.py chat           # 执行沟通
python cli.py config         # 显示配置
```

### 独立函数调用

```python
from main import *

# 只执行点击和截图
click_job_item()
path = capture_screenshot()

# 自定义流程
click_chat_button()
send_chat_message("自定义消息")

# 处理单个职位
process_job()
```

## ⚙️ 配置参数

编辑 `config.json` 可自定义：

```json
{
  "browser": {
    "url": "https://www.zhipin.com/web/geek/jobs"
  },
  "coordinates": {
    "resolution": [2560, 1440],
    "scale_multiplier": 1.0
  },
  "matching": {
    "threshold": 60
  }
}
```

## 🎯 技术匹配策略

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

## 📦 依赖关系

```
boss-automation/
├── main.py              # 主流程
├── cli.py              # CLI 接口
├── boss_automation.py  # 核心自动化
├── config.json         # 配置
├── chat_template.txt   # 话术模板
├── requirements.txt    # Python 依赖
├── SKILL.md            # 主文档
├── README.md           # 快速指南
└── .gitignore          # Git 忽略
```

## 🔧 后续扩展

如需扩展功能，可添加：
- 自定义话术模板
- 新增技术方向
- 调整匹配阈值
- 添加新的自动化逻辑

---

**转换日期：** 2026-04-29

**版本：** 1.0.0

**状态：** 已完成转换
