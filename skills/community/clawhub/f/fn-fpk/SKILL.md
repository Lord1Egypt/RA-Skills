---
name: fn-fpk
description: 飞牛NAS (fnOS) FPK 应用打包开发技能。使用此技能开发和打包飞牛NAS第三方应用（.fpk），包括：Native 应用（Node.js/Python/Java/Go/Shell 等）和 Docker 应用。涵盖整个开发周期：开发环境准备、fnpack 创建项目、manifest 配置、权限/资源配置、用户入口配置（应用入口 app/ui/config + 桌面图标 + 文件右键菜单）、生命周期脚本编写（cmd/main）、向导配置（wizard）、图标规范、CGI 反向代理、统一网关注册/认证、运行时环境（Python/Node.js/Java）、中间件服务（Redis/MinIO/RabbitMQ/MariaDB）、依赖管理、fnpack CLI 打包、appcenter-cli 测试安装、到上架发布。用户提到"飞牛"、"fnOS"、"FPK"、"飞牛应用"等关键词时触发。
---

# fn-fpk — 飞牛 NAS fnOS FPK 应用开发

> 基于官方文档 https://developer.fnnas.com 于 2026-06-02 全面更新。
> 系统架构: x86_64, Linux 内核 6.12.18+, Debian 发行版。
> fnpack 版本: 1.2.1, appcenter-cli 预装在 fnOS 中。

---

## 1. 开发环境准备

### 1.1 系统要求
- **fnOS 版本**: ≥ 0.9.27
- **架构**: 仅支持 x86_64 (AMD64) — 应用的编译选项也需选择 x86_64
- **存储**: 至少创建一个存储空间
- **权限**: 管理员权限（安装/卸载/系统设置）

### 1.2 开发方式
- **本地开发**: 在本地用 fnpack CLI 打包，再传送到 fnOS 设备安装
- **远程开发**: SSH 到 fnOS 设备直接开发，结合 `appcenter-cli install-local` 快速测试

### 1.3 技术栈
| 语言/框架 | 支持情况 |
|-----------|---------|
| Node.js | ✅ (v14/v16/v18/v20/v22) |
| Python | ✅ (3.8/3.9/3.10/3.11/3.12) |
| Java | ✅ (11/17/21 OpenJDK) |
| Go | ✅ Linux 运行时支持 |
| Shell | ✅ (Bash) |
| HTML/JS/CSS | ✅ 前端任意框架 |

### 1.4 CLI 工具

#### fnpack 打包工具
下载地址：https://static2.fnnas.com/fnpack/fnpack-1.2.1-{os}-{arch}

| 平台 | 二进制 |
|------|--------|
| Windows x86 | `fnpack-1.2.1-windows-amd64` |
| Linux x86 | `fnpack-1.2.1-linux-amd64` |
| Linux ARM | `fnpack-1.2.1-linux-arm64` |
| macOS Intel | `fnpack-1.2.1-darwin-amd64` |
| macOS M 系列 | `fnpack-1.2.1-darwin-arm64` |

安装：
```bash
chmod +x fnpack-1.2.1-linux-amd64
sudo mv fnpack-1.2.1-linux-amd64 /usr/local/bin/fnpack
fnpack --help
```

#### appcenter-cli （预装在 fnOS 中）
```bash
# 安装 fpk 文件
appcenter-cli install-fpk myapp.fpk

# 从本地目录安装（开发模式，无需打包）
cd /path/to/myapp
appcenter-cli install-local

# 管理应用
appcenter-cli list              # 已安装列表
appcenter-cli start myapp       # 启动
appcenter-cli stop myapp        # 停止

# 手动安装功能（仅测试用途）
appcenter-cli manual-install             # 查看状态
appcenter-cli manual-install enable      # 开启
appcenter-cli manual-install disable     # 关闭

# 设置默认存储空间
appcenter-cli default-volume             # 查看当前
appcenter-cli default-volume 1           # 设置存储空间1

# 静默安装（跳过向导）
appcenter-cli install-fpk myapp.fpk --env config.env
```

---

## 2. 应用类型

| 类型 | 描述 | 创建命令 |
|------|------|----------|
| **Native 应用** | 直接运行在 fnOS 上的应用 | `fnpack create <appname>` |
| **Docker 应用** | 基于 Docker Compose 容器编排 | `fnpack create <appname> --template docker` |
| **纯服务应用**（无 UI） | 无 Web 访问入口 | 加 `--without-ui true` |

---

## 3. 项目结构与核心文件

### 3.1 通用结构（fnpack create 生成）

```
myapp/
├── app/                      # 应用可执行文件/资源目录
│   ├── server/               # 后台服务程序（Native 应用）
│   ├── ui/                   # Web UI 入口配置
│   │   ├── images/           # 入口图标（icon_64.png, icon_256.png）
│   │   └── config            # 入口配置文件（JSON）
│   ├── www/                  # Web 静态资源（HTML/CSS/JS）
│   └── docker/               # Docker Compose 文件（Docker 应用）
│       └── docker-compose.yaml
├── manifest                  # 应用基本信息（必需）
├── cmd/                      # 生命周期管理脚本（全部必需）
│   ├── main                  # 启动/停止/状态检查
│   ├── install_init          # 安装前初始化
│   ├── install_callback      # 安装后回调
│   ├── uninstall_init        # 卸载前
│   ├── uninstall_callback    # 卸载后
│   ├── upgrade_init          # 升级前
│   ├── upgrade_callback      # 升级后
│   ├── config_init           # 配置变更前
│   └── config_callback       # 配置变更后
├── config/
│   ├── privilege             # 权限配置（JSON，必需）
│   └── resource              # 资源配置（JSON，必需）
├── wizard/                   # 向导配置（可选）
│   ├── install               # 安装向导
│   ├── uninstall             # 卸载向导
│   ├── upgrade               # 更新向导
│   └── config                # 配置向导
├── ICON.PNG                  # 64×64 应用图标（必需）
├── ICON_256.PNG              # 256×256 应用图标（必需）
└── LICENSE                   # 许可证（可选）
```

### 3.2 安装后的目录结构

当应用安装到 fnOS 后，系统创建如下目录：

```
/var/apps/[appname]/
├── cmd/                      # 生命周期脚本（来自包）
├── config/
│   ├── privilege             # 权限配置
│   └── resource              # 资源配置
├── ICON_256.PNG
├── ICON.PNG
├── LICENSE
├── manifest
├── etc -> /vol{volume}/@appconf/[appname]     # 静态配置文件
├── home -> /vol{volume}/@apphome/[appname]    # 用户数据
├── target -> /vol{volume}/@appcenter/[appname] # 可执行文件
├── tmp -> /vol{volume}/@apptemp/[appname]     # 临时文件
├── var -> /vol{volume}/@appdata/[appname]     # 运行时数据
├── shares/                   # 共享数据目录（按 resource 配置）
│   ├── datashare1 -> /vol{volume}/@appshare/datashare1
│   └── datashare2 -> /vol{volume}/@appshare/datashare2
└── wizard/                   # 向导配置（安装/卸载/升级/配置）
    ├── install
    ├── uninstall
    ├── upgrade
    └── config
```

---

## 4. manifest — 应用基本信息

`manifest` 文件是应用的"身份证"，放在项目根目录，**无扩展名**。

### 4.1 完整字段参考

