"""SpecTemplateManager - 동적 스펙 템플릿 시스템

복잡도별, 소스별 동적 템플릿으로 스펙 품질 향상
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger('builder-agent.integration.template_manager')


@dataclass
class SuccessPattern:
    """성공 패턴 데이터"""
    source: str
    complexity: str
    pattern: str
    success_rate: float
    usage_count: int


class SpecTemplateManager:
    """동적 스펙 템플릿 관리자

    복잡도별, 소스별 맞춤 템플릿 제공
    """

    # 복잡도별 기본 템플릿
    COMPLEXITY_TEMPLATES = {
        'simple': {
            'min_sections': 5,
            'required_sections': ['개요', '기능', '기술 스택', '파일 구조', '성공 기준'],
            'estimated_hours': '2-4'
        },
        'medium': {
            'min_sections': 7,
            'required_sections': ['개요', '목표', '주요 기능', '기술 스펙', '아키텍처', '파일 구조', '성공 기준'],
            'estimated_hours': '4-8'
        },
        'complex': {
            'min_sections': 10,
            'required_sections': ['개요', '배경', '목표', '요구사항', '아키텍처', '기술 스펙',
                                'API 설계', '파일 구조', '테스트 전략', '성공 기준', '롤아웃 계획'],
            'estimated_hours': '8-16'
        }
    }

    # 소스별 추가 섹션
    SOURCE_SPECIFIC_SECTIONS = {
        'cve_database': {
            'CVE 정보': ['CVE ID', '심각도', 'CVSS 점수', '영향도', '참조 링크'],
            '보안 고려사항': ['취약점 분석', '완화 방법', '보안 모범 사례']
        },
        'security_news': {
            '위협 분석': ['위협 유형', '공격 벡터', '영향 범위'],
            '탐지 메커니즘': ['시그니처', '패턴 매칭', '행태 분석']
        },
        'github_trending': {
            '참조 프로젝트': ['원본 레포지토리', '핵심 기능', '개선점'],
            '확장 계획': ['추가 기능', '최적화', '문서화']
        }
    }

    def __init__(self, success_patterns_path: Optional[Path] = None):
        """초기화

        Args:
            success_patterns_path: 성공 패턴 데이터 파일 경로
        """
        self.success_patterns_path = success_patterns_path
        self.success_patterns = self._load_success_patterns()

    def generate_dynamic_spec(self, idea: Dict) -> str:
        """아이디어에 맞는 동적 스펙 생성

        Args:
            idea: 프로젝트 아이디어

        Returns:
            마크다운 형식 스펙
        """
        source = idea.get('source', 'manual')
        complexity = idea.get('complexity', 'medium')

        # 기본 템플릿 선택
        template_config = self.COMPLEXITY_TEMPLATES.get(
            complexity,
            self.COMPLEXITY_TEMPLATES['medium']
        )

        # 소스별 추가 섹션
        source_sections = self.SOURCE_SPECIFIC_SECTIONS.get(source, {})

        # 성공 패턴 통합
        pattern_enhancements = self._get_pattern_enhancements(source, complexity)

        # 스펙 생성
        spec = self._build_spec_content(
            idea,
            template_config,
            source_sections,
            pattern_enhancements
        )

        return spec

    def _load_success_patterns(self) -> List[SuccessPattern]:
        """성공 패턴 로드"""
        patterns = []

        if self.success_patterns_path and self.success_patterns_path.exists():
            try:
                import json
                with open(self.success_patterns_path, 'r') as f:
                    data = json.load(f)
                    patterns = [
                        SuccessPattern(**p) for p in data.get('patterns', [])
                    ]
                logger.info("Loaded %d success patterns", len(patterns))
            except Exception as e:
                logger.warning("Failed to load success patterns: %s", e)

        return patterns

    def _get_pattern_enhancements(self, source: str, complexity: str) -> List[str]:
        """성공 패턴 기반 개선사항 추출"""
        enhancements = []

        # 관련 패턴 필터링
        relevant_patterns = [
            p for p in self.success_patterns
            if (p.source == source or p.source == 'all') and
            (p.complexity == complexity or p.complexity == 'all')
        ]

        # 성공률이 높은 패턴 우선 적용
        relevant_patterns.sort(key=lambda p: p.success_rate, reverse=True)

        for pattern in relevant_patterns[:5]:  # 최대 5개 패턴
            if pattern.success_rate > 0.7:
                enhancements.append(f"✓ {pattern.pattern}")

        return enhancements

    def _build_spec_content(self, idea: Dict, template_config: Dict,
                          source_sections: Dict, pattern_enhancements: List[str]) -> str:
        """스펙 내용 빌드"""
        title = idea['title']
        description = idea.get('description', '')
        complexity = idea.get('complexity', 'medium')
        source = idea.get('source', 'manual')
        url = idea.get('url', '')

        # 헤더
        spec_parts = [self._generate_header(title, description, complexity)]

        # 기본 섹션들
        spec_parts.append(self._generate_overview_section(idea))
        spec_parts.append(self._generate_objectives_section(idea, complexity))
        spec_parts.append(self._generate_features_section(idea, complexity))
        spec_parts.append(self._generate_tech_spec_section(idea, complexity))

        # 아키텍처 추천
        if complexity in ['medium', 'complex']:
            spec_parts.append(self._generate_architecture_section(idea))

        # 소스별 섹션
        for section_name, section_content in source_sections.items():
            spec_parts.append(self._generate_source_specific_section(
                section_name, section_content, idea
            ))

        # 파일 구조
        spec_parts.append(self._generate_file_structure_section(idea, complexity))

        # API 설계 (medium+)
        if complexity in ['medium', 'complex']:
            spec_parts.append(self._generate_api_section(idea))

        # 성공 기준
        spec_parts.append(self._generate_success_criteria_section(idea, complexity))

        # 성공 패턴 기반 추천
        if pattern_enhancements:
            spec_parts.append(self._generate_pattern_recommendations(pattern_enhancements))

        # 참고 자료
        spec_parts.append(self._generate_references_section(idea, url))

        # 실행 예시
        spec_parts.append(self._generate_usage_example_section(idea))

        # 푸터
        spec_parts.append(self._generate_footer())

        return '\n\n'.join(spec_parts)

    def _generate_header(self, title: str, description: str, complexity: str) -> str:
        """헤더 생성"""
        return f"""# 📋 {title}

