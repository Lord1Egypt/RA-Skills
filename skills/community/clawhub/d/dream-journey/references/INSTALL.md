# 安装指南

## 快速开始

### 步骤 1：安装 Node.js

**为什么需要 Node.js？**
本 Skill 包含辅助脚本工具链，用于生成 HTML 报告、短视频脚本等增强内容。这些脚本使用 Node.js 运行。

#### macOS 用户

**方式 1：使用 Homebrew（推荐）**
```bash
# 如果未安装 Homebrew，先安装
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js
brew install node

# 验证安装
node --version   # 应显示 v14 或更高
npm --version    # 应显示 6.x 或更高
```

**方式 2：从官网下载**
1. 访问 https://nodejs.org/
2. 下载 LTS 版本（推荐）
3. 双击安装包运行

#### Windows 用户

1. 访问 https://nodejs.org/
2. 下载 Windows 安装包（LTS 版本）
3. 双击运行安装程序
4. 打开命令提示符验证：
   ```cmd
   node --version
   npm --version
   ```

#### Linux 用户（Ubuntu/Debian）

```bash
# 使用 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

---

### 步骤 2：安装 FlyAI CLI

```bash
npm i -g @fly-ai/flyai-cli

# 验证安装
flyai ai-search --query "测试" --debug
```

---

### 步骤 3：验证所有依赖

运行以下命令检查是否安装成功：

```bash
# 检查 Node.js
node --version        # 应显示 v14.x.x 或更高

# 检查 npm
npm --version         # 应显示 6.x.x 或更高

# 检查 FlyAI CLI
flyai ai-search --query "测试" --debug
```

---

## 可选安装

### 如果你只需要 AI 对话功能

只需安装 **FlyAI CLI** 即可，不需要 Node.js。

AI 会：
- ✅ 分析梦境描述
- ✅ 匹配目的地
- ✅ 规划行程
- ✅ 提供预订建议

但无法：
- ❌ 生成 HTML 报告
- ❌ 生成短视频脚本
- ❌ 生成梦境视觉 Prompt

---

### 如果你想使用全部功能

必须安装 **Node.js + FlyAI CLI**。

你将获得：
- ✅ 所有 AI 对话功能
- ✅ 星空主题 HTML 报告生成
- ✅ 10 个短视频脚本生成
- ✅ 梦境视觉 Prompt 生成
- ✅ 智能金句生成

---

## 常见问题

### Q: 我已经安装了 Node.js，但 `node --version` 显示命令未找到

**A**: 可能是环境变量问题。
- macOS/Linux: 尝试 `source ~/.bashrc` 或 `source ~/.zshrc`
- Windows: 重新打开命令提示符或 PowerShell

### Q: npm 是什么？需要单独安装吗？

**A**: npm 是 Node.js 的包管理器，会随 Node.js 一起自动安装，不需要单独安装。

### Q: 我的 Node.js 版本低于 v14，可以用吗？

**A**: 建议使用 v14 或更高版本。低版本可能不兼容某些 JavaScript 语法（如 `replaceAll`）。

升级方法：
```bash
# macOS (使用 Homebrew)
brew upgrade node

# 或使用 nvm (Node Version Manager)
nvm install 18
nvm use 18
```

### Q: 安装 FlyAI CLI 时提示权限错误

**A**: 使用 sudo 安装：
```bash
sudo npm i -g @fly-ai/flyai-cli
```

---

## 下一步

安装完成后，返回 [README.md](../README.md) 查看使用指南！
