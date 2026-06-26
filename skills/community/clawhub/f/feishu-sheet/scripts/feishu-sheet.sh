#!/bin/bash
# feishu-sheet.sh — Feishu Spreadsheet (Sheets) API wrapper for OpenClaw
# Version: 1.2.0
# Usage: feishu-sheet.sh <action> [args...]
#
# Required credentials (auto-read from config):
#   channels.feishu.appId     - Feishu app ID
#   channels.feishu.appSecret - Feishu app secret
# Config location: ~/.openclaw/openclaw.json (override with OPENCLAW_CONFIG)
#
# Feishu app permissions needed: sheets:spreadsheet (spreadsheet read/write)
# Recommend using a minimal-permission Feishu app for this skill.

set -euo pipefail

FEISHU_BASE="https://open.feishu.cn/open-apis"
TOKEN_CACHE="${TMPDIR:-/tmp}/.feishu_tenant_token_$(id -u)"
TOKEN_EXPIRE="${TMPDIR:-/tmp}/.feishu_tenant_token_expire_$(id -u)"

resolve_credentials() {
  local config_path="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
  if [[ ! -f "$config_path" ]]; then
    echo '{"error":"openclaw.json not found. Set OPENCLAW_CONFIG or ensure ~/.openclaw/openclaw.json exists."}' >&2
    exit 1
  fi

  local creds rc
  creds=$(python3 -c '
import json, sys, re
try:
    with open(sys.argv[1]) as f:
        c = json.load(f)
    feishu = c.get("channels", {}).get("feishu", {})
    app_id = str(feishu.get("appId", ""))
    app_secret = str(feishu.get("appSecret", ""))
    if not app_id or not app_secret:
        print("feishu appId/appSecret not found in openclaw.json channels.feishu", file=sys.stderr)
        sys.exit(1)
    pat = re.compile(r"^[A-Za-z0-9_\-]+$")
    if not pat.match(app_id) or not pat.match(app_secret):
        print("appId/appSecret contain unexpected characters", file=sys.stderr)
        sys.exit(1)
    print(app_id)
    print(app_secret)
except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
' "$config_path" 2>/dev/null)
  rc=$?

  if [[ $rc -ne 0 || -z "$creds" ]]; then
    echo '{"error":"Failed to read feishu credentials from openclaw.json. Ensure channels.feishu.appId and channels.feishu.appSecret are configured."}' >&2
    exit 1
  fi

  FEISHU_APP_ID=$(echo "$creds" | head -1)
  FEISHU_APP_SECRET=$(echo "$creds" | tail -1)

  if [[ -z "$FEISHU_APP_ID" || -z "$FEISHU_APP_SECRET" ]]; then
    echo '{"error":"Failed to read feishu credentials from openclaw.json"}' >&2
    exit 1
  fi
}

resolve_credentials

get_tenant_token() {
  local now
  now=$(date +%s)
  if [[ -f "$TOKEN_CACHE" && -f "$TOKEN_EXPIRE" ]]; then
    local expire
    expire=$(cat "$TOKEN_EXPIRE")
    if (( now < expire )); then
      cat "$TOKEN_CACHE"
      return
    fi
  fi
  local resp
  resp=$(curl -s -X POST "$FEISHU_BASE/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}")
  local token
  token=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))" 2>/dev/null)
  local expire_in
  expire_in=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('expire',7200))" 2>/dev/null)
  if [[ -z "$token" ]]; then
    echo "{\"error\":\"Failed to get tenant_access_token\"}" >&2
    exit 1
  fi
  echo "$token" > "$TOKEN_CACHE"
  echo $(( now + expire_in - 300 )) > "$TOKEN_EXPIRE"
  echo "$token"
}

api_call() {
  local method="$1" path="$2"
  shift 2
  local token
  token=$(get_tenant_token)
  curl -s -X "$method" "$FEISHU_BASE$path" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    "$@"
}

api_upload() {
  local path="$1"
  shift
  local token
  token=$(get_tenant_token)
  curl -s -X POST "$FEISHU_BASE$path" \
    -H "Authorization: Bearer $token" \
    "$@"
}

pj() { python3 -m json.tool 2>/dev/null || cat; }

# ========================= Spreadsheet =========================

