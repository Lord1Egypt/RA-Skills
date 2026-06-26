#!/usr/bin/env bash
set -euo pipefail
# ADHD Daily Planner v1.0
# Bullet Journal style planning for ADHD brains

PLANNER_DIR="${HOME}/.openclaw/skills/adhd-daily-planner"
DAILY_DIR="$PLANNER_DIR/daily"
MONTHLY_DIR="$PLANNER_DIR/monthly"
COLLECTIONS_DIR="$PLANNER_DIR/collections"
TEMPLATE_DIR="$PLANNER_DIR/templates"

# Create directories
mkdir -p "$DAILY_DIR" "$MONTHLY_DIR" "$COLLECTIONS_DIR" "$TEMPLATE_DIR"

# Get today's date
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$DAILY_DIR/$TODAY.md"
MONTH=$(date +%Y-%m)
MONTH_FILE="$MONTHLY_DIR/$MONTH.md"
DAY_NAME=$(date +%A)
DAY_MONTH=$(date +"%B %d")
TIME_OF_DAY=$(date +%H)

# Determine time of day label
if [ "$TIME_OF_DAY" -ge 5 ] && [ "$TIME_OF_DAY" -lt 12 ]; then
  TIME_LABEL="morning"
  GREETING="🌅 Good morning!"
elif [ "$TIME_OF_DAY" -ge 12 ] && [ "$TIME_OF_DAY" -lt 17 ]; then
  TIME_LABEL="afternoon"
  GREETING="🌞 Good afternoon!"
elif [ "$TIME_OF_DAY" -ge 17 ] && [ "$TIME_OF_DAY" -lt 22 ]; then
  TIME_LABEL="evening"
  GREETING="🌙 Good evening!"
else
  TIME_LABEL="night"
  GREETING="🦉 Working late?"
fi

show_help() {
  echo "ADHD Daily Planner 📝🧠"
  echo ""
  echo "Usage: ./plan.sh [command]"
  echo ""
  echo "Commands:"
  echo "  today       - View today's swim lanes"
  echo "  plan        - Morning intent setting + rapid log"
  echo "  reflect     - Evening reflection"
  echo "  migrate     - Carry unfinished tasks forward"
  echo "  log [task]  - Quick add a task"
  echo "  done [task] - Mark task complete"
  echo "  dopamine    - Show dopamine menu"
  echo "  monthly     - View monthly overview"
  echo ""
  echo "Examples:"
  echo "  ./plan.sh plan"
  echo "  ./plan.sh log 'Call dentist'"
  echo "  ./plan.sh done 'Email client'"
  echo ""
  exit 0
}

create_daily_file() {
  if [ ! -f "$TODAY_FILE" ]; then
    cat > "$TODAY_FILE" << EOF
# $DAY_NAME, $DAY_MONTH 📝

## 🎯 TODAY'S ONE THING
_What ONE thing must happen for today to be a success?_

**ONE THING:** _________________________________

---

## 🏊 SWIM LANES

### 🎯 MUST HAPPEN (The ONE thing)
- [ ] 

### 🔥 HIGH ENERGY (Deep work, creative)
- [ ] 
- [ ] 

### 💧 MEDIUM ENERGY (Standard tasks)
- [ ] 
- [ ] 

### ❄️ LOW ENERGY (Admin, easy wins)
- [ ] 
- [ ] 

### 🚫 NOT TODAY (Captured but deferred)
- [ ] 

---

## 📝 RAPID LOG
_Capture everything as it comes:_

- 

---

## 🎁 DOPAMINE MENU (Today's Rewards)

When I complete the ONE thing:
- [ ] _________________________________

When I finish a swim lane:
- [ ] _________________________________

---

## 🌙 EVENING REFLECTION
_Fill in at end of day:_

### ✅ Today's Wins
- 

### 📊 What Worked?
- 

### 📊 What Didn't?
- 

### 🔄 Migrated Tasks
- 

### 🌟 One Thing for Tomorrow
- 

---

**Created:** $TODAY  
**Time:** $TIME_LABEL
EOF
  fi
}

