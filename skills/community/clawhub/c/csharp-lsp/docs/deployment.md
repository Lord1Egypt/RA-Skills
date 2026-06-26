# Deployment Pipeline

## Overview

```
[개발]              [검증]              [배포]
skills/csharp-lsp   bash tests/test.sh  git tag + push
에서 수정           Docker 테스트        GitHub release
```

## Workflow

### 1. 개발

`skills/csharp-lsp/` 디렉토리가 곧 git working copy.
수정 사항은 여기서 직접 편집하고, 즉시 실사용 가능 (심볼릭 링크가 이 경로를 가리킴).

```bash
# 수정
vim scripts/lsp-query.py

# 로컬에서 바로 동작 확인
LSP_WORKSPACE=/path/to/project lsp-query hover file.cs 10 20
```

### 2. 배포 전 검증

Docker 클린 환경에서 자동 테스트:

```bash
bash tests/test.sh
```

검증 항목:
- 클린 환경 설치 (setup.sh)
- 기능 테스트 (hover, definition, references, symbols)
- 멱등성 (setup.sh 재실행)

### 3. 배포

```bash
# 버전 업데이트
# - SKILL.md의 version 필드
# - CHANGELOG.md에 변경 내역 추가

git add -A
git commit -m "feat: 변경 내용 설명"
git tag v1.2.0
git push origin main --tags
```

GitHub Actions CI가 push 시 자동으로 테스트를 실행합니다.

### 4. 배포본 전환

**별도 전환 작업이 필요 없습니다.**

`skills/csharp-lsp/` 자체가 git repo이므로, push한 시점의 코드가 곧 배포본입니다.
다른 사용자는 `git clone`으로 동일한 코드를 받습니다.

## Branch 전략 (선택)

현재는 `main` 단일 브랜치로 운영.
필요 시 `dev` 브랜치를 분리할 수 있습니다:

| 브랜치 | 용도 |
|--------|------|
| `main` | 검증 완료된 안정본 |
| `dev`  | 작업 중 수정사항 |

```bash
# dev에서 작업
git checkout dev
# ... 수정 ...
bash tests/test.sh  # 테스트

# main에 머지
git checkout main
git merge dev
git tag v1.2.0
git push origin main --tags

# 다시 dev로
git checkout dev
```

브랜치 전환만으로 실사용 버전이 변경됩니다 (심볼릭 링크 경로 불변).

## Version Numbering

[Semantic Versioning](https://semver.org/) 사용:

- **MAJOR**: 호환성 깨지는 변경 (LSP 프로토콜 변경, CLI 인터페이스 변경 등)
- **MINOR**: 기능 추가 (새 쿼리 타입, 새 언어 지원 등)
- **PATCH**: 버그 수정, 문서 수정

## CI (GitHub Actions)

`.github/workflows/test.yml`이 push/PR 시 자동 실행:

1. Docker 이미지 빌드 (`mcr.microsoft.com/dotnet/sdk:9.0` + Python3)
2. `setup.sh` 실행
3. 기능 테스트 (hover, definition, references, symbols)
4. 멱등성 테스트 (setup.sh 재실행)
