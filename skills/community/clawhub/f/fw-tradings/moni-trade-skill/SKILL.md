---
name: moni-trade
description: 复星财富港美股模拟盘 OpenAPI skill。通过 `FOSUN_ENV_PATH` 复用共享凭证；未设置时自动解析到总 skill 根目录的 `fosun.env`，只执行模拟盘接口，不负责凭证生成或修复。
version: 1.8.0
requires:
  bins:
    - bash
    - curl
install: install.sh
---

# moni-trade — 复星模拟盘 OpenAPI Skill

这是模拟盘子 skill。只负责执行模拟盘接口，直接复用 `FOSUN_ENV_PATH` 指向的共享凭证；未设置时自动解析到总 skill 根目录 `fosun.env`。

> **本文件设计原则**：只放"模型决策时必须知道"的内容（安全规则、决策树、错误码处置）。
> 每个脚本的详细参数请直接 `脚本.py --help` 查阅，文档不重复维护，**避免文档与代码脱节**。

## 合法脚本清单（18 个业务脚本 + 2 个内部模块，封闭集合，跑命令前先逐字符核对）

> ⚠️ **本表是工具箱总目录**，刻意放在所有铁律之前 —— 模型即使只读到这里也必须先记住：**清单之外的所有脚本名都是脑补**。
> 命名规则统一是 **`<domain>_<action>.py`**（唯一例外：`sync_accounts.py`，历史遗留 action_domain 顺序，**不要泛化**）。

| domain | 脚本（精确文件名） | 一句话作用 |
|---|---|---|
| **meta** | `account_list.py` | 列账户（顺带刷账户索引） |
| **meta** | `sync_accounts.py` | **唯一例外**：强刷账户索引（action_domain 顺序，历史遗留，不要泛化） |
| **meta** | `check_shared_env.py` | 共享凭证体检 |
| **账户（变更）** | `sim_account_create.py` | 创建模拟账户（必带 `--confirm`） |
| **账户（变更）** | `sim_account_reset.py` | 重置模拟账户（必带 `--confirm`；旧账户会被禁用） |
| **资产** | `cash_summary.py` | 现金/购买力 |
| **资产** | `holdings.py` | 持仓 |
| **资产** | `cash_flows.py` | 资金流水 |
| **交易（变更）** | `order_create.py` | 下单（必带 `--confirm`） |
| **交易（变更）** | `order_modify.py` | 改单（必带 `--confirm`；**不是** `modify_order.py`） |
| **交易（变更）** | `order_cancel.py` | 撤单（必带 `--confirm`；**不是** `cancel_order.py`） |
| **交易（查询）** | `order_list.py` | 订单列表（可按市场/标的/日期/状态筛选） |
| **行情** | `market_quote.py` | 实时报价 |
| **行情** | `market_orderbook.py` | 盘口 |
| **行情** | `market_kline.py` | K 线 |
| **行情** | `market_min.py` | 分时 |
| **行情** | `market_tick.py` | 逐笔成交 |
| **行情** | `market_broker_list.py` | 经纪商队列 |
| **内部** | `_client.py` | 公共 SDK 工厂 + 错误处理（**不直接调用**） |
| **内部** | `_traps.py` | 脑补陷阱共享 helper（**不直接调用**） |

> **常见脑补黑名单**（v1.7.2 起这些名字已被 trap stub 接住，跑了直接吐结构化 `WRONG_SCRIPT_NAME`，**不再是 OS-level No such file**）：
> `modify_order.py` → `order_modify.py` / `cancel_order.py` → `order_cancel.py` / `create_order.py` → `order_create.py`
> `list_orders.py` / `query_orders.py` → `order_list.py` / `get_holdings.py` / `query_holdings.py` → `holdings.py`
> `get_cash.py` / `query_cash.py` → `cash_summary.py` / `cancel.py` / `modify.py` → 对应 `order_*.py`
> `buy.py` / `sell.py` → `order_create.py`（用 `--direction 1/2` 区分买卖）
> 跑这些 trap 后，**直接照 stderr 里的 `intended_script` 字段替换脚本名重试即可，禁止再猜其它名字**。

## 第 0 条铁律：单步原则（最高优先级，违反 = bug）

**一次用户请求，原则上只跑一个脚本。** 拿到结果先汇报，等用户给下一个明确指令再继续。

| 类型 | 示例脚本 | 跑完后允许做什么 |
|---|---|---|
| **meta 查询**（账户/凭证体检/同步） | `account_list` / `sync_accounts` / `check_shared_env` | **只汇报、停手**；禁止自动接 `cash_summary` / `holdings` / `cash_flows` / `order_*` |
| **账户变更**（创建/重置模拟账户） | `sim_account_create` / `sim_account_reset` | 跑完汇报新账户、初始现金和缓存刷新结果，然后停手；禁止自动接交易/资产脚本 |
| **业务查询**（钱/股/单/流水/行情） | `cash_summary` / `holdings` / `cash_flows` / `order_list` / `market_*` | **只汇报、停手**；禁止基于查询结果脑补"那就帮你下单/改单/撤单" |
| **业务变更**（下单/改单/撤单） | `order_create` / `order_modify` / `order_cancel` | 跑完汇报结果，不允许"成功了我再给你跑一遍 holdings 看看"这种自动连环 |

例外（允许自动连一步）：
- 业务脚本报"账户类错误"→ `_client.py` 内部已自带刷缓存重试，模型不需要也不允许手动接 `account_list`。
- 用户原话明确串了多个动作（如"列账户再查余额"），按用户原话顺序逐个跑、逐步汇报。

**先读 stdout 顶层 `next_action` 字段再行动**（v1.7.3 起**所有查询/行情/交易脚本** stdout JSON 顶层一定带 `next_action`，是模型必须遵守的下一步指令，**优先级高于本节其它说法**）。

> **抗长会话衰减说明**：本文件在长会话中会因为 LLM 注意力机制被"挤压"，模型可能记不清第 0 条铁律。
> 但**每跑一次脚本，stdout 顶层 `next_action` 都是 stateless 的**，会被新鲜地喂到模型嘴边，
> 等于把"单步原则"在每条命令的输出里**重新灌一遍**。所以无论会话多长，**只要模型把 stdout 完整读完、按 `next_action` 行动**，第 0 条铁律就不会失效。
> 这是当前体系下最强的抗衰减武器，**不要忽视任何一次 stdout 的 `next_action`**。

