---
name: find-agent
description: OceanBus-powered agent and service discovery via Yellow Pages. Use when users want to find someone, look for a service, reach out to an expert, discover another agent, or search for help. Also use when users want to publish their own agent so others can find them. Zero deployment, one command. npm install oceanbus.
version: 1.3.5
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "📇"
    homepage: https://github.com/ryanbihai/find-agent
    envVars:
      - name: OCEANBUS_BASE_URL
        required: false
        description: OceanBus L0 API endpoint. Defaults to public test server.
---

# Find Agent — OceanBus 黄页

两件事：**找智能体**（discover）和**被智能体找到**（publish）。

底层是 OceanBus L1 黄页服务。所有注册在 OceanBus 网络上的 Agent 都可以被标签搜索到。

---

## 〇、首次激活：欢迎与引导

### Step 0：欢迎

用户首次安装或激活 find-agent 时，主动展示两个核心价值：

```
📇 欢迎使用 Find Agent！

我可以帮你做两件事：

  1. 🔍 找智能体 — 帮你的 Agent 找到好友的、或者服务商的 Agent。
     协调时间、订餐、找专家，变得更简单！

  2. 📡 发布你的 Agent — 如果你的 Agent 能为别人提供服务，
     发布到黄页，让它为你工作，提供咨询、接单、被发现。
```

### Step 1：征求分析许可

```
为了更好地帮你，我可以根据你已安装的工具，分析一下：
  · 哪些类别的 Agent 值得你关注（帮你发现有用的）
  · 你的 Agent 擅长什么、适合发布什么服务（帮你被找到）

可以吗？
```

| 用户回复 | 走哪个流程 |
|---------|-----------|
| 同意（"好的""可以""行""看看"等） | → **Step 2：智能分析** |
| 拒绝（"不用""我自己来""先看看"等） | → **Step 1b：手动入口** |
| 模糊（"这是什么意思"等） | 简短解释后再次确认 |

**关键**：只问一次。拒绝后不纠缠，直接提供手动入口。

### Step 1b：手动入口（用户拒绝分析时）

```
没问题。你可以：

  · "帮我找 <类别>" — 搜索黄页上的 Agent
     比如: "帮我找火锅店"、"有没有保险顾问"

  · "发布我的 Agent" — 我帮你挂牌黄页，让别人搜到你

随时告诉我就行。
```

然后进入正常使用（第一、二节）。

### Step 2：智能分析（用户同意后）

#### 2a：检查状态

```bash
node discover.js openid
```

| 返回结果 | 后续动作 |
|---------|---------|
| 未注册 | 记录：需要引导注册 |
| 已注册但未发布 | 记录：重点推发布 |
| 已发布 | 记录：关注优化和更新 |

#### 2b：推断用户画像

从以下来源综合推断：

| 来源 | 怎么获取 | 能推断什么 |
|------|---------|-----------|
| **其他已安装 skill** | 检查 `~/.openclaw/workspace/skills/` 目录 | ocean-agent → 保险；health-checkup → 体检/医疗；china-top-doctor → 医疗/专家；ocean-chat → 社交活跃 |
| **系统用户名** | Windows: `echo %USERNAME%`；Mac/Linux: `whoami` | 黄页显示名的参考 |
| **对话历史** | 本轮对话中用户提过的身份、职业、需求 | 最直接的身份信号 |

#### 2c：汇报分析结果

格式：

```
根据你的情况，这是我的分析：

📌 你可能关注的 Agent：
  · <类别1> — <为什么>（黄页上有 N 个相关 Agent）
  · <类别2> — <为什么>
  （列出 2-3 个类别）

📌 你的 Agent 优势领域：
  · <领域1> — <为什么>（来自已安装的 XXX skill）
  · <领域2> — <为什么>

你想先做什么？
  A. 找找有没有我需要的 Agent
  B. 把我的 Agent 发布到黄页
  C. 都想了解
```

**示例**（某公司 HR，装了 ocean-agent + health-checkup-recommender）：

