# calibre-openclaw-server

FastAPI server to query a local Calibre library and provide RAG semantic search
with page-level citations.

The server uses:

- Calibre `metadata.db` as the book catalog.
- PostgreSQL with `pgvector` for embeddings.
- Ollama to generate embeddings.
- OpenLibrary API for book metadata enrichment and public domain download links.
- Systemd to keep the API running and run RAG in a scheduled window.

## Requirements

- Python 3.10+
- PostgreSQL with `vector` extension
- Ollama running
- Embedding model configured in `OLLAMA_MODEL`
- Local Calibre library with `metadata.db`

## Configuration

Create a `.env` in this directory or in the parent directory `skills/calibre-ebooks/`.
Use `.env.example` as a base.

Essential variables:

```env
CALIBRE_DB_PATH=/path/to/Library/metadata.db
CALIBRE_LIBRARY_PATH=/path/to/Library

API_KEY=secure-token
ALLOW_UNAUTHENTICATED=false

POSTGRESQL_DB_USER=calibre_openclaw
POSTGRESQL_DB_PASSWD=secure-password
POSTGRESQL_DB_DATABASE=calibre_openclaw
POSTGRESQL_DB_HOST=localhost
POSTGRESQL_DB_PORT=5432

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=nomic-embed-text-v2-moe:latest
ALLOW_REMOTE_OLLAMA=false

VT_API_KEY=your-virustotal-api-key
```

Sensitive options, disabled by default in code:

```env
ALLOW_BOOK_CONTENT_DOWNLOADS=false
ENABLE_NETWORK_BINDINGS_ENDPOINT=false
ENABLE_NETWORK_BINDINGS_MONITOR=false
ALLOW_GET_AUTO_SYNC=false
```

## Run the API

```bash
cd skills/calibre-ebooks/calibre-openclaw-server
./run.sh
```

Main URLs:

- API: `http://127.0.0.1:6180`
- Swagger: `http://127.0.0.1:6180/docs`
- ReDoc: `http://127.0.0.1:6180/redoc`
- Health: `http://127.0.0.1:6180/health`

## Ebook Upload and Virus Scanning

The server supports uploading ebook files with format validation and optional virus scanning using VirusTotal API.

### Upload Endpoint

**POST** `/api/books/upload`

Upload an ebook file with automatic format validation. The file is checked to ensure it's a valid ebook format before being accepted.

**Query Parameters:**

- `check_virus` (boolean, optional): Enable virus scanning using VirusTotal API. Requires `VT_API_KEY` to be configured. Default: `false`

**Supported Formats:**

PDF, EPUB, MOBI, AZW3, KFX, DJVU, LIT, PDB, TXT, RTF, DOCX, ODT, FB2, HTML, CBZ, CBR

**Example:**

```bash
curl -X POST "http://127.0.0.1:6180/api/books/upload?check_virus=true" \
  -H "X-API-Key: $API_KEY" \
  -F "file=@ebook.pdf"
```

**Response:**

```json
{
  "message": "File uploaded successfully",
  "filename": "ebook.pdf",
  "format": "PDF",
  "size_bytes": 1234567,
  "path": "/path/to/library/uploads/ebook.pdf",
  "virus_scan": {
    "scanned": true,
    "malicious": false,
    "detection_ratio": "0/60",
    "file_hash": "abc123...",
    "summary": "Detection ratio: 0/60"
  }
}
```

### Virus Scanning on File Retrieval

Existing file retrieval endpoints support optional virus scanning when `VT_API_KEY` is configured:

- **GET** `/api/books/{id}/pdf?check_virus=true`
- **GET** `/api/books/{id}/file?check_virus=true`

When `check_virus=true` is passed and `VT_API_KEY` is configured, the file is scanned before being returned. If malware is detected, a 403 error is returned with scan details.

**Example:**

```bash
curl -H "X-API-Key: $API_KEY" \
  "http://127.0.0.1:6180/api/books/123/pdf?check_virus=true"
```

### VirusTotal Configuration

To enable virus scanning, set the `VT_API_KEY` in your `.env` file:

```env
VT_API_KEY=your-virustotal-api-key
```

