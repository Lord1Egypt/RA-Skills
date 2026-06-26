# 发布指南

## GitHub仓库

### 创建仓库并推送

```bash
# 在GitHub网页创建仓库: https://github.com/new
# 仓库名: apple-notes-writer
# 设置为Public

# 本地推送
cd ~/.openclaw/workspace/skills/apple-notes-writer
git remote add origin https://github.com/YOUR_USERNAME/apple-notes-writer.git
git branch -M main
git push -u origin main
```

### 仓库地址

- **GitHub**: https://github.com/YOUR_USERNAME/apple-notes-writer

---

## ClawHub发布

### 安装ClawHub CLI

```bash
npm i -g clawhub
```

### 登录

```bash
clawhub login
clawhub whoami
```

### 发布技能

```bash
cd ~/.openclaw/workspace/skills/apple-notes-writer
clawhub publish . \
  --slug apple-notes-writer \
  --name "Apple Notes Writer" \
  --version 1.0.0 \
  --changelog "Initial release: HTML format support, Markdown conversion, folder management"
```

### 安装命令

用户安装命令：
```bash
clawhub install apple-notes-writer
```
gitHub仓库已创建，现在发布到ClawHub：

## 小红书笔记要点

### 标题建议
- "OpenClaw技能：完美写入Apple备忘录"
- "3分钟学会自动化Apple备忘录"
- "Mac用户必备：AppleNotes自动化技能"

### 核心卖点
1. **痛点**：手动整理笔记费时费力
2. **解决方案**：OpenClaw技能自动写入
3. **技术亮点**：
   - HTML完美格式
   - Markdown自动转换
   - 特殊字符自动转义
4. **安装简单**：一行命令安装

### 代码示例（小红书展示）
```python
# 安装
clawhub install apple-notes-writer

# 使用
from apple_notes import AppleNotesWriter

writer = AppleNotesWriter()
writer.write(
    title="会议纪要",
    content="<div><h1>标题</h1><p>内容</p></div>",
    folder="工作"
)
```

### 标签建议
#OpenClaw #Apple备忘录 #效率工具 #Mac技巧 #自动化 #Python #技能分享

---

## 版本历史

### v1.0.0 (2024-03-28)
- Initial release
- HTML format support
- Markdown to HTML conversion
- Folder management
- Special character escaping
- CLI interface
