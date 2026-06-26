---
name: apple-notes-writer
description: 完美格式写入Apple备忘录。支持HTML格式、Markdown转换、多文件夹管理、自动转义特殊字符。
---

# Apple Notes Writer

将内容以完美格式写入Apple备忘录（macOS only）。

## 功能特性

- ✅ **HTML格式支持** - 标题、列表、粗体、斜体等丰富格式
- ✅ **Markdown转换** - 自动将Markdown转为Apple Notes支持的HTML
- ✅ **特殊字符转义** - 自动处理引号、反斜杠等棘手字符
- ✅ **文件夹管理** - 支持创建文件夹、指定目标文件夹
- ✅ **更新模式** - 可选择更新同名笔记或创建新笔记

## 使用方法

### 方式一：直接调用Python脚本

```bash
# 写入HTML格式内容
python scripts/apple_notes.py write \
    --title "我的笔记" \
    --content "<div><h1>标题</h1><p>内容</p></div>"

# 从Markdown文件写入
python scripts/apple_notes.py write \
    --title "Markdown笔记" \
    --file content.md \
    --markdown

# 写入指定文件夹
python scripts/apple_notes.py write \
    --title "工作笔记" \
    --content "<div><p>内容</p></div>" \
    --folder "工作"

# 更新已存在的笔记
python scripts/apple_notes.py write \
    --title "我的笔记" \
    --content "<div><p>新内容</p></div>" \
    --update

# 读取笔记内容
python scripts/apple_notes.py read --title "我的笔记"

# 列出文件夹中的所有笔记
python scripts/apple_notes.py list --folder "工作"

# 创建新文件夹
python scripts/apple_notes.py create-folder --title "新项目"
```

### 方式二：在Python代码中使用

```python
from scripts.apple_notes import AppleNotesWriter, markdown_to_html

# 创建写入器
writer = AppleNotesWriter(account="iCloud")

# 写入HTML内容
html_content = """<div>
<h1>会议记录</h1>
<p>时间：2024年3月28日</p>
<ul>
    <li>讨论项目进度</li>
    <li>确定下周计划</li>
</ul>
</div>"""

result = writer.write(
    title="会议记录",
    content=html_content,
    folder="工作",
    update_existing=True
)
print(result)  # SUCCESS: Note created/updated - 会议记录

# Markdown转HTML后写入
markdown_text = """
# 学习笔记

## 重点内容

- **第一点**：非常重要
- *第二点*：次要内容

### 总结
这是总结段落。
"""

html = markdown_to_html(markdown_text)
writer.write(title="学习笔记", content=html)
```

## 支持的HTML标签

Apple Notes原生支持以下HTML标签：

| 标签 | 效果 |
|------|------|
| `<h1>` `<h2>` `<h3>` | 大标题、中标题、小标题 |
| `<p>` | 段落 |
| `<br>` | 换行 |
| `<ul>` `<li>` | 无序列表（圆点） |
| `<ol>` `<li>` | 有序列表（数字） |
| `<b>` `<strong>` | 粗体 |
| `<i>` `<em>` | 斜体 |
| `<u>` | 下划线 |
| `<div>` | 容器（必须包裹内容） |

## HTML格式规范

### ✅ 正确示例

```html
<div>
<h1>大标题</h1>
<p>这是一个段落，包含<b>粗体文字</b>和<i>斜体文字</i>。</p>
<ul>
    <li>列表项1</li>
    <li>列表项2</li>
</ul>
</div>
```

### ❌ 错误示例

```html
<!-- 错误：没有外层div包裹 -->
<h1>标题</h1>
<p>内容</p>

<!-- 错误：使用不支持的标签 -->
<div>
<code>代码块</code>  <!-- code标签不支持 -->
<img src="...">    <!-- img标签不支持 -->
</div>

<!-- 错误：未闭合的标签 -->
<div>
<p>内容
</div>
```

## Markdown转换规则

使用 `markdown_to_html()` 函数转换：

| Markdown | 转换结果 |
|----------|----------|
| `# 标题` | `<h1>标题</h1>` |
| `## 标题` | `<h2>标题</h2>` |
| `### 标题` | `<h3>标题</h3>` |
| `**粗体**` | `<b>粗体</b>` |
| `*斜体*` | `<i>斜体</i>` |
| `- 列表项` | `<ul><li>列表项</li></ul>` |
| `1. 列表项` | `<ol><li>列表项</li></ol>` |
| 空行 | `<br>` |

## 特殊字符与符号

### 自动转义的字符

脚本自动处理以下特殊字符：

| 字符 | 处理方式 |
|------|----------|
| `\` | 转义为 `\\` |
| `"` | 转义为 `\"` |
| `'` | 无需转义 |
| `\n` | 转为 `<br>` |
| `<` `>` | HTML转义（Markdown模式） |

### 推荐使用的特殊符号

Apple Notes完美支持以下Unicode符号：

