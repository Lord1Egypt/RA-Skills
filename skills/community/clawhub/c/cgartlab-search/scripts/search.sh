#!/usr/bin/env bash
# cgartlab-search dispatcher (curl + python). For harnesses whose shell can reach the network.
# In DSH's sandboxed shell (no outbound network) use web_fetch instead — see references/backends.md.
#
# Usage: ./search.sh <backend> "<query>" [limit]
#   backend: brave|exa|context7|tencent|zhihu|bing|qqnews|hupu|so|github|hn
# Keys: env vars, or secrets.json next to SKILL.md (key-less backends need none).
# Output: one line of normalized JSON on stdout.
set -euo pipefail
b="${1:-}"; q="${2:-}"; n="${3:-5}"
# `tencent` is the only backend whose query may be empty — that means its 热点榜.
if [ -z "$b" ] || { [ -z "$q" ] && [ "$b" != "tencent" ]; }; then
  echo 'usage: search.sh <backend> "<query>" [limit]   (tencent: empty query = 热点榜)' >&2; exit 2
fi
here="$(cd "$(dirname "$0")" && pwd)"

# Python interpreter probe: every parser below is Python. On Windows `python3` can be a
# Store/App-Execution-Alias stub that exits 0 while printing nothing, so verify real
# output instead of trusting the exit code.
py=""
for cand in "${PYTHON:-}" python3 python; do
  [ -n "$cand" ] || continue
  if [ "$("$cand" -c 'print(1)' 2>/dev/null)" = "1" ]; then py="$cand"; break; fi
done
if [ -z "$py" ]; then
  echo '{"errors":[{"backend":"*","error":"no working python3/python found — set PYTHON=/path/to/python"}]}'; exit 0
fi

# secrets.json lives next to SKILL.md (skill root); a copy beside this script still works.
secrets_file=""
for cand in "$here/secrets.json" "$here/../secrets.json"; do
  [ -f "$cand" ] && secrets_file="$cand" && break
done

if [ -n "$secrets_file" ]; then
  while IFS='=' read -r ek val; do
    case "$ek" in
      BRAVE_SEARCH_API_KEY|EXA_API_KEY|CONTEXT7_API_KEY|TENCENT_NEWS_KEY|ZHIHU_API_KEY)
        [ -z "${!ek:-}" ] && export "$ek=$val" ;;
    esac
  done < <("$py" -c '
import json,sys
d=json.load(sys.stdin)
m={"brave_api_key":"BRAVE_SEARCH_API_KEY","exa_api_key":"EXA_API_KEY","context7_api_key":"CONTEXT7_API_KEY","tencent_news_key":"TENCENT_NEWS_KEY","zhihu_api_key":"ZHIHU_API_KEY"}
for fk,ek in m.items():
    v=d.get(fk) or ""
    # No shell quoting: the value is consumed via `read -r ek val`, and a quoted value
    # would put literal quotes into the header sent upstream.
    if v: print(f"{ek}={v}")
' < "$secrets_file")
fi

enc(){ "$py" -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$1"; }

case "$b" in
  bing)
    curl -sS --compressed "https://cn.bing.com/search?q=$(enc "$q")&format=rss" \
      | "$py" -c 'import sys,re,html,json
n=int(sys.argv[1]); xml=sys.stdin.read(); out=[]
def g(src,t):
    m=re.search("<"+t+"[^>]*>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?</"+t+">", src)
    return html.unescape(m.group(1).strip()) if m else ""
for it in re.findall("<item>([\\s\\S]*?)</item>", xml)[:n]:
    t,u=g(it,"title"),g(it,"link")
    if t and u: out.append({"backend":"bing","type":"web","title":t,"url":u,"snippet":g(it,"description"),"published":g(it,"pubDate") or None})
print(json.dumps({"results":out},ensure_ascii=False))' "$n"
    ;;
  qqnews)
    curl -sS --compressed "https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=10" \
      | "$py" -c 'import sys,json
n=int(sys.argv[1]); j=json.load(sys.stdin)
nl=((j.get("idlist") or [{}])[0].get("newslist")) or []
out=[{"backend":"qqnews","type":"news","title":x.get("title"),"url":x.get("url"),"snippet":(x.get("abstract") or "")[:300],"published":x.get("time"),"source":((x.get("card") or {}).get("chlname"))} for x in nl if x.get("url") and x.get("title")][:n]
print(json.dumps({"results":out,"note":"hot list, not query-filtered"},ensure_ascii=False))' "$n"
    ;;
  hupu)
    curl -sS --compressed "https://soccer.hupu.com/" \
      | "$py" -c 'import sys,re,html,json
