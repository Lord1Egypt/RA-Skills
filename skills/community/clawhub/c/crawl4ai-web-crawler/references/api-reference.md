# Crawl4AI API Reference

Detailed class and parameter reference. Read the main SKILL.md first before using this reference.

## BrowserConfig

```python
BrowserConfig(
    browser_type: str = "chromium",        # "chromium" | "firefox" | "webkit"
    headless: bool = True,
    viewport_width: int = 1080,
    viewport_height: int = 600,
    user_agent: Optional[str] = None,      # Custom User-Agent
    proxy: Optional[str] = None,            # Proxy URL
    proxy_config: Optional[dict] = None,    # Advanced proxy configuration
    use_managed_browser: bool = False,      # Use an existing browser (anti-detection)
    user_data_dir: Optional[str] = None,    # Browser profile path
    channel: Optional[str] = None,          # Playwright channel
    ignore_https_errors: bool = True,
    java_script_enabled: bool = True,
    cookies: list = [],                     # Pre-set cookies
    headers: dict = {},                     # Additional HTTP headers
    accept_downloads: bool = False,
    downloads_path: Optional[str] = None,
    storage_state: Optional[str] = None,    # Authentication state file path
    text_mode: bool = False,                # Disable image loading (faster)
    light_mode: bool = False,               # Lightweight mode
    verbose: bool = True,
    extra_args: Optional[list] = None,      # Additional browser launch arguments
    cdp_url: Optional[str] = None,          # Connect to remote Chrome DevTools
)
```

## CrawlerRunConfig

```python
CrawlerRunConfig(
    # Cache
    cache_mode: CacheMode = CacheMode.BYPASS,   # BYPASS | ENABLED | WRITE_ONLY | READ_ONLY
    
    # Content Extraction
    css_selector: Optional[str] = None,          # Only extract matching CSS regions
    word_count_threshold: int = 10,              # Filter short text (discard if below this value)
    excluded_tags: list = [],                     # Excluded HTML tags
    excluded_selector: Optional[str] = None,      # Excluded CSS selector
    keep_data_attributes: bool = False,           # Preserve data-* attributes
    remove_forms: bool = False,
    remove_overlay_elements: bool = False,        # Remove pop-ups/masks
    
    # Markdown Generation
    markdown_generator: Optional[DefaultMarkdownGenerator] = None,
    
    # Extraction Strategy
    extraction_strategy: Optional = None,         # JsonCssExtractionStrategy | LLMExtractionStrategy
    
    # Dynamic Pages
    js_code: Optional[list] = None,               # List of JS code snippets to execute
    js_only: bool = False,                        # Use JS only (do not load HTML)
    wait_for: Optional[str] = None,               # CSS selector to wait for
    wait_for_images: bool = False,                # Wait for images to load
    delay_before_return_html: float = 0.0,        # Additional wait in seconds before returning
    page_timeout: int = 60000,                    # Page load timeout (ms)
    
    # Media
    screenshot: bool = False,
    screenshot_wait_for: Optional[float] = None,  # Wait before taking screenshot
    pdf: bool = False,
    
    # Session
    session_id: Optional[str] = None,             # Reuse browser session
    magic: bool = False,                          # Automatic anti-detection
    
    # Hooks
    on_before_goto: Optional = None,              # Callback before navigation
    on_after_goto: Optional = None,               # Callback after navigation
    
    # Links
    extract_links: bool = True,
    check_robots_txt: bool = False,
    
    # LLM Content Filtering
    llm_filter: Optional[str] = None,             # LLM instruction to filter content
    
    # Deep Crawl
    deep_crawl_strategy: Optional = None,          # BFSDeepCrawlStrategy | BestFirstCrawlStrategy
    
    # Adaptive Crawl
    adaptive_config: Optional[AdaptiveConfig] = None,
    
    # Other
    scan_full_page: bool = False,                 # Full page scroll
    process_iframes: bool = False,
    remove_overlay_elements: bool = False,
    mean_delay: float = 0.1,                      # Average delay between requests
    max_range: float = 0.3,                       # Random range for delay
    verbose: bool = True,
)
```

## CacheMode

```python
class CacheMode:
    BYPASS = "bypass"           # Do not use cache; re-crawl every time
    ENABLED = "enabled"         # Read from and write to cache
    WRITE_ONLY = "write_only"   # Write only, do not read
    READ_ONLY = "read_only"     # Read only, do not write (return cached results only)
```

## LLMConfig

```python
LLMConfig(
    provider: str,              # e.g., "openai/gpt-4o", "ollama/llama3.3", "anthropic/claude-3"
    api_token: Optional[str] = None,   # API key (can be left blank for local models)
    base_url: Optional[str] = None,    # Custom API endpoint
    temperature: float = 0.0,
    max_tokens: int = 2000,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
)
```

