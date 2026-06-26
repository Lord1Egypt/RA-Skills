# Activity Stream (Feed)

Use this file for the Bitrix24 news feed — posting, reading, commenting, and sharing messages in the company feed.

Scope: `log`

## Core Methods

- `log.blogpost.get` — read feed posts (filter by `POST_ID` or `LOG_RIGHTS`)
- `log.blogpost.add` — post a message to the feed
- `log.blogpost.update` — update a feed post
- `log.blogpost.share` — add recipients to an existing post
- `log.blogcomment.add` — add comment to a feed post
- `log.blogcomment.user.get` — get comments by user for a post

Also related (CRM-specific):

- `crm.livefeedmessage.add` — post to CRM entity feed

## Recipients (DEST / LOG_RIGHTS)

Feed messages use recipient codes:

- `UA` — all authorized users
- `U<id>` — specific user (e.g. `U1`, `U42`)
- `SG<id>` — workgroup/project (e.g. `SG15`)
- `DR<id>` — department including subdepartments (e.g. `DR5`)

Default recipient: `['UA']` (everyone).

## Common Use Cases

### Read recent feed posts

```bash
python3 scripts/bitrix24_call.py log.blogpost.get --json
```

### Read a specific post

```bash
python3 scripts/bitrix24_call.py log.blogpost.get \
  --param 'POST_ID=755' \
  --json
```

### Read posts visible to a specific group

```bash
python3 scripts/bitrix24_call.py log.blogpost.get \
  --param 'LOG_RIGHTS=SG15' \
  --json
```

### Post a message to the feed

```bash
python3 scripts/bitrix24_call.py log.blogpost.add \
  --param 'POST_MESSAGE=Hello team!' \
  --param 'DEST[]=UA' \
  --json
```

### Post to a specific department

```bash
python3 scripts/bitrix24_call.py log.blogpost.add \
  --param 'POST_TITLE=Department Update' \
  --param 'POST_MESSAGE=Monthly results are ready.' \
  --param 'DEST[]=DR5' \
  --json
```

### Post to a project group

```bash
python3 scripts/bitrix24_call.py log.blogpost.add \
  --param 'POST_MESSAGE=Sprint review tomorrow at 10:00' \
  --param 'DEST[]=SG15' \
  --json
```

### Add a comment

```bash
python3 scripts/bitrix24_call.py log.blogcomment.add \
  --param 'POST_ID=755' \
  --param 'TEXT=Great work!' \
  --json
```

### Share a post with additional recipients

```bash
python3 scripts/bitrix24_call.py log.blogpost.share \
  --param 'POST_ID=755' \
  --param 'DEST[]=U42' \
  --json
```

## Working Rules

- `log.blogpost.get` without `POST_ID` returns recent posts for current user.
- Posts are visible only to specified recipients. Use `DEST` to control visibility.
- Comments inherit visibility from the parent post.
- `IMPORTANT=Y` flag makes a post pinnable with an optional expiration date.

## Good MCP Queries

- `log blogpost add get`
- `log blogcomment`
- `crm livefeedmessage`
