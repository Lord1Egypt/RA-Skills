"""
Notion Publisher
Notion API를 사용하여 블로그 글을 관리합니다.
"""

import requests
import subprocess
import tempfile
import base64
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
from modules.intelligence.config import NOTION_API_KEY, NOTION_DATABASE_ID, BLOG_REPO_PATH, BLOG_URL
from modules.intelligence.utils import setup_logger

logger = setup_logger(__name__, "notion_publisher.log")

class NotionPublisher:
    """Notion Publisher"""

    def __init__(self, api_key: Optional[str] = None, database_id: Optional[str] = None,
                 blog_repo_path: Path = None, blog_url: str = None):
        """초기화"""
        self.api_key = api_key or NOTION_API_KEY
        self.database_id = database_id or NOTION_DATABASE_ID
        self.version = "2022-06-28"
        self.blog_repo_path = blog_repo_path or BLOG_REPO_PATH
        self.blog_url = blog_url or BLOG_URL

        if not self.api_key:
            raise ValueError("NOTION_API_KEY is not set.")
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID is not set.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": self.version,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, path: str, data: Optional[Dict] = None) -> Dict:
        """API 요청 헬퍼"""
        url = f"https://api.notion.com/v1{path}"
        try:
            response = self.session.request(method, url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Notion API Failed ({method} {path}): {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            # 에러 발생 시 빈 딕셔너리 반환하거나 예외 전파
            raise

    def _convert_mermaid_to_image(self, mermaid_code: str, mermaid_index: int,
                                  output_format: str = 'svg') -> Optional[Dict]:
        """
        Mermaid 코드를 이미지로 변환하여 Hugo 블로그에 저장
        반환값: {'local_path': 로컬 경로, 'url': 블로그 URL}
        """
        try:
            # 이미지 저장 디렉토리 생성
            images_dir = self.blog_repo_path / "static" / "images" / "mermaid"
            images_dir.mkdir(parents=True, exist_ok=True)

            # 고유한 파일명 생성 (타임스탬프 + 인덱스)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mermaid_{timestamp}_{mermaid_index}.{output_format}"
            output_file = images_dir / filename

            # Mermaid 코드를 임시 파일로 저장
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(mermaid_code)
                mmd_file = f.name

            try:
                # Mermaid CLI 실행
                result = subprocess.run([
                    'npx', '-y', '@mermaid-js/mermaid-cli',
                    '-i', mmd_file,
                    '-o', str(output_file),
                    '-b', 'transparent',
                    '-s', '2'  # scale
                ], capture_output=True, timeout=30, text=True)

                if result.returncode != 0:
                    logger.error(f"Mermaid CLI failed: {result.stderr}")
                    return None

                # 파일이 생성되었는지 확인
                if not output_file.exists():
                    logger.error(f"Image file not created: {output_file}")
                    return None

                # Hugo 내부 경로와 외부 URL 생성
                local_path = f"/images/mermaid/{filename}"
                blog_image_url = f"{self.blog_url.rstrip('/')}/images/mermaid/{filename}"

                logger.info(f"Mermaid diagram saved: {output_file} ({output_file.stat().st_size} bytes)")

                return {
                    'local_path': local_path,
                    'url': blog_image_url,
                    'file_path': str(output_file)
                }

            finally:
                # 임시 Mermaid 파일 삭제
                try:
                    Path(mmd_file).unlink(missing_ok=True)
                except:
                    pass

        except subprocess.TimeoutExpired:
            logger.error("Mermaid CLI timeout")
            return None
        except Exception as e:
            logger.error(f"Failed to convert Mermaid to image: {e}")
            return None

    def create_article(self, article_data: Dict) -> Dict:
        """새 글 생성 (상태: 초안 작성중 -> 검토중)"""
        title = article_data.get('title', 'N/A')
        summary = article_data.get('summary', '')
        
        logger.info(f"Creating Notion page: {title}")

        # Properties
        properties = {
            "내용": {"title": [{"text": {"content": title}}]},
            "URL": {"url": article_data.get('original_url')},
            "상태": {"status": {"name": "초안 작성중"}},
        }

        if article_data.get('category'):
            properties["카테고리"] = {"select": {"name": article_data.get('category')}}

        if article_data.get('tags'):
            properties["테그"] = {"multi_select": [{"name": tag} for tag in article_data.get('tags')[:5]]}

        # Blocks (Content)
        children = self._convert_to_blocks(article_data.get('content', summary))

        # 1. Create Page
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties
        }

        try:
            page = self._request("POST", "/pages", payload)
            page_id = page['id']
            
            # 2. Append Blocks (Batch processing)
            if children:
                self._append_children(page_id, children)

            # 3. Update Status
            self.update_status(page_id, "검토중")
            
            return {"id": page_id, "url": page.get('url')}

        except Exception as e:
            logger.error(f"Failed to create article: {e}")
            return {}

    def _convert_to_blocks(self, content: str) -> List[Dict]:
        """Markdown 텍스트를 Notion 블록으로 변환 (개선)"""
        # 이스케이프 문자 처리
        content = content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')

        blocks = []
        lines = content.split('\n')
        i = 0
        mermaid_index = 0  # Mermaid 다이어그램 인덱스
        current_paragraph = []

        def flush_paragraph():
            if current_paragraph:
                text = ' '.join(current_paragraph)
                blocks.append(self._create_paragraph_block(text))
                current_paragraph.clear()

        while i < len(lines):
            line = lines[i].rstrip()

            # 빈 줄: 문단 플러시
            if not line:
                flush_paragraph()
                i += 1
                continue

            # 코드 블록 시작
            if line.startswith('```'):
                flush_paragraph()
                lang = line[3:].strip() or "plain text"

                # 먼저 코드 라인들을 수집
                i += 1
                code_lines = []
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1

                # 코드 텍스트 생성
                code_text = '\n'.join(code_lines)

                # Mermaid는 Notion에서 코드 블록으로 저장 (Hugo에서 렌더링)
                if lang.lower() == "mermaid":
                    mermaid_index += 1

                    # Notion에는 코드 블록으로 저장 (안내 메시지 없음)
                    blocks.append({
                        "object": "block",
                        "type": "code",
                        "code": {
                            "rich_text": [{"type": "text", "text": {"content": code_text}}],
                            "language": "javascript"  # Notion은 mermaid 언어를 지원하지만 렌더링 안 됨
                        }
                    })

                    i += 1  # closing ``` skip
                    continue

                # Notion 지원 언어로 매핑
                notion_langs = {
                    "python": "python", "javascript": "javascript", "js": "javascript",
                    "typescript": "typescript", "ts": "typescript",
                    "java": "java", "c": "c", "cpp": "c++", "c++": "c++",
                    "c#": "c#", "go": "go", "rust": "rust", "ruby": "ruby",
                    "php": "php", "swift": "swift", "kotlin": "kotlin",
                    "scala": "scala", "shell": "shell", "bash": "bash",
                    "sql": "sql", "html": "html", "css": "css",
                    "json": "json", "yaml": "yaml", "xml": "xml",
                    "markdown": "markdown", "md": "markdown",
                    "dart": "dart", "lua": "lua"
                }

                lang = notion_langs.get(lang.lower(), "plain text")

                # Notion code block 생성 (2000자 제한 처리, 문장 단위 분할)
                max_code_length = 2000

                if len(code_text) <= max_code_length:
                    # 코드가 2000자 이내이면 한 블록으로 생성
                    blocks.append({
                        "object": "block",
                        "type": "code",
                        "code": {
                            "rich_text": [{"type": "text", "text": {"content": code_text}}],
                            "language": lang
                        }
                    })
                else:
                    # 코드가 2000자를 초과하면 문장/문단 단위로 분할
                    logger.warning(f"Code block too long ({len(code_text)} chars), splitting at natural boundaries")
                    chunks = self._split_code_at_boundaries(code_text, max_code_length)
                    for chunk in chunks:
                        blocks.append({
                            "object": "block",
                            "type": "code",
                            "code": {
                                "rich_text": [{"type": "text", "text": {"content": chunk}}],
                                "language": lang
                            }
                        })

                i += 1  # closing ``` skip
                continue

            # 헤딩
            if line.startswith('# '):
                flush_paragraph()
                blocks.append({
                    "object": "block", "type": "heading_1",
                    "heading_1": {"rich_text": [{"text": {"content": line[2:].strip()}}]}
                })
            elif line.startswith('## '):
                flush_paragraph()
                blocks.append({
                    "object": "block", "type": "heading_2",
                    "heading_2": {"rich_text": [{"text": {"content": line[3:].strip()}}]}
                })
            elif line.startswith('### '):
                flush_paragraph()
                blocks.append({
                    "object": "block", "type": "heading_3",
                    "heading_3": {"rich_text": [{"text": {"content": line[4:].strip()}}]}
                })
            # 불릿 리스트
            elif line.startswith('- ') or line.startswith('* '):
                flush_paragraph()
                blocks.append({
                    "object": "block", "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": [{"text": {"content": line[2:].strip()}}]}
                })
            # 숫자 리스트
            elif line[0].isdigit() and line.startswith('. '):
                flush_paragraph()
                blocks.append({
                    "object": "block", "type": "numbered_list_item",
                    "numbered_list_item": {"rich_text": [{"text": {"content": line[2:].strip()}}]}
                })
            # 인용문
            elif line.startswith('> '):
                flush_paragraph()
                blocks.append({
                    "object": "block", "type": "quote",
                    "quote": {"rich_text": [{"text": {"content": line[2:].strip()}}]}
                })
            # 일반 텍스트 (문단에 추가)
            else:
                current_paragraph.append(line)

            i += 1

        flush_paragraph()
        return blocks

    def _create_paragraph_block(self, text: str) -> Dict:
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _append_children(self, block_id: str, children: List[Dict]):
        """블록 자식 추가 (배치 처리)"""
        batch_size = 50
        for i in range(0, len(children), batch_size):
            batch = children[i:i + batch_size]
            try:
                self._request("PATCH", f"/blocks/{block_id}/children", {"children": batch})
            except Exception as e:
                logger.error(f"Failed to append blocks batch {i}: {e}")

    def update_status(self, page_id: str, status: str) -> bool:
        """상태 업데이트"""
        try:
            self._request("PATCH", f"/pages/{page_id}", {
                "properties": {"상태": {"status": {"name": status}}}
            })
            return True
        except Exception:
            return False

    def get_review_done_articles(self) -> List[Dict]:
        """검토 완료 글 조회"""
        return self._query_database({"property": "상태", "status": {"equals": "검토 완료"}})
        
    def _query_database(self, filter_condition: Dict) -> List[Dict]:
        """데이터베이스 조회"""
        try:
            res = self._request("POST", f"/databases/{self.database_id}/query", {
                "filter": filter_condition
            })
            return res.get('results', [])
        except Exception:
            return []

    def update_published_url(self, page_id: str, url: str):
        """배포 URL 업데이트"""
        try:
            self._request("PATCH", f"/pages/{page_id}", {
                "properties": {"배포 URL": {"url": url}}
            })
        except Exception as e:
            logger.error(f"Failed to update published URL: {e}")

    def get_page_content(self, page_id: str) -> str:
        """페이지 본문 가져오기 (Markdown 변환)"""
        try:
            res = self._request("GET", f"/blocks/{page_id}/children")
            blocks = res.get('results', [])
            return "\n\n".join([self._block_to_text(b) for b in blocks])
        except Exception:
            return ""

    def _block_to_text(self, block: Dict) -> str:
        """블록 -> 마크다운 텍스트 변환 (개선)"""
        btype = block.get('type')
        if btype not in block:
            return ""

        # 코드 블록 처리
        if btype == 'code':
            code_data = block['code']
            language = code_data.get('language', 'plain text')

            # 코드 내용 추출
            lines = [t.get('text', {}).get('content', '') for t in code_data.get('rich_text', [])]
            code_content = ''.join(lines)

            # Javascript 코드 블록이지만 Mermaid 다이어그램인지 확인
            # Mermaid 키워드로 시작하면 Mermaid로 처리

            # 언어 확인 (대소문자 구분 없이)
            lang_lower = language.lower() if isinstance(language, str) else ''

            # 코드 내용에서 선행 공백 제거
            stripped_content = code_content.strip()

            # Mermaid 키워드 목록 (확장)
            mermaid_keywords = [
                # 다이어그램 타입
                'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
                'stateDiagram', 'stateDiagram-v2', 'entityRelationshipDiagram', 'userJourney',
                'gantt', 'pie', 'mindmap', 'timeline', 'gitgraph', 'erDiagram', 'journey',
                'pieChart', 'requirementDiagram', 'git',
                # 서브그래프 및 구조
                'subgraph', 'end[', 'end;',
                # 노드 연결 패턴 (-->, --->, -.-, ==>)
            ]

            # Mermaid 문법 패턴 확인 (전체 내용 스캔)
            is_mermaid = False

            if lang_lower == 'javascript':
                # 첫 라인 확인
                first_line = stripped_content.split('\n')[0].strip() if stripped_content else ''

                # 1. 첫 라인이 Mermaid 키워드로 시작하는지 확인
                if any(first_line.startswith(keyword) or first_line.startswith(keyword + ' ')
                       for keyword in mermaid_keywords):
                    is_mermaid = True

                # 2. 전체 내용에서 Mermaid 패턴 확인 (서브그래프, 화살표 등)
                if not is_mermaid:
                    # 서브그래프 패턴: subgraph ...
                    if 'subgraph' in stripped_content.lower():
                        is_mermaid = True
                    # 화살표 패턴: -->, --->, -.-, ==>
                    elif re.search(r'\w+\s*--?>\s*\w+', stripped_content):
                        is_mermaid = True
                    # 노드 패턴: Node1[Label], Node2(Label), Node3{Label}
                    elif re.search(r'\w+\[[^\]]+\]', stripped_content) or \
                         re.search(r'\w+\([^)]+\)', stripped_content) or \
                         re.search(r'\w+\{[^}]+\}', stripped_content):
                        is_mermaid = True

            if is_mermaid:
                logger.info(f"🔄 Converting javascript to mermaid (first_line: {stripped_content[:50]})")
                return f"```mermaid\n{code_content}\n```"

            # Notion 언어 → 마크다운 언어 매핑
            lang_map = {
                'plain text': 'text',
                'python': 'python',
                'javascript': 'javascript',
                'typescript': 'typescript',
                'java': 'java',
                'c': 'c',
                'c++': 'cpp',
                'c#': 'csharp',
                'go': 'go',
                'rust': 'rust',
                'ruby': 'ruby',
                'php': 'php',
                'swift': 'swift',
                'kotlin': 'kotlin',
                'scala': 'scala',
                'shell': 'bash',
                'bash': 'bash',
                'sql': 'sql',
                'html': 'html',
                'css': 'css',
                'json': 'json',
                'yaml': 'yaml',
                'xml': 'xml',
                'markdown': 'markdown',
                'mermaid': 'mermaid'  # Notion mermaid → markdown mermaid
            }
            md_lang = lang_map.get(language, 'text')
            return f"```{md_lang}\n{code_content}\n```"

        # 이미지 블록 처리 (Mermaid 다이어그램 이미지)
        if btype == 'image':
            image_data = block.get('image', {})
            image_type = image_data.get('type', '')

            if image_type == 'external':
                url = image_data.get('external', {}).get('url', '')
                if url:
                    # 이미지가 있는 경우 마크다운 이미지로 변환
                    # 캡션이나 alt 텍스트가 있다면 추가
                    return f"\n![Mermaid Diagram]({url})\n"
            elif image_type == 'file':
                url = image_data.get('file', {}).get('url', '')
                if url:
                    return f"\n![Mermaid Diagram]({url})\n"

            return ""  # 이미지 처리 실패

        # 테이블 처리
        if btype == 'table':
            return self._convert_table_to_markdown(block['table'])

        # 리치 텍스트 기반 블록 처리
        if 'rich_text' in block[btype]:
            texts = [t.get('text', {}).get('content', '') for t in block[btype]['rich_text']]
            text = "".join(texts)

            if btype == 'paragraph':
                # Mermaid 안내 문구 필터링
                if 'Mermaid 다이어그램' in text and '블로그에서 자동으로 다이어그램으로 렌더링됩니다' in text:
                    return ''  # 안내 문구는 제거
                return text
            if btype == 'heading_1':
                return f"# {text}"
            if btype == 'heading_2':
                return f"## {text}"
            if btype == 'heading_3':
                return f"### {text}"
            if btype == 'bulleted_list_item':
                return f"- {text}"
            if btype == 'numbered_list_item':
                return f"1. {text}"
            if btype == 'to_do':
                checked = block[btype].get('checked', False)
                checkbox = '- [x]' if checked else '- [ ]'
                return f"{checkbox} {text}"
            if btype == 'quote':
                return f"> {text}"
            if btype == 'callout':
                icon = block[btype].get('icon', {}).get('emoji', '💡')
                return f"> {icon} {text}"
            if btype == 'divider':
                return "---"
            if btype == 'toggle':
                return f"<details>\n<summary>{text}</summary>\n\n"
            if btype == 'synct_atomic_block':
                return f"```{text}\n```"

        return ""

    def _convert_table_to_markdown(self, table_data: Dict) -> str:
        """Notion 테이블을 마크다운 테이블로 변환"""
        try:
            rows = table_data.get('table_row', [])
            if not rows:
                return ""

            markdown_rows = []
            for i, row_block in enumerate(rows):
                if 'table_row' not in row_block:
                    continue
                cells = row_block['table_row'].get('cells', [])
                cell_texts = []
                for cell in cells:
                    cell_text = ''.join([t.get('text', {}).get('content', '') for t in cell])
                    cell_texts.append(cell_text.strip())

                # 첫 번째 행은 헤더로 처리
                if i == 0:
                    header = "| " + " | ".join(cell_texts) + " |"
                    separator = "|" + "|".join([" --- " for _ in cell_texts]) + "|"
                    markdown_rows.append(header)
                    markdown_rows.append(separator)
                else:
                    row = "| " + " | ".join(cell_texts) + " |"
                    markdown_rows.append(row)

            return "\n".join(markdown_rows)
        except Exception as e:
            logger.error(f"Failed to convert table to markdown: {e}")
            return ""

    def _split_code_at_boundaries(self, code_text: str, max_length: int) -> List[str]:
        """코드를 자연스러운 경계에서 분할 (줄바꿈, 쉼표, 마침표 기준)"""
        if len(code_text) <= max_length:
            return [code_text]

        chunks = []
        remaining = code_text

        while len(remaining) > max_length:
            # 현재 청크 크기
            current_chunk = remaining[:max_length]

            # 거꾸로 탐색하여 적절한 분리점 찾기
            # 우선순위: 1) 빈 줄(\n\n) 2) 쉼표(;) 3) 마침표(.) 4) 줄바꿈(\n)
            split_pos = -1

            # 1. 빈 줄(연속된 두 줄바꿈) 찾기 - 함수/클래스 구분
            last_double_newline = current_chunk.rfind('\n\n')
            if last_double_newline > max_length * 0.8:  # 최소 80%는 확보
                split_pos = last_double_newline + 2
            else:
                # 2. 쉼표(;) 찾기 - 문장 완성 기준
                last_semicolon = current_chunk.rfind(';')
                if last_semicolon > max_length * 0.85:
                    split_pos = last_semicolon + 1
                else:
                    # 3. 마침표(.) 찾기 (단, 콜론(:), 느낌표(!) 제외)
                    for punct in ['.', ':', '!']:
                        last_punct = current_chunk.rfind(punct)
                        # 다음 문자가 알파벳이나 공백인지 확인하여 실제 문장 끝인지 체크
                        if last_punct > max_length * 0.85:
                            next_char_idx = last_punct + 1
                            if next_char_idx < len(current_chunk):
                                next_char = current_chunk[next_char_idx]
                                if next_char.isalnum() or next_char.isspace():
                                    split_pos = last_punct + 1
                                    break

            # 4. 줄바꿈(\n) 찾기
            if split_pos == -1:
                last_newline = current_chunk.rfind('\n')
                if last_newline > max_length * 0.9:
                    split_pos = last_newline + 1

            # 적절한 분리점을 찾지 못하면 강제로 max_length에서 분할
            if split_pos == -1:
                split_pos = max_length

            chunks.append(remaining[:split_pos])
            remaining = remaining[split_pos:]

        # 남은 부분 추가
        if remaining:
            chunks.append(remaining)

        logger.info(f"Code split into {len(chunks)} chunks (original: {len(code_text)} chars)")
        return chunks

if __name__ == "__main__":
    pub = NotionPublisher()
    # print(pub.get_review_done_articles())