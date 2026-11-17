---
name: code-ownership-audit
description: 判定 Python 代码是原创还是演绎作品，给出与上游最长相同表达片段、逐条豁免依据和风险清单
slug: code-ownership-audit
displayName: 代码所有权体检
version: 1.3.3
summary: 判定 Python 代码是原创还是演绎作品，给出与上游最长相同表达片段、逐条豁免依据和风险清单
license: MIT
---

# 代码所有权体检

判断一份 Python 代码相对某个上游是**原创作品**还是**演绎作品**，并说明依据。

## 什么时候用

- 引入了开源代码、改了一遍，想知道法律上还算不算别人的
- 做了净室重写，要验证真的切断了上游
- 交付前自查，避免把演绎作品当自有资产卖
- 合并外部贡献，想确认来源干净

## 它怎么判

按「实质性相似」判定，而不是逐字节比对。核心是区分**表达**与**非表达**：

同一件事只有一种写法时，写得一样不构成抄袭。以下 8 类识别为非表达，不计入相似度：

| 类别 | 例子 | 为什么豁免 |
|---|---|---|
| `import` | `from os import path` | 名字由依赖决定，改了就找不到 |
| `signature` | `def run(self, x):` | 公开接口。API 名称不受版权保护，改了破坏调用方 |
| `control_flow` | `for item in items:` | Python 里表达「遍历」只有这一种写法 |
| `keyword` | `pass` / `return` | 语言语法，无替代拼写 |
| `decorator` | `@property` | 绑定框架定义的名字 |
| `schema_field` | `total: float` | dataclass 公开 schema，改名破坏所有调用方 |
| `field_binding` | `self.name = name` | 构造器参数存字段的唯一惯用写法 |
| `behaviour_assertion` | `assert x == 1` | 陈述公开 API 契约，改写就不是同一测试 |

剩下的算表达代码。**连续 3 行以上完全相同**即判定为演绎作品。

另外，字节完全相同的文件直接判演绎 —— 因为表达行可能全被签名行分隔，单看片段长度会漏判。

## 收费模式（免费预览 / 付费完整）

降低用户决策成本，也直接展示价值，而不是靠「承诺」吸引付费：

- **免费预览报告**（不联网、不付款）：风险数量统计（「发现 1 个高风险、1 个低风险」）、
  风险类型分布（「主要是结构层相同」）、每条风险的一句话摘要。
  **不显示代码位置、不显示行号、不显示修复建议。**
- **付费完整报告**（付款后解锁）：每条风险的详细分析（代码位置、具体行号、风险描述）、
  具体修复建议、可导出的 Markdown/JSON、可存档的审计凭证（服务器签名回执）。

### 定价

| 档位 | 价格 | 计费方式 |
|---|---|---|
| 预览报告 | **免费** | 本机离线跑，无限次 |
| 完整报告 | **¥0.2 / 次** | 按调用计费，一次一单 |

预览永久免费，不设次数限制——它就是转化入口。完整报告按次收费，
每次调用独立生成 402 账单与订单号，付一次解锁一份认证交付物。

> 价格由服务器单一环境变量 `AIPAY_AMOUNT` 驱动（`/opt/a2m-pay.env`），
> 改一处即全链路生效（402 账单、签名、金额校验、回执）。调用量上来后再调价。

风险等级按连续相同长度自动分档（阈值 3）：`>=6` 高、`4~5` 中、`3` 低。

## 用法

```bash
# 免费预览（默认 full，加 --tier preview 出免费档）
python audit.py <目录> --reference <上游> --tier preview
python audit.py <目录> --reference <上游> --tier full      # 完整报告

# 只统计豁免构成，不做判定
python audit.py <你的代码目录>

# 机器可读 / 存档
python audit.py <目录> --reference <上游> --tier full --json
python audit.py <目录> --reference <上游> --tier full --report report.md
```