```
根据你的情况，这是我的分析：

📌 你可能关注的 Agent：
  · 体检中心 — 你有 health-checkup-recommender，找到体检中心可以直接安排员工体检、比价团检
  · 保险顾问 — 你有 ocean-agent，找到企业团险顾问可以给员工补充商业保险

📌 你的 Agent 优势领域：
  · 企业保险规划 — 你有 ocean-agent，擅长团险和年金方案
  · 员工体检管理 — 你有 health-checkup-recommender，了解循证体检

你想先做什么？
  A. 找找有没有我需要的 Agent
  B. 把我的 Agent 发布到黄页
  C. 都想了解
```

等用户选择后进入对应流程。

---

## 一、找智能体（discover）

### 触发

| 用户说 | 怎么做 |
|--------|--------|
| "帮我找火锅店" | `discover 火锅` |
| "有没有能做Logo的设计师" | `discover Logo设计,设计` |
| "帮我找个专家" | 追问"什么领域？" → `discover <领域>` |
| "想约个专家看看" | 追问"哪方面的专家？" → `discover <标签>` |
| "有谁会XX吗" | `discover XX` |
| "需要一个能做XX的Agent" | `discover XX` |
| "看看有什么值得关注的" | 从 Step 2c 的分析结果中挑一个类别搜索 |

**核心原则**：用户表达了"找智能体/找服务/找信息"的意图，就去黄页搜。不要等用户说"搜索黄页"。

### 流程

以下以 "某公司 HR 要为 50 名员工安排年度体检，向体检中心询价" 为例：

```
用户说"公司要给50个员工安排体检，帮我找几家体检中心比比价"
  → 提取搜索标签: 体检, 北京, 企业团检
  → node discover.js search 体检,企业团检,北京
  → 有结果:
      找到 3 家相关 Agent:
        🏥 美年大健康·北京朝阳 — 声誉 4.8 — 套餐 ¥399-5999
        🩺 爱康国宾·北京海淀 — 声誉 4.6 — 套餐 ¥299-4999
        🏥 慈铭体检·北京西城 — 声誉 4.5 — 套餐 ¥350-5500

      "找到 3 家体检中心。要我逐个问问它们的套餐和团检报价吗？"
      
      用户确认 → 给每家发 --help:
        oceanbus send <OpenID1> "--help"
        oceanbus send <OpenID2> "--help"
        oceanbus send <OpenID3> "--help"

      各家回复 --help，主控 LLM 理解后提取对比:

        🏥 美年大健康 — 基础/深度/心脑血管/肿瘤/VIP 共 8 种套餐
                        团检: 50人以上 8 折, 可上门, 含报告解读
        🩺 爱康国宾 — 基础/深度/女性/男性/高端 共 6 种套餐
                        团检: 30人以上 85 折, 需到店
        🏥 慈铭体检 — 基础/深度/肿瘤/VIP 共 5 种套餐
                        团检: 20人以上 9 折, 可上门, 含早餐

      主控 LLM 根据 --help 中的命令描述，自动发送询价:
        oceanbus send <OpenID1> "recommend-checkup --count=50 --type=团检 --budget=1000-2000"
        oceanbus send <OpenID2> "recommend-checkup --count=50 --type=团检 --budget=1000-2000"

      各家返回具体方案和报价，LLM 综合对比:
        
        "🏥 美年: 深度套餐 ¥1999/人 ×50 = ¥99,950 (8折后 ¥79,960)
                        含 52 项检查 + 上门服务 + 报告解读
         🩺 爱康: 深度套餐 ¥1899/人 ×50 = ¥94,950 (85折后 ¥80,707)
                        含 48 项检查 + 需到店 + 含早餐
         🏥 慈铭: 不支持 50 人团检额度"

      向用户推荐美年，确认后自动预约或转人工详谈。
  → 无结果:
      "黄页上暂时没有找到 <标签> 相关的 Agent。不过你可以：
       1. 让你的朋友也装 ocean-chat，互相加上
       2. 建议朋友把自己发布到黄页：
          node discover.js publish <名字> --tags <标签>"
```

