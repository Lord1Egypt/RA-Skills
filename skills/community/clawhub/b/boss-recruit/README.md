# boss-recruit

> 一个 [Claude Code](https://claude.com/claude-code) Skill：把 **BOSS 直聘招聘端的"新招呼收件箱"**自动化——读候选人简历 → 同步到**飞书多维表格** → 有附件简历则零弹窗下载并同步、没附件则受控地主动发消息要简历。内置**反风控节奏层**模拟真人操作。

⚠️ **使用前请先阅读 [免责声明](#免责声明) 与 [DISCLAIMER.md](./DISCLAIMER.md)。本工具仅供个人提效与技术研究，使用风险自负。**

---

## 它解决什么

HR 处理 BOSS"新招呼"收件箱很耗时：逐个点开候选人、看简历、判断、要附件简历、再录入系统。本 skill 把这条流水线自动化，并把数据沉淀到飞书多维表格人才库：

```
boss recommend(拉新招呼) → 去重 → 逐个[一人一事务]:
   读在线简历 → 同步飞书人才表
   试下附件简历:
     有  → 零弹窗下载 PDF → 同步到「简历附件」字段 → 通过初筛
     无  → 主动发消息要简历(默认 DRY-RUN, 需显式 --live 才真发)
   → 反风控节奏层(随机延时 / 风控熔断 / 单轮上限 / 权益耗尽诊断)
```

**设计理念**：用确定性命令（零 LLM 运行成本、快、稳）干活，把"像真人"的反风控逻辑沉在代码里，不靠大模型即兴点页面。

## 依赖

| 依赖 | 用途 | 获取 |
|------|------|------|
| [Claude Code](https://claude.com/claude-code) | 运行 skill 的宿主 | 官方 |
| [OpenCLI](https://github.com/jackwener/opencli) + Browser Bridge 扩展 | 复用已登录 Chrome 操作 Boss | `npm i -g @jackwener/opencli` |
| Node.js ≥ 20 | 跑编排脚本 | — |
| 飞书多维表格 | 人才库目标表 | 自建/用模板 |
| lark-cli（可选） | 飞书 OAuth 后端 | 仅 lark-cli 模式需要 |

> 飞书同步支持两种后端：**授权码（base-api，可分发，推荐）** 或 **lark-cli（本机 OAuth）**。授权码模式无需任何 SDK 依赖。

## 安装

```bash
# 1) 装 skill
git clone https://github.com/<your-name>/boss-recruit ~/.claude/skills/boss-recruit

# 2) 装配套的 OpenCLI 适配器（零弹窗下载附件简历）
mkdir -p ~/.opencli/clis/boss
cp ~/.claude/skills/boss-recruit/adapters/boss/attachment.js ~/.opencli/clis/boss/

# 3) 确认 OpenCLI 就绪（需先装好 Browser Bridge 扩展并登录 Boss 招聘端）
opencli doctor
```

## 配置飞书目标表（首次必做）

"同步到哪张表"不硬编码，由 `setup.mjs` 解析飞书链接并持久化。

```bash
# A) 授权码模式（推荐，可分发）—— 只认 /base/ 链接（个人端）
#    授权码在多维表格「更多 → 高级权限 → 获取授权码」生成
node ~/.claude/skills/boss-recruit/scenarios/setup.mjs \
  "https://xxx.feishu.cn/base/<app_token>?table=<table_id>" --token "pt-..."

# B) lark-cli 模式（本机自用，需已登录 lark-cli）
node ~/.claude/skills/boss-recruit/scenarios/setup.mjs "<飞书表链接>"

# 查看当前配置
node ~/.claude/skills/boss-recruit/scenarios/setup.mjs --show
```

> 目标表至少应有这些字段：`姓名`、`简历来源`、`当前阶段`，以及一个附件字段（同步 PDF 简历用）。缺的字段会自动跳过不写。

## 使用

```bash
# 安全模式：只读 + 同步全自动，打招呼只演示不真发（随时可跑）
node ~/.claude/skills/boss-recruit/scenarios/inbox.mjs --limit 10

# 真发要简历消息（对外动作！首次务必小批量盯着跑）
node ~/.claude/skills/boss-recruit/scenarios/inbox.mjs --live --limit 3

# 重扫已处理候选人
node ~/.claude/skills/boss-recruit/scenarios/inbox.mjs --force
```

在 Claude Code 里也可直接说"处理一下 Boss 新招呼"触发本 skill。

### 安全模型

- **只读 + 同步**（读简历、建/更飞书记录、下附件）→ 无对外副作用，默认全自动。
- **要简历打招呼**（对外发消息、不可撤回）→ **默认 DRY-RUN 只打印话术**，确认后加 `--live` 才真发。
- 触发**验证码 / 登录失效 / 频控 / 权益耗尽** → **自动熔断暂停**，保留进度。

## 兼容性：不只 Claude Code

本仓库是一个**工具**，不绑定任何特定 AI 助手：

- `SKILL.md` 只是 [Claude Code](https://claude.com/claude-code) 的自动触发外壳（Anthropic Agent Skills 格式）。
- 真正的功能是 `scenarios/*.mjs` + `lib/*.mjs` 这些**纯 Node 脚本**，配合 `opencli` / `lark-cli` / base-api。
- **任何能执行 shell 的代理**（Codex、Cursor、Cline、Aider、OpenClaw…）或你本人，都能直接 `node scenarios/inbox.mjs` 驱动它——见 [AGENTS.md](./AGENTS.md)。

目前跨厂商没有统一的 skill 标准；其它助手只要读 `AGENTS.md` 或被告知运行对应脚本即可，移植成本几乎为零。`lib/` 下的反风控节奏层、base-api 后端、状态机均为无依赖 ESM，可被其它项目 import 复用。

## 反风控要点（详见 [references/anti-detection.md](./references/anti-detection.md)）

1. 单轮 ≤ 5 人；相邻动作**随机 25~70s**（非固定）
2. 每 3 人做一次风控/状态校验
3. **连续 3 次打招呼失败 → 优先判定当日沟通权益耗尽**（而非代码问题）
4. 发消息前**身份校验**防发错人；一人一事务
5. 原生 CDP 点击 + 逐字输入，不用 DOM `.click()` / 瞬时填充
6. 验证码/登录失效/频控 → 立即熔断停整轮

## 项目结构

```
SKILL.md                  Claude Code skill 入口与说明
config.mjs                字段映射 / 话术模板 / 节奏参数
lib/
  rhythm.mjs              反风控节奏层
  task-memory.mjs         状态机 + 记忆（去重/断点续跑）
  target.mjs              飞书目标表解析/持久化
  feishu.mjs              飞书同步 dispatch
  feishu-base.mjs         授权码 base-api 后端（纯 HTTP）
scenarios/
  setup.mjs               首次配置飞书目标表
  inbox.mjs               场景1：新招呼收件箱编排
adapters/boss/
  attachment.js           OpenCLI 适配器：零弹窗下载附件简历
references/
  anti-detection.md       反风控/拟人操作规范
```

## 路线图

- [x] 场景1：新招呼收件箱（读简历 / 同步 / 附件 / 要简历）
- [ ] 场景2：推荐列表主动打招呼
- [ ] 场景3：按人才画像搜索牛人并触达
- [ ] 附件闭环跟进（候选人发来简历后自动接收+同步）

---

## 免责声明

**本工具仅供个人学习、技术研究与提升个人工作效率之用。下载、安装或使用即表示你已阅读、理解并同意以下条款：**

1. **使用风险自负**：本工具按"现状"提供，不附带任何明示或默示担保。作者不对因使用本工具导致的任何后果负责，包括但不限于**账号被封禁、限制、数据丢失、法律纠纷或经济损失**。

2. **遵守平台条款**：自动化访问、抓取、批量操作可能违反 BOSS 直聘等平台的用户协议。**是否使用、如何使用由你自行判断并承担全部责任。** 强烈建议在使用前阅读相关平台的服务条款。

3. **账号安全**：本工具操作你**自己登录的真实账号**。平台风控可能导致账号被限制或封禁。请务必小批量、低频率、谨慎使用，并自行承担账号风险。

4. **数据合规**：候选人简历、联系方式属于**个人敏感信息**。你作为数据处理者，须遵守《个人信息保护法》等相关法律法规，**不得用于非法收集、转售或任何未授权用途**。本工具不鼓励、不支持任何形式的数据爬取转售。

5. **非商业转售**：本工具定位为**个人提效工具**，不得用于规模化抓取、数据贩卖或搭建侵犯他人权益的商业服务。

6. **无关联声明**：本项目与 BOSS 直聘、飞书（Lark）及任何第三方平台**无任何隶属、合作或授权关系**，相关商标归各自所有者。

7. **凭证安全**：飞书授权码、登录凭证等敏感信息仅存于你本地（`~/.opencli/boss-recruit/`），**切勿提交至代码仓库或分享给他人**。

> 若你不同意以上任一条款，请勿使用本工具。

完整声明见 [DISCLAIMER.md](./DISCLAIMER.md)。

## License

[MIT](./LICENSE)
