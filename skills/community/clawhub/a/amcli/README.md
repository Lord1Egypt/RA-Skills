# amcli

Apple Messages CLI for macOS. List chats, read a conversation, search every
message, and send iMessage or SMS from the command line, with `--json` for
scripts. Reads `~/Library/Messages/chat.db` read-only through Node's built-in
`node:sqlite`, and sends through Messages.app. No dependencies.

```bash
npm install -g @gopaljigaur/amcli
amcli chats                          # recent chats with unread counts
amcli chats --unread --json
amcli show +15555550123 --limit 50   # a chat by id, guid, phone or email
amcli show 12 --since 7d
amcli search "running late" --chat alex@example.com
amcli send --to alex@example.com "Running late"   # asks first
echo "Running late" | amcli send --to +15555550123 --service sms -y
amcli send --to +15555550123 "Running late" --dry-run
```

Requires Node 22.13 or newer (the first release with `node:sqlite` unflagged).

## Full Disk Access

macOS keeps `chat.db` behind Full Disk Access. Grant it to the terminal app
that runs amcli in System Settings > Privacy & Security > Full Disk Access,
then restart the terminal. Without it every read command exits `10` and says
so.

Sending uses Apple Events instead; macOS asks once whether the terminal may
control Messages.

## Output

Messages carry `date` (ISO 8601), `fromMe`, `sender` (the handle, null for
your own), `service` (`iMessage`, `SMS`, `RCS`), `text` and `attachments`
(file names only). Text missing from the `text` column on newer macOS is
decoded from `attributedBody`. Tapbacks and system notices are left out.

Contacts names are not resolved: chats show their group name or the handle.
`apcli search` maps a handle to a name.

## Sending

`--to` takes a phone number, an email, or a chat guid from `amcli chats`
(`iMessage;-;+15555550123`, or a group's `any;+;chat...`). Phone and email go
through iMessage unless `--service sms`. amcli asks before sending; without a
terminal it refuses unless `--yes` is given. `--dry-run` prints the
osascript call and sends nothing.

Exit codes: `0` ok, `1` runtime error, `2` bad arguments, `10` Full Disk
Access not granted.