cmd_today() {
  create_daily_file
  
  echo "═══════════════════════════════════════════════════════"
  echo "  $GREETING"
  echo "  $DAY_NAME, $DAY_MONTH"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  
  # Check if file exists and has content
  if [ -f "$TODAY_FILE" ]; then
    # Extract swim lanes section
    echo "📋 TODAY'S SWIM LANES"
    echo ""
    
    # Show must happen
    echo "🎯 MUST HAPPEN (Today's ONE thing):"
    grep -A 2 "### 🎯 MUST HAPPEN" "$TODAY_FILE" | tail -n +2
    echo ""
    
    # Show each swim lane
    for lane in "🔥 HIGH ENERGY" "💧 MEDIUM ENERGY" "❄️ LOW ENERGY"; do
      echo "$lane:"
      grep -A 3 "### $lane" "$TODAY_FILE" | tail -n +2 | sed 's/^/  /'
      echo ""
    done
    
    # Show completion stats
    COMPLETED=$(grep -c '^\- \[x\]\|^\- \[X\]' "$TODAY_FILE" 2>/dev/null || echo "0")
    TOTAL=$(grep -c '^\- \[ \]' "$TODAY_FILE" 2>/dev/null || echo "0")
    TOTAL=$((TOTAL + COMPLETED))
    
    echo "📊 Progress: $COMPLETED/$TOTAL tasks"
    
    # Energy-based suggestion
    if [ "$TIME_LABEL" = "morning" ]; then
      echo "💡 Try the 🔥 HIGH ENERGY lane while you're fresh!"
    elif [ "$TIME_LABEL" = "afternoon" ]; then
      echo "💡 Energy dip? Try the 💧 MEDIUM ENERGY lane."
    else
      echo "💡 Winding down? Stick to ❄️ LOW ENERGY tasks."
    fi
    
  else
    echo "No plan for today yet. Run: ./plan.sh plan"
  fi
  
  echo ""
  echo "Edit: $TODAY_FILE"
}

cmd_plan() {
  echo "═══════════════════════════════════════════════════════"
  echo "  🌅 MORNING PLANNING SESSION"
  echo "  $DAY_NAME, $DAY_MONTH"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  
  # Step 1: ONE thing
  echo "🎯 STEP 1: TODAY'S ONE THING"
  echo "What ONE thing must happen for today to be a success?"
  echo "(Be specific. This is your ★ priority.)"
  read -p "> " ONE_THING
  echo ""
  
  # Step 2: Energy check
  echo "🧠 STEP 2: ENERGY CHECK"
  echo "How's your energy right now? (1-10)"
  read -p "> " ENERGY
  
  SWIM_LANE="💧 MEDIUM ENERGY"
  if [ "$ENERGY" -ge 8 ] 2>/dev/null; then
    SWIM_LANE="🔥 HIGH ENERGY"
    ENERGY_MSG="You're feeling sharp! Tackle the hard stuff."
  elif [ "$ENERGY" -le 4 ] 2>/dev/null; then
    SWIM_LANE="❄️ LOW ENERGY"
    ENERGY_MSG="Low energy day. Be gentle with yourself."
  else
    ENERGY_MSG="Moderate energy. Good for standard tasks."
  fi
  echo "$ENERGY_MSG"
  echo ""
  
  # Step 3: Rapid log
  echo "📝 STEP 3: RAPID LOG"
  echo "Brain dump - list EVERYTHING on your mind."
  echo "(Type each item, ENTER. Empty line when done.)"
  
  RAPID_LOG=""
  while true; do
    read -p "> " ITEM
    if [ -z "$ITEM" ]; then
      break
    fi
    RAPID_LOG="${RAPID_LOG}
- [ ] ${ITEM}"
  done
  
  # Step 4: Dopamine menu
  echo ""
  echo "🎁 STEP 4: DOPAMINE MENU"
  echo "What will you do when you complete the ONE thing?"
  echo "1. Movement (walk, stretch)"
  echo "2. Sensory (coffee, snack)"
  echo "3. Social (text friend)"
  echo "4. Creation (doodle, music)"
  echo "5. Nature (step outside)"
  echo "6. Novelty (read/watch something)"
  echo "7. Other"
  read -p "Pick (1-7): " DOPAMINE_CHOICE
  
  case $DOPAMINE_CHOICE in
    1) REWARD="Movement break (10 min)" ;;
    2) REWARD="Special coffee/snack" ;;
    3) REWARD="Social connection" ;;
    4) REWARD="Creative play" ;;
    5) REWARD="Nature time" ;;
    6) REWARD="Novelty break" ;;
    *) 
      echo "Custom reward:"
      read -p "> " REWARD
      ;;
  esac
  
  # Create the file
  cat > "$TODAY_FILE" << EOF
