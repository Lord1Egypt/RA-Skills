---
name: cn-mirror-download
description: |
  国内（中国大陆网络环境）下载任何程序、依赖、镜像、模型、SDK 时的镜像优先策略与完整配置手册。
  适用场景：pip / uv / conda 装包慢或超时、npm / pnpm / yarn install 卡住、go mod 拉不下来、cargo 编译失败、
  docker pull 超时、apt / yum 更新慢、Gradle / Maven 依赖下载失败、Android SDK / Flutter / gradle 发行包卡住、
  GitHub Release / git clone 龟速、HuggingFace 模型下不动、Playwright / Puppeteer / Electron / ChromeDriver 下载失败。
  核心原则：默认先走国内镜像 → 失败再回退官方源 → 全程可验证（校验和 + 版本一致），不改动业务产物逻辑。
  触发关键词：镜像、国内源、加速、下载慢、超时、timeout、连接失败、pip 慢、npm 慢、go proxy、goproxy、crates、apt 源、
  docker registry、GitHub 加速、ghproxy、hf-mirror、清华源、阿里源、中科大源、腾讯源、华为源、tuna、npmmirror、rsproxy。
allowed-tools: Bash(*), Read, Write, Edit
---

# 国内镜像下载（CN Mirror First）

## 行动准则（先读这 5 条）

1. **默认中国网络**：任何下载动作前，先判断有无国内镜像；有则用镜像，不要直接打官方源试运气。
2. **优先项目级、其次会话级、最后全局**：`.npmrc` / `pip.conf` 优先于 `npm config set -g` / 全局 `pip.conf`；临时任务用环境变量即可，不要污染用户全局配置。
3. **回退链固定**：主镜像失败 → 备用镜像（≥2 个厂商）→ 官方源 + 代理。每一步都要看 exit code，不要一次失败就宣称环境不支持。
4. **不降级安全性**：镜像只改"地址"，不改校验。`--trusted-host` 仅在 HTTPS 证书确实不通时使用；下载二进制必须校验 sha256 / 签名。
5. **不动业务语义**：只改下载通道。禁止为了"能下"而改 `go.mod` / `package.json` / `pom.xml` 的依赖版本、关掉 lockfile 校验、或 `--force` 覆盖已有产物（除非用户明确要求）。

## 0. 先做 30 秒连通性探测（不要盲试）

**必须探真实构件路径，不能探索引根路径。** 清华 / 阿里 / 北外等站点对非浏览器 UA 直接返回 `403`，`https://pypi.tuna.tsinghua.edu.cn/simple/` 403 **不代表镜像不可用**，用 `/simple/<包名>/` 才是有效判据。

```bash
probe() { for u in "$@"; do printf '%-58s ' "$u"; curl -sS -o /dev/null -m 8 -A "pip/24.0" -w '%{http_code} %{time_total}s\n' "$u" 2>/dev/null || echo "FAIL"; done; }

# pip：取一个必定存在的小包的索引页
probe https://pypi.tuna.tsinghua.edu.cn/simple/requests/ \
      https://mirrors.aliyun.com/pypi/simple/requests/ \
      https://mirrors.cloud.tencent.com/pypi/simple/requests/ \
      https://mirrors.huaweicloud.com/repository/pypi/simple/requests/ \
      https://mirrors.ustc.edu.cn/pypi/simple/requests/ \
      https://mirror.sjtu.edu.cn/pypi/web/simple/requests/

# 其他生态
probe https://registry.npmmirror.com/react \
      https://goproxy.cn/github.com/pkg/errors/@v/list \
      https://rsproxy.cn/index/config.json \
      https://maven.aliyun.com/repository/public/org/apache/commons/commons-lang3/maven-metadata.xml \
      https://cdn.npmmirror.com/binaries/chrome-for-testing/last-known-good-versions.json \
      https://ghfast.top/https://raw.githubusercontent.com/octocat/Hello-World/master/README
```

判读规则：
- `200` → 可用，按 `time_total` 升序排成回退链。
- `403` → 该站点拒绝当前 UA / 出口 IP（反爬），**换下一个镜像，不要加 `--trusted-host`**。
- `404` → 路径写错，不是镜像坏了。
- `FAIL` / 超时 → 本网络不可达。

实测参考（2026-10，本机 macOS 直连无代理）：npmmirror / goproxy / rsproxy / 阿里 maven / 腾讯·华为·中科大·上交 pypi = `200`；清华、阿里 pypi、北外 = `403`（UA 拦截）。所以**首选清单里必须至少有腾讯或华为做兜底**，不能只写清华一个。

