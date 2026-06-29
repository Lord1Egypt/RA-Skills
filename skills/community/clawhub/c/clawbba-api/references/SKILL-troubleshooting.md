# ClawBBA × OpenClaw — 故障排查（完整版）

用户可见 SKILL 仅保留简短表；详细项见本文。Agent 处理用户问题时先读 `error-translation.md`，勿向用户暴露上游内部标签。

## 安装与配置

| 现象 | 处理 |
|------|------|
| `skills install` 后不能用 | 必须 `export CLAWBBA_API_KEY` 后跑 `setup.sh --yes` + `gateway restart` |
| `setup.sh` 卡住 | 使用 `./scripts/setup.sh --yes` |
| `openclaw: command not found` | 先安装 OpenClaw CLI |
| `validate` 失败 | 重跑 `setup.sh --yes`；勿手删模型凑通过 |
| `[assistant turn failed]` / `403 Your request was blocked` | `models.json` 中 apiKey 为占位符 → `export CLAWBBA_API_KEY=… && node scripts/fix-provider-config.mjs && gateway restart` |
| `models.json` 只有 1 个 clawbba 模型 | 重跑 `setup.sh --yes` |

## 生图 / 生视频

| 现象 | 处理 |
|------|------|
| 没有 `image_generate` / `video_generate` | OpenClaw ≥ 2026.5；重跑安装脚本；`gateway restart` |
| `No image-generation provider registered for clawbba` | 生图 **禁止** `clawbba/` 前缀；用语义 `模型 black-forest-labs/flux.2-pro` 或见 `media-model-ref.md` |
| 日志有 `MEDIA:` 但 WebChat 无图 | 重跑 `setup.sh`；`node scripts/verify-openclaw-patch.mjs` |
| `webchat image embedding skipped` | 确认 patch；清 `~/.openclaw/agents/main/sessions/*.lock` 后重启 |
| 已扣费无图 | `image_generate action=tasks` → `action=recover jobId=… timeoutMs=600000`（同一 job，勿重新 generate） |
| 已扣费无视频 / fetch timeout | `video_generate action=tasks` → `action=recover jobId=… timeoutMs=600000`（同一 job，勿重新 generate） |
| 工具报余额不足但 estimate 足够 | 鉴权/配置问题 → 重跑一键安装，勿反复换模型 |
| Agent 长篇诊断 | 读 `error-translation.md`；对用户只说 ClawBBA 话术 |

## 会话与模型

| 现象 | 处理 |
|------|------|
| 切换模型无响应 | 重跑 `setup.sh`；`gateway restart`；**新开对话** 或 `/model clawbba/<id>` |
| 会话锁定 | 停 Gateway → 删 `*.jsonl.lock` → 重启 → 新对话 |

## 验证命令

```bash
CLAWBBA_API_KEY='cbb_sk_live_…' ./scripts/verify-key.sh
node scripts/verify-openclaw-runtime.mjs
node scripts/verify-openclaw-patch.mjs
openclaw config validate
```