## 第 1 条铁律：禁脑补（参数 + 脚本名都不许猜）

### 1.1 参数维度
`subAccountId` / `direction` / `quantity` / `price` —— 任意一个不确定，立刻停手问用户，**严禁瞎填默认值**。下单/改单/撤单的市场维度统一用 `--market hk|us` 简写（脚本会自动展开成对应的 market_code/currency/product_type，零脑补、零拼错）；高级用户也可显式三件套，但和 `--market` 互斥，本地会直接拦截。

#### 1.1.1 「标的代码」参数名抗脑补三层防御（v1.7.4 起）
跨脚本"标的代码"参数名历史上叫法不一（行情用 `--code`、交易用 `--stock-code`、持仓用 `--symbols`），是模型脑补 `--ticker` / `--instrument` / `--stocks` 这种罕见名的根本诱因。v1.7.4 起加了三层兜底：

- **L1 · argparse alias**：所有相关脚本现在都同时接受 4 个官方 alias `--code` / `--stock-code` / `--symbol` / `--symbols`，模型用其中任一个都能跑通（每个脚本仍有"主名"，但只用于 help 文案）。
- **L2 · 智能 hint**：模型用了 4 个之外的脑补名（如 `--ticker` / `--instrument` / `--stockcode` / `--stocks`），脚本会回 `INVALID_PARAM` 并精准指出脑补名、给出"立刻改成 `--code` / `--stock-code`"的指引；这是兜底，**不要依赖、首先要走 L1 / L3**。
- **L3 · `--args-json` 模板**（首选）：见文首「JSON 填空模板」一节，模型从模板复制、按规则填值，**根本没有"想参数名"的环节**，彻底消除脑补窗口。

> **三层是冗余防御不是替代**：JSON 模板（L3）是默认首选；CLI 写法用 alias（L1）兜底；万一模型还是写出罕见脑补名，智能 hint（L2）会引导回正轨。

#### 1.1.2 「标的代码」**值**自动规范化 + silent fail 兜底（v1.7.5 起）
1.1.1 治了"参数名"维度的脑补；v1.7.5 接着治"参数值"维度——模型对市场前缀（hk/us）的拼接同样容易脱节。

- **L1 · 自动规范化**（事前）：行情/持仓/订单查询脚本在 `parse_args()` 之后调用 `normalize_security_code`：
  - `01810` / `01810`（前导）/ `700`（不足 5 位）→ 自动补 `hk` 前缀 + 前导 0 → `hk00700`
  - `AAPL` / `aapl` / `Aapl` → 自动补 `us` 前缀 + 大写 → `usAAPL`
  - `HK.01810` / `US.AAPL` / `us.aapl` 点分写法 → 自动归一化
  - 已带合法前缀（`hk` / `us` / `sh` / `sz`）→ 原样保留
  - 无法推断的格式（如 `123456` 6 位数字）→ 原样转给 SDK，失败时由 L2 兜底
- **交易下单主路径必须用纯代码**：`order_create.py` 遵循 `OrderCreate.md`，请求体已有 `marketCode`，所以模型从一开始就应生成 `marketCode=hk, stockCode=00700` / `marketCode=us, stockCode=AAPL` 这种格式。CLI 写法对应为 `--market hk --stock-code 00700`、`--market us --stock-code AAPL`，**不要主动拼 `hk00700` / `usAAPL` 给下单脚本**。`normalize_trade_stock_code()` 只做意外兜底：若误传 `hk00700` / `HK.00700` / `usAAPL`，脚本会按 `--market` 校验后剥离前缀；若代码前缀和 `--market` 冲突，本地直接拦截。
- **L2 · silent fail 兜底**（事后）：实测发现 SDK 对"看似合法但实际不存在"的代码会返回 `{ok:true, code:0, data:null, message:"success"}`（**比报错危险 10 倍**——模型读 ok=true 会以为成功，可能凭空编数字）。`dump_with_directive` 在输出层强制识别这种"成功外壳 + 空 data"模式，重写为 `SILENT_FAIL_EMPTY_DATA` 结构化错误。

> **直接受益**：模型听到用户说"查 01810 现价"，可以**原样**传 `--code 01810` 或 `{"code":["01810"]}`，不用做"先判断市场再拼前缀"的认知动作。
> **真不存在的代码**也会被精准拦截而不是 silent 编数，对用户负责。

### 1.2 脚本名维度（v1.7.2 加固，**双层防御**）
**只许使用「合法脚本清单」里精确出现的文件名，禁止按英文动宾习惯反推。**

本 skill 的命名规则统一为 **`<domain>_<action>.py`**（domain 在前、action 在后）：
- ✅ 正确：`order_create.py` / `order_modify.py` / `order_cancel.py` / `order_list.py`
- ❌ 错误（**这些文件根本不存在**）：`create_order.py` / `modify_order.py` / `cancel_order.py` / `list_orders.py` / `query_holdings.py` / `get_cash.py` / `cancel.py` / `modify.py` / `buy.py` / `sell.py`

> **唯一例外**：`sync_accounts.py`（历史遗留，action_domain 顺序）—— **这是孤例，不要泛化推断其它脚本可以反着写**。

#### 双层防御机制
- **L1（事前）**：跑命令前先在「合法脚本清单」里逐字符核对脚本名
- **L2（运行时强制兜底）**：13 个最常被脑补的错名（上面 ❌ 列表）已被 `code/` 目录里的 **trap stub 接住**——即使模型完全不读 SKILL.md、直接靠拼写直觉跑命令，也会立刻得到结构化 `WRONG_SCRIPT_NAME` 错误，里面带 `intended_script` 字段直接指向正确脚本名，模型读了 `next_action` 应当**立刻把命令里的错名改成 `intended_script` 重试**，不要再猜其它脚本名

