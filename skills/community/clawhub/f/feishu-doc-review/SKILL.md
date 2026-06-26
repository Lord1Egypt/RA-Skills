---
name: feishu-doc-review
description: |
  飞书云文档修订工具。支持三种文档标注操作：高亮文字、添加下划线、插入批注（评论）。

  **当以下情况时使用此 Skill**：
  (1) 需要对飞书文档中的文字添加高亮颜色
  (2) 需要对飞书文档中的文字添加下划线
  (3) 需要在飞书文档中插入批注/评论
  (4) 用户说"帮我高亮这段"、"加个批注"、"给这个词加下划线"、"标注一下"、"review一下文档"
  (5) 审阅、修订飞书文档场景
---

# Feishu Doc Review（飞书文档修订）SKILL

## 三种操作

### 操作一：高亮文字

调用 `feishu_doc`（action: `color_text`），指定 block_id 和颜色。

**支持颜色值（背景高亮）：**
- `yellow`：黄色高亮（最醒目，推荐）
- `green`：绿色高亮
- `blue`：蓝色高亮
- `red`：红色高亮
- `purple`：紫色高亮
- `grey`：灰色高亮
- `orange`：橙色高亮

**执行步骤：**
1. 用 `feishu_doc`（action: `list_blocks`）找到目标文字所在的 block_id
2. 用 `feishu_doc`（action: `color_text`）对该 block 设置背景色

### 操作二：下划线

调用 `feishu_doc`（action: `update_block`），在 text_element_style 中设置 `underline: true`。

**执行步骤：**
1. 用 `feishu_doc`（action: `get_block`）获取目标 block 的当前内容结构
2. 用 `feishu_doc`（action: `update_block`）修改样式，添加 underline

### 操作三：批注（评论）

调用飞书 Comment API，直接 POST 到文档评论接口。

**API 路径：**
```
POST https://open.feishu.cn/open-apis/drive/v1/files/{doc_token}/comments?file_type=docx
```

**鉴权：**
- 使用环境变量中的飞书 App 配置获取 tenant_access_token
- App ID: `cli_a92d5b4257391bcb`
- App Secret: 通过环境变量 `FEISHU_APP_SECRET` 读取（或直接用已知值）

**请求体结构：**
```json
{
  "reply_list": {
    "replies": [{
      "content": {
        "elements": [{
          "type": "text_run",
          "text_run": {
            "text": "批注内容"
          }
        }]
      }
    }]
  }
}
```

**执行脚本：**调用 `scripts/add_comment.sh`，传入 doc_token 和批注内容。

---

## 执行流程

### 用户说"帮我高亮XXX"时：
1. 确认目标文档 URL（提取 doc_token）
2. `list_blocks` 找到包含目标文字的 block
3. `color_text` 设置高亮颜色（默认 yellow）
4. 报告完成

### 用户说"帮我加批注：XXX"时：
1. 确认目标文档 URL（提取 doc_token）
2. 调用 `scripts/add_comment.sh {doc_token} "{批注内容}"`
3. 报告批注 ID

### 用户说"帮我对XXX加下划线"时：
1. 确认目标文档 URL
2. `list_blocks` + `get_block` 定位目标 block
3. `update_block` 修改 underline 样式
4. 报告完成

---

## 注意事项

- 批注是文档级别的，不锁定到特定段落（飞书 API 当前限制）
- 高亮和下划线操作针对整个 block，无法精确到 block 内的部分文字（飞书 API 限制）
- 操作前先确认 doc_token 正确
- 批注内容建议控制在 500 字以内
