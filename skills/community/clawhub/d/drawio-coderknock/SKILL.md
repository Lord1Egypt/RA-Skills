# 🎨 Draw.io 流程图生成器

智能流程图生成技能 - 一键生成专业的系统架构图和流程图，自动检测并使用本地 Draw.io。

## 功能特性

- ✅ 直接生成真正的 draw.io 文件，包含完整图形元素
- 🔍 自动检测本地 Draw.io 安装状态
- 🚀 自动打开本地 Draw.io 并显示完整流程图
- 💡 未安装时提供友好的安装指引
- 🎨 使用泳道图展示，层次清晰
- 🎯 预设电商系统架构图和 CEX 交易所架构图模板
- 🌈 优化的配色方案，高对比度，文字清晰可见

## 快速开始

**使用稳定版本（推荐）：**

```bash
# 生成电商系统架构图
python stable_generator.py

# 生成 CEX 交易所架构图
python cex_architecture_v2.py

# 指定工作目录
python stable_generator.py --workspace /path/to/workspace
```

**稳定版本特点：**
- 直接生成完整的 draw.io XML 文件
- 包含真实的图形元素，无需 Mermaid 导入
- 使用泳道图展示系统架构
- 自动检测并打开本地 Draw.io
- 优化的配色方案，文字清晰

## 预设模板

### 1. 电商系统架构图
- 5层完整架构：用户层、接入层、应用层、数据层、基础设施层
- 包含完整的电商微服务组件
- 文件：`stable_generator.py`

### 2. CEX 交易所整体架构图
- 6层完整架构：用户接入层、网关层、交易核心层、数据层、区块链层、运维层
- 包含撮合引擎、风控、热钱包/冷钱包等核心组件
- 优化的配色方案，高对比度
- 文件：`cex_architecture_v2.py`

## 安装 Draw.io

### Windows
```powershell
winget install drawio
```

### Mac
```bash
brew install --cask drawio
```

### 手动下载
访问：https://github.com/jgraph/drawio-desktop/releases

## 使用说明

1. 运行对应的生成器脚本
2. 脚本会自动生成 .drawio 文件
3. 如果本地安装了 Draw.io，会自动打开
4. 如果没有安装，会提示安装方式
5. 在 Draw.io 中可以直接编辑和导出

## 文件结构

```
skills/drawio-flow-generator/
├── SKILL.md                    # 本文件
├── package.json                # 技能配置
├── README.md                   # 详细使用说明
├── stable_generator.py         # 电商架构图生成器（稳定版）
├── cex_architecture_v2.py      # CEX 交易所架构图（优化配色）
├── generate_flow.py            # 通用流程图生成器
├── simple_test.py              # 简单测试脚本
└── templates/                  # Mermaid 模板库
    ├── login_flow.mmd
    ├── order_flow.mmd
    ├── approval_flow.mmd
    ├── generic_flow.mmd
    └── ecommerce_architecture.mmd
```

## 作者

AI Assistant

## 欢迎关注

欢迎关注微信公众号：**拿客**

获取更多技术干货和开源工具分享！

## 许可证

MIT License