# $DAY_NAME, $DAY_MONTH 📝

## 🎯 TODAY'S ONE THING
_What ONE thing must happen for today to be a success?_

**ONE THING:** $ONE_THING

**Status:** ⬜ Not started | 🟡 In progress | ✅ Complete

---

## 🏊 SWIM LANES
_These are context/energy based, NOT time-based_
_Work in whatever lane matches your CURRENT energy_

### 🎯 MUST HAPPEN (The ONE thing)
- [ ] ★ $ONE_THING

### 🔥 HIGH ENERGY (Deep work, creative)
- [ ] 
- [ ] 

### 💧 MEDIUM ENERGY (Standard tasks)
- [ ] 
- [ ] 

### ❄️ LOW ENERGY (Admin, easy wins)
- [ ] 
- [ ] 

### 🚫 NOT TODAY (Captured but deferred)
- [ ] 

---

## 📝 RAPID LOG
_Capture everything as it comes:_
$RAPID_LOG

---

## 🎁 DOPAMINE MENU (Today's Rewards)

When I complete the ONE thing:
- [ ] $REWARD

When I finish a swim lane:
- [ ] 

---

## 🌙 EVENING REFLECTION
_Fill in at end of day:_

### ✅ Today's Wins
- 

### 📊 What Worked?
- 

### 📊 What Didn't?
- 

### 🔄 Migrated Tasks
- 

### 🌟 One Thing for Tomorrow
- 

---

**Planned:** $TODAY $TIME_LABEL  
**Energy Start:** $ENERGY/10  
**Suggested Lane:** $SWIM_LANE  
**File:** $TODAY_FILE
EOF

  echo ""
  echo "═══════════════════════════════════════════════════════"
  echo "  ✅ PLAN CREATED!"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  echo "🎯 ONE THING: $ONE_THING"
  echo "⚡ Energy: $ENERGY/10 → $SWIM_LANE lane"
  echo "🎁 Reward: $REWARD"
  echo ""
  echo "File: $TODAY_FILE"
}

cmd_reflect() {
  create_daily_file
  
  echo "═══════════════════════════════════════════════════════"
  echo "  🌙 EVENING REFLECTION"
  echo "  $DAY_NAME, $DAY_MONTH"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  
  # Get wins
  echo "✅ STEP 1: TODAY'S WINS"
  echo "List everything you completed (even tiny things!):"
  WINS=""
  while true; do
    read -p "Win: " WIN
    if [ -z "$WIN" ]; then
      break
    fi
    WINS="${WINS}
- × ${WIN}"
  done
  
  # What worked
  echo ""
  echo "📊 STEP 2: WHAT WORKED?"
  echo "What helped you today? (techniques, conditions, etc.)"
  WORKED=""
  while true; do
    read -p "> " ITEM
    if [ -z "$ITEM" ]; then
      break
    fi
    WORKED="${WORKED}
- ${ITEM}"
  done

  # What didn't
  echo ""
  echo "📊 STEP 3: WHAT DIDN'T?"
  echo "What got in the way? (distractions, blockers, etc.)"
  DIDNT=""
  while true; do
    read -p "> " ITEM
    if [ -z "$ITEM" ]; then
      break
    fi
    DIDNT="${DIDNT}
- ${ITEM}"
  done
  
  # Migration
  echo ""
  echo "🔄 STEP 4: MIGRATION CHECK"
  echo "Any incomplete tasks to carry forward?"
  echo "(List them, we'll decide what to do with each)"
  
  MIGRATED=""
  while true; do
    read -p "Task (empty to finish): " TASK
    if [ -z "$TASK" ]; then
      break
    fi
    echo "  > Migrate to tomorrow (>)"
    echo "  < Schedule for future date"
    echo "  x Complete it now"
    echo "  ~ Drop it (not happening)"
    read -p "Action (>/<x/~): " ACTION
    case $ACTION in
      '>') MIGRATED="${MIGRATED}