{description}

**복잡도**: {complexity.upper()}
**생성일시**: {self._get_timestamp()}"""

    def _generate_overview_section(self, idea: Dict) -> str:
        """개요 섹션"""
        source = idea.get('source', 'manual')

        source_info = ""
        if source == 'cve_database':
            source_info = f"""
## 🔍 CVE 정보
- **CVE ID**: `{idea.get('cve_id', 'Unknown')}`
- **심각도**: {idea.get('severity', 'MEDIUM')}
- **CVSS 점수**: {idea.get('cvss_score', 0):.1f}/10.0
"""
        elif source == 'github_trending':
            metrics = idea.get('github_metrics', {})
            stars = metrics.get('stars', 0)
            source_info = f"""
## 🔍 GitHub 정보
- **Stars**: {stars:,} ⭐
- **Forks**: {metrics.get('forks', 0):,}
"""
        elif source == 'security_news':
            source_info = f"""
## 🔍 뉴스 정보
- **키워드**: {idea.get('keyword', 'security')}
"""

        return f"""## 📋 프로젝트 개요
{idea.get('description', '자동 생성된 프로젝트 스펙')}
{source_info}"""

    def _generate_objectives_section(self, idea: Dict, complexity: str) -> str:
        """목표 섹션"""
        source = idea.get('source', 'manual')

        if source == 'cve_database':
            cve_id = idea.get('cve_id', 'Unknown')
            objectives = f"""## 🎯 개발 목표
{cve_id} 취약점을 탐지하고 분석하는 CLI 도구 개발

