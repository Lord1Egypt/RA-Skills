#!/bin/bash
# bytetech-fetch.sh - 获取 ByteTech 文章内容
# 用法: ./bytetech-fetch.sh <article_id> [doc_token]
#
# 如果提供了 doc_token（URL hash 部分），则同时获取飞书文档正文
# 如果只提供 article_id，则只获取元信息

set -euo pipefail

SESSION="bytetech"
BASE_URL="https://bytetech.info"
LARK_BASE="https://bytedance.larkoffice.com/docx"

ARTICLE_ID="${1:?用法: $0 <article_id> [doc_token]}"
DOC_TOKEN="${2:-}"

# 确保浏览器 session 存在
check_session() {
    local url
    url=$(agent-browser --session-name "$SESSION" get url --json 2>/dev/null | \
        node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);console.log(r.data?.result||'')}catch(e){console.log('')}}" 2>/dev/null)
    if echo "$url" | grep -q "accounts.feishu.cn"; then
        echo "SESSION_EXPIRED" >&2
        return 1
    fi
    return 0
}

# 打开文章页
open_article() {
    local url="${BASE_URL}/articles/${ARTICLE_ID}"
    [ -n "$DOC_TOKEN" ] && url+="#${DOC_TOKEN}"
    
    agent-browser --session-name "$SESSION" open "$url" --timeout 30000 --json > /dev/null 2>&1
    agent-browser --session-name "$SESSION" wait --load networkidle --json > /dev/null 2>&1
}

# 提取元信息
get_meta() {
    agent-browser --session-name "$SESSION" eval --stdin --json <<'EVALEOF' 2>/dev/null | \
        node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);const inner=JSON.parse(r.data.result);console.log(JSON.stringify({title:inner.title,description:inner.description,docToken:inner.docToken,og:image:inner.ogImage},null,2))}catch(e){console.error('Parse error:',e.message)}})"
(() => {
  const title = document.title.replace(/ - 文章 - ByteTech$/, '');
  const og = {};
  document.querySelectorAll('meta[property^="og:"],meta[name]').forEach(m => {
    const k = m.getAttribute('property') || m.getAttribute('name');
    og[k] = m.content || '';
  });
  const token = location.hash.replace('#','') || 
    document.querySelector('tt-docs-component')?.getAttribute('src')?.match(/docx\/([a-zA-Z0-9]+)/)?.[1] || '';
  return JSON.stringify({ 
    title, 
    description: (og['og:description'] || '').replace(/[\n\r]/g, ' '),
    docToken: token,
    ogImage: og['og:image'] || ''
  });
})()
EVALEOF
}

# 获取飞书文档正文
get_doc_content() {
    local token="$1"
    agent-browser --session-name "$SESSION" open \
        "${LARK_BASE}/${token}?opendoc=1&hideTemplate=true&onboarding=0&theme=light" \
        --timeout 30000 --json > /dev/null 2>&1
    agent-browser --session-name "$SESSION" wait --load networkidle --json > /dev/null 2>&1
    
    # 飞书文档虚拟滚动，需要分段获取
    # 先获取当前可见内容
    agent-browser --session-name "$SESSION" get text body --json 2>/dev/null | \
        node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);console.log(r.data?.result||'')}catch(e){console.error(e.message)}})"
}

# === 主流程 ===

if ! check_session 2>/dev/null; then
    echo '{"error":"session_expired","hint":"请运行: agent-browser --headed --session-name bytetech open https://bytetech.info --timeout 120000"}'
    exit 1
fi

open_article

# 获取元信息
echo "=== 元信息 ==="
META=$(get_meta)
echo "$META"

# 如果有 doc_token 且未被提供，从 meta 中提取
if [ -z "$DOC_TOKEN" ]; then
    DOC_TOKEN=$(echo "$META" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{console.log(JSON.parse(d).docToken||'')}catch(e){console.log('')}}" 2>/dev/null)
fi

# 如果有 doc_token，获取正文
if [ -n "$DOC_TOKEN" ] && [ "$DOC_TOKEN" != '""' ] && [ "$DOC_TOKEN" != "null" ]; then
    echo ""
    echo "=== 飞书文档正文 (token: ${DOC_TOKEN}) ==="
    get_doc_content "$DOC_TOKEN"
else
    echo ""
    echo "未找到飞书文档 token，无法获取正文。"
fi
