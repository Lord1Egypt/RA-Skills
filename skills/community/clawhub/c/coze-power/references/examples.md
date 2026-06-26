# Coze-Power Examples

Real-world scenarios and Coze bot prompts for using Coze-Power.

---

## 1. Web Research Assistant

**Bot prompt:**
> "Search the web for 2026 AI industry trends and summarize the top 5 results."

**Bot output (via Coze-Power):**
```
1. 2026 AI Industry Top 10 Trends: AI Agents Go Mainstream
   Source: techcrunch.com
   AI agents are entering大规模 deployment in 2026...

2. ...(more results)
```

**Use case for**: Research, news monitoring, competitive analysis

---

## 2. Local File Assistant

**Bot prompt:**
> "Read the recent documents on my desktop and help me organize a work log."

**Coze-Power flow:**
1. `list-dir ~/Desktop` → Scan desktop directory
2. `read-file` → Read documents one by one
3. Coze bot understands content and generates a work log
4. `write-file` → Save the work log back to desktop

---

## 3. System Monitor Bot

**Bot prompt:**
> "Check my system status. If disk usage is over 80%, alert me."

**Coze-Power response:**
```
📊 System Status Report:
- OS: Linux 6.6.1
- CPU: 16 cores
- Disk: 512GB total, 67.3% used (normal)
- No alert needed ✅
```

---

## 4. Notification Reminder

**Bot prompt:**
> "Remind me about the meeting tomorrow at 10 AM."

**Coze-Power flow:**
1. Coze bot parses time and event
2. `notify` → Send notification: "Reminder: Meeting at 10 AM tomorrow"
3. Coze bot replies: "Reminder set ✅"
4. (Optional) `clipboard-write` → Copy meeting details to clipboard

---

## 5. Code Helper

**Bot prompt:**
> "Look at my project structure, find all Python files, and count the total lines of code."

**Coze-Power flow:**
1. `list-dir /home/user/projects` → View project root
2. `run-command find . -name '*.py' -type f` → Find all Python files
3. `run-command wc -l $(find . -name '*.py')` → Count total lines

---

## 6. Automated Backup Pipeline

**Bot prompt:**
> "Back up my work directory every Friday and write a report to the desktop."

**Setup:** Coze bot scheduled task + plugin

**Coze-Power flow:**
1. `list-dir ~/work-dir` → Scan work directory
2. `run-command tar -czf backup.tar.gz ...` → Package backup
3. `write-file` → Generate backup report
4. `notify` → Notify user backup is complete

---

## 7. Creative Writing + Local Save

**Bot prompt:**
> "Write a blog post about digital transformation and save it to my desktop."

**Coze-Power flow:**
1. Coze bot generates the article
2. `write-file ~/Desktop/digital-transformation-blog.md` → Save to desktop
3. `notify` → Notify: "Article saved to desktop 📝"
4. (Optional) `clipboard-write` → Auto-copy content to clipboard

---

## 8. Quick Information Bridge

**Bot prompt:**
> "I just copied some text to my clipboard. Analyze it and tell me what product manual it belongs to."

**Coze-Power flow:**
1. `clipboard-read` → Get clipboard content
2. Coze bot analyzes content, identifies product type
3. Returns the analysis

---

## Prompt Template

Add this to your Coze bot's **Persona & Prompt** to teach it how to use Coze-Power:

```yaml
When you need the following capabilities, use the Coze-Power plugin:
1. Search the internet → webSearch
2. Read local files → readFile
3. Write files → writeFile
4. Browse directories → listDir
5. Execute commands → runCommand
6. Get system info → systemInfo
7. Read clipboard → clipboardRead
8. Write to clipboard → clipboardWrite
9. Send notifications → sendNotification

Guidelines:
- Do NOT call tools by default — wait for the user to ask
- Confirm file paths before reading/writing
- Explain why you're running a command before executing it
- Use the user's language for web searches
```