| 符号 | 用途 | 示例 |
|------|------|------|
| ✓ | 完成/正确 | `<li>✓ 已完成</li>` |
| ✗ | 失败/错误 | `<li>✗ 失败</li>` |
| ⚠️ | 警告/注意 | `<p>⚠️ 重要提醒</p>` |
| ☐ | 待办复选框 | `<li>☐ 待办事项</li>` |
| ● | 列表圆点 | （`<ul>`自动显示） |
| → | 箭头/流程 | `<p>步骤1 → 步骤2</p>` |
| 📌 | 标记重点 | `<p>📌 核心结论</p>` |
| 💡 | 提示/想法 | `<p>💡 建议</p>` |

## 触发词

当用户提到以下内容时，使用此技能：

| 触发词 | 场景 |
|--------|------|
| "记笔记到备忘录" | 创建新笔记 |
| "写入Apple Notes" | 创建/更新笔记 |
| "创建备忘录" | 创建新笔记 |
| "更新备忘录" | 更新现有笔记 |
| "记录到备忘录" | 创建新笔记 |
| "保存到Apple备忘录" | 创建新笔记 |
| "添加到备忘录" | 追加内容 |
| "写入备忘录" | 创建新笔记 |

## 工作流程

1. **确认需求** - 了解笔记主题、目标文件夹
2. **准备内容** - 用HTML格式组织内容，或使用Markdown转换
3. **转义字符** - 使用内置函数处理特殊字符
4. **执行写入** - 运行AppleScript创建/更新笔记
5. **验证结果** - 确认内容正确写入
6. **反馈用户** - 报告完成情况和笔记位置

## 高级用法

### 更新现有笔记

通过笔记ID更新已有笔记：

```python
# 获取笔记ID后更新
note_id = "x-coredata://.../ICNote/p20"

script = f'''
tell application "Notes"
    set targetNote to note id "{note_id}"
    set body of targetNote to "{escaped_content}"
end tell
'''

subprocess.run(['osascript', '-e', script])
```

### 验证写入结果

```python
verify_script = f'''
tell application "Notes"
    set targetNote to note id "{note_id}"
    return body of targetNote
end tell
'''
result = subprocess.run(['osascript', '-e', verify_script], 
                     capture_output=True, text=True)
print(result.stdout)  # 打印笔记内容验证
```

## 完整示例

### 示例1：记录会议纪要

```python
from scripts.apple_notes import AppleNotesWriter

writer = AppleNotesWriter()

content = """<div>
<h1>产品评审会议纪要</h1>
<p><b>时间：</b>2024年3月28日 14:00</p>
<p><b>参会人：</b>张三、李四、王五</p>

<h2>讨论事项</h2>
<ul>
    <li>确认Q2产品路线图</li>
    <li>讨论新功能优先级</li>
    <li>确定下周迭代计划</li>
</ul>

<h2>待办事项</h2>
<ul>
    <li><b>张三</b>：完成需求文档（3月30日前）</li>
    <li><b>李四</b>：准备技术方案（4月1日前）</li>
</ul>

<p>---</p>
<p><i>记录时间：2024-03-28 16:30</i></p>
</div>"""

writer.write(
    title="产品评审会议纪要-20240328",
    content=content,
    folder="工作",
    update_existing=True
)
```

### 示例2：从Markdown文件批量导入

```python
import os
from scripts.apple_notes import AppleNotesWriter, markdown_to_html

writer = AppleNotesWriter()
notes_dir = "/path/to/notes"

for filename in os.listdir(notes_dir):
    if filename.endswith('.md'):
        with open(os.path.join(notes_dir, filename), 'r') as f:
            markdown_content = f.read()
        
        html_content = markdown_to_html(markdown_content)
        title = filename.replace('.md', '')
        
        writer.write(
            title=title,
            content=html_content,
            folder="导入的笔记"
        )
        print(f"已导入: {title}")
```

## 注意事项

1. **仅支持macOS** - 依赖AppleScript，Windows/Linux不可用
2. **iCloud账户** - 默认使用iCloud账户，可修改`account`参数
3. **文件夹必须存在** - 写入前确保目标文件夹已创建
4. **HTML标签限制** - 不支持`<code>`、`<img>`、`<table>`等复杂标签
5. **内容长度限制** - 单条笔记建议不超过10MB

## 故障排查

### 问题：笔记创建成功但格式错乱

**原因**：HTML标签未闭合或不支持
**解决**：检查所有标签是否正确闭合，只使用支持的标签

### 问题：特殊字符显示异常

**原因**：引号或反斜杠未正确转义
**解决**：使用脚本内置的转义函数，不要手动转义

### 问题：找不到文件夹

**原因**：文件夹不存在或名称错误
**解决**：先用`create-folder`创建文件夹，或检查文件夹名称

### 问题：AppleScript执行失败

**原因**：权限问题或Apple Notes未运行
**解决**：确保Apple Notes已安装并至少运行过一次，检查自动化权限

## 依赖

- macOS 10.14+
- Python 3.7+
- Apple Notes.app

## 许可证

MIT License
