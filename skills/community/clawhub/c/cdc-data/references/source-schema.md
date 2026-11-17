# Source adapter and page schema

## Adapter fields

| Field | Meaning |
|---|---|
| `id` | Stable report type and registry key |
| `index_url` | Official initial listing URL |
| `allowed_path_prefix` | Prefix passed to the verified PDF downloader |
| `period_type` | `week` or `month` |
| `content_mode` | `html_with_pdf`, `html`, or `pdf` |
| `title_pattern` | Anchored title parser with named period groups |
| `pagination_mode` | Semantic discovery strategy, not a fixed count |
| `transport_preference` | `browser_first` for registered sources; `http_first` and `browser_required` remain reserved adapter values |
| `supports_issue_number` | Whether exact issue queries are legal |
| `index_marker` | Text that confirms the correct index |
| `allowed_url_patterns` | Immutable navigation permission boundary |
| `adapter_version` | Semantic version for route/parser behavior |

## List page

Extract `link_text`, `href`, adjacent/displayed `publish_date`, and `source_page_url`. Normalize repeated whitespace before applying the anchored title regex. Resolve `href` against `source_page_url`. Only valid title links become records.

Discover pages using links labeled `下一页`, `尾页`, or numeric page labels. Current observed paths use the first page `/` or `index.html` and later pages `index_N.html`, but derive them from links rather than generating a fixed range.

Examples:

- `2026年第28周第917期中国流感监测周报` → year 2026, week 28, issue 917.
- `2026年第28周全国急性呼吸道传染病哨点监测情况` → year 2026, week 28.
- `全国新型冠状病毒感染疫情情况（2026年6月）` → year 2026, month 6.
- `2026 年 6 月全球传染病事件风险评估` → year 2026, month 6.
- `2026年6月中国需关注的突发公共卫生事件风险评估` → year 2026, month 6.

## Detail page and carriers

For HTML detail pages, record final URL, heading/title, displayed publication date if available, main body, and attachment anchors. Require semantic agreement with the list title and adapter.

Attachment types:

- `.pdf` or `application/pdf` → `pdf`
- `.doc`/`.docx` → `word`
- `.xls`/`.xlsx` → `excel`
- Otherwise use `unknown` and warn.

For direct PDF list entries, the list link supplies `document_url`; do not fabricate a detail page. For HTML-only entries, set `document_url=null`. For HTML+PDF, verify both carriers.

## Transport order

Use an isolated named agent-browser session first for index and detail access. Verify document links from the detail/list page without opening the document viewer. For index/detail recovery, fall back to ordinary HTTP only after recording a concrete browser failure such as startup failure, navigation timeout, invalid final URL, missing semantic marker, or failed carrier assertion. Apply the same URL, title, content-type, and nonempty-body validation to that HTTP page result. Authorized document bytes always flow through `scripts/download_official_document.py` after URL verification; this is the standard transfer path, not a browser-download fallback.
