# Everything Search Skill

🔍 基于 Everything HTTP Server API 的快速文件搜索技能，支持中文/英文搜索、模糊匹配、文件类型过滤。

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-000000?style=flat-square)
![Everything](https://img.shields.io/badge/Everything-1.4%2B-FF6B35?style=flat-square)

## ✨ 功能特性

- 🚀 **毫秒级搜索** - 利用 Everything 的索引引擎，实现即时搜索
- 🌏 **中文支持** - 完美支持中文关键词搜索
- 📸 **图片搜索** - 可按文件类型搜索照片、文档等
- 🔍 **高级过滤** - 支持文件类型、路径、大小、日期过滤
- 🛠️ **诊断工具** - 内置配置检查和故障诊断工具
- 📝 **详细文档** - 包含完整的使用指南和问题排查手册

## 📦 安装要求

- **Everything** 1.4+ (https://www.voidtools.com/)
- **Python** 3.8+
- **HTTP Server** 已启用（端口 2853）

## 🚀 快速开始

### 1. 配置 Everything

```bash
# 1. 安装 Everything
# 下载地址：https://www.voidtools.com/

# 2. 启用 HTTP 服务器
# - 打开 Everything
# - 按 Ctrl+P 打开选项
# - 点击 HTTP Server
# - 勾选 "Enable HTTP server"
# - 设置端口：2853
# - 点击 OK

# 3. 重启 Everything
# - 完全退出（系统托盘右键 → Exit）
# - 重新启动
```

### 2. 验证配置

```bash
# 运行诊断脚本
python scripts/check-config.py
```

### 3. 使用示例

```bash
# 搜索文件
python examples/search_files.py "数据资产"

# 搜索图片
python examples/search_photos.py "张三"

# 高级搜索
python examples/advanced_search.py --type jpg --size ">1mb" "照片"
```

## 📁 项目结构

```
everything-search-skill/
├── README.md                 # 项目说明
├── LICENSE                   # 许可证
├── requirements.txt          # Python 依赖
├── SKILL.md                  # 技能详细说明
├── src/
│   ├── __init__.py
│   ├── everything_search.py  # 核心搜索模块
│   └── utils.py              # 工具函数
├── examples/
│   ├── basic_search.py       # 基础搜索示例
│   ├── search_photos.py      # 图片搜索示例
│   ├── advanced_search.py    # 高级搜索示例
│   └── batch_search.py       # 批量搜索示例
├── scripts/
│   ├── check-config.py       # 配置检查脚本
│   ├── test-api.py           # API 测试脚本
│   └── diagnose.py           # 完整诊断工具
├── tests/
│   ├── __init__.py
│   ├── test_search.py        # 搜索测试
│   └── test_utils.py         # 工具测试
└── docs/
    ├── configuration.md      # 配置指南
    ├── troubleshooting.md    # 故障排查
    └── api-reference.md      # API 参考
```

## 💡 使用示例

### 基础搜索

```python
from src.everything_search import EverythingSearch

# 初始化
search = EverythingSearch(port=2853)

# 搜索文件
results = search.search("数据资产")
print(f"找到 {results.total} 个结果")

# 显示前 10 个结果
for item in results.items[:10]:
    print(f"  - {item.full_path}")
```

### 搜索特定类型文件

```python
# 搜索 JPG 图片
results = search.search("张三", file_type="jpg")

# 搜索 PDF 文档
results = search.search("报告", file_type="pdf")

# 搜索 Excel 文件
results = search.search("数据", file_type="xlsx")
```

### 高级搜索

```python
# 按大小过滤
results = search.search("视频", min_size="10mb")

# 按日期过滤
results = search.search("文档", modified_after="2024-01-01")

# 组合搜索
results = search.search(
    "照片",
    file_type="jpg",
    min_size="1mb",
    max_results=20
)
```

## 🛠️ 诊断工具

### 检查配置

```bash
# 检查 Everything 配置
python scripts/check-config.py
```

### 测试 API

```bash
# 测试 API 端点
python scripts/test-api.py
```

### 完整诊断

```bash
# 运行完整诊断
python scripts/diagnose.py
```

## 📚 文档

- **[SKILL.md](SKILL.md)** - 完整的技能说明和故障排查指南
- **[docs/configuration.md](docs/configuration.md)** - 详细配置步骤
- **[docs/troubleshooting.md](docs/troubleshooting.md)** - 常见问题解决方案
- **[docs/api-reference.md](docs/api-reference.md)** - API 参考文档

## ⚠️ 注意事项

1. **HTTP 服务器必须手动启用** - 配置文件不会自动启用，必须在 GUI 中勾选
2. **配置生效需要重启** - 修改配置后需完全退出并重启 Everything
3. **中文需要 URL 编码** - 脚本会自动处理，手动构建 URL 时需注意
4. **正确的 API 端点** - 使用 `/?search=xxx` 而不是 `/everything/?search=xxx`

## 🐛 常见问题

### HTTP 服务器无法连接

**解决方案：**
1. 打开 Everything 窗口
2. Ctrl+P → HTTP Server
3. 确认已勾选 "Enable HTTP server"
4. 完全退出并重启 Everything

### API 返回 404

**解决方案：**
- 使用正确的端点：`http://127.0.0.1:2853/?search=关键词&json=1`
- 不要使用 `/everything/` 或 `/api/` 前缀

### 中文搜索乱码

**解决方案：**
- 使用 `urllib.parse.quote()` 编码中文关键词
- 示例代码已自动处理编码

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

- 问题反馈：441457345@qq.com
- 技能来源：nanobot @ DeskClaw

## 🙏 致谢

- [Everything](https://www.voidtools.com/) - 强大的文件搜索工具
- [DeskClaw](https://github.com/deskclaw) - 个人 AI 桌面助手框架

---

**最后更新：** 2026-04-02  
**版本：** 1.0.0
