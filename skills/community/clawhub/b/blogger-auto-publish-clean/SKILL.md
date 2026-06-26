---
name: blogger-auto-publish
description: Automatically publish Markdown articles to Google Blogger. Supports batch publishing, draft management, and automatic HTML conversion.
---

# Blogger Auto-Publish Skill

**版本**: 1.1.0  
**发布日期**: 2026-03-28  
**更新日期**: 2026-03-28 (Live Implementation)  
**兼容性**: OpenClaw >= 2026.3.0  
**状态**: 生产就绪 ✅

## ⚠️ 重要前提条件

**使用此技能前，你必须准备好以下文件**：

### 1. Google API凭据 (`credentials.json`)
- 从Google Cloud Console创建项目
- 启用Blogger API v3
- 创建OAuth 2.0凭据（Web应用类型）
- 下载`credentials.json`文件

### 2. 博客ID
- 登录你的Blogger账户
- 找到要发布的博客
- 获取博客的数字ID（查看博客URL中的数字部分）

### 3. 首次授权
- 运行授权脚本生成`token.json`
- 完成浏览器OAuth流程

## 🎯 技能描述

自动将Markdown文章发布到Google Blogger博客。支持：
- 批量发布文章
- 定时发布
- 草稿管理
- 英文内容验证
- Markdown到HTML转换

## 📋 功能特性

### 核心功能
- ✅ 自动发布Markdown文章到Blogger
- ✅ 支持草稿和已发布状态
- ✅ 批量处理多个文章
- ✅ 自动HTML转换

### 管理功能
- ✅ 列出所有博客文章
- ✅ 删除测试文章
- ✅ 管理草稿
- ✅ 查找博客ID

### 工具功能
- ✅ 完整的授权流程
- ✅ 配置管理
- ✅ 错误处理和日志
- ✅ 环境变量支持

## 🚀 快速开始

### 步骤1：安装依赖
```bash
npm install googleapis@latest
```

### 步骤2：配置项目
1. 复制`credentials.json`到项目根目录
2. 设置博客ID（环境变量或config.js）
3. 运行首次授权

### 步骤3：使用示例
```bash
# 列出所有博客
node list_blogs.js

# 发布文章
node publish.js --file posts/my-article.md

# 管理草稿
node delete-all-drafts.js
```

## 📁 项目结构

```
blogger-auto-publish/
├── auth.js                 # 授权模块
├── blogger.js              # 主发布模块
├── config.js              # 配置文件
├── credentials.json       # Google API凭据（用户提供）
├── token.json            # 授权token（自动生成）
├── list_blogs.js         # 列出博客
├── publish.js            # 发布文章
├── delete-all-drafts.js  # 删除所有草稿
├── delete-test-posts.js  # 删除测试文章
├── direct-delete-drafts.js # 直接删除草稿
├── find-blog-id.js       # 查找博客ID
├── complete-auth.js      # 完整授权流程
├── index.js              # 主入口文件
├── package.json          # 项目配置
├── posts/                # 文章目录
│   └── example-post.md  # 示例文章
└── scripts/             # 工具脚本
    └── setup-blogger.sh # 安装脚本
```

## 🔧 详细使用指南

### 1. 获取Google API凭据
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用Blogger API v3
4. 创建OAuth 2.0凭据（Web应用）
5. 设置重定向URI：`http://localhost:3000/oauth2callback`
6. 下载`credentials.json`

