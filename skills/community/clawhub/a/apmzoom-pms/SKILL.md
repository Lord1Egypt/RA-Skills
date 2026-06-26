---
name: APM 메시지 푸시 API
description: "APM 플랫폼의 메시지 푸시 서비스 API 모음. 헬스 체크, 관리자/사용자 푸시 메시지 목록·상세·읽음 상태 업데이트, 커스텀 정보 업로드 등 8개 엔드포인트를 포함. authcode 헤더(HH + access_token)로 호출. 서비스명: ApmZoomPushMessageService."
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - APM_USER_TOKEN
    primaryEnv: APM_USER_TOKEN
    homepage: https://github.com/apmzoom-ai/apm-skills
---

# APM 메시지 푸시 API

APM 플랫폼의 메시지 푸시 서비스 API 모음. 헬스 체크, 관리자/사용자 푸시 메시지 목록·상세·읽음 상태 업데이트, 커스텀 정보 업로드 등 8개 엔드포인트를 포함. authcode 헤더(HH + access_token)로 호출. 서비스명: ApmZoomPushMessageService.

## 공통 규약

- **Base URL**: `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com`
- **요청 헤더**: `v=7.0.1`, `p=1`, `t=<unix초>`, `lang=zh-cn`
- **인증 헤더**: `authcode: "HH " + access_token` (로그인 계열 제외)
- **서명**: `sign = MD5(<params> + <salt>).toUpperCase()` — 엔드포인트별 salt는 각 문서 참조
- **성공 코드**: `code=100`, 결과는 `result` 필드
- **페이지네이션**: `last_update_time` 커서 방식, `page_size=20`

## 엔드포인트 목록 (8개)

- [`pms_health`](pms_health.md) — **메시지 푸시 서비스 헬스 체크** · `GET /pms/health`
- [`pms_m_editpushmsgreadstatus`](pms_m_editpushmsgreadstatus.md) — **메시지를 읽음으로 변경[판매자]** · `POST /pms/app/m_editpushmsgreadstatus`
- [`pms_m_pushmsginfo`](pms_m_pushmsginfo.md) — **홈 공지 정보 조회[판매자]** · `GET /pms/app/m_pushmsginfo`
- [`pms_m_pushmsglist`](pms_m_pushmsglist.md) — **공지 목록 조회[판매자]** · `GET /pms/app/m_pushmsglist`
- [`pms_u_editpushmsgreadstatus`](pms_u_editpushmsgreadstatus.md) — **메시지를 읽음으로 변경[사용자]** · `POST /pms/app/u_editpushmsgreadstatus`
- [`pms_u_pushmsginfo`](pms_u_pushmsginfo.md) — **홈 공지 정보 조회[사용자]** · `GET /pms/app/u_pushmsginfo`
- [`pms_u_pushmsglist`](pms_u_pushmsglist.md) — **공지 목록 조회[사용자]** · `GET /pms/app/u_pushmsglist`
- [`pms_uploadcustominfo`](pms_uploadcustominfo.md) — **커스텀 정보 업로드** · `POST /pms/app/uploadcustominfo`

## 사용법

1. 필요한 엔드포인트 문서를 확인 (파일명 = 엔드포인트 이름)
2. `ids_*_login_*` 중 하나로 `access_token` 획득 (APM_USER_TOKEN 환경변수에 저장)
3. 요청 헤더에 `authcode: "HH " + $APM_USER_TOKEN` 추가
4. 해당 문서의 서명 규칙에 따라 `sign` 계산 후 호출

원본 문서: https://github.com/apmzoom-ai/apm-skills
