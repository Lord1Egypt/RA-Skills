# Pinecone RAG Integration

This guide explains how to use Docling MCP with Pinecone vector database for Retrieval-Augmented Generation (RAG) applications.

## Overview

The Pinecone RAG integration allows you to:
- Convert documents using Docling's powerful parsing capabilities
- Store document chunks as embeddings in Pinecone
- Perform semantic search across multiple namespaces
- Build RAG applications with multi-tenant support

## Installation

Install Docling MCP with the Pinecone RAG extra:

```bash
pip install -e ".[pinecone-rag]"
```

This installs:
- `pinecone-client>=5.0.0` - Pinecone vector database client
- `openai>=1.0.0` - OpenAI API for embeddings

## Configuration

Create a `.env` file in the project root with your credentials:

```bash
# OpenAI Configuration (for embeddings)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-index-name
PINECONE_DIMENSION=1024
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

# Namespace Configuration
PINECONE_PRIMARY_NAMESPACE=main
PINECONE_DEFAULT_NAMESPACES=main,docs,knowledge,test
```

## Usage

### Starting the MCP Server with Pinecone Tools

```bash
docling-mcp-server --tools conversion generation pinecone-rag
```

Or using uvx:

```bash
uvx --from docling-mcp docling-mcp-server conversion generation pinecone-rag
```

### Available Tools

#### 1. `export_docling_document_to_pinecone`

Exports a converted document to Pinecone vector database.

**Parameters:**
- `document_key` (str): The document identifier from local cache
- `namespace` (str, optional): Target namespace (defaults to primary namespace)
- `chunk_size` (int, optional): Size of text chunks in characters (default: 1000)

**Example prompt:**
```
Convert the PDF at /path/to/document.pdf and upload it to Pinecone in the 'research' namespace.
```

#### 2. `search_pinecone`

Search documents using semantic similarity.

**Parameters:**
- `query` (str): The search query
- `namespaces` (list[str], optional): Namespaces to search (defaults to all configured)
- `top_k` (int, optional): Number of results to return (default: 5)

**Example prompt:**
```
Search for information about "machine learning models" in the research namespace.
```

#### 3. `list_pinecone_namespaces`

List all namespaces and their statistics.

**Example prompt:**
```
Show me all Pinecone namespaces and how many vectors are in each.
```

## Example Workflow

### 1. Convert and Upload a Document

```prompt
I have a PDF at https://arxiv.org/pdf/2408.09869. 
Please convert it using Docling and upload it to Pinecone in the 'papers' namespace.
```

The agent will:
1. Convert the PDF using Docling
2. Chunk the document into manageable pieces
3. Create embeddings using OpenAI
4. Upload to Pinecone with metadata

### 2. Search Across Documents

```prompt
Search for "document understanding" across all namespaces and give me the top 5 results.
```

### 3. Multi-Namespace RAG

```prompt
I want to search for "PDF parsing techniques" but only in the 'papers' and 'docs' namespaces.
```

## Multi-Namespace Support

The Pinecone integration supports multiple namespaces for organizing documents:

- **Primary Namespace**: Where new documents are stored by default
- **Search Namespaces**: Multiple namespaces can be searched simultaneously
- **Priority Order**: Namespaces are searched in the order specified in `PINECONE_DEFAULT_NAMESPACES`

## Advanced Configuration

### Custom Embedding Models

You can use different OpenAI embedding models:

```bash
OPENAI_EMBEDDING_MODEL=text-embedding-3-large  # Higher quality, more expensive
OPENAI_EMBEDDING_MODEL=text-embedding-3-small  # Faster, cheaper
```

### Chunk Size Optimization

Adjust chunk size based on your use case:

- **Small chunks (500-1000)**: Better for precise retrieval
- **Large chunks (1500-2000)**: Better for context-rich answers

### Namespace Strategy

Organize namespaces by:
- **Content type**: `papers`, `docs`, `manuals`
- **Project**: `project-a`, `project-b`
- **Time period**: `2024-q1`, `2024-q2`
- **Access level**: `public`, `internal`, `confidential`

## Testing

Run the test script to verify your setup:

```bash
python test_pinecone_integration.py
```

This will:
1. Convert a sample document
2. Upload it to Pinecone
3. Perform test searches
4. Display results

## Troubleshooting

### "Pinecone not available" Error

Make sure you installed the pinecone-rag extra:
```bash
pip install -e ".[pinecone-rag]"
```

### "Index not found" Error

The index will be created automatically on first use. Make sure your Pinecone API key has permission to create indexes.

### Embedding Dimension Mismatch

Ensure `PINECONE_DIMENSION` matches your embedding model:
- `text-embedding-3-small`: 1536 dimensions
- `text-embedding-3-large`: 3072 dimensions
- `text-embedding-ada-002`: 1536 dimensions

## License

MIT License - Same as Docling MCP

