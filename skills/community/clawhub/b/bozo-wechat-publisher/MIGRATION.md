# bozo-wechat-publisher 移植指南

本指南帮助你在新电脑上设置 bozo-wechat-publisher skill。

## 目录

1. [系统要求](#系统要求)
2. [快速安装](#快速安装)
3. [详细配置步骤](#详细配置步骤)
4. [验证安装](#验证安装)
5. [常见问题](#常见问题)

## 系统要求

### 最低要求
- **操作系统**: macOS 10.15+, Ubuntu 18.04+, Windows 10+
- **网络**: 能访问微信公众号 API (api.weixin.qq.com)

### 可选要求
- **Node.js 18.x**: 使用 wenyan-cli 完整功能
- **curl**: 备用方案（macOS/Linux 通常已内置）

## 快速安装

### macOS

```bash
# 1. 复制 skill 目录
cp -r bozo-wechat-publisher ~/.claude/skills/

# 2. 安装 Node.js 18
brew install node@18

# 3. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 4. 配置环境变量
echo 'export WECHAT_APP_ID=your_app_id' >> ~/.zshrc
echo 'export WECHAT_APP_SECRET=your_app_secret' >> ~/.zshrc
source ~/.zshrc

# 5. 添加 IP 到白名单
curl ifconfig.me
# 登录 https://mp.weixin.qq.com/ 添加此 IP
```

### Linux

```bash
# 1. 复制 skill 目录
cp -r bozo-wechat-publisher ~/.claude/skills/

# 2. 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 3. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 4. 配置环境变量
echo 'export WECHAT_APP_ID=your_app_id' >> ~/.bashrc
echo 'export WECHAT_APP_SECRET=your_app_secret' >> ~/.bashrc
source ~/.bashrc

# 5. 添加 IP 到白名单
curl ifconfig.me
# 登录 https://mp.weixin.qq.com/ 添加此 IP
```

### Windows

```powershell
# 1. 复制 skill 目录
# 复制到 C:\Users\<你的用户名>\.claude\skills\

# 2. 安装 Node.js 18
# 下载: https://nodejs.org/dist/v18.20.2/node-v18.20.2-x64.msi

# 3. 安装 wenyan-cli
npm install -g @wenyan-md/cli

# 4. 配置环境变量
# 系统属性 → 环境变量 → 新建用户变量
# WECHAT_API_ID = your_app_id
# WECHAT_API_SECRET = your_app_secret

# 5. 添加 IP 到白名单
# 访问 https://ifconfig.me/ 获取 IP
# 登录 https://mp.weixin.qq.com/ 添加此 IP
```

## 详细配置步骤

### 1. 获取微信公众号凭证

1. 登录 [微信公众号后台](https://mp.weixin.qq.com/)
2. 进入 **开发 → 基本配置**
3. 记录下：
   - **AppID**: 类似 `wx1234567890abcdef`
   - **AppSecret**: 点击"重置"或"查看"获取，类似 `abc123def456ghi789jkl012mno345pq`

### 2. 设置环境变量

#### macOS/Linux

编辑 `~/.zshrc` (macOS) 或 `~/.bashrc` (Linux):

```bash
# 微信公众号配置
export WECHAT_APP_ID=wx1234567890abcdef
export WECHAT_APP_SECRET=abc123def456ghi789jkl012mno345pq
```

保存后执行：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

#### Windows

1. 右键"此电脑" → 属性 → 高级系统设置
2. 环境变量 → 新建用户变量
3. 添加:
   - 变量名: `WECHAT_APP_ID`
   - 变量值: `wx1234567890abcdef`
   - 变量名: `WECHAT_APP_SECRET`
   - 变量值: `abc123def456ghi789jkl012mno345pq`

### 3. 配置 IP 白名单

1. 获取公网 IP:
   ```bash
   curl ifconfig.me
   ```

2. 登录微信公众号后台

3. 开发 → 基本配置 → IP 白名单

4. 点击"配置"，添加你的 IP 地址

5. 保存

### 4. 准备测试文章

创建 `test.md`:

```markdown
---
title: 测试文章
cover: https://via.placeholder.com/1080x864
author: 测试作者
---

# 这是一篇测试文章

测试微信公众号发布功能。

## 代码示例

```javascript
console.log("Hello, WeChat!");
```

## 功能验证

- [x] 标题显示
- [x] 作者信息
- [x] 代码高亮
- [x] 封面图
```

## 验证安装

### 验证 Node.js 和 wenyan-cli

```bash
# 检查 Node.js 版本
node --version  # 应显示 v18.x.x

# 检查 wenyan-cli
wenyan --version  # 应显示版本号

# 测试发布
wenyan publish -f test.md -t lapis -h solarized-light
```

### 验证 curl 备用方案

```bash
# 检查 curl
curl --version

# 测试备用脚本
./scripts/publish-curl.sh test.md
```

### 检查环境变量

```bash
# macOS/Linux
echo $WECHAT_APP_ID
echo $WECHAT_APP_SECRET

# Windows PowerShell
echo $Env:WECHAT_APP_ID
echo $Env:WECHAT_APP_SECRET
```

## 常见问题

### Q1: wenyan-cli 报 "fetch failed"

**原因**: Node.js 版本不兼容（v20 或 v24）

**解决方案**:
```bash
# 方案 A: 降级到 Node.js 18
nvm install 18
nvm use 18
npm install -g @wenyan-md/cli

# 方案 B: 使用 curl 备用方案
./scripts/publish-curl.sh article.md
```

### Q2: "ip not in whitelist" 错误

**解决方案**:
1. 获取当前 IP: `curl ifconfig.me`
2. 登录公众号后台添加到白名单
3. 如果使用 VPN，确保使用 VPN 后的 IP

### Q3: "未能找到文章封面" 错误

**解决方案**: 确保 frontmatter 完整：
```markdown
---
title: 文章标题
cover: 封面图路径或 URL
---
```

### Q4: Windows 上找不到 wenyan 命令

**解决方案**:
1. 重新打开命令行窗口（环境变量需要重启终端生效）
2. 或手动添加 npm 全局路径到系统 PATH:
   - `C:\Users\<用户名>\AppData\Roaming\npm`

### Q5: Linux 上权限错误

**解决方案**:
```bash
# 设置脚本可执行权限
chmod +x scripts/*.sh

# 或使用 bash 直接运行
bash scripts/publish-curl.sh article.md
```

### Q6: GitHub 网络问题

**中国大陆用户**，可能需要配置 npm 镜像：

```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# 然后安装 wenyan-cli
npm install -g @wenyan-md/cli
```

## 文件结构说明

```
bozo-wechat-publisher/
├── SKILL.md           # Skill 主文档
├── README.md          # 本说明文件
├── MIGRATION.md       # 移植指南（本文件）
├── example.md         # 示例 Markdown 文件
├── scripts/
│   ├── publish.sh     # wenyan-cli 发布脚本
│   ├── publish-curl.sh # curl 备用脚本
│   └── setup.sh       # 环境配置脚本
└── references/
    └── wechat-api.md  # 微信 API 参考
```

## 下一步

安装完成后：

1. 阅读 `SKILL.md` 了解完整功能
2. 查看 `example.md` 了解 Markdown 格式要求
3. 尝试发布第一篇文章
4. 登录微信公众号后台查看草稿

## 获取帮助

遇到问题？

1. 查看 `SKILL.md` 的故障排查章节
2. 检查 [wenyan-cli issues](https://github.com/caol64/wenyan-cli/issues)
3. 查看 [微信官方文档](https://developers.weixin.qq.com/doc/offiaccount/)

---

**祝使用愉快！** 📱
