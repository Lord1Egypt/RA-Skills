# Enterprise File Writer

写入内容到本地文件，支持企业安全策略环境，正确处理编码避免乱码。

## ⚠️ 安全警告

本工具会直接修改或覆盖本地文件，属于**高风险操作**：

- **覆盖写入**会永久删除文件原有内容
- **自动创建目录**可能在意外位置创建文件夹
- 可用于覆盖配置文件、脚本、日志等关键文件
- 如果路径或内容被恶意控制，可能导致系统篡改

### 安全检查机制

工具内置以下安全检查，检测到风险时会中止操作并输出警告：

- 敏感系统路径检测
- 敏感文件类型检测（凭据、配置、证书等）
- 可执行脚本写入警告
- 路径遍历风险检测（`..`）
- 文件覆盖警告

遇到安全警告时，需要使用 `--force` 参数才能继续执行。

### 用户确认要求

- 覆盖重要文件前必须向用户说明风险
- 写入敏感路径前必须获得用户明确授权
- 不得在未告知用户的情况下使用 `--force` 参数

---

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
- 支持 .docx 和 .xlsx 文件写入

## 许可证

MIT License
