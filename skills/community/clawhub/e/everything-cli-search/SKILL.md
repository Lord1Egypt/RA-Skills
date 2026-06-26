# Everything CLI Search Skill

Fast file and folder search on Windows using Everything's command line interface with advanced search features: operators, wildcards, macros, modifiers, and functions.

## Overview

**Everything** is a filename search engine for Windows that provides:
- Small installation file
- Clean and simple user interface
- Quick file indexing
- Quick searching
- Quick startup
- Minimal resource usage
- Small database on disk
- Real-time updating

## Installation

### 1. Install Everything

Download and install Everything from https://www.voidtools.com

### 2. Enable Everything Service

- Open Everything
- Go to **Tools** → **Options** → **General**
- Check **"Run as service"**
- Click **OK**
- Restart Everything

### 3. Verify Installation

Open Command Prompt or PowerShell and run:

```bash
es.exe "test"
```

If you see search results, Everything CLI is ready to use!

## Usage

### Python Script

```bash
python3 everything_search.py "query"
```

### Bash Script

```bash
./es_search.sh "query"
```

### PowerShell Script

```bash
.\es_search.ps1 "query"
```

### Direct es.exe

```bash
es.exe "query"
```

## Command Line Options

### Installation Options

```bash
# Install Everything to specific location
Everything.exe -install "C:\Program Files\Everything"

# Install Everything service
Everything.exe -install-service

# Install Everything client service
Everything.exe -install-client-service

# Uninstall Everything
Everything.exe -uninstall
```

### Search Options

```bash
# Set search text
es.exe -s "search query"
es.exe -search "search query"

# Search in specific path
es.exe -p "C:\Users" "filename"
es.exe -path "C:\Users" "filename"

# Search in parent path (no subfolders)
es.exe -parent "C:\Users" "filename"

# Enable case-sensitive search
es.exe -case "Test"

# Enable regex search
es.exe -regex "test.*"

# Enable whole word matching
es.exe -wholeword "test"

# Enable path matching
es.exe -matchpath "test"

# Open a bookmark
es.exe -bookmark "mybookmark"

# Select a filter
es.exe -filter "audio"

# Load local database
es.exe -local

# Search from URL
es.exe -url "es:search query"
```

### Result Options

```bash
# Sort results
es.exe -sort "size"
es.exe -sort "Date Modified"

# Sort ascending/descending
es.exe -sort-ascending
es.exe -sort-descending

# Show details view
es.exe -details

# Show thumbnails
es.exe -thumbnails

# Set thumbnail size
es.exe -thumbnail-size 256

# Focus specific result
es.exe -select "filename.txt"

# Focus top/bottom result
es.exe -focus-top-result
es.exe -focus-bottom-result

# Focus most run result
es.exe -focus-most-run-result
```

### Database Options

```bash
# Force database rebuild
es.exe -reindex

# Save database to disk
es.exe -update

# Do not save/load database
es.exe -nodb

# Read-only mode
es.exe -read-only

# Set database file
es.exe -db "C:\Everything.db"

# Rescan all folder indexes
es.exe -rescan-all

# Pause/resume monitors
es.exe -monitor-pause
es.exe -monitor-resume
```

### Window Options

```bash
# Show new window
es.exe -newwindow

# Show existing window
es.exe -nonewwindow

# Maximize/minimize
es.exe -maximized
es.exe -minimized

# Fullscreen
es.exe -fullscreen

# Always on top
es.exe -ontop

# Close window
es.exe -close

# Toggle window
es.exe -toggle-window
```

### File List Options

```bash
# Create file list
es.exe -create-file-list "output.efu" "C:\path"

# Include only specific files
es.exe -create-file-list-include-only-files "*.mp3;*.flac"

# Exclude files
es.exe -create-file-list-exclude-files "*.tmp;thumbs.db"

# Exclude folders
es.exe -create-file-list-exclude-folders "temp;cache"

# Open file list
es.exe -f "music.efu"
es.exe -filelist "music.efu"

# Edit file list
es.exe -edit "music.efu"
```

### ETP/FTP Options

```bash
# Connect to ETP server
es.exe -connect "username:password@hostname:port"

# Use drive links
es.exe -connect "hostname" -drive-links

# Use FTP links
es.exe -connect "hostname" -ftp-links
```

### General Options

