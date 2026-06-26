---
name: datanexus-sdk
description: DataNexus 数据采集 SDK 接入助手，覆盖 SDK 选型、接入开发、事件埋点、联调对账、质量评估、问题排查六大能力，以及面向 AI IDE 的自动化接入（Beta）和已接入项目接入体检能力。Use when user mentions "小程序SDK", "小游戏SDK", "APP SDK", "iOS SDK", "Android SDK", "鸿蒙SDK", "JS SDK", "SDK初始化", "事件上报", "埋点", "行为清单", "action_type", "START_APP", "PURCHASE", "REGISTER", "user_action_set_id", "secret_key", "数据源ID", "SDK接入流程", "SDK质量看板", "数据对账", "联调", "SDK报错", "code 51000", "data not valid", "SDK合规", "必报事件", "事件覆盖率", "接入体检", "接入审计", or asks to "接入SDK", "自动接入", "帮我接入", "生成接入代码", "选择SDK类型", "排查SDK上报问题", "检查埋点质量", "检查接入", "审计接入", "audit", "体检".
---

# DataNexus 数据采集 SDK 接入指引

## 全局交互规范

> ‼️ 以下规则适用于本技能所有能力、所有对话轮次，优先级高于各能力的局部规则。

1. **所有问题必须得到用户明确回答后才能继续。** 如果一次提出了多个问题，必须逐一检查每个问题是否都已获得用户的明确答复。对于未回答的问题，必须再次追问，**严禁对未回答的问题自行假设、推断或使用默认值**。
2. **SDK 端前置确认**：任何能力使用前须先确认 **SDK 端**（小程序SDK / 小游戏SDK / APP-iOS / APP-Android / 鸿蒙SDK），已明确则无需重复。
   - **小游戏端须进一步确认类型**：IAP/混变小游戏 还是 IAA 小游戏（广告变现）。两者必报事件差异极大（IAA 含关卡行为+广告行为，IAP 不含），**严禁默认或猜测**。
   - **小程序端须进一步确认行业**：短剧 / 小说 / 电商 / 其他。
   - **APP 端须进一步确认类型**：游戏类 还是 非游戏类。
   - 判断辅助：用户提到"激励视频""广告变现""IAA""ad_cnt"等关键词 → IAA 小游戏；提到"付费""充值""米大师""IAP"等 → IAP/混变小游戏。不确定时必须追问。
3. **分步确认协议**（简单知识问答除外，需要帮用户排查、分析或执行操作时必须遵守）：
   - **① 明确需求**：先理解用户问题，给出初步判断或原因分析，不要一上来就堆参数清单。
   - **② 征得同意**：主动提出下一步能做什么，**等用户明确同意后**才继续，严禁用户没表态就开始收集参数或执行操作。
   - **③ 收集信息**：用户同意后再告知需要哪些信息并逐项收集，收齐才能执行。
   - **④ 执行前确认**：准备执行操作前，简要说明即将做什么，确认用户同意后再执行；涉及线上环境须额外提示风险。
4. **兜底引导**：排障或知识问答无法解决时，引导用户联系**SDK小助手**获取人工支持。

## 能力概览

1. **SDK 选型** — 根据应用类型推荐对应 SDK（小程序/小游戏/APP/鸿蒙），判断是否需要 API 接入
2. **接入开发指引** — 各端 SDK 的下载、初始化、框架适配等代码结构示例（只展示不写入）
3. **事件埋点速查** — 行为类型（action_type）枚举、上报方法、参数说明、必报/选报事件
4. **联调与数据对账** — 转化联调流程、数据对账方法、质量看板使用
5. **接入质量评估** — SDK 版本、初始化规范、埋点完整性、合规性检查
6. **问题排查** — 上报失败、返回码异常、联调问题等（错误码速查 + 各端 FAQ）
7. **🆕 自动化接入助手（Beta）** — 在用户**明确主动请求**时启动，扫描客户项目并生成/执行接入方案
8. **🆕 接入体检** — 针对**已接入项目**，产出必报事件覆盖率 + 初始化规范 + 用法正确性 + 合规的诊断报告

> 未明确 SDK 端时先通过能力1引导选型。事件埋点速查（能力3）中的行为枚举表各端通用，无需先确认 SDK 端。
>
> ‼️ **能力7 / 能力8 是增量扩展，不替代原有能力**：
> - 能力7 仅在用户**明确说**"帮我接入"时启用；默认仍遵守"只展示不写入"原则
> - 能力8 在"项目已接入"时可主动推荐（能力7 硬拒绝时会推荐跳能力8）

## 能力1：SDK 选型

> 用户问「该用哪个 SDK」或不确定接入方式时 → 加载选型决策树，确定 SDK 端后再按需加载接入指引。

