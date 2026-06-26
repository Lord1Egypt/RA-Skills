---
name: document-learning
description: Comprehensive document learning system with progress tracking, resume capability, and long-term memory integration. Use when you need to read PDF/text documents, track your learning progress (chapter/page bookmarks), resume from where you left off in future sessions, and automatically store learned knowledge into MEMORY.md for permanent retention. Supports large file handling and chunked processing.
---

# Document Learning System

A complete system for reading documents, tracking progress across multiple sessions, and building long-term memory.

## Quick Start

**To start learning a document:**
```
Please learn this document: [filename]
```

**To resume from where you left off:**
```
Resume learning [filename] from last position
```

**To check current progress:**
```
What's my progress on learning [filename]?
```

## Core Features

### 1. Large File Support
- Handles PDF files up to hundreds of MBs
- Text-based documents (TXT, MD, LOG, etc.)
- Chunked processing to avoid memory issues
- Automatic encoding detection and recovery

### 2. Progress Tracking & Resume
- **Bookmark system**: Automatically tracks your position (chapter/page)
- **Resume capability**: Pick up exactly where you left off, even days later
- **Progress visualization**: See what's been learned vs remaining
- **Manual control**: Jump to specific chapters/pages if needed

### 3. Long-term Memory Integration
- Extracts key concepts automatically
- Stores learning summaries in `MEMORY.md`
- Creates session notes in `memory/YYYY-MM-DD.md`
- Builds a searchable knowledge base over time

## How It Works

### Session Flow

1. **Start Learning**
   - Upload or specify document path
   - System reads and extracts content
   - Creates initial progress entry

2. **Track Progress**
   - After each session, note where you stopped
   - Progress is saved automatically
   - Key points are extracted to memory files

3. **Resume Later**
   - Say "resume learning [document]"
   - System loads last position
   - Continues from there seamlessly

4. **Build Knowledge Base**
   - Over time, all learned content accumulates in MEMORY.md
   - Use `memory_search` to find specific topics later
   - Create comprehensive summaries periodically

## Multi-Document Learning Support 📚🔄

**You can now learn multiple PDFs simultaneously and switch between them!**

### How It Works

The system maintains a **progress store** that tracks ALL your learning documents:
- ✅ Track progress for Document A, B, C... all at once
- ✅ Learn Document A → Pause → Learn Document B → Pause → Resume Document A
- ✅ Each document remembers its exact position (chapter/page)
- ✅ Switch context seamlessly between different documents

### Multi-Document Workflow Example

```
Day 1: Start learning PDF-A
User: Please learn this driver manual for me.
Assistant: Started tracking itop-3568-driver.pdf
   Progress: Page 0/450 (not started)

[Read some content]
User: Pause here, let's learn another document
Assistant: ✅ Saved progress for PDF-A at page 120/450
   Now learning PDF-B: user-guide.pdf

[Start PDF-B]
User: Please also learn this user guide
Assistant: Started tracking user-guide.pdf
   Progress: Page 0/80 (not started)

[Read some of PDF-B]
User: Pause, back to the driver manual
Assistant: ✅ Saved progress for PDF-B at page 35/80
   Switching context back to PDF-A...
   Resume from page 120/450

Day 2: Continue learning different documents
User: Let's continue with the user guide today
Assistant: Loading progress for user-guide.pdf...
   Last read: Page 35/80 (PDF-B)
   Continuing from where we left off...

[After reading PDF-B]
User: Show me status of all my learning documents
Assistant: 📚 Document Learning Status
   ==================================
   
   ✅ itop-3568-driver.pdf
      Progress: 120/450 pages (27%)
      Last updated: Today
   
   🔄 user-guide.pdf
      Progress: 50/80 pages (63%)
      Last updated: Just now

Day 3: Query specific document knowledge
User: What did I learn about the driver installation in PDF-A?
Assistant: [Searches memory and provides answer from PDF-A]
Based on my notes from itop-3568-driver.pdf...
```

### Commands for Multi-Document Learning

