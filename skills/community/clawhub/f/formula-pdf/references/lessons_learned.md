# 公式PDF生成经验教训

## ⚠️ 关键！不要杀Edge进程

**之前犯的错：** 用 `Stop-Process -Name msedge -Force` 杀Edge进程

**后果：**
- 用户正在用的Edge浏览器窗口也会被杀
- 实际上headless模式可以和普通Edge共存
- 杀进程并不会导致HTML文件被删，杀进程不是文件丢失的原因

**正确做法：** 不需要杀进程。直接跑新的headless实例就行。

## ⚠️ 关键！写HTML文件的正确方式

**之前犯的错：** 用 `write` 工具直接写含复杂符号的HTML

**原因：** HTML内容含大量双引号（`"`）和反斜杠（`\frac`、`\lim`），在XML/JSON参数传递时序列化错误，`path`和`content`被拼接成一个字符串，文件写不进去。

**正确做法：**

```powershell
# 方法1：PowerShell here-string（推荐）
@'
<html>...</html>
'@ | Out-File -FilePath F:\openclaw\file.html -Encoding UTF8
```

```python
# 方法2：Python写文件（内容无编码问题）
F:\Python\python.exe -c "
with open('<output_dir>/file.html', 'w', encoding='utf-8') as f:
    f.write('''<html>...</html>''')
"
```

**不要用 write 工具写含大量引号和反斜杠的HTML文件。**

## ⚠️ 关键！不要杀Edge进程

**之前犯的错：** 用 `Stop-Process -Name msedge -Force` 杀Edge进程

**后果：**
- 用户正在用的Edge浏览器窗口也会被杀
- 实际上headless模式可以和普通Edge共存
- 杀进程并不会导致HTML文件被删，杀进程不是文件丢失的原因

**正确做法：** 不需要杀进程。直接跑新的headless实例就行。

## ⚠️ 关键！写HTML文件的正确方式

**之前犯的错：** 用 `write` 工具直接写含复杂符号的HTML

**原因：** HTML内容含大量双引号（`"`）和反斜杠（`\frac`、`\lim`），在XML/JSON参数传递时序列化错误，`path`和`content`被拼接成一个字符串，文件写不进去。

**正确做法：**

```powershell
# 方法1：PowerShell here-string（推荐）
@'
<html>...</html>
'@ | Out-File -FilePath F:\openclaw\file.html -Encoding UTF8
```

```python
# 方法2：Python写文件（内容无编码问题）
F:\Python\python.exe -c "
with open('<output_dir>/file.html', 'w', encoding='utf-8') as f:
    f.write('''<html>...</html>''')
"
```

**不要用 write 工具写含大量引号和反斜杠的HTML文件。**

## 实战发现的问题

### 1. MathJax渲染延迟问题
**现象：** PDF中公式显示为原始LaTeX代码（如`\frac`, `\lim`, `$$`）  
**原因：** Edge无头模式在MathJax还没渲染完就打印PDF了  
**解决方案：**
- `--virtual-time-budget=30000`（30秒等待时间）
- 至少保证20秒以上，网络慢的话要更久
- 转换后立即验证PDF内容中是否含LaTeX原始代码

**验证脚本：**
```python
import fitz
def verify_formulas(pdf_path):
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    patterns = [r'\frac', r'\sqrt', r'\lim', r'\sum', r'\int', r'$$']
    if any(p in text for p in patterns):
        print("公式未渲染！")
```

### 2. 文件名与路径问题
**问题：**
- 中文文件名在Edge命令行中可能乱码
- file://协议必须用正斜杠，不能用Windows反斜杠
- 输出路径含空格需要引号

**最佳实践：**
```powershell
# ✅ 正确
& 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' `
    --headless=new --virtual-time-budget=30000 `
    --print-to-pdf="F:\openclaw\output.pdf" `
    --no-margins "file:///<output_dir>/input.html"

# ❌ 错误（中文文件名、Windows路径）
msedge.exe --headless=new --print-to-pdf=F:\文档.pdf --no-margins F:\输入.html
```

### 3. Edge进程冲突
**现象：** Edge已在运行，导致无头模式冲突  
**解决方案：**
```powershell
# 转换前清理进程
Stop-Process -Name msedge -Force -ErrorAction SilentlyContinue
```

### 4. 超时设置
**发现：**
- `--virtual-time-budget=5000`（5秒）不够
- 公式越多、越复杂，需要时间越长
- 推荐30秒起步，复杂文档用60秒

### 5. CDN依赖风险
**风险点：**
- 如果Edge无头模式网络受限，无法加载MathJax CDN
- 公式就无法渲染
- 目前暂未遇到，但理论上可能

**应对（暂未实施）：**
- 本地部署MathJax（过于复杂）
- 用Python matplotlib渲染公式（中文字体问题）
- 保持CDN，遇到问题再处理

## 完整工作流程（改进版）

1. **编写HTML**
   - 用英文命名文件（`physics_formula.html`）
   - 在head里加MathJax配置和CDN
   - 内容用`$...$`和`$$...$$`写公式
   - CSS包含中文字体设置

2. **清理环境**
   ```powershell
   Stop-Process -Name msedge -Force -ErrorAction SilentlyContinue
   ```

3. **转换为PDF**
   ```powershell
   & 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' `
       --headless=new `
       --virtual-time-budget=30000 `
       --print-to-pdf="F:\openclaw\output.pdf" `
       --no-margins `
       file:///<output_dir>/input.html
   ```

4. **验证结果**
   - 用pymupdf检查是否含LaTeX原始代码
   - 如果未渲染，增加`--virtual-time-budget`重试
   - 确认PDF文件大小正常（>100KB）

5. **发送用户**
   ```python
   message(action="send", filePath="PDF路径", message="公式已渲染")
   ```

## 故障排除表

| 现象 | 可能原因 | 解决方案 |
|------|----------|----------|
| PDF文件为空/很小 | Edge进程冲突 | 杀掉msedge进程重试 |
| 公式显示为代码 | MathJax没渲染完 | 增加`--virtual-time-budget` |
| PDF未生成 | 文件路径问题 | 检查file://协议和路径格式 |
| 中文乱码 | 字体未指定 | CSS加`font-family: 'Microsoft YaHei'` |
| 转换超时 | 文档太复杂 | 增加超时到60秒 |

## 未来优化方向

### 短期优化
- 脚本集成进程清理
- 自动重试机制（公式未渲染时）
- 模板库（报告、笔记、试卷格式）

### 中期优化
- 从markdown自动生成HTML
- 公式缓存（减少重复渲染时间）
- 多语言支持（英文公式模板）

### 长期愿景
- 离线MathJax支持（无网络环境）
- 自动公式编号和引用
- 与LaTeX编译集成

---

**总结：** 目前方案在实践中验证可用，公式渲染成功，PDF质量合格。核心是**足够的等待时间**和**正确的路径格式**。Edge无头模式稳定可靠，MathJax CDN速度快，两者结合是公式PDF的最优解。