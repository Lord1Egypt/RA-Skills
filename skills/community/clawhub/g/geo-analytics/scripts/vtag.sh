#!/usr/bin/env bash
# Vtag GEO Analytics —— 设备码授权 + 只读取数的 curl 封装。
#
# 用法:
#   vtag.sh login                                   # 跑一次设备码流程,凭证存 ~/.vtag/credentials
#   vtag.sh overview from=2026-08-01 to=2026-08-20  # 取数(tag_id 自动带上,不用填)
#   vtag.sh acquisition from=… to=… dimension=engine
#   vtag.sh whoami                                  # 看当前凭证绑的是哪个站
#   vtag.sh logout                                  # 删本地凭证(注意:不等于吊销,见下)
#
# ⚠️ 这个脚本是**可选件**。不是所有 agent 平台都给 shell 执行权 —— SKILL.md 里的
#    授权三步与端点表必须能让对面用自己的 HTTP 能力直接跑通,不能只写「运行 vtag.sh」。
#
# ⚠️ logout 只删本地文件,**不吊销 token**。真要作废那把,去控制台的站点凭证面板吊销 ——
#    删掉本地副本而库里那把还有效,是「以为已经收回了」这类事故的标准开头。
set -euo pipefail

BASE="${VTAG_BASE:-https://geo-analytics.info}"
CRED="${VTAG_CRED:-$HOME/.vtag/credentials}"
CLIENT_ID="vtag-skill"

_json() {  # _json <字段名>,从 stdin 的 JSON 里取一个字符串/数字字段
  python3 -c 'import json,sys
try: print(json.load(sys.stdin).get(sys.argv[1], ""))
except Exception: print("")' "$1"
}

usage() { sed -n '2,12p' "$0" >&2; exit 1; }

cmd="${1:-}"; [ -n "$cmd" ] || usage

if [ "$cmd" = "login" ]; then
  r=$(curl -fsS -X POST "$BASE/api/oauth/device_authorization" -d "client_id=$CLIENT_ID")
  dc=$(printf '%s' "$r" | _json device_code)
  uc=$(printf '%s' "$r" | _json user_code)
  uri=$(printf '%s' "$r" | _json verification_uri)
  full=$(printf '%s' "$r" | _json verification_uri_complete)
  iv=$(printf '%s' "$r" | _json interval)
  [ -n "$dc" ] || { echo "拿不到 device_code:$r" >&2; exit 1; }
  echo "打开 $uri 并输入: $uc" >&2
  echo "(或直接点带码链接: $full)" >&2
  while :; do
    sleep "$iv"
    # 这里**不加 -f**:400 带的 error 体正是流程的一部分,-f 会把它变成 curl 报错。
    t=$(curl -sS -X POST "$BASE/api/oauth/token" \
        -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
        -d "device_code=$dc" -d "client_id=$CLIENT_ID") || continue
    case "$t" in
      *authorization_pending*) continue ;;
      *slow_down*)             iv=$((iv + 5)); continue ;;
      # access_denied / expired_token / invalid_grant 都不重试 —— 第一个是用户说了不,
      # 后两个重试也只会一直失败。静默重试会把「用户拒绝了」变成一个转圈的进度条。
      *access_denied*)         echo "用户拒绝了授权" >&2; exit 1 ;;
      *expired_token*)         echo "验证码已过期,请重新 login" >&2; exit 1 ;;
      *invalid_grant*)         echo "device_code 无效或已被领取,请重新 login" >&2; exit 1 ;;
    esac
    # ⚠️ 必须确认真拿到了 access_token 再落盘。上面的 case 只认识已知错误,
    #    未知响应(503、网关的 HTML 错误页)会掉到这里 —— 直接写进凭证文件的话,
    #    脚本会打印「已授权」,然后每次取数都 401,而用户以为自己已经授权过了。
    if [ -z "$(printf '%s' "$t" | _json access_token)" ]; then
      echo "换 token 失败,响应不是预期格式:$t" >&2; exit 1
    fi
    mkdir -p "$(dirname "$CRED")"
    # umask 077 不是装饰:这里面是一把长期有效的只读凭证。
    ( umask 077; printf '%s' "$t" > "$CRED" )
    echo "已授权,站点 $(printf '%s' "$t" | _json tag_id)" >&2
    exit 0
  done
fi

[ -f "$CRED" ] || { echo "请先运行: $(basename "$0") login" >&2; exit 1; }
tok=$(_json access_token < "$CRED")
tag=$(_json tag_id < "$CRED")
[ -n "$tok" ] && [ -n "$tag" ] || { echo "凭证文件不完整,请重新 login" >&2; exit 1; }

case "$cmd" in
  whoami) echo "$tag"; exit 0 ;;
  logout) rm -f "$CRED"; echo "已删除本地凭证(库里那把仍然有效,要作废请去控制台吊销)" >&2; exit 0 ;;
esac

ep="$cmd"; shift
q="tag_id=${tag}"; for kv in "$@"; do q="${q}&${kv}"; done
curl -fsS -H "Authorization: Bearer ${tok}" "$BASE/api/reports/${ep}?${q}"