n=int(sys.argv[1]); h=sys.stdin.read(); seen=set(); out=[]
for m in re.finditer("<a[^>]+href=[\"\x27](https://bbs\\.hupu\\.com/\\d+\\.html)[\"\x27][^>]*>([\\s\\S]*?)</a>", h):
    t=html.unescape(re.sub("<[^>]+>","",m.group(2))).strip()
    if len(t)<8 or m.group(1) in seen: continue
    seen.add(m.group(1)); out.append({"backend":"hupu","type":"news","title":t,"url":m.group(1),"snippet":""})
    if len(out)>=n: break
print(json.dumps({"results":out},ensure_ascii=False))' "$n"
    ;;
  so)
    curl -sS --compressed "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=$(enc "$q")&site=stackoverflow&pagesize=$n" \
      | "$py" -c 'import sys,json,html,datetime
j=json.load(sys.stdin); out=[]
for x in j.get("items",[]):
    out.append({"backend":"so","type":"qa","title":html.unescape(x.get("title") or ""),"url":x.get("link"),"snippet":"[%s] %s · %s views" % (", ".join((x.get("tags") or [])[:5]), "answered" if x.get("is_answered") else "unanswered", x.get("view_count")),"score":x.get("score"),"published":datetime.datetime.fromtimestamp(x["creation_date"],datetime.timezone.utc).isoformat().replace("+00:00","Z") if x.get("creation_date") else None})
print(json.dumps({"results":out},ensure_ascii=False))'
    ;;
  github)
    curl -sS --compressed -H "Accept: application/vnd.github+json" "https://api.github.com/search/repositories?q=$(enc "$q")&sort=stars&per_page=$n" \
      | "$py" -c 'import sys,json
j=json.load(sys.stdin); out=[{"backend":"github","type":"repo","title":x.get("full_name"),"url":x.get("html_url"),"snippet":(x.get("description") or "")[:300],"score":x.get("stargazers_count"),"published":x.get("pushed_at")} for x in j.get("items",[])]
print(json.dumps({"results":out},ensure_ascii=False))'
    ;;
  hn)
    curl -sS --compressed "https://hn.algolia.com/api/v1/search?query=$(enc "$q")&hitsPerPage=$n" \
      | "$py" -c 'import sys,json
j=json.load(sys.stdin); out=[]
for x in j.get("hits",[]):
    if not x.get("title"): continue
    out.append({"backend":"hn","type":"community","title":x.get("title"),"url":x.get("url") or ("https://news.ycombinator.com/item?id=%s" % x.get("objectID")),"snippet":"%s points · %s comments" % (x.get("points") or 0, x.get("num_comments") or 0),"published":x.get("created_at")})
print(json.dumps({"results":out},ensure_ascii=False))'
    ;;
  context7)
    lib=$(curl -sS --compressed "https://context7.com/api/v1/search?query=$(enc "$q")" \
      | "$py" -c 'import json,sys
d=json.load(sys.stdin); r=d.get("results",[]); top=next((x for x in r if x.get("verified")), r[0] if r else None)
print(top["id"] if top else "")')
    if [ -z "$lib" ]; then echo '{"errors":[{"backend":"context7","error":"no library found"}]}'; exit 0; fi
    curl -sS --compressed "https://context7.com/api/v1/$(enc "${lib#/}")?tokens=4000" \
      | "$py" -c 'import json,sys
c=sys.stdin.read()
print(json.dumps({"backend":"context7","results":[{"backend":"context7","type":"docs","library":sys.argv[1],"title":sys.argv[1],"url":"https://context7.com/"+sys.argv[1],"content":c}]}))' "$lib"
    ;;
  brave)
    if [ -z "${BRAVE_SEARCH_API_KEY:-}" ]; then echo '{"errors":[{"backend":"brave","error":"missing key"}]}'; exit 0; fi
    curl -sS --compressed "https://api.search.brave.com/res/v1/web/search?q=$(enc "$q")&count=$n" \
      -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY" -H "Accept: application/json" \
      | "$py" -c 'import json,sys
d=json.load(sys.stdin)
print(json.dumps({"backend":"brave","results":[{"backend":"brave","type":"web","title":x.get("title"),"url":x.get("url"),"snippet":x.get("description",""),"published":x.get("age")} for x in d.get("web",{}).get("results",[])]}))'
    ;;
  exa)
    if [ -z "${EXA_API_KEY:-}" ]; then echo '{"errors":[{"backend":"exa","error":"missing key"}]}'; exit 0; fi
    body=$("$py" -c 'import json,sys;print(json.dumps({"query":sys.argv[1],"numResults":int(sys.argv[2]),"type":"auto","contents":{"text":True,"maxCharacters":1000}}))' "$q" "$n")
    curl -sS --compressed -X POST "https://api.exa.ai/search" -H "x-api-key: $EXA_API_KEY" -H "Content-Type: application/json" -d "$body" \
      | "$py" -c 'import json,sys