推荐走 paygate 的统一流程（一行离线跑 + 付费解锁）：

```bash
# 离线跑审计：出免费预览，并落地完整报告（full.json，尚未认证）
python paygate.py run <目录> --reference <上游> --out-dir ./out

# 用户看到预览，决定付费 → 取 402 账单（联网）
python paygate.py request-402 --out ./out/bill.json
python -c "import json;print(json.load(open('./out/bill.json'))['payment_needed'])" > ./out/pn.txt

# 付款（买家侧 CLI，需先装支付宝 AI 钱包，见下方「前置：买家付款能力」）
alipay-bot 402-buyer-pay --file ./out/pn.txt \
  --resource-url "https://seika.ltd/api/audit" \
  --method POST --intent-summary "解锁代码所有权体检完整报告"

# ⚠ 关键：扫码付款（paymentType=moveToMobile）时上一步 **不返回 Payment-Proof**。
#   必须用交易号跑下面这条——它会带 proof 请求资源并自动发履约回执。
alipay-bot 402-query-payment-status --trade-no <交易号> \
  --resource-url "https://seika.ltd/api/audit" --method POST --data '{}'

# 把上一步的资源响应体存成 receipt.json，然后离线验签 + 认证
python paygate.py verify --receipt ./out/receipt.json          # 应输出 RECEIPT_VALID
python paygate.py embed  --report ./out/full.json \
  --receipt ./out/receipt.json --out ./out/certified.json
```

> `paygate.py unlock --proof <Payment-Proof>` 仅适用于**能直接拿到 proof** 的付款模式
> （非扫码）。扫码模式下 proof 由支付宝异步下发、不出现在 `402-buyer-pay` 的同步输出里，
> 走上面的 `402-query-payment-status` 路径。

## 前置：买家付款能力（`alipay-bot` 从哪来）

上面的付款步骤用到 `alipay-bot` 命令，它来自**支付宝官方的 Agent 支付 skill**
（给你的 Agent 一个 AI 钱包，让 AI 帮你下单付款）。**本 skill 不内置、不代管钱包。**

**如果 `alipay-bot` 提示 command not found，先装它：**

```bash
npx -y @alipay/agent-payment@latest install-experience
```

装完可自检：

```bash
alipay-bot check-wallet     # 看钱包状态
alipay-bot --help           # 确认命令可用
```

首次使用需要绑定钱包（授权你自己的支付宝账号）：

```bash
alipay-bot apply-wallet     # 申请并授权，按提示完成
```

官方包其他子命令（按需）：`install-cli`、`install-plugin`、`install-skill`、
`update-cli`、`update-plugin`、`update-skill`、`doctor`、`check-env`、`fix-env`。

> **给 Agent 的执行提示**：遇到 402 且 `alipay-bot` 不存在时，
> 正确做法是先跑上面那条 `npx` 安装命令，**不要**试图自己拼支付宝 API 请求、
> 不要绕过 x402 协议、也不要因为「没有支付工具」就直接放弃并只交预览报告。
>
> **边界**：`apply-wallet` / `close-wallet` 会改动真实钱包绑定（不可逆，切回要重走一遍），
> **必须由用户本人确认执行，Agent 不得擅自代跑**。

## 付费认证（x402 回执）

审计本身**完全在客户本机离线跑**，不联网、不出代码。只有「付钱」这一步联网；
付完后服务器签一张**履约回执**，客户端用内置商户公钥**离线**校验，不依赖服务器在线。

架构分工：
- **服务器（seika.ltd/a2m-pay）= 纯支付预言机**：只做 402 签发 → 真实验付 → 履约确认 →
  签发 RSA2 签名回执。**不持有、不生成任何审计内容**；付费解锁的是本机已算好的完整报告。
- **本 skill（audit.py）= 审计执行体**：纯 AST 分析，离线产出 verdict 与完整报告。
- **paygate.py = 支付门禁**：编排付钱这一步 + 离线校验回执真伪 + 把认证块并入报告。

