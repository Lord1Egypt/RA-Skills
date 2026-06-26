#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
입찰 제안서 벡터화 엔진
PostgreSQL + pgvector를 사용하여 입찰 공고 데이터를 임베딩하고 검색하는 도구

특징:
- 여러 임베딩 제공자 지원 (sentence-transformers, OpenAI, Ollama)
- 시맨틱 청크 분할
- 코사인 거리 기반 유사도 검색
- 환경 변수를 통한 유연한 설정
"""

import sys
import os
import json
import logging
import argparse
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


@dataclass
class EmbeddingConfig:
    """임베딩 설정"""
    provider: str
    dimension: int
    batch_size: int = 32


class EmbeddingProvider:
    """임베딩 제공자 기본 클래스"""

    def __init__(self, config: EmbeddingConfig):
        self.config = config

    def embed(self, texts: List[str]) -> List[List[float]]:
        """텍스트 목록을 임베딩으로 변환"""
        raise NotImplementedError

    def embed_single(self, text: str) -> List[float]:
        """단일 텍스트를 임베딩으로 변환"""
        return self.embed([text])[0]


class SentenceTransformersProvider(EmbeddingProvider):
    """Sentence Transformers 임베딩 제공자"""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Loaded sentence-transformers model: all-MiniLM-L6-v2")
        except ImportError:
            logger.error("sentence-transformers not installed")
            raise

    def embed(self, texts: List[str]) -> List[List[float]]:
        """배치로 텍스트를 임베딩"""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()


class OpenAIProvider(EmbeddingProvider):
    """OpenAI 임베딩 제공자"""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            raise ValueError("OPENAI_API_KEY required for OpenAI provider")

        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized: text-embedding-3-small")
        except ImportError:
            logger.error("openai package not installed")
            raise

    def embed(self, texts: List[str]) -> List[List[float]]:
        """OpenAI API를 사용해 텍스트를 임베딩"""
        embeddings = []
        # Process in batches to avoid rate limits
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )
            embeddings.extend([item.embedding for item in response.data])
            logger.debug(f"Embedded batch {i//self.config.batch_size + 1}")
        return embeddings


class OllamaProvider(EmbeddingProvider):
    """Ollama 임베딩 제공자"""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        try:
            import requests
            self.base_url = base_url
            self.session = requests.Session()
            # Test connection
            response = self.session.get(f"{base_url}/api/tags", timeout=5)
            response.raise_for_status()
            logger.info(f"Connected to Ollama at {base_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            raise

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Ollama를 사용해 텍스트를 임베딩"""
        import requests
        embeddings = []
        for text in texts:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": "nomic-embed-text", "prompt": text},
                    timeout=30
                )
                response.raise_for_status()
                embedding = response.json()["embedding"]
                embeddings.append(embedding)
            except Exception as e:
                logger.error(f"Failed to embed text with Ollama: {e}")
                raise
        return embeddings


def get_embedding_provider() -> EmbeddingProvider:
    """환경 변수와 설치된 패키지에 따라 임베딩 제공자 선택"""
    provider_name = os.getenv("EMBEDDING_PROVIDER", "sentence_transformers").lower()

    # Try the requested provider, with fallback chain
    providers_to_try = []

    if provider_name == "sentence_transformers":
        providers_to_try = [
            ("sentence_transformers", 384),
            ("openai", 1536),
            ("ollama", 768),
        ]
    elif provider_name == "openai":
        providers_to_try = [
            ("openai", 1536),
            ("sentence_transformers", 384),
            ("ollama", 768),
        ]
    elif provider_name == "ollama":
        providers_to_try = [
            ("ollama", 768),
            ("sentence_transformers", 384),
            ("openai", 1536),
        ]
    else:
        logger.error(f"Unknown embedding provider: {provider_name}")
        providers_to_try = [
            ("sentence_transformers", 384),
            ("openai", 1536),
            ("ollama", 768),
        ]

    last_error = None
    for provider_name, dimension in providers_to_try:
        try:
            config = EmbeddingConfig(provider=provider_name, dimension=dimension)

            if provider_name == "sentence_transformers":
                logger.info(f"Attempting to load {provider_name} (dim={dimension})")
                return SentenceTransformersProvider(config)
            elif provider_name == "openai":
                logger.info(f"Attempting to load {provider_name} (dim={dimension})")
                return OpenAIProvider(config)
            elif provider_name == "ollama":
                logger.info(f"Attempting to load {provider_name} (dim={dimension})")
                return OllamaProvider(config)
        except Exception as e:
            logger.warning(f"Failed to load {provider_name}: {e}")
            last_error = e
            continue

    logger.error(f"All embedding providers failed. Last error: {last_error}")
    raise RuntimeError("No embedding provider available")


