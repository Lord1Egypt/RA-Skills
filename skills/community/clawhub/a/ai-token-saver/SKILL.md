---
name: token-saver
description: AI 토큰 사용량 96% 절감. 한국어 Context DB로 프롬프트 최적화. Trigger: "토큰 절약", "토큰세이버", "컨텍스트 저장", "메모리 검색", "프롬프트 최적화".
compatibility: Python 3.10+
---

# 토큰세이버 (TokenSaver)

**AI 토큰 사용량 96% 절감!**

한국어 Context DB로 긴 프롬프트를 짧은 검색으로 대체.

## 🎯 왜 필요한가?

| 상황 | 기존 | 토큰세이버 |
|------|------|-----------|
| 컨텍스트 전달 | 1,500토큰 | ~50토큰 |
| 메모리 검색 | 전체 로드 | 레벨별 검색 |
| 월 비용 | $100 | $4 |

**96% 절감!**

## 🚀 사용법

### 설치
```bash
pip install token-saver
```

### 기본 사용

```python
from token_saver import TokenSaver

# API Key 설정 (무료: 50회/월)
ts = TokenSaver(api_key="your_key")

# 저장
ts.save("project/alpha", "이 프로젝트는...")

# 검색 (토큰 절약!)
result = ts.search("프로젝트 정보", level=0)  # 96% 절약
```

### CLI

```bash
# 저장
token-saver save "memories/roadmap" --content "2026년 목표: 10억"

# 검색
token-saver search "목표" --level 0

# 사용량
token-saver usage
```

## 📊 검색 레벨

| 레벨 | 토큰 | 절감 | 용도 |
|------|------|------|------|
| 0 | ~50 | 96% | 빠른 검색, 키워드만 |
| 1 | ~200 | 91% | 컨텍스트 파악 |
| 2 | ~500+ | 원본 | 상세 작업 |

## 💰 요금제

| 플랜 | 가격 | API 호출 |
|------|------|----------|
| Free | $0 | 50회/월 |
| Pro | $9/월 | 1,000회/월 |
| Team | $29/월 | 무제한 |

## 🔑 API Key 발급

1. https://tokensaver.ai 접속
2. 회원가입
3. API Key 발급

---

## 🇰🇷 한국어 특화

- 형태소 분석 기반 검색
- 한국어 비즈니스 템플릿
- 한국 시간대 기반

---

*토큰세이버 v1.0.0*
*AI 토큰 96% 절감!*