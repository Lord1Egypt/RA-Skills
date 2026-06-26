#!/usr/bin/env bash
# =============================================================================
# ClawChimera — clawhub.ai 融合怪测试 (ECS) Skill 入口脚本
# 上游项目: https://github.com/oneclickvirt/ecs
#
# 本脚本自动从 GitHub Releases 下载 goecs 预编译二进制并执行。
# 二进制缓存于 ~/.cache/clawchimera/<version>/ 目录，避免重复下载。
# 下载逻辑完全参照上游 goecs.sh 的 CDN 加速方案。
#
# 用法（所有参数直接透传给 goecs）:
#   ./run.sh                            # 全套测试，中文，菜单关闭
#   ./run.sh -l en                      # 英文输出
#   ./run.sh -basic -cpu -disk          # 只测基础/CPU/磁盘
#   ./run.sh -cpu=false -memory=false   # 禁用 CPU 和内存测试
#   ./run.sh -cpum geekbench            # 使用 geekbench 做 CPU 测试
#   ./run.sh -spnum 3 -l zh             # 每运营商3节点测速
#   ./run.sh --help                     # 查看 goecs 原始帮助
#
# 环境变量:
#   CN=true   强制使用国内 CNB 镜像加速（不自动检测 IP）
#   CN=false  强制使用直连/CDN，跳过 CN 检测
# =============================================================================
set -euo pipefail

# ── 常量 ───────────────────────────────────────────────────────────────────────
readonly GITHUB_REPO="oneclickvirt/ecs"
readonly BINARY_NAME="goecs"
readonly CACHE_DIR="${HOME}/.cache/clawchimera"
readonly GITHUB_API="https://api.github.com/repos/${GITHUB_REPO}/releases/latest"
# 上游 goecs.sh 使用的 CDN 前缀列表（同顺序）
readonly CDN_LIST="https://cdn0.spiritlhl.top/ http://cdn3.spiritlhl.net/ http://cdn1.spiritlhl.net/ http://cdn2.spiritlhl.net/"

# ── 颜色输出 ───────────────────────────────────────────────────────────────────
_red()    { printf '\033[31m%s\033[0m\n' "$*" >&2; }
_green()  { printf '\033[32m%s\033[0m\n' "$*" >&2; }
_yellow() { printf '\033[33m%s\033[0m\n' "$*" >&2; }
_cyan()   { printf '\033[36m%s\033[0m\n' "$*" >&2; }
_info()   { _cyan   "[ClawChimera] $*"; }
_ok()     { _green  "[ClawChimera] $*"; }
_warn()   { _yellow "[ClawChimera] $*"; }
_fatal()  { _red    "[ClawChimera] $*"; exit 1; }

# ── HTTP 工具（curl 优先，回退 wget）──────────────────────────────────────────
_has_curl() { command -v curl &>/dev/null; }
_has_wget() { command -v wget &>/dev/null; }

http_get() {
    # 下载到文件，失败返回非零
    local url="$1" dest="$2"
    if _has_curl; then
        curl -fsSL --retry 3 --retry-delay 2 --connect-timeout 10 --max-time 120 \
             --progress-bar -o "$dest" "$url" 2>&1
    elif _has_wget; then
        wget -q --show-progress --tries=3 --timeout=10 -O "$dest" "$url"
    else
        _fatal "未找到 curl 或 wget，请先安装其中之一"
    fi
}

http_text() {
    # 返回 URL 纯文本内容，失败返回空
    local url="$1"
    if _has_curl; then
        curl -sf --max-time 8 --retry 2 "$url" 2>/dev/null || true
    elif _has_wget; then
        wget -qO- --timeout=8 "$url" 2>/dev/null || true
    fi
}

# ── OS / 架构检测（完全对齐上游 goecs.sh）────────────────────────────────────
detect_os() {
    local os
    os=$(uname -s 2>/dev/null || echo "unknown")
    case "$os" in
        Linux|linux|LINUX)       echo "linux"   ;;
        Darwin|darwin)           echo "darwin"  ;;
        FreeBSD|freebsd)         echo "freebsd" ;;
        *) _fatal "不支持的操作系统: $os（仅支持 linux / darwin / freebsd）" ;;
    esac
}

