---
name: docker-compose-yaml-field-order
description: >
  docker compose YAML 文件字段排序默认约定。只要用户没有对字段顺序提出要求，凡是写、改、审 docker-compose*.yaml / 
  compose*.yaml / docker-compose*.yml / compose*.yml 的字段，都必须套用本 skill。权威定义来自
  <https://github.com/foxydock/foxydock/blob/c875b600ce8ccac60a896103e158e55e80e0e9bd/compose/tool/find_unordered.py>。
when_to_use: >
  当用户在写、修改、审查自定义 docker compose 文件且没有对字段顺序提出要求时，使用本 skill
license: MIT
metadata:
  author: xfl12345
  version: "1.0.0"
---

# Docker Compose 字段排序约定

## When to Use

- 当用户在写、修改、审查自定义 docker compose 文件且没有对字段顺序提出要求时，使用本 skill

## service 块字段顺序约定

每个服务块的字段按以下链条的相对顺序排列。不需要的字段可以跳过，但出现的字段不能打乱顺序。`restart` 永远是最后一个字段。

### 按职责分组（便于记忆）

**① 环境与继承** — `env_file` → `extends`  
**② 元数据 / 运行身份** — `labels` → `user` → `pid` → `ipc`  
**③ 权限与安全** — `privileged` → `cap_add` → `sysctls` → `security_opt`  
**④ IO 与共享内存** — `stdin_open` → `tty` → `shm_size`  
**⑤ 镜像与构建** — `image` → `container_name` → `pull_policy` → `build`  
**⑥ 设备与临时存储** — `devices` → `tmpfs`  
**⑦ 持久化挂载** — `volumes`  
**⑧ 运行时入口** — `entrypoint` → `command` → `healthcheck` → `logging`  
**⑨ 网络身份** — `hostname` → `extra_hosts` → `links`  
**⑩ 网络接入** — `networks` → `network_mode` → `ports`  
**⑪ 依赖与生命周期** — `depends_on` → `stop_grace_period` → `restart`

**为什么要按职责分组。** 从「配置注入 → 身份 → 权限 → 资源 → 镜像 → 存储 → 运行时 → 网络 → 生命周期」是一条从「容器是什么」到「容器怎么跑、怎么死」的自然阅读链。统一顺序让 diff 最小、review 时一眼能看出新字段插得对不对。

**字段先后关系的判定优先级。** 决定先后时，「变量基于」关系优先级最高：一个字段的值或产物若由另一个字段决定，被依赖的排前、派生的排后，覆盖分组、作用域、粒度等其它理由。例：`build` 产出的镜像名默认取自 `image`，所以 `image` 在 `build` 前；同理 `ports` 基于 `expose`、`environment` 覆盖 `env_file`、`deploy` 部署的镜像来自 `image`/`build`。

### 不在权威清单里的字段

以下字段都不在 find_unordered.py 的 `the_service_key_order` 里，按概念分组就近插入（位置见下表）：

| 扩展字段      | 归属分组         | 插入位置                         | 由头                                   |
| ------------- | ---------------- | -------------------------------- | -------------------------------------- |
| `profiles`    | ① 环境与继承     | 顶部                             | 最高层开关，决定服务是否启用           |
| `environment` | ① 环境与继承     | `profiles` 之后，`env_file` 之前 | `environment`优先级比`env_file`高      |
| `group_add`   | ③ 权限与安全     | `security_opt` 之后              | `security_opt`比`group_add`更底层      |
| `deploy`      | ⑤ 镜像与构建     | `build` 之后                     | `deploy`部署的镜像来自 `image`/`build` |
| `expose`      | ⑩ 网络接入       | `ports` 之前                     | 一般都是基于`expose`定制的`ports`      |
| `init`        | ⑪ 依赖与生命周期 | `restart` 之前                   | `init` 管进程，`restart` 管容器        |
| `post_start`  | ⑪ 依赖与生命周期 | `init` 之后                      | 启动后触发的钩子，紧跟 `init`(PID 1)   |

### 完整链条（全字段，自上而下）

把上面分组与表格的插入位置整合后的全字段顺序：

- profiles
- environment
- env_file
- extends
- labels
- user
- pid
- ipc
- privileged
- cap_add
- sysctls
- security_opt
- group_add
- stdin_open
- tty
- shm_size
- image
- container_name
- pull_policy
- build
- deploy
- devices
- tmpfs
- volumes
- entrypoint
- command
- healthcheck
- logging
- hostname
- extra_hosts
- links
- networks
- network_mode
- expose
- ports
- depends_on
- stop_grace_period
- init
- post_start
- restart

### 示例

以 archivebox 官方 compose 为例（<https://github.com/ArchiveBox/ArchiveBox/blob/c8d0e2e8e70b27c6d3db059f8fe765cb17aab418/docker-compose.yml>）：

```yaml
# ❌ 官方原版：字段乱序——①environment、④shm_size 错位
services:
  archivebox:
    image: ${ARCHIVEBOX_IMAGE:-archivebox/archivebox:dev} # ⑤
    ports: # ⑩
      - 8000:8000
    volumes: # ⑦
      - ./data:/data
    environment: # ① ← 跑到 ⑤⑦⑩ 后
      - BASE_URL=...
    shm_size: 1gb # ④ ← 跑到 ⑤ 后
```

```yaml
# ✅ 按约定重排：「变量基于」优先（environment 先、shm_size 在 image 前），分组自上而下
services:
  archivebox:
    environment: # ①
      - BASE_URL=${BASE_URL:-http://archivebox.localhost:8000}
    shm_size: 1gb # ④
    image: ${ARCHIVEBOX_IMAGE:-archivebox/archivebox:dev} # ⑤
    container_name: archivebox # ⑤
    volumes: # ⑦
      - archivebox_storage:/data
    ports: # ⑩
      - 8000:8000
    restart: unless-stopped # ⑪

volumes:
  archivebox_storage:
```

**override 文件** — 只写需要覆写的字段，相对顺序仍遵守链条：

```yaml
services:
  dind:
    environment:
    build:
```

## 不适用的情况

直接复制上游官方 compose 文件零改动的项目不强制遵守本约定。一旦对 compose 文件做了个人定制，就应当遵守本约定。
