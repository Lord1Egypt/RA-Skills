#!/usr/bin/env bash
# air_chart.sh — air-chart main entry
# Natural-language query -> OpenAQ station pick -> data cleaning -> SVG chart
#
# Usage:
#   air_chart.sh --city Beijing --param pm25 --period 7d
#   air_chart.sh --city Tokyo --city Seoul --param pm25 --period 7d     # multi-city compare
#   air_chart.sh --city Beijing --param pm25 --param pm10 --period 48h  # multi-parameter
#   air_chart.sh --city Delhi --param pm10 --snapshot                   # station snapshot
#   air_chart.sh --city Beijing --param pm25 --period 7d --demo         # demo data (no API key)
# Options: --city/-c --param/-p --period/-t --snapshot --theme --lang en|zh|es|hi|ja|ko|fr --demo
# Output: 默认打印 x-cmd Draw 图表 URL; --out/-o file.svg|file.png 下载落盘
# Language: auto-detected from system locale (zh -> Chinese), override with --lang.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./openaq_client.sh
source "$SCRIPT_DIR/openaq_client.sh"

# ---------- 参数默认值 ----------
CITIES=(); PARAMS=("pm25"); PERIOD="7d"; SNAPSHOT=0; THEME="light"; STYLE="opendata"; OUT=""; DEMO=0
LANG_OPT=""

usage() { sed -n '2,15p' "${BASH_SOURCE[0]}"; }

while (( $# )); do
  case "$1" in
    -c|--city) CITIES+=("$2"); shift 2 ;;
    -p|--param) PARAMS+=("$2"); shift 2 ;;
    -t|--period) PERIOD="$2"; shift 2 ;;
    --snapshot) SNAPSHOT=1; shift ;;
    --theme) THEME="$2"; shift 2 ;;
    --style) STYLE="$2"; shift 2 ;;
    --lang) LANG_OPT="$2"; shift 2 ;;
    -o|--out) OUT="$2"; shift 2 ;;
    --demo) DEMO=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf '[air-chart] ERROR: 未知参数 %s\n' "$1" >&2; usage >&2; exit 1 ;;
  esac
done

# ---------- 语言 (默认按系统 locale 自动检测, --lang 覆盖) ----------
detect_lang() {
  local l="${LANG_OPT:-${LC_ALL:-${LC_MESSAGES:-${LANG:-}}}}"
  l="${l%%.*}"; l="${l%%@*}"
  case "${l,,}" in
    zh*) printf 'zh' ;; es*) printf 'es' ;; hi*) printf 'hi' ;;
    ja*) printf 'ja' ;; ko*) printf 'ko' ;; fr*) printf 'fr' ;;
    *) printf 'en' ;;
  esac
}
AIR_CHART_LANG="$(detect_lang)"
export AIR_CHART_LANG