action_create() {
  local title="${1:-新建电子表格}" folder="${2:-}"
  local body="{\"title\":\"$title\""
  [[ -n "$folder" ]] && body+=",\"folder_token\":\"$folder\""
  body+="}"
  api_call POST "/sheets/v3/spreadsheets" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
ss = d.get('data',{}).get('spreadsheet',{})
if ss:
    t = ss.get('spreadsheet_token','')
    print(json.dumps({'success':True,'spreadsheet_token':t,'title':ss.get('title',''),'url':ss.get('url',f'https://feishu.cn/sheets/{t}')}, ensure_ascii=False, indent=2))
else:
    print(json.dumps({'error':d.get('msg','unknown'),'code':d.get('code',0)}, ensure_ascii=False, indent=2))
"
}

action_meta() {
  api_call GET "/sheets/v2/spreadsheets/$1/metainfo" | python3 -c "
import sys,json
d = json.load(sys.stdin)
props = d.get('data',{}).get('properties',{})
sheets = d.get('data',{}).get('sheets',[])
print(json.dumps({
    'title': props.get('title',''),
    'sheet_count': len(sheets),
    'sheets': [{'sheet_id':s.get('sheetId',''),'title':s.get('title',''),'rows':s.get('rowCount',0),'cols':s.get('columnCount',0)} for s in sheets]
}, ensure_ascii=False, indent=2))
"
}

# ========================= Data R/W =========================

action_read() {
  api_call GET "/sheets/v2/spreadsheets/$1/values/$2?valueRenderOption=ToString" | python3 -c "
import sys,json
d = json.load(sys.stdin)
vr = d.get('data',{}).get('valueRange',{})
print(json.dumps({'range':vr.get('range',''),'rows':len(vr.get('values',[])),'values':vr.get('values',[])}, ensure_ascii=False, indent=2))
"
}

action_read_multi() {
  local token="$1"
  shift
  local ranges_param=""
  for r in "$@"; do
    [[ -n "$ranges_param" ]] && ranges_param+="&"
    ranges_param+="ranges=$r"
  done
  api_call GET "/sheets/v2/spreadsheets/$token/values_batch_get?$ranges_param&valueRenderOption=ToString" | python3 -c "
import sys,json
d = json.load(sys.stdin)
vrs = d.get('data',{}).get('valueRanges',[])
result = []
for vr in vrs:
    result.append({'range':vr.get('range',''),'rows':len(vr.get('values',[])),'values':vr.get('values',[])})
print(json.dumps(result, ensure_ascii=False, indent=2))
"
}

action_write() {
  local body="{\"valueRange\":{\"range\":\"$2\",\"values\":$3}}"
  api_call PUT "/sheets/v2/spreadsheets/$1/values" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
da = d.get('data',{})
print(json.dumps({'success':d.get('code',1)==0,'updated_range':da.get('updatedRange',''),'updated_cells':da.get('updatedCells',0),'updated_rows':da.get('updatedRows',0),'updated_columns':da.get('updatedColumns',0)}, ensure_ascii=False, indent=2))
"
}

action_write_multi() {
  local token="$1" data="$2"
  api_call POST "/sheets/v2/spreadsheets/$token/values_batch_update" -d "$data" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'responses':d.get('data',{}).get('responses',[])}, ensure_ascii=False, indent=2))
"
}

action_append() {
  local body="{\"valueRange\":{\"range\":\"$2\",\"values\":$3}}"
  api_call POST "/sheets/v2/spreadsheets/$1/values_append" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
da = d.get('data',{})
print(json.dumps({'success':d.get('code',1)==0,'updated_range':da.get('updatedRange',''),'updated_cells':da.get('updatedCells',0)}, ensure_ascii=False, indent=2))
"
}

action_prepend() {
  local body="{\"valueRange\":{\"range\":\"$2\",\"values\":$3}}"
  api_call POST "/sheets/v2/spreadsheets/$1/values_prepend" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
da = d.get('data',{})
print(json.dumps({'success':d.get('code',1)==0,'updated_range':da.get('updatedRange',''),'updated_cells':da.get('updatedCells',0)}, ensure_ascii=False, indent=2))
"
}

# ========================= Images =========================

