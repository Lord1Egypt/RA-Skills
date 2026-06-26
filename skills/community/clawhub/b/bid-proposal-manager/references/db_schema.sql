-- ============================================================
-- 입찰/공모 관리 시스템 - PostgreSQL + pgvector 스키마
-- ============================================================
-- 사전 요구사항:
--   PostgreSQL 15+
--   pgvector 확장 (CREATE EXTENSION vector)
-- ============================================================

-- pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- 1. 프로젝트(공고) 테이블
-- ============================================================
CREATE TABLE IF NOT EXISTS bid_projects (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name    TEXT NOT NULL,                          -- 사업명
    announcement_no TEXT,                                   -- 공고번호
    issuing_org     TEXT,                                   -- 발주기관
    project_type    TEXT CHECK (project_type IN (           -- 사업유형
                        'bid', 'research', 'grant',
                        'contest', 'procurement', 'other'
                    )),
    announcement_date DATE,                                 -- 공고일
    submission_deadline TIMESTAMPTZ,                         -- 제출마감일
    briefing_date   TIMESTAMPTZ,                            -- 설명회일시
    qa_deadline     TIMESTAMPTZ,                            -- 질의응답 마감
    result_date     DATE,                                   -- 선정결과 발표일
    project_period  TEXT,                                   -- 사업 기간
    total_budget    BIGINT,                                 -- 총 사업비 (원)
    gov_funding     BIGINT,                                 -- 정부출연금 (원)
    private_funding BIGINT,                                 -- 민간부담금 (원)
    status          TEXT DEFAULT 'active' CHECK (status IN (
                        'active', 'preparing', 'submitted',
                        'won', 'lost', 'cancelled', 'archived'
                    )),
    source_url      TEXT,                                   -- 원본 공고 URL
    source_file     TEXT,                                   -- 원본 파일 경로
    notion_page_id  TEXT,                                   -- Notion 페이지 ID
    contact_name    TEXT,                                   -- 담당자
    contact_phone   TEXT,                                   -- 연락처
    contact_email   TEXT,                                   -- 이메일
    raw_text        TEXT,                                   -- 원본 파싱 텍스트 (전문)
    summary         TEXT,                                   -- 요약
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_projects_status ON bid_projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_deadline ON bid_projects(submission_deadline);
CREATE INDEX IF NOT EXISTS idx_projects_type ON bid_projects(project_type);
CREATE INDEX IF NOT EXISTS idx_projects_org ON bid_projects(issuing_org);

-- ============================================================
-- 2. 자격요건 테이블
-- ============================================================
CREATE TABLE IF NOT EXISTS bid_qualifications (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id      UUID REFERENCES bid_projects(id) ON DELETE CASCADE,
    qual_type       TEXT CHECK (qual_type IN (
                        'required', 'preferred', 'restriction'
                    )),                                       -- 필수/우대/제한
    description     TEXT NOT NULL,                            -- 요건 설명
    is_met          BOOLEAN DEFAULT NULL,                     -- 충족 여부 (사용자 입력)
    notes           TEXT,                                     -- 메모
    sort_order      INT DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_quals_project ON bid_qualifications(project_id);

-- ============================================================
-- 3. 제출서류 테이블
-- ============================================================
CREATE TABLE IF NOT EXISTS bid_documents (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id      UUID REFERENCES bid_projects(id) ON DELETE CASCADE,
    doc_name        TEXT NOT NULL,                            -- 서류명
    doc_type        TEXT CHECK (doc_type IN (
                        'required', 'optional', 'form_provided'
                    )),                                       -- 필수/선택/양식제공
    format_req      TEXT,                                    -- 형식 요구사항 (예: "A4, 20페이지 이내")
    template_url    TEXT,                                    -- 양식 다운로드 URL
    page_limit      INT,                                     -- 분량 제한 (페이지)
    is_prepared     BOOLEAN DEFAULT FALSE,                    -- 준비 완료 여부
    file_path       TEXT,                                    -- 준비된 파일 경로
    notes           TEXT,
    sort_order      INT DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_docs_project ON bid_documents(project_id);

-- ============================================================
-- 4. 평가기준/배점 테이블
-- ============================================================
CREATE TABLE IF NOT EXISTS bid_evaluation_criteria (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id      UUID REFERENCES bid_projects(id) ON DELETE CASCADE,
    category        TEXT NOT NULL,                            -- 대분류 (예: 기술, 가격, 경험)
    criterion       TEXT NOT NULL,                            -- 세부 항목
    max_score       NUMERIC(5,1),                            -- 배점
    weight          NUMERIC(5,2),                            -- 가중치 (%)
    notes           TEXT,
    sort_order      INT DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_eval_project ON bid_evaluation_criteria(project_id);

-- ============================================================
-- 5. 작성 요령 테이블
-- ============================================================
CREATE TABLE IF NOT EXISTS bid_writing_guidelines (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id      UUID REFERENCES bid_projects(id) ON DELETE CASCADE,
    section_title   TEXT NOT NULL,                            -- 목차 제목
    section_number  TEXT,                                     -- 번호 (예: "1.2.3")
    description     TEXT,                                     -- 작성 지침
    page_limit      INT,                                      -- 해당 섹션 분량 제한
    parent_id       UUID REFERENCES bid_writing_guidelines(id), -- 상위 섹션 (계층 구조)
    sort_order      INT DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_guidelines_project ON bid_writing_guidelines(project_id);

-- ============================================================
-- 6. 벡터 임베딩 테이블
-- ============================================================
-- 384차원: sentence-transformers/all-MiniLM-L6-v2 기본
-- 768차원: nomic-embed-text (Ollama)
-- 1536차원: OpenAI text-embedding-3-small
-- 사용하는 임베딩 모델에 맞춰 차원을 변경하세요.

CREATE TABLE IF NOT EXISTS bid_embeddings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id      UUID REFERENCES bid_projects(id) ON DELETE CASCADE,
    chunk_type      TEXT CHECK (chunk_type IN (
                        'title', 'summary', 'qualification',
                        'document_req', 'evaluation', 'full_text',
                        'writing_guide'
                    )),                                       -- 청크 유형
    chunk_text      TEXT NOT NULL,                            -- 원본 텍스트
    chunk_index     INT DEFAULT 0,                            -- 텍스트 내 순서
    embedding       vector(384),                              -- 벡터 (기본 384차원)
    metadata        JSONB DEFAULT '{}',                       -- 추가 메타데이터
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- pgvector 인덱스 (IVFFlat - 대량 데이터 시 성능 향상)
-- 데이터가 100건 이상 쌓인 후 생성 권장
-- CREATE INDEX IF NOT EXISTS idx_embeddings_vector
--     ON bid_embeddings USING ivfflat (embedding vector_cosine_ops)
--     WITH (lists = 20);

-- 기본 인덱스
CREATE INDEX IF NOT EXISTS idx_embeddings_project ON bid_embeddings(project_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_type ON bid_embeddings(chunk_type);

-- ============================================================
-- 7. 검색 이력 테이블 (선택)
-- ============================================================
CREATE TABLE IF NOT EXISTS bid_search_history (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_text      TEXT NOT NULL,
    query_embedding vector(384),
    results         JSONB,                                    -- 검색 결과 ID 목록
    searched_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 유틸리티 함수
-- ============================================================

-- 코사인 유사도 기반 검색 함수
CREATE OR REPLACE FUNCTION search_similar_projects(
    query_vec vector(384),
    match_count INT DEFAULT 5,
    min_similarity FLOAT DEFAULT 0.3
)
RETURNS TABLE (
    project_id UUID,
    project_name TEXT,
    chunk_type TEXT,
    chunk_text TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.project_id,
        p.project_name,
        e.chunk_type,
        e.chunk_text,
        1 - (e.embedding <=> query_vec) AS similarity
    FROM bid_embeddings e
    JOIN bid_projects p ON p.id = e.project_id
    WHERE 1 - (e.embedding <=> query_vec) >= min_similarity
    ORDER BY e.embedding <=> query_vec
    LIMIT match_count;
END;
$$;

-- 프로젝트 마감 임박 알림 뷰
CREATE OR REPLACE VIEW bid_upcoming_deadlines AS
SELECT
    id,
    project_name,
    issuing_org,
    submission_deadline,
    status,
    submission_deadline - NOW() AS time_remaining
FROM bid_projects
WHERE status = 'active'
  AND submission_deadline > NOW()
ORDER BY submission_deadline ASC;

-- updated_at 자동 갱신 트리거
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER set_updated_at
    BEFORE UPDATE ON bid_projects
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ============================================================
-- 초기 데이터 확인
-- ============================================================
-- SELECT COUNT(*) FROM bid_projects;
-- SELECT * FROM bid_upcoming_deadlines;
