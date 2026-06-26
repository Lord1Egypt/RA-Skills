---
name: bozo-wechat-publisher
description: "一键发布 Markdown 文章到微信公众号草稿箱。当用户提到发布到微信、公众号、推文、草稿箱、上传文章时触发。支持 wenyan-cli 完整排版和 curl 备用方案，兼容所有 Node.js 版本。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
      },
  }
---

# bozo-wechat-publisher

**一键发布 Markdown 文章到微信公众号草稿箱**

基于 [wenyan-cli](https://github.com/caol64/wenyan-cli) 封装，提供 curl 备用方案兼容所有环境。

## 核心功能

- 🚀 一键发布到草稿箱
- 🎨 多主题支持（8 种内置 + 2 种自定义卡片主题）
- 💻 代码高亮（9 种主题）
- 🖼️ 图片自动上传到微信图床
- 🔧 三种发布方案（wenyan-cli / 自定义主题 / curl 备用）
- 📚 完整移植文档
- 🎴 **卡片式布局**（支持深色/浅色主题，CSS 样式内联注入）

## 快速开始（3 分钟配置）

### 1. 安装 wenyan-cli

```bash
npm install -g @wenyan-md/cli
```

### 2. 修复 wenyan 命令

**重要：** wenyan-cli 2.x 存在 ESM 模块加载问题，需要创建包装脚本：

```bash
# 创建包装脚本
mkdir -p ~/.local/bin
cat > ~/.local/bin/wenyan << 'EOF'
#!/bin/bash
node /usr/local/lib/node_modules/@wenyan-md/cli/dist/cli.js "$@"
EOF
chmod +x ~/.local/bin/wenyan

# 确保 ~/.local/bin 在 PATH 中
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 验证
wenyan --version
```

### 3. 配置 API 凭证

```bash
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
```

永久配置（添加到 `~/.zshrc`）：
```bash
echo 'export WECHAT_APP_ID=your_app_id' >> ~/.zshrc
echo 'export WECHAT_APP_SECRET=your_app_secret' >> ~/.zshrc
source ~/.zshrc
```

### 4. 添加 IP 到白名单

```bash
curl ifconfig.me
```

登录 https://mp.weixin.qq.com/ → 开发 → 基本配置 → IP 白名单 → 添加此 IP

## 准备 Markdown 文件

文件顶部**必须**包含 frontmatter：

```markdown
---
title: 文章标题（必填）
cover: ./assets/cover.jpg  # 封面图（必填）
description: 公众号摘要。 # 可选
author: 作者名称
source_url: https://example.com  # 可选
---

# 正文开始

你的内容...
```

**⚠️ 必填字段：**
- `title` - 文章标题
- `cover` - 封面图路径或 URL

**封面图推荐：**
- 尺寸：1080×864 像素（5:4）
- 格式：JPG/PNG
- 大小：< 2MB

## 发布文章

### 方案一：wenyan-cli（推荐）

**适用环境：** Node.js 18 及以下

```bash
# 使用默认主题
wenyan publish -f article.md

# 指定主题和代码高亮
wenyan publish -f article.md -t lapis -h solarized-light

# 关闭 Mac 风格代码块
wenyan publish -f article.md -t lapis --no-mac-style

# 列出所有主题
wenyan theme -l
```

**内置主题：**
- `default` - 默认主题
- `lapis` - 青金石（推荐）
- `phycat` - 物理猫
- `orangeheart` - 橙心
- `rainbow` - 彩虹
- `pie` - 派派风格
- `maize` - 玉米色
- `purple` - 紫色

### 方案二：自定义卡片主题（新增）

**适用环境：** 任何 Node.js 版本

使用自定义卡片主题发布，支持深色/浅色风格：

```bash
# 使用 card-tech-dark 深色科技主题（默认）
./scripts/publish-card-theme-v2.sh article.md

# 使用 card-neon-light 霓虹浅色主题
./scripts/publish-card-theme-v2.sh article.md card-neon-light
```

**自定义主题：**
- `card-tech-dark` - 卡片科技暗色 🎴（适合技术文章、AI 内容）
  - 深色背景 (#0a0e27)
  - 紫色渐变强调色 (#6366f1 → #8b5cf6)
  - 卡片式布局 + 悬停动效

- `card-neon-light` - 卡片霓虹浅色 🎴（适合教程、指南、操作手册）
  - 浅色背景 (#f8fafc)
  - 霓虹效果 (#06b6d4 → #8b5cf6)
  - 流畅动画 + 移动端优化

### 方案三：curl 备用方案

**适用环境：** 任何 Node.js 版本

当 wenyan-cli 不可用时，使用备用脚本：

```bash
# 从 skill 目录运行
./scripts/publish-curl.sh article.md

# 或指定环境变量
WECHAT_APP_ID=wx123 WECHAT_APP_SECRET=secret ./scripts/publish-curl.sh article.md
```

**代码高亮：**
- `solarized-light` / `solarized-dark`
- `github` / `github-dark`
- `atom-one-light` / `atom-one-dark`
- `monokai`
- `dracula`
- `xcode`

---

## 重要说明

### 自定义卡片主题工作原理

**样式注入方式：**
- 主题 CSS 样式作为 `<style>` 标签放在内容开头（body 内）
- 不使用 `<head>` 标签，直接发送 body 内容到微信 API
- 确保 CSS 变量（如 `--bg-primary: #0a0e27`）在内容中生效

**wenyan-cli 输出格式：**
- `wenyan render` 输出**不包含** `<html>` 或 `<body>` 标签
- 直接以 `<section id="wenyan">` 开头
- 这是正常的，直接使用完整输出即可

**封面图要求：**
- 草稿箱 API **必须**提供 `thumb_media_id`（即使 `show_cover_pic: 0`）
- 脚本会自动上传封面图并获取 media_id
- 如果没有封面图，会使用默认的 assets/logo.png

### 内容审核限制

**错误 45166 - invalid content hint：**

某些内容可能触发微信的内容审核，导致发布失败：

| 可能原因 | 解决方案 |
|---------|---------|
| 敏感关键词 | 简化内容，避免争议性话题 |
| 过长的文章 | 分段发布或精简内容 |
| 特殊格式 | 使用标准 Markdown 格式 |
| 代码块过多 | 减少代码示例数量 |

**建议：** 先使用简单内容测试，确认发布流程正常后再添加完整内容。

**适用环境：** 任何 Node.js 版本

当 wenyan-cli 不可用时，使用备用脚本：

```bash
# 从 skill 目录运行
./scripts/publish-curl.sh article.md

# 或指定环境变量
WECHAT_APP_ID=wx123 WECHAT_APP_SECRET=secret ./scripts/publish-curl.sh article.md
```

## 完整安装步骤

### macOS

```bash
# 1. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 2. 修复 wenyan 命令
mkdir -p ~/.local/bin
cat > ~/.local/bin/wenyan << 'EOF'
#!/bin/bash
node /usr/local/lib/node_modules/@wenyan-md/cli/dist/cli.js "$@"
EOF
chmod +x ~/.local/bin/wenyan
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# 3. 配置环境变量
echo 'export WECHAT_APP_ID=your_app_id' >> ~/.zshrc
echo 'export WECHAT_APP_SECRET=your_app_secret' >> ~/.zshrc

# 4. 应用配置
source ~/.zshrc
```

### Linux (Ubuntu/Debian)

```bash
# 1. 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 3. 修复 wenyan 命令
mkdir -p ~/.local/bin
cat > ~/.local/bin/wenyan << 'EOF'
#!/bin/bash
node /usr/local/lib/node_modules/@wenyan-md/cli/dist/cli.js "$@"
EOF
chmod +x ~/.local/bin/wenyan
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# 4. 配置环境变量
echo 'export WECHAT_APP_ID=your_app_id' >> ~/.bashrc
echo 'export WECHAT_APP_SECRET=your_app_secret' >> ~/.bashrc

# 5. 应用配置
source ~/.bashrc
```

### Windows

```powershell
# 1. 安装 Node.js 18
# 下载: https://nodejs.org/dist/v18.20.2/node-v18.20.2-x64.msi

# 2. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 3. 创建包装脚本 wenyan.bat
# 保存到 npm 全局目录（运行 npm config get prefix 查看）
@echo off
node "%APPDATA%\npm\node_modules\@wenyan-md\cli\dist\cli.js" %*

# 4. 配置环境变量
# 系统属性 → 环境变量 → 新建用户变量
# WECHAT_APP_ID = your_app_id
# WECHAT_APP_SECRET = your_app_secret
```

## 故障排查

### wenyan 命令无响应

**问题：** 执行 `wenyan --version` 或 `wenyan --help` 时没有任何输出

**原因：** wenyan-cli 2.x 存在 ESM 模块加载问题

**解决方案：** 创建包装脚本（见上文"修复 wenyan 命令"）

### wenyan-cli 报 "fetch failed"

**原因：** Node.js 20/24 与 wenyan-cli 的 fetch 实现不兼容

**解决方案：**
```bash
# 方案 A: 使用 Node.js 18
nvm install 18 && nvm use 18

# 方案 B: 使用 curl 备用方案
./scripts/publish-curl.sh article.md
```

### 自定义主题发布后内容为空白

**问题：** 发布成功但草稿箱中内容为空白

**原因：** 主题 CSS 背景色与文字颜色冲突

**解决方案：**
- card-tech-dark 使用深色背景 (#0a0e27) 和浅色文字 (#f1f5f9)
- 确保微信编辑器没有覆盖样式
- 检查 CSS 变量是否正确注入

### 错误 40007 - invalid media_id

**问题：** 发布时报 "invalid media_id" 错误

**原因：** 未提供 `thumb_media_id` 字段

**解决方案：**
- 确保封面图路径正确
- 检查封面图文件是否存在
- 脚本会自动上传封面图

### 错误 45166 - invalid content hint

**问题：** 内容触发微信审核

**原因：** 文章内容包含敏感词或格式问题

**解决方案：**
- 简化文章内容
- 避免争议性话题
- 使用标准 Markdown 格式
- 减少代码块数量

### IP 不在白名单

**错误信息：** `ip not in whitelist`

**解决方法：**
```bash
# 1. 获取当前 IP
curl ifconfig.me

# 2. 登录公众号后台添加 IP
# https://mp.weixin.qq.com/ → 开发 → 基本配置 → IP 白名单
```

### Frontmatter 缺失

**错误信息：** `title is required in frontmatter`

**解决方法：** 在 Markdown 文件顶部添加：
```markdown
---
title: 你的文章标题
cover: 封面图路径
---
```

### 封面图错误

**错误信息：** `未能找到文章封面`

**解决方法：**
- 确保 frontmatter 中有 `cover` 字段
- 检查图片路径是否正确（支持相对路径和绝对路径）
- 确保图片尺寸符合要求（建议 1080×864）
- 支持的格式：JPG/PNG

### 订阅号 API 限制

**说明：** 订阅号草稿箱 API 与服务号不同

**限制：**
- 不支持某些高级 API（如 freepublish）
- 草稿箱 API 可用但需注意权限配置
- 某些接口需要服务号权限

**解决方案：**
- 使用草稿箱 API (draft/add)
- 发布需要手动在后台操作
- 考虑升级为服务号以获得完整功能

## 移植到新电脑

在新的电脑上使用此 skill：

### 1. 复制 skill 目录

```bash
cp -r /Volumes/AI/AIGC/aigc/Skills/bozo-wechat-publisher ~/.claude/skills/
```

### 2. 安装依赖

```bash
# 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 修复 wenyan 命令
mkdir -p ~/.local/bin
cat > ~/.local/bin/wenyan << 'EOF'
#!/bin/bash
node /usr/local/lib/node_modules/@wenyan-md/cli/dist/cli.js "$@"
EOF
chmod +x ~/.local/bin/wenyan
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 配置环境变量

```bash
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
```

### 4. 添加 IP 到白名单

```bash
curl ifconfig.me
# 登录公众号后台添加此 IP
```

## 发布示例

### 示例 Markdown 文件

```markdown
---
title: 使用 Claude Code 提升开发效率
cover: ./assets/cover.jpg
author: 张三
source_url: https://myblog.com/original-post
---

# 使用 Claude Code 提升开发效率

Claude Code 是一款强大的 AI 编程助手...

## 代码示例

```javascript
function hello() {
    console.log("Hello, WeChat!");
}
```

## 图片示例

![示例图片](./images/example.png)
```

### 发布命令

```bash
# 方案一：wenyan-cli
wenyan publish -f article.md -t lapis -h solarized-light

# 方案二：curl 备用
./scripts/publish-curl.sh article.md
```

## 工作流程

```
准备 Markdown (含 frontmatter)
         │
         ▼
    选择发布方案
         │
    ┌────┴────┐
    │         │
    ▼         ▼
wenyan-cli  curl 脚本
(完整功能)  (备用方案)
    │         │
    └────┬────┘
         ▼
   发布到草稿箱
         │
         ▼
   公众号后台审核发布
```

## 版本历史

### v1.3.0 (2026-04-04)
- ✅ 修复自定义卡片主题发布脚本（publish-card-theme-v2.sh）
- ✅ 修复 wenyan render 输出格式问题（不包含 body 标签）
- ✅ 添加自动封面图上传功能
- ✅ 使用稳定版 access_token API
- ✅ 添加内容审核问题说明
- ✅ 完善故障排查指南

### v1.2.0 (2026-04-04)
- ✅ 修复 wenyan 命令无响应问题
- ✅ 添加自动包装脚本设置
- ✅ 完善安装步骤说明
- ✅ 更新移植指南

### v1.1.0 (2026-04-04)
- ✅ 添加 curl 备用方案
- ✅ 完善 Node.js 版本兼容性说明
- ✅ 添加详细移植指南

### v1.0.0 (2026-02-05)
- ✅ 初始版本
- ✅ 基于 wenyan-cli 封装

## 参考资料

- [wenyan-cli GitHub](https://github.com/caol64/wenyan-cli)
- [微信公众号 API 文档](https://developers.weixin.qq.com/doc/offiaccount/)
- [文颜官网](https://wenyan.yuzhi.tech)

## License

Apache License 2.0
