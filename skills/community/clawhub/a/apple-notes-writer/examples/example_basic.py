#!/usr/bin/env python3
"""
Apple Notes Writer 基础示例
"""

import sys
sys.path.insert(0, '../scripts')

from apple_notes import AppleNotesWriter

# 创建写入器
writer = AppleNotesWriter(account="iCloud")

# 示例1：写入简单HTML内容
print("=== 示例1：写入简单HTML ===")
html_content = """<div>
<h1>我的第一条笔记</h1>
<p>这是使用Apple Notes Writer创建的笔记。</p>
<ul>
    <li>支持HTML格式</li>
    <li>自动转义特殊字符</li>
    <li>完美格式显示</li>
</ul>
</div>"""

result = writer.write(
    title="测试笔记-基础示例",
    content=html_content,
    folder="Notes"
)
print(result)

# 示例2：写入带格式的复杂内容
print("\n=== 示例2：复杂格式 ===")
complex_content = """<div>
<h2>会议纪要</h2>
<p><b>日期：</b>2024年3月28日</p>
<p><i>记录人：</i>AI助手</p>

<h3>讨论要点</h3>
<ul>
    <li><b>重点项目</b>：进度正常</li>
    <li><i>待跟进</i>：需要确认需求</li>
    <li>下次会议时间：下周一</li>
</ul>

<p>---</p>
<p>如有疑问请联系相关人员。</p>
</div>"""

result = writer.write(
    title="会议纪要-20240328",
    content=complex_content,
    folder="Notes",
    update_existing=True
)
print(result)

# 示例3：列出所有笔记
print("\n=== 示例3：列出笔记 ===")
notes = writer.list_notes("Notes")
print(f"找到 {len(notes)} 条笔记:")
for note in notes[:5]:  # 只显示前5条
    print(f"  - {note}")

# 示例4：读取笔记内容
print("\n=== 示例4：读取笔记 ===")
content = writer.read("测试笔记-基础示例", "Notes")
if content:
    print(f"笔记内容（前200字符）:\n{content[:200]}...")
else:
    print("笔记不存在")

print("\n=== 示例完成 ===")
