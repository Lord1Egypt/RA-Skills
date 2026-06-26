# Korean Semiconductor Terminology (한국어)

Full lexicon compiled from research.

## Critical Translation Traps

| DON'T translate as... | ACTUALLY use... | Why |
|---|---|---|
| 에칭 (etching) | **식각** | Korean industry uses Sino-Korean term |
| 디포지션 (deposition) | **증착** | Universal in Korean semiconductor press |
| 익스포저 (exposure) | **노광** | Standard lithography term |
| 재료 (material) | **소재** | In supply chain context, 소재 is dominant |
| 회사 (company) | **업체** | Industry press default |

## Must-Know Terms

| English | Korean | Context |
|---|---|---|
| Semiconductor material | 반도체 소재 | The standard supply chain term |
| Materials/parts/equipment | **소부장** (소재+부품+장비) | Post-2019 policy buzzword — appears everywhere |
| Localization | **국산화** | THE key search term for supply chain shifts |
| De-Japan | **탈일본** | 2019-2020 buzzword for import substitution |
| Dual-sourcing | **이원화** / 공급선 이원화 | Supply diversification |
| Supplier | **공급업체** / 납품업체 / 협력업체 | 협력업체 = Samsung's preferred term |
| Precursor | **프리커서** (press) / **전구체** (filings/academic) | Use BOTH in searches |
| High purity | **고순도** / 초고순도 | |
| Etch | **식각** | NOT 에칭 |
| Deposition | **증착** | NOT 디포지션 |
| Lithography exposure | **노광** | |
| Photoresist | **포토레지스트** / **감광액** / PR | 감광액 in older/formal docs |
| EUV | EUV / **극자외선** | |
| CMP slurry | CMP **슬러리** / 연마액 | |
| Specialty gas | **특수가스** | |
| NF3 | NF3 / **삼불화질소** | Chemical name in DART filings |
| HF (hydrofluoric acid) | **불산** / 불화수소 | 불산 = extremely common |
| Silicon wafer | **실리콘 웨이퍼** | |
| Sputtering target | **스퍼터링 타겟** | |

## DART Filing Search Sections

When searching Korean company filings (dart.fss.or.kr):

| Section (Korean) | English | What it reveals |
|---|---|---|
| 주요 제품 등의 현황 | Status of major products | What they make |
| 매출 현황 | Sales status | Revenue breakdown |
| **주요 거래처** | **Major trading partners** | Customers/suppliers |
| **특수관계자와의 거래내역** | Related party transactions | Intra-group supply |
| **원재료 매입 현황** | Raw material purchase status | What they buy and from whom |
| 사업의 내용 | Business description | Company overview |

## Search Query Patterns

```
# Who supplies X to Samsung?
삼성전자 [소재] 공급업체
삼성전자에 [소재] 납품하는 업체

# Who supplies X to SK Hynix?
SK하이닉스 [소재] 공급업체
SK하이닉스 [소재] 납품

# Localization progress for a material
[소재] 국산화 성공
[소재] 국산화 진행

# New supplier qualification
[업체명] [고객사]향 납품 개시
[업체명] [고객사] 공급업체 선정
```