```bash
# Run as administrator
es.exe -admin

# Show help
es.exe -help
es.exe -h
es.exe -?

# Show debug console
es.exe -console
es.exe -debug

# Enable debug logging
es.exe -debug-log

# Exit Everything
es.exe -exit
es.exe -quit

# Start in background
es.exe -startup

# Start/stop service
es.exe -start-service
es.exe -stop-service

# Set instance name
es.exe -instance "myinstance"

# Set config file
es.exe -config "C:\Everything.ini"
```

## Search Syntax

### Operators

#### AND Operator (space)

```bash
# Search for files containing both "file1" and "file2"
es "file1 file2"

# Search for PDF files containing "report"
es "*.pdf report"
```

#### OR Operator (|)

```bash
# Search for files containing "file1" or "file2"
es "file1|file2"

# Search for PDF or DOCX files
es "*.pdf|*.docx"
```

#### NOT Operator (!)

```bash
# Search for files containing "file1" but not "file2"
es "file1 !file2"

# Search for PDF files not containing "temp"
es "*.pdf !temp"
```

#### Grouping (< >)

```bash
# Search for files containing (file1 or file2) and file3
es "<file1|file2> file3"

# Search for PDF or DOCX files containing "report"
es "<*.pdf|*.docx> report"
```

#### Exact Phrase (" ")

```bash
# Search for exact phrase
es "\"exact phrase\""

# Search for files containing "hello world"
es "\"hello world\""
```

### Wildcards

#### * (Zero or more characters)

```bash
# Match all PDF files
es "*.pdf"

# Match all files starting with "test"
es "test*"

# Match all Python files
es "*.py"
```

#### ? (One character)

```bash
# Match files with single character
es "file?.txt"

# Match files with pattern
es "test_?.py"
```

### Macros

#### File Type Macros

```bash
# Search audio files
es "audio:"

# Search compressed files
es "zip:"

# Search document files
es "doc:"

# Search executable files
es "exe:"

# Search picture files
es "pic:"

# Search video files
es "video:"
```

#### Special Character Macros

```bash
# Literal double quote
es "quot:test"

# Literal apostrophe
es "apos:test"

# Literal ampersand
es "amp:test"

# Literal less than
es "lt:test"

# Literal greater than
es "gt:test"

# Unicode character (decimal)
es "#65"

# Unicode character (hex)
es "#x41"
```

### Modifiers

#### Case Modifiers

```bash
# Case-sensitive search
es "case:Test"

# Case-insensitive search (default)
es "nocase:test"
```

#### Whole Filename Modifiers

```bash
# Match whole filename
es "wfn:test.txt"

# Match whole word
es "ww:test"

# Match whole word only
es "wholeword:test"
```

#### File/Folder Modifiers

```bash
# Match files only
es "file:test"

# Match folders only
es "folder:test"
```

#### Path Modifiers

```bash
# Match path and filename
es "path:test"

# Match full path
es "matchpath:test"
```

#### Start/End Modifiers

```bash
# Match filenames starting with text
es "startwith:test"

# Match filenames ending with text
es "endwith:.pdf"
```

#### Regex Modifiers

```bash
# Enable regex
es "regex:test.*"

# Disable regex (default)
es "noregex:test"
```

#### Other Modifiers

```bash
# Enable wildcards
es "wildcards:test*"

# Disable wildcards
es "nowildcards:test"

# Enable diacritics
es "diacritics:café"

# Disable diacritics (default)
es "nodiacritics:cafe"
```

## Advanced Search Functions

### Size Search

```bash
# Search files larger than 1MB
es "size:>1mb"

# Search files smaller than 10MB
es "size:<10mb"

# Search files between 10MB and 100MB
es "size:10mb..100mb"

# Search tiny files (0 KB < size <= 10 KB)
es "size:tiny"

# Search huge files (16 MB < size <= 128 MB)
es "size:huge"

# Search gigantic files (size > 128 MB)
es "size:gigantic"

# Search empty files
es "size:empty"
```

### Date Search

```bash
# Search files modified today
es "datemodified:today"

# Search files modified yesterday
es "datemodified:yesterday"

# Search files modified last week
es "datemodified:lastweek"

# Search files modified in 2024
es "datemodified:2024"

# Search files created last month
es "datecreated:lastmonth"

# Search files accessed last 7 days
es "dateaccessed:last7days"

# Search files modified this week
es "datemodified:thisweek"

# Search files modified next month
es "datemodified:nextmonth"
```

### Attribute Search