> 只有在用户用了**清单外的、连 trap 都没覆盖到的**罕见错名（如 `update_order.py` / `place_order.py`）时，才会落到 OS-level `No such file or directory`——此时按错误处置矩阵执行（停手 + `ls $SKILL/code/*.py` 核对 + 回查清单）。

## 第 2 条铁律：变更操作二次确认（v1.7.3 起改为「argparse 强制 intent + ensure_user_confirmed 验证 confirm」三层防御）

**任何下单 / 改单 / 撤单 / 创建模拟账户 / 重置模拟账户，模型必须分三步走，禁止"打了就跑"：**

1. **在对话里先复述意图**：用自然语言把完整变更意图整段复述给用户，**不省略任何关键字段**：
   - 下单：操作（买/卖）+ 市场（港股/美股）+ 标的（含中文名最好）+ 数量 + 价格（市价单说明不传价格）+ 订单类型（只能是限价/市价）
   - 改单：要改的 orderId + 市场 + 修改类型 + 要修改的字段（数量/价格）
   - 撤单：要撤的 orderId + 市场 + 该订单的标的/方向/数量/订单类型/关键条件摘要
   - 创建模拟账户：说明会新建模拟证券账户，并初始化 HKD/USD 各 100 万现金
   - 重置模拟账户：说明旧模拟账户 ID、旧账户会被禁用、会创建新账户，并初始化 HKD/USD 各 100 万现金；重置间隔 7 天
2. **再明确反问**："以上信息确认执行吗？"——**等用户给出明确肯定**才能执行。
3. **执行命令时把同一段复述填到 `--intent`**（**v1.7.3 必传**）：脚本会把 intent 原样打印到 stdout，长会话再衰减用户也能立刻看到模型理解的意图、错了立刻纠。

**何为"明确肯定"**（白名单，命中才放行）："确认 / 是 / 是的 / 下吧 / 执行 / 撤 / 改 / 走 / yes / ok / go / 没问题 / 对" 等。
**何为"未确认"**（拒绝执行，再问一次）："嗯 / 可以吧 / 看着办 / 应该是吧 / 你决定 / 随便 / 都行" 等模糊词，以及任何带"如果/或者/也许/可能"的条件式回答。

**运行时三层防御（即使模型漏看本节铁律也兜底）**：
- L1 `--intent` `required=True` —— 模型不带就 argparse `INVALID_PARAM` 拦截，**复述意图变成 schema 强制项**
- L2 `--confirm` 必须为 True —— 模型在用户明确确认前禁止带 `--confirm`；不带就 `NEED_CONFIRMATION` 拦截，**且错误信息里会回显 `--intent` 内容**让用户校验
- L3 stdout 顶层 `intent` 字段 —— 执行成功的 stdout 也会原样回显 intent，便于审计

> 这条铁律覆盖**所有有副作用的变更操作**（即使用户原话已经给了完整参数，仍然要先复述+反问、再带 `--intent + --confirm` 执行）。模拟盘也按真实流程演练，培养肌肉记忆，避免接实盘时误操作。

## JSON 填空模板（v1.7.4 · 反脑补终极方案 · 首选用法）

> **为什么必须首选 JSON 模板**：v1.7.4 起所有业务脚本统一支持 `--args-json '<JSON>'`。
> 模型只需要 ① 复制对应模板 → ② 把 `<...>` 占位符换成实际值 → ③ 一行命令直接跑。
> **不用想参数名 / 不用想必填项 / 不用想顺序**——长会话里最容易脑补的"参数名"维度被完全消除。
>
> 跟下面「零思考速抄表」的传统命令行写法 **100% 等价**，可任选一种；新会话推荐 **JSON 模板**。

**通用调用形式**（所有脚本统一）：

```bash
$MONI_PY $SKILL/code/<脚本名>.py --args-json '<填好的 JSON 对象>'
```

**机械翻译规则**（脚本内部自动做，模型只需要按规则填 JSON）：
- `"code"` → `--code`；`"stock_code"` 或 `"stock-code"` → `--stock-code`（下划线自动转中划线）
- `true` → 只放 flag 名（覆盖 `store_true` 类，如 `confirm` / `active-only`）
- `false` / `null` → 跳过该字段
- 数组 → 重复展开（`["a","b"]` → `--key a --key b`）
- 数字裸传，字符串脚本会自动加引号

> **v1.7.5 起：查询/行情类标的代码可以直接用「用户原话格式」**——不用再拼市场前缀。
> 脚本侧会自动规范化：`"01810"` → `hk01810`、`"00700"` → `hk00700`、`"700"` → `hk00700`（前导补 0）、
> `"AAPL"` → `usAAPL`、`"aapl"` → `usAAPL`、`"HK.01810"` → `hk01810`、`"US.AAPL"` → `usAAPL`。
> 模型听到用户说"查 01810 现价"，直接 `{"code":["01810"]}` 即可，**不用想这是港股还是美股**。
> 如果代码格式实在异常无法推断，会触发 `SILENT_FAIL_EMPTY_DATA` 错误（v1.7.5 兜底，不会再 silent 编数）。
>
> **交易下单例外**：下单 JSON/CLI 模板里的 `<STOCK_CODE>` 必须填纯代码，例如港股 `00700`、美股 `AAPL`。带前缀格式只作为脚本的兼容兜底，不作为模型首选输出。

### 高频 JSON 模板（覆盖 80%+ 日常问；交易类仍受第 2 条铁律约束）

