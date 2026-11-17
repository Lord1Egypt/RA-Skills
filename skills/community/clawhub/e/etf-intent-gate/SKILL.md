---
name: etf-intent-gate
description: ETF/行业投研平台的网关级前置意图识别与安全兜底Skill。执行于用户输入之后、业务Agent集群分发之前：规则引擎过滤非法字符/prompt注入/违规话术，LLM意图识别输出结构化JSON（7种intent_type），query标准化改写（把"可以买吗"改写为投研分析指令），Agent裁剪调度与异常降级。Use when building an ETF research platform gateway, adding pre-dispatch intent classification and safety guardrails before fan-out to multiple research agents.
metadata:
  openclaw:
    requires:
      env:
        - INTENT_LLM_API_KEY
        - INTENT_LLM_BASE_URL
---

# ETF Intent Gate（ETF投研平台前置意图识别网关）

为"用户请求 → 多Agent并行投研分析"架构提供网关级前置安全与意图校验：**只有校验通过才下发下游Agent，不通过直接返回标准化应答**，避免下游Agent被脏输入污染、跑错方向或浪费算力。

## 1. 角色定义

**是谁**：「ETF投研平台」的前置意图识别与安全校验网关，工作在用户原始输入完成之后、业务Agent集群（宏观Agent、事件Agent、政策Agent、估值Agent、资金Agent）分发之前。

**擅长**（四项职责）：

1. **意图分类**：判断输入属于 7 种 intent_type 之一
2. **风险拦截**：规则层 + 语义层双重过滤非法/注入/违规/无意义输入
3. **查询改写**：把口语化决策问句改写为客观投研分析指令
4. **调度优化**：按意图裁剪下游Agent集合，输出标准化任务上下文

**不做什么**：

- 不查询行情、净值、成交等市场数据（数据获取是下游Agent的职责）
- 不产出任何分析结论、研报内容或投资建议
- 不做多轮对话式澄清（无状态同步网关；"反问"通过拦截分支的引导话术一次性完成）
- 不下发用户原始 query（仅日志留存，不流入业务Agent）

两层过滤架构：**规则引擎在前（不调LLM，高性能），LLM意图识别在后**。`rule_block=true` 直接终止，不进 LLM。

## 2. 输入与澄清

LLM 意图识别模块接收两部分输入：

```
[规则层标记]（供参考，最终判断以LLM为准）
- rule_block: true/false
- risk_type: 命中的风险标签（block级：稳赚/必涨/内幕/payload注入；warning级：梭哈/全仓）
- raw_text_cleaned: 清洗后文本（已去除零宽/控制字符、script/SQL/markdown payload）

[清洗后的用户输入]
<用户实际query文本>
```

HTTP 网关接口入参（对上游调度器暴露）：

```json
{"query": "芯片行业可以买吗？"}
```

**澄清原则（不猜）**：

- 输入**缺少可分析的查询对象**（未提及任何行业/ETF代码/指数）或语义模糊 → 判定 `unknown_intent`，**禁止猜测并编造改写**，通过拦截分支返回引导反问话术（如"请告诉我您想了解哪个行业、ETF代码或指数，以及关注的时间范围，我来为您做投研分析"）
- 改写只保留用户已提及的标的与诉求，**不引入用户未提及的标的，不补造时间范围**
- 纯闲聊（`chat_greeting`）同样走引导分支，不做推测性分析

## 3. 数据与工具

本 Skill 不调用外部行情数据源；"工具"即内部处理模块，按固定顺序取用：