```bash
# Search hidden files
es "attrib:H"

# Search read-only files
es "attrib:R"

# Search system files
es "attrib:S"

# Search encrypted files
es "attrib:E"

# Search hidden and read-only files
es "attrib:HR"

# Search archive files
es "attrib:A"

# Search compressed files
es "attrib:C"

# Search directories
es "attrib:D"
```

### Content Search

```bash
# Search files containing "hello world"
es "content:\"hello world\""

# Search UTF-8 content
es "content:\"hello\" encoding:utf8"

# Search UTF-16 content
es "content:\"hello\" encoding:utf16"

# Search UTF-16 BE content
es "content:\"hello\" encoding:utf16be"

# Search ANSI content
es "content:\"hello\" encoding:ansi"
```

### Image Search

```bash
# Search images with width 1920
es "width:1920"

# Search images with height 1080
es "height:1080"

# Search landscape images
es "orientation:landscape"

# Search portrait images
es "orientation:portrait"

# Search images with specific dimensions
es "width:1920 height:1080"

# Search images with 24-bit depth
es "bitdepth:24"

# Search images with specific dimensions
es "dimensions:1920x1080"
```

### Media Search

```bash
# Search by album
es "album:\"Album Name\""

# Search by artist
es "artist:\"Artist Name\""

# Search by genre
es "genre:Rock"

# Search by title
es "title:\"Song Title\""

# Search by track number
es "track:5"

# Search by comment
es "comment:\"Comment\""
```

### Other Functions

```bash
# Search duplicate files
es "dupe:"

# Search empty folders
es "empty:"

# Search files by name length
es "len:10"

# Search files by run count
es "runcount:>5"

# Search recently changed files
es "daterecentlychanged:today"
```

## Keyboard Shortcuts

### Search Edit Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + A | Select all text |
| Ctrl + Backspace | Delete previous word |
| Ctrl + Space | Complete search |
| Enter | Focus result list and select highest run count |
| Up/Down Arrow | Focus result list |
| Alt + Up/Down Arrow | Show search history |

### Result List Shortcuts

| Shortcut | Action |
|----------|--------|
| F2 | Rename focused item |
| Delete | Move to recycle bin |
| Shift + Delete | Permanently delete |
| Enter | Open selected items |
| Ctrl + Enter | Open path of selected item |
| Alt + Enter | Display properties |
| Ctrl + C | Copy selected items |
| Ctrl + V | Paste items |
| Ctrl + X | Cut selected items |
| Ctrl + Shift + C | Copy full path |
| Ctrl + A | Select all items |
| Space | Select focus |
| Ctrl + Space | Toggle selection |

### Global Shortcuts

| Shortcut | Action |
|----------|--------|
| Escape / Ctrl + W | Close window |
| F1 | Show help |
| F3 / Ctrl + F / Alt + D | Focus search edit |
| F5 | Reload icons, sizes, dates |
| F11 | Toggle fullscreen |
| Ctrl + N | Open new search window |
| Ctrl + O | Open file list |
| Ctrl + P | Show options |
| Ctrl + Q | Exit Everything |
| Ctrl + S | Export results |
| Ctrl + T | Toggle always on top |
| Ctrl + B | Toggle whole word |
| Ctrl + I | Toggle case |
| Ctrl + M | Toggle diacritics |
| Ctrl + R | Toggle regex |
| Ctrl + U | Toggle path |
| Ctrl + D | Bookmark search |
| Ctrl + 1-9 | Sort by column |
| Alt + Home | Go to home search |
| Alt + Left/Right | Back/Forward |

## Complex Query Examples

### Combined Operators

```bash
# Search for PDF files containing "report" or "summary"
es "*.pdf <report|summary>"

# Search for files containing "file1" and "file2" but not "temp"
es "file1 file2 !temp"

# Search for PDF or DOCX files containing "invoice"
es "<*.pdf|*.docx> invoice"
```

### Combined Functions

```bash
# Search PDF files larger than 1MB modified today
es "*.pdf size:>1mb datemodified:today"

# Search Python files modified last week
es "*.py datemodified:lastweek"

# Search hidden files in Documents
es "attrib:H infolder:\"C:\Documents\""

# Search files containing "error" in content
es "content:\"error\""

# Search images with width >= 1920
es "width:>=1920"

# Search files with name length 10
es "len:10"
```

### Combined Modifiers

