---
name: "data-prompt-coach"
slug: "data-prompt-coach"
displayName: "Data Prompt Coach 数据分析Prompt引导教练"
description: "数据分析 Prompt 引导教练+教程蒸馏自进化。触发『启动数据分析』『CRISP-DM』『我有 CSV 想端到端分析』『蒸馏教程』→双入口（8 场景+26 方法论+自修改预审+回滚）。Do NOT use for 直接接入生产数据库、ML 建模、纯摘要。"
version: "3.4.4"
license: "MIT-0"
summary: "v3.4.4 ClawHub 审计 concern 整改版：修复 SkillSpector 3 项 LLM concern（Credentials/Instruction Scope/Purpose Capability）+ HTTP 库 YARA 措辞。M22+M23+M25+M26 添加脱敏门控+目的限定+401/403 边界+UA 措辞修订+统一 dual_storage 脱敏版。基于 v3.4.3（硬门禁合规）+ v3.4.2（[SDI-4]+[SQP-1]+[SQP-2] HIGH 修复）+ v3.4.0（M22-M26 爬虫强化）+ 26 原子方法论库 + 8 场景。"
allowed-tools: "Read,Write,Edit,Glob,Grep,WebFetch"
metadata:
  openclaw:
    skillKey: "data-prompt-coach"
    emoji: "🎯"
    homepage: "https://github.com/EdwardWason/data-prompt-coach"
    os: ["windows", "macos", "linux"]
    requires:
      bins: []
      env: []
    primaryEnv: ""
    envVars: []
    always: false
---

# Data Prompt Coach v3.4.4 — ClawHub 审计 concern 整改版

> v3.4.4：修复 ClawHub SkillSpector LLM 审计 3 项 concern（Credentials/Instruction Scope/Purpose & Capability）+ M23 <HTTP library with TLS fingerprint simulation> YARA 误报措辞。
> v3.4.3：外迁大段内容到 references/audit/ + references/routing/，回应 SKILL.md ≤300 行硬门禁 + description ≤250 字符硬门禁。
> v3.4.2：修复 ClawHub SkillSpector 3 项 HIGH 发现（[SDI-4] 代码产出边界 + [SQP-1] 反路由保护 + [SQP-2] 缓存/破坏性重写安全控制）。
> v3.4.1：安全合规强化（预写审批+敏感脱敏+爬虫合规+凭证保护+脚本备份）。
> v3.4.0：M22-M26 爬虫能力深度强化（SPA 动态 API/动态 Key/增量 ID/HTML 定位/飞书双存储）。
> v3.3.2：触发引导深度强化（置信度分级+输出反推+用户原话示例库+onboarding 完整版）。

## 任务

通过 **双入口架构**服务两类需求：

- **入口 A 引导入口**：为用户的数据分析需求生成高质量 Prompt（覆盖 **8 场景** + 26 方法论触发信号 + CRISP-DM 7 步全流程）
- **入口 B 蒸馏入口**：从教程中萃取方法论，自动挂载到原子方法库（自我进化）

两个入口共享 **26 原子方法论库**（M1-M11 基础 + M12-M16 蒸馏扩展 + M17-M21 v3.3 D1 教程蒸馏 + M22-M26 v3.4.0 爬虫强化）。

## 权限声明

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ✅ | WebFetch 抓取用户提供的 URL（仅场景 1 网页采集引导）；抓取前必检查 robots.txt 和 ToS（详见 [security-compliance.md](references/audit/security-compliance.md) § 2） |
| 文件读写 | ✅ | 读：用户样表/资料；写：① 蒸馏入口产出 `references/methods/M{N+1}-*.md` + 索引/路由/测试；② 引导入口生成 .bat/CSV/JSON/Python 模板到用户工作目录（用户明确要求时） |
| 环境变量 | ⚠️ | 本技能自身不读取环境变量，但生成的爬虫/飞书存储代码会从用户 `.env` 读取 Token，禁止硬编码（详见 [security-compliance.md](references/audit/security-compliance.md) § 3） |
| subprocess | ❌ | 无（仅生成 .bat 模板文件，不直接执行） |
| 外部 API | ⚠️ | 本技能自身不调用外部 API，但生成的爬虫代码会调用目标网站 API，飞书存储代码会调用飞书 OpenAPI（必须遵守服务条款和限频） |

