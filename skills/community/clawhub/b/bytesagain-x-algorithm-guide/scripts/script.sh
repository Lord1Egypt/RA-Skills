#!/usr/bin/env bash
# bytesagain-x-algorithm-guide
# Audit and optimize X (Twitter) posts using 2026 algorithm rules
set -euo pipefail

CMD="${1:-summary}"

cmd_summary() {
  echo "=== 2026 X Algorithm Rules (from open-source code) ==="
  echo ""
  echo "POSTING RULES"
  echo "  1. No links in main tweet (30-50% reach penalty) -- put links in first reply"
  echo "  2. Max 1-2 hashtags (more than 2 = 40% penalty)"
  echo "  3. Pure text beats video by 30% -- X is unique in this"
  echo "  4. Post 3-5 times/day, 30-60 min apart -- high freq + low quality = penalty"
  echo "  5. Premium = 10x reach vs free accounts"
  echo ""
  echo "HIGH LEVERAGE ACTIONS"
  echo "  6. Reply every genuine comment in first hour (+75 weight = 150x a like)"
  echo "  7. Create bookmark-worthy content (+10 weight = 20x a like)"
  echo "  8. End with a question -- conversation depth is the strongest ranking signal"
  echo "  9. Keep tone positive/constructive -- Grok suppresses aggressive content"
  echo " 10. Long posts beat threads -- 2+ min read time gets +10 weight"
  echo ""
  echo "ENGAGEMENT WEIGHTS (from open-source code)"
  echo "  Author reply to comment: +75  <-- strongest"
  echo "  Bookmark:                +10"
  echo "  Retweet:                 +1"
  echo "  Like:                    +0.5  <-- weakest"
  echo ""
  echo "PENALTIES TO AVOID"
  echo "  External link in body    -30 to -50% reach"
  echo "  More than 2 hashtags     -40%"
  echo "  Low TweepCred (< 65)     only 3 tweets distributed"
  echo "  Engagement pods/fake     detected, lowers TweepCred"
}

cmd_checklist() {
  echo "=== Pre-Post Checklist ==="
  echo ""
  echo "[ ] No external links in tweet body"
  echo "[ ] 1-2 hashtags only"
  echo "[ ] Under 280 characters"
  echo "[ ] Ends with a question or clear opinion"
  echo "[ ] Positive, constructive tone"
  echo "[ ] Link ready to paste as first reply"
  echo "[ ] Plan to check replies within 30 minutes"
  echo "[ ] Content has bookmark value (data, list, framework, or insight)"
}