action_insert_image() {
  local token="$1" range="$2" image_path="$3"
  local filename
  filename=$(basename "$image_path")

  local image_array
  image_array=$(python3 -c "
with open('$image_path','rb') as f:
    print(list(f.read()))
")
  local body="{\"range\":\"$range\",\"image\":$image_array,\"name\":\"$filename\"}"
  api_call POST "/sheets/v2/spreadsheets/$token/values_image" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
if d.get('code',1)==0:
    print(json.dumps({'success':True,'range':'$range','image':'$filename'}, ensure_ascii=False, indent=2))
else:
    print(json.dumps({'error':d.get('msg','unknown'),'code':d.get('code',0)}, ensure_ascii=False, indent=2))
"
}

action_float_image() {
  local token="$1" sheet_id="$2" image_path="$3" range="${4:-${sheet_id}!A1:A1}"
  local width="${5:-400}" height="${6:-300}"
  local filename
  filename=$(basename "$image_path")
  local filesize
  filesize=$(stat -c%s "$image_path" 2>/dev/null || stat -f%z "$image_path" 2>/dev/null)

  local upload_resp
  upload_resp=$(api_upload "/drive/v1/medias/upload_all" \
    -F "file_name=$filename" \
    -F "parent_type=sheet_image" \
    -F "parent_node=$token" \
    -F "size=$filesize" \
    -F "file=@$image_path")

  local file_token
  file_token=$(echo "$upload_resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('file_token',''))" 2>/dev/null)

  if [[ -z "$file_token" ]]; then
    echo "$upload_resp" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'error':'upload failed','detail':d.get('msg',str(d))}, ensure_ascii=False, indent=2))
"
    return 1
  fi

  local body="{\"float_image_token\":\"$file_token\",\"range\":\"$range\",\"width\":$width,\"height\":$height}"
  api_call POST "/sheets/v3/spreadsheets/$token/sheets/$sheet_id/float_images" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
fi = d.get('data',{}).get('float_image',{})
if fi:
    print(json.dumps({'success':True,'float_image_id':fi.get('float_image_id',''),'range':fi.get('range',''),'width':fi.get('width',0),'height':fi.get('height',0)}, ensure_ascii=False, indent=2))
else:
    print(json.dumps({'error':d.get('msg','unknown'),'code':d.get('code',0)}, ensure_ascii=False, indent=2))
"
}

action_float_image_url() {
  local token="$1" sheet_id="$2" image_url="$3" range="${4:-${sheet_id}!A1:A1}"
  local width="${5:-400}" height="${6:-300}"

  local tmpfile
  tmpfile=$(mktemp /tmp/feishu_img_XXXXXX)
  local filename
  filename=$(basename "$image_url" | sed 's/\?.*//')
  [[ "$filename" != *.* ]] && filename="${filename}.png"

  curl -sL "$image_url" -o "$tmpfile"
  if [[ ! -s "$tmpfile" ]]; then
    rm -f "$tmpfile"
    echo '{"error":"Failed to download image from URL"}'
    return 1
  fi

  action_float_image "$token" "$sheet_id" "$tmpfile" "$range" "$width" "$height"
  rm -f "$tmpfile"
}

# ========================= Style =========================

