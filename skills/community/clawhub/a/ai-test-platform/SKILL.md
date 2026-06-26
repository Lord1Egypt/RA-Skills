---
name: ai-test-platform
description: This skill should be used when developing or using an AI-powered automated testing platform based on LangChain+DeepSeek. It implements intelligent test case generation, automated script execution (API/UI), test reporting, and authorization management for internal company use.
---

# AI Test Platform Developer Guide

## Purpose

Build an AI-powered automated testing platform for internal company use, leveraging DeepSeek LLM and LangChain framework to achieve intelligent test case generation, automated script creation, and test execution management. The platform focuses on API testing (Pytest+Requests) and UI testing (Playwright) with Docker-based isolation and authorization control.

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Vue3 | ^3.3.0 | Reactive UI framework |
| Frontend UI | Element Plus | ^2.4.0 | UI component library |
| State Management | Pinia | ^2.1.0 | Global state management |
| Backend | FastAPI | ^0.104.0 | Async web framework |
| AI Framework | LangChain | ^0.1.0 | LLM orchestration |
| LLM | DeepSeek | API | Core AI capabilities |
| API Testing | Pytest | ^7.4.0 | Test framework |
| API Reporting | pytest-json-report | ^1.5.0 | JSON report generation |
| UI Testing | Playwright | ^1.40.0 | Browser automation |
| Database | MySQL | 8.0 | Relational database |
| Vector DB | Chroma | ^0.4.0 | Vector retrieval |
| Deployment | Docker | Latest | Containerization |

## Architecture Overview

### System Layers
```
【Frontend Layer】Vue3 + Element Plus + Pinia
      ↓ (Polling for progress)
【API Layer】FastAPI + Auth Interceptor
      ↓
【Business Layer】Auth Management, Test Design, Execution, Reporting
      ↓
【AI Layer】LangChain + DeepSeek + RAG (Chroma)
      ↓
【Test Engine Layer】Pytest (API) + Playwright (UI)
      ↓
【Data Layer】MySQL (Business) + Chroma (Vectors)
```

## Core Modules

### 1. Authorization Management Module

**Permission Types:**
- `all` - Full functionality
- `generate` - Case/script generation only
- `execute` - Script execution only

**Encryption:**
- Algorithm: AES
- Key generation: `"yanghua" + timestamp + "360sb"`

**Authorization Flow:**
```
Request with auth_code → AuthInterceptor → Verify validity/expire/count/permission
→ Pass: Allow access + increment usage count
→ Fail: Return 401/403
```
### Key Services:
- `AuthCodeService`: CRUD, validation, count updates
- `AuthService`: Global request interceptor

### 2. AI Generation Module

**Supported Document Formats:**
- Word (.docx) - python-docx
- Excel (.xlsx) - openpyxl
- PDF (.pdf) - PyPDF2/pdfplumber
- Markdown (.md) - markdown

**Core Chains:**
- `TestCaseChain`: Generate test cases from documents
- `ApiScriptChain`: Generate Pytest+Requests scripts
- `UiScriptChain`: Generate Playwright scripts

**AI Configuration:**
- No QPS limit
- Retry: 2 times on failure
- Timeout: 30 seconds
- Expected usage: ≤20 calls/day

### 3. API Automation Module

**Integration:**
- Execute via `pytest.main()`
- Parse results using `pytest-json-report`

**Environment:**
- Docker container isolation
- Dependencies managed via `requirements.txt`

**Script Features:**
- Save, edit, categorize, batch manage
- Configure test environment, headers, global params
- Real-time debugging with request/response

### 4. UI Automation Module

**Playwright Configuration:**
- Headless mode (no UI)
- Screenshot on every test case (success + failure)
- Trace on failure (HTML trace viewer)
- Support Chrome and Edge

**Capabilities:**
- AI-generated element locators (ID/XPath)
- Flow script generation (login, click, input, assert, screenshot)
- Multi-browser compatibility

### 5. Test Execution Module

**Features:**
- Single or batch script execution
- Real-time log capture
- Execution timeout control
- Failure retry mechanism
- Historical record management

### 6. Test Report Module

**Auto-generation:**
- HTML reports after execution
- Export to HTML/PDF
- AI analysis of failures (simple log analysis)

**AI Analysis Prompt:**
```
Analyze the following test execution log and identify the failure reason:
{execution_log}

Provide:
1. Main failure cause
2. Possible problem location
3. Suggested solution

Keep it concise and highlight key information.
```

### 7. System Configuration Module

**Configuration Management:**
- DeepSeek API settings
- Environment URLs
- System initialization

**Features:**
- Operation logs
- Authorization usage logs
- AI call logs
- Automatic data backup

## Database Schema

### Core Tables

1. **auth_codes** - Authorization codes
   - Fields: id, code(encrypted), permission, expire_time, use_count, max_count, is_active

2. **test_cases** - Test cases
   - Fields: id, title, content, type(api/ui), created_by, create_time

3. **auto_scripts** - Automated scripts
   - Fields: id, name, content, type(api/ui), status, created_by, create_time, update_time

4. **execute_records** - Execution records
   - Fields: id, script_id, auth_code, result(success/fail), log, execute_time, duration

