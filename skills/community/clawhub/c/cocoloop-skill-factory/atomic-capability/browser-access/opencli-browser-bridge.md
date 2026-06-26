# OpenCLI Browser Bridge 安装指南

## 适用场景

当用户接受安装浏览器扩展，且浏览器自动化任务已经被 `OpenCLI` 支持面覆盖时，使用这份说明。

## 官方基线

- 仓库：`jackwener/OpenCLI`
- npm 包：`@jackwener/opencli`
- 当前核实版本：`1.7.4`

## 安装步骤

### 1. 安装 OpenCLI

```bash
npm install -g @jackwener/opencli@latest
```

安装后先确认版本：

```bash
opencli --version
```

### 2. 下载 Browser Bridge 扩展

1. 打开 OpenCLI 的 GitHub Releases 页面
2. 下载最新的 `opencli-extension-v{version}.zip`
3. 解压到本地目录

### 3. 在 Chrome 或 Chromium 里加载扩展

1. 打开 `chrome://extensions`
2. 开启右上角 `Developer mode`
3. 点击 `Load unpacked`
4. 选择刚刚解压出的扩展目录

### 4. 验证连接

```bash
opencli doctor
```

验收通过时，至少应看到这些状态：

- `Daemon: running`
- `Extension: connected`
- `Connectivity: connected`

## 使用前检查

- Chrome 或 Chromium 已打开
- 目标站点已经在浏览器里登录
- 浏览器里加载的是刚才解压后的扩展目录

## 初次使用建议

先跑这组命令确认支持面和基础连接：

```bash
opencli list
opencli doctor
opencli browser open <url>
opencli browser state
```

如果任务已经有现成命令，优先直接使用：

```bash
opencli <site> <command>
```

## 常见问题

### `doctor` 显示扩展未连接

- 确认扩展已经在 `chrome://extensions` 中启用
- 确认使用的是解压后的目录，而不是 zip 文件
- 确认当前打开的是 Chrome 或 Chromium

### 浏览器已连接但命令拿不到数据

- 确认目标站点已经登录
- 先在浏览器里手动打开目标页面，再重试
- 如果现成命令覆盖不足，改用 `opencli browser` 或适配器流程

### 覆盖不足

- 先尝试 `opencli browser`
- 再尝试 `opencli generate <url>`
- 仍不合适时，回退到 `agent-browser` 或 `playwright-interactive`
