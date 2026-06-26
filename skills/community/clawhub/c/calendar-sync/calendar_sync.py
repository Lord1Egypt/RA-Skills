"""
calendar_sync.py - Apple 캘린더 연동 스크립트
structured_results.json에서 날짜 정보 추출 → ICS 파일 생성 또는 AppleScript로 직접 등록
"""

import os
import sys
import json
import subprocess
import platform
from datetime import datetime, timedelta, date

try:
    from icalendar import Calendar, Event, Alarm
except ImportError:
    print("❌ icalendar 라이브러리가 필요합니다.")
    print("   pip install icalendar")
    sys.exit(1)


# --- 알림 설정 ---
ALARM_PRESETS = {
    "상": [
        timedelta(days=-7),   # 7일 전
        timedelta(days=-3),   # 3일 전
        timedelta(days=-1),   # 1일 전
        timedelta(hours=-2),  # 당일 2시간 전 (시간 이벤트용)
    ],
    "중": [
        timedelta(days=-3),
        timedelta(days=-1),
        timedelta(hours=-2),
    ],
    "하": [
        timedelta(days=-1),
    ],
}

# 종일 이벤트용 알림 (시간 기반 대신 일 기반)
ALLDAY_ALARM_PRESETS = {
    "상": [-7, -3, -1, 0],   # 일 단위
    "중": [-3, -1, 0],
    "하": [0],
}


