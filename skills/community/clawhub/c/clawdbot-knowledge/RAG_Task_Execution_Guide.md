# RAG Implementation Task Execution Guide

## Overview
This guide provides detailed execution instructions for each task in the RAG-Enhanced N8N Workflow System implementation plan.

## Phase 1: Foundation & Infrastructure

### Task 1.1.1: Qdrant Collection Architecture

#### Objective
Design and create specialized Qdrant collections for workflows, nodes, documentation, and troubleshooting with optimized schemas.

#### Prerequisites
- Existing Qdrant instance running
- Python Qdrant client installed
- Access to Qdrant configuration

#### Implementation Steps

1. **Create Collection Schemas**
```python
# File: backend/rag/qdrant_collections.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, CollectionInfo

class RAGCollectionManager:
    def __init__(self, qdrant_client: QdrantClient):
        self.client = qdrant_client
        
    async def create_workflows_collection(self):
        """Create workflows collection with optimized schema"""
        collection_name = "n8n_workflows"
        
        # Delete existing collection if it exists
        try:
            await self.client.delete_collection(collection_name)
        except:
            pass
            
        # Create new collection
        await self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=768,  # OpenAI text-embedding-3-small
                distance=Distance.COSINE
            )
        )
        
        # Create payload indexes for efficient filtering
        await self.client.create_payload_index(
            collection_name=collection_name,
            field_name="category",
            field_schema="keyword"
        )
        
        await self.client.create_payload_index(
            collection_name=collection_name,
            field_name="complexity",
            field_schema="integer"
        )
        
        return collection_name
```

2. **Define Collection Schemas**
```python
# Collection configurations
COLLECTIONS_CONFIG = {
    "n8n_workflows": {
        "vector_size": 768,
        "distance": "COSINE",
        "indexes": ["category", "complexity", "node_count", "success_rate"]
    },
    "n8n_nodes": {
        "vector_size": 768,
        "distance": "DOT",
        "indexes": ["node_type", "category", "version"]
    },
    "n8n_documentation": {
        "vector_size": 1536,
        "distance": "COSINE",
        "indexes": ["doc_type", "section", "last_updated"]
    },
    "n8n_troubleshooting": {
        "vector_size": 768,
        "distance": "COSINE",
        "indexes": ["error_type", "severity", "resolution_success"]
    }
}
```

#### Validation Criteria
- [ ] All 4 collections created successfully
- [ ] Payload indexes created for efficient filtering
- [ ] Collections accessible via Qdrant client
- [ ] Performance test: Insert 1000 vectors in <30 seconds

#### Deliverables
- `backend/rag/qdrant_collections.py` - Collection management module
- `backend/rag/schemas.py` - Collection schema definitions
- `tests/test_qdrant_collections.py` - Unit tests for collection operations

### Task 1.1.2: Vector Indexing Strategy

#### Objective
Implement efficient indexing strategies for different content types with appropriate distance metrics and payload structures.

#### Implementation Steps

1. **Create Indexing Strategy Manager**
```python
# File: backend/rag/indexing_strategy.py
class IndexingStrategy:
    def __init__(self, collection_name: str, content_type: str):
        self.collection_name = collection_name
        self.content_type = content_type
        
    def get_vector_config(self):
        """Get optimal vector configuration for content type"""
        strategies = {
            "workflow": {
                "size": 768,
                "distance": "COSINE",
                "hnsw_config": {
                    "m": 16,
                    "ef_construct": 200,
                    "full_scan_threshold": 10000
                }
            },
            "node": {
                "size": 768,
                "distance": "DOT",
                "hnsw_config": {
                    "m": 32,
                    "ef_construct": 400,
                    "full_scan_threshold": 20000
                }
            }
        }
        return strategies.get(self.content_type, strategies["workflow"])
```

2. **Implement Batch Indexing**
```python
async def batch_index_vectors(self, vectors_data: List[Dict], batch_size: int = 100):
    """Efficiently index vectors in batches"""
    for i in range(0, len(vectors_data), batch_size):
        batch = vectors_data[i:i + batch_size]
        
        points = [
            PointStruct(
                id=item["id"],
                vector=item["vector"],
                payload=item["payload"]
            )
            for item in batch
        ]
        
        await self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
```

