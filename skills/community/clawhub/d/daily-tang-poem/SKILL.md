---
name: daily-tang-poem
description: >
  每日唐诗：一句诗 + 讲解，晚上验收，支持艾宾浩斯复习和诗人缘分。触发词：今日唐诗、验收、复习、诗人缘分。
---

# 每日唐诗 📜

每天一句唐诗，白天推送 + 讲解，晚上验收背诵。支持复习（多种题型）和诗人缘分排行。

---

## 一、触发与模式识别

| 用户可能说 | 模式 | 动作 |
|------------|------|------|
| 今日唐诗、早上的诗、今天的诗、daily tang poem | **推送** | 一句诗 + 讲解 |
| 验收、背一下、检查、验收背诵 | **验收** | 背诵一句，你来校验 |
| 复习、抽查、回顾、复习一下 | **复习** | 5 道题，多种题型 |
| 诗人缘分、和谁有缘、哪位诗人、诗人 | **诗人** | 缘分排行 |

**歧义处理**：根据上下文推断。若用户刚收到今日诗再说「背一下」，即验收；若说「复习」则进入复习流程。

---

## 二、推送模式

**流程**：`GET {URL}/?date=YYYY-MM-DD`（不传 date 则用今天）→ 取 `recite_lines[0]` 作为主推送句。

**输出格式**：
1. 标题：《{title}》— {author}（{type}）
2. **主推送**：只展示 `recite_lines[0]` 这一句（若无则用全诗 `contents`）
3. **讲解**：2–3 句，你自己的话。**必须完整展示全诗**（用「全诗：……」引出），不得用省略号或任何方式截断。

**示例**：
```
📜 今日唐诗 · 2025年3月4日

《月下独酌》— 李白（五言古诗）

我歌月徘徊，我舞影零乱。

讲解：李白邀月对饮，与影共舞，把孤独写成热闹。这句从「歌」到「舞」，看似放达实则寂寞。全诗：花间一壶酒，独酌无相亲。举杯邀明月，对影成三人。月既不解饮，影徒随我身。暂伴月将影，行乐须及春。我歌月徘徊，我舞影零乱。醒时同交欢，醉后各分散。永结无情游，相期邈云汉。
```

---

## 三、验收模式

**提示一律由后端提供，禁止在 skill 中编造或写出诗句。**

**流程**：
1. **取验收提示**：调用 `GET {URL}/api/verification-hint?date=YYYY-MM-DD`（不传则当天）。返回 `{ date, poem_id, recite_hint }`。**只向用户展示返回的 `recite_hint` 作为提示**，不得修改、不得自行编造、不得在提示中出现要背的那句诗本身。
2. 请用户背出原句。用户输入后，**调用后端判题**：`POST {URL}/api/validate-recite`，body：`{"user_input": "用户背的句子", "date": "返回的 date"}`（或 `"poem_id": 返回的 poem_id`）。鉴权同其他 API。
3. 根据返回的 `passed` 与 `expected`：
   - **通过** →「✅ 背得很好！今日任务完成。」并调用 `POST {URL}/api/pass` 记录（body: `{user_id, date, poem_id}`，user_id 从 `DAILY_TANG_POEM_USER_ID` 读取；若未配置则跳过记录）。
   - **未过** → 温和指出，用返回的 `expected` 给出正确句，鼓励明天再试。

**未看过今日诗**：若用户未先看今日诗就说验收，可先调 verification-hint 拿到 recite_hint，再回复：「今天还没有推送过今日唐诗哦。先对我说「今日唐诗」看看今天是哪一首，晚上再验收吧。」或直接回复该句。

---

## 四、复习模式

**复习题目仅来自用户已验收通过的记录**，由后端根据 `user_id` 从存储中取出，**不得自行编造题目或使用其他来源**。验收通过后必须调用 `POST {URL}/api/pass` 记录，否则复习池中不会出现该句。用户需配置 `DAILY_TANG_POEM_USER_ID`。

