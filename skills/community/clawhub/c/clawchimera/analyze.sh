#!/usr/bin/env bash
# =============================================================================
# analyze.sh — ClawChimera ECS 测试结果 AI 分析工具
#
# 用法:
#   bash analyze.sh                           # 生成分析提示词（打印到 stdout）
#   bash analyze.sh -f myresult.txt           # 指定结果文件（默认 ./goecs.txt）
#   bash analyze.sh --call-ai                 # 自动调用本地 AI 工具
#   bash analyze.sh --copy                    # 复制提示词到剪贴板
#   bash analyze.sh --compare b.txt           # 与另一个结果对比
#   bash analyze.sh -f a.txt --compare b.txt  # 对比两个指定文件
# =============================================================================
set -euo pipefail

# ── 解析参数 ──────────────────────────────────────────────────────────────────
RESULT_FILE="./goecs.txt"
COMPARE_FILE=""
CALL_AI=false
COPY_CLIP=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--file)    RESULT_FILE="$2";  shift 2 ;;
        --compare)    COMPARE_FILE="$2"; shift 2 ;;
        --call-ai)    CALL_AI=true;      shift ;;
        --copy)       COPY_CLIP=true;    shift ;;
        -h|--help)
            sed -n 's/^# \?//p' "$0" | head -12
            exit 0
            ;;
        *) echo "未知参数: $1  (使用 -h 查看帮助)" >&2; exit 1 ;;
    esac
done

# ── 工具函数 ──────────────────────────────────────────────────────────────────

# 去除 ANSI 颜色/控制码
strip_ansi() {
    sed 's/\x1b\[[0-9;]*[mGKHF]//g; s/\x1b\[[0-9;]*[A-Za-z]//g; s/\x1b(B//g'
}

check_file() {
    local f="$1"
    if [[ ! -f "$f" ]]; then
        echo -e "\033[31m[analyze]\033[0m 未找到结果文件: $f" >&2
        echo -e "\033[33m[analyze]\033[0m 请先运行 bash run.sh 执行 ECS 测试，结果将保存到 goecs.txt" >&2
        exit 1
    fi
    if [[ ! -s "$f" ]]; then
        echo -e "\033[31m[analyze]\033[0m 结果文件为空: $f" >&2
        exit 1
    fi
}

