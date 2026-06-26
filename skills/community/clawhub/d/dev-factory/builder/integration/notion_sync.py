"""NotionSync - Notion 양방향 동기화"""

import json
import logging
import time
import urllib.request
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger('builder-agent.integration.notion')


class NotionSync:
    """Notion 데이터베이스와 양방향 동기화"""

    def __init__(self, database_id: str, token: Optional[str] = None):
        self.database_id = database_id
        self.token = token or self._load_token()
        self.api_base = "https://api.notion.com/v1"
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }

    def _load_token(self) -> Optional[str]:
        """.env 파일에서 Notion API 토큰 로드"""
        import os
        workspace = os.getenv("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))
        env_file = Path(workspace) / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith('NOTION_API_KEY='):
                    return line.split('=', 1)[1].strip()
        return None

    # ──────────────────────────────────────────────
    # Push: 아이디어를 Notion에 등록
    # ──────────────────────────────────────────────

    def queue_ideas(self, ideas: List[Dict], max_count: int = 10) -> int:
        """아이디어를 Notion 큐에 등록 (본문 블록 포함)"""
        if not self.token:
            logger.warning("Notion token not configured")
            return 0

        queued = 0

        for idea in ideas[:max_count]:
            try:
                # 상세 스펙 생성
                detailed_spec = self._generate_detailed_spec(idea)
                blocks = self._markdown_to_blocks(detailed_spec)
                
                logger.info(f"Generated {len(blocks)} blocks for {idea['title'][:40]}")
                
                # 페이지 생성 (속성 + children 블록)
                page_data = self._build_page_data(idea)
                
                # children 블록 추가 (최대 100개)
                if blocks:
                    page_data["children"] = blocks[:100]
                
                page_result = self._create_page(page_data)
                page_id = page_result['id']
                
                queued += 1
                logger.info(f"✅ Queued: {idea['title'][:50]} (with {len(blocks[:100])} blocks)")

                time.sleep(0.5)  # Rate limit

            except Exception as e:
                logger.error(f"Failed to queue {idea['title'][:30]}: {e}")

        return queued

    def _build_page_data(self, idea: Dict) -> Dict:
        """Notion 페이지 데이터 생성 (속성만)"""
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "내용": {
                    "title": [{"text": {"content": idea['title'][:100]}}]
                },
                "상태": {"status": {"name": "아이디어"}},
                "카테고리": {"select": {"name": self._map_category(idea.get('source', 'manual'))}},
            }
        }

        # 간단한 요약만 속성에 저장
        if idea.get('description'):
            summary = idea['description'][:200]  # 200자 제한
            data["properties"]["도구 설명"] = {
                "rich_text": [{"text": {"content": summary}}]
            }

        # URL
        if idea.get('url'):
            data["properties"]["URL"] = {"url": idea['url']}

        # 테그
        tags = [{"name": "아이디어"}]
        if idea.get('source') == 'cve_database':
            tags.append({"name": "CVE"})
        elif idea.get('source') == 'security_news':
            tags.append({"name": "보안"})
        elif idea.get('source') == 'github_trending':
            tags.append({"name": "GitHub"})
        
        data["properties"]["테그"] = {"multi_select": tags}

        return data

    def _add_page_content(self, page_id: str, markdown_content: str):
        """페이지 본문에 블록 추가 (배치 처리)"""
        
        # 마크다운을 Notion 블록으로 변환
        blocks = self._markdown_to_blocks(markdown_content)
        
        logger.info(f"Generated {len(blocks)} blocks for page content")
        
        # 100개씩 나누어 전송 (Notion API 제한)
        batch_size = 100
        total_batches = (len(blocks) + batch_size - 1) // batch_size
        
        for i in range(0, len(blocks), batch_size):
            batch = blocks[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            try:
                url = f"{self.api_base}/blocks/{page_id}/children/append"
                
                req = urllib.request.Request(
                    url,
                    data=json.dumps({"children": batch}).encode('utf-8'),
                    headers=self.headers
                )
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    if response.status == 200:
                        logger.info(f"Successfully added batch {batch_num}/{total_batches} ({len(batch)} blocks)")
                    else:
                        logger.warning(f"Failed to add batch {batch_num}: {response.status}")
                        
            except urllib.error.HTTPError as e:
                # 에러 응답 본문 읽기
                error_body = e.read().decode('utf-8')
                logger.error(f"Notion API Error (batch {batch_num}): {e.code} {e.reason}")
                logger.error(f"Error body: {error_body}")
                logger.error(f"Failed batch size: {len(batch)} blocks")
                logger.error(f"First block type: {batch[0].get('type', 'unknown') if batch else 'empty'}")
                
                # 첫 번째 블록만 자세히 로깅
                if batch:
                    logger.error(f"First block: {json.dumps(batch[0], indent=2, ensure_ascii=False)}")
                
                raise
            
            # Rate limit 준수 (배치 간 0.5초 대기)
            if i + batch_size < len(blocks):
                time.sleep(0.5)
    
    def _markdown_to_blocks(self, markdown: str) -> List[Dict]:
        """마크다운을 Notion 블록 배열로 변환 (최적화)"""
        
        blocks = []
        lines = markdown.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 빈 줄 스킵
            if not line.strip():
                i += 1
                continue
            
            # Heading 1 (## )
            if line.startswith('## '):
                text = self._clean_markdown(line[3:])
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": text[:100]}}]
                    }
                })
            
            # Heading 2 (### )
            elif line.startswith('### '):
                text = self._clean_markdown(line[4:])
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": text[:100]}}]
                    }
                })
            
            # Bullet list (- or •)
            elif line.strip().startswith('- ') or line.strip().startswith('• '):
                text = self._clean_markdown(line.strip()[2:])
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
                    }
                })
            
            # Checkbox (- [ ])
            elif line.strip().startswith('- [ ]'):
                text = self._clean_markdown(line.strip()[5:].strip())
                blocks.append({
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
                        "checked": False
                    }
                })
            
            # Code block (```)
            elif line.strip().startswith('```'):
                code_lines = []
                i += 1  # 시작 ``` 스킵
                
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                code_content = '\n'.join(code_lines)[:2000]  # 2000자 제한
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": code_content}}],
                        "language": "python"
                    }
                })
            
            # Divider (---)
            elif line.strip() == '---':
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
            
            # Normal paragraph
            else:
                # 텍스트 정리 (마크다운 문법 제거)
                text = self._clean_markdown(line)
                
                if text:
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
                        }
                    })
            
            i += 1
        
        return blocks
    
    def _clean_markdown(self, text: str) -> str:
        """마크다운 문법 정리"""
        import re
        
        # **bold** → bold
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        
        # *italic* → italic
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        
        # `code` → code
        text = re.sub(r'`(.+?)`', r'\1', text)
        
        # [link](url) → link
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        
        return text.strip()

    def _generate_detailed_spec(self, idea: Dict) -> str:
        """Notion 마크다운 형식의 상세 스펙 생성"""
        
        source = idea.get('source', 'manual')
        
        if source == 'cve_database':
            return self._generate_cve_spec(idea)
        elif source == 'security_news':
            return self._generate_security_news_spec(idea)
        elif source == 'github_trending':
            return self._generate_github_spec(idea)
        else:
            return self._generate_generic_spec(idea)

    def _generate_cve_spec(self, idea: Dict) -> str:
        """CVE 기반 프로젝트 스펙"""
        
        cve_id = idea.get('cve_id', 'Unknown')
        severity = idea.get('severity', 'MEDIUM')
        score = idea.get('score', 0.5)
        complexity = idea.get('complexity', 'medium')
        
        spec = f"""## 📋 프로젝트 개요
{idea.get('description', '자동 생성된 보안 스캐너')}

## 🔍 CVE 정보
- **CVE ID**: `{cve_id}`
- **심각도**: {severity}
- **점수**: {score:.2f}/1.00
- **출처**: CVE Database (NVD)
- **참조**: [NVD 상세 정보]({idea.get('url', '')})

## 🎯 개발 목표
{cve_id} 취약점을 탐지하고 분석하는 CLI 도구 개발

### 주요 기능
1. **취약점 스캔**: 대상 시스템에서 {cve_id} 취약점 탐지
2. **영향 분석**: 취약점의 영향도 평가 및 보고서 생성
3. **완화 가이드**: 취약점 해결을 위한 권장 사항 제공
4. **결과 출력**: JSON/CSV/TXT 형식으로 결과 저장

## 💻 기술 스펙

### 복잡도: {complexity.upper()}
- 예상 개발 시간: 2-4시간
- 필요 기술: Python, API 호출, 데이터 파싱

### 기술 스택
- **Language**: Python 3.9+
- **HTTP Client**: `requests` or `urllib`
- **Testing**: `pytest` + 80% 커버리지
- **Packaging**: `setuptools` + `wheel`

### 파일 구조 (제안)
```
{cve_id.lower().replace('-', '_')}_scanner/
├── src/
│   ├── __init__.py
│   ├── scanner.py      # 메인 스캔 로직
│   ├── api_client.py   # NVD API 클라이언트
│   ├── analyzer.py     # 취약점 분석
│   └── reporter.py     # 결과 리포트 생성
├── tests/
│   ├── __init__.py
│   ├── test_scanner.py
│   ├── test_api_client.py
│   └── test_analyzer.py
├── README.md
├── requirements.txt
└── setup.py
```

### 핵심 API
```python
# scanner.py
class CVEScanner:
    def scan(target: str) -> ScanResult:
        \"\"\"대상 시스템 스캔\"\"\"
        pass
    
    def get_cve_details(cve_id: str) -> CVEDetails:
        \"\"\"CVE 상세 정보 조회\"\"\"
        pass
```

## ✅ 성공 기준
- [ ] CVE 상세 정보 정상 조회
- [ ] 스캔 기능 구현 완료
- [ ] JSON/CSV 리포트 생성
- [ ] unittest 5개 이상 작성
- [ ] 테스트 커버리지 80%+ 달성
- [ ] README.md 작성 (사용법 포함)
- [ ] requirements.txt 생성

## 📚 참고 자료
- [NVD API Documentation](https://nvd.nist.gov/developers/vulnerabilities)
- [CVE-2026-3377 상세]({idea.get('url', '')})
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## 🚀 실행 예시
```bash
# 설치
pip install {cve_id.lower().replace('-', '_')}_scanner

# 스캔 실행
{cve_id.lower().replace('-', '_')}_scanner --target https://example.com --output report.json

# 결과 확인
cat report.json | jq '.vulnerabilities'
```

---
*자동 생성됨: Builder Agent v5.0*
*생성 일시: {self._get_timestamp()}*
"""
        return spec

    def _generate_security_news_spec(self, idea: Dict) -> str:
        """Security News 기반 프로젝트 스펙"""
        
        keyword = idea.get('keyword', 'security')
        score = idea.get('score', 0.5)
        complexity = idea.get('complexity', 'medium')
        
        spec = f"""## 📋 프로젝트 개요
{idea.get('description', '최신 보안 뉴스 기반 도구')}

## 🔍 뉴스 정보
- **키워드**: {keyword}
- **점수**: {score:.2f}/1.00
- **출처**: Security News (brave-search)
- **참조**: [원문 기사]({idea.get('url', '')})

## 🎯 개발 목표
"{keyword}" 관련 보안 위협 탐지 또는 방어 도구 개발

### 주요 기능
1. **위협 탐지**: {keyword} 관련 위협 요소 식별
2. **실시간 모니터링**: 지속적인 보안 상태 확인
3. **알림 시스템**: 위협 감지 시 즉시 알림
4. **로그 분석**: 보안 로그 분석 및 시각화

## 💻 기술 스펙

### 복잡도: {complexity.upper()}
- 예상 개발 시간: 3-6시간
- 필요 기술: Python, 정규표현식, 파일 시스템

### 기술 스택
- **Language**: Python 3.9+
- **Pattern Matching**: `re` (정규표현식)
- **Testing**: `pytest`
- **Logging**: `logging` module

### 파일 구조 (제안)
```
{keyword.lower().replace(' ', '_')}_detector/
├── src/
│   ├── __init__.py
│   ├── detector.py     # 탐지 로직
│   ├── patterns.py     # 시그니처/패턴
│   ├── monitor.py      # 모니터링
│   └── alerter.py      # 알림 발송
├── tests/
│   ├── __init__.py
│   ├── test_detector.py
│   └── test_patterns.py
├── config.yaml         # 설정 파일
├── README.md
└── requirements.txt
```

### 핵심 API
```python
# detector.py
class ThreatDetector:
    def scan_logs(log_path: str) -> List[Threat]:
        \"\"\"로그 파일 스캔\"\"\"
        pass
    
    def detect_pattern(line: str) -> Optional[Threat]:
        \"\"\"패턴 매칭 탐지\"\"\"
        pass
```

## ✅ 성공 기준
- [ ] 위협 탐지 기능 구현
- [ ] 실시간 모니터링 기능
- [ ] 알림 발송 기능
- [ ] unittest 5개 이상
- [ ] 테스트 커버리지 80%+
- [ ] README.md 작성
- [ ] 샘플 로그 파일로 테스트

## 📚 참고 자료
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Security Best Practices](https://www.sans.org/security-resources/)
- [Python Security Guide](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## 🚀 실행 예시
```bash
# 설치
pip install {keyword.lower().replace(' ', '_')}_detector

# 로그 스캔
{keyword.lower().replace(' ', '_')}_detector --log /var/log/auth.log --output threats.json

# 실시간 모니터링
{keyword.lower().replace(' ', '_')}_detector --monitor --alert-email admin@example.com
```

---
*자동 생성됨: Builder Agent v5.0*
*생성 일시: {self._get_timestamp()}*
"""
        return spec

    def _generate_github_spec(self, idea: Dict) -> str:
        """GitHub Trending 기반 프로젝트 스펙"""
        
        stars = idea.get('stars', 0)
        language = idea.get('language', 'Python')
        score = idea.get('score', 0.5)
        complexity = idea.get('complexity', 'medium')
        
        spec = f"""## 📋 프로젝트 개요
{idea.get('description', 'GitHub Trending 기반 프로젝트')}

## 🔍 GitHub 정보
- **별점**: {stars:,} ⭐
- **언어**: {language}
- **점수**: {score:.2f}/1.00
- **출처**: GitHub Trending
- **참조**: [GitHub Repository]({idea.get('url', '')})

## 🎯 개발 목표
인기 있는 GitHub 프로젝트를 참고한 유사 도구 또는 개선판 개발

### 접근 방식
1. **Clone & Analyze**: 원본 프로젝트 분석
2. **Improve**: 기능 개선 또는 단순화
3. **Korean Support**: 한국어 문서화 추가
4. **Extend**: 새로운 기능 추가

### 주요 기능
1. **핵심 기능 구현**: 원본의 핵심 기능 재현
2. **개선 사항 적용**: 사용성/성능 개선
3. **확장 기능**: 추가 기능 구현
4. **문서화**: 한국어 README + 사용 가이드

## 💻 기술 스펙

### 복잡도: {complexity.upper()}
- 예상 개발 시간: 4-8시간
- 필요 기술: {language}, Git, 문서화

### 기술 스택
- **Language**: {language}
- **Version Control**: Git
- **Testing**: 적절한 테스트 프레임워크
- **Documentation**: Markdown

### 파일 구조 (제안)
```
project_name/
├── src/
│   ├── core/           # 핵심 로직
│   ├── utils/          # 유틸리티
│   └── cli.py          # CLI 인터페이스
├── tests/
│   └── test_*.py
├── docs/
│   ├── README_KO.md    # 한국어 문서
│   └── USAGE.md        # 사용 가이드
├── examples/           # 예제 코드
├── README.md
└── requirements.txt
```

## ✅ 성공 기준
- [ ] 핵심 기능 구현 완료
- [ ] 원본 대비 개선 사항 2개 이상
- [ ] 한국어 문서 작성
- [ ] unittest 작성
- [ ] 테스트 커버리지 80%+
- [ ] 예제 코드 3개 이상
- [ ] CI/CD 설정 (선택)

## 📚 참고 자료
- [원본 Repository]({idea.get('url', '')})
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Open Source Best Practices](https://opensource.guide/)

## 🔄 개선 아이디어
1. 성능 최적화 (캐싱, 병렬 처리)
2. CLI UX 개선 (진행률 표시, 색상 출력)
3. 설정 파일 지원 (YAML/JSON)
4. 플러그인 시스템
5. 웹 UI (선택)

---
*자동 생성됨: Builder Agent v5.0*
*생성 일시: {self._get_timestamp()}*
"""
        return spec

    def _generate_generic_spec(self, idea: Dict) -> str:
        """일반 프로젝트 스펙"""
        
        score = idea.get('score', 0.5)
        complexity = idea.get('complexity', 'medium')
        
        spec = f"""## 📋 프로젝트 개요
{idea.get('description', '자동 생성된 프로젝트 아이디어')}

## 🔍 프로젝트 정보
- **점수**: {score:.2f}/1.00
- **복잡도**: {complexity.upper()}
- **출처**: {idea.get('source', 'manual')}

## 🎯 개발 목표
명확하고 유지보수 가능한 프로젝트 개발

### 주요 기능
1. **핵심 기능**: 프로젝트의 주요 기능
2. **입출력**: 데이터 입력 및 결과 출력
3. **에러 처리**: 예외 상황 핸들링
4. **문서화**: 사용법 및 API 문서

## 💻 기술 스펙

### 복잡도: {complexity.upper()}
- 예상 개발 시간: 2-4시간
- 필요 기술: Python, 기본 알고리즘

### 기술 스택
- **Language**: Python 3.9+
- **Testing**: pytest
- **Documentation**: Markdown

### 파일 구조 (제안)
```
project/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── README.md
└── requirements.txt
```

## ✅ 성공 기준
- [ ] 핵심 기능 구현
- [ ] unittest 작성
- [ ] 테스트 커버리지 80%+
- [ ] README.md 작성
- [ ] 에러 처리 구현

---
*자동 생성됨: Builder Agent v5.0*
*생성 일시: {self._get_timestamp()}*
"""
        return spec

    def _map_category(self, source: str) -> str:
        """출처별 카테고리 매핑"""
        mapping = {
            'cve_database': 'CLI',
            'security_news': 'CLI',
            'github_trending': 'AI-Agent',
            'manual': 'CLI'
        }
        return mapping.get(source, '기타')
    
    def _get_timestamp(self) -> str:
        """현재 타임스탬프 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _create_page(self, page_data: Dict) -> Dict:
        """Notion 페이지 생성"""
        req = urllib.request.Request(
            f"{self.api_base}/pages",
            data=json.dumps(page_data).encode('utf-8'),
            headers=self.headers
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())

    # ──────────────────────────────────────────────
    # Pull: Notion에서 "개발 시작" 상태 프로젝트 조회
    # ──────────────────────────────────────────────

    def get_ready_projects(self) -> List[Dict]:
        """Notion에서 "개발중" 상태인 프로젝트 조회"""
        if not self.token:
            return []

        try:
            query_data = {
                "filter": {
                    "property": "상태",
                    "status": {"equals": "개발중"}
                }
            }

            req = urllib.request.Request(
                f"{self.api_base}/databases/{self.database_id}/query",
                data=json.dumps(query_data).encode('utf-8'),
                headers=self.headers
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())

            projects = []
            for page in result.get('results', []):
                projects.append(self._parse_page(page))

            return projects

        except Exception as e:
            logger.warning("Failed to query Notion: %s", e)
            return []

    def _parse_page(self, page: Dict) -> Dict:
        """Notion 페이지를 ProjectIdea 형식으로 파싱"""
        props = page.get('properties', {})

        title = ""
        if '내용' in props and 'title' in props['내용']:
            titles = props['내용']['title']
            if titles:
                title = titles[0].get('text', {}).get('content', '')

        description = ""
        if '도구 설명' in props and 'rich_text' in props['도구 설명']:
            texts = props['도구 설명']['rich_text']
            if texts:
                description = texts[0].get('text', {}).get('content', '')

        url = ""
        if 'URL' in props and 'url' in props['URL']:
            url = props['URL']['url']

        return {
            'title': title,
            'description': description,
            'url': url,
            'notion_page_id': page['id']
        }

    # ──────────────────────────────────────────────
    # Update: 빌드 결과에 따라 상태 업데이트
    # ──────────────────────────────────────────────

    def update_status(self, page_id: str, status: str) -> bool:
        """페이지 상태 업데이트"""
        if not self.token:
            return False

        try:
            update_data = {
                "properties": {
                    "상태": {"status": {"name": status}}
                }
            }

            req = urllib.request.Request(
                f"{self.api_base}/pages/{page_id}",
                data=json.dumps(update_data).encode('utf-8'),
                headers=self.headers,
                method='PATCH'
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200

        except Exception as e:
            logger.warning("Failed to update status: %s", e)
            return False
