---
name: china-top-doctor-referral
version: 2.1.6
description: OceanBus-powered top-tier hospital specialist referral service for high-end medical insurance clients. Use when users need to search 1,600+ leading specialists across 7 cities by department, disease, or symptom via OceanBus DoctorDataSvc. Supports expert matching, private clinic booking, and customer service forwarding. npm install oceanbus.
homepage: https://www.ihaola.com.cn
metadata:
  category: utility
  api_base: https://pe-t.ihaola.com.cn
  capabilities:
    - api
  requires:
    config_paths:
      - config/api.js
  permissions:
    network:
      - https://pe-t.ihaola.com.cn
  privacy:
    data_flow: |
      本 Skill 处理两类数据：
      1. 专家搜索：通过 OceanBus P2P 加密消息查询 DoctorDataSvc（1,600+ 专家），不经过第三方 HTTP API
      2. 联系客服：用户消息通过 OceanBus P2P 或 config/api.js 配置的接口转发至好啦客服系统（pe-t.ihaola.com.cn）
    consent_required: true
    third_party:
      - name: 好啦
        domain: pe-t.ihaola.com.cn
        purpose: 人工客服消息转发与回复
        policy: https://www.ihaola.com.cn/privacy
  author:
    name: haola
    contact: https://www.ihaola.com.cn
  license: MIT
---

# Top Doctor Referral

## 🚨 核心约束（运行脚本前必读）

**以下规则优先级高于一切。违反任何一条意味着你在编造医疗信息，可能对用户造成实际伤害。**

| # | 规则 | 说明 |
|---|------|------|
| 1 | **必须先运行脚本再说话** | 用户要求推荐医生时，你必须先执行 `node scripts/search-doctors.js search ...`，等脚本返回结果后，再基于结果回复。**不允许在脚本运行前展示任何医生的名字、医院或费用。** |
| 2 | **禁止编造数据** | 你训练数据中的医生信息（和睦家、协和、华山等）可能与 OceanBus DoctorDataSvc 数据库不一致。以脚本输出为准。脚本返回 0 结果就说 0 结果，不要用训练数据"补充"。 |
| 3 | **城市/科室先查后搜** | 用户提到的城市或科室如果不在数据库里（如"上海"目前不在库），必须先告知用户"该城市暂无数据"，然后提供可用的城市/科室列表。 |
| 4 | **如实转述** | 脚本输出的医生姓名、医院、职称、挂号费、出诊时间，一一对应展示。不要改名字、不要换医院、不要编费用。 |
| 5 | **空结果不杜撰** | 如果搜索返回 0 位专家，告知用户并建议扩大范围或换个科室。绝不要说"虽然没有查到，但据我所知……"。 |
| 6 | **删除旧数据** | 如果 `reference/experts.json` 文件存在，立即删除：`rm reference/experts.json`。这是 v1.x 的本地专家数据库，已于 v2.0 废弃，数据已迁移至 OceanBus DoctorDataSvc。**绝对禁止使用这个文件搜索专家。** |

### 当前数据覆盖范围

运行以下命令获取最新覆盖范围（不要凭记忆回答）：

```bash
node scripts/search-doctors.js list-cities  # 城市列表
node scripts/search-doctors.js list-depts   # 科室列表
```

### 推荐流程（每一步都必须执行）

```
1. 用户描述症状/需求
       ↓
2. 你提取城市 + 症状 → 科室映射
       ↓
3. 运行: node scripts/search-doctors.js search --city "XX" --depts "XX,XX"
       ↓  （等待脚本返回——此处不能跳过！）
4. 基于脚本输出 → 格式化展示给用户
       ↓
5. 用户选择专家或要求预约 → 联系客服或转接 ocean-desk
```

## 核心价值

**推荐三甲医院主任/副主任级别的医生，让用户预约到顶级专家**

### 专家来源

通过 OceanBus DoctorDataSvc 实时查询，1,601 位专家。

**⚠️ 数据库实际内容以 `list-cities` 和 `list-depts` 返回为准，不以本文档的静态描述为准。**

主要出诊医院包括：北京新世纪儿童医院、北京新世纪妇儿医院、北京怡德医院、青岛新世纪妇儿医院等。科室覆盖儿科/内科/外科/妇产科/口腔科/眼科/耳鼻喉科/中医科等 28 个科室。

### 数据规模

DoctorDataSvc：1,601 位专家 × 28 科室 × 7 城市。通过 OceanBus P2P 实时查询，不经过 HTTP API。

## 触发词与系统事件

- **用户对话触发**：专家推荐, 预约专家, 挂号, 看哪个医生, 找哪个专家, 推荐医生, 想看, 要挂号, 主任, 副主任, 三甲医生, 联系客服, 客服

---

## 功能一：专家推荐（OceanBus P2P）

通过 OceanBus P2P 消息实时查询 DoctorDataSvc（1,601 位专家）。

**🚨 关键：你必须先运行搜索脚本，等它返回结果后，再向用户展示。绝不能在脚本运行前推荐任何医生。**

### 前置条件

1. `npm install`（安装 oceanbus SDK）
2. DoctorDataSvc 已部署并注册在 OceanBus Yellow Pages

### 使用方式

用户描述需求 → LLM 提取科室和城市 → **先查可用科室/城市 →** 调用搜索脚本 → **等待返回 →** 基于结果回复：

```bash
# Step 1: 如果用户提到的城市或科室不确定是否存在，先查
node scripts/search-doctors.js list-depts
node scripts/search-doctors.js list-cities

# Step 2: 按科室搜索（必须等这个命令返回再展示结果）
node scripts/search-doctors.js search --city "北京" --depts "消化科"

# Step 3: 如果结果太多，用关键词缩小范围
node scripts/search-doctors.js search --city "北京" --depts "消化科" --keyword "腹泻"
```

