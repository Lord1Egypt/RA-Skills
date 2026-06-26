---

name: "clawtip-invention-patent"
description: >
  中国发明专利申请文件撰写助手：在用户完成支付（每次 2.00 元人民币）后，通过多轮中文对话，依据国知局常见结构引导用户完成说明书、权利要求书、摘要等草稿。
  请全程使用中文与用户交互（含思考过程）。
metadata:
  author: "风清扬-李"
  license: "MIT-0"
  category: "legal-tech"
  capabilities:
    - "payment.process"
  permissions:
    - "network.outbound"
    - "credential.read"

---

# 中国发明专利撰写（clawtip 付费）

## 技能概述

> **支付依赖（clawtip）：** 本技能为付费服务，**支付环节必须由 `clawtip` 支付技能提供支持**（与《完全 Skill 模板》一致）。使用本技能前，请确认运行环境中**已安装并可用「clawtip」支付技能**；若当前环境尚未安装，须**先安装 clawtip 支付技能**，否则无法完成第二阶段支付、也无法取得有效 `credential`。

本技能在 **支付成功前** 不得进入撰写引导。标准路径为：**创建订单 → 使用 clawtip 完成支付 → 履约脚本校验 → 支付成功后开始对话撰写**。

若用户已在首轮提供 `<技术主题>`、`<订单号>`、`<支付凭证>`，可跳过前两阶段，直接进入 **第三阶段** 与 **第四阶段**。

**计费：** 每次有效会话 **2.00 元人民币**（OpenClaw 中 `AMOUNT=200`，单位为分）。

**本技能服务地址：** `http://api.clawtip.top/api`（创建订单、履约校验均指向该地址下的接口；若需覆盖，可设置环境变量 `SKILL_SERVER_BASE_URL`）。

---

## 中国发明专利（模板结构）

撰写时按以下板块组织输出（与常见申请文件结构对齐，便于用户后续交代理机构或自行润色）：


| 板块        | 说明                                                                         |
| --------- | -------------------------------------------------------------------------- |
| **发明名称**  | 简明、准确，与主题一致                                                                |
| **摘要**    | 技术问题、手段、主要用途；不超过 300 字                                                     |
| **摘要附图**  | 指定最能说明技术方案的图号                                                              |
| **权利要求书** | 独立权利要求 + 从属权利要求；主题清晰、层次分明                                                  |
| **说明书**   | **技术领域** / **背景技术** / **发明内容**（要解决的技术问题、技术方案、有益效果） / **附图说明** / **具体实施方式** |
| **附图**    | 若用户无图，用文字示意框图或流程说明替代，并提示后续补图                                               |


对话中应 **分步提问**，避免一次倾倒过长；每步可给出「示例句式」供用户改写。

---

## 第一阶段：创建订单

在用户未付款且未提供凭证时，必须先下单。

### 1. 所需参数

- `<技术主题>`：用户拟申请专利的发明方向、应用场景或希望保护的技术要点（一句话或多句均可）。

### 2. 执行命令

将路径替换为你工作区中本技能实际位置；**参数务必加引号**。

```bash
python3 skills/clawtip-invention-patent/scripts/create_order.py "<技术主题>"
```

脚本默认将 `SKILL_SERVER_BASE_URL` 设为主机根地址（如 `http://api.clawtip.top`），再拼接 `/api/clawtip/...`；**请勿**把 `SKILL_SERVER_BASE_URL` 写成带 `/api` 的完整 API 根，以免路径重复。仅当需要指向其他环境时，再覆盖该环境变量。

### 3. 输出处理

**成功时** 脚本打印：

```
ORDER_NO=<值>
AMOUNT=<值>
ENCRYPTED_DATA=<值>
PAY_TO=<值>
```

提取四元组，进入 **第二阶段**。

> [!NOTE]
> **关于 `AMOUNT`：** 单位为**人民币分**。`AMOUNT=200` 表示 **2.00 元**。向用户展示时除以 100 并说明「元」。

**失败时** 脚本以非零退出，并打印：

```
订单创建失败: <错误详情>
```

若出现上述失败，**立即终止流程**，不得进入支付或撰写；仅向用户说明原因。

---

