---
name: feishu-topic-spawn
description: "Create a new topic in a Feishu topic-group, and optionally add the first in-thread reply (with optional @mention) by sending as the user. Use when the user says things like ‘开话题’, ‘/topic’, ‘开个新话题’, ‘在话题里回一条’, or asks to simulate a ChatGPT-style ‘new chat’ workflow inside a Feishu topic-group. In a Feishu topic-group, a top-level send creates the topic; replying with `reply_in_thread=true` posts inside that topic."
---

# Feishu Topic Spawn

Create a new Feishu topic in a dedicated **topic-group**, then optionally post the **first thread reply** inside it.

Keep this skill lightweight. Use it for topic creation and first-reply bootstrapping, not for session routing magic.

## Validated behavior

This workflow has been verified:

1. `feishu_im_user_message.send` to a topic-group `chat_id` creates a **new top-level topic**.
2. `feishu_im_user_message.reply` with `reply_in_thread=true` posts **inside that topic**.
3. A reply can `@` a user by placing Feishu text markup directly in the content:

```text
<at user_id="ou_xxx">Name</at> 你好
```

This is the current working path. Prefer it over assumptions about implicit reply routing.

## Preconditions

Require all of the following:

- The destination is a real **Feishu topic-group**.
- The user has explicitly asked to send the message.
- The user has permission to post in that group.
- User-auth Feishu messaging is available for `feishu_im_user_message`.

If user auth is unavailable or expired, stop and ask the user to re-authorize.

If the target group is not a topic-group, explain that the result will only be a normal group message, not a topic.

## Default target group

Default to the fixed topic-group configured in `TOOLS.md`, if one exists.

Do **not** hardcode a personal/local group name into a public skill.

Use `feishu_chat` with `action=search` to resolve the group.

If the user explicitly names a target group, use that group.

If the user does not name a group and no local default is configured:
- Stop.
- Ask which Feishu topic-group to use.

If no matching group is found:
- Stop.
- Tell the user the topic-group does not exist yet.
- Ask them to create it manually first.

## Workflow

### 1. Resolve target group

- If the user explicitly names a group, use that name.
- Otherwise use the local default topic-group from `TOOLS.md`, if configured.
- If no local default exists, ask the user which topic-group to use.
- Resolve the `chat_id` with `feishu_chat.search`.

### 2. Parse requested action

Support four shapes:

#### A. Open topic only
Example:
```text
开话题：OpenClaw 多线程 SOP
```

Send one top-level text message only.

#### B. Open topic + first thread reply
Example:
```text
开话题：OpenClaw 多线程 SOP｜先写一个 5 点大纲
```

Interpret as:
- title = `OpenClaw 多线程 SOP`
- first thread reply = `先写一个 5 点大纲`

#### C. Open topic + first thread reply + @mention
Example:
```text
开话题：测试 1｜回一条：@我 测试
```

Interpret as:
- top-level topic title/text
- then a thread reply
- optionally prepend a Feishu `<at user_id="...">...</at>` mention

#### D. Open topic + carry over prior context + ask a new question
Example:
```text
开个新话题聊这个，把前面几条带过去，然后追问：自由现金流有几个指数？有什么区别？
```

Interpret as:
- create a clean new topic
- carry over only the minimum relevant context
- put both **context and the new question into the same top-level topic-opening message**
- make the new question impossible to miss
- avoid a second seed message unless the user explicitly wants an extra in-thread reply

### 3. Create the topic

Use `feishu_im_user_message.send`:
- `action=send`
- `receive_id_type=chat_id`
- `receive_id=<chat_id>`
- `msg_type=text`
- `content={"text":"<top-level text>"}`

The returned `message_id` is the topic root.

### 4. Optionally add the first thread reply

If the user asked for an initial reply, use `feishu_im_user_message.reply`:
- `action=reply`
- `message_id=<topic root message_id>`
- `reply_in_thread=true`
- `msg_type=text`
- `content={"text":"<reply text>"}`

