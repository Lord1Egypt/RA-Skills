---
name: ClawHub 技能开发模板
slug: clawhub-skill-template
description: ClawHub技能开发标准模板，包含完整的目录结构、SKILL.md模板、package.json模板，一键初始化新技能项目，帮助你快速发布技能到ClawHub。
version: 1.0.0
author: xiatian5
tags: [clawhub, template, skill, development, cli, generator, chinese]
---

# ClawHub 技能开发模板 📦🛠️

ClawHub技能开发标准模板，一键初始化新技能项目，包含完整的目录结构、标准SKILL.md模板、package.json模板，帮助你快速创建并发布技能到ClawHub市场。

## 触发词

当用户说这些话时，调用这个技能：
- "创建新技能模板"
- "ClawHub技能开发"
- "发布技能到ClawHub"
- "初始化技能项目"
- "怎么开发OpenClaw技能"

## 功能特性

- ✅ 标准目录结构一键生成
- ✅ 完整的SKILL.md frontmatter模板
- ✅ 符合规范的package.json配置模板
- ✅ 包含中文注释和开发说明
- ✅ 提供开发 checklist 发布前检查
- ✅ 常见问题解答

## 快速开始

### 1. 创建新技能

```powershell
# 1. 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/your-skill-slug

# 2. 复制模板文件
# 从本技能复制SKILL.md和package.json，替换占位符

# 3. 编辑内容，填写技能信息
# 按照模板提示替换所有占位符

# 4. 发布到ClawHub
clawhub publish ~/.openclaw/workspace/skills/your-skill-slug `
  --slug your-skill-slug `
  --name "Your Skill Name" `
  --version "1.0.0" `
  --changelog "Initial release" `
  --tags "tag1,tag2,tag3"
```

## 标准目录结构

```
your-skill/
├── SKILL.md          # 主要文档，必填
├── package.json      # 元数据，必填
├── README.md         # 额外说明，可选
├── scripts/          # 脚本目录，可选
│   └── main.js
└── assets/           # 资源文件，可选
    └── screenshot.png
```

## SKILL.md 模板

```markdown
---
name: 你的技能名称
slug: your-skill-slug
description: 一句话描述你的技能功能
version: 1.0.0
author: your-name
tags: [tag1, tag2, tag3]
---

# 你的技能名称

这里写详细介绍...

## 触发词

当用户说这些话时，调用这个技能：
- "触发词1"
- "触发词2"
- "触发词3"

## 功能特性

| 功能 | 说明 |
|------|------|
| 功能1 | 功能1说明 |
| 功能2 | 功能2说明 |

## 快速开始

这里写使用步骤...

## 更新日志

### v1.0.0 (YYYY-MM-DD)
- 初始发布

## 相关技能

- [related-skill](https://clawhub.ai/skills/related-skill) - 相关技能描述

---

*如果你觉得这个技能有用，请给它点个星，谢谢！⭐*
```

## package.json 模板

```json
{
  "name": "your-skill-slug",
  "version": "1.0.0",
  "description": "一句话描述你的技能功能",
  "main": "SKILL.md",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "author": "your-name",
  "license": "MIT",
  "dependencies": {},
  "peerDependencies": {
    "dependency-skill": ">=1.0.0"
  }
}
```

## 发布前检查清单

- [ ] slug 是唯一且小写，不含空格
- [ ] name 清晰描述技能功能
- [ ] description 一句话说明，不超过100字
- [ ] tags 包含3-6个相关标签
- [ ] SKILL.md 包含触发词列表
- [ ] 依赖的技能都已经在 peerDependencies 声明
- [ ] 没有包含敏感信息或凭证
- [ ] 已经测试过主要功能可以正常使用

## 命名规范

| 项目 | 规范 | 示例 |
|------|------|------|
| slug | 小写字母，连字符分隔 | `windows-gui-automation-cn` |
| name | 清晰可读，可以含中文 | `Windows GUI 自动化集成 (中文)` |
| tags | 小写关键词，3-6个 | `windows,automation,gui,chinese` |
| description | 一句话，中文推荐20-50字 | 开箱即用的Windows桌面GUI自动化集成技能 |

## 最佳实践

1. **技能要聚焦** - 一个技能做好一件事比什么都做一点好
2. **触发词要自然** - 想想用户会怎么说，包含不同说法
3. **文档要清晰** - 给用户看的文档要简单明了，配有示例
4. **依赖要明确** - 在peerDependencies声明需要的其他技能
5. **版本号遵循语义化** - `主版本.次版本.修订` 格式

## 常见问题

**Q: 我的技能需要收费还是免费？**
A: 新手推荐先发布免费技能积累评价，有了口碑再出付费技能。

**Q: 定价多少合适？**
A: 简单工具技能 ¥19-¥49，完整工作流 ¥59-¥129，大型解决方案 ¥199+。

**Q: 需要写多少字的文档？**
A: SKILL.md 推荐 50-200 行，包含触发词、功能、使用示例足够。

**Q: 更新技能怎么发布？**
A: 改版本号，重新运行 publish 命令即可，平台会自动更新。

## 更新日志

### v1.0.0 (2026-03-30)
- 初始发布
- 完整的ClawHub技能开发模板
- 包含SKILL.md和package.json标准模板
- 开发检查清单和最佳实践指南

## 相关链接

- [ClawHub Official](https://clawhub.ai) - ClawHub技能市场
- [OpenClaw Official Docs](https://docs.openclaw.ai) - OpenClaw官方文档
- [Awesome OpenClaw Skills ZH](https://github.com/clawdbot-ai/awesome-openclaw-skills-zh) - 精选中文技能列表

---

*如果你觉得这个技能有用，请给它点个星，谢谢！⭐*
