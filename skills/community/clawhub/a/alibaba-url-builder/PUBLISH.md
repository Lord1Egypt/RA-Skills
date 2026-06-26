# ClawHub 发布指南

本指南帮助你发布 `alibaba-sourcing` skill 到 ClawHub。

## 前置要求

1. **Node.js / npm** - 用于安装 ClawHub CLI
2. **GitHub 账号** - 用于 ClawHub 登录
3. **Git** - 用于创建 GitHub 仓库

## 步骤 1: 安装 ClawHub CLI

```bash
# 使用 npm 安装
npm install -g clawdhub

# 或使用 npx 直接运行
npx clawdhub@latest --version
```

## 步骤 2: 登录 ClawHub

```bash
# 浏览器登录（推荐）
clawdhub login

# 或手动提供 token
clawdhub login --token clh_xxx
```

登录流程：
1. 运行 `clawdhub login` 后会自动打开浏览器
2. 使用 GitHub 账号授权
3. 授权完成后自动返回 CLI

## 步骤 3: 验证登录

```bash
clawdhub whoami
```

应该显示你的 GitHub 用户名。

## 步骤 4: 发布 Skill

### 方式 A: 直接发布（推荐）

```bash
cd /Users/zhouzeyu/.openclaw/workspace-code/alibaba-sourcing

# 发布到 ClawHub
clawdhub publish . --version 1.0.0 --tags latest --changelog "Initial release: Alibaba.com URL builder with traffic tracking"
```

### 方式 B: 使用 sync 命令

```bash
# 同步当前目录下的所有 skills
clawdhub sync --root /Users/zhouzeyu/.openclaw/workspace-code/alibaba-sourcing --all
```

## 步骤 5: 验证发布

```bash
# 搜索你的 skill
clawdhub search alibaba-sourcing

# 查看 skill 详情
clawdhub inspect alibaba-sourcing

# 在浏览器中查看
open https://clawhub.ai/skills/alibaba-sourcing
```

## 步骤 6: 创建 GitHub 仓库（可选但推荐）

```bash
cd /Users/zhouzeyu/.openclaw/workspace-code/alibaba-sourcing

# 初始化 Git
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "Initial release: alibaba-sourcing skill for OpenClaw"

# 创建 GitHub 仓库（替换为你的仓库名）
git remote add origin https://github.com/zhouzeyu/openclaw-skill-alibaba-sourcing.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 更新 Skill

当你需要更新 skill 时：

```bash
# 1. 更新 SKILL.md 中的 version
# 2. 更新代码和文档
# 3. 发布新版本

clawdhub publish . --version 1.1.0 --tags latest --changelog "Added new URL patterns for X"

# 或自动版本号
clawdhub publish . --bump minor --tags latest
```

## 常见问题

### Q: 发布失败，提示认证错误
A: 运行 `clawdhub login` 重新登录，或检查 token 是否过期。

### Q: 提示 skill 已存在
A: 使用新版本号发布，ClawHub 支持版本管理。

### Q: 如何删除已发布的 skill
A: 使用 `clawdhub delete alibaba-sourcing --yes`（软删除，可恢复）

### Q: 如何查看发布历史
A: 访问 https://clawhub.ai/skills/alibaba-sourcing 或运行 `clawdhub inspect alibaba-sourcing --versions`

## 宣传技巧

发布后，在以下渠道分享你的 skill：

1. **OpenClaw Discord** - https://discord.com/invite/clawd
   - 在 #skills 频道分享
   - 附上 ClawHub 链接和简短介绍

2. **GitHub** - 创建仓库并添加话题标签
   - `openclaw`
   - `openclaw-skill`
   - `alibaba`
   - `ecommerce`

3. **社交媒体**
   - Twitter/X: 带上 #OpenClaw #AI #Agent 标签
   - LinkedIn: 分享技术细节

4. **ClawHub 社区**
   - 在技能页面添加详细文档
   - 响应评论和反馈

## 示例宣传文案

```
🚀 新 Skill 发布：alibaba-sourcing

为 OpenClaw agent 打造的 Alibaba.com URL 构建工具！

✨ 特性：
- 10+ URL 模式（搜索、商品详情、供应商等）
- 自动流量追踪 (traffic_type=ags_llm)
- Python CLI 辅助脚本
- 完整文档和示例

🔗 https://clawhub.ai/skills/alibaba-sourcing
📦 clawdhub install alibaba-sourcing

#OpenClaw #AI #Agent #Alibaba #Ecommerce
```

## 资源链接

- ClawHub 官网：https://clawhub.ai
- ClawHub CLI 文档：https://github.com/openclaw/clawhub/blob/main/docs/cli.md
- OpenClaw 文档：https://docs.openclaw.ai
- 社区 Discord：https://discord.com/invite/clawd
