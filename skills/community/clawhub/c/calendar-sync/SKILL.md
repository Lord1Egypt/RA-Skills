---
name: calendar-sync
description: "구조화된 문서 데이터에서 날짜 정보(마감일, 일정, 이벤트)를 추출하여 Apple 캘린더에 자동 등록하는 스킬. 문서에서 추출한 일정을 캘린더에 자동 반영한다."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    os:
      - macos
    emoji: "📅"
    tags:
      - calendar
      - apple-calendar
      - scheduling
      - date-extraction
---

# calendar-sync: Apple 캘린더 연동 스킬

## 목적

`doc-structurer`에서 구조화된 문서 데이터 중 날짜 정보가 포함된 항목을 Apple 캘린더에 자동 등록한다. 마감일, 계약기간, 회의일정, 행사일 등 다양한 유형의 날짜를 적절한 캘린더 이벤트로 변환한다.

## 캘린더 이벤트 유형

문서 유형과 날짜 성격에 따라 이벤트를 구분한다:

### 이벤트 매핑 규칙

| 날짜 필드 | 이벤트 유형 | 알림 설정 |
|-----------|-------------|-----------|
| deadline (마감일) | 종일 이벤트 | 3일 전 + 1일 전 + 당일 오전 9시 |
| event_dates (행사) | 시간 이벤트 (기본 10:00~12:00) | 1일 전 + 2시간 전 |
| start_date ~ end_date (기간) | 다일(multi-day) 이벤트 | 시작 3일 전 + 시작 당일 |
| document_date (작성일) | 등록하지 않음 | - |

### 우선순위별 알림 강화

| 우선순위 | 추가 알림 |
|----------|-----------|
| 상 | 7일 전 알림 추가 |
| 중 | 기본 알림 유지 |
| 하 | 당일 알림만 |

## 이벤트 구성

### 이벤트 필드 매핑

```
제목: [문서유형] 문서제목
  예: [계약서] 용역계약 마감
  예: [공문] 사업계획서 제출 기한

위치: (해당 시 장소 정보)

메모:
  문서유형: 계약서
  발신: OO기관
  담당: 홍길동
  요약: 3줄 요약 내용
  금액: 50,000,000원
  ---
  Notion 링크: https://notion.so/...
  원본 파일: 파일경로

캘린더: "문서 일정" (자동 생성)

URL: Notion 페이지 링크 (있는 경우)
```

### 캘린더 색상 코드

문서 유형별 캘린더를 분리하거나, 단일 캘린더 내에서 색상으로 구분:

| 문서유형 | 색상 |
|----------|------|
| 공문/관공서 | 빨간색 (긴급/공식) |
| 계약서 | 주황색 |
| 제안서 | 파란색 |
| 보고서 | 초록색 |
| 회의록 | 보라색 |
| 기획서 | 노란색 |
| 견적서/청구서 | 분홍색 |
| 기타 | 회색 |

## 실행 방식

### Claude Cowork 환경

Apple Notes MCP 또는 AppleScript를 통해 캘린더에 직접 접근한다:

**AppleScript 방식:**
```applescript
tell application "Calendar"
    -- "문서 일정" 캘린더가 없으면 생성
    if not (exists calendar "문서 일정") then
        make new calendar with properties {name:"문서 일정"}
    end if

    tell calendar "문서 일정"
        make new event with properties {
            summary: "[계약서] 용역계약 마감",
            start date: date "2024-04-15 00:00:00",
            end date: date "2024-04-15 23:59:59",
            allday event: true,
            description: "문서유형: 계약서\n발신: OO기관\n담당: 홍길동",
            url: "https://notion.so/..."
        }
    end tell
end tell
```

**알림 추가:**
```applescript
tell application "Calendar"
    tell calendar "문서 일정"
        tell event "이벤트명"
            -- 3일 전 알림 (분 단위: 3 * 24 * 60 = 4320)
            make new display alarm with properties {trigger interval: -4320}
            -- 1일 전 알림
            make new display alarm with properties {trigger interval: -1440}
            -- 당일 오전 9시
            make new display alarm with properties {trigger interval: 0}
        end tell
    end tell
end tell
```

### ChatGPT 환경

ChatGPT에서는 직접 캘린더 접근이 불가하므로 다음 방식을 제공한다:

**방법 1: ICS 파일 생성**

표준 iCalendar(.ics) 파일을 생성하여 사용자가 더블클릭으로 캘린더에 추가:

```python
from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta

def create_ics(events_data):
    cal = Calendar()
    cal.add('prodid', '-//Doc Calendar Sync//KO')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')

    for item in events_data:
        event = Event()
        event.add('summary', f"[{item['doc_type']}] {item['title']}")
        event.add('dtstart', item['date'])
        event.add('description', item['notes'])

        if item.get('url'):
            event.add('url', item['url'])

        # 알림 추가
        for minutes in item.get('alarms', [-4320, -1440, 0]):
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('trigger', timedelta(minutes=minutes))
            alarm.add('description', f"[{item['doc_type']}] {item['title']}")
            event.add_component(alarm)

        cal.add_component(event)

    return cal.to_ical()
```

**방법 2: AppleScript 코드 제공**

사용자가 macOS 터미널에서 실행할 수 있는 osascript 명령어를 생성.

**방법 3: Shortcuts(단축어) 연동 가이드**

Apple Shortcuts 앱을 활용한 자동화 워크플로우 설정 안내.

## 중복 방지

동일 이벤트가 이미 캘린더에 존재하는지 확인:

1. 같은 제목 + 같은 날짜의 이벤트가 있으면 → 스킵
2. 제목은 같지만 날짜가 다르면 → 기존 이벤트 업데이트 제안
3. doc_id를 메모 필드에 포함시켜 추적 가능하게 함

## 반복 일정 처리

문서에서 "매주", "매월", "분기별" 등의 반복 패턴이 감지되면:

| 패턴 | 반복 규칙 |
|------|-----------|
| 매주 | FREQ=WEEKLY |
| 매월 | FREQ=MONTHLY |
| 분기별 | FREQ=MONTHLY;INTERVAL=3 |
| 매년 | FREQ=YEARLY |

반복 종료일은 문서의 end_date 또는 계약 종료일로 설정.

## 처리 보고

등록 완료 후 보고:
- 총 등록 이벤트 수
- 유형별 분포 (마감일 N건, 행사 N건, 기간 N건)
- 스킵된 항목 (중복, 날짜 없음)
- 캘린더 이름 및 확인 방법
- 알림 설정 요약

## 전체 파이프라인 연결

이 스킬은 전체 워크플로우의 마지막 단계이다:

```
doc-parser → doc-structurer → notion-sync → calendar-sync
   (읽기)      (구조화)        (DB 저장)     (일정 등록)
```

4개 스킬을 순서대로 실행하면, 폴더 내 문서를 읽고 → 분류/구조화하고 → Notion에 저장하고 → 일정을 캘린더에 등록하는 전체 자동화가 완성된다.
