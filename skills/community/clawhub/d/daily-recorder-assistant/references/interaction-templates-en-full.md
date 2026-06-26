# Interaction Templates (Morning/Evening Queries) - Full English Version

## Template Structure

Each template consists of three parts:
1. **Status Reference**: Key info from yesterday's record
2. **Today Task Hint**: Clear daily core task
3. **Readiness Check / Review Guide**: Different based on time period

---

## Morning Query Templates (by Weekday)

### Monday Morning Template
```
"Your Sunday night plan indicates you intend to do [Task Name] today. How was your rest quality yesterday (score {{last_night_energy}})? Do you feel energized enough to start this task?"
```

**Use case**: Before high-intensity creative work on Monday, confirm recovery status and energy level

---

### Tuesday Morning Template
```
"Yesterday's completion: [Task Name] completed [[ ]]%. Today plan continues with [Next Steps] or enters [New Task]. Are there any unfinished items that need priority?"
```

**Use case**:承接昨日进度，确认连续性或切换点

---

### Wednesday Morning Template
```
"Week halfway. Review the completion rate and energy status of first two days (avg score {{avg_energy_m1_m2}}). Today plan is [Task Name]. Do you need to adjust pace to avoid fatigue accumulation?"
```

**Use case**: Mid-week checkpoint, prevent burnout

---

### Thursday Morning Template
```
"Previous days encountered [Common Barrier Type] issues. Today's plan is [攻坚 Task]. Suggested strategy: [Coping Strategy]. Ready to start?"
```

**Use case**: Anticipate obstacles based on historical patterns and provide预案

---

### Friday Morning Template
```
"Week wrap-up day. Plan is [Summary Tasks / Closing Work]. Do you feel energized enough? Or need buffer time for unexpected items?"
```

**Use case**: Confirm remaining capacity and缓冲需求 before weekend

---

### Saturday Morning Template (Rest Day)
```
"After last week's high-intensity tasks, yesterday's energy score was {{last_night_energy}}. Today is rest-adjustment day. Do you feel fully recovered? Can light creative activity or continue relaxation?"
```

**Use case**: Confirm recovery status and适度活动边界 on weekend

---

### Sunday Morning Template (Minimal)
```
"Weekend wrap-up. Overall week completion rate how? Need to prepare for next week or maintain rest state?"
```

**Use case**: Lightweight Sunday query, prepare Monday launch

---

## Evening Query Templates (by Weekday)

### Monday Evening Template
```
"Today review: Task completion rate how? Any encountered obstacles? Energy status score 1-5? Ideas for tomorrow's plan?"
```

**Use case**: Day-one summary, confirm按计划推进

---

### Tuesday Evening Template
```
"承昨日进度， today completion [[ ]]%. Did problems match预估 (Barrier Type)? Do you feel fatigue accumulation needing pace adjustment?"
```

**Use case**: Mid-week feedback check,节奏预警

---

### Wednesday Evening Template
```
"Week halfway review: Completion rate and energy trend how? Need buffer for second half or adjust intensity?"
```

**Use case**: Half-cycle总结，预防透支

---

### Thursday Evening Template
```
"攻坚任务 completion rate how? Encountered [预判障碍]? Is coping strategy effective? Need extra support?"
```

**Use case**: Key task feedback and预案验证

---

### Friday Evening Template
```
"Week wrap-up completion [[ ]]%. Energy status how (score {{energy_score}})? Need full weekend rest or light activity adjustment?"
```

**Use case**: Confirm休息需求 and下周衔接 on week end

---

### Sunday Night Template (Prep for Monday)
```
"Week review: Completion rate [[ ]]%, avg energy [[ ]]分。Main issues were [Problem Types Summary]. Any ideas for next week's plan? Want to adjust task distribution or pace?"
```

**Use case**: Collect人工规划 input at cycle end,供智能进化使用

---

## Data-Driven Template (Cycle N+1, N≥2)

### Data-Driven Morning Template
```
"Based on {{cycle_number}} weeks data: you typically have higher energy on [Day_of_week] (avg {{avg_energy_day}}), encounter barriers with probability [[ ]]% in [Task_type]. Today plan is [Task Name],建议 start from [Time Slot] to improve success rate."
```

**Use case**: Generate个性化启动建议 based on historical patterns

---

## Template Variables

- `{{last_night_energy}}`: Yesterday evening energy score (1-5)
- `{{avg_energy_m1_m2}}`: Avg energy of first 2 days
- `{{avg_energy_day}}`: Historical avg energy for specific weekday
- `{{common_barrier_type}}`: Historical problem pattern identification type
- `{{plan_completion_pct}}`: Today plan completion rate percentage

---

*Templates dynamically called by skill based on state, not fixed output*
