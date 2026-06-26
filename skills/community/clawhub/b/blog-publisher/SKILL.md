---
name: blog-publisher
description: "Obsidian 노트나 텍스트를 dev-blog에 발행. Markdown → .mdoc 변환, 이미지 프롬프트 제공, 사용자가 직접 생성한 이미지 후처리, preview 배포 승인 후 main 배포까지 처리."
---

# Blog Publisher

Obsidian 노트 또는 텍스트를 dev-blog에 발행하는 워크플로우.

**이미지 생성 정책:** 사용자가 직접 이미지를 생성하고 전송하면, 에이전트는 후처리(crop, webp 변환) 및 배포를 담당합니다.

## 전제 조건

- dev-blog repo: `~/projects/dev-blog`  
  - 없으면 clone: `git@github.com:sonim1/dev-blog.git`
- `cwebp` 설치 (`brew install webp`) - 이미지 후처리용
- Git user 설정:
  - `Kendrick B Jung <bumfoo@gmail.com>`

## 이미지 생성 정책 (중요)

**우선순위: `chatgpt-image-gen` 스킬 → 사용자 직접 생성**

### 1순위: chatgpt-image-gen 스킬 시도

에이전트가 먼저 `chatgpt-image-gen` 스킬을 사용해 이미지 생성을 시도합니다.

**조건:**
- Chrome 확장프로그램(OpenClaw Browser Relay)이 설치되어 있어야 함
- ChatGPT 탭이 attach 되어 있어야 함 (`openclaw browser tabs --profile=chrome`으로 확인)

**성공 시:**
- 바로 이미지 생성 후 후처리(crop, webp 변환) 진행

**실패 시:**
- Chrome 확장프로그램 미설치/미연결 → 사용자에게 안내
- 기타 오류 → 사용자에게 알림 후 수동 생성 요청

### 2순위: 사용자 직접 생성

`chatgpt-image-gen` 실패 시 사용자가 직접 생성:

- 사용자가 이미지 생성 도구(Gemini, DALL-E, Midjourney 등) 사용
- 생성된 이미지를 Telegram으로 전송
- 에이전트가 후처리(crop, webp 변환) 및 배포

### 사용자 안내 메시지 (스킬 실패 시)

```
⚠️ ChatGPT 이미지 자동 생성을 시도했으나 Chrome 확장프로그램이 연결되지 않았습니다.

**해결 방법:**
1. Chrome에서 ChatGPT (chat.openai.com) 탭 열기
2. OpenClaw Browser Relay 확장프로그램 아이콘 클릭
3. 배지가 ON으로 바뀌면 완료

**또는 직접 생성:**
위 프롬프트로 직접 이미지 생성 후 Telegram으로 전송해주세요.
```

## Vercel 정보

- 프로젝트: `it-blog`
- 팀: `bumfoo-s-team`
- Preview 브랜치: `preview`
  - `https://it-blog-git-preview-bumfoo-s-team.vercel.app`
- Production: `main`
  - `https://sonim1.com`

## 핵심 작성 규칙 (중요)

1. `tldr`는 반드시 frontmatter에 작성한다.
- 본문에 `## TL;DR` 섹션을 만들지 않는다.

2. `faq`는 선택 필드다.
- 2개 이상 입력 시 FAQPage JSON-LD로 출력된다.
- UI에 직접 보이는 섹션이 아니라 SEO/GEO용 구조화 데이터다.

3. ko/en 페어 글은 `slug`, 태그, 구조를 최대한 맞춘다.

4. 이미지 경로는 현재 기준 `src/assets` 상대 경로를 사용한다.
- 예: `../../../assets/{slug}-{timestamp}.webp`

5. Related Posts는 임베딩 기반이다.
- 로컬에서 `DATABASE_URL`, `OPENAI_API_KEY`가 없으면 related가 안 보일 수 있음.
- 상용 env에서는 정상 동작.

## 워크플로우

### 1) 소스 가져오기

Obsidian 기준:
- 볼트: `~/Library/Mobile Documents/com~apple~CloudDocs/_Obsidian/_Personal/Personal/`
- 초안: `Projects/블로그 - *.md` 또는 `Inbox/*.md`

### 2) `.mdoc` 변환 및 Frontmatter 작성

파일:
- ko: `src/content/blog/ko/{slug}.mdoc`
- en: `src/content/blog/en/{slug}.mdoc`

권장 기본 템플릿:

