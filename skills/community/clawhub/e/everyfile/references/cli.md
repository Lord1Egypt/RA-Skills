# everyfile — CLI Reference

Shell command for instant file search via Voidtools Everything.
Aliases: `everyfile`, `every`, `ev`. Use `ev` for brevity.

## Install

```powershell
pip install everyfile
```

## Search Syntax (passed verbatim to Everything)

### Operators & Wildcards
```
space   AND       |   OR        !   NOT      < >   grouping     " "  exact phrase
*   zero or more chars (matches whole filename by default)
?   one char
```

### Modifiers — prefix any term or function
```
Filename matching:
  exact:  wfn:  wholefilename:      match whole filename ← use before regex for exact names
  nowfn:  nowholefilename:          match anywhere in filename
  path:   nopath:                   match full path vs filename only
  wildcards:  nowildcards:          enable/disable wildcard expansion

Files/folders:
  file:  files:                     files only
  folder:  folders:                 folders only

Case / encoding:
  case:  nocase:                    case-sensitive / insensitive
  diacritics:  nodiacritics:        match/ignore accent marks
  ascii:  utf8:  noascii:           fast ASCII case comparisons

Word / regex:
  ww:  wholeword:  noww:  nowholeword:   whole words only
  regex:  noregex:                       enable/disable regex
```

### Functions
```
Extension / type:
  ext:<ext>              ext:py   ext:py;js;ts  (semicolon OR list)
  type:<type>            file type description string

Paths:
  parent:<path>          in path, including subfolders
  infolder:<path>        in path, NO subfolders  (alias: nosubfolders:<path>)
  depth:<n>              folder depth from drive root
  root:                  items with no parent folder (drive roots)
  shell:<name>           known shell folder (Desktop, Downloads, Documents…)
  child:<name>           folders containing a matching child
  childcount:<n>         folders with n total children
  childfilecount:<n>     folders with n files
  childfoldercount:<n>   folders with n subfolders

Size:
  size:<size>            size:>1mb  size:2mb..10mb
  size words: empty  tiny  small  medium  large  huge  gigantic

Dates (all share same value syntax):
  dm:   datemodified:     dc:  datecreated:
  da:   dateaccessed:     dr:  daterun:
  rc:   recentchange:
  Constants: today  yesterday
    <last|past|prev|this|current|next><year|month|week>
    last<n><years|months|weeks|days|hours|minutes|seconds>
    january..december  jan..dec  sunday..saturday  sun..sat  unknown

Attributes:
  attrib:<flags>    A=archive  C=compressed  D=dir  E=encrypted  H=hidden
                    I=not-indexed  L=reparse  N=normal  O=offline  P=sparse
                    R=readonly  S=system  T=temp

Duplicates:
  dupe:          same filename       namepartdupe:  same name (no ext)
  sizedupe:      same size           dmdupe:        same date modified
  dcdupe:        same date created   dadupe:        same date accessed
  attribdupe:    same attributes

Filename text:
  startwith:<text>         filename starts with
  endwith:<text>           filename ends with
  len:<n>                  filename character length

Miscellaneous:
  empty:                   empty folders
  count:<n>                limit results to n
  runcount:<n>             Everything run count
  filelist:<a|b|c>         pipe-delimited filename list
  filelistfilename:<file>  load list from file
  frn:<list>               semicolon-delimited File Reference Numbers
  fsi:<index>              internal file system index

Content search (slow — narrow with other filters first!):
  content:<text>           via iFilter, falls back to UTF-8
  ansicontent:  utf8content:  utf16content:  utf16becontent:

Images (slow): width:<px>  height:<px>  dimensions:<w>x<h>  orientation:landscape|portrait  bitdepth:<n>
ID3/FLAC (slow): title:  artist:  album:  genre:  track:  year:  comment:
```

### Value / range syntax
```
fn:value      fn:=value    fn:>value    fn:>=value    fn:<value    fn:<=value
fn:start..end   (range, inclusive)     fn:start-end  (alternative range)
```

### Built-in macros
```
File groups:    audio:  video:  doc:  pic:  zip:  exe:
Literal chars:  quot:"  apos:'  amp:&  lt:<  gt:>  #<n>:  #x<n>:  (unicode dec/hex)
```