#### Start a new document
```
Please learn this document: /path/to/document.pdf
```

#### Pause current, start another
```
Pause learning [current-doc], let's learn [new-doc]
```

#### Switch back to previous document
```
Resume learning [doc-name] from last position
```

#### Check all documents status
```
What's my progress on all my learning documents?
Show me the status of everything I'm learning
```

### Key Benefits

1. **No interference**: Each document has independent progress tracking
2. **Seamless switching**: System automatically loads correct position for each doc
3. **Complete history**: All learning sessions are preserved and searchable
4. **Flexible workflow**: Learn at your own pace across multiple sources

---

## Usage Patterns

### Pattern 1: Learning a Technical Manual (e.g., PDF)

```
User: Here's a driver manual. Please learn it for me.
Assistant: I'll read the document, extract key points, and save progress. Let me start with Chapter 1...

[After reading first chapter]
Assistant: Progress update: Read chapters 1-2 of 15. Saved to memory. Ready to continue when you are!

[Days later - resume]
User: Resume learning the driver manual
Assistant: Loading last position (chapter 3)... Continuing from where we left off...
```

### Pattern 2: Learning a Book/Text Document

```
User: I want to learn this book. Track my progress chapter by chapter.
Assistant: Got it! I'll read each chapter and save the summary after every session. Progress tracking enabled.

[After Chapter 1]
Assistant: ✅ Chapter 1 complete - Summary saved to memory/YYYY-MM-DD.md
📊 Progress: 1/24 chapters (4%)

[Next day]
User: Continue from last position
Assistant: Resuming at Chapter 2...
```

### Pattern 3: Reference Learning (Look-up as needed)

```
User: I need to learn this specification document for reference.
Assistant: I'll read it and create a searchable knowledge base. You can later ask questions like "What does section 5 say about API limits?"

Later: What are the API rate limits mentioned in the spec?
Assistant: [Searches memory and provides answer from learned content]
```

## Commands & Tools

### Built-in Script

The skill includes `scripts/read_large_document.py` which handles:
- PDF reading with pdfplumber
- Text file encoding detection
- Progress saving/loading
- Key point extraction

### Memory Integration Files

Read these for detailed integration patterns:
- [`references/memory_integration.md`](references/memory_integration.md) - How to integrate with MEMORY.md

## Best Practices

1. **Start small**: Begin with one document at a time
2. **Regular updates**: Add progress notes after each session, even brief ones
3. **Use summaries**: Ask for chapter summaries to reinforce learning
4. **Review periodically**: Use `memory_search` to find what you've learned before
5. **Be specific**: When asking about content, mention the document name

## Limitations & Notes

- PDFs must be text-based (not scanned images) for optimal reading
- Very large PDFs (>200MB) may take longer to process
- Progress tracking works best with structured documents (chapters/sections)
- For scanned PDFs, consider OCR tools first

## Examples

### Example 1: Learning a Driver Manual

```
User: Please learn this driver manual for me. It's in /workspace/linuxdriver/itop-3568-driver-v2.8.pdf
Assistant: I'll start reading the document now...

[Reads and extracts]
✅ Document loaded: itop-3568-driver-v2.8.pdf (120MB)
📑 Total pages: 450
🔑 Key concepts extracted: Hardware specs, Pinout details, Driver installation...

Progress saved! You can resume anytime with "Resume learning the driver manual"
```

### Example 2: Resume After Days

```
User: Resume learning the driver manual from last position
Assistant: Loading progress... Last read: page 156 of 450 (Chapter 7)
Continuing from where we left off...

[Reads next section]
✅ Chapter 7 complete - Progress updated to page 234/450
```

### Example 3: Query Learned Content

```
User: What did I learn about the pinout configuration?
Assistant: [Searches memory and provides answer from driver manual learning session]
Based on my notes from the itop-3568 driver manual (learned on April 6):
- GPIO pins are numbered X, Y, Z...
- Power supply requirements: 5V at 2A...
```

---

**Ready to start learning?** Just tell me which document you want to learn! 📚
