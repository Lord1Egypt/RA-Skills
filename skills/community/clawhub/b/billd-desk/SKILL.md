---
name: billd-desk
version: 1.0.0
description: BilldDesk远程桌面控制工具 - WebRTC技术，支持2K+60fps，自定义设备码，隐私屏，虚拟屏，屏幕墙，批量群控。免费无限制，配合Tailscale更安全。
keywords: [billd-desk,remote-desktop,remote-control,webrtc,tailscale,远程桌面]
---

# BilldDesk 远程桌面

**官网：** https://desk.hsslive.cn  
**GitHub：** https://github.com/galaxy-s10/billd-desk  
**下载：** https://desk.hsslive.cn/#/download  
**快速体验：** https://desk.hsslive.cn

---

## 核心优势 vs ToDesk

| 功能 | BilldDesk | ToDesk |
|------|-----------|--------|
| 连接限制 | ✅ 无限制免费 | ⚠️ 80h/月 |
| 画质 | ✅ 2K+60fps免费 | ⚠️ 1080p限制 |
| 帧率 | ✅ 无限制 | ⚠️ 30帧 |
| 安卓被控 | ✅ 免费 | ❌ ¥24/月 |
| 自定义设备码 | ✅ 免费 | ❌ 不支持 |
| 隐私屏 | ✅ 免费 | ❌ ¥24/月 |
| 虚拟屏 | ✅ 免费 | ❌ ¥95/月 |
| 屏幕墙 | ✅ 免费 | ❌ ¥218/月 |
| 批量群控 | ✅ 支持 | ❌ 不支持 |
| Web控制 | ✅ 免费 | ❌ ¥24/月 |
| 私有化部署 | ✅ 免费开源 | ❌ 企业版 |

---

## 支持平台

| 平台 | 状态 | 说明 |
|------|------|------|
| Windows 10/11 | ✅ 完全支持 | 推荐 |
| Windows Server | ✅ 支持 | |
| macOS 15+ | ✅ 支持 | |
| Android 8-15 | ✅ 支持 | 被控/主控 |
| Web浏览器 | ✅ 支持 | Chrome/Edge/Firefox/Safari |
| Linux/WASM | ❌ 不支持 | |

---

## 功能列表

### 基础功能
- ✅ 2K+60fps 高画质
- ✅ 自定义设备码/密码
- ✅ 剪贴板同步
- ✅ 分辨率同步
- ✅ 文件传输
- ✅ 开机自启（无人值守）
- ✅ 进程保活
- ✅ 在线更新
- ✅ 系统托盘

### 高级功能
- ✅ 隐私屏（图片/文字）
- ✅ 虚拟屏
- ✅ 扩展屏
- ✅ 屏幕墙（单控/群控）
- ✅ 多屏操作
- ✅ 多设备同时控制
- ✅ 批量群控
- ✅ 快捷键支持

### 技术特性
- ✅ WebRTC P2P
- ✅ H264/H265/VP8/VP9/AV1
- ✅ NVIDIA/AMD 硬件加速
- ✅ 自定义中继服务器
- ✅ 私有化部署
- ✅ Docker一键部署

---

## 快速开始

### 1. 下载客户端

访问：https://desk.hsslive.cn/#/download

下载对应平台的客户端

### 2. 注册账号

免费注册，开始使用

### 3. 添加设备

在要控制的电脑上安装并登录

### 4. 开始控制

在控制端选择设备，开始远程

---

## 配合 Tailscale 使用（推荐）

**最佳安全方案：**
```
Tailscale组网 + BilldDesk远程控制
```

### 步骤：

1. **安装 Tailscale**
```bash
# Linux
curl -fsSL https://tailscale.com/install.sh | sh

# Windows: https://tailscale.com/download
# macOS: App Store
# Android: Play Store
```

2. **加入网络**
```bash
tailscale up
# 浏览器授权
```

3. **获取Tailscale IP**
```bash
tailscale status
# 显示所有设备的 100.x.x.x IP
```

4. **BilldDesk使用Tailscale IP连接**

在BilldDesk中：
- 输入对方设备码
- 或使用Tailscale IP直接连接

**优势：**
- ✅ 公网IP完全隐藏
- ✅ WireGuard加密
- ✅ 无需端口映射
- ✅ P2P直连低延迟

---

## 私有化部署

### Docker一键部署

```bash
# 部署中继服务器
docker run -d \
  --name billd-desk \
  -p 3000:3000 \
  -p 8000:8000 \
  billd-desk-server:latest
```

### 自定义配置

```bash
# 设置中继服务器地址
# 在BilldDesk设置中填入你的服务器地址
```

---

## 远程控制技巧

### 快捷键

| 操作 | 快捷键 |
|------|--------|
| Ctrl+Alt+Del | 锁定/注销 |
| 显示桌面 | 快速返回 |
| 打开设置 | 远程配置 |
| 任务视图 | 多任务切换 |
| 任务管理器 | 系统监控 |
| 资源管理器 | 文件管理 |

### 画质优化

在设置中调整：
- 码率：越高越清晰
- 帧率：越高越流畅
- 编码：H265更省带宽

---

## 适用场景

| 场景 | 推荐功能 |
|------|---------|
| 居家办公 | Tailscale + BilldDesk |
| 远程服务器 | 开机自启 + 隐私屏 |
| 多设备管理 | 屏幕墙 + 批量群控 |
| 游戏串流 | 2K+60fps + 硬件编码 |
| IT运维 | 私有化部署 + 自定义中继 |

---

## 开源版本 vs Pro版

| 版本 | 开源版 | Pro版 |
|------|--------|-------|
| 源码 | ✅ 完全开源 | ❌ 闭源 |
| 价格 | 免费 | 订阅制 |
| 隐私屏 | ❌ 无 | ✅ 有 |
| 虚拟屏 | ❌ 无 | ✅ 有 |
| 屏幕墙 | ❌ 无 | ✅ 有 |
| 高码率 | ❌ 限制 | ✅ 无限制 |

**开源版地址：** https://github.com/galaxy-s10/billd-desk

---

## 安全建议

1. **配合Tailscale**：隐藏公网IP
2. **设置强密码**：防止未授权访问
3. **私有化部署**：数据不经过第三方
4. **隐私屏**：远程时保护隐私
5. **定期更新**：修复安全漏洞

---

*WebRTC远程桌面 | 免费无限制*
