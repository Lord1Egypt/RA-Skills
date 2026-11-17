# Fetch Solana Logs（中文）

> 英文主文档：[SKILL.md](SKILL.md)（含触发 description，agent 发现技能以英文版为准）  
> 本文件是完整中文操作说明，与英文版行为一致。

**Agent 优先执行：** 用户要拉某个 Solana 地址的 tx 时，**不要只解释**——校验地址后立刻写配置并开始拉取。

```
用户给出地址
  → 用 isSolanaAddress 校验（必须通过）
  → 确保项目存在（没有则 scaffold）
  → 写入 target_solana_addr.json
  → 确保 .env（HELIUS_API_KEY）
  → pnpm s1 → pnpm s2
  → 汇报 output 路径
```

## 何时使用（触发）

用户类似以下说法时，立刻启用本 skill：

| 用户说法 | 动作 |
|----------|------|
| 「帮我获取 / 拉取某个 Solana 地址的 tx」 | 自动配置并拉取 |
| 「帮我拉这个 program 的交易 / instruction」 | 自动配置并拉取 |
| 「fetch txs for `<base58>`」 | 自动配置并拉取 |
| 粘贴 Solana 地址并要历史 / 日志 | 自动配置并拉取 |

**不要用于：** EVM 日志（→ `fetch-evm-logs`）、纯统计分析、或不需要拉 tx 的一般 Solana 问答。

## Agent 必须执行的行为

用户给出地址后，按下列步骤执行。**校验未通过前禁止拉取。**

### 0. 校验地址（`isSolanaAddress`）——最先做

使用项目内方法（**不要自己发明校验逻辑**）：

```typescript
import { isSolanaAddress } from './src/utils/utils';
isSolanaAddress(addr) // 必须为 true
```

或运行：

```bash
pnpm validate -- --addr <ADDR>
# 或写完 JSON 后：
pnpm validate
```

- 若为 `false` / 非零退出 → **停止**，告知用户不是合法 Solana 地址，请其提供正确的 base58 pubkey。**不要**写入 `target_solana_addr.json`，也不要跑 s1。
- `s1`/`s2` 内部还会通过 `common.ts` 的 `validateAddresses` 再拦一层。

### 1. 确保项目就绪

若当前目录（或约定目录）已有 `src/tx_logs/s1.pull.tx.ts`，直接用。

否则脚手架：

```bash
bash ~/.cursor/skills/fetch-solana-logs/scripts/init-project.sh [target_dir]
cd [target_dir]
```

默认目录：`./fetch_solana_logs`。

### 2. 写入 `target_solana_addr.json`

**仅在** `isSolanaAddress` 通过后，把用户地址写入项目根目录：

```json
["DLvbp3sZCdoK6FoGnMdLSP2NZCCZdVfSGHD8KAGazZQH"]
```

规则：

- 多个地址 → JSON 数组；每个都必须通过 `isSolanaAddress`
- 用户换了新地址 → 按语义替换或追加（默认：写成用户刚给出的地址列表）

### 3. 确保 `.env`

可靠拉取需要 `HELIUS_API_KEY`。

- 若用户提供了 `HELIUS_API_KEY`，立刻在目标项目下创建 `.env` 并写入：

  ```dotenv
  HELIUS_API_KEY=<user-provided-key>
  ```

- Key 只写到正在操作的项目目录；不要写进 skill 目录，也不要在日志/回复里打印 Key
- 若 `.env` 已存在，只更新 `HELIUS_API_KEY`，保留其他无关配置
- 若没有 `.env` 且用户没给 Key → 从 `.env.example` 复制
- 若 Key 为空 → **只问一次**，写入后再继续
- 若用户没有 Key → 仍可用 `--limit` 走公共 RPC，并提示可能限流

脚手架时若 Key 已就绪，通过环境变量传入，让 `init-project.sh` 自动生成 `.env`：

```bash
HELIUS_API_KEY="$HELIUS_API_KEY" \
  bash ~/.cursor/skills/fetch-solana-logs/scripts/init-project.sh [target_dir]
```

### 4. 立刻拉取并解析

新请求且用户未要求全量历史时，默认：

```bash
pnpm s1 -- --limit 50
pnpm s2
```

地址从 `target_solana_addr.json` 读取。

覆盖场景：

| 用户意图 | 命令 |
|----------|------|
| 最近 N 条 | `pnpm s1 -- --limit N` 再 `pnpm s2` |
| JSON 里有多个地址、只拉其中一个 | `pnpm s1 -- --addr <ADDR> --limit 50`，s2 同理 |
| 全量历史（需要 Helius） | `pnpm s1`（不要 `--limit`）再 `pnpm s2` |
| 清空重拉 | 删除 `output/<addr>/` 后再 s1/s2 |

### 5. 汇报结果

告知用户：

- 写入了哪些地址到 `target_solana_addr.json`
- `output/<addr>/` 下的输出路径
- IDL 是否已自动保存；若 program **没有**链上 IDL 且需要解码，向用户要 IDL JSON，写入 `output/<addr>/idl_<addr>.json`，再跑一次 `pnpm s2`

## 若缺少地址

用户只说「帮我获取 Solana 的 tx」但**没给地址** → 只问：

> 请提供 Solana 地址（base58）。

然后直接进入步骤 2–5。**不要**一上来问一堆无关选项。

## IDL 说明

- `s1` 会自动尝试链上 Anchor IDL → `output/<addr>/idl_<addr>.json`
- 可选探测：`node ~/.cursor/skills/fetch-solana-logs/scripts/probe-idl.mjs --addr <ADDR>`（在项目内 `pnpm install` 之后运行）
- **禁止编造** IDL

## 输出目录结构

```
output/<addr>/
  ├── idl_<addr>.json              # 有则保存 / 用户提供
  ├── tx_logs_<addr>.txt           # s1 NDJSON
  └── tx_logs_parsed_<addr>.json   # s2（有 IDL 时可含 parsed instruction）
```

## Checklist（Agent）

```
- [ ] isSolanaAddress(addr) === true（pnpm validate）
- [ ] 项目就绪（已有或 init-project.sh）
- [ ] 地址已写入 target_solana_addr.json
- [ ] .env 中有 HELIUS_API_KEY（或已说明走公共 RPC）
- [ ] pnpm s1（默认 --limit 50）完成
- [ ] pnpm s2 完成
- [ ] 已告知用户输出路径 / IDL 状态
```

## 常见坑

- 非法地址 → 校验失败；禁止写入/拉取
- 传参必须用 `pnpm s1 -- --limit 50`（`--` 在 flags 前）
- 不加 `--limit` 的全量同步需要 Helius
- 钱包 / 非 Anchor program 可能没有 IDL —— 仍可正常拉 tx

## 相关资源

- [SKILL.md](SKILL.md)（英文主文档）
- [scripts/init-project.sh](scripts/init-project.sh)
- [scripts/probe-idl.mjs](scripts/probe-idl.mjs)
- [reference.md](reference.md)
- [examples.md](examples.md)