- > ${TASK} (→ tomorrow)" ;;
      '<')
        read -p "Date (YYYY-MM-DD): " DATE
        MIGRATED="${MIGRATED}
- < ${TASK} (→ ${DATE})" ;;
      'x') MIGRATED="${MIGRATED}
- × ${TASK} (completed now!)" ;;
      '~') MIGRATED="${MIGRATED}
- ~ ~~${TASK}~~ (dropped)" ;;
      *) MIGRATED="${MIGRATED}
- ? ${TASK}" ;;
    esac
  done
  
  # Tomorrow
  echo ""
  echo "🌟 STEP 5: ONE THING FOR TOMORROW"
  echo "What's one thing you'll do differently tomorrow?"
  read -p "> " TOMORROW_LESSON
  
  # Write reflection to file
  # Append a reflection section to the daily file
  cat >> "$TODAY_FILE" << EOF

---

## 🌙 EVENING REFLECTION (completed)

### ✅ Today's Wins
${WINS:-
- (none recorded)}

### 📊 What Worked?
${WORKED:-
- (none recorded)}

### 📊 What Didn't?
${DIDNT:-
- (none recorded)}

### 🔄 Migrated Tasks
${MIGRATED:-
- (none)}

### 🌟 One Thing for Tomorrow
- ${TOMORROW_LESSON:-(not set)}

---

**Reflected:** $(date +%Y-%m-%d) $TIME_LABEL
EOF

  # Count stats
  WIN_COUNT=0
  WORKED_COUNT=0
  MIGRATED_COUNT=0
  [ -n "$WINS" ] && WIN_COUNT=$(echo "$WINS" | grep -c '×' || true)
  [ -n "$WORKED" ] && WORKED_COUNT=$(echo "$WORKED" | grep -c '^-' || true)
  [ -n "$MIGRATED" ] && MIGRATED_COUNT=$(echo "$MIGRATED" | grep -c '^-' || true)

  echo ""
  echo "═══════════════════════════════════════════════════════"
  echo "  ✅ REFLECTION COMPLETE & SAVED!"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  echo "📊 Summary:"
  echo "  Wins: $WIN_COUNT"
  echo "  What worked: $WORKED_COUNT"
  echo "  Migrated: $MIGRATED_COUNT"
  echo ""
  echo "Remember: Migration is strategy, not failure!"
  echo ""
  echo "Saved to: $TODAY_FILE"
}

cmd_migrate() {
  echo "═══════════════════════════════════════════════════════"
  echo "  🔄 TASK MIGRATION"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  
  YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)
  YESTERDAY_FILE="$DAILY_DIR/$YESTERDAY.md"
  
  if [ -f "$YESTERDAY_FILE" ]; then
    echo "Yesterday's file found: $YESTERDAY_FILE"
    echo ""
    echo "Incomplete tasks from yesterday:"
    grep '^\- \[ \]' "$YESTERDAY_FILE" 2>/dev/null || echo "  (none found)"
    echo ""
    echo "Mark tasks with:"
    echo "  > - Migrate to today"
    echo "  < - Schedule for future"
    echo "  ~ - Drop it"
    echo ""
    echo "Edit $YESTERDAY_FILE to process, then run:"
    echo "  ./plan.sh plan (to add migrated tasks to today)"
  else
    echo "No file found for yesterday ($YESTERDAY)"
    echo ""
    echo "Migration workflow:"
    echo "1. Review yesterday's incomplete tasks"
    echo "2. Decide: migrate (>), schedule (<), or drop (~)"
    echo "3. Today's planning includes migrated tasks"
  fi
}

cmd_log() {
  TASK="$1"
  if [ -z "$TASK" ]; then
    echo "Usage: ./plan.sh log 'task description'"
    exit 1
  fi
  
  create_daily_file
  
  # Append to rapid log
  echo "" >> "$TODAY_FILE"
  echo "- [ ] $TASK" >> "$TODAY_FILE"
  
  echo "📝 Added to rapid log: $TASK"
}

