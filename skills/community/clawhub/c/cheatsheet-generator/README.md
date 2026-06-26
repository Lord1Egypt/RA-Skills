# 速查表生成器 📋

> 生成结构化 Markdown 速查表，沉淀实战经验，支持导出分享

---

## ✨ 功能特性

- 📋 **结构化输出** - 检查清单 + 核心命令 + 常见问题 + 实战经验
- 🎯 **模板驱动** - 内置高质量模板，持续扩展
- 💾 **支持导出** - 保存为 Markdown 文件，方便查阅
- 🔧 **可扩展** - 轻松添加新模板
- 🌍 **全领域支持** - 不仅支持技术类，还支持生活/健康/学习/工作/美食等任何领域！

---

## 🚀 快速开始

### 使用技能（推荐）

在 OpenClaw 中直接说：

```
# 技术类
生成 npm 发布速查表
Git 速查表
OpenClaw 技能开发指南

# 非技术类 ✨
生成咖啡冲泡速查表
生成健身深蹲速查表
生成英语时态速查表
生成会议组织速查表
生成红烧肉速查表
```

### 命令行使用

```bash
cd ~/.openclaw/skills/cheatsheet-generator

# 生成速查表
node index.js "npm 发布"

# 列出所有模板
node index.js --list

# 搜索模板
node index.js --search npm

# 保存为文件
node index.js "npm 发布" > ~/Documents/cheatsheets/npm-速查表.md
```

---

## 📋 内置模板

| 模板 | 触发词 | 说明 |
|------|--------|------|
| npm 发布 | `npm 速查表`、`npm 发布` | npm 包发布完整指南 |
| OpenClaw 技能开发 | `技能开发速查表`、`OpenClaw 技能` | OpenClaw 技能开发指南 |
| Git 常用命令 | `Git 速查表`、`Git 命令` | Git 高频命令速查 |

---

## 📁 文件结构

```
cheatsheet-generator/
├── SKILL.md              # OpenClaw 技能说明
├── skill.json            # 技能触发配置
├── package.json          # npm 包信息
├── README.md             # 本文档
├── index.js              # 主入口
├── renderer.js           # Markdown 渲染器
└── templates/
    └── index.js          # 模板库
```

---

## 🔧 添加新模板

### 步骤 1：编辑 templates/index.js

```javascript
'your-topic': {
  id: 'your-topic',
  title: '你的速查表标题',
  keywords: ['关键词 1', '关键词 2'],
  sections: [
    {
      name: '📋 前置准备',
      type: 'checklist',
      items: ['检查项 1', '检查项 2']
    }
  ]
}
```

### 步骤 2：测试模板

```bash
node index.js "你的主题"
```

### 步骤 3：提交模板

欢迎贡献模板到 ClawHub 技能市场！

---

## 💡 使用技巧

### 导出为 PDF

```bash
# 1. 生成 Markdown
node index.js "npm 发布" > npm.md

# 2. 转换为 PDF（需要 pandoc）
pandoc npm.md -o npm.pdf
```

### 添加到笔记软件

- **Obsidian**: 保存到笔记目录，自动同步
- **Notion**: 复制 Markdown，粘贴为代码块
- **语雀**: 导入 Markdown 文件

### 团队分享

- 保存到团队共享目录
- 发送到群聊
- 发布到内部 Wiki

---

## 🎯 最佳实践

1. **定期更新** - 发现新坑 → 更新到速查表
2. **实战验证** - 所有命令都要实际测试过
3. **简洁明了** - 不要冗长，只保留关键信息
4. **持续积累** - 每次遇到问题都记录下来

---

## 📝 更新日志

### v1.0.0 (2026-03-23)
- ✅ 初始版本发布
- ✅ 内置 3 个模板（npm/Git/OpenClaw 技能）
- ✅ 支持 Markdown 导出
- ✅ OpenClaw 技能集成

---

## 🤝 贡献

欢迎提交新模板或改进建议！

---

*版本：v1.0.0 | 作者：万万粥 <wanwan_app@163.com> | 协议：MIT-0*