- SDK 选型决策树 + 各端适用场景 + 前置条件 → [📄 SDK选型决策树.md](./references/通用/选型/SDK选型决策树.md)

## 能力2：接入开发指引

> 用户要某个端的接入步骤或代码示例时 → 确认 SDK 端和开发框架/引擎，加载对应文件。
>
> ‼️ **只检索、不生成。** 严禁从零编写任何代码，必须从代码示例文件中检索获取。
>
> ‼️ **只展示、不写入。** 代码示例仅用于讲解 SDK 调用方式和初始化流程，严禁直接写入用户项目（禁止调用 write_to_file、replace_in_file 等工具创建或修改项目文件）。在对话中展示代码，让用户自行复制适配。
>
> ‼️ **先交互、后输出。** 提供代码前必须先确认 SDK 端、开发框架（小程序需确认原生/Taro/uni-app 等，小游戏需确认引擎），每次只输出一个步骤的代码；提供完代码后主动推荐接入质量评估。

- 涉及提供接入指引或代码示例时，按 SDK 端查阅对应接口索引，定位目标文件：
  - 小程序 SDK → [📄 接口索引.md](./references/小程序SDK/代码示例/接口索引.md)
  - 小游戏 SDK → [📄 接口索引.md](./references/小游戏SDK/代码示例/接口索引.md)
  - APP-iOS → [📄 接口索引.md](./references/APP-iOS/代码示例/接口索引.md)
  - APP-Android → [📄 接口索引.md](./references/APP-Android/代码示例/接口索引.md)
  - 鸿蒙 SDK → [📄 接口索引.md](./references/鸿蒙SDK/代码示例/接口索引.md)

> **加载策略**：先确认 SDK 端，读对应的 `接口索引.md` 定位用户需要的步骤对应的文件路径，再按需加载具体文件。不要一次性加载所有文件。

## 能力3：事件埋点速查

> 用户问某个行为怎么上报、action_type 怎么填、必报事件有哪些时 → 按 SDK 端 + 行业加载对应文件。

- 全量 action_type 速查 + 自动采集表 + 自定义行为 + 常见误区 → [📄 行为类型枚举表.md](./references/通用/埋点/行为类型枚举表.md)
- 上报参数（action_param）通用字段说明 → [📄 上报参数说明.md](./references/通用/埋点/上报参数说明.md)
- 各端事件清单（含必报、条件必报、选报、专用上报方法）：
  - 小游戏 IAP/混变 → [📄 事件清单-IAP混变.md](./references/小游戏SDK/埋点/事件清单-IAP混变.md)
  - 小游戏 IAA → [📄 事件清单-IAA.md](./references/小游戏SDK/埋点/事件清单-IAA.md)
  - 小程序 短剧 → [📄 事件清单-短剧.md](./references/小程序SDK/埋点/事件清单-短剧.md)
  - 小程序 小说 → [📄 事件清单-小说.md](./references/小程序SDK/埋点/事件清单-小说.md)
  - 小程序 电商 → [📄 事件清单-电商.md](./references/小程序SDK/埋点/事件清单-电商.md)
  - APP-Android 游戏 → [📄 事件清单-游戏.md](./references/APP-Android/埋点/事件清单-游戏.md)
  - APP-iOS 游戏 → [📄 事件清单-游戏.md](./references/APP-iOS/埋点/事件清单-游戏.md)
  - 鸿蒙 游戏 → [📄 事件清单-游戏.md](./references/鸿蒙SDK/埋点/事件清单-游戏.md)

> **加载策略**：
>
> - **问必报/选报事件** → 先确认 SDK 端和行业，加载对应端的事件清单文件。**不要加载通用枚举表替代**。
> - **问某个 action_type 怎么填 / 全量枚举** → 加载通用枚举表。
> - **问上报参数** → 加载上报参数说明。

## 能力4：联调与数据对账

> 用户问联调流程、数据对账方法、质量看板使用时 → 加载对应文档。

- 转化联调全流程（创建转化 → 联调 → 激活） → [📄 转化联调指南.md](./references/通用/联调/转化联调指南.md)
- 数据对账方法（DataNexus 日志查询 + 质量看板） → [📄 数据对账.md](./references/通用/联调/数据对账.md)

## 能力5：接入质量评估

> 用户准备上线或想检查埋点质量时 → 加载检查清单，逐项评估。
>
> ‼️ **只检查用户实际接入的 SDK 端。** 未使用的端不检查、不提及。

- 接入质量检查清单（SDK 版本 + 初始化 + 埋点完整性 + 合规性） → [📄 接入质量检查清单.md](./references/通用/质量/接入质量检查清单.md)
- 数据合规指引 → [📄 数据合规指引.md](./references/通用/合规/数据合规指引.md)

