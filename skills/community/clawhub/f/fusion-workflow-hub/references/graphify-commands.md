# Graphify 命令参考

## 安装

```bash
pip install graphifyy
```

可选依赖：
```bash
pip install python-docx openpyxl pillow
```

## 核心命令

### 构建图谱

```bash
# 基本用法
python -m graphify <目录路径>

# 增量更新（仅分析更改的文件）
python -m graphify <目录路径> --update

# 指定输出目录
python -m graphify <目录路径> --output ./my-graph
```

### 查询

```bash
# 自然语言查询
python -m graphify query "这个模块的主要功能是什么？"

# 概念路径追踪
python -m graphify path "用户认证" "数据库"

# 显示关系
python -m graphify relations <文件名>
```

### 可视化

```bash
# 生成 HTML 报告
python -m graphify visualize <目录路径>

# 打开交互式图谱
open graphify-out/graph.html
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `graph.html` | D3.js 交互式可视化 |
| `GRAPH_REPORT.md` | 摘要报告，包含 God Nodes |
| `graph.json` | 完整图谱数据（可加载查询） |
| `cache/` | SHA256 缓存目录 |

## 支持语言

- Python, JavaScript, TypeScript
- Go, Rust, Java, C, C++
- Ruby, PHP, Swift, Kotlin
- 以及 20+ 其他语言

## 文档格式

- Markdown (.md)
- PDF (.pdf)
- Word (.docx)
- Excel (.xlsx)
- 图片 (.png, .jpg, .webp)

---

*来源: https://github.com/safishamsi/graphify*