cmd_audit() {
  local tweet="${2:-}"
  if [ -z "$tweet" ]; then
    echo "Usage: $0 audit \"your tweet text\""
    exit 1
  fi

  echo "=== Tweet Audit ==="
  echo "Text: $tweet"
  echo ""

  score=100
  passed=0
  failed=0

  # Check for external links
  if echo "$tweet" | grep -qE 'https?://'; then
    echo "FAIL: External link in body (-40 pts) -- move to first reply"
    score=$((score - 40))
    failed=$((failed + 1))
  else
    echo "PASS: No external link in body"
    passed=$((passed + 1))
  fi

  # Check hashtag count
  tag_count=$(echo "$tweet" | grep -oE '#[A-Za-z0-9_]+' | wc -l | tr -d ' ')
  if [ "$tag_count" -gt 2 ]; then
    echo "FAIL: $tag_count hashtags (max 2, -20 pts) -- remove extras"
    score=$((score - 20))
    failed=$((failed + 1))
  else
    echo "PASS: Hashtag count OK ($tag_count)"
    passed=$((passed + 1))
  fi

  # Check character count
  char_count=${#tweet}
  if [ "$char_count" -gt 280 ]; then
    echo "FAIL: $char_count characters (max 280, -30 pts)"
    score=$((score - 30))
    failed=$((failed + 1))
  else
    echo "PASS: Character count OK ($char_count/280)"
    passed=$((passed + 1))
  fi

  # Check for question
  if echo "$tweet" | grep -qE '\?'; then
    echo "PASS: Ends with question (triggers replies)"
    passed=$((passed + 1))
  else
    echo "TIP:  Add a question to boost reply rate (weight +75 per reply)"
  fi

  echo ""
  echo "Score: $score/100 | Passed: $passed | Failed: $failed"
  if [ "$score" -ge 90 ]; then
    echo "Result: GOOD -- ready to post"
  elif [ "$score" -ge 70 ]; then
    echo "Result: OK -- minor issues above"
  else
    echo "Result: FIX -- address issues before posting"
  fi
}

cmd_draft() {
  local topic="${2:-AI agents}"
  echo "=== Tweet Draft Templates: $topic ==="
  echo ""
  echo "--- Draft 1 (insight format) ---"
  echo "Most people get $topic wrong."
  echo ""
  echo "The real approach:"
  echo "- [key point 1]"
  echo "- [key point 2]"
  echo "- [key point 3]"
  echo ""
  echo "What has worked for you? #AI"
  echo ""
  echo "Reply with: [your link here]"
  echo ""
  echo "--- Draft 2 (data format) ---"
  echo "3 things about $topic worth bookmarking:"
  echo ""
  echo "1. [fact or insight]"
  echo "2. [fact or insight]"
  echo "3. [fact or insight]"
  echo ""
  echo "Which one surprised you most? #AIAgents"
  echo ""
  echo "Reply with: [your link here]"
  echo ""
  echo "--- Rules applied ---"
  echo "  No link in body (put in reply)"
  echo "  Max 2 hashtags"
  echo "  Ends with question"
  echo "  Pure text format"
}

cmd_growth() {
  echo "=== 30-Day X Growth Playbook ==="
  echo "(Verified: 4,500 followers / 5M views / 1M single-day peak in 30 days)"
  echo ""
  echo "DAILY ACTIONS (non-negotiable)"
  echo "  1. 30-50 high-quality replies under top creator posts"
  echo "     -- Real opinions, not 'great post!' or 'lol'"
  echo "     -- Goal: get the creator to reply or like you back"
  echo "     -- This signals to the algorithm you are a quality account"
  echo "  2. 3-5 original tweets (NOT more)"
  echo "     -- New accounts get penalized for spam volume"
  echo "     -- Quality > quantity, always"
  echo "  3. Follow 5-10 accounts in your niche"
  echo "     -- Top creators or quality accounts, not random follows"
  echo ""
  echo "CONTENT MIX STRATEGY"
  echo "  80% broad/relatable content:"
  echo "     -- Cognitive contrast (what people expect vs reality)"
  echo "     -- Interesting personal observations"
  echo "     -- Counterintuitive takes"
  echo "     -- These get reach because they appeal to human nature"
  echo "  20% niche expertise:"
  echo "     -- Deep-dive insights, data, frameworks"
  echo "     -- This converts readers to followers"
  echo "     -- Broad content brings people to your page,"
  echo "        expertise content makes them stay"
  echo ""
  echo "WEEK-BY-WEEK PLAN"
  echo "  Week 1-2: Focus on engagement only"
  echo "     -- Reply 30-50x/day under top creators"
  echo "     -- Do not expect follower growth yet"
  echo "     -- Build algorithm weight first"
  echo "  Week 3: Start posting 3-5x/day consistently"
  echo "     -- Mix 80/20 content ratio"
  echo "     -- Check replies within 30 min of posting"
  echo "  Week 4: Double down on what works"
  echo "     -- Which tweet format got most bookmarks?"
  echo "     -- Which topics drove replies?"
  echo "     -- Repeat those patterns"
  echo ""
  echo "ACCELERATORS"
  echo "  Open Premium early:"
  echo "     -- Comments ranked higher in feeds"
  echo "     -- Platform treats you as legitimate account (not a bot)"
  echo "     -- Required for creator monetization program"
  echo "  First hour after posting:"
  echo "     -- Reply to every genuine comment (+75 weight each)"
  echo "     -- One real reply = 150 likes in algorithm weight"
  echo "     -- This is your highest-leverage daily action"
  echo ""
  echo "WHAT DOES NOT WORK FOR NEW ACCOUNTS"
  echo "  x  Posting pure technical deep-dives (audience too small)"
  echo "  x  Posting links in main tweet (30-50% reach penalty)"
  echo "  x  More than 2 hashtags (40% penalty)"
  echo "  x  Posting 10+ times per day (spam signal)"
  echo "  x  Engagement pods / follow-for-follow (lowers TweepCred)"
  echo "  x  Copy-pasting from other platforms without adapting"
}

cmd_help() {
  echo "bytesagain-x-algorithm-guide -- 2026 X Algorithm Tool"
  echo ""
  echo "Commands:"
  echo "  summary            Show 10 core algorithm rules"
  echo "  checklist          Pre-post checklist (8 items)"
  echo "  audit <tweet>      Score tweet against algorithm rules"
  echo "  draft <topic>      Generate algorithm-compliant tweet templates"
  echo "  growth             30-day growth playbook (verified tactics)"
  echo ""
  echo "Examples:"
  echo "  bash script.sh summary"
  echo "  bash script.sh audit \"Check out bytesagain.com #AI #AIAgents #OpenClaw\""
  echo "  bash script.sh draft \"local AI agents\""
  echo "  bash script.sh growth"
}

case "$CMD" in
  summary)   cmd_summary ;;
  checklist) cmd_checklist ;;
  audit)     cmd_audit "$@" ;;
  draft)     cmd_draft "$@" ;;
  growth)    cmd_growth ;;
  help|*)    cmd_help ;;
esac
