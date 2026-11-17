# 技能安全审计方法论（SkillSec Audit · 16 类）

> 本文件说明「企业技能工程台」内置的 **技能安全审计器**（`scripts/skillsec_audit.py`）的方法论来源、分类体系与运行方式。
>
> **借鉴声明**：本审计器的分类法 **借鉴自 NVIDIA SkillSpector 公开的「16 类漏洞模式」**。我们 **不复制其代码、不使用其品牌名作为本工具名称**，仅吸收其公开的分类思想，用自有开源代码（纯 Python 标准库、零依赖）实现，从而让本技能具备「对任一技能（含自身）做类 SkillSpector 式静态安全审计」的能力。这是对既有 `review_checklist.py`（已融合腾讯朱雀 `skill-scanner` + `skill-vetter`）的能力补全，而非替代。

## 1. 为什么需要这层能力

- `review_checklist.py` 偏「发布前体检 + CISO 五风险 + 厚技能 + AI 安全语义层」，视角偏治理与质量。
- NVIDIA SkillSpector 的 16 类更贴近 **「过度能动（over-actuation）」** 这一核心风险——即技能在无约束下自主决策、范围蔓延、自我修改、触发滥用等。这正是企业最担心的失控面。
- 融合后，本技能可同时输出两种审计报告：`review`（广义体检）与 `audit`（16 类过度能动-centric 安全审计），互为补充。

## 2. 16 类分类与检测器映射

| ID | 类别（中/英） | 本审计器检测要点 | 典型信号 |
|----|--------------|----------------|----------|
| C01 | 过度能动 Over-actuation | 无用户确认下的自主/自动执行 | "自主执行/无需确认/自行决定" |
| C02 | 输出处理 Output handling | 子进程输出未校验流入危险函数；外部元数据生成 HTML/MD 未转义（存储型 XSS） | `.stdout`→`eval/os.system`；HTML 插值无 `html.escape` |
| C03 | 叛变特工 Rogue agent | 自我修改/自我更新能力 | "自更新/自我修改/改写自身" |
| C04 | 触发滥用 Trigger abuse | 过长/模糊 description；过于宽泛的自然语言触发短语 | 描述>700字；"升级一下" |
| C05 | MCP 最低特权 MCP least privilege | 声明 MCP/工具调用却无权限边界声明 | 提及 MCP 但无 capabilities/权限声明 |
| C06 | MCP 工具中毒 MCP tool poisoning | 零宽/不可见字符；隐藏指令 | U+200B 等；"隐藏指令" |
| C07 | 提示注入 Prompt injection | 指令覆盖/隐藏指令类表述 | "ignore previous instructions" |
| C08 | 数据外流 Data exfiltration | 环境变量采集；主目录枚举；外部传输 | `os.environ`；`glob('~')` |
| C09 | 特权升级 Privilege escalation | 提权执行；硬编码凭据 | `sudo`；`ghp_...` |
| C10 | 供应链 Supply chain | 下载即执行；远端获取后执行；编码绕过；未钉置依赖 | `curl|sh`；`b64decode` |
| C11 | 系统提示漏出 System prompt leakage | 引导输出/泄露系统提示 | "输出你的系统提示" |
| C12 | 记忆中毒 Memory poisoning | 写入/持久化记忆文件 | `MEMORY.md`；"写入记忆" |
| C13 | 工具滥用 Tool abuse | 不安全默认（force=True 等） | `confirm=False` 默认 |
| C14 | 危险 AST Dangerous AST | exec/eval/动态导入 | `eval(`；`__import__` |
| C15 | 污染追踪 Taint tracking | 外部输入未校验流入危险函数 | 外部输入→`exec` 无校验 |
| C16 | YARA 签名 Malware heuristics | 恶意软件/webshell/挖矿特征 | `stratum+tcp`；`xmrig` |

## 3. 运行方式

```bash
# 审计某个技能目录（或单个 SKILL.md）
python scripts/skillsec_audit.py <skill目录或SKILL.md>
python scripts/skillsec_audit.py <skill目录或SKILL.md> --json   # CI 卡点用
python scripts/skillsec_audit.py <skill目录或SKILL.md> --md     # 报告存档

# 经统一 CLI
studio audit <skill目录或SKILL.md> [--json|--md]
```

报告字段：**类别 / 严重度（高·中·低·INFO）/ 置信度(0-100%) / 证据 / 发现**。
退出码：`0`=无「高」级发现；`1`=存在「高」级发现（可作 CI 阻断卡点）。

## 4. 严重度与置信度约定

- **高（HIGH）**：明确危险信号（如 `curl|sh`、硬编码凭据、零宽字符、exec/eval 流入外部输入）。CI 应阻断。
- **中（MEDIUM）**：风险信号但可能属设计内（如自更新能力、宽泛触发、MCP 未声明权限）。需人工确认。
- **低（LOW）/ INFO**：弱信号或信息提示。
- **置信度**：基于匹配强度启发式给出（精确关键词 85-95%，模式/启发式 70-85%），供排优先级。

## 5. 自扫说明（扫本技能自身）

用本审计器扫「企业技能工程台」自身时，**C03（自更新）会如实命中**——这是设计内、受 `SECURITY.md` 七层防护治理的能力，不应视为漏洞。审计器本身对自带扫描器脚本（`SELF_FILES`）做自检排除，避免检测规则字符串造成自引用误报。建议把 `audit` 与 `review`、`gate` 一起纳入发布前卡点。