| 用户原话特征 | 模板（替换 `<...>` 后即跑） |
|---|---|
| 余额 / 现金 / 购买力 | `$MONI_PY $SKILL/code/cash_summary.py --args-json '{}'` |
| 持仓 | `$MONI_PY $SKILL/code/holdings.py --args-json '{}'` |
| 只看某只持仓 | `$MONI_PY $SKILL/code/holdings.py --args-json '{"code":["<CODE>"]}'`<br>（CODE 直接用用户原话：`01810` / `00700` / `AAPL` 都行，v1.7.5 自动补市场前缀） |
| 资金流水 | `$MONI_PY $SKILL/code/cash_flows.py --args-json '{}'` |
| 今天哪些单 / 未成交 | `$MONI_PY $SKILL/code/order_list.py --args-json '{"active-only":true}'` |
| 全部最近 7 天委托 | `$MONI_PY $SKILL/code/order_list.py --args-json '{}'` |
| 查实时报价 | `$MONI_PY $SKILL/code/market_quote.py --args-json '{"code":["<CODE>"]}'` |
| 同时查多只 | `$MONI_PY $SKILL/code/market_quote.py --args-json '{"code":["<CODE1>","<CODE2>"]}'` |
| 查盘口 5 档 | `$MONI_PY $SKILL/code/market_orderbook.py --args-json '{"code":"<CODE>","count":5}'` |
| 我有哪些账户 | `$MONI_PY $SKILL/code/account_list.py --args-json '{}'` |
| 共享凭证体检 | `$MONI_PY $SKILL/code/check_shared_env.py --args-json '{}'` |
| 创建模拟账户 | `$MONI_PY $SKILL/code/sim_account_create.py --args-json '{"intent":"创建一个新的模拟盘证券账户，HKD/USD 各初始化 100 万现金","confirm":true}'`<br>必须先向用户复述并确认 |
| 重置模拟账户 | `$MONI_PY $SKILL/code/sim_account_reset.py --args-json '{"sub-account-id":"<OLD_MOCK_SUB_ACCOUNT_ID>","intent":"重置旧模拟账户 <OLD_MOCK_SUB_ACCOUNT_ID>：禁用旧账户并创建新模拟账户，HKD/USD 各初始化 100 万现金","confirm":true}'`<br>必须由用户明确指定旧模拟账户 ID 并确认；重置间隔 7 天 |

### 交易类 JSON 模板（必须先按第 2 条铁律完成"复述 + 反问 + 用户明确肯定"再跑）

| 场景 | 模板 |
|---|---|
| 下单（限价单） | `$MONI_PY $SKILL/code/order_create.py --args-json '{"market":"<hk|us>","stock-code":"<STOCK_CODE>","direction":<1|2>,"order-type":3,"quantity":<QTY>,"price":"<PRICE>","intent":"<完整下单意图，含市场/方向/标的/数量/价格/限价单>","confirm":true}'` |
| 下单（市价单） | `$MONI_PY $SKILL/code/order_create.py --args-json '{"market":"<hk|us>","stock-code":"<STOCK_CODE>","direction":<1|2>,"order-type":9,"quantity":<QTY>,"intent":"<完整下单意图，含市场/方向/标的/数量/市价单>","confirm":true}'` |
| 非交易时段下单 | **模拟盘不支持预埋单**：非交易时段也只是普通下单，订单类型仍只能是 `3` 或 `9`；不要把"预埋"理解成新订单类型，也不要追加条件/触发/跟踪字段 |
| 改单（普通订单） | `$MONI_PY $SKILL/code/order_modify.py --args-json '{"market":"<hk|us>","order-id":<OID>,"modify-type":1,"intent":"<完整改单意图，含市场/orderId/原订单摘要/要修改的数量或价格>","confirm":true}'` |
| 改单（带修改字段） | 模拟盘普通改单仅支持 `"quantity"`、`"price"`，且 `"modify-type"` 固定用 `1`。条件单、跟踪止损、止盈止损相关字段不支持 |
| 撤单（任意可撤订单） | `$MONI_PY $SKILL/code/order_cancel.py --args-json '{"market":"<hk|us>","order-id":<OID>,"intent":"撤掉<市场>订单 <OID>（<原标的/方向/数量/订单类型/关键条件摘要>）","confirm":true}'` |

> **shell 引号约定**：永远用**单引号**包整个 JSON 字符串、JSON 内部用**双引号**。这样 shell 不会吃掉 `"`、不会触发变量替换、不会和 zsh 的 `!` 历史扩展冲突。
> **JSON 写错 → 结构化 `INVALID_PARAM`**（不是 OS 报错），错误信息会精确指出"该用单引号包"或"缺逗号"等修正方法。

## 零思考速抄表（传统命令行写法，与上面 JSON 模板等价）

> **使用顺序**：① 先在 JSON 填空模板 / 本表里找用户原话 → 找到 → **直接抄命令** → 跑完按 stdout 顶层 `next_action` 行动；② 找不到 → 走下面的「调用决策树」+ `<脚本> --help`。
> **目的**：把高频场景的"想脚本/想路径/想参数"三步推理，压成"复制即跑"零思考。

### 起手式（每个新会话先跑一次，env 变量持久到当前 shell）

```bash
# $SKILL = moni-trade-skill 根目录（含 code/、本 SKILL.md）；由本机安装位置或运行时注入，不要写死某条绝对路径。
export SKILL="<moni-trade-skill 绝对路径>"
# $FOSUN_PY / $MONI_PY = 总入口 install.sh 创建的共享 venv 解释器（默认 fw-trade-skill/.venv/bin/python）
export FOSUN_PY="<python 绝对路径>"
export MONI_PY="${FOSUN_PY}"
# 唯一真源：总入口 fw-trade-skill/fosun.env（与 moni-trade-skill 并列）。不设则脚本仍会从 code/_client.py 自动推出同一路径。
export FOSUN_ENV_PATH="${FOSUN_ENV_PATH:-$SKILL/../fosun.env}"
```

### 高频命令（覆盖 80%+ 日常问）

| 用户原话特征 | 直接抄这一行 |
|---|---|
| 余额 / 现金 / 购买力 / 还能买多少 | `$MONI_PY $SKILL/code/cash_summary.py` |
| 持仓 / 我买了什么 / 现在有什么股票 | `$MONI_PY $SKILL/code/holdings.py` |
| 今天哪些单 / 未成交订单 / 还没成 | `$MONI_PY $SKILL/code/order_list.py --active-only` |
| 全部最近 7 天委托 | `$MONI_PY $SKILL/code/order_list.py` |
| 资金流水 / 出入金（默认全部） | `$MONI_PY $SKILL/code/cash_flows.py` |
| 查 X 股实时价（如 hk00700 / usAAPL） | `$MONI_PY $SKILL/code/market_quote.py --code <CODE>` |
| 同时查多只 | `$MONI_PY $SKILL/code/market_quote.py --code hk00700 --code usAAPL` |
| 查 X 股盘口 5 档 | `$MONI_PY $SKILL/code/market_orderbook.py --code <CODE> --count 5` |
| 我有哪些账户 | `$MONI_PY $SKILL/code/account_list.py` |
| 共享凭证体检 | `$MONI_PY $SKILL/code/check_shared_env.py` |
| 创建模拟账户 | `$MONI_PY $SKILL/code/sim_account_create.py --intent "创建一个新的模拟盘证券账户，HKD/USD 各初始化 100 万现金" --confirm` |
| 重置模拟账户 | `$MONI_PY $SKILL/code/sim_account_reset.py --sub-account-id <OLD_MOCK_SUB_ACCOUNT_ID> --intent "重置旧模拟账户 <OLD_MOCK_SUB_ACCOUNT_ID>：禁用旧账户并创建新模拟账户，HKD/USD 各初始化 100 万现金" --confirm` |

