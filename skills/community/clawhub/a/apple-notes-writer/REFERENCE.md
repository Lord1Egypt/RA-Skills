# Apple Notes 自动化写入技能

## 🎯 核心方法

使用 **HTML 格式 + AppleScript** 直接写入备忘录内容。

---

## 📝 完整代码模板

```python
import subprocess

def write_to_notes(title, content_html, note_id=None):
    """
    自动化写入 Apple Notes
    
    Args:
        title: 笔记标题
        content_html: HTML 格式内容
        note_id: 现有笔记 ID（可选，用于更新）
    """
    # 转义特殊字符
    escaped = content_html.replace('\\', '\\\\').replace('"', '\\"')
    
    # 构建 AppleScript
    if note_id:
        script = f'''
        tell application "Notes"
            activate
            try
                set targetNote to note id "{note_id}"
            on error
                set targetFolder to folder "Notes" of account "iCloud"
                set targetNote to make new note at targetFolder with properties {{name:"{title}"}}
            end try
            
            set body of targetNote to "{escaped}"
            
            display notification "✅ 笔记已更新" with title "Notes"
        end tell
        '''
    else:
        script = f'''
        tell application "Notes"
            activate
            set targetFolder to folder "Notes" of account "iCloud"
            set targetNote to make new note at targetFolder with properties {{name:"{title}", body:"{escaped}"}}
            
            display notification "✅ 笔记已创建" with title "Notes"
        end tell
        '''
    
    # 执行
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    
    if result.returncode == 0:
        return True, "成功"
    else:
        return False, result.stderr

# 使用示例
content = """<div>
<h1>笔记标题</h1>
<p>最后更新：2026-03-06</p>

<h2>章节标题</h2>
<p>段落内容</p>

<h3>子标题</h3>
<ul>
<li>列表项 1</li>
<li>列表项 2</li>
</ul>

<ol>
<li>步骤 1</li>
<li>步骤 2</li>
</ol>

<p><i>持续更新中...</i></p>
</div>"""

success, msg = write_to_notes("我的笔记", content)
```

---

## 🎨 支持的 HTML 标签

| 标签 | 效果 | 示例 |
|------|------|------|
| `<h1>` | 大标题（24px 加粗） | `<h1>主标题</h1>` |
| `<h2>` | 中标题（18px 加粗） | `<h2>章节</h2>` |
| `<h3>` | 小标题（18px 加粗） | `<h3>小节</h3>` |
| `<p>` | 段落 | `<p>内容</p>` |
| `<br>` | 换行 | `第一行<br>第二行` |
| `<ul>` | 无序列表 | `<ul><li>项</li></ul>` |
| `<ol>` | 有序列表 | `<ol><li>1</li></ol>` |
| `<b>` | 加粗 | `<b>重要</b>` |
| `<i>` | 斜体 | `<i>备注</i>` |
| `<div>` | 容器（必需） | `<div>...</div>` |

---

## ✅ 特殊符号

| 符号 | 用途 | 示例 |
|------|------|------|
| ✓ | 完成/正确 | ✓ 已完成 |
| ✗ | 失败/错误 | ✗ 失败 |
| ⚠️ | 警告 | ⚠️ 注意 |
| ☐ | 待办复选框 | ☐ 待办事项 |
| ● | 列表圆点 | （自动识别） |
| → | 箭头 | 步骤 1 → 步骤 2 |

---

## 📋 完整示例

```python
content = """<div>
<h1>OpenClaw 实战经验总结</h1>
<p>最后更新：2026-03-06<br>持续更新中...</p>

<h2>环境准备</h2>
<p>必需工具</p>
<ul>
<li>Homebrew（macOS 包管理器）</li>
<li>Node.js（OpenClaw 运行环境）</li>
<li>OpenClaw</li>
</ul>

<h2>邮件配置</h2>
<h3>126 邮箱（不推荐）</h3>
<p>问题：IMAP 无法连接</p>
<p>解决方案</p>
<ul>
<li>✓ 联系 126 客服</li>
<li>✓ 换用其他邮箱</li>
</ul>

<h2>待办事项</h2>
<ul>
<li>☐ 3-20 配置 QQ 邮箱</li>
<li>☐ 测试 backup 功能</li>
</ul>

<p><i>持续更新中...</i></p>
</div>"""

write_to_notes("OpenClaw 实战经验", content)
```

---

## ⚠️ 注意事项

### 必须遵守
1. **最外层必须用 `<div>` 包裹**
2. **所有 HTML 标签必须闭合**
3. **特殊字符必须转义**：
   - `"` → `\\"`
   - `\` → `\\\\`
   - `<` → `&lt;`
   - `>` → `&gt;`

### 避免使用
- ❌ Markdown 语法（`**粗体**` 等）
- ❌ `\n` 换行符（用 `<br>` 代替）
- ❌ 复杂 CSS 样式
- ❌ JavaScript

### 最佳实践
- ✅ 使用语义化 HTML 标签
- ✅ 段落之间用空行分隔
- ✅ 列表用 `<ul>` 或 `<ol>`
- ✅ 特殊符号直接用 Unicode

---

## 🔧 高级用法

### 更新现有笔记
```python
# 使用笔记 ID 更新
note_id = "x-coredata://32B6C268-4DE4-45E5-BAB5-1D2A41F70387/ICNote/p20"
write_to_notes("更新标题", content, note_id=note_id)
```

### 获取笔记 ID
```python
import subprocess

script = '''
tell application "Notes"
    set foundNotes to search notes for "关键词"
    if (count of foundNotes) > 0 then
        return id of item 1 of foundNotes
    end if
end tell
'''
result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
note_id = result.stdout.strip()
```

### 验证写入结果
```python
verify_script = f'''
tell application "Notes"
    set targetNote to note id "{note_id}"
    return body of targetNote
end tell
'''
result = subprocess.run(['osascript', '-e', verify_script], capture_output=True, text=True)
print(result.stdout)
```

---

## 📊 触发词

当用户提到以下内容时，使用此技能：
- "记笔记到备忘录"
- "写入 Apple Notes"
- "创建备忘录"
- "更新备忘录"
- "记录到备忘录"
- "保存到 Apple 备忘录"

---

## 🎯 工作流程

1. **确认需求** - 了解笔记主题和内容
2. **准备内容** - 用 HTML 格式组织内容
3. **转义字符** - 处理特殊字符
4. **执行写入** - 运行 AppleScript
5. **验证结果** - 确认写入成功
6. **反馈用户** - 报告完成情况

---

**最后更新**: 2026-03-06  
**技能版本**: 1.0  
**适用系统**: macOS (Apple Notes)