```
# ═══════════════ 基本信息 ═══════════════
appname        = myapp                        # ① 应用唯一标识，系统全局唯一
version        = 1.0.0                        # ② 版本号：x[.y[.z]][-build]
display_name   = 我的应用                      # ③ 用户可见的名称
desc           = 这是一个示例应用              # ④ 详细介绍，支持 HTML 格式
source         = thirdparty                   # ⑤ 固定值：thirdparty

# ═══════════════ 系统要求 ═══════════════
platform       = x86                          # ⑥ 架构：x86 | arm | all (V1.1.8+)
arch           = x86_64                       # ⑦ 已废弃，请用 platform
os_min_version = 0.9.0                        # ⑧ 最低系统版本
os_max_version = 0.9.100                      # ⑨ 最高系统版本

# ═══════════════ 开发者信息 ═══════════════
maintainer     = 张三                          # 开发者/团队名称
maintainer_url = https://example.com           # 开发者网站
distributor    = 示例公司                      # 发布者
distributor_url = https://company.com          # 发布者网站

# ═══════════════ 安装与运行控制 ═══════════════
install_type   =                              # 安装位置：空=用户可选存储空间，root=系统分区
ctl_stop       = true                         # 是否显示启动/停止按钮，默认 true
checkport      = true                         # 是否启用端口检查，默认 true
service_port   = 8080                         # 应用监听端口（单个端口）
disable_authorization_path = false            # 是否禁用授权目录功能

# ═══════════════ 用户界面 ═══════════════
desktop_uidir          = ui                   # UI 组件目录（相对应用根目录）
desktop_applaunchname  = myapp.Application    # 默认启动入口 ID

# ═══════════════ 依赖管理 ═══════════════
install_dep_apps = mariaDB:redis              # 依赖应用列表，格式：app1>2.2.2:app2:app3

# ═══════════════ 应用更新 ═══════════════
changelog = 新增了XX功能                       # 更新日志（升级时展示）
```

### 4.2 字段详解

#### 应用标识
| 字段 | 必填 | 说明 |
|------|------|------|
| `appname` | ✅ | 全局唯一标识符，用于系统识别 |
| `version` | ✅ | 格式：`x[.y[.z]][-build]`，例如 `1.0.0`、`2.1.3-beta` |
| `display_name` | ✅ | 应用中心显示的名称 |
| `desc` | ✅ | 详细介绍，支持 HTML 格式 |
| `source` | ✅ | 固定为 `thirdparty` |

#### 系统要求（V1.1.8+ 新增 platform 字段）
| 字段 | 说明 |
|------|------|
| `platform = x86` | 仅支持 x86 架构 |
| `platform = arm` | 仅支持 arm 架构 |
| `platform = all` | 所有架构，Docker 应用常用 |
| `arch` | 【已废弃】用 platform 替代 |

#### 安装控制
| 字段 | 默认值 | 说明 |
|------|--------|------|
| `install_type` | 空 | `root` = 安装到系统分区 `/usr/local/apps/@appcenter/`；空 = 用户选择存储位置 |
| `ctl_stop` | `true` | `false` 时隐藏启动/停止按钮和运行状态（无进程应用） |
| `checkport` | `true` | `false` 时系统不检查端口占用 |
| `service_port` | — | 应用监听端口（仅支持单个端口） |
| `disable_authorization_path` | `false` | `true` 时应用设置页不显示授权目录操作 |

#### 依赖管理
```ini
# 格式：app1>2.2.2:app2:app3
# > 表示最低版本要求
# : 分隔多个依赖
# 系统按列表顺序自动安装依赖
install_dep_apps = mariaDB:redis
```

---

## 5. 权限配置 (config/privilege)

`config/privilege` 文件定义应用运行时的权限级别和用户身份，JSON 格式，**必需**。

### 5.1 默认权限模式（推荐）

```json
{
  "defaults": {
    "run-as": "package"
  },
  "username": "myapp_user",
  "groupname": "myapp_group"
}
```

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `run-as` | `package` | `package` = 应用用户模式，`root` = root 模式 |
| `username` | appname | 应用专用用户名 |
| `groupname` | appname | 应用专用用户组名 |

#### 默认模式行为
- 系统为应用创建专用用户和用户组
- 所有应用进程以专用用户身份运行
- 应用文件所有者是该专用用户
- 应用只能访问自己的目录和系统允许的公共资源

### 5.2 Root 权限模式

> ⚠️ 仅飞牛官方合作的企业开发者可使用，第三方应用默认无法在应用中心发布 root 权限应用。

```json
{
  "defaults": {
    "run-as": "root"
  },
  "username": "myapp_user",
  "groupname": "myapp_group"
}
```

#### Root 模式行为
- 应用脚本以 root 身份执行
- 应用进程可以 root 身份或指定应用用户身份运行
- 应用文件所有者变为 root
- 系统仍会创建应用专用用户和用户组

### 5.3 外部文件访问权限

应用默认无法访问用户个人文件。用户需要在应用设置中授权：
- **读写权限**：读取和修改文件
- **只读权限**：只能读取，不能修改
- **禁止访问**：无法访问该路径

也可通过 `config/resource` 的 `data-share` 设置默认共享目录。

### 5.4 当前用户检查

```bash
echo "当前运行用户: $TRIM_RUN_USERNAME"
echo "应用专用用户: $TRIM_USERNAME"
```

---

## 6. 资源配置 (config/resource)

`config/resource` 文件声明应用的扩展能力，JSON 格式，**必需**。

### 6.1 数据共享 (data-share)

创建共享目录，用户通过 **文件管理 → 应用文件** 可访问，应用也可实时访问。

```json
{
  "data-share": {
    "shares": [
      {
        "name": "documents",
        "permission": {
          "rw": ["myapp_user"]
        }
      },
      {
        "name": "documents/backups",
        "permission": {
          "ro": ["myapp_user"]
        }
      }
    ]
  }
}
```

| 字段 | 说明 |
|------|------|
| `name` | 共享目录名，支持多级（如 `documents/backups`） |
| `permission.rw` | 读写权限用户列表 |
| `permission.ro` | 只读权限用户列表 |

### 6.2 系统集成 (usr-local-linker)

应用启动时自动创建软链接到系统目录，停止时自动移除。

```json
{
  "usr-local-linker": {
    "bin": [
      "bin/myapp-cli",
      "bin/myapp-server"
    ],
    "lib": [
      "lib/mylib.so",
      "lib/mylib.a"
    ],
    "etc": [
      "etc/myapp.conf",
      "etc/myapp.d/default.conf"
    ]
  }
}
```

| 链接 | 目标目录 |
|------|----------|
| `bin` | `/usr/local/bin/` |
| `lib` | `/usr/local/lib/` |
| `etc` | `/usr/local/etc/` |

### 6.3 Docker 项目支持 (docker-project)

Docker 应用需要在 `config/resource` 中声明：

```json
{
  "docker-project": {
    "projects": [
      {
        "name": "myapp-stack",
        "path": "docker"
      }
    ]
  }
}
```

| 字段 | 说明 |
|------|------|
| `name` | Docker Compose 项目名称 |
| `path` | 相对于 app 目录的路径，指向含 `docker-compose.yaml` 的文件夹 |

---

## 7. 入口配置 (app/ui/config)

