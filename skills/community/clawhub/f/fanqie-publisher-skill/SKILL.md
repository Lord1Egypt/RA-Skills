---
name: fanqie-novel-publisher
description: 番茄小说章节自动发布工具。使用场景：(1) 发布单个章节到番茄小说平台；(2) 批量发布多个章节；(3) 存入草稿箱；(4) 登录番茄小说作家后台；(5) 查看作品列表和状态。触发词：番茄发布、番茄小说上传、发布章节、存入草稿箱、番茄登录。
---

# 番茄小说自动发布

自动化发布小说章节到番茄小说作家后台。

## 快速开始

```bash
cd /path/to/fanqie-publisher-skill/scripts
pip install -r requirements.txt
playwright install
```

## 常用命令

```bash
# 登录（扫码）
python main.py login

# 查看作品列表
python main.py works

# 检查登录状态
python main.py status

# 交互式发布
python main.py publish
```

## 发布模式

支持两种发布模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `publish` | 直接发布章节 | 确认内容无误，直接发布 |
| `draft` | 存入草稿箱 | 内容待完善，先保存草稿 |

## 发布章节

### 从文件发布单个章节

```python
from publisher import publish_from_file

# 直接发布
result = publish_from_file(
    work_title="灵契觉醒",
    file_path="/path/to/第36章_标题.md"
)

# 存入草稿箱
result = publish_from_file(
    work_title="灵契觉醒",
    file_path="/path/to/第36章_标题.md",
    mode="draft"
)
```

### 批量发布

```python
from publisher import publish_batch

chapters = [
    {"title": "第38章 遗迹守护者", "content": "正文内容..."},
    {"title": "第39章 暗影的动向", "content": "正文内容..."},
]

# 直接发布
results = publish_batch("灵契觉醒", chapters, interval=5)

# 存入草稿箱
results = publish_batch("灵契觉醒", chapters, interval=5, mode="draft")
```

## 章节文件格式

支持两种模板格式，系统自动检测：

### 模板A - 详细版（带元数据）

适用于需要记录创作规划的场景：

```markdown
# 第36章 标题

> **本章概要**：...
> **本章爽点**：...

---

正文内容...

---

> **章末钩子**：...
```

自动处理：
- 元数据块（开头 `>` 引用）→ **自动去除**
- 章末钩子（结尾 `>` 引用）→ **自动去除**
- 章节号前导零 → 自动去掉（"第05章" → "第5章")

### 模板B - 简洁版（纯正文）

适用于简洁风格的章节文件：

```markdown
# 第一章 重生

正文内容...
```

特点：
- 只有标题和正文
- 无分隔符、无元数据块
- 支持"第一章"、"第1章"等格式

## 发布流程

### 直接发布模式 (publish)

1. 进入创建章节页面
2. 关闭引导弹窗
3. 填写章节号、标题、正文
4. 点击下一步
5. 处理弹窗（错别字检测 → 风险检测 → AI选项 → 确认发布）
6. 等待审核

### 草稿箱模式 (draft)

1. 进入创建章节页面
2. 关闭引导弹窗
3. 填写章节号、标题、正文
4. 点击右上角"存入草稿箱"
5. 确认保存
6. 章节保存到草稿箱

## 注意事项

- 正文至少 1000 字
- Cookie 有效期约 24 小时
- 批量发布建议间隔 5 秒
- 审核约 1 小时完成
- 草稿箱保存的章节可随时编辑发布