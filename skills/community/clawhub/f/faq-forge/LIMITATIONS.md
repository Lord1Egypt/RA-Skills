# Limitations & Known Issues

**FAQ Forge** is designed to be simple, reliable, and dependency-free. This document outlines known limitations and design constraints.

---

## By Design (Not Bugs)

### 1. Command-Line Interface Only

**Limitation:** No graphical interface or web dashboard.

**Why:** Keeps the tool simple, fast, and portable. No web server required.

**Workaround:** 
- Use your favorite text editor to edit `faq_data.json` directly
- Build a simple web UI on top if needed (JSON is easy to integrate)
- Command-line is scriptable and automation-friendly

### 2. Single JSON Database File

**Limitation:** All FAQs stored in one JSON file (`faq_data.json`).

**Why:** Simple, portable, version-control friendly, no database server needed.

**Implications:**
- Not ideal for >10,000 entries (but who has 10,000 FAQs?)
- All data loaded into memory (fast, but uses RAM)
- Concurrent writes from multiple processes may conflict

**Workaround:**
- For most businesses, 50-500 FAQs is typical—works perfectly
- Use file locking for concurrent access if needed
- Export/import for migration or splitting large databases

### 3. No Built-in Version Control

**Limitation:** Changes overwrite previous versions. No built-in history tracking.

**Why:** Keeps the tool simple and the JSON file clean.

**Workaround:**
- Store `faq_data.json` in Git for automatic version history
- Export to JSON periodically for backups
- Track the `updated` timestamp to see when answers changed

### 4. Static HTML Output Only

**Limitation:** Published HTML is static. No dynamic search backend.

**Why:** Simplicity and portability. Host anywhere, no server required.

**Implications:**
- Search runs client-side in JavaScript (works fine for <1000 entries)
- No server-side analytics tracking (unless you add Google Analytics)
- No real-time updates (need to republish)

**Workaround:**
- Client-side search is fast for typical FAQ sizes
- Add Google Analytics to published HTML for tracking
- Re-publish when content changes (takes seconds)

### 5. Manual Publishing Required

**Limitation:** After updating FAQs, you must run `faq_publish.py` again.

**Why:** Separation of content management and publishing.

**Workaround:**
- Automate with a simple script: `python faq_forge.py add ... && python faq_publish.py html faq.html`
- Set up a cron job or webhook to auto-publish on changes
- Use file watching tools (like `watchdog`) to auto-regenerate HTML

---

## Technical Constraints

### 6. Python 3.6+ Required

**Limitation:** Requires Python 3.6 or newer.

**Why:** Uses f-strings and modern type hints.

**Workaround:**
- Python 3.6 is from 2016—widely available
- If stuck on older Python, minor code changes can backport

### 7. No Fuzzy Search

**Limitation:** Search is exact substring matching, not fuzzy/typo-tolerant.

**Why:** Python stdlib doesn't include fuzzy search. Keeping it dependency-free.

**Workaround:**
- Use clear, descriptive questions
- Add multiple tags to improve searchability
- HTML client-side search works well for exact matches

### 8. No Natural Language Understanding

**Limitation:** Can't automatically categorize or understand question intent.

**Why:** No AI/ML libraries (staying dependency-free).

**Workaround:**
- Auto-tagging uses keyword matching (works well)
- Templates provide good starting structure
- Manual categorization is fast and accurate

---

## Import Limitations

### 9. Markdown Import Heuristics

**Limitation:** Markdown import uses pattern matching, not semantic understanding.

**Why:** No natural language processing (NLP) libraries.

**Implications:**
- May miss unusually formatted Q&A pairs
- May incorrectly parse section headings as questions
- Needs manual review after import

**Workaround:**
- Review imported questions: `faq_forge.py list`
- Delete incorrect imports: `faq_forge.py delete ID`
- Format your source markdown consistently for best results

### 10. No Automatic Merging

**Limitation:** Importing can create duplicate questions if similar ones exist.

**Why:** No sophisticated duplicate detection.

**Workaround:**
- Review imports before applying: Use `--category` to organize
- Search existing questions first: `faq_forge.py search "keyword"`
- Manually merge duplicates after import

---

## Publishing Limitations

### 11. Basic HTML Theme

**Limitation:** Single professional theme. No theme marketplace.

**Why:** Keeping it simple and focused.

**Workaround:**
- Edit `faq_publish.py` to customize the HTML template
- The HTML/CSS is clean and well-commented
- Change colors via `theme_color` in config
- Or export to Markdown and use your own static site generator

### 12. No PDF Export

**Limitation:** Can't directly export to PDF.

**Why:** Python stdlib doesn't include PDF generation.

**Workaround:**
- Export to HTML, then print to PDF from browser
- Export to Markdown, then use Pandoc or similar tool
- Use plain text output and convert with external tools

### 13. Limited Markdown Tables in HTML

**Limitation:** Markdown inside answers isn't rendered in HTML.

**Why:** No markdown parser (staying dependency-free).