应用入口是用户访问应用的"大门"。配置文件位于 `app/ui/config`（JSON 格式），入口键名必须以 `appname` 为前缀。

### 7.1 桌面图标入口

```json
{
  ".url": {
    "myapp.main": {
      "title": "我的应用",
      "icon": "images/icon_{0}.png",
      "type": "url",
      "protocol": "http",
      "port": "8080",
      "url": "/",
      "allUsers": true
    },
    "myapp.admin": {
      "title": "管理后台",
      "icon": "images/admin_icon_{0}.png",
      "type": "url",
      "protocol": "http",
      "port": "8080",
      "url": "/admin",
      "allUsers": false
    }
  }
}
```

### 7.2 文件右键入口

```json
{
  ".url": {
    "myapp.editor": {
      "title": "文本编辑器",
      "icon": "images/editor-{0}.png",
      "type": "url",
      "protocol": "http",
      "port": "8080",
      "url": "/edit",
      "allUsers": true,
      "fileTypes": ["txt", "md", "json", "xml"],
      "noDisplay": true
    }
  }
}
```

`fileTypes` + `noDisplay: true` 实现"只在文件右键菜单中显示，不在桌面显示"。

### 7.3 CGI 入口（推荐用于静态页面/Native 应用）

```json
{
  ".url": {
    "myapp.Application": {
      "title": "我的应用",
      "icon": "images/icon_{0}.png",
      "type": "iframe",
      "protocol": "http",
      "url": "/cgi/ThirdParty/myapp/index.cgi/",
      "allUsers": true
    }
  }
}
```

> CGI 方案不需要声明 `port` 字段。

### 7.4 入口字段参考

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✅ | 入口显示标题（桌面图标名称/右键菜单名称） |
| `icon` | ✅ | 图标路径（相对 UI 目录），`{0}` 会被替换为 `64` 或 `256` |
| `type` | ✅ | `url` = 新标签页打开，`iframe` = 桌面窗口内嵌 |
| `protocol` | ✅ | `http` / `https` / `""`（空字符串=自适应协议；不声明则默认 `http`） |
| `port` | ✅ | 端口号；CGI 方案无需声明；可使用 `${wizard_port}` 动态配置 (V1.1.8+) |
| `url` | ✅ | 访问路径（相对路径）；可使用 `${wizard_url}` 动态配置 (V1.1.8+) |
| `allUsers` | ✅ | `true` = 所有用户可见，`false` = 仅管理员可见 |
| `fileTypes` | ❌ | 文件右键关联的文件扩展名数组，如 `["txt","md"]` |
| `noDisplay` | ❌ | `true` = 不在桌面显示，仅右键菜单显示 |
| `accessPerm` | ❌ | 桌面访问设置权限：`editable` / `readonly` / `hidden` |
| `gatewaySocket` | ❌ | 统一网关 Socket 文件名 |
| `gatewayPrefix` | ❌ | 统一网关访问前缀，如 `/app/myapp` |

#### 入口配置文件支持环境变量 (V1.1.8+)
```json
{
  "myapp.configurable": {
    "title": "可配置应用",
    "port": "${wizard_port}",
    "url": "${wizard_path}"
  }
}
```

#### 控制字段
```json
{
  "myapp.advanced": {
    "title": "高级功能",
    "control": {
      "accessPerm": "readonly"
    }
  }
}
```

### 7.5 文件路径参数

通过右键菜单打开文件时，系统自动在 URL 后拼接 `path` 参数：
```
http://localhost:8080/edit?path=/vol1/Users/admin/Documents/example.txt
```

### 7.6 CGI 脚本示例

`app/ui/index.cgi` — 通过 Shell 脚本实现静态资源转发：

```bash
#!/bin/bash

# 【注意】修改为你的静态文件根目录
BASE_PATH="/var/apps/App.Native.HelloFnosAppCenter/target/www"

# 从 REQUEST_URI 里拿到 index.cgi 后面的路径
URI_NO_QUERY="${REQUEST_URI%%\?*}"
REL_PATH="/"

case "$URI_NO_QUERY" in
  *index.cgi*)
    REL_PATH="${URI_NO_QUERY#*index.cgi}"
    ;;
esac

if [ -z "$REL_PATH" ] || [ "$REL_PATH" = "/" ]; then
  REL_PATH="/index.html"
fi

TARGET_FILE="${BASE_PATH}${REL_PATH}"

# 防御 .. 越级访问
if echo "$TARGET_FILE" | grep -q '\.\.'; then
  echo "Status: 400 Bad Request"
  echo "Content-Type: text/plain; charset=utf-8"
  echo ""
  echo "Bad Request"
  exit 0
fi

if [ ! -f "$TARGET_FILE" ]; then
  echo "Status: 404 Not Found"
  echo "Content-Type: text/plain; charset=utf-8"
  echo ""
  echo "404 Not Found: ${REL_PATH}"
  exit 0
fi

# 根据扩展名判断 Content-Type（精简版，完整版见社区参考）
ext="${TARGET_FILE##*.}"
case "$ext" in
  html|htm)  mime="text/html; charset=utf-8" ;;
  css)       mime="text/css; charset=utf-8" ;;
  js)        mime="application/javascript; charset=utf-8" ;;
  png)       mime="image/png" ;;
  jpg|jpeg)  mime="image/jpeg" ;;
  *)         mime="application/octet-stream" ;;
esac

echo "Content-Type: $mime"
echo ""
cat "$TARGET_FILE"
```

> 更多 CGI 实现参考：https://github.com/FNOSP/fnosAppCenterCgiCollection

---

## 8. 生命周期脚本 (cmd/)

系统通过调用 `cmd/` 目录下的脚本来管理应用的全生命周期。所有脚本均为 Bash 脚本，全部**必需**（即使只写 `exit 0`）。

> 注意：不要用 `echo` 直接输出错误信息，而是写入 `$TRIM_TEMP_LOGFILE`；不要直接 `exit`，而是返回错误码 `1`。

### 8.1 cmd/main — 启动/停止/状态检查

```bash
#!/bin/bash

case $1 in
start)
  # 启动应用的命令，成功返回 0，失败返回 1
  exit 0
  ;;
stop)
  # 停止应用的命令，成功返回 0，失败返回 1
  exit 0
  ;;
status)
  # 检查应用运行状态，运行中返回 0，未运行返回 3
  exit 0
  ;;
*)
  exit 1
  ;;
esac
```

#### 应用状态监控

| 返回值 | 含义 |
|--------|------|
| `exit 0` | 应用正在运行 |
| `exit 3` | 应用未运行 |
| `exit 1` | 执行失败 |

系统会在启动前检查一次，运行期间定期轮询检查。

### 8.2 Native 应用完整启动脚本