## 自修改能力披露

⚠️ **本技能蒸馏入口（Entry B）具有自修改能力**：方法库自扩展 + 路由矩阵自更新 + 测试用例自追加 + 引用图自维护。

**用户须知**：蒸馏入口完成后必须人工审查 diff；单次挂载上限 5 个方法论；自修改仅限本技能目录内，不影响其他技能或全局配置。

### 🔒 预写审批机制（v3.4.1 强制）

执行 L0.4 RIA++ 挂载前，必须先输出"挂载预审清单"等待用户确认（包含即将创建/修改文件清单、影响范围评估、风险声明）。**铁律**：
- 🚫 禁止未经用户确认就执行 L0.4 挂载
- 🚫 禁止挂载超出预审清单的文件
- 🚫 禁止在用户拒绝后用"已部分挂载"为由继续
- ✅ 用户回复"确认挂载"后逐项执行并实时报告进度

### 🔒 破坏性重写先备份规范（v3.4.2 强制）

L0.4 挂载时对"已存在文件的修改"必须先备份再写入。详细备份策略表、回滚函数实现、回滚命令使用方法见 [rollback-policy.md](references/audit/rollback-policy.md)。

**铁律**：
- 🚫 禁止直接覆盖已存在文件而不先备份
- 🚫 禁止 `.backup/` 目录被提交到 GitHub（已在 `.gitignore` 排除）
- ✅ 必须在挂载报告中输出"已备份文件清单 + 备份目录位置"
- ✅ 必须提供回滚命令：`python scripts/rollback_mount.py --to <timestamp>`

## 安全合规边界

详细原则见 [security-compliance.md](references/audit/security-compliance.md)，包含 4 大节：

1. **敏感数据处理原则**：数据最小化 + 脱敏优先 + 本地优先 + 云端存储前脱敏（含 4 类样本字段表 + 脱敏建议 + 二次脱敏铁律）
2. **爬虫合规边界**：7 条铁律（robots.txt + ToS + 礼貌限流 + 真实 UA + 禁止绕过认证 + 公开数据 + 数据用途限制）
3. **凭证保护原则**：4 条铁律（禁止硬编码 + 本地保存限制 + 示例脱敏 + Token 失效处理）+ .env 文件规范 + 日志脱敏
4. **自动化脚本安全提示**：生成前告知 6 项副作用 + 等待用户确认 + 提供备份建议

## 双入口路由

| 入口 | 触发词 | 流程 |
|------|--------|------|
| **A 引导** | `启动数据分析` / `引导数据分析` / `你能做什么` / `有哪些场景` / `SQL Prompt` / `我有一堆简历` / `我有 CSV 想端到端分析` / `CRISP-DM` / `完整分析全流程` / `从问题到报告` / `requests.get 抓不到` / `Algolia` / `飞书多维表格双存储` | L1 场景预识别（含 onboarding）→ L2 资料感知访谈 → L3 路由+生成 → L4 多物交付 |
| **B 蒸馏** | `蒸馏教程` / `萃取方法论` / `榨干教程` / `提取教程方法论` | L0.1 整体理解 → L0.2 5 维度并行提取 → L0.3 三重验证 → L0.4 RIA++ 挂载（含预审） |

**模糊判定**：用户给 URL/PDF/MD 但没说"蒸馏" → 反问"你要做数据分析（引导）还是蒸馏教程（萃取方法论）？"

### 场景识别快速路径

详细触发引导、方法论咒语表、场景联动、反路由保护清单见 [trigger-guide.md](references/routing/trigger-guide.md)；用户原话示例 + 完整 onboarding 菜单见 [quickstart-examples.md](references/routing/quickstart-examples.md)；能力总览 + 场景流转图见 [capability-map.md](references/routing/capability-map.md)。