# 文案表 (key: en/zh/es/hi/ja/ko/fr, 缺失键回退英文)
declare -A T_EN T_ZH T_ES T_HI T_JA T_KO T_FR
T_EN[err_no_city]="Please specify at least one city via --city."
T_ZH[err_no_city]="请至少通过 --city 指定一个城市。"
T_ES[err_no_city]="Especifica al menos una ciudad con --city."
T_HI[err_no_city]="कम से कम एक शहर --city से निर्दिष्ट करें।"
T_JA[err_no_city]="--city で都市を 1 つ以上指定してください。"
T_KO[err_no_city]="--city 로 도시를 하나 이상 지정하세요."
T_FR[err_no_city]="Spécifiez au moins une ville via --city."
T_EN[err_too_many_cities]="Multi-city comparison supports at most 4 cities."
T_ZH[err_too_many_cities]="多城对比最多支持 4 个城市。"
T_ES[err_too_many_cities]="La comparación multiciudad admite como máximo 4 ciudades."
T_HI[err_too_many_cities]="बहु-शहर तुलना में अधिकतम 4 शहर समर्थित हैं।"
T_JA[err_too_many_cities]="複数都市の比較は最大 4 都市までです。"
T_KO[err_too_many_cities]="도시 간 비교는 최대 4개까지 지원합니다."
T_FR[err_too_many_cities]="La comparaison multi-villes accepte au maximum 4 villes."
T_EN[err_bad_param]='Unsupported parameter "%s" (choose from: %s).'
T_ZH[err_bad_param]='不支持的指标 "%s" (可选: %s)。'
T_ES[err_bad_param]='Parámetro no soportado "%s" (elige entre: %s).'
T_HI[err_bad_param]='असमर्थित पैरामीटर "%s" (चुनें: %s)।'
T_JA[err_bad_param]='未対応のパラメータ "%s" (選択肢: %s)。'
T_KO[err_bad_param]='지원하지 않는 매개변수 "%s" (선택: %s).'
T_FR[err_bad_param]='Paramètre non pris en charge « %s » (choix : %s).'
T_EN[err_multi_param]="Multi-city comparison supports only one --param."
T_ZH[err_multi_param]="多城对比模式仅支持单指标, 请只传一个 --param。"
T_ES[err_multi_param]="La comparación multiciudad admite un solo --param."
T_HI[err_multi_param]="बहु-शहर तुलना में केवल एक --param समर्थित है।"
T_JA[err_multi_param]="複数都市の比較では --param は 1 つのみ指定できます。"
T_KO[err_multi_param]="도시 간 비교에서는 --param 하나만 지정할 수 있습니다."
T_FR[err_multi_param]="La comparaison multi-villes n'accepte qu'un seul --param."
T_EN[err_bad_period]='Unsupported period "%s" (choose from: 24h 48h 7d 14d 30d).'
T_ZH[err_bad_period]='不支持的时间跨度 "%s" (可选: 24h 48h 7d 14d 30d)。'
T_ES[err_bad_period]='Rango no soportado "%s" (elige entre: 24h 48h 7d 14d 30d).'
T_HI[err_bad_period]='असमर्थित अवधि "%s" (चुनें: 24h 48h 7d 14d 30d)।'
T_JA[err_bad_period]='未対応の期間 "%s" (選択肢: 24h 48h 7d 14d 30d)。'
T_KO[err_bad_period]='지원하지 않는 기간 "%s" (선택: 24h 48h 7d 14d 30d).'
T_FR[err_bad_period]='Période non prise en charge « %s » (choix : 24h 48h 7d 14d 30d).'
T_EN[err_no_series]="Nothing to plot. Check the city/parameter/period, or use --demo to preview."
T_ZH[err_no_series]="没有任何序列可绘制。请检查城市名/指标/时间范围, 或使用 --demo 预览效果。"
T_ES[err_no_series]="Nada que graficar. Revisa ciudad/parámetro/periodo, o usa --demo para previsualizar."
T_HI[err_no_series]="बनाने के लिए कुछ नहीं। शहर/पैरामीटर/अवधि जांचें, या झलक के लिए --demo उपयोग करें।"
T_JA[err_no_series]="描画するデータがありません。都市/パラメータ/期間を確認するか、--demo でプレビューしてください。"
T_KO[err_no_series]="그릴 데이터가 없습니다. 도시/매개변수/기간을 확인하거나 --demo 로 미리 보세요."
T_FR[err_no_series]="Rien à tracer. Vérifiez ville/paramètre/période, ou utilisez --demo pour un aperçu."
T_EN[warn_no_active]="WARN: no active monitoring station within 25km of %s (no update in 24-72h)."
T_ZH[warn_no_active]="WARN: %s 附近 25km 内没有活性监测站点 (24-72h 内无数据更新)。"
T_ES[warn_no_active]="AVISO: ninguna estación activa en un radio de 25 km de %s (sin datos en 24-72 h)."
T_HI[warn_no_active]="चेतावनी: %s के 25 किमी दायरे में कोई सक्रिय स्टेशन नहीं (24-72 घंटे में कोई डेटा नहीं)।"
T_JA[warn_no_active]="警告: %s の半径 25 km 内に稼働中の測定局がありません (24〜72 時間データなし)。"
T_KO[warn_no_active]="경고: %s 반경 25km 내에 활성 관측소가 없습니다 (24-72시간 데이터 없음)."
T_FR[warn_no_active]="AVERTISSEMENT : aucune station active dans un rayon de 25 km de %s (aucune donnée depuis 24-72 h)."
T_EN[warn_no_sensor]="WARN: active stations of %s have no %s sensor data, skipped."
T_ZH[warn_no_sensor]="WARN: %s 的活性站点中暂无 %s 传感器数据, 已跳过。"
T_ES[warn_no_sensor]="AVISO: las estaciones activas de %s no tienen datos del sensor %s; omitida."
T_HI[warn_no_sensor]="चेतावनी: %s के सक्रिय स्टेशनों में %s सेंसर डेटा नहीं, छोड़ा गया।"
T_JA[warn_no_sensor]="警告: %s の稼働局中に %s センサーデータがないためスキップしました。"
T_KO[warn_no_sensor]="경고: %s 의 활성 관측소에 %s 센서 데이터가 없어 건너뜁니다."
T_FR[warn_no_sensor]="AVERTISSEMENT : les stations actives de %s n'ont pas de données %s, ignoré."
T_EN[warn_no_data]="WARN: no valid data points for %s %s in the selected period."
T_ZH[warn_no_data]="WARN: %s %s 在时间范围内无有效数据点。"
T_ES[warn_no_data]="AVISO: sin puntos válidos para %s %s en el periodo seleccionado."
T_HI[warn_no_data]="चेतावनी: चुनी गई अवधि में %s %s के लिए कोई वैध डेटा बिंदु नहीं।"
T_JA[warn_no_data]="警告: 選択期間内に %s %s の有効なデータポイントがありません。"
T_KO[warn_no_data]="경고: 선택한 기간에 %s %s 의 유효 데이터 포인트가 없습니다."
T_FR[warn_no_data]="AVERTISSEMENT : aucun point valide pour %s %s sur la période choisie."
T_EN[warn_no_snapshot]="WARN: no active %s stations near %s for snapshot."
T_ZH[warn_no_snapshot]="WARN: %s 附近没有可用于快照的活性 %s 站点。"
T_ES[warn_no_snapshot]="AVISO: no hay estaciones activas de %s cerca de %s para la instantánea."
T_HI[warn_no_snapshot]="चेतावनी: स्नैपशॉट के लिए %s के पास कोई सक्रिय %s स्टेशन नहीं।"
T_JA[warn_no_snapshot]="警告: スナップショット用に %s 近くの稼働中 %s 測定局がありません。"
T_KO[warn_no_snapshot]="경고: %s 근처에 스냅샷용 활성 %s 관측소가 없습니다."
T_FR[warn_no_snapshot]="AVERTISSEMENT : aucune station %s active près de %s pour l'instantané."
T_EN[warn_no_latest]="WARN: latest data unavailable for all stations."
T_ZH[warn_no_latest]="WARN: 站点最新数据均不可用。"
T_ES[warn_no_latest]="AVISO: datos más recientes no disponibles en ninguna estación."
T_HI[warn_no_latest]="चेतावनी: सभी स्टेशनों का ताजा डेटा उपलब्ध नहीं।"
T_JA[warn_no_latest]="警告: すべての測定局で最新データを取得できません。"
T_KO[warn_no_latest]="경고: 모든 관측소의 최신 데이터를 사용할 수 없습니다."
T_FR[warn_no_latest]="AVERTISSEMENT : données les plus récentes indisponibles pour toutes les stations."
T_EN[note_who_skipped]="NOTE: sensor units differ from the dictionary default; WHO guideline line skipped to avoid dimensional confusion."
T_ZH[note_who_skipped]="NOTE: 站点传感器单位与默认单位不一致, 已跳过 WHO 基准线以避免量纲误导。"
T_ES[note_who_skipped]="NOTA: las unidades del sensor difieren del valor por defecto; se omite la línea guía de la OMS para evitar confusiones de magnitud."
T_HI[note_who_skipped]="नोट: सेंसर इकाइयाँ डिफ़ॉल्ट से भिन्न हैं; मात्रा की भ्रांति से बचने के लिए WHO मार्गदर्शन रेखा छोड़ी गई।"
T_JA[note_who_skipped]="注: センサーの単位が既定値と異なるため、量綱の混乱を避ける WHO ガイドライン線は省略されました。"
T_KO[note_who_skipped]="참고: 센서 단위가 기본값과 달라 차원 오류를 피하기 위해 WHO 기준선을 생략했습니다."
T_FR[note_who_skipped]="NOTE : les unités du capteur diffèrent du réglage par défaut ; la ligne de référence OMS est omise pour éviter toute confusion dimensionnelle."
T_EN[demo_note]="demo mode (real API not called)"
T_ZH[demo_note]="演示数据模式 (未请求真实 API)"
T_ES[demo_note]="modo demo (API real no consultada)"
T_HI[demo_note]="डेमो मोड (वास्तविक API कॉल नहीं)"
T_JA[demo_note]="デモモード (実 API は呼び出しません)"
T_KO[demo_note]="데모 모드 (실제 API 미호출)"
T_FR[demo_note]="mode démo (API réelle non appelée)"
T_EN[ref_grade]="(reference-grade)"
T_ZH[ref_grade]="(参考级)"
T_ES[ref_grade]="(de referencia)"
T_HI[ref_grade]="(संदर्भ-श्रेणी)"
T_JA[ref_grade]="(リファレンス級)"
T_KO[ref_grade]="(국가표준측정소급)"
T_FR[ref_grade]="(de référence)"
T_EN[summary]="Data summary:"
T_ZH[summary]="数据摘要:"
T_ES[summary]="Resumen de datos:"
T_HI[summary]="डेटा सारांश:"
T_JA[summary]="データ要約:"
T_KO[summary]="데이터 요약:"
T_FR[summary]="Résumé des données :"
T_EN[chart_saved]="Chart URL (data-in-URL, rendered by x-cmd Draw):"
T_ZH[chart_saved]="图表链接 (URL 即数据, 由 x-cmd Draw 渲染):"
T_ES[chart_saved]="URL del gráfico (los datos van en la URL, renderizado por x-cmd Draw):"
T_HI[chart_saved]="चार्ट URL (डेटा URL में, x-cmd Draw द्वारा रेंडर):"
T_JA[chart_saved]="チャート URL (データは URL 内、x-cmd Draw レンダリング):"
T_KO[chart_saved]="차트 URL (데이터가 URL에, x-cmd Draw 렌더링):"
T_FR[chart_saved]="URL du graphique (données dans l'URL, rendu par x-cmd Draw) :"
T_EN[snapshot_saved]="Snapshot URL (rendered by x-cmd Draw):"
T_ZH[snapshot_saved]="快照链接 (由 x-cmd Draw 渲染):"
T_ES[snapshot_saved]="URL de la instantánea (renderizada por x-cmd Draw):"
T_HI[snapshot_saved]="स्नैपशॉट URL (x-cmd Draw द्वारा रेंडर):"
T_JA[snapshot_saved]="スナップショット URL (x-cmd Draw レンダリング):"
T_KO[snapshot_saved]="스냅샷 URL (x-cmd Draw 렌더링):"
T_FR[snapshot_saved]="URL de l'instantané (rendue par x-cmd Draw) :"
T_EN[station]="Station"
T_ZH[station]="站点"
T_ES[station]="Estación"
T_HI[station]="स्टेशन"
T_JA[station]="測定局"
T_KO[station]="관측소"
T_FR[station]="Station"
T_EN[latest]="latest"
T_ZH[latest]="最新"
T_ES[latest]="más reciente"
T_HI[latest]="ताज़ा"
T_JA[latest]="最新"
T_KO[latest]="최신"
T_FR[latest]="dernier"
T_EN[title_compare]="%s comparison · last %s"
T_ZH[title_compare]="%s 走势对比 · 最近 %s"
T_ES[title_compare]="Comparación de %s · últimos %s"
T_HI[title_compare]="%s तुलना · पिछले %s"
T_JA[title_compare]="%s 比較 · 過去 %s"
T_KO[title_compare]="%s 비교 · 최근 %s"
T_FR[title_compare]="Comparaison %s · derniers %s"
T_EN[sub_compare]="multi-city · same parameter"
T_ZH[sub_compare]="多城市同指标对比"
T_ES[sub_compare]="multiciudad · mismo parámetro"
T_HI[sub_compare]="बहु-शहर · समान पैरामीटर"
T_JA[sub_compare]="複数都市 · 同一パラメータ"
T_KO[sub_compare]="다중도시 · 동일 매개변수"
T_FR[sub_compare]="multi-villes · même paramètre"
T_EN[title_single]="%s %s trend · last %s"
T_ZH[title_single]="%s %s 趋势 · 最近 %s"
T_ES[title_single]="Tendencia de %s %s · últimos %s"
T_HI[title_single]="%s %s रुझान · पिछले %s"
T_JA[title_single]="%s %s の推移 · 過去 %s"
T_KO[title_single]="%s %s 추이 · 최근 %s"
T_FR[title_single]="Tendance %s %s · derniers %s"
T_EN[sub_multi_param]="multi-parameter"
T_ZH[sub_multi_param]="单城市多指标对比"
T_ES[sub_multi_param]="multiparámetro"
T_HI[sub_multi_param]="बहु-पैरामीटर"
T_JA[sub_multi_param]="複数パラメータ"
T_KO[sub_multi_param]="다중매개변수"
T_FR[sub_multi_param]="multi-paramètres"
T_EN[sub_single]="local time (%s)"
T_ZH[sub_single]="站点当地时间 (%s)"
T_ES[sub_single]="hora local (%s)"
T_HI[sub_single]="स्थानीय समय (%s)"
T_JA[sub_single]="現地時間 (%s)"
T_KO[sub_single]="현지 시각 (%s)"
T_FR[sub_single]="heure locale (%s)"
T_EN[ylabel_multi]="Concentration (%s)"
T_ZH[ylabel_multi]="浓度 (%s)"
T_ES[ylabel_multi]="Concentración (%s)"
T_HI[ylabel_multi]="सान्द्रता (%s)"
T_JA[ylabel_multi]="濃度 (%s)"
T_KO[ylabel_multi]="농도 (%s)"
T_FR[ylabel_multi]="Concentration (%s)"
T_EN[title_snapshot]="%s %s snapshot by station"
T_ZH[title_snapshot]="%s 各站点 %s 实时快照"
T_ES[title_snapshot]="Instantánea de %s por estación · %s"
T_HI[title_snapshot]="%s स्टेशन-वार स्नैपशॉट · %s"
T_JA[title_snapshot]="%s 測定局別スナップショット · %s"
T_KO[title_snapshot]="%s 관측소별 스냅샷 · %s"
T_FR[title_snapshot]="Instantané %s par station · %s"
T_EN[sub_snapshot]="%s · 25km radius"
T_ZH[sub_snapshot]="%s · 25km 半径"
T_ES[sub_snapshot]="%s · radio de 25 km"
T_HI[sub_snapshot]="%s · 25 किमी त्रिज्या"
T_JA[sub_snapshot]="%s · 半径 25 km"
T_KO[sub_snapshot]="%s · 반경 25km"
T_FR[sub_snapshot]="%s · rayon de 25 km"
T_EN[demo_tag]=" (demo)"
T_ZH[demo_tag]=" (演示)"
T_ES[demo_tag]=" (demo)"
T_HI[demo_tag]=" (डेमो)"
T_JA[demo_tag]=" (デモ)"
T_KO[demo_tag]=" (데모)"
T_FR[demo_tag]=" (démo)"
T_EN[demo_mode_tag]=" · demo mode"
T_ZH[demo_mode_tag]=" · 演示模式"
T_ES[demo_mode_tag]=" · modo demo"
T_HI[demo_mode_tag]=" · डेमो मोड"
T_JA[demo_mode_tag]=" · デモモード"
T_KO[demo_mode_tag]=" · 데모 모드"
T_FR[demo_mode_tag]=" · mode démo"
T_EN[sub_snapshot_demo]="demo · 25km radius"
T_ZH[sub_snapshot_demo]="演示 · 25km 半径"
T_ES[sub_snapshot_demo]="demo · radio de 25 km"
T_HI[sub_snapshot_demo]="डेमो · 25 किमी त्रिज्या"
T_JA[sub_snapshot_demo]="デモ · 半径 25 km"
T_KO[sub_snapshot_demo]="데모 · 반경 25km"
T_FR[sub_snapshot_demo]="démo · rayon de 25 km"
T_EN[who_label]="WHO 24h"
T_ZH[who_label]="WHO 24h"
T_ES[who_label]="OMS 24h"
T_HI[who_label]="WHO 24h"
T_JA[who_label]="WHO 24時間"
T_KO[who_label]="WHO 24시간"
T_FR[who_label]="OMS 24h"