Get your API key from [VirusTotal](https://www.virustotal.com/).

**Notes:**

- Virus scanning is optional. If `VT_API_KEY` is not set, virus scanning is disabled and files are accepted without scanning.
- When `check_virus=true` is requested but `VT_API_KEY` is not configured, the operation proceeds without scanning and a warning is logged.
- Files are scanned using VirusTotal's file analysis API. The service checks if the file hash already exists in VirusTotal's database to avoid unnecessary uploads.
- Maximum file size for upload is 100MB.

## OpenLibrary Integration

The server integrates with OpenLibrary.org to enrich book metadata and provide download links for public domain books.

### Configuration

Add the following to your `.env` file:

```env
# OpenLibrary Configuration (optional)
OPENLIBRARY_ENABLED=true
OPENLIBRARY_BASE_URL=https://openlibrary.org
OPENLIBRARY_ACCESS_KEY=
OPENLIBRARY_SECRET_KEY=
```

- `OPENLIBRARY_ENABLED`: Enable/disable OpenLibrary integration (default: true)
- `OPENLIBRARY_BASE_URL`: OpenLibrary API base URL (default: https://openlibrary.org)
- `OPENLIBRARY_ACCESS_KEY` and `OPENLIBRARY_SECRET_KEY`: Optional credentials for write operations (not required for read-only access)

## Download Queue

The server includes a download queue system for automatically downloading books from OpenLibrary/Archive.org.

### Configuration

Add the following to your `.env` file:

```env
# Download Queue Configuration
DOWNLOAD_DIR=/path/to/download/directory
DOWNLOAD_QUEUE_ENABLED=true
DOWNLOAD_AUTO_PROCESS=true
DOWNLOAD_IDLE_SLEEP_SECONDS=60
DOWNLOAD_MAX_CONCURRENT=3
```

- `DOWNLOAD_DIR`: Directory where downloaded books will be saved (required)
- `DOWNLOAD_QUEUE_ENABLED`: Enable/disable download queue (default: true)
- `DOWNLOAD_AUTO_PROCESS`: Enable automatic processing of download queue (default: true)
- `DOWNLOAD_IDLE_SLEEP_SECONDS`: Seconds to wait between queue checks when idle (default: 60)
- `DOWNLOAD_MAX_CONCURRENT`: Maximum concurrent downloads (default: 3)

### API Endpoints

#### Add to Download Queue

**POST** `/api/downloads/queue`

Add a book to the download queue.

```bash
curl -X POST "http://127.0.0.1:6180/api/downloads/queue" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "source": "openlibrary",
    "olid": "OL266687W",
    "ocaid": "hobbit00tolk_0",
    "preferred_format": "PDF",
    "priority": 10
  }'
```

Request fields:
- `title` (required): Book title
- `author` (optional): Book author
- `source` (required): Source type ('openlibrary' or 'archive')
- `source_id` (optional): Source-specific ID
- `olid` (optional): OpenLibrary ID
- `ocaid` (optional): Archive.org identifier
- `download_url` (optional): Direct download URL
- `preferred_format` (optional): Preferred format (PDF, EPUB, Kindle, Daisy) - default: PDF
- `priority` (optional): Download priority (0-100, higher = first) - default: 0

#### Get Download Queue

**GET** `/api/downloads/queue?status={status}&limit={limit}`

Get download queue items with LLM-friendly structured response. This endpoint is designed for agent consumption to provide clear, structured information about the download queue status.

```bash
curl -H "X-API-Key: $API_KEY" \
  "http://127.0.0.1:6180/api/downloads/queue?status=pending&limit=20"
```

Parameters:
- `status`: Filter by status (pending, processing, completed, failed) - optional
- `limit`: Maximum items to return (default: 50, max: 100)

**LLM-Friendly Response Structure:**

```json
{
  "success": true,
  "statistics": {
    "total": 10,
    "pending": 3,
    "processing": 2,
    "completed": 5,
    "failed": 0,
    "added_to_calibre": 3
  },
  "items": [
    {
      "id": 1,
      "title": "The Hobbit",
      "author": "J.R.R. Tolkien",
      "status": "completed",
      "priority": 10,
      "source": "openlibrary",
      "preferred_format": "PDF",
      "created_at": "2024-01-15T10:30:00",
      "calibre_integration": {
        "is_added_to_calibre": true,
        "calibre_book_id": 456,
        "added_at": "2024-01-15T11:00:00"
      },
      "download_info": {
        "file_path": "/downloads/J.R.R. Tolkien - The Hobbit.pdf",
        "file_size": 5242880,
        "downloaded_at": "2024-01-15T10:45:00",
        "error_message": null
      },
      "source_info": {
        "olid": "OL266687W",
        "ocaid": "hobbit00tolk_0",
        "download_url": null
      }
    }
  ],
  "summary": "Download queue contains 10 items: 3 pending, 2 processing, 5 completed, 0 failed. Of the completed downloads, 3 have been added to Calibre.",
  "filter_applied": "pending",
  "limit": 20
}
```

**Agent Usage Example:**

The response includes a natural language `summary` field that agents can use directly, or construct custom responses using the structured data:

```python
response = requests.get("/api/downloads/queue?status=completed")
data = response.json()

# Use the pre-generated summary
print(data["summary"])
# Output: "Download queue contains 10 items: 3 pending, 2 processing, 5 completed, 0 failed. Of the completed downloads, 3 have been added to Calibre."

# Or construct a custom response
added_books = [item for item in data["items"] if item["calibre_integration"]["is_added_to_calibre"]]
print(f"You have {len(added_books)} books ready in your Calibre library.")
```

#### Update Priority

**PUT** `/api/downloads/queue/{item_id}/priority?priority={priority}`

Update the priority of a download queue item.

```bash
curl -X PUT "http://127.0.0.1:6180/api/downloads/queue/123/priority?priority=50" \
  -H "X-API-Key: $API_KEY"
```

#### Delete from Queue

**DELETE** `/api/downloads/queue/{item_id}`

Delete a download queue item.

```bash
curl -X DELETE "http://127.0.0.1:6180/api/downloads/queue/123" \
  -H "X-API-Key: $API_KEY"
```

#### Retry Failed Download

**POST** `/api/downloads/queue/{item_id}/retry`

Retry a failed or completed download.

```bash
curl -X POST "http://127.0.0.1:6180/api/downloads/queue/123/retry" \
  -H "X-API-Key: $API_KEY"
```

#### Mark as Added to Calibre

**POST** `/api/downloads/queue/{item_id}/mark-added?calibre_book_id={calibre_book_id}`

Mark a downloaded book as added to Calibre library. This endpoint is designed for LLM consumption to provide clear, structured responses about the book's status in the download-to-Calibre workflow.

```bash
curl -X POST "http://127.0.0.1:6180/api/downloads/queue/123/mark-added?calibre_book_id=456" \
  -H "X-API-Key: $API_KEY"
```

**LLM-Friendly Response Structure:**

```json
{
  "success": true,
  "message": "Book successfully marked as added to Calibre",
  "book": {
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "file_path": "/downloads/J.R.R. Tolkien - The Hobbit.pdf",
    "file_size": 5242880,
    "format": "PDF",
    "source": "openlibrary",
    "olid": "OL266687W",
    "ocaid": "hobbit00tolk_0"
  },
  "calibre_integration": {
    "calibre_book_id": 456,
    "added_at": "2024-01-15T11:00:00",
    "status": "integrated"
  },
  "timeline": {
    "downloaded_at": "2024-01-15T10:45:00",
    "added_to_calibre_at": "2024-01-15T11:00:00"
  },
  "next_actions": [
    "The book is now available in your Calibre library",
    "You can access it via Calibre with ID: 456",
    "The book file is located at: /downloads/J.R.R. Tolkien - The Hobbit.pdf",
    "You can now search for this book in the catalog"
  ],
  "summary": "The book 'The Hobbit' by J.R.R. Tolkien has been successfully downloaded from openlibrary and added to your Calibre library (ID: 456). The file is available at /downloads/J.R.R. Tolkien - The Hobbit.pdf."
}
```

**Agent Usage Example:**

The response includes a pre-generated `summary` field and `next_actions` array that agents can use to construct natural language responses:

```python
response = requests.post("/api/downloads/queue/123/mark-added?calibre_book_id=456")
data = response.json()

# Use the pre-generated summary
print(data["summary"])
# Output: "The book 'The Hobbit' by J.R.R. Tolkien has been successfully downloaded from openlibrary and added to your Calibre library (ID: 456). The file is available at /downloads/J.R.R. Tolkien - The Hobbit.pdf."

# Or use the next_actions for step-by-step guidance
for action in data["next_actions"]:
    print(f"- {action}")
```

### Background Worker

Run the download worker to automatically process the download queue:

```bash
cd /mnt/Backup_2/Biblioteca/calibre-openclaw-server
python -m app.download_worker
```

The worker will:
- Check for pending downloads at regular intervals
- Download books from OpenLibrary/Archive.org
- Save files to the configured DOWNLOAD_DIR
- Update queue status (pending → processing → completed/failed)
- Handle errors and retry failed downloads

### Dashboard Integration

The dashboard displays download queue status:
- Pending, Processing, Completed, and Failed counts
- Real-time updates via WebSocket
- Statistics included in `/api/stats/database` endpoint

### Download Sources

The download queue supports:

1. **OpenLibrary**: Books with `ocaid` field (Archive.org hosted)
2. **Archive.org**: Direct Archive.org downloads
3. **Direct URLs**: Custom download URLs

When a book is added to the queue:
- If `ocaid` is provided, the worker constructs Archive.org download URLs
- If `download_url` is provided, it's used directly
- The worker checks URL availability before downloading
- Files are saved with sanitized filenames (Author - Title.format)
- Each downloaded file gets a SHA256 hash for tracking

### Download Availability

The system automatically checks if a book can be downloaded automatically:

- **download_available=true**: The book can be downloaded automatically by the worker
- **download_available=false**: Automatic download is not available (e.g., no public domain copy)

When `download_available=false`:
- The book remains in the queue with status 'pending'
- The worker skips it and processes other books
- The user can download manually and mark it as completed
- Use the `mark-manual-download` endpoint to track manual downloads

### Manual Download Tracking

When automatic download is not available, users can download books manually and track them:

#### Mark Manual Download

**POST** `/api/downloads/queue/{item_id}/mark-manual-download?file_path={path}&file_size={size}`

Mark a book as manually downloaded when automatic download was not available.

```bash
curl -X POST "http://127.0.0.1:6180/api/downloads/queue/123/mark-manual-download?file_path=/path/to/book.pdf" \
  -H "X-API-Key: $API_KEY"
```

The endpoint will:
- Calculate the file's SHA256 hash automatically
- Update the queue item status to 'completed'
- Store the file path and hash for later matching
- Return an LLM-friendly response with next steps

#### Match Downloaded File

**GET** `/api/downloads/match?file_hash={hash}` or `?file_path={path}`

Match a downloaded file with the download queue to determine if it can be removed after being added to Calibre.

```bash
# Match by file hash (preferred)
curl -H "X-API-Key: $API_KEY" \
  "http://127.0.0.1:6180/api/downloads/match?file_hash=abc123..."

# Match by file path (alternative)
curl -H "X-API-Key: $API_KEY" \
  "http://127.0.0.1:6180/api/downloads/match?file_path=/path/to/book.pdf"
```

The response includes:
- Whether the file matches a queue item
- The item's status and Calibre integration status
- Whether the item can be removed from the queue (if already added to Calibre)
- Next actions for the user

**Workflow Example:**

1. Agent searches for a book on OpenLibrary
2. Book is added to queue with `download_available=false`
3. User downloads the book manually
4. Agent calls `mark-manual-download` to track the file
5. User adds the book to Calibre
6. Agent calls `mark-added` with the Calibre book ID
7. Agent can now remove the item from the queue (optional cleanup)

### API Endpoints

#### Enrich a Single Book

**POST** `/api/books/{book_id}/openlibrary/enrich`

Enrich a book with metadata from OpenLibrary by ISBN or title/author match.

```bash
curl -X POST "http://127.0.0.1:6180/api/books/123/openlibrary/enrich" \
  -H "X-API-Key: $API_KEY"
```

#### Get Download Links

**GET** `/api/books/{book_id}/openlibrary/download-links`

Get download links for public domain books from OpenLibrary/Archive.org.

```bash
curl -H "X-API-Key: $API_KEY" \
  "http://127.0.0.1:6180/api/books/123/openlibrary/download-links"
```

Response includes:
- Preview and read URLs
- Download formats (PDF, EPUB, Kindle, Daisy)
- Public domain status

#### Bulk Enrichment

**POST** `/api/books/openlibrary/bulk-enrich?limit=100`

Enrich all books in the database with OpenLibrary metadata.

```bash
curl -X POST "http://127.0.0.1:6180/api/books/openlibrary/bulk-enrich?limit=100" \
  -H "X-API-Key: $API_KEY"
```

### Features

- **ISBN Search**: Search books by ISBN-10 or ISBN-13
- **Title/Author Search**: Fallback search by title and author when ISBN is not available
- **Author Information**: Retrieve author details and work counts
- **Download Links**: Get direct download links for public domain books from Archive.org
- **Metadata Enrichment**: Automatically enrich book metadata with OpenLibrary data including:
  - Cover images
  - Publisher information
  - Publication dates
  - Page counts
  - Subjects and languages
  - Descriptions and notes

### Search Endpoints

#### Integrated Catalog Search

**GET** `/api/search?query={query}&limit={limit}&openlibrary_search={true|false}`

Search across local catalog, OpenLibrary, and semantic search (fallback).

```bash
curl "http://127.0.0.1:6180/api/search?query=hobbit&limit=20&openlibrary_search=true"
```

Parameters:
- `query`: Search query (required)
- `limit`: Maximum results (default: 50, max: 100)
- `openlibrary_search`: Include OpenLibrary results (default: true)
- `semantic_fallback`: Enable semantic search fallback (default: true)
- `semantic_threshold`: Similarity threshold for semantic search (default: 0.3)

#### OpenLibrary-Only Search

**GET** `/api/search/openlibrary?query={query}&limit={limit}&author={author}`

Search only OpenLibrary API for books.

```bash
curl "http://127.0.0.1:6180/api/search/openlibrary?query=hobbit&limit=20&author=tolkien"
```

Parameters:
- `query`: Search query (required)
- `limit`: Maximum results (default: 20, max: 100)
- `author`: Optional author name to narrow search

Response includes:
- Book title and author
- OpenLibrary ID (OLID)
- Cover image URL
- Preview URL (link to OpenLibrary page)
- First publication year
- List of authors

## Local Client

```bash
node scripts/books-api-client.mjs docs
node scripts/books-api-client.mjs paths
node scripts/books-api-client.mjs search "term" --limit 10
node scripts/books-api-client.mjs book 123
node scripts/books-api-client.mjs request GET /books --query q=python
```

## Manual RAG

To process embeddings continuously outside the nightly window:

```bash
cd skills/calibre-ebooks
./calibre-openclaw-server/run-rag.sh
```

By default `run-rag.sh` runs until `Ctrl+C`. To enforce a stop time in manual
execution:

```env
RAG_RUN_STOP_AT_LOCAL=18:00
```

You can also pass the limit directly:

```bash
./calibre-openclaw-server/run-rag.sh --stop-at-local 18:00
```

## Scheduled RAG

The nightly service is generated by `install_service.sh` and reads the schedule
from `.env`. There is no fixed time in the code.

```env
RAG_STOP_AT_LOCAL=06:00
RAG_TIMER_ON_CALENDAR=*-*-* 01:00:00
RAG_RUNTIME_MAX_SEC=5h
RAG_SERVICE_CONTINUOUS=true
RAG_IDLE_SLEEP_SECONDS=60
RAG_PREFETCH_RANDOM_BOOKS=false
RAG_RECONCILE_ON_START=false
RAG_ALLOW_MODEL_PULL=false
INSTALL_NIGHTLY_EMBEDDINGS=false
```

Meaning:

- `RAG_TIMER_ON_CALENDAR`: when the systemd timer starts the worker.
- `RAG_STOP_AT_LOCAL`: local time when the worker stops starting new books.
- `RAG_RUNTIME_MAX_SEC`: maximum limit imposed by systemd.
- `RAG_SERVICE_CONTINUOUS`: keeps the worker looking for new books while there is a window.
- `RAG_IDLE_SLEEP_SECONDS`: pause between checks when there is no queue.
- `RAG_PREFETCH_RANDOM_BOOKS`: allows automatically queuing books when the queue is empty.
- `RAG_RECONCILE_ON_START`: allows invalidating old embeddings when the signature changes.
- `RAG_ALLOW_MODEL_PULL`: allows the helper script to run `ollama pull` if the model is missing.
- `INSTALL_NIGHTLY_EMBEDDINGS`: allows installing and enabling the nightly timer.

To disable the worker's internal time limit, leave `RAG_STOP_AT_LOCAL` empty.
In this case, use `RAG_RUNTIME_MAX_SEC` or control the time via systemd itself.

## Install Services

```bash
cd skills/calibre-ebooks/calibre-openclaw-server
./install_service.sh install
```

Services created:

- `calibre-openclaw-server.service`
- `calibre-openclaw-server-nightly-embeddings.service`
- `calibre-openclaw-server-nightly-embeddings.timer`

Useful commands:

```bash
sudo systemctl status calibre-openclaw-server.service
sudo systemctl restart calibre-openclaw-server.service
sudo systemctl status calibre-openclaw-server-nightly-embeddings.timer
sudo systemctl start calibre-openclaw-server-nightly-embeddings.service
```

## Database

The server always uses the database defined in `POSTGRESQL_DB_DATABASE`.
On startup, it creates the necessary tables if they don't exist.

Main tables:

- `books`
- `book_chunks`
- `processing_queue`
- `settings`

## Dashboard

The dashboard is served at `/` and offers real-time monitoring and a
**RAG Test Search** panel to test semantic search directly on the indexed base.

- Query field, number of results (1–50) and similarity threshold (0–1).
- Results show title, author, citation (page and section/chapter), similarity
  and the corresponding excerpt.
- The request uses `POST /api/search/content` with the same API key as the
  dashboard (entered once via prompt and sent as `Authorization: Bearer`).
- The returned content is treated as untrusted and escaped before rendering,
  preventing HTML injection.

> Semantic search requires the query parameter to be cast to `vector`
> (`%s::vector`) in the pgvector `<=>` operator; without the explicit cast,
> PostgreSQL rejects the `vector <=> numeric[]` comparison.

## Embedding Statistics

RAG statistics distinguish the complete catalog from actually indexed books:

- `books.total`: all Calibre books synchronized (`books`).
- `books.with_embeddings` / `embeddings.indexed_books`: books that already have
  embeddings in `book_chunks`.
- `embeddings.avg_chunks_per_indexed_book`: average chunks per **indexed**
  book (correct metric for diagnostics).
- `embeddings.avg_chunks_per_catalog_book`: average over the entire catalog,
  artificially low while most titles have not been processed.

> The "per book" average should be read over indexed books. Dividing the total
> number of chunks by the entire catalog produces a small and misleading number
> (e.g., ~4 chunks/book when the real value per indexed book is in the hundreds).

### Content Diagnostics

Endpoint: `GET /api/stats/content-insights`

Returns, for content already with embeddings:

- `distribution`: number of indexed books, total chunks, average, minimum,
  maximum and median of chunks per indexed book.
- `top_relevant_words`: most relevant words (frequency via `ts_stat`
  on a random sample; PT/EN stopwords, short tokens and non-alphabetic
  tokens are discarded).
- `top_concepts`: most cited concepts, derived from detected section/chapter
  titles.

Query parameters (all optional and validated/limited in backend):

| Parameter | Default | Description |
| --------- | ------- | ----------- |
| `top_words` | 25 | Number of relevant words (1–200). |
| `top_concepts` | 15 | Number of concepts. |
| `sample_size` | 6000 | Sample of chunks for frequency (1–50000). |
| `min_word_length` | 4 | Minimum word length (1–40). |
| `language` | `simple` | Text search configuration: `simple`, `english` or `portuguese`. |

Example:

```bash
curl -H "X-API-Key: $API_KEY" \
  "http://127.0.0.1:6180/api/stats/content-insights?top_words=30&language=simple"
```

## Synchronization

When this folder is used in more than one location, keep code copies synchronized
and preserve local files such as `.env`, `.venv` and `logs/`.

Example:

```bash
rsync -avc \
  --exclude '.env' \
  --exclude '.venv/' \
  --exclude 'logs/' \
  --exclude '__pycache__/' \
  skills/calibre-ebooks/calibre-openclaw-server/ \
  /mnt/Backup_2/Biblioteca/calibre-openclaw-server/
```
