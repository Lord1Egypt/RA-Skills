---
name: bazi-qimen
description: Bazi (Four Pillars Astrology) and Qi Men Dun Jia chart calculation and interpretation skills. Provides data analysis and cognitive science based calculations and interpretations, serving as an auxiliary decision-making reference rooted in traditional Chinese metaphysics.
---

# Bazi-Qimen

Provides data analysis and cognitive science based Bazi (Four Pillars Astrology) and Qi Men Dun Jia chart calculation and interpretation, serving as an auxiliary rational decision-making reference rooted in traditional Chinese metaphysics.

## Use Cases

- Bazi chart / Four Pillars calculation
- Bazi interpretation (Career / Wealth / Relationships / Health)
- Qi Men Dun Jia chart calculation
- Qi Men Dun Jia interpretation / divination
- Major Luck (Da Yun) and Annual Luck (Liu Nian) analysis
- Day Master elemental strength and pattern analysis
- Divine spirits / Peach Blossom / Traveling Horse queries
- Favorable and unfavorable element analysis (Yong Shen / Ji Shen)
- Qi Men element spirit palace auspiciousness/inauspiciousness judgment.

## Trigger Words

Bazi, Four Pillars, chart calculation, interpretation, astrology, Day Master, Major Luck, Annual Luck, Ten Gods, Qi Men, Dun Jia, Qi Men chart, divination, Five Elements, Favorable Element, pattern, Divine Spirits, Peach Blossom, Horse, Heavenly Help Star, Star of Wisdom.

## Usage

This skill supports two metaphysical systems, selected based on user intent:

**Bazi Chart Calculation/Interpretation**: User mentions "Bazi", "Four Pillars", "chart calculation", "astrology", "Day Master", "Major Luck", "Annual Luck", "Ten Gods" → Bazi route.
**Qi Men Dun Jia Chart Calculation/Interpretation**: User mentions "Qi Men", "Dun Jia", "Qi Men chart", "divination" → Qi Men route.

If the user does not specify clearly, default to calculating the Bazi chart first to analyze the life profile, then supplement with a Qi Men chart based on the specific question.

## Bazi Workflow

### Chart Calculation
Run `scripts/bazi_calculator.py` to generate a complete Bazi chart:

```bash
python3 "{SKILL_DIR}/scripts/bazi_calculator.py" --year 1990 --month 5 --day 15 --hour 14 --gender male
```

Output includes:
- Four Pillars (Year, Month, Day, Hour) and their Celestial Stems, Earthly Branches, Five Elements, Ten Gods
- Hidden Stems within each Earthly Branch
- Na Yin (Elemental Melody)
- Major Luck (Da Yun) arrangement
- Basic Divine Spirits
- Five Elements statistics

### Interpretation
Refer to `references/bazi_basics.md` and `references/interpretation_guide.md` for analysis, following these layers:

1.  **Day Master Characterization**: Day stem's Five Element + Yin/Yang → personality archetype.
2.  **Strength Assessment**: Does the month command the element? Roots? Support → Strong / Weak / Balanced.
3.  **Pattern & Usage**: Pattern determined by the month branch → Ten God combinations → Favorable (Yong Shen) / Unfavorable (Ji Shen) elements.
4.  **Major Luck & Annual Luck**: Interactions (Generate, Control, Clash, Harm, Combine) between the current Major Luck, Annual Luck, and the natal chart.
5.  **Specific Topic Analysis**: Conduct detailed analysis based on the user's question (Career/Wealth/Relationships/Health).

Refer to the output standards in `references/interpretation_guide.md` for the output format.

### Key Calculation Formulas
- **Year Pillar**: Uses Li Chun (Start of Spring) as the boundary. 1984 = Jia Zi year. Calculate using `(Year - 1984) % 60`.
- **Month Pillar**: Months are divided by Solar Terms (Jie Qi), with the day of the Solar Term as the boundary. Use the "Five Tiger Escape" to determine the month stem ("Jia Ji year, Bing leads...").
- **Day Pillar**: Uses 1900-01-01 = Jia Xu day as the reference. Accumulate total days and take modulo 60.
- **Hour Pillar**: Zi hour is 23:00-01:00. Each two hours is one Shichen (Double Hour). Use the "Five Rat Escape" to determine the hour stem ("Jia Ji day, Jia leads...").

## Qi Men Dun Jia Workflow

### Chart Calculation
Run `scripts/qimen_calculator.py` to generate a Qi Men chart:

```bash
python3 "{SKILL_DIR}/scripts/qimen_calculator.py" --year 2026 --month 5 --day 10 --hour 10
```

If no parameters are passed, it uses the current time. Output includes:
- Solar Term (Jie Qi), Yin/Yang Dun type, and Bureau number
- Hour stem and branch
- Value Star (Zhi Fu) and Value Door (Zhi Men)
- Complete 9-palace chart (Earth Stem, Star Stem, Heavenly Stem, 8 Doors, 8 Gods)

Refer to `references/qimen_basics.md` for detailed calculation principles.

### Interpretation
Refer to the key judgment points in `references/qimen_basics.md`:
1.  Day Stem's palace (Represents the querent's status)
2.  Hour Stem's palace (Represents the matter's status)
3.  Element Spirit (Yong Shen)'s palace (Select symbols based on the question asked)
4.  Value Star & Value Door analysis (overall trend and direction)
5.  Auspicious/Inauspicious pattern determination

## Reference Materials

Load on demand to avoid consuming context:
- `references/bazi_basics.md` — Bazi foundation tables (Heavenly Stems, Earthly Branches, Five Elements, Ten Gods, complete Divine Spirits list)
- `references/qimen_basics.md` — Qi Men foundation tables (9 Palaces, 9 Stars, 8 Doors, 8 Gods, Solar Term / Bureau table)
- `references/interpretation_guide.md` — Interpretation methodology framework and output standards

## Important Notes

- The chart calculation uses simplified Solar Term dates, which may differ from the actual calendar by 1-2 days.
- The age of starting Major Luck is simplified. Precise calculation requires the number of days from the birth date to the next Solar Term.
- The triple-ternary (San Yuan) judgment for Qi Men is simplified. The precise version requires consulting a perpetual calendar for Solar Term transition times.
- This tool is intended for traditional culture study and reference, not for making substantive decisions.
- All analyses must state the probabilistic nature of the basis for analysis, avoiding absolute language.
- Each analysis must end with a disclaimer (see the disclaimer template in `interpretation_guide.md`).