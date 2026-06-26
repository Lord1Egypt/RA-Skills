---
name: "configure-openclaw-anyrouter-model-and-fix-baseurl"
description: "用于在 OpenClaw 中新增或覆盖 anyrouter 模型配置、把小肠 Agent 默认模型切到 `anyrouter/claude-opus-4-6`，并结合运行日志判断是不是 `baseUrl`、网关兼容、鉴权或协议端点导致不可用。遇到“把某个供应商模型写进 openclaw.json”“切换默认模型”“为什么配置生效了但实际没调用上”“查看 fallback 日志”“排查 403/500/invalid claude code request”“同步 ClaudeCode 配置”这类需求时，就应启用本技能；即使用户没明确说 OpenClaw，只要描述的是本地 Agent 模型路由切换与调用异常排查，也适用。"
metadata: { "openclaw": { "emoji": "🦞" } }
---

# 配置 OpenClaw 的 AnyRouter 模型并修复 baseUrl 可用性

这个技能帮助你把 `anyrouter/claude-opus-4-6` 正确接入 OpenClaw、切换小肠 Agent 默认模型，并用真实日志与实测调用区分“配置已生效”和“上游实际可用”这两件事。

## When to use this skill
- 当你需要把用户提供的一段 JSON 合并进 `openclaw.json`，并把小肠 / main Agent 的默认模型切到指定供应商模型。
- 当配置看起来已经写对，但运行时仍报 `403`、`500`、`invalid claude code request`，需要结合日志判断是不是 `baseUrl`、协议端点或 key 权限问题。
- 当用户要求“确认当前小肠 Agent 到底是什么模型”“配置是否真的生效”“是否只是 fallback 在回答”。
- 当你还需要顺手检查 `ClaudeCode` 本地配置，避免它仍指向旧网关地址。

## Steps

1. **先读取当前 OpenClaw 配置基线，再决定是新增还是覆盖 `anyrouter`。**  
   这样做是为了避免盲写导致已有 provider、默认模型、agent 列表配置被误覆盖。  
   本次执行中先确认了：
   - 当前配置里已经存在 `anyrouter`
   - 但 `baseUrl` 仍是旧值
   - 小肠默认模型仍是 `openai-codex/gpt-5.4`

2. **按用户给定 JSON 覆盖 `models.providers.anyrouter`，并保留 `models.mode = "merge"`。**  
   保留 `merge` 可以让新 provider 配置与现有模型体系共存，而不是整块替换掉其他 providers。  
   首轮实际写入的关键字段是：
   ```json
   {
     "models": {
       "mode": "merge",
       "providers": {
         "anyrouter": {
           "baseUrl": "https://a-ocnfniawgw.cn-shanghai.fcapp.run",
           "apiKey": "[REDACTED]",
           "api": "anthropic-messages",
           "models": [
             {
               "id": "claude-opus-4-6",
               "name": "Claude Opus 4.6",
               "reasoning": true,
               "input": ["text"],
               "cost": {
                 "input": 0,
                 "output": 0,
                 "cacheRead": 0,
                 "cacheWrite": 0
               },
               "contextWindow": 200000,
               "maxTokens": 8192
             }
           ]
         }
       }
     }
   }
   ```

3. **把默认模型切到 `anyrouter/claude-opus-4-6`，并同时确认 `agents.defaults` 与 `agents.list.main` 都已对齐。**  
   只改默认值不检查 `main.model`，容易出现“默认写了但主 Agent 仍走旧模型”的假生效。  
   本次确认后的生效状态是：
   - `agents.defaults.model.primary = anyrouter/claude-opus-4-6`
   - `agents.list.main.model = anyrouter/claude-opus-4-6`

4. **记录当前密钥写入方式：是环境变量引用，还是明文写入。**  
   这是后续排查权限与可维护性问题的关键，因为“能否解析环境变量”和“key 本身是否可用”是两回事。  
   本次两种形式都出现过：
   - 环境变量版：`"apiKey": "${AnyRouterKey}"`
   - 明文版：`"apiKey": "[REDACTED]"`