detect_arch() {
    local arch
    arch=$(uname -m 2>/dev/null || echo "unknown")
    case "$arch" in
        x86_64|amd64|x64)            echo "amd64"   ;;
        i386|i686)                    echo "386"     ;;
        aarch64|arm64|armv8|armv8l)   echo "arm64"   ;;
        arm|armv7l)                   echo "arm"     ;;
        mipsle)                       echo "mipsle"  ;;
        mips)                         echo "mips"    ;;
        s390x)                        echo "s390x"   ;;
        riscv64)                      echo "riscv64" ;;
        *)
            _warn "未识别的架构 $arch，回退使用 amd64"
            echo "amd64"
            ;;
    esac
}

# ── CDN 可用性检测（参照上游 check_cdn / check_cdn_file）────────────────────
CDN_OK=""   # 全局变量，成功的 CDN 前缀

check_cdn() {
    local cdn_url
    for cdn_url in $CDN_LIST; do
        # 使用上游相同的测试 URL
        if http_text "${cdn_url}https://raw.githubusercontent.com/spiritLHLS/ecs/main/back/test" \
                | grep -q "success" 2>/dev/null; then
            CDN_OK="$cdn_url"
            _ok "CDN 可用: ${cdn_url}"
            return 0
        fi
        sleep 0.3
    done
    CDN_OK=""
    _warn "所有 CDN 均不可用，使用直连 GitHub"
    return 1
}

# ── 中国 IP 检测 ──────────────────────────────────────────────────────────────
is_china_network() {
    # 已由环境变量强制指定时直接返回
    if [[ "${CN:-}" == "true" ]];  then return 0; fi
    if [[ "${CN:-}" == "false" ]]; then return 1; fi
    # 检测 IP 归属（6秒超时，失败视为非国内）
    if http_text "https://ipapi.co/json" | grep -q '"country_code":"CN"' 2>/dev/null; then
        return 0
    fi
    # 备用检测
    if http_text "http://ip-api.com/json/?fields=countryCode" | grep -q '"countryCode":"CN"' 2>/dev/null; then
        return 0
    fi
    return 1
}

