#!/usr/bin/env python3
"""
OAuth 2.0 인증 설정 및 토큰 관리
Google Calendar API 접근을 위한 인증 처리
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 권한 범위 (Calendar 읽기/쓰기)
SCOPES = ['https://www.googleapis.com/auth/calendar']

# 토큰 저장 경로
TOKEN_FILE = Path.home() / '.google-calendar-token.pickle'
CREDENTIALS_FILE = Path.home() / '.google-credentials.json'


def authenticate():
    """
    OAuth 2.0 인증 수행 및 Credentials 반환
    처음 실행시 브라우저에서 로그인 진행
    """
    creds = None
    
    # 기존 토큰이 있으면 로드
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # 토큰이 없거나 만료되었으면 새로 인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 리프레시
            creds.refresh(Request())
        else:
            # OAuth 클라이언트 키가 있어야 함
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"OAuth 클라이언트 키 파일이 없습니다.\n"
                    f"Google Cloud Console 에서 다운로드한 client_secret_*.json 파일을\n"
                    f"{CREDENTIALS_FILE} 로 복사해주세요."
                )
            
            # OAuth 흐름 시작
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=8080)
        
        # 토큰 저장
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def get_calendar_service():
    """
    Google Calendar API 서비스 객체 반환
    """
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)
    return service


def list_calendars():
    """
    사용자의 모든 캘린더 목록 조회
    """
    service = get_calendar_service()
    calendar_list = service.calendarList()
    result = calendar_list.list(maxResults=25).execute()
    
    calendars = result.get('items', [])
    return calendars


def main():
    """
    인증 테스트 및 캘린더 목록 출력
    """
    try:
        print("🔐 인증 중...")
        calendars = list_calendars()
        
        print(f"\n✅ 총 {len(calendars)} 개의 캘린더가 있습니다:\n")
        for cal in calendars:
            summary = cal.get('summary', 'Unknown')
            access_role = cal.get('accessRole', 'unknown')
            primary = " (기본)" if cal.get('primary') else ""
            print(f"  • {summary}{primary} [{access_role}]")
        
        print("\n✅ 인증 성공!")
        
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\n설정 방법:")
        print("1. Google Cloud Console 에서 OAuth 클라이언트 키 다운로드")
        print("2. 파일을 ~/.google-calendar-credentials.json 으로 복사")
        print("3. 다시 실행")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")


if __name__ == '__main__':
    main()
