# Numbers, Dates, Names, and Addresses

**Before rendering a person's, company's or product's name in Chinese**, read `### Terms` in the glossary box `## Boxes` names in `~/Clawic/data/chinese/memory.md`. A name written two ways across two documents has been changed by accident, and it is the drift readers notice first.

**Contents:** [Numbers Group by Four](#numbers-group-by-four) · [二 and 两](#二-and-两) · [Money](#money) · [Dates and Time](#dates-and-time) · [Phone Numbers](#phone-numbers) · [Addresses](#addresses) · [Chinese Names](#chinese-names) · [Foreign Names in Chinese](#foreign-names-in-chinese) · [Naming a Product or Company](#naming-a-product-or-company) · [Lucky and Unlucky Numbers](#lucky-and-unlucky-numbers) · [What Gets Written Down](#what-gets-written-down)

## Numbers Group by Four

万 = 10⁴, 亿 = 10⁸, 兆 = 10¹² (and in Taiwan 兆 sometimes means 10⁶ in technical contexts — state the figure in digits when it matters).

Conversion: `value ÷ 10,000` → 万 · `value ÷ 100,000,000` → 亿.

| Digits | Chinese | Wrong |
|---|---|---|
| 12,000 | 1.2万 or 一万二 | 12千 |
| 1,200,000 | 120万 | 1.2百万 |
| 35,000,000 | 3500万 | 35百万 |
| 3,500,000,000 | 35亿 | 3.5十亿 |
| 0.5 billion | 5亿 | 半十亿 |

- The comma-grouped seven-digit figure (`1,200,000`) inside Chinese prose is a translation artefact. In tables and financial statements digits with commas are normal; in a sentence, use 万/亿.
- Reading English financial figures across is where errors happen: **million ÷ 100 = 万**, **billion × 10 = 亿**. Do the arithmetic explicitly rather than pattern-matching the word.
- 几 marks approximation: 十几个 (ten-something), 几十个 (dozens), 上百 (over a hundred), 好几千 (several thousand).
- Percentages: 30%, or 百分之三十 in formal written text. A percentage-point change is 百分点: 从30%涨到35%是涨了5个百分点，不是5%.
- 倍 counts multiples and is a classic trap: 增加了三倍 means it became four times the original in careful usage, while 增加到三倍 unambiguously means three times. Write the unambiguous form (增加到X倍 or 增加了X%) whenever money depends on it.

## 二 and 两

| Context | Form |
|---|---|
| Before a measure word | 两 — 两个人, 两天, 两次 |
| Ordinals and compound numbers | 二 — 第二, 十二, 二十二 |
| Before 百/千/万/亿 | Both occur; 两百 is common in the south, 二百 in the north; 两万 and 两亿 are standard everywhere |
| Fractions and decimals | 二 — 二分之一, 零点二 |
| Time | 两点 (two o'clock), 二十分 (twenty minutes past) |
| Phone numbers and ID digits, spoken | 幺 for 1 and 二 for 2, digit by digit |

## Money

| Currency | Written | Spoken | Symbol |
|---|---|---|---|
| 人民币 | 元 | 块 | ¥ or ￥, and RMB / CNY in international text |
| 新台币 | 元 | 塊 | NT$, TWD |
| 港币 | 元 | 蚊 (Cantonese) | HK$, HKD |

- 角 (written) = 毛 (spoken) = 0.1元; 分 = 0.01元. 三块五 means 3.5元; 三块五毛 is the fuller spoken form.
- Formal and legal amounts use the anti-tampering numerals: 壹 贰 叁 肆 伍 陆 柒 捌 玖 拾 佰 仟 万 亿, closed with 整 — 人民币壹万贰仟元整. Used on cheques, contracts and invoices, and getting it right is a competence signal in `documents.md`.
- Every amount in stored data carries its currency inside the value (`800 CNY`), never a bare symbol (`memory-template.md`).
- 含税 / 不含税 must be stated on any quoted price (`business.md`).

## Dates and Time

- Full date: 2026年7月26日. Never 26/7/2026 in Chinese prose.
- Short forms: 7月26日, 26号 (spoken and casual), 本月26日 (formal).
- Weekday: 星期六 (standard) · 周六 (most common in writing) · 礼拜六 (spoken, southern-leaning). Sunday is 星期日 in writing, 星期天 in speech; 周日 either way. Record the user's habit in `conventions.weekday`.
- Time: 上午9点 / 下午3点 / 晚上8点 in ordinary text; 09:00 and 15:00 in schedules and formal notices. 凌晨 covers roughly midnight to dawn and is used precisely, not poetically.
- 半 is the half hour (三点半), 一刻 the quarter (三点一刻), 差五分 the "five to" (差五分三点).
- Ranges use ～ or 至: 3～5天, 2026年7月26日至7月30日.
- Relative time: 前天 / 昨天 / 今天 / 明天 / 后天 · 上周 / 本周 / 下周 · 上个月 / 这个月 / 下个月. 大前天 and 大后天 exist and are used.
- 农历 (lunar calendar) dates matter for festivals and for older people's birthdays; a date that is 农历 must say so — 农历八月十五, otherwise it will be read as solar.

## Phone Numbers

- Mainland mobile: 11 digits, grouped 3-4-4 — 138 0013 8000.
- Landline: area code plus number, 010-12345678 (Beijing), 021-12345678 (Shanghai).
- Taiwan mobile: 09xx-xxx-xxx. Hong Kong: 8 digits, grouped 4-4.
- Spoken digit by digit with 幺 for 1: 幺三八，零零幺三，八零零零.
- A phone number the user did not ask to keep is not written to `~/Clawic/data/` (`memory-template.md`).

## Addresses

**Big to small**, the opposite of English:

`国家 → 省/直辖市 → 市 → 区/县 → 街道/路 + 号 → 小区/大厦 → 楼/座 → 室`

中国 广东省 深圳市 南山区 科技园南路 15号 软件大厦 3座 1802室

- Postcode (邮编) is six digits and goes at the end or on its own line.
- 收件人 (recipient) and 联系电话 are part of a mailing address and expected on a delivery label.
- Romanised addresses reverse the order and are for international post only; a Chinese courier needs the Chinese order.
- 座 / 栋 / 号楼 all name a building within a compound and differ by city — copy whatever the address itself uses rather than normalising it.

## Chinese Names

- Order is 姓 + 名: 王建国 is surname 王, given name 建国. In Latin script the mainland convention is Wang Jianguo (surname first, given name joined); Taiwanese and Hong Kong conventions often hyphenate (Wang Chien-kuo) or reverse the order.
- Never address someone by given name alone unless you are peers or intimates (`register.md`).
- 姓 + title is the default: 王总, 李老师, 张医生.
- 老 + 姓 and 小 + 姓 depend on relative age and direction (`register.md`).
- 哥 / 姐 attach to the **surname**: 王哥, 李姐. Attaching them to a given name can collide with a product or meme name.
- Two-character surnames exist (欧阳, 司马, 上官) and splitting them is an embarrassing error; when a three-character name is unfamiliar, check before assuming the first character is the surname.
- 女士 / 先生 for formal external address. 小姐 is unsafe on the mainland and normal in Taiwan and Hong Kong.

## Foreign Names in Chinese

- Transliteration joins syllables with the interpunct ·: 史蒂夫·乔布斯, 埃隆·马斯克.
- Established renderings are not negotiable — a person, brand or place with a known Chinese name keeps it. Inventing a new transliteration for a known name reads as an error, not a choice.
- Mainland and Taiwan transliterate differently for the same person (奥巴马 / 歐巴馬, 悉尼 / 雪梨, 新西兰 / 紐西蘭). Pick by `variant` (`regions.md`).
- A foreign name a Chinese reader must say aloud benefits from a short 拼音 or descriptive gloss on first use, and then never again.
- Once decided, a name is a glossary row. This is the single most drift-prone item in the whole domain.

## Naming a Product or Company

Four checks before proposing a Chinese name:

1. **Mandarin reading** — does it sound like anything unintended, including in the tones?
2. **Cantonese and dialect readings** — a name that works in Mandarin can be a joke in Cantonese, and Hong Kong and Guangdong will find it.
3. **Character meanings in combination** — four characters that accidentally form or near-form an existing 成语 will be read as that 成语.
4. **Whether to transliterate at all** — phonetic (可口可乐 style), semantic (苹果 style), keeping the Latin name, or Latin plus a Chinese descriptor. All four are defensible and all four are irreversible once a market knows the brand.

Trademark clearance is a legal step, not a language one, and it belongs in the project file rather than here.

## What Gets Written Down

- **Every name rendered in Chinese for the first time** — person, company, product, place, technical term → a `### Terms` row with the variant and the date. Names are what drifts.
- **A naming decision with its rejected options and the reason** → `artifacts/naming-<what>.md`, with its `## Boxes` line in the same turn. The rejected candidate matters as much as the chosen one, because it will be re-proposed.
- **A person's title and how they are addressed** → their `## Recipients` row (`register.md`); the person themselves goes to the shared contacts box.
- **A convention the user states** — 周六 versus 星期六, 元 versus 块, date shape → `conventions` in `config.yaml`.