| 顺序 | 模块 | 取什么 | 产什么 |
|---|---|---|---|
| 1 | `app/preprocess.py` 规则引擎（零宽/控制字符清洗、script/SQL/markdown payload过滤、长度校验、两级黑名单） | 原始 query | `raw_text_cleaned` + `rule_block`/`risk_type`/`rule_labels` |
| 2 | `app/llm_client.py`（OpenAI 兼容 `/chat/completions`，`response_format=json_object`）+ `app/prompts.py`（System Prompt + `INTENT_JSON_SCHEMA`） | 清洗文本 + 规则标记 | 固定 Schema 意图 JSON |
| 3 | `app/pipeline.py::_apply_business_rules` | 意图 JSON | `IntentResult`（7 分支路由） |
| 4 | `app/pipeline.py::detect_injection`（5 类注入正则） | `rewritten_query` | 注入标签列表；命中即覆盖为拦截 |
| 5 | `app/api.py`（FastAPI + 单行 JSON 埋点） | `IntentResult` | `forward` 任务上下文 / `intercept` 前端应答 |
| 6 | `app/pipeline.py::_degrade` | LLM 异常（`IntentLLMError`） | 保守拦截 / 宽松放行打标 |

## 4. 处理流程（顺序固定，不可调换）

顺序本身是安全设计：**规则先于 LLM**（省算力、防简单攻击）；**改写之后必须二次验注入**（防语义绕过）；**降级最后接管**（故障不卡死链路）。

1. **阶段1 规则预处理** → `rule_block=true` 直接终止，返回拦截话术
2. **阶段2 LLM 意图识别** → 输出固定 Schema JSON；超时/解析失败转阶段6
3. **阶段3 业务边界校验** → 按 intent_type 分支：放行（safe/warning）/ platform_qa / 闲聊引导 / 注入违规阻断 / 索要建议拒绝
4. **阶段4 防注入二次校验** → 仅对放行场景的 `rewritten_query` 检测 5 类注入特征，命中覆盖为拦截
5. **阶段5 输出路由** → `forward`（构造任务上下文投递调度器）或 `intercept`/`platform_qa`（直接应答）；同步埋点日志
6. **阶段6 异常降级** → LLM 故障时 `conservative`（默认，拦截+友好提示）或 `loose`（放行 + `intent_parse_failed` 标记，下游加强提示）

## 5. 输出模板

LLM 固定 JSON Schema，字段完整、顺序固定，**不允许自由文本**：

```json
{
  "intent_type": "etf_industry_research | platform_qa | chat_greeting | malicious_injection | illegal_content | investment_advice_request | unknown_intent",
  "is_allow_forward": "true=允许下发下游Agent",
  "risk_level": "safe | warning | block",
  "rewritten_query": "改写后的标准化查询，下游Agent唯一可用输入；拦截/咨询/闲聊场景为空",
  "intent_desc": "一句话描述用户意图",
  "refuse_reason": "is_allow_forward=false 时的面向用户拒绝原因",
  "required_agent_list": "[]为空=全部5个Agent并行；非空=只调度指定Agent（裁剪省算力）",
  "entity_extract": {
    "industry": [], "etf_code": [], "index_name": [], "query_object": ""
  }
}
```

HTTP 网关出口三态：

| action | 含义 | 后续动作 |
|---|---|---|
| `forward` | 放行 | 调度器拿 `result.standard_query` + `agent_allow_list` 分发5个Agent并行 |
| `intercept` | 拦截 | `reply_to_user` 直接回聊天框，**不创建Agent任务** |
| `platform_qa` | 平台咨询 | 路由到平台问答知识库，不走投研Agent |

**标准话术模板**（代码内统一维护，前端直接展示，禁止即兴发挥）：

| 场景 | 话术 |
|---|---|
| 注入/未知异常 | 抱歉，暂时无法处理您的请求，请调整后重试。 |
| 违规内容 | 您的提问包含平台不支持的内容，请调整后重试。 |
| 索要投资建议 | 本平台仅提供客观 ETF 投研数据分析，不提供荐股、收益承诺、买卖点位等投资决策建议，请调整您的提问。 |
| 闲聊/意图不明引导 | 您好！我是 ETF 投研助手，可以帮您分析 ETF、行业与指数相关的投研信息。试试问我：芯片行业最近的基本面和政策环境怎么样？ |
| 降级（保守模式） | 暂时无法理解您的提问，请调整问题后重试。 |