### 下单 / 改单 / 撤单（用户原话明确**且经二次确认**后再用，参数仍需用户给齐）

> 全部用 **`--market hk|us` 简写**，脚本自动展开三件套，**绝不要手填 `--currency` / `--product-type`**。
> ⚠️ 模板末尾都带 `--intent "..."` + `--confirm`：**模型必须先按「第 2 条铁律」用自然语言复述意图、得到用户明确肯定，再把同一段复述填到 `--intent` 后跑**。在拿到明确确认前，先把命令展示给用户**但不要执行**。
> ⚠️ **`--intent` 是 v1.7.3 起的 `required=True` 必填项**——不带就 argparse `INVALID_PARAM`，没有任何绕过空间。

| 场景 | 模板（占位符替换后即跑） |
|---|---|
| 下单（限价单） | `$MONI_PY $SKILL/code/order_create.py --market <hk|us> --stock-code <STOCK_CODE> --direction <1|2> --order-type 3 --quantity <QTY> --price <PRICE> --intent "<完整下单意图，含市场/方向/标的/数量/价格/限价单>" --confirm` |
| 下单（市价单） | `$MONI_PY $SKILL/code/order_create.py --market <hk|us> --stock-code <STOCK_CODE> --direction <1|2> --order-type 9 --quantity <QTY> --intent "<完整下单意图，含市场/方向/标的/数量/市价单>" --confirm` |
| 改单（普通订单） | `$MONI_PY $SKILL/code/order_modify.py --market <hk|us> --order-id <OID> --modify-type 1 --intent "<完整改单意图，含市场/orderId/原订单摘要/要修改的数量或价格>" --confirm`<br>按用户意图追加 `--quantity` / `--price` |
| 撤单（任意可撤订单） | `$MONI_PY $SKILL/code/order_cancel.py --market <hk|us> --order-id <OID> --intent "撤掉<市场>订单 <OID>（<原标的/方向/数量/订单类型/关键条件摘要>）" --confirm` |

> 港股最小手数 100；不知 `<OID>` 先 `order_list.py`；TIF / expType / 盘前盘后 / 夜盘等高级字段走 `$MONI_PY $SKILL/code/order_create.py --help`。模拟盘订单类型始终只允许 `3` / `9`，且**不支持预埋单**（非交易时段也只是普通下单，不会被转成预埋单）。
> 漏带 `--intent` → `INVALID_PARAM`（argparse 阶段就拒）；漏带 `--confirm` → `NEED_CONFIRMATION`（intent 会回显在错误里给用户校验）—— 这是「第 2 条铁律」的三层运行时兜底，不要怀疑、不要绕过。

## 调用决策树（速抄表没覆盖时走这里）

按用户原话定位脚本，**只跑一个**，跑完汇报：

| 用户原话特征 | 调用 | 备注 |
|---|---|---|
| "我有哪些账户" / "账户列表" | `account_list.py` | meta 查询，跑完只汇报 |
| "刚开了新账户 / 账户变了" | `sync_accounts.py` | 平时不需要主动跑 |
| 共享凭证体检 / 怀疑失效 | `check_shared_env.py` | 体检，不要当业务前置步骤 |
| "创建模拟账户 / 新开模拟账户" | `sim_account_create.py` | 有副作用，必须先复述+确认；成功后脚本会刷新账户索引 |
| "重置模拟账户 / 模拟账户初始化" | `sim_account_reset.py` | 有副作用，必须用户明确指定旧模拟账户 ID 并确认；旧账户会被禁用，重置间隔 7 天 |
| "余额 / 现金 / 购买力 / 还能买多少" | `cash_summary.py` | **不要先跑 account_list** |
| "持仓 / 我买了什么 / 现在有什么股票" | `holdings.py` | 同上 |
| "今天买卖了什么 / 流水 / 出入金" | `cash_flows.py` | |
| "今天的订单 / 委托记录 / 哪些没成" | `order_list.py` | 查某笔单先按 `--stock-code` + 日期 / 市场 / 状态缩小列表；对用户只说明“可按市场/标的/日期/状态筛选订单列表”，不要说某脚本不支持 |
| "下单 / 买 / 卖" | `order_create.py` | 用 `--market hk|us` 简写，见下文 |
| "撤单 / 取消那张单" | `order_cancel.py` | 不知道 order-id 先 `order_list.py` |
| "改价 / 改单 / 改数量" | `order_modify.py` | 同上 |
| "K 线 / 走势图" | `market_kline.py` | |
| "实时价 / 现在多少钱 / 报价" | `market_quote.py` | 多只用 `--code` 多次 |
| "盘口 / 买卖档" | `market_orderbook.py` | |
| "分时" | `market_min.py` | |
| "逐笔成交" | `market_tick.py` | |
| "经纪商" | `market_broker_list.py` | |

> **不知道脚本怎么用？** → `$MONI_PY $SKILL/code/<脚本>.py --help`
> 每个脚本都自带 EPILOG（何时调用 + 示例 + 强制规则）；本文档不重复维护脚本细节，**避免漂移**。

## 其它必须遵守

### 盘别确认

用户没有明确选择`模拟盘`时，禁止调用本 skill。

### 只用共享凭证

