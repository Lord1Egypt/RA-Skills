---
doc: runbook-templates-index
purpose: 按绑定点类型的 Runbook 模板集合索引
parent: ../../SKILL.md
updated: 2026-04-23
---

# 📦 Runbook Templates · 按绑定点类型

> 本目录提供**各类绑定点的 Runbook 骨架**，对应 `05-dry-run-matrix.md §1` 方法库。
> 所有模板使用 `${VAR}` 占位符，**严禁硬编码生产值**；密钥类变量通过客户密钥管理系统获取（详见 `05-dry-run-matrix.md §5`）。

## 当前模板

| 绑定点类型 | 模板文件 | 适用 | 回滚复杂度 |
|-----------|---------|------|-----------|
| Java KeyStore | [`jks-rollover.sh.tpl.md`](./jks-rollover.sh.tpl.md) | Java 应用，keystore.jks | 🟡 中（有中间态风险）|
| Nginx | [`nginx-reload.sh.tpl.md`](./nginx-reload.sh.tpl.md) | Nginx `ssl_certificate`（Fast Path 主力）| 🟢 低 |
| K8s Secret（手工）| [`k8s-secret-rollover.sh.tpl.md`](./k8s-secret-rollover.sh.tpl.md) | 没接入 cert-manager 的手工 Secret | 🟡 中 |
| CDN 手工上传 | [`cdn-manual-upload.md.tpl.md`](./cdn-manual-upload.md.tpl.md) | 无 API / 老版本 CDN | 🟢 低 |

## 待补模板（backlog）

- [ ] `pfx-iis-rollover.ps1.tpl.md` · Windows / IIS PowerShell
- [ ] `haproxy-reload.sh.tpl.md` · HAProxy
- [ ] `envoy-sds.sh.tpl.md` · Envoy + SDS 动态证书下发
- [ ] `acme-sh-cron.sh.tpl.md` · acme.sh 定时续签（含 deploy hook 集成）
- [ ] `cert-manager-renewal.yaml.tpl.md` · cert-manager Certificate 资源
- [ ] `api-gateway-custom-domain.md.tpl.md` · API 网关自定义域名绑定

## 使用约定

1. **复制即用**：客户/Agent 复制 `.tpl.md` 内容到本地 `.sh` / `.ps1` / `.yaml` 文件
2. **先 Dry-Run**：执行前必须在 Phase 5 Dry-Run 做过一次测试
3. **占位符审计**：所有 `${VAR}` 必须有值来源说明（见 `05-dry-run-matrix.md §5` 密钥获取方式对齐表）
4. **回滚命令独立记忆**：每个模板末尾都有独立的回滚命令块，便于故障现场复制
