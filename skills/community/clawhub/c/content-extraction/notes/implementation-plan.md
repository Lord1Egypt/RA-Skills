# Implementation Plan: content-extraction

## Goal

Build an OpenClaw-native skill that turns URLs and documents into clean Markdown with minimal noise and strong platform-specific handling.

## Phase 1: Skill skeleton

- [x] Write OpenClaw `SKILL.md`
- [x] Write README and source mapping notes
- [x] Decide whether to add helper scripts or keep logic in skill text
  - Decision: keep the core logic in skill text and lightweight notes/scripts only

## Phase 2: Platform handlers

### WeChat
- Use browser toolchain
- Detect page load success
- Extract title, author, date, body, images
- Return Markdown + optional local save path

### Feishu
- Use feishu_doc / feishu_wiki tools
- Preserve block structure
- Convert lists, headings, quotes, code, todo, tables where possible

### Generic URLs
- Try r.jina.ai first
- Then defuddle.md
- Then web_fetch / browser fallback
- Return why each fallback failed when necessary

### YouTube
- Delegate to existing transcript skill chain
- Normalize transcript into Markdown

## Phase 3: UX

- Always show title / source / URL
- Provide concise summary
- Save full Markdown when content is long
- Keep failure messages explicit and short

## Phase 4: Hardening

- Add examples for common URLs
- Add clear fallback order
- Add platform-specific failure messages
- Add test URLs for internal verification

## Phase 5: Test samples

### WeChat samples
- Public account article with正文、作者、发布时间齐全
- Article that loads slowly and needs retry handling
- Article with image-heavy content
- Article that fails direct extraction and should fall back gracefully

### Feishu samples
- doc 文档（含标题、列表、代码块）
- docx 文档（含表格、引用、待办）
- wiki 页面（含多层级 block）
- 有权限限制的页面，验证失败提示是否清晰

### Generic URL samples
- News/blog article with clean HTML
- JS-heavy page with poor fetch output
- Page that succeeds via r.jina.ai
- Page that only succeeds via browser fallback

### YouTube samples
- Video with available transcript
- Video with missing transcript, verify fallback message
- Long transcript, verify summary + save path behavior

## Deliverable

A single OpenClaw skill directory that can be dropped into the workspace and used as the default content extraction helper.
