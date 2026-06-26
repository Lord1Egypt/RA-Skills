---
name: docx-tools
description: "Word文档处理工具集 - 支持DOCX/Markdown互转、文档读取写入、多章节整合。纯本地操作，无需网络，安全可靠。"
metadata:
  openclaw:
    emoji: 📝
---

# docx-tools - Word文档处理工具集

安全、本地、高效的Word文档处理工具集。纯本地操作，无需网络连接。

---

## 🎯 一句话定义

提供Word文档(DOCX)与Markdown的互转、内容读取/写入、多章节整合等功能，支持基金申请书、论文等学术文档的自动化处理。

---

## 📥 如何调用 (How to use me)

**触发语句：**
- "读取Word文档"
- "将Markdown转成Word"
- "合并多个Word章节"
- "提取文档内容"

**需要提供的信息：**
1. **必需：** 操作类型（读/写/转换/整合）、文件路径
2. **可选：** 输出格式、样式要求

---

## 🔄 执行逻辑 (What I do)

### Step 1: 任务识别
- 📖 **读取** → 进入 Step 2A
- ✍️ **写入** → 进入 Step 2B
- 🔄 **转换** → 进入 Step 2C
- 📦 **整合** → 进入 Step 2D

### Step 2A: 读取流程
1. 验证文件存在性和格式
2. 使用 python-docx 读取文档
3. 提取段落文本和格式信息
4. 返回结构化数据

### Step 2B: 写入流程
1. 创建新文档或打开现有文档
2. 根据输入添加段落/表格
3. 应用格式设置
4. 保存到指定路径

### Step 2C: 转换流程
- DOCX → Markdown：提取文本，保留标题层级
- Markdown → DOCX：解析MD，生成对应样式段落

### Step 2D: 整合流程
1. 读取多个章节文件
2. 按顺序合并内容
3. 统一格式和样式
4. 生成完整文档

---

## 🛠️ 工具详解

### 1. read_docx - 读取Word文档

**功能：** 提取Word文档的文本内容和基本格式

**使用示例：**
```python
from docx_tools.read_docx import read_docx

# 读取文档
content = read_docx("D:/docs/申请书.docx")

# 返回结构
{
    "paragraphs": [
        {"text": "段落文本", "style": "Heading 1"},
        {"text": "正文内容", "style": "Normal"}
    ],
    "tables": [...],  # 表格数据
    "metadata": {...} # 文档属性
}
```

**参数说明：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| file_path | str | ✅ | Word文档路径 |
| include_styles | bool | ❌ | 是否包含样式信息，默认True |
| extract_tables | bool | ❌ | 是否提取表格，默认True |

---

### 2. write_docx - 写入Word文档

**功能：** 创建新Word文档或修改现有文档

**使用示例：**
```python
from docx_tools.write_docx import write_docx

# 创建新文档
doc = write_docx.create_document()

# 添加标题
write_docx.add_heading(doc, "第一章 立项依据", level=1)

# 添加段落
write_docx.add_paragraph(doc, "这是正文内容...")

# 保存
write_docx.save(doc, "D:/output/新文档.docx")
```

**参数说明：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| document | Document | ✅ | docx文档对象 |
| text | str | ✅ | 要添加的文本 |
| style | str | ❌ | 段落样式，默认"Normal" |
| font_name | str | ❌ | 字体名称，如"宋体" |
| font_size | int | ❌ | 字号，如12 |

---

### 3. docx_to_md - DOCX转Markdown

**功能：** 将Word文档转换为Markdown格式

**使用示例：**
```python
from docx_tools.docx_to_md import convert

# 转换文档
markdown_text = convert(
    input_path="D:/docs/论文.docx",
    output_path="D:/output/论文.md"
)

# 或仅获取文本不保存
md_text = convert("D:/docs/论文.docx", save=False)
```

**参数说明：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| input_path | str | ✅ | 输入DOCX路径 |
| output_path | str | ❌ | 输出MD路径，默认不保存 |
| save | bool | ❌ | 是否保存文件，默认True |

---

### 4. md_to_docx - Markdown转DOCX

**功能：** 将Markdown文件转换为Word文档

**使用示例：**
```python
from docx_tools.md_to_docx import convert

# 转换
convert(
    input_path="D:/docs/内容.md",
    output_path="D:/output/文档.docx",
    template="D:/templates/基金模板.docx"  # 可选：使用模板
)
```