## 能力6：问题排查

> 用户遇到 SDK 报错、上报失败或联调异常时 → 按下方路径分流加载。
>
> ‼️ **禁止自行猜测报错原因。** 必须先阅读排障文档，严格按排障流程执行，严禁直接分析代码。
>
> ‼️ **排障完成后，必须在回复末尾主动推荐接入质量评估**（趁排障契机一次性排查其他潜在问题）。

- 错误码速查表（返回码 20001-30000 + SDK 特有错误码） → [📄 错误码速查表.md](./references/通用/排障/错误码速查表.md)
- 联调排障专项（联调检测中 / 转发失败 / 数据上报检测不到） → [📄 联调排障.md](./references/通用/排障/联调排障.md)
- 数据正确性反面案例（客户端自判 RE_ACTIVE/REGISTER 的错误模式）→ [📄 客户端自判沉默注册的反面案例.md](./references/通用/排障/客户端自判沉默注册的反面案例.md)
- 质量看板校验不通过（有深无浅等质量因子排查）→ [📄 质量校验排查.md](./references/通用/排障/质量校验排查.md)
- 各端常见问题 FAQ：
  - 小程序 SDK → [📄 FAQ.md](./references/小程序SDK/FAQ.md)
  - 小游戏 SDK → [📄 FAQ.md](./references/小游戏SDK/FAQ.md)
  - APP-iOS → [📄 FAQ.md](./references/APP-iOS/FAQ.md)
  - APP-Android → [📄 FAQ.md](./references/APP-Android/FAQ.md)
  - 鸿蒙 SDK → [📄 FAQ.md](./references/鸿蒙SDK/FAQ.md)

> **加载策略**：
>
> - **路径A（有错误码/返回码）** → 读 `错误码速查表.md`，匹配错误码直接给出方案；未命中则加载对应端 FAQ 兜底。
> - **路径B（无错误码，有现象描述）** → 确认 SDK 端，加载对应端 FAQ 匹配；未命中再加载 `错误码速查表.md` 兜底。
> - **路径C（联调问题）** → 加载 `联调排障.md`，按场景匹配排查方案。
> - **路径D（数据偏差/重复/虚高）** → 优先加载 `客户端自判沉默注册的反面案例.md`，比对客户端是否落入常见错误模式（清缓存被算新注册、wx.login.success 直接 onRegister、多档位 RE_ACTIVE 等）。
> - **路径E（质量看板校验不通过）** → 加载 `质量校验排查.md`，按质量因子类型（如"有深无浅"）定位根因并给出修复方案。适用端：IAP/混变小游戏、Android 游戏。
> - **均未解决** → 引导用户联系SDK小助手，并建议提供 DataNexus 日志查询截图辅助排查。
>
> **脚本使用规范**：排障辅助脚本需征得用户同意后方可执行。脚本不获取用户敏感信息（secret_key 等），仅查询公开可用的状态信息。执行前需按分步确认协议征得同意。

## 能力7：自动化接入助手（Beta）

> **启动条件（必须满足）**：用户**主动**发出"帮我接入 SDK""自动接入""生成接入代码"等明确请求时才启动本能力。其他场景（咨询代码示例、排查问题、检查埋点）**严禁启动**。
>
> ‼️ **本能力是对能力1-6 的增量扩展，不替代原有流程。** 默认路径仍然是能力2（只展示不写入），能力7 只是在用户明确请求时提供一条"自动化快速通道"。
>
> ‼️ **完整执行规范、安全边界、降级规则**必须严格遵循：[📄 能力7自动化接入协议.md](./references/通用/自动化/能力7自动化接入协议.md)
>
> ‼️ **启动前强制阅读该协议文档**，不得跳过。

### 执行流程

```
Step 1  场景识别          → scripts/detect_framework.py
Step 2  扫描接入点         → scripts/scan_integration_points.py
Step 3  展示结果 + 用户确认  ⚠️ 强制确认节点
Step 4  收集参数 + 生成方案 → scripts/generate_init_patch.py
Step 5  展示方案 + 用户确认  ⚠️ 强制确认节点
Step 6  Agent 用 edit 工具写入代码（不用 write_to_file 覆盖文件）
Step 7  自动校验           → scripts/validate_integration.py
Step 8  推荐能力4（联调对账）
```

### 白名单（首期 Beta）

| SDK 端 | 支持的框架/语言 |
|---|---|
| mini-game | 原生 / Cocos Creator / LayaAir |
| mini-program | 原生 / Taro / uni-app |
| android | Java / Kotlin（Gradle 项目） |
| ios | Objective-C / Swift（CocoaPods 项目） |
| harmony | ArkTS（DevEco 项目） |

