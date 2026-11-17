# 环境准备与安装方式（实测 2026-08）

> 从零构建插件前先确保环境就绪。本文件解决"用什么安装 DSH CLI、去哪儿发现插件、安装安全注意"。
> 代码形态理解见 [plugin-forms.md](../00-understanding/plugin-forms.md)；工程初始化见 [scaffolding.md](scaffolding.md)；部署进入 DSH 见 [deployment-overview.md](../50-ship/deployment-overview.md)。

## 1. 前提条件

**Node.js ≥ 22**（`node -v` 确认）。若版本低于 22，通过 nvm / fnm 或 Node.js 官网升级。

## 2. 三种安装方式

| 维度 | 全局安装 | npx 临时调用 | 项目本地安装 |
|------|---------|-------------|-------------|
| 安装命令 | `npm i -g @deepseek-ai/dsh` | 无需安装 | `npm i @deepseek-ai/dsh` 或 `pnpm add @deepseek-ai/dsh` |
| 使用命令 | `dsh xxx` | `npx @deepseek-ai/dsh xxx` | `pnpm exec dsh xxx` / `npx dsh xxx` |
| 版本管理 | 手动 `npm update -g` | 每次拉取最新 | package.json + lockfile 锁定 |
| 环境隔离 | ❌ 全局共享 | ✅ 无残留 | ✅ 项目级隔离 |
| 团队协作 | ❌ 版本可能不一致 | ⚠️ 版本不锁定 | ✅ lockfile 保证一致 |
| 首次速度 | 快 | 慢（需下载） | 中等 |
| 推荐场景 | 个人长期使用 | 尝鲜 / 一次性任务 | 团队项目 / 生产环境 |

### 方式 A：项目本地安装（推荐，已验证）

```bash
# 1. 安装 dsh CLI 到项目（提供 node_modules/.bin/dsh）
pnpm add @deepseek-ai/dsh

# 2. 添加插件到 web profile（写入 ~/.dsh/profiles/web/package.json）
pnpm exec dsh plugin --profile web add @kiwifruit/dsh-context-pro

# 3. 验证已生效
pnpm exec dsh plugin --profile web list
```

### 方式 B：全局安装

```bash
npm install -g @deepseek-ai/dsh
dsh --version      # 验证成功
# 后续可直接使用 dsh 命令
dsh plugin --profile web add <package>
```

若遇 EACCES 权限错误，推荐配置 npm 全局目录到用户空间：

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc   # 或 ~/.zshrc
source ~/.bashrc
npm install -g @deepseek-ai/dsh
```

### 方式 C：npx 临时调用（零安装，推荐尝鲜）

```bash
# 启动 Web UI
npx -y @deepseek-ai/dsh web

# 安装插件
npx @deepseek-ai/dsh plugin --profile web add <package>

# 卸载插件
npx @deepseek-ai/dsh plugin --profile web remove <package>
```

`-y` 自动确认下载，首次稍慢，后续使用 npx 缓存。

## 3. 安装后验证

```bash
pnpm exec dsh plugin --profile web list
```

能正常列出已安装包即表示 DSH CLI 可用。

## 4. 插件社区（去哪儿找插件）

| 入口 | 说明 |
|------|------|
| **GitHub `dsh-plugin` 话题标签** | 开发者给插件仓库打上 `dsh-plugin` 话题标签即可被社区检索，目前 700+ 公开仓库 |
| **awesome-dsh-plugin 精选目录** | 社区维护的精选列表，收录标准：声明 `dsh.bundle`、能正常安装、描述与实际一致、仍在维护 |
| **dsh-find-plugin** | 插件搜索工具：`dsh plugin --profile web add dsh-find-plugin` |
| **dsh-market（内置）** | DSH 设置页内置的插件市场，可按分类浏览/搜索/一键安装 |
| **Plugin Store（内置）** | 官方已内置 100+ 插件 |

## 5. 安全提醒

插件安装后以**你的用户权限**在你的机器上运行——可读写文件、使用凭据、访问网络。DSH 的工具审批不会为插件代码加沙箱。"已验证"仅代表核验到 manifest 清单，不构成安全审查。建议安装前先用 `dsh-plugin-check` 等工具做检查。