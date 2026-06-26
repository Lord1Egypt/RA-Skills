# 故障排除

本指南解决使用 `document-organizer` 技能时可能遇到的常见问题。

---

## 快速诊断

在寻求帮助前，请运行：

```bash
npx skills run document-organizer --source "你的目录" --dry-run --verbose
```

查看输出，然后对照下面的分类查找解决方案。

---

## 错误代码汇总

| 错误代码 | 说明 | 严重程度 | 自动重试 |
|---------|------|---------|---------|
| `E001` | LibreOffice 未找到 | 高 | 否 |
| `E002` | LibreOffice 转换超时 | 中 | 是（跳过文件）|
| `E003` | MarkItDown 导入失败 | 高 | 否 |
| `E004` | 源文件损坏 | 低 | 否 |
| `E005` | 权限不足 | 高 | 否 |
| `E006` | 磁盘空间不足 | 高 | 否 |
| `E007` | 编码错误（非 UTF-8）| 中 | 否 |
| `E008` | 临时文件清理失败 | 低 | 是（忽略）|

---

## 分类问题解决

### 🔴 严重错误（阻止运行）

#### E001: LibreOffice 未找到

**症状**:
```
❌ 未找到 LibreOffice，请安装或指定路径
```

**原因**:
- LibreOffice 未安装
- 未添加到 PATH
- 安装路径非标准

**解决**:

1. **验证安装**:
```bash
where soffice  # Windows
which soffice  # Linux/macOS
```

2. **安装 LibreOffice**:
   - 下载: https://zh-cn.libreoffice.org/
   - 安装到默认位置

3. **显式指定路径**:
```bash
npx skills run document-organizer \
  --source "docs" \
  --soffice-path "D:\Program Files\LibreOffice\program\soffice.exe"
```

4. **添加到 PATH** (Windows):
   - 系统属性 → 环境变量 → PATH
   - 添加: `D:\Program Files\LibreOffice\program`
   - 重启终端

---

#### E003: MarkItDown 未安装

**症状**:
```
ModuleNotFoundError: No module named 'markitdown'
```

**原因**:
- Python 依赖未安装
- 虚拟环境未激活
- 安装不完整

**解决**:

1. **检查 Python 环境**:
```bash
python --version  # 应 >= 3.10
which python      # 确认使用的 Python
```

2. **安装依赖**:
```bash
# 完整功能（推荐）
pip install 'markitdown[all]'

# 或仅需要的格式
pip install 'markitdown[docx,xlsx,pdf]'
```

3. **验证安装**:
```bash
python -c "import markitdown; print(markitdown.__version__)"
```

4. **OpenClaw 技能专用**:
```bash
# 在技能目录内安装
cd d:\workspace\clawd\skills\document-organizer
pip install -e .
```

---

#### E005: 权限不足

**症状**:
```
PermissionError: [Errno 13] Permission denied
```

**原因**:
- 源目录只读
- 输出目录无写入权限
- 文件被其他进程占用

**解决**:

1. **Windows**:
   - 右键目录 → 属性 → 安全
   - 添加当前用户，赋予完全控制
   - 或以管理员身份运行终端

2. **Linux/macOS**:
```bash
sudo chmod -R u+rwX /path/to/directory
```

3. **检查文件占用**:
```bash
# Windows: 使用 Process Explorer
# Linux: lsof | grep filename
```

4. **关闭占用程序**:
   - 关闭 Word/Excel 中打开的文件
   - 关闭索引服务

---

#### E006: 磁盘空间不足

**症状**:
```
OSError: [Errno 28] No space left on device
```

**原因**:
- 源文件巨大（如高清 PDF）
- 临时目录空间不足
- 输出目录磁盘已满

**解决**:

1. **检查空间**:
```bash
# Windows
dir C:\  # 查看剩余空间

# Linux
df -h
```

2. **清理临时文件**:
```bash
# 手动清理旧的转换临时文件
rm -rf ./temp_batch/*
```

