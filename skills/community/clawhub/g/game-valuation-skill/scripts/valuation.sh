#!/bin/bash
set -euo pipefail

BASE_URL="${GAME_VALUATION_BASE_URL:-http://ruliurobot.baizhanlive.com/game_valuation}"
QRCodeDir="${GAME_VALUATION_QRCODE_DIR:-/tmp/game-valuation-qrcode}"

request_json() {
  local method="$1" path="$2" body="${3:-}"
  local url="${BASE_URL}${path}"
  local args=(-s -X "$method")
  if [ -n "$body" ]; then
    args+=(-H "Content-Type: application/json" -d "$body")
  fi
  curl "${args[@]}" "$url"
}

post_json() { request_json POST "$1" "$2"; }
get_json() { request_json GET "$1"; }

open_target() {
  case "$(uname -s)" in
    Darwin) open "$1" >/dev/null 2>&1 || true ;;
    Linux) xdg-open "$1" >/dev/null 2>&1 || true ;;
  esac
}

account_type_from_server() {
  case "$1" in
    android_qq|ios_qq) printf '1' ;;
    android_wx|ios_wx) printf '2' ;;
    *) echo "Error: server 只支持 android_qq、ios_qq、android_wx、ios_wx" >&2; exit 1 ;;
  esac
}

