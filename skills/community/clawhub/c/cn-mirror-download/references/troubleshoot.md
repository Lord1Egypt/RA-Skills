# 镜像故障字典

## 判定顺序

1. 镜像域名能不能连（`curl -sS -o /dev/null -m 6 -w '%{http_code}\n' URL`）→ 不通 = 换镜像，不是配置问题。
2. 通了但 403/404 → 路径规则变了（见下表）。
3. 通了、200，但客户端还慢 → 客户端没读到配置（见「配置没生效」）。
4. 都正常但仍失败 → 目标版本镜像没同步 → 回官方源。

## 报错 → 处置

| 报错 | 真实原因 | 处置 |
|---|---|---|
| `SSL: CERTIFICATE_VERIFY_FAILED` | 镜像 HTTPS 被公司网关 MITM，或缺 CA | 换镜像；确属内网才 `--trusted-host` / 导入企业 CA。不要 `NODE_TLS_REJECT_UNAUTHORIZED=0` |
| `ProxyError` / `407` | 环境设了 `HTTPS_PROXY` 但代理不认镜像域名 | `NO_PROXY` 加镜像域名，或确认代理白名单 |
| `403 Forbidden`（npmmirror binaries） | 路径前缀变更 | `cdn.npmmirror.com/binaries/...` ↔ `npmmirror.com/mirrors/...` 互换再试 |
| `404`（pip 某版本） | 镜像同步延迟（新发布常差 5–60 分钟） | 官方源装该包：`pip install -i https://pypi.org/simple PKG` |
| `no matching distribution` | 该包只发 sdist 或平台不匹配，不是镜像问题 | 检查 Python 版本 / 平台 wheel，别看镜像 |
| `ETIMEDOUT` 反复 | 该镜像在本网络不可达 | 回退链下一项；记录可用清单 |
| `Read timed out` | 带宽不足（大 wheel / 模型） | `--timeout 120 --retries 5`，降并发（`npm i --maxsockets 3`） |
| `unexpected EOF` / 包损坏 | 半截下载被缓存 | 清缓存：`pip cache purge`、`npm cache clean --force`、删 `~/.cargo/registry/cache`、删 electron/playwright 缓存目录 |
| `checksum mismatch` | 镜像内容与预期不一致 | **停**。换镜像重下，比对官方 sha256；仍不一致按供应链问题上报，不要 `--no-verify` |
| `go: module ... verifying ... 410 Gone` | `GOSUMDB` 指向的 sumdb 不可达 | `GOSUMDB=sum.golang.google.cn`；仍失败改用 `GOPRIVATE` 精确排除 |
| `error: failed to select a version`（cargo） | sparse index 未生效或源不可达 | 确认 `config.toml` 是 `sparse+https://`，`cargo update -v` 看实际请求域名 |
| `Could not find method maven()`（gradle） | `init.gradle` 里注入位置不对（settings 阶段 vs project 阶段） | 用 `settingsEvaluated`/`beforeSettings` 或在 `settings.gradle` 的 `dependencyResolutionManagement` 里配 |
| `Could not resolve ...` 但 curl 该 URL 是 200 | Gradle/Maven 缓存了失败结果 | `--refresh-dependencies`，删 `~/.gradle/caches/modules-2` |
| `docker: toomanyrequests` | 镜像站限流 | 换 registry mirror；或登录后拉 |
| `docker pull` 报 `manifest unknown` | 镜像站未同步该 tag（常见于新 tag / 非 library 命名空间） | 换 `docker.m.daocloud.io/library/X:TAG` 试，或回 Docker Hub + 代理 |

## 配置没生效的排查

```bash
# pip：看真实 index
pip -v install --dry-run requests 2>&1 | grep -i "Looking in indexes"
python -c "import os;print({k:v for k,v in os.environ.items() if k.startswith('PIP_')})"

# npm：优先级 project .npmrc > user .npmrc > global > env
npm config ls -l | grep -E "^registry|userconfig|globalconfig"
npm config get registry

# go
go env GOPROXY GOSUMDB GOPRIVATE GONOSUMDB GOFLAGS

# cargo
cargo -Vv | sed -n '1,20p'; ls -l ~/.cargo/config.toml

# docker
docker info | sed -n '/Registry Mirrors/,+5p'
```

常见失效原因：
- `pip.conf` 放错位置（Linux `~/.config/pip/pip.conf`、macOS `~/Library/Application Support/pip/pip.conf`、Windows `%APPDATA%\pip\pip.ini`）。
- `.npmrc` 被 `--registry` 或 CI 的 `NPM_CONFIG_REGISTRY` 覆盖；或 pnpm 用了自己的 `pnpm config` 作用域。
- `~/.cargo/config`（旧名，无扩展）与 `config.toml` 同时存在 → 旧文件优先，改了新的没反应。
- Gradle 的 `init.gradle` 放在 `~/.gradle/init.d/` 才自动加载（放 `~/.gradle/init.gradle` 需要 `--init-script`）。
- 容器内构建不继承宿主的 daemon.json / `.npmrc`，要在 `Dockerfile` 里显式复制或传 `--build-arg`。

## 回滚清单（改过就要能退）

```bash
# 全局 npm
npm config delete registry
# 全局 go
go env -u GOPROXY GOSUMDB
# git URL 改写
git config --global --unset-all url."https://ghfast.top/https://github.com/".insteadOf
# apt
sudo mv /etc/apt/sources.list.bak-YYYY-MM-DD /etc/apt/sources.list && sudo apt-get update
# cargo
mv ~/.cargo/config.toml ~/.cargo/config.toml.bak
```

原则：任何 `[GLOBAL]` 级改动，执行前先备份，执行后在答复里给出上面这种逐条回滚命令。
