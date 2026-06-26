---
name: openclaw-updater
description: 飞牛 OpenClaw 更新助手。触发词：「更新openclaw」「升级openclaw」。功能：检测当前运行的 openclaw 版本 → 查找最新稳定版本 → 在 managed-install 目录内执行 npm install 覆盖更新 → 自动重启网关生效。
---

# 飞牛 OpenClaw 更新助手

## 关键原则

OpenClaw 安装在 **managed-install** 目录，即 `$OPENCLAW_DATA_DIR/openclaw`（飞牛系统标准路径，普通用户无权限写 `/vol1/@appcenter/` 系统层）。

> 路径公式：`{OPENCLAW_DATA_DIR}/openclaw`
> 每个飞牛系统的 `OPENCLAW_DATA_DIR` 不同，但 managed-install 结构一致。
> 不要硬编码 `/vol1/@apphome/...` 路径，动态获取更安全。  
**不要** 用 `npm i -g openclaw`（会报 EACCES 权限错误），也**不要**用 `openclaw update`（同样是全局安装路径）。

## 正确更新方式

在 managed-install 目录内直接 `npm install`：

```bash
# 1. 查询当前运行版本
openclaw --version

# 2. 查询最新版本
npm view openclaw version

# 3. 在 managed-install 目录内更新（会覆盖旧版本，自动生效）
cd "$OPENCLAW_DATA_DIR/openclaw" && npm install openclaw@<最新版本>

# 4. 等待几秒让进程重新加载
```

## 更新流程（按顺序执行）

### Step 1：确认当前版本和最新版本

```bash
openclaw --version
npm view openclaw version
```

比较两者：
- 如果 `openclaw --version` >= `npm view openclaw version`，已是最新的，无需操作
- 否则继续 Step 2

### Step 2：在 managed-install 目录内安装

```bash
cd "$OPENCLAW_DATA_DIR/openclaw" && npm install openclaw@<最新版本>
```

等待 npm 完成（通常 1-2 分钟）。

### Step 3：验证更新成功

```bash
openclaw --version
```

确认输出为新版本号。网关会自动在新版本下运行。

## 注意事项

- **不要**使用 `sudo`、`npm i -g`、`openclaw update`——这些都会失败
- 更新是覆盖安装，无需卸载
- 网关进程会自动在新版本下运行，无需手动重启（除非有异常）
- 遇到 EBADENGINE 警告（undici / node 版本提示）可以忽略，不影响更新

## 常见问题

| 症状 | 原因 | 解决 |
|------|------|------|
| `EACCES permission denied` | 用了全局安装 | 改用 managed-install 目录内 `npm install` |
| 更新后版本没变 | 进程缓存了旧路径 | 等几秒再查，或确认 openclaw 路径指向正确目录 |
| npm 下载慢 | 网络问题 | 可以给 npm 设置镜像：`npm config set registry https://registry.npmmirror.com` |