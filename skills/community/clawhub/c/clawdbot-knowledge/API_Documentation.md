# RAG-Enhanced N8N System - API Documentation

## 📋 **Document Information**

- **Document Version**: 1.0
- **Last Updated**: 2024-01-08
- **Document Type**: API Documentation
- **Audience**: Developers, Integration Engineers, Technical Architects
- **Classification**: Technical Documentation

---

## 🚀 **API Overview**

The RAG-Enhanced N8N System provides a comprehensive RESTful API that enables programmatic access to all system functionality. The API follows OpenAPI 3.0 specification and supports JSON request/response formats with optional XML support.

### **API Base Information**

```yaml
API Details:
  Base URL: https://api.n8n-mcp.yourdomain.com/api/v1
  Protocol: HTTPS (TLS 1.3)
  Format: JSON (primary), XML (optional)
  Authentication: JWT Bearer Token + API Key
  Rate Limiting: 1000 requests/minute (default)
  Versioning: URI versioning (/api/v1, /api/v2)
  Documentation: OpenAPI 3.0 / Swagger UI
```

### **API Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                       │
├─────────────────────────────────────────────────────────────┤
│  Authentication │ Rate Limiting │ SSL Termination │ Routing │
├─────────────────────────────────────────────────────────────┤
│                    Service APIs                            │
├─────────────────┬─────────────────┬─────────────────────────┤
│   RAG Engine    │   Workflows     │   Monitoring &          │
│   API           │   API           │   Security APIs         │
├─────────────────┼─────────────────┼─────────────────────────┤
│   User Mgmt     │   Analytics     │   Compliance            │
│   API           │   API           │   API                   │
└─────────────────┴─────────────────┴─────────────────────────┘
```

---

## 🔐 **Authentication & Authorization**

### **Authentication Methods**

**1. JWT Bearer Token Authentication**
```http
Authorization: Bearer <jwt_token>
```

**2. API Key Authentication**
```http
X-API-Key: <api_key>
Authorization: Bearer <jwt_token>
```

**3. OAuth 2.0 (Enterprise)**
```http
Authorization: Bearer <oauth_access_token>
```

### **Authentication Flow**

**Step 1: Obtain JWT Token**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "secure_password",
  "mfa_code": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "read write admin"
}
```

**Step 2: Use Token in Requests**
```http
GET /api/v1/workflows
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-API-Key: your_api_key_here
```

### **API Key Management**

**Generate API Key:**
```http
POST /api/v1/auth/api-keys
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "Integration API Key",
  "description": "For external system integration",
  "permissions": ["workflows:read", "workflows:execute"],
  "expires_at": "2024-12-31T23:59:59Z"
}
```

**Response:**
```json
{
  "api_key_id": "ak_1234567890abcdef",
  "api_key": "n8n_mcp_ak_1234567890abcdef1234567890abcdef",
  "name": "Integration API Key",
  "permissions": ["workflows:read", "workflows:execute"],
  "created_at": "2024-01-08T10:00:00Z",
  "expires_at": "2024-12-31T23:59:59Z"
}
```

---

## 🔄 **RAG Engine API**

### **Document Management**

**Upload Document**
```http
POST /api/v1/rag/documents
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "file": <binary_file_data>,
  "metadata": {
    "title": "Product Manual",
    "category": "documentation",
    "classification": "internal",
    "tags": ["product", "manual", "v2.0"]
  }
}
```

**Response:**
```json
{
  "document_id": "doc_1234567890abcdef",
  "title": "Product Manual",
  "filename": "product_manual_v2.pdf",
  "size": 2048576,
  "pages": 45,
  "chunks_created": 89,
  "processing_status": "completed",
  "uploaded_at": "2024-01-08T10:00:00Z",
  "metadata": {
    "title": "Product Manual",
    "category": "documentation",
    "classification": "internal",
    "tags": ["product", "manual", "v2.0"]
  }
}
```