5. **重启 OpenClaw，并先回答“当前小肠 Agent 是什么模型”。**  
   先确认静态配置状态，能快速回答用户最关心的问题，也为后续日志比对建立基线。  
   本次实际结论是：
   - 当前小肠 Agent：`anyrouter/claude-opus-4-6`

6. **当用户怀疑 `baseUrl` 异常时，先查日志，不要只看 JSON。**  
   因为配置写进去只说明路由目标被设置了，不代表上游网关真的兼容该协议与模型。  
   本次日志里实际出现了：
   ```text
   HTTP 500 new_api_error: invalid claude code request
   provider=anyrouter model=claude-opus-4-6
   ```
   以及：
   ```text
   OpenAI ... failed (403): <html><h1>403 Forbidden</h1>...
   ```
   随后回退为：
   ```text
   requested=anyrouter/claude-opus-4-6 ... next=openai-codex/gpt-5.3-codex
   ```

7. **基于日志判断 `fcapp.run` 链路高概率不兼容后，把 `baseUrl` 切回 `https://anyrouter.top`。**  
   这样做不是因为域名“更短”，而是因为日志已经显示原链路存在网关兼容或鉴权异常，继续保留会让所有请求落入 fallback。  
   修复后保留不变的内容：
   - `api = "anthropic-messages"`
   - 模型仍是 `claude-opus-4-6`
   - 小肠默认模型仍是 `anyrouter/claude-opus-4-6`

8. **修复后执行“真实调用验证”，不要只做静态配置检查。**  
   真实请求能区分“OpenClaw 配对了”与“上游真能回答”这两个层次。  
   本次实际验证为：
   - 对 `https://anyrouter.top/v1/messages` 发最小请求，`model=claude-opus-4-6`
   - 返回：
     - `HTTP 500`
     - `new_api_error: invalid claude code request`

9. **继续做协议对照测试：`messages`、`chat/completions`、`responses`、`models` 分开看。**  
   这是为了判断问题到底出在端点协议不匹配，还是模型只“可见不可调”。  
   本次实测结果：
   - `/v1/chat/completions` + `claude-opus-4-6` → `404 不支持该模型`
   - `/v1/responses` + `claude-opus-4-6` → `404 不支持该模型`
   - `/v1/models` 能列出模型（包含 `claude-opus-4-6`）
   - 但实际调用仍被拒绝  
   结论：**模型列表可见 ≠ 当前 key/路由可实际调用该模型。**

10. **检查 ClaudeCode 本地配置，把旧 `fcapp` 地址对齐到 `https://anyrouter.top`。**  
    这样做是为了避免 OpenClaw 已改好，但 ClaudeCode 仍指向旧地址，导致排查结果互相打架。  
    本次已修正 `~/.claude/settings.json` 中相关配置，核心对齐为：
    - `ANTHROPIC_BASE_URL = https://anyrouter.top`
    - 模型变量保持 `claude-opus-4-6`

11. **如果上游仍不可用，给出“恢复可用态”的回退方案。**  
    这是为了避免用户虽然坚持把主模型设成 opus，但实际每次都失败，影响日常使用。  
    本次实际执行过的恢复方案是：
    - 保留 `anyrouter` provider 不删除
    - 把小肠（main）默认模型切回：`openai-codex/gpt-5.4`
    - 重启 OpenClaw 使其恢复可用

12. **当用户后来手动又切回 `claude-opus-4-6` 时，再次查日志核对“配置状态”和“实际运行状态”是否一致。**  
    这一步能明确告诉用户：当前到底是主模型真在工作，还是配置虽然切了，但回答仍由 fallback 完成。  
    本次最终核对得到：
    - 配置中确实是 `anyrouter/claude-opus-4-6`
    - 日志里也确实请求了 `provider=anyrouter model=claude-opus-4-6`
    - 但随后 `HTTP 500 new_api_error: invalid claude code request`
    - 再进入 fallback：`openai-codex/gpt-5.3-codex`

## Pitfalls and solutions

❌ **只看 `openclaw.json` 已改成功，就断言模型可用**  
→ 失败原因：配置生效只说明路由目标被设置，不代表上游网关接受该协议和模型  
✅ **同时查运行日志与真实请求结果**，确认有没有 `403/500`、有没有 fallback

