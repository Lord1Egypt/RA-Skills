---
name: fmr-user-guide
description: "Free Model Router（FMR）免费模型路由的用户指南：安装、升级、从 Skill 模式迁移、把 agent harness 接入其 OpenAI/Anthropic 兼容端点、渠道注册与 API key 录入、模型与渠道切换停用、故障排查、数据安全说明、能力发现（FMR 能干什么/有哪些功能/组合用法，按所装版本运行时实测）。当用户提到 FMR、free-model-router、免费 token、模型路由，或描述其症状（router 起不来/挂了、切模型失败、要配渠道 key），或询问 FMR 的功能、用途与组合用法时使用。"
---

# fmr-user-guide

本技能让宿主 agent 代用户完成 Free Model Router（FMR）的安装、升级、迁移、接入、排障、日常用法与**能力发现**（按所装版本如实介绍 FMR 能干什么、怎么组合）；唯一必须人工的环节是渠道注册拿 key——agent 输出注册指引后**停下等待**，不代填、不声称已注册。

三条全局纪律：

- **判据一律机器观测**：存活、版本、写入结果以 HTTP 探针与文件指针回读为准；CLI/脚本的"成功"输出与 agent 的自我声称不构成判据。
- **判定靠证据层级，不押注单一端点**：连接层证据先于 HTTP 层证据——拒连/超时 = 无监听，任何 HTTP 应答 = 有进程在。端点缺失时落到明确分支（受限正常态 / 接口面不符态），拿不到的字段标注"此版本不暴露"，不得让状态流向失效。
- **写操作三道门**：先过版本门（下方判定表 P4），再查写入位置合法性（`${CLAUDE_SKILL_DIR}/references/data/data-map.md` 禁区表），写入方式守全局写规则的三级写阶梯。

界面词：用户可见文字一律称 **Free Model Router（FMR）**。FMR 有两种形态：现行 **standalone**（便携包 + 平台服务），旧 **Skill** 形态（OpenClaw 技能）已逐渐弃用，仅迁移章面向其存量用户。

## 主流程

1. **探针定状态**：按下方判定表顺序执行 P1→P2→P3，得出三态之一（未安装 / 装了未启动 / 正常）。P4 是写操作前置门，不占探针顺序，写操作前随时执行。
2. **意图路由**：按意图路由表命中一章，只加载命中的章文件；章内指针再加载所需数据表，其余一律不加载。
3. **执行章流程**：核对该章进入条件（状态前置 + 意图），执行到完成判据为止。

## 状态机判定表

**地址约定**：文中 `127.0.0.1:5678` 均指"配置的 host:port"——默认即此值；`data/router-config.json` 改绑后以配置为准（P2 含重探逻辑，各章 curl 示例按实际配置替换）。

| # | 探针 | 判定 | 分发 |
|---|------|------|------|
| P1 | 数据目录存在性：先查环境变量 `FMR_DATA_DIR`/`FMR_ROOT_DIR`（已设置则查其指向，data-map 路径根覆盖），否则 `~/.free-model-router/`（Windows `%USERPROFILE%\.free-model-router\`） | 不存在 → **连接层反证**（表后第二注）：端口有 HTTP 应答 → **跨用户/异位置实例分支**；无应答 → **未安装态** | 分支有应答 → 按分支处置（**不进 install**）；未安装态 → install 章 |
| | | 存在 ↓ | P2 |
| P2 | **存活判定（连接层证据）**：对 5678 发任意 HTTP 请求（首选 `GET http://127.0.0.1:5678/healthz`，短超时秒级）；拒连/超时且 P1 已过时，读 `data/router-config.json` 的 `server.host/port`（只读白名单），非默认值按配置地址重探一轮 | 重探后仍拒连/超时 → **装了未启动态** | 按下方"平台拉起面"启动（先核对 `data/router.pid`，见该段），勿走 CLI 自启（见 usage 章陷阱） |
| | | 任何 HTTP 应答（200/404/500 均算）→ 端口有进程监听 = 存活 ↓ | P3 |
| P3 | **状态判定（替代证据链，自上而下取第一个可用）**：`GET /api/status` → `/healthz` body（`version`/`uptimeSec`）→ `GET /v1/models` → `GET /api/providers` | `/api/status` 200 → 完整状态（版本/部署模式/主备/`apiKeyConfigured`）；仅次级证据在 → **正常态（受限）**：版本走版本证据链（P4 落地细则），缺失字段标注"此版本不暴露"；四项全不认识 → **接口面不符态**。`/api/status` 响应体含明文 `apiKey` 字段（各态通用）：任何面向用户的输出一律不回显 | **正常态**（含受限）→ 下方意图路由表；**接口面不符态** → 表后注 |
| P4 | **版本门**（所有写操作前置；Router 关着也能执行）：读 CLI 所在 zip 根 `package.json` 版本，与安装目录 `current` 指针指向版本的 `package.json` 比对 | 不一致 → **拦截一切写操作** | upgrade 章（含回退路径）。`/api/status` 可用时以 P3 的 `version` 交叉核对；端点缺失不阻塞本门（主判据是文件比对） |
| | | 一致 | 放行写操作 |

