# 各生态镜像配置全文

> 所有片段默认「项目级优先」。标注 `[GLOBAL]` 的才动全局配置，执行前先备份。

## 1. Python

### pip（项目级 `pip.conf` / 全局 `~/.config/pip/pip.conf`）
```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
extra-index-url =
    https://mirrors.aliyun.com/pypi/simple/
    https://mirrors.cloud.tencent.com/pypi/simple/
timeout = 60
retries = 5
[install]
trusted-host =
    pypi.tuna.tsinghua.edu.cn
    mirrors.aliyun.com
    mirrors.cloud.tencent.com
```
命令行等价：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PKG`
备选：`https://mirrors.cloud.tencent.com/pypi/simple`、`https://mirrors.huaweicloud.com/repository/pypi/simple`、`https://mirrors.ustc.edu.cn/pypi/simple`、`https://mirror.sjtu.edu.cn/pypi/web/simple`

> 实测提醒：清华、阿里、北外的 pip 索引对非浏览器 UA / 部分出口 IP 返回 `403`（反爬）。pip 自身通常能通，但 `curl` 探测会看到 403 —— 不要把 curl 的 403 当成"镜像不可用"，直接用 `pip -v install --dry-run X | grep 'Looking in indexes'` 验证。若 pip 也 403，切腾讯 / 华为 / 中科大。

### uv
```bash
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PKG     # 单次
export UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple     # 会话
# uv 自己装 Python 解释器（走 python-build-standalone 的 GitHub Release）
export UV_PYTHON_INSTALL_MIRROR=https://ghfast.top/https://github.com/astral-sh/python-build-standalone/releases/download
```
`pyproject.toml` 里写死源：
```toml
[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

### conda / mamba（`~/.condarc`）[GLOBAL]
```yaml
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```
换完必须 `conda clean -i` 清索引缓存。

### PyTorch wheel（CUDA 版专用索引）
```bash
pip install torch torchvision --index-url https://mirrors.aliyun.com/pytorch-wheels/cu121
# 备选：https://mirror.sjtu.edu.cn/pytorch-wheels/cu121
# 官方源（回退）：https://download.pytorch.org/whl/cu121
```

## 2. Node / 前端

### npm / pnpm / yarn（项目级 `.npmrc`）
```ini
registry=https://registry.npmmirror.com
electron_mirror=https://npmmirror.com/mirrors/electron/
electron_builder_binaries_mirror=https://npmmirror.com/mirrors/electron-builder-binaries/
sass_binary_site=https://npmmirror.com/mirrors/node-sass
sharp_binary_host=https://npmmirror.com/mirrors/sharp
sharp_libvips_binary_host=https://npmmirror.com/mirrors/sharp-libvips
puppeteer_download_base_url=https://cdn.npmmirror.com/binaries/chrome-for-testing
playwright_download_host=https://cdn.npmmirror.com/binaries/playwright
node_sqlite3_binary_host_mirror=https://npmmirror.com/mirrors/
prisma_engines_mirror=https://npmmirror.com/mirrors/prisma
```
命令：`npm i --registry=https://registry.npmmirror.com`、`pnpm i --registry=...`、`yarn config set registry ...`（yarn 1）

### Node 版本管理
```bash
export NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node          # nvm
export FNM_NODE_DIST_MIRROR=https://npmmirror.com/mirrors/node           # fnm
export N_NODE_MIRROR=https://npmmirror.com/mirrors/node                  # n
```
`nvm install 20` 卡在 `nodejs.org` 时基本就是这个变量没设。

### Playwright / Puppeteer 浏览器二进制
```bash
PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright npx playwright install chromium
# 若 404：改用 https://npmmirror.com/mirrors/playwright （老路径，部分版本仍在）
PUPPETEER_DOWNLOAD_BASE_URL=https://cdn.npmmirror.com/binaries/chrome-for-testing npx puppeteer browsers install chrome
```

### Electron
```bash
export ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
export ELECTRON_CUSTOM_DIR="{{ version }}"
```
缓存已有损坏包时：删 `~/Library/Caches/electron` / `~/.cache/electron` 再装。

## 3. Go

```bash
go env -w GOPROXY=https://goproxy.cn,https://goproxy.io,https://mirrors.aliyun.com/goproxy/,direct
go env -w GOSUMDB=sum.golang.google.cn
go env -w GOFLAGS=-mod=mod
```
- 私有仓库混合：`GOPRIVATE=git.corp.example.com/*` + `GONOSUMDB`（不要设 `GONOSUMDB=*`）。
- 校验和数据库国内镜像只有 `sum.golang.google.cn`；它不可达时用 `GONOSUMCHECK` 是错解，正确做法是 `GOFLAGS=-mod=mod GONOSUMDB=<仅该模块>` 或临时 `GOSUMDB=off` 并记录风险。
- `direct` 放最后：只在镜像缺版本（新 tag、私有 fork）时兜底。

## 4. Rust

`~/.cargo/config.toml` [GLOBAL]
```toml
[source.crates-io]
replace-with = "rsproxy-sparse"

[source.rsproxy-sparse]
registry = "sparse+https://rsproxy.cn/index/"

[registries.rsproxy]
index = "https://rsproxy.cn/crates.io-index"

[net]
git-fetch-with-cli = true
```
```bash
export RUSTUP_DIST_SERVER=https://rsproxy.cn
export RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup
```
备选：中科大 `sparse+https://mirrors.ustc.edu.cn/crates.io-index/`、字节 `sparse+https://rsproxy.cn/index/`、清华 `sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/`。
注意：`replace-with` 会绕过 crates.io 签名链，仅 `rsproxy` 这类可信镜像可用。

## 5. Java / JVM