**Workaround:**
- Use plain HTML in answers (supported)
- Keep formatting simple
- Use line breaks and basic text formatting

---

## Multi-User / Team Limitations

### 14. No User Permissions

**Limitation:** No built-in user authentication or role-based access.

**Why:** Command-line tool, not a web application.

**Workaround:**
- Use file system permissions to control access
- Store FAQ database in a shared Git repo for team collaboration
- Build a simple web wrapper if multi-user editing is critical

### 15. No Conflict Resolution

**Limitation:** Concurrent edits may conflict if multiple users edit simultaneously.

**Why:** Simple file-based storage.

**Workaround:**
- Use Git for collaboration (automatic conflict resolution)
- Coordinate who edits when (small teams)
- Export/import for merging changes from different sources

---

## Scaling Limitations

### 16. Not Optimized for Huge FAQs

**Limitation:** Performance degrades with >5,000 entries.

**Why:** In-memory JSON loading, linear search.

**Reality:** Most businesses have 50-500 FAQs. If you have 5,000, you need a knowledge base platform, not a FAQ.

**Workaround:**
- Split into multiple products/databases
- Archive old or irrelevant questions
- Use multi-product feature to organize large sets

### 17. Client-Side Search Limits

**Limitation:** HTML search loads entire FAQ in browser. Slow for very large FAQs.

**Why:** Static site, no backend.

**Reality:** Works fine up to ~1,000 entries. Beyond that, use Markdown + static site generator.

**Workaround:**
- Split large FAQs by product or category
- Publish separate HTML pages per category
- Use Markdown export + static site generator for very large FAQs

---

## Analytics Limitations

### 18. View Counts Are Local

**Limitation:** View counts track database access, not actual customer views.

**Why:** Static HTML can't report back to database.

**Workaround:**
- Add Google Analytics to published HTML
- Use server logs if hosting on your own server
- View counts show which questions you look at (useful for maintenance)

### 19. No Built-in A/B Testing

**Limitation:** Can't test different answer variations.

**Why:** Out of scope for a simple FAQ tool.

**Workaround:**
- Use external A/B testing tools on your website
- Track metrics via Google Analytics
- Manually update answers based on support ticket trends

---

## Integration Limitations

### 20. No API

**Limitation:** No REST API for dynamic FAQ delivery.

**Why:** Static tool, not a service.

**Workaround:**
- JSON database is easy to parse from any language
- Build a simple API on top if needed (Flask, FastAPI, etc.)
- Use HTML output with iframe embedding

### 21. No Zapier/Webhook Integration

**Limitation:** Can't automatically create FAQs from support tickets.

**Why:** Command-line tool, not a web service.

**Workaround:**
- Build a simple script to parse support tickets and call `faq_forge.py`
- Use cron + API polling to import from external sources
- Export/import JSON for integration with other systems

---

## What FAQ Forge Does Well

Despite these limitations, FAQ Forge excels at:

✅ **Quick setup** - No dependencies, no complex config  
✅ **Professional output** - Beautiful HTML, clean Markdown  
✅ **Easy maintenance** - Simple commands, clear structure  
✅ **Portability** - Works anywhere Python runs  
✅ **Version control friendly** - JSON format, git-compatible  
✅ **Small to medium businesses** - Perfect for 50-500 FAQs  
✅ **Zero hosting costs** - Static HTML, host anywhere  
✅ **Privacy** - Your data stays local, no cloud service  

---

## When to Use Something Else

Consider a different solution if you need:

- ❌ Multi-user collaboration with permissions (use a wiki or CMS)
- ❌ Dynamic, real-time FAQ delivery (use a knowledge base SaaS)
- ❌ Advanced AI/ML categorization (use dedicated KB platforms)
- ❌ Thousands of articles with complex relationships (use a proper CMS)
- ❌ Multi-language with translation workflows (use localization platforms)
- ❌ Advanced analytics and A/B testing (use enterprise KB software)

---

## Known Bugs (None Currently!)


If you discover a bug:
1. Check if it's a documented limitation above
2. Verify you're using Python 3.6+
3. Check `faq_data.json` for corruption (JSON syntax)
4. Try exporting and reimporting to fix database issues

---

## Future Enhancements (Maybe)

These are NOT currently implemented but could be added:

- Web-based editor
- PDF export
- Advanced search (fuzzy, semantic)
- Multi-language support
- Automatic duplicate detection
- Revision history UI
- Zapier integration
- REST API
- Theme marketplace

FAQ Forge is intentionally **simple and complete**. These features may come in future versions if there's demand, but the current version is production-ready as-is.

---

**Questions about limitations?** Most are by design to keep the tool simple and dependency-free. For 95% of businesses, these trade-offs are worth it for the simplicity gained.

**Need something more complex?** FAQ Forge is MIT licensed—fork it and extend it! Or consider enterprise knowledge base platforms if you need advanced features.

**Bottom line:** FAQ Forge is perfect for small to medium businesses who want a professional FAQ without the complexity and cost of enterprise solutions.