**List Documents**
```http
GET /api/v1/rag/documents?page=1&limit=20&category=documentation
Authorization: Bearer <token>
```

**Response:**
```json
{
  "documents": [
    {
      "document_id": "doc_1234567890abcdef",
      "title": "Product Manual",
      "filename": "product_manual_v2.pdf",
      "size": 2048576,
      "pages": 45,
      "chunks_created": 89,
      "uploaded_at": "2024-01-08T10:00:00Z",
      "metadata": {
        "category": "documentation",
        "classification": "internal"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "pages": 8
  }
}
```

**Delete Document**
```http
DELETE /api/v1/rag/documents/{document_id}
Authorization: Bearer <token>
```

### **RAG Query Operations**

**Execute RAG Query**
```http
POST /api/v1/rag/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "How do I configure the authentication settings?",
  "max_results": 5,
  "min_score": 0.7,
  "filters": {
    "category": ["documentation", "manual"],
    "classification": "internal"
  },
  "llm_config": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

**Response:**
```json
{
  "query_id": "qry_1234567890abcdef",
  "query": "How do I configure the authentication settings?",
  "response": {
    "answer": "To configure authentication settings, navigate to the Admin Panel > Security Settings. You can enable multi-factor authentication, configure password policies, and set up SSO integration...",
    "confidence": 0.92,
    "sources": [
      {
        "document_id": "doc_1234567890abcdef",
        "chunk_id": "chunk_123",
        "title": "Admin Guide",
        "content": "Authentication configuration can be found in...",
        "score": 0.89,
        "page": 15
      }
    ]
  },
  "processing_time": 1.23,
  "timestamp": "2024-01-08T10:00:00Z"
}
```

**Get Query History**
```http
GET /api/v1/rag/queries?user_id=user123&limit=10
Authorization: Bearer <token>
```

---

## ⚙️ **Workflows API**

### **Workflow Management**

**List Workflows**
```http
GET /api/v1/workflows?status=active&page=1&limit=20
Authorization: Bearer <token>
```

**Response:**
```json
{
  "workflows": [
    {
      "workflow_id": "wf_1234567890abcdef",
      "name": "Customer Onboarding",
      "description": "Automated customer onboarding process",
      "status": "active",
      "version": "1.2.0",
      "created_by": "user123",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-08T10:00:00Z",
      "tags": ["onboarding", "customer", "automation"],
      "execution_count": 1247,
      "success_rate": 98.5
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

**Create Workflow**
```http
POST /api/v1/workflows
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Data Processing Pipeline",
  "description": "Automated data processing and analysis",
  "definition": {
    "nodes": [
      {
        "id": "start",
        "type": "trigger",
        "name": "Manual Trigger",
        "parameters": {}
      },
      {
        "id": "process",
        "type": "rag-query",
        "name": "RAG Analysis",
        "parameters": {
          "query": "{{$json.input_text}}",
          "max_results": 5
        }
      },
      {
        "id": "output",
        "type": "webhook",
        "name": "Send Results",
        "parameters": {
          "url": "https://api.example.com/results",
          "method": "POST"
        }
      }
    ],
    "connections": {
      "start": {
        "main": [["process"]]
      },
      "process": {
        "main": [["output"]]
      }
    }
  },
  "tags": ["data", "processing", "rag"]
}
```

**Execute Workflow**
```http
POST /api/v1/workflows/{workflow_id}/execute
Authorization: Bearer <token>
Content-Type: application/json

{
  "input_data": {
    "input_text": "Analyze customer feedback data",
    "customer_id": "cust_123",
    "priority": "high"
  },
  "execution_mode": "synchronous"
}
```

**Response:**
```json
{
  "execution_id": "exec_1234567890abcdef",
  "workflow_id": "wf_1234567890abcdef",
  "status": "completed",
  "started_at": "2024-01-08T10:00:00Z",
  "finished_at": "2024-01-08T10:00:15Z",
  "duration": 15.23,
  "input_data": {
    "input_text": "Analyze customer feedback data",
    "customer_id": "cust_123",
    "priority": "high"
  },
  "output_data": {
    "analysis_result": "Customer feedback indicates high satisfaction...",
    "sentiment_score": 0.85,
    "recommendations": ["Maintain current service level", "Focus on response time"]
  },
  "execution_details": {
    "nodes_executed": 3,
    "nodes_successful": 3,
    "nodes_failed": 0,
    "total_processing_time": 15.23
  }
}
```

### **Workflow Execution Monitoring**

**Get Execution Status**
```http
GET /api/v1/workflows/{workflow_id}/executions/{execution_id}
Authorization: Bearer <token>
```

**List Workflow Executions**
```http
GET /api/v1/workflows/{workflow_id}/executions?status=completed&limit=10
Authorization: Bearer <token>
```

---

## 📊 **Monitoring & Analytics API**

### **Metrics and Performance**

**Get System Metrics**
```http
GET /api/v1/monitoring/metrics?metric=cpu_usage&start_time=2024-01-08T00:00:00Z&end_time=2024-01-08T23:59:59Z
Authorization: Bearer <token>
```

**Response:**
```json
{
  "metric_name": "cpu_usage",
  "unit": "percentage",
  "data_points": [
    {
      "timestamp": "2024-01-08T10:00:00Z",
      "value": 45.2,
      "labels": {
        "instance": "api-server-1",
        "component": "rag-engine"
      }
    }
  ],
  "aggregation": {
    "avg": 42.1,
    "min": 15.3,
    "max": 78.9,
    "count": 1440
  }
}
```

**Get Analytics Dashboard Data**
```http
GET /api/v1/analytics/dashboard?dashboard=performance&time_range=24h
Authorization: Bearer <token>
```

**Create Custom Alert**
```http
POST /api/v1/monitoring/alerts
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "High CPU Usage Alert",
  "description": "Alert when CPU usage exceeds 80%",
  "metric": "cpu_usage",
  "condition": "greater_than",
  "threshold": 80,
  "duration": 300,
  "severity": "warning",
  "notification_channels": ["email", "slack"]
}
```

---

## 👥 **User Management API**

### **User Operations**

**List Users**
```http
GET /api/v1/users?role=operator&status=active&page=1&limit=20
Authorization: Bearer <token>
```

**Create User**
```http
POST /api/v1/users
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "john.doe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "roles": ["operator", "analyst"],
  "require_mfa": true,
  "profile": {
    "first_name": "John",
    "last_name": "Doe",
    "department": "Operations",
    "phone": "+1-555-0123"
  }
}
```

**Update User**
```http
PUT /api/v1/users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "roles": ["operator", "analyst", "admin"],
  "status": "active",
  "profile": {
    "department": "IT Operations",
    "phone": "+1-555-0124"
  }
}
```

---

## 🔒 **Security & Compliance API**

### **Security Operations**

**Get Security Events**
```http
GET /api/v1/security/events?severity=high&start_time=2024-01-08T00:00:00Z
Authorization: Bearer <token>
```

**Generate Compliance Report**
```http
POST /api/v1/compliance/reports
Authorization: Bearer <token>
Content-Type: application/json

{
  "framework": "gdpr",
  "period_start": "2024-01-01T00:00:00Z",
  "period_end": "2024-01-31T23:59:59Z",
  "format": "pdf",
  "include_evidence": true
}
```

**Response:**
```json
{
  "report_id": "rpt_1234567890abcdef",
  "framework": "gdpr",
  "status": "generating",
  "estimated_completion": "2024-01-08T10:05:00Z",
  "download_url": null
}
```

---

## 📝 **Error Handling**

### **HTTP Status Codes**

```yaml
Success Codes:
  200: OK - Request successful
  201: Created - Resource created successfully
  202: Accepted - Request accepted for processing
  204: No Content - Request successful, no content returned

Client Error Codes:
  400: Bad Request - Invalid request format
  401: Unauthorized - Authentication required
  403: Forbidden - Insufficient permissions
  404: Not Found - Resource not found
  409: Conflict - Resource conflict
  422: Unprocessable Entity - Validation error
  429: Too Many Requests - Rate limit exceeded

Server Error Codes:
  500: Internal Server Error - Server error
  502: Bad Gateway - Upstream server error
  503: Service Unavailable - Service temporarily unavailable
  504: Gateway Timeout - Request timeout
```

### **Error Response Format**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "INVALID_FORMAT"
      }
    ],
    "request_id": "req_1234567890abcdef",
    "timestamp": "2024-01-08T10:00:00Z"
  }
}
```

---

## 🚀 **Rate Limiting**

### **Rate Limit Headers**

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1704715200
X-RateLimit-Window: 60
```