### Maven `~/.m2/settings.xml` [GLOBAL]
```xml
<mirrors>
  <mirror>
    <id>aliyun</id>
    <name>aliyun public</name>
    <url>https://maven.aliyun.com/repository/public</url>
    <mirrorOf>central</mirrorOf>
  </mirror>
  <mirror>
    <id>aliyun-google</id>
    <url>https://maven.aliyun.com/repository/google</url>
    <mirrorOf>google</mirrorOf>
  </mirror>
</mirrors>
```
备选：`https://mirrors.huaweicloud.com/repository/maven/`、`https://mirrors.cloud.tencent.com/nexus/repository/maven-public/`

### Gradle：依赖镜像 `init.gradle`（放 `~/.gradle/init.gradle`）
```groovy
allprojects {
  buildscript {
    repositories {
      maven { url 'https://maven.aliyun.com/repository/google' }
      maven { url 'https://maven.aliyun.com/repository/public' }
      maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
    }
  }
  repositories {
    maven { url 'https://maven.aliyun.com/repository/google' }
    maven { url 'https://maven.aliyun.com/repository/public' }
  }
}
```

### Gradle 发行包本身（`gradle/wrapper/gradle-wrapper.properties`）
```properties
distributionUrl=https\://mirrors.cloud.tencent.com/gradle/gradle-8.7-bin.zip
```
备选：`https://mirrors.aliyun.com/macports/distfiles/gradle/gradle-8.7-bin.zip`、`https://downloads.gradle.org/distributions/gradle-8.7-bin.zip`（官方，回退）。

## 6. Android / 移动端

- `settings.gradle` 里 `google()` / `mavenCentral()` 之前插阿里云 `google`、`public` 仓库（见 §5）。
- Android SDK / build-tools 下载卡住：`~/.android/repositories.cfg` 无用，真正做镜像要走 SDK Manager 的代理，或手动用 `dl.google.com` 的国内可达性探测；`sdkmanager --list` 前设 `HTTPS_PROXY`。
  ```bash
  probe https://dl.google.com/android/repository/repository2-3.xml
  probe https://mirrors.cloud.tencent.com/AndroidSDK/
  ```
- Flutter / Dart：
  ```bash
  export PUB_HOSTED_URL=https://pub.flutter-io.cn
  export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
  ```
- Gradle 依赖 + AGP 都走阿里云 `google`/`public` 后，`android` 工程首次 sync 时间通常降 5–10 倍。

## 7. 容器

`/etc/docker/daemon.json` [GLOBAL，需 `systemctl restart docker`]
```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com",
    "https://mirror.ccs.tencentyun.com",
    "https://hub-mirror.c.163.com"
  ],
  "max-concurrent-downloads": 10
}
```
- 国内厂商公共 registry 大多已收紧，实际可用性以 `probe https://<mirror>/v2/` 返回 `200` 为准。
- 单次拉取不想改 daemon：`docker pull docker.m.daocloud.io/library/nginx:1.27` 然后 `tag` 回原名。
- K8s：`imagePullPolicy` + 私有 harbor 同步；Helm chart 仓库镜像 `https://mirrors.huaweicloud.com/helm/`。

## 8. Linux 包管理

### Debian / Ubuntu（`/etc/apt/sources.list.d/*.sources` 或 `sources.list`）[GLOBAL]
```bash
sudo cp /etc/apt/sources.list{,.bak-$(date +%F)}
sudo sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g; s|http://security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g; s|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sudo apt-get update
```
备选：`mirrors.aliyun.com`、`mirrors.ustc.edu.cn`、`mirrors.huaweicloud.com`、`mirrors.cloud.tencent.com`

### RHEL / CentOS / Rocky
```bash
sudo sed -i 's|^mirrorlist=|#mirrorlist=|; s|^#baseurl=http://mirror.centos.org|baseurl=https://mirrors.aliyun.com|' /etc/yum.repos.d/*.repo
sudo yum makecache
```

## 9. GitHub / HuggingFace

```bash
# 代理前缀（可用性随时间变化，逐个探）
for p in https://ghfast.top/ https://gh-proxy.com/ https://ghproxy.net/ https://gh.llkk.cc/; do probe "${p}https://raw.githubusercontent.com/octocat/Hello-World/master/README"; done

# git 全局改写（只在需要时开，用完 unset）
git config --global url."https://ghfast.top/https://github.com/".insteadOf "https://github.com/"
# 回滚
git config --global --unset url."https://ghfast.top/https://github.com/".insteadOf

# HuggingFace
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_ENABLE_HF_TRANSFER=1        # 装 hf_transfer 后启用
pip install -U hf_transfer huggingface_hub
hf download ORG/MODEL --local-dir ./MODEL
```
`git clone` 大仓：`--depth 1 --single-branch`，必要时 `--filter=blob:none` 后再按需拉 blob。

## 10. 桌面/驱动/其他常见裸文件

| 目标 | 镜像地址模式 |
|---|---|
| ChromeDriver | `https://npmmirror.com/mirrors/chromedriver/LATEST_RELEASE_<major>` |
| GeckoDriver | `https://npmmirror.com/mirrors/geckodriver/` |
| Python 安装包（Windows） | `https://mirrors.huaweicloud.com/python/<ver>/python-<ver>-amd64.exe` |
| Miniconda | `https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/` |
| JDK（Temurin） | `https://mirrors.tuna.tsinghua.edu.cn/Adoptium/` |
| MySQL / PG 客户端包 | 同 §8 厂商源 |
| Homebrew（macOS） | `export HOMEBREW_API_DOMAIN=https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api` + `HOMEBREW_BOTTLE_DOMAIN=https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles`（仅在国内网络显著变慢时启用） |