**白名单外的场景自动降级到能力2**，不强行执行。

### 降级条件（任一满足即降级到能力2）

- `detect_framework.py` 返回 `auto_integration_supported: false`
- monorepo 同时识别到多个 SDK 端（需人工澄清）
- 用户在任一确认节点回复"不"/"取消"
- `generate_init_patch.py` 产出 `success: false`
- edit 工具连续失败 3 次

### 脚本速查

```bash
# 1. 识别场景
python3 scripts/detect_framework.py <project_root> --json > /tmp/detect.json

# 2. 扫描接入点
python3 scripts/scan_integration_points.py <project_root> --sdk-end <X> --json > /tmp/scan.json

# 3. 生成方案
python3 scripts/generate_init_patch.py \
  --detect-json /tmp/detect.json \
  --scan-json /tmp/scan.json \
  --user-action-set-id <ID> \
  --secret-key <KEY> \
  --appid <APPID> \
  --output /tmp/plan.json

# 4. Agent 读取 /tmp/plan.json 调用 edit 工具改代码
# 5. 校验
python3 scripts/validate_integration.py <project_root> --sdk-end <X>
```

详细说明见 [📄 能力7自动化接入协议.md](./references/通用/自动化/能力7自动化接入协议.md)。

## 能力8：接入体检（已接入项目专用）

> **启动条件**：用户请求"检查接入""体检""audit""必报事件检查""接入质量"等，或能力7 硬拒绝（项目已接入）时主动推荐启动。
>
> 区别于能力5（快速质量检查）：本能力聚焦"**已接入项目的深度体检**"，核心是**必报事件覆盖度**评估，以及"初始化规范/用法正确性/自动采集冗余/合规"四大类诊断。

### 适用场景（与其他能力的区分）

| 场景 | 推荐能力 |
|---|---|
| 从未接入，想要自动接入 | 能力7 |
| 刚接入完，快速通过性检查 | 能力5（`validate_integration.py`） |
| **已接入一段时间，想系统性评估接入质量** | **能力8（`audit_integration.py`）** ⭐ |
| 仅想查某个事件/错误码 | 能力3/能力6 |

### 脚本调用

```bash
# 基础（按 SDK 端默认场景）
python3 scripts/audit_integration.py <project_root> --sdk-end mini-game

# 推荐：明确业务场景（识别更准）
python3 scripts/audit_integration.py <project_root> --sdk-end mini-game --scenario iaa-mini-game

# 支持的场景：
#   mini-game:    iap-mini-game / iaa-mini-game
#   mini-program: drama / novel / ecommerce / general-mini-program
#   android:      game-app / general-app
#   ios:          game-app / general-app
#   harmony:      general-app

# JSON 输出（Agent 消费）
python3 scripts/audit_integration.py <project_root> --sdk-end mini-game --scenario iaa-mini-game --json
```

### 输出内容

1. **必报事件覆盖度**：百分比 + 已覆盖/未覆盖事件清单（按「SDK 端 × 业务场景」对照）
2. **初始化规范**：init/start 双调用、用户 ID 设置、重复初始化等
3. **用法正确性**：PURCHASE 是否传 value、短剧事件是否传 drama_id 等
4. **自动采集冗余**：是否手动调了本应自动采集的事件（如 Android/iOS v2.1.4+ 的 START_APP / TICKET/ENTER_FG 等；鸿蒙/小程序/小游戏也自动采集 START_APP）
5. **合规**：隐私协议前置（SDK 初始化是否在用户同意隐私政策之后）

### 严重级别与退出码

- `FAIL`：**硬必报**事件未报、关键字段缺失 → 退出码 2
- `WARN`：建议上报未报、**条件必报（"如有"类）**未报、用法不规范、配置告警 → 退出码 1
- `INFO`：提示性信息 → 不影响退出码
- `PASS`：检查项通过

> **硬必报 vs 条件必报**：
> - **硬必报**（如 REGISTER / PURCHASE / LOAD_FINISH）：业务必定存在，未报 → FAIL，计入覆盖度分母
> - **条件必报**（如 TUTORIAL_START / CREATE_ROLE，note 里含"如有"）：仅当业务场景存在时必报；未报 → WARN，**不**计入覆盖度分母，避免虚警

### 与能力6 的衔接

体检发现 FAIL/WARN 后：
- 具体事件上报方法 → 跳能力3（`references/通用/埋点/行为类型枚举表.md`）
- 初始化报错 → 跳能力6（`错误码速查表.md`）
- 合规细节 → 跳 `references/通用/合规/数据合规指引.md`
