## Description: <br>
扫描本地电子书库，自动提取元数据、分类整理、联网搜索书籍简介，生成Obsidian笔记的完整工作流。支持EPUB/MOBI/AZW3/PDF格式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatblue](https://clawhub.ai/user/fatblue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan a local ebook collection, organize extracted metadata, optionally enrich missing introductions through online search, and generate Obsidian-ready Markdown notes and index files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local ebook directories and writes persistent index and note files. <br>
Mitigation: Use a narrow source folder, choose a private output location, and review generated JSON and Markdown before importing them into a personal knowledge base. <br>
Risk: Optional online enrichment may send book titles or metadata to an external search service. <br>
Mitigation: Review the search helper before enabling online enrichment, adjust the delay and batch size for rate limits, and avoid processing sensitive library metadata with online search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fatblue/book-library-scanner) <br>
- [Dublin Core Metadata Element Set](http://purl.org/dc/elements/1.1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated artifacts include JSON indexes and Obsidian Markdown notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected ebook directory and writes persistent JSON/Markdown files to the chosen output directory; optional online enrichment may send book titles or metadata to an external search service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
