#!/usr/bin/env python3
"""
Google Calendar 연산 함수들
일정 조회, 생성, 수정, 삭제 등
"""

from datetime import datetime, timedelta
from oauth_setup import get_calendar_service, list_calendars


def list_events(calendar_id='primary', date_from=None, date_to=None, max_results=10):
    """
    일정 목록 조회
    
    Args:
        calendar_id: 캘린더 ID (기본: 'primary')
        date_from: 시작 날짜 (YYYY-MM-DD 형식 또는 datetime 객체)
        date_to: 종료 날짜 (YYYY-MM-DD 형식 또는 datetime 객체)
        max_results: 최대 결과 수
    
    Returns:
        일정 목록
    """
    service = get_calendar_service()
    
    # 날짜 처리
    if date_from:
        if isinstance(date_from, str):
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
        time_min = date_from.isoformat() + 'Z'
    else:
        time_min = datetime.utcnow().isoformat() + 'Z'
    
    if date_to:
        if isinstance(date_to, str):
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
        time_max = date_to.isoformat() + 'Z'
    else:
        time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
    
    # API 호출
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    return events


def create_event(summary, start_time, end_time, description='', location='', attendees=None, calendar_id='primary'):
    """
    새 일정 생성
    
    Args:
        summary: 일정 제목
        start_time: 시작 시간 (datetime 객체 또는 'YYYY-MM-DDTHH:MM:SS' 형식)
        end_time: 종료 시간 (datetime 객체 또는 'YYYY-MM-DDTHH:MM:SS' 형식)
        description: 설명
        location: 위치
        attendees: 참석자 이메일 목록 (예: ['user@example.com'])
    
    Returns:
        생성된 일정 객체
    """
    service = get_calendar_service()
    
    # 시간 처리
    if isinstance(start_time, datetime):
        start_time = start_time.isoformat()
    if isinstance(end_time, datetime):
        end_time = end_time.isoformat()
    
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Seoul'
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Seoul'
        },
        'description': description,
        'location': location
    }
    
    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]
    
    created_event = service.events().insert(
        calendarId=calendar_id,
        body=event
    ).execute()
    
    return created_event


def update_event(event_id, summary=None, start_time=None, end_time=None, 
                 description=None, location=None, calendar_id=None):
    """
    일정 수정
    
    Args:
        event_id: 수정할 일정 ID
        summary: 새 제목 (선택)
        start_time: 새 시작 시간 (선택)
        end_time: 새 종료 시간 (선택)
        description: 새 설명 (선택)
        location: 새 위치 (선택)
        calendar_id: 이동할 캘린더 ID (선택 - 이동시 필요)
    
    Returns:
        수정된 일정 객체
    """
    service = get_calendar_service()
    
    # 실제 이벤트 ID (recurring event 인 경우 _ 날짜 부분 제거)
    base_event_id = event_id.split('_')[0] if '_' in event_id else event_id
    
    # 기존 일정 가져오기 (기본 캘린더에서)
    event = service.events().get(
        calendarId='primary',
        eventId=base_event_id
    ).execute()
    
    # 업데이트
    if summary:
        event['summary'] = summary
    if start_time:
        if isinstance(start_time, datetime):
            start_time = start_time.isoformat()
        event['start'] = {'dateTime': start_time, 'timeZone': 'Asia/Seoul'}
    if end_time:
        if isinstance(end_time, datetime):
            end_time = end_time.isoformat()
        event['end'] = {'dateTime': end_time, 'timeZone': 'Asia/Seoul'}
    if description is not None:
        event['description'] = description
    if location is not None:
        event['location'] = location
    
    # 캘린더 이동시: 원본에서 삭제하고 새 캘린더에 생성
    if calendar_id and calendar_id != 'primary':
        # 반복 일정 인스턴스면 ID 관련 필드 제거하고 새로 생성 (충돌 방지)
        if 'id' in event:
            del event['id']
        if 'iCalUID' in event:
            del event['iCalUID']
        if 'sequence' in event:
            del event['sequence']
        
        # 새 캘린더에 생성
        new_event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        
        # 원본 삭제 (base_event_id 사용)
        try:
            service.events().delete(
                calendarId='primary',
                eventId=base_event_id
            ).execute()
        except:
            pass  # 이미 삭제되었거나 단일 인스턴스일 수 있음
        
        return new_event
    else:
        updated_event = service.events().update(
            calendarId='primary',
            eventId=base_event_id,
            body=event
        ).execute()
        
        return updated_event


def delete_event(event_id):
    """
    일정 삭제
    
    Args:
        event_id: 삭제할 일정 ID
    """
    service = get_calendar_service()
    service.events().delete(
        calendarId='primary',
        eventId=event_id
    ).execute()
    return True


def format_event(event):
    """
    일정 포맷팅 (출력용)
    """
    summary = event.get('summary', 'No title')
    start = event['start'].get('dateTime', event['start'].get('date', 'Unknown'))
    end = event['end'].get('dateTime', event['end'].get('date', 'Unknown'))
    location = event.get('location', '')
    
    # 시간 포맷팅
    try:
        if 'T' in start:
            start = datetime.fromisoformat(start.replace('Z', '+00:00'))
            start = start.strftime('%m/%d %H:%M')
        if 'T' in end:
            end = datetime.fromisoformat(end.replace('Z', '+00:00'))
            end = end.strftime('%m/%d %H:%M')
    except:
        pass
    
    return f"  • {summary} | {start} - {end} {'📍 ' + location if location else ''}"


def main():
    """
    테스트용 메인 함수
    """
    print("📅 Google Calendar 테스트\n")
    
    # 캘린더 목록
    print("=== 캘린더 목록 ===")
    calendars = list_calendars()
    for cal in calendars[:3]:  # 상위 3 개만
        print(f"  • {cal['summary']}")
    
    # 일정 목록
    print("\n=== 향후 7 일 일정 ===")
    events = list_events(max_results=5)
    if events:
        for event in events:
            print(format_event(event))
    else:
        print("  예정된 일정이 없습니다.")
    
    # 새 일정 생성 테스트
    # create_event(
    #     summary="테스트 회의",
    #     start_time=(datetime.now() + timedelta(days=1)).isoformat(),
    #     end_time=(datetime.now() + timedelta(days=1, hours=1)).isoformat(),
    #     description="테스트용 일정입니다",
    #     location="Zoom"
    # )
    # print("\n✅ 새 일정 생성 완료!")


if __name__ == '__main__':
    main()
