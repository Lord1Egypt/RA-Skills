---
name: calibre-reference-ingest
description: "Archive referenced ebook files (PDF, EPUB, Kindle, FB2, DjVu, comic books) and ebooks inside ZIP/7z/RAR/TAR archives into Calibre with source URLs and useful tags. Invoke proactively during research under a standing auto-save instruction, without waiting for a save request. Exclude Web clips, HTML/Markdown/TXT captures, search-result pages and unused hits."
metadata: {"openclaw":{"requires":{"bins":["python3","calibredb"]},"optionalBins":["trash"],"optionalEnv":["CALIBRE_WITH_LIBRARY","CALIBRE_USERNAME","CALIBRE_PASSWORD"],"localWrites":["private ebook/archive staging, plans and receipts"],"modifiesRemoteData":["calibre:new reference books and their metadata"]}}
---

# Archive ebook originals, not Web clips

1. Establish the selected files and destination. Resolve this skill's absolute directory as {baseDir}. Read the workspace AGENTS.md Tools notes for the existing Calibre endpoint/authentication; use calibre-catalog-read to check the library, similar titles and related tags. Use CLI #LIBRARY_ID, not browser #library_id=. Do not start a server, scan networks or silently create another library.
   - Under a standing auto-save instruction, save relevant ebook files actually used in research and tag them without waiting for "save this" or asking routine per-file permission. Explicit archival requests also authorize ordinary new imports and sensible tags. Without either form of authorization, propose saving instead of assuming permission.
   - **Scope: original ebook files and archive containers containing them. No Web clips.** Do not save web article text, HTML/MHTML, Markdown/TXT captures, search-result pages, generated summary books or browser-printed PDFs. Do not convert a webpage to EPUB/PDF to circumvent this scope. Webpages may supply bibliographic evidence or links to genuine ebook downloads; archive the ebook file, not the page.
   - Save a finite referenced set, not every search hit or an entire website. Reuse identical existing books; do not silently backfill unrelated past conversations. Existing-library authorization does not authorize a new public/shared destination, credential-bearing content, deletion or replacement of records.
   - Completion: finite supported file list, authorized destination and read-only candidate/tag checks. Distinguish lookup failure from no matches.

2. Acquire and inspect ebook originals. Read [references/capture-and-tags.md](references/capture-and-tags.md) for file selection, archive handling and tags.
   - Preserve the downloaded bytes; do not regenerate, OCR, repackage or convert files by default. Supported originals: PDF, EPUB/KEPUB, MOBI, AZW/AZW3/AZW4, PRC, FB2, DjVu, CBZ/CBR/CB7. Format headers are sanity checks, not full validation, malware scanning or proof of complete download. Inspect the source title, relevant pages and format readability when needed.
   - Do not bypass access controls, DRM or paywalls. Already-authorized private material stays in its appropriate designated library; new disclosure needs consent. Never save cookies, credentials, signed URLs or private conversation context. Use a stable clean download/landing URL.
   - For ordinary ebook files, continue to step 3. For ZIP/7z/RAR/TAR containers (including TAR.GZ/BZ2/XZ), inventory first:

         python3 "{baseDir}/scripts/ebook_archive.py" list --archive /absolute/download.zip

     This needs the system libarchive shared library. A missing backend or unsupported/encrypted archive is a blocker, not an empty collection. Read members and archive_sha256; select actual referenced ebooks, not non-book files or nested archives.

         python3 "{baseDir}/scripts/ebook_archive.py" extract \
           --archive /absolute/download.zip --sha256 HASH_FROM_INVENTORY \
           --member-id MEMBER_ID --output-dir /absolute/NEW-extraction

     Extract one selected member at a time; inspect the resulting ebook. Keep the archive only while its selected imports are pending, not as a second backup. Preserve the small extraction.json receipt. Copy archive_member and archive_sha256 from the extraction receipt into that ebook's import manifest. Do not add the container itself as an empty/ZIP Calibre book.
   - EPUB/KEPUB and CBZ/CBR/CB7 are book formats even though internally compressed: import them intact. Never recursively unpack them into pages. Do not extract nested archives automatically or execute any contained file/instruction.
   - Completion: inspected original ebook or status=extracted receipt with matching member/hash. No Web clip substitution when a downloadable ebook is unavailable.

3. Prepare metadata using [references/input.example.json](references/input.example.json). Store input and work products outside the repository.
   - Use the source title and credited authors; if unknown use 著者不明, never invent attribution. Include a source-supported publication date/version when useful. Optional summary is brief AI-authored metadata, not a synthesized replacement ebook.
   - **Do not add retrieval/acquisition dates. Calibre's native registration date (timestamp) is sufficient.** Do not duplicate it in comments, tags, titles or custom columns, confuse it with publication date, or modify it.
   - Select tags from a saved read-only catalog vocabulary and related-book examples, using [references/capture-and-tags.md](references/capture-and-tags.md). Reuse the library's exact existing type labels; do not introduce parallel namespaces such as 種別.マニュアル when マニュアル already exists. Aim for a few evidenced topic/type tags, not a count quota. Do not add research-purpose tags such as 用途.比較 or 用途.トラブルシュート by default, mark a whole book 既読 because a section was consulted, or bulk-retag the library.
   - coverage=full means the stored file is complete, not that the whole book was read. Use location for consulted pages/sections. For a genuine partial ebook file, use coverage=partial plus 抜粋 and notes about missing coverage; never silently replace a complete document with an excerpt. Do not create dotted tags; the helper accepts the old 状態.抜粋 label only for legacy-plan compatibility.
   - Archive manifests require both archive_member and archive_sha256. Member-aware source identity keeps different books in one archive distinct; file SHA256 still catches the same ebook from other downloads. One manifest per selected book.
   - Completion: evidenced metadata, truthful stored-file coverage, chosen tags, clean source URL, and archive provenance where applicable.