### 핵심 목표
1. **취약점 스캔**: 대상 시스템에서 {cve_id} 취약점 탐지
2. **영향 분석**: 취약점의 영향도 평가 및 보고서 생성
3. **완화 가이드**: 취약점 해결을 위한 권장 사항 제공
4. **결과 출력**: JSON/CSV/TXT 형식으로 결과 저장"""
        elif source == 'security_news':
            keyword = idea.get('keyword', 'security')
            objectives = f"""## 🎯 개발 목표
"{keyword}" 관련 보안 위협 탐지 또는 방어 도구 개발

### 핵심 목표
1. **위협 탐지**: {keyword} 관련 위협 요소 식별
2. **실시간 모니터링**: 지속적인 보안 상태 확인
3. **알림 시스템**: 위협 감지 시 즉시 알림
4. **로그 분석**: 보안 로그 분석 및 시각화"""
        elif source == 'github_trending':
            objectives = """## 🎯 개발 목표
인기 있는 GitHub 프로젝트를 참고한 유사 도구 또는 개선판 개발

### 접근 방식
1. **Clone & Analyze**: 원본 프로젝트 분석
2. **Improve**: 기능 개선 또는 단순화
3. **Korean Support**: 한국어 문서화 추가
4. **Extend**: 새로운 기능 추가"""
        else:
            objectives = """## 🎯 개발 목표
명확하고 유지보수 가능한 프로젝트 개발

### 핵심 목표
1. **핵심 기능**: 프로젝트의 주요 기능 구현
2. **입출력**: 데이터 입력 및 결과 출력
3. **에러 처리**: 예외 상황 핸들링
4. **문서화**: 사용법 및 API 문서"""

        return objectives

    def _generate_features_section(self, idea: Dict, complexity: str) -> str:
        """기능 섹션"""
        if complexity == 'simple':
            features = """## 💡 주요 기능
1. **핵심 기능**: 프로젝트의 주요 기능 구현
2. **CLI 인터페이스**: 명령행 인터페이스 제공
3. **기본 설정**: 설정 파일 지원
4. **에러 처리**: 적절한 예외 처리"""
        elif complexity == 'medium':
            features = """## 💡 주요 기능
1. **핵심 기능**: 주요 기능 완전 구현
2. **CLI 인터페이스**: 직관적인 명령행 인터페이스
3. **설정 관리**: YAML/JSON 설정 파일 지원
4. **로깅**: 상세한 로그 출력
5. **에러 처리**: 포괄적인 예외 처리
6. **테스트**: 단위 테스트 및 통합 테스트"""
        else:  # complex
            features = """## 💡 주요 기능
1. **핵심 기능**: 모든 기능 완전 구현
2. **CLI 인터페이스**: 고급 명령행 인터페이스 (서브커맨드, 플래그)
3. **설정 관리**: 계층적 설정 파일, 환경변수 지원
4. **로깅**: 구조화된 로그, 다양한 레벨
5. **에러 처리**: 세분화된 예외, 재시도 로직
6. **테스트**: 단위, 통합, E2E 테스트
7. **확장성**: 플러그인 시스템, API
8. **문서화**: API 문서, 가이드, 예제"""

        return features

    def _generate_tech_spec_section(self, idea: Dict, complexity: str) -> str:
        """기술 스펙 섹션"""
        tech_stack = ', '.join(idea.get('tech_stack', ['Python']))

        if complexity == 'simple':
            estimated = "2-4시간"
        elif complexity == 'medium':
            estimated = "4-8시간"
        else:
            estimated = "8-16시간"

        return f"""## 💻 기술 스펙

### 복잡도: {complexity.upper()}
- 예상 개발 시간: {estimated}
- 필요 기술: {tech_stack}

### 기술 스택
- **Language**: Python 3.9+
- **Testing**: pytest + 80% 커버리지
- **Packaging**: setuptools + wheel
- **Documentation**: Markdown"""

    def _generate_architecture_section(self, idea: Dict) -> str:
        """아키텍처 섹션"""
        complexity = idea.get('complexity', 'medium')

        if complexity == 'medium':
            return """## 🏗️ 아키텍처

