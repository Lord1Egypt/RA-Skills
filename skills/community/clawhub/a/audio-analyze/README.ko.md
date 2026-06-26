# audio-analyze-skill-for-openclaw

오디오/비디오 콘텐츠를 높은 정확도로 텍스트로 변환하고 분석합니다. [Powered by Evolink.ai](https://evolink.ai/?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

🌐 English | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Türkçe](README.tr.md) | [Русский](README.ru.md)

## 소개

Gemini 3.1 Pro를 사용하여 오디오/비디오 파일을 자동으로 텍스트로 변환하고 분석하세요. [무료 API 키 받기 →](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

## 설치

### ClawHub를 통한 설치 (권장)

```bash
openclaw skills add https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
```

### 수동 설치

```bash
git clone https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
cd audio-analyze-skill-for-openclaw
pip install -r requirements.txt
```

## 설정

| 변수명 | 설명 | 기본값 |
| :--- | :--- | :--- |
| `EVOLINK_API_KEY` | Evolink API 키 | (필수) |
| `EVOLINK_MODEL` | 텍스트 변환 모델 | gemini-3.1-pro-preview-customtools |

*자세한 API 설정 및 모델 지원에 대해서는 [EvoLink API 문서](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)를 참조하세요.*

## 사용법

### 기본 사용법

```bash
export EVOLINK_API_KEY="your-key-here"
./scripts/transcribe.sh audio.mp3
```

### 고급 사용법

```bash
./scripts/transcribe.sh audio.mp3 --diarize --lang ja
```

### 출력 예시

* **요약(TL;DR)**: 이 오디오는 테스트용 샘플 트랙입니다.
* **주요 요점(Key Takeaways)**: 고음질 사운드, 명확한 주파수 응답.
* **실행 항목(Action Items)**: 최종 테스트를 위해 프로덕션 환경에 업로드하기.

## 사용 가능한 모델

- **Gemini 시리즈** (OpenAI API — `/v1/chat/completions`)

## 파일 구조

```
.
├── README.md
├── SKILL.md
├── _meta.json
├── scripts/
│   └── transcribe.sh
└── references/
    └── api-params.md
```

## 문제 해결

- **Argument list too long (인수 목록이 너무 김)**: 대용량 오디오 데이터의 경우 임시 파일을 사용하세요.
- **API Key Error (API 키 오류)**: `EVOLINK_API_KEY`가 환경 변수로 설정(export)되었는지 확인하세요.

## 링크

- [ClawHub](https://clawhub.ai/EvoLinkAI/audio-analyze)
- [API 참조](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)
- [커뮤니티](https://discord.com/invite/5mGHfA24kn)
- [고객 지원](mailto:support@evolink.ai)

## 라이선스

MIT