### 2. 获取博客ID
1. 登录 [Blogger](https://www.blogger.com/)
2. 进入博客设置
3. 查看URL中的数字ID，或使用`find-blog-id.js`脚本

### 3. 首次授权
```bash
# 设置环境变量
export BLOG_ID="你的博客ID"

# 运行授权
node auth.js login
# 或使用完整授权脚本
node complete-auth.js
```

### 4. 发布文章
```bash
# 发布单篇文章
node publish.js --file posts/my-article.md --title "文章标题"

# 发布为草稿
node publish.js --file posts/draft.md --draft

# 批量发布
for file in posts/*.md; do
  node publish.js --file "$file"
done
```

## 📝 文章格式要求

### Markdown文件结构
```markdown
---
title: 文章标题
labels: 标签1,标签2,标签3
draft: false
---

# 文章内容

这里是文章的Markdown内容...

- 支持标准Markdown语法
- 支持代码块
- 支持图片链接
```

### 元数据字段
- `title`: 文章标题（必需）
- `labels`: 标签，逗号分隔（可选）
- `draft`: 是否作为草稿发布，true/false（可选，默认false）

## ⚙️ 配置选项

### 环境变量
```bash
export BLOG_ID="YOUR_BLOG_ID_HERE"
export CREDENTIALS_PATH="./credentials.json"
export TOKEN_PATH="./token.json"
export POSTS_DIR="./posts"
```

### config.js 配置
```javascript
module.exports = {
  blogId: process.env.BLOG_ID || "YOUR_BLOG_ID_HERE",
  credentialsPath: process.env.CREDENTIALS_PATH || "./credentials.json",
  tokenPath: process.env.TOKEN_PATH || "./token.json",
  postsDir: process.env.POSTS_DIR || "./posts",
  maxRetries: 3,
  retryDelay: 1000,
};
```

## 🔍 故障排除

### 常见问题

1. **授权失败**
   - 检查`credentials.json`文件是否正确
   - 确保重定向URI配置正确
   - 删除旧的`token.json`重新授权

2. **博客ID错误**
   - 使用`find-blog-id.js`查找正确ID
   - 确保有博客的编辑权限

3. **发布失败**
   - 检查网络连接
   - 验证API配额是否充足
   - 查看错误日志详细信息

### 错误代码
- `401`: 授权无效，重新运行授权
- `403`: 权限不足，检查博客权限
- `404`: 博客ID错误，验证博客ID
- `429`: API配额超限，等待后重试

## 📊 性能优化

### 批量处理建议
- 一次处理不超过10篇文章
- 添加延迟避免API限制
- 使用草稿模式先验证

### 资源管理
- 定期清理旧的`token.json`
- 备份`credentials.json`
- 使用环境变量管理敏感信息

## 🔄 更新日志

### v1.0.0 (2026-03-28)
- 初始稳定版本
- 完整的发布功能
- 详细的文档
- 打包为OpenClaw技能

## 📞 支持与反馈

如有问题或建议：
1. 查看`references/`目录中的详细文档
2. 运行`node index.js --help`查看帮助
3. 检查错误日志获取详细信息

## 🎯 技能触发条件

当OpenClaw检测到以下需求时自动触发：
- 自动发布文章到Blogger
- 批量或定时发布
- Blogger API集成需求
- Markdown到Blogger转换

## 🚀 实际应用案例

此技能已经过完整测试和验证：

### ✅ 已验证功能
- **博客连接**: 成功连接到Google Blogger平台
- **OAuth授权**: 完整的Google OAuth 2.0流程已实现
- **文章发布**: Markdown文章可成功发布为草稿或正式文章
- **API集成**: Blogger API v3 完全集成

### 🔧 配置要求
- **凭据文件**: 用户需要提供自己的`credentials.json`
- **授权令牌**: 首次运行时会自动生成`token.json`
- **博客ID**: 用户需要提供自己的Blogger博客ID
- **依赖包**: 需要安装`googleapis@latest`

### 📝 测试流程
1. ✅ **API连接测试**: 验证与Google API的连接
2. ✅ **博客列表测试**: 检索用户博客信息
3. ✅ **发布测试**: 示例文章发布测试
4. ✅ **授权测试**: OAuth授权流程测试

### 🛠️ 包含的文件
- `auth.js` - OAuth授权模块
- `publish.js` - 发布主模块  
- `config.js` - 配置文件
- `package.json` - 项目配置
- `README.md` - 使用说明
- `posts/example-post.md` - 示例文章
- `SETUP.md` - 详细设置指南
- `credentials-example.json` - 凭据模板文件

---

**重要**: 此技能不包含任何敏感凭据文件。用户需要按照SETUP.md指南自行配置Google API凭据和博客ID。