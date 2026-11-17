---
name: ai-security-redteam
version: 1.0.0
author: 诺卫(Phylax)@SynomosAI
description: AI 安全与红队测试实操手册——覆盖六大攻击面（提示注入、越权与工具滥用、数据与隐私泄露、幻觉与质量缺陷、供应链与模型投毒、拒绝服务）、OWASP LLM Top 10 映射、完整红队流程与零依赖本地工具。当你要做 AI 系统红队测试、攻击面建模、测试用例生成、漏洞分级或修复复测时使用。触发词：AI安全、红队测试、提示注入、LLM安全、OWASP、渗透测试、安全测试、AI红队。
license: MIT
tags: [SynomosAI, Phylax, 红队测试, AI安全]
品牌归属: SynomosAI
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: tools/ai_redteam_toolkit.py
  runtime: python3
  call_pattern: args
capabilities:
  - red_team_checklist
  - security_radar
  - stdlib_cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
input_schema:
  type: object
  properties:
    args:
      type: array
      items:
        type: string
      description: CLI arguments forwarded to the entry point script.
output_schema:
  type: object
  properties:
    exit_code:
      type: integer
      description: Process exit code; 0 means success.
    stdout:
      type: string
      description: Captured standard output.
    result:
      type: string
      description: Human-readable result summary.
changelog: "2026-10-16: USK v3 interface block injected; desensitized for public listing."

---

> 凡自治之物 · LGD 治理学 · 创造术家族

## 何时用
- 做 AI 系统红队测试、攻击面建模、测试用例生成、漏洞分级或修复复测（详见正文"定位·何时用"与"三、触发场景"表）
- 触发词：AI安全、红队测试、提示注入、越权逃逸、OWASP LLM Top 10、安全测试
- 边界：未获书面授权的真实系统攻击不用本技能（见正文"七、铁律"）

## 用法
- 零依赖本地工具：`python tools/ai_redteam_toolkit.py`
  - `risk --system "..."`：攻击面清单
  - `cases --surface injection|overreach|privacy|hallucination|supplychain|dos`：测试用例
  - `grade --desc "..."`：漏洞分级；`fix --vuln ...`：修复建议
  - 全部命令支持 `--help`

## 流程
1. 目标定义 + 书面授权 / 合规边界（正文 SOP 步 3）
2. 摸攻击面：`risk --system`（步 1，对照 references/01）
3. 跑测试：`cases --surface` 按 references/02 五步流程执行（步 2）
4. 分级 `grade --desc`（步 4）→ 出报告 + `fix`（步 5）→ 修复后按报告复测（步 6）


# AI 安全与红队测试

AI 安全验证工作台：**看得见攻击面、造得出测试用例、跑得了红队流程、出得来分级报告、修得了关键漏洞**。面向 AI 工程、安全测试与信息安全负责人——治理管「制度与风险」，红队管「技术验证」，两者闭环才是完整防线。

## 定位

**何时用（声明式）**
- 安全评估：「我们的 AI 应用有什么攻击面？优先测什么？」
- 红队流程：「AI 红队测试怎么做？从哪开始？」
- 注入测试：「提示注入怎么测？直接 / 间接注入用例怎么写？」
- Agent 安全：「Agent 越权 / 逃逸怎么测？沙箱怎么验证？」
- 数据隐私：「训练数据会泄露吗？记忆攻击怎么测？」
- 报告修复：「漏洞怎么分级？怎么修？怎么复测？」

**何时不用（声明式）**
- 未获书面授权的真实系统攻击——本技能只生成用例与流程，绝不发起真实攻击。
- 传统 IT 渗透测试（非 AI 特有）——本技能聚焦 AI 攻击面，传统 IT 见专业渗透团队。
- 需要真正执行漏洞利用或对外发起 DoS——本技能是方法库与工具，不联网、不攻击。
- 缺安全资质却要做高危项——先做轻量自测，高危项委托专业红队。

## 一、能力边界

**本技能做（In scope）**
- 六大攻击面建模：提示注入、越权与工具滥用、数据与隐私泄露、幻觉与质量缺陷、供应链与模型投毒、拒绝服务。
- OWASP LLM Top 10 风险映射与红队流程（目标定义 / 攻击面建模 / 用例设计 / 执行 / 报告 / 修复复测）。
- 测试用例库生成（直接 / 间接注入、Agent 越权与沙箱逃逸、训练数据泄露与记忆攻击、幻觉检测基准）。
- 漏洞分级与修复建议、报告模板、零依赖本地工具。
- 「轻量自测」方法论（用例库 + 人工评审）供无安全团队时参考。

**本技能不做（Out scope，集中声明）**
1. 不对未获书面授权的系统发起任何真实攻击或漏洞利用。
2. 不生成可用于违法攻击的「开箱即用」利用代码——只给测试思路与防御视角用例。
3. 不替代具备资质的安全团队 / 机构的正式红队与合规审计。
4. 不联网、不采集数据、不发起 DoS / 社工 / 物理入侵。
5. 不对测试发现做终局法律责任裁定。

