# Blog Format Reference

## 디렉토리 구조

```text
dev-blog/
├── src/
│   ├── assets/                    # 콘텐츠 이미지 (webp 권장)
│   │   └── {slug}-{timestamp}.webp
│   └── content/
│       └── blog/
│           ├── ko/
│           │   └── {slug}.mdoc
│           └── en/
│               └── {slug}.mdoc
```

## Frontmatter 스키마 (현재 기준)

```yaml
---
draft: false
featured: false          # optional
external: false          # optional
title: "제목"            # required
description: "설명"       # required 권장
date: 2026-01-29         # required (YYYY-MM-DD)
tldr:                    # optional (권장)
  - 핵심 요약 1
  - 핵심 요약 2
faq:                     # optional (SEO/GEO용, 2개 이상 권장)
  - q: 질문 1
    a: 답변 1
  - q: 질문 2
    a: 답변 2
cover: ../../../assets/{파일명}.webp  # required 권장
coverAlt: "Cover"        # optional
tags:
  - Tag1
  - Tag2
category: Tech           # optional
modifiedDate: 2026-01-30 # optional
---
```

## TL;DR 규칙

- TL;DR는 **frontmatter `tldr`만 사용**
- 본문에 `## TL;DR` 섹션 작성 금지
- 권장: 2줄, 짧고 행동/판단 중심 문장

## FAQ 규칙

- `faq`는 화면용 섹션이 아니라 **JSON-LD (FAQPage) 생성용**
- Q/A 2개 이상일 때만 넣는 것을 권장
- 과장 없는 사실 기반 답변 사용

예시:
```yaml
faq:
  - q: 이 글은 누구에게 유용한가요?
    a: 관련 도구를 실무에 적용하려는 개발자에게 유용합니다.
  - q: 읽고 나면 무엇을 할 수 있나요?
    a: 도입 여부를 판단할 기준과 초기 적용 순서를 잡을 수 있습니다.
```

## 에셋 네이밍 컨벤션

패턴:
- `{slug}-{YYYYMMDDHHmmssSSS}.webp`
- 영어 전용 이미지 필요 시: `{slug}-en-{YYYYMMDDHHmmssSSS}.webp`

예시:
- `obsidian-zettelkasten-with-para-20260129152500000.webp`
- `obsidian-zettelkasten-with-para-en-20260129160300001.webp`

## 인라인 이미지

Markdoc 삽입:
```markdown
![](../../../assets/{파일명}.webp)
```

권장:
- 섹션 핵심 설명 직후 배치
- 한 섹션에 이미지 과다 삽입 금지
- 이미지 내 텍스트는 가능하면 영어 사용

## 태그 가이드

자주 쓰는 태그:
- `AI`, `Tech`, `Dev`, `Books`, `Life`, `Security`, `Tools`

규칙:
- 2~5개 권장
- ko/en 페어는 동일 태그 유지

## 다국어(ko/en) 규칙

- 같은 주제면 `slug` 동일
- frontmatter 구조 동일
- `tldr`, `faq`도 의미상 페어 정렬
- 내부 링크는 동일 언어 경로로 치환

## 배포 전 확인 포인트

- [ ] `tldr` 존재 (권장)
- [ ] 본문 `## TL;DR` 없음
- [ ] `faq` 형식 유효 (`q`, `a`)
- [ ] cover 경로 정상
- [ ] 이미지 파일 존재
- [ ] ko/en 페어 정합성
- [ ] preview에서 ko/en 둘 다 확인
