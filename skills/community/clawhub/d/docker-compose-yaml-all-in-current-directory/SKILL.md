---
name: docker-compose-yaml-all-in-current-directory
description: >
  创建一个仅使用当前工作目录的 docker compose YAML配置文件约定
when_to_use: >
  当用户说类似 "参考一个已有的 docker compose 配置文件重写成一个仅使用当前工作目录的 docker compose YAML配置文件" 时使用本 skill
license: MIT
metadata:
  author: xfl12345
  version: "1.0.0"
---

# Docker Compose Yaml 单目录流派的约定

## When to Use

- 当用户说类似 "参考一个已有的 docker compose 配置文件重写成一个仅使用当前工作目录的 docker compose YAML配置文件" 时使用本 skill

## YAML 字段排序

字段排序是独立 skill `docker-compose-yaml-field-order`（强制触发，写/改/审 compose 服务块时自动套用）。

## 目录结构约定

项目内文件统一走镜像目录结构，分 `./volume/`（持久化）、`./env/`（环境变量）、`./build_resource/`（构建）三类。前两类下一级都允许有一个可选的 **namespace**（一个 compose 区分多个变体或公共资源时用，如 `ubuntu/kde`、`common`），再接 `moved_root` 或直接放文件。

**volume**：

```
./volume/[<namespace>/]moved_root/<容器内路径>  →  /<容器内路径>
```

`moved_root` 镜像容器根文件系统——容器内要持久化什么路径，就在 `moved_root/` 下建相同相对路径。例：`/data` → `./volume/moved_root/data`；多变体时 `/config` → `./volume/ubuntu/kde/moved_root/config`。

**env**：

```
./env/[<namespace>/]<name>.env
```

环境变量外置到 `./env/` 下的 `.env` 文件，compose 用 `env_file` 引用。例：`./env/new-api.env`、`./env/common.env`。

**build_resource**：

```
./build_resource/
├── <variant>.Dockerfile   # 多变体一文件一个，按变体命名（如 ubuntu-kde.Dockerfile / alpine-kde.Dockerfile）
├── *.*                    # 容器镜像构建辅助工具等，不放入容器镜像里的文件（如 patch-openssh-server.sh）
└── moved_root/            # 镜像容器根目录，用于构建期注入文件到镜像中（etc/apt/ 源、etc/fonts/、usr/share/…）
```

- 多变体用 **文件名** 区分（不像 volume/env 用 namespace 子目录）
- compose 里 `build.context: ./build_resource` + `build.dockerfile: ./<variant>.Dockerfile` 选用。
- `moved_root/` 与卷里的 `moved_root/` 同义——都镜像容器根目录，区别只是这里在构建期注入文件（如 apt 源 template、字体），成为镜像的一部分，而volume那套在运行期持久化。

### 规则

- 卷宿主机侧路径统一走 `./volume/[<namespace>/]moved_root/`，禁止直接挂 `./volume/` 或随意路径。
- env 变量外置到 `./env/[<namespace>/]` 下的 `.env` 文件，禁止把敏感信息内联进 `environment`。
- namespace 可选：单一服务直接 `./volume/moved_root/...`；一个 compose 含多变体或公共资源时用它分组（参考 [webtop 示例](https://github.com/xfl12345/webtop/blob/0cd2bb65361e2985fb13c989001bcc94a27fe8a1/docker-compose.example.yaml) 的 `ubuntu/kde`、`common`）。
- 把官方 compose 改造成自己的风格时：只保留核心服务，删掉注释掉的可选 sidecar，卷改走 `moved_root`、env 改走 `./env/`，字段按链条重排。

### 示例

以 new-api 官方 compose 为例（<https://github.com/QuantumNous/new-api/blob/3e1e728279884d83358811aec00980dd55f6ad4e/docker-compose.yml>），把内联 `environment`（含 `SQL_DSN`、`REDIS_CONN_STRING` 等带密码的变量）外置成 `env_file`：

```yaml
# ❌ 官方原版：env 全内联在 compose（密码明文写进来），卷也挂随意路径
services:
  new-api:
    image: calciumion/new-api:latest
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    environment:
      - SQL_DSN=postgresql://root:123456@postgres:5432/new-api # ← 密码明文
      - REDIS_CONN_STRING=redis://:123456@redis:6379
      - TZ=Asia/Shanghai
      - NODE_NAME=new-api-node-1
```

```yaml
# ✅ 按约定：env 走 env_file（外置到 ./env/ 下的文件），卷走 moved_root
services:
  new-api:
    env_file:
      - ./env/new-api.env
    image: calciumion/new-api:latest
    volumes:
      - ./volume/moved_root/data:/data
      - ./volume/moved_root/app/logs:/app/logs
```

```env
# ./env/new-api.env —— 变量集中放文件，compose 只引用路径
SQL_DSN=postgresql://root:123456@postgres:5432/new-api
REDIS_CONN_STRING=redis://:123456@redis:6379
TZ=Asia/Shanghai
NODE_NAME=new-api-node-1
```

## 不适用的情况

直接复制上游官方 compose 文件零改动的项目不强制遵守本约定。一旦对 compose 做了个人定制，就应当回到本约定。