def get_db_connection():
    """데이터베이스 연결 생성"""
    try:
        import psycopg2
    except ImportError:
        logger.error("psycopg2 not installed")
        raise

    # Try DATABASE_URL first
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        try:
            return psycopg2.connect(db_url)
        except Exception as e:
            logger.error(f"Failed to connect via DATABASE_URL: {e}")
            raise

    # Fall back to individual parameters
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    database = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")

    if not database or not user:
        logger.error("DATABASE_URL or PGDATABASE/PGUSER environment variables required")
        raise ValueError("Database configuration missing")

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


def init_db(db_url: Optional[str] = None):
    """데이터베이스 초기화 및 스키마 생성"""
    if db_url:
        os.environ["DATABASE_URL"] = db_url

    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Check pgvector extension
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        logger.info("pgvector extension created/verified")

        # Get embedding dimension from current provider
        provider = get_embedding_provider()
        dim = provider.config.dimension
        logger.info(f"Using embedding dimension: {dim}")

        # Create tables with appropriate vector dimension
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS bid_projects (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                project_name VARCHAR(500) NOT NULL,
                announcement_no VARCHAR(100),
                issuing_org VARCHAR(255),
                project_type VARCHAR(50),
                announcement_date DATE,
                submission_deadline TIMESTAMP WITH TIME ZONE,
                budget_range VARCHAR(100),
                location VARCHAR(255),
                description TEXT,
                raw_text TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS bid_qualifications (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                project_id UUID NOT NULL REFERENCES bid_projects(id) ON DELETE CASCADE,
                requirement VARCHAR(500),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS bid_documents (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                project_id UUID NOT NULL REFERENCES bid_projects(id) ON DELETE CASCADE,
                document_name VARCHAR(255),
                document_type VARCHAR(100),
                requirement TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS bid_evaluation_criteria (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                project_id UUID NOT NULL REFERENCES bid_projects(id) ON DELETE CASCADE,
                criteria_name VARCHAR(255),
                criteria_description TEXT,
                weight NUMERIC(5,2),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS bid_embeddings (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                project_id UUID NOT NULL REFERENCES bid_projects(id) ON DELETE CASCADE,
                chunk_type VARCHAR(100) NOT NULL,
                chunk_text TEXT NOT NULL,
                embedding vector({dim}) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_bid_embeddings_project_id ON bid_embeddings(project_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_bid_embeddings_chunk_type ON bid_embeddings(chunk_type);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_bid_embeddings_embedding ON bid_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists=100);")

        conn.commit()
        logger.info("Database schema initialized successfully")
        return {"status": "success", "message": "Database initialized"}
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to initialize database: {e}")
        raise
    finally:
        conn.close()


def chunk_text(text: str, max_tokens: int = 500) -> List[Tuple[str, str]]:
    """텍스트를 시맨틱 청크로 분할"""
    if not text:
        return []

    # 문장 단위로 분할 (마침표, 느낌표, 물음표)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        # 대략적인 토큰 개수 (글자수 / 3.5)
        sentence_tokens = len(sentence) // 3 + 1

        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_tokens = sentence_tokens
        else:
            current_chunk += " " + sentence if current_chunk else sentence
            current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(current_chunk.strip())

    return [(chunk, "text") for chunk in chunks if chunk]


def store(input_file: str):
    """분석 JSON을 데이터베이스에 저장하고 임베딩 생성"""
    # Load analysis JSON
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load analysis JSON: {e}")
        raise

    # Get embedding provider
    provider = get_embedding_provider()
    conn = get_db_connection()

    try:
        cur = conn.cursor()

        # Extract project info
        project_data = analysis.get("project", {})
        project_id = str(uuid.uuid4())

        cur.execute("""
            INSERT INTO bid_projects (
                id, project_name, announcement_no, issuing_org, project_type,
                announcement_date, submission_deadline, budget_range, location,
                description, raw_text
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            project_id,
            project_data.get("project_name", ""),
            project_data.get("announcement_no", ""),
            project_data.get("issuing_org", ""),
            project_data.get("project_type", ""),
            project_data.get("announcement_date"),
            project_data.get("submission_deadline"),
            project_data.get("budget_range", ""),
            project_data.get("location", ""),
            project_data.get("summary", ""),
            analysis.get("raw_text", "")
        ))
        logger.info(f"Created project: {project_id}")

        # Store qualifications
        qualifications = analysis.get("qualifications", [])
        for qual in qualifications:
            if isinstance(qual, dict):
                requirement = qual.get("requirement", str(qual))
            else:
                requirement = str(qual)

            cur.execute("""
                INSERT INTO bid_qualifications (project_id, requirement)
                VALUES (%s, %s)
            """, (project_id, requirement))
        logger.info(f"Stored {len(qualifications)} qualifications")

        # Store documents
        documents = analysis.get("documents", [])
        for doc in documents:
            if isinstance(doc, dict):
                doc_name = doc.get("name") or doc.get("document_name", "")
                doc_type = doc.get("type") or doc.get("document_type", "")
                requirement = doc.get("requirement", doc.get("description", ""))
            else:
                doc_name = str(doc)
                doc_type = ""
                requirement = ""

            cur.execute("""
                INSERT INTO bid_documents (project_id, document_name, document_type, requirement)
                VALUES (%s, %s, %s, %s)
            """, (project_id, doc_name, doc_type, requirement))
        logger.info(f"Stored {len(documents)} documents")

        # Store evaluation criteria
        criteria = analysis.get("evaluation_criteria", [])
        for crit in criteria:
            if isinstance(crit, dict):
                crit_name = crit.get("name") or crit.get("criteria_name", "")
                crit_desc = crit.get("description") or crit.get("criteria_description", "")
                weight = crit.get("weight", 0)
            else:
                crit_name = str(crit)
                crit_desc = ""
                weight = 0

            cur.execute("""
                INSERT INTO bid_evaluation_criteria (project_id, criteria_name, criteria_description, weight)
                VALUES (%s, %s, %s, %s)
            """, (project_id, crit_name, crit_desc, weight))
        logger.info(f"Stored {len(criteria)} evaluation criteria")

        # Prepare text chunks and embeddings
        chunks_to_embed = []
        chunk_metadata = []

        # Title and summary chunk
        title = project_data.get("project_name", "")
        summary = project_data.get("summary", "")
        if title:
            chunk_text = f"{title}. {summary}".strip()
            chunks_to_embed.append(chunk_text)
            chunk_metadata.append(("title_summary", chunk_text))

        # Qualifications chunk
        if qualifications:
            qual_text = "자격 요건: " + " ".join([
                q.get("requirement", str(q)) if isinstance(q, dict) else str(q)
                for q in qualifications
            ])
            chunks_to_embed.append(qual_text)
            chunk_metadata.append(("qualifications", qual_text))

        # Documents chunk
        if documents:
            doc_text = "필요 서류: " + " ".join([
                f"{d.get('name') or d.get('document_name', '')} - {d.get('requirement', d.get('description', ''))}"
                if isinstance(d, dict)
                else str(d)
                for d in documents
            ])
            chunks_to_embed.append(doc_text)
            chunk_metadata.append(("documents", doc_text))

        # Evaluation criteria chunk
        if criteria:
            crit_text = "평가 기준: " + " ".join([
                f"{c.get('name') or c.get('criteria_name', '')} ({c.get('weight', 0)}%): {c.get('description') or c.get('criteria_description', '')}"
                if isinstance(c, dict)
                else str(c)
                for c in criteria
            ])
            chunks_to_embed.append(crit_text)
            chunk_metadata.append(("evaluation_criteria", crit_text))

        # Full text chunks
        raw_text = analysis.get("raw_text", "")
        if raw_text:
            text_chunks = chunk_text(raw_text)
            for chunk, _ in text_chunks:
                chunks_to_embed.append(chunk)
                chunk_metadata.append(("full_text", chunk))

        # Generate embeddings
        if chunks_to_embed:
            logger.info(f"Generating {len(chunks_to_embed)} embeddings...")
            embeddings = provider.embed(chunks_to_embed)

            # Store embeddings
            for (chunk_type, chunk_text), embedding in zip(chunk_metadata, embeddings):
                cur.execute("""
                    INSERT INTO bid_embeddings (project_id, chunk_type, chunk_text, embedding)
                    VALUES (%s, %s, %s, %s)
                """, (project_id, chunk_type, chunk_text, embedding))

            logger.info(f"Stored {len(embeddings)} embeddings")

        conn.commit()
        result = {
            "status": "success",
            "project_id": project_id,
            "project_name": title,
            "chunks_stored": len(chunks_to_embed),
            "embeddings_stored": len(embeddings) if chunks_to_embed else 0
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to store analysis: {e}")
        raise
    finally:
        conn.close()


def search(query: str, top: int = 10):
    """쿼리를 통해 유사한 청크 검색"""
    provider = get_embedding_provider()

    # Embed query
    logger.info(f"Embedding query: {query}")
    query_embedding = provider.embed_single(query)

    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Search using cosine distance
        cur.execute(f"""
            SELECT
                p.project_name,
                e.chunk_type,
                e.chunk_text,
                1 - (e.embedding <=> %s::vector) as similarity
            FROM bid_embeddings e
            JOIN bid_projects p ON e.project_id = p.id
            ORDER BY e.embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, top))

        results = cur.fetchall()

        output = {
            "status": "success",
            "query": query,
            "results": [
                {
                    "project_name": r[0],
                    "chunk_type": r[1],
                    "text_preview": r[2][:200] + "..." if len(r[2]) > 200 else r[2],
                    "similarity": float(r[3])
                }
                for r in results
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output
    finally:
        conn.close()


def similar(project_id: str, top: int = 10):
    """주어진 프로젝트와 유사한 다른 프로젝트 찾기"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Get the title+summary embedding of the project
        cur.execute("""
            SELECT embedding FROM bid_embeddings
            WHERE project_id = %s AND chunk_type = 'title_summary'
            LIMIT 1
        """, (project_id,))

        result = cur.fetchone()
        if not result:
            logger.warning(f"No title_summary embedding found for project {project_id}")
            output = {
                "status": "error",
                "message": f"No embedding found for project {project_id}"
            }
            print(json.dumps(output, ensure_ascii=False))
            return output

        project_embedding = result[0]

        # Find similar projects
        cur.execute("""
            SELECT DISTINCT
                p.id,
                p.project_name,
                1 - (e.embedding <=> %s::vector) as similarity
            FROM bid_embeddings e
            JOIN bid_projects p ON e.project_id = p.id
            WHERE p.id != %s AND e.chunk_type = 'title_summary'
            ORDER BY e.embedding <=> %s::vector
            LIMIT %s
        """, (project_embedding, project_id, project_embedding, top))

        results = cur.fetchall()

        output = {
            "status": "success",
            "reference_project_id": project_id,
            "similar_projects": [
                {
                    "project_id": str(r[0]),
                    "project_name": r[1],
                    "similarity": float(r[2])
                }
                for r in results
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output
    finally:
        conn.close()


def delete(project_id: str):
    """프로젝트와 관련된 모든 데이터 삭제"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Delete cascades automatically due to foreign key constraints
        cur.execute("DELETE FROM bid_projects WHERE id = %s", (project_id,))
        affected = cur.rowcount

        conn.commit()

        output = {
            "status": "success" if affected > 0 else "not_found",
            "project_id": project_id,
            "deleted": affected > 0
        }
        print(json.dumps(output, ensure_ascii=False))
        return output
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to delete project: {e}")
        raise
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="PostgreSQL + pgvector 기반 입찰 제안서 벡터화 엔진"
    )
    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # init-db subcommand
    init_parser = subparsers.add_parser("init-db", help="데이터베이스 초기화")
    init_parser.add_argument("--db-url", help="DATABASE_URL 오버라이드")

    # store subcommand
    store_parser = subparsers.add_parser("store", help="분석 JSON을 저장")
    store_parser.add_argument("--input", required=True, help="입력 analysis.json 파일 경로")

    # search subcommand
    search_parser = subparsers.add_parser("search", help="유사 청크 검색")
    search_parser.add_argument("--query", required=True, help="검색 쿼리")
    search_parser.add_argument("--top", type=int, default=10, help="상위 N개 결과 반환 (기본값: 10)")

    # similar subcommand
    similar_parser = subparsers.add_parser("similar", help="유사 프로젝트 찾기")
    similar_parser.add_argument("--project-id", required=True, help="프로젝트 UUID")
    similar_parser.add_argument("--top", type=int, default=10, help="상위 N개 결과 반환 (기본값: 10)")

    # delete subcommand
    delete_parser = subparsers.add_parser("delete", help="프로젝트 삭제")
    delete_parser.add_argument("--project-id", required=True, help="삭제할 프로젝트 UUID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "init-db":
            init_db(args.db_url)
        elif args.command == "store":
            store(args.input)
        elif args.command == "search":
            search(args.query, args.top)
        elif args.command == "similar":
            similar(args.project_id, args.top)
        elif args.command == "delete":
            delete(args.project_id)
    except Exception as e:
        logger.error(f"Command failed: {e}")
        error_output = {
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(error_output, ensure_ascii=False), file=sys.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()