### **Rate Limit Tiers**

```yaml
Rate Limits by Authentication:
  Unauthenticated: 100 requests/hour
  Authenticated User: 1000 requests/hour
  API Key: 5000 requests/hour
  Enterprise: 10000 requests/hour

Rate Limits by Endpoint:
  Authentication: 10 requests/minute
  RAG Queries: 100 requests/minute
  Workflow Execution: 50 requests/minute
  File Upload: 20 requests/minute
  Bulk Operations: 10 requests/minute
```

---

## 📚 **SDK and Integration Examples**

### **Python SDK Example**

```python
from n8n_mcp_sdk import N8NMCPClient

# Initialize client
client = N8NMCPClient(
    base_url="https://api.n8n-mcp.yourdomain.com",
    api_key="your_api_key",
    username="user@example.com",
    password="password"
)

# Upload document
document = client.rag.upload_document(
    file_path="./manual.pdf",
    metadata={
        "title": "User Manual",
        "category": "documentation"
    }
)

# Execute RAG query
result = client.rag.query(
    query="How do I reset my password?",
    max_results=5
)

print(f"Answer: {result.response.answer}")
print(f"Confidence: {result.response.confidence}")

# Execute workflow
execution = client.workflows.execute(
    workflow_id="wf_1234567890abcdef",
    input_data={"user_input": "Process this data"}
)

print(f"Execution Status: {execution.status}")
```