```bash
# Case-sensitive whole filename search
es "case:wfn:test.txt"

# Whole word file-only search
es "ww:file:test"

# Start with and end with
es "startwith:test endwith:.pdf"
```

### All Combined

```bash
# Complex query with operators, functions, and modifiers
es "<*.pdf|*.docx> size:>1mb datemodified:lastweek case:wfn:report"

# Search for audio files modified today
es "audio: datemodified:today"

# Search for images with specific dimensions and orientation
es "pic: dimensions:1920x1080 orientation:landscape"

# Search for files containing "error" in content, modified last week
es "content:\"error\" datemodified:lastweek"
```

## Common Use Cases

### Find SKILL.md files in openclaw-skills

```bash
es -p "F:\openclaw-skills" "SKILL.md"
```

### Find all browser-related skills

```bash
es -p "F:\openclaw-skills\skills" -regex ".*browser.*"
```

### Find all Python scripts

```bash
es -p "F:\openclaw-skills" "*.py"
```

### Find files modified today

```bash
es "datemodified:today"
```

### Find large files

```bash
es "size:>100mb"
```

### Find hidden files

```bash
es "attrib:H"
```

### Find files containing specific text

```bash
es "content:\"TODO\""
```

### Find images with specific dimensions

```bash
es "width:1920 height:1080"
```

### Find PDF files larger than 1MB

```bash
es "*.pdf size:>1mb"
```

### Find files modified last week

```bash
es "datemodified:lastweek"
```

### Find duplicate files

```bash
es "dupe:"
```

### Find empty folders

```bash
es "empty:"
```

### Find audio files

```bash
es "audio:"
```

### Find video files

```bash
es "video:"
```

### Find picture files

```bash
es "pic:"
```

## Size Constants

| Constant | Size Range |
|----------|------------|
| `empty` | 0 bytes |
| `tiny` | 0 KB < size <= 10 KB |
| `small` | 10 KB < size <= 100 KB |
| `medium` | 100 KB < size <= 1 MB |
| `large` | 1 MB < size <= 16 MB |
| `huge` | 16 MB < size <= 128 MB |
| `gigantic` | size > 128 MB |
| `unknown` | Unknown size |

## Date Constants

| Constant | Description |
|----------|-------------|
| `today` | Today |
| `yesterday` | Yesterday |
| `tomorrow` | Tomorrow |
| `lastweek` | Last week |
| `thisweek` | This week |
| `nextweek` | Next week |
| `lastmonth` | Last month |
| `thismonth` | This month |
| `nextmonth` | Next month |
| `lastyear` | Last year |
| `thisyear` | This year |
| `nextyear` | Next year |
| `last7days` | Last 7 days |
| `last30days` | Last 30 days |
| `last90days` | Last 90 days |

## Attribute Constants

| Constant | Description |
|----------|-------------|
| `A` | Archive |
| `C` | Compressed |
| `D` | Directory |
| `E` | Encrypted |
| `H` | Hidden |
| `I` | Not content indexed |
| `L` | Reparse point |
| `N` | Normal |
| `O` | Offline |
| `P` | Sparse file |
| `R` | Read only |
| `S` | System |
| `T` | Temporary |
| `V` | Device |

## Indexes

### Database Location

Everything stores the database in:
```
%LOCALAPPDATA%\Everything\Everything.db
```

If "Store settings and data in %APPDATA%\Everything" is disabled, Everything.db is stored in the same location as Everything.exe.

### Indexing Options

To include extra file information in the Everything index:
- In Everything, go to **Tools** → **Options** → **Indexes**
- Check desired options:
  - Index file size
  - Index folder size
  - Index date created
  - Index date modified
  - Index date accessed
  - Index attributes

### Fast Sorting

Enable fast sorting for better performance:
- In Everything, go to **Tools** → **Options** → **Indexes**
- Check desired fast sort options:
  - Fast size sort
  - Fast date created sort
  - Fast date modified sort
  - Fast date accessed sort
  - Fast attribute sort
  - Fast path sort
  - Fast extension sort

### Force Rebuild

To force Everything to rebuild its indexes:
- In Everything, go to **Tools** → **Options** → **Indexes**
- Click **Force Rebuild**
- Click **OK**

Or use command line:
```bash
es.exe -reindex
```

## File Lists

File lists allow you to index CDs, DVDs, BluRays and other offline files and folders.

### Create File List

