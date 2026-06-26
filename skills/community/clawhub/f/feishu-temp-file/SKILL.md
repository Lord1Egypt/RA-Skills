---
name: feishu-file-sender
description: 飞书文件发送助手 - 通过临时目录解决OpenClaw飞书发送文件路径白名单问题 | Feishu File Sender - Solve OpenClaw Feishu file path whitelist issue
metadata:
  author: 寇助理
  openclaw:
    emoji: 📎
    category: tools
    tags: [feishu, file, upload, image, openclaw]
    requires:
      paths: [/home/admin/.openclaw/media, /tmp]
---

# 飞书文件发送助手 | Feishu File Sender

> 解决 OpenClaw 飞书发送文件时的路径白名单问题！
> Solve OpenClaw Feishu file path whitelist issue!

## 📋 问题说明 | Problem

OpenClaw 发送飞书图片/文件时，飞书插件读取本地文件经过核心的路径白名单检查，导致只能发送白名单路径内的文件。

When sending Feishu images/files via OpenClaw, the Feishu plugin reads local files through OpenClaw's path whitelist check, which only allows files in whitelisted paths.

## 💡 解决方案 | Solution

1. 配置技能读取权限 - 自动适配多系统
2. 在临时目录下创建文件夹，发送前复制文件到临时目录
3. 发送成功后删除临时文件

## 🚀 快速开始 | Quick Start

### 第一步：配置权限（必做）

```bash
cd skills/feishu-temp-file

# 显示权限选项
node scripts/perm-config.js

# 选择并应用配置 (1/2/3)
node scripts/perm-config.js 2
```

**权限选项说明：**

| 选项 | 名称 | 路径范围 |
|------|------|---------|
| 1 | 限制级 | /home/admin, /tmp, /home |
| 2 | 中等 | /home, /tmp, /opt, /var, /srv |
| 3 | 宽松 | /** (整个系统) |

### 第二步：检查目录权限

```bash
# 检查临时目录权限状态
node scripts/check-perm.js
```

### 第三步：使用技能

```bash
# 复制文件到临时目录
node scripts/prepare.js /path/to/your/file.png

# 发送成功后清理
node scripts/clean.js
```

## 📜 所有脚本 | All Scripts

| 脚本 | 功能 |
|------|------|
| `perm-config.js` | 配置技能读取权限 (首次必做) ✅ |
| `check-perm.js` | 检查临时目录权限状态 |
| `prepare.js` | 复制文件到临时目录 |
| `list.js` | 列出临时文件 |
| `clean.js` | 清理临时文件 |
| `detect-system.js` | 检测系统类型 |

## 📁 项目结构 | Project Structure

```
feishu-temp-file/
├── SKILL.md              
├── _meta.json            
├── package.json          
├── config.example.json   
└── scripts/
    ├── shared.js         
    ├── perm-config.js    # 配置权限 ✅ (新增)
    ├── check-perm.js     
    ├── prepare.js        
    ├── list.js           
    └── clean.js           
```

## ⚠️ 注意事项 | Notes

1. **首次使用必须先运行 `perm-config.js`** - 配置技能读取权限
2. 选择权限级别后会自动写入 `~/.openclaw/openclaw.json`
3. 发送成功后记得清理临时文件

## 🔗 相关链接 | Links

- [OpenClaw 文档](https://docs.openclaw.ai)
- [飞书开发文档](https://open.feishu.cn/)

---

**提示**: 建议选择"中等"权限，既方便使用又相对安全！
**Tip**: Recommend option 2 (Medium) for balance between convenience and security!
