---
name: create-mckinsey-ppt
description: "Generate McKinsey-style consulting PPTs with python-pptx. Produces professional, elegant presentations with cover, content slides, and ending page."
metadata:
  openclaw:
    requires:
      bins:
        - python
---

# McKinsey-Style PPT Generator

生成麦肯锡风格的咨询PPT文档。支持封面页、执行摘要、卡片式内容、列表、表格等多种布局，自动生成结尾页「谢谢，请指导」。

## 前置条件

```bash
# 确保 python-pptx 已安装
python -m pip install python-pptx
```

## 使用方法

### 方式一：直接用JSON内容字符串（推荐快速使用）

```bash
python <skill-dir>/scripts/mckinsey_ppt_generator.py \
  --title "PPT标题" \
  --subtitle "副标题" \
  --client "客户名称" \
  --date "2026年7月" \
  --content '{"cover_extra":"","sections":[...]}' \
  --output /path/to/output.pptx
```

### 方式二：从JSON文件加载内容

```bash
python <skill-dir>/scripts/mckinsey_ppt_generator.py \
  --title "..." \
  --content content.json \
  --output output.pptx
```

### 方式三：生成后保存到指定网页可访问目录

```bash
python <skill-dir>/scripts/mckinsey_ppt_generator.py \
  --title "..." \
  --subtitle "..." \
  --client "..." \
  --date "..." \
  --content content.json \
  --output /path/to/workspace/documents/file_name.pptx
```

## JSON内容格式

```json
{
  "client": "客户名称（可选）",
  "date": "日期（可选）",
  "cover_extra": "封面额外信息行（可选）",
  "sections": [
    {
      "title": "页面标题",
      "subtitle": "页面副标题（可选）",
      "type": "executive_summary | cards | list | table | text",
      "items": [...],     // executive_summary, cards, list 类型使用
      "content": "...",   // text 类型使用
      "headers": [...],   // table 类型使用
      "rows": [...],      // table 类型使用
      "col_widths": [...] // table 类型使用
    }
  ]
}
```

### 类型说明

| 类型 | 描述 | 关键字段 |
|------|------|---------|
| `executive_summary` | 执行摘要 — 5个纵向卡片 | `items[]` 每个含 `title`, `desc`, `color` |
| `cards` | 卡片网格 | `items[]`, `cols`, `rows`, 每个含 `title`, `desc`, `color` |
| `list` | 垂直列表（左侧色条） | `items[]` 每个含 `title`, `desc`, `color` |
| `table` | 数据表格 | `headers[]`, `rows[][]`, `col_widths[]`, `footnote` |
| `text` | 纯文本页面 | `content` |

### 可用颜色名称

`navy`, `dark_blue`, `mid_blue`, `light_blue`, `teal`, `purple`, `red`, `green`, `orange`, `gold`

也支持 `#RRGGBB` 格式的十六进制颜色。

## 工作流程

1. **确认用户需求** — 理解用户想要生成的PPT主题
2. **准备内容** — 通过对话获取用户提供的文字/数据/要点
3. **构建JSON** — 将用户内容组织成上述JSON格式
4. **运行生成脚本**
   ```bash
   python <skill-dir>/scripts/mckinsey_ppt_generator.py \
     --title "..." \
     --subtitle "..." \
     --content '...' \
     --output output.pptx
   ```
5. **交付** — 提供PPT文件路径给用户

## 输出说明

- 自动生成**封面页**（深蓝色麦肯锡风格）
- 根据 `sections` 依次生成内容页
- **结尾页**固定为「谢谢，请指导」（深蓝背景）
- 每页底部有 `CONFIDENTIAL AND PROPRIETARY — 页码`
- 页面尺寸：13.333" × 7.5"（宽屏16:9）

## 示例

```bash
python <skill-dir>/scripts/mckinsey_ppt_generator.py ^
  --title "企业数字化转型战略规划" ^
  --subtitle "打造行业级工业互联网平台" ^
  --client "示例科技有限公司" ^
  --date "2026年7月" ^
  --content "{\"cover_extra\":\"\",\"sections\":[{\"title\":\"市场分析\",\"type\":\"cards\",\"cols\":3,\"rows\":1,\"items\":[{\"title\":\"趋势一\",\"desc\":\"描述内容\",\"color\":\"navy\"},{\"title\":\"趋势二\",\"desc\":\"描述内容\",\"color\":\"teal\"},{\"title\":\"趋势三\",\"desc\":\"描述内容\",\"color\":\"green\"}]}]}" ^
  --output digital_transformation.pptx
```