```bash
#!/bin/bash

LOG_FILE="${TRIM_PKGVAR}/info.log"
PID_FILE="${TRIM_PKGVAR}/app.pid"
DATA_DIR="${TRIM_DATA_SHARE_PATHS%%:*}"
CMD="DATA_DIR=${DATA_DIR} PORT=5001 node ${TRIM_APPDEST}/server/server.js"

log_msg() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> ${LOG_FILE}
}

start_process() {
  if status; then return 0; fi
  log_msg "Starting process ..."
  bash -c "${CMD}" >> ${LOG_FILE} 2>&1 &
  printf "%s" "$!" > ${PID_FILE}
  return 0
}

stop_process() {
  log_msg "Stopping process ..."
  if [ -r "${PID_FILE}" ]; then
    pid=$(head -n 1 "${PID_FILE}" | tr -d '[:space:]')
    log_msg "pid=${pid}"
    if ! kill -0 "${pid}" 2>/dev/null; then
      rm -f "${PID_FILE}"
      return
    fi
    log_msg "send TERM signal to PID:${pid}..."
    kill -TERM ${pid} >> ${LOG_FILE} 2>&1
    local count=0
    while kill -0 "${pid}" 2>/dev/null && [ $count -lt 10 ]; do
      sleep 1; count=$((count + 1))
    done
    if kill -0 "${pid}" 2>/dev/null; then
      kill -KILL "${pid}"
    fi
    rm -f "${PID_FILE}"
  fi
}

status() {
  if [ -f "${PID_FILE}" ]; then
    pid=$(head -n 1 "${PID_FILE}" | tr -d '[:space:]')
    if kill -0 "${pid}" 2>/dev/null; then return 0; fi
    rm -f "${PID_FILE}"
  fi
  return 1
}

case $1 in
  start)  start_process ;;
  stop)   stop_process ;;
  status) if status; then exit 0; else exit 3; fi ;;
  *)      exit 1 ;;
esac
```

### 8.3 运行环境配置

#### Node.js
```bash
# 在 cmd 脚本中配置，可选版本：nodejs_v22 / v20 / v18 / v16 / v14
export PATH=/var/apps/nodejs_v22/target/bin:$PATH
node -v
npm -v
```

#### Python
```bash
# 可选版本：python312 / 311 / 310 / 39 / 38
export PATH=/var/apps/python312/target/bin:$PATH
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Java
```bash
# 可选版本：java-21-openjdk / java-17-openjdk / java-11-openjdk
export PATH=/var/apps/java-21-openjdk/target/bin:$PATH
java --version
```

### 8.4 应用配置与文件写入

飞牛 NAS 应用安装后，系统会在多个目录下为应用分配存储空间。不同目录的用途和权限差异很大，理解它们对写出健壮的应用至关重要。

#### 目录一览

| 目录 | 权限 | 用途 | 系统写入 | 应用写入 |
|------|------|------|----------|----------|
| `/vol1/@appconf/{appname}/settings.conf` | 应用用户 | **应用配置**（端口、路径等） | ✅（向导/设置页面） | ✅ |
| `/vol1/@appdata/{appname}/` | 应用用户 | **应用数据**（运行时日志、数据库等） | ✘ | ✅ |
| `/vol1/@apphome/{appname}/` | 应用用户 | **应用家目录** | ✘ | ✅ |
| `/vol1/@apptemp/{appname}/` | 应用用户 | **缓存/临时文件** | ✘ | ✅ |
| `/vol1/@appshare/{appname}/` | 应用用户 | **共享目录**（同 `TRIM_DATA_SHARE_PATHS`） | ✘ | ✅ |
| `/vol1/@appcenter/{appname}/` | 应用用户 | **应用本身代码（只读）** | ✘（可手动修改但不建议） | ✘ |

> 存储在 `/vol1/@appcenter/` 下的是应用包的运行目录（`app/server/` 等），不是 `@appconf/`。

#### settings.conf：应用配置的核心

`/vol1/@appconf/{appname}/settings.conf` 是 NAS 系统与应用之间的配置桥梁。它的格式为 `KEY=VALUE` 纯文本，**系统会在以下时机自动重写此文件**：

1. **安装/更新**时——写入 `wizard/` 向导收集的用户输入（以 `wizard_` 为前缀的环境变量）
2. **应用设置页面**修改时——写入授权文件夹、端口等系统级配置
3. 应用本身也可以主动写入此文件，但要注意**系统下次重写时会覆盖**

#### ⚠️ 常见陷阱：系统重写覆盖问题

```
# settings.conf 被系统重写后：
MUSIC_PATH=/vol1/1000/Music       ← 路径被系统改写，可能与真实路径名不符
PORT=5200
```

已知问题：
1. **路径命名差异**——用户实际选的文件夹名（如 `music11` / `music22`）被系统写成了 `Music`（大小写不一致或截断）
2. **授权文件夹丢失**——用户授权了多个数据目录，但系统只保存了第一个
3. **每次修改设置都会覆盖**——手动改 `settings.conf` 后，只要用户进一次应用设置页面就会被重置
4. **`data-share` 可能为空**——`config/resource` 中 `data-share.shares` 数组不更新，导致 `TRIM_DATA_ACCESSIBLE_PATHS` 环境变量为空

#### 应对策略

**策略一：应用启动时自读 settings.conf（推荐，最通用）**

不依赖 `cmd/main` 传环境变量，让应用服务进程启动时**自己读取 `settings.conf`**。这样不管 NAS 系统以何种方式拉起进程（自动启动、手动重启）都能正确拿到配置。

```javascript
// Node.js — 在读取 PORT / MUSIC_PATH 之前执行
var path = require('path');
var fs = require('fs');

// settings.conf 实际位置：
//   @appconf 的挂载点 = __dirname 减去 @appcenter 后的相对路径
var confPath = path.resolve(__dirname, '../../../@appconf/YOUR_APP_NAME/settings.conf');
try {
  var confContent = fs.readFileSync(confPath, 'utf-8');
  var confLines = confContent.split(String.fromCharCode(10));
  for (var i = 0; i < confLines.length; i++) {
    var line = confLines[i].trim();
    if (line && !line.startsWith('#')) {
      var eqIdx = line.indexOf('=');
      if (eqIdx > 0) {
        var key = line.substring(0, eqIdx).trim();
        var val = line.substring(eqIdx + 1).trim();
        if (process.env[key] === undefined) process.env[key] = val;
      }
    }
  }
} catch(e) { /* 配置文件不存在时忽略 */ }

const PORT = process.env.PORT || 6688;      // 已被 settings.conf 注入
```

> 注意：这段代码必须放在 `PORT` 声明**之前**，否则环境变量已经读过了，兜底逻辑不会生效。

```python
# Python 版本
import os

def load_settings():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               '..', '@appconf', 'YOUR_APP_NAME', 'settings.conf')
    # 更准确的：从 __file__ 向上走到 @appcenter，再到 @appconf
    config_path = os.path.normpath(config_path)
    if not os.path.exists(config_path):
        return
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip()
                if key not in os.environ:
                    os.environ[key] = val