## 二、输入约束与输出承诺

**推荐问法（引导给足上下文）**
- 「我们的客服 AI 有哪些攻击面？优先测什么？」
- 「提示注入测试用例给我来一组。」
- 「红队测试报告怎么出？漏洞怎么分级？」
- 工具模式：给系统描述 / 攻击面 / 危害描述 / 漏洞类型，取结构化清单。

**输入字段引导**
- `risk --system "..."`：系统描述（接知识库 / 可调工具等）。
- `cases --surface`：`injection` / `overreach` / `privacy` / `hallucination` / `supplychain` / `dos`。
- `grade --desc "..."`：危害描述；`fix --vuln`：漏洞类型。
- 所有命令支持 `--help` 查看全集。

**输出承诺**
- 方法论 + 用例 + 分级报告模板，不夸大确定性；建议均附防御视角。
- 工具零依赖、本地运行、不联网、不发起任何真实攻击。
- OWASP LLM Top 10 等清单引用前复核最新版（**待核验**）。

## 三、触发场景

| 用户意图 | 触发词 | 应加载章节 |
|----------|--------|------------|
| 攻击面评估 | AI安全、攻击面、红队测试、安全评估 | 五、六、九 |
| 注入测试 | 提示注入、直接注入、间接注入、Prompt Injection | 五、六、九 |
| Agent 安全 | 越权、逃逸、沙箱、工具滥用 | 五、六、九 |
| 数据隐私 | 数据泄露、记忆攻击、PII、训练数据 | 五、六、九 |
| 报告与修复 | 漏洞分级、修复、复测、报告模板 | 五、九、十 |
| 合规/授权边界 | 书面授权、合法性、轻量自测 | 一、七、四 |

**示例对话 1**
> 用户：「我们的客服 AI 有哪些攻击面？优先测什么？」
> 加载：第五章 SOP 步 1 `risk --system "客服AI，接知识库，可调用CRM和发邮件"` → 对照 references/01 六大攻击面，优先提示注入与越权。

**示例对话 2**
> 用户：「提示注入测试用例给我来一组。」
> 加载：第五章 SOP 步 2 `cases --surface injection` → 对照 references/03 用例库。

## 四、常见错误与反模式

**反模式 1 ✗** 对未获书面授权的系统直接「开测」甚至发起真实攻击。
**替代方案 ✓** 真实系统测试须取得书面授权；本技能只生成用例与流程，不发起攻击（第七章铁律 1）。

**反模式 2 ✗** 把测试用例当「攻击利用代码」外发或用于违法目的。
**替代方案 ✓** 用例以防御视角呈现，用于验证与加固；不提供开箱即用利用代码。

**反模式 3 ✗** 缺安全资质却硬上高危项（越权 / 逃逸 / 数据泄露）。
**替代方案 ✓** 先做「轻量自测」（用例库 + 人工评审），高危项委托专业红队。

**反模式 4 ✗** 引用过期 OWASP LLM Top 10 版本做结论。
**替代方案 ✓** 引用前复核最新版，标注**待核验**。

**高频 Q&A**
- **Q：红队测试合法吗？** A：只对已获书面授权的自有 / 托管系统执行；未授权测试可能违法（references/02 合规边界）。
- **Q：没有安全团队能做吗？** A：可先做轻量自测（用例库 + 人工评审），高危项再委托专业红队。
- **Q：和渗透测试有什么区别？** A：渗透测传统 IT 系统，AI 红队额外覆盖提示注入 / 幻觉 / Agent 越权等 AI 特有攻击面。
- **Q：工具会真的攻击吗？** A：不会——只生成用例与流程，不发起攻击、不联网。

## 五、标准 SOP

| 步 | 动作 | 产物 | 易踩坑 |
|----|------|------|--------|
| 1 | 摸攻击面：`python tools/ai_redteam_toolkit.py risk --system "..."` | 攻击面清单 | 漏列 Agent 工具滥用 |
| 2 | 跑测试：`cases --surface injection` 取用例，按 references/02 流程执行 | 测试用例集 | 用例未覆盖间接注入 |
| 3 | 定范围：目标定义 + 授权边界 + 合规边界 | 测试范围书 | 缺书面授权即开测 |
| 4 | 分级：`grade --desc "..."` | 漏洞分级 | 危害描述过简致分级错 |
| 5 | 出报告：`report` 模板 + 修复建议 `fix --vuln ...` | 分级报告 | 报告漏复测计划 |
| 6 | 复测：修复后按报告复测流程验证 | 复测结论 | 未验证即宣称修复 |

## 六、关键事实速查

