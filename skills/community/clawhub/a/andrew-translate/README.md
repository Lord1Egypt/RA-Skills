# andrew-translate

Andrew Ng translation-agent style three-step translation skill: **initial translate → reflect → improve**.

基于吴恩达 translation-agent 思路的三步翻译技能：**初译 → 反思 → 改进**。

## Evaluation / 评测

Agent model `glm-5.3-flash-external` via miniagent, 2026-10-19. 10 cases, assertions graded by script, one run per case.

| Version | With skill | Baseline (no skill) |
|---|---|---|
| **1.3.2** | **38 / 38** (10/10 cases all-pass) | 36 / 38 (8/10) |
| 1.3.0 | 36 / 38 (8/10) | 36 / 38 (8/10) |

- **Long document (2,092 words):** 1.3.2 counts the words with a tool, then forces the chunked workflow. The run's trace shows glossary → chunk plan → 5 × (reflection, revised draft) → merge → heading check (13/13). It scores 6/6 in 366s. 1.3.0 ignored its own 2,000-word threshold, translated in one shot and scored 5/6.
- **Term consistency (k8s):** 4/5 → 5/5. "Node" is now kept as Node.
- **SKILL.md is read on every case**, versus 1.3.0, which skipped it once and read only part of it once. Short texts take a no-tool fast path. Total wall time for cases 1–9 was 476s, down from 660s.
- **Triggering** (24 mixed queries, 4 skills installed): 6/6 recall, 0 false triggers.
- **Caveats:**
  - Each case ran once.
  - The baseline is already strong on this model, so the lift is small: +2 assertions.
  - On the Markdown-structure case, the final reply still only points to the saved file instead of including the translation.

被测模型 `glm-5.3-flash-external`（miniagent），2026-10-19，10 个用例，每例 1 次。

- **得分：** 1.3.2 得 **38/38**，无技能基线 36/38，1.3.0 为 36/38。
- **长文（2,092 词）：** 先用工具计数，再强制走分块流程（术语表 → 分块 → 5 块各自反思+修订 → 合并 → 标题核对 13/13），6/6，用时 366s。
- **触发：** 24 条混合查询中召回 6/6，无误触发。
- **不足：** Markdown 用例的最终回复仍只提示"已保存到文件"，未贴出译文。

## Install / 安装

- ClawHub: https://clawhub.ai/linkxzhou/andrew-translate
- SkillHub: https://skillhub.cn/skills/user_16e7431e/andrew-translate

## Structure / 结构

```
SKILL.md                 # Skill definition / 技能定义
references/prompts.md    # Prompts for each step / 各步骤提示词
references/languages.md  # Language notes / 语言说明
evals/evals.json         # Evaluation cases / 评测用例
```