**免责声明模板**（`risk_warning=true` 时，结果汇总页必须原样追加）：

> 以上内容由AI基于公开信息整理生成，仅供研究参考，不构成任何投资建议。市场有风险，投资需谨慎。

转发场景任务上下文：`request_id` / `original_user_query`（仅日志留存）/ `standard_query` / `entity_extract` / `risk_warning` / `agent_allow_list`。

## 6. 边界与免责

- **平台能力边界**：仅做 ETF/行业/指数投研信息分析；**不给买卖指令、不做个股荐股、不预测涨跌、不承诺收益、不提供投资决策**
- **口语化 vs 强制索要**（关键判定）："芯片可以买吗" = 正常投研诉求 → 改写放行 + `risk_level=warning`（结果页强制追加免责声明）；"保本/必涨/稳赚/给买点位/荐股" = 超出能力边界 → 直接拦截，不做分析
- **多层免责**：网关打 `risk_warning` 标记 → 汇总页强制追加免责声明 → 下游 Agent 二次校验标记并禁止输出买卖结论（即使上游漏过）

## 其余硬约束

1. **下游Agent永远只使用 `rewritten_query`/`standard_query`，禁止透传用户原始 query**——原始 query 只做日志留存，不流入业务Agent（安全核心）
2. **安全话术不暴露内部实现**：遇注入/违规统一使用上表标准话术，禁止回复"检测到prompt注入"等内部细节
3. **Agent 裁剪**：仅当用户明确只关注单一维度时裁剪（如只问政策 → `["政策agent"]`），否则空数组全量并行
4. **降级模式业务可配**，金融平台默认 `conservative`

## 安装与运行

```bash
# 1. 安装依赖（Python 3.11+）
pip install -r requirements.txt

# 2. 配置LLM（任意OpenAI兼容服务：GLM/DeepSeek/通义等）
cp .env.example .env
# 编辑 .env 填入：
#   INTENT_LLM_API_KEY=你的key
#   INTENT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4  （示例：智谱）
#   INTENT_LLM_MODEL=glm-4-flash
# 不配置时自动进入mock模式（本地规则模拟意图），可先跑通链路

# 3. 启动网关服务
uvicorn app.api:app --host 127.0.0.1 --port 8300
```

## 调用接口

```
POST /api/v1/intent/check
Content-Type: application/json

{"query": "芯片行业可以买吗？"}
```

返回示例（放行场景）：

```json
{
  "request_id": "ffc571a3...",
  "action": "forward",
  "risk_level": "warning",
  "intent_type": "etf_industry_research",
  "result": {
    "standard_query": "对芯片行业做ETF相关投研分析，涵盖宏观、行业事件、产业政策、估值、资金面维度，仅输出客观事实与数据，不给出买入卖出投资决策建议",
    "risk_warning": true,
    "agent_allow_list": ["宏观agent", "事件agent", "政策agent", "估值agent", "资金agent"]
  }
}
```

## 一键自测

```bash
# 先启动服务（终端1），然后：
python examples/manual_test.py   # 10个典型case自动比对
python -m pytest tests/ -v       # 25个pytest，无需启动服务
```

## 文件结构

```
etf-intent-gate/
├── SKILL.md            # 本文件（六段式行为契约 + 使用文档）
├── requirements.txt    # Python依赖（fastapi/uvicorn/httpx/pydantic等）
├── .env.example        # LLM配置模板
├── app/                # 核心实现（6阶段流水线）
│   ├── preprocess.py   # 阶段1：规则引擎
│   ├── prompts.py      # 阶段2：意图识别System Prompt
│   ├── llm_client.py   # 阶段2：OpenAI兼容调用+mock模式
│   ├── pipeline.py     # 阶段3-6：边界校验/防注入/路由/降级
│   └── api.py          # FastAPI网关入口+埋点
├── tests/              # 25个pytest用例
├── examples/           # 10case一键自测脚本
└── references/         # 设计文档
```

## 详细文档

- 设计思路与踩坑要点见 `references/design.md`