#### Validation Criteria
- [ ] Indexing performance: >1000 vectors/minute
- [ ] Query performance: <100ms for similarity search
- [ ] Memory usage: <8GB for 1M vectors
- [ ] Concurrent access: Support 50+ simultaneous queries

### Task 1.2.1: Data Source Connectors

#### Objective
Create connectors for N8N documentation, GitHub repositories, community forums, and existing workflow libraries.

#### Implementation Steps

1. **N8N Documentation Connector**
```python
# File: backend/rag/connectors/n8n_docs.py
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict

class N8NDocsConnector:
    def __init__(self, base_url: str = "https://docs.n8n.io"):
        self.base_url = base_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def fetch_documentation(self) -> List[Dict]:
        """Fetch all N8N documentation pages"""
        sitemap_url = f"{self.base_url}/sitemap.xml"
        
        async with self.session.get(sitemap_url) as response:
            sitemap_content = await response.text()
            
        # Parse sitemap and extract URLs
        soup = BeautifulSoup(sitemap_content, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]
        
        documents = []
        for url in urls:
            doc = await self.fetch_single_page(url)
            if doc:
                documents.append(doc)
                
        return documents
        
    async def fetch_single_page(self, url: str) -> Dict:
        """Fetch and parse a single documentation page"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract structured content
                    title = soup.find('h1').text if soup.find('h1') else ""
                    content_div = soup.find('div', class_='content')
                    text_content = content_div.get_text() if content_div else ""
                    
                    return {
                        "url": url,
                        "title": title,
                        "content": text_content,
                        "source": "n8n_docs",
                        "last_updated": None,
                        "doc_type": self.classify_doc_type(url)
                    }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
```

2. **GitHub Workflows Connector**
```python
# File: backend/rag/connectors/github_workflows.py
from github import Github
import json
from typing import List, Dict

class GitHubWorkflowConnector:
    def __init__(self, github_token: str):
        self.github = Github(github_token)
        
    async def fetch_workflows(self, repositories: List[str]) -> List[Dict]:
        """Fetch N8N workflows from GitHub repositories"""
        workflows = []
        
        for repo_name in repositories:
            try:
                repo = self.github.get_repo(repo_name)
                
                # Search for .n8n files
                contents = repo.get_contents("")
                n8n_files = self.find_n8n_files(contents)
                
                for file_info in n8n_files:
                    workflow_data = await self.process_workflow_file(repo, file_info)
                    if workflow_data:
                        workflows.append(workflow_data)
                        
            except Exception as e:
                print(f"Error processing repository {repo_name}: {e}")
                
        return workflows
        
    def find_n8n_files(self, contents) -> List:
        """Recursively find .n8n workflow files"""
        n8n_files = []
        
        for content in contents:
            if content.type == "file" and content.name.endswith('.n8n'):
                n8n_files.append(content)
            elif content.type == "dir":
                # Recursively search directories
                sub_contents = content.repository.get_contents(content.path)
                n8n_files.extend(self.find_n8n_files(sub_contents))
                
        return n8n_files
```

#### Validation Criteria
- [ ] Successfully connect to all data sources
- [ ] Fetch >1000 documents from N8N docs
- [ ] Extract >100 workflows from GitHub
- [ ] Handle rate limiting and errors gracefully
- [ ] Process documents in <5 minutes

### Task 1.3: Embedding Generation System

#### Objective
Implement embedding generation for workflows, nodes, documentation, and troubleshooting content.

#### Implementation Steps