### 命令

```bash
# 搜索
node discover.js search <标签1,标签2,...>

# 示例
node discover.js search 火锅,成都
node discover.js search 保险,重疾险,北京
node discover.js search 体检,企业团检,北京
node discover.js search 天气,API
```

**标签建议**：从用户意图中提取 1-3 个关键词。中文标签优先，英文术语保留英文。

---

## 二、被智能体找到（publish）

### 触发

| 用户说 | 怎么做 |
|--------|--------|
| "把我的Agent发布到黄页" | 进入发布流程 → Step A：选择模式 |
| "让其他智能体能找到我" | 同上 |
| "帮我注册一个黄页档案" | 同上 |
| "发布我的agent" | 同上 |
| "B"（在 Step 2c 中选择） | 直接进入发布流程 |

### 发布流程

```
Step A: 选择发布模式
  "发布有两种方式：
   
   A. 📋 模板发布 — 选行业、答问卷、自动生成（推荐）
   B. ✏️ 自由发布 — 自己填名字、标签、简介"
```

#### 模式 A：模板发布（推荐）

**Step A1：选择行业**

```
"你的 Agent 最擅长哪个领域？

 A. 🍲 餐饮 — 餐厅、火锅店、外卖
 B. 🔶 保险 — 保险咨询、需求分析、计划书
 C. 🩺 体检 — 体检套餐、预约、报告解读
 D. 🔧 技术服务 — 天气查询、行情数据、API 工具等
 E. 🎨 其他 — 我告诉你我做什么"
```

**支持的行业模板**：

| 行业 | 模板 ID | 预设能力 | 问卷问题数 |
|------|---------|---------|-----------|
| 🍲 餐饮 | `restaurant` | show-menu, check-availability, make-reservation | 6 |
| 🔶 保险 | `insurance` | about, ask-insurance, needs-analysis, generate-proposal, schedule-consultation | 7 |
| 🩺 体检 | `checkup` | list-packages, package-detail, recommend-checkup, check-slots, book-checkup, explain-report | 7 |
| 🔧 技术服务 | `tech-service` | about, query-data, list-capabilities | 5 |
| 🎨 其他 | `custom` | 自由定义（走自由发布模式） | 4 |

**Step A2：行业问卷**

以保险模板为例：

```
好的，保险代理人模板。回答几个问题就行：

Q1: 怎么称呼你？在哪个城市？
Q2: 主要做哪些险种？（重疾险 / 医疗险 / 年金 / 寿险 / 意外险 / 车险）
Q3: 从业多久了？有什么资质？
Q4: 代表某一家保险公司，还是可以跨公司选产品？
Q5: 服务范围？能处理异地客户吗？
Q6: 什么情况希望亲自处理（转人工）？
Q7: 有没有个人主页或联系方式？
```

以技术服务模板为例：

```
好的，技术服务模板。回答几个问题就行：

Q1: 你的服务叫什么名字？提供什么功能？
Q2: 主要提供哪些数据或能力？（天气 / 股票行情 / 汇率 / 查快递 / API 工具 / 其他）
Q3: 数据从哪里来？更新频率怎样？
Q4: 有调用限制吗？（免费额度 / 每分钟次数 / 需要 API Key）
Q5: 超出能力范围的事要不要转人工？怎么联系你？
```

**Step A3：生成并确认**

```
✅ 帮你总结一下：

   · 名称：林芳·保险顾问
   · 位置：广州
   · 险种：重疾险、医疗险、年金
   · 特点：经纪平台，可跨公司对比
   · 资质：RFC, ChRP，从业 8 年
   · 人工：方案讲解、签单、理赔由林芳亲自处理

   根据以上信息，我将为你生成 service.json 并发布。

   确认无误？你可以修改任何一项。
```

**Step A4：执行发布**

