---
name: fw-trade-skill
description: 复星财富（Fosun Wealth）港美股 OpenAPI 交易总入口 skill：统一管理共享凭证 `fosun.env`（生成/修复/备份恢复），并在实盘与模拟盘间路由执行账户、资金、持仓、流水、行情、下单/撤单/改单等能力；全局单凭证 `FOSUN_ENV_PATH`，变更操作强制二次确认并遵循单步执行。
---

# fw-trade-skill

这是总入口 skill，不直接实现交易。它只负责三件事：解析共享凭证路径、确保 `fosun.env` 已由 `fosun-env-setup` 生成或修复、判断盘别后路由到实盘或模拟盘子 skill。

## 模型必须遵守

### 0. 先思考再行动（最高优先级）

每一步动作前，必须先在内部完成一轮显式思考，再决定下一步：

- 复盘已有信息：用户原话、当前共享凭证状态、上一步脚本输出（含 stderr / 退出码）、缓存里的账户索引；
- 明确这一步要回答的问题：现在到底是路由、凭证生成/修复、查询还是交易？所需参数是否齐全？
- 评估可行方案，挑最小改动 / 最少副作用 / 最少询问用户的那一条；
- 严禁基于猜测或不完整信息直接调用脚本、改写参数、跨盘别切换；
- 任何不确定项（盘别、`subAccountId`、市场/产品类型、金额方向）必须先回头问用户，不得脑补。
- 港美股交易的币种、余额和购买力彼此独立：`HKD` 余额只能用于港股，`USD` 余额只能用于美股，不能跨市场混用或替用户做换汇推断。

### 1. 先定位共享凭证

全局只使用一个共享凭证路径变量 `FOSUN_ENV_PATH`。

- 未设置时：由脚本根据自身位置解析为总 skill 根目录下的 `fosun.env` 绝对路径
- 已设置且为相对路径时：以总 skill 根目录为基准解析
- 已设置且为绝对路径时：直接使用
- 推荐写法：`FOSUN_ENV_PATH=fosun.env`，既保留可迁移性，又不会受当前工作目录影响

禁止在文档或脚本里写死某台机器的绝对路径；需要绝对路径时，只能由相对路径和环境变量在运行时解析得到。

### 2. 先确保 `fosun.env` 可用（委托子 skill）

任何实盘或模拟盘操作前，必须先完成共享凭证准备。**开通、续期、重置、回填、二维码交付、备份恢复等全部规则以子 skill `fosun-env-setup` 为准**——执行前阅读其子目录 [`fosun-env-setup/SKILL.md`](fosun-env-setup/SKILL.md)；凭据流程设计见 [`fosun-env-setup/reference/credential-management-flow.md`](fosun-env-setup/reference/credential-management-flow.md)。**禁止**在母技能中自行解释或改写凭据细节，避免与子 skill 冲突。

默认入口（已 `install.sh` 时优先 `$FOSUN_PY`）：

```bash
$FOSUN_PY fosun-env-setup/code/ensure_fosun_env.py
```

母技能只根据脚本 JSON 的 `status` 决定是否继续：

- `valid` → 可进入盘别判断与业务子 skill
- `pending` / `error` → **停手**，严格按子 skill 返回的 `operation_guide`、`user_message`、`next_action` 执行，不得跳过 env-setup 直接跑交易脚本

### 3. 再判盘别

凡是涉及以下任一金融相关操作，都必须确认用户这次是`实盘`还是`模拟盘`：

- 查询账户 / 资金 / 持仓 / 流水
- 查询订单
- 下单 / 撤单 / 改单
- 查询行情
- 任何需要 `subAccountId` 的证券操作

如果用户没有明确回答，禁止继续执行。禁止根据账户类型、脚本名或历史上下文替用户猜盘别。

### 4. 凭证体检与路由

- 用户选择`实盘`：
  1. 使用 `real-trade-skill`。
  2. 只读取同一个 `FOSUN_ENV_PATH` 指向的共享 `fosun.env`。
  3. 凭证未 `valid` 时，先按 `fosun-env-setup` 子 skill 处理，不得直接跑实盘脚本。
  4. 实盘变更操作必须先复述完整意图并获得用户明确确认。

- 用户选择`模拟盘`：
  1. 使用 `moni-trade-skill`。
  2. 只读取同一个 `FOSUN_ENV_PATH` 指向的共享 `fosun.env`。
  3. 凭证未 `valid` 时，先按 `fosun-env-setup` 子 skill 处理，不得直接跑模拟盘脚本。
  4. 模拟盘不得生成、复制或维护第二份凭证。

## 子 skill 职责

### `fosun-env-setup`

- 共享凭证的**唯一**生成、修复与引导入口；命令、场景、回填、续期/重置规则见其 `SKILL.md` 与 `reference/`
- 不执行交易业务；母技能不得重复描述凭据流程

### `moni-trade-skill`

- 模拟盘子 skill
- 不生成、不修复共享凭证
- 直接复用 `FOSUN_ENV_PATH` 指向的共享凭证
- 只负责执行模拟盘接口

### `real-trade-skill`

- 实盘子 skill
- 直接复用 `FOSUN_ENV_PATH` 指向的共享凭证
- 只负责执行实盘接口
- 任何下单、改单、撤单等变更动作都必须先确认用户明确选择实盘，并完成二次确认

## 最简执行顺序

1. 按 **`fosun-env-setup` 子 skill** 完成凭证准备，直至 `ensure_fosun_env.py` 输出 `status=valid`
2. 确认用户选择 `实盘` 还是 `模拟盘`
3. 路由到 `real-trade-skill` 或 `moni-trade-skill`（全程同一 `FOSUN_ENV_PATH` / `fosun.env`）

## 一键安装（组合技能共用）

在 **总 skill 根目录**执行（模拟盘 / 实盘 / env-setup 共用同一份 venv 与 fsopenapi）：

```bash
bash install.sh
```

- 虚拟环境默认：`fw-trade-skill/.venv`（可用 `FW_TRADE_VENV` 覆盖；兼容旧名 `MONI_VENV`）
- SDK 缓存默认：`fw-trade-skill/.cache/`
- 安装完成后导出 `FOSUN_PY`（`MONI_PY` / `REAL_PY` 与之相同，兼容旧速抄表）

子目录下的 `moni-trade-skill/install.sh`、`real-trade-skill/install.sh` 仅为兼容入口，会转调本脚本。

## 目录结构

```text
fw-trade-skill/
├── _meta.json                      # 母技能版本（pack.sh 打包用）
├── SKILL.md
├── install.sh                      # 组合技能共享安装（venv + fsopenapi）
├── .venv/                          # 默认虚拟环境（git 忽略，install.sh 生成）
├── fosun.env                       # 默认共享凭证落点（未设置 FOSUN_ENV_PATH 时使用）
├── fosun-env-setup/                # 共享凭证生成与修复
├── real-trade-skill/               # 实盘 skill
└── moni-trade-skill/               # 模拟盘 skill
```
