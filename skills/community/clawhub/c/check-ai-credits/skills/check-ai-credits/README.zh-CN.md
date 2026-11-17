# check-ai-credits

[English](README.md) · **简体中文**

**一个命令查 10 家 AI provider 还剩多少 credit/balance。**
Check AI provider credits and balance across 10 providers from one CLI —
DeepSeek、DeepInfra、Codex (ChatGPT)、Grok、MiMo、Claude、Gemini、Kimi、
OpenRouter、apikey.fun，附带烧钱趋势和预计可用天数。

- 单文件静态二进制（TypeScript + Bun），零运行时依赖
- 自动发现本地凭据（环境变量、CLI auth store、CodexBar）
- 只读：绝不刷新/改写 OAuth token，绝不打印密钥
- 统一 snapshot schema → `--json` 直接进 dashboard/cron

## 安装

```bash
# 作为 skill 安装（任意支持 Agent Skills 的 agent）
npx skills add mfang0126/check-ai-credits

# 从源码构建（需要 Bun >= 1.1）
# 克隆本仓库（ssh 或 https 均可），然后：
cd check-ai-credits && bun install && bun run build   # -> dist/check-ai-credits
```

## 60 秒上手

```bash
check-ai-credits                 # 查所有已配置 provider
check-ai-credits deepseek        # 查单个
check-ai-credits --json          # 机器可读快照
check-ai-credits --trend         # 烧钱速率 + 预计用完天数
check-ai-credits --list          # 每个 provider 的凭据检测状态
check-ai-credits deepinfra --models  # DeepInfra 按模型月明细
```

## Provider 矩阵

| Provider | ID | 凭据来源（自动探测） | 指标 |
|---|---|---|---|
| DeepSeek 官方 | `deepseek` | `DEEPSEEK_API_KEY`（env / agent env 文件） | 钱包余额 USD |
| DeepInfra | `deepinfra` | `DEEPINFRA_API_KEY`（env / agent env 文件） | 预付池、月消费 |
| Codex (ChatGPT) | `codex` | `~/.codex/auth.json`（Codex CLI，只读） | credits + 限速窗口 |
| Grok (xAI) | `grok` | `~/.grok/auth.json`（Grok CLI，只读） | 月度 credits + 预付 |
| Xiaomi MiMo | `mimo` | `MIMO_COOKIE` env，否则 CodexBar 兜底 | CNY 余额 + 套餐 |
| Claude | `claude` | CodexBar usage | 窗口已用 % |
| Gemini | `gemini` | CodexBar usage | 窗口已用 % |
| Kimi | `kimi` | CodexBar usage | 窗口已用 % |
| OpenRouter | `openrouter` | CodexBar usage | 窗口已用 % |
| apikey.fun 中转 | `apikeyfun` | CodexBar 插件 | 组共享钱包余额 |

凭据缺失的 provider 报 `not configured` + 登录/设置 URL，不会拖垮整次运行。

## 凭据解析（按 provider，顺序）

1. 进程环境变量
2. agent 的 env 文件（如 Hermes 的 `$HERMES_HOME/.env`，从不 export）
3. 本地 CLI auth store（`~/.codex/auth.json`、`~/.grok/auth.json`）—— **只读**
4. CodexBar CLI（macOS 菜单栏应用）承载的 web-session provider
5. 交互兜底：打印登录 URL 并以非零码退出

安全红线（写死在代码里）：绝不刷新 OAuth access token（刷新会轮换 CLI 自己的
refresh token、把用户踢下线）；任何输出模式都不回显密钥；零遥测。

## 证据

| 能力 | 验证方式 |
|---|---|
| 余额语义正确 | 与独立实现（legacy Python 直连脚本）同端点对拍一致：DeepSeek 余额、DeepInfra spendable/month 完全相同 |
| 趋势算法 | 40 个 fixture 单测覆盖 7 天最小二乘、reset 裁剪、LOW 阈值（`bun test`） |
| 端点真实性 | DeepSeek `GET /user/balance`（[platform.deepseek.com](https://platform.deepseek.com)）、DeepInfra `/payment/checklist`（[deepinfra.com/dash](https://deepinfra.com/dash)）等均实测通过 |
| 类型安全 | TypeScript strict `tsc --noEmit` 零错误 |

## 仓库结构

```
SKILL.md            # skill 入口（frontmatter ≤60 字符 description）
src/
  cli.ts            # CLI 入口
  types.ts          # 统一 snapshot schema + Provider 接口
  core/             # env/http/auth/codexbar/trend/log
  providers/        # 每个 provider 一个 adapter
  registry.ts       # 10 provider 注册表
  format.ts         # 人类可读输出格式化
test/               # bun:test fixture 单测（不打真 API）
docs/MIGRATION.md   # 端点语义与单位坑位对照表
README.zh-CN.md     # 本文档中文版
```

## JSON snapshot schema

```jsonc
{
  "provider": "deepseek",
  "source": "api",
  "timestamp": "2026-09-24T00:00:00.000Z",
  "currency": "USD",
  "balance": 12.34,
  "usedPercent": null,
  "resetsAt": null,
  "monthCost": null,
  "monthPeriod": null,
  "details": { },     // provider 特有扩展字段
  "error": null
}
```

## 趋势日志

快照默认追加到 `~/.check-ai-credits/log.json`（可用 `$CHECK_AI_CREDITS_LOG`
覆盖）。`--trend` 在 7 天窗口内做最小二乘烧钱速率拟合、裁掉上次 reset 之前的
配额序列，并标记低余额（USD 钱包 < 5，或剩余 < 20%）。`--no-log` 跳过追加。

## 开发

```bash
bun run typecheck   # tsc --noEmit，strict
bun test            # fixture 单测（不打真 API）
bun run build       # 单文件二进制
```

新增 provider = 在 `src/providers/` 写一个实现 `Provider` 接口
（`detect()` + `fetch()`）的文件，再在 `src/registry.ts` 注册一行。

## License

MIT
