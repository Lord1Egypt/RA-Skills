# bozo-wechat-publisher

**一键发布 Markdown 到微信公众号草稿箱 🚀**

基于 [wenyan-cli](https://github.com/caol64/wenyan-cli) 封装，提供 curl 备用方案兼容所有环境。

---

## ✨ 功能特性

- 🚀 **一键发布** - Markdown 自动转换并推送到草稿箱
- 🎨 **多主题支持** - lapis、phycat、default 等精美主题
- 💻 **代码高亮** - 9 种代码高亮主题，Mac 风格代码块
- 🖼️ **图片自动处理** - 本地/网络图片自动上传到微信图床
- 🔧 **双方案支持** - wenyan-cli + curl 备用，兼容所有 Node.js 版本
- 📚 **完整文档** - 详细的使用说明、移植指南和故障排查

---

## 📦 快速开始

### 方案选择

| 方案 | 适用环境 | 功能完整度 | 推荐度 |
|------|----------|-----------|--------|
| **wenyan-cli** | Node.js 18 及以下 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **curl 脚本** | 任何环境 | ⭐⭐⭐ | ⭐⭐⭐ |

**推荐策略**: 优先尝试 wenyan-cli，遇到兼容性问题时使用 curl 备用方案。

### 环境检查

```bash
# 检查 Node.js 版本
node --version

# v18.x 或更低 → 使用 wenyan-cli
# v20.x 或 v24.x → 使用 curl 备用方案
```

### 安装步骤

#### macOS / Linux

```bash
# 1. 复制 skill 到你的 Claude skills 目录
cp -r bozo-wechat-publisher ~/.claude/skills/

# 2. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 3. 修复 wenyan 命令（绕过 ESM 模块加载问题）
mkdir -p ~/.local/bin
cat > ~/.local/bin/wenyan << 'EOF'
#!/bin/bash
node /usr/local/lib/node_modules/@wenyan-md/cli/dist/cli.js "$@"
EOF
chmod +x ~/.local/bin/wenyan

# 确保 ~/.local/bin 在 PATH 中
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 4. 配置环境变量
echo 'export WECHAT_APP_ID=your_app_id' >> ~/.zshrc
echo 'export WECHAT_APP_SECRET=your_app_secret' >> ~/.zshrc
source ~/.zshrc

# 5. 添加 IP 到白名单
curl ifconfig.me  # 复制此 IP
# 登录 https://mp.weixin.qq.com/ 添加到白名单
```

#### Windows

```powershell
# 1. 安装 Node.js 18
# 下载: https://nodejs.org/dist/v18.20.2/

# 2. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 3. 配置环境变量
# 系统属性 → 环境变量 → 新建
# WECHAT_APP_ID = your_app_id
# WECHAT_APP_SECRET = your_app_secret
```

---

## 📝 使用方法

### 准备 Markdown 文件

文件顶部**必须**包含 frontmatter：

```markdown
---
title: 文章标题（必填）
cover: ./assets/cover.jpg  # 封面图（必填）
author: 作者名称
source_url: https://example.com/original
---

# 正文开始

你的内容...
```

### 发布命令

**方案一：wenyan-cli**（Node.js 18 及以下）

```bash
# 使用默认主题
wenyan publish -f article.md

# 指定主题和代码高亮
wenyan publish -f article.md -t lapis -h solarized-light

# 关闭 Mac 风格代码块
wenyan publish -f article.md -t lapis --no-mac-style
```

**方案二：curl 备用**（任何 Node.js 版本）

```bash
# 使用备用脚本
./scripts/publish-curl.sh article.md
```

---

## 🎨 主题选项

| 主题 | 风格 | 适合场景 |
|------|------|----------|
| **lapis** | 蓝色优雅 | 技术文章、教程 |
| **phycat** | 绿色清新 | 博客、随笔 |
| **default** | 经典简约 | 通用场景 |

**代码高亮**: solarized-light, monokai, github, atom-one-dark, dracula, xcode

查看完整主题列表：`wenyan theme -l`

---

## 🛠️ 故障排查

### wenyan 命令无响应

**问题**: 执行 `wenyan --version` 或 `wenyan --help` 时没有任何输出

**原因**: wenyan-cli 2.x 存在 ESM 模块加载问题，直接运行 `/usr/local/bin/wenyan` 不会执行任何操作

**解决方案**: 创建包装脚本

```bash
# 创建用户级别的 bin 目录
mkdir -p ~/.local/bin

# 创建 wenyan 包装脚本
cat > ~/.local/bin/wenyan << 'EOF'
#!/bin/bash
node /usr/local/lib/node_modules/@wenyan-md/cli/dist/cli.js "$@"
EOF

chmod +x ~/.local/bin/wenyan

# 确保 ~/.local/bin 在 PATH 中
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 验证修复
wenyan --version
```

**修复后可以直接使用**:
```bash
# 查看版本
wenyan --version

# 发布文章
wenyan publish -f article.md -t lapis -h solarized-light

# 渲染文章
wenyan render -f article.md

# 列出主题
wenyan theme -l
```

### wenyan-cli 报 "fetch failed"

**原因**: Node.js 20/24 兼容性问题

**解决方案**:
```bash
# 方案 A: 使用 Node.js 18
nvm install 18 && nvm use 18

# 方案 B: 使用 curl 备用方案
./scripts/publish-curl.sh article.md
```

### IP 不在白名单

```bash
# 获取当前 IP
curl ifconfig.me

# 登录添加
# https://mp.weixin.qq.com/ → 开发 → 基本配置 → IP 白名单
```

### 封面图错误

**错误**: `未能找到文章封面`

**解决**: 确保 frontmatter 完整：
```markdown
---
title: 标题
cover: 封面图路径
---
```

更多问题查看：[SKILL.md](SKILL.md#故障排查)

---

## 📂 项目结构

```
bozo-wechat-publisher/
├── SKILL.md              # Skill 完整文档
├── README.md             # 本文件
├── MIGRATION.md          # 移植指南 ⭐
├── example.md            # 示例文章
├── assets/
│   └── default-cover.jpg # 默认封面
├── scripts/
│   ├── publish.sh        # wenyan-cli 发布脚本
│   └── publish-curl.sh   # curl 备用脚本 ⭐
└── references/
    └── wechat-api.md     # 微信 API 参考
```

---

## 🚀 移植到新电脑

完整的移植指南请查看：[MIGRATION.md](MIGRATION.md)

**快速步骤**:

1. 复制 skill 目录
2. 安装 Node.js 18 或使用 curl 方案
3. 配置环境变量
4. 添加 IP 到白名单

---

## 🔄 版本历史

### v1.2.0 (2026-04-04)
- ✅ 修复 wenyan 命令无响应问题（ESM 模块加载）
- ✅ 添加 wenyan 包装脚本自动设置
- ✅ 完善安装步骤说明

### v1.1.0 (2026-04-04)
- ✅ 添加 curl 备用方案
- ✅ 完善 Node.js 版本兼容性说明
- ✅ 添加详细移植指南
- ✅ 更新示例文档

### v1.0.0 (2026-02-05)
- ✅ 初始版本
- ✅ 基于 wenyan-cli 封装

---

## 📄 许可证

Apache License 2.0

---

## 🙏 致谢

- [wenyan-cli](https://github.com/caol64/wenyan-cli) - 核心发布工具
- [OpenClaw](https://openclaw.ai) - AI Agent 框架

---

**如果这个 skill 对你有帮助，请给个 ⭐️ Star！**