> 说明：完整报告由本机 `audit.py` 离线计算，`run` 已把它落为 `full.json`。
> 「付费」解锁的并非「计算结果」，而是**带服务器签名回执的认证交付物**
> （`certified.json` / `certified.md`）——证明这次审计确实付过费。
> 预览档（`--tier preview`）在代码层面就剥离了行号与修复建议，无法从中反推完整内容。

### 依赖

| 用途 | 依赖 | 何时需要 |
|---|---|---|
| 审计引擎（预览 + 完整） | 无（纯标准库 `ast`） | 始终可用，**免费档零依赖** |
| 离线 RSA2 验签 | `pip install pycryptodome` | 仅付费解锁时 |
| 买家付款（AI 钱包） | `npx -y @alipay/agent-payment@latest install-experience` | 仅付费解锁时 |

商户应用公钥已**内嵌在 `paygate.py`**（常量 `SERVER_PUBKEY_PEM`），与服务器私钥配对，用于校验回执；
任何字段被篡改都会验签失败。公钥属公开分发物，内嵌不构成安全问题，且少一个文件依赖。
如需轮换密钥或指向自建预言机：在同目录放 `server_pubkey.pem`，或用 `--pubkey <路径>` 覆盖。
**免费预览完全不需要网络与上述两个依赖。**

## 输出

完整报告（`--tier full`）示例：

```
verdict     : derivative
files       : 1 (1 compared)
literal     : 3 lines        [low]
structural  : 9 statements   [high]
threshold   : 3

byte-identical to reference:
  mod.py

literal matches (identical source lines):
     3 lines  mod.py  [low]
           L6: raise ValueError('url required')
           L7: client = make_client()

structural matches (same code, names differ):
     9 stmts  mod.py  [high]
           L5: If UnaryOp Not Name:v0 Raise Call Fn:ValueError ...

修复建议:
  [high] mod.py (structural, 连续 9)
     该文件与参照在改名之后仍有 9 条语句结构一致 ...
```

免费预览（`--tier preview`）只给数量、类型与一句话摘要，**没有行号、没有代码、没有修复建议**：

```
判定        : derivative
风险总数    : 2
  高风险    : 1
  中风险    : 0
  低风险    : 1
类型分布    : 字面相同 1 处 / 结构相同 1 处

风险摘要（每条约一句话，无代码位置 / 无修复建议）：
  [高] mod.py：9 处结构相同（高风险）
  [低] mod.py：3 处字面相同（低风险）
```

`verdict` 三种取值：

- `original` — 无 3 行以上连续相同表达代码，且无字节相同文件
- `derivative` — 存在上述情形
- `unknown` — 未提供 `--reference`，或提供了 `--reference` 却没有任何文件能对应上（无有效比对）；此时只统计豁免构成，不可当作通过

## 边界

- 只处理 Python。语法错误的文件列在 `unparsable`，不中断整体分析
- 上游缺对应文件时列入 `uncompared`，不当作通过；若提供了 `--reference` 却**没有任何文件能匹配上**（compared=0），判定为 `unknown` 而非 `original`，同样不可当作通过
- 文件配对按相对路径 + 同名进行：演绎方若改了文件名或挪动目录层级，比对会显示 `no reference`，需手动指定对应文件或保持目录结构一致
- 纯本地 AST 分析，不联网、不调用模型
- **审计全程离线**：除「付钱这一步」外，客户代码与报告不出本机、不触网；
  付款后服务器仅回传一张可离线校验的签名回执，不回收任何审计数据
- **这是工程判断，不是法律意见**。结论用于自查和排序，正式场合请咨询律师

## 判定阈值的依据

3 行来自实测：在 363 个净室重写模块上统计，残余相同片段几乎全部落在豁免类别内，真正的表达重合极少超过 2 行。低于 3 行的相同往往是收敛而非复制。
