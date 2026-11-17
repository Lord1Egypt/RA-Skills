<div align="center">

# Air-chart

**한 문장이면 됩니다. AI가 전문적인 대기질 차트를 그려드립니다.**

English | [简体中文](README.zh.md) | [Español](README.es.md) | [हिन्दी](README.hi.md) | [日本語](README.ja.md) | **한국어** | [Français](README.fr.md)

![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blue)
![Cursor](https://img.shields.io/badge/Cursor-native-blue)
![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-publishable-green)
![skills.sh](https://img.shields.io/badge/skills.sh-installable-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 이 스킬이 하는 일

AI 채팅에 한 문장만 적으면 — **관측소를 찾고, 데이터를 가져와 차트 링크를 걸어줍니다**. 엔진은 [x-cmd Draw](https://x-cmd.com/draw) — 데이터와 차트가 하나의 URL에:

> 💬 "베이징 지난 일주일 PM2.5 추이 보여줘"
> 💬 "도쿄와 서울의 지난 7일 대기질 비교해줘"
> 💬 "뉴 델리 30일간 PM10, WHO 기준선과 함께"
> 💬 "싱가포르 지난 48시간 시간대별 오존"
> 💬 "베이징에서 지금 가장 나쁜 관측소는 어디야?"

뒤에서는 전 과정이 자동화된 파이프라인이 돌아갑니다: 도시 확인 → **OpenAQ** 에서 **실제로 활동 중인** 관측소 선택 (100개 이상 국가의 정부 기준측정 데이터) → 이상치와 결측 정제 → 전문 차트 렌더링.

**이런 점이 좋습니다:**

- **차트가 곧 URL — URL이 곧 데이터** — 기본적으로 `x-cmd.com/draw` 링크를 받으며, 차트 렌더링과 모든 수치 보관을 동시에 합니다. 공유하거나 Markdown에 이미지로 삽입하거나, URL 속 숫자를 바꾸면 차트도 즉시 업데이트됩니다. 파일이 필요하면 `--out chart.svg` (또는 `.png`) 로 다운로드.
- **x-cmd Draw 렌더링** — 로컬 파이프라인은 순수 `bash`/`jq`/`awk`/`curl` 을 유지하고, 차트 엔진은 [x-cmd Draw](https://x-cmd.com/draw) 를 사용하므로 계속 늘어나는 풍부한 차트 유형 (선, 막대, 영역, 파이, 레이더, 게이지, 샌키, 간트, 마인드맵 등), 라이트/다크 테마, 다국어 렌더링, 온라인 에디터를 그대로 상속하며 유지할 렌더러 코드가 전혀 없습니다. 설치할 것도, 업데이트할 것도 없습니다.
- **설계부터 신뢰할 수 있습니다** — 정부 기준측정 관측소를 우선 선택하고, 차트에는 물리적 농도 (µg/m³) 를 명시하며 **WHO 24시간 기준선**을 참조 시리즈로 겹쳐 표시합니다 — 한계값이 데이터와 함께 따라다니므로 사후 처리가 아닙니다. 겉치레용 AQI 숫자가 아니라 보고서에 그대로 쓸 수 있는 데이터입니다.
- **글로벌 커버리지, 관대한 입력** — 250여 개 도시의 내장 좌표; `delhi`, `tOKyo`, `中山` 같은 뭉그적한 이름도 그대로 작동하며, 원시 `lat,lon` 도 허용됩니다.
- **장난감이 아닌 실제 데이터** — 침묵하는 «좀비» 관측소와 센서 고장 스파이크를 제거하고, 결측 시간대는 축에서 빠지며 0으로 채워지지 않습니다.

## 쇼케이스

아래 차트는 모두 **OpenAQ의 실제 측정값**을 데이터를 품은 URL에서 라이브로 렌더링한 것입니다 — 이 저장소에는 이미지 파일을 저장하지 않습니다. 차트를 클릭하면 x-cmd Draw 에디터에서 값을 조정할 수 있습니다.

| 다중도시 PM2.5, 최근 7일 (도쿄 · 서울 · 런던) | 뉴 델리 PM2.5 / PM10, 최근 14일 |
| --- | --- |
| [![다중도시 PM2.5, 최근 7일 (도쿄 · 서울 · 런던)][sc1] | [![뉴 델리 PM2.5 / PM10, 최근 14일][sc3] |

| 런던 오존 (O₃), 최근 48시간 | 뉴 델리: 관측소별 PM10 스냅샷 (실시간) |
| --- | --- |
| [![런던 오존 (O₃), 최근 48시간][sc2] | [![뉴 델리: 관측소별 PM10 스냅샷 (실시간)][sc4] |

| 다크 테마: 다중도시 PM2.5 | 뉴 델리 PM2.5, 최근 30일 |
| --- | --- |
| [![다크 테마: 다중도시 PM2.5][sc5] | [![뉴 델리 PM2.5, 최근 30일][sc6] |

[sc1]: https://x-cmd.com/draw?type=line&title=PM2.5%20%EB%B9%84%EA%B5%90%20%C2%B7%20%EC%B5%9C%EA%B7%BC%207d%20%C2%B7%20%EB%8B%A4%EC%A4%91%EB%8F%84%EC%8B%9C%20%C2%B7%20%EB%8F%99%EC%9D%BC%20%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024%EC%8B%9C%EA%B0%84:15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc2]: https://x-cmd.com/draw?type=line&title=London%20O3%20%EC%B6%94%EC%9D%B4%20%C2%B7%20%EC%B5%9C%EA%B7%BC%2048h%20%C2%B7%20%ED%98%84%EC%A7%80%20%EC%8B%9C%EA%B0%81%20%28Europe%2FLondon%29&unit=%C2%B5g%2Fm%C2%B3&labels=11-12%2001%3A00,11-12%2002%3A00,11-12%2003%3A00,11-12%2004%3A00,11-12%2005%3A00,11-12%2006%3A00,11-13%2000%3A00,11-13%2001%3A00,11-13%2002%3A00,11-13%2003%3A00,11-13%2004%3A00,11-13%2005%3A00,11-13%2006%3A00,11-13%2007%3A00&series=London%20O3:52.7,51.2,42.7,43.1,41,31.4,42.7,44.9,46.5,48.3,39.6,17.1,15.4,17&series=WHO%2024%EC%8B%9C%EA%B0%84:100,100,100,100,100,100,100,100,100,100,100,100,100,100&w=960&h=500&t=opendata
[sc3]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20%2F%20PM10%20%EC%B6%94%EC%9D%B4%20%C2%B7%20%EC%B5%9C%EA%B7%BC%2014d%20%C2%B7%20%EB%8B%A4%EC%A4%91%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98&unit=%C2%B5g%2Fm%C2%B3&labels=10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=WHO%2024%EC%8B%9C%EA%B0%84:15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc4]: https://x-cmd.com/draw?type=hbar&title=New%20Delhi%20%EA%B4%80%EC%B8%A1%EC%86%8C%EB%B3%84%20%EC%8A%A4%EB%83%85%EC%83%B7%20%C2%B7%20PM10%20%C2%B7%202026-11-14%2013%3A27%20IST%20%C2%B7%20%EB%B0%98%EA%B2%BD%2025km&unit=%C2%B5g%2Fm%C2%B3&labels=Alipur,Anand%20Vihar,Ashok%20Vihar,Aya%20Nagar,Bawana,Burari%20Crossing&values=418.0,409.0,426.0,501.0,382.0,533.0&num=all&w=960&h=480&t=evil-glow
[sc5]: https://x-cmd.com/draw?type=line&title=PM2.5%20%EB%B9%84%EA%B5%90%20%C2%B7%20%EC%B5%9C%EA%B7%BC%207d%20%C2%B7%20%EB%8B%A4%EC%A4%91%EB%8F%84%EC%8B%9C%20%C2%B7%20%EB%8F%99%EC%9D%BC%20%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024%EC%8B%9C%EA%B0%84:15,15,15,15,15,15,15&w=960&h=500&scheme=dark&t=opendata
[sc6]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20%EC%B6%94%EC%9D%B4%20%C2%B7%20%EC%B5%9C%EA%B7%BC%2030d%20%C2%B7%20%ED%98%84%EC%A7%80%20%EC%8B%9C%EA%B0%81%20%28Asia%2FKolkata%29&unit=%C2%B5g%2Fm%C2%B3&labels=10-15,10-16,10-17,10-18,10-19,10-20,10-21,10-22,10-23,10-27,10-28,10-29,10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:73.6,65.7,94,127,94,125,142,136,142,138,131,95,44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=WHO%2024%EC%8B%9C%EA%B0%84:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata

## 특징

- **무거운 의존성 제로** — 순수 `bash` / `jq` / `awk` / `curl`; SVG 렌더러는 awk로 작성.
- **글로벌 커버리지** — 200여 개 주요 도시의 내장 좌표, 또는 `lat,lon` 직접 지정.
- **스마트 관측소 선택** — 반경 25km 검색 → 24시간 침묵한 «좀비» 관측소 제외 (72시간 폴백) → 정부 기준측정 모니터 우선.
- **전문가급 시각화** — 물리적 농도 단위 (µg/m³) 를 뚜렷이 표기, WHO 24시간 기준선 기본 오버레이 (준수 시 초록, 초과 시 빨강), 라이트/다크 테마.
- **실사용을 위한 설계** — 로컬 캐시 (시간별 20분 / 일별 2시간), HTTP 429 지수 백오프, 결측 인식 렌더링 (결측은 선을 끊으며 0으로 채우지 않음), UTC → 관측소 현지 시각 정렬.

## 빠른 시작

### 1. API 키 발급 (무료, 약 1분)

1. [OpenAQ Explorer](https://explore.openaq.org/register) 에서 가입 또는 로그인 (기존 계정: [로그인](https://explore.openaq.org/login)).
2. [계정 페이지](https://explore.openaq.org/account) 를 열어 하단의 API 키를 복사합니다.
3. 설정 — 둘 중 하나:

```bash
export OPENAQ_API_KEY="your_key"                             # ephemeral / CI
echo 'OPENAQ_API_KEY=your_key' > ~/.config/air-chart/config  # persistent
```

시스템 키체인이 필요 없습니다 — 무료 공개 서비스 자격증명은 평문 설정 파일에 보관합니다. 키 없이도 `--demo` 모드가 샘플 데이터로 전부 렌더링합니다.

### 2. 실행

```bash
# 단일 도시, 7일 PM2.5 추이
./scripts/air_chart.sh --city Beijing --param pm25 --period 7d

# 다중도시 비교 (최대 4개)
./scripts/air_chart.sh --city Tokyo --city Seoul --param pm25 --period 7d

# 단일 도시 다중매개변수 (PM2.5 + PM10)
./scripts/air_chart.sh --city Beijing --param pm25 --param pm10 --period 30d

# 48시간 시간별 곡선 (주야 패턴)
./scripts/air_chart.sh --city Singapore --param o3 --period 48h

# 관측소 실시간 막대 차트 스냅샷
./scripts/air_chart.sh --city Delhi --param pm10 --snapshot

# 다크 테마, 파일 출력
./scripts/air_chart.sh --city London --param no2 --period 14d --theme dark -o london.svg
```

### 3. AI 에이전트 스킬로 설치

```bash
git clone https://github.com/qiakai/air-chart.git ~/.claude/skills/air-chart
# or: npx skills add qiakai/air-chart
```

그런 다음 에이전트에게 부탁하세요: *«도쿄와 서울의 지난 7일 PM2.5 를 비교해줘.»*

`SKILL.md` 는 넓은 에이전트/레지스트리 호환성을 위해 영어로 작성했습니다; 중국어 버전은 `SKILL.zh.md` 에 있습니다. 차트 출력은 `--lang en|zh|es|hi|ja|ko|fr` 을 지원하며 기본값은 시스템 로케일 자동 감지입니다.

## CLI 레퍼런스

| Flag | Description | Values |
| --- | --- | --- |
| `--city, -c` | 도시 이름 (반복 가능, ≤4) 또는 좌표 `"lat,lon"` | `Beijing`, `New Delhi`, `39.9,116.4` |
| `--param, -p` | 오염물질 (기본값 `pm25`) | `pm25` `pm10` `o3` `no2` `so2` `co` |
| `--period, -t` | 기간 (기본값 `7d`) | `24h` `48h` (시간별) · `7d` `14d` `30d` (일별) |
| `--snapshot` | 도시 활성 관측소의 막대 차트 스냅샷 | flag |
| `--theme` | 색 테마 | `light` / `dark` |
| `--lang` | 출력 언어 (차트 + 메시지) | `en` `zh` `es` `hi` `ja` `ko` `fr` (기본값: 로케일 자동 감지) |
| `--out, -o` | 차트를 `.svg` 또는 `.png` 로 다운로드 | 기본값: x-cmd Draw URL 만 출력 |
| `--demo` | 데모 모드, API 키 불필요 | flag |

## 아키텍처

```text
[city / pollutant / time range]
   │
   ▼
geo_resolve.sh      city name → coordinates + timezone (built-in gazetteer / raw lat,lon)
   │
   ▼
openaq_client.sh    OpenAQ API v3: auth, User-Agent, md5 cache,
                    429 exponential backoff, liveness filter (24h/72h),
                    sensor match by fixed parameter ID, reference-grade first
   │
   ▼
data_transform.awk  cleaning (negatives / physically impossible spikes),
                    gap detection (breaks, never zero-filled), stats, local-time labels
   │
   ▼
render_draw.sh      x-cmd Draw URL builder (URL-as-Data; optional .svg/.png download)
```

`data/parameters.tsv` 는 openaq-api 고정 오염물질 ID에 맞춘 정적 매개변수 사전입니다: slug / param_id / 이름 / 단위 / WHO 24시간 기준 / 물리적 상한 / 매개변수별 색상 — `/parameters` 중복 호출 없음. 시각화는 openaq-explorer 관례를 따릅니다: 매개변수별 팔레트 (PM2.5 `#E65100`, PM10 `#6A1B9A`, O3 `#0277BD`, NO2 `#00838F`), 색약 친화 다중도시 팔레트, 안전 초록 `#10B981` / 경고 빨강 `#EF4444` WHO 기준선. 관측소가 사전 기본과 다른 단위 (ppm 등) 를 보고하면 Y축은 실제 단위를 사용하고 차원 오독을 막기 위해 WHO 선은 생략됩니다.

## 종료 코드

| Code | Meaning |
| --- | --- |
| 3 | API 키 미설정 (설정 안내 출력) |
| 4 | 네트워크 / API 오류 / 레이트리밋 재시도 소진 |
| 5 | 활성 관측소 없음 또는 유효 데이터 없음 |
| 2 | 도시 이름을 해석할 수 없음 (유사 후보 출력) |

## 라이선스

MIT
