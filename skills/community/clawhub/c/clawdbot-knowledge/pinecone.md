# Pinecone Setup for Self-Memory System

Complete guide to set up Pinecone vector database for semantic skill search.

## What is Pinecone?

Pinecone enables **semantic search** for skills. Instead of exact keyword matching, it finds skills based on **meaning**.

**Example:**
- User searches: "analyze customer feedback"
- Pinecone finds: "sentiment-analysis-tool", "customer-review-analyzer"
- Even if search terms don't exactly match skill names!

---

## Quick Start

### 1. Create Pinecone Account

```bash
1. Go to https://www.pinecone.io
2. Sign up (free tier available)
3. Verify email
4. Log in to dashboard
```

### 2. Create Index

**Via Pinecone Dashboard:**

```
1. Click "Create Index"
2. Fill in:
   - Name: deepallspeak-skills
   - Dimensions: 1536
   - Metric: cosine
   - Pod Type: p1.x1 (free tier) or s1 (serverless, recommended)
3. Click "Create Index"
4. Wait ~1 minute for initialization
```

**Via Pinecone API:**

```bash
# Install Pinecone CLI
pip install pinecone-client

# Create index via Python
python << 'EOF'
import pinecone

pinecone.init(
    api_key="YOUR_API_KEY",
    environment="YOUR_ENVIRONMENT"  # e.g., us-west1-gcp
)

# Create index
pinecone.create_index(
    name="deepallspeak-skills",
    dimension=1536,
    metric="cosine",
    pod_type="p1.x1"
)

print("✅ Index created successfully!")
EOF
```

### 3. Get API Credentials

```bash
1. In Pinecone Dashboard → API Keys
2. Copy:
   - API Key: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   - Environment: us-west1-gcp (or your region)
```

### 4. Configure Environment

```bash
# Add to your .env file:
PINECONE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=deepallspeak-skills
```

### 5. Verify Setup

```bash
# Test connection via Python
python << 'EOF'
import pinecone
import os

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)

# List indexes
indexes = pinecone.list_indexes()
print(f"Available indexes: {indexes}")

# Check index stats
index = pinecone.Index("deepallspeak-skills")
stats = index.describe_index_stats()
print(f"Index stats: {stats}")
print("✅ Pinecone connection successful!")
EOF
```

---

## Index Configuration Details

### Recommended Settings

**Serverless (Recommended for production):**
```yaml
Name: deepallspeak-skills
Cloud: AWS
Region: us-east-1
Dimension: 1536
Metric: cosine
```

**Benefits:**
- ✅ Auto-scaling (no capacity planning)
- ✅ Pay only for usage
- ✅ Lower costs for low-traffic
- ✅ Faster for bursty workloads

**Pod-based (Good for development):**
```yaml
Name: deepallspeak-skills
Dimension: 1536
Metric: cosine
Pod Type: p1.x1 (free tier)
Pods: 1
Replicas: 1
```

**Benefits:**
- ✅ Free tier available
- ✅ Predictable performance
- ✅ Good for testing

### Why These Settings?

**Dimension: 1536**
- Matches OpenAI `text-embedding-3-small` model
- Provides good semantic accuracy
- Efficient storage/search

**Metric: cosine**
- Best for semantic similarity
- Ranges from -1 (opposite) to 1 (identical)
- Industry standard for text embeddings

---

## How It Works

### 1. Skill Creation Flow

```
User creates skill
    ↓
Generate embedding text:
  "skill-name
   skill description
   category
   tag1, tag2, tag3"
    ↓
OpenAI text-embedding-3-small
  → [1536 float numbers]
    ↓
Store in Pinecone:
  {
    id: "skill-uuid",
    values: [embedding],
    metadata: {
      name, description, category, tags
    }
  }
```

### 2. Skill Search Flow

```
User searches: "analyze customer feedback"
    ↓
Generate query embedding:
  OpenAI embedding("analyze customer feedback")
  → [1536 float numbers]
    ↓
Pinecone similarity search:
  Find top K most similar vectors
    ↓
Return results:
  [
    {skill_id: "...", score: 0.92},
    {skill_id: "...", score: 0.87},
    ...
  ]
    ↓
Fetch full skill data from Supabase
```

---

## Testing Pinecone

### Manual Test via Python

```python
import pinecone
import openai
import os

# Initialize
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)
openai.api_key = os.getenv("OPENAI_API_KEY")

index = pinecone.Index("deepallspeak-skills")

# 1. Create test embedding
text = "analyze sales report\nAnalyze quarterly sales reports\nbusiness_intelligence\nsales, analytics, business"

response = openai.Embedding.create(
    model="text-embedding-3-small",
    input=text
)
embedding = response['data'][0]['embedding']

print(f"✅ Embedding generated: {len(embedding)} dimensions")

# 2. Upsert to Pinecone
index.upsert([
    {
        "id": "test-skill-1",
        "values": embedding,
        "metadata": {
            "name": "analyze-sales-report",
            "description": "Analyze quarterly sales reports",
            "category": "business_intelligence",
            "tags": ["sales", "analytics", "business"]
        }
    }
])

print("✅ Vector upserted to Pinecone")

# 3. Search
query_text = "sales analysis tool"
query_response = openai.Embedding.create(
    model="text-embedding-3-small",
    input=query_text
)
query_embedding = query_response['data'][0]['embedding']

results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)

print("\n✅ Search results:")
for match in results['matches']:
    print(f"  - {match['metadata']['name']} (score: {match['score']:.4f})")
```