**平台拉起面**（装了未启动态；CLI 不承担 standalone 启动职责）：拉起前先核对 `data/router.pid`——PID 指向的进程仍在（超时/僵死场景）→ 不拉起，转 troubleshoot 章。Linux = systemd 用户级或系统级 `free-model-router.service`；macOS = launchd `com.free-model-router.plist`；Windows = 管理员 schtasks 任务 `FreeModelRouter`／非管理员 VBS 隐藏启动项（停止需 `Stop-Process` 过滤 node+server.js）。查询时用户级与系统级**都查**——跨用户安装时，实例可能只在其安装账户下可见（Windows 任务定义硬编码安装者的 profile 路径）。

P4 落地细则：现行 standalone 便携包不含 CLI，"CLI 所在 zip 根"落地为**安装版本目录根**（zip 根即版本目录内容）。 Router 活着：比对 `GET /api/status` 的 `version` 与 `current/package.json`。 存在 Skill 形态 CLI（迁移期用户）：按表比对 CLI 包根与 `current`。 无 CLI 且 Router 停止：写操作没有执行者，门自然放行。

**版本证据链**（P3 受限与 P4 共用，自上而下取第一个可得；旧布局安装无 `versions/`/`current`，不构成断流点）：① `current/package.json`（versioned 布局）→ ② `data/install-info.json` 的 `nodePath` 所在目录的 `package.json`（该字段指向安装目录内 node.exe：versioned 布局即 `current` 指向处，**旧布局即应用目录根**；字段缺失则跳过）→ ③ 运行中端点返回的 `version`（P3 链顺带所得）→ ④ 全部不可得 = **版本未知**：如实标注、流向不断。旧布局且版本未知时的 P4：REST/面板写放行（执行者即 Router 本体，无跨版本写入者），③级配置文件手改前额外标注"版本未核实"。

**接口面不符态处置**：5678 有应答但替代证据链全部不认识 = 所装版本的接口面与技能知识面差异极大（版本极旧、极新，或 5678 被其他程序占用）。处置：① 写操作**全部拦截**——P4 文件比对可做，但接口面不认识时写风险不可评估；② 报告版本号（走版本证据链，最坏为"版本未知"，如实标注）；③ 能力发现按降级给（定位叙述 + 提示升级）；④ 转 upgrade 章核对版本漂移；若版本号新于技能已知面，标注"技能知识面可能落后"并提议勘误回写（须用户确认）。接口面实况（哪些端点在）可按全局写规则"接口面自发现"核实，作面板指引与勘误提议之据，不据此解除①的拦截。

**跨用户/异位置实例分支**：本用户数据目录不存在（环境变量路径亦无）但端口有 HTTP 应答 = 存在数据目录在别处的运行实例（其他 OS 用户、`FMR_*` 重定向、旧布局异位安装）。处置：① 报告事实——应答方版本走版本证据链，数据目录文件证据不可读即如实标注；② 只给两个选项：**用现有实例**（access 章接入；本机回环 REST/面板可用；REST/面板写放行——执行者即 Router 本体，③级配置手改因文件不可达自然排除，输出标注"版本门降级：数据目录不在当前用户可达范围"）或 **停旧重装**（需安装者账户/管理员权限，权限不足如实告知并交有权限的会话处理）；**不提供"再装一份"**——同机多实例徒增运维复杂度；③ 能力发现走降级显示。盲区声明：实例改绑了端口且数据目录不可读时本分支无法探测，如实承认，不虚构。

## 意图路由表

| 意图话术族（示例词） | 章 |
|---|---|
| 装/部署/下载 FMR；未装状态下的任何使用请求 | install |
| 升级/版本/回退/卸载/更新失败 | upgrade |
| 把 <某 harness> 接进来/端点/baseURL/跨机使用 | access |
| 从旧版（Skill/OpenClaw）迁移过来 | migrate |
| 切换模型/看渠道/停用启用 provider/配 key/通知与掉线询问 | usage |
| 能干什么/有哪些功能/组合用法/值不值得装·升级/功能速览 | capabilities |
| router 挂了/起不来/转圈/4xx/切了没生效 | troubleshoot |
| 数据安全/隐私/上传了什么 | security |

