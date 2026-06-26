# 安装指南

## 适用场景

- 在 Linux 或 macOS 上安装 Lightpanda 二进制
- 使用 Docker 快速部署
- 在 Windows 上通过 WSL2 使用

---

## Linux 安装（x86_64）

> **AI 可自动执行**

```bash
# 下载 nightly 版本
curl -L -o lightpanda \
  https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux

# 添加执行权限
chmod a+x ./lightpanda

# 验证安装
./lightpanda version
```

### Linux aarch64

```bash
curl -L -o lightpanda \
  https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-linux
chmod a+x ./lightpanda
```

---

## macOS 安装

### Apple Silicon (aarch64)

```bash
curl -L -o lightpanda \
  https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos
chmod a+x ./lightpanda
./lightpanda version
```

### Intel Mac (x86_64)

```bash
curl -L -o lightpanda \
  https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-macos
chmod a+x ./lightpanda
```

---

## Docker 安装（推荐生产环境）

```bash
# 启动容器（在 9222 端口暴露 CDP 服务器）
docker run -d --name lightpanda \
  -p 127.0.0.1:9222:9222 \
  lightpanda/browser:nightly

# 验证 CDP 服务器
curl http://127.0.0.1:9222/json/version

# 查看运行状态
docker logs lightpanda
```

---

## Windows（WSL2）

Lightpanda 没有原生 Windows 二进制，需通过 WSL2 运行：

```powershell
# 安装 WSL2（管理员 PowerShell）
wsl --install

# 重启后，在 WSL 终端中按 Linux 步骤安装
```

WSL 会自动将 `localhost:9222` 转发给 Windows 宿主机，Puppeteer 脚本可在 Windows 侧直接连接。

---

## 系统安装（移动到 PATH）

```bash
# 将二进制移到系统 PATH
sudo mv lightpanda /usr/local/bin/

# 任意目录下都可使用
lightpanda version
```

---

## 验证安装

```bash
# 检查版本
./lightpanda version

# 测试 fetch 功能
./lightpanda fetch --dump markdown https://example.com | head -20

# 测试 CDP 服务器
./lightpanda serve &
curl http://127.0.0.1:9222/json/version
```

期望输出：`{"Browser": "lightpanda/..."}` 格式的 JSON。

---

## 完成确认检查清单

- [ ] `./lightpanda version` 返回版本号
- [ ] `./lightpanda fetch --dump markdown https://example.com` 返回 Markdown 内容
- [ ] CDP 服务器启动后 `curl http://127.0.0.1:9222/json/version` 返回 JSON

---

## 下一步

- [快速开始](02-quickstart.md) — CDP 服务器、Puppeteer 集成、MCP 配置