5. **test_reports** - Test reports
   - Fields: id, record_id, report_content, file_path, ai_analysis, create_time

6. **task_progress** - Task progress tracking
   - Fields: id, task_id, task_type(generate/execute), status, progress, message, result_data

See `references/architecture.md` for complete SQL definitions.

## API Design

### Unified Response Format
```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

### Common Parameters
- `auth_code` (required) - Authorization code for all core endpoints

### Core Endpoints

**Authorization:**
- `POST /admin/add_auth` - Create authorization code
- `POST /auth/verify` - Verify authorization
- `GET /auth/list` - List authorization codes

**AI Generation:**
- `POST /generate/case` - Generate test cases
- `POST /generate/api` - Generate API scripts
- `POST /generate/ui` - Generate UI scripts
- `GET /progress/{task_id}` - Get task progress

**Automation Management:**
- `POST /script/save` - Save script
- `GET /script/list` - List scripts
- `GET /script/{id}` - Get script details

**Test Execution:**
- `POST /execute/run` - Run test script
- `GET /execute/record` - Get execution records

**Report Management:**
- `GET /report/generate` - Generate report
- `GET /report/export` - Export report

**System Configuration:**
- `GET /system/config` - Get system config
- `POST /system/config` - Update system config

## Frontend Progress Polling

**Implementation:**
- State management: Pinia
- Polling interval: Every 2 seconds
- Progress types:
  - AI generation (parsing → vectorizing → generating → complete)
  - Script execution (running → collecting → reporting)

**Polling Endpoint:**
```bash
GET /api/progress/{task_id}
# Response
{
  "status": "processing|completed|failed",
  "progress": 50,
  "message": "Generating test cases..."
}
```

## Deployment

### Docker Compose Setup

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: ai_test_platform
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mysql
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=mysql+pymysql://root:root123@mysql:3306/ai_test_platform
      - DEEPSEEK_API_KEY=your_api_key

volumes:
  mysql_data:
```

### Data Persistence
- MySQL: Docker Volume
- Scripts: `./data/scripts/`
- Reports: `./data/reports/`
- Screenshots: `./data/screenshots/`
- Vectors: `./data/chroma/`

## When to Use This Skill

Use this skill when:
- Developing the AI test platform backend or frontend
- Implementing test case generation features
- Creating API or UI automated test scripts
- Integrating AI models (DeepSeek) with LangChain
- Setting up authorization and security mechanisms
- Configuring Docker deployment environment
- Debugging test execution issues
- Designing test report generation

## Usage Guidelines

### Backend Development
1. Follow FastAPI best practices
2. Implement async/await for I/O operations
3. Use Pydantic models for request/response validation
4. Implement proper exception handling
5. Add logging for all operations

### Frontend Development
1. Use Vue3 Composition API
2. Implement proper state management with Pinia
3. Handle loading and error states
4. Implement progress polling for async operations
5. Follow Element Plus component guidelines

### AI Integration
1. Use LangChain for chain orchestration
2. Implement retry logic for API calls
3. Handle timeouts gracefully
4. Cache common responses
5. Monitor API usage

### Security Considerations
- All core endpoints must verify auth_code
- Encrypt authorization codes using AES
- Sanitize all user inputs
- Implement rate limiting (optional)
- Never expose sensitive data in logs

## Project Structure

```
ai-test-platform/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core security and config
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── auth.py       # Authorization service
│   │   │   ├── ai.py         # AI generation service
│   │   │   ├── execute.py    # Execution service
│   │   │   └── report.py     # Report service
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Test files
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── pages/            # Page components
│   │   ├── stores/           # Pinia stores
│   │   ├── api/              # API calls
│   │   └── main.js           # Entry point
│   └── package.json
├── data/                     # Persistent data
│   ├── scripts/
│   ├── reports/
│   ├── screenshots/
│   └── chroma/
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
│   ├── generate_auth.py      # Auth code generator
│   ├── init_db.py            # Database initializer
│   └── setup.sh              # Setup script
├── docker-compose.yml
└── README.md
```

## Development Workflow

### 1. Setup Development Environment
```bash
# Clone and setup
git clone <repo>
cd ai-test-platform

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Initialize Database
```bash
python scripts/init_db.py
```

### 3. Generate Authorization Codes
```bash
python scripts/generate_auth.py
```

### 4. Run Development Server
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

### 5. Docker Deployment
```bash
docker-compose up -d
```

## Reference Documents

- `references/architecture.md` - Complete system architecture and database design
- `references/AI 自动化测试平台 需求规格说明书.docx` - Original requirements
- `references/AI 自动化测试平台 系统设计说明书.docx` - Original system design

## Next Steps

1. Review architecture documentation in `references/architecture.md`
2. Set up development environment
3. Initialize database schema
4. Generate authorization codes using provided script
5. Start with core backend services (Auth, AI Generation)
6. Implement frontend components
7. Test end-to-end workflows
8. Deploy using Docker Compose

## Notes

- This platform is designed for internal company use only
- All data must be stored internally, no external uploads
- DeepSeek API is the only allowed external model integration
- Authorization codes are mandatory for all core features
- Docker-based isolation ensures security and consistency
