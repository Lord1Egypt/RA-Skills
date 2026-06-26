#!/bin/bash
# express-tracker: 快递物流查询脚本
# 依赖: curl, jq, openssl/md5sum/md5
# 用法: ./track.sh <快递单号> [快递公司编码]

set -euo pipefail

# ---- 配置 ----
API_KEY="${EXPRESS_TRACKER_KEY:-}"
CUSTOMER="${EXPRESS_TRACKER_CUSTOMER:-}"

if [[ -z "$API_KEY" || -z "$CUSTOMER" ]]; then
  echo "❌ 请设置环境变量 EXPRESS_TRACKER_KEY 和 EXPRESS_TRACKER_CUSTOMER"
  echo "   export EXPRESS_TRACKER_KEY=your_key"
  echo "   export EXPRESS_TRACKER_CUSTOMER=your_customer"
  exit 1
fi

TRACKING_NUM="${1:-}"
CARRIER_CODE="${2:-}"

if [[ -z "$TRACKING_NUM" ]]; then
  echo "❌ 用法: ./track.sh <快递单号> [快递公司编码]"
  exit 1
fi

# ---- MD5 签名函数 ----
calc_md5() {
  local input="$1"
  if command -v md5sum &>/dev/null; then
    echo -n "$input" | md5sum | awk '{print toupper($1)}'
  elif command -v md5 &>/dev/null; then
    echo -n "$input" | md5 | awk '{print toupper($0)}'
  elif command -v openssl &>/dev/null; then
    echo -n "$input" | openssl md5 -r | awk '{print toupper($1)}'
  else
    echo "❌ 需要 md5sum、md5 或 openssl" >&2
    exit 1
  fi
}

# ---- 本地智能识别快递公司 ----
guess_carrier() {
  local num="$1"
  local len=${#num}
  local prefix2="${num:0:2}"
  local prefix3="${num:0:3}"
  local prefix4="${num:0:4}"

  # 顺丰: SF开头
  if [[ "$num" =~ ^[Ss][Ff] ]]; then echo "shunfeng"; return; fi

  # 京东: JD/JDVA/JDV 开头
  if [[ "$num" =~ ^[Jj][Dd] ]]; then echo "jd"; return; fi

  # 极兔: JT 开头 或 J0 开头
  if [[ "$num" =~ ^[Jj][Tt] ]]; then echo "jitu"; return; fi
  if [[ "$num" =~ ^J0 ]]; then echo "jitu"; return; fi

  # EMS: E 开头 + 字母结尾
  if [[ "$num" =~ ^[Ee][A-Za-z][0-9]{9}[A-Za-z]{2}$ ]]; then echo "ems"; return; fi

  # 邮政国内小包: 数字开头 9/1 + 11位
  if [[ "$num" =~ ^99 && $len -ge 13 ]]; then echo "youzhengguonei"; return; fi

  # 德邦: DPK 开头 或 数字 6 开头 + 10位
  if [[ "$num" =~ ^[Dd][Pp][Kk] ]]; then echo "debangkuaidi"; return; fi
  if [[ "${num:0:1}" == "6" && $len -eq 10 ]]; then echo "debangkuaidi"; return; fi

  # 中通: 78/73/72/21/68 开头，一般 12-15 位纯数字
  if [[ "$num" =~ ^[0-9]+$ && $len -ge 12 && $len -le 15 ]]; then
    case "$prefix2" in
      78|73|72|21|68) echo "zhongtong"; return ;;
    esac
  fi

  # 圆通: YT 开头 或 V/D 开头 + 数字
  if [[ "$num" =~ ^[Yy][Tt] ]]; then echo "yuantong"; return; fi
  if [[ "$num" =~ ^[VvDd][0-9] ]]; then echo "yuantong"; return; fi

  # 韵达: 10/11/12/13/19/46 开头，一般 13 位纯数字
  if [[ "$num" =~ ^[0-9]+$ && $len -eq 13 ]]; then
    case "$prefix2" in
      10|11|12|13|19|46) echo "yunda"; return ;;
    esac
  fi

  # 申通: 77/88/66/55/44 开头，一般 13-15 位纯数字
  if [[ "$num" =~ ^[0-9]+$ && $len -ge 13 && $len -le 15 ]]; then
    case "$prefix2" in
      77|88|66|55|44) echo "shentong"; return ;;
    esac
  fi

  # 百世汇通: 7 开头 + 纯数字 + 长度 10-15
  if [[ "$num" =~ ^7[0-9]+$ && $len -ge 10 && $len -le 15 ]]; then
    echo "huitongkuaidi"; return
  fi

  # 天天快递: 66/77/88 开头 14 位
  if [[ "$num" =~ ^[0-9]+$ && $len -eq 14 ]]; then
    case "$prefix2" in
      66|77|88) echo "tiantian"; return ;;
    esac
  fi

  # 菜鸟速递: CN 开头
  if [[ "$num" =~ ^[Cc][Nn] ]]; then echo "cainiao"; return; fi

  # 跨越: KYE 开头
  if [[ "$num" =~ ^[Kk][Yy][Ee] ]]; then echo "kuayue"; return; fi

  # 安能: AN 开头
  if [[ "$num" =~ ^[Aa][Nn] ]]; then echo "annengwuliu"; return; fi

  # 宅急送: 数字开头，长度 10
  if [[ "$num" =~ ^[0-9]+$ && $len -eq 10 ]]; then echo "zhaijisong"; return; fi

  # 邮政: 100/101 开头 13位
  if [[ "$num" =~ ^10[01] && $len -eq 13 ]]; then echo "youzhengguonei"; return; fi

  # 国际: DHL
  if [[ "$num" =~ ^[0-9]{10}$ ]]; then echo "dhl"; return; fi

  # UPS: 1Z 开头
  if [[ "$num" =~ ^1[Zz] ]]; then echo "ups"; return; fi

  # FedEx: 纯数字 12/15/20/22 位
  if [[ "$num" =~ ^[0-9]+$ ]]; then
    case "$len" in
      12|15|20|22) echo "fedex"; return ;;
    esac
  fi

  echo ""
}

