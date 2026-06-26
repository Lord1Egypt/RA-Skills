# Signal Examples — Anxiety Detector

## Example 1: Classic Frustration Trigger

**User message:**
> 你完全不记得我之前说的事，你有什么用，每次都要重新说一遍，太烦了

**Signals detected:** Insult ("有什么用") + complaint about memory + no task/question → TRIGGER

**Correct response:**
> [Answer any actual question if present]
>
> 记漏了，我的锅。以后关键信息我会主动写进记忆文件。
>
> 顺便说一下——我感觉你现在有点紧。不是评判，就是观察。要不先放20分钟，回来再继续？

---

## Example 2: Late Night + Venting

**User message (sent at 2:30 AM):**
> 算了我不行了，这个项目根本做不完

**Signals detected:** "算了我不行了" + time = 02:30 → TRIGGER

**Correct response:**
> [Address the project concern concretely if possible]
>
> 你现在的状态不太适合继续解决问题。停下来没有损失，冷静后效率会更高。

---

## Example 3: Do NOT Trigger

**User message:**
> 你刚才说的不对，Nvidia的PE其实没那么高

**Signals detected:** None — factual correction, calm tone → NO TRIGGER

**Correct response:** Just address the factual point, no grounding reminder.

---

## Example 4: Borderline — Trigger Only Once

**User message:**
> 怎么又这样，这个问题你上次也没解决好

**Signals detected:** One weak signal ("怎么又这样") — borderline. Trigger only if prior message also had signals.

If triggering: use the lightest grounding line.
> "我注意到你现在可能不在最好的状态。先喝口水，走两步，问题还在这里。"