Supported provider prefixes (via LiteLLM):
- `openai/` — OpenAI models (gpt-4o, gpt-4o-mini, gpt-4, ...)
- `ollama/` — Local Ollama models (llama3.3, qwen2.5, ...)
- `anthropic/` — Claude models (claude-3-5-sonnet, ...)
- `groq/` — Groq models
- `deepseek/` — DeepSeek models
- `gemini/` — Google Gemini
- And all other providers supported by LiteLLM

## LLMExtractionStrategy

```python
LLMExtractionStrategy(
    llm_config: LLMConfig,
    schema: Optional[dict] = None,               # Pydantic model_json_schema()
    extraction_type: str = "schema",             # "schema" | "block"
    instruction: Optional[str] = None,           # Prompt for the LLM
    chunk_token_threshold: int = 4000,           # Chunking threshold
    overlap_rate: float = 0.1,                   # Chunk overlap rate
    apply_chunking: bool = True,
    input_format: str = "markdown",              # "markdown" | "html" | "fit_markdown"
    extra_args: Optional[dict] = None,           # temperature, max_tokens, etc.
    verbose: bool = False,
)
```

Methods:
- `show_usage()` — Print token usage and cost
- `generate_schema(html, llm_config)` — Class method, auto-generates a CSS extraction schema

## JsonCssExtractionStrategy

```python
JsonCssExtractionStrategy(
    schema: dict,       # Schema definition
    verbose: bool = False
)
```

Schema format:
```python
{
    "name": "SchemaName",
    "baseSelector": "div.item",           # CSS selector for repeating elements (optional)
    "fields": [
        {
            "name": "field_name",          # Key in the output JSON
            "selector": "h2.title",        # CSS selector
            "type": "text",                # "text" | "attribute" | "html" | "regex"
            "attribute": "href",           # Attribute name when type="attribute"
            "regex": r"pattern",           # Extraction pattern when type="regex"
            "transform": lambda x: ...,    # Optional transformation function
            "default": "N/A"               # Default value
        }
    ]
}
```

Class method:
- `generate_schema(html, llm_config, target_elements_description="...")` — Auto-generate schema via LLM

## JsonXPathExtractionStrategy

Similar to `JsonCssExtractionStrategy`, but uses XPath expressions in the `selector` field for each field.

## BFSDeepCrawlStrategy

```python
BFSDeepCrawlStrategy(
    max_depth: int = 3,
    max_pages: int = 50,
    include_paths: Optional[list] = None,      # Whitelist paths, e.g., ["/docs/*"]
    exclude_paths: Optional[list] = None,      # Blacklist paths, e.g., ["/blog/*"]
    filter_patterns: Optional[list] = None,
    url_filter: Optional[callable] = None,     # Custom URL filter
    on_result: Optional[callable] = None,       # Per-page result callback
)
```

## Content Filters

### PruningContentFilter

```python
PruningContentFilter(
    threshold: float = 0.5,               # 0-1; the lower the score, the more is pruned
    threshold_type: str = "dynamic",      # "fixed" | "dynamic"
    min_word_threshold: int = 0,          # Minimum word count threshold
)
```

### BM25ContentFilter

```python
BM25ContentFilter(
    user_query: Optional[str] = None,     # Search query, used for relevance scoring
    bm25_threshold: float = 1.0,          # BM25 score threshold
)
```

## CrawlResult

```python
result.url: str                          # Final URL
result.html: str                         # Raw HTML
result.cleaned_html: str                 # Cleaned HTML
result.markdown: MarkdownGenerationResult # Markdown result
result.markdown.raw_markdown: str        # Raw Markdown
result.markdown.fit_markdown: str        # Filtered Markdown
result.markdown.references_markdown: str # Reference list Markdown
result.extracted_content: str            # Extracted JSON string
result.screenshot: str                   # Base64 screenshot
result.pdf: str                          # Base64 PDF
result.media: dict                       # {"images": [...], "videos": [...]}
result.links: dict                       # {"internal": [...], "external": [...]}
result.metadata: dict                    # Page metadata
result.success: bool                     # Whether the crawl was successful
result.error_message: str                # Error message
result.status_code: int                  # HTTP status code
result.response_headers: dict            # Response headers
result.downloaded_files: list            # Paths of downloaded files
```

## Complete CLI Reference

```bash
crwl <url> [options]

Options:
  -o, --output FORMAT     Output format: markdown, html, cleaned_html, screenshot, all
  -q, --question TEXT     Ask the LLM a question (requires API key configuration)
  --css-selector TEXT     CSS selector to limit the crawl scope
  --deep-crawl STRATEGY   Deep crawl strategy: bfs
  --max-pages N           Maximum number of pages for deep crawl
  --max-depth N           Maximum depth for deep crawl
  --screenshot            Take a page screenshot
  --json                  Output in JSON format
  --headless / --no-headless  Whether to run in headless mode
  --verbose               Verbose output
```

Environment Variables:
- `OPENAI_API_KEY` — OpenAI API key for LLM extraction
- `CRAWL4AI_CACHE_DIR` — Cache directory