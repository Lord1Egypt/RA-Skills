#!/usr/bin/awk -f
# data_transform.awk — OpenAQ 传感器原始 TSV 清洗 / 缺口检测 / 统计聚合 (POSIX awk 兼容)
# 输入: TSV  "utc_ts \t local_ts \t value"   (来自 openaq_fetch_series)
# 输出: TSV  "label \t value"               (供 render_draw.sh 消费; 断点行 value 为空)
# 参数: -v gran=hours|days  -v stats=/path/to/stats.tsv
BEGIN { FS = OFS = "\t"; n = 0; skipped = 0 }

function trim(s) { gsub(/^[ \t\r]+|[ \t\r]+$/, "", s); return s }

# UTC "YYYY-MM-DDTHH:MM:SS..." -> epoch 秒 (days-from-civil 算法, 免 gawk 扩展)
function epoch(s,   y, mo, d, h, mi, se, a, y2, m2, era, doe, doy, doe_days) {
  y = substr(s, 1, 4) + 0; mo = substr(s, 6, 2) + 0; d = substr(s, 9, 2) + 0
  h = substr(s, 12, 2) + 0; mi = substr(s, 15, 2) + 0; se = substr(s, 18, 2) + 0
  a = int((14 - mo) / 12)
  y2 = y + 4800 - a
  m2 = mo + 12 * a - 3
  doe_days = d + int((153 * m2 + 2) / 5) + 365 * y2 + int(y2 / 4) - int(y2 / 100) + int(y2 / 400) - 32045
  return (doe_days - 2440588) * 86400 + h * 3600 + mi * 60 + se
}

{
  utc = trim($1); local = trim($2); v = trim($3)
  if (utc == "") next
  if (v == "" || v !~ /^-?[0-9]+(\.[0-9]+)?$/ || v + 0 < 0) { skipped++; next }
  if (cap != "" && v + 0 > cap + 0) { skipped_extreme++; next }   # 超物理上限尖峰(故障)剔除
  # 标签: 小时级 "MM-DD HH:00", 日级 "MM-DD"
  label = local
  if (gran == "hours") {
    if (match(local, /[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}/))
      label = substr(local, RSTART + 5, 5) " " substr(local, RSTART + 11, 2) ":00"
  } else {
    if (match(local, /[0-9]{4}-[0-9]{2}-[0-9]{2}/))
      label = substr(local, RSTART + 5, 5)
  }
  n++
  ep[n] = epoch(utc); lab[n] = label; val[n] = v + 0
  sum += val[n]
  if (n == 1 || val[n] < vmin) vmin = val[n]
  if (n == 1 || val[n] > vmax) vmax = val[n]
}

END {
  # 缺口检测: 聚合端点粒度固定 (hours=1h, days=1d), 超过 1.5 步长视为断点, 插入空行
  step = (gran == "hours" ? 3600 : 86400)
  prev_t = 0
  for (i = 1; i <= n; i++) {
    if (prev_t > 0 && ep[i] - prev_t > step * 1.5) print "", ""   # 断点标记
    print lab[i], val[i]
    prev_t = ep[i]
  }
  if (stats != "") {
    printf "count\t%d\n", n > stats
    printf "min\t%s\n", (n ? vmin : "") >> stats
    printf "max\t%s\n", (n ? vmax : "") >> stats
    printf "avg\t%s\n", (n ? sum / n : "") >> stats
    printf "skipped\t%d\n", skipped >> stats
    printf "skipped_extreme\t%d\n", skipped_extreme + 0 >> stats
  }
}