3. **移动临时目录**:
```bash
npx skills run document-organizer \
  --source "docs" \
  --temp-dir "D:\LargeSSD\temp" \
  --output "D:\LargeSSD\output"
```

4. **分批处理**:
```bash
# 按子目录分批运行
npx skills run document-organizer --source "docs/subdir1"
npx skills run document-organizer --source "docs/subdir2"
```

---

### 🟡 警告错误（跳过个别文件）

#### E002: 转换超时

**症状**:
```
Timeout: LibreOffice conversion of file.doc
```

**原因**:
- 文件过大（>100MB）
- LibreOffice 进程卡死
- 系统资源不足

**解决**:

1. **增加超时**（修改脚本）:
```python
# 将 timeout=300 改为 timeout=600
```

2. **排除大文件**:
```bash
# 先转换小文件
find . -size -50M -name "*.doc"  # 仅 <50MB
```

3. **手动转换大文件**:
```bash
# 用 LibreOffice GUI 打开大文件另存为
```

4. **检查 LibreOffice 状态**:
```bash
tasklist | findstr soffice  # Windows
ps aux | grep soffice       # Linux
```

**自动恢复**: ✅ 脚本自动跳过超时文件，继续其他文件

---

#### E004: 源文件损坏

**症状**:
```
Error: cannot open file (damaged or corrupted)
```

**原因**:
- 文件系统错误
- 传输中断导致的不完整文件
- 文件格式不匹配（如 .doc 实际是 .pdf）

**解决**:

1. **验证文件**:
```bash
# Windows
certutil -hashfile file.doc MD5

# Linux
md5sum file.doc
```

2. **尝试手动打开**:
   - 用 Word/Excel 打开文件
   - 是否能正常打开？

3. **修复尝试**:
   - Word/Excel → 打开 → 修复
   - 或另存为新格式

4. **跳过方法**:
```python
# 在脚本中添加文件大小检查
if file.size < 100:  # <100 字节可能是损坏文件
    continue
```

**自动恢复**: ✅ 损坏文件跳过，记录到日志

---

#### E007: 编码错误

**症状**:
```
UnicodeDecodeError: 'gbk' codec can't decode...
```

**原因**:
- 源文件编码非 UTF-8（如 GB2312）
- 控制台编码限制（PowerShell GBK）

**说明**: 这是**控制台显示问题，不是文件问题**。输出文件仍是 UTF-8。

**解决（控制台）**:
```powershell
# Windows PowerShell
chcp 65001  # 切换 UTF-8 代码页
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
```

**解决（源文件）**:
```python
# 在转换时指定编码
result = md_converter.convert(str(src_file), encoding='gb2312')
```

---

### 🟢 低优先级问题

#### E008: 临时文件清理失败

**症状**:
```
PermissionError: [WinError 5] Access is denied: 'temp\\...'
```

**原因**:
- 文件被其他进程锁定
- 权限不足

**影响**: 磁盘空间占用，下次运行可能冲突

**解决**:
```bash
# 手动删除
rmdir /s /q temp_batch  # Windows
rm -rf temp_batch       # Linux/macOS

# 或在脚本末尾使用
shutil.rmtree(temp_root, ignore_errors=True)
```

**自动恢复**: ✅ 下一个 run 会清理旧的临时文件

---

## 性能问题

### 问题: 转换太慢

**诊断**:
```bash
# 测量单个文件时间
time markitdown large.pdf
```

**优化**:
1. **检查 `.doc` 比例**: `.doc` 最慢，批量优化已应用
2. **使用 SSD**: 临时目录放在 SSD
3. **减少 PDF OCR**: OCR 很慢，避免 `--ocr` 除非必要
4. **并行处理**: 修改脚本使用 `ThreadPoolExecutor`

---

### 问题: 内存占用高

**症状**:
- 转换大文件时内存飙升
- 系统卡顿