t() { # t <key> — 取当前语言文案 (回退英文)
  local -n _tref="T_${AIR_CHART_LANG^^}"
  printf '%s' "${_tref[$1]:-${T_EN[$1]}}"
}

VALID_PARAMS="$(param_slugs)"
# 从 data/parameters.tsv 静态字典加载指标元数据 (列: 3名称 4单位 5WHO基准 6上限 7色 8深色色)
declare -A WHO_BASELINE PARAM_LABEL PARAM_UNITS PARAM_CAP PARAM_COLOR PARAM_COLOR_DARK
while IFS=$'\t' read -r slug pid pname punits pwho pcap pcolor pcolord; do
  [[ "$slug" == \#* || -z "$slug" ]] && continue
  WHO_BASELINE[$slug]="$pwho"; PARAM_LABEL[$slug]="$pname"; PARAM_UNITS[$slug]="$punits"
  PARAM_CAP[$slug]="$pcap"; PARAM_COLOR[$slug]="$pcolor"; PARAM_COLOR_DARK[$slug]="$pcolord"
done < "$PARAMS_TSV"

# 默认参数修正: --param 显式传入时去掉默认值
if (( ${#PARAMS[@]} > 1 )) && [[ "${PARAMS[0]}" == "pm25" ]]; then PARAMS=("${PARAMS[@]:1}"); fi
[[ ${#CITIES[@]} -eq 0 ]] && { printf '[air-chart] ERROR: %s\n' "$(t err_no_city)" >&2; exit 1; }
[[ ${#CITIES[@]} -gt 4 ]] && { printf '[air-chart] ERROR: %s\n' "$(t err_too_many_cities)" >&2; exit 1; }
for p in "${PARAMS[@]}"; do
  [[ " $VALID_PARAMS " == *" $p "* ]] || { printf '[air-chart] ERROR: '"$(t err_bad_param)"'\n' "$p" "$VALID_PARAMS" >&2; exit 1; }
done
if (( ${#CITIES[@]} > 1 && ${#PARAMS[@]} > 1 )); then
  printf '[air-chart] ERROR: %s\n' "$(t err_multi_param)" >&2; exit 1
fi

case "$PERIOD" in
  24h) GRAN="hours"; HOURS=24 ;;
  48h) GRAN="hours"; HOURS=48 ;;
  7d)  GRAN="days";  HOURS=$((7 * 24)) ;;
  14d) GRAN="days";  HOURS=$((14 * 24)) ;;
  30d) GRAN="days";  HOURS=$((30 * 24)) ;;
  *) printf '[air-chart] ERROR: '"$(t err_bad_period)"'\n' "$PERIOD" >&2; exit 1 ;;
esac

# 默认输出 x-cmd Draw URL (--out 指定 .svg/.png 时才下载落盘)
DATE_FROM="$(date -u -d "-$((HOURS + 6)) hours" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-"$((HOURS + 6))"H +%Y-%m-%dT%H:%M:%SZ)"
DATE_TO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

# ---------- 演示数据生成 ----------
demo_series() { # <city> <param> <gran> <n> -> 生成 label\tvalue 到 stdout
  local city="$1" param="$2" gran="$3" n="$4" seed
  seed=$(( $(printf '%s' "$city$param" | cksum | awk '{print $1}') % 1000 ))
  # 用城市时区生成当地时间标签
  local tz; tz="$(cut -f5 <<<"$GEO_LINE")"
  awk -v seed="$seed" -v n="$n" -v gran="$gran" -v base="$(date +%s)" -v step="$([[ "$gran" == hours ]] && echo 3600 || echo 86400)" -v tz="$tz" '
  BEGIN {
    amp = (gran == "hours") ? 8 : 20
    mid = (gran == "hours") ? 25 : 45
    for (i = n - 1; i >= 0; i--) {
      ts = base - i * step
      cmd = "TZ=" tz " date -d @" ts " \"+%m-%d" ((gran == "hours") ? " %H:00" : "") "\""
      cmd | getline l; close(cmd)
      x = n - 1 - i
      v = mid + amp * sin((x + seed % 24) / (gran == "hours" ? 3.8 : 2.2)) + amp * 0.35 * sin(x / 1.7 + seed)
      if (v < 0.5) v = 0.5
      printf "%s\t%.1f\n", l, v
    }
  }'
}

# ---------- 主流程 ----------
declare -a RENDER_SPECS=() CITY_NOTES=() SERIES_PARAMS=() SERIES_UNITS=()
FIRST_UNITS=""; FIRST_TZ=""; GLOBAL_MAX=""

fetch_city_series() { # <city> -> 为每个 param 生成 series 文件, 输出到 RENDER_SPECS
  local city="$1"
  GEO_LINE="$("$SCRIPT_DIR/geo_resolve.sh" "$city")" || exit $?
  local lat lon tz
  lat="$(cut -f3 <<<"$GEO_LINE")"; lon="$(cut -f4 <<<"$GEO_LINE")"; tz="$(cut -f5 <<<"$GEO_LINE")"
  local geo_name; geo_name="$(cut -f1 <<<"$GEO_LINE")"
  [[ -z "${FIRST_GEO_NAME:-}" ]] && FIRST_GEO_NAME="$geo_name"

  local locations
  locations="$(openaq_find_locations "$lat" "$lon" 25000)"
  local active
  active="$(openaq_filter_active "$locations" 24)"
  if [[ "$(jq '(.results // []) | length' <<<"$active")" == "0" ]]; then
    # 24h 无活性站点, 放宽到 72h 再试一次
    active="$(openaq_filter_active "$locations" 72)"
  fi
  if [[ "$(jq '(.results // []) | length' <<<"$active")" == "0" ]]; then
    printf '[air-chart] '"$(t warn_no_active)"'\n' "$city" >&2
    return 1
  fi

  for param in "${PARAMS[@]}"; do
    local picked
    picked="$(openaq_pick_sensor "$active" "$param")"
    if [[ -z "$picked" ]]; then
      printf '[air-chart] '"$(t warn_no_sensor)"'\n' "$city" "${PARAM_LABEL[$param]}" >&2
      continue
    fi
    local sensor_id units stz sname monitor
    sensor_id="$(cut -f1 <<<"$picked")"; units="$(cut -f2 <<<"$picked")"
    stz="$(cut -f3 <<<"$picked")"; sname="$(cut -f4 <<<"$picked")"; monitor="$(cut -f5 <<<"$picked")"
    [[ -z "$units" || "$units" == "null" ]] && units="${PARAM_UNITS[$param]}"
    [[ -z "$FIRST_UNITS" ]] && { FIRST_UNITS="$units"; FIRST_TZ="$stz"; }

    local raw clean
    raw="$(openaq_fetch_series "$sensor_id" "$GRAN" "$DATE_FROM" "$DATE_TO")"
    clean="$WORK/${geo_name}.${param}.tsv"
    awk -v gran="$GRAN" -v cap="${PARAM_CAP[$param]}" -v stats="$WORK/${geo_name}.${param}.stats" \
        -f "$SCRIPT_DIR/data_transform.awk" <<<"$raw" > "$clean"
    if [[ ! -s "$clean" ]]; then
      printf '[air-chart] '"$(t warn_no_data)"'\n' "$city" "${PARAM_LABEL[$param]}" >&2
      continue
    fi
    RENDER_SPECS+=("${geo_name} ${PARAM_LABEL[$param]}:${clean}")
    SERIES_PARAMS+=("$param"); SERIES_UNITS+=("$units")
    local st_min st_max st_avg st_cnt
    st_cnt="$(awk -F'\t' '$1=="count"{print $2}' "$WORK/${geo_name}.${param}.stats")"
    st_min="$(awk -F'\t' '$1=="min"{print $2}' "$WORK/${geo_name}.${param}.stats")"
    st_max="$(awk -F'\t' '$1=="max"{print $2}' "$WORK/${geo_name}.${param}.stats")"
    st_avg="$(awk -F'\t' '$1=="avg"{print $2}' "$WORK/${geo_name}.${param}.stats")"
    if [[ -n "$st_max" && ( -z "$GLOBAL_MAX" || "$(awk -v a="$GLOBAL_MAX" -v b="$st_max" 'BEGIN{print (b>a)?1:0}')" == "1" ) ]]; then GLOBAL_MAX="$st_max"; fi
    CITY_NOTES+=("  - ${geo_name} · ${PARAM_LABEL[$param]} · $(t station): ${sname}$( [[ "$monitor" == "true" ]] && echo " $(t ref_grade)") · n=${st_cnt} min=${st_min} max=${st_max} avg=$(printf '%.1f' "$st_avg") ${units}")
  done
}

fetch_city_snapshot() { # <city> <param> -> 渲染柱状图所需 items
  local city="$1" param="$2"
  GEO_LINE="$("$SCRIPT_DIR/geo_resolve.sh" "$city")" || exit $?
  local lat lon tz geo_name
  lat="$(cut -f3 <<<"$GEO_LINE")"; lon="$(cut -f4 <<<"$GEO_LINE")"; tz="$(cut -f5 <<<"$GEO_LINE")"
  geo_name="$(cut -f1 <<<"$GEO_LINE")"

  local locations active
  locations="$(openaq_find_locations "$lat" "$lon" 25000)"
  active="$(openaq_filter_active "$locations" 24)"
  [[ "$(jq '(.results // []) | length' <<<"$active")" == "0" ]] && active="$(openaq_filter_active "$locations" 72)"
  local sensors
  sensors="$(openaq_pick_all_sensors "$active" "$param" | head -6)"
  if [[ -z "$sensors" ]]; then
    printf '[air-chart] '"$(t warn_no_snapshot)"'\n' "$city" "${PARAM_LABEL[$param]}" >&2
    return 1
  fi
  local items=() units=""
  while IFS=$'\t' read -r sensor_id u s_tz s_name monitor; do
    [[ -z "$sensor_id" ]] && continue
    local latest v utc_ts
    latest="$(openaq_fetch_latest "$sensor_id")"
    [[ -z "$latest" ]] && continue
    v="$(cut -f3 <<<"$latest")"; utc_ts="$(cut -f1 <<<"$latest")"
    [[ -z "$units" ]] && units="$u"
    s_short="${s_name%%,*}"   # 站名含逗号会破坏 hbar 解析, 取逗号前短名
    items+=("${s_short}:${v}")
    CITY_NOTES+=("  - ${s_name}$( [[ "$monitor" == "true" ]] && echo " $(t ref_grade)") · $(t latest): ${v} ${u} @ ${utc_ts} UTC")
  done <<<"$sensors"
  [[ ${#items[@]} -eq 0 ]] && { printf '[air-chart] %s\n' "$(t warn_no_latest)" >&2; return 1; }
  [[ -z "$units" || "$units" == "null" ]] && units="${PARAM_UNITS[$param]}"
  FIRST_UNITS="$units"
  url="$("$SCRIPT_DIR/render_draw.sh" bar \
    --title "$(printf "$(t title_snapshot)" "$geo_name" "${PARAM_LABEL[$param]}")" \
    --subtitle "$(printf "$(t sub_snapshot)" "$(TZ="$tz" date '+%Y-%m-%d %H:%M %Z')")" \
    --unit "$units" \
    --items "${items[@]}" \
    --theme "$THEME" --style "$STYLE" ${OUT:+--out "$OUT"})"
  SNAPSHOT_URL="$url"
}

# ---------- 执行 ----------
if (( ! DEMO )); then
  openaq_require_key
fi

if (( SNAPSHOT )); then
  snap_param="${PARAMS[0]}"
  snap_units="${PARAM_UNITS[$snap_param]}"
  if (( DEMO )); then
    # 演示快照
    demo_city="${CITIES[0]}"
    if [[ "$AIR_CHART_LANG" == "zh" ]]; then
      items=("朝阳公园:32.4" "奥体中心:45.1" "万寿西宫:51.8" "通州:58.2" "昌平:26.9" "大兴:63.5")
    else
      items=("Chaoyang Park:32.4" "Olympic Center:45.1" "Wanshou Xigong:51.8" "Tongzhou:58.2" "Changping:26.9" "Daxing:63.5")
    fi
    FIRST_UNITS="µg/m³"
    CITY_NOTES=("  - $(t demo_note)")
    SNAPSHOT_URL="$("$SCRIPT_DIR/render_draw.sh" bar \
      --title "$(printf "$(t title_snapshot)" "$demo_city" "${PARAM_LABEL[$snap_param]}")$(t demo_tag)" \
      --subtitle "$(t sub_snapshot_demo)" \
      --unit "$snap_units" --items "${items[@]}" \
      --theme "$THEME" --style "$STYLE" ${OUT:+--out "$OUT"})"
  else
    fetch_city_snapshot "${CITIES[0]}" "${PARAMS[0]}"
  fi
  printf '\n[air-chart] %s\n%s\n' "$(t snapshot_saved)" "$SNAPSHOT_URL" >&2
  if (( ${#CITY_NOTES[@]} )); then
    printf '[air-chart] %s\n%s\n' "$(t summary)" "${CITY_NOTES[*]}" >&2
  fi
  [[ -n "$OUT" ]] && printf '%s\n' "$OUT" || printf '%s\n' "$SNAPSHOT_URL"
  exit 0
fi

for city in "${CITIES[@]}"; do
  if (( DEMO )); then
    GEO_LINE="$("$SCRIPT_DIR/geo_resolve.sh" "$city")" || exit $?
    geo_name="$(cut -f1 <<<"$GEO_LINE")"
    [[ -z "${FIRST_GEO_NAME:-}" ]] && FIRST_GEO_NAME="$geo_name"
    for param in "${PARAMS[@]}"; do
      clean="$WORK/${geo_name}.${param}.tsv"
      demo_series "$city" "$param" "$GRAN" "$((HOURS / ($( [[ "$GRAN" == hours ]] && echo 1 || echo 24 ))))" > "$clean"
      FIRST_UNITS="${PARAM_UNITS[$param]}"; FIRST_TZ="$(cut -f5 <<<"$GEO_LINE")"
      RENDER_SPECS+=("${geo_name} ${PARAM_LABEL[$param]}:${clean}")
      SERIES_PARAMS+=("$param"); SERIES_UNITS+=("${PARAM_UNITS[$param]}")
      dmax="$(awk -F'\t' '$2!=""{if($2>m)m=$2}END{print m+0}' "$clean")"
      if [[ -z "$GLOBAL_MAX" || "$(awk -v a="$GLOBAL_MAX" -v b="$dmax" 'BEGIN{print (b>a)?1:0}')" == "1" ]]; then GLOBAL_MAX="$dmax"; fi
    done
    CITY_NOTES+=("  - ${geo_name}: $(t demo_note)")
  else
    fetch_city_series "$city" || true
  fi
done

if (( ${#RENDER_SPECS[@]} == 0 )); then
  printf '[air-chart] ERROR: %s\n' "$(t err_no_series)" >&2
  exit 5
fi

param0="${PARAMS[0]}"
city_count=${#CITIES[@]}
# 仅拼接用户请求的指标名
param_labels=""
for p in "${PARAMS[@]}"; do param_labels+="${param_labels:+ / }${PARAM_LABEL[$p]}"; done
ylabel="${PARAM_LABEL[$param0]} (${FIRST_UNITS})"
if (( city_count > 1 )); then
  title="$(printf "$(t title_compare)" "${PARAM_LABEL[$param0]}" "$PERIOD")"
  subtitle="$(t sub_compare)"
else
  gname="${FIRST_GEO_NAME:-${CITIES[0]}}"
  title="$(printf "$(t title_single)" "$gname" "$param_labels" "$PERIOD")"
  if (( ${#PARAMS[@]} > 1 )); then
    subtitle="$(t sub_multi_param)"
    ylabel="$(printf "$(t ylabel_multi)" "$FIRST_UNITS")"
  else
    subtitle="$(printf "$(t sub_single)" "$FIRST_TZ")"
  fi
fi

  # WHO 基准线: 以常量序列注入 URL (x-cmd draw 渲染); 仅当单位与字典默认一致
  who_args=()
  if [[ -n "${WHO_BASELINE[$param0]:-}" ]]; then
    units_match=1
    for i in "${!SERIES_PARAMS[@]}"; do
      [[ "${SERIES_UNITS[$i]}" == "${PARAM_UNITS[${SERIES_PARAMS[$i]}]}" ]] || units_match=0
    done
    if (( units_match )); then
      who_args=(--who "${WHO_BASELINE[$param0]}" --who-label "$(t who_label)")
    else
      printf '[air-chart] NOTE: %s\n' "$(t note_who_skipped)" >&2
    fi
  fi

  url="$("$SCRIPT_DIR/render_draw.sh" line \
    --title "$title" --subtitle "$subtitle" --unit "$FIRST_UNITS" \
    --series "${RENDER_SPECS[@]}" \
    ${who_args[@]+"${who_args[@]}"} \
    --theme "$THEME" --style "$STYLE" ${OUT:+--out "$OUT"})"

  printf '\n[air-chart] %s\n%s\n' "$(t chart_saved)" "$url" >&2
  if (( ${#CITY_NOTES[@]} )); then
    printf '[air-chart] %s\n%s\n' "$(t summary)" "${CITY_NOTES[*]}" >&2
  fi
  [[ -n "$OUT" ]] && printf '%s\n' "$OUT" || printf '%s\n' "$url"
