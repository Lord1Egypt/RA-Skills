# 🎨 Draw.io 流程图生成器

智能流程图生成技能 - 根据用户描述自动生成流程图，自动检测并使用本地 Draw.io。

## ✨ 功能特性

- ✅ 直接生成真正的 draw.io 文件，包含完整图形元素
- 🔍 自动检测本地 Draw.io 安装状态
- 🚀 自动打开本地 Draw.io 并显示完整流程图
- 💡 未安装时提供友好的安装指引
- 🎨 使用泳道图展示，层次清晰
- 🎯 预设电商系统架构图模板

## 🚀 快速开始 - 稳定版本（推荐）

### 使用稳定版本

```bash
# 生成电商系统架构图
python stable_generator.py

# 指定工作目录
python stable_generator.py --workspace /path/to/workspace
```

### 稳定版本特点

- 直接生成完整的 draw.io XML 文件
- 包含真实的图形元素，无需 Mermaid 导入
- 使用泳道图展示系统架构
- 自动检测并打开本地 Draw.io
- 5层清晰的电商系统架构

## 🚀 快速开始

### 安装依赖

不需要额外安装 Python 包，使用标准库即可。

### 安装 Draw.io（推荐）

**Windows:**
```powershell
winget install drawio
```

**Mac:**
```bash
brew install --cask drawio
```

**或从官网下载：**
https://github.com/jgraph/drawio-desktop/releases

### 使用示例

```bash
# 生成用户登录流程图
python generate_flow.py "用户登录流程"

# 生成订单处理流程图
python generate_flow.py "订单处理流程" --template order

# 生成审批流程图
python generate_flow.py "审批流程" --template approval

# 测试模式
python generate_flow.py --test
```

## 📝 使用方式

### 命令行参数

```bash
python generate_flow.py <描述> [选项]

选项:
  --template, -t  模板类型 (login|order|approval|generic)
  --test          测试模式
  --workspace, -w 工作目录
```

### 预设模板

| 模板类型 | 说明 |
|---------|------|
| `login` | 用户登录/注册流程 |
| `order` | 订单处理流程 |
| `approval` | 审批流程 |
| `generic` | 通用流程图（默认） |

## 🎯 工作原理

1. **理解用户需求** → 解析用户想画什么流程图
2. **选择合适模板** → 根据关键词自动选择模板
3. **生成 Mermaid 代码** → 输出流程图代码
4. **创建 .drawio 文件** → 保存为 Draw.io 格式
5. **检测本地 Draw.io** → 检查是否安装
6. **自动打开导入** → 安装了就自动打开，没安装就提示

## 📁 技能结构

```
skills/drawio-flow-generator/
├── SKILL.md              # 技能定义
├── package.json          # 技能配置
├── generate_flow.py      # 主程序
├── templates/            # 流程图模板库
│   ├── login_flow.mmd
│   ├── order_flow.mmd
│   ├── approval_flow.mmd
│   └── generic_flow.mmd
└── README.md             # 本文件
```

## 💡 使用技巧

### 在 Draw.io 中使用 Mermaid

1. 打开 Draw.io
2. 点击菜单：**Arrange** → **Insert** → **Advanced** → **Mermaid...**
3. 复制粘贴生成的 .mmd 文件中的代码
4. 点击 **Insert**，流程图就自动生成了！

### 自定义模板

在 `templates/` 目录下添加新的 `.mmd` 文件即可扩展模板库。

## 🔧 故障排除

### 找不到 Draw.io

程序会自动在以下位置查找：
- Windows: `C:\Program Files\draw.io\draw.io.exe`
- Mac: `/Applications/draw.io.app/Contents/MacOS/draw.io`
- Linux: `/usr/bin/drawio`, `/usr/local/bin/drawio`

如果找不到，可以：
1. 从官网下载安装
2. 使用在线版：https://app.diagrams.net/

## 📄 许可证

MIT License

## 👤 作者

AI Assistant

## 🎉 开始使用

现在就试试生成你的第一个流程图吧！

```bash
cd skills/drawio-flow-generator
python generate_flow.py "我的第一个流程图"
```
