---
name: daily-fitness
description: "Daily no-equipment workout — 5–15 min bodyweight routines (HIIT, yoga, core, mobility) with instructions and streak tracking. Works at home, office, or travel."
keywords:
  - 今日运动
  - 每日锻炼
  - 运动推荐
  - 健身计划
  - 快速运动
  - 无器材训练
  - 拉伸
  - 办公室运动
  - 瑜伽
  - HIIT
  - 核心训练
  - 有氧运动
  - daily fitness
  - daily workout
  - quick workout
  - exercise routine
  - morning workout
  - no equipment workout
  - home workout
  - office workout
  - stretch
  - yoga
  - bodyweight workout
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Fitness / 今日运动

Generate a daily workout routine with visual exercise cards and a built-in timer.

## Workflow

1. **Get today's date** — Use day of week to determine workout focus:
   - Mon: Upper body (push-ups, planks, arm circles)
   - Tue: Core (crunches, leg raises, russian twists)
   - Wed: Lower body (squats, lunges, calf raises)
   - Thu: Cardio (jumping jacks, high knees, burpees)
   - Fri: Full body HIIT
   - Sat: Yoga/Flexibility
   - Sun: Active recovery/Stretching
2. **Design the routine** — Create 5-7 exercises, each with duration/reps, rest periods. Total time 8-12 minutes. No equipment needed.
3. **Generate the visual** — Create a single-file HTML artifact with interactive timer.

## Visual Design Requirements

Create an energetic, app-like workout interface:

- **Layout**: Scrollable card-based layout. Each exercise is a card with: name (EN + CN), duration/reps, brief description of form.
- **Typography**: Bold, sporty fonts (e.g., Rajdhani, Exo 2, Barlow Condensed). High contrast.
- **Color scheme**: Energetic palette — electric blue + neon green, or warm orange + dark gray. Match the workout type (calming blues for yoga, fiery reds for HIIT).
- **Exercise cards**: Each card shows exercise name, duration ("30 seconds" / "12 reps"), form tip in 1 line, and a text-art or emoji representation of the movement.
- **Interactive timer**: A START button at the top that begins a countdown through all exercises with rest intervals. Visual countdown circle. Audio beep (use Web Audio API for a simple tone) at transitions.
- **Progress bar**: Shows overall workout progress.
- **Stats**: Total workout time, estimated calories, difficulty level (⭐⭐⭐).
- **Ad-ready zone**: `<div id="ad-slot-top">` above the workout. `<div id="ad-slot-bottom">` after completion.
- **Footer**: "Powered by ClawCode"

## Content Guidelines

- All exercises should be doable in a small space (apartment/office friendly)
- No equipment required
- Include form tips to prevent injury
- Provide modifications (easier/harder) for at least 2 exercises
- Bilingual exercise names and instructions

## Output

Save as `/mnt/user-data/outputs/daily-fitness.html` and present to user.

---

## 推送管理

```bash
# 开启每日推送（早晚各一次）
node scripts/push-toggle.js on <userId>

# 自定义时间和渠道
node scripts/push-toggle.js on <userId> --morning 08:00 --evening 20:00 --channel feishu

# 关闭推送
node scripts/push-toggle.js off <userId>

# 查看推送状态
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`