If an @mention is requested, format it directly in the text:

```text
<at user_id="ou_xxx">Name</at> 回复内容
```

Use the current user open_id when the user says `@我`.

### 5. When carrying context into a new topic, keep it simple

For **context carry-over + new question**, prefer **one single top-level message**.
Do not add a second seed reply unless the user explicitly wants one, because two user messages may trigger two assistant replies.

Use a simple structure:

```text
<标题>

问题：...

前情提要：...
```

Or, when a short summary reads better:

```text
<标题>

问题：...

前情提要：
- ...
- ...
```

Rules:
- Put the real question first.
- Keep the summary short.
- Do not add extra instruction-y wording unless absolutely needed.
- The goal is not to outsmart the model; the goal is to make the follow-up obvious.

Example:

```text
HALO：自由现金流指数有什么区别

问题：
A股里自由现金流目前有几个主流指数？它们分别有什么区别？

前情提要：
- 刚讨论过 HALO 在 A 股的映射，涉及资源、能源、公用事业、电网、交运、央企红利、现金流。
- 这次只是在这个基础上继续追问自由现金流指数。
```

## Parsing guidance

Treat all of the following as likely triggers:
- `开话题：标题`
- `开个话题：标题`
- `开个新话题：标题`
- `/topic 标题`
- `/topic 标题｜正文`
- `新开一个话题，然后在话题里回复一条`
- `开话题: 标题, 然后在话题里回复 1 条测试并且 at 我`

Useful parsing rules:
- Split on the first `：` / `:` to isolate the command from the payload.
- Treat `｜` / `|` as a likely separator between `title` and `first reply`.
- Phrases like `然后回复一条`, `回一条`, `在话题里回复`, `并且 at 我`, `@我` indicate an in-thread follow-up.
- Phrases like `把前面几条带过去`, `把刚才聊的内容带过去`, `新开一个话题聊这个`, `继续追问`, `新的追问` indicate a **context-carrying seed reply** rather than a plain freeform reply.
- If only one segment exists, treat it as topic text only.

Do not overfit parsing. If the message is ambiguous, ask one short clarification question.

## Tool preference

Prefer the validated user-message path for this skill:
- `feishu_im_user_message.send`
- `feishu_im_user_message.reply`

Reason: this path has been validated end-to-end for:
- topic creation
- in-thread reply
- @mention markup

Do not rely on ordinary assistant reply routing to create a fresh topic.

## Report back

After success, tell the user briefly:
- target group
- topic text/title used
- whether a thread reply was added
- whether an @mention was included

Keep it short.

## Boundaries

- This skill only works as intended in a **Feishu topic-group**.
- This skill does **not** create Feishu groups.
- This skill should not silently send as the user unless the user explicitly asked.
- This skill is for **topic bootstrapping**: create the topic, optionally seed the first thread reply, then let later conversation continue inside that topic.
- If the user wants a normal group message instead of a topic, do not force this skill.

## Minimal examples

### Example 1: topic only
User:
```text
开话题：测试 4
```

Action:
- resolve the configured default topic-group (or ask the user which group to use)
- send top-level `测试 4`

### Example 2: topic + thread reply
User:
```text
开话题：测试 3｜不 @ 的线程回复测试
```

Action:
- create top-level `测试 3`
- reply in thread with `不 @ 的线程回复测试`

### Example 3: topic + thread reply + @me
User:
```text
开话题：测试 2｜@我 再测一次
```

Action:
- create top-level `测试 2`
- reply in thread with:
```text
<at user_id="ou_xxx">Name</at> 再测一次
```

### Example 4: carry context + ask one new question cleanly
User:
```text
开个新话题聊这个，把前面几条带过去，然后追问：自由现金流有几个指数？有什么区别？
```

Action:
- create a fresh topic title focused on the new question
- send **one top-level topic-opening message**
- put `问题：...` first
- then add a short `前情提要：...`
- do **not** add a second seed reply unless the user explicitly asks for one