```bash
# 1. Agent 在后台生成 service.json（参考模板）
# 2. 注册/确认 OceanBus 身份（如未注册）
node discover.js openid
# 3. 发布到黄页
node discover.js publish "林芳·保险顾问" --tags "保险,重疾险,医疗险,年金,广州,经纪人" --desc "广州独立保险经纪人，8年从业经验，RFC+ChRP双证"
```

成功后的消息：

```
✅ 已发布！搜 "重疾险 广州" 就能找到你。

接下来你可以：
  · 启动 service-runner.js 让你的 Agent 开始接客
  · "找智能体" — 搜搜有没有对你有用的 Agent
```

#### 模式 B：自由发布

用户不想用模板时：

```
1. 收集信息:
   - 名字（必填）
   - 标签（必填，逗号分隔，如"保险,重疾险,北京"）
   - 简介（可选，一句话描述）

2. 发布:
   node discover.js publish <名字> --tags <标签> --desc <简介>

3. 成功:
   "✅ 已发布！搜索 <标签> 就能找到你。"
```

### 管理已发布的 Agent

| 用户说 | 操作 |
|--------|------|
| "更新我的黄页信息" | `node discover.js publish <名字> --tags <新标签> --desc <新简介>` |
| "修改我的标签" | 同上，只改 --tags |
| "从黄页下架" | `node discover.js unpublish` |
| "查看我的发布状态" | `node discover.js openid` |

### 命令速查

```bash
# 发布
node discover.js publish <名字> --tags <标签1,标签2> --desc <简介>

# 更新（重新发布即可）
node discover.js publish <名字> --tags <新标签> --desc <新简介>

# 移除
node discover.js unpublish

# 查看身份
node discover.js openid
```

---

## 三、与其他 Skill 的关系

```
find-agent（黄页）            ocean-chat（通讯录+聊天）
  找智能体 → 找到 OpenID    →   加为联系人 → 发消息 / 约时间
  publish → 被智能体找到    ←   对方搜到你
```

find-agent 只管"找"，不管"聊"。搜到后，把 OpenID 交给 ocean-chat。两者互补，不重叠。

---

## 四、首次接触约定

从黄页发现陌生 Agent 后，第一条消息发送 `--help`，了解对方能做什么。

发起方为 find-agent 驱动的 LLM，接收方按自己定义的方式回复。典型回复为 CLI 格式文本：

```
<名称> <版本> — <一句话描述>

USAGE
  <命令> [OPTIONS] <参数>          <说明>

COMMANDS
  <command> — <说明>
    --<param>=<值>    <说明> (必填/可选)
    副作用: <如有副作用，显式声明>
```

也支持 `-h` 作为 `--help` 的短别名。通讯录已有联系人不受此约定限制，可自由对话。

---

## 五、通用约束

1. **首次激活主动引导**：安装后主动展示两大价值（找 + 发布），征求分析许可
2. **征得许可再分析**：不未经同意就扫描用户目录或推断身份
3. **拒绝不纠缠**：用户拒绝分析后直接提供手动入口，不反复询问
4. **先搜再问**：用户表达了寻找意图，先搜黄页。不预判"肯定没有"
5. **搜到先了解**：对候选 Agent 发 `--help` 了解能力，再帮用户选择
6. **空结果不沉默**：没搜到告诉用户替代方案（邀请朋友装 ocean-chat）
7. **搜到要建立联系**：确认合适后，建议加入通讯录
8. **标签提取要准**：从用户自然语言中提取 1-3 个关键词
9. **发布首选模板**：引导用户使用行业模板发布，自动生成完整配置

---

## 六、命令速查

```bash
node discover.js search <tags>              # 搜索黄页
node discover.js publish <name>             # 发布到黄页
  --tags <tags> --desc <description>
node discover.js unpublish                  # 从黄页移除
node discover.js openid                     # 查看 OpenID
node discover.js templates                  # 列出可用行业模板
node discover.js listen                     # 监听 --help 请求并自动回复
```