## 全局写规则

- **三级写阶梯**：① REST 直调（本机回环免密；Skill 形态安装中的同义 CLI 命令等同此级）＞ ② 管理面板（用户自助，同一 REST 的前端）＞ ③ 配置文件手改（仅白名单项，改前备份）。`versions/`、`staging/`、`current`、`update-state`、事件文件 = 手改禁区；全表见 `${CLAUDE_SKILL_DIR}/references/data/data-map.md`。
- **版本硬约束**：数据文件格式随 FMR 版本漂移，任何写操作执行前先过 P4，无一例外。
- **接口面自发现**：技能记载的 REST 端点为知识面时点清单；写端点 404 或回包结构不认识 = 接口面可能漂移——**停手，不猜替代端点**，按序自发现实况：① `GET /api/endpoints`（管理面自述端点）应答即以它为权威清单；② 缺失则降级提取 `/admin` 面板 JS bundle 内的 `/api/*` 清单（面板与后端同版本一体分发，该清单即所装版本实况，bundle 内亦含各端点调用形状可比对）；③ 端点在实况清单 → 比对形状后执行，仍按完成判据回读；不在 → 该操作转面板指引（面板与后端同版本，指引永不漂移）或如实报告不可执行；两种去向均提议勘误回写（须用户确认，维护层落账）。
- **provider apiKey 双通道**：agent 经 REST 代配（先向用户声明配置文件明文 key 风险，见 security 章），或用户自行在 `/admin` 面板配置。
- **人工项交接铁律**：渠道注册类操作，agent 输出注册指引后**停下等待**用户完成注册拿 key，不代填、不声称已注册。
- **渠道动态原则**：渠道随时增减，一律以运行时 `GET /api/providers` 下发列表为准（含每渠道 `website` 注册链接），不硬编码渠道名、数量、额度。模板见 `${CLAUDE_SKILL_DIR}/references/data/provider-registration.md`。
- **能力动态原则**：特性、虚拟端点、组合、版本时效一律以运行时 `GET /api/features` 为准（接口自带名称与描述），禁硬编码任何"版本 → 功能清单"映射；接口缺失（404）即版本低，走降级显示并建议升级，不拼凑功能清单（详见 capabilities 章）。

## 参考（何时读）

### 章文件（一次只加载命中的章）

| 章 | 何时读 |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/chapters/install.md` | P1 未安装态；意图"装/部署/下载"；未装状态下的任何使用请求 |
| `${CLAUDE_SKILL_DIR}/references/chapters/upgrade.md` | 意图升级/版本/回退/卸载/更新没生效；P4 拦截写操作时 |
| `${CLAUDE_SKILL_DIR}/references/chapters/access.md` | 正常态；意图把某 harness 接进来/端点/baseURL/跨机使用 |
| `${CLAUDE_SKILL_DIR}/references/chapters/migrate.md` | 自述旧 Skill 模式/OpenClaw 存量，意图迁移 |
| `${CLAUDE_SKILL_DIR}/references/chapters/usage.md` | 正常态：切模型/看渠道/停用启用/配 key/通知与掉线询问 |
| `${CLAUDE_SKILL_DIR}/references/chapters/capabilities.md` | 意图"能干什么/有哪些功能/组合用法/值不值得用"；任意状态（章内自带降级分支） |
| `${CLAUDE_SKILL_DIR}/references/chapters/troubleshoot.md` | 症状话术（挂了/起不来/转圈/4xx/切了没生效）；install、upgrade 失败时跳入 |
| `${CLAUDE_SKILL_DIR}/references/chapters/security.md` | 数据安全/隐私询问；跨机改绑定前的强制告警（access 章跳入） |

### 数据表（按章内指针加载）

| 表 | 何时读 |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/data/cli-commands.md` | 执行写操作前核对命令/REST 等价与自动拉起副作用 |
| `${CLAUDE_SKILL_DIR}/references/data/failure-modes.md` | troubleshoot 章匹配症状时 |
| `${CLAUDE_SKILL_DIR}/references/data/data-map.md` | 任何写操作前定位文件与写权限 |
| `${CLAUDE_SKILL_DIR}/references/data/provider-registration.md` | 渠道注册与 key 录入（usage 章指针） |
| `${CLAUDE_SKILL_DIR}/references/data/events.md` | event-check 触发点的输出解读（usage、troubleshoot） |
| `${CLAUDE_SKILL_DIR}/references/data/capability-dictionary.md` | capabilities 章为 `/api/features` 返回的 id 补深解/归组/组合说明时 |
