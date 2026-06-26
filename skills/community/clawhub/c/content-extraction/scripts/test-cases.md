# content-extraction Test Cases

## Expected behavior

- 输入先路由，再抓取
- 输出 Markdown，不输出 HTML 噪音
- 长内容默认建议落盘
- 失败时说明卡在哪一层

## Test matrix

### 1. 微信公众号
- **Input**: `https://mp.weixin.qq.com/...`
- **Expected**:
  - route = browser
  - output includes title / author / date /正文
  - images preserved
  - if extraction fails, explain which selector / load stage failed

### 2. 飞书文档
- **Input**: `https://*.feishu.cn/docx/...`
- **Expected**:
  - route = feishu toolchain
  - headings/lists/code blocks kept
  - tables converted when possible

### 3. 飞书知识库
- **Input**: `https://*.feishu.cn/wiki/...`
- **Expected**:
  - resolve wiki node first
  - extract underlying doc structure
  - preserve hierarchy

### 4. YouTube
- **Input**: `https://www.youtube.com/watch?v=...`
- **Expected**:
  - route = transcript chain
  - transcript or summary returned
  - if no transcript, say so clearly

### 5. 通用网页
- **Input**: ordinary article URL
- **Expected**:
  - try r.jina.ai
  - if fail, try defuddle.md
  - if fail, try web_fetch/browser fallback
  - return final failure reason if all fail

## Pass criteria

- Route choice matches source type
- Markdown is readable and concise
- Failure path is explicit
- No silent success on empty content
