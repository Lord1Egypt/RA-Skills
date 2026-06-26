# CDISC Library API Skill - 快速开始

## 🚀 5 分钟上手

### 1. 配置 API Key

编辑 `../../TOOLS.md`，添加你的 API Key：

```markdown
## CDISC API

- **API Key**: `你的 API Key`
```

获取 Key: https://api.developer.library.cdisc.org/profile

### 2. 测试连接

```bash
cd skills/cdisc
python cdisc_client.py
```

看到 `✓ 连接成功！` 即表示配置正确。

### 3. 开始使用

```bash
# 查看所有产品类别
python commands/products.py

# 查询量表（自动获取最新版）
python commands/qrs.py AIMS01

# 查询指定版本
python commands/qrs.py AIMS01 2-0

# 查询量表项目列表
python commands/items.py AIMS01 2-0

# 查询 ADaM 数据结构
python commands/adam.py adam-2-1 ADSL

# 查询 SDTM 域变量
python commands/sdtm.py 3-4 DM

# 查询受控术语
python commands/ct.py C102111

# 搜索
python commands/search.py USUBJID

# 版本比较
python commands/compare.py qrs AIMS01 1-0 2-0
```

**命令前缀**: `/cdisc-library-api`

## 📚 完整文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 完整命令列表和说明 |
| [assets/quickref.md](assets/quickref.md) | 速查表（量表代码、数据结构、域列表） |
| [E:\openclaw\CDISC_API_使用指南.md](../../E:/openclaw/CDISC_API_使用指南.md) | API 完整文档 |

## 📦 命令分类

### 基础查询（8 个）
- `products` - 产品列表
- `qrs` - QRS 量表
- `items` - 量表项目
- `adam` - ADaM
- `sdtm` - SDTM
- `cdash` - CDASH
- `ct` - 受控术语
- `ct-packages` - 术语包

### 高级查询（5 个）
- `root` - 根资源
- `docs` - 文档
- `rules` - 规则
- `search` - 搜索
- `compare` - 版本比较

### 工具命令（3 个）
- `export` - 导出 JSON/CSV
- `batch` - 批量查询
- `cache` - 缓存管理

## 💡 提示

- **版本号格式**：`2-0` (不是 `2.0`)
- **缓存**：首次查询会缓存，后续相同请求秒回
- **速率限制**：自动处理，无需担心
- **导出文件**：保存在当前目录

## 🎯 典型工作流

### 场景 1：查找量表信息
```bash
/cdisc-library-api qrs HAM-D              # 查看量表详情
/cdisc-library-api items HAM-D 1-0        # 查看完整项目
/cdisc-library-api export items HAM-D 1-0 --format=csv  # 导出 CSV
```

### 场景 2：对比版本变化
```bash
/cdisc-library-api compare qrs AIMS01 1-0 2-0  # 查看差异
```

### 场景 3：批量获取多个量表
```bash
# 创建查询文件
echo "qrs AIMS01" > queries.txt
echo "qrs CGI01" >> queries.txt
echo "qrs HAM-D" >> queries.txt

# 批量执行
/cdisc-library-api batch queries.txt
```

### 场景 4：查找变量定义
```bash
/cdisc-library-api search USUBJID      # 搜索变量
/cdisc-library-api sdtm 3-4 DM         # 查看 SDTM DM 域详情
```