❌ **看到 `/v1/models` 能列出 `claude-opus-4-6`，就认为该模型可调用**  
→ 失败原因：模型可见性不等于当前 key、当前路由、当前协议端点都具备实际调用权限  
✅ **补做真实请求验证**，至少测试 `/v1/messages`

❌ **把问题简单归因于“模型不存在”**  
→ 失败原因：本次日志明确出现的是 `invalid claude code request` 与 `403 Forbidden`，更像网关兼容或鉴权异常  
✅ **按日志判断为链路/协议/权限问题**，而不是盲目改模型 ID

❌ **只改 `agents.defaults.model.primary`，不检查 `agents.list.main.model`**  
→ 失败原因：某些场景下主 Agent 仍可能保留旧模型，造成“默认值变了但实际没切过去”  
✅ **同时确认 defaults 与 main 的最终值**

❌ **修复了 OpenClaw 的 `baseUrl`，却忘了 ClaudeCode 仍指向旧网关**  
→ 失败原因：两个入口的配置不一致，会导致排查结论混乱  
✅ **顺手检查 `~/.claude/settings.json` 并对齐 `ANTHROPIC_BASE_URL`**

❌ **用户坚持保留不可用主模型时，不提供可用态恢复方案**  
→ 失败原因：系统会持续报错并依赖隐式 fallback，用户体验差且不透明  
✅ **给出两类方案：临时切回稳定主模型，或保留主模型但明确 fallback 策略**

## Key code and configuration

### 1) 初始目标配置（环境变量版）
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "anyrouter": {
        "baseUrl": "https://anyrouter.top",
        "apiKey": "${AnyRouterKey}",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-opus-4-6",
            "name": "Claude Opus 4.6",
            "reasoning": true,
            "input": [
              "text"
            ],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anyrouter/claude-opus-4-6"
      }
    }
  }
}
```

### 2) 首轮实际写入配置（fcapp.run 版）
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "anyrouter": {
        "baseUrl": "https://a-ocnfniawgw.cn-shanghai.fcapp.run",
        "apiKey": "[REDACTED]",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-opus-4-6",
            "name": "Claude Opus 4.6",
            "reasoning": true,
            "input": [
              "text"
            ],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anyrouter/claude-opus-4-6"
      }
    }
  }
}
```

### 3) 日志分析后修复的推荐配置（切回 anyrouter.top）
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "anyrouter": {
        "baseUrl": "https://anyrouter.top",
        "apiKey": "[REDACTED]",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-opus-4-6",
            "name": "Claude Opus 4.6",
            "reasoning": true,
            "input": [
              "text"
            ],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anyrouter/claude-opus-4-6"
      }
    }
  }
}
```

### 4) 本次排查中确认过的关键状态
```text
agents.defaults.model.primary = anyrouter/claude-opus-4-6
agents.list.main.model = anyrouter/claude-opus-4-6
anyrouter.baseUrl = https://anyrouter.top
```

### 5) 关键错误日志
```text
HTTP 500 new_api_error: invalid claude code request
provider=anyrouter model=claude-opus-4-6
```

```text
OpenAI ... failed (403): <html><h1>403 Forbidden</h1>...
```

```text
requested=anyrouter/claude-opus-4-6 ... next=openai-codex/gpt-5.3-codex
candidate_succeeded ... openai-codex/gpt-5.3-codex
```

### 6) ClaudeCode 需要对齐的关键配置项
```json
{
  "ANTHROPIC_BASE_URL": "https://anyrouter.top"
}
```

## Environment and prerequisites
- 已安装并可重启的 OpenClaw 环境
- 有权限读取和修改当前 `openclaw.json`
- 有权限查看 OpenClaw 运行日志
- 若需要联动排查，还需可读写 `~/.claude/settings.json`
- 上游 anyrouter 需要提供：
  - 可用 `apiKey`
  - 正确的 `baseUrl`
  - 与 `anthropic-messages` 协议兼容的路由能力
- 本次实测表明，即便 `/v1/models` 可见 `claude-opus-4-6`，仍可能无法实际调用，因此需要额外做真实请求验证