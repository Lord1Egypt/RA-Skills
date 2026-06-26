#!/usr/bin/env python3
"""
Google Tasks 연산 함수들
작업 (Task) 생성, 조회, 수정, 완료 처리 등
"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

# 권한 범위
SCOPES = ['https://www.googleapis.com/auth/tasks']

# 인증 파일 경로
CREDENTIALS_FILE = Path.home() / '.google-credentials.json'
TOKEN_FILE = Path.home() / '.google-tasks-token.pickle'


def authenticate():
    """
    OAuth 2.0 인증 수행 및 Credentials 반환
    """
    creds = None
    
    # 기존 토큰이 있으면 로드
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # 토큰이 없거나 만료되었으면 새로 인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"OAuth 클라이언트 키 파일이 없습니다.\n"
                    f"{CREDENTIALS_FILE} 파일을 준비해주세요."
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=8083)
        
        # 토큰 저장
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def get_tasks_service():
    """
    Google Tasks API 서비스 객체 반환
    """
    creds = authenticate()
    service = build('tasks', 'v1', credentials=creds)
    return service


def list_tasklists():
    """
    사용자의 모든 작업 목록 (Task Lists) 조회
    """
    service = get_tasks_service()
    
    result = service.tasklists().list(maxResults=100).execute()
    
    tasklists = result.get('items', [])
    return tasklists


def list_tasks(tasklist_id='@default'):
    """
    특정 작업 목록의 모든 작업 조회
    
    Args:
        tasklist_id: 작업 목록 ID (@default: 기본 목록 사용)
    
    Returns:
        작업 목록
    """
    service = get_tasks_service()
    
    result = service.tasks().list(tasklist=tasklist_id, showCompleted=False).execute()
    
    tasks = result.get('items', [])
    return tasks


def create_task(tasklist_id, title, notes='', due=None, parent=None):
    """
    새 작업 생성
    
    Args:
        tasklist_id: 작업 목록 ID
        title: 작업 제목
        notes: 메모/설명
        due: 마감일 (ISO 8601 형식, 예: '2026-04-20T10:00:00+09:00')
        parent: 부모 작업 ID (하위 작업일 경우)
    
    Returns:
        생성된 작업 객체
    """
    service = get_tasks_service()
    
    task = {
        'title': title,
        'notes': notes
    }
    
    if due:
        task['due'] = due
    
    if parent:
        task['parent'] = parent
    
    created_task = service.tasks().insert(
        tasklist=tasklist_id,
        body=task
    ).execute()
    
    return created_task


def update_task(tasklist_id, task_id, title=None, notes=None, due=None, status=None):
    """
    작업 수정
    
    Args:
        tasklist_id: 작업 목록 ID
        task_id: 작업 ID
        title: 새 제목 (선택)
        notes: 새 메모 (선택)
        due: 새 마감일 (선택)
        status: 새 상태 ('needsAction' 또는 'completed')
    
    Returns:
        수정된 작업 객체
    """
    service = get_tasks_service()
    
    # 기존 작업 가져오기
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    
    # 업데이트
    if title:
        task['title'] = title
    if notes is not None:
        task['notes'] = notes
    if due:
        task['due'] = due
    if status:
        task['status'] = status
    
    updated_task = service.tasks().update(
        tasklist=tasklist_id,
        task=task_id,
        body=task
    ).execute()
    
    return updated_task


def complete_task(tasklist_id, task_id):
    """
    작업 완료 처리
    
    Args:
        tasklist_id: 작업 목록 ID
        task_id: 작업 ID
    
    Returns:
        완료된 작업 객체
    """
    return update_task(tasklist_id, task_id, status='completed')


def delete_task(tasklist_id, task_id):
    """
    작업 삭제
    
    Args:
        tasklist_id: 작업 목록 ID
        task_id: 작업 ID
    """
    service = get_tasks_service()
    service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
    return True


def format_task(task, indent=0):
    """
    작업 포맷팅 (출력용, 하위 작업 포함)
    """
    prefix = '  ' * indent
    title = task.get('title', 'No title')
    status = '✅' if task.get('status') == 'completed' else '⬜'
    due = task.get('due', '')
    notes = task.get('notes', '')
    
    # 마감일 포맷팅
    if due:
        try:
            due = due.split('T')[0]  # 날짜 부분만 추출
        except:
            pass
    
    line = f"{prefix}{status} {title}"
    if due:
        line += f" 📅 {due}"
    
    lines = [line]
    
    if notes and indent < 2:
        lines.append(f"{prefix}   📝 {notes}")
    
    return '\n'.join(lines)


def main():
    """
    테스트용 메인 함수
    """
    print("✅ Google Tasks 테스트\n")
    
    try:
        # 작업 목록 목록
        print("=== 작업 목록 (Task Lists) ===")
        tasklists = list_tasklists()
        if tasklists:
            for tl in tasklists:
                print(f"  • {tl['title']} ({tl['id']})")
        else:
            print("  작업 목록이 없습니다.")
        
        # 기본 작업 목록의 작업들
        print("\n=== 기본 작업 목록의 작업 ===")
        tasks = list_tasks('@default')
        if tasks:
            for task in tasks:
                print(format_task(task))
        else:
            print("  할 일이 없습니다! 🎉")
        
        print("\n✅ 인증 및 연결 성공!")
        
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")


if __name__ == '__main__':
    main()