action_style() {
  local token="$1" range="$2" style_json="$3"
  local body="{\"appendStyle\":{\"range\":\"$range\",\"style\":$style_json}}"
  api_call PUT "/sheets/v2/spreadsheets/$token/style" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

action_style_batch() {
  local token="$1" data="$2"
  api_call PUT "/sheets/v2/spreadsheets/$token/styles_batch_update" -d "$data" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

# ========================= Merge =========================

action_merge() {
  local token="$1" range="$2" merge_type="${3:-MERGE_ALL}"
  api_call POST "/sheets/v2/spreadsheets/$token/merge_cells" \
    -d "{\"range\":\"$range\",\"mergeType\":\"$merge_type\"}" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

action_unmerge() {
  local token="$1" range="$2"
  api_call POST "/sheets/v2/spreadsheets/$token/unmerge_cells" \
    -d "{\"range\":\"$range\"}" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

# ========================= Sheets =========================

action_add_sheet() {
  local body="{\"requests\":[{\"addSheet\":{\"properties\":{\"title\":\"$2\"}}}]}"
  api_call POST "/sheets/v2/spreadsheets/$1/sheets_batch_update" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
replies = d.get('data',{}).get('replies',[])
if replies:
    p = replies[0].get('addSheet',{}).get('properties',{})
    print(json.dumps({'success':True,'sheet_id':p.get('sheetId',''),'title':p.get('title','')}, ensure_ascii=False, indent=2))
else:
    print(json.dumps({'error':d.get('msg','unknown'),'code':d.get('code',0)}, ensure_ascii=False, indent=2))
"
}

action_delete_sheet() {
  local body="{\"requests\":[{\"deleteSheet\":{\"sheetId\":\"$2\"}}]}"
  api_call POST "/sheets/v2/spreadsheets/$1/sheets_batch_update" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

action_copy_sheet() {
  local body="{\"requests\":[{\"copySheet\":{\"source\":{\"sheetId\":\"$2\"},\"destination\":{\"title\":\"$3\"}}}]}"
  api_call POST "/sheets/v2/spreadsheets/$1/sheets_batch_update" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
replies = d.get('data',{}).get('replies',[])
if replies:
    p = replies[0].get('copySheet',{}).get('properties',{})
    print(json.dumps({'success':True,'sheet_id':p.get('sheetId',''),'title':p.get('title','')}, ensure_ascii=False, indent=2))
else:
    print(json.dumps({'error':d.get('msg','unknown'),'code':d.get('code',0)}, ensure_ascii=False, indent=2))
"
}

# ========================= Rows/Cols =========================

action_add_rows() {
  local body="{\"dimension\":{\"sheetId\":\"$2\",\"majorDimension\":\"ROWS\",\"length\":$3}}"
  api_call POST "/sheets/v2/spreadsheets/$1/dimension_range" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

action_add_cols() {
  local body="{\"dimension\":{\"sheetId\":\"$2\",\"majorDimension\":\"COLUMNS\",\"length\":$3}}"
  api_call POST "/sheets/v2/spreadsheets/$1/dimension_range" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

action_insert_rows() {
  local body="{\"dimension\":{\"sheetId\":\"$2\",\"majorDimension\":\"ROWS\",\"startIndex\":$3,\"endIndex\":$4},\"inheritStyle\":\"BEFORE\"}"
  api_call POST "/sheets/v2/spreadsheets/$1/insert_dimension_range" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

action_delete_rows() {
  local body="{\"dimension\":{\"sheetId\":\"$2\",\"majorDimension\":\"ROWS\",\"startIndex\":$3,\"endIndex\":$4}}"
  api_call DELETE "/sheets/v2/spreadsheets/$1/dimension_range" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

action_delete_cols() {
  local body="{\"dimension\":{\"sheetId\":\"$2\",\"majorDimension\":\"COLUMNS\",\"startIndex\":$3,\"endIndex\":$4}}"
  api_call DELETE "/sheets/v2/spreadsheets/$1/dimension_range" -d "$body" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(json.dumps({'success':d.get('code',1)==0,'msg':d.get('msg','')}, ensure_ascii=False, indent=2))
"
}

# ========================= Find/Replace =========================

action_find() {
  api_call POST "/sheets/v3/spreadsheets/$1/sheets/$2/find" \
    -d "{\"find\":\"$3\",\"find_condition\":{\"range\":\"$2\"}}" | python3 -c "
import sys,json
d = json.load(sys.stdin)
fr = d.get('data',{}).get('find_result',{})
cells = fr.get('matched_cells',[]) if fr else []
print(json.dumps({'success':d.get('code',1)==0,'matched':len(cells),'rows_count':fr.get('rows_count',0),'cells':cells[:50]}, ensure_ascii=False, indent=2))
"
}

action_replace() {
  api_call POST "/sheets/v3/spreadsheets/$1/sheets/$2/replace" \
    -d "{\"find\":\"$3\",\"replacement\":\"$4\",\"find_condition\":{\"range\":\"$2\"}}" | python3 -c "
import sys,json
d = json.load(sys.stdin)
rr = d.get('data',{}).get('replace_result',{})
print(json.dumps({'success':d.get('code',1)==0,'matched':rr.get('matched_cells_count',0),'replaced':rr.get('replaced_cells_count',0)}, ensure_ascii=False, indent=2))
"
}

# ========================= Main =========================

ACTION="${1:-help}"
shift || true

case "$ACTION" in
  create)       action_create "${1:-}" "${2:-}" ;;
  meta)         action_meta "$1" ;;
  read)         action_read "$1" "$2" ;;
  read_multi)   action_read_multi "$@" ;;
  write)        action_write "$1" "$2" "$3" ;;
  write_multi)  action_write_multi "$1" "$2" ;;
  append)       action_append "$1" "$2" "$3" ;;
  prepend)      action_prepend "$1" "$2" "$3" ;;
  insert_image)      action_insert_image "$1" "$2" "$3" ;;
  float_image)       action_float_image "$1" "$2" "$3" "${4:-}" "${5:-400}" "${6:-300}" ;;
  float_image_url)   action_float_image_url "$1" "$2" "$3" "${4:-}" "${5:-400}" "${6:-300}" ;;
  style)        action_style "$1" "$2" "$3" ;;
  style_batch)  action_style_batch "$1" "$2" ;;
  merge)        action_merge "$1" "$2" "${3:-MERGE_ALL}" ;;
  unmerge)      action_unmerge "$1" "$2" ;;
  add_sheet)    action_add_sheet "$1" "$2" ;;
  delete_sheet) action_delete_sheet "$1" "$2" ;;
  copy_sheet)   action_copy_sheet "$1" "$2" "$3" ;;
  add_rows)     action_add_rows "$1" "$2" "$3" ;;
  add_cols)     action_add_cols "$1" "$2" "$3" ;;
  insert_rows)  action_insert_rows "$1" "$2" "$3" "$4" ;;
  delete_rows)  action_delete_rows "$1" "$2" "$3" "$4" ;;
  delete_cols)  action_delete_cols "$1" "$2" "$3" "$4" ;;
  find)         action_find "$1" "$2" "$3" ;;
  replace)      action_replace "$1" "$2" "$3" "$4" ;;
  help|*)
    cat << 'HELPEOF'