| 用户说（强信号词） | 置信度 | 直接锁定场景 | 默认方法论组合 |
|------------------|-------|------------|---------------|
| "CRISP-DM""端到端分析""从问题到报告""完整分析全流程""我有数据想分析""CSV 想知道" | **S 级** | **场景 8 完整分析全流程** | **M1+M2+M7+M17+M18+M19+M20** |
| "抓数据""爬取""网页表格""基金排行榜" | A 级 | 场景 1 网页采集 | M1+M2+M7 |
| "简历""合同""发票""名片""抠字段" | A 级 | 场景 2 文档字段提取 | M1+M2（<100）/ M1+M2+M6（>100） |
| "写 SQL""JOIN""子查询""聚合" | A 级 | 场景 3 SQL 生成 | M3+M10+M2 |
| "对账""核对""两张表对得上""报销" | A 级 | 场景 4 数据核对 | M2+M7 |
| "打标签""分类""标注""工单""用户反馈" | A 级 | 场景 5 批量分类标注 | M5+M2 |
| "周报""合并""汇总""完成率""风险预警" | A 级 | 场景 6 周报敏捷分析 | M1+M7+M4 |
| "深度分析""报告""1500 行""HTML 报告" | B 级 | 场景 7 深度洞察报告 | M8+M9 |

**关键触发规则**：
1. 优先匹配 S 级词 → 直接锁定场景 8，跳过模糊判定
2. A 级词需配套数据源/任务类型确认
3. B 级词必反问"深度报告（场景 7）还是端到端分析（场景 8）？"
4. 多信号冲突按场景优先级：场景 8 > 场景 7 > 场景 6 > 其他
5. 场景 8 教学特化触发：用户说"教学""学习""背答案""数据陷阱"时追加 M21
6. 场景识别失败：反问"这是采集/提取/SQL/核对/标注/周报/深度报告/完整分析全流程哪一类？"或 Read [quickstart-examples.md](references/routing/quickstart-examples.md) 展示示例

### 模糊触发反路由保护（v3.4.2 新增，回应 [SQP-1]）

⚠️ 8 类通用短语（"帮我分析一下""整理一下""看下这个""处理一下""有什么建议""画个图""写个报告""做个表"）禁止自动路由到数据处理工作流。详细清单和反路由铁律见 [trigger-guide.md](references/routing/trigger-guide.md) § 模糊触发反路由保护清单。

**核心铁律**：① 数据缺失即不路由 ② 意图不明确即反问 ③ 3 轮内必须收敛 ④ 拒绝猜测性路由

---

## 入口 A：引导入口工作流程

### Step A1: 场景预识别（L1，含 onboarding）

读取 [scenario-router.md](references/routing/scenario-router.md) + [trigger-guide.md](references/routing/trigger-guide.md) + [capability-map.md](references/routing/capability-map.md)，按数据源 + 任务类型识别 8 场景候选。

**首次启动 onboarding**（v3.3.1 新增，v3.4.3 外迁）：当用户说"启动数据分析""引导数据分析""你能做什么""有哪些场景"等首次接触信号词且未提供具体需求时，**必须 Read [quickstart-examples.md](references/routing/quickstart-examples.md) § 完整 onboarding 菜单**展示给用户。用户已提供强信号词时跳过 onboarding。

**8 场景**：1 网页采集 / 2 文档字段提取 / 3 SQL 生成 / 4 数据核对 / 5 批量分类标注 / 6 周报敏捷分析 / 7 深度洞察报告 / **8 完整数据分析全流程（v3.3 新增，CRISP-DM 7 步）**。

**触发引导硬规则**（详见 [trigger-guide.md](references/routing/trigger-guide.md) § 触发引导快速参考）：① 不凭记忆工作 ② 首次启动必展示 onboarding 菜单 ③ 场景识别失败必 Read quickstart-examples.md ④ 用户问能力必 Read capability-map.md ⑤ 场景完成后必按流转图提示下一步。

### Step A2: 资料感知访谈（L2+，v3.0 增强）

读取 [interview-flow.md](references/routing/interview-flow.md)，按 5 要素完备性检查：范围 + 字段 + 处理规则 + 输出格式 + 异常处理。

**v3.0 增强**：资料感知（根据场景主动要求样表/DDL/标签体系/上周报告）+ 资料分析（调用对应分析器回填 5 要素）。

**访谈原则**：① 最少 3 轮 ② 一次一问 ③ 方向性建议 ④ 该问到完备为止 ⑤ 可降级（用户主动说"差不多就行"立即用当前信息生成）。

### Step A3: 智能路由（L3）

读取 [method-composition.md](references/routing/method-composition.md)，基于场景 + 数据规模匹配方法论组合。8 场景的方法论组合矩阵详见 [method-composition.md](references/routing/method-composition.md) § 场景组合矩阵。

