# 환경 설정 가이드

## 1. PostgreSQL + pgvector 설치

### macOS (Homebrew)

```bash
# PostgreSQL 설치
brew install postgresql@15
brew services start postgresql@15

# pgvector 설치
brew install pgvector

# DB 생성
createdb biddb

# pgvector 확장 활성화
psql -d biddb -c "CREATE EXTENSION IF NOT EXISTS vector;"
psql -d biddb -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

### Ubuntu/Debian

```bash
# PostgreSQL 설치
sudo apt update
sudo apt install postgresql-15 postgresql-contrib-15

# pgvector 설치
sudo apt install postgresql-15-pgvector

# DB 생성
sudo -u postgres createdb biddb
sudo -u postgres psql -d biddb -c "CREATE EXTENSION IF NOT EXISTS vector;"
sudo -u postgres psql -d biddb -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

### Windows

```powershell
# 1. PostgreSQL 15+ 설치: https://www.postgresql.org/download/windows/
# 2. pgvector 빌드 또는 미리 컴파일된 바이너리 사용:
#    https://github.com/pgvector/pgvector#windows

# DB 생성 (pgAdmin 또는 psql)
createdb biddb
psql -d biddb -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Docker (이식성 최고)

```bash
docker run -d \
  --name biddb \
  -e POSTGRES_DB=biddb \
  -e POSTGRES_USER=biduser \
  -e POSTGRES_PASSWORD=bidpass \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

## 2. 스키마 초기화

```bash
# SQL 파일로 직접 실행
psql -d biddb -f references/db_schema.sql

# 또는 스크립트로 실행
python3 scripts/vectorizer.py init-db --db-url "postgresql://user:pass@localhost:5432/biddb"
```

## 3. Python 패키지 설치

```bash
pip install --break-system-packages \
  psycopg2-binary \
  pgvector \
  sentence-transformers \
  pdfplumber \
  PyMuPDF \
  python-docx \
  beautifulsoup4 \
  requests \
  lxml
```

### HWP 지원 (선택)

```bash
# pyhwp: HWP 텍스트 추출
pip install --break-system-packages pyhwp

# HWPX: ZIP 기반 XML이므로 별도 패키지 불필요 (표준 라이브러리로 처리)
```

### 임베딩 제공자별 추가 패키지

```bash
# OpenAI 사용 시
pip install --break-system-packages openai

# Ollama 사용 시 (서버 별도 설치 필요)
# https://ollama.com
pip install --break-system-packages ollama
```

## 4. 환경변수 설정

`~/.bashrc` 또는 `~/.zshrc`에 추가:

```bash
# PostgreSQL
export DATABASE_URL="postgresql://user:pass@localhost:5432/biddb"

# 임베딩 (기본값: sentence_transformers)
export EMBEDDING_PROVIDER=sentence_transformers
# export EMBEDDING_PROVIDER=openai
# export OPENAI_API_KEY=sk-...
# export EMBEDDING_PROVIDER=ollama
# export OLLAMA_BASE_URL=http://localhost:11434

# Notion
export NOTION_API_KEY=ntn_...
# export NOTION_DATABASE_ID=...  # 선택: 기본 DB ID
```

## 5. Notion API 설정

1. https://www.notion.so/my-integrations 에서 새 Integration 생성
2. 토큰(ntn_...)을 `NOTION_API_KEY`에 설정
3. 대상 Notion 페이지/DB에서 "연결" → 생성한 Integration 추가
4. 데이터베이스 ID는 Notion URL에서 추출:
   `https://www.notion.so/workspace/DATABASE_ID?v=...`

## 6. 설치 확인

```bash
python3 scripts/vectorizer.py init-db
# → "DB 초기화 완료" 메시지 확인

python3 scripts/document_parser.py --help
# → 사용법 출력 확인

python3 scripts/notion_builder.py --help
# → 사용법 출력 확인
```
