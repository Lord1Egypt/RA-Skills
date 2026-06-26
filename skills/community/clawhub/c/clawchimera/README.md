# ClawChimera — OpenClaw 融合怪测试 Skill

[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Upstream ECS](https://img.shields.io/badge/upstream-oneclickvirt%2Fecs-orange.svg)](https://github.com/oneclickvirt/ecs)
[![Platform](https://img.shields.io/badge/platform-clawhub.ai-blue.svg)](https://clawhub.ai)

ClawChimera 是 [clawhub.ai](https://clawhub.ai) 平台的**融合怪测试 (ECS) Skill**。  
本 Skill **无需编译、无额外依赖**——运行时自动从 [oneclickvirt/ecs](https://github.com/oneclickvirt/ecs) 的 GitHub Releases 下载对应平台的预编译二进制，直接执行。

---

## 文件说明

| 文件 | 说明 |
|---|---|
| `skill.json` | clawhub.ai 技能元信息（名称、版本、参数描述等） |
| `run.sh` | 主入口：自动下载 ECS 二进制并执行 |
| `pack.sh` | 一键生成 `clawchimera.zip` 供上传 |
| `README.md` | 本文档 |

---

## 快速打包上传

```bash
bash pack.sh
# 生成 clawchimera.zip，上传到 https://clawhub.ai/upload
```

---

## 本地直接使用

```bash
chmod +x run.sh

# 全套测试（中文，菜单关闭）
./run.sh

# 英文输出，3个测速节点
./run.sh -l en -spnum 3

# 只跑流媒体解锁 + IP质量（关闭其他测试）
./run.sh -basic=false -cpu=false -memory=false -disk=false \
         -backtrace=false -nt3=false -speed=false -email=false

# 使用 geekbench 做 CPU 单线程测试
./run.sh -cpum geekbench -cput single

# 三网路由测全国节点，双栈
./run.sh -nt3loc ALL -nt3t both

# 查看 goecs 原始帮助
./run.sh --help

# 强制使用国内 CNB 镜像下载
CN=true ./run.sh
```

---

## 测试类别

| 类别 | 说明 |
|---|---|
| 系统信息 | CPU型号/核心/缓存、内存、磁盘、OS、内核、虚拟化、NAT 类型 |
| CPU 基准 | sysbench / geekbench，单线程+多线程得分及等级 |
| 内存基准 | STREAM 带宽（读/写/复制/Triad），DDR 代际检测 |
| 磁盘 IO  | fio / dd：4K 随机读写 IOPS，1M 顺序吞吐 |
| 流媒体解锁 | Netflix、Disney+、ChatGPT、YouTube Premium 等 20+ 平台 |
| IP 质量  | 18 个数据库（scamalytics、abuseipdb 等），代理/机房检测 |
| 邮件端口 | SMTP 25/465/587，POP3 110/995，IMAP 143/993 |
| 回程路由 | 电信/联通/移动 BGP 上行 traceroute |
| 三网路由 | NT3：广州/上海/北京/成都，IPv4/IPv6 |
| 延迟测试 | TG 数据中心、国内外主流网站延迟 |
| 多节点测速 | 三网（CMCC/CU/CT）+ 国际节点，上传/下载 |

---

## goecs 完整参数透传

`run.sh` 在 `-menu=false` 基础上将所有参数原样透传给 `goecs`：

### 功能开关（`-xxx=false` 可禁用）

| 参数 | 默认 | 说明 |
|---|---|---|
| `-basic` | true | 系统基础信息 |
| `-cpu` | true | CPU 基准测试 |
| `-memory` | true | 内存基准测试 |
| `-disk` | true | 磁盘 IO 测试 |
| `-ut` | true | 流媒体解锁检测 |
| `-security` | true | IP 安全质量检测 |
| `-email` | true | 邮件端口检测 |
| `-backtrace` | true | 回程路由（en 模式下强制 false）|
| `-nt3` | true | 三网详细路由（en 模式下强制 false）|
| `-speed` | true | 多节点测速 |
| `-ping` | false | 延迟/PING 测试 |
| `-tgdc` | false | Telegram DC 测试 |
| `-web` | false | 主流网站延迟测试 |
| `-upload` | true | 上传结果到公共粘贴板 |
| `-log` | false | 在当前目录写日志 |

### 方法参数

| 参数（短/长） | 默认 | 可选值 |
|---|---|---|
| `-cpum` / `-cpu-method` | sysbench | sysbench, geekbench, winsat |
| `-cput` / `-cpu-thread` | multi | multi, single |
| `-memorym` / `-memory-method` | stream | stream, sysbench, dd, winsat, auto |
| `-diskm` / `-disk-method` | fio | fio, dd, winsat |
| `-diskp` | — | 自定义磁盘测试路径 |
| `-diskmc` | true | 多路径检测，`-diskmc=false` 禁用 |
| `-l` / `-lang` | zh | zh, en |
| `-spnum` | 2 | 每运营商测速节点数（整数）|
| `-nt3loc` / `-nt3-location` | GZ | GZ, SH, BJ, CD, ALL |
| `-nt3t` / `-nt3-type` | ipv4 | ipv4, ipv6, both |

---

## 下载加速逻辑

首次运行时自动选择最快下载源（完全参照上游 [goecs.sh](https://github.com/oneclickvirt/ecs/blob/main/goecs.sh)）：

1. **检测 IP 归属**：若为国内 IP（或设 `CN=true`），使用 **CNB.cool 国内镜像**
2. **CDN 探测**：依次测试 `cdn0.spiritlhl.top` / `cdn3.spiritlhl.net` / `cdn1.spiritlhl.net` / `cdn2.spiritlhl.net`，选用第一个可用的作为 GitHub Releases 的代理前缀
3. **直连 GitHub**：CDN 全不可用时降级为直连
4. **下载失败自动换源**：主源失败后自动切换备用源重试

二进制缓存于 `~/.cache/clawchimera/<version>/goecs`，之后运行直接使用缓存。

---

## 运行要求

- **OS**：Linux / macOS / FreeBSD
- **架构**：amd64, arm64, arm, 386, mips, mipsle, s390x, riscv64
- **依赖**：`curl` 或 `wget` + `unzip`（或 `python3`）
- **权限**：默认普通用户（root 时仅警告，不阻断）
- **网络**：首次运行需访问下载源，后续使用本地缓存

---

## 上游项目

- [oneclickvirt/ecs](https://github.com/oneclickvirt/ecs) — 融合怪测试主程序（GPL-3.0）

---

## 许可证

GPL-3.0 — 与上游 ECS 项目保持一致。

[![Go Version](https://img.shields.io/badge/go-1.22+-blue.svg)](https://golang.org)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Upstream ECS](https://img.shields.io/badge/upstream-oneclickvirt%2Fecs-orange.svg)](https://github.com/oneclickvirt/ecs)

ClawChimera 是 [OpenClaw](https://github.com/oneclickvirt) 平台的**融合怪测试 (ECS) Skill**，  
封装了 [oneclickvirt/ecs](https://github.com/oneclickvirt/ecs) 全套 VPS 性能与网络测试能力，  
并通过标准 Skill 接口上架到 OpenClaw 市场。

---

## 功能特性

| 类别 ID | 名称 | 说明 |
|---|---|---|
| `sysinfo` | 基础系统信息 | CPU型号/核心数/缓存、内存、磁盘、OS、内核、虚拟化类型、NAT 类型 |
| `cpu` | CPU 性能基准 | sysbench / geekbench / winsat，单线程+多线程得分及等级评定 |
| `memory` | 内存基准 | STREAM 带宽（读/写/复制/Triad）、DDR 代际检测 |
| `disk` | 磁盘 IO 基准 | fio / dd：4K 随机读写 IOPS、1M 顺序读写吞吐 |
| `streaming` | 流媒体解锁检测 | Netflix、Disney+、ChatGPT、YouTube Premium、Spotify 等 20+ 平台 |
| `ipquality` | IP 质量检测 | ipinfo、scamalytics、abuseipdb 等 18 个数据库，风险评分与代理检测 |
| `email` | 邮件端口检测 | SMTP(25/465/587)、POP3(110/995)、IMAP(143/993) 连通性 |
| `backtrace` | 回程路由追踪 | 四大运营商（电信/联通/移动）BGP 上行 traceroute |
| `routing` | 三网详细路由 | NT3：广州/上海/北京/成都，IPv4/IPv6 路由追踪 |
| `ping` | 延迟测试 | TG 数据中心、国内外主流网站延迟（ms）|
| `speedtest` | 多节点测速 | 三网（CMCC/CU/CT）+ 国际节点，上传/下载速度 |

---

## 快速开始

### 安装

```bash
# 从源码编译
git clone https://github.com/oneclickvirt/ClawChimera
cd ClawChimera
make build

# 或使用 go install
go install github.com/oneclickvirt/ClawChimera@latest
```

### 运行全套测试

```bash
# 运行所有测试，中文输出（默认）
./clawchimera run

# 英文输出
./clawchimera run --lang en

# JSON 格式输出并保存到文件
./clawchimera run --format json --output result.json
```

### 选择性运行

```bash
# 只运行系统信息 + 流媒体解锁
./clawchimera run --categories sysinfo,streaming

# 只运行网络类测试
./clawchimera run --categories speedtest,ping,backtrace,routing

# IP 质量 + 邮件端口
./clawchimera run --categories ipquality,email
```

### 自定义测试方法

```bash
# 使用 geekbench 做 CPU 测试
./clawchimera run --extra cpu_method=geekbench

# 使用 fio 测磁盘，指定测试路径
./clawchimera run --extra disk_method=fio,disk_path=/data

# 三网路由测北京节点，只测 IPv4
./clawchimera run --categories routing --extra nt3_location=BJ,nt3_type=ipv4
```

---

## 作为 OpenClaw Skill 部署

### HTTP 服务模式

```bash
# 默认监听 :8080
./clawchimera serve

# 自定义端口
./clawchimera serve --addr :9090
```

OpenClaw 平台通过以下标准端点与 Skill 交互：

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/meta` | 技能元信息（名称/版本/类别列表） |
| `POST` | `/run` | 执行测试，请求体为 JSON `Options` |
| `GET` | `/health` | 健康检查 |
| `GET` | `/manifest.json` | OpenClaw 市场清单 |

#### POST /run 示例

```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["sysinfo", "cpu", "streaming"],
    "language": "zh",
    "timeout": 300,
    "speed_nodes": 2
  }'
```

响应结构：

```json
{
  "success": true,
  "result": {
    "skill_name": "融合怪测试 (ECS)",
    "version": "1.0.0",
    "start_time": "2026-03-17T12:00:00Z",
    "end_time":   "2026-03-17T12:08:32Z",
    "duration_seconds": 512.3,
    "data": {
      "sysinfo": { "cpu_model": "Intel Xeon E5-2680 v4", "..." : "..." },
      "cpu":     { "method": "sysbench", "single_score": 3200 },
      "streaming": { "ipv4_results": ["..."] }
    },
    "raw_output": "...",
    "errors": []
  }
}
```

### 生成市场清单

```bash
./clawchimera manifest > manifest.json
```

---

## 作为 Go 库使用

```go
package main

import (
    "context"
    "fmt"
    "os"
    "time"

    "github.com/oneclickvirt/ClawChimera/output"
    "github.com/oneclickvirt/ClawChimera/skill"
    skillecs "github.com/oneclickvirt/ClawChimera/skill/ecs"
)

func main() {
    s := skillecs.New()

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Minute)
    defer cancel()

    result, err := s.Run(ctx, skill.Options{
        Categories: []skill.Category{
            skill.CategorySysInfo,
            skill.CategoryCPU,
            skill.CategoryStreaming,
        },
        Language:   "zh",
        SpeedNodes: 2,
    })
    if err != nil {
        panic(err)
    }

    output.New(output.FormatText).Format(os.Stdout, result)
    fmt.Printf("共检测 %d 项错误\n", len(result.Errors))
}
```

---

## 架构说明

```
ClawChimera/
├── main.go                    # CLI 入口
├── cmd/root.go                # cobra 命令（run / serve / meta / manifest / list）
│
├── skill/
│   ├── interface.go           # Skill 接口 + Options/Result/Metadata 定义
│   ├── registry.go            # 全局 Skill 注册中心
│   └── ecs/
│       ├── skill.go           # ECSSkill — 实现 skill.Skill 接口
│       ├── config.go          # skill.Options → ECS api.Config 映射
│       ├── executor.go        # ECS 执行器 + 输出文本解析
│       └── types.go           # 各测试类别的结构化结果类型
│
├── openclaw/
│   ├── adapter.go             # HTTP REST 适配器（供 OpenClaw 平台调用）
│   └── manifest.go            # OpenClaw 市场清单 (manifest.json) 生成
│
└── output/
    └── formatter.go           # text / JSON 格式化输出
```

---

## skill.Options 参数参考

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `categories` | `[]string` | `["all"]` | 要运行的测试类别 |
| `language` | `string` | `"zh"` | 输出语言：`zh` / `en` / `ja` |
| `timeout` | `int` | `600` | 最大执行时长（秒） |
| `speed_nodes` | `int` | `2` | 每运营商测速节点数 |
| `extra.cpu_method` | `string` | `"sysbench"` | CPU 测试工具 |
| `extra.cpu_thread` | `string` | `"both"` | `single` / `multi` |
| `extra.memory_method` | `string` | `"stream"` | 内存测试工具 |
| `extra.disk_method` | `string` | `"fio"` | 磁盘测试工具 |
| `extra.disk_path` | `string` | — | 自定义磁盘测试路径 |
| `extra.nt3_location` | `string` | `"ALL"` | 三网路由目标：`GZ`/`SH`/`BJ`/`CD`/`ALL` |
| `extra.nt3_type` | `string` | `"both"` | `ipv4` / `ipv6` / `both` |

---

## 构建与测试

```bash
# 安装依赖
go mod tidy

# 构建
make build

# 运行单元测试
make test

# 代码检查
make lint

# 构建多平台二进制
make release
```

---

## 上游项目

本技能依赖并感谢以下开源项目：

- **[oneclickvirt/ecs](https://github.com/oneclickvirt/ecs)** — 融合怪测试主程序
- **[oneclickvirt/basics](https://github.com/oneclickvirt/basics)** — 系统信息采集
- **[oneclickvirt/cputest](https://github.com/oneclickvirt/cputest)** — CPU 基准测试
- **[oneclickvirt/memorytest](https://github.com/oneclickvirt/memorytest)** — 内存带宽测试
- **[oneclickvirt/disktest](https://github.com/oneclickvirt/disktest)** — 磁盘 IO 测试
- **[oneclickvirt/UnlockTests](https://github.com/oneclickvirt/UnlockTests)** — 流媒体解锁检测
- **[oneclickvirt/security](https://github.com/oneclickvirt/security)** — IP 质量检测
- **[oneclickvirt/backtrace](https://github.com/oneclickvirt/backtrace)** — 回程路由追踪
- **[oneclickvirt/speedtest](https://github.com/oneclickvirt/speedtest)** — 网络测速
- **[oneclickvirt/nt3](https://github.com/oneclickvirt/nt3)** — 三网详细路由

---

## 许可证

ClawChimera 遵循 [GNU General Public License v3.0](LICENSE) 发布，  
与其依赖的 ECS 上游项目保持一致。