Feishu Spreadsheet Tool v1.0.0

Usage: feishu-sheet.sh <action> [args...]

Credentials are auto-read from ~/.openclaw/openclaw.json (channels.feishu).
Set OPENCLAW_CONFIG to override the config path.

Spreadsheet:
  create [title] [folder_token]                         Create spreadsheet
  meta <token>                                          Get metadata (sheets list)

Data:
  read <token> <range>                                  Read cell range
  read_multi <token> <range1> <range2> ...              Read multiple ranges
  write <token> <range> <values_json>                   Write data (overwrite)
  write_multi <token> <json_body>                       Write to multiple ranges
  append <token> <range> <values_json>                  Append rows
  prepend <token> <range> <values_json>                 Prepend rows

Images:
  insert_image <token> <range> <file_path>              Insert image into cell
  float_image <token> <sheet_id> <path> [range] [w] [h] Insert floating image (local)
  float_image_url <token> <sheet_id> <url> [range] [w] [h] Insert floating image (URL)

Style:
  style <token> <range> <style_json>                    Set cell style
  style_batch <token> <json_body>                       Batch set styles

Merge:
  merge <token> <range> [MERGE_ALL|MERGE_ROWS|MERGE_COLUMNS]
  unmerge <token> <range>

Sheets:
  add_sheet <token> <title>                             Add worksheet
  delete_sheet <token> <sheet_id>                       Delete worksheet
  copy_sheet <token> <sheet_id> <new_title>             Copy worksheet

Rows/Columns:
  add_rows <token> <sheet_id> <count>
  add_cols <token> <sheet_id> <count>
  insert_rows <token> <sheet_id> <start> <end>          Insert rows (0-indexed)
  delete_rows <token> <sheet_id> <start> <end>
  delete_cols <token> <sheet_id> <start> <end>

Find/Replace:
  find <token> <sheet_id> <keyword>
  replace <token> <sheet_id> <find> <replacement>

Style JSON example: {"bold":true,"foreColor":"#FF0000","backColor":"#FFFF00","fontSize":14}
HELPEOF
    ;;
esac
