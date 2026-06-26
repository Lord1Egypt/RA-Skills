# Dev-Factory v6.0 Enhanced - Quick Start

## 🎉 새로운 기능

### ✅ 구현 완료 (P0/P1)

1. **적응형 다차원 점수 시스템**
   - 소스별 가중치 자동 조정 (CVE/GitHub/News)
   - 실제 GitHub 메트릭 수집 (stars, forks, issues)
   - 피드백 루프 기반 학습

2. **체크포인트 및 재개 기능**
   - 각 스테이지별 상태 저장
   - 실패 시 마지막 체크포인트부터 재개
   - 재시도 횟수 추적

3. **테스트 커버리지 검증**
   - pytest-cov로 실제 커버리지 측정
   - 80% 미만 시 빌드 실패
   - 미달 파일 식별

4. **스펙 품질 검증**
   - 필수 섹션 검증
   - 소스별 요구사항 확인
   - 복잡도 적절성 평가
   - 개선 권고사항 생성

5. **동적 스펙 템플릿**
   - 복잡도별 템플릿 (simple/medium/complex)
   - 소스별 섹션 자동 추가
   - 성공 패턴 통합

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd /Users/rebugui/.openclaw/workspace/skills/dev-factory
pip install -r requirements-enhanced.txt
```

### 2. Discovery 실행

```bash
python run_discovery.py
```

### 3. Build 실행

```bash
python run_build_from_notion.py
```

### 4. 테스트 실행

```bash
# 전체 테스트
python -m pytest tests/ -v

# 커버리지 확인
python -m pytest tests/ --cov=builder --cov-report=html
```

## ⚙️ Feature Flags

`config.yaml`에서 기능 켜기/끄기:

```yaml
features:
  adaptive_scoring: true        # 적응형 점수 시스템
  checkpoint_resume: true       # 체크포인트/재개
  coverage_validation: true     # 커버리지 검증
  spec_validation: true         # 스펙 검증
  dynamic_templates: true       # 동적 템플릿
```

## 📊 기대 효과

| 항목 | 개선 전 | 개선 후 |
|------|---------|---------|
| 점수 정확도 | 40% | 85%+ |
| 스펙 완성도 | 60% | 90%+ |
| 작업 손실 (실패 시) | 100% | 0% |
| 테스트 커버리지 | 미측정 | 80%+ |

## 📁 새로운 파일

```
builder/
├── checkpoint.py              # 체크포인트 시스템
├── integration/
│   ├── spec_validator.py     # 스펙 검증
│   └── template_manager.py   # 템플릿 관리
└── testing/
    └── runner.py             # 커버리지 검증 추가

tests/integration/
└── test_enhancements.py      # 26개 새 테스트

requirements-enhanced.txt     # 새 의존성
ENHANCEMENT_REPORT.md         # 상세 보고서
```

## 🔧 롤백 방법

문제 발생 시 `config.yaml`에서 해당 feature를 `false`로 설정:

```yaml
features:
  adaptive_scoring: false  # 기존 점수 시스템으로 복귀
```

## 📚 자세한 문서

- [ENHANCEMENT_REPORT.md](ENHANCEMENT_REPORT.md) - 상세 구현 보고서

---

**버전**: v6.0 Enhanced
**구현일**: 2026-03-12
**상태**: ✅ P0/P1 완료
