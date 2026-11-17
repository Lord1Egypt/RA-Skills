# When to use ABS — task catalog

Use ABS when the user's request is about running operations or a business the lean / operational-excellence way
and an answer grounded in ABS materials is more useful than general knowledge. If the user says "use ABS",
"查 ABS", "问 ABS" or similar, always use it.

## 1. Look up a method or tool → `search`, then `card`

| User says (中文) | User says (English) |
|---|---|
| 5S 审核怎么打分？ | How is a 5S audit scored? |
| SMED 换型时间怎么压？ | How do I cut changeover time with SMED? |
| 标准作业三张表是哪三张？ | What are the three standard work forms? |
| 安灯升级时限一般怎么定？ | How should andon escalation times be set? |
| 看板张数怎么算？ | How many kanban cards do I need? |
| 保龄球图的黄色是什么意思？ | What does yellow mean on a bowler chart? |

Search first; if one tool card is clearly the subject, read it with `card <id>` (the `id` is in the search result)
to get its definition, steps and the exact decision rules / formulas.

## 2. A question that needs a sourced answer → `ask`

| 中文 | English |
|---|---|
| 新产线的节拍和配员怎么算？给我出处 | How do I set takt and staffing for a new line? Cite the source |
| 改善周的基线应该取什么数？ | What baseline should a kaizen event use? |
| OEE 多少算世界级？ | What OEE is world class? |
| 问题解决的九步是哪九步？ | What are the nine steps of problem solving? |

`ask` answers only from the ABS knowledge base and marks each claim with a source. Keep those citations.

## 3. Learn → `courses`, `course`

| 中文 | English |
|---|---|
| 中层管理者该学哪门课？ | Which course suits a middle manager? |
| 我学到哪了？ | Where am I in my courses? |
| 讲讲快速换型这门课的第 3 课 | Walk me through lesson 3 of the SMED course |
| 出几道题考考我 | Quiz me on this lesson |

`course <id>` returns each lesson's objective, points, practice task and knowledge-check question.
To quiz the user, ask the check questions one at a time and explain the answer from the lesson points.

## 4. Plan → `plan`

| 中文 | English |
|---|---|
| 下周一开一场改善周，提升 L1 线的一次合格率 | Run a kaizen week next Monday to raise first-pass yield on line 1 |
| 给中层做一期精益培训，三个月 | A three-month lean training program for middle managers |
| 导入日常管理，先从两条线试点 | Roll out daily management, piloting on two lines |
| 招一位精益总监 | Hire a lean director |

One sentence is enough; add the goal, scope and start date if the user gave them (`--start YYYY-MM-DD`).
The plan is a **draft** in ABS: phases, steps, a dated schedule (Gantt), forms and sources. The user reviews and
submits it in ABS. Read-only accounts cannot plan (HTTP 403).

## 5. Diagnose → `diagnose`

| 中文 | English |
|---|---|
| 为什么日产总是完不成？（附小时产量表） | Why do we keep missing daily output? (hourly output attached) |
| 看看这张现场照片，5S 做得怎么样 | How is 5S in this shop-floor photo? |
| 这份月度经营报告反映了什么问题 | What problems does this monthly report show? |
| 我们的交付准时率一直在 85% 左右，从哪下手 | On-time delivery is stuck around 85% — where do we start? |

Files: xlsx, csv, pdf, docx, txt, md or an image, up to 5 MB. Ask before sending confidential material.
Add `--save` if the user wants it kept in their ABS diagnosis records.

## Do not use ABS for

General programming, travel, shopping, chit-chat, or when the user explicitly wants your own view without ABS.
If ABS returns nothing relevant, say so; do not present general knowledge as coming from ABS.