# ── 预提取关键指标（本地 grep，减轻 AI 负担）────────────────────────────────
extract_metrics() {
    local raw="$1"
    local clean; clean=$(echo "$raw" | strip_ansi)

    # ── 基础信息 ──
    local cpu_model cpu_cores cpu_cache ram disk os_name kernel virt tcp_cc uptime location
    cpu_model=$(echo "$clean" | grep -iE 'CPU Model\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    cpu_cores=$(echo "$clean" | grep -iE 'CPU Cores?\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    cpu_cache=$(echo "$clean" | grep -iE 'CPU Cache\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    ram=$(echo  "$clean" | grep -iE 'Total (Mem|RAM|Memory)\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    disk=$(echo "$clean" | grep -iE 'Total Disk\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    os_name=$(echo  "$clean" | grep -iE '^OS\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    kernel=$(echo   "$clean" | grep -iE 'Kernel\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    virt=$(echo     "$clean" | grep -iE 'Virtuali[sz]ation\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    tcp_cc=$(echo   "$clean" | grep -iE 'TCP CC\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    uptime=$(echo   "$clean" | grep -iE '(System Uptime|运行时间)\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)
    location=$(echo "$clean" | grep -iE '(Location|地区|机房|Region)\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs)

    # ── CPU 基准 ──
    # sysbench 行格式: "events/s  单核: 3827 pts" 或 "Single: 3827 pts"
    local sysbench_single sysbench_multi gb5_single gb5_multi
    sysbench_single=$(echo "$clean" | grep -iE 'sysbench' | grep -oP '(?i)(单核|single)[^0-9]*\K[0-9]+(?=\s*pts)' | head -1 || true)
    sysbench_multi=$(echo  "$clean" | grep -iE 'sysbench' | grep -oP '(?i)(多核|multi)[^0-9]*\K[0-9]+(?=\s*pts)' | head -1 || true)
    gb5_single=$(echo "$clean" | grep -iP 'geekbench.{0,30}(single|单核)' | grep -oP '\d{3,5}' | head -1 || true)
    gb5_multi=$(echo  "$clean" | grep -iP 'geekbench.{0,30}(multi|多核)' | grep -oP '\d{3,5}' | head -1 || true)

    # ── 内存 STREAM ──
    local mem_copy mem_scale mem_add mem_triad
    mem_copy=$(echo  "$clean" | grep -iP '^\s*Copy\s*[:|：]'  | grep -oP '[\d.]+\s*(GB|MB)/s' | head -1 || true)
    mem_scale=$(echo "$clean" | grep -iP '^\s*Scale\s*[:|：]' | grep -oP '[\d.]+\s*(GB|MB)/s' | head -1 || true)
    mem_add=$(echo   "$clean" | grep -iP '^\s*Add\s*[:|：]'   | grep -oP '[\d.]+\s*(GB|MB)/s' | head -1 || true)
    mem_triad=$(echo "$clean" | grep -iP '^\s*Triad\s*[:|：]' | grep -oP '[\d.]+\s*(GB|MB)/s' | head -1 || true)

    # ── 磁盘 fio ──
    local disk_4k_rread disk_4k_rwrite disk_1m_read disk_1m_write
    # ECS fio 输出标准行: "  Read  4K (Q= 1,T= 1): xxxxxx IOPS, xxx MB/s"
    disk_4k_rread=$(echo  "$clean" | grep -iP 'Read\s+4[Kk]'  | grep -oP '\d+\s*IOPS' | head -1 || true)
    disk_4k_rwrite=$(echo "$clean" | grep -iP 'Write\s+4[Kk]' | grep -oP '\d+\s*IOPS' | head -1 || true)
    disk_1m_read=$(echo   "$clean" | grep -iP 'Read\s+1[Mm]'  | grep -oP '[\d.]+\s*(GB|MB)/s' | head -1 || true)
    disk_1m_write=$(echo  "$clean" | grep -iP 'Write\s+1[Mm]' | grep -oP '[\d.]+\s*(GB|MB)/s' | head -1 || true)

    # ── 流媒体 ──
    local netflix disney youtube chatgpt tiktok spotify primev
    netflix=$(echo  "$clean" | grep -iP '^Netflix\s*[:|：]'          | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    disney=$(echo   "$clean" | grep -iP '^Disney\+?\s*[:|：]'        | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    youtube=$(echo  "$clean" | grep -iP '^YouTube Premium\s*[:|：]'  | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    chatgpt=$(echo  "$clean" | grep -iP '^(ChatGPT|OpenAI)\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    tiktok=$(echo   "$clean" | grep -iP '^TikTok\s*[:|：]'           | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    spotify=$(echo  "$clean" | grep -iP '^Spotify\s*[:|：]'          | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    primev=$(echo   "$clean" | grep -iP '^(Amazon Prime|Prime Video)\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)

    # ── IP 质量 ──
    local fraud_score ip_type abuse_score as_info ip_addr
    fraud_score=$(echo "$clean" | grep -iP '(欺诈评分|Fraud Score|Scamalytics)' | grep -oP '\d+' | head -1 || true)
    ip_type=$(echo     "$clean" | grep -iP '(IP\s*类型|IP\s*Type)\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    abuse_score=$(echo "$clean" | grep -iP 'AbuseIPDB' | grep -oP '\d+%' | head -1 || true)
    as_info=$(echo     "$clean" | grep -iP '^AS\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)
    ip_addr=$(echo     "$clean" | grep -iP '(IPv4|查询 IP|IP Address)\s*[:|：]' | head -1 | sed 's/.*[:|：]\s*//' | xargs || true)

    # ── 端口 ──
    local port_25 port_465 port_587
    port_25=$(echo  "$clean" | grep -P '^\s*25\s*[|│]' | grep -oiP '(开放|关闭|open|closed|blocked)' | head -1 || true)
    port_465=$(echo "$clean" | grep -P '^\s*465\s*[|│]'| grep -oiP '(开放|关闭|open|closed|blocked)' | head -1 || true)
    port_587=$(echo "$clean" | grep -P '^\s*587\s*[|│]'| grep -oiP '(开放|关闭|open|closed|blocked)' | head -1 || true)

    # ── 三网延迟（NT3 汇总行）──
    # 典型格式: "电信CN  |  xxx.xx ms  |"
    local lat_ct lat_cu lat_cm
    lat_ct=$(echo "$clean" | grep -iP '(电信|ChinaTelecom|\bCT\b)' | grep -oP '\d+\.\d+\s*ms' | head -1 || true)
    lat_cu=$(echo "$clean" | grep -iP '(联通|ChinaUnicom|\bCU\b|Unicom)' | grep -oP '\d+\.\d+\s*ms' | head -1 || true)
    lat_cm=$(echo "$clean" | grep -iP '(移动|ChinaMobile|\bCM\b|Mobile)' | grep -oP '\d+\.\d+\s*ms' | head -1 || true)

    # ── 网络测速（iperf3 / speedtest 峰值）──
    local max_dl max_ul
    # 取所有 Mbps 数值中最大两个分别作下载/上传参考
    local all_speeds
    all_speeds=$(echo "$clean" | grep -oP '[\d.]+\s*Mbps' | grep -oP '[\d.]+' | sort -rn)
    max_dl=$(echo "$all_speeds" | sed -n '1p' || true)
    max_ul=$(echo "$all_speeds" | sed -n '2p' || true)

    # ── 回程路由关键词（取 traceroute 段中出现的最具代表性词）──
    local route_ct route_cu route_cm
    # CT 段：电信/ChinaTelecom 后的路由跳信息
    route_ct=$(echo "$clean" | grep -iP '(CN2 GIA|CN2 GT|CN2|as4134|as9929|4134|163|CMIN2|CMI|AS4837|NTT|GTT|Cogent|PCCW|zayo)' \
        | grep -iP '(电信|ChinaTelecom|CT|59\.43\.)' | grep -ioP '(CN2 GIA|CN2 GT|CN2|163|CMIN2|NTT|GTT|Cogent|PCCW|直连)' | head -1 || true)
    route_cu=$(echo "$clean" | grep -iP '(AS4837|AS9929|9929|4837|163|NTT|GTT|PCCW)' \
        | grep -iP '(联通|ChinaUnicom|CU|Unicom)' | grep -ioP '(AS9929|AS4837|4837|9929|163|直连|NTT|GTT|PCCW)' | head -1 || true)
    route_cm=$(echo "$clean" | grep -iP '(CMI|CMIN2|AS58453|58453|NTT|GTT)' \
        | grep -iP '(移动|ChinaMobile|CM|Mobile)' | grep -ioP '(CMIN2|CMI|AS58453|直连|NTT|GTT)' | head -1 || true)

    # ── 输出格式化摘要 ──
    cat <<EOF
### 📋 预提取指标摘要（本地解析，供 AI 快速定位，以完整原始结果中的数值为准）

#### 基础配置
| 项目 | 数值 |
|---|---|
| IP 地址 | ${ip_addr:-未检测到} |
| 地区/机房 | ${location:-见原始结果} |
| CPU 型号 | ${cpu_model:-未识别} |
| CPU 核心/频率 | ${cpu_cores:-未识别} |
| CPU 缓存 | ${cpu_cache:-未识别} |
| 内存 | ${ram:-未识别} |
| 磁盘 | ${disk:-未识别} |
| 系统 | ${os_name:-未识别} |
| 内核 | ${kernel:-未识别} |
| 虚拟化 | ${virt:-未识别} |
| TCP 拥塞控制 | ${tcp_cc:-未识别} |
| 运行时间 | ${uptime:-未识别} |

#### CPU 基准
| 测试 | 结果 | 档位参考 |
|---|---|---|
| sysbench 单核 | ${sysbench_single:+${sysbench_single} pts}${sysbench_single:-未检测到} | ≥5000旗舰 / ≥4000高端 / ≥3000中高 / ≥2000主流 / ≥1000入门 / <1000低端 |
| sysbench 多核 | ${sysbench_multi:+${sysbench_multi} pts}${sysbench_multi:-未检测到} | 与单核×核心数对比，差距大说明超售 |
| Geekbench5 单核 | ${gb5_single:-未检测到} | ≥1500高端 / ≥1000主流 / <800低端 |
| Geekbench5 多核 | ${gb5_multi:-未检测到} | 参考上游排行榜 |

#### 内存 STREAM 带宽
| 测试 | 带宽 | 档位参考 |
|---|---|---|
| Copy  | ${mem_copy:-未检测到} | >40 GB/s优 / 20-40 GB/s良(DDR4) / <20 GB/s差(DDR3/单通道) |
| Scale | ${mem_scale:-未检测到} | 同 Copy |
| Add   | ${mem_add:-未检测到} | 同 Copy |
| Triad | ${mem_triad:-未检测到} | **最重要** — >50 GB/s DDR5 / 20-50 GB/s DDR4 / <20 GB/s DDR3 |

#### 磁盘 IO（fio）
| 测试 | 结果 | 档位参考 |
|---|---|---|
| 4K 随机读 IOPS  | ${disk_4k_rread:-未检测到} | >200K NVMe高端 / >50K NVMe普通 / >10K SATA SSD / <5K HDD或网络存储 |
| 4K 随机写 IOPS  | ${disk_4k_rwrite:-未检测到} | 同上（写通常低于读） |
| 1M 顺序读吞吐   | ${disk_1m_read:-未检测到} | >2 GB/s NVMe高端 / >500 MB/s SSD主流 / <200 MB/s 可能为共享存储 |
| 1M 顺序写吞吐   | ${disk_1m_write:-未检测到} | 同上 |

#### 流媒体解锁
| 平台 | 状态 | 说明 |
|---|---|---|
| Netflix  | ${netflix:-未检测到} | Full=原生地区IP(最优) / Self Only=仅自制 / Yes(DNS)=DNS代理(低价值) / No=封锁 |
| Disney+  | ${disney:-未检测到} | Yes=原生解锁高价值 |
| YouTube Premium | ${youtube:-未检测到} | 地区标注即为IP归属地 |
| ChatGPT / OpenAI | ${chatgpt:-未检测到} | Yes=高价值，国内严封 |
| TikTok   | ${tiktok:-未检测到} | |
| Spotify  | ${spotify:-未检测到} | |
| Prime Video | ${primev:-未检测到} | |

#### IP 质量
| 指标 | 数值 | 档位参考 |
|---|---|---|
| 欺诈评分 (Scamalytics) | ${fraud_score:-未检测到} | <20 优秀 / 20-60 中等 / >60 高风险（可能被服务拒绝） |
| IP 类型 | ${ip_type:-未检测到} | residential=住宅IP(稀有高价值) / datacenter=数据中心(正常) |
| AbuseIPDB 举报 | ${abuse_score:-未检测到} | <5% 干净 / >20% 历史较差 |
| ASN 信息 | ${as_info:-未检测到} | |

#### 邮件端口
| 端口 | 状态 | 说明 |
|---|---|---|
| 25  (SMTP 原始) | ${port_25:-未检测到} | 开放=可自建邮件服务器（大多数 VPS 已封锁） |
| 465 (SMTPS)    | ${port_465:-未检测到} | 开放=可发加密邮件 |
| 587 (STARTTLS) | ${port_587:-未检测到} | 开放=可发加密邮件 |

#### 三网延迟（本机 ping → 中国各运营商）
| 运营商 | 延迟 | 档位参考 |
|---|---|---|
| 电信 CT | ${lat_ct:-未检测到} | <80ms极优(港/日) / <150ms良(新/美西) / <200ms一般(美东/欧) / >200ms差 |
| 联通 CU | ${lat_cu:-未检测到} | 同上 |
| 移动 CM | ${lat_cm:-未检测到} | 同上 |

#### 网络测速（峰值参考，以原始测速节点明细为准）
| 指标 | 峰值 |
|---|---|
| 最快下载速度 | ${max_dl:+${max_dl} Mbps}${max_dl:-未检测到} |
| 次快速度（上传参考） | ${max_ul:+${max_ul} Mbps}${max_ul:-未检测到} |

#### 回程路由质量（关键词）
| 运营商 | 识别线路 | 优劣参考 |
|---|---|---|
| 电信 CT | ${route_ct:-见原始 traceroute} | CN2 GIA > CN2 GT > 163 > 绕行(NTT/GTT) |
| 联通 CU | ${route_cu:-见原始 traceroute} | AS9929 > AS4837直连 > 163 > 绕行 |
| 移动 CM | ${route_cm:-见原始 traceroute} | CMIN2 > CMI直连 > 绕行 |

EOF
}

# ── 构建单文件分析提示词 ─────────────────────────────────────────────────────
build_prompt_single() {
    local raw="$1"
    local clean; clean=$(echo "$raw" | strip_ansi)
    local metrics; metrics=$(extract_metrics "$raw")

cat <<PROMPT_EOF
你是一位资深 VPS 服务器评测专家，精通中国大陆网络环境、服务器硬件性能基准（sysbench/STREAM/fio）和运营商路由质量（CN2/4837/CMI 等）。

以下是 ECS 融合怪测试（https://github.com/oneclickvirt/ecs）的测试结果，分为两部分：
① 【预提取指标摘要】— 本地脚本提前解析的关键数值和档位标注（可能有少量偏差）
② 【完整原始结果】— 去除 ANSI 控制码后的完整测试输出（各模块以空白行或━/─分割）

**如摘要数值与原始结果有出入，以原始结果为准。**

${metrics}

========== 【完整原始结果】==========

${clean}

========== 【分析要求】==========

注意事项：
- 流媒体中 "Yes (US)" 指 IP 归属地为 US 的原生解锁，优于 "Yes (DNS)"（DNS 代理解锁）
- 回程路由请仔细看 traceroute 每跳的 ASN，判断是否经过国际绕行（NTT/GTT/PCCW/Zayo 等为绕行信号）
- 若某项测试结果缺失（如未启用 -cpu=false），请标注"未测试"，不要猜测
- 评分请严格按数值档位打分，不要主观偏高

请按以下格式输出分析报告：

## 📌 基本信息
（2-3行：服务商推测/机房位置/IP归属/虚拟化类型/核心硬件配置）

## ✅ 优点
（逐条列出，格式：**标题** — 具体数值 + 档位 + 对实际用途的意义；至少覆盖性能、网络、解锁三个维度）

## ❌ 不足与风险
（逐条列出，格式：⚠️中等 或 🔴严重 + **标题** — 说明影响；无不足也需说明"暂无明显不足"）

## 📊 各项评分（满分10分）
| 项目 | 得分 | 关键依据（填写实际数值和对应档位） |
|---|---|---|
| CPU 性能 | x/10 | sysbench 单核 xxx pts → 第x档 |
| 内存带宽 | x/10 | STREAM Triad xxx GB/s → DDRx水平 |
| 磁盘 IO  | x/10 | 4K读 xxx IOPS → xxx类型存储 |
| 网络速度 | x/10 | 峰值下载 xxx Mbps |
| 三网延迟 | x/10 | CT/CU/CM 均值约 xxxms |
| 流媒体解锁 | x/10 | Netflix: xxx / ChatGPT: xxx |
| IP 质量  | x/10 | 欺诈分 xx / IP类型 xxx |
| 回程路由 | x/10 | CT: xxx / CU: xxx / CM: xxx |
| **综合** | **x/10** | |

## 🎯 推荐用途（Top 3，按优先级排序）
1. **xxx** — 理由：（结合最优指标说明）
2. **xxx** — 理由：
3. **xxx** — 理由：

## 💡 综合建议
（3-5行：总体定位，适合哪类用户，性价比评价，主要注意事项）
PROMPT_EOF
}

# ── 构建双文件对比提示词 ─────────────────────────────────────────────────────
build_prompt_compare() {
    local raw_a="$1"
    local raw_b="$2"
    local name_a="${3:-VPS-A}"
    local name_b="${4:-VPS-B}"
    local clean_a; clean_a=$(echo "$raw_a" | strip_ansi)
    local clean_b; clean_b=$(echo "$raw_b" | strip_ansi)
    local metrics_a; metrics_a=$(extract_metrics "$raw_a")
    local metrics_b; metrics_b=$(extract_metrics "$raw_b")

cat <<PROMPT_EOF
你是一位资深 VPS 服务器评测专家，擅长横向对比分析。

以下是两台 VPS 的 ECS 融合怪测试结果（已去除 ANSI 控制码），请进行横向对比。
每台结果均包含预提取摘要（本地解析，以便快速定位）和完整原始结果。

=================== 【${name_a} 指标摘要】===================

${metrics_a}

=================== 【${name_b} 指标摘要】===================

${metrics_b}

=================== 【${name_a} 完整原始结果】===================

${clean_a}

=================== 【${name_b} 完整原始结果】===================

${clean_b}

========== 【对比分析要求】==========

请按以下格式输出横向对比报告：

## 📊 核心指标横向对比
| 指标 | ${name_a} | ${name_b} | 胜出 |
|---|---|---|---|
| CPU sysbench 单核 (pts) | | | |
| 内存 STREAM Triad | | | |
| 磁盘 4K 随机读 IOPS | | | |
| 磁盘 1M 顺序读吞吐 | | | |
| 峰值下载速度 (Mbps) | | | |
| 电信 CT 延迟 | | | |
| 联通 CU 延迟 | | | |
| 移动 CM 延迟 | | | |
| 电信回程路由 | | | |
| 联通回程路由 | | | |
| 移动回程路由 | | | |
| Netflix 解锁 | | | |
| ChatGPT 可用 | | | |
| IP 欺诈评分 | | | |
| IP 类型 | | | |

## 🏆 各维度胜出分析
- **CPU / 内存 / 磁盘性能**：谁更强，差距有多大？
- **网络速度**：谁的上下行更好？
- **三网延迟与路由质量**：谁的中国访问体验更好，原因是什么？
- **流媒体与解锁能力**：谁更适合翻墙/流媒体节点？
- **IP 纯净度**：谁的 IP 历史更干净，被封锁风险更低？

## 📌 ${name_a} 独特优势
（${name_b} 不具备或明显劣于 ${name_a} 的地方）

## 📌 ${name_b} 独特优势
（${name_a} 不具备或明显劣于 ${name_b} 的地方）

## 🎯 场景选购建议
| 使用场景 | 推荐 | 原因 |
|---|---|---|
| 科学上网 / 代理节点 | | |
| 流媒体解锁 | | |
| 建站 / 低延迟服务 | | |
| 大流量下载 / 存储 | | |
| 计算密集型任务 | | |

## 💡 总结
（2-3行：综合价值哪台更高，分别适合什么类型用户）
PROMPT_EOF
}

# ── 主逻辑 ────────────────────────────────────────────────────────────────────
check_file "$RESULT_FILE"
RAW_A=$(cat "$RESULT_FILE")

if [[ -n "$COMPARE_FILE" ]]; then
    check_file "$COMPARE_FILE"
    RAW_B=$(cat "$COMPARE_FILE")
    name_a=$(basename "$RESULT_FILE" .txt)
    name_b=$(basename "$COMPARE_FILE" .txt)
    PROMPT=$(build_prompt_compare "$RAW_A" "$RAW_B" "$name_a" "$name_b")
else
    PROMPT=$(build_prompt_single "$RAW_A")
fi

# ── 输出处理 ──────────────────────────────────────────────────────────────────

if [[ "$COPY_CLIP" == "true" ]]; then
    if command -v xclip &>/dev/null; then
        echo "$PROMPT" | xclip -selection clipboard
        echo -e "\033[32m[analyze]\033[0m 提示词已复制到剪贴板（xclip）" >&2
    elif command -v xsel &>/dev/null; then
        echo "$PROMPT" | xsel --clipboard --input
        echo -e "\033[32m[analyze]\033[0m 提示词已复制到剪贴板（xsel）" >&2
    elif command -v pbcopy &>/dev/null; then
        echo "$PROMPT" | pbcopy
        echo -e "\033[32m[analyze]\033[0m 提示词已复制到剪贴板（pbcopy）" >&2
    else
        echo -e "\033[33m[analyze]\033[0m 未找到剪贴板工具（xclip/xsel/pbcopy），直接打印" >&2
        echo "$PROMPT"
    fi
    exit 0
fi

if [[ "$CALL_AI" == "true" ]]; then
    if command -v llm &>/dev/null; then
        echo -e "\033[36m[analyze]\033[0m 使用 llm 分析..." >&2
        echo "$PROMPT" | llm
    elif command -v aichat &>/dev/null; then
        echo -e "\033[36m[analyze]\033[0m 使用 aichat 分析..." >&2
        echo "$PROMPT" | aichat
    elif command -v ollama &>/dev/null; then
        MODEL="${OLLAMA_MODEL:-llama3}"
        echo -e "\033[36m[analyze]\033[0m 使用 ollama ($MODEL) 分析..." >&2
        echo "$PROMPT" | ollama run "$MODEL"
    else
        echo -e "\033[33m[analyze]\033[0m 未找到本地 AI 工具（llm / aichat / ollama）" >&2
        echo -e "\033[33m[analyze]\033[0m 已打印提示词，请手动粘贴到 AI 对话：" >&2
        echo ""
        echo "$PROMPT"
    fi
    exit 0
fi

# 默认：打印提示词
echo "$PROMPT"
echo "" >&2
if [[ -n "$COMPARE_FILE" ]]; then
    echo -e "\033[36m[analyze]\033[0m 对比分析提示词已生成（$(basename "$RESULT_FILE") vs $(basename "$COMPARE_FILE")）" >&2
else
    echo -e "\033[36m[analyze]\033[0m 分析提示词已生成。" >&2
fi
echo -e "\033[36m[analyze]\033[0m 💡 将上方内容粘贴到 ChatGPT / Claude / Gemini / Kimi 等 AI 对话中即可获得分析报告。" >&2
echo -e "\033[36m[analyze]\033[0m    --copy              直接复制到剪贴板" >&2
echo -e "\033[36m[analyze]\033[0m    --call-ai           自动调用本地 llm/aichat/ollama" >&2
[[ -z "$COMPARE_FILE" ]] && \
echo -e "\033[36m[analyze]\033[0m    --compare other.txt 与另一台 VPS 结果对比" >&2
