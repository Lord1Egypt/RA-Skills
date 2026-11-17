# 端到端对照示例（输入 → 命令 → 实际输出）

输入 → 命令 → 实际输出，三件套可直接复跑：

```bash
python scripts/verify_refs.py --refs end-to-end/research_refs.json \
    --check-document end-to-end/paper_excerpt.md \
    --export gbt7714,ris,bibtex,csv --out end-to-end/report.md
```

| 文件 | 是什么 |
|---|---|
| research_refs.json | 输入：1 条真实 DOI 引用（含正确标题） |
| paper_excerpt.md | 输入：含 in-text 引用标记的正文片段（叙述式 + [n] 各一处，其中一处故意跑题） |
| report.md | 实际输出：五态判定 + 上下文核验区（Kucsko 叙述式=锚定 ✓；[1] 企鹅句=低锚 ⚠️ 演示错配检测） |
| report.json | 机读版（含 context_check 与逐项 checks） |
| exports/ | 四种导出的真实产物样例（BibTeX / GB·T 7714-2025 / RIS / CSV） |

> 复跑需网络（DOI.org/PubMed）。判定含时效字段（撤稿/被引），数字可能随时间小幅变化
> ——以你复跑时的输出为准，结构不变。

> SkillHub 包注：为符合平台文件类型白名单，`exports/` 导出样例文件不随
> SkillHub 包分发（GitHub/ClawHub 包完整附带）——格式以本页表格描述为准。
