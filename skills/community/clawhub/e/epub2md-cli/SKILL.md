---
name: epub2md-cli
description: Use the local `epub2md` CLI to inspect EPUB files and convert them into Markdown. Make sure to use this whenever the user mentions `.epub` files, EPUB 转 Markdown、电子书章节导出、合并章节为单个 Markdown、下载或本地化 EPUB 中的远程图片、查看书籍信息/目录/章节结构、或解压 EPUB 内容，即使用户没有明确说出 `epub2md`。
---

# epub2md CLI

Use this skill to operate on local EPUB files with `epub2md` instead of hand-rolling parsing logic.

## Bundled script

For any conversion that writes files, use the bundled wrapper script:

`/home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py`

The wrapper exists to enforce a stable workspace layout and avoid `epub2md 1.6.2` merge-path quirks.

One more `epub2md 1.6.2` quirk: source filenames containing glob metacharacters such as `[` `]` `?` or `*` can still be treated as patterns by `epub2md`, even when the shell path was quoted correctly. When that happens, keep the original EPUB in `inputs/`, but stage a temporary safe basename such as `book.epub` before calling raw `epub2md`, then copy the generated `book/` directory into the expected workspace output folder.

## What `epub2md` is good at

- Inspecting book metadata with `--info`
- Inspecting table of contents and nesting with `--structure`
- Listing sections/chapters with `--sections`
- Converting an EPUB into chapter-by-chapter Markdown files
- Merging an EPUB into one Markdown file, preferably with an explicit output name
- Merging an existing Markdown directory with plain `--merge`
- Downloading remote images referenced by the EPUB with `--localize`
- Unzipping EPUB contents for inspection with `--unzip`
- Batch conversion with quoted glob patterns like `"books/*.epub"`

## Prerequisites

Check the command first:

```bash
command -v epub2md
```

If it is missing and the environment allows installs, install it with npm:

```bash
npm install -g epub2md
```

If `--localize` is needed, make sure Node.js is at least `18.0.0`.

## Workspace layout

By default, write conversion jobs to:

`/home/admin1/.agents/skills/epub2md-cli-workspace/{bookname}`

Within that directory:

- `inputs/` contains the original EPUB file
- `outputs/` contains conversion results
- `outputs/split/` contains chapter-by-chapter Markdown output
- `outputs/merge/` contains merged Markdown output and related assets
- `outputs/inspect/` contains saved inspection results when the user explicitly asks for inspection output

Do not write conversion output next to the user's source EPUB unless they explicitly ask for a different layout.

## Working style

1. Start from the user's real goal, not from the default conversion.
   - If they only want metadata or structure, do not convert the book.
   - Inspection is opt-in only. Do not run it unless the user explicitly asked to inspect the EPUB.
   - If they want one final Markdown file from an EPUB, use merge mode.
   - If they want chapter files, use split mode.

2. Confirm the source path before running commands.
   - Prefer exact paths the user already gave you.
   - If they referred to "that epub in this folder", discover it with shell tools such as `rg --files -g '*.epub'`.
   - Quote paths and glob patterns when they contain spaces or wildcard characters.
   - Quoting is necessary but not sufficient when the EPUB basename itself contains `[` `]` `?` or `*`; `epub2md` may still interpret the basename as a glob internally.

3. If the user asked for conversion but did not specify the output shape, ask one short clarifying question before writing files.
   - Ask whether they want `多个文件`、`只要 merge 文件`、or `都转换`.
   - Do not guess between split and merge when the user clearly cares about the output form.

4. Use the wrapper script for any file-writing conversion task.
   - Do not call `epub2md` directly for split/merge/both output jobs unless the user explicitly asked for raw CLI invocation.
   - The wrapper copies the original EPUB into `inputs/` and writes results into `outputs/`.
   - The wrapper always uses a safe merge invocation and should not produce a stray `home/` directory.
   - If conversion still fails with `No files found matching pattern:` or a wrapper `FileNotFoundError` caused by a glob-like source basename, fall back to safe-basename staging: copy the EPUB into a temp directory as `book.epub`, run raw `epub2md` there, then copy the generated `book/` directory back into `outputs/merge/` or `outputs/split/`.

5. After the command finishes, report concrete outputs.
   - Say which command you ran.
   - Say where the generated files were written.
   - Mention any limitations, such as remote images not being localized unless `--localize` was used.

6. Treat `--sections` as an inspection tool, not a default user-facing output.
   - In `epub2md 1.6.2`, `--sections` prints very large objects with raw HTML.
   - Use it when you need deep inspection.
   - Summarize the findings for the user unless they explicitly asked for the raw dump.

## Command selection

### Inspect only

```bash
epub2md --info "/path/to/book.epub"
epub2md --structure "/path/to/book.epub"
epub2md --sections "/path/to/book.epub"
epub2md --unzip "/path/to/book.epub"

python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode inspect

python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode inspect \
  --inspect-actions info structure sections
```

