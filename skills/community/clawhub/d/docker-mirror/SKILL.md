---
name: docker-mirror
description: Docker 镜像拉取工具，自动切换镜像源。当官方 registry (docker.io) 拉取超时或失败时，自动尝试备用镜像（docker.1ms.run、docker.m.daocloud.io）。适用于网络受限的 Linux 环境。需要 sg (sgdocker group) 和 docker 已安装。触发场景：(1) 用户请求拉取 Docker 镜像，(2) docker pull 失败，(3) 任何涉及 Docker 镜像下载的场景。
---

# Docker Mirror

自动处理 Docker 镜像拉取失败，切换到国内镜像源。

## 工作原理

1. 先尝试官方 registry (`docker.io`)
2. 失败则按顺序尝试备用镜像
3. 成功后 tag 回原名并清理镜像残留

## 使用方法

```bash
# 拉取镜像（核心用法）
bash ./scripts/docker.sh pull <镜像名>[:标签]

# 示例
bash ./scripts/docker.sh pull nginx:latest
bash ./scripts/docker.sh pull redis:alpine
bash ./scripts/docker.sh pull postgres:15
```

## 其他 Docker 命令

非 pull 命令直接透传给 docker：

```bash
bash ./scripts/docker.sh ps -a
bash ./scripts/docker.sh images
bash ./scripts/docker.sh run -it nginx:latest
bash ./scripts/docker.sh stop nginx
```

## 镜像源状态

最新验证结果（2026-03-29）：

| 镜像源 | 状态 | 备注 |
|--------|------|------|
| docker.io | ❌ 超时 | 国内访问不稳定 |
| docker.1ms.run | ✅ 可用 | 主要备用源 |
| docker.m.daocloud.io | ✅ 可用 | DaoCloud 镜像 |

已验证可正常拉取：`hello-world`、`nginx:latest`、`nginx:alpine`

## 故障排除

如果 `docker.sh pull` 失败：

1. 检查 Docker daemon 是否运行：
   ```bash
   bash ./scripts/docker.sh ps
   ```

2. 查看本地镜像：
   ```bash
   bash ./scripts/docker.sh images
   ```

3. 手动指定镜像源：
   ```bash
   bash ./scripts/docker.sh pull docker.1ms.run/library/nginx
   ```

## 环境依赖

- `sg` 命令（sgdocker 组权限）
- `docker` 已安装且 daemon 运行中
