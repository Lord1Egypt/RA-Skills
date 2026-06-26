#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
입찰/제안 공고 분석기

파싱된 문서 텍스트에서 구조화된 정보를 추출하고, 제출 서류를 검증합니다.
한국어 입찰/제안 공고 문서의 주요 정보를 자동으로 추출하여 JSON 형식으로 출력합니다.
"""

import json
import argparse
import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass, asdict
import mimetypes

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


@dataclass
class Project:
    """프로젝트 정보"""
    project_name: str = ""
    announcement_no: str = ""
    issuing_org: str = ""
    project_type: str = "other"  # bid|research|grant|contest|procurement|other
    announcement_date: str = ""
    submission_deadline: str = ""
    briefing_date: str = ""
    qa_deadline: str = ""
    result_date: str = ""
    project_period: str = ""
    total_budget: Optional[int] = None
    gov_funding: Optional[int] = None
    private_funding: Optional[int] = None
    source_url: str = ""
    source_file: str = ""
    contact_name: str = ""
    contact_phone: str = ""
    contact_email: str = ""
    summary: str = ""


@dataclass
class Qualification:
    """자격 요건"""
    qual_type: str  # required|preferred|restriction
    description: str = ""
    sort_order: int = 0


@dataclass
class Document:
    """제출 서류"""
    doc_name: str = ""
    doc_type: str = "required"  # required|optional|form_provided
    format_req: str = ""
    page_limit: Optional[int] = None
    sort_order: int = 0


@dataclass
class EvaluationCriterion:
    """평가 기준"""
    category: str = ""
    criterion: str = ""
    max_score: int = 0
    weight: int = 0
    sort_order: int = 0


@dataclass
class WritingGuideline:
    """작성 가이드라인"""
    section_title: str = ""
    section_number: str = ""
    description: str = ""
    page_limit: Optional[int] = None
    sort_order: int = 0


class ProposalAnalyzer:
    """입찰/제안 공고 분석기"""

    # 정규식 패턴 정의
    PATTERNS = {
        'project_name': r'(?:사업명|과제명|연구과제명|연구사업명|건명|프로젝트명)\s*[:：]\s*(.+?)(?:\n|$)',
        'announcement_no': r'(?:공고번호|공고\s*제|공고\s*\(|공시번호|입찰공고번호)\s*[:：]?\s*([^\n\r]+?)(?:\n|$)',
        'issuing_org': r'(?:발주기관|주관기관|발주처|기관명|주최|주최기관|담당|제출처)\s*[:：]\s*([^\n\r]+?)(?:\n|$)',
        'announcement_date': r'(?:공고일|공고일자|공시일|공고\s*일)\s*[:：]\s*([^\n\r]+?)(?:\n|$)',
        'submission_deadline': r'(?:제출기한|접수마감|마감일|제출마감|제출기간|신청기간|응모기간|신청마감)\s*[:：]\s*([^\n\r]+?)(?:\n|$)',
        'briefing_date': r'(?:설명회|기술설명회|입찰설명회)\s*[:：]?\s*([^\n\r]*?\d+년\s*\d+월\s*\d+일[^\n\r]*)(?:\n|$)',
        'qa_deadline': r'(?:질의|Q&A|문의기한|질문마감|질의마감)\s*[:：]\s*([^\n\r]+?)(?:\n|$)',
        'result_date': r'(?:결과발표|선정발표|개찰|개찰일|결과공시)\s*[:：]?\s*([^\n\r]*?\d+년\s*\d+월\s*\d+일[^\n\r]*)(?:\n|$)',
        'project_period': r'(?:사업기간|연구기간|과제기간|수행기간|사업수행기간)\s*[:：]?\s*([^\n\r]+?)(?:\n|$)',
        'contact_name': r'(?:담당자|문의담당자|담당자\s*명)\s*[:：]?\s*([^\n\r]+?)(?:\n|$)',
        'contact_phone': r'(?:전화|전화번호|Tel)\s*[:：]?\s*([0-9\-\(\)]+)',
        'contact_email': r'(?:이메일|E-?mail|Email)\s*[:：]?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
    }

    def __init__(self):
        """분석기 초기화"""
        pass

    def extract_text(self, parsed_data: Dict[str, Any]) -> str:
        """파싱된 데이터에서 전체 텍스트 추출"""
        if isinstance(parsed_data, dict):
            if 'content' in parsed_data and isinstance(parsed_data['content'], dict):
                return parsed_data['content'].get('full_text', '')
            elif 'full_text' in parsed_data:
                return parsed_data['full_text']
        return str(parsed_data)

    def parse_date(self, date_str: str) -> str:
        """한국어 및 ISO 형식 날짜 파싱"""
        if not date_str:
            return ""

        date_str = date_str.strip()

        # 이미 ISO 형식인 경우
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            return date_str

        # 한국어 형식: "2026년 4월 30일"
        korean_pattern = r'(\d+)년\s*(\d+)월\s*(\d+)일'
        match = re.search(korean_pattern, date_str)
        if match:
            year, month, day = match.groups()
            try:
                return f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"
            except:
                pass

        # 점 형식: "2026.04.30"
        dot_pattern = r'(\d{4})\.(\d{1,2})\.(\d{1,2})'
        match = re.search(dot_pattern, date_str)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        # 하이픈 형식: "2026-04-30"
        hyphen_pattern = r'(\d{4})-(\d{1,2})-(\d{1,2})'
        match = re.search(hyphen_pattern, date_str)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        return date_str

    def parse_time(self, text: str) -> str:
        """시간 정보 추출 (HH:MM 형식)"""
        # "18:00", "18시" 등 시간 정보 추출
        time_pattern = r'(\d{1,2}):?(\d{2})\s*(?:시)?'
        match = re.search(time_pattern, text)
        if match:
            hour, minute = match.groups()
            return f"{hour.zfill(2)}:{minute.zfill(2)}"
        return ""

    def parse_amount(self, amount_str: str) -> Optional[int]:
        """금액 파싱: "1,000,000원", "10억원", "5백만원" 등"""
        if not amount_str:
            return None

        amount_str = amount_str.strip()

        # 한국어 단위 제거 및 숫자 추출
        multiplier = 1

        if '억' in amount_str:
            multiplier = 100_000_000
            amount_str = amount_str.replace('억', '')
        elif '백만' in amount_str:
            multiplier = 1_000_000
            amount_str = amount_str.replace('백만', '')
        elif '만' in amount_str:
            multiplier = 10_000
            amount_str = amount_str.replace('만', '')
        elif '천' in amount_str:
            multiplier = 1_000
            amount_str = amount_str.replace('천', '')

        # 원, 달러 등 통화 제거
        amount_str = re.sub(r'[^\d.,]', '', amount_str)

        # 쉼표 제거
        amount_str = amount_str.replace(',', '')

        try:
            # 소수점이 있으면 정수 부분만 취함
            if '.' in amount_str:
                amount = int(float(amount_str) * multiplier)
            else:
                amount = int(amount_str) * multiplier
            return amount
        except (ValueError, AttributeError):
            return None

    def extract_with_pattern(self, text: str, pattern: str, default: str = "") -> str:
        """정규식 패턴으로 텍스트 추출"""
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            result = match.group(1).strip()
            # 줄바꿈 정리
            result = re.sub(r'\s+', ' ', result)
            return result[:200] if len(result) > 200 else result
        return default

    def extract_project_type(self, text: str) -> str:
        """프로젝트 타입 분류"""
        text_lower = text.lower()

        if any(keyword in text for keyword in ['입찰', '공사', '용역', '물품']):
            return 'bid'
        elif any(keyword in text for keyword in ['연구', '과제', '기술개발']):
            return 'research'
        elif any(keyword in text for keyword in ['지원금', '보조금', '보조']):
            return 'grant'
        elif any(keyword in text for keyword in ['공모', '경진', '대회', '선발']):
            return 'contest'
        elif any(keyword in text for keyword in ['조달', '구매', '발주']):
            return 'procurement'

        return 'other'

    def extract_qualifications(self, text: str) -> List[Dict[str, Any]]:
        """자격요건 섹션 추출"""
        qualifications = []

        # 자격요건 섹션 찾기
        qual_section_pattern = r'(?:참가자격|자격요건|응모자격|신청자격|기본요건)\s*[:：]?\s*\n((?:.|\n)*?)(?=\n(?:제출서류|구비서류|평가기준|문의|.*담당자|$))'
        match = re.search(qual_section_pattern, text, re.IGNORECASE)

        if match:
            qual_text = match.group(1)

            # 필수/권장/제한 사항 분류
            for line in qual_text.split('\n'):
                line = line.strip()
                if not line or len(line) < 5:
                    continue

                qual_type = 'required'
                if '필수' in line or '반드시' in line:
                    qual_type = 'required'
                elif '권장' in line or '선호' in line or '바람직' in line:
                    qual_type = 'preferred'
                elif '제한' in line or '불가' in line or '제외' in line:
                    qual_type = 'restriction'

                qualifications.append({
                    'qual_type': qual_type,
                    'description': line[:200],
                    'sort_order': len(qualifications)
                })

        return qualifications

    def extract_documents(self, text: str) -> List[Dict[str, Any]]:
        """제출서류 추출"""
        documents = []

        # 제출서류 섹션 찾기
        doc_section_pattern = r'(?:제출서류|구비서류|첨부서류|제출물)\s*[:：]?\s*\n((?:.|\n)*?)(?=\n(?:평가기준|선정기준|심사기준|문의|.*담당자|$))'
        match = re.search(doc_section_pattern, text, re.IGNORECASE)

        if match:
            doc_text = match.group(1)

            for line in doc_text.split('\n'):
                line = line.strip()
                if not line or len(line) < 3:
                    continue

                # 서식 제공 여부 판단
                doc_type = 'required'
                if '선택' in line or '필요시' in line or '해당시' in line:
                    doc_type = 'optional'
                elif '서식' in line or '양식' in line or '제공' in line:
                    doc_type = 'form_provided'

                # 페이지 제한 추출
                page_limit = None
                page_match = re.search(r'(\d+)\s*(?:페이지|쪽|p\.)', line, re.IGNORECASE)
                if page_match:
                    page_limit = int(page_match.group(1))

                # 형식 요구사항 추출
                format_req = ""
                if 'pdf' in line.lower():
                    format_req = "PDF"
                elif 'docx' in line.lower() or 'doc' in line.lower():
                    format_req = "DOCX"
                elif 'hwp' in line.lower():
                    format_req = "HWP"

                documents.append({
                    'doc_name': line[:100],
                    'doc_type': doc_type,
                    'format_req': format_req,
                    'page_limit': page_limit,
                    'sort_order': len(documents)
                })

        return documents

    def extract_evaluation_criteria(self, text: str) -> List[Dict[str, Any]]:
        """평가기준 추출"""
        criteria = []

        # 평가기준 섹션 찾기
        eval_section_pattern = r'(?:평가기준|선정기준|심사기준|배점)\s*[:：]?\s*\n((?:.|\n)*?)(?=\n(?:제출서류|문의|.*담당자|$))'
        match = re.search(eval_section_pattern, text, re.IGNORECASE)

        if match:
            eval_text = match.group(1)

            for line in eval_text.split('\n'):
                line = line.strip()
                if not line or len(line) < 3:
                    continue

                # 배점 및 가중치 추출
                max_score = 0
                weight = 0

                score_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:점|점수|배점)', line)
                if score_match:
                    max_score = int(float(score_match.group(1)))

                weight_match = re.search(r'(\d+(?:\.\d+)?)\s*%', line)
                if weight_match:
                    weight = int(float(weight_match.group(1)))

                criteria.append({
                    'category': '',
                    'criterion': line[:150],
                    'max_score': max_score,
                    'weight': weight,
                    'sort_order': len(criteria)
                })

        return criteria

    def extract_writing_guidelines(self, text: str) -> List[Dict[str, Any]]:
        """작성 가이드라인 추출"""
        guidelines = []

        # 섹션 제목 패턴 찾기
        section_pattern = r'^(\d+\.?\s*)?([^\n]+(?:방안|방법|계획|전략|내용|요구사항))[^\n]*$'

        for match in re.finditer(section_pattern, text, re.MULTILINE | re.IGNORECASE):
            section_number = match.group(1) or ""
            section_title = match.group(2)

            # 페이지 제한 추출
            page_limit = None
            if '페이지' in match.group(0) or '쪽' in match.group(0):
                page_match = re.search(r'(\d+)\s*(?:페이지|쪽)', match.group(0))
                if page_match:
                    page_limit = int(page_match.group(1))

            guidelines.append({
                'section_title': section_title[:100],
                'section_number': section_number.strip(),
                'description': '',
                'page_limit': page_limit,
                'sort_order': len(guidelines)
            })

        return guidelines[:10]  # 최대 10개

    def analyze(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """파싱된 문서 데이터 분석"""
        text = self.extract_text(parsed_data)

        if not text:
            logger.warning("입력 텍스트가 비어있습니다")
            return self._create_empty_analysis()

        # 프로젝트 정보 추출
        project = Project(
            project_name=self.extract_with_pattern(text, self.PATTERNS['project_name']),
            announcement_no=self.extract_with_pattern(text, self.PATTERNS['announcement_no']),
            issuing_org=self.extract_with_pattern(text, self.PATTERNS['issuing_org']),
            project_type=self.extract_project_type(text),
            announcement_date=self.parse_date(self.extract_with_pattern(text, self.PATTERNS['announcement_date'])),
            submission_deadline=self.parse_date(self.extract_with_pattern(text, self.PATTERNS['submission_deadline'])),
            briefing_date=self.parse_date(self.extract_with_pattern(text, self.PATTERNS['briefing_date'])),
            qa_deadline=self.parse_date(self.extract_with_pattern(text, self.PATTERNS['qa_deadline'])),
            result_date=self.parse_date(self.extract_with_pattern(text, self.PATTERNS['result_date'])),
            project_period=self.extract_with_pattern(text, self.PATTERNS['project_period']),
            source_file=parsed_data.get('source_file', '') if isinstance(parsed_data, dict) else "",
            contact_name=self.extract_with_pattern(text, self.PATTERNS['contact_name']),
            contact_phone=self.extract_with_pattern(text, self.PATTERNS['contact_phone']),
            contact_email=self.extract_with_pattern(text, self.PATTERNS['contact_email']),
            summary=text[:500]
        )

        # 예산 정보 추출
        budget_pattern = r'(?:총\s*사업비|연구비|예산|사업예산|총예산)\s*[:：]?\s*([^\n\r]+?)(?:원|$)'
        budget_match = re.search(budget_pattern, text, re.IGNORECASE)
        if budget_match:
            project.total_budget = self.parse_amount(budget_match.group(1))

        gov_pattern = r'(?:정부|국고|국비)\s*(?:예산|지원금|사업비)\s*[:：]?\s*([^\n\r]+?)(?:원|$)'
        gov_match = re.search(gov_pattern, text, re.IGNORECASE)
        if gov_match:
            project.gov_funding = self.parse_amount(gov_match.group(1))

        private_pattern = r'(?:민간|자부담|기업|참여\s*기업)\s*(?:예산|지원금|사업비)\s*[:：]?\s*([^\n\r]+?)(?:원|$)'
        private_match = re.search(private_pattern, text, re.IGNORECASE)
        if private_match:
            project.private_funding = self.parse_amount(private_match.group(1))

        # 추가 정보 추출
        qualifications = self.extract_qualifications(text)
        documents = self.extract_documents(text)
        evaluation_criteria = self.extract_evaluation_criteria(text)
        writing_guidelines = self.extract_writing_guidelines(text)

        analysis = {
            'project': asdict(project),
            'qualifications': qualifications,
            'documents': documents,
            'evaluation_criteria': evaluation_criteria,
            'writing_guidelines': writing_guidelines,
            'raw_text': text[:1000]  # 처음 1000자만 포함
        }

        return analysis

    def _create_empty_analysis(self) -> Dict[str, Any]:
        """빈 분석 결과 생성"""
        return {
            'project': asdict(Project()),
            'qualifications': [],
            'documents': [],
            'evaluation_criteria': [],
            'writing_guidelines': [],
            'raw_text': ''
        }


class SubmissionVerifier:
    """제출 서류 검증기"""

    def __init__(self):
        """검증기 초기화"""
        pass

    def get_page_count(self, file_path: Path) -> Optional[int]:
        """PDF/DOCX 파일의 페이지 수 반환"""
        try:
            suffix = file_path.suffix.lower()

            if suffix == '.pdf':
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        return len(reader.pages)
                except ImportError:
                    logger.warning("PyPDF2가 설치되어 있지 않습니다")
                    return None

            elif suffix in ['.docx', '.doc']:
                try:
                    from docx import Document
                    doc = Document(file_path)
                    return len(doc.paragraphs)
                except ImportError:
                    logger.warning("python-docx가 설치되어 있지 않습니다")
                    return None

        except Exception as e:
            logger.warning(f"페이지 수 계산 실패 ({file_path}): {str(e)}")

        return None

    def verify(self, analysis: Dict[str, Any], prepared_dir: Path, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """제출 서류 검증"""
        if not prepared_dir.exists():
            logger.error(f"제출 디렉토리가 존재하지 않습니다: {prepared_dir}")
            return {'error': f'디렉토리 없음: {prepared_dir}'}

        documents = analysis.get('documents', [])
        verification_results = []

        for doc in documents:
            doc_name = doc.get('doc_name', '')
            required = doc.get('doc_type', '') == 'required'
            page_limit = doc.get('page_limit')

            # 파일 찾기 (간단한 매칭)
            found_files = list(prepared_dir.glob('*'))
            matched_file = None

            for file_path in found_files:
                if doc_name.lower() in file_path.name.lower() or file_path.name.lower() in doc_name.lower():
                    matched_file = file_path
                    break

            result = {
                'doc_name': doc_name,
                'required': required,
                'status': '✅' if matched_file else ('❌' if required else '⚠️'),
                'file_exists': matched_file is not None,
                'file_path': str(matched_file) if matched_file else None,
                'page_count': None,
                'page_limit': page_limit,
                'page_ok': True
            }

            # 페이지 수 확인
            if matched_file and page_limit:
                page_count = self.get_page_count(matched_file)
                result['page_count'] = page_count
                if page_count and page_count <= page_limit:
                    result['page_ok'] = True
                    result['status'] = '✅'
                else:
                    result['page_ok'] = False
                    result['status'] = '❌'

            verification_results.append(result)

        verification = {
            'verification_timestamp': datetime.now().isoformat(),
            'verified_dir': str(prepared_dir),
            'total_documents': len(documents),
            'verified_documents': len([r for r in verification_results if r['file_exists']]),
            'results': verification_results
        }

        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(verification, f, ensure_ascii=False, indent=2)
                logger.info(f"검증 결과 저장: {output_path}")
            except Exception as e:
                logger.error(f"검증 결과 저장 실패: {str(e)}")

        return verification


class ChecklistGenerator:
    """체크리스트 생성기"""

    def generate(self, analysis: Dict[str, Any]) -> str:
        """한국어 체크리스트 생성"""
        lines = []

        project = analysis.get('project', {})

        # 헤더
        lines.append("=" * 70)
        lines.append(f"[입찰/제안 체크리스트]")
        if project.get('project_name'):
            lines.append(f"프로젝트: {project['project_name']}")
        if project.get('announcement_no'):
            lines.append(f"공고번호: {project['announcement_no']}")
        lines.append("=" * 70)
        lines.append("")

        # 주요 날짜
        lines.append("[📅 주요 일정]")
        if project.get('announcement_date'):
            lines.append(f"  • 공고일: {project['announcement_date']}")
        if project.get('submission_deadline'):
            lines.append(f"  • 제출마감: {project['submission_deadline']}")
        if project.get('briefing_date'):
            lines.append(f"  • 설명회: {project['briefing_date']}")
        if project.get('qa_deadline'):
            lines.append(f"  • 질의마감: {project['qa_deadline']}")
        if project.get('result_date'):
            lines.append(f"  • 결과발표: {project['result_date']}")
        lines.append("")

        # 예산
        if project.get('total_budget') or project.get('gov_funding') or project.get('private_funding'):
            lines.append("[💰 예산]")
            if project.get('total_budget'):
                lines.append(f"  • 총 예산: {project['total_budget']:,}원")
            if project.get('gov_funding'):
                lines.append(f"  • 정부 지원: {project['gov_funding']:,}원")
            if project.get('private_funding'):
                lines.append(f"  • 민간 부담: {project['private_funding']:,}원")
            lines.append("")

        # 자격요건
        qualifications = analysis.get('qualifications', [])
        if qualifications:
            lines.append("[✓ 자격요건]")
            for qual in qualifications[:10]:
                symbol = "✓" if qual.get('qual_type') == 'required' else "○"
                lines.append(f"  {symbol} {qual.get('description', '')[:60]}")
            lines.append("")

        # 제출서류
        documents = analysis.get('documents', [])
        if documents:
            lines.append("[📄 제출서류]")
            for i, doc in enumerate(documents, 1):
                symbol = "✓" if doc.get('doc_type') == 'required' else "○"
                page_info = f" ({doc['page_limit']}쪽)" if doc.get('page_limit') else ""
                lines.append(f"  {symbol} [{i}] {doc.get('doc_name', '')[:50]}{page_info}")
                lines.append(f"       ☐ 준비 완료")
            lines.append("")

        # 평가기준
        criteria = analysis.get('evaluation_criteria', [])
        if criteria:
            lines.append("[📊 평가기준]")
            for crit in criteria[:10]:
                score_info = f" ({crit.get('max_score')}점)" if crit.get('max_score') else ""
                lines.append(f"  • {crit.get('criterion', '')[:60]}{score_info}")
            lines.append("")

        # 연락처
        lines.append("[📞 문의처]")
        if project.get('issuing_org'):
            lines.append(f"  • 발주기관: {project['issuing_org']}")
        if project.get('contact_name'):
            lines.append(f"  • 담당자: {project['contact_name']}")
        if project.get('contact_phone'):
            lines.append(f"  • 전화: {project['contact_phone']}")
        if project.get('contact_email'):
            lines.append(f"  • 이메일: {project['contact_email']}")
        lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='입찰/제안 공고 분석기',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='실행할 명령어')

    # analyze 서브커맨드
    analyze_parser = subparsers.add_parser('analyze', help='공고 문서 분석')
    analyze_parser.add_argument('--input', required=True, help='입력 JSON 파일 경로')
    analyze_parser.add_argument('--output', required=True, help='출력 JSON 파일 경로')

    # verify 서브커맨드
    verify_parser = subparsers.add_parser('verify', help='제출 서류 검증')
    verify_parser.add_argument('--requirements', required=True, help='분석 결과 JSON 파일')
    verify_parser.add_argument('--prepared-dir', required=True, help='준비된 서류 디렉토리')
    verify_parser.add_argument('--output', help='검증 결과 출력 파일')

    # checklist 서브커맨드
    checklist_parser = subparsers.add_parser('checklist', help='체크리스트 생성')
    checklist_parser.add_argument('--input', required=True, help='분석 결과 JSON 파일')

    args = parser.parse_args()

    try:
        if args.command == 'analyze':
            # 입력 파일 읽기
            with open(args.input, 'r', encoding='utf-8') as f:
                parsed_data = json.load(f)

            # 분석
            analyzer = ProposalAnalyzer()
            analysis = analyzer.analyze(parsed_data)

            # 결과 저장
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)

            logger.info(f"분석 완료: {args.output}")
            print(json.dumps(analysis, ensure_ascii=False))

        elif args.command == 'verify':
            # 분석 결과 읽기
            with open(args.requirements, 'r', encoding='utf-8') as f:
                analysis = json.load(f)

            # 검증
            verifier = SubmissionVerifier()
            prepared_dir = Path(args.prepared_dir)
            output_path = Path(args.output) if args.output else None

            verification = verifier.verify(analysis, prepared_dir, output_path)

            logger.info(f"검증 완료")
            print(json.dumps(verification, ensure_ascii=False))

        elif args.command == 'checklist':
            # 분석 결과 읽기
            with open(args.input, 'r', encoding='utf-8') as f:
                analysis = json.load(f)

            # 체크리스트 생성
            generator = ChecklistGenerator()
            checklist = generator.generate(analysis)

            print(checklist)

        else:
            parser.print_help()
            sys.exit(1)

    except FileNotFoundError as e:
        logger.error(f"파일을 찾을 수 없습니다: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 파싱 오류: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