- 只读取 `FOSUN_ENV_PATH` 指向的共享凭证；未设置时自动解析到总 skill 根目录 `fosun.env`。
- 推荐写法：`FOSUN_ENV_PATH=fosun.env`，由脚本自动解析成绝对路径。
- 不生成、不复制、不维护第二份凭证；凭证无效时先去同级 `fosun-env-setup` 生成或修复。

### 能力边界

- 仅支持港股、美股正股。
- 不支持 A 股交易、期权交易、`BidAskInfo` 与订阅类接口。
- **用户口径**：当用户请求当前接口不支持的功能时，不要对用户说“某个 Python 文件/某个脚本不支持”。只说明当前支持范围和可替代能力：
  - 支持：港股/美股正股的账户、资金、持仓、资金流水、订单列表、下单、改单、撤单。
  - 支持：报价、K 线、分时、逐笔、盘口、经纪商队列等单次行情查询。
  - 不支持：A 股交易、期权交易、订阅类接口、`BidAskInfo`、按订单号直接单笔查询、批量撤单接口。
  - 可替代：查某笔订单时，用市场/标的/日期/状态缩小订单列表；订阅需求改为单次行情查询；批量撤单需求先列出待撤订单，复述清单并经用户确认后逐笔撤。

### 错误处理：先读 next_action，再行动

所有脚本错误统一以结构化 JSON 输出到 **stderr**：先读 `error_code` 和 `next_action`，按本文末尾「错误码处置矩阵」执行。**`NO_MOCK_ACCOUNT`（exit 3）必须立即停手转告用户**，禁止私自切实盘 skill / 挑其他账户继续 / 改写口径推进。

## 一键安装

在 **总 skill 根目录**安装（与实盘、env-setup 共用 venv；本目录 `install.sh` 会转调上级脚本）：

```bash
bash ../install.sh
# 或：cd .. && bash install.sh
```