1. **Multi-Model Embedding Generator**
```python
# File: backend/rag/embeddings/generator.py
from openai import AsyncOpenAI
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Union

class EmbeddingGenerator:
    def __init__(self, primary_model: str = "text-embedding-3-small"):
        self.primary_model = primary_model
        self.openai_client = AsyncOpenAI()
        self.fallback_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    async def generate_embeddings(self, texts: List[str], model: str = None) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        model = model or self.primary_model
        
        try:
            if model.startswith("text-embedding"):
                return await self.generate_openai_embeddings(texts, model)
            else:
                return self.generate_local_embeddings(texts, model)
        except Exception as e:
            print(f"Error with primary model, falling back: {e}")
            return self.generate_local_embeddings(texts)
            
    async def generate_openai_embeddings(self, texts: List[str], model: str) -> List[List[float]]:
        """Generate embeddings using OpenAI API"""
        # Handle token limits by chunking
        max_tokens = 8192
        chunked_texts = []
        
        for text in texts:
            if len(text.split()) > max_tokens:
                # Split long texts into chunks
                chunks = self.chunk_text(text, max_tokens)
                chunked_texts.extend(chunks)
            else:
                chunked_texts.append(text)
        
        # Batch process with rate limiting
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(chunked_texts), batch_size):
            batch = chunked_texts[i:i + batch_size]
            
            response = await self.openai_client.embeddings.create(
                model=model,
                input=batch
            )
            
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            
        return all_embeddings
```

2. **Content-Specific Embedding Strategies**
```python
class ContentEmbeddingStrategy:
    def __init__(self, content_type: str):
        self.content_type = content_type
        
    def prepare_text_for_embedding(self, content: Dict) -> str:
        """Prepare content for embedding based on type"""
        if self.content_type == "workflow":
            return self.prepare_workflow_text(content)
        elif self.content_type == "node":
            return self.prepare_node_text(content)
        elif self.content_type == "documentation":
            return self.prepare_doc_text(content)
        else:
            return str(content)
            
    def prepare_workflow_text(self, workflow: Dict) -> str:
        """Create embedding-optimized text for workflows"""
        parts = []
        
        if workflow.get("name"):
            parts.append(f"Workflow: {workflow['name']}")
            
        if workflow.get("description"):
            parts.append(f"Description: {workflow['description']}")
            
        if workflow.get("nodes"):
            node_types = [node.get("type", "") for node in workflow["nodes"]]
            parts.append(f"Nodes: {', '.join(node_types)}")
            
        if workflow.get("tags"):
            parts.append(f"Tags: {', '.join(workflow['tags'])}")
            
        return " | ".join(parts)
```

#### Validation Criteria
- [ ] Generate embeddings for 1000+ documents in <10 minutes
- [ ] Support multiple embedding models
- [ ] Handle token limits automatically
- [ ] Achieve >0.8 similarity for related content
- [ ] Cost optimization: <$50 for 10,000 embeddings

## Task Management Integration

### Progress Tracking
Use the task management system to track progress:

```python
# Update task status
await update_tasks([{
    "task_id": "fGpSV3TD3YfyKYBCMTigYt",  # 1.1.1: Qdrant Collection Architecture
    "state": "IN_PROGRESS"
}])

# Mark task complete with validation
await update_tasks([{
    "task_id": "fGpSV3TD3YfyKYBCMTigYt",
    "state": "COMPLETE",
    "description": "Qdrant collections created successfully. All validation criteria met."
}])
```

### Dependency Management
Before starting a task, verify dependencies:

```python
def check_task_dependencies(task_id: str) -> bool:
    """Check if all dependency tasks are complete"""
    dependencies = get_task_dependencies(task_id)
    
    for dep_id in dependencies:
        dep_task = get_task(dep_id)
        if dep_task.state != "COMPLETE":
            return False
            
    return True
```

### Quality Gates
Each task must pass quality gates before marking complete:

1. **Code Review**: All code reviewed by senior developer
2. **Unit Tests**: >90% code coverage, all tests passing
3. **Integration Tests**: End-to-end functionality verified
4. **Performance Tests**: Meets specified performance criteria
5. **Documentation**: Complete technical documentation

### Rollback Procedures
If a task fails validation:

1. **Immediate Rollback**: Revert changes to last known good state
2. **Root Cause Analysis**: Identify and document failure cause
3. **Fix Implementation**: Address root cause with targeted fix
4. **Re-validation**: Complete full validation cycle again
5. **Lessons Learned**: Update procedures to prevent recurrence