# ── 获取最新版本号 ─────────────────────────────────────────────────────────────
get_latest_version() {
    local ver
    # 优先 GitHub API
    ver=$(http_text "$GITHUB_API" \
          | grep '"tag_name"' | head -1 \
          | sed 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' \
          | sed 's/^v//')
    if [[ -n "$ver" ]]; then echo "$ver"; return 0; fi

    # 回退：CNB API（国内可达）
    ver=$(http_text "https://cnb.cool/api/v1/repos/oneclickvirt/ecs/releases/latest" 2>/dev/null \
          | grep '"tag_name"' | head -1 \
          | sed 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' \
          | sed 's/^v//')
    if [[ -n "$ver" ]]; then echo "$ver"; return 0; fi

    _fatal "无法获取 ECS 最新版本。请检查网络是否可访问 api.github.com"
}

# ── 解压 zip（unzip 或 Python 回退）──────────────────────────────────────────
extract_zip() {
    local zip_file="$1" dest_dir="$2"
    if command -v unzip &>/dev/null; then
        unzip -o -q "$zip_file" -d "$dest_dir"
    elif command -v python3 &>/dev/null; then
        python3 -c "
import zipfile, sys
with zipfile.ZipFile('${zip_file}') as z:
    z.extractall('${dest_dir}')
"
    elif command -v python &>/dev/null; then
        python -c "
import zipfile
with zipfile.ZipFile('${zip_file}') as z:
    z.extractall('${dest_dir}')
"
    else
        _fatal "未找到 unzip / python 以解压文件，请安装: apt install unzip"
    fi
}

# ── 下载并缓存 goecs 二进制 ───────────────────────────────────────────────────
ensure_binary() {
    local os arch version zip_name bin_dir bin_path
    os=$(detect_os)
    arch=$(detect_arch)
    version=$(get_latest_version)
    zip_name="${BINARY_NAME}_${os}_${arch}.zip"
    bin_dir="${CACHE_DIR}/${version}"
    bin_path="${bin_dir}/${BINARY_NAME}"

    # 命中缓存直接返回
    if [[ -x "$bin_path" ]]; then
        _info "使用缓存 ECS v${version} (${os}/${arch})"
        echo "$bin_path"
        return 0
    fi

    mkdir -p "$bin_dir"

    # ── 构造下载地址（参照上游 CDN 逻辑）──────────────────────────────────
    local base_url=""
    local gh_release_base="https://github.com/${GITHUB_REPO}/releases/download/v${version}"

    local use_cn=false
    _info "检测网络环境..."
    if is_china_network; then
        use_cn=true
        _info "检测到国内网络（或 CN=true），优先使用 CNB 镜像"
    fi

    if [[ "$use_cn" == "true" ]]; then
        # 国内：CNB.cool 镜像（与上游 CN=true 分支一致）
        base_url="https://cnb.cool/oneclickvirt/ecs/-/releases/download/v${version}"
    else
        # 国外：尝试 CDN 加速前缀
        _info "检测 CDN 可用性..."
        if check_cdn 2>/dev/null && [[ -n "$CDN_OK" ]]; then
            base_url="${CDN_OK}${gh_release_base}"
        else
            base_url="$gh_release_base"
        fi
    fi

    # ── 下载 ────────────────────────────────────────────────────────────────
    local download_url="${base_url}/${zip_name}"
    local tmp_zip
    tmp_zip=$(mktemp "${bin_dir}/${BINARY_NAME}_XXXXXX.zip")

    _info "下载 ECS v${version} (${os}/${arch})..."
    _info "地址: ${download_url}"

    if ! http_get "$download_url" "$tmp_zip" 2>/dev/null; then
        rm -f "$tmp_zip"
        # 下载失败时做一次全量回退尝试
        _warn "主地址下载失败，尝试备用下载源..."

        if [[ "$use_cn" == "true" ]]; then
            # CNB 失败 → 尝试 CDN → 直连 GitHub
            if check_cdn 2>/dev/null && [[ -n "$CDN_OK" ]]; then
                download_url="${CDN_OK}${gh_release_base}/${zip_name}"
            else
                download_url="${gh_release_base}/${zip_name}"
            fi
        else
            # CDN 失败 → 直连 GitHub
            download_url="${gh_release_base}/${zip_name}"
        fi

        _info "备用地址: ${download_url}"
        tmp_zip=$(mktemp "${bin_dir}/${BINARY_NAME}_XXXXXX.zip")
        http_get "$download_url" "$tmp_zip" \
            || { rm -f "$tmp_zip"; _fatal "所有下载源均失败，请检查网络连接"; }
    fi

    # ── 解压 ─────────────────────────────────────────────────────────────────
    _info "正在解压..."
    extract_zip "$tmp_zip" "$bin_dir"
    rm -f "$tmp_zip"

    # 兼容 zip 内二进制可能命名为 goecs 或 goecs_linux_amd64
    if [[ ! -f "$bin_path" ]]; then
        # 尝试找到任意 goecs* 可执行文件
        local alt
        alt=$(find "$bin_dir" -maxdepth 1 -name "${BINARY_NAME}*" -not -name "*.zip" | head -1)
        if [[ -n "$alt" ]]; then
            mv "$alt" "$bin_path"
        else
            _fatal "解压后未找到 ${BINARY_NAME} 二进制，zip 内容可能不符合预期"
        fi
    fi

    chmod +x "$bin_path"
    _ok "ECS v${version} 就绪: ${bin_path}"
    echo "$bin_path"
}

# ── 主入口 ─────────────────────────────────────────────────────────────────────
main() {
    # 非 root 建议（clawhub.ai 默认以普通用户运行，不强制阻断）
    if [[ "$(id -u)" -eq 0 ]]; then
        _warn "当前以 root 运行，建议使用普通用户以遵循最小权限原则"
    fi

    local binary
    binary=$(ensure_binary)

    _info "启动 ECS 测试..."
    # -menu=false : 禁用交互式菜单（无人值守/CI 模式）
    # "$@"        : 透传所有用户参数（支持全部 goecs 选项，见下方说明）
    "$binary" -menu=false "$@" || true

    # ── 测试完成：引导用户使用结果文件 ────────────────────────────────────────
    local result_file; result_file="$(pwd)/goecs.txt"
    echo ""
    if [[ -f "$result_file" ]]; then
        local size; size=$(du -sh "$result_file" 2>/dev/null | cut -f1)
        _info "测试完成！结果已保存至:"
        echo "        $result_file  (${size})"
        echo ""
        echo -e "  \033[36m💡 快速查看:\033[0m"
        echo "        cat \"$result_file\""
        echo ""
        local script_dir; script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        if [[ -f "${script_dir}/analyze.sh" ]]; then
            echo -e "  \033[36m🔍 AI 分析（提取优缺点）:\033[0m"
            echo "        bash ${script_dir}/analyze.sh -f \"$result_file\""
            echo "        bash ${script_dir}/analyze.sh -f \"$result_file\" --copy      # 复制到剪贴板"
            echo "        bash ${script_dir}/analyze.sh -f \"$result_file\" --call-ai   # 调用本地 AI 工具"
            echo "        bash ${script_dir}/analyze.sh -f \"$result_file\" --compare other.txt  # 与另一台对比"
        fi
    else
        _warn "未找到结果文件 goecs.txt（测试可能未完整运行）"
    fi
}

# =============================================================================
# goecs 全参数说明（透传，直接跟在 ./run.sh 后面即可）:
#
#   基础开关（-xxx=false 可禁用）:
#     -basic          系统基础信息     (默认 true)
#     -cpu            CPU 基准测试     (默认 true)
#     -memory         内存基准测试     (默认 true)
#     -disk           磁盘 IO 测试     (默认 true)
#     -ut             流媒体解锁检测   (默认 true)
#     -security       IP 安全质量检测  (默认 true)
#     -email          邮件端口检测     (默认 true)
#     -backtrace      回程路由追踪     (默认 true; en 模式/Windows 下强制 false)
#     -nt3            三网详细路由     (默认 true; en 模式/Windows 下强制 false)
#     -speed          多节点测速       (默认 true)
#     -ping           延迟测试         (默认 false)
#     -tgdc           Telegram DC 测试 (默认 false)
#     -web            主流网站延迟测试  (默认 false)
#     -upload         上传结果         (默认 true; 本脚本传入 -upload=false 可禁用)
#     -log            在当前目录记录日志
#
#   方法参数:
#     -cpum / -cpu-method        sysbench(默认) | geekbench | winsat
#     -cput / -cpu-thread        multi(默认) | single
#     -memorym / -memory-method  stream(默认) | sysbench | dd | winsat | auto
#     -diskm / -disk-method      fio(默认) | dd | winsat
#     -diskp                     自定义磁盘测试路径, 如 -diskp /data
#     -diskmc                    多路径检测, 禁用: -diskmc=false
#
#   语言与网络:
#     -l / -lang          zh(默认) | en
#     -spnum              每运营商测速节点数 (默认 2)
#     -nt3loc / -nt3-location  GZ(默认) | SH | BJ | CD | ALL
#     -nt3t / -nt3-type        ipv4(默认) | ipv6 | both
#
# 示例:
#   ./run.sh -l en -spnum 3
#   ./run.sh -cpu=false -memory=false -disk=false -ut -security
#   ./run.sh -cpum geekbench -cput single
#   ./run.sh -diskm dd -diskp /tmp
#   ./run.sh -nt3loc ALL -nt3t both
# =============================================================================

main "$@"
