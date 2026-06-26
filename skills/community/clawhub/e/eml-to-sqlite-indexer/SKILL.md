---
name: EML to SQLite Indexer
description: Indexes EML emails into an SQLite database, providing a web interface for searching, management, Excel export, and file deletion, with IP access control and integrated JSON automated backup/restore.
version: 7.0.1
author: 威廉陳
category: Data Processing & Management
---

# EML to SQLite Indexer Skill (V7.0.0 - Management & Export Edition)

This skill indexes EML email files from a specified directory into an SQLite database and provides a feature-rich web interface for searching and management. It includes automatic deduplication, IP access control, Excel export, and a **JSON-formatted scheduled backup and restore system** configurable via the web interface.

## Features

- **Efficient Indexing**: Uses MD5 fingerprinting for automatic deduplication, ensuring no duplicate emails are imported. Supports processing millions of email records.
- **Key Information Extraction**: Automatically parses and stores email sender, recipient, subject, body content, and sent time.
- **Web Query Interface**: Provides a Flask-based web interface with:
    - **Advanced Search**: Keywords (subject/body, case-insensitive), sender (fuzzy matching), recipient (fuzzy matching), and date range filtering.
    - **Excel Export**: Export search results to an Excel-compatible CSV file, including the **original file path**.
    - **File Deletion**: Delete specific emails from both the database and the **physical disk** (Admin only).
    - **Pagination**: Optimized for large datasets to prevent browser slowdowns.
- **IP Access Control**: Configurable whitelist of allowed IP addresses for web access, enhancing security. By default, only `localhost` and `127.0.0.1` are allowed.
- **Web-Configurable Scheduled Backup**: 
    - **Scheduled Mode**: Configure via the web interface to set the backup frequency (e.g., every X days) and specific hour (0-23) for execution.
    - **JSON Format**: Backups export email data as structured JSON and compress it into a ZIP file, named `eml-indexer_YYYYMMDD.zip`, offering excellent cross-platform compatibility.
    - **Automatic Circular Overwrite**: The system automatically retains a configured number of backups, deleting the oldest one when the limit is exceeded.
    - **Manual Management**: One-click download of JSON backup ZIPs and upload of ZIPs for database restoration via the web interface.
- **Admin-Exclusive Interface**: When accessed from `localhost` or `127.0.0.1`, a "⚙️ System Settings" tab is displayed, providing IP management, backup configuration, and deletion functionalities.

## Installation & Deployment

### 1. Environment Requirements
- Python 3.8+ (latest stable version recommended)
- Recommended OS: Windows, Linux

### 2. Dependency Installation
Ensure your Python environment has the following packages installed:
```bash
pip install -r requirements.txt
# Or install manually:
pip install Flask tqdm
```

### 3. File Structure
```
eml_indexer/
├── app.py              # Web application (Flask) - includes scheduled backup thread
├── indexer.py          # Core EML indexing script
├── requirements.txt    # Python dependencies list
├── SKILL.md            # Skill documentation (English)
├── config.json         # Runtime configuration (allowed IPs, backup frequency, retention)
├── emails.db           # SQLite database file (generated after running indexer.py)
├── backups/            # Directory for JSON backups (automatically created)
└── templates/
    ├── detail.html     # Email detail page template
    └── index.html      # Email search and management main page template
└── references/
    └── SKILL-TW.md     # Traditional Chinese version of the skill documentation
```

## Usage

### 1. Index EML Emails
Run `indexer.py` to import EML files from a specified directory into the database. It automatically skips already indexed emails on subsequent runs.
```bash
python indexer.py <EML_DIRECTORY_PATH> <DATABASE_PATH (default: emails.db)>
```

### 2. Start Web Query Interface (with Scheduled Backup)
Execute `app.py` to start the Flask web server. The background scheduled backup thread will also start automatically.
```bash
python app.py
```
After starting, visit `http://localhost:5000` in your browser.

### 3. Manage System Settings
When accessing the web interface from `localhost` or `127.0.0.1`, click the "⚙️ System Settings" tab. Here you can:
- **IP Management**: Add or remove allowed IP addresses.
- **Backup Settings**: Configure "Backup Interval (Days)", "Backup Time (Hour)", and "Number of Backups to Retain".
- **Manual Backup**: Click "Create and Download Backup (ZIP)" to generate an immediate JSON backup.
- **Manual Restore**: Upload a JSON backup ZIP file to restore the database.

## Version History

- **V7.0.1 (2026-03-30)**:
    - Added **Excel Export** functionality (includes file paths).
    - Added **Physical File Deletion** functionality (Admin only).
    - Updated documentation to include Traditional Chinese version in `references/SKILL-TW.md`.
- **V6.0.0 (2026-03-29)**:
    - Web-configurable scheduled backups (days interval and specific hour).
    - Backup filenames formatted as `eml-indexer_YYYYMMDD.zip`.
    - Integrated scheduled check logic into the background thread.
    - SKILL.md updated to English, with author changed to "威廉陳". Original Traditional Chinese SKILL.md moved to `references/SKILL-TW.md`.

## License

MIT License
