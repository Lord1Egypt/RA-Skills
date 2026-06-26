# Journal-Specific Style Conventions

Moved from main SKILL.md §17.

## 心理学报 (Acta Psychologica Sinica)

- Language: Chinese
- Statistics: "F(1, 58) = 12.34, p = 0.001, ηp² = 0.18"
- Decimals: p to 3 decimal places (except p < 0.001)
- Tone: restrained, avoid over-interpretation
- "结果表明/显示" preferred over "证明"
- Figure/table citation: "见图 1" "见表 2"

## APA 7th Edition (English)

- Language: English
- Statistics: "F(1, 58) = 12.34, p = .001, ηp² = .18"
- p-value format: no leading zero (.001 not 0.001)
- Abbreviations: full term on first use
- Numbers: words for <10, numerals for ≥10
- Effect sizes must be reported

## Chinese Statistical-Format Consistency Rule

Default Chinese Results use **APA-like Chinese statistical format**:
- `p = .021`
- `ηp² = .144`
- `Cohen's d = 0.50`

If user explicitly requests 《心理学报》 style, switch to:
- `p = 0.021`
- `p < 0.001`
- `ηp² = 0.144`

**Hard rule:** Never mix `p = .021` and `p = 0.021` in the same output. All p-values, ηp², and other decimal statistics must follow the same format throughout.

- APA / English style requested → APA format (no leading zero on p)
- 《心理学报》/ Chinese core journal requested → Chinese journal format (with leading zero)
- Not specified → default APA-like Chinese format