## 1. 生态 → 镜像 快速决策表

| 目标 | 首选镜像 | 关键变量 / 参数 |
|---|---|---|
| Python pip | `https://pypi.tuna.tsinghua.edu.cn/simple` → 403 则 `https://mirrors.cloud.tencent.com/pypi/simple` | `-i` 或 `PIP_INDEX_URL` |
| Python uv | 同上 + `UV_DEFAULT_INDEX` | `UV_PYTHON_INSTALL_MIRROR`（装 Python 本体）|
| conda / mamba | `https://mirrors.tuna.tsinghua.edu.cn/anaconda` | `~/.condarc` channels |
| Node npm | `https://registry.npmmirror.com` | `--registry` / `.npmrc` |
| pnpm / yarn | 同上 | `.npmrc` 同源 |
| Node 二进制 / nvm | `https://npmmirror.com/mirrors/node/` | `NVM_NODEJS_ORG_MIRROR` |
| Go modules | `https://goproxy.cn,direct` | `GOPROXY` + `GOSUMDB=sum.golang.google.cn` |
| Rust cargo | `https://rsproxy.cn/index/` | `~/.cargo/config.toml` + sparse 协议 |
| Rustup 工具链 | `https://rsproxy.cn/rustup` | `RUSTUP_DIST_SERVER` |
| Java Maven | `https://maven.aliyun.com/repository/public` | `settings.xml` mirror |
| Gradle 依赖 | 同上 | `init.gradle` 或 `repositories` |
| Gradle 发行包 | `https://mirrors.cloud.tencent.com/gradle/` | `distributionUrl` |
| Android SDK/AGP | `https://maven.aliyun.com/repository/google` | `google()` 前插镜像 |
| Flutter / Dart | `https://pub.flutter-io.cn` | `PUB_HOSTED_URL` + `FLUTTER_STORAGE_BASE_URL` |
| Docker Hub | 阿里/腾讯/华为 registry-mirrors | `daemon.json` |
| apt (Debian/Ubuntu) | `https://mirrors.tuna.tsinghua.edu.cn` | `sources.list` 域名替换 |
| yum/dnf (RHEL系) | `https://mirrors.aliyun.com/centos` | repo 文件 |
| GitHub clone / Release | `https://ghfast.top/` 或 `https://gh-proxy.com/` | URL 前缀拼接 |
| HuggingFace 模型 | `https://hf-mirror.com` | `HF_ENDPOINT` |
| PyTorch wheel | `https://mirrors.aliyun.com/pytorch-wheels` | `--index-url` |
| Playwright 浏览器 | `https://npmmirror.com/mirrors/playwright/` | `PLAYWRIGHT_DOWNLOAD_HOST` |
| Puppeteer Chrome | `https://cdn.npmmirror.com/binaries/chrome-for-testing` | `PUPPETEER_DOWNLOAD_BASE_URL` |
| Electron | `https://npmmirror.com/mirrors/electron/` | `ELECTRON_MIRROR` |
| ChromeDriver | `https://npmmirror.com/mirrors/chromedriver/` | 手动落盘 |
| Python 官方安装包 | `https://mirrors.huaweicloud.com/python/` | 手动下载 |

完整命令、配置文件全文、坑位说明见 `references/ecosystems.md`。

## 2. 标准工作流

**Step 1 判型**：这是"包管理器下载"还是"裸文件下载"？
- 包管理器 → 走 §3 环境变量注入（最快、可逆）。
- 裸文件（Release / 模型 / 二进制）→ 走 §4 URL 改写。

**Step 2 选范围**：一次性任务用环境变量前缀（`FOO_MIRROR=... cmd`）；会反复跑的项目写项目级配置文件；只有用户明确要求"永久生效"才动全局配置。

**Step 3 执行并观察**：镜像失败时先看错误类型——
- `SSL: CERTIFICATE_VERIFY_FAILED` → 镜像 HTTPS 被中间设备干扰，换镜像，别急着 `--trusted-host`。
- `403 / 404` → 镜像路径变了（尤其 npmmirror 的 binaries 前缀），按 `references/troubleshoot.md` 换路径。
- `Connection timed out` → 该镜像在当前网络不可达，走回退链下一项。
- `Read timed out` 但能连上 → 提高超时 + 并发降级：`--timeout 120 --retries 5`。

**Step 4 校验**：二进制/模型必须核对大小与校验和（`sha256sum`、`shasum -a 256`）；包安装后跑一次最小 import / 版本命令验证（`python -c "import X"`、`node -e "require('X')"`、`go build ./...`）。

