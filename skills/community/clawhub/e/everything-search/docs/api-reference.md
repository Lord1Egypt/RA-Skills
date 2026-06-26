# API Reference

Complete API documentation for Everything Search skill.

## Table of Contents

- [EverythingSearch Class](#everythingsearch-class)
- [SearchResult Class](#searchresult-class)
- [SearchItem Class](#searchitem-class)
- [Utility Functions](#utility-functions)
- [Examples](#examples)

---

## EverythingSearch Class

Main class for interacting with Everything HTTP Server API.

### Constructor

```python
EverythingSearch(host: str = "127.0.0.1", port: int = 2853, timeout: int = 10)
```

**Parameters:**
- `host` (str): Server hostname (default: "127.0.0.1")
- `port` (int): Server port (default: 2853)
- `timeout` (int): Request timeout in seconds (default: 10)

**Example:**
```python
from src.everything_search import EverythingSearch

search = EverythingSearch(port=2853)
```

---

### Methods

#### search()

Execute a file/folder search.

```python
search(
    keyword: str,
    file_type: Optional[str] = None,
    min_size: Optional[str] = None,
    max_size: Optional[str] = None,
    path: Optional[str] = None,
    exclude_path: Optional[str] = None,
    modified_after: Optional[str] = None,
    max_results: int = 100,
    include_size: bool = True
) -> SearchResult
```

**Parameters:**
- `keyword` (str): Search keyword (supports Chinese)
- `file_type` (str, optional): Filter by extension (e.g., "jpg", "pdf")
- `min_size` (str, optional): Minimum size (e.g., "1mb", "100kb")
- `max_size` (str, optional): Maximum size
- `path` (str, optional): Search only in this path
- `exclude_path` (str, optional): Exclude this path
- `modified_after` (str, optional): Only files modified after date (YYYY-MM-DD)
- `max_results` (int): Maximum results to return (default: 100)
- `include_size` (bool): Include file size in results (default: True)

**Returns:**
- `SearchResult` object with total count and list of items

**Example:**
```python
# Basic search
results = search.search("数据资产")

# Search with filters
results = search.search(
    "报告",
    file_type="pdf",
    min_size="1mb",
    max_results=20
)

# Search by date
results = search.search("文档", modified_after="2024-01-01")
```

---

#### search_photos()

Search for photos of a specific person.

```python
search_photos(person_name: str, formats: List[str] = None) -> SearchResult
```

**Parameters:**
- `person_name` (str): Person's name (e.g., "张三")
- `formats` (List[str], optional): Image formats (default: ["jpg", "png"])

**Returns:**
- `SearchResult` with photo files

**Example:**
```python
results = search.search_photos("张三")
print(f"Found {results.total} photos")
```

---

#### search_documents()

Search for document files.

```python
search_documents(keyword: str, doc_types: List[str] = None) -> SearchResult
```

**Parameters:**
- `keyword` (str): Search keyword
- `doc_types` (List[str], optional): Document types (default: ["pdf", "docx", "xlsx", "pptx"])

**Returns:**
- `SearchResult` with document files

**Example:**
```python
results = search.search_documents("年度报告")
```

---

#### check_connection()

Check if Everything HTTP Server is accessible.

```python
check_connection() -> bool
```

**Returns:**
- `True` if connection successful, `False` otherwise

**Example:**
```python
if search.check_connection():
    print("Server is online")
else:
    print("Server is offline")
```

---

## SearchResult Class

Represents complete search results.

### Attributes

```python
@dataclass
class SearchResult:
    keyword: str          # Search keyword used
    total: int            # Total number of matches
    items: List[SearchItem]  # List of search result items
    query_time: float     # Query execution time in seconds
```

**Example:**
```python
results = search.search("数据")
print(f"Found {results.total} results")
print(f"Query took {results.query_time:.2f} seconds")
print(f"First result: {results.items[0].name}")
```

---

## SearchItem Class

Represents a single search result item.

### Attributes

```python
@dataclass
class SearchItem:
    name: str              # File/folder name
    path: str              # Parent directory path
    full_path: str         # Complete file path
    item_type: str         # "file" or "folder"
    size: int = 0          # File size in bytes
    date_modified: Optional[str] = None  # Last modified date
```

### Methods

#### format_size()

Format file size in human-readable format.

```python
format_size() -> str
```

**Returns:**
- Formatted string (e.g., "1.5 MB", "256 KB")

**Example:**
```python
for item in results.items:
    print(f"{item.name} - {item.format_size()}")
```

---

## Utility Functions

### format_size()

Format file size in bytes to human-readable string.

```python
format_size(size_bytes: int) -> str
```

**Example:**
```python
from src.utils import format_size

print(format_size(1048576))  # Output: "1.0 MB"
print(format_size(2048))     # Output: "2.0 KB"
```

---

### encode_keyword()

URL-encode a search keyword (handles Chinese).

```python
encode_keyword(keyword: str) -> str
```

**Example:**
```python
from src.utils import encode_keyword

encoded = encode_keyword("数据资产")
# Output: "%E6%95%B0%E6%8D%AE%E8%B5%84%E4%BA%A7"
```

---

### check_connection()

Check if Everything HTTP Server is accessible.

```python
check_connection(host: str = "127.0.0.1", port: int = 2853, timeout: int = 3) -> bool
```

**Example:**
```python
from src.utils import check_connection

if check_connection(port=2853):
    print("Server is online")
```

---

### get_file_extension()

Get file extension from filename.

```python
get_file_extension(filename: str) -> str
```

**Example:**
```python
get_file_extension("document.pdf")  # Returns: "pdf"
get_file_extension("image.JPG")     # Returns: "jpg"
```

---

### is_image_file()

Check if file is an image.

```python
is_image_file(filename: str) -> bool
```

**Example:**
```python
is_image_file("photo.jpg")  # Returns: True
is_image_file("doc.pdf")    # Returns: False
```

---

### is_document_file()

Check if file is a document.

```python
is_document_file(filename: str) -> bool
```

**Example:**
```python
is_document_file("report.pdf")   # Returns: True
is_document_file("data.xlsx")    # Returns: True
is_document_file("photo.jpg")    # Returns: False
```

---

### is_archive_file()

Check if file is an archive.

```python
is_archive_file(filename: str) -> bool
```

**Example:**
```python
is_archive_file("backup.zip")    # Returns: True
is_archive_file("archive.tar")   # Returns: True
```

---

## Convenience Functions

### quick_search()

Quick search function - returns list of full paths.

```python
quick_search(keyword: str, port: int = 2853, max_results: int = 20) -> List[str]
```

**Example:**
```python
from src.everything_search import quick_search

paths = quick_search("数据资产")
for path in paths:
    print(path)
```

---

## Examples

### Basic Search

```python
from src.everything_search import EverythingSearch

# Initialize
search = EverythingSearch(port=2853)

# Check connection
if not search.check_connection():
    print("Server offline")
    exit(1)

# Search
results = search.search("数据资产", max_results=10)

# Display results
print(f"Found {results.total} results")
for item in results.items:
    print(f"  {item.full_path} ({item.format_size()})")
```

### Advanced Search with Filters

```python
from src.everything_search import EverythingSearch

search = EverythingSearch()

# Search PDF files larger than 1MB
results = search.search(
    "年度报告",
    file_type="pdf",
    min_size="1mb",
    max_results=20
)

# Search in specific path
results = search.search(
    "合同",
    path="D:\\Documents\\Legal",
    max_results=10
)

# Search by date
results = search.search(
    "报告",
    modified_after="2024-01-01",
    max_results=20
)
```

### Search Photos

```python
from src.everything_search import EverythingSearch

search = EverythingSearch()

# Search for photos
results = search.search_photos("张三")

print(f"Found {results.total} photos")

# Group by format
jpg_count = sum(1 for item in results.items if item.name.lower().endswith('.jpg'))
png_count = sum(1 for item in results.items if item.name.lower().endswith('.png'))

print(f"  JPG: {jpg_count}")
print(f"  PNG: {png_count}")
```

### Batch Search

```python
from src.everything_search import EverythingSearch

search = EverythingSearch()

keywords = ["数据资产", "年度报告", "合同"]

for keyword in keywords:
    results = search.search(keyword, max_results=5)
    print(f"{keyword}: {results.total} results")
```

---

## Error Handling

```python
from src.everything_search import EverythingSearch
from urllib.error import URLError

search = EverythingSearch()

try:
    results = search.search("数据资产")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except RuntimeError as e:
    print(f"Search failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

**Last Updated:** 2024-04-02  
**Version:** 1.0.0