d=json.load(sys.stdin)
print(json.dumps({"backend":"exa","results":[{"backend":"exa","type":"web","title":x.get("title"),"url":x.get("url"),"snippet":(x.get("text") or "")[:300],"score":x.get("score"),"published":x.get("publishedDate")} for x in d.get("results",[])]}))'
    ;;
  zhihu)
    if [ -z "${ZHIHU_API_KEY:-}" ]; then echo '{"errors":[{"backend":"zhihu","error":"missing key"}]}'; exit 0; fi
    if [ "$n" -lt 1 ]; then n=1; elif [ "$n" -gt 20 ]; then n=20; fi   # API caps Count at 20
    curl -sS --compressed "https://developer.zhihu.com/api/v1/content/global_search?Query=$(enc "$q")&Count=$n" \
      -H "Authorization: Bearer $ZHIHU_API_KEY" \
      -H "X-Request-Timestamp: $(date +%s)" \
      | "$py" -c 'import sys,json,datetime
raw=sys.stdin.buffer.read().decode("utf-8","replace")
try: j=json.loads(raw)
except Exception: sys.stdout.buffer.write(json.dumps({"errors":[{"backend":"zhihu","error":"unparseable response"}]},ensure_ascii=False).encode("utf-8")); sys.exit(0)
if j.get("Code") not in (0,None):
    sys.stdout.buffer.write(json.dumps({"errors":[{"backend":"zhihu","error":"API Code %s: %s"%(j.get("Code"),j.get("Message"))}]},ensure_ascii=False).encode("utf-8")); sys.exit(0)
items=((j.get("Data") or {}).get("Items")) or []
out=[{"backend":"zhihu","type":"web","title":x.get("Title") or "","url":x.get("Url") or "","snippet":(x.get("ContentText") or "")[:300],"published":datetime.datetime.fromtimestamp(x["EditTime"],datetime.timezone.utc).isoformat().replace("+00:00","Z") if x.get("EditTime") else None,"author":x.get("AuthorName"),"score":x.get("RankingScore")} for x in items]
sys.stdout.buffer.write(json.dumps({"results":out},ensure_ascii=False).encode("utf-8"))'
    ;;
  tencent)
    # Official Go CLI (not an HTTP API). Resolution: env override -> PATH -> installer dir.
    cli="${TENCENT_NEWS_CLI_PATH:-}"
    if [ -z "$cli" ]; then cli="$(command -v tencent-news-cli 2>/dev/null || true)"; fi
    if [ -z "$cli" ] && [ -x "$HOME/.tencent-news-cli/bin/tencent-news-cli.exe" ]; then cli="$HOME/.tencent-news-cli/bin/tencent-news-cli.exe"; fi
    if [ -z "$cli" ] && [ -x "$HOME/.tencent-news-cli/bin/tencent-news-cli" ]; then cli="$HOME/.tencent-news-cli/bin/tencent-news-cli"; fi
    if [ -z "$cli" ]; then
      echo '{"errors":[{"backend":"tencent","error":"tencent-news-cli not found — install from https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1"}]}'; exit 0
    fi
    if [ "$n" -lt 1 ]; then n=1; elif [ "$n" -gt 50 ]; then n=50; fi
    # hot takes no query: only used when the keyword is empty (--news never drops a keyword).
    if [ -n "$q" ]; then raw="$("$cli" search "$q" --limit "$n" 2>&1 || true)"; else raw="$("$cli" hot --limit "$n" 2>&1 || true)"; fi
    printf '%s' "$raw" | "$py" -c 'import sys,re,json
raw=sys.stdin.buffer.read().decode("utf-8","replace")
w=lambda o: sys.stdout.buffer.write(json.dumps(o,ensure_ascii=False).encode("utf-8"))
if re.search("未设置 API Key|not set", raw): w({"errors":[{"backend":"tencent","error":"API key not configured — run: tencent-news-cli apikey-set <KEY>"}]}); sys.exit(0)
if re.search("API Key 无效|invalid api key|unauthorized", raw, re.I): w({"errors":[{"backend":"tencent","error":"API key invalid or unauthorized"}]}); sys.exit(0)
if "未找到与" in raw: w({"results":[]}); sys.exit(0)
out=[]
for b in re.split(r"\n(?=\d+\.\s*标题[:：])", raw):
    def g(label):
        m=re.search(r"^\s*"+label+r"[:：]\s*(.+)$", b, re.M)
        return m.group(1).strip() if m else ""
    t=re.search(r"^\s*\d+\.\s*标题[:：]\s*(.+)$", b, re.M)
    u=g("链接")
    if not t or not u: continue
    out.append({"backend":"tencent","type":"news","title":t.group(1).strip(),"url":u,"snippet":re.sub(r"\.\.\.$","",g("摘要")),"published":g("发布时间") or None,"source":g("来源") or None})
w({"results":out})'
    ;;
  *) echo "unknown backend: $b (choose: brave,exa,context7,tencent,zhihu,bing,qqnews,hupu,so,github,hn)" >&2; exit 2 ;;
esac