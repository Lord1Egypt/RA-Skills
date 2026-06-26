# Fudan Rankings 2025 Snapshot

This file is the bundled static ranking baseline for this skill. Use it for recommendation logic without runtime web search.

## Snapshot Notes

- Internal snapshot label: 2025 working reference
- Intended use: hospital and specialty ranking baseline inside this skill
- Runtime rule: do not search for Fudan rankings during report generation
- Delivery note: dynamic hospital pages and logistics still need current verification

## Top Comprehensive Hospitals

The following hospitals are treated as the top comprehensive tier in this bundled snapshot:

1. 中国医学科学院北京协和医院 — Peking Union Medical College Hospital — Beijing
2. 四川大学华西医院 — West China Hospital, Sichuan University — Chengdu
3. 中国人民解放军总医院 — Chinese PLA General Hospital — Beijing
4. 上海交通大学医学院附属瑞金医院 — Ruijin Hospital, Shanghai Jiao Tong University — Shanghai
5. 中山大学附属第一医院 — The First Affiliated Hospital of Sun Yat-sen University — Guangzhou
6. 复旦大学附属中山医院 — Zhongshan Hospital, Fudan University — Shanghai
7. 华中科技大学同济医学院附属同济医院 — Tongji Hospital, Tongji Medical College — Wuhan
8. 空军军医大学第一附属医院（西京医院）— Xijing Hospital — Xi'an
9. 北京大学第三医院 — Peking University Third Hospital — Beijing
10. 浙江大学医学院附属第一医院 — The First Affiliated Hospital, Zhejiang University — Hangzhou

## Structured Specialty Rankings Included In This Snapshot

These specialties include bundled top-3 hospital rows in the current internal snapshot:

- 心血管病
- 血液科
- 肿瘤学
- 神经外科
- 神经内科
- 呼吸科
- 消化病
- 肾脏病
- 内分泌
- 骨科
- 眼科
- 妇产科
- 小儿内科
- 皮肤科
- 胸外科
- 心外科 / 心血管外科
- 口腔科
- 烧伤科
- 整形外科
- 传染感染科
- 精神医学
- 风湿免疫科
- 麻醉科
- 病理科
- 放射科
- 急诊医学
- 重症医学
- 康复医学
- 核医学
- 检验医学
- 超声医学
- 耳鼻喉科
- 普外科
- 泌尿外科
- 变态反应
- 疼痛

## Coverage List: 45 Specialties

The bundled 2025 working reference covers these 45 specialties as the full specialty universe for mapping and scope control:

1. 神经内科
2. 肾脏病
3. 神经外科
4. 消化病
5. 小儿内科
6. 风湿病
7. 妇产科
8. 骨科
9. 精神医学
10. 口腔科
11. 小儿外科
12. 心血管病
13. 心外科
14. 胸外科
15. 血液科
16. 病理科
17. 传染感染
18. 耳鼻喉科
19. 放射科
20. 呼吸科
21. 眼科
22. 整形外科
23. 皮肤科
24. 泌尿外科
25. 普外科
26. 烧伤科
27. 麻醉科
28. 肿瘤学
29. 内分泌
30. 老年医学
31. 运动医学
32. 康复医学
33. 急诊医学
34. 重症医学
35. 超声医学
36. 核医学
37. 检验医学
38. 变态反应
39. 疼痛
40. 放疗
41. 内镜
42. 药学
43. 临床药学
44. 护理
45. 病案信息

## Example Top-3 Rows Used Frequently

### 肿瘤学

| Rank | Hospital (Chinese) | Hospital (English) | City |
|---|---|---|---|
| #1 | 中国医学科学院肿瘤医院 | Cancer Hospital, CAMS | Beijing |
| #2 | 中山大学肿瘤防治中心 | Sun Yat-sen University Cancer Center | Guangzhou |
| #3 | 复旦大学附属肿瘤医院 | Fudan University Shanghai Cancer Center | Shanghai |

### 心血管病

| Rank | Hospital (Chinese) | Hospital (English) | City |
|---|---|---|---|
| #1 | 复旦大学附属中山医院 | Zhongshan Hospital, Fudan University | Shanghai |
| #2 | 中国医学科学院北京协和医院 | Peking Union Medical College Hospital | Beijing |
| #3 | 首都医科大学附属北京安贞医院 | Beijing Anzhen Hospital | Beijing |

### 神经外科

| Rank | Hospital (Chinese) | Hospital (English) | City |
|---|---|---|---|
| #1 | 首都医科大学附属北京天坛医院 | Beijing Tiantan Hospital | Beijing |
| #2 | 复旦大学附属华山医院 | Huashan Hospital, Fudan University | Shanghai |
| #3 | 中国医学科学院北京协和医院 | Peking Union Medical College Hospital | Beijing |

### 血液科

| Rank | Hospital (Chinese) | Hospital (English) | City |
|---|---|---|---|
| #1 | 中国医学科学院血液病医院 | Institute of Hematology & Blood Diseases Hospital | Tianjin |
| #2 | 苏州大学附属第一医院 | The First Affiliated Hospital of Soochow University | Suzhou |
| #3 | 北京大学人民医院 | Peking University People's Hospital | Beijing |

### 妇产科

| Rank | Hospital (Chinese) | Hospital (English) | City |
|---|---|---|---|
| #1 | 复旦大学附属妇产科医院 | Obstetrics and Gynecology Hospital, Fudan University | Shanghai |
| #2 | 中国医学科学院北京协和医院 | Peking Union Medical College Hospital | Beijing |
| #3 | 北京大学第三医院 | Peking University Third Hospital | Beijing |

## Usage Rule

If a case maps to a specialty in the 45-specialty universe but the current bundled snapshot does not include structured top-3 rows for that specialty, say so in internal reasoning and fall back to:

1. top comprehensive hospitals
2. city fit
3. department-level current verification

Do not invent missing specialty ranking rows.
