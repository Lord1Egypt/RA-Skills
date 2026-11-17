# Ebook selection, archive containers and tags

## Inclusion and exclusion

Save actual referenced ebook files: PDF, EPUB/KEPUB, MOBI, AZW/AZW3/AZW4, PRC, FB2, DjVu, CBZ/CBR/CB7. These are the helper's explicit supported formats, not every format that Calibre can theoretically convert. A renamed HTML error page is not a book. DRM/encryption and unfamiliar formats are not invitations to bypass controls or guess.

Save books contained in ZIP, 7z, RAR or TAR containers, including TAR.GZ/BZ2/XZ. The container is temporary intake packaging: extract selected ebook members and register those as individual books. Once all selected imports are verified, trash this task's downloaded container rather than retaining another backup. A collection may include irrelevant ebooks; select the referenced/requested subset, not every member automatically.

Do not save Web clips, HTML/MHTML/HTMLZ, article Markdown/TXT, browser printouts, synthetic EPUB/PDF summaries or search-result listings. A webpage can identify the author/title/source URL or expose a direct ebook download without being archived itself. If there is no ebook, leave the webpage unarchived; do not manufacture one to satisfy the archive workflow.

EPUB/KEPUB, CBZ, CBR and CB7 are books in their own right; never treat them as outer containers or recursively extract their internal resources. PDF/EPUB ebook originals with published layout should not be OCR'd/rebuilt by default.

## Archive safety and provenance

Use scripts/ebook_archive.py list before extract. The libarchive C API reads known native ZIP/7z/RAR/TAR formats and none/gzip/bzip2/xz filters; it never runs external decompressors, document code or commands found in filenames.

- Inventory is bounded: input <=1 GiB, <=2000 entries, each declared member <=200 MiB, total expanded sizes <=512 MiB. Normal invocation has a 120-second process alarm on platforms supporting SIGALRM, plus per-operation elapsed-time checks. Do not disable limits to force a bomb or an unexplained huge file through.
- Reject links, device/special files, encrypted entries, traversal/absolute/drive paths, duplicate/case-colliding paths and invalid names. Some archive formats normalize backslashes before validation. Extraction never uses member names as output paths: one selected member goes to a new private directory as ebook.EXT.
- Validate every entry before extracting even one ebook. Output must be new and is not overwritten. A failure may leave ebook.partial; it is not a ready book and must not be imported.
- Nested containers and non-book members are ignored, not recursively unpacked. An empty members list is an explicit no-eligible-books result. Unsupported archives, native decoder warnings and missing libarchive are failures, not empty success.
- Extract binds the reviewed archive SHA256 and member ID, checks size/hash again, then emits extraction.json. Keep the task-owned archive only until all selected members have verified stored copies in Calibre, then trash it along with redundant task-owned extractions. Keep failed/pending work for recovery, not indefinitely after success. Do not silently retry extraction over an existing output directory.
- Source URL is the clean archive download/landing URL. Copy archive_member and archive_sha256 from the receipt to the individual book manifest. refsource is based on canonical URL + member path, while refsha256 is the extracted ebook's content hash. Do not give all members a single source identity or invent fragment/query suffixes.

An identical ebook from a direct URL and a container is caught by its file hash. Different extraction bytes, renamed members or alternate URLs still require bibliographic review. Existing records are not retroactively indexed. If the same source/member changes version, preserve the old record and resolve the version policy instead of replacing it automatically.

## Metadata and tags

Use a stable clean source_url and an evidenced canonical_url when different. Known tracking parameters/fragments are removed; meaningful version/language/query parameters remain. Consulted pages/sections go in location. File coverage and read coverage are different: consulting 5 pages of an intact 300-page PDF does not make the stored file partial.

No retrieval date. Calibre assigns its registration timestamp. published_date is the source's publication date only; omit when unknown.

Before selecting tags, save a read-only `id,title,tags` catalog lookup and derive its exact vocabulary; inspect related books' tags as well. If the lookup fails or is truncated, resolve that gap before creating a new spelling. A small related-book sample alone cannot establish that an equivalent type label is absent.

Choose a small set describing the document itself:

- Reuse the established type label, e.g. マニュアル or 論文. Never create 種別.マニュアル alongside マニュアル, or 種別.論文 alongside 論文. Where synonyms such as manual and マニュアル already coexist, use the established Japanese label for new imports unless the user specifies otherwise; do not copy both or silently rename existing records.
- Reuse 1-3 evidenced topics/products, e.g. Calibre, OpenClaw, TRPG, 電気設備. A manufacturer or product label must actually identify the document's subject.
- 資料 may be reused for research references when it is already an established label; don't add it just to satisfy a tag count.
- If no equivalent label exists, use a concise plain-language tag grounded in the document. Do not invent a prefixed taxonomy merely because examples show dotted names.
- Do not add 用途.設定 / 用途.トラブルシュート / 用途.比較 / 用途.設計 by default: why this conversation consulted a book is not the book's subject. Use purpose labels only when the user explicitly requests that classification.
- 抜粋 only for an actually incomplete stored ebook, with an explanatory note; not for a fully stored book read only in part. Do not create the old dotted 状態.抜粋 label in new imports.

Aim for a few useful tags, not URL/date/session IDs or every keyword. Fewer than 3 is fine when that is all the evidence supports. Do not add 既読, ai-summary or cached-analysis simply because a book was referenced. Do not remove existing tags or globally retag the library. Before apply, compare the chosen tags against the saved vocabulary and explain any genuinely new tag in the local plan/review record.

Search examples: tags:"=資料", tags:"=Calibre", tags:"=マニュアル". UI saved-search/virtual-library changes are separate from ordinary import.
