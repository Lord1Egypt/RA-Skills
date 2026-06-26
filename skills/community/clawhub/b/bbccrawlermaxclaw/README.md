---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3045022074c546b58330a07da35f0e0d94c0ad51cc6d4e445b235ef033071d1b4da4a11f022100b661c9e283570d245986240a3688ea7cfc0107c8f8d80d9985d4b35a77cfa953
    ReservedCode2: 3045022100f1f6d58d0a92215eab415fba9da1ec4c2525d726e00458bb0456467ff4e572550220151c90d6d8f68eb711764b45a38831c0f5ba52612215d97fcc3e218db6ed5873
---

# BBC Crawler Skill

这是一个基于OpenClaw的BBC和通用网站爬虫Skill。

## 功能特性

- 支持BBC News、BBC Sport等栏目的精准内容提取
- 支持通用网站爬取（Generic Mode）
- 支持Markdown格式输出
- 自动提取正文、标题、作者、发布时间等元数据
- 智能去重和深度控制
- **图片本地化下载**：自动下载正文图片到本地，并更新Markdown链接，支持离线查看。

## 独立安装指南

该 Skill 支持在 Windows、Linux 和 macOS 等多种环境下运行。

### 1. 准备环境

确保已安装 Python 3.8+。

### 2. 快速安装与运行 (推荐)

**Windows 用户:**
1. 双击运行 `install_dependencies.bat` 安装依赖。
2. 双击运行 `run_bbc_crawler.bat` 启动演示爬虫。

**Linux / macOS 用户:**
1. 在终端中运行安装脚本：
   ```bash
   chmod +x install_dependencies.sh
   ./install_dependencies.sh
   ```
2. 运行演示爬虫：
   ```bash
   chmod +x run_bbc_crawler.sh
   ./run_bbc_crawler.sh
   ```

### 3. 手动安装 (高级用户)

在Skill目录下运行：

```bash
pip install -r requirements.txt
```

### 3. 运行爬虫

#### 基本用法

```bash
python universal_crawler_v2.py --url https://www.bbc.com/news --max-pages 50
```

#### 常用参数

- `--url`: 起始URL（必填）
- `--max-pages`: 最大爬取页面数（默认50）
- `--depth`: 爬取深度（默认5）
- `--output`: 输出目录（默认当前目录下的 `data` 文件夹）
- `--delay`: 请求间隔时间（秒，默认3.0）

### 4. 输出结果

爬取结果将保存在指定的输出目录中，结构如下：

```
data/
└── {日期}/
    └── {栏目}/
        ├── images/             # 图片文件夹
        │   ├── {hash}.jpg
        │   └── ...
        └── {域名}_{时间}_{标题}.md  # Markdown文档
```

## 文件结构

```
bbc_crawler_maxclaw/
├── universal_crawler_v2.py  # 主程序
├── requirements.txt         # 依赖文件
├── README.md                # 本文件
├── SKILL.md                 # OpenClaw 元数据
├── USAGE.md                 # OpenClaw 使用指南
├── skill.json               # Skill 描述文件
└── install_dependencies.bat # Windows 安装脚本
└── run_bbc_crawler.bat      # Windows 运行脚本
```
