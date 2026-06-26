"""SpecValidator - 스펙 품질 검증 시스템

스펙 문서의 완성도와 품질을 검증하여 개발 성공률 향상
"""

import logging
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

logger = logging.getLogger('builder-agent.integration.spec_validator')


class ValidationResult(Enum):
    """검증 결과"""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


@dataclass
class ValidationCheck:
    """개별 검증 항목"""
    name: str
    result: ValidationResult
    message: str
    suggestion: Optional[str] = None


@dataclass
class SpecValidationReport:
    """스펙 검증 리포트"""
    spec_title: str
    overall_result: ValidationResult
    checks: List[ValidationCheck] = field(default_factory=list)
    score: float = 0.0  # 0.0 ~ 1.0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'spec_title': self.spec_title,
            'overall_result': self.overall_result.value,
            'score': round(self.score, 2),
            'checks': [
                {
                    'name': check.name,
                    'result': check.result.value,
                    'message': check.message,
                    'suggestion': check.suggestion
                }
                for check in self.checks
            ],
            'recommendations': self.recommendations
        }


class SpecValidator:
    """스펙 품질 검증기

    필수 섹션 존재 여부, 소스별 요구사항 충족 확인, 복잡도 적절성 평가
    """

    # 필수 섹션 (모든 스펙)
    REQUIRED_SECTIONS = [
        '개요',
        '목표',
        '기능',
        '기술',
        '성공'
    ]

    # 소스별 추가 요구사항
    SOURCE_REQUIREMENTS = {
        'cve_database': [
            'CVE 정보',
            '심각도',
            'CVSS',
            '취약점',
            '스캔'
        ],
        'security_news': [
            '위협',
            '탐지',
            '모니터링',
            '알림'
        ],
        'github_trending': [
            '참조',
            '개선',
            '확장'
        ]
    }

    def __init__(self):
        self.checks = []

    def validate_spec(self, spec: str, idea: Dict) -> SpecValidationReport:
        """스펙 검증 수행

        Args:
            spec: 스펙 내용 (마크다운)
            idea: 프로젝트 아이디어

        Returns:
            SpecValidationReport
        """
        self.checks = []
        title = idea.get('title', 'Unknown')
        source = idea.get('source', 'manual')
        complexity = idea.get('complexity', 'medium')

        # 1. 필수 섹션 검증
        self._check_required_sections(spec)

        # 2. 소스별 요구사항 검증
        self._check_source_requirements(spec, source)

        # 3. 복잡도 적절성 검증
        self._check_complexity_appropriateness(spec, complexity)

        # 4. 내용 충실도 검증
        self._check_content_depth(spec)

        # 5. 구조화 정도 검증
        self._check_structure(spec)

        # 점수 계산
        score = self._calculate_score()

        # 전체 결과 결정
        overall_result = self._determine_overall_result(score)

        # 권장사항 생성
        recommendations = self._generate_recommendations()

        return SpecValidationReport(
            spec_title=title,
            overall_result=overall_result,
            checks=self.checks,
            score=score,
            recommendations=recommendations
        )

    def _check_required_sections(self, spec: str):
        """필수 섹션 존재 여부 검증"""
        spec_lower = spec.lower()

        for section in self.REQUIRED_SECTIONS:
            # 섹션 헤더 패턴 (##, ###)
            pattern = rf'##\s*{re.escape(section)}'
            if re.search(pattern, spec, re.IGNORECASE):
                self.checks.append(ValidationCheck(
                    name=f'필수 섹션: {section}',
                    result=ValidationResult.PASS,
                    message=f'"{section}" 섹션 존재'
                ))
            else:
                self.checks.append(ValidationCheck(
                    name=f'필수 섹션: {section}',
                    result=ValidationResult.FAIL,
                    message=f'"{section}" 섹션 누락',
                    suggestion=f'## {section} 섹션 추가 필요'
                ))

    def _check_source_requirements(self, spec: str, source: str):
        """소스별 요구사항 충족 확인"""
        if source not in self.SOURCE_REQUIREMENTS:
            return

        spec_lower = spec.lower()
        requirements = self.SOURCE_REQUIREMENTS[source]

        for req in requirements:
            if req in spec_lower:
                self.checks.append(ValidationCheck(
                    name=f'소스 요구사항 ({source}): {req}',
                    result=ValidationResult.PASS,
                    message=f'"{req}" 관련 내용 포함'
                ))
            else:
                self.checks.append(ValidationCheck(
                    name=f'소스 요구사항 ({source}): {req}',
                    result=ValidationResult.WARNING,
                    message=f'"{req}" 관련 내용 부족',
                    suggestion=f'"{req}"에 대한 설명 추가 권장'
                ))

    def _check_complexity_appropriateness(self, spec: str, complexity: str):
        """복잡도 적절성 평가"""
        spec_length = len(spec)
        section_count = len(re.findall(r'^##+', spec, re.MULTILINE))
        code_block_count = len(re.findall(r'```', spec)) // 2
        checklist_count = len(re.findall(r'- \[ \]', spec))

        # 복잡도별 기대치
        expectations = {
            'simple': {
                'min_length': 500,
                'min_sections': 5,
                'min_code_blocks': 1,
                'min_checklist': 5
            },
            'medium': {
                'min_length': 1000,
                'min_sections': 7,
                'min_code_blocks': 2,
                'min_checklist': 8
            },
            'complex': {
                'min_length': 1500,
                'min_sections': 10,
                'min_code_blocks': 3,
                'min_checklist': 12
            }
        }

        expected = expectations.get(complexity, expectations['medium'])

        # 길이 검증
        if spec_length >= expected['min_length']:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 스펙 길이',
                result=ValidationResult.PASS,
                message=f'스펙 길이 적절 ({spec_length}자)'
            ))
        else:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 스펙 길이',
                result=ValidationResult.WARNING,
                message=f'스펙 길이 부족 ({spec_length}자 < {expected["min_length"]}자)',
                suggestion=f'상세 설명 추가 필요 (최소 {expected["min_length"]}자 권장)'
            ))

        # 섹션 수 검증
        if section_count >= expected['min_sections']:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 섹션 수',
                result=ValidationResult.PASS,
                message=f'섹션 수 적절 ({section_count}개)'
            ))
        else:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 섹션 수',
                result=ValidationResult.WARNING,
                message=f'섹션 수 부족 ({section_count}개 < {expected["min_sections"]}개)',
                suggestion=f'필요한 섹션 추가 (최소 {expected["min_sections"]}개 권장)'
            ))

        # 코드 블록 검증
        if code_block_count >= expected['min_code_blocks']:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 코드 예제',
                result=ValidationResult.PASS,
                message=f'코드 예시 포함 ({code_block_count}개)'
            ))
        else:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 코드 예제',
                result=ValidationResult.WARNING,
                message=f'코드 예시 부족 ({code_block_count}개 < {expected["min_code_blocks"]}개)',
                suggestion='API 예시 코드 추가 권장'
            ))

        # 체크리스트 검증
        if checklist_count >= expected['min_checklist']:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 체크리스트',
                result=ValidationResult.PASS,
                message=f'체크리스트 항목 적절 ({checklist_count}개)'
            ))
        else:
            self.checks.append(ValidationCheck(
                name=f'복잡도({complexity}): 체크리스트',
                result=ValidationResult.WARNING,
                message=f'체크리스트 항목 부족 ({checklist_count}개 < {expected["min_checklist"]}개)',
                suggestion=f'성공 기준 항목 추가 (최소 {expected["min_checklist"]}개 권장)'
            ))

    def _check_content_depth(self, spec: str):
        """내용 충실도 검증"""
        lines = spec.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]

        # 빈 줄 비율
        empty_ratio = 1 - (len(non_empty_lines) / len(lines) if lines else 0)

        if empty_ratio < 0.3:
            self.checks.append(ValidationCheck(
                name='내용 충실도: 공백 비율',
                result=ValidationResult.PASS,
                message=f'적절한 내용 밀도 (공백 {empty_ratio*100:.1f}%)'
            ))
        else:
            self.checks.append(ValidationCheck(
                name='내용 충실도: 공백 비율',
                result=ValidationResult.WARNING,
                message=f'공백이 많음 (공백 {empty_ratio*100:.1f}%)',
                suggestion='내용을 더 채우거나 불필요한 공백 제거'
            ))

        # 평균 라인 길이
        avg_line_length = sum(len(l) for l in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0

        if avg_line_length > 30:
            self.checks.append(ValidationCheck(
                name='내용 충실도: 설명 상세도',
                result=ValidationResult.PASS,
                message=f'적절한 설명 상세도 (평균 {avg_line_length:.1f}자/라인)'
            ))
        else:
            self.checks.append(ValidationCheck(
                name='내용 충실도: 설명 상세도',
                result=ValidationResult.WARNING,
                message=f'설명이 간단함 (평균 {avg_line_length:.1f}자/라인)',
                suggestion='각 항목에 더 상세한 설명 추가'
            ))

    def _check_structure(self, spec: str):
        """구조화 정도 검증"""
        # 헤딩 구조 확인
        headings = re.findall(r'^(#{1,6})\s+(.+)$', spec, re.MULTILINE)

        if len(headings) >= 5:
            # 적절한 헤딩 계층 구조 확인
            has_h1 = any(level == '#' for level, _ in headings)
            has_h2 = any(level == '##' for level, _ in headings)

            if has_h1 and has_h2:
                self.checks.append(ValidationCheck(
                    name='구조화: 헤딩 계층',
                    result=ValidationResult.PASS,
                    message=f'적절한 헤딩 구조 ({len(headings)}개 헤딩)'
                ))
            else:
                self.checks.append(ValidationCheck(
                    name='구조화: 헤딩 계층',
                    result=ValidationResult.WARNING,
                    message='헤딩 계층 구조 개선 필요',
                    suggestion='#, ## 헤딩을 적절히 사용'
                ))
        else:
            self.checks.append(ValidationCheck(
                name='구조화: 헤딩 계층',
                result=ValidationResult.WARNING,
                message=f'헤딩이 부족 ({len(headings)}개)',
                suggestion='최소 5개 이상의 헤딩 사용'
            ))

    def _calculate_score(self) -> float:
        """종합 점수 계산 (0.0 ~ 1.0)"""
        if not self.checks:
            return 0.0

        total_score = 0.0
        weights = {
            ValidationResult.PASS: 1.0,
            ValidationResult.WARNING: 0.5,
            ValidationResult.FAIL: 0.0
        }

        for check in self.checks:
            total_score += weights.get(check.result, 0.0)

        return total_score / len(self.checks)

    def _determine_overall_result(self, score: float) -> ValidationResult:
        """전체 결과 결정"""
        if score >= 0.8:
            return ValidationResult.PASS
        elif score >= 0.6:
            return ValidationResult.WARNING
        else:
            return ValidationResult.FAIL

    def _generate_recommendations(self) -> List[str]:
        """개선 권고사항 생성"""
        recommendations = []

        # FAIL 항목에 대한 권고사항
        fails = [c for c in self.checks if c.result == ValidationResult.FAIL]
        if fails:
            recommendations.append(f"**긴급**: {len(fails)}개의 필수 항목이 누락되었습니다.")
            for fail in fails[:3]:  # 최대 3개만 표시
                if fail.suggestion:
                    recommendations.append(f"- {fail.suggestion}")

        # WARNING 항목에 대한 권고사항
        warnings = [c for c in self.checks if c.result == ValidationResult.WARNING]
        if warnings:
            recommendations.append(f"**개선**: {len(warnings)}개의 항목을 개선하면 스펙 품질이 향상됩니다.")

        # 전체적인 권고사항
        score = self._calculate_score()
        if score < 0.5:
            recommendations.append("스펙을 크게 보강할 필요가 있습니다. 각 섹션에 상세한 내용을 추가하세요.")
        elif score < 0.8:
            recommendations.append("스펙의 품질을 높이기 위해 누락된 부분을 채워주세요.")
        else:
            recommendations.append("스펙이 잘 작성되었습니다. 개발을 진행해도 좋습니다.")

        return recommendations

    def validate_notion_spec(self, spec_content: str, idea: Dict) -> bool:
        """Notion 스펙 검증 (빠른 검사)

        Args:
            spec_content: Notion 페이지 내용
            idea: 프로젝트 아이디어

        Returns:
            검증 통과 여부
        """
        report = self.validate_spec(spec_content, idea)

        # 점수 0.7 이상이면 통과
        return report.score >= 0.7