**原因**:
- MarkItDown 一次性加载整个文件
- Python 垃圾回收延迟

**解决**:
```bash
# 1. 分批处理
--limit 100  # 每次只处理 100 个

# 2. 使用流式 API（需修改脚本）
result = md.convert_stream(file_handle, streaming=True)

# 3. 重启脚本（内存泄漏）
```

---

## 文件特定问题

### 问题: 某个文件总是失败

**诊断步骤**:

1. **检查文件基本信息**:
```bash
# 大小、扩展名
ls -lh problematic.doc

# 文件类型检测
file problematic.doc  # Linux/macOS
```

2. **手动转换测试**:
```bash
# 测试 LibreOffice
soffice --headless --convert-to markdown problematic.doc

# 测试 MarkItDown
python -c "from markitdown import MarkItDown; MarkItDown().convert('problematic.doc')"
```

3. **查看详细错误**:
```bash
# 启用详细模式
npx skills run document-organizer --verbose --source "docs" 2>&1 | tee debug.log
```

4. **常见原因**:
   - 文件名包含特殊字符（`?`, `*`, `:`）
   - 路径过长（Windows > 260 字符）
   - 文件被锁定

**绕过方法**:
```bash
# 1. 重命名文件（去除特殊字符）
# 2. 使用短路径（Windows: \\?\ 前缀）
# 3. 排除该文件 --exclude "problematic.doc"
```

---

## 日志分析

### 日志文件结构

```log
# 转换失败记录 (2026-03-11 13:00:00)

## LibreOffice 转换失败
- G:\docs\file1.doc: Exit code: 1, stderr: ...

## MarkItDown 转换失败
- G:\docs\file2.xlsx: Traceback...
```

### 常见错误消息

| 错误消息 | 含义 | 解决 |
|---------|------|------|
| `Exit code: 1` | LibreOffice 内部错误 | 文件损坏 |
| `Timeout` | 超过 300 秒 | 文件太大，增加超时 |
| `Unsupported format` | 格式不识别 | 文件不是标准格式 |
| `FileNotFoundError` | 文件不存在 | 路径错误，已被移动/删除 |
| `MemoryError` | 内存不足 | 分批处理 |

---

## 调试模式

### 启用详细日志

```bash
npx skills run document-organizer \
  --source "docs" \
  --verbose \
  --log-file "debug-$(date +%s).log" \
  2>&1 | tee full_debug.log
```

### 检查中间文件

```bash
# 临时目录保留（不自动删除）
# 修改脚本: shutil.rmtree(temp_root, ignore_errors=True)  # 注释掉
# 或设置 --keep-temp

# 查看 LibreOffice 生成的中间文件
ls temp_batch/docs/
```

---

## 获取帮助

### 1. 自检

```bash
# 版本信息
python -c "import markitdown; print(markitdown.__version__)"
soffice --version

# 环境信息
npx skills run document-organizer --version
```

### 2. 查看文档

- `skills/document-organizer/README.md`
- `skills/document-organizer/references/` 全套参考资料

### 3. 社区支持

- OpenClaw Discord: https://discord.com/invite/clawd
- GitHub Issues: https://github.com/openclaw/openclaw/issues

---

## 常见问题速查

| 问题 | 症状 | 一键解决 |
|------|------|---------|
| LibreOffice 找不到 | `E001` | `--soffice-path "正确路径"` |
| 转换慢 | 10+ 分钟 | 临时目录放到 SSD |
| 个别文件失败 | E002/E004 | 查看日志，手动修复或排除 |
| 中文乱码 | 控制台显示问题 | 切换代码页 `chcp 65001` |
| 磁盘满 | `E006` | 清理临时目录，分批处理 |
| 内存溢出 | 程序崩溃 | `--limit 50` 分批处理 |

---

**最后更新**: 2026-03-11  
**维护状态**: ✅ 活跃维护  
**报告问题**: https://github.com/openclaw/openclaw/issues
