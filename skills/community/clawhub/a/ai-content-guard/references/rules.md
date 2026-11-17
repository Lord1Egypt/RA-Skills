# PITAX 规则卡（v1.6.1，9 条已实现）

依据 Arcanum Prompt Injection Taxonomy v1.6.1（Jason Haddix, CC BY 4.0）。
**红线：解读与报告中只允许使用下列编号；不得编造编号、CWE、CVE。**
MITRE ATLAS 统一映射 `AML.T0051.001`（Indirect Prompt Injection，经官方 atlas-data 核实，勿改）。

严重度与置信度为引擎确定性输出：单层编码置信度 70，其余 90。
命中计数口径 = "签名数"（同一行多个模式各计一条）。

---
## PIT-E-23 · Invisible Text ｜ severity: high
零宽字符（U+200B/200C/200D/FEFF 等）、软连字符、U+E0000–E007F Tag 字符（ASCII Smuggling）走私人类不可见、LLM 可解析的指令。
- **检测特征**：逐字符扫描；每种字符每文件各出一条命中，证据含字符名与行号列表。
- **误报边界**：UTF-16 文件 BOM；emoji 家族序列中的 ZWJ；排版文档软连字符。安全测试夹具含样本属预期。
- **修复**：删除不可见字符；CI 加 Unicode 字符白名单；追溯 git blame 提交者。

## PIT-E-54 · Trojan Source（CVE-2021-42574）｜ severity: high
Bidi 控制符（U+202A–E、U+2066–9）改变源码视觉顺序，"看起来"的逻辑 ≠ 实际 parsed 逻辑。
- **检测特征**：整文件聚合为一条；证据列出具体 Bidi 字符。
- **误报边界**：正当 RTL 文案（希伯来/阿拉伯语）使用隔离符——确认内容语境后豁免。
- **修复**：源码/文档中禁用裸 Bidi 控制符；RTL 文案改用 Unicode 隔离标记方案或纯文本标注方向。

## PIT-T-46 · Agent Instruction-File Injection（CVE-2025-53773, CWE-77）｜ severity: critical
AI 指令文件（`.cursor/rules`、`CLAUDE.md`、`copilot-instructions.md`、`AGENTS.md`、`.claude/` 等）植入指令覆盖/角色劫持/安全旁路后门，劫持全仓 AI 助手（同 Copilot YOLO→RCE 攻击链）。
- **检测特征**：仅对 AI 配置文件路径跑 10 个模式（ignore/override/disregard instructions、system prompt、you are now、DAN/dev mode、jailbreak、disable/bypass safety），每模式各计一条。
- **误报边界**：安全防御类规则文件本身的合理表述（需逐条人审确认）。
- **修复**：删除后门行并全文件 diff 审查；该仓库视为已投毒，审查近史所有指令文件变更；通知使用方。

## PIT-T-51 · Instruction Override（注释注入）｜ severity: high
代码注释内嵌提示注入（"ignore previous instructions" / "reveal the system prompt" / 角色劫持 / dev/DAN mode）。
- **检测特征**：先粗提取注释片段（#、//、/*、<!-- 等），再跑 7 个高置信模式。
- **误报边界**：安全测试/红队夹具与检测器自身用例；安全教材示例。报告时标注"fixture，预期命中"。
- **修复**：删除；对 AI 编码助手产出的注释保持抽检纪律。

## PIT-N-06 · Document / File Upload（文档投毒）｜ severity: high
README/设计文档等（.md/.rst/.txt，不含 AI 配置文件）面向 Agent 的恶意指令——文档是 Agent 常规输入，传统工具不检出。
- **检测特征**：同指令注入模式集，文档语境。
- **误报边界**：安全产品文档、讲解提示注入的文章（可能原文引用攻击句式）——逐条人审。
- **修复**：删除或改写为中性描述（提及攻击而非发出指令）；对外发布文档纳入审计流。

## PIT-E-07 · Base64 ｜ PIT-E-14 · ROT13 ｜ PIT-E-36 · Reverse ｜ severity: medium，置信度 70
字符串常量单层编码，**仅当解码后命中注入关键词**才报告（严控误报）。
- **检测特征**：引号包裹 ≥20 字符字面量 → 严格解码 → 关键词命中才计；证据含解码载荷。
- **误报边界**：确需内嵌编码数据的安全工具代码；随机 blob 撞库概率极低（严格解码+关键词双门槛）。
- **修复**：改为明文配置+密钥管理；必须保留时加注释说明解码语义。

## PIT-E-57 · Layered Encoding ｜ severity: critical
≥2 层组合编码（base64→rot13→reverse…，至多 5 层剥链）规避关键词过滤。
- **检测特征/误报边界/修复**：同编码类，但命中即视为蓄意规避——优先按恶意处理，复核 `scripts/decode.py` 输出后再下结论。

---
*编号对齐记录：官方 taxonomy 172 节点核对（rules.py 头注）；CVE 逐个查过 NVD。引用前重查 `eval/expected.json` 口径。*

## 覆盖层（v1.1.0 新增）

中文指令覆盖/角色劫持/系统提示泄露/判决劫持/数据外传/工具滥用由覆盖层 `engine/zh_rules.py` 检出，复用上表编号（配置文件语境→T-46，文档→N-06，代码注释→T-51），置信度统一 70（变体规则，待实弹确认后升级）。