### 모듈 구조
- **Core**: 핵심 로직 및 비즈니스 규칙
- **CLI**: 명령행 인터페이스
- **Utils**: 공통 유틸리티 함수
- **Config**: 설정 관리

### 데이터 흐름
```
사용자 입력 → CLI → Core → 처리 → 결과 출력
```

### 확장 지점
- 플러그인 시스템 (선택)
- 백엔드 연동 (선택)"""
        else:  # complex
            return """## 🏗️ 아키텍처

### 시스템 구조
```
┌─────────────┐
│   CLI/UI    │
└──────┬──────┘
       │
┌──────▼──────┐
│  Interface  │
└──────┬──────┘
       │
┌──────▼──────┐     ┌─────────────┐
│   Core      │────▶│  Database   │
│  (Service)  │     └─────────────┘
└──────┬──────┘
       │
┌──────▼──────┐
│ Providers   │
└─────────────┘
```

### 레이어 구조
- **Presentation Layer**: CLI/UI
- **Application Layer**: 비즈니스 로직 조율
- **Domain Layer**: 핵심 도메인 로직
- **Infrastructure Layer**: 외부 연동

### 디자인 패턴
- Factory: 객체 생성
- Strategy: 알고리즘 교체
- Observer: 이벤트 처리
- Repository: 데이터 접근"""

    def _generate_source_specific_section(self, section_name: str,
                                         section_content: List[str], idea: Dict) -> str:
        """소스별 섹션 생성"""
        content_lines = [f"## 🔧 {section_name}"]
        for item in section_content:
            content_lines.append(f"- **{item}**: (설명 추가 필요)")
        return '\n'.join(content_lines)

    def _generate_file_structure_section(self, idea: Dict, complexity: str) -> str:
        """파일 구조 섹션"""
        project_name = idea['title'].lower().replace(' ', '_').replace(':', '')

        if complexity == 'simple':
            return f"""## 📁 파일 구조
```
{project_name}/
├── src/
│   ├── __init__.py
│   └── main.py          # 메인 모듈
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── README.md
├── requirements.txt
└── setup.py
```"""
        elif complexity == 'medium':
            return f"""## 📁 파일 구조
```
{project_name}/
├── src/
│   ├── __init__.py
│   ├── core/            # 핵심 로직
│   │   ├── __init__.py
│   │   └── processor.py
│   ├── cli/             # CLI 인터페이스
│   │   ├── __init__.py
│   │   └── commands.py
│   └── utils/           # 유틸리티
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_cli.py
├── config.yaml
├── README.md
├── requirements.txt
└── setup.py
```"""
        else:  # complex
            return f"""## 📁 파일 구조
```
{project_name}/
├── src/
│   ├── __init__.py
│   ├── core/            # 핵심 도메인
│   │   ├── __init__.py
│   │   ├── entities.py
│   │   ├── services.py
│   │   └── repositories.py
│   ├── application/     # 애플리케이션 계층
│   │   ├── __init__.py
│   │   ├── use_cases.py
│   │   └── dto.py
│   ├── infrastructure/  # 인프라
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── external_api.py
│   ├── interface/       # 인터페이스
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   └── api.py
│   └── shared/          # 공유
│       ├── __init__.py
│       ├── config.py
│       └── logging.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── api.md
│   └── architecture.md
├── config/
│   ├── default.yaml
│   └── production.yaml
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── setup.py
```"""

    def _generate_api_section(self, idea: Dict) -> str:
        """API 설계 섹션"""
        return """## 🔌 API 설계

### 핵심 API
```python
# main.py
class Processor:
    def process(self, input_data: Any) -> Result:
        \"\"\"메인 처리 함수\"\"\"
        pass

    def configure(self, config: Dict) -> None:
        \"\"\"설정 로드\"\"\"
        pass
```

