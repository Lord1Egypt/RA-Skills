# ClawTune Skill Package

这是 ClawTune skill 的脚本化工作目录。现在的重点已经不是只搭结构，而是把 playlist → draft → order → recovery 这条主链路尽量收进稳定脚本里，让宿主优先调用脚本而不是临场拼 curl。后续流程应由 ClawTune 网页承接，skill 只负责给继续入口与完成后的状态恢复。

## 当前目录

```text
skills/clawtune/
├── SKILL.md
├── README.md
├── TEST_PROMPTS.md
├── scripts/
│   ├── _common.sh
│   ├── session-state.sh
│   ├── auth-bootstrap.sh
│   ├── api-request.sh
│   ├── generate-playlist.sh
│   ├── create-draft.sh
│   ├── update-draft.sh
│   ├── recommend-draft.sh
│   ├── create-order.sh
│   ├── check-order-status.sh
│   ├── check-order-delivery.sh
│   ├── check-public-result.sh
│   ├── recover-order.sh
│   └── main-flow-smoke.sh
├── references/
│   ├── api-playbook.md
│   ├── scenario-playbook.md
│   ├── curl-auth.md
│   ├── curl-api-calls.md
│   └── curl-recovery.md
├── examples/
│   └── usage-examples.md
└── evals/
    └── evals.json
```

## 脚本分工

### 基础层
- `auth-bootstrap.sh`：确保 `auth.json` 可用，必要时 bootstrap / refresh
- `api-request.sh`：统一带 token 发请求
- `_common.sh`：JSON 断言、evidence 写入、session snapshot、idempotency helper
- `session-state.sh`：统一读写 `session.json`

### 主流程脚本
- `generate-playlist.sh`：生成歌单并把主锚点切到 `playlist`
- `create-draft.sh`：创建创作草案并写入 `draft_id`
- `update-draft.sh`：补充草案字段
- `recommend-draft.sh`：拿草案推荐方向
- `create-order.sh`：创建订单并把主锚点切到 `order`
- `check-order-status.sh`：查询订单聚合状态
- `check-order-delivery.sh`：查询交付状态，拿到 `playlist_id` 时切到结果歌单
- `check-public-result.sh`：查询公开结果页或公开歌单页接口
- `recover-order.sh`：围绕 `order_id` 恢复链路，并优先拿回结果歌单
- `main-flow-smoke.sh`：串起整条 smoke 路径

## 现在的推荐使用顺序

宿主执行时，优先按下面顺序走：
1. `auth-bootstrap.sh ensure`
2. `generate-playlist.sh`
3. `create-draft.sh`
4. `update-draft.sh`
5. `recommend-draft.sh`
6. `create-order.sh`
7. 把继续入口给用户，由网页继续后续流程
8. `check-order-status.sh`
9. `check-order-delivery.sh`
10. `recover-order.sh`
11. 如果已经拿到 `playlist_id`，再 `check-public-result.sh playlist`

## Evidence 目录

所有脚本都支持把完成证据落到 `CLAWTUNE_EVIDENCE_DIR`。

默认 smoke 目录：
- `$TMPDIR/clawtune-script-evidence-<timestamp>`（若未设置则回退到系统临时目录）

本轮人工验证目录：
- `clawtune-script-evidence-20260317-164742`（目录名示例）

其中已经包含：
- 线上发布日志 `release-prod.log`
- nginx 修复日志 `nginx-api-prefix-fix.txt`
- 线上健康检查与 bootstrap 结果
- Prisma migration / db push 结果
- 多轮 `main-flow-smoke` 执行日志
- 每一步脚本的 response / payload / session snapshot

## 已验证到的主流程结果

当前线上已经验证：
- `GET /api/v1/health` 正常
- `POST /api/v1/bootstrap` 正常
- playlist / draft / order / status / delivery / recover 这条链路可跑通
- 真实网页完成与后续选择由网页负责，因此脚本 smoke 不再覆盖网页内动作

这意味着现在的 smoke 结果是“订单创建后到结果恢复链路已验证”，而不是“生产环境下的完整生成交付已自动完成”。

## 常用入口

```bash
# 1) 确保本地凭证可用
bash scripts/auth-bootstrap.sh ensure

# 2) 统一鉴权请求
bash scripts/api-request.sh GET /content/facets

# 3) 跑整条 smoke，并把日志落到指定目录
CLAWTUNE_EVIDENCE_DIR="${TMPDIR:-/tmp}/clawtune-script-evidence-manual" \
  bash scripts/main-flow-smoke.sh

# 4) 完成后恢复
bash scripts/recover-order.sh
```

## 注意

这套脚本的目标是让主流程稳定，不是把所有生产运营动作都自动化掉。
当前要特别记住三件事：
- 对外 API 基址使用 `https://clawtune.aqifun.com/api/v1`
- 主锚点切换始终遵守 `playlist_id -> draft_id -> order_id -> playlist_id(结果歌单)`
- 后续选择与页面内动作由网页承接，skill 不应在聊天里继续下探网页内部流程
- 下单链路对 skill 只暴露线上正式继续入口，不暴露网页内部选择细节或非正式地址
- 完成后的用户主去向是生成好的结果歌单页，不是其他页面对象