```bash
# Create file list of a path
es.exe -create-file-list "music.efu" "D:\Music"

# Include only specific files
es.exe -create-file-list "music.efu" "D:\Music" -create-file-list-include-only-files "*.mp3;*.flac"

# Exclude files
es.exe -create-file-list "music.efu" "D:\Music" -create-file-list-exclude-files "*.tmp;thumbs.db"

# Exclude folders
es.exe -create-file-list "music.efu" "D:\Music" -create-file-list-exclude-folders "temp;cache"
```

### Open File List

```bash
# Open file list
es.exe -f "music.efu"
es.exe -filelist "music.efu"

# Edit file list
es.exe -edit "music.efu"
```

## HTTP Server

Everything can start a web server to access your files from your phone or other device.

### Start HTTP Server

- In Everything, go to **Tools** → **Options** → **HTTP Server**
- Check **Enable HTTP server**
- Set port (default: 80)
- Click **OK**

### Access HTTP Server

Open your browser and navigate to:
```
http://localhost:80
```

## ETP Server

Everything ETP/FTP server allows you to search and access your files from an Everything client or FTP client.

### Start ETP Server

- In Everything, go to **Tools** → **Options** → **ETP/FTP**
- Check **Enable ETP/FTP server**
- Set username and password
- Set port (default: 21)
- Click **OK**

### Connect to ETP Server

```bash
# Connect to ETP server
es.exe -connect "username:password@hostname:port"

# Use drive links
es.exe -connect "hostname" -drive-links

# Use FTP links
es.exe -connect "hostname" -ftp-links
```

## Tips

1. **Use quotes for paths with spaces**: `es -p "C:\Program Files" "filename"`
2. **Combine operators**: `es "file1 file2|file3"`
3. **Use wildcards**: `*.txt`, `test_*.py`, `file?.ext`
4. **Sort for better results**: Use `-sort` and `-sort-descending` for large result sets
5. **Use regex for complex patterns**: `es -regex "pattern.*"`
6. **Use functions for advanced filtering**: `size:>1mb datemodified:today`
7. **Combine multiple functions**: `*.pdf size:>1mb datemodified:lastweek`
8. **Use modifiers for precise matching**: `wfn:test.txt`, `ww:test`, `case:Test`
9. **Use macros for quick filtering**: `audio:`, `pic:`, `video:`
10. **Use operators for complex queries**: `file1 file2|file3 !file4`
11. **Enable fast sorting for better performance**: Check fast sort options in Indexes
12. **Use file lists for offline media**: Create EFU files for CDs, DVDs, etc.
13. **Use HTTP server for remote access**: Access files from phone or other devices
14. **Use ETP server for network access**: Share files across computers
15. **Pause monitors when needed**: Use `/monitor_pause` and `/monitor_resume`

## Limitations

- Only works on Windows
- Requires Everything to be installed and running
- Everything service must be enabled for real-time indexing
- Some options require Everything to be running
- Content search requires files to be indexed
- NTFS/ReFS indexing doesn't follow junctions
- Hard link changes only update first entry

## Troubleshooting

### "es.exe not found" Error

If you see this error, Everything is not installed or not in your PATH:

1. Download and install Everything from https://www.voidtools.com
2. Add Everything installation directory to your PATH
3. Restart your terminal

### No Results Found

If you get no results:

1. Make sure Everything service is running
2. Check if the path is correct
3. Try rebuilding the Everything database:
   ```bash
   es.exe -reindex
   ```

### Slow Search Performance

If search is slow:

1. Make sure Everything service is enabled
2. Check if NTFS indexing is enabled
3. Enable fast sorting options
4. Reduce the number of indexed volumes

### ETP Server Won't Start

If ETP server fails to start with "bind failed 10048":

1. Check if another FTP server is running on port 21
2. Change ETP server port to 2121 or another available port
3. Make sure port is not blocked by firewall

## See Also

- [Everything Command Line Options](https://www.voidtools.com/support/everything/command_line_options)
- [Everything Documentation](https://www.voidtools.com/support/everything/)
- [Everything Download](https://www.voidtools.com/)
- [Everything HTTP Server](https://www.voidtools.com/support/everything/http)
- [Everything ETP Server](https://www.voidtools.com/support/everything/etp)
- [Everything Indexes](https://www.voidtools.com/support/everything/indexes)
- [Everything File Lists](https://www.voidtools.com/support/everything/file_lists)

## License

This skill is part of OpenClaw and follows the same license.
