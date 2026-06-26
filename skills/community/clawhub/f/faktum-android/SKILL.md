---
name: faktum-android
description: Faktum News Android 앱 개발 세션. Google 공식 Android CLI(`~/bin/android`) + 공식 Skills(android-cli, navigation-3, edge-to-edge)를 조합해 Kotlin + Jetpack Compose로 모바일 앱을 만든다. "안드로이드 앱 만들어", "팩툼 앱", "모바일 앱", "android 앱", "faktum 앱", "앱 만들자" 등 한국어 트리거로 발동. Faktum 웹(Next.js 16, 포트 3099)의 SQLite/FTS5 API를 백엔드로 재사용.
---

# Faktum Android App 개발

## 1. 필독 컨텍스트 (작업 시작 시 순서대로 Read)

1. `~/Documents/ntriq-vault/wiki/decisions/2026-04-19-android-cli-채택.md` — 도입 결정/스택
2. `~/Documents/ntriq-vault/wiki/tools/android-cli.md` — CLI 사용법·커맨드 레퍼런스
3. `~/Documents/ntriq-vault/wiki/decisions/2026-04-18-faktum-news-첫-사업-확정.md` — Faktum 사업 컨텍스트
4. `~/Documents/ntriq-vault/wiki/system/faktum-news-current-state.md` — 현재 웹 스택/DB/API 스냅샷
5. `~/.claude/projects/-Users-youareplan/memory/project-faktum-news.md` — 프로젝트 메모리 + 모바일 섹션

## 2. 공식 스킬 체이닝

이 스킬 발동 시 아래 공식 스킬도 함께 활용:
- `android-cli` — `android create`, `android run`, `android sdk install` 등 CLI 오케스트레이션
- `navigation-3` — Jetpack Navigation 3 (딥링크, 리스트-디테일 scene)
- `edge-to-edge` — Compose edge-to-edge 적용

## 3. 앱 스택 (확정)

| 계층 | 선택 |
|------|------|
| 언어 | Kotlin |
| UI | Jetpack Compose |
| 내비게이션 | Navigation 3 (리스트-디테일 scene) |
| 디스플레이 | edge-to-edge |
| 백엔드 | Faktum 웹 API 재사용 (http://localhost:3099 → 배포 시 도메인 교체) |
| DB | 서버측 SQLite/FTS5 그대로, 클라이언트는 Retrofit/Ktor |
| 디자인 | Ground News 스타일 다크 테마 (웹과 일관성 유지) |

## 4. 핵심 커맨드

```bash
# 프로젝트 생성 (위치는 대표님 결정 필요)
android create --help           # 옵션 먼저 확인
android create <project-path>

# SDK
android sdk install             # 필요 컴포넌트만
android info                    # 현재 환경

# 실행
android emulator                # 에뮬레이터
android run                     # 배포

# 문서/UI 지원
android docs <query>
android layout                  # 앱 UI 트리
android screen                  # 디바이스 화면

# 스킬 추가 (시점 도래 시)
android skills add --skill play-billing-library-version-upgrade  # 구독
android skills add --skill r8-analyzer                            # 크기 최적화
```

## 5. 작업 시작 워크플로우

1. 위 1번 필독 컨텍스트 5개 Read
2. 작업 분해 선언 (08-foundation, Stanford Pattern 1):
   - 출력, 성공 기준, 필요 정보, 단계 수
3. 프로젝트 경로 대표님께 확인 (모노레포 vs 별도 리포)
4. `android create` → `android skills add` 순서로 뼈대
5. Faktum 웹 API 계약 Read (`~/Documents/Projects/faktum-news/app/api/`)
6. Compose 화면 구현 → `android run`으로 에뮬레이터 검증

## 6. 모든 AI 공유 확인

이 스킬은 Claude Code 전용이지만, 공식 Android CLI 스킬(`android-cli`/`navigation-3`/`edge-to-edge`)은 **8개 AI 디렉토리** (`.claude` `.codex` `.cursor` `.gemini` `.copilot` `.continue` `.agents` `.openclaw`)에 자동 배포됨. Cursor/Codex/Gemini가 앱 코드 만질 때도 동일한 SKILL.md를 참조.

Obsidian vault(`~/Documents/ntriq-vault/`)는 5분 sync로 3개 시스템 공유 뇌 역할. 다른 AI도 vault의 `wiki/tools/android-cli.md`와 `wiki/decisions/2026-04-19-android-cli-채택.md`를 읽으면 동일 컨텍스트 획득.

## 7. 주의

- Google 공식 스킬(`android-cli` 등)은 `android skills add`로 업데이트됨 → 수정 금지. 우리 보강사항은 **이 래퍼 스킬에만** 기록.
- CLI는 preview(v0.7). 브레이킹 체인지 가능. `android update` 정기 실행.
- Faktum 웹이 Next.js 16 (학습 데이터와 다름) → API 연동 시 웹 소스 Read 필수.