> macOS / Linux 用 `bash install.sh`。**用户机器无需预装 Python**——[uv](https://docs.astral.sh/uv/) 会在总入口目录创建 `.venv` 并下载解释器（符合 [Agent Skills](https://agentskills.io/specification) 约定：依赖相对 skill 根目录管理，不写入 Agent 工作区外路径）。

`../install.sh` 会自动：
1. 检测 `uv`，未安装时一键自动拉取；
2. 在 `$FW_TRADE_VENV`（默认 `fw-trade-skill/.venv`）创建**共享**环境，Python 由 uv 自动下载；
3. 下载 SDK 压缩包并解压到 `fw-trade-skill/.cache/`；
4. `uv pip install --editable` 安装 `fsopenapi`（含 setup.py 依赖；PyPI 失败时自动改用清华镜像重试）；
5. 自检 `import fsopenapi`；导出 `FOSUN_PY`（`MONI_PY` 与之相同）。

> 可选环境变量：`FW_TRADE_VENV`、`FW_TRADE_PYTHON_VERSION`、`FW_TRADE_SDK_*`、`FW_TRADE_CACHE_DIR`、`FW_TRADE_PYPI_MIRROR`（兼容旧前缀 `MONI_*`）。

## 使用前提

- `FOSUN_ENV_PATH` 指向的共享凭证文件已存在
- 共享凭证已通过同级 `fosun-env-setup` 生成或修复
- 当前请求已明确选择为`模拟盘`
- 模型每个新会话先按上面「速抄表 → 起手式」export 一次 `$MONI_PY` `$SKILL`

## 下单/改单/撤单：市场参数规则

**推荐唯一路径**：用 `--market hk|us` 简写，脚本自动展开三件套，模型零脑补、零拼错。

| 用户意图 | 推荐写法 | 等价的三件套（高级用户用） |
|---|---|---|
| 港股交易 | `--market hk` | `--market-code hk --currency HKD --product-type 5` |
| 美股交易 | `--market us` | `--market-code us --currency USD --product-type 6` |

- `--market` 与三件套**互斥**，混用本地直接 `INVALID_PARAM` 拦截。
- `order_modify.py` / `order_cancel.py` 只用 `product_type`，简写效果是 `--market hk → 5`、`--market us → 6`。
- 完整模板见上面「交易类 JSON 模板」和「速抄表 → 下单/改单/撤单」节；TIF / expType / 盘前盘后 / 夜盘等高级字段走 `--help`。

## 通用规则与枚举值（速查）

- **市场代码**：`hk` 港股 / `us` 美股（模拟盘只这两种）
- **币种**：`HKD` / `USD` / `CNH`，**港股只用 HKD、美股只用 USD，不自动换汇**
- **方向**：`1=买` / `2=卖`
- **产品类型**：`5`=港股 / `6`=美股
- **订单类型（模拟盘下单唯一允许值）**：`3`=限价单, `9`=市价单
  - **易错（必读）**：**市价单是 `9`，不是 `4`**；`4` 增强限价单、`1/2` 竞价类、`5/6` 特殊/暗盘、`31/32/33/35` 条件/跟踪/止盈止损类均不属于模拟盘能力。
  - **预埋单口径**：**模拟盘不支持预埋单**；非交易时段也只是普通下单（仍只允许 `3=限价单` / `9=市价单`），不要为了“预埋”改用条件单或触发价字段，也不要承诺"会自动预埋"。
- **行情价格解码（强约束）**：凡响应里出现 `power`，价格类字段实际值一律按 `raw / (10^power)` 计算；展示时小数位必须按 `power` 截取，禁止按经验猜位数、禁止脱离 `power` 自行四舍五入。
- **时段 timeInForce（下单 OrderCreate）**：`0`=当日有效, `2`=允许美股盘前盘后, `4`=允许夜盘。美股下单未显式传 `--time-in-force` 时，脚本按 ET 当前时段自动填充（盘前/盘后=`2`，夜盘=`4`，盘中=`0`）；且盘前/盘后/夜盘仅支持限价单（不支持市价单 `orderType=9`）。
- **订单列表 showType（OrderList）**：`0`=只有正股订单, `1`=正股和期权订单, `2`=只有期权订单；**本模拟盘 skill 仅支持正股，查询请用 `0` 或不传（由脚本默认约束）**
- **订单状态**：`10`=未报, `20`=待报, `22`=待处理, `23`=待复核, `40`=已报, `50`=全成, `60`=部成, `70`=已撤, `80`=部撤, `90`=废单, `100`=已失效；服务端通用枚举还可能返回 `21/71/91/101/901`，但模拟盘新下单仍只支持限价单/市价单
- **用户汇报状态码规则**：对用户输出时，禁止只说数字响应码或状态码。凡是结果里出现 `code` / `message` / `orderStatus` / `status` / `statusArr` 等字段，必须同时给出可读说明：
  - `code=0` 要说成“接口返回成功（code=0 / message=success）”；非 0 要同时带出 `message` 和可读失败原因。
  - `orderStatus` 等订单状态必须写成“数字 + 中文状态”，例如 `40=已报`、`50=全成`、`70=已撤`；未知码要说“未知状态码 X”，不能只把数字丢给用户。
  - 如果响应里既有 `orderId` 又有状态码，汇报格式应包含：订单号、操作结果、状态码对应文字说明、是否还需要用户下一步确认。

### 参数说明「根治」规则（维护必读）

- **单一事实来源**：同仓库内复星 OpenAPI 文档在 `fw-tradings-1.0.4/fosun-trading/doc/`（相对 moni-trade-skill 目录为 `../fw-tradings-1.0.4/fosun-trading/doc/`）。**交易下单**以 `OrderCreate.md` 为准；**改单** `OrderModify.md`；**订单列表** `OrderList.md`；**资金流水** `CashFlows.md`。
- **冲突处理**：模拟盘能力边界优先于通用 `OrderCreate.md` 全量枚举；若某脚本 `--help` 与模拟盘只支持 `3/9` 不一致，**视为 bug：改脚本/help，不反推瞎编枚举**。

### 子账户解析机制（模型理解即可，不需要主动调）

- **优先级**：CLI `--sub-account-id` > `MONI_SUB_ACCOUNT_ID` 环境变量 > 共享凭证 `FSOPENAPI_ACCOUNT_INDEX` 缓存 > 自动调 `/v1/account/Accounts` 刷新
- **缓存自愈**：业务接口报账户类错（含 "subAccountId"、"账户" 等关键字）→ 自动刷一次缓存并以新 ID 重试一次；新旧一致直接抛错，不无意义重试
- **类型净化**：所有路径出入 `subAccountId` 都强制走 `_coerce_sub_account_id`（强转 str + strip），杜绝下游类型踩坑
- **无 mock 账号 → 强拦截**：缓存和刷新后都查不到 `subAccountType=2` 时抛 `NoMockAccountError`（exit 3），按错误码处置矩阵处理

## 错误处理规约（必读）

**所有脚本失败时，stderr 输出统一结构化 JSON**，模型直接解析即可决策，不必回查文档：

```json
{
  "ok": false,
  "error_code": "NO_MOCK_ACCOUNT",
  "message": "...",
  "hint": "为什么会这样（机制说明）",
  "next_action": "模型应该做什么（祈使句）",
  "code": 60009,           // 仅 APIError 才有
  "requestId": "...",      // 仅 APIError 才有
  "data": {...}            // 仅 APIError 才有
}
```

**退出码**：`0` 成功 / `1` APIError / `2` 参数/配置/未确认错（含 `NEED_CONFIRMATION`） / `3` NO_MOCK_ACCOUNT（强拦截）

### 错误码处置矩阵

| error_code | 含义 | 模型必须做什么 |
|---|---|---|
| `NO_MOCK_ACCOUNT`（exit 3） | 共享凭证下没有 mock 子账户 | **立即停手**，把账户缺失情况完整转告用户。**禁止**自动切到实盘 skill、**禁止**挑选其他账户继续 |
| `ENV_FILE_MISSING`（exit 2） | 共享凭证文件不存在 | 让用户先通过同级 `fosun-env-setup` 生成 |
| `ENV_INCOMPLETE`（exit 2） | 凭证缺关键字段 | 让用户通过同级 `fosun-env-setup` 修复或刷新凭证 |
| `SESSION_EXPIRED`（exit 1） | 共享凭证里的券商会话已过期 | 先跑 `check_shared_env.py` 体检；仍失败就回同级 `fosun-env-setup` 修复或刷新凭证。**不要**把它解释成“订单/持仓不存在” |
| `INVALID_SIGNATURE`（exit 1） | 共享凭证的签名链失效 | 回同级 `fosun-env-setup` 修复或刷新凭证，再重试当前操作；**不要**把它解释成“查无此单” |
| `APIERROR_40010`（exit 1） | 共享凭证 apikey 已过期 | **停手**，引导用户回同级 `real-trade-skill` 执行续期（扫码）；续期只延长原 apikey 有效期，**不改本地 apikey、无需用户回填**；扫码后直接重试 |
| `APIERROR_40001` / `APIERROR_40015`（exit 1） | apikey 无效 / 密钥不匹配 | **停手**，引导用户回同级 `real-trade-skill` 完成重置扫码；提醒已开通过则在页面上点 **「忘记 API 参数」**；**须等用户发来页面上 API Key 与服务端公钥（PEM）一并**由 `update_api_key.py`（`--api-key` + `--server-public-key`）写入共享凭证后再重试 |
| `APIERROR_40005` / `APIERROR_40008`（exit 1） | apikey 禁用 / 撤销 | **停手**，用大白话告知用户联系星财富客服；模拟盘不建票、不出码 |
| `NEED_CONFIRMATION`（exit 2） | 变更类脚本未带 `--confirm`，触发「第 2 条铁律」运行时兜底（v1.7.3 起错误信息会回显 `--intent` 内容） | **立即停手**，把 stderr JSON 里的 `intent_summary` 字段（即模型自己填的 `--intent`）原样复述给用户、明确反问"以上意图确认执行吗？"；得到明确肯定后在原命令末尾补 `--confirm` 重试；**禁止**自己加 `--confirm` 绕过、**禁止**用模糊回答（"嗯/可以吧/看着办"）当作确认 |
| `INVALID_PARAM` 提示「the following arguments are required: --intent」 | v1.7.3 起 `--intent` 是 required，模型漏填 | 不要瞎猜——先按「第 2 条铁律」用自然语言复述完整变更意图给用户、得到明确肯定后，**把这段复述原样填到 `--intent "..."` 里**，连同 `--confirm` 一起重试 |
| `WRONG_SCRIPT_NAME`（exit 2） | 命中 v1.7.2 trap stub：脚本名拼错（如 `modify_order.py` / `cancel_order.py` / `buy.py` 等 13 个常见错名） | **立即把命令里的错名替换为 stderr JSON 里的 `intended_script` 值**，其它参数保持不变直接重试；**禁止再去猜其它脚本名**——`intended_script` 就是正确答案 |
| `No such file or directory`（OS-level，**非结构化 JSON**） | 罕见错名连 trap 都没覆盖（如 `update_order.py` / `place_order.py`） | **立即停手**：① 跑 `ls $SKILL/code/*.py` 列出真实文件名 ② 回查 SKILL.md 「合法脚本清单」逐字符核对 ③ 改正脚本名后重试 ④ **严禁靠拼写直觉猜下一个名字重新提交** |
| `INVALID_PARAM` 提示「参数名 `--xxx` 是脑补出来的」 | v1.7.4 智能 hint：模型用了官方 4 alias 之外的标的脑补名（`--ticker` / `--instrument` / `--stockcode` / `--stocks` 等） | **立即把脑补名改成 `--code`（行情类）或 `--stock-code`（交易类）**，其它名字（`--symbol` / `--symbols`）也都接受；**禁止再去猜其它写法**——4 个 alias 之外都是脑补；下次直接走「JSON 填空模板」节，连参数名都不用想 |
| `INVALID_PARAM` 提示「`--args-json` 解析失败」 | v1.7.4 模型用 `--args-json` 时 JSON 写错（缺逗号 / 双引号被 shell 吃掉 / 单双引号混用） | 按 next_action 改正：用单引号包整个 JSON、JSON 内部用双引号；从「JSON 填空模板」节里复制一份完整模板再填值；**禁止**手写 JSON 不用模板 |
| `SILENT_FAIL_EMPTY_DATA`（exit 2，v1.7.5 新） | SDK 返回 `code:0/message:success` 但 `data:null`——多见于"标的代码不存在"或"格式诡异 normalize 也救不回来" | **立即停手**并把"SDK 返回空数据"如实告诉用户，请用户确认完整代码（含市场前缀，如 `hk00700`/`usAAPL`）后再重试；**严禁**把 ok=true 的外壳误读成成功、**严禁**自己编一个价格汇报给用户。这是 v1.7.5 输出层强制兜底，专门防"模型读 ok=true 凭空编数"的人命级故障 |
| `INVALID_PARAM`（exit 2） | 本地参数校验失败（`--market` 缺失/与三件套混用、三件套错配、请求了能力边界外功能等） | 按 message 修正命令行后重试；涉及用户原始意图先确认。若属于接口能力边界，对用户只说明“当前支持什么/可替代怎么做”，不要带出内部 Python 文件或脚本名 |
| `APIERROR_50001` | 列表类接口分页 Count 校验失败 | 加 `--count 50` 重试一次，不要原样重试 |
| `APIERROR_60006` | 服务端业务校验（价格/数量/停牌等） | 原样转告用户，等待用户调整后再重试，**禁止自行猜测修正** |
| `APIERROR_60009` | 单笔金额超模拟盘限额 | 建议用户减少 quantity 或换标的，**不要用相同参数重试** |
| `APIERROR_60014` | 风控/合规拦截 | 原样转告用户，等待决策 |
| `APIERROR_*`（其他） | 服务端业务错 | 看脚本输出的 hint / next_action；message 提示参数问题就按提示改后重试，否则转告用户 |

> 模型遇到任意错误：**先读 `next_action`，再决定下一步**。不要凭直觉重试。

## 已知服务端 vs 文档差异（已自动处理）

| 接口 | 文档行为 | 服务端实际行为 | 本 skill 处理 |
|---|---|---|---|
| OrderList | "fromDate/toDate 不传则查最近 7 天" | 实际**强制要求**两个字段 | `order_list.py` 在用户未指定时自动填充 7 天前与今天 |
| OrderCreate / OrderModify / OrderCancel | `productType` 文档标注可选 | 实际**强制要求** | 三个脚本要求显式 `--market hk\|us`（推荐）或完整 `--product-type`（兼容），缺失/混用一律 `INVALID_PARAM`；`order_create.py` 还做三件套对齐校验 |
| CashSummary 等 | `subAccountId` 文档允许数字 | 部分路径要求字符串 | `_client.py` 单一出口 `_coerce_sub_account_id` 强转 str + strip，杜绝类型踩坑 |

## 目录结构

```
moni-trade-skill/
├── SKILL.md                # 本文件，模拟盘子 skill 主入口
├── _meta.json              # slug / version
├── README.md               # 安装与故障排查
├── install.sh              # 兼容入口 → 转调 ../install.sh
├── install.ps1             # Windows 一键安装
├── code/                   # CLI 脚本
│   ├── _client.py          # 公共 SDKClient 工厂 + env 加载 + 账户索引缓存 + 自愈重试 + 错误处理
│   ├── check_shared_env.py # 显式检查 FOSUN_ENV_PATH 指向的共享凭证是否可用（顺带刷新账户索引）
│   ├── account_list.py     # 查账户列表（顺带刷新账户索引到 FOSUN_ENV_PATH 指向的共享凭证）
│   ├── sync_accounts.py    # 强制同步账户索引到 FOSUN_ENV_PATH 指向的共享凭证（账户有变更时再跑）
│   ├── sim_account_create.py # 创建模拟账户（成功后刷新账户索引）
│   ├── sim_account_reset.py  # 重置模拟账户（禁用旧账户、创建新账户、成功后刷新账户索引）
│   ├── cash_summary.py
│   ├── holdings.py
│   ├── cash_flows.py
│   ├── order_create.py
│   ├── order_cancel.py
│   ├── order_modify.py
│   ├── order_list.py
│   ├── market_kline.py
│   ├── market_min.py
│   ├── market_broker_list.py
│   ├── market_orderbook.py
│   ├── market_quote.py
│   └── market_tick.py
```
