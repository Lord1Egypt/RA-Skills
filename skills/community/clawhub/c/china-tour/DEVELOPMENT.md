# ChinaTour Development Guide

## Project Structure

```
china-tour/
 SKILL.md                    # Main skill file (trigger logic + workflow)
 scripts/
    recommend_route.py      # Route recommendation algorithm
    extract_profile.py      # User profile extraction
    feedback_handler.py     # Feedback handling and dynamic adjustment
 references/
    attractions/            # Attraction basic information
    photo-spots/            # Photography locations
    culture-stories/        # Cultural narratives (CN + EN)
 assets/
     guide-card-template.md  # Tour guide card template
```

---

## Quick Testing

### Test 1: Route Recommendation

```bash
# Photographer route
python scripts/recommend_route.py --attraction "forbidden-city" --profile "solo-photographer" --time "15:00"

# Couple romantic route
python scripts/recommend_route.py --attraction "forbidden-city" --profile "couple-romantic"

# Family with kids route
python scripts/recommend_route.py --attraction "forbidden-city" --profile "family-kids"

# History buff route
python scripts/recommend_route.py --attraction "forbidden-city" --profile "history-buff"

# Quick visit route
python scripts/recommend_route.py --attraction "forbidden-city" --profile "quick-visit"
```

### Test 2: Profile Extraction

```bash
# Extract from conversation
python scripts/extract_profile.py --conversation "我一个人想拍照大概 3 小时"

# Couple trip
python scripts/extract_profile.py --conversation "和女朋友一起想看历史文物"

# Family with kids
python scripts/extract_profile.py --conversation "带孩子想轻松一点"

# JSON output
python scripts/extract_profile.py --conversation "一个人拍照" --json
```

### Test 3: Feedback Handling

```bash
# Satisfied feedback
python scripts/feedback_handler.py --feedback "满意继续" --current-spot "太和殿"

# Request more depth
python scripts/feedback_handler.py --feedback "想听更多历史细节" --current-spot "乾清宫" --depth "L2"

# Request simplification
python scripts/feedback_handler.py --feedback "太啰嗦了简单点" --current-spot "保和殿" --depth "L3"

# Tired, need rest
python scripts/feedback_handler.py --feedback "走不动了想休息" --current-spot "御花园"
```

### Test 4: Multilingual Support

```bash
# English narration data exists
references/culture-stories/forbidden-city-stories-en.md

# Test English route recommendation
python scripts/recommend_route.py --attraction "Forbidden City" --profile "solo-photographer" --language "en"
```

---

## Adding New Attractions

### Step 1: Create Attraction Data

Create file in `references/attractions/`: `[province]/[attraction].md`

```markdown
# [Attraction Name]

## Basic Information
- Location:
- Opening Hours:
- Suggested Duration:
- Ticket Price:

## Layout
[Text description or ASCII map]

## Main Attractions
1. [Spot Name] - Suggested Time - Highlights

## Entrance/Exit
- Main Entrance:
- Exit Location:

## Facilities
- Rest Areas:
- Restrooms:
- Dining:
```

### Step 2: Create Photo Spots Data

Create file in `references/photo-spots/`: `[province]/[attraction]-spots.md`

```markdown
# [Attraction Name] Photo Spots

## Spot 1: [Name]
- Location:
- Best Time:
- Shooting Tips:
- Crowd Avoidance:

## Spot 2: [Name]
...
```

### Step 3: Create Cultural Stories Data

Create file in `references/culture-stories/`: `[province]/[attraction]-stories.md` (Chinese)
Create file in `references/culture-stories/`: `[province]/[attraction]-stories-en.md` (English)

```markdown
# [Attraction Name] Cultural Stories

## Attraction 1
### L1 Brief (30 seconds)
...

### L2 Standard (2-3 minutes)
...

### L3 Deep (5-10 minutes)
...

## Attraction 2
...
```

### Step 4: Update SKILL.md

Add new attraction to the supported list in `SKILL.md`.

---

## User Profile Types

| Type | Description | Route Features |
|------|-------------|----------------|
| solo-photographer | Solo photography enthusiast | Best lighting + less crowded spots + ample shooting time |
| couple-romantic | Couple trip | Romantic scenes + photo spots + private spaces |
| family-kids | Family with children | Interactive experiences + rest points + fun stories |
| history-buff | History enthusiast | Deep narration + hidden spots + historical details |
| quick-visit | Quick tour | Highlights + shortest path + time optimization |

---

## Feedback Types and Adjustments

| Feedback | Keywords | Adjustment Strategy |
|----------|----------|---------------------|
| Satisfied | 满意/好的/不错/继续 | Continue to next stop |
| Want more depth | 想更深/更多/详细点 | Increase narration depth (L2->L3) |
| Too verbose | 太啰嗦/简单点/太多了 | Reduce narration depth (L3->L2) |
| Want photos | 想拍照/拍照/机位 | Add more photo spot recommendations |
| Tired | 累了/休息/走不动 | Add rest points, reduce walking |
| Dissatisfied | 不满意/不喜欢/不好 | Ask reason, replan route |
| Bored | 无聊/没意思 | Add interesting stories |
| In a hurry | 赶时间/快点/着急 | Speed up, skip minor attractions |

---

## Narration Depth Levels

| Level | Duration | Content | Suitable For |
|-------|----------|---------|--------------|
| L1 | 30 seconds | Core info, one-sentence highlight | Quick visits, tired, in a hurry |
| L2 | 2-3 minutes | Historical background + highlights + stories | Regular tourists, standard experience |
| L3 | 5-10 minutes | Detailed history + architectural details + trivia | History enthusiasts, deep tours |

---

## Future Enhancements

- [ ] Add more attractions (West Lake, Terracotta Army, Potala Palace, etc.)
- [ ] Integrate opening hours and ticket price query
- [ ] Add voice narration support (TTS integration)
- [ ] Implement AR navigation (future expansion)

---

## Packaging and Publishing

### Pre-publish Checklist

1. SKILL.md contains complete name and description
2. All scripts run correctly
3. Reference files are well-organized
4. No test or temporary files

### Publishing to ClawHub

```bash
clawhub publish . --version 1.0.0 --changelog "Initial release"
```

---

## Usage Examples

### Scenario 1: First-time User

```
User: 我在故宫怎么逛

AI: 为了给您推荐最合适的路线快速问下
    1. 和谁一起一个人/情侣/带娃/朋友
    2. 更想看什么历史/拍照/文化/随便逛逛
    3. 时间大概多久1 小时/2-3 小时/半天/一天

User: 一个人想拍照大概 3 小时

AI: 收到为您定制故宫摄影路线...
```

### Scenario 2: Returning User (Profile Known)

```
User: 我在故宫还是想拍照

AI: 按您的摄影爱好者偏好推荐以下路线...
```

### Scenario 3: During Tour Feedback

```
AI: 太和殿讲解完毕
    当前体验如何
    1. 满意 -> 继续下一站
    2. 想更深 -> 补充更多细节
    3. 太啰嗦 -> 简化讲解
    4. 想拍照 -> 推荐更多机位

User: 想更深

AI: 好的补充太和殿的深度讲解...
    [Detailed history, architectural details, trivia]
```

---

## Support

- OpenClaw Docs: https://docs.openclaw.ai
- ClawHub: https://clawhub.com
- Discord Community: https://discord.com/invite/clawd