def parse_date(date_str):
    """날짜 문자열을 date 객체로 변환"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


def create_event_title(doc):
    """이벤트 제목 생성: [문서유형] 문서제목"""
    doc_type = doc.get("doc_type", "기타")
    title = doc.get("title", "제목 없음")
    return f"[{doc_type}] {title}"


def create_event_description(doc):
    """이벤트 메모/설명 생성"""
    lines = []
    if doc.get("doc_type"):
        lines.append(f"문서유형: {doc['doc_type']}")
    if doc.get("organization"):
        lines.append(f"발신: {doc['organization']}")
    if doc.get("assignee"):
        lines.append(f"담당: {doc['assignee']}")
    if doc.get("summary"):
        lines.append(f"요약: {doc['summary'][:200]}")

    financial = doc.get("financial", {})
    if financial.get("total_amount"):
        amount = financial["total_amount"]
        lines.append(f"금액: {amount:,.0f}원")

    lines.append("---")
    meta = doc.get("raw_metadata", {})
    if meta.get("filepath"):
        lines.append(f"원본: {meta['filepath']}")
    if doc.get("doc_id"):
        lines.append(f"문서ID: {doc['doc_id']}")

    return "\n".join(lines)


def add_alarms(event, priority, is_allday=False):
    """우선순위별 알림 추가"""
    if is_allday:
        days_list = ALLDAY_ALARM_PRESETS.get(priority, [0])
        for days in days_list:
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('description', 'Document Reminder')
            alarm.add('trigger', timedelta(days=days))
            event.add_component(alarm)
    else:
        deltas = ALARM_PRESETS.get(priority, [timedelta(days=-1)])
        for delta in deltas:
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('description', 'Document Reminder')
            alarm.add('trigger', delta)
            event.add_component(alarm)


def generate_ics(docs, output_path):
    """ICS 파일 생성"""
    cal = Calendar()
    cal.add('prodid', '-//DocAutomation//CalendarSync//KO')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('x-wr-calname', '문서 일정')

    stats = {"total": 0, "deadline": 0, "event": 0, "period": 0, "skipped": 0}
    events_created = []

    for doc in docs:
        # 에러 문서 스킵
        if doc.get("error"):
            stats["skipped"] += 1
            continue

        dates = doc.get("dates", {})
        priority = doc.get("priority", "하")
        title = create_event_title(doc)
        description = create_event_description(doc)
        has_date = False

        # 1. 마감일 이벤트 (종일)
        deadline = parse_date(dates.get("deadline"))
        if deadline:
            event = Event()
            event.add('summary', f"{title} - 마감")
            event.add('dtstart', deadline)
            event.add('dtend', deadline + timedelta(days=1))
            event.add('description', description)
            event.add('categories', [doc.get("doc_type", "기타")])
            event.add('priority', 1 if priority == "상" else 5 if priority == "중" else 9)
            add_alarms(event, priority, is_allday=True)
            cal.add_component(event)
            stats["deadline"] += 1
            has_date = True
            events_created.append(f"[마감] {title} ({deadline})")

        # 2. 행사/이벤트 날짜 (시간 이벤트)
        for event_date_str in dates.get("event_dates", []):
            event_date = parse_date(event_date_str)
            if event_date:
                event = Event()
                event.add('summary', title)
                event.add('dtstart', datetime.combine(event_date, datetime.min.time().replace(hour=10)))
                event.add('dtend', datetime.combine(event_date, datetime.min.time().replace(hour=12)))
                event.add('description', description)
                event.add('categories', [doc.get("doc_type", "기타")])
                add_alarms(event, priority, is_allday=False)
                cal.add_component(event)
                stats["event"] += 1
                has_date = True
                events_created.append(f"[행사] {title} ({event_date})")

        # 3. 기간 이벤트 (시작~종료)
        start = parse_date(dates.get("start_date"))
        end = parse_date(dates.get("end_date"))
        if start and end and start != end:
            event = Event()
            event.add('summary', f"{title} (기간)")
            event.add('dtstart', start)
            event.add('dtend', end + timedelta(days=1))
            event.add('description', description)
            event.add('categories', [doc.get("doc_type", "기타")])
            add_alarms(event, priority, is_allday=True)
            cal.add_component(event)
            stats["period"] += 1
            has_date = True
            events_created.append(f"[기간] {title} ({start} ~ {end})")

        if not has_date:
            stats["skipped"] += 1

    stats["total"] = stats["deadline"] + stats["event"] + stats["period"]

    # ICS 파일 저장
    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())

    return stats, events_created


def register_via_applescript(docs):
    """macOS에서 AppleScript로 직접 캘린더에 등록"""
    if platform.system() != "Darwin":
        return False, "macOS가 아닙니다."

    success_count = 0
    errors = []

    for doc in docs:
        dates = doc.get("dates", {})
        title = create_event_title(doc)
        description = create_event_description(doc).replace('"', '\\"').replace('\n', '\\n')

        deadline = dates.get("deadline")
        if not deadline:
            continue

        # AppleScript 생성
        script = f'''
        tell application "Calendar"
            if not (exists calendar "문서 일정") then
                make new calendar with properties {{name:"문서 일정"}}
            end if
            tell calendar "문서 일정"
                set eventDate to date "{deadline}"
                make new event with properties {{
                    summary:"{title} - 마감",
                    start date:eventDate,
                    allday event:true,
                    description:"{description}"
                }}
            end tell
        end tell
        '''

        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                success_count += 1
            else:
                errors.append(f"{title}: {result.stderr[:80]}")
        except Exception as e:
            errors.append(f"{title}: {str(e)[:80]}")

    return success_count > 0, f"성공 {success_count}개" + (f", 실패 {len(errors)}개" if errors else "")


def sync_to_calendar(input_path, output_path=None, method="ics"):
    """structured_results.json → 캘린더 등록"""

    with open(input_path, 'r', encoding='utf-8') as f:
        docs = json.load(f)

    print(f"📂 {len(docs)}개 문서 로드 완료")

    if output_path is None:
        output_path = os.path.join(os.path.dirname(input_path), "calendar_events.ics")

    # ICS 파일 생성 (항상)
    stats, events = generate_ics(docs, output_path)

    # macOS에서 AppleScript 직접 등록 시도
    if method == "applescript" and platform.system() == "Darwin":
        print("  🍎 AppleScript로 직접 등록 시도...")
        success, msg = register_via_applescript(docs)
        if success:
            print(f"  ✅ {msg}")
        else:
            print(f"  ⚠️ AppleScript 실패: {msg}")
            print(f"  📁 ICS 파일로 대체: {output_path}")
    else:
        print(f"  📁 ICS 파일 생성: {output_path}")

    # 등록된 이벤트 목록
    if events:
        print(f"\n  등록된 이벤트:")
        for ev in events[:20]:  # 최대 20개 표시
            print(f"    📌 {ev}")
        if len(events) > 20:
            print(f"    ... 외 {len(events) - 20}개")

    # 요약 보고
    print(f"\n📅 캘린더 등록 완료")
    print(f"  - 총 이벤트: {stats['total']}개 (마감일 {stats['deadline']}, 행사 {stats['event']}, 기간 {stats['period']})")
    print(f"  - 스킵: {stats['skipped']}개 (날짜 없음)")
    print(f"  - ICS 파일: {output_path}")
    if method != "applescript":
        print(f"  💡 Apple 캘린더에 추가: ICS 파일을 더블클릭하거나, 캘린더 앱 > 파일 > 가져오기")

    return stats


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python calendar_sync.py <structured_results.json 경로> [출력경로] [method]")
        print("  method: ics (기본) 또는 applescript (macOS)")
        print("예시: python calendar_sync.py ./structured_results.json ./events.ics ics")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    method = sys.argv[3] if len(sys.argv) > 3 else "ics"

    sync_to_calendar(input_file, output_file, method)
