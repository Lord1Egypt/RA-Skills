#!/usr/bin/env bash
set -euo pipefail
cd /home/irtual/.openclaw/workspace/skills/ai-orchestrator

echo '[1/8] dry-run daemon'
bash ask-deepseek.sh --dry-run --daemon >/tmp/deepseek-test-dryrun.txt

echo '[2/8] single prompt daemon'
bash ask-deepseek.sh --daemon 'Reply with exactly: MATRIX_ONE' >/tmp/deepseek-test-single.txt
if ! grep -Eq '📦 Ответ:|✅ Статус:' /tmp/deepseek-test-single.txt; then
  echo '[FAIL] single prompt daemon did not produce a usable response path' >&2
  cat /tmp/deepseek-test-single.txt >&2
  exit 1
fi
sleep 5

echo '[3/8] session continuity basic'
bash ask-deepseek.sh --daemon --session deepseek-matrix 'Reply with exactly: MATRIX_SESSION_ONE' >/tmp/deepseek-test-session-1.txt
if ! grep -Eq '📦 Ответ:|✅ Статус:' /tmp/deepseek-test-session-1.txt; then
  echo '[FAIL] session step 1 did not produce a usable response path' >&2
  cat /tmp/deepseek-test-session-1.txt >&2
  exit 1
fi
sleep 5
bash ask-deepseek.sh --daemon --session deepseek-matrix 'Reply with exactly: MATRIX_SESSION_TWO' >/tmp/deepseek-test-session-2.txt
if ! grep -Eq '📦 Ответ:|✅ Статус:' /tmp/deepseek-test-session-2.txt; then
  echo '[FAIL] session step 2 did not produce a usable response path' >&2
  cat /tmp/deepseek-test-session-2.txt >&2
  exit 1
fi
bash ask-deepseek.sh --session deepseek-matrix --end-session >/tmp/deepseek-test-session-end.txt
sleep 5

echo '[4/8] search mode daemon'
bash ask-deepseek.sh --daemon --search 'Reply with exactly: MATRIX_SEARCH' >/tmp/deepseek-test-search.txt
if ! grep -Eq '📦 Ответ:|✅ Статус:' /tmp/deepseek-test-search.txt; then
  echo '[FAIL] search mode did not produce a usable response path' >&2
  cat /tmp/deepseek-test-search.txt >&2
  exit 1
fi
sleep 5

echo '[5/8] think mode daemon'
bash ask-deepseek.sh --daemon --think 'Reply with exactly: MATRIX_THINK' >/tmp/deepseek-test-think.txt
if ! grep -Eq '📦 Ответ:|✅ Статус:' /tmp/deepseek-test-think.txt; then
  echo '[FAIL] think mode did not produce a usable response path' >&2
  cat /tmp/deepseek-test-think.txt >&2
  exit 1
fi
sleep 5

echo '[6/8] stdin daemon'
printf 'Reply with exactly: MATRIX_STDIN' | bash ask-deepseek.sh --daemon --stdin >/tmp/deepseek-test-stdin.txt
if ! grep -Eq '📦 Ответ:|✅ Статус:' /tmp/deepseek-test-stdin.txt; then
  echo '[FAIL] stdin mode did not produce a usable response path' >&2
  cat /tmp/deepseek-test-stdin.txt >&2
  exit 1
fi
sleep 5

echo '[7/8] oversize detection path'
python3 - <<'PY' > /tmp/deepseek-oversize-prompt.txt
print('Reply with exactly: TOO_BIG\\n')
print('X' * 260000)
PY
set +e
bash ask-deepseek.sh --daemon --session deepseek-oversize-test --stdin < /tmp/deepseek-oversize-prompt.txt >/tmp/deepseek-test-oversize.txt 2>&1
rc=$?
set -e
if [[ $rc -ne 0 ]]; then
  if ! grep -Eq 'DEEPSEEK_SUBMIT_BLOCKED_OVERSIZE_PROMPT|✂️ Retry with shortened prompt|📦 Ответ:' /tmp/deepseek-test-oversize.txt; then
    echo '[FAIL] oversize path failed without explicit detection/retry signal' >&2
    cat /tmp/deepseek-test-oversize.txt >&2
    exit 1
  fi
else
  if ! grep -Eq '✂️ Retry with shortened prompt|📦 Ответ:' /tmp/deepseek-test-oversize.txt; then
    echo '[FAIL] oversize path succeeded without visible shorten/delivery evidence' >&2
    cat /tmp/deepseek-test-oversize.txt >&2
    exit 1
  fi
fi
bash ask-deepseek.sh --session deepseek-oversize-test --end-session >/tmp/deepseek-test-oversize-end.txt || true

echo '[8/8] giant file transport path'
wc -c /home/irtual/.openclaw/workspace/tmp/super-memori-dt-20260410/large_prompt_ack_test_full.md >/tmp/deepseek-test-giant-size.txt

echo '[OK] ai-orchestrator mode matrix passed'