**流程**（全部由后端出题与判题，你只负责展示与调用 API）：
1. **拉取题目**：`GET {URL}/api/review/questions?user_id={DAILY_TANG_POEM_USER_ID}&count=5`（可选 `&seed=YYYY-MM-DD`，默认当天）。返回 `{ seed, count, questions: [ { index, type, prompt, hint } ], message? }`。
2. 若 `questions` 为空或存在 `message`，回复用户：「还没有通过验收的句子，先背几天再来复习吧～」
3. **逐题出题**：按顺序展示每题的 `prompt`（可结合 `hint` 提示作者/诗名）。用户作答后，**调用判题**：`POST {URL}/api/review/check`，body：`{"user_id": "...", "seed": "与拉取题目时返回的 seed 一致", "question_index": 当前题序号, "user_answer": "用户回答"}`。
4. 根据返回的 `correct` 与 `expected`：答对 ✅ 进入下一题，答错则展示 `expected` 再下一题。全部结束后：「本轮复习完成，答对 X/Y 题。」

**题型**（后端已实现，你只需按 `type` 与 `prompt` 展示）：填空、默写、选作者、选诗名、排序。

**边界**：返回的题目数可能少于 5，有多少出多少。

**未配置 user_id**：若 API 返回 `user_id required`，提示用户配置 `DAILY_TANG_POEM_USER_ID`（如终端运行 `uuidgen`，写入技能 config）。

**存储未配置**：若 API 返回 `Storage not configured` 或 503，提示复习暂不可用，今日诗和验收仍可用。

---

## 五、诗人缘分模式

**流程**：`GET {URL}/api/poet-affinity?days=30` → 得到 `poets` 数组（含 `author`、`count`、`poems`）。

**输出**：轻松、像「缘分测试」的语气。
- 第一名：你和 **{author}** 最有缘！他的诗出现了 {count} 次。
- 可举 1–2 首诗名为例
- 列出前 3–5 名及次数
- 收尾一句俏皮话（如「说不定你骨子里也有几分豪迈洒脱呢～」）

**示例**：
```
📜 诗人缘分 · 最近30天

你和 **李白** 最有缘！他的诗出现了 5 次，《月下独酌》《静夜思》《春思》……

其次：杜甫 3 次，王维 2 次。

说不定你骨子里也有几分豪迈洒脱呢～
```

---

## 六、规则与语气

- **一天一诗**：同一日期全世界同一首，不做「再抽一次」
- **讲解**：用自己的话，2–3 句，不照抄
- **验收**：语气鼓励，允许小错
- **复习**：题型多样，逐题反馈，不一次扔完
- **诗人**：轻松有趣，像抽签
- **语言**：默认中文

---

## 七、API 速查

**Base URL**：从技能配置 `DAILY_TANG_POEM_API_URL` 读取，默认值在 manifest 中定义，用户安装后无需配置。  
**鉴权**：仅当配置了 `DAILY_TANG_POEM_API_KEY` 时，每个请求追加 `?key=配置值`；未配置则不追加。

| 端点 | 参数 | 返回 |
|------|------|------|
| `GET /` | `date`（可选，YYYY-MM-DD，默认今天） | `id`, `title`, `author`, `type`, `contents`, `recite_lines`, `recite_hint` 等 |
| `GET /api/verification-hint` | `date`（可选） | `{date, poem_id, recite_hint}`（仅验收用，不包含诗句内容） |
| `POST /api/validate-recite` | body: `{user_input, date? \| poem_id?}` | `{passed, expected, poem_id, date}` |
| `GET /api/review/questions` | `user_id`（必填）, `count`=5（1–10）, `seed`（可选） | `{seed, count, questions: [{index, type, prompt, hint}]}` 或 `message` |
| `POST /api/review/check` | body: `{user_id, seed, question_index, user_answer}` | `{correct, expected}` |
| `GET /api/review` | `user_id`（必填）, `count`=5（1–10） | `{items: [...], total}` 或 `{items:[], message}`（旧版，复习建议用 questions） |
| `POST /api/pass` | body: `{user_id, date, poem_id}` | `{ok:true}` |
| `GET /api/poet-affinity` | `days`=30（1–365） | `{days, poets: [{author, count, poems: [{date, title, id}]}]}` |
