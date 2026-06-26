---
name: cwphil-citation-style
description: "《中國文哲研究集刊》撰稿格式檢查器——中文人文學科論文文獻引用格式化與合規檢查工具。嚴格遵循中央研究院《中國文哲研究集刊》撰稿規範，自動處理中文與外文文獻的腳註、文末參考文獻格式，並支援「同上」「同註」等縮寫規則。只提取用戶提供的真實文獻資料，絕不編造任何書目資訊。Use when the user mentions the journal citation style, requests formatting or checking footnotes/bibliographies for Chinese humanities papers, or needs academic citation compliance verification. Supports: (1) formatting footnotes and end references during paper composition, (2) checking and correcting existing citations, (3) Chinese and Western source handling with proper abbreviations."
---

# CWPHIL Citation Style

## Trigger

This skill activates when the user requests work related to the *Bulletin of the Institute of Chinese Literature and Philosophy* (《中國文哲研究集刊》) citation style, such as:
- "請按照《中國文哲研究集刊》的撰稿格式..."
- "幫我檢查論文引用是否符合集刊格式"
- "格式化我的腳註/參考文獻"
- Any mention of the journal's style requirements

## Workflow

### 1. Understand the Task

Determine whether the user needs:
- **Generation**: Writing new content with proper citations
- **Checking**: Validating and fixing existing citations
- **Both**: A mix of the above

### 2. Load the Style Guide

Read `references/citation-guide.md` for complete formatting rules. Key points to remember:

**Footnotes (腳註)**:
- First citation: Full format with author, title, publication info, page
- Second citation: 同上, with page if different
- Non-consecutive repeat: 同註[number], page
- Chinese titles use 《》for books, 〈〉for articles
- Western titles use italics for books/journals, quotes for articles

**End References (文末參考文獻)**:
- Chinese sources: Author：《Title》。Place：Publisher，Year。
- Western sources: Last Name, First Name. *Title*. Place: Publisher, Year.
- Sort: Chinese by stroke count, Western by alphabet

**Common mistakes**:
- Missing publication info in first citation
- Using 同上 on first citation
- Wrong punctuation (Chinese vs Western)
- Incorrect author name order in Western references

### 3. Execute

**Critical Rule — No Fabrication**:
NEVER invent or hallucinate bibliographic information. Only extract and format data that the user explicitly provides (e.g., uploaded PDFs, pasted text, direct input). If any required field is missing, flag it as `【待補：作者/書名/出版地/出版社/年份/頁碼】` rather than guessing.

**For Generation**:
- Only when user provides raw citation data (uploaded files, pasted excerpts, explicit text), extract and format according to rules
- If information is incomplete, ask the user to provide the missing field instead of guessing
- Maintain a running list of cited works to track first vs repeat citations
- Auto-apply 同上 and 同註 abbreviations
- Generate both footnotes and end references

**For Checking**:
- Scan the provided text for all citations
- Check each against rules in citation-guide.md
- Flag errors with specific corrections
- If a citation is missing required fields, mark as `【資訊不全：缺作者/書名/出版資訊】` — do NOT invent data to fill gaps
- Return corrected version

### 4. Output Format

Always present citations in clean, copy-paste ready format:

```
[腳註]
1 作者名，《書名》（出版地：出版社，年份），頁碼。
2 同上，頁碼。
3 同註[1]，頁碼。

[參考文獻]
中文文獻
作者名：《書名》。出版地：出版社，年份。

外文文獻
Author, Name. *Title*. Place: Publisher, Year.
```

## References

- `references/citation-guide.md` — Complete formatting rules and examples
