# 故障排查 — 看 doctor.sh 的 issues / 看 codex 报错信息,对照下表给用户处方

> **v7 架构提醒**:每个 profile 占独立的 relay 端口(agentplan=4446 / kimi=4447 / deepseek=4448 / custom=4449),arkv3 是直连模式。报"connection refused 127.0.0.1:444X"时,先看当前 active-profile 是哪个,再排查对应端口。

## 按现象索引

### 1. `command not found: codex`

**原因**:npm 全局 bin 不在 PATH。

**处方**:
```bash
bash scripts/install.sh   # install 会自动写 PATH 到 .bashrc
source ~/.bashrc
```

### 2. doctor.sh 显示 `codex_outdated=true`

**原因**:codex 版本 < 0.130,新版有 breaking change(`--print` 废弃、强制 `responses` 协议)。

**处方**:
```bash
bash scripts/install.sh   # 会自动升级到最新
```

### 3. `Not inside a trusted directory and --skip-git-repo-check was not specified`

**原因**:codex 默认要求在 git 目录跑,沙箱家目录通常不是。

**处方**:每次调用 codex 都加 `--skip-git-repo-check`:
```bash
codex exec --skip-git-repo-check "你的需求"
```
本 skill 在使用态调用模板里已经默认带这个参数,不会触发。

### 4. `error: unexpected argument '--print' found`

**原因**:用了老脚本里的 `codex --print`,Codex 0.130 已废弃。

**处方**:改成 `codex exec`。

### 5. `wire_api = "chat" is no longer supported` 或 codex 卡死无响应

**原因**:profile 里写了 `wire_api = "chat"`,但 codex 0.130+ 强制 `responses`。

**处方**:v7 之后所有 profile 的 `wire_api` 都是 `responses`,Chat-only 的上游通过本机 codex-relay 翻译。如果用户 profile 还是老版的 `chat`:
```bash
# 重跑 setup 即可生成新 profile
bash scripts/setup-thirdparty.sh <provider> "<key>" [model]
```

如果 setup 脚本写出来的 profile 有问题:
```bash
cat ~/.codex/profiles/<name>.toml
# 应该看到 wire_api = "responses",base_url 视 provider 不同
#   agentplan → http://127.0.0.1:4446/v1
#   kimi      → http://127.0.0.1:4447/v1
#   deepseek  → http://127.0.0.1:4448/v1
#   arkv3     → https://ark.cn-beijing.volces.com/api/v3   (直连)
#   custom    → 上游 URL 或 http://127.0.0.1:4449/v1       (探测决定)
```

### 6. `connection refused 127.0.0.1:444X`(任意 profile)

**原因**:对应端口的 codex-relay 没启动。每个 profile 占一个端口:agentplan=4446 / kimi=4447 / deepseek=4448 / custom=4449。

**处方**:
```bash
# 1. 看当前是哪个 profile
cat ~/.codex/active-profile

# 2. 一键自动恢复
bash scripts/ensure-relay.sh

# 3. 看日志(替换 <profile> 为实际名字)
tail -50 ~/.codex-relay-<profile>.log

# 4. 如果还不行,手动重启
codex-relay --port <端口> --upstream <对应上游URL>
```

### 7. `401 unauthorized`

**原因**:Key 错或不在对应路径有权限。

**处方**:
- AgentPlan 路径:必须用 **AgentPlan 控制台分配的"专属 Key"**,不能用普通 API Key 管理里的 Key
- 普通 v3 路径:必须用普通 API Key 管理里的 Key,不能用 AgentPlan 的
- 重新跑对应 setup 脚本传入正确的 Key:
  ```bash
  bash scripts/setup-agentplan.sh "<正确的 AgentPlan Key>"
  bash scripts/setup-thirdparty.sh kimi "<正确的 Moonshot Key>"
  ```

### 8. `404 Not Found`

**原因**:base_url 写错了。

**处方**:
- 看 `~/.codex/config.toml`(其实是当前 active profile 的软链)的 `base_url`
- 各 profile 期望值:
  - agentplan → `http://127.0.0.1:4446/v1`
  - kimi → `http://127.0.0.1:4447/v1`
  - deepseek → `http://127.0.0.1:4448/v1`
  - arkv3 → `https://ark.cn-beijing.volces.com/api/v3`(直连)
  - custom → 自动探测,要么是上游 URL,要么是 `http://127.0.0.1:4449/v1`

### 9. `400 invalid temperature/top_p`

**原因**:profile 里写了被后端模型写死的采样参数。

**处方**:删掉 profile 里所有 `temperature` / `top_p` 字段。本 skill 出厂的 profile 已经不带这些,如果用户手动加了 → 删掉。

### 10. 模型重复回复 N 次

**原因**:`request_max_retries / stream_max_retries / responses_websockets_v2` 三个开关没设全。

**处方**:本 skill profile 模板已经预设了。如果用户手动改过 profile 删了这几行 → 重跑 setup 脚本恢复。

### 11. doctor.sh 显示对应 Key 是空的

**原因**:`source ~/.bashrc` 还没生效,或者 setup 没成功。

**处方**:
```bash
# 看哪个 Key 没设
case "$(cat ~/.codex/active-profile)" in
  agentplan) echo "${#ARK_API_KEY}" ;;
  kimi)      echo "${#MOONSHOT_API_KEY}" ;;
  deepseek)  echo "${#DEEPSEEK_API_KEY}" ;;
  arkv3)     echo "${#ARK_V3_API_KEY}" ;;
  custom)    echo "${#CUSTOM_API_KEY}" ;;
esac
# 应该不为 0;为 0 → 重跑对应 setup 脚本
source ~/.bashrc
```

### 12. 沙箱重启后挂了

**原因**:Key 没持久化或 codex-relay 没自启。

**处方**:本 skill 的 setup 脚本会写一个**通用** auto-recover 块到 `~/.bashrc`,根据 active-profile 自动启对应端口的 relay。正常 `source ~/.bashrc` 即恢复。如果还是不行:
```bash
grep -E '(API_KEY|codex-allinone)' ~/.bashrc   # 应能看到 Key + auto-recover marker
bash scripts/ensure-relay.sh                    # 手动触发恢复
```

### 13. 切换 profile 后 codex 还是用旧的

**原因**:codex 是按 `~/.codex/config.toml` 读的,本 skill 用软链切换。检查软链:
```bash
ls -la ~/.codex/config.toml
# 应该指向 ~/.codex/profiles/<active>.toml
cat ~/.codex/active-profile
```

如果软链坏了:
```bash
bash scripts/switch-profile.sh <name>   # 重跑切换
```

### 14. `failed to load skill ... missing YAML frontmatter`

**原因**:同目录下有其他 Skill 的 SKILL.md 格式错了(不影响本 skill 自身)。

**处方**:可忽略;或者把那个有问题的 skill 目录删了。

## 兜底:把 doctor.sh 完整输出贴给我

如果上面都对不上,让用户:
```bash
bash scripts/doctor.sh
```
把完整 JSON 贴回来,Skill 根据 issues 数组逐项处理。