### Key examples
```
exact:env.json                           exact filename (not substring)
ext:py;js;ts                             multiple extensions
ext:py dm:thisweek size:>10kb            AND combination
parent:C:\Dev\myproject                  in folder (+ subfolders)
infolder:C:\Dev\myproject                in folder only, no subfolders
sizedupe: ext:mp4 size:>1gb             large duplicate videos
ext:py content:"TODO"                   content search (slow)
attrib:H                                 hidden files
dm:last7days size:>1mb                   modified last 7 days
startwith:test_ ext:py                   files starting with test_
```

## Output Modes

| Flag | Stdout | When to use |
|------|--------|-------------|
| *(none)* | NDJSON when piped, human table on stderr | Interactive / piping |
| `-l` / `--list` | One full path per line | `ForEach-Object`, subshells |
| `-0` / `--null` | Null-separated paths | Paths with spaces/special chars |
| `-j` / `--json` | Force NDJSON | Structured processing |

## Complex Examples

```powershell
# Large Python files modified this week, biggest first
ev "ext:py size:>50kb dm:thisweek" --sort size -d -n 20

# Duplicate DLLs across all drives (name-only)
ev "dupe: ext:dll" -f name,full_path,size --sort name

# Regex: test files following pytest convention
ev "regex:^test_.*\.py$" --sort modified -d

# Files in a specific subtree (use path: function)
ev "ext:ts path:webapp\src" --sort modified -d -n 50

# Zero-byte placeholder files
ev "size:empty ext:py|ext:js|ext:ts" -f name,full_path

# Recently accessed executables (last 2 weeks)
ev "ext:exe da:last2weeks" --sort accessed -d -n 10 -f name,full_path,date_accessed

# Content search — find Python files containing "async def"
ev 'ext:py content:"async def"' -l

# Count before acting
ev --count "ext:tmp|ext:log dm:>30days"

# Chain filters via pipe composition (local filter, no re-query)
ev ext:py -j | ev "path:src" | ev "!test" | ev "!__pycache__"

# Structured filter on NDJSON stream
ev ext:py -f all -j | ev filter --size-gt 10000 --modified-after 2026-01-01 --is-file

# Extract specific fields
ev ext:py -f all -j | ev pick name size date_modified
```

## Scripting Patterns

```powershell
# Open most recently modified match in VS Code
code $(ev "search.py" --sort modified -d -n 1 -l)

# Batch process: lint all Python files modified today
ev "ext:py dm:today" -l | ForEach-Object { pylint $_ }

# Copy large logs to archive
ev "ext:log size:>10mb" -l | ForEach-Object { Move-Item $_ D:\Archive\ }

# Count lines of code in a project subtree
ev "ext:py path:src" -l | ForEach-Object { Get-Content $_ } | Measure-Object -Line

# Search contents of recently changed files
ev "ext:py dm:thisweek" -l | ForEach-Object { Select-String -Path $_ "TODO|FIXME|HACK" }

# JSON pipeline with jq — top 10 largest by size
ev "ext:py" -f name,size -j | jq -s 'sort_by(-.size) | .[0:10] | .[] | "\(.name) \(.size)"'

# Paginate results
ev ext:py -l | Select-Object -Skip 100 -First 25
```

## Fields & Sorting

```powershell
ev ext:py -f name,size,date_modified    # select fields (display + NDJSON)
ev ext:py -f all                        # every field
ev ext:py -f dates                      # group: date_created, date_modified, date_accessed
ev ext:py -f meta                       # group: size, attributes, is_file, is_folder
ev --help-fields                        # list all available fields
```

Fields: `name` `path` `full_path` `ext` `size` `date_created` `date_modified` `date_accessed` `date_run` `date_recently_changed` `run_count` `attributes` `is_file` `is_folder` `hl_name` `hl_path` `hl_full_path`

Sort: `name` `path` `size` `ext` `created` `modified` `accessed` `run-count` `date-run` `recently-changed` `attributes` — append `-d` for descending.

## Instance Management

```powershell
ev --instances                         # list running instances
ev --instance 1.5a ext:py             # target specific version
$env:EVERYTHING_INSTANCE = "1.5a"     # persist for session
ev --version                          # CLI + Everything version
ev --info                             # service status
```

Priority: `--instance` flag > `$EVERYTHING_INSTANCE` env var > auto-detect (1.5a → 1.5 → 1.4 → default).