**Step 5 落盘记录**：在最终答复里写清"用了哪个镜像、改的是哪个配置、如何回滚"。

## 3. 环境变量注入模板（一次覆盖当前命令，无副作用）

```bash
# Python 全家桶（清华 403 时把 PIP_INDEX_URL 换成腾讯那条）
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
export PIP_EXTRA_INDEX_URL=https://mirrors.cloud.tencent.com/pypi/simple,https://mirrors.huaweicloud.com/repository/pypi/simple
export PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
export UV_DEFAULT_INDEX=$PIP_INDEX_URL
export UV_PYTHON_INSTALL_MIRROR=https://ghfast.top/https://github.com/astral-sh/python-build-standalone/releases/download

# Node 全家桶
export NPM_CONFIG_REGISTRY=https://registry.npmmirror.com
export ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
export PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright
export PUPPETEER_DOWNLOAD_BASE_URL=https://cdn.npmmirror.com/binaries/chrome-for-testing
export SASS_BINARY_SITE=https://npmmirror.com/mirrors/node-sass
export NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node

# Go / Rust
export GOPROXY=https://goproxy.cn,https://goproxy.io,direct
export GOSUMDB=sum.golang.google.cn
export RUSTUP_DIST_SERVER=https://rsproxy.cn
export RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup

# 移动端 / 模型
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
export HF_ENDPOINT=https://hf-mirror.com
```

需要跨会话复用时，把上面整块放进项目的 `.envrc`（direnv）或 `scripts/mirror-env.sh`，由用户决定是否 source，不要写进 `~/.zshrc`。

## 4. 裸文件下载：URL 改写与回退

```bash
# GitHub Release / raw / archive：前缀代理，失败自动轮换
fetch_gh() {
  local url="$1" out="${2:-$(basename "$url")}"
  for p in https://ghfast.top/ https://gh-proxy.com/ https://ghproxy.net/ ""; do
    echo ">> ${p:-direct}$url"
    curl -fL --retry 3 --connect-timeout 10 -m 600 "$p$url" -o "$out.part" && mv "$out.part" "$out" && { echo "OK: $out"; return 0; }
    rm -f "$out.part"
  done
  echo "ALL MIRRORS FAILED: $url" >&2; return 1
}

# HuggingFace 模型（单文件 + 大文件断点续传）
HF_ENDPOINT=https://hf-mirror.com hf download --resume-download ORG/MODEL --local-dir ./MODEL
# 或裸 URL：https://hf-mirror.com/ORG/MODEL/resolve/main/FILE
curl -fL -C - --retry 5 https://hf-mirror.com/ORG/MODEL/resolve/main/FILE -o FILE

# clone（浅克隆优先，代理失败再直连）
git clone --depth 1 https://ghfast.top/https://github.com/OWNER/REPO.git
```

## 5. 硬约束清单

- `uv` / `pip` 混用同一 `PIP_INDEX_URL` 会互相干扰：跑 uv 时显式带 `--default-index`，别只依赖全局 env。
- 不要为了装包成功而 `--no-verify`、`NODE_TLS_REJECT_UNAUTHORIZED=0`、`GOPRIVATE=*`、`GONOSUMDB=*`、`--insecure-registry`——这些会永久削弱后续所有安全校验。
- Docker daemon 镜像需要重启 daemon；容器内构建建议用 `--build-arg` 传镜像地址，避免改宿主 daemon。
- apt 换源前 `cp /etc/apt/sources.list{,.bak}`，换完 `apt-get update` 必须成功再继续。
- 镜像同步有延迟：镜像缺新版本时优先回退官方源，不要在镜像上找 `--pre` / 刚发布的版本死磕。
- 企业内网/代理环境（如百度内网）先确认已存在 HTTP(S) proxy 变量，镜像域名可能需走代理：`HTTPS_PROXY=... curl` 先探一次。

## 6. 自检

装完跑这些，任一失败说明镜像没真正生效：

```bash
pip config list | grep -i index            # 或 pip -v install X 看 "Looking in indexes"
npm config get registry
go env GOPROXY GOSUMDB
cargo -Vv | grep -i "config" ; cat ~/.cargo/config.toml
docker info | grep -A3 "Registry Mirrors"
```

## 交叉引用

- 全量配置文件与厂商镜像清单：`references/ecosystems.md`
- 报错字典与换路径规则：`references/troubleshoot.md`
- 需要判断"下载的二进制是否可信"时：`../supply-chain-security/SKILL.md`