### CLI 인터페이스
```bash
# 기본 사용
python -m {module} --input <path> --output <path>

# 설정 파일 사용
python -m {module} --config config.yaml

# 상세 모드
python -m {module} --verbose --log-level DEBUG
```"""

    def _generate_success_criteria_section(self, idea: Dict, complexity: str) -> str:
        """성공 기준 섹션"""
        if complexity == 'simple':
            checklist = [
                '핵심 기능 구현 완료',
                'unittest 3개 이상 작성',
                '테스트 커버리지 80%+ 달성',
                'README.md 작성 (사용법 포함)',
                'requirements.txt 생성'
            ]
        elif complexity == 'medium':
            checklist = [
                '모든 주요 기능 구현',
                'unittest 5개 이상 작성',
                '테스트 커버리지 80%+ 달성',
                '에러 처리 완료',
                'README.md 작성',
                'API 문서화',
                '설정 예시 파일 제공',
                '동작 예시 3개 이상'
            ]
        else:  # complex
            checklist = [
                '모든 기능 완전 구현',
                '단위/통합/E2E 테스트 작성',
                '테스트 커버리지 80%+ 달성',
                '에러 처리 및 재시도 로직',
                '성능 최적화',
                'README.md + 가이드 작성',
                'API 문서 완비',
                '아키텍처 다이어그램',
                'CI/CD 설정 (선택)',
                '배포 가이드'
            ]

        items = '\n'.join(f'- [ ] {item}' for item in checklist)
        return f"""## ✅ 성공 기준
{items}"""

    def _generate_pattern_recommendations(self, enhancements: List[str]) -> str:
        """성공 패턴 기반 추천"""
        return """## 🎯 성공 패턴 기반 추천
""".format('\n'.join(enhancements))

    def _generate_references_section(self, idea: Dict, url: str) -> str:
        """참고 자료 섹션"""
        refs = [
            "- [Python Documentation](https://docs.python.org/3/)",
            "- [pytest Documentation](https://docs.pytest.org/)"
        ]

        if url:
            refs.insert(0, f"- [참조 자료]({url})")

        return "## 📚 참고 자료\n" + '\n'.join(refs)

    def _generate_usage_example_section(self, idea: Dict) -> str:
        """실행 예시 섹션"""
        module_name = idea['title'].lower().replace(' ', '_').replace(':', '').replace('-', '_')

        return f"""## 🚀 실행 예시
```bash
# 설치
pip install {module_name}

# 기본 사용
{module_name} --help

# 상세 사용
{module_name} --input data.txt --output result.json --verbose
```"""

    def _generate_footer(self) -> str:
        """푸터"""
        return f"""
---
*자동 생성됨: Builder Agent v6.0 (Enhanced)*
*생성 일시: {self._get_timestamp()}*
"""

    def _get_timestamp(self) -> str:
        """현재 타임스탬프"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def record_success_pattern(self, idea: Dict, success: bool,
                               pattern: str = "default"):
        """성공 패턴 기록"""
        if not self.success_patterns_path:
            self.success_patterns_path = Path("builder/integration/success_patterns.json")

        # 데이터 로드
        if self.success_patterns_path.exists():
            try:
                import json
                with open(self.success_patterns_path, 'r') as f:
                    data = json.load(f)
            except:
                data = {'patterns': []}
        else:
            data = {'patterns': []}

        # 패턴 찾기 또는 생성
        source = idea.get('source', 'manual')
        complexity = idea.get('complexity', 'medium')

        pattern_found = False
        for p in data['patterns']:
            if (p['source'] == source and
                p['complexity'] == complexity and
                p['pattern'] == pattern):

                p['usage_count'] += 1
                if success:
                    p['success_count'] += 1
                p['success_rate'] = p['success_count'] / p['usage_count']
                pattern_found = True
                break

        if not pattern_found:
            new_pattern = {
                'source': source,
                'complexity': complexity,
                'pattern': pattern,
                'success_count': 1 if success else 0,
                'usage_count': 1,
                'success_rate': 1.0 if success else 0.0
            }
            data['patterns'].append(new_pattern)

        # 저장
        try:
            self.success_patterns_path.parent.mkdir(parents=True, exist_ok=True)
            import json
            with open(self.success_patterns_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning("Failed to save success pattern: %s", e)