save_and_open_qrcode() {
  local qrcode="$1" login_uuid="$2"
  mkdir -p "$QRCodeDir"

  if [[ "$qrcode" == http://* || "$qrcode" == https://* ]]; then
    open_target "$qrcode"
    printf '%s\n' "$qrcode"
    return
  fi

  local image_path="${QRCodeDir}/qrcode_${login_uuid}.png"
  local data="$qrcode"
  data="${data#data:image/png;base64,}"
  data="${data#data:image/jpeg;base64,}"
  data="${data#data:image/jpg;base64,}"

  if printf '%s' "$data" | python3 -c 'import base64,sys;sys.stdout.buffer.write(base64.b64decode(sys.stdin.read().strip()))' > "$image_path" 2>/dev/null; then
    open_target "$image_path"
    printf '%s\n' "$image_path"
    return
  fi

  local text_path="${QRCodeDir}/qrcode_${login_uuid}.txt"
  printf '%s\n' "$qrcode" > "$text_path"
  open_target "$text_path"
  printf '%s\n' "$text_path"
}

cmd_qrcode() {
  local game="$1" account_type="$2"
  post_json "/api/qrcode" "$(printf '{"game":"%s","account_type":"%s"}' "$game" "$account_type")"
}

cmd_poll_once() {
  local login_uuid="$1"
  get_json "/api/poll?login_uuid=${login_uuid}"
}

cmd_query() {
  local body="$1"
  post_json "/api/query" "$body"
}

wait_for_scan() {
  local login_uuid="$1"
  for _ in $(seq 1 150); do
    local resp status success message
    resp=$(cmd_poll_once "$login_uuid")
    success=$(printf '%s' "$resp" | python3 -c 'import json,sys; print(str(json.loads(sys.stdin.read()).get("success", False)).lower())' 2>/dev/null || printf false)
    status=$(printf '%s' "$resp" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("status", ""))' 2>/dev/null || true)
    if [ "$success" != "true" ]; then
      message=$(printf '%s' "$resp" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("message", "扫码轮询失败"))' 2>/dev/null || printf '扫码轮询失败')
      echo "Error: ${message}" >&2
      printf '%s\n' "$resp" >&2
      exit 1
    fi
    if [ "$status" = "success" ]; then
      printf '%s\n' "$resp"
      return
    fi
    sleep 4
  done
  echo "Error: 二维码已过期，请重新获取二维码" >&2
  exit 1
}

format_report() {
  python3 -c '
import json, sys
raw = sys.stdin.read()
try:
    resp = json.loads(raw)
except Exception:
    print(raw)
    sys.exit(0)

if not resp.get("success"):
    print(resp.get("message") or raw)
    sys.exit(1)

estimate = resp.get("estimate") or {}
extra = estimate.get("extra") if isinstance(estimate, dict) else {}
info = None
if isinstance(extra, dict):
    info = extra.get("estimate_info") or extra.get("estimateInfo")
if not isinstance(info, dict):
    print(json.dumps({k: v for k, v in resp.items() if k != "request_logs"}, ensure_ascii=False, indent=2))
    sys.exit(0)

game_names = {"delta": "三角洲行动", "hok": "王者荣耀", "pubg": "和平精英"}
game = game_names.get(resp.get("game"), "游戏账号")
predict = info.get("predict_valuation") or info.get("predictValuation") or "--"
min_v = info.get("min_valuation") or info.get("minValuation") or "--"
max_v = info.get("max_valuation") or info.get("maxValuation") or "--"
surpassed = info.get("surpassed_user") or info.get("surpassedUser") or "--"
most = info.get("most_value") or info.get("mostValue") or "--"

lines = [
    f"🎮 {game} — 账号估值报告",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━",
    f"💰 预估价格: ¥{predict}",
    f"📈 价格区间: ¥{min_v} ~ ¥{max_v}",
    f"🏆 超越用户: {surpassed}",
    f"👑 最值钱单品: {most}",
]

assets = resp.get("assets") or {}
summary = []
if isinstance(assets, dict):
    hok = assets.get("hasData") if isinstance(assets.get("hasData"), dict) else assets
    if "totalSkinNum" in hok:
        summary.append(("皮肤数量", hok.get("totalSkinNum")))
    if "owned" in hok:
        summary.append(("英雄数量", hok.get("owned")))
    pubg_role = (((assets.get("data") or {}).get("ItemsNewArr") or {}).get("roleInfo") or {}) if isinstance(assets.get("data"), dict) else {}
    for label, key in [("等级", "level"), ("段位", "roleJob"), ("热力值", "newHeat"), ("时装", "shizhuangNum"), ("枪械", "qiangxieNum"), ("载具", "zaijuNum")]:
        if key in pubg_role:
            summary.append((label, pubg_role.get(key)))
    delta_role = (((assets.get("data") or {}).get("roleInfo") or {}) if isinstance(assets.get("data"), dict) else {})
    for label, key in [("等级", "level"), ("总资产", "totalPrice"), ("哈夫币", "hafcoinnum")]:
        if key in delta_role:
            summary.append((label, delta_role.get(key)))

if summary:
    lines.append("")
    lines.append("📊 核心数据:")
    for label, value in summary[:8]:
        lines.append(f"  {label}: {value}")

lines.append("")
lines.append("🔍 详细估值: https://mall.yy.com/?pageId=20000")
print("\n".join(lines))
'
}

cmd_hok() {
  local server="$1" yingdi_id="$2" real_name_status="$3" anti_addiction="$4"
  local body
  body=$(python3 -c 'import json,sys; print(json.dumps({"game":"hok","server":sys.argv[1],"yingdi_id":sys.argv[2],"real_name_status":sys.argv[3],"anti_addiction":sys.argv[4]}, ensure_ascii=False))' "$server" "$yingdi_id" "$real_name_status" "$anti_addiction")
  cmd_query "$body" | python3 -c 'import json,sys; d=json.load(sys.stdin); d["game"]="hok"; print(json.dumps(d, ensure_ascii=False))' | format_report
}

scan_and_query() {
  local game="$1" account_type="$2" body="$3"
  local qr_resp login_uuid qrcode opened
  qr_resp=$(cmd_qrcode "$game" "$account_type")
  login_uuid=$(printf '%s' "$qr_resp" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("login_uuid", ""))')
  qrcode=$(printf '%s' "$qr_resp" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("qrcode", ""))')
  if [ -z "$login_uuid" ] || [ -z "$qrcode" ]; then
    printf '%s\n' "$qr_resp" >&2
    echo "Error: 获取二维码失败" >&2
    exit 1
  fi
  opened=$(save_and_open_qrcode "$qrcode" "$login_uuid")
  echo "二维码已打开：${opened}" >&2
  echo "请用手机扫码并确认登录，扫码成功后会自动查询估值。" >&2
  wait_for_scan "$login_uuid" >/dev/null
  local final_body
  final_body=$(python3 -c 'import json,sys; d=json.loads(sys.argv[1]); d["login_uuid"]=sys.argv[2]; print(json.dumps(d, ensure_ascii=False))' "$body" "$login_uuid")
  cmd_query "$final_body" | python3 -c 'import json,sys; d=json.load(sys.stdin); d["game"]=sys.argv[1]; print(json.dumps(d, ensure_ascii=False))' "$game" | format_report
}

cmd_delta() {
  local account_type="$1" real_name_status="$2" safety_box="$3"
  local body
  body=$(python3 -c 'import json,sys; print(json.dumps({"game":"delta","account_type":sys.argv[1],"real_name_status":sys.argv[2],"safety_box":sys.argv[3]}, ensure_ascii=False))' "$account_type" "$real_name_status" "$safety_box")
  scan_and_query delta "$account_type" "$body"
}

cmd_pubg() {
  local server="$1" real_name_status="$2" anti_addiction="$3" role_id="${4:-}"
  local account_type body
  account_type=$(account_type_from_server "$server")
  body=$(python3 -c 'import json,sys; print(json.dumps({"game":"pubg","account_type":sys.argv[1],"server":sys.argv[2],"real_name_status":sys.argv[3],"anti_addiction":sys.argv[4],"role_id":sys.argv[5]}, ensure_ascii=False))' "$account_type" "$server" "$real_name_status" "$anti_addiction" "$role_id")
  scan_and_query pubg "$account_type" "$body"
}

usage() {
  cat <<'EOF'
Usage: valuation.sh <command> [args...]

Commands:
  hok <server> <yingdi_id> <real_name_status> <anti_addiction>
      王者荣耀估值，无需扫码

  delta <account_type> <real_name_status> <safety_box>
      三角洲行动估值，自动获取二维码、轮询扫码并查询

  pubg <server> <real_name_status> <anti_addiction> [role_id]
      和平精英估值，根据 server 自动选择 QQ/微信扫码

  qrcode <game> <account_type>
      仅获取二维码 JSON，game 支持 delta/pubg，account_type: 1=QQ, 2=微信

  poll <login_uuid>
      仅轮询一次扫码状态 JSON

  query '<json_body>'
      直接调用 /api/query，输出原始 JSON

Enums:
  server: android_qq | ios_qq | android_wx | ios_wx
  account_type: 1(QQ) | 2(微信)
  real_name_status: re_auth_allowed | re_auth_denied
  anti_addiction: yes | no
  safety_box: top | advanced | intermediate | basic
EOF
}

if [ $# -lt 1 ]; then
  usage
  exit 1
fi

case "$1" in
  hok)
    [ $# -lt 5 ] && echo "Usage: valuation.sh hok <server> <yingdi_id> <real_name_status> <anti_addiction>" >&2 && exit 1
    cmd_hok "$2" "$3" "$4" "$5"
    ;;
  delta)
    [ $# -lt 4 ] && echo "Usage: valuation.sh delta <account_type> <real_name_status> <safety_box>" >&2 && exit 1
    cmd_delta "$2" "$3" "$4"
    ;;
  pubg)
    [ $# -lt 4 ] && echo "Usage: valuation.sh pubg <server> <real_name_status> <anti_addiction> [role_id]" >&2 && exit 1
    cmd_pubg "$2" "$3" "$4" "${5:-}"
    ;;
  qrcode)
    [ $# -lt 3 ] && echo "Usage: valuation.sh qrcode <game> <account_type>" >&2 && exit 1
    cmd_qrcode "$2" "$3"
    ;;
  poll)
    [ $# -lt 2 ] && echo "Usage: valuation.sh poll <login_uuid>" >&2 && exit 1
    cmd_poll_once "$2"
    ;;
  query)
    [ $# -lt 2 ] && echo "Usage: valuation.sh query '<json_body>'" >&2 && exit 1
    cmd_query "$2"
    ;;
  *) usage; exit 1 ;;
esac
