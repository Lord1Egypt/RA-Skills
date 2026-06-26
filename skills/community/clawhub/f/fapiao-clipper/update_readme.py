#!/usr/bin/env python3
"""Update README with Web UI section"""

readme_path = Path("/Users/alanli/.openclaw/workspace/skills/fapiao-clipper/README.md")

with open(readme_path) as f:
    content = f.read()

# Web UI section to insert
web_ui_section = """
### 4. Web UI 界面（可选）

发票夹子提供图形化 Web 界面，更适合财务人员日常使用：

```bash
# 启动 Web UI
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`，界面如下：

![Web UI 截图](./docs/web-ui-screenshot.png)

**功能说明**：
- **📤 扫描发票**：拖拽上传 PDF/图片，实时显示识别结果
- **📋 发票列表**：表格展示所有发票，支持状态筛选和批量操作
- **🔍 查询筛选**：按日期范围、销售方、购买方精准查找
- **📥 导出报销**：一键导出 Excel 明细表 + PDF 报销包

**特点**：
- 无需命令行，浏览器即可操作
- 实时预览，识别结果即时可见
- 批量管理，支持多选标记排除/恢复
"""

# Insert after "🎉 完成！文件在..."
insert_marker = "🎉 完成！文件在 `~/Documents/发票夹子/exports/`，直接发给财务。"
if insert_marker in content:
    content = content.replace(
        insert_marker,
        insert_marker + web_ui_section
    )
    print("✅ Web UI section added to README")
else:
    print("⚠️ Marker not found")

with open(readme_path, "w") as f:
    f.write(content)
