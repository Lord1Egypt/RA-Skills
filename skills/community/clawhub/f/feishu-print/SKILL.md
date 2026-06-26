---
name: feishu-print
description: 'Print files uploaded to a Feishu group chat. Supports smart matching: multiple files, filename prefix/keyword filter, file type (pdf/image), and time range ("just now" = "last 5 minutes"). Trigger when the user says things like "print the file from Feishu", "print the PDF I just sent to Feishu", "print the Feishu file", etc.'
user-invocable: true
---

# Feishu Print Skill

**Strict rules:**
- **Do not** use write/edit tools to create or modify any files
- **Do not** create Python scripts, test scripts, or any auxiliary files
- **Only** run existing shell scripts or `lp` commands via exec

---

## Print Files from Feishu

### Smart Matching: Interpret Intent → Set Variables → Call Script

The agent interprets the user's natural language, determines intent, sets the corresponding environment variables, then calls the script.

| User says | Environment variables |
|-----------|----------------------|
| "Print the latest file" / "Print this file" | (default, no variables needed) |
| "Print the last two files" / "Print these two files" | `LIMIT=2` |
| "Print files starting with report" | `NAME_PREFIX=report` |
| "Print files with contract in the name" | `NAME_CONTAINS=contract` |
| "Print the PDF I just uploaded" / "Print the PDF from just now" | `MINUTES=5 FILE_TYPE=pdf` |
| "Print the last three files" | `LIMIT=3 MINUTES=10` |

**FILE_TYPE values**: `pdf` / `image` / `video` / `doc` / `file` (default — matches all)

### Invocation

```bash
# Default: print latest file
PRINTER=MyPrinter <SKILL_DIR>/feishu_fetch_and_print.sh

# Print the latest 2 files
PRINTER=MyPrinter LIMIT=2 <SKILL_DIR>/feishu_fetch_and_print.sh

# Print files whose name starts with "report"
PRINTER=MyPrinter NAME_PREFIX=report <SKILL_DIR>/feishu_fetch_and_print.sh

# Print PDFs uploaded in the last 5 minutes
PRINTER=MyPrinter MINUTES=5 FILE_TYPE=pdf <SKILL_DIR>/feishu_fetch_and_print.sh
```

Script prints `Sent to printer: <filename>` for each file on success.

---

## Print Text Content Directly

```bash
echo "content to print" | lp -d <PrinterName>
```

Multi-line content:
```bash
cat > /tmp/openclaw_print.txt << 'EOF'
content
EOF
lp -d <PrinterName> /tmp/openclaw_print.txt
```

---

## List Available Printers

```bash
lpstat -a
```

## Check Print Queue

```bash
lpq -P <PrinterName>
```

## Cancel Print Jobs

```bash
cancel -a <PrinterName>
```