### **JavaScript/Node.js Example**

```javascript
const { N8NMCPClient } = require('@n8n-mcp/sdk');

const client = new N8NMCPClient({
  baseUrl: 'https://api.n8n-mcp.yourdomain.com',
  apiKey: 'your_api_key',
  username: 'user@example.com',
  password: 'password'
});

// Execute RAG query
async function queryRAG() {
  try {
    const result = await client.rag.query({
      query: 'What are the system requirements?',
      maxResults: 5,
      filters: {
        category: ['documentation']
      }
    });
    
    console.log('Answer:', result.response.answer);
    console.log('Sources:', result.response.sources);
  } catch (error) {
    console.error('Query failed:', error.message);
  }
}

// Create and execute workflow
async function runWorkflow() {
  try {
    const execution = await client.workflows.execute(
      'wf_1234567890abcdef',
      {
        inputData: { message: 'Hello World' },
        executionMode: 'synchronous'
      }
    );
    
    console.log('Execution completed:', execution.outputData);
  } catch (error) {
    console.error('Workflow execution failed:', error.message);
  }
}
```

### **cURL Examples**

**RAG Query:**
```bash
curl -X POST "https://api.n8n-mcp.yourdomain.com/api/v1/rag/query" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I configure SSL certificates?",
    "max_results": 3,
    "filters": {
      "category": ["documentation", "manual"]
    }
  }'
```

**Execute Workflow:**
```bash
curl -X POST "https://api.n8n-mcp.yourdomain.com/api/v1/workflows/wf_1234567890abcdef/execute" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "customer_id": "cust_123",
      "action": "process_order"
    },
    "execution_mode": "asynchronous"
  }'
```

This comprehensive API documentation provides developers with all the information needed to integrate with the RAG-Enhanced N8N System effectively.