**v3.1 叠加规则**：M12↔M13 成对、M15↔M16 成对、M14+M6+M7 三件套、单场景最多叠加 3 个 v3.1 方法论。

**v3.3 叠加规则**：M17/M18/M19/M20 在场景 8 默认成套挂载（CRISP-DM 7 步骨架不可拆分）；M21 仅在教学场景信号触发时挂载；单场景最多叠加 5 个 v3.1+v3.3 方法论。

**v3.4.0 叠加规则**：M22 默认追加到场景 1（80% 现代网站是 SPA）；M23 触发自动追加 M22；M24 触发自动追加 M14+M6；M25 仅在 AI 识别失败时由用户主动调用；M26 触发自动追加 M14+M24。

### Step A4: 多物交付（L4+，v3.0 新增，v3.3 扩展）

读取 [references/asset-templates/](references/asset-templates/) 按场景路由交付物。8 场景交付物清单详见 [method-composition.md](references/routing/method-composition.md) § 交付物清单。

**4 段结构（v2.0 保留）+ 附加交付物（v3.0 新增）+ 场景联动提示（v3.3.1 新增）**：

```
## 📋 你即将使用的 Prompt（直接复制粘贴）
## 🛡️ 防幻觉清单（本场景的关键防错点）
## ✅ 验真抽查建议（拿到结果后必做 3 件事）
## ⚙️ 场景化补充（本场景的"隐藏坑")
## 📁 附加交付物（v3.0 新增，按场景路由）
## 🔗 接下来可以做什么（v3.3.1 新增，按场景流转图主动提示 1-2 个最相关下一步）
```

**场景联动提示规则**：完成场景 N 交付后，按 [capability-map.md](references/routing/capability-map.md) § 场景流转图 主动提示 1-2 个最相关下一步（场景 1-7 完成后默认推荐场景 8；场景 7 完成后必提示场景 8；同一场景不重复提示）。

---

## 入口 B：蒸馏入口工作流程

读取 [distillation-router.md](references/routing/distillation-router.md) 完整编排。

### Step B1: L0.1 整体理解

读取 [cangjie-lite.md](references/distillation/cangjie-lite.md) § L0.1（Adler 精简版 3 步：结构拆解→主题识别→适用边界）。产出：内存概览（体裁/主题/受众/边界）。

### Step B2: L0.2 5 维度并行提取

读取 [interview-miner-adapted.md](references/distillation/interview-miner-adapted.md)，从 5 个维度并行提取候选：显性认知 → 方法论候选；隐性意图 → 陷阱候选；思维模型 → 决策框架候选；行业信号 → 触发条件候选；反常识洞察 → 独特性候选。产出：候选清单（去重 + 关联）。

### Step B3: L0.3 三重验证

读取 [three-fold-verification.md](references/distillation/three-fold-verification.md)，每个候选过 3 关：V1 跨域（原文 ≥ 2 处独立佐证）+ V2 预测力（能回答教程未明说的问题）+ V3 独特性（不是常识）。通过率目标 ≥ 50%。全部淘汰 → 终止并报告。

### Step B4: L0.4 RIA++ 挂载（v3.4.1 强化预写审批）

读取 [cangjie-lite.md](references/distillation/cangjie-lite.md) § L0.4。

**Step B4.0 挂载预审**（v3.4.1 强制门控）：① 列出 L0.3 验证通过的候选清单 ② 输出"挂载预审清单"（参考 § 自修改能力披露 → 预写审批机制） ③ 等待用户回复"确认挂载"或"先看一下候选内容" ④ 用户未确认前禁止执行 B4.1-B4.6 任何写文件操作。

**Step B4.1-B4.6**：用户确认后执行 ① 创建 `references/methods/M{N+1}-{slug}.md`（RIA++ 六维） ② 更新 `assets/INDEX.md` ③ 更新 `references/routing/method-composition.md` ④ 追加 `assets/test-prompts.json` ⑤ 淘汰候选写入 `references/audit/rejected.md`/`candidates.md` ⑥ 输出蒸馏报告。

**Step B4.7 挂载完成确认书**：新增方法论 + 修改文件清单 + 测试用例数 + 提示人工审查 git diff + 提示 git checkout 回滚。

**单次挂载上限 5 个**（超过的留 candidates.md）。**禁止行为**：跳过 B4.0 预审 / 用户拒绝后强行继续 / 挂载超出预审清单的文件。

