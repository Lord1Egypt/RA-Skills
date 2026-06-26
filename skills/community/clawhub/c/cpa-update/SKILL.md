---
name: cpa-update
description: 安全更新和维护 CLI Proxy API（CPA）部署与配置。用于 CPA 镜像升级、配置变更、认证目录兼容修复、上线验证与回滚。适用于用户提到“CPA 更新/升级/配置改了/容器重建/回滚”等场景。
---

# CPA Update（v2.2.1）

## 目标
在**不丢配置、不丢认证、可快速回滚**的前提下，完成 CLI Proxy API 更新或配置迁移。

## 官方资源
- **Docker Hub**: [`eceasy/cli-proxy-api`](https://hub.docker.com/r/eceasy/cli-proxy-api)
- **GitHub**: [router-for-me/Cli-Proxy-API](https://github.com/router-for-me/Cli-Proxy-API)
- **最新版本查询**: `docker pull eceasy/cli-proxy-api:latest` 或查看 Docker Hub tags

## 强制安全规则
1. 任何修改前先确认用户同意（尤其是重启/替换生产容器）。
2. 任何修改前先备份（镜像 + 配置 + auth 目录）。
3. 先测试再切生产。
4. 保留可执行回滚路径。

## 0) 先做现网发现（禁止硬编码）
> 不要假设固定容器名、镜像名、版本号、端口。

```bash
# 找 CPA 容器
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'

# 查看当前版本信息（注意：某些版本会输出版本后返回非0）
docker exec <CONTAINER_NAME> ./CLIProxyAPI --version || true

# 假设配置路径为 /opt/cliproxyapi/config.yaml，读取关键项
sed -n '1,220p' /opt/cliproxyapi/config.yaml

# 快速定位当前启用的 provider 段
grep -n -- "-api-key:" /opt/cliproxyapi/config.yaml

# 检查官方最新版本
docker pull eceasy/cli-proxy-api:latest
```

记录以下基线（用于变更对比）：
- 容器名、镜像名、映射端口
- 当前版本号（通过 `./CLIProxyAPI --version` 获取）
- `auth-dir`
- `remote-management.allow-remote`
- 当前使用的 provider 段（如 `gemini-api-key`、`claude-api-key`、`codex-api-key`、`xai-api-key` 等）

## 1) 备份（必须）
```bash
mkdir -p /opt/cliproxyapi/backup /opt/cliproxyapi/backups
TS=$(date +%Y%m%d-%H%M%S)

# 备份镜像（将 <IMAGE> 替换为当前生产镜像）
docker save <IMAGE> > /opt/cliproxyapi/backup/cliproxyapi-image-${TS}.tar

# 备份配置
cp /opt/cliproxyapi/config.yaml /opt/cliproxyapi/backup/config-${TS}.yaml

# 备份认证目录
cp -a /opt/cliproxyapi/auth /opt/cliproxyapi/backup/auth-${TS}

# 保存现网基线信息
HOST_PORT=$(docker inspect <CONTAINER_NAME> --format '{{(index (index .NetworkSettings.Ports "8317/tcp") 0).HostPort}}' 2>/dev/null || echo "unknown")
VERSION_RAW=$(docker exec <CONTAINER_NAME> ./CLIProxyAPI --version 2>&1 || true)
VERSION_LINE=$(printf '%s\n' "$VERSION_RAW" | grep -m1 'CLIProxyAPI Version' || echo "$VERSION_RAW")
cat > /opt/cliproxyapi/backups/baseline-${TS}.md << EOF
# Baseline ${TS}
Container: <CONTAINER_NAME>
Image: <IMAGE>
Version: ${VERSION_LINE}
Port: ${HOST_PORT}
Auth Dir: /opt/cliproxyapi/auth
Config: /opt/cliproxyapi/config.yaml
EOF
```

## 2) 判断更新类型

### A. 仅配置变更（推荐优先）
适用于：新增/修改 provider、模型路由、管理参数、重试策略等。

流程：
1. 编辑 `config.yaml`
2. 校验 YAML 格式（建议）
3. 重启容器并验证

```bash
# 2A-1 重启
docker restart <CONTAINER_NAME>

# 2A-2 健康检查
curl -s http://127.0.0.1:8317/v1/models -H "Authorization: Bearer <API_KEY>" | head
```

### B. 镜像升级（涉及容器替换）
适用于：官方发布新版本或需要修复基础镜像问题。

**官方镜像地址**: `eceasy/cli-proxy-api:latest`

**兼容修复要点：**确保容器内存在 auth 目录并可写（常见问题是 `/root/.cli-proxy-api` 权限/挂载冲突）。

**直接使用官方镜像（推荐）**:
```bash
# 拉取最新官方镜像
docker pull eceasy/cli-proxy-api:latest

# 测试容器（使用测试端口 8318）
docker run -d --name cliproxyapi-test \
  -p 8318:8317 \
  -v /opt/cliproxyapi/config.yaml:/CLIProxyAPI/config.yaml \
  -v /opt/cliproxyapi/auth:/root/.cli-proxy-api \
  --restart unless-stopped \
  eceasy/cli-proxy-api:latest

# 等待启动（约 5-10 秒）
sleep 10

# 健康检查
curl -s http://127.0.0.1:8318/v1/models -H "Authorization: Bearer <API_KEY>" | head

# 检查日志
docker logs --tail 50 cliproxyapi-test

# 验证成功后停止测试容器
docker stop cliproxyapi-test && docker rm cliproxyapi-test
```

**自定义镜像构建（如需特殊配置）**:
```dockerfile
FROM eceasy/cli-proxy-api:latest
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir -p /root/.cli-proxy-api && chmod 755 /root/.cli-proxy-api
WORKDIR /CLIProxyAPI
EXPOSE 8317
CMD ["./CLIProxyAPI"]
```

## 3) 生产发布（需用户确认）
```bash
# 停止并删除当前容器
docker stop <CONTAINER_NAME>
docker rm <CONTAINER_NAME>

# 使用官方最新镜像启动生产容器
docker run -d \
  --name <CONTAINER_NAME> \
  -p 8317:8317 \
  -v /opt/cliproxyapi/config.yaml:/CLIProxyAPI/config.yaml \
  -v /opt/cliproxyapi/auth:/root/.cli-proxy-api \
  --restart unless-stopped \
  eceasy/cli-proxy-api:latest
```

## 4) 发布后验收清单
1. `/v1/models` 可返回完整模型列表
2. 随机抽测至少 1 个关键模型（如 `gpt`/`claude`/`gemini`/`xai`）
3. 日志无持续报错（auth、401、timeout、panic）
4. 管理接口（若启用）可访问且权限正确
5. 版本信息确认：`docker exec <CONTAINER_NAME> ./CLIProxyAPI --version`

## 5) 回滚（必须可用）
```bash
# 停新容器
docker stop <CONTAINER_NAME> && docker rm <CONTAINER_NAME>

# 恢复旧镜像
docker load < /opt/cliproxyapi/backup/cliproxyapi-image-<TS>.tar

# 用旧镜像重启
docker run -d \
  --name <CONTAINER_NAME> \
  -p 8317:8317 \
  -v /opt/cliproxyapi/config.yaml:/CLIProxyAPI/config.yaml \
  -v /opt/cliproxyapi/auth:/root/.cli-proxy-api \
  --restart unless-stopped \
  <OLD_IMAGE>
```

## 6) 更新成功后归档与清理（需用户确认）
> 目标：保持 `/opt/cliproxyapi` 干净可读；不删除在线配置与认证目录；保留回滚能力。

**默认原则（推荐）**
1. 永远保留在线目录：
   - `/opt/cliproxyapi/config.yaml`
   - `/opt/cliproxyapi/auth/`
2. 每次升级成功后，把历史备份移动到时间戳归档目录：
   - `/opt/cliproxyapi/archive/<YYYYmmdd-HHMM>/`
3. 保留策略：
   - `archive/` 保留最近 **2** 次升级归档
   - `backup/` 仅保留“当前升级批次”产物（可为空）
   - 至少保留 **1 份可用回滚镜像**（tar 或已打 tag 的本地镜像）
4. 仅归档/删除“历史备份”，不动生产容器和在线挂载。

**归档命令模板（先归档，不直接删除）**
```bash
set -euo pipefail
TS=$(date +%Y%m%d-%H%M)
ARCHIVE_DIR="/opt/cliproxyapi/archive/${TS}"
mkdir -p "$ARCHIVE_DIR"

# 记录归档前快照
find /opt/cliproxyapi -maxdepth 2 -mindepth 1 | sort > "$ARCHIVE_DIR/PRE_ARCHIVE_SNAPSHOT.txt"

# 移动历史备份（仅示例，可按实际目录调整）
shopt -s nullglob
for f in \
  /opt/cliproxyapi/backup/auth-* \
  /opt/cliproxyapi/backup/config-*.yaml \
  /opt/cliproxyapi/backup/*.tar \
  /opt/cliproxyapi/config.yaml.backup.*
 do
  [ -e "$f" ] && mv "$f" "$ARCHIVE_DIR/"
 done

# 写归档说明
cat > "$ARCHIVE_DIR/README.md" <<EOF
# CPA Archive ${TS}

归档时间：$(date '+%Y-%m-%d %H:%M:%S %Z')

在线目录（未修改）：
- /opt/cliproxyapi/config.yaml
- /opt/cliproxyapi/auth/

本次归档用于保留历史备份，便于审计与回滚追溯。
EOF
```

**可选清理（确认后执行）**
```bash
# 仅清理 dangling 镜像层（安全）
docker image prune -f

# 如需删除旧测试容器（示例）
docker rm -f cliproxyapi-test || true
```

**归档后复检（必须）**
```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl -s http://127.0.0.1:8317/v1/models -H "Authorization: Bearer <API_KEY>" | head
```

## 常见故障排查
- **容器循环重启**：优先看 auth 目录挂载与权限。
- **模型列表缺失**：检查 provider 段和 API key 是否生效。
- **请求 401/403**：检查调用 key 与 upstream key 是否混淆。
- **管理接口异常**：检查 `remote-management.secret-key` 与 `allow-remote`。
- **版本升级后功能异常**：检查新版本是否有 breaking changes，参考官方 changelog。

## 维护建议
- **定期检查更新**：每月检查一次官方镜像是否有新版本
- **基线文档化**：把“现网基线”单独保存为 `/opt/cliproxyapi/backups/baseline-<date>.md`
- **测试先行**：任何变更都先在测试端口验证
- **版本记录**：在配置文件注释中记录当前使用的镜像版本和更新日期

## 版本升级最佳实践
1. **小步快跑**：不要跳过多版本升级，逐版本验证
2. **关注 changelog**：升级前查看官方 release notes
3. **备份验证**：确保备份文件可以正常恢复
4. **监控告警**：升级后密切监控日志和错误率