### Expected Output

```
✅ Embedding generated: 1536 dimensions
✅ Vector upserted to Pinecone
✅ Search results:
  - analyze-sales-report (score: 0.9234)
```

---

## Performance Tuning

### Search Parameters

```python
# Basic search (fast, less accurate)
results = index.query(
    vector=query_embedding,
    top_k=5
)

# Search with filters (slower, more targeted)
results = index.query(
    vector=query_embedding,
    top_k=5,
    filter={
        "category": "business_intelligence",
        "tags": {"$in": ["sales", "analytics"]}
    }
)

# Search with metadata (slower, full context)
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True,
    include_values=False  # Don't return embeddings (saves bandwidth)
)
```

### Optimization Tips

**1. Batch Upserts:**
```python
# Instead of upserting one at a time
for skill in skills:
    index.upsert([skill])  # ❌ Slow

# Batch upsert
index.upsert(skills, batch_size=100)  # ✅ Fast
```

**2. Caching:**
```python
# Cache frequently searched queries
from functools import lru_cache

@lru_cache(maxsize=100)
def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']
```

**3. Metadata Indexing:**
```python
# For faster filtered searches, index metadata
# Already done automatically by Pinecone!
```

---

## Cost Optimization

### Free Tier Limits

**Serverless:**
- No free tier (pay per request)
- ~$0.01 per 1000 queries
- Good for low-volume production

**Pod-based:**
- 1 free p1.x1 pod (1GB storage)
- ~100,000 1536-dim vectors
- Enough for most use cases

### Reducing Costs

**1. Use smaller embeddings (if acceptable):**
```python
# Instead of text-embedding-3-small (1536 dims)
# Use text-embedding-3-small with dimensions param
response = openai.Embedding.create(
    model="text-embedding-3-small",
    input=text,
    dimensions=512  # Reduce to 512 dims (3x less storage)
)
```

**2. Delete old/unused vectors:**
```python
# Delete skills that haven't been used in 6 months
old_skill_ids = get_unused_skills(months=6)
index.delete(ids=old_skill_ids)
```

**3. Use namespaces for multi-tenancy:**
```python
# Separate indexes per user/org (if needed)
index.upsert([...], namespace="user_123")
index.query(..., namespace="user_123")
```

---

## Monitoring

### Index Statistics

```python
stats = index.describe_index_stats()
print(stats)

# Output:
# {
#   'dimension': 1536,
#   'index_fullness': 0.05,  # 5% full
#   'namespaces': {
#     '': {
#       'vector_count': 47
#     }
#   },
#   'total_vector_count': 47
# }
```

### Query Performance

```python
import time

start = time.time()
results = index.query(vector=embedding, top_k=10)
duration = time.time() - start

print(f"Query took {duration*1000:.2f}ms")
# Should be <100ms for serverless, <50ms for pod-based
```

---

## Troubleshooting

### Common Issues

**1. "Index not found"**
```python
# List available indexes
indexes = pinecone.list_indexes()
print(indexes)

# Check spelling and environment
```

**2. "Dimension mismatch"**
```python
# Error: Vector has wrong dimensions
# Fix: Make sure embedding model matches index

# Index dimension: 1536
# Embedding model: text-embedding-3-small (1536) ✅
# Embedding model: text-embedding-ada-002 (1536) ✅
# Embedding model: custom (768) ❌
```

**3. "API key invalid"**
```bash
# Regenerate API key in Pinecone Dashboard
# Update .env file
# Restart application
```

**4. Slow queries**
```python
# Check index statistics
stats = index.describe_index_stats()

# If index_fullness > 0.8 (80% full):
# - Upgrade to larger pod
# - OR switch to serverless
# OR delete old vectors
```

---

## Migration Guide

### From Development to Production

**1. Export vectors from dev:**
```python
# Fetch all vectors
results = index.query(
    vector=[0]*1536,  # Dummy vector
    top_k=10000,
    include_metadata=True,
    include_values=True
)

# Save to file
import json
with open('vectors_backup.json', 'w') as f:
    json.dump(results['matches'], f)
```

**2. Create production index:**
```
Follow "Create Index" steps above
Use serverless for production
```

**3. Import to production:**
```python
import json

with open('vectors_backup.json', 'r') as f:
    vectors = json.load(f)

# Batch upsert
prod_index.upsert(vectors, batch_size=100)
```

---

## Security

### API Key Management

**❌ Don't:**
```javascript
// Hardcode API keys
const apiKey = "xxxxx-xxxxx";

// Commit to git
PINECONE_API_KEY=xxxxx  # In .env file committed to repo
```

**✅ Do:**
```javascript
// Use environment variables
const apiKey = process.env.PINECONE_API_KEY;

// Add .env to .gitignore
echo ".env" >> .gitignore
```

### Access Control

**Server-side only:**
```javascript
// Pinecone API key should ONLY be used server-side
// skill-memory-server.js ✅
// Browser/client-side ❌
```

---

## Next Steps

After Pinecone setup:

1. ✅ Pinecone index created
2. ✅ API credentials configured
3. ⏭️ Install dependencies for skill-memory-server.js
4. ⏭️ Update .env with all credentials
5. ⏭️ Start skill-memory-server.js
6. ⏭️ Test semantic search

---

**Pinecone Version:** Compatible with all versions
**Embedding Model:** OpenAI text-embedding-3-small (1536 dimensions)
**Metric:** cosine similarity
**Last Updated:** December 2024
