# Extraction Examples

## 公众号

**Input**: `https://mp.weixin.qq.com/...`

**Expected**:
- source = 公众号
- handler = browser
- include title / author / date / body / images
- save path based on title

## 飞书文档

**Input**: `https://*.feishu.cn/docx/...`

**Expected**:
- source = 飞书文档
- handler = feishu
- preserve headings, lists, code blocks, tables, todos

## 飞书知识库

**Input**: `https://*.feishu.cn/wiki/...`

**Expected**:
- source = 飞书知识库
- resolve node first
- then extract the underlying doc content

## YouTube

**Input**: `https://www.youtube.com/watch?v=...`

**Expected**:
- source = YouTube
- handler = transcript
- if transcript missing, say so explicitly

## 通用网页

**Input**: article/blog/news page

**Expected**:
- source = 网页
- try r.jina.ai first
- then defuddle.md
- then web_fetch/browser
- keep a short failure reason if all fail

## Extractor

**Input**: any supported URL

**Expected**:
- route first
- build execution spec
- choose save path
- emit Markdown contract
- preserve fallback chain