```yaml
---
draft: false
title: "제목"
description: "설명 (SEO용 1~2문장)"
date: YYYY-MM-DD
tldr:
  - 핵심 요약 1
  - 핵심 요약 2
faq:
  - q: 질문 1
    a: 답변 1
  - q: 질문 2
    a: 답변 2
cover: ../../../assets/{slug}-{YYYYMMDDHHmmssSSS}.webp
tags:
  - Tag1
  - Tag2
---
```

### 3) 이미지 스타일/배치 제안 + 자동 생성 시도

**단계 A: 프롬프트 작성 및 자동 생성 시도**

1. 이미지 스타일/배치 제안 작성
2. 상세한 영문 프롬프트 작성
3. `chatgpt-image-gen` 스킬로 자동 생성 시도

**단계 B: 자동 생성 결과 처리**

- **성공**: 생성된 이미지 후처리로 바로 진행
- **실패**: 사용자에게 안내 후 수동 생성 요청

**보고 포맷:**
```md
### 🎨 이미지 스타일 제안
1. 스타일 A: 설명
2. 스타일 B: 설명
3. 스타일 C: 설명

### 📍 이미지 배치 계획
- **커버 이미지**: [설명]
- **인라인 이미지 1**: [설명]
- **인라인 이미지 2**: [설명] (필요시)

### 📝 이미지 생성용 프롬프트

#### 커버 이미지
```
[상세한 영문 프롬프트]
- 해상도: 1408x768 (16:9)
- 스타일: [flat design / 3D / etc]
- 색상: [color palette]
```

#### 인라인 이미지 1
```
[상세한 영문 프롬프트]
- 해상도: 1024x768 또는 1200x800
- 스타일: [설명]
```

### 🤖 자동 생성 실행

프롬프트 준비 후 `chatgpt-image-gen` 스킬 사용:

```
ChatGPT 이미지 생성 스킬로 커버 이미지 생성 시도
- 스킬: chatgpt-image-gen
- 탭 확인: browser tabs --profile=chrome
- 동작: ChatGPT 탭에서 새 채팅 → 프롬프트 입력 → 생성 → 다운로드
```

**성공**: 후처리로 바로 진행  
**실패**: 위 사용자 안내 메시지 출력 후 수동 생성 요청
```

### 4) 이미지 수신 + 후처리

**자동 생성 성공 시:**
- 생성된 이미지 바로 후처리 (crop, webp 변환)
- 사용자 확인 후 진행

**자동 생성 실패 → 수동 생성 시:**
- 사용자가 생성한 이미지를 Telegram으로 전송
- 이미지 확인 및 후처리 (crop, resize, webp 변환)
- 승인 후 진행

**절차:**
1. 이미지 수신 (자동 또는 Telegram)
2. 필요시 후처리
3. webp 변환
4. 사용자 승인 후 배포 진행

### 5) 이미지 후처리 + webp 변환

- AI 생성 이미지는 필요 시 공백 crop
- 스크린샷은 본문 가독성 맞춰 리사이즈
- webp 변환:
```bash
cwebp -q 80 input.png -o "src/assets/{slug}-{timestamp}.webp"
```

네이밍:
- `{slug}-{YYYYMMDDHHmmssSSS}.webp`
- en 별도 이미지 필요 시: `{slug}-en-{YYYYMMDDHHmmssSSS}.webp`

### 6) 영어 버전 생성

- 파일: `src/content/blog/en/{slug}.mdoc`
- ko 내용 자연 번역
- 내부 링크는 같은 언어 경로로 맞춤
- 이미지 내 한글이 있으면 영어 버전 이미지 별도 생성/편집

### 7) Preview 배포 + 승인 (필수)

main 직행 금지, preview 검토 후 배포.

```bash
cd ~/projects/dev-blog
git checkout -B preview
git add -A
git commit -m "Add blog post: {title}"
git push origin preview --force
```

확인 링크:
- ko: `https://it-blog-git-preview-bumfoo-s-team.vercel.app/ko/blog/{slug}`
- en: `https://it-blog-git-preview-bumfoo-s-team.vercel.app/en/blog/{slug}`

승인 후:
```bash
git checkout main
git merge preview
git push origin main
```

## 최종 체크리스트

- [ ] frontmatter에 `tldr` 있음
- [ ] 본문에 `## TL;DR` 없음
- [ ] `faq`가 있으면 Q/A 2개 이상
- [ ] 사용자 제공 이미지 확인 및 webp 변환 완료
- [ ] cover/inline 이미지 경로 정상
- [ ] ko/en slug 및 구조 정합성 확인
- [ ] preview 링크 확인 및 승인 완료
- [ ] main 배포 완료

## 참고

- 포맷 상세: `references/blog-format.md`