load_settings()
PORT = int(os.environ.get('PORT', 6688))
```

**策略二：只用 cmd/main 传环境变量（较脆弱）**

```bash
# cmd/main 中正确的做法：读 settings.conf + 传环境变量
. /vol1/@appconf/YOUR_APP_NAME/settings.conf
export PORT MUSIC_PATH
node /vol1/@appcenter/YOUR_APP_NAME/server/server.js
```

局限：NAS 自动启动时可能不经过 `cmd/main`，环境变量仍然丢失。

**策略三：验证路径有效性，失败时友好报错**

```javascript
var musicPaths = (process.env.MUSIC_PATH || '').split(':').filter(Boolean);
var validPaths = [];
musicPaths.forEach(function(p) {
  try {
    if (fs.statSync(p).isDirectory()) {
      validPaths.push(p);
    }
  } catch(e) {
    console.error('Music directory not found:', p);
  }
});
if (validPaths.length === 0) {
  console.error('No valid music folder. Please set it in App Settings.');
  process.exit(1);
}
```

#### 实践建议

1. **首选策略一**（应用自读 settings.conf）+ **策略三**（路径验证），覆盖所有启动场景
2. 不要依赖 `TRIM_DATA_ACCESSIBLE_PATHS` 环境变量——它可能为空
3. 对于 Native 应用，建议在 `cmd/main` 和 app 代码中都实现配置读取，双重保险
4. 如果发现路径不匹配（如实际文件夹 `music11` 但配置写 `Music`），先确认是否是 NAS 系统写入的问题，**不要**在代码里做硬编码的路径猜测

#### ⚠️ 端口变更的实战陷阱

##### 问题描述
用户在安装向导/应用设置中修改端口（`wizard_port`）后，应用重启仍然监听默认端口。

##### 根因分析
飞牛系统通过 `TRIM_SERVICE_PORT` 环境变量（来源：manifest 的 `service_port` 字段）将端口注入 `cmd/main`。但关键问题在于：

- **`service_port` 只在打包时固定**，用户在安装向导或应用设置中修改端口后，`service_port` **不会自动更新**
- `TRIM_SERVICE_PORT` 的值在首次安装后即固定，不会因 `wizard_port` 变更而重新注入
- `config_callback` 虽然能通过 `$wizard_port` 变量拿到新端口，但直接调用 `cmd/main start` 时传给 Node 的仍然是旧的 `TRIM_SERVICE_PORT`

##### 修复方案：三级端口优先级
`cmd/main` 中端口获取应按以下优先级：

```bash
# 第一优先级：settings.conf 中持久化的 PORT（来自安装向导 / 应用设置的 wizard_port）
if [ -f "${TRIM_PKGETC}/settings.conf" ]; then
  . "${TRIM_PKGETC}/settings.conf"
fi
# 第二优先级：TRIM_SERVICE_PORT（系统注入，来自 manifest service_port）
# 第三优先级：默认值
PORT="${PORT:-${TRIM_SERVICE_PORT:-8080}}"
```

##### 完整工作流
1. **安装时**：`install_callback` 将 `$wizard_port` 写入 `${TRIM_PKGETC}/settings.conf`
2. **修改端口时**（应用设置页面）：`config_callback` 将 `$wizard_port` 写入 `settings.conf`，然后重启
3. **任何后续启动**（系统自动启动、手动重启）：`cmd/main` 优先读取 `settings.conf` 中的 `PORT`，不受 `TRIM_SERVICE_PORT` 旧值影响

##### 配套的 config_callback
```bash
PORT="${wizard_port:-8080}"

# 先持久化端口到 settings.conf
mkdir -p "${TRIM_PKGETC}"
cat > "${TRIM_PKGETC}/settings.conf" <<EOF
PORT=${PORT}
EOF

# 然后重启（此时不需要传 TRIM_SERVICE_PORT，因为 cmd/main 会自读 settings.conf）
bash "${0%/*}/main" stop
sleep 1
bash "${0%/*}/main" start
```

##### 要点
- **`settings.conf` 的自定义写入要放到 `install_callback` 和 `config_callback` 中**，不要在 `install_init` 或其他脚本中写，否则可能在安装流程中被系统覆盖
- `TRIM_SERVICE_PORT` 仍然可以作为 fallback 使用，但**不要把它作为唯一的端口来源**
- 如果 `settings.conf` 被系统重写覆盖了 `PORT`（某些系统版本已知问题），检查端口是否仍然正确，必要时在 `config_init` 中添加校验

### 8.4 Docker 应用的 main 脚本

Docker 应用的启停由系统通过 compose 管理，但需要定义状态检查：

```bash
#!/bin/bash

FILE_PATH="${TRIM_APPDEST}/docker/docker-compose.yaml"

is_docker_running () {
  DOCKER_NAME=""
  if [ -f "$FILE_PATH" ]; then
    DOCKER_NAME=$(cat $FILE_PATH | grep "container_name" | awk -F ':' '{print $2}' | xargs)
    echo "DOCKER_NAME is set to: $DOCKER_NAME"
  fi
  if [ -n "$DOCKER_NAME" ]; then
    docker inspect $DOCKER_NAME | grep -q "\"Status\": \"running\"," || exit 1
    return
  fi
}

case $1 in
  start)  exit 0 ;;  # compose 管理，无需额外操作
  stop)   exit 0 ;;  # compose 管理，无需额外操作
  status) if is_docker_running; then exit 0; else exit 3; fi ;;
  *)      exit 1 ;;
esac
```

### 8.5 错误异常展示处理（V1.1.8+）

向 `$TRIM_TEMP_LOGFILE` 写入错误信息并返回错误码 `1`，系统会自动以 Dialog 对话框展示给用户：

```bash
# ✅ 正确做法
echo "配置文件不存在，应用启动失败！" > "${TRIM_TEMP_LOGFILE}"
exit 1

# ❌ 错误做法
# echo "配置文件不存在，应用启动失败！"
# exit 1
```

### 8.6 生命周期事件说明

| 事件 | 脚本 | 时机 |
|------|------|------|
| 安装前 | `install_init` | 文件解压前，可做环境检查、依赖安装 |
| 安装后 | `install_callback` | 文件解压后，可做初始化配置 |
| 卸载前 | `uninstall_init` | 停止应用后，卸载前 |
| 卸载后 | `uninstall_callback` | 可清理剩余数据和目录 |
| 升级前 | `upgrade_init` | 更新处理前 |
| 升级后 | `upgrade_callback` | 可做数据库升级、配置迁移 |
| 配置变更前 | `config_init` | 用户保存配置后，重启前 |
| 配置变更后 | `config_callback` | 可监听配置变化调整运行逻辑 |

#### 卸载时保留/删除数据
系统默认保留 `var` 和 `shares` 目录。如果希望在卸载向导中让用户选择是否删除数据，在 `wizard/uninstall` 中配置选项，在 `cmd/uninstall_callback` 中根据用户选择清理：

```bash
if [ "$wizard_data_action" = "delete" ]; then
  rm -rf "${TRIM_PKGVAR}" "${TRIM_DATA_SHARE_PATHS}"
