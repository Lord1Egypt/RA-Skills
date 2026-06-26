---
slug: clawchimera-ecs
displayName: "ClawChimera · 融合怪测试 ECS"
license: MIT-0
version: "1.0.0"
author: oneclickvirt
homepage: https://github.com/oneclickvirt/ClawChimera
upstream: https://github.com/oneclickvirt/ecs
tags:
  - vps
  - benchmark
  - network
  - streaming
  - china
  - ecs
  - 融合怪
  - backtrace
  - ipquality
  - speedtest
---

# ClawChimera · 融合怪测试 ECS

基于 [oneclickvirt/ecs](https://github.com/oneclickvirt/ecs) 的 VPS 全方位性能与网络测试 Skill。  
**无需编译、无额外依赖**——运行时自动下载对应平台预编译二进制，支持 CDN/国内镜像加速。

## 功能覆盖

| 类别 | 说明 |
|---|---|
| 系统信息 | CPU 型号/核心/缓存、内存、磁盘、OS、内核、虚拟化、NAT 类型 |
| CPU 基准 | sysbench / geekbench 单/多线程得分，6 档性能等级评定 |
| 内存基准 | STREAM 带宽（读/写/复制/Triad），DDR3/4/5 代际检测 |
| 磁盘 IO  | fio / dd：4K 随机读写 IOPS，1M 顺序吞吐 |
| 流媒体解锁 | Netflix、Disney+、ChatGPT、YouTube Premium 等 20+ 平台 |
| IP 质量  | 18 个数据库（scamalytics、abuseipdb 等）、代理/机房检测 |
| 邮件端口 | SMTP 25/465/587，POP3 110/995，IMAP 143/993 连通性 |
| 回程路由 | 电信/联通/移动 BGP 上行 traceroute |
| 三网路由 | NT3：广州/上海/北京/成都，IPv4/IPv6 |
| 延迟测试 | TG 数据中心、国内外主流网站延迟 |
| 多节点测速| 三网（CMCC/CU/CT）+ 国际节点，上传/下载 |

## 文件说明

| 文件 | 说明 |
|---|---|
| `run.sh` | 主入口：自动下载 ECS 二进制并运行，测试后输出结果文件路径 |
| `analyze.sh` | 结果分析：读取 `goecs.txt` 并生成 AI 可直接处理的结构化分析提示 |
| `skill.json` | 技能元信息与参数描述 |
| `SKILL.md` | 本文件 |

## 使用方式

```bash
# 全套测试（中文，菜单关闭，自动保存 goecs.txt）
bash run.sh

# 英文输出 + 3节点测速
bash run.sh -l en -spnum 3

# 测试完成后 AI 分析结果
bash analyze.sh                   # 生成提示词（粘贴到 AI 对话）
bash analyze.sh --call-ai         # 自动调用本地 AI 工具（需配置）

# 强制国内 CDN 加速
CN=true bash run.sh
```

## 运行要求

- **OS**：Linux / macOS / FreeBSD
- **架构**：amd64, arm64, arm, 386, mips, mipsle, s390x, riscv64
- **依赖**：`curl` 或 `wget` + `unzip`（或 `python3`）
- **权限**：普通用户即可（非 root）

## 参数全览

所有参数直接透传给 `goecs`：

```
-basic / -cpu / -memory / -disk / -ut / -security / -email
-backtrace / -nt3 / -speed / -ping / -tgdc / -web / -upload / -log

-l zh|en                         输出语言
-cpum sysbench|geekbench|winsat  CPU 工具
-cput multi|single               CPU 线程模式
-memorym stream|sysbench|dd|...  内存工具
-diskm fio|dd|winsat             磁盘工具
-diskp <path>                    磁盘测试路径
-spnum <N>                       每运营商测速节点数
-nt3loc GZ|SH|BJ|CD|ALL          三网路由位置
-nt3t ipv4|ipv6|both             三网路由协议
```

## 结果文件

测试完成后在**当前目录**生成 `goecs.txt`（纯文本，去除 ANSI 颜色码）。  
运行 `analyze.sh` 可基于该文件生成 AI 分析提示词，提取优缺点。

---

*本 Skill 遵循 [MIT-0](https://opensource.org/licenses/MIT-0) 许可发布；上游 ECS 工具遵循 GPL-3.0。*
