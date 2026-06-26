---
name: fix-cli-device-scope
description: |
  修复 OpenClaw CLI 设备权限不足导致 subagent/spawn/cron 等操作被拒绝的问题。
  触发词: pairing required, spawn失败, cron失败, 设备权限不足, admin scope, 死循环, CLI设备, scope不足。
  当 spawn subagent 报 "gateway closed (1008): pairing required"，且 gateway 本身运行正常时触发。
---

# Fix CLI Device Scope

修复 OpenClaw CLI 设备 scope 权限不足导致的配对失败。

## 症状

```
sessions_spawn error: gateway closed (1008): pairing required
[tools] cron failed: gateway closed (1008): pairing required
```

同时确认：
- `openclaw gateway status` 显示 gateway **running**
- `openclaw devices list` 显示 CLI 设备 **Paired** 但 scopes 只有 `operator.read`，没有 admin

---

## 快速诊断

一行命令输出完整诊断：

```bash
python3 scripts/diagnose.py
```

输出示例（需要修复）：
```
=== CLI Device Scope 诊断 ===

✓ Gateway 正在运行
  设备 ID:    2f5c98cfd06a980cb20ca1217580e6d8be7df78034a278b0fdaf81a9d8ac99c5
  当前 scopes: ['operator.read']
  pending:    1 repair 请求

⚠️  需要修复：CLI 设备缺少 admin scope
   死循环：当前只有 read，无法 approve 自己的升级请求

修复命令：
  python3 scripts/fix.py --dry-run  # 先预览
  python3 scripts/fix.py            # 执行修复
```

---

## 核心原因

Gateway 设备的 scope 太低（只有 `operator.read`），而 subagent spawn / cron 等操作需要 `operator.admin`。有一个 repair pending 请求在队列里等着升级 scope，但当前 token 权限不够 approve 不了——死循环：

```
需要 admin scope → 才能 approve → admin scope 申请
```

---

## ⚠️ 检查点：修复前确认

执行修复脚本前，**必须先展示将要改动的配置**，等待用户确认：

```bash
# 先用 --dry-run 看改动（不执行写入）
python3 scripts/fix.py --dry-run

# 输出示例：
# Device: 2f5c98cf...
# Current scopes: ['operator.read']
# New scopes: ['operator.admin', 'operator.read', 'operator.write', ...]
# Files to modify:
#   - paired.json
#   - device-auth.json
#   - pending.json (cleanup)
#
# ❓ Proceed? [y/N]:
```

用户确认后才执行：
```bash
python3 scripts/fix.py  # 默认会先展示再询问
python3 scripts/fix.py --force  # 跳过确认（仅限自动化场景）
```

---

## 验证修复

```bash
# 重启 gateway 加载新 scope
openclaw gateway restart

# 等待 ~5 秒后测试 spawn
```

用 `sessions_spawn` 工具验证，应该返回 `status: accepted`。

---

## 预防措施

- **修改前先备份** `paired.json.bak` 和 `device-auth.json.bak`
- 确认 DEVICE_ID 是要修的设备（看 `clientId=cli` 且 `platform=linux`）
- 不要删除其他正常设备的 paired 记录
- 修复后建议 `openclaw doctor --fix` 检查整体健康状态

---

## 注意事项

- 必须重启 gateway 才能加载新 scopes
- 新 token 格式 `cli_admin_<random>`，每次修复会更新
- 如果 gateway 从旧备份恢复，旧 token 会重新生效，需重新修复
- 没有 pending repair 请求的情况下，可手动构造 full_scopes 列表写入（`['operator.admin', 'operator.read', 'operator.write', 'operator.approvals', 'operator.pairing', 'operator.talk.secrets']`）