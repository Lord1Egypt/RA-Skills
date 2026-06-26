# NowCoder 面经搜索工具

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个强大的牛客网面试经验搜索和分析工具，作为 Claude Code Skill 运行，提供完整的自动化工作流。

## 核心功能

### 🎯 主要特性
- 🚀 **完整 Onboarding** - 首次使用引导配置
- 📝 **自动生成报告** - 结构化面经报告，包含面试题汇总、经验总结、趋势分析
- ⚙️ **配置管理** - 动态调整搜索关键词、时间窗口、报告风格
- 💡 **智能推荐** - 自动筛选高价值内容

## 快速开始

### 前置要求

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)（推荐）或 pip

### 安装

#### 使用 uv 安装（推荐）

```bash
# 克隆项目
git clone https://github.com/Infinityay/nowcoder-mcp.git
cd nowcoder-mcp

# 安装依赖
uv sync
```

#### 使用 pip 安装

```bash
# 克隆项目
git clone https://github.com/Infinityay/nowcoder-mcp.git
cd nowcoder-mcp

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 使用方法

在 Claude Desktop 或其他支持 Skill 的 AI 助手中：

1. 将 `SKILL.md` 文件加载到对话中
2. 首次使用会自动运行 Onboarding 流程
3. 配置您的偏好设置
4. 自动生成第一个面经报告

详细说明请查看 [SKILL.md](SKILL.md)。

## 项目结构

```
nowcoder-search/
├── SKILL.md                    # Agent Skill 主文档
├── config/
│   └── default_config.json     # 默认配置
├── prompts/
│   └── report_summary.md       # 面经报告提示词模板
├── src/
│   ├── __init__.py
│   ├── utils.py                # 工具函数（配置、提示词管理）
│   ├── search.py               # 搜索功能模块
│   └── analyzer.py             # 分析和报告准备模块
└── README.md                   # 本文件
```

## 功能说明

### 1. 面经报告生成

根据配置的关键词、时间窗口等参数，自动搜索并生成结构化面经报告，包括：
- 整体概览
- 重点推荐（3-5篇）
- 技术面试题汇总
- 经验总结
- 趋势观察
- 行动建议

### 2. 配置管理

通过对话动态调整：
- 搜索关键词
- 时间窗口
- 标签筛选
- 报告语言（中文/英文/双语）
- 报告风格

## 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `search_keywords` | 搜索关键词列表 | `["Java后端", "秋招"]` |
| `time_window_days` | 时间窗口（天） | `7` |
| `max_pages` | 每个关键词最大页数 | `5` |
| `tag` | 标签筛选ID | `818`（面经） |
| `order` | 排序方式 | `"create"`（按时间） |
| `language` | 报告语言 | `"zh"`（中文） |

### 标签筛选选项

| tag ID | 含义 |
|--------|------|
| `818` | 面经 |
| `861` | 求职进度 |
| `823` | 内推 |
| `856` | 公司评价 |
| `null` | 不筛选（全部） |

## 配置路径

- 用户配置: `~/.nowcoder-search/config.json`
- 用户提示词: `~/.nowcoder-search/prompts/`
- 报告输出: `~/.nowcoder-search/reports/`
- 默认配置: `config/default_config.json`
- 默认提示词: `prompts/`

## 性能考虑

- 搜索时添加 2 秒延迟，避免请求过快
- 支持多关键词并行搜索
- 支持分页获取，避免一次性加载过多数据

## 内容类型说明

牛客网的内容分为两种类型：

| 类型 | rc_type | 标识字段 | 详情页 URL |
|-----|---------|---------|-----------|
| **Feed 动态** | 201 | `uuid` | `nowcoder.com/feed/main/detail/{uuid}` |
| **讨论帖** | 207 | `content_id` | `nowcoder.com/discuss/{content_id}` |

## 常见使用场景

### 场景 1: 准备特定公司的面试

```
用户: "我下周要面试字节跳动的后端岗位，帮我看看面经"

助手会:
1. 检查配置中的关键词是否包含"字节跳动"
2. 如果不包含，临时搜索或更新配置
3. 搜索并生成报告
4. 筛选出字节跳动相关的帖子
5. 重点推荐和分析
```

### 场景 2: 快速浏览最新面经

```
用户: "给我看看最近的面经"

助手会:
1. 使用当前配置直接搜索
2. 生成报告
3. 按时间排序展示
4. 快速概览
```

### 场景 3: 针对性学习

```
用户: "我想重点准备算法题"

助手会:
1. 修改配置，添加"算法"关键词
2. 搜索并生成报告
3. 重点提取算法面试题
4. 提供练习建议
```

## 注意事项

- 首次使用会运行 Onboarding 流程
- 配置保存在 `~/.nowcoder-search/config.json`
- 自定义提示词保存在 `~/.nowcoder-search/prompts/`
- 报告可导出到 `~/.nowcoder-search/reports/`

## 技术栈

- **Python 3.12+**: 核心语言
- **requests**: HTTP 请求
- **pydantic**: 数据验证

## License

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---
