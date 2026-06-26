# 安装指南

## 安装 fboxcli

### 通过 npm 安装（推荐）

```bash
npm install -g @flexem/fboxcli
```

安装后即可直接使用 `fboxcli` 命令。支持 Windows (x64)、macOS (ARM64) 和 Linux (x64)，npm 会自动下载对应平台的二进制文件。

### 从源码编译

前置条件：Rust 工具链（rustc 1.85+，支持 edition 2024）。

```bash
git clone https://github.com/flexem/fboxcli.git
cd fboxcli
cargo build --release
```

编译完成后，可执行文件位于：
- Windows: `target/release/fboxcli.exe`
- Linux/macOS: `target/release/fboxcli`

将可执行文件添加到系统 PATH，或复制到 PATH 中已有的目录。

### 从 Release 下载

前往 [GitHub Releases](https://github.com/flexem/fboxcli/releases) 下载对应平台的预编译文件。

## 配置 fboxcli

### 开发者模式

```bash
fboxcli config set \
  --server https://openapi.fbox360.com \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET

fboxcli auth login
```

### 用户模式

```bash
fboxcli auth login -u YOUR_USERNAME -p YOUR_PASSWORD
```

### 验证

```bash
fboxcli auth token
fboxcli box list
```

---

## 安装技能

### Claude Code

```bash
claude plugin marketplace add https://github.com/flexem/fbox-skills
claude plugin install fboxcli
```

### OpenClaw

在技能市场搜索 `fboxcli` 安装，或通过 URL 安装：

```
https://github.com/flexem/fbox-skills
```