# 快递公司编码 → 中文名映射
carrier_name() {
  case "$1" in
    shunfeng) echo "顺丰速运" ;;
    zhongtong) echo "中通快递" ;;
    yuantong) echo "圆通速递" ;;
    yunda) echo "韵达快递" ;;
    shentong) echo "申通快递" ;;
    jitu) echo "极兔速递" ;;
    ems) echo "EMS" ;;
    jd) echo "京东快递" ;;
    debangkuaidi) echo "德邦快递" ;;
    cainiao) echo "菜鸟速递" ;;
    huitongkuaidi) echo "百世快递" ;;
    tiantian) echo "天天快递" ;;
    kuayue) echo "跨越速运" ;;
    annengwuliu) echo "安能物流" ;;
    zhaijisong) echo "宅急送" ;;
    youzhengguonei) echo "邮政快递" ;;
    dhl) echo "DHL" ;;
    ups) echo "UPS" ;;
    fedex) echo "FedEx" ;;
    *) echo "$1" ;;
  esac
}

# ---- 自动识别快递公司 ----
if [[ -z "$CARRIER_CODE" ]]; then
  echo "🔍 正在识别快递公司..."
  CARRIER_CODE=$(guess_carrier "$TRACKING_NUM")

  if [[ -z "$CARRIER_CODE" ]]; then
    echo "❌ 无法自动识别快递公司，请手动指定编码"
    echo ""
    echo "   ./track.sh ${TRACKING_NUM} <快递公司编码>"
    echo ""
    echo "   常用编码:"
    echo "     shunfeng    顺丰速运"
    echo "     zhongtong   中通快递"
    echo "     yuantong    圆通速递"
    echo "     yunda       韵达快递"
    echo "     shentong    申通快递"
    echo "     jitu        极兔速递"
    echo "     ems         EMS"
    echo "     jd          京东快递"
    echo "     debangkuaidi 德邦快递"
    echo "     cainiao     菜鸟速递"
    exit 1
  fi
  echo "✅ 识别为: $(carrier_name "$CARRIER_CODE") ($CARRIER_CODE)"
fi

# ---- 构造请求参数 ----
PARAM="{\"com\":\"${CARRIER_CODE}\",\"num\":\"${TRACKING_NUM}\",\"resultv2\":\"4\",\"order\":\"desc\"}"

# MD5 签名: param + key + customer -> 32位大写MD5
SIGN=$(calc_md5 "${PARAM}${API_KEY}${CUSTOMER}")

# ---- 发起查询 ----
echo "📦 正在查询单号: ${TRACKING_NUM}"
echo ""

RESPONSE=$(curl -s -X POST "https://poll.kuaidi100.com/poll/query.do" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "customer=${CUSTOMER}&sign=${SIGN}&param=${PARAM}")

# ---- 错误处理 ----
if echo "$RESPONSE" | jq -e '.result == false' &>/dev/null; then
  RETURN_CODE=$(echo "$RESPONSE" | jq -r '.returnCode // "unknown"')
  case "$RETURN_CODE" in
    400) echo "❌ 错误: 提交数据不完整或快递公司编码错误" ;;
    408) echo "❌ 错误: 电话号码校验不通过（顺丰/中通需要填写手机号）" ;;
    500) echo "❌ 错误: 未查到物流信息，请确认单号和快递公司是否正确" ;;
    503) echo "❌ 错误: 签名验证失败" ;;
    601) echo "❌ 错误: API Key 已过期或余额不足" ;;
    *)   echo "❌ 错误 (${RETURN_CODE}): $(echo "$RESPONSE" | jq -r '.message // "未知错误"')" ;;
  esac
  exit 1