---

## 26 原子方法论库（references/methods/）

| # | 名称 | 一句话 | 何时用 |
|---|------|--------|--------|
| M1 | 黄金五要素 | 范围+字段+规则+格式+异常 | 采集/提取类 |
| M2 | 防幻觉三招 | 亮证据+给示弱+禁脑补 | 涉及金额/人数/结论 |
| M3 | 80/20 协作 | AI 写初稿+人审业务口径 | 写 SQL/代码 |
| M4 | 任务拆解 | 提取→清洗→核对→分析 | 复杂多步任务 |
| M5 | 两级标签体系 | 一级+二级+边界+样例 | 分类标注 |
| M6 | 分批处理 | 50-100/批+对齐基准+序号 | >1000 条 |
| M7 | 验真闭环 | 标注依据+抽查+异常标记 | 任何关键输出 |
| M8 | 目标导向 | 多给目标少给绘图指令 | 深度分析 |
| M9 | 分步提问 | /plan 出大纲→确认→深挖 | 高要求报告 |
| M10 | SQL 4 必看 | JOIN/时间/去重/口径 | 审查 SQL |
| M11 | 大文件阈值 | <1500 直拖/>10万写脚本 | 大数据量 |
| M12 | 下钻触发 | 基础分析→识别有趣维度→主动追问→下钻→联动深挖 | 探索性分析 |
| M13 | 中间逻辑可追溯 | 中间产物显式+可追问+推导链完整+逻辑校验点 | AI 分析可信度 |
| M14 | 增量同步 | 指纹缓存+批量写入+频率控制+失败兜底 | 定期运行任务 |
| M15 | 迭代式可视化 | 基础代码块→美化配色→增加交互 | 图表制作 |
| M16 | 多维数据联动 | 识别维度→评估局限→选联动组合→联动交互 | 多维关系展现 |
| M17 | CRISP-DM 7 步 SOP | 问题定义→数据探索→清洗→分析→可视化→洞察→报告 | 端到端分析全流程（场景 8 默认） |
| M18 | 清洗决策审查 | 每条清洗决策记录问题+选择+理由+影响，可审计 | 数据清洗决策审计（场景 8 Step 3） |
| M19 | 图表三秒体检 | 轴标签+数据范围+图表类型三维度快速验证 | 图表正确性验收（场景 8 Step 5） |
| M20 | 相关≠因果验证 | 6 维度验证（第三变量+反向因果+时序+实验证据+机制+统计显著） | 统计因果断言验证（场景 8 Step 6） |
| M21 | AI 背答案识别 | 数据手术 5 步+自我诊断三问 | 教学场景 AI 真实分析能力诊断 |
| M22 | SPA 动态 API 识别 | 6 步识别流程：网站类型→Network 面板→请求参数→响应结构→动态参数→抓取流程 | 现代 SPA 网站抓取前置（场景 1 默认追加） |
| M23 | 动态 API Key 模拟 | 5 步模拟流程：Key 来源→追踪获取链→requests.Session 模拟→请求头完整性→Key 刷新机制 | Algolia 等动态 Key 服务（触发自动追加 M22） |
| M24 | 增量唯一 ID 设计 | 5 种策略：URL 解析 ID/API 原生 ID/字段组合哈希/内容指纹/时间戳+序号 | 增量抓取区分已抓/未抓（触发自动追加 M14+M6） |
| M25 | HTML 元素定位 | 5 步定位流程：DevTools→选元素→定位 HTML→复制→发送 AI | AI 识别失败兜底（不当默认方法论用） |
| M26 | 飞书多维表格双存储 | 6 种字段类型映射+双存储代码框架 | 本地 CSV + 飞书 Base 双写（触发自动追加 M14+M24） |

**版本演进**：v3.1 已扩展 M12-M16 / v3.3 已扩展 M17-M21 / v3.4.0 已扩展 M22-M26。后续蒸馏入口产出的 M27+ 会继续追加到此表。

## 规则

