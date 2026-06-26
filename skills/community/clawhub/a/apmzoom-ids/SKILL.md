---
name: APM 인증 센터 API
description: "APM 플랫폼의 인증 센터 API 모음. 계정/이메일/휴대폰 기반 로그인, 관리자/공급업체/사용자 로그인, 토큰 갱신, 인증 코드 발송, 토큰 검증 등 19개 엔드포인트를 포함합니다. 요청 헤더(v/p/t/lang), MD5 서명 규칙, authcode 헤더(HH + access_token) 사용법을 문서화. Base URL: https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com"
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - APM_USER_TOKEN
    primaryEnv: APM_USER_TOKEN
    homepage: https://github.com/apmzoom-ai/apm-skills
---

# APM 인증 센터 API

APM 플랫폼의 인증 센터 API 모음. 계정/이메일/휴대폰 기반 로그인, 관리자/공급업체/사용자 로그인, 토큰 갱신, 인증 코드 발송, 토큰 검증 등 19개 엔드포인트를 포함합니다. 요청 헤더(v/p/t/lang), MD5 서명 규칙, authcode 헤더(HH + access_token) 사용법을 문서화. Base URL: https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com

## 공통 규약

- **Base URL**: `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com`
- **요청 헤더**: `v=7.0.1`, `p=1`, `t=<unix초>`, `lang=zh-cn`
- **인증 헤더**: `authcode: "HH " + access_token` (로그인 계열 제외)
- **서명**: `sign = MD5(<params> + <salt>).toUpperCase()` — 엔드포인트별 salt는 각 문서 참조
- **성공 코드**: `code=100`, 결과는 `result` 필드
- **페이지네이션**: `last_update_time` 커서 방식, `page_size=20`

## 엔드포인트 목록 (19개)

- [`ids_admin_app_tool_login`](ids_admin_app_tool_login.md) — **관리자 APP 도구 로그인** · `POST /ids/admin_app_tool_login`
- [`ids_admin_desk_tool_login`](ids_admin_desk_tool_login.md) — **관리자 데스크탑 도구 로그인** · `POST /ids/admin_desk_tool_login`
- [`ids_admin_login`](ids_admin_login.md) — **관리자 로그인** · `POST /ids/admin_login`
- [`ids_captcha_img`](ids_captcha_img.md) — **인증 코드 이미지 획득** · `GET /ids/captcha_img`
- [`ids_m_login_account`](ids_m_login_account.md) — **판매자 로그인-계정/비밀번호** · `POST /ids/m_login_account`
- [`ids_m_login_email`](ids_m_login_email.md) — **판매자 로그인-이메일 인증 코드** · `POST /ids/m_login_email`
- [`ids_m_login_tel`](ids_m_login_tel.md) — **판매자 로그인-휴대폰 번호 인증 코드** · `POST /ids/m_login_tel`
- [`ids_refresh_token`](ids_refresh_token.md) — **access_token 갱신** · `POST /ids/refresh_token`
- [`ids_send_email_code`](ids_send_email_code.md) — **이메일 인증 코드 발송** · `POST /ids/send_email_code`
- [`ids_send_email_code_r`](ids_send_email_code_r.md) — **이메일 인증 코드 발송(회원가입)** · `POST /ids/send_email_code_r`
- [`ids_send_tel_code`](ids_send_tel_code.md) — **SMS 인증 코드 발송** · `POST /ids/send_tel_code`
- [`ids_send_tel_code_r`](ids_send_tel_code_r.md) — **SMS 인증 코드 발송(회원가입)** · `POST /ids/send_tel_code_r`
- [`ids_suppliers_login`](ids_suppliers_login.md) — **공급업체 로그인** · `POST /ids/suppliers_login`
- [`ids_u_login_account`](ids_u_login_account.md) — **사용자 로그인-계정/비밀번호** · `POST /ids/u_login_account`
- [`ids_u_login_email`](ids_u_login_email.md) — **사용자 로그인-이메일 인증 코드** · `POST /ids/u_login_email`
- [`ids_u_login_tel`](ids_u_login_tel.md) — **사용자 로그인-휴대폰 번호 인증 코드** · `POST /ids/u_login_tel`
- [`ids_u_login_to_ce`](ids_u_login_to_ce.md) — **사용자 로그인-계정/비밀번호(CE)** · `POST /ids/u_login_to_ce`
- [`ids_verfy_t`](ids_verfy_t.md) — **Token 검증** · `POST /ids/verfy_t`
- [`ids_verfy_ttoken`](ids_verfy_ttoken.md) — **Token 검증** · `POST /ids/verfy_ttoken`

## 사용법

1. 필요한 엔드포인트 문서를 확인 (파일명 = 엔드포인트 이름)
2. `ids_*_login_*` 중 하나로 `access_token` 획득 (APM_USER_TOKEN 환경변수에 저장)
3. 요청 헤더에 `authcode: "HH " + $APM_USER_TOKEN` 추가
4. 해당 문서의 서명 규칙에 따라 `sign` 계산 후 호출

원본 문서: https://github.com/apmzoom-ai/apm-skills
