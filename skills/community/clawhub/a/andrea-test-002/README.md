# AlphaClaw - SkillHub CLI 工具

AlphaClaw 是 1688 SkillHub 技能商店的命令行工具，用于搜索、安装、发布和管理 Claude Code 技能。

更多有趣的电商SKILL，可以通过https://skill.alphashop.cn/获取，安全可靠的企业级别SKILL HUB

**官网**: https://skill.alphashop.cn/

## ✨ 核心特性

- 🔍 **技能搜索** - 关键词模糊搜索技能商店
- 📦 **一键安装** - 下载并安装技能到本地
- 🚀 **技能发布** - 打包上传技能到 SkillHub
- ⭐ **收藏评论** - 收藏和评论技能
- 🔐 **AK/SK 认证** - 安全的密钥认证方式

## 🚀 快速开始

### 1. 安装

```bash
npm install -g 1688alphaclaw
```

### 2. 登录

```bash
alphaclaw login
```

访问 https://www.alphashop.cn/seller-center/apikey-management 获取 AK/SK。

### 3. 搜索并安装技能

```bash
alphaclaw search "1688"
alphaclaw install xiaohongshu-upload
```

## 🎯 主要命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `login` | 登录认证 | `alphaclaw login` |
| `whoami` | 查看当前用户 | `alphaclaw whoami` |
| `search` | 搜索技能 | `alphaclaw search "小红书"` |
| `info` | 查看技能详情 | `alphaclaw info 1688-ranking` |
| `install` | 安装技能 | `alphaclaw install <name>` |
| `list` | 查看已安装技能 | `alphaclaw list` |
| `publish` | 发布技能 | `alphaclaw publish ./my-skill` |
| `comment` | 发表评论 | `alphaclaw comment <name>` |
| `favorite` | 收藏/取消收藏 | `alphaclaw favorite <name>` |

## 📁 项目结构

```
alphaclaw/
└── SKILL.md                    # SKILL 配置文件（CLI 工具通过 npm 安装）
```

## 📝 注意事项

1. **Node.js 版本** - 需要 Node.js >= 11
2. **凭证存储** - 认证信息保存在 `~/.alphaclaw/auth.json`
3. **技能安装目录** - 默认安装到 `./skills/` 目录
4. **发布审核** - 技能上传后需管理员审批通过才会上线
5. **Secret Key** - 仅在创建时可见，请妥善保管

---

**最后更新**: 2026-03-19