**支持的Markdown语法：**
- 标题（# ## ###）
- 粗体、斜体
- 列表（有序/无序）
- 表格
- 代码块（作为普通文本）

---

### 5. integrate_proposal - 整合申请书章节

**功能：** 将多个章节文件合并为完整的申请书

**使用示例：**
```python
from docx_tools.integrate_proposal import integrate

# 定义章节顺序
sections = [
    {"file": "D:/chapters/摘要.docx", "title": "摘要"},
    {"file": "D:/chapters/立项依据.docx", "title": "一、立项依据"},
    {"file": "D:/chapters/研究内容.docx", "title": "二、研究内容"},
    {"file": "D:/chapters/研究基础.docx", "title": "三、研究基础"}
]

# 整合
integrate(
    sections=sections,
    output_path="D:/output/完整申请书.docx",
    add_page_breaks=True,  # 章节间添加分页
    unify_styles=True      # 统一格式
)
```

**参数说明：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| sections | list | ✅ | 章节文件列表 |
| output_path | str | ✅ | 输出路径 |
| add_page_breaks | bool | ❌ | 章节间分页，默认True |
| unify_styles | bool | ❌ | 统一样式，默认True |

---

## 💡 典型使用场景

### 场景1: 基金申请书整合
```python
# 整合分散撰写的各章节
integrate(
    sections=[
        {"file": "摘要.docx", "title": "摘要"},
        {"file": "立项依据.docx", "title": "一、立项依据与研究内容"},
        {"file": "研究方案.docx", "title": "二、研究方案"},
        {"file": "创新点.docx", "title": "三、创新点"},
        {"file": "研究基础.docx", "title": "四、研究基础与工作条件"}
    ],
    output_path="NSFC申请书_完整版.docx"
)
```

### 场景2: 批量读取多个文档
```python
import os
from docx_tools.read_docx import read_docx

# 批量读取文件夹内所有文档
folder = "D:/papers"
contents = []

for file in os.listdir(folder):
    if file.endswith('.docx'):
        path = os.path.join(folder, file)
        content = read_docx(path)
        contents.append({"file": file, "content": content})
```

### 场景3: Markdown转Word提交
```python
# 用Markdown写作，最终转为Word提交
md_to_docx(
    input_path="论文.md",
    output_path="论文_提交版.docx",
    template="期刊格式模板.docx"
)
```

---

## ⚙️ 配置与依赖

### 安装依赖
```bash
pip install python-docx markdown
```

### 系统要求
- Python 3.8+
- Windows/Linux/macOS
- **无需安装Microsoft Word**

---

## 🔒 安全特性

| 特性 | 说明 |
|------|------|
| ✅ 纯本地操作 | 不连接网络，不上传文件 |
| ✅ 无外部依赖 | 仅使用 python-docx 库 |
| ✅ 沙盒限制 | 只在指定目录操作 |
| ✅ 只读默认 | 写操作需要显式路径 |

---

## 🐛 故障排除

### 问题："ModuleNotFoundError: No module named 'docx'"
**解决：** 安装依赖 `pip install python-docx`

### 问题："Package not found at 'xxx.docx'"
**解决：** 检查文件路径是否正确，文件是否存在

### 问题：中文显示为方框或乱码
**解决：** 指定中文字体
```python
write_docx.add_paragraph(doc, "中文内容", font_name="宋体")
```

### 问题：表格格式丢失
**解决：** 复杂表格建议手动调整，简单表格转换正常

### 问题：Markdown中的公式未正确转换
**解决：** docx-tools 不支持LaTeX公式转换，建议保留为文本或截图

---

## 📊 与 word-vba 技能的区别

| 特性 | docx-tools | word-vba |
|------|------------|----------|
| 依赖 | python-docx (纯Python) | Microsoft Word |
| 平台 | 跨平台 | 仅Windows |
| 速度 | 快 | 较慢（需启动Word） |
| 格式保留 | 基本格式 | 完整格式（包括复杂样式） |
| 适用场景 | 批量处理、简单操作 | 精确格式控制 |

**建议：**
- 批量处理、简单读写 → **docx-tools**
- 复杂格式、精确控制 → **word-vba**

---

_技能版本: v2.0_  
_更新日期: 2026-03-04_  
_更新说明: 完善文档，添加详细使用示例和参数说明_