Use these only when the user explicitly wants to understand the book before deciding how to export it.

### Convert into chapter Markdown files

```bash
python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode split

python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode split \
  --autocorrect
```

Use `--autocorrect` when the user explicitly wants spacing or punctuation cleanup in the Markdown output.

### Merge into one Markdown file

```bash
python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode merge

python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode merge \
  --merge-name custom-name.md
```

Use the custom merged filename form when the user asks for a specific final filename.

### Convert both split and merge outputs

```bash
python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode both
```

### Localize remote images

```bash
python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode split \
  --localize

python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode merge \
  --merge-name custom-name.md \
  --localize
```

Use this only when the user wants remote images downloaded into the output folder. Mention the Node.js `>=18` requirement if needed.

### Batch conversion

```bash
epub2md "books/*.epub"
epub2md --merge "books/*.epub"
```

Keep the glob quoted so `epub2md` receives the pattern directly.

This is a raw CLI fallback for explicit bulk-processing requests. It does not use the per-book workspace layout above. Prefer the bundled wrapper for normal single-book conversion jobs.

### Fallback for glob-like EPUB filenames

Use this only when the source basename itself contains `[` `]` `?` or `*` and the normal wrapper flow fails.

```bash
src="/path/to/Book [Annotated].epub"
book_name="Book [Annotated]"
book_dir="/home/admin1/.agents/skills/epub2md-cli-workspace/$book_name"
merge_dir="$book_dir/outputs/merge"
merge_name="$book_name-merged.md"

mkdir -p "$book_dir/inputs" "$merge_dir"
cp "$src" "$book_dir/inputs/"

tmpdir=$(mktemp -d "$book_dir/.manual-merge-XXXXXX")
cp "$src" "$tmpdir/book.epub"
cd "$tmpdir"
epub2md --merge="$merge_name" "book.epub"
cp -a "$tmpdir/book/." "$merge_dir/"
```

This preserves the normal workspace layout while avoiding `epub2md`'s internal glob matching on the original basename.

## Expected outputs

Use these expectations when explaining results:

- The original EPUB is copied to `.../{bookname}/inputs/{bookname}.epub`
- Split output is written under `.../{bookname}/outputs/split/`
- Merge output is written under `.../{bookname}/outputs/merge/`
- Inspection output is written under `.../{bookname}/outputs/inspect/` only when the user asked for inspection
- Chapter Markdown files are typically written as numbered Markdown files
- Many chapter files are named like `NNN-title.md`, but fallback names such as `NNN-partXXXX.md` can also appear
- Images are stored under an `images/` subdirectory inside the relevant output folder
- Merge mode defaults to `{bookname}-merged.md` unless the user asked for another filename

Do not claim remote images were downloaded unless `--localize` was part of the command.

## Known quirks

These were validated against `epub2md 1.6.2`:

- `--sections` is often too verbose to show directly because it includes raw HTML payloads
- Plain `--merge` on an absolute EPUB path can generate an awkward nested path and keep the `.epub` extension on the merged Markdown file
- The bundled wrapper avoids that behavior by never relying on plain `--merge` for EPUB merge jobs
- EPUB basenames containing `[` `]` `?` or `*` can be interpreted as glob patterns by `epub2md` itself, even when shell quoting is correct
- The common symptom is `No files found matching pattern:` from `epub2md`, or a wrapper `FileNotFoundError` because `epub2md` created `book/` while the wrapper expected a directory named after the original book
- The practical workaround is to stage the source EPUB to a safe basename such as `book.epub`, run `epub2md` from that temp directory, then copy the generated `book/` contents back into the expected workspace output directory

## Response format

Keep the response practical and concrete:

1. State the action you took
2. Show the exact `epub2md` command you ran
3. List the output path or paths created
4. Mention blockers or caveats, if any

## Examples

**Example 1: convert to chapter files**

User intent: "把 `~/Books/foo.epub` 转成多个 markdown 章节。"

Good command:

```bash
python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "$HOME/Books/foo.epub" \
  --mode split
```

**Example 2: merge and localize**

User intent: "把 `~/Books/foo.epub` 合成一个 markdown，并把远程图片下载到本地。"

Good command:

```bash
python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "$HOME/Books/foo.epub" \
  --mode merge \
  --merge-name foo.md \
  --localize
```

**Example 3: user did not specify split or merge**

User intent: "把这个 epub 转成 markdown。"

Good response:

```text
要哪种输出：多个章节文件、只要一个 merge 文件，还是两种都要？
```

**Example 4: inspect only**

User intent: "先帮我看看这本书的目录结构，不要导出正文。"

Good command:

```bash
python3 /home/admin1/.agents/skills/epub2md-cli/scripts/run_epub2md.py \
  --input "/path/to/book.epub" \
  --mode inspect
```
