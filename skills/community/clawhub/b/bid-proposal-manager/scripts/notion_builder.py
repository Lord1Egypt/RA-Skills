#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion 입찰/제안 분석 결과 페이지 빌더

이 모듈은 Notion API를 통해 입찰 및 제안 분석 결과를 구조화된 프로젝트 페이지로 생성합니다.
Notion 공식 SDK 대신 requests 라이브러리를 직접 사용하며, 한국어 프로젝트 관리를 위한
다양한 블록 타입을 지원합니다.

사용 예:
    python notion_builder.py create --input analysis.json --database-id DB_ID --create-subpages
    python notion_builder.py update --page-id PAGE_ID --input analysis.json
    python notion_builder.py dashboard --database-id DB_ID
"""

import argparse
import json
import sys
import os
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import requests
from requests.exceptions import RequestException

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


@dataclass
class NotionConfig:
    """Notion API 설정"""
    api_key: str
    database_id: Optional[str] = None
    api_url: str = "https://api.notion.com/v1"
    api_version: str = "2022-06-28"
    max_retries: int = 3
    retry_delay: float = 1.0


class NotionAPIClient:
    """Notion API와 통신하는 클라이언트"""

    def __init__(self, config: NotionConfig):
        self.config = config
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """세션 헤더 설정"""
        self.session.headers.update({
            "Authorization": f"Bearer {self.config.api_key}",
            "Notion-Version": self.config.api_version,
            "Content-Type": "application/json"
        })

    def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """재시도 로직을 포함한 요청"""
        url = f"{self.config.api_url}{endpoint}"

        for attempt in range(self.config.max_retries):
            try:
                response = self.session.request(
                    method,
                    url,
                    json=data,
                    params=params,
                    timeout=10
                )

                # 429 (Rate Limited) 처리
                if response.status_code == 429:
                    wait_time = self.config.retry_delay * (2 ** attempt)
                    logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()

            except RequestException as e:
                if attempt == self.config.max_retries - 1:
                    logger.error(f"Request failed after {self.config.max_retries} attempts: {e}")
                    raise

                wait_time = self.config.retry_delay * (2 ** attempt)
                logger.warning(f"Request failed. Retrying in {wait_time}s...")
                time.sleep(wait_time)

        raise RuntimeError(f"Failed to complete request to {endpoint}")

    def create_page(
        self,
        database_id: str,
        properties: Dict[str, Any],
        children: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """새 페이지 생성"""
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }

        if children:
            data["children"] = children

        logger.info(f"Creating new page in database {database_id}")
        return self._request_with_retry("POST", "/pages", data)

    def update_page_properties(
        self,
        page_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """페이지 속성 업데이트"""
        logger.info(f"Updating page properties for {page_id}")
        return self._request_with_retry(
            "PATCH",
            f"/pages/{page_id}",
            {"properties": properties}
        )

    def append_blocks(
        self,
        block_id: str,
        children: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """블록 추가 (최대 100개)"""
        if len(children) > 100:
            logger.warning(f"Appending {len(children)} blocks in chunks of 100")
            results = []
            for i in range(0, len(children), 100):
                chunk = children[i:i+100]
                logger.info(f"Appending blocks {i+1}-{min(i+100, len(children))}")
                result = self._request_with_retry(
                    "PATCH",
                    f"/blocks/{block_id}/children",
                    {"children": chunk}
                )
                results.append(result)
            return results[-1]  # 마지막 결과 반환

        logger.info(f"Appending {len(children)} blocks to {block_id}")
        return self._request_with_retry(
            "PATCH",
            f"/blocks/{block_id}/children",
            {"children": children}
        )

    def query_database(
        self,
        database_id: str,
        filter_obj: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """데이터베이스 쿼리"""
        data = {"page_size": page_size}

        if filter_obj:
            data["filter"] = filter_obj

        if sorts:
            data["sorts"] = sorts

        logger.info(f"Querying database {database_id}")
        response = self._request_with_retry(
            "POST",
            f"/databases/{database_id}/query",
            data
        )

        return response.get("results", [])

    def retrieve_page(self, page_id: str) -> Dict[str, Any]:
        """페이지 정보 조회"""
        return self._request_with_retry("GET", f"/pages/{page_id}")

    def retrieve_block_children(
        self,
        block_id: str,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """블록의 자식 블록 조회"""
        response = self._request_with_retry(
            "GET",
            f"/blocks/{block_id}/children",
            params={"page_size": page_size}
        )
        return response.get("results", [])


class NotionPageBuilder:
    """Notion 페이지 구성 및 생성"""

    def __init__(self, client: NotionAPIClient):
        self.client = client

    def _split_rich_text(self, text: str, max_length: int = 2000) -> List[str]:
        """긴 텍스트를 최대 길이로 분할"""
        if len(text) <= max_length:
            return [text]

        chunks = []
        current = ""

        for line in text.split("\n"):
            if len(current) + len(line) + 1 <= max_length:
                current += line + "\n"
            else:
                if current:
                    chunks.append(current.rstrip())
                current = line + "\n"

        if current:
            chunks.append(current.rstrip())

        return chunks

    def _create_rich_text_block(self, text: str, block_type: str = "paragraph") -> Dict[str, Any]:
        """텍스트 블록 생성"""
        return {
            block_type: {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": "default"
            }
        }

    def _create_heading_block(self, text: str, level: int = 2) -> Dict[str, Any]:
        """제목 블록 생성"""
        heading_key = f"heading_{level}"
        return {
            heading_key: {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": "default",
                "is_toggleable": False
            }
        }

    def _create_callout_block(self, text: str, emoji: str = "💡") -> Dict[str, Any]:
        """콜아웃 블록 생성"""
        return {
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "icon": {"type": "emoji", "emoji": emoji},
                "color": "blue_background"
            }
        }

    def _create_bulleted_list_block(self, text: str) -> Dict[str, Any]:
        """불릿 리스트 블록 생성"""
        return {
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": "default"
            }
        }

    def _create_todo_block(self, text: str, checked: bool = False) -> Dict[str, Any]:
        """체크리스트 블록 생성"""
        return {
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "checked": checked,
                "color": "default"
            }
        }

    def _create_table_block(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> Dict[str, Any]:
        """테이블 블록 생성"""
        table_width = len(headers)

        # 헤더 행
        header_cells = [
            [{"type": "text", "text": {"content": h}}] for h in headers
        ]

        # 데이터 행
        data_cells = []
        for row in rows:
            cells = [
                [{"type": "text", "text": {"content": str(cell) if cell else ""}}]
                for cell in row[:table_width]
            ]
            data_cells.append(cells)

        return {
            "table": {
                "table_width": table_width,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    {"table_row": {"cells": header_cells}},
                    *[{"table_row": {"cells": cells}} for cells in data_cells]
                ]
            }
        }

    def _create_bookmark_block(self, url: str, title: Optional[str] = None) -> Dict[str, Any]:
        """북마크 블록 생성"""
        block = {"bookmark": {"url": url}}
        if title:
            block["bookmark"]["caption"] = [{"type": "text", "text": {"content": title}}]
        return block

    def _build_project_properties(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """프로젝트 속성 구성"""
        properties = {
            "사업명": {
                "title": [{"type": "text", "text": {"content": data.get("project_name", "")}}]
            }
        }

        # 선택적 속성들
        if "client" in data:
            properties["발주기관"] = {
                "rich_text": [{"type": "text", "text": {"content": data["client"]}}]
            }

        if "deadline" in data:
            properties["마감일"] = {
                "date": {"start": data["deadline"]}
            }

        if "status" in data:
            properties["상태"] = {
                "select": {"name": data["status"]}
            }

        if "project_type" in data:
            properties["사업유형"] = {
                "select": {"name": data["project_type"]}
            }

        if "budget" in data:
            properties["예산"] = {
                "number": int(data["budget"]) if isinstance(data["budget"], (int, float)) else 0
            }

        if "announcement_number" in data:
            properties["공고번호"] = {
                "rich_text": [{"type": "text", "text": {"content": data["announcement_number"]}}]
            }

        if "qualification_met" in data:
            properties["자격충족"] = {
                "checkbox": bool(data["qualification_met"])
            }

        return properties

    def _build_project_blocks(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """프로젝트 콘텐츠 블록 구성"""
        blocks = []

        # 1. 📋 기본 정보
        basic_info = self._build_basic_info_block(data)
        blocks.extend(basic_info)

        # 2. 📅 주요 일정
        if "schedule" in data:
            schedule_blocks = self._build_schedule_block(data["schedule"])
            blocks.extend(schedule_blocks)

        # 3. ✅ 제출서류 체크리스트
        if "required_documents" in data:
            checklist_blocks = self._build_checklist_block(data["required_documents"])
            blocks.extend(checklist_blocks)

        # 4. 📝 자격요건
        if "qualifications" in data:
            qual_blocks = self._build_qualifications_block(data["qualifications"])
            blocks.extend(qual_blocks)

        # 5. 💰 예산/규모
        if "budget_breakdown" in data:
            budget_blocks = self._build_budget_block(data["budget_breakdown"])
            blocks.extend(budget_blocks)

        # 6. 📖 제안서 작성 요령
        if "writing_guidelines" in data:
            guide_blocks = self._build_writing_guidelines_block(data["writing_guidelines"])
            blocks.extend(guide_blocks)

        # 7. 🔍 평가기준
        if "evaluation_criteria" in data:
            eval_blocks = self._build_evaluation_criteria_block(data["evaluation_criteria"])
            blocks.extend(eval_blocks)

        # 8. 📎 원본 링크
        if "source_url" in data:
            link_blocks = self._build_source_link_block(data["source_url"])
            blocks.extend(link_blocks)

        return blocks

    def _build_basic_info_block(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """기본 정보 블록"""
        blocks = []

        blocks.append(self._create_heading_block("📋 기본 정보", 2))

        info_text = self._format_basic_info(data)
        blocks.append(self._create_callout_block(info_text, "💡"))

        return blocks

    def _format_basic_info(self, data: Dict[str, Any]) -> str:
        """기본 정보 포맷팅"""
        lines = []

        if "project_name" in data:
            lines.append(f"프로젝트: {data['project_name']}")

        if "client" in data:
            lines.append(f"발주기관: {data['client']}")

        if "announcement_number" in data:
            lines.append(f"공고번호: {data['announcement_number']}")

        if "deadline" in data:
            lines.append(f"마감일: {data['deadline']}")

        if "budget" in data:
            budget_str = f"{int(data['budget']):,}" if isinstance(data['budget'], (int, float)) else str(data['budget'])
            lines.append(f"예산: {budget_str}원")

        if "project_type" in data:
            lines.append(f"사업유형: {data['project_type']}")

        return "\n".join(lines)

    def _build_schedule_block(self, schedule: Dict[str, str]) -> List[Dict[str, Any]]:
        """주요 일정 블록"""
        blocks = []

        blocks.append(self._create_heading_block("📅 주요 일정", 2))

        headers = ["항목", "날짜"]
        rows = []

        schedule_items = [
            ("공고일", "announcement_date"),
            ("설명회", "briefing_date"),
            ("질의마감", "q_deadline"),
            ("제출마감", "submission_deadline"),
            ("결과발표", "result_date")
        ]

        for label, key in schedule_items:
            if key in schedule:
                rows.append([label, schedule[key]])

        if rows:
            blocks.append(self._create_table_block(headers, rows))

        return blocks

    def _build_checklist_block(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """제출서류 체크리스트 블록"""
        blocks = []

        blocks.append(self._create_heading_block("✅ 제출서류 체크리스트", 2))

        for doc in documents:
            doc_name = doc.get("name", "문서")
            doc_desc = doc.get("description", "")

            if doc_desc:
                text = f"{doc_name} - {doc_desc}"
            else:
                text = doc_name

            blocks.append(self._create_todo_block(text))

        return blocks

    def _build_qualifications_block(self, qualifications: List[str]) -> List[Dict[str, Any]]:
        """자격요건 블록"""
        blocks = []

        blocks.append(self._create_heading_block("📝 자격요건", 2))

        for qual in qualifications:
            blocks.append(self._create_bulleted_list_block(qual))

        return blocks

    def _build_budget_block(self, budget: Dict[str, Any]) -> List[Dict[str, Any]]:
        """예산/규모 블록"""
        blocks = []

        blocks.append(self._create_heading_block("💰 예산/규모", 2))

        headers = ["항목", "금액"]
        rows = []

        budget_items = [
            ("총사업비", "total"),
            ("정부출연금", "government"),
            ("민간부담금", "private")
        ]

        for label, key in budget_items:
            if key in budget:
                value = budget[key]
                if isinstance(value, (int, float)):
                    value_str = f"{int(value):,}원"
                else:
                    value_str = str(value)
                rows.append([label, value_str])

        if rows:
            blocks.append(self._create_table_block(headers, rows))

        return blocks

    def _build_writing_guidelines_block(
        self,
        guidelines: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """제안서 작성 요령 블록"""
        blocks = []

        blocks.append(self._create_heading_block("📖 제안서 작성 요령", 2))

        for section_name, section_content in guidelines.items():
            blocks.append(self._create_heading_block(section_name, 3))

            if isinstance(section_content, list):
                for item in section_content:
                    blocks.append(self._create_bulleted_list_block(item))
            elif isinstance(section_content, str):
                for text in self._split_rich_text(section_content):
                    blocks.append(self._create_rich_text_block(text))

        return blocks

    def _build_evaluation_criteria_block(
        self,
        criteria: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """평가기준 블록"""
        blocks = []

        blocks.append(self._create_heading_block("🔍 평가기준", 2))

        headers = ["항목", "평가기준", "만점", "배점"]
        rows = []

        for criterion in criteria:
            row = [
                criterion.get("category", ""),
                criterion.get("criterion", ""),
                str(criterion.get("max_score", "")),
                str(criterion.get("weight", ""))
            ]
            rows.append(row)

        if rows:
            blocks.append(self._create_table_block(headers, rows))

        return blocks

    def _build_source_link_block(self, url: str) -> List[Dict[str, Any]]:
        """원본 링크 블록"""
        blocks = []

        blocks.append(self._create_heading_block("📎 원본 링크", 2))
        blocks.append(self._create_bookmark_block(url, "원본 페이지"))

        return blocks

    def create_page_from_analysis(
        self,
        database_id: str,
        analysis_data: Dict[str, Any],
        create_subpages: bool = True
    ) -> Tuple[str, str]:
        """분석 결과로부터 페이지 생성"""
        logger.info(f"Creating page from analysis data in database {database_id}")

        properties = self._build_project_properties(analysis_data)

        children = None
        if create_subpages:
            children = self._build_project_blocks(analysis_data)

        response = self.client.create_page(database_id, properties, children)

        page_id = response.get("id", "")
        page_url = response.get("url", "")

        logger.info(f"Page created successfully: {page_id}")

        return page_id, page_url

    def update_page_from_analysis(
        self,
        page_id: str,
        analysis_data: Dict[str, Any]
    ) -> str:
        """기존 페이지 업데이트"""
        logger.info(f"Updating page {page_id}")

        properties = self._build_project_properties(analysis_data)
        self.client.update_page_properties(page_id, properties)

        # 기존 블록 조회 및 삭제는 복잡하므로, 새 블록 추가만 진행
        children = self._build_project_blocks(analysis_data)

        if children:
            self.client.append_blocks(page_id, children)

        logger.info(f"Page updated successfully: {page_id}")

        return page_id


class NotionDashboard:
    """Notion 대시보드 조회 및 출력"""

    def __init__(self, client: NotionAPIClient):
        self.client = client

    def get_dashboard_summary(self, database_id: str) -> Dict[str, Any]:
        """대시보드 요약 정보 조회"""
        logger.info(f"Fetching dashboard data for {database_id}")

        # 모든 페이지 조회
        pages = self.client.query_database(database_id)

        summary = {
            "total_projects": len(pages),
            "active_projects": [],
            "upcoming_deadlines": [],
            "preparation_status": {}
        }

        for page in pages:
            props = page.get("properties", {})

            # 활성 프로젝트 (상태: active)
            status = self._extract_select(props, "상태")
            if status == "active":
                summary["active_projects"].append({
                    "name": self._extract_title(props, "사업명"),
                    "deadline": self._extract_date(props, "마감일"),
                    "id": page.get("id")
                })

            # 준비 상태
            prep_status = self._extract_checkbox(props, "자격충족")
            if prep_status is not None:
                status_key = "자격충족" if prep_status else "자격미충족"
                summary["preparation_status"][status_key] = \
                    summary["preparation_status"].get(status_key, 0) + 1

        # 마감일이 가까운 순서로 정렬
        summary["active_projects"].sort(
            key=lambda x: x.get("deadline", "9999-12-31")
        )
        summary["upcoming_deadlines"] = summary["active_projects"][:5]

        return summary

    def _extract_title(self, properties: Dict, prop_name: str) -> str:
        """title 속성 추출"""
        prop = properties.get(prop_name, {})
        if "title" in prop:
            return "".join(t.get("text", {}).get("content", "") for t in prop["title"])
        return ""

    def _extract_select(self, properties: Dict, prop_name: str) -> Optional[str]:
        """select 속성 추출"""
        prop = properties.get(prop_name, {})
        if "select" in prop and prop["select"]:
            return prop["select"].get("name", "")
        return None

    def _extract_date(self, properties: Dict, prop_name: str) -> Optional[str]:
        """date 속성 추출"""
        prop = properties.get(prop_name, {})
        if "date" in prop and prop["date"]:
            return prop["date"].get("start", "")
        return None

    def _extract_checkbox(self, properties: Dict, prop_name: str) -> Optional[bool]:
        """checkbox 속성 추출"""
        prop = properties.get(prop_name, {})
        if "checkbox" in prop:
            return prop["checkbox"]
        return None

    def print_dashboard(self, summary: Dict[str, Any]):
        """대시보드 출력"""
        print(f"\n전체 프로젝트: {summary['total_projects']}", file=sys.stderr)
        print(f"활성 프로젝트: {len(summary['active_projects'])}", file=sys.stderr)

        if summary["upcoming_deadlines"]:
            print("\n[가까운 마감일]", file=sys.stderr)
            for project in summary["upcoming_deadlines"]:
                print(
                    f"  - {project['name']}: {project.get('deadline', 'N/A')}",
                    file=sys.stderr
                )

        if summary["preparation_status"]:
            print("\n[준비 상태]", file=sys.stderr)
            for status, count in summary["preparation_status"].items():
                print(f"  - {status}: {count}", file=sys.stderr)


def load_analysis_file(file_path: str) -> Dict[str, Any]:
    """분석 JSON 파일 로드"""
    logger.info(f"Loading analysis file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info(f"Loaded analysis data with {len(data)} keys")
    return data


def output_result(result: Dict[str, Any]):
    """결과를 JSON으로 stdout에 출력"""
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Notion 입찰/제안 분석 결과 페이지 빌더",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  python notion_builder.py create --input analysis.json --database-id DB_ID
  python notion_builder.py update --page-id PAGE_ID --input analysis.json
  python notion_builder.py dashboard --database-id DB_ID
        """
    )

    # API 키 환경변수 확인
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        logger.error("NOTION_API_KEY 환경변수가 설정되지 않았습니다")
        sys.exit(1)

    default_db_id = os.getenv("NOTION_DATABASE_ID")

    config = NotionConfig(api_key=api_key, database_id=default_db_id)
    client = NotionAPIClient(config)

    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # create 서브명령어
    create_parser = subparsers.add_parser("create", help="새 페이지 생성")
    create_parser.add_argument(
        "--input",
        required=True,
        help="분석 결과 JSON 파일 경로"
    )
    create_parser.add_argument(
        "--database-id",
        default=default_db_id,
        help="Notion 데이터베이스 ID"
    )
    create_parser.add_argument(
        "--create-subpages",
        action="store_true",
        default=True,
        help="서브페이지 컨텐츠 생성 (기본값: True)"
    )

    # update 서브명령어
    update_parser = subparsers.add_parser("update", help="기존 페이지 업데이트")
    update_parser.add_argument(
        "--page-id",
        required=True,
        help="업데이트할 페이지 ID"
    )
    update_parser.add_argument(
        "--input",
        required=True,
        help="분석 결과 JSON 파일 경로"
    )

    # dashboard 서브명령어
    dashboard_parser = subparsers.add_parser("dashboard", help="대시보드 조회")
    dashboard_parser.add_argument(
        "--database-id",
        default=default_db_id,
        help="Notion 데이터베이스 ID"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "create":
            if not args.database_id:
                logger.error("--database-id를 지정하거나 NOTION_DATABASE_ID 환경변수를 설정하세요")
                sys.exit(1)

            analysis_data = load_analysis_file(args.input)
            builder = NotionPageBuilder(client)

            page_id, page_url = builder.create_page_from_analysis(
                args.database_id,
                analysis_data,
                args.create_subpages
            )

            output_result({
                "status": "success",
                "page_id": page_id,
                "page_url": page_url,
                "message": "페이지가 성공적으로 생성되었습니다"
            })

        elif args.command == "update":
            analysis_data = load_analysis_file(args.input)
            builder = NotionPageBuilder(client)

            page_id = builder.update_page_from_analysis(args.page_id, analysis_data)

            output_result({
                "status": "success",
                "page_id": page_id,
                "message": "페이지가 성공적으로 업데이트되었습니다"
            })

        elif args.command == "dashboard":
            if not args.database_id:
                logger.error("--database-id를 지정하거나 NOTION_DATABASE_ID 환경변수를 설정하세요")
                sys.exit(1)

            dashboard = NotionDashboard(client)
            summary = dashboard.get_dashboard_summary(args.database_id)

            dashboard.print_dashboard(summary)

            output_result({
                "status": "success",
                "total_projects": summary["total_projects"],
                "active_projects": len(summary["active_projects"]),
                "preparation_status": summary["preparation_status"],
                "message": "대시보드 조회가 완료되었습니다"
            })

    except FileNotFoundError as e:
        logger.error(f"파일을 찾을 수 없습니다: {e}")
        output_result({
            "status": "error",
            "error": str(e),
            "type": "FileNotFoundError"
        })
        sys.exit(1)

    except RequestException as e:
        logger.error(f"API 요청 오류: {e}")
        output_result({
            "status": "error",
            "error": str(e),
            "type": "RequestException"
        })
        sys.exit(1)

    except json.JSONDecodeError as e:
        logger.error(f"JSON 파싱 오류: {e}")
        output_result({
            "status": "error",
            "error": str(e),
            "type": "JSONDecodeError"
        })
        sys.exit(1)

    except Exception as e:
        logger.error(f"예상치 못한 오류: {e}")
        output_result({
            "status": "error",
            "error": str(e),
            "type": type(e).__name__
        })
        sys.exit(1)


if __name__ == "__main__":
    main()