fi

# ---- 解析物流状态 ----
STATE=$(echo "$RESPONSE" | jq -r '.state // "0"')
COM=$(echo "$RESPONSE" | jq -r '.com // "unknown"')
NU=$(echo "$RESPONSE" | jq -r '.nu // "unknown"')

# 状态映射（支持高级状态码）
case "$STATE" in
  0)    STATE_TEXT="🚚 在途" ;;
  1)    STATE_TEXT="📬 揽收" ;;
  101)  STATE_TEXT="📝 已下单" ;;
  102)  STATE_TEXT="⏳ 待揽收" ;;
  103)  STATE_TEXT="📬 已揽收" ;;
  1001) STATE_TEXT="🚚 到达派件城市" ;;
  1002) STATE_TEXT="🚚 干线运输中" ;;
  1003) STATE_TEXT="🔄 转递" ;;
  2)    STATE_TEXT="⚠️ 疑难" ;;
  201)  STATE_TEXT="⚠️ 超时未签收" ;;
  202)  STATE_TEXT="⚠️ 超时未更新" ;;
  203)  STATE_TEXT="🚫 拒收" ;;
  204)  STATE_TEXT="⚠️ 派件异常" ;;
  205)  STATE_TEXT="⚠️ 柜/驿站超时未取" ;;
  206)  STATE_TEXT="⚠️ 无法联系" ;;
  207)  STATE_TEXT="⚠️ 超区" ;;
  208)  STATE_TEXT="⚠️ 滞留" ;;
  209)  STATE_TEXT="⚠️ 破损" ;;
  210)  STATE_TEXT="📝 销单" ;;
  3)    STATE_TEXT="✅ 已签收" ;;
  301)  STATE_TEXT="✅ 本人签收" ;;
  302)  STATE_TEXT="✅ 派件异常后签收" ;;
  303)  STATE_TEXT="✅ 代签" ;;
  304)  STATE_TEXT="✅ 快递柜/驿站签收" ;;
  4)    STATE_TEXT="↩️ 退签" ;;
  401)  STATE_TEXT="📝 已销单" ;;
  5)    STATE_TEXT="🏃 派件中" ;;
  501)  STATE_TEXT="📦 已投柜/驿站" ;;
  6)    STATE_TEXT="↩️ 退回" ;;
  7)    STATE_TEXT="🔄 转投" ;;
  8)    STATE_TEXT="🛃 清关中" ;;
  10)   STATE_TEXT="⏳ 待清关" ;;
  11)   STATE_TEXT="🛃 清关中" ;;
  12)   STATE_TEXT="✅ 已清关" ;;
  13)   STATE_TEXT="⚠️ 清关异常" ;;
  14)   STATE_TEXT="❌ 拒签" ;;
  *)    STATE_TEXT="❓ 状态码:${STATE}" ;;
esac

# 路由信息
FROM_CITY=$(echo "$RESPONSE" | jq -r '.routeInfo.from.name // empty')
TO_CITY=$(echo "$RESPONSE" | jq -r '.routeInfo.to.name // empty')
CUR_CITY=$(echo "$RESPONSE" | jq -r '.routeInfo.cur.name // empty')

# ---- 输出 ----
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 快递单号: ${NU}"
echo "🏢 快递公司: $(carrier_name "$COM")"
echo "📊 当前状态: ${STATE_TEXT}"
[[ -n "$FROM_CITY" ]] && echo "📍 出发地:   ${FROM_CITY}"
[[ -n "$TO_CITY" ]]   && echo "📍 目的地:   ${TO_CITY}"
[[ -n "$CUR_CITY" ]]  && echo "📍 当前位置: ${CUR_CITY}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 物流轨迹（最新在前）:"
echo ""

# 输出全部物流轨迹（倒序，最新在前）
DATA_COUNT=$(echo "$RESPONSE" | jq '.data | length')

if [[ "$DATA_COUNT" == "0" || "$DATA_COUNT" == "null" ]]; then
  echo "  暂无物流轨迹信息"
else
  INDEX=0
  echo "$RESPONSE" | jq -r '.data[] | "\(.ftime)|\(.status // "")|\(.context)"' | while IFS='|' read -r ftime status context; do
    INDEX=$((INDEX + 1))
    echo "  ${INDEX}. 【${ftime}】${status}"
    echo "     └ ${context}"
    echo ""
  done
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  查询时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