fi
```

---

## 9. 环境变量参考

### 9.1 系统环境变量

| 变量 | 说明 |
|------|------|
| `$TRIM_APPNAME` | 应用名称 |
| `$TRIM_APPVER` | 应用版本号 |
| `$TRIM_APPDEST` | 应用可执行文件目录（target） |
| `$TRIM_PKGETC` | 配置文件目录（etc） |
| `$TRIM_PKGVAR` | 运行时数据目录（var） |
| `$TRIM_TEMP_LOGFILE` | 临时日志文件路径（用户可见） |
| `$TRIM_SERVICE_PORT` | 服务端口 |
| `$TRIM_USERNAME` | 应用专用用户名 |
| `$TRIM_RUN_USERNAME` | 当前运行用户（`root` 或应用用户） |
| `$TRIM_DATA_SHARE_PATHS` | 数据共享目录路径列表（冒号分隔） |

### 9.2 向导输入变量

用户在向导中的选择会变成同名的环境变量，在脚本中可直接使用：

```bash
ADMIN_USERNAME="$wizard_admin_username"
DATABASE_TYPE="$wizard_database_type"
APP_PORT="$wizard_app_port"
```

### 9.3 应用入口中的动态变量（V1.1.8+）

入口配置文件 `app/ui/config` 中可使用 `${variable_name}` 动态引用向导参数：

```json
{
  "port": "${wizard_port}",
  "url": "${wizard_path}"
}
```

---

## 10. 向导配置 (wizard/)

向导是用户与应用交互的"引导员"，JSON 格式，每个文件是一个 JSON 数组（多个步骤）。

### 10.1 向导类型

| 文件 | 用途 |
|------|------|
| `wizard/install` | 安装时的配置界面 |
| `wizard/uninstall` | 卸载时的确认界面 |
| `wizard/upgrade` | 更新时的配置界面 |
| `wizard/config` | 设置时的配置界面 |

### 10.2 向导文件结构

```json
[
  {
    "stepTitle": "第一步标题",
    "items": [
      { 表单项 1 },
      { 表单项 2 }
    ]
  },
  {
    "stepTitle": "第二步标题",
    "items": [
      { 表单项 3 }
    ]
  }
]
```

### 10.3 表单项类型

#### text — 文本输入
```json
{
  "type": "text",
  "field": "wizard_username",
  "label": "用户名",
  "initValue": "admin",
  "rules": [
    { "required": true, "message": "请输入用户名" },
    { "min": 3, "max": 20, "message": "长度应在3-20字符之间" }
  ]
}
```

#### password — 密码输入
```json
{
  "type": "password",
  "field": "wizard_password",
  "label": "管理员密码",
  "rules": [
    { "required": true, "message": "请输入密码" },
    { "min": 6, "message": "密码长度不能少于6位" }
  ]
}
```

#### radio — 单选
```json
{
  "type": "radio",
  "field": "wizard_install_type",
  "label": "安装类型",
  "initValue": "standard",
  "options": [
    { "label": "标准安装", "value": "standard" },
    { "label": "自定义安装", "value": "custom" }
  ],
  "rules": [{ "required": true, "message": "请选择安装类型" }]
}
```

#### checkbox — 多选
```json
{
  "type": "checkbox",
  "field": "wizard_modules",
  "label": "安装模块",
  "initValue": ["web", "api"],
  "options": [
    { "label": "Web界面", "value": "web" },
    { "label": "API接口", "value": "api" },
    { "label": "数据库", "value": "database" }
  ],
  "rules": [{ "required": true, "message": "请至少选择一个模块" }]
}
```

#### select — 下拉选择
```json
{
  "type": "select",
  "field": "wizard_database_type",
  "label": "数据库类型",
  "initValue": "sqlite",
  "options": [
    { "label": "SQLite (推荐)", "value": "sqlite" },
    { "label": "MySQL", "value": "mysql" },
    { "label": "PostgreSQL", "value": "postgresql" }
  ],
  "rules": [{ "required": true, "message": "请选择数据库类型" }]
}
```

#### switch — 开关
```json
{
  "type": "switch",
  "field": "wizard_enable_backup",
  "label": "启用自动备份",
  "initValue": "true"
}
```

#### tips — 提示文本（不收集输入）
```json
{
  "type": "tips",
  "helpText": "请阅读 <a target=\"_blank\" href=\"https://example.com/privacy\">隐私政策</a>。"
}
```

### 10.4 验证规则

| 规则 | 示例 |
|------|------|
| 必填 | {\"required\": true, \"message\": \"此字段不能为空\"} |
| 最小长度 | {\"min\": 3, \"message\": \"长度不能少于3\"} |
| 最大长度 | {\"max\": 50, \"message\": \"长度不能超过50\"} |
| 精确长度 | {\"len\": 6, \"message\": \"请输入6位验证码\"} |
| 正则 | {\"pattern\": \"^[a-zA-Z0-9_]+$\", \"message\": \"只能含字母数字下划线\"} |

### 10.5 安装向导完整示例

```json
[
  {
    \"stepTitle\": \"欢迎安装\",
    \"items\": [
      {
        \"type\": \"tips\",
        \"helpText\": \"欢迎使用我们的应用！在开始使用前，请阅读并同意我们的服务条款。\"
      },
      {
        \"type\": \"switch\",
        \"field\": \"wizard_agree_terms\",
        \"label\": \"我已阅读并同意服务条款\",
        \"rules\": [
          { \"required\": true, \"message\": \"请同意服务条款\" }
        ]
      }
    ]
  },
  {
    \"stepTitle\": \"创建管理员账号\",
    \"items\": [
      {
        \"type\": \"text\",
        \"field\": \"wizard_admin_username\",
        \"label\": \"管理员用户名\",
        \"initValue\": \"admin\",
        \"rules\": [
          { \"required\": true, \"message\": \"请输入管理员用户名\" },
          { \"pattern\": \"^[a-zA-Z0-9_]+$\", \"message\": \"只能包含字母、数字和下划线\" }
        ]
      },
      {
        \"type\": \"password\",
        \"field\": \"wizard_admin_password\",
        \"label\": \"管理员密码\",
        \"rules\": [
          { \"required\": true, \"message\": \"请输入密码\" },
          { \"min\": 8, \"message\": \"密码长度不能少于8位\" }
        ]
      },
      {
        \"type\": \"password\",
        \"field\": \"wizard_admin_password_confirm\",
        \"label\": \"确认密码\",
        \"rules\": [
          { \"required\": true, \"message\": \"请确认密码\" }
        ]
      }
    ]
  },
  {
    \"stepTitle\": \"应用配置\",
    \"items\": [
      {
        \"type\": \"select\",
        \"field\": \"wizard_database_type\",
        \"label\": \"数据库类型\",
        \"initValue\": \"sqlite\",
        \"options\": [
          { \"label\": \"SQLite (推荐，无需额外配置)\", \"value\": \"sqlite\" },
          { \"label\": \"MySQL\", \"value\": \"mysql\" }
        ]
      },
      {
        \"type\": \"text\",
        \"field\": \"wizard_app_port\",
        \"label\": \"应用端口\",
        \"initValue\": \"8080\",
        \"rules\": [
          { \"required\": true, \"message\": \"请输入端口号\" },
          { \"pattern\": \"^[0-9]+$\", \"message\": \"端口号必须是数字\" }
        ]
      }
    ]
  }
]
```

### 10.6 卸载向导示例

```json
[
  {
    \"stepTitle\": \"确认卸载\",
    \"items\": [
      {
        \"type\": \"tips\",
        \"helpText\": \"您即将卸载此应用。请选择如何处理应用数据：\"
      },
      {
        \"type\": \"radio\",
        \"field\": \"wizard_data_action\",
        \"label\": \"数据保留选项\",
        \"initValue\": \"keep\",
        \"options\": [
          { \"label\": \"保留数据（推荐）- 将来重新安装时可恢复\", \"value\": \"keep\" },
          { \"label\": \"删除所有数据 - 此操作不可恢复！\", \"value\": \"delete\" }
        ],
        \"rules\": [
          { \"required\": true, \"message\": \"请选择数据保留选项\" }
        ]
      },
      {
        \"type\": \"tips\",
        \"helpText\": \"<strong>警告：</strong> 选择删除数据后，所有应用数据将永久丢失，无法恢复。\"
      }
    ]
  }
]
```

### 10.7 获取用户输入

```bash
# 用户输入直接作为环境变量使用
ADMIN_USERNAME=\"\$wizard_admin_username\"
ADMIN_PASSWORD=\"\$wizard_admin_password\"
DATABASE_TYPE=\"\$wizard_database_type\"
APP_PORT=\"\$wizard_app_port\"
```

## 11. 图标规范

### 11.1 包文件图标（根目录）

| 文件 | 尺寸 | 格式 | 必填 |
|------|------|------|------|
| `ICON.PNG` | 64×64 像素 | PNG，不透明 | ✅ |
| `ICON_256.PNG` | 256×256 像素 | PNG，不透明 | ✅ |

> 含圆角矩形背景的 PSD 源文件可下载：https://static.fnnas.com/appcenter-marketing/fnpack_ICON_256.zip

### 11.2 UI 入口图标（app/ui/images/）

| 文件 | 尺寸 | 命名规则 |
|------|------|----------|
| `icon_64.png` | 64×64 | **小写**，配置中 `{0}` 替换为尺寸 |
| `icon_256.png` | 256×256 | 如 `images/icon_{0}.png` → 自动选取 |

---

## 12. Docker 应用构建详解

### 12.1 创建项目

```bash
fnpack create my-app --template docker
```

### 12.2 目录结构

```
my-app/
├── app/
│   ├── docker/
│   │   └── docker-compose.yaml
│   └── ui/
│       ├── images/
│       └── config
├── manifest
├── cmd/
├── config/
│   ├── privilege
│   └── resource
├── wizard/
├── LICENSE
├── ICON.PNG
└── ICON_256.PNG
```

### 12.3 docker-compose.yaml 示例

```yaml
version: '3.8'

services:
  web:
    image: myapp:latest
    container_name: myapp-web
    ports:
      - "${TRIM_SERVICE_PORT}:80"
    volumes:
      - "${TRIM_PKGVAR}:/app/data"
      - "${TRIM_DATA_SHARE_PATHS}:/app/shares"
    environment:
      - DB_HOST=db
      - APP_PORT=${TRIM_SERVICE_PORT}

  db:
    image: mysql:8.0
    container_name: myapp-db
    environment:
      - MYSQL_ROOT_PASSWORD=${wizard_db_password}
      - MYSQL_DATABASE=myapp
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

> `docker-compose.yaml` 支持使用全部系统环境变量和向导变量。
> 系统统一管理 compose 的启动/停止，`cmd/main` 只需要实现 status 检查。

### 12.4 资源配置

```json
{
  "docker-project": {
    "projects": [
      {
        "name": "myapp-stack",
        "path": "docker"
      }
    ]
  }
}
```

---

## 13. 统一网关（fnOS V1.1.3100+）

统一网关为应用提供稳定的访问入口，无需新增端口监听。HTTP 和 WebSocket 均可接入。

### 13.1 接入方式

在 `app/ui/config` 中声明 `gatewayPrefix` 和 `gatewaySocket`：

```json
{
  ".url": {
    "myapp.main": {
      "title": "我的应用",
      "icon": "images/icon_{0}.png",
      "type": "iframe",
      "protocol": "",
      "gatewaySocket": "app.sock",
      "gatewayPrefix": "/app/myapp",
      "url": "/app/myapp",
      "allUsers": true
    }
  }
}
```

#### 字段说明
| 字段 | 条件 | 说明 |
|------|------|------|
| `gatewayPrefix` | 两者均非空时注册 | 网关访问前缀，格式 `/app/{appname}/{customPath}` 或 `/app/{appname}`，不能包含 `.` |
| `gatewaySocket` | 两者均非空时注册 | Socket 文件名，如 `app.sock`，放在应用 target 目录 |

### 13.2 WebSocket 支持

```json
{
  "myapp.chat": {
    "title": "聊天应用",
    "icon": "images/icon_{0}.png",
    "type": "iframe",
    "protocol": "",
    "gatewaySocket": "chat.sock",
    "gatewayPrefix": "/app/chat",
    "url": "/app/chat",
    "allUsers": true
  }
}
```

前端连接示例：
```javascript
const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
const wsUrl = `${wsProtocol}//${window.location.host}/app/chat/ws`;
const socket = new WebSocket(wsUrl);
```

> WebSocket 路由建议固定为网关前缀下的子路径（如 `/ws`），不要信任客户端主动上报的用户 ID。

### 13.3 登录认证

统一网关转发请求前完成登录态校验，认证通过后增加以下 Header：

| Header | 说明 | 示例 |
|--------|------|------|
| `X-Trim-Userid` | 当前登录用户 UID | `1000` |
| `X-Trim-Isadmin` | 是否管理员 | `true` / `false` |
| `X-Trim-Username` | 当前登录用户名 | `admin` |

Node.js 获取用户信息：
```javascript
function getGatewayUser(req) {
  return {
    uid: req.headers["x-trim-userid"],
    isAdmin: req.headers["x-trim-isadmin"] === "true",
    username: req.headers["x-trim-username"]
  };
}
```

> 应用仍需要自己的权限判断逻辑（数据隔离、管理员接口、高风险操作校验）。

### 13.4 不鉴权接口

公开资源、OAuth 回调等无需登录态的特殊接口：
- 只开放必要路径
- 只允许必要 HTTP 方法
- 不返回用户敏感信息
- 不提供写入/删除等高危能力

### 13.5 静态文件安全
- 路径标准化处理
- 禁止 `..` 访问上级目录
- 限制可访问目录范围
- 不暴露配置文件、密钥、数据库
- 可下载文件类型做白名单控制

---

## 14. 运行时环境与中间件

### 14.1 运行时环境

通过 `manifest` 的 `install_dep_apps` 声明依赖，系统确保安装和启动时目标环境已就绪。

| 运行时 | manifest 声明 | PATH 配置 |
|--------|---------------|-----------|
| Node.js v22 | `install_dep_apps=nodejs_v22` | `export PATH=/var/apps/nodejs_v22/target/bin:$PATH` |
| Node.js v20 | `install_dep_apps=nodejs_v20` | `export PATH=/var/apps/nodejs_v20/target/bin:$PATH` |
| Node.js v18 | `install_dep_apps=nodejs_v18` | `export PATH=/var/apps/nodejs_v18/target/bin:$PATH` |
| Python 3.12 | `install_dep_apps=python312` | `export PATH=/var/apps/python312/target/bin:$PATH` |
| Python 3.11 | `install_dep_apps=python311` | `export PATH=/var/apps/python311/target/bin:$PATH` |
| Python 3.10 | `install_dep_apps=python310` | `export PATH=/var/apps/python310/target/bin:$PATH` |
| Java 21 | `install_dep_apps=java-21-openjdk` | `export PATH=/var/apps/java-21-openjdk/target/bin:$PATH` |
| Java 17 | `install_dep_apps=java-17-openjdk` | `export PATH=/var/apps/java-17-openjdk/target/bin:$PATH` |

**Python 虚拟环境最佳实践：**
```bash
export PATH=/var/apps/python312/target/bin:$PATH
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 14.2 中间件服务

| 中间件 | manifest 声明 | 连接信息 |
|--------|---------------|----------|
| Redis | `install_dep_apps=redis` | `127.0.0.1:6379` |
| MinIO | `install_dep_apps=minio` | `127.0.0.1:9000` |
| RabbitMQ | `install_dep_apps=rabbitmq` | `127.0.0.1:5672`，默认 `guest/guest` |
| MariaDB | `install_dep_apps=mariaDB` | 即将上线 |

#### Redis 使用示例（Python）
```python
import redis

pool = redis.ConnectionPool(
    host='127.0.0.1', port=6379, db=1,
    decode_responses=True, max_connections=10
)
client = redis.Redis(connection_pool=pool)
client.lpush('my_list', 'item1', 'item2')
items = client.lrange('my_list', 0, -1)
```

#### MinIO 使用示例（Python）
```python
from minio import Minio

client = Minio(
    endpoint="127.0.0.1:9000",
    access_key="your_access_key",
    secret_key="your_secret_key",
    secure=False
)
if not client.bucket_exists("my-bucket"):
    client.make_bucket("my-bucket")
```

#### RabbitMQ 使用示例（Python）
```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="127.0.0.1", port=5672,
    virtual_host="/",
    credentials=pika.PlainCredentials("guest", "guest")
))
channel = connection.channel()
channel.queue_declare(queue="my_queue")
channel.basic_publish(exchange="", routing_key="my_queue", body="Hello")
```

---

## 15. 应用依赖关系

### 15.1 声明依赖

在 `manifest` 中使用 `install_dep_apps` 字段：

```ini
# 格式：app1>2.2.2:app2:app3
# > 表示最低版本要求
# : 分隔多个依赖
install_dep_apps = dep2:dep1
```

### 15.2 依赖检查逻辑

| 操作 | 行为 |
|------|------|
| 安装/启用 | 检查依赖是否已安装启用，未安装则自动安装，未启用则自动启用 |
| 停用/卸载 | 检查是否有其他应用依赖本应用，有则提示自动停用 |
| 更新 | 检查是否有其他应用依赖，有则在更新期间自动停用 |

### 15.3 依赖顺序

自动安装和启用的顺序**从后往前**：
```ini
# 先安装 dep1，后安装 dep2
install_dep_apps = dep2:dep1
```

### 15.4 嵌套依赖

> 应用中心仅对一层依赖进行检查，不做递归检查。

如果 A 依赖 B，B 依赖 C，则 A 需要同时声明 B 和 C：
```ini
install_dep_apps = depB:depC
```

---

## 16. Native 应用完整构建流程

### 16.1 开发 → 打包流程

1. 开发应用代码（如 Node.js + Express）
2. 编译打包到 `dist/` 目录
3. `fnpack create <appname>` 创建打包目录
4. 将编译产物复制到 `app/server/`
5. 编辑 `manifest`、`config/privilege`、`config/resource`
6. 编写 `cmd/main` 生命周期脚本
7. 配置 `app/ui/config` 入口
8. 添加 `app/ui/images/icon_64.png` 和 `icon_256.png`
9. 更新根目录 `ICON.PNG` 和 `ICON_256.PNG`
10. `fnpack build` 打包

### 16.2 集成到编译脚本

```javascript
// scripts/build-combined.js（Node.js 项目）
const packDir = path.join(root, 'fnnas.notepad')
const packServerDir = path.join(packDir, 'app', 'server');
run(`rm -rf ${packServerDir}`);
run(`mkdir ${packServerDir}`);
run(`cp -r ${outDir}/* ${packServerDir}/`);
run(`fnpack build -d ${packDir}`);
```

### 16.3 纯静态页面 Native 应用

对于无后台服务的静态页面应用，`cmd/main` 只需：
```bash
#!/bin/bash

case $1 in
start)   exit 0 ;;  # 无进程需要启动
stop)    exit 0 ;;  # 无进程需要停止
status)  exit 0 ;;  # 静态页面始终"运行中"
*)       exit 1 ;;
esac
```

> 此时的 CGI 脚本负责处理 HTTP 请求，从 `app/www/` 中读取并返回静态文件。

---

## 17. 打包与校验

### 17.1 基本打包

```bash
cd myapp
fnpack build                    # 当前目录打包
fnpack build --directory <path> # 指定目录打包
```

### 17.2 打包校验规则

| 路径 | 校验要求 |
|------|----------|
| `manifest` | 必须存在，必选字段存在 |
| `config/privilege` | 必须存在，符合 JSON 格式 |
| `config/resource` | 必须存在，符合 JSON 格式 |
| `ICON.PNG` | 必须存在 |
| `ICON_256.PNG` | 必须存在 |
| `app/` | 目录必须存在 |
| `cmd/` | 目录必须存在 |
| `wizard/` | 目录必须存在 |
| `app/{desktop_uidir}/` | 若 manifest 定义，目录必须存在 |

### 17.3 输出

打包后在当前目录生成 `{appname}.fpk` 文件。

---

## 18. 测试安装

### 方式一：install-fpk（上传后安装）

```bash
# 将 fpk 文件上传到 fnOS 设备
appcenter-cli install-fpk myapp.fpk

# 静默安装（跳过向导）
appcenter-cli install-fpk myapp.fpk --env config.env
```

环境变量文件 `config.env` 格式：
```ini
# 应用配置
wizard_admin_username=admin
wizard_admin_password=mypassword123
wizard_database_type=sqlite
wizard_app_port=8080
wizard_agree_terms=true
```

### 方式二：install-local（开发测试）

```bash
# 在应用目录中直接安装，无需打包
cd /path/to/myapp
appcenter-cli install-local
```

### 检查日志

日志位置：`/var/apps/{appname}/var/info.log`

---

## 19. 上架发布

开发者后台即将上线。当前可通过加入**应用中心开发者先锋交流群**，联系专员办理应用内测和上架。

---

## 20. 文档更新历史

| 版本 | 日期 | 主要内容 |
|------|------|----------|
| 20251216 | 2025-12-16 | manifest 新增 changelog；fnpack 更新至 1.0.4；新增搜索；优化创建应用教学案例（HelloFnosAppCenter） |
| 20251231 | 2025-12-31 | 新增 New!/Update! 徽标；arch 废弃，platform 字段替代；入口配置支持环境变量；protocol 支持空字符串（自适应）；fnpack 1.2.0（新增 Linux ARM，补全校验错误处理）；新增错误异常展示处理（$TRIM_TEMP_LOGFILE）；框架文档结构调整 |
| 20260509 | 2026-05-09 | 新增统一网关注册文档；新增登录认证文档（fnOS V1.1.3100+） |

---

## 附录：命令行速查

```bash
# === fnpack 打包 ===
fnpack create <appname>                                    # 创建 Native 项目
fnpack create <appname> --template docker                  # 创建 Docker 项目
fnpack create <appname> --without-ui true                  # 纯服务项目
fnpack build                                               # 打包
fnpack build --directory <path>                            # 指定目录打包

# === appcenter-cli 管理 ===
appcenter-cli install-fpk <file.fpk>                       # 安装 fpk
appcenter-cli install-fpk <file.fpk> --env config.env      # 静默安装
appcenter-cli install-local                                # 本地目录安装
appcenter-cli list                                         # 已安装列表
appcenter-cli start <appname>                              # 启动
appcenter-cli stop <appname>                               # 停止
appcenter-cli manual-install [enable|disable]              # 手动安装开关
appcenter-cli default-volume [number]                      # 默认存储空间
```
