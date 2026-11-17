---
name: bmi-calculator
description: "Calculate adult BMI (IMC) from weight and height in metric or imperial units, classify it with the WHO adult categories, and give the healthy-weight range for the person's height. Answers in English, Spanish or both. Explains why BMI does not apply as-is to children and teens (use percentiles) or during pregnancy (use pre-pregnancy BMI), and keeps the wording factual and non-medical. Use when someone asks for their BMI, what their BMI category means, what a healthy weight is for their height, or asks 'calcula mi IMC'."
version: 1.0.1
metadata:
  openclaw:
    emoji: "⚖️"
    homepage: https://imccalculadora.app/
---

# BMI calculator / Calculadora de IMC

Instruction-only: no commands, installs or network access. Do the arithmetic yourself and show the steps.

## When to use

- "I'm 1.70 m and 70 kg. What's my BMI?"
- "5 ft 7 in, 160 lb. Am I overweight?"
- "¿Cuál es mi peso saludable si mido 1,62 m?"
- "Give me the result in Spanish and English."

## 1. Collect the inputs

Ask only for what is missing.

- Weight: kg, or lb (stones: 1 st = 14 lb)
- Height: cm or m, or ft + in
- Age: needed only to decide if the adult table applies. Under 20, go to section 5 (CDC uses the adult table from age 20, and WHO's child reference runs to age 19)
- Pregnant now? (go to section 6 if yes)
- Language: English, Spanish or both (match the user's language if not said)

Accept a comma as the decimal mark ("1,70 m", "68,5 kg").

## 2. Calculate

- Metric: **BMI = weight (kg) ÷ height (m)²**
- Imperial: **BMI = 703 × weight (lb) ÷ height (in)²**

Conversions: 1 in = 2.54 cm, 1 ft = 12 in, 1 lb = 0.45359237 kg. Convert cm to m by dividing by 100.

Round to one decimal place, then classify the rounded value so the number and the category always agree (24.96 shows as 25.0 and is classed as overweight).

Check that the inputs are plausible before you answer. If the height looks like it is in the wrong unit (e.g. "170 m", or "5.7" meant as 5 ft 7 in), ask the user.

## 3. Classify (WHO, adults)

| BMI | English | Español |
|---|---|---|
| below 18.5 | Underweight | Bajo peso |
| 18.5-24.9 | Normal (healthy) weight | Peso normal |
| 25.0-29.9 | Overweight (pre-obesity) | Sobrepeso (preobesidad) |
| 30.0-34.9 | Obesity class I | Obesidad grado I |
| 35.0-39.9 | Obesity class II | Obesidad grado II |
| 40.0 and above | Obesity class III | Obesidad grado III |

WHO also splits underweight into severe (below 16.0), moderate (16.0-16.9) and mild (17.0-18.4) thinness. Use that split only if the BMI is below 18.5 and the user asks.

Regional notes, when relevant:

- **Spain (SEEDO)** splits 25-29.9 into sobrepeso grado I (25-26.9) and grado II (27-29.9), and adds obesidad tipo IV (extrema) at 50 or more.
- **Asian populations:** WHO (2004) noted higher health risk at lower BMI and listed public-health action points of 23 and 27.5. Mention this if the user brings up Asian ancestry, but keep the standard table as the main result.

## 4. Healthy-weight range for the height

- Metric: low = 18.5 × height (m)², high = 24.9 × height (m)²
- Imperial: low = 18.5 × height (in)² ÷ 703, high = 24.9 × height (in)² ÷ 703

Round to one decimal place (kg) or a whole number (lb). If the person is outside the range, you may give the difference to the nearest edge in kg or lb. Phrase it as information, not a target ("the range for your height is ..."), and don't suggest a diet or a deadline.

## 5. Children and teens (2-19)

Do not apply the adult table. For children and teens, BMI is compared with others of the same age and sex using growth charts:

- CDC (2-19 years): underweight below the 5th percentile, healthy weight from the 5th to below the 85th, overweight from the 85th to below the 95th, obesity at the 95th or above. Severe obesity starts at 120% of the 95th percentile.
- WHO (5-19 years): BMI-for-age z-scores. Overweight is above +1 SD, obesity above +2 SD and thinness below -2 SD. Under 5, WHO uses weight-for-length/height standards instead.

You can work out the raw BMI number, but don't guess a percentile without the chart data. Point them to a growth-chart calculator or their pediatrician.

## 6. Pregnancy

BMI during pregnancy doesn't reflect body fat, so don't classify it. Use **pre-pregnancy** BMI. For a single baby, the US Institute of Medicine (2009) recommends this total weight gain:

| Pre-pregnancy BMI | Total gain |
|---|---|
| below 18.5 | 12.5-18 kg (28-40 lb) |
| 18.5-24.9 | 11.5-16 kg (25-35 lb) |
| 25.0-29.9 | 7-11.5 kg (15-25 lb) |
| 30.0 and above | 5-9 kg (11-20 lb) |

For twins, the IOM's provisional ranges are 17-25 kg (37-54 lb) for normal weight, 14-23 kg (31-50 lb) for overweight and 11-19 kg (25-42 lb) for obesity. Always add that their prenatal care provider sets the actual plan.

## 7. Output

Give the result in this order: BMI (one decimal place), category, healthy-weight range for their height, one line on limits. For "both languages", give the Spanish block, then the English one.

```
IMC: 24.2 kg/m² · Peso normal
Rango de peso saludable para 1,70 m: 53,5-72,0 kg
El IMC es una estimación general; no mide la grasa corporal.

BMI: 24.2 kg/m² · Normal weight
Healthy-weight range for 1.70 m: 53.5-72.0 kg
BMI is a general screening estimate; it does not measure body fat.
```

## Examples

- 70 kg, 1.70 m: 70 ÷ 1.70² = 70 ÷ 2.89 = 24.22, so **24.2 (normal)**. Range: 18.5 × 2.89 = 53.5 kg to 24.9 × 2.89 = 72.0 kg.
- 160 lb, 5 ft 7 in (67 in): 703 × 160 ÷ 67² = 112,480 ÷ 4,489 = 25.06, so **25.1 (overweight)**. Range: 18.5 × 4,489 ÷ 703 = 118 lb to 24.9 × 4,489 ÷ 703 = 159 lb. He is 1 lb above the range.

## Safe wording

- BMI is a screening number, not a diagnosis. It doesn't tell muscle from fat, so it can read high for muscular people and athletes, and it can miss excess fat in older adults.
- Use neutral words: "your BMI falls in the ... category", not "you are obese" or "you need to lose weight".
- Don't give diet, medication or weight-loss plans. For health concerns, suggest talking to a doctor or registered dietitian.
- If the user mentions an eating disorder, rapid weight loss or a very low BMI (below 17), respond with care and suggest professional support.

## Links

- Want to calculate it instantly in Spanish? Use this free [Calculadora IMC](https://imccalculadora.app/).