- 六大攻击面：提示注入 / 越权与工具滥用 / 数据与隐私泄露 / 幻觉与质量缺陷 / 供应链与模型投毒 / 拒绝服务。
- OWASP LLM Top 10：映射见 references/01（版本**待核验**，引用前复核最新版）。
- `cases --surface` 枚举：`injection` / `overreach` / `privacy` / `hallucination` / `supplychain` / `dos`。
- 红队流程五步：目标定义 → 攻击面建模 → 用例设计 → 执行 → 报告 / 修复复测（references/02）。
- 工具零依赖、本地运行、不联网、不发起任何真实攻击。

## 七、铁律

1. **PROHIBITED** 绝不对未获书面授权的系统发起任何真实攻击、漏洞利用或数据外发。
2. **PROHIBITED** 绝不生成可用于违法攻击的「开箱即用」利用代码——只给防御视角测试用例。
3. **PROHIBITED** 绝不越权访问、社工钓鱼、物理入侵或发起 DoS / 资源耗尽攻击。
4. **PROHIBITED** 绝不伪造漏洞、篡改测试结果或出具虚假安全报告。
5. **PROHIBITED** 绝不替代具备资质的安全团队 / 机构的正式红队与合规审计。
6. **PROHIBITED** 绝不联网采集数据或借本技能规避授权与法律边界。

## 八、输入输出依赖

- **依赖工具**：`tools/ai_redteam_toolkit.py`（Python 标准库，零外部依赖，本地运行）。
- **依赖知识库（references/）**：
  - `01-AI安全风险全景.md`（六大攻击面、OWASP LLM Top 10 映射）
  - `02-红队测试流程.md`（五步流程、范围界定、合规边界）
  - `03-提示注入测试.md`（直接 / 间接注入、用例库、防御绕过）
  - `04-越权与逃逸测试.md`（Agent 越权、工具滥用、沙箱逃逸）
  - `05-数据与隐私测试.md`（训练数据泄露、记忆攻击、PII 提取）
  - `06-幻觉与质量测试.md`（幻觉检测、基准、RAG 场景）
  - `07-供应链与拒绝服务.md`（模型投毒、组件供应链、DoS）
  - `08-报告与修复.md`（漏洞分级、修复建议、复测流程）
  - `09-FAQ.md`（高频疑问）
- **环境**：Python 3（标准库即可），无网络依赖。
- **凭据规则**：本技能不涉及任何账号 / 密钥 / Token。任何凭据一律从保险库 `~/本机系统保险库` 读取，绝不进入对话、代码或日志；真实系统测试凭据仅限书面授权范围内使用。

## 九、示例

**示例 1（攻击面评估）**
- 问题：客服 AI 有哪些攻击面？优先测什么？
- 加载：SOP 步 1 `risk --system "客服AI，接知识库，可调用CRM和发邮件"` → 对照 references/01。
- 答案框架：攻击面 = 提示注入、越权调用 CRM/发邮件、知识库数据泄露；优先测注入与越权（Agent 工具滥用）。

**示例 2（注入用例）**
- 问题：提示注入测试用例来一组。
- 加载：SOP 步 2 `cases --surface injection` → 对照 references/03。
- 答案框架：直接注入（指令覆盖）+ 间接注入（外部内容夹带指令）用例组，均附防御验证要点。

**示例 3（漏洞分级与修复）**
- 问题：漏洞怎么分级、怎么修？
- 加载：SOP 步 4 `grade --desc "攻击者可注入指令让AI泄露全部客户数据"` + 步 5 `fix --vuln injection`。
- 答案框架：分级 = 高危（数据泄露）；修复 = 输入隔离 + 权限最小化 + 输出过滤，附复测计划。

## 十、错误处理

| 现象 | 原因 | 修正引导 |
|------|------|----------|
| `错误：--system 不能为空`（退出码 2） | risk 缺系统描述 | 补 `--system "..."`，描述能力/接口/数据 |
| `错误：--surface 仅支持 injection/overreach/...` | 攻击面枚举错 | 用六个合法 surface 之一 |
| `错误：--vuln 仅支持 ...` | 漏洞类型错 | 用合法 vuln 类型 |
| 要求对未授权系统真打 | 违反铁律 1 | 停止，先取书面授权；本技能只生成用例不攻击 |
| 要求生成利用代码 | 违反铁律 2 | 改提供防御视角测试用例，不提供利用代码 |
| 引用 OWASP 版本过期 | 未核最新 | 标**待核验**，以 OWASP 官方最新版为准 |
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺卫(Phylax)@SynomosAI。指纹 FP-MX-23DBCB951508。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。


## 证据与安全声明
- 证据：见包内 verify/security_results.json（本地闭环验证快照，2026-10-16 读取）
- 版本：1.0.0
- 安全：见包内 verify/security_results.json：零网络 / 零攻击 / 零数据采集，六大攻击面、OWASP LLM Top 10、五步红队流程、书面授权要求与合规边界红线等检查均 pass（2026-10-16 读取）