1. **双入口边界**：引导入口不挂载方法论；蒸馏入口不生成用户 Prompt
2. **主动访谈**：主控必须提方向性选项，不能让用户自己想要素
3. **一次一问**：每轮只问 1 个问题 + 2-3 选项
4. **最少 3 轮**：3 轮是下限，该问到完备为止（用户主动可降级）
5. **方法论组合**：必须从 26 原子方法论（M1-M26）中选，不能自创
6. **RIA++ 完整**：每个生成的 Prompt 必须含方法论的核心要素
7. **不替代业务口径**：涉及比率指标必须提示"请先定义分子分母"
8. **蒸馏挂载上限**：单次蒸馏 ≤ 5 个方法论，超过的留 candidates.md
9. **代码产出边界（v3.4.2 修订，回应 [SDI-4]）**：
   - ✅ **允许产出**（作为"附加交付物模板"）：SQL/DDL/JSON Schema/验真脚本骨架/Python 数据处理代码模板/.bat 自动化模板/图表代码
   - ❌ **禁止行为**：直接执行这些代码 / 写入用户系统路径 / 替代业务口径判断
   - 📌 **铁律**：所有代码交付物必须附带"使用前必读"声明（副作用清单+备份建议+用户确认门）
10. **v3.1 方法论叠加**：M12↔M13 成对、M15↔M16 成对、单场景最多叠加 3 个 v3.1 方法论
11. **v3.3 方法论叠加**：M17/M18/M19/M20 在场景 8 默认成套挂载；M21 仅教学场景触发；单场景最多叠加 5 个 v3.1+v3.3 方法论
12. **v3.3.1 触发引导强化**：首次启动 onboarding + 能力地图主动展示 + 方法论咒语可见 + 场景联动提示（详见 [trigger-guide.md](references/routing/trigger-guide.md)）
13. **v3.3.2 触发引导深度强化**：触发词置信度分级（S/A/B 级）+ 输出反推场景索引 + 用户原话示例库 + 触发引导硬规则 5 条 + onboarding 菜单完整版
14. **v3.4.1 安全合规强化**：自修改预写审批 + 敏感数据脱敏 + 爬虫合规边界 + 凭证保护 + 自动化脚本备份（详见 [security-compliance.md](references/audit/security-compliance.md)）
15. **v3.4.2 反路由保护**：8 类通用短语禁止自动路由（详见 [trigger-guide.md](references/routing/trigger-guide.md) § 模糊触发反路由保护清单）
16. **v3.4.2 破坏性重写备份**：L0.4 挂载时已存在文件必先备份（详见 [rollback-policy.md](references/audit/rollback-policy.md)）+ 回滚脚本 `scripts/rollback_mount.py`

## 示例与故障排除

详见 [examples.md](references/examples.md)（2 个端到端示例）+ [troubleshooting.md](references/troubleshooting.md)（11 条故障排除表）+ [references/examples/world-happiness-demo.md](references/examples/world-happiness-demo.md)（CRISP-DM 7 步完整演示）+ [references/examples/student-exam-challenge.md](references/examples/student-exam-challenge.md)（M21 AI 背答案识别 + 数据手术演示）。

## 来源声明

- **方法论来源**：v2.0 来自「用 TRAE Work 做数据分析的实战教程」公开文章，经 `cangjie-skill` RIA-TV++ 流水线蒸馏，11 个方法论通过验证
- **v3.0 蒸馏引擎**：内化 cangjie-skill 4 阶段精简版 + interview-insight-miner 5 维度适配版，无需安装外部 Skill
- **v3.1 教程蒸馏升级**：M12-M16 由蒸馏入口从 6 篇真实教程中萃取，2026-07-22 挂载
- **v3.3 D1 教程蒸馏升级**：M17-M21 由蒸馏入口从 D1 数据分析与可视化课程中萃取，2026-07-24 挂载
- **v3.4.0 爬虫能力强化**：M22-M26 由 TRAE 社区爬虫教程中萃取，2026-07-26 挂载（场景 1 网页采集专项强化）
- **v3.4.1 安全合规强化**：2026-07-31 引入，回应 ClawHub SkillSpector v3.2.0 Credentials concern 维度
- **v3.4.2 审计整改**：2026-07-31 修复 ClawHub SkillSpector 3 项 HIGH 发现（[SDI-4]+[SQP-1]+[SQP-2a/b/c]）
- **v3.4.3 硬门禁合规**：2026-07-31 外迁大段内容到 references/audit/ + references/routing/，回应 SKILL.md ≤300 行 + description ≤250 字符硬门禁
- 蒸馏方法详见 [references/distillation/](references/distillation/)