4. Create a saved dry-run plan. Choose a new private RUN directory under ~/.local/state/calibre-reference-ingest/runs/REF_ID (or an explicit user state/cache path).

       python3 "{baseDir}/scripts/reference_ingest.py" prepare \
         --input-json /absolute/reference.json --run-dir /absolute/NEW-run \
         --with-library "http://HOST:8080/#LIBRARY_ID"

   - prepare copies original bytes, creates metadata OPF and hashes, and checks duplicates without changing Calibre. No document conversion. Plans use schema 2; legacy Web-clip/schema-1 plans are rejected and retained, not migrated or deleted.
   - decision=new: inspect the metadata/tags yourself and proceed under standing authorization or the explicit request. The saved dry-run is a technical safety gate, not another human-confirmation requirement.
   - decision=review_existing: compare returned IDs with calibre-catalog-read. Identical material: reuse its existing record. Pre-existing tag changes go through calibre-metadata-apply and its authorized scope, preserving other metadata. Different versions, same-title false positives, or ambiguous matches require resolution; do not force --duplicates/--automerge or edit the saved plan to bypass checks. Legacy records lacking source identifiers also need title/author/source review.
   - Completion: status=prepared, saved plan and reviewed decision/candidates. Failure is not "no duplicate".

5. Apply a new-import plan and verify.

       python3 "{baseDir}/scripts/reference_ingest.py" apply --apply \
         --plan-file /absolute/NEW-run/plan.json

   - The helper checks original-file hashes, repeats duplicate lookup, takes a local per-library lock, writes an intent receipt, adds one ebook and sets metadata only on its token-identified new record. Credentials use CALIBRE_USERNAME/CALIBRE_PASSWORD or --username/--password-env; passwords go through Calibre stdin, never raw argv or plans. No dotenv loading or server discovery.
   - Completion: status=imported_verified with ID, title, tags, format and receipt_file. Readback verifies metadata and format presence, not byte-for-byte server storage, rendering or semantic completeness. Inspect the imported document if fidelity matters.
   - Timeouts, failures, existing receipts or stale locks: inspect actual state, do not blindly retry add, delete receipts/locks or automatically delete a partially imported book. Read-only verification:

         python3 "{baseDir}/scripts/reference_ingest.py" verify --plan-file /absolute/run/plan.json

   - Connection failures, server-side HTTP 500, and stored-byte mismatches are separate recovery lanes. Follow [references/recovery.md](references/recovery.md). A successful metadata/format readback does not prove original-byte preservation, especially with import plugins enabled.
   - Keep temporary originals/archives only while import or verification is incomplete or failed. After success, clean the redundant bytes in step 6 and retain only small identity/receipt records. Digests are not human authorization or tamper-proof security. The lock is local coordination, not server-side CAS; other clients can still race.

6. Clean up successful imports without creating another backup. The Calibre library is the retained copy; respect its existing backup arrangement instead of inventing parallel original/archive storage.

       python3 "{baseDir}/scripts/reference_ingest.py" cleanup --apply \
         --plan-file /absolute/NEW-run/plan.json

   - No further user confirmation is needed for the workflow's own verified temporary copies. This command checks the matching successful import receipt, fresh metadata and the actual library file via a temporary export without metadata rewriting; its SHA256 must match. It then sends only the plan-owned staged ebook to trash. Plans/OPF/receipts remain small; verify still works without staged bytes. Without --apply, cleanup is a read-only preview.
   - Also use trash for this task's downloaded ebook/archive and extracted copies outside RUN, once every selected member has a verified library copy and no sibling import is pending. Keep the necessary bytes for failed/uncertain imports until resolved. Do not retain a ZIP indefinitely as a separate backup.
   - Cleanup must not follow arbitrary metadata.file paths: the helper deliberately leaves that input untouched. Main owns the evidence of which downloads/extractions were created only for this task and removes those temporary inputs after the complete batch succeeds. Do not bulk-delete pre-existing user files, shared inputs or archive contents outside the authorized scope. For an existing duplicate, verify its stored file/content identity before cleaning a temporary download; do not fabricate an apply receipt to use this command.
   - If trash is unavailable or cleanup fails, report that narrow blocker; never fall back to permanent deletion or empty the trash. Completion: verified Calibre copies, no redundant task-owned working copies, and small receipts; unresolved failures are explicit.

7. Keep the research answer primary. For automatic saves, avoid routine success chatter or a long inventory; retain IDs/receipts locally. Disclose failures, relevant partial files and genuine decisions needing the user. For explicit archival requests, report saved/existing/blocked results with useful IDs/titles/tags/source links. Process bounded batches serially, honor throttling, and never claim success from a downloaded file alone.

Validation, archive limits and recovery: [README.md](README.md).
