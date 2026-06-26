# Site-Specific Patterns

Anti-detection strategies and verified workflows for specific websites.

## Xiaohongshu (小红书)

**Anti-detection level**: High — requires CDP native events, not JS `.click()`

### Key Rules

1. **Use `detail_url` from search results** — contains `xsec_token` required for navigation
2. **Never navigate to `/explore/<id>` directly** — redirects to homepage
3. **Use CDP `Input.dispatchMouseEvent`** for clicking — `isTrusted=true`, bypasses detection
4. **`cdp_exec.py open` returns 405** — use `curl -X PUT` or `eval` navigation instead

### Search → Extract → Detail Workflow

```bash
# 1. Open search page
TAB_ID=$(curl -s -X PUT "http://localhost:9222/json/new?https://www.xiaohongshu.com/search_result?keyword=关键词&type=51" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
sleep 5

# 2. (Optional) Scroll to load more
python3 SKILL_DIR/scripts/smart_interact.py scroll $TAB_ID --direction down --amount 300 --steps 3

# 3. Extract search list with links
python3 SKILL_DIR/scripts/cdp_exec.py eval $TAB_ID "(function(){
  const notes=document.querySelectorAll('section.note-item');
  const results=[];
  notes.forEach((n,i)=>{
    if(i>=24)return;
    const link=n.querySelector('a.cover, a.title');
    const text=n.innerText;
    if(text.includes('大家都在搜'))return;
    results.push({index:results.length,text:text.substring(0,200),detail_url:link?link.getAttribute('href'):null});
  });
  return JSON.stringify({total:results.length,results},null,2);
})()"

# 4. Click note via CDP (anti-detection)
python3 SKILL_DIR/scripts/smart_interact.py click $TAB_ID --selector "section.note-item" --index 0
sleep 5

# 5. Extract note detail
python3 SKILL_DIR/scripts/cdp_exec.py eval $TAB_ID "(function(){
  const r={};
  r.title=(document.querySelector('.note-content .title')||{}).innerText?.trim()||document.title;
  r.author=(document.querySelector('[class*=\"author\"] [class*=\"name\"]')||{}).innerText?.trim()||'';
  r.date=(document.querySelector('[class*=\"date\"]')||{}).innerText?.trim()||'';
  r.body=(document.querySelector('#detail-desc, .desc')||{}).innerText?.trim()||'';
  const seen=new Set(),comments=[];
  document.querySelectorAll('[class*=\"comment-item\"],[class*=\"comment-inner\"]').forEach(c=>{
    const t=c.innerText.trim().substring(0,300);
    const k=t.substring(0,50);
    if(!seen.has(k)&&t.length>5){seen.add(k);comments.push(t);}
  });
  r.comments_count=comments.length;
  r.comments=comments.slice(0,20);
  return JSON.stringify(r,null,2);
})()"

# 6. Go back to search results
python3 SKILL_DIR/scripts/cdp_exec.py eval $TAB_ID "history.back()"
```

### DOM Selectors

| Element | Selector |
|---------|----------|
| Note cards | `section.note-item` |
| Cover link (with xsec_token) | `a.cover, a.title` |
| Note title | `.note-content .title` |
| Note body | `#detail-desc, .desc` |
| Author name | `[class*="author"] [class*="name"]` |
| Date | `[class*="date"]` |
| Comments | `[class*="comment-item"], [class*="comment-inner"]` |

### Gotchas

- Filter out "大家都在搜" recommendation module from results
- Comments have duplicates from DOM nesting — deduplicate with `Set`
- Each search returns ~24 results max
- Search types: `type=51` (default), `type=2` (newest)
- Use "避雷" keyword for finding negatives, more trustworthy than high-likes

## Generic Anti-Detection Sites

### When to Use CDP Native Events vs JS eval

| Scenario | Method | Why |
|----------|--------|-----|
| Simple navigation | `eval "location.href='...'"` | No click needed |
| Reading content | `eval "document.body.innerText"` | No interaction |
| Clicking buttons on anti-bot sites | `smart_interact.py click` | `isTrusted=true` |
| Filling forms on anti-bot sites | `smart_interact.py type --human` | Char-by-char simulation |
| Sites checking `isTrusted` property | `smart_interact.py click` | Real browser events |

### Universal Anti-Detection Pattern

```bash
# 1. Navigate
python3 SKILL_DIR/scripts/cdp_exec.py eval $TAB_ID "location.href='https://example.com'"
python3 SKILL_DIR/scripts/smart_interact.py wait $TAB_ID --page-load --timeout 10

# 2. Wait for content
python3 SKILL_DIR/scripts/smart_interact.py wait $TAB_ID --selector ".content" --timeout 10

# 3. Click using CDP events
python3 SKILL_DIR/scripts/smart_interact.py click $TAB_ID --selector "button.load-more"

# 4. Extract after action
python3 SKILL_DIR/scripts/cdp_exec.py eval $TAB_ID "document.querySelector('.content').innerText"
```

## SPA (Single Page Applications)

### Challenge
SPA pages don't do full page reloads — content loads dynamically via JavaScript.

### Strategy

```bash
# 1. Navigate
python3 SKILL_DIR/scripts/cdp_exec.py eval $TAB_ID "location.href='https://spa-example.com'"

# 2. Wait for selector (not just page load)
python3 SKILL_DIR/scripts/smart_interact.py wait $TAB_ID --selector ".app-loaded" --timeout 15

# 3. Optionally wait for network idle
python3 SKILL_DIR/scripts/smart_interact.py wait $TAB_ID --network-idle --timeout 10

# 4. Interact
python3 SKILL_DIR/scripts/smart_interact.py click $TAB_ID --selector "nav a.dashboard"
python3 SKILL_DIR/scripts/smart_interact.py wait $TAB_ID --selector ".dashboard-content"
```

### Tips

- Always wait for a specific selector, not just `readyState`
- Use `page_state.py status` to check load progress
- Use `page_state.py pagination` to detect dynamic load-more buttons
- Use `smart_interact.py scroll` to trigger lazy-loaded content

## Infinite Scroll Pages

```bash
# Scroll and collect data in a loop
for i in $(seq 1 5); do
    python3 SKILL_DIR/scripts/smart_interact.py scroll $TAB_ID --direction down --amount 400 --steps 2
    sleep 2
    python3 SKILL_DIR/scripts/cdp_exec.py eval $TAB_ID "document.querySelectorAll('.item').length"
done
```
