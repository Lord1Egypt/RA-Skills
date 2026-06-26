# Quick Start Guide 🚀

## Single Document Learning (Basic)

### Step 1: Start Learning

```
Please learn this document for me: [filename]
```

Example:
```
Please learn the driver manual from /workspace/linuxdriver/itop-3568-driver-v2.8.pdf
```

**What happens:**
- Document is loaded and read
- Key concepts are extracted
- Progress tracking begins
- Initial summary saved to memory

### Step 2: Continue Learning

After reading some content, you can pause. When ready to continue:

```
Resume learning [document name] from last position
```

Example:
```
Resume learning the driver manual from last position
```

**What happens:**
- Last saved position is loaded (chapter/page)
- Reading continues from there
- Progress automatically updated

### Step 3: Query Your Knowledge

After learning, ask questions about what you've learned:

```
What did I learn about [topic]?
Show me notes on [concept]
```

Example:
```
What did I learn about the pinout configuration?
Summarize my driver manual learning so far
```

**What happens:**
- Memory search retrieves relevant content
- Answers based on previously learned material

---

## Multi-Document Learning (Advanced) 📚🔄

### Scenario: Learn PDF-A → Pause → Learn PDF-B → Resume PDF-A

#### Day 1: Start with Document A
```
User: Please learn this driver manual for me.
Assistant: ✅ Started tracking itop-3568-driver.pdf
   Progress: Page 0/450 (not started)

[After reading first section]
User: Pause here, let's learn another document today
Assistant: ✅ Saved progress for PDF-A at page 120/450
   Now starting PDF-B...

User: Please also learn this user guide
Assistant: ✅ Started tracking user-guide.pdf
   Progress: Page 0/80 (not started)

[Read some of PDF-B]
User: Pause, let's go back to the driver manual tomorrow
```

#### Day 2: Switch between documents
```
User: Let's continue with the user guide today
Assistant: Loading progress for user-guide.pdf...
   Last read: Page 35/80
   Continuing from where we left off...

[After reading PDF-B]
User: Now let's resume the driver manual
Assistant: Switching context to itop-3568-driver.pdf...
   Last read: Page 120/450 (from Day 1)
   Resuming from page 121...

[After reading more of PDF-A]
User: What's my progress on all documents?
Assistant: 📚 Document Learning Status
   ==================================
   
   ✅ itop-3568-driver.pdf
      Progress: 200/450 pages (44%)
      Last updated: Today
   
   🔄 user-guide.pdf
      Progress: 50/80 pages (63%)
      Last updated: Earlier today

Day 3: Query specific document knowledge
User: What did I learn about driver installation in the manual?
Assistant: [Searches memory and provides answer from PDF-A only]
Based on my notes from itop-3568-driver.pdf...
```

### Key Commands for Multi-Document Learning

| Command | Purpose |
|---------|---------|
| `Please learn this document: [filename]` | Start learning a new document |
| `Pause here, let's learn [another-doc]` | Pause current, start another |
| `Resume learning [doc-name] from last position` | Switch back to specific doc |
| `What's my progress on all documents?` | Show status of ALL tracked docs |
| `Show me the status of everything I'm learning` | Alternative status command |

### Benefits of Multi-Document Learning

1. **✅ No interference**: Each document has independent progress tracking
2. **✅ Seamless switching**: System automatically loads correct position for each doc
3. **✅ Complete history**: All learning sessions preserved and searchable
4. **✅ Flexible workflow**: Learn at your own pace across multiple sources

---

## Tips for Best Results

### For Single Document Learning
- ✅ Be specific: Always mention document name when resuming or querying
- ✅ Regular updates: Add progress notes after each session
- ✅ Use summaries: Ask for summaries to reinforce learning

### For Multi-Document Learning
- ✅ Clear naming: Give documents memorable names if they're long filenames
- ✅ Status checks: Periodically check `What's my progress on all documents?`
- ✅ Context switching: Be explicit when switching between docs
- ✅ Review separately: Query each document independently for focused answers

---

## Troubleshooting

### "Progress not found" error
- The document hasn't been started yet, or progress file was deleted
- Just say "Start learning [document]" again

### Can't read PDF
- Ensure it's a text-based PDF (not scanned images)
- Try converting to text first if needed

### Want to reset progress for one document
- Just say: `Reset progress on [doc-name] and start fresh`

---

**Ready?** Just tell me which document you want to learn! 🚀📚

## Common Scenarios

### Scenario 1: Learning a Book Chapter by Chapter

```
Day 1:
User: Please learn this book. Start with Chapter 1.
Assistant: [Reads and summarizes Chapter 1]
Progress: 1/24 chapters saved!

Day 2:
User: Continue from last position
Assistant: Resuming at Chapter 2...

Day 3:
User: What did I learn in the first two chapters?
Assistant: [Searches memory and provides summary]
```

### Scenario 2: Learning a Technical Manual (PDF)

```
User: Please read this PDF for me. It's long, so track my progress.
Assistant: [Reads entire document or up to limit]
Progress tracking enabled! You can ask "Resume learning the manual" anytime.

Later: Resume learning the manual from page 50
Assistant: Continuing from page 50...
```

### Scenario 3: Reference Learning (Look-up Later)

```
User: I need to learn this specification for future reference. Please create a searchable knowledge base.
Assistant: [Reads and creates structured notes]
Knowledge base ready! You can later ask specific questions about the content.

Later: What are the API rate limits in this spec?
Assistant: [Searches memory and provides exact answer from learned content]
```

## Tips for Best Results

1. **Be Specific**: Always mention document name when resuming or querying
2. **Regular Updates**: Add progress notes after each session
3. **Use Summaries**: Ask for summaries to reinforce learning
4. **Review Often**: Use memory search to find what you've learned before

## Troubleshooting

### "Progress not found" error
- The document hasn't been started yet, or progress file was deleted
- Just say "Start learning [document]" again

### Can't read PDF
- Ensure it's a text-based PDF (not scanned images)
- Try converting to text first if needed

### Want to reset progress
- Delete the `.document_learning_progress.json` file in the document's directory
- Start fresh with new learning session

---

**Ready?** Just tell me which document you want to learn! 🚀