## 第二阶段：支付处理（clawtip）

**操作：** 使用技能 **`clawtip`** 处理支付并获取支付凭证（支付凭证 `credential`）。**若环境中不存在该技能，须先安装 clawtip 支付技能后再继续。**

**调用参数示例（可按上架信息调整 `skill-id` 等）：**

```json
{
  "skill-id": "si-invention-patent-draft",
  "order_no": "<ORDER_NO>",
  "amount": "<AMOUNT>",
  "question": "<与第一阶段相同的技术主题>",
  "payTo": "<PAY_TO>",
  "encrypted_data": "<ENCRYPTED_DATA>",
  "description": "中国发明专利撰写引导（单次）",
  "skill_name": "发明专利撰写助手",
  "resource_url": "http://api.clawtip.top/api"
}
```

等待支付成功后再进入第三阶段。

---

## 第三阶段：履约校验

在取得 `credential` 后（或用户已同时提供三要素时），执行服务脚本。

### 1. 执行命令

```bash
python3 skills/clawtip-invention-patent/scripts/service.py "<技术主题>" "<订单号>" "<支付凭证>"
```

### 2. 输出约定

- 解析控制台中的 `PAY_STATUS:`。
- `**PAY_STATUS: SUCCESS**`：支付与履约校验通过。脚本可能随后打印一段 **JSON**（服务端返回的 `answer`），其中含 `user_topic`、`message` 等；阅读后进入 **第四阶段**。
- `**PAY_STATUS: ERROR`**：读取 `ERROR_INFO:`，向用户说明，**不得**开始撰写。
- `**PAY_STATUS: PROCESSING`**：告知用户稍后再试。

---

## 第四阶段：支付成功后的对话撰写

仅在 **第三阶段输出 `PAY_STATUS: SUCCESS`** 之后执行本节。

### 1. 对话策略

1. **确认主题**：用用户 `技术主题` 与订单 JSON 中的 `user_topic` 对齐，简要复述待保护点。
2. **分块撰写**：按「模板结构」顺序推进；每步先问缺什么信息，再生成该节草稿。
3. **权利要求书**：先协助独立权利要求，再引导从属权利要求。
4. **免责声明**：明确本输出为**草稿**，不构成法律意见；正式递交需由专利代理机构或申请人审阅、修改并符合国家知识产权局格式要求。
5. **语言**：全程 **中文**。

### 2. 禁止行为

- 支付未成功或 `PAY_STATUS` 非 `SUCCESS` 时，不得进行专利全文撰写引导。
- 不得跳过第三阶段脚本输出自行假设「已支付」。

---

## 开发检查清单（发布前）

- `create_order.py` 成功时输出 `ORDER_NO`、`AMOUNT`、`ENCRYPTED_DATA`、`PAY_TO`
- 失败时以 `订单创建失败:` 开头且 `exit(1)`
- `SKILL.md` 中第二阶段 JSON 已按需填写 `skill_name`、`description`、`resource_url`
- `service.py` 接受三参数且输出含 `PAY_STATUS:`
- 后端 `order_amount_fen` 与技能标价一致（本技能为 **200** 分 = 2 元）

---

## 联系与扩展

服务端实现可参考仓库内 `api/clawtip` 与《技能开发指南》。线上服务地址：**`http://api.clawtip.top/api`**。若需调整单价，请同步修改服务端配置 `order_amount_fen` 与本说明中的用户展示文案。

---

## 许可（License）

与 **ClawHub** 一致：**在 ClawHub 发布的技能均采用 MIT-0。**

> All skills published on ClawHub are licensed under MIT-0. Free to use, modify, and redistribute. No attribution required.

本技能所附 **SKILL.md** 与 **scripts/** 下的内容按 **MIT No Attribution（SPDX：`MIT-0`）** 提供：可自由使用、修改、再分发；**无需署名**。以「原样」提供，不作任何明示或默示担保。

参考：[MIT-0（SPDX）](https://spdx.org/licenses/MIT-0.html)

---

## 致谢与开发者联系

感谢您使用本发明专利撰写技能。若对接入、支付、履约或文档有任何疑问，欢迎发邮件联系：**43865140@qq.com**。