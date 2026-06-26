# Builder Agent Discovery Integration

## 개요

agent-browser를 활용하여 GitHub Trending, CVE Database, Security News에서 자동으로 프로젝트 아이디어를 발굴한다.

## Discovery Sources

### 1. GitHub Trending
**URL**: https://github.com/trending
**주기**: 매일 08:00, 20:00
**필터**: Python, Security, CLI, DevTools

### 2. CVE Database
**URL**: https://cve.mitre.org, https://nvd.nist.gov
**주기**: 6시간마다
**필터**: High/Critical severity

### 3. Security News
**URL**: https://www.krcert.or.kr, https://dailysecu.com
**주기**: 1시간마다
**필터**: 취약점, 악성코드, 해킹

## agent-browser 워크플로우

### 1. GitHub Trending 크롤링
```python
async def discover_from_github_trending() -> List[dict]:
    """GitHub Trending에서 아이디어 발굴"""
    
    # agent-browser로 페이지 접근
    browser = AgentBrowser()
    await browser.navigate("https://github.com/trending/python?since=daily")
    
    # 레포지토리 정보 추출
    repos = await browser.extract([
        {"selector": "h2 a", "attr": "href"},  # 레포 URL
        {"selector": "p.col-9", "attr": "text"},  # 설명
        {"selector": "span.d-inline-block.ml-0", "attr": "text"}  # 스타 수
    ])
    
    # 보안/DevOps 관련 필터링
    ideas = []
    for repo in repos:
        if any(kw in repo['description'].lower() for kw in 
               ['security', 'scanner', 'vulnerability', 'cli', 'tool', 'automation']):
            ideas.append({
                'title': f"Clone/Improve: {repo['name']}",
                'description': repo['description'],
                'source': 'github_trending',
                'url': repo['url'],
                'complexity': 'medium',
                'priority': 'high' if repo['stars'] > 1000 else 'medium'
            })
    
    return ideas
```

### 2. CVE Database 모니터링
```python
async def discover_from_cve() -> List[dict]:
    """CVE에서 취약점 기반 도구 아이디어 발굴"""
    
    browser = AgentBrowser()
    
    # NVD API 사용 (더 안정적)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://services.nvd.nist.gov/rest/json/cves/2.0",
            params={
                "pubStartDate": (datetime.now() - timedelta(days=1)).isoformat(),
                "cvssV3Severity": "HIGH,CRITICAL"
            }
        )
    
    cves = response.json()['vulnerabilities']
    
    ideas = []
    for cve in cves[:10]:  # 상위 10개만
        cve_id = cve['cve']['id']
        description = cve['cve']['descriptions'][0]['value']
        
        ideas.append({
            'title': f"CVE Scanner: {cve_id}",
            'description': f"Scanner for {description[:200]}",
            'source': 'cve_database',
            'cve_id': cve_id,
            'complexity': 'medium',
            'priority': 'high'
        })
    
    return ideas
```

### 3. Security News 스크래핑
```python
async def discover_from_security_news() -> List[dict]:
    """보안 뉴스에서 도구 아이디어 발굴"""
    
    sources = [
        "https://www.krcert.or.kr/krcert/secNoticeList.do",
        "https://dailysecu.com/news/articleList.html",
        "https://www.boho.or.kr/krcert/secNoticeList.do"
    ]
    
    browser = AgentBrowser()
    ideas = []
    
    for source in sources:
        await browser.navigate(source)
        
        # 뉴스 헤드라인 추출
        headlines = await browser.extract([
            {"selector": "a[href*='article']", "attr": "text"},
            {"selector": "a[href*='article']", "attr": "href"}
        ])
        
        for headline in headlines[:5]:
            # 키워드 기반 도구 아이디어 생성
            if any(kw in headline['text'] for kw in 
                   ['취약점', '랜섬웨어', '악성코드', '해킹', '공격']):
                
                tool_type = infer_tool_type(headline['text'])
                
                ideas.append({
                    'title': f"Security Tool: {tool_type}",
                    'description': f"Based on: {headline['text']}",
                    'source': 'security_news',
                    'url': headline['url'],
                    'complexity': 'medium',
                    'priority': 'medium'
                })
    
    return ideas

def infer_tool_type(headline: str) -> str:
    """뉴스 헤드라인에서 도구 타입 추론"""
    
    if '취약점' in headline:
        return "Vulnerability Scanner"
    elif '랜섬웨어' in headline:
        return "Ransomware Detector"
    elif '악성코드' in headline:
        return "Malware Analyzer"
    elif '해킹' in headline:
        return "Intrusion Detector"
    else:
        return "Security Monitor"
```

## Notion 큐 통합

### 큐 등록
```python
async def queue_idea_to_notion(idea: dict):
    """Notion 큐에 아이디어 등록"""
    
    notion = NotionClient(os.getenv('NOTION_API_KEY'))
    database_id = os.getenv('PROJECT_DATABASE_ID')
    
    # 중복 체크
    existing = await notion.query_database(
        database_id,
        filter={"property": "Title", "title": {"equals": idea['title']}}
    )
    
    if existing['results']:
        return  # 이미 존재
    
    # 새 아이디어 등록
    await notion.create_page(
        database_id,
        properties={
            "Title": {"title": [{"text": {"content": idea['title']}}]},
            "Status": {"select": {"name": "Idea"}},
            "Priority": {"select": {"name": idea['priority']}},
            "Source": {"select": {"name": idea['source']}},
            "Complexity": {"select": {"name": idea['complexity']}},
            "Description": {"rich_text": [{"text": {"content": idea['description']}}]},
            "URL": {"url": idea.get('url', '')},
            "Created": {"date": {"start": datetime.now().isoformat()}}
        }
    )
```

## Discovery 스케줄러

### config.yaml
```yaml
discovery:
  enabled: true
  
  sources:
    github_trending:
      enabled: true
      schedule: "0 8,20 * * *"  # 매일 08:00, 20:00
      max_ideas: 5
      
    cve_database:
      enabled: true
      schedule: "0 */6 * * *"  # 6시간마다
      max_ideas: 3
      
    security_news:
      enabled: true
      schedule: "0 * * * *"  # 매시간
      max_ideas: 5
  
  filters:
    keywords:
      - security
      - scanner
      - vulnerability
      - cli
      - tool
      - automation
      - devops
    
    exclude_keywords:
      - tutorial
      - example
      - demo
      - learning
  
  notion:
    database_id: "${PROJECT_DATABASE_ID}"
    auto_queue: true
    max_queue_size: 50
```

## 메모리 연동

### 이전 아이디어와 중복 방지
```python
async def is_duplicate_idea(idea: dict) -> bool:
    """elite-memory에서 이전 아이디어 검색"""
    
    # 1. Notion에서 체크
    notion_existing = await check_notion_queue(idea['title'])
    if notion_existing:
        return True
    
    # 2. elite-memory에서 체크
    memory_hits = memory_recall(
        query=f"project idea {idea['title']}",
        limit=5
    )
    
    for hit in memory_hits:
        if similarity(idea['title'], hit['text']) > 0.8:
            return True
    
    return False
```

### 유사 프로젝트 컨텍스트 수집
```python
async def gather_context_for_idea(idea: dict) -> dict:
    """byterover로 유사 프로젝트 컨텍스트 수집"""
    
    context = {
        'similar_projects': [],
        'failed_patterns': [],
        'success_patterns': []
    }
    
    # 1. 유사 프로젝트 검색 (byterover)
    brv_results = brv_search(idea['title'])
    context['similar_projects'] = brv_results[:5]
    
    # 2. 실패 패턴 검색 (self-improving)
    corrections = load_corrections()
    context['failed_patterns'] = [
        c for c in corrections 
        if any(kw in c['context'].lower() for kw in idea['title'].lower().split())
    ][:3]
    
    # 3. 성공 패턴 검색 (elite-memory)
    success = memory_recall(query=f"successful {idea['title']}", limit=3)
    context['success_patterns'] = success
    
    return context
```

## 구현 체크리스트

- [ ] agent-browser 초기화
- [ ] GitHub Trending 크롤러
- [ ] CVE Database 모니터링
- [ ] Security News 스크래퍼
- [ ] Notion 큐 연동
- [ ] 중복 방지 로직
- [ ] 메모리 연동
- [ ] 스케줄러 등록
- [ ] 에러 핸들링
- [ ] 로깅 시스템
