#!/usr/bin/env bash
# 离线样例 runner：30 秒内在临时目录里走完「机检自测 → 无通道骨架 → 骨架该红就红」三档。
# 用法：bash scripts/fixtures/run_fixtures.sh     （零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp}，跑完即删）
# 退码：0 三档全合期望；1 有不合（逐档点名并附那次真实退码与真实末行）；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。
# 三档各自的期望都挂在两条分支上都被读的断言里（通与不通都读同一个数），不是只在失败分支里写死的死数。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-research-brief.XXXXXX")"
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then echo "3 取值域故障：临时目录没建成（TMPDIR=$TMPDIR 是否存在、可写？），不带空路径往下跑"; exit 3; fi
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
for f in "$ROOT/scripts/check_brief.py" "$ROOT/scripts/make_outline.py" "$FIX/good-brief.md" "$FIX/sources.jsonl"; do
  if [ ! -f "$f" ]; then echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; fi
done

echo "档① 机检自测（好样须过、四枚坏样须各发它该发的那一道）"
out=$(cd "$ROOT" && python3 -B scripts/check_brief.py --selftest 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | tail -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then echo "  → 不合"; bad=$((bad + 1)); else echo "  → 合"; fi

echo "档② 无通道骨架（来源清单 → 待填骨架；本件不代填结论、不发请求）"
out=$(cd "$ROOT" && python3 -B scripts/make_outline.py --sources scripts/fixtures/sources.jsonl --out "$WORK/outline.md" 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | head -1)"; echo "  实发退码=$rc｜期望=0｜骨架行数=$(wc -l < "$WORK/outline.md" 2>/dev/null || echo 取不到)"
if [ "$rc" -ne 0 ]; then
  if [ "$rc" -eq 3 ]; then echo "  → 不可判：骨架生成走到取值域出口（见上一行原文）"; unk=$((unk + 1));
  else echo "  → 不合：期望退码 0，实发 $rc"; bad=$((bad + 1)); fi
else
  echo "  → 合（骨架落成，结论位仍留占位）"
fi

echo "档③ 骨架过机检——期望红，且红在结论占位那一行"
if [ -f "$WORK/outline.md" ]; then
  out=$(cd "$ROOT" && python3 -B scripts/check_brief.py "$WORK/outline.md" 2>&1); rc=$?
  hit=$(printf '%s\n' "$out" | grep -c '结论仍是占位')
  echo "  实发退码=$rc｜期望=1｜「结论仍是占位」命中=$hit｜末行=$(printf '%s\n' "$out" | head -1)"
  if [ "$rc" -eq 1 ] && [ "$hit" -ge 1 ]; then echo "  → 合（骨架不该被当成速览交付，红在这行是设计）";
  else echo "  → 不合：期望的红不再在场（退码 $rc／命中 $hit）——这一形变了就复读 make_outline 的结论位与 check_brief 的占位判据，别沿用本断言"; bad=$((bad + 1)); fi
else
  echo "  → 不可判：档②没出骨架，这一档无从跑"; unk=$((unk + 1))
fi

echo "----"
echo "档数=3（由上面逐档现报）｜合期望=$((3 - bad - unk))｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo "有档取值域故障，整趟按 3 读，不并入「不合」。"; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