cmd_done() {
  TASK="$1"
  if [ -z "$TASK" ]; then
    echo "Usage: ./plan.sh done 'task description'"
    echo "Or edit $TODAY_FILE directly"
    exit 1
  fi
  
  create_daily_file
  
  # Try to mark as complete in file (use fixed-string grep for safety)
  if grep -Fq "[ ] $TASK" "$TODAY_FILE" 2>/dev/null; then
    # Escape sed special chars in task name
    TASK_SED=$(printf '%s' "$TASK" | sed 's/[&/\]/\\&/g')
    sed -i.bak "s/\[ \] ${TASK_SED}/[x] ${TASK_SED}/" "$TODAY_FILE"
    rm -f "${TODAY_FILE}.bak"
    echo "✅ Marked complete: $TASK"
  else
    # Add to wins section
    echo "" >> "$TODAY_FILE"
    echo "- × $TASK (added retroactively)" >> "$TODAY_FILE"
    echo "✅ Added to wins: $TASK"
  fi
}

cmd_dopamine() {
  echo "═══════════════════════════════════════════════════════"
  echo "  🧠 DOPAMINE MENU"
  echo "  Quick rewards for ADHD brains"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  echo "Pick ONE. Do it. Back to work."
  echo ""
  echo "1. 🏃 MOVEMENT (2-5 min)"
  echo "   - 10 jumping jacks"
  echo "   - Stretch"
  echo "   - Walk around the room"
  echo ""
  echo "2. ☕ SENSORY (2-5 min)"
  echo "   - Make coffee/tea"
  echo "   - Eat a snack"
  echo "   - Splash water on face"
  echo ""
  echo "3. 💬 SOCIAL (2-5 min)"
  echo "   - Text a friend"
  echo "   - Check social (set timer!)"
  echo "   - Call someone quick"
  echo ""
  echo "4. 🎨 CREATION (2-5 min)"
  echo "   - Doodle"
  echo "   - Play one song"
  echo "   - Organize a drawer"
  echo ""
  echo "5. 🌿 NATURE (2-5 min)"
  echo "   - Step outside"
  echo "   - Look at a plant"
  echo "   - Open a window"
  echo ""
  echo "6. ✨ NOVELTY (2-5 min)"
  echo "   - Read something new"
  echo "   - Watch a short video"
  echo "   - Change your environment"
  echo ""
  echo "7. ✅ COMPLETION (instant)"
  echo "   - Check off a small task"
  echo "   - Make a 'done' list"
  echo "   - Celebrate the win!"
  echo ""
}

cmd_monthly() {
  create_monthly_file
  
  echo "═══════════════════════════════════════════════════════"
  echo "  📅 MONTHLY OVERVIEW"
  echo "  $MONTH"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  
  if [ -f "$MONTH_FILE" ]; then
    cat "$MONTH_FILE"
  else
    echo "No monthly overview yet."
    echo "Edit: $MONTH_FILE"
  fi
}

create_monthly_file() {
  if [ ! -f "$MONTH_FILE" ]; then
    cat > "$MONTH_FILE" << EOF
# $(date +%B) $(date +%Y) 📅

## 🎯 Monthly Theme/Intent
_What is this month about?_

**THEME:** _________________________________

---

## 📊 Weekly Tracker

| Week | ONE Thing | Completed | Avg Energy | Key Win |
|------|-----------|-----------|------------|---------|
| W1   |           |           |            |         |
| W2   |           |           |            |         |
| W3   |           |           |            |         |
| W4   |           |           |            |         |
| W5   |           |           |            |         |

---

## 🔄 Recurring Tasks
_Tasks that repeat this month:_

- [ ] 

---

## 🏆 Monthly Goals

- [ ] 

---

## 💡 Ideas & Capture
_Don't forget these:_

- 

---

Created: $TODAY
EOF
  fi
}

# Main command dispatcher
case "${1:-today}" in
  today)
    cmd_today
    ;;
  plan)
    cmd_plan
    ;;
  reflect)
    cmd_reflect
    ;;
  migrate)
    cmd_migrate
    ;;
  log)
    shift
    cmd_log "$1"
    ;;
  done)
    shift
    cmd_done "$1"
    ;;
  dopamine|menu)
    cmd_dopamine
    ;;
  monthly)
    cmd_monthly
    ;;
  --help|-h|help)
    show_help
    ;;
  *)
    echo "Unknown command: $1"
    echo ""
    show_help
    ;;
esac
