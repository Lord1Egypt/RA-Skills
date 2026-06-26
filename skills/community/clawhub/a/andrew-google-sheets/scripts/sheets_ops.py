#!/usr/bin/env python3
"""
Google Sheets 연산 함수들
스프레드시트 읽기, 쓰기, 생성, 수정 등
"""

from datetime import datetime
from oauth_setup import get_sheets_service, get_drive_service, list_spreadsheets


def read_range(spreadsheet_id, range_name):
    """
    스프레드시트의 특정 범위 읽기
    
    Args:
        spreadsheet_id: 스프레드시트 ID
        range_name: 범위 명 (예: 'Sheet1!A1:D10')
    
    Returns:
        2 차원 데이터 목록
    """
    service = get_sheets_service()
    
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    
    values = result.get('values', [])
    return values


def write_range(spreadsheet_id, range_name, values, value_input_option='USER_ENTERED'):
    """
    스프레드시트의 특정 범위 쓰기
    
    Args:
        spreadsheet_id: 스프레드시트 ID
        range_name: 범위 명 (예: 'Sheet1!A1:D1')
        values: 쓸 데이터 (2 차원 목록)
        value_input_option: 값 입력 옵션 (RAW 또는 USER_ENTERED)
    
    Returns:
        업데이트된 정보
    """
    service = get_sheets_service()
    
    body = {
        'values': values
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input_option,
        body=body
    ).execute()
    
    return result


def append_rows(spreadsheet_id, range_name, values, value_input_option='USER_ENTERED'):
    """
    스프레드시트에 행 추가
    
    Args:
        spreadsheet_id: 스프레드시트 ID
        range_name: 범위 명 (예: 'Sheet1!A:D')
        values: 추가할 데이터 (2 차원 목록)
        value_input_option: 값 입력 옵션
    
    Returns:
        추가된 정보
    """
    service = get_sheets_service()
    
    body = {
        'values': values
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input_option,
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    
    return result


def batch_read(spreadsheet_id, ranges):
    """
    여러 범위 한 번에 읽기
    
    Args:
        spreadsheet_id: 스프레드시트 ID
        ranges: 범위 목록 (예: ['Sheet1!A1:D10', 'Sheet2!A1:C5'])
    
    Returns:
        각 범위의 데이터 딕셔너리
    """
    service = get_sheets_service()
    
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=ranges
    ).execute()
    
    value_ranges = result.get('valueRanges', [])
    return value_ranges


def batch_write(spreadsheet_id, value_ranges, value_input_option='USER_ENTERED'):
    """
    여러 범위 한 번에 쓰기
    
    Args:
        spreadsheet_id: 스프레드시트 ID
        value_ranges: [{'range': 'Sheet1!A1:B2', 'values': [...]}, ...]
        value_input_option: 값 입력 옵션
    
    Returns:
        업데이트된 정보
    """
    service = get_sheets_service()
    
    body = {
        'valueInputOption': value_input_option,
        'data': value_ranges
    }
    
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    
    return result


def create_spreadsheet(title, sheet_title='Sheet1'):
    """
    새 스프레드시트 생성
    
    Args:
        title: 스프레드시트 제목
        sheet_title: 초기 시트 제목
    
    Returns:
        생성된 스프레드시트 정보
    """
    service = get_sheets_service()
    
    spreadsheet = {
        'properties': {
            'title': title
        },
        'sheets': [
            {
                'properties': {
                    'title': sheet_title
                }
            }
        ]
    }
    
    result = service.spreadsheets().create(
        body=spreadsheet
    ).execute()
    
    return result


def get_spreadsheet_info(spreadsheet_id):
    """
    스프레드시트 메타데이터 조회
    
    Args:
        spreadsheet_id: 스프레드시트 ID
    
    Returns:
        스프레드시트 정보
    """
    service = get_sheets_service()
    
    result = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id
    ).execute()
    
    return result


def clear_range(spreadsheet_id, range_name):
    """
    특정 범위 내용 지우기
    
    Args:
        spreadsheet_id: 스프레드시트 ID
        range_name: 범위 명
    """
    service = get_sheets_service()
    
    result = service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    
    return result


def find_spreadsheet_by_name(name):
    """
    이름으로 스프레드시트 찾기
    
    Args:
        name: 스프레드시트 이름 (일부 일치)
    
    Returns:
        일치하는 스프레드시트 목록
    """
    spreadsheets = list_spreadsheets()
    matches = []
    
    for sheet in spreadsheets:
        if name.lower() in sheet.get('name', '').lower():
            matches.append(sheet)
    
    return matches


def format_row(row_data, headers):
    """
    딕셔너리 데이터를 행 데이터로 변환
    
    Args:
        row_data: {'header1': 'value1', 'header2': 'value2'}
        headers: ['header1', 'header2', ...]
    
    Returns:
        ['value1', 'value2', ...]
    """
    return [row_data.get(h, '') for h in headers]


def main():
    """
    테스트용 메인 함수
    """
    print("📊 Google Sheets 테스트\n")
    
    # 스프레드시트 목록
    print("=== 스프레드시트 목록 ===")
    spreadsheets = list_spreadsheets()
    if spreadsheets:
        for sheet in spreadsheets[:5]:  # 상위 5 개만
            print(f"  • {sheet['name']}")
            print(f"    ID: {sheet['id']}")
    else:
        print("  스프레드시트가 없습니다.")
    
    # 특정 스프레드시트 읽기 테스트
    # if spreadsheets:
    #     test_id = spreadsheets[0]['id']
    #     print(f"\n=== 첫 번째 스프레드시트 데이터 ===")
    #     data = read_range(test_id, 'Sheet1!A1:D10')
    #     for row in data:
    #         print(row)
    
    # 새 스프레드시트 생성 테스트
    # new_sheet = create_spreadsheet('테스트 스프레드시트')
    # print(f"\n✅ 새 스프레드시트 생성 완료: {new_sheet['spreadsheetId']}")


if __name__ == '__main__':
    main()
