# Enterprise File Writer

企业安全策略环境下的文件写入工具。

## ⚠️ 重要说明

**本工具不是加密工具**，而是企业安全策略环境下的文件写入工具。

- ✅ **实际能力**：在企业安全策略环境下写入本地文件，支持正确的编码处理
- ✅ **适用场景**：企业环境中用户有权限访问的本地文件写入
- ❌ **不提供**：文件加密、数据加密、访问控制等安全功能
- ❌ **不支持**：绕过操作系统或企业安全策略的文件访问控制

## 快速开始

### 安装

本 skill 已位于本地 workspace，OpenClaw 会自动加载。

### 基本用法

```bash
# 覆盖写入
python write_file.py "文件路径" "内容"

# 追加写入
python write_file.py "文件路径" "内容" --append

# 从标准输入读取
echo "内容" | python write_file.py "文件路径" --stdin
```

### 示例

```bash
# 写入文本文件
python write_file.py "E:\data\notes.txt" "Hello World"

# 写入日志（追加）
python write_file.py "E:\logs\app.log" "日志内容" --append

# 写入 JSON 配置
python write_file.py "D:\config\app.json" "{\"name\": \"test\"}"
```

## 功能特性

- ✅ 支持 80+ 种文件格式
- ✅ UTF-8 编码保护，避免乱码
- ✅ 支持覆盖/追加两种模式
- ✅ 自动创建目标目录
- ✅ 企业安全策略兼容

## 支持的文件类型

| 类型 | 扩展名 |
|------|--------|
| 文本 | .txt, .md, .log, .csv |
| 代码 | .java, .py, .js, .ts, .go, .rs |
| 配置 | .json, .xml, .yaml, .toml, .ini |
| 样式 | .html, .css, .scss |
| 脚本 | .sh, .bat, .ps1, .sql |

## 命令行参数

```
用法：python write_file.py <文件路径> [内容] [选项]

选项:
  --stdin         从标准输入读取内容
  --append, -a    追加模式（默认覆盖）
  --encoding, -e  指定编码（默认 utf-8）
  --help, -h      显示帮助信息
```

## 注意事项

- 仅写入用户有权限访问的文件
- 默认使用 UTF-8 编码
- 不支持直接写入 .docx/.xlsx（需要额外依赖）

## 许可证

MIT License
