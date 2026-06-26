# Color-Filer API 参考

## 脚本 API 文档

---

## analyze_folder.py

### 功能

扫描目标目录，分析文件结构，生成命名建议报告。

### 使用方法

```bash
python scripts/analyze_folder.py <目标目录>
```

### 参数

| 参数 | 说明 |
|------|------|
| `target_path` | 目标目录路径（必需） |

### 输出

分析报告（Markdown 格式），包含：
- 📊 统计摘要（文件数、目录数、最大深度）
- 📋 文件类型分布（Top 10）
- 📂 根目录列表
- ⚠️ 问题检测（序号重复、空目录）
- 💡 整理建议
- 🎯 命名规范速查表

### 示例

```bash
python scripts/analyze_folder.py "F:\笔记\学习笔记"
```

---

## rename_files.py

### 功能

批量重命名文件，支持 Dry-Run 模式和安全验证。

### 使用方法

```bash
# 预览重命名（Dry-Run 模式，推荐）
python scripts/rename_files.py <目标目录> --dry-run

# 执行实际重命名
python scripts/rename_files.py <目标目录> --rename

# 执行重命名且不创建备份
python scripts/rename_files.py <目标目录> --rename --no-backup
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `target` | 目标目录路径（必需） | - |
| `--dry-run` | 预演模式，不实际重命名 | `True` |
| `--rename` | 执行实际重命名 | `False` |
| `--no-backup` | 不创建备份 | `False` |

### 安全特性

1. **默认 Dry-Run**：仅预览，不修改文件
2. **路径验证**：拒绝处理系统关键目录
3. **冲突处理**：自动追加序号解决命名冲突
4. **可选备份**：执行前自动备份整个目录

### 禁止处理的路径

- Windows: `C:\Windows*`, `C:\Program Files*`, `C:\ProgramData*`
- Linux/Mac: `/root`, `/bin`, `/usr`, `/etc`, `/var`

### 输出

操作统计：
- ✅ 成功重命名文件数
- ❌ 失败文件数及原因
- ⚠️ 冲突文件数及调整详情

### 示例

```bash
# 预览重命名
python scripts/rename_files.py "F:\笔记" --dry-run

# 执行重命名
python scripts/rename_files.py "F:\笔记" --rename
```

---

## example.py

### 功能

Color-Filer 使用示例，展示如何调用核心函数。

### 使用方法

```bash
python scripts/example.py <目标目录>
```

### 示例代码

```python
from color_filer import analyze_directory, generate_naming_suggestions

# 分析目录
files, dirs = analyze_directory("F:\笔记")

# 生成命名建议
suggestions = generate_naming_suggestions(files)

# 显示建议
for item in suggestions:
    print(f"{item['old']} → {item['new']}")
```

---

## 函数 API

### validate_target_path(target_path)

验证目标路径是否安全。

**参数：**
- `target_path` (str): 目标路径

**返回：**
- `tuple`: (is_safe: bool, reason: str)

**示例：**
```python
is_safe, reason = validate_target_path("F:\笔记")
if is_safe:
    print(f"✅ {reason}")
else:
    print(f"❌ {reason}")
```

---

### analyze_directory(target_path)

分析目录结构，生成文件和目录列表。

**参数：**
- `target_path` (str): 目标目录路径

**返回：**
- `tuple`: (file_list, dir_list)

**示例：**
```python
files, dirs = analyze_directory("F:\笔记")
print(f"文件数: {len(files)}")
print(f"目录数: {len(dirs)}")
```

---

### generate_naming_suggestions(files)

根据文件类型生成命名建议。

**参数：**
- `files` (list): 文件列表

**返回：**
- `list`: 命名建议列表

**示例：**
```python
suggestions = generate_naming_suggestions(files)
for item in suggestions:
    print(f"{item['old']} → {item['new']}")
```

---

### rename_files(target_path, mapping, dry_run=True)

执行文件重命名。

**参数：**
- `target_path` (str): 目标目录路径
- `mapping` (list): 命名映射列表
- `dry_run` (bool): 是否预演模式

**返回：**
- `tuple`: (success_count, fail_count, conflict_count)

**示例：**
```python
success, fail, conflict = rename_files(
    "F:\笔记",
    mapping,
    dry_run=True
)
print(f"成功: {success}, 失败: {fail}, 冲突: {conflict}")
```

---

### create_backup(target_path)

创建目录备份。

**参数：**
- `target_path` (str): 目标目录路径

**返回：**
- `str`: 备份目录路径（失败返回 `None`）

**示例：**
```python
backup = create_backup("F:\笔记")
if backup:
    print(f"备份成功: {backup}")
else:
    print("备份失败")
```

---

## 错误处理

### 常见错误代码

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `安全检查失败` | 目标路径是系统目录 | 使用用户数据目录 |
| `路径不存在` | 目标路径不存在 | 检查路径拼写 |
| `不是目录` | 目标路径是文件 | 检查路径类型 |
| `备份失败` | 无法创建备份 | 检查磁盘空间/权限 |

---

*Color-Filer API Reference v1.0*