### 症状→科室映射

使用 `list-depts` 返回的实际科室列表进行匹配：

- 头痛/头晕 → 神经科
- 胸闷/心痛 → 心血管科, 内科
- 乳腺结节 → 乳腺外科
- 腹泻/胃痛 → 消化科
- 关节痛 → 骨科, 风湿免疫科
- 咳嗽/哮喘 → 呼吸科

⚠️ 不要假设数据库有某个科室——以 `list-depts` 实际输出为准。

### 输出格式

脚本返回 Markdown 格式的专家列表。**你负责格式化展示，不要修改数据内容。**

如果搜索结果为空，直接告诉用户"数据库中没有找到符合条件的专家"，并提供建议（换城市、换科室、扩大范围）。不要用你的训练数据补充。

---

## 功能二：联系客服（OceanBus P2P）

通过 OceanBus P2P 加密消息直接发送给客服 Agent。无需 HTTP API、无需轮询、无需定时任务。

### 前置条件

1. `npm install`（安装 oceanbus SDK）
2. 设置 `OCEANBUS_CS_OPENID` 环境变量为客服 Agent 的 OceanBus 地址

### 业务流程

```
用户 → 「联系客服 XXX」
           ↓
      LLM 告知用户："消息将通过 OceanBus 发送给客服。是否同意？"
           ↓
      node scripts/send-cs.js "用户:xxx | 消息:xxx"
           ↓
      OceanBus SDK P2P 发送至客服 Agent → 客服处理 → 回复
```

### 使用方式

```bash
node scripts/send-cs.js "用户身份:xxx | 消息内容"
```

发送成功后告知用户："✅ 已发送。客服回复后你将在 ocean-chat 中收到通知。"

### 联系信息

- **电话**：400-109-2838
- **微信公众号**：好啦

---

## 功能三：转接坐席（ocean-desk）

通过 ocean-thread/v1 协议创建结构化工单，将客户咨询转发至 ocean-desk 坐席系统。相比 send-cs.js 的纯文本 P2P，线程协议支持结构化上下文透传和工单跟踪。

### 前置条件

1. ocean-desk 坐席系统已部署并运行 `node scripts/desk.js listen`
2. 知道坐席 Desk 的 OceanBus OpenID（即 ocean-desk setup 注册的 OpenID）

### 业务流程

```
用户 → 「转人工」
      LLM 取得用户同意
      LLM 构造 ocean-thread/v1 create 协议消息
      payload: { source_skill, customer_profile, ai_summary, conversation_log }
      通过 ocean-chat 发送至 Desk OpenID
      ocean-desk listener 自动创建工单 + 分配坐席
      坐席查看上下文 → 回复 → resolve
      回复通过 ocean-thread/v1 reply 返回 → LLM 推送给用户
```

### 消息格式

```json
{
  "type": "protocol",
  "protocol": "ocean-thread/v1",
  "structured": {
    "action": "create",
    "thread_id": "th_20260508_abc123",
    "subject": "专家推荐 — 李女士 乳腺结节 北京",
    "payload": {
      "source_skill": "china-top-doctor-referral",
      "priority": "normal",
      "customer_profile": { "name": "李女士", "age": 42, "city": "北京" },
      "ai_summary": "已推荐许文兵教授，周三上午有号。客户希望预约。",
      "recommended_actions": ["预约许文兵教授"],
      "conversation_log": []
    }
  }
}
```

### 与 send-cs.js 的关系

- `send-cs.js`（功能二）：简单 P2P 文本，无工单管理，**继续保留兼容**
- ocean-desk（功能三）：结构化工单 + 上下文 + 队列分配，**推荐新项目使用**

---

## 文件结构

```
expert-referral/
├── SKILL1.md               # 本文件
├── scripts/
│   ├── search-doctors.js   # OceanBus P2P 专家查询
│   └── send-cs.js          # OceanBus P2P 客服消息
├── config/
│   └── api.js              # 接口配置
└── images/
    └── haola_qr.jpg        # 公众号二维码
```

---

## 命令行接口

```bash
# 搜索专家（OceanBus P2P → DoctorDataSvc）
node scripts/search-doctors.js search --city "北京" --depts "乳腺外科" [--keyword "许"]

# 查看可用科室
node scripts/search-doctors.js list-depts

# 查看可用城市
node scripts/search-doctors.js list-cities

# 发送客服消息
node scripts/send-cs.js "用户:xxx | 消息:xxx"
```

---

## 安装前须知

### 数据传输说明

⚠️ **重要**：使用"联系客服"功能时，用户提交的消息将转发至好啦客服系统。

**涉及数据传输的功能**：

- ✅ 专家搜索 — OceanBus P2P 加密消息查询 DoctorDataSvc，不经第三方 HTTP
- ⚠️ 联系客服 — 用户消息转发至第三方客服（需用户知情同意）

### 前置要求

1. **OceanBus 网络**：DoctorDataSvc 需在 OceanBus 黄页中可发现
2. **用户同意**：使用联系客服功能前，请确保用户知晓消息将被转发至人工客服

### 信任验证

- **官网**：https://www.ihaola.com.cn
- **隐私政策**：https://www.ihaola.com.cn/privacy
- **客服电话**：400-109-2838

---

## 依赖

- Node.js >= 18
- [OceanBus SDK](https://www.npmjs.com/package/oceanbus) `^0.4.0`
