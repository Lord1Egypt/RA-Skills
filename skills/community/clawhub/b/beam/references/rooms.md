# Beam Rooms reference

A Room is a private group of members that exchange messages, byte streams,
datagrams, media and files over typed channels, with roles and per-channel
grants. Members are machines running the Beam agent, object-storage buckets
attached from Studio, and browsers through a Web Agent.

The `beam` CLI drives the agent on this machine over a local socket and starts it
when needed. Run `beam help room` for the full syntax of the installed version.

## Conventions

- Pass `--json` on every command. Success prints one JSON value on stdout.
  Errors print `{"error":{"code":N,"message":"…","hint":"…"}}` on stderr, with a
  `kind` field when the error has a specific cause. `--quiet` prints only the
  main ID.
- Use the room-first form, `beam room ROOM …`. Older spellings take arguments in
  inconsistent orders.
- Global flags are recognized anywhere in the arguments, even where a value was
  meant (`--literal -v` loses its value). Write values that start with `-` as
  `--flag=value`, or send payloads with `--stdin`.
- Some bad states still exit 0: `beam agent status` when stopped, `beam doctor`
  when unhealthy, and an empty `beam room list`. Read the JSON fields.
- Invitation tokens and media bearer tokens are secrets. Never print them; use
  `invite --out FILE` and hand media tokens only to the user.

## Set up this machine

```bash
beam agent connect --json          # enrolls with BEAM_API_KEY from the environment
beam agent status --json           # expect a registered, connected agent
beam doctor --json                 # diagnose; `beam doctor --fix` repairs what it can
```

A machine that joined only through an invitation cannot create Rooms.

Each OS user runs its own agent. Agents bind `127.0.0.1:8621` for Room data, so
a second user's agent on the same host fails to start ("Could not start" the
agent); `~/.beam/agent.log` then shows `address already in use`. Set
`BEAM_TUNNEL_ROOM_DATA_ADDR=127.0.0.1:<free port>` for that user. If `room join`
fails this way, check `beam room list --json` before retrying: the membership may
already exist and the one-use invitation may be spent.

## Create, inspect, close

```bash
beam room create --json --idempotency-key <stable-key>   # 1 credit, charged to BEAM_API_KEY
beam room list --json [--state active|closed|all]
beam room ROOM show --json
beam room ROOM member list --json
beam room ROOM close --json
```

Creating a Room needs an API key whose role grants `rooms:start`. Reuse the same
`--idempotency-key` on a retry so only one credit hold is taken.

## Channels and grants

```bash
beam room ROOM channel create --json --name events --kind message
beam room ROOM channel list --json
beam room ROOM channel CHAN grant put --json --subject-type member --subject MEMBER --actions discover,subscribe
beam room ROOM channel CHAN grant list --json
```

- Kinds: `message`, `stream`, `datagram`, `request-reply`, `object`, `media`.
- Channels are `restricted` by default. A member needs `discover` to see one,
  plus `subscribe` to receive and `publish` to send. `grant put` **replaces** the
  member's action list, so include the actions it already has.
- Grant commands need `manage` on the channel or the Room owner role.
- Roles: `beam room ROOM role create --name NAME`, then
  `beam room ROOM role assign ROLE MEMBER`.

## Invite anyone

One invitation works for any party: another AI agent such as an OpenClaw or
Hermes agent, a person running the `beam` CLI, or a bare machine. The invitee needs no Beam
account; joining gives its machine an identity that can use the Room but cannot
create Rooms of its own.

1. **Decide what the invitee may do.** Grant only the channels it needs, and the
   fewest actions: `discover` plus `subscribe` to receive, `publish` to send,
   `manage` only for a party trusted to administer the channel. A shared role
   (`--role`) suits several invitees with the same access.
2. **Create a one-use invitation into a private file.** The token is a bearer
   secret: never print it, paste it into a chat, or commit it.

   ```bash
   beam room ROOM invite --json \
     --channel-access JOBS=discover,subscribe --channel-access RESULTS=discover,publish \
     --max-uses 1 --ttl 900 --out invitation.token
   ```

   If the invitee already has a Beam identity, bind the invitation to it with
   `--agent AGENT_ID` (or `--principal PRINCIPAL_ID`), so a leaked token is
   useless to anyone else. Raise `--ttl` (seconds) when the invitee will not join
   within 15 minutes.
3. **Deliver the file over a private channel** the user approves: an existing
   Room channel both sides are already in, an encrypted file transfer, or the
   invitee's operator. Tell the user who receives it.
4. **The invitee joins** (its own agent with this skill runs the same command):

   ```bash
   chmod 600 invitation.token
   beam room join ROOM --invitation-file invitation.token --json
   ```

   `join` creates the machine identity if needed, restarts the agent and waits
   for the Room to appear. Delete the file afterwards.
5. **Confirm and manage access** from the inviting side:

   ```bash
   beam room ROOM member list --json             # the new member and its presence
   beam room ROOM invitation list --json         # unused invitations
   beam room ROOM invitation revoke INVITATION   # cancel one before it is used
   beam room ROOM member remove MEMBER           # remove a member later
   ```

A Room needs at least two members for messages to flow: a member publishing
alone gets `channel_no_recipient`. Invite the second party before relying on
`publish`.

Invite only parties the user has approved, and only through their operators.
Never send invitations to agents or machines whose owners have not agreed to
join; a member uses its own compute and model credits for the work it does.

## Messages

```bash
beam room ROOM channel CHAN listen --json                       # runs until stopped; one JSON object per message
beam room ROOM channel CHAN publish --json --literal '{"ready":true}'
printf '%s' "$PAYLOAD" | beam room ROOM channel CHAN publish --json --stdin   # up to 1 MiB
```

Delivery is live only by default (`--retention none`): only members listening
when a message is published receive it. **Start `listen` first.** For a channel
created with `--persistence-modes none,sender_local,receiver_local` and positive
`--persistence-max-bytes` and `--persistence-max-age`, publish with
`--retention sender_local` and listen with `--retention receiver_local`.

## Streams and datagrams

```bash
beam room ROOM channel CHAN stream listen > received.bin
producer | beam room ROOM channel CHAN stream publish
beam room ROOM channel CHAN datagram send --literal "event" --ttl-millis 5000
beam room ROOM channel CHAN datagram listen
```

A stream has no declared size: `publish` reads stdin until it closes, and
`listen` writes raw bytes to stdout. A datagram carries at most 1,008 plaintext
bytes. Concurrent publishers on one stream channel interleave, so use one channel
per publisher.

Beam Workers serve streams, end-to-end encrypted with the channel's key: a
Worker never sees the plaintext. Start `listen` before `publish`; a member that
starts listening later does not receive the running stream. `listen` exits
non-zero if the stream was cut short, even after writing part of it; treat that
output as incomplete. Every member needs a current CLI and agent (`beam update`).

## Files (object channels)

```bash
beam room ROOM channel CHAN object publish --json --file ./artifact.bin --follow
beam room ROOM channel CHAN object publish --json --from BUCKET_MEMBER --object-key path/obj.bin \
  --to AGENT_MEMBER --to OTHER_BUCKET_MEMBER --follow
beam room ROOM channel CHAN object watch PUBLICATION
beam room ROOM channel CHAN object cancel PUBLICATION
```

- The file must be a regular, non-empty file.
- Every recipient must finish unless you pass `--allow-partial`. With
  `--follow`, a failed, cancelled, expired or rejected publication exits non-zero.
- A publication between agents only is end-to-end encrypted (MLS). If it
  includes any bucket, every leg uses TLS and workers can read the plaintext,
  including on the agent legs. Warn the user before adding a bucket to
  confidential data.

## Media (WHIP in, WHEP out)

```bash
beam room ROOM channel CHAN media publish --json --as studio-cam   # WHIP URL + bearer for an encoder such as OBS
beam room ROOM channel CHAN media list --json
beam room ROOM channel CHAN media view --json [--session WORKLOAD | --all]
beam room ROOM channel CHAN media stop WORKLOAD
```

Each publisher name has its own stable URL and token. Viewing needs `subscribe`
(plus `discover` on a restricted channel).

Without OBS, ffmpeg 8 or later publishes over WHIP. Save the `media publish
--json` output to a file, read `whip_url` and `token` from it, and never print the
token:

```bash
ffmpeg -re -i input.mp4 -c:v libx264 -profile:v baseline -tune zerolatency -bf 0 \
  -c:a libopus -ar 48000 -ac 2 -f whip -authorization "$TOKEN" "$WHIP_URL"
```

On the receiving member, `media view --json --sdp` republishes the stream as RTP
on loopback and returns an SDP URL. Record from it with
`ffmpeg -protocol_whitelist file,udp,rtp,http,tcp -i <sdp url> -t 15 -c copy out.mkv`,
then `ffprobe -count_frames out.mkv` to confirm frames arrived.

## Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | Success |
| 2 | Invalid command or argument |
| 3 | Configuration or credential storage problem |
| 4 | Missing or expired authentication, or permission denied |
| 6 | The local agent is unavailable (`beam agent start`, `beam agent repair`) |
| 7 | CLI and agent versions differ (`beam update`) |
| 8 | Not found |
| 9 | Conflict |
| 10 | Operation failed |

## Error kinds worth recognizing

| `kind` | What to do |
| --- | --- |
| `room_api_key_required` | Set `BEAM_API_KEY` |
| `room_api_key_permission` | Use a key whose role grants `rooms:start` |
| `room_credit_required` | The key or organization cannot pay; the user checks the Console |
| `room_create_requires_account_agent` | Joined by invitation; `beam agent disconnect`, then `beam agent connect` |
| `channel_not_visible` | Wrong channel ID, or missing `discover` grant |
| `channel_permission_denied` | Missing `publish` or `subscribe` grant |
| `channel_not_ready` | Encryption setup still converging; retry shortly, then follow the hint |
| `mls_no_manager_agent`, `mls_managers_offline` | No online member agent holds `manage` on the channel; a Room owner grants it |
| `channel_listen_closed` | `listen` ended before any message: missing `subscribe`, or channel not ready |
| `channel_no_recipient`, `channel_not_delivered` | Nobody was listening; start `listen` first or use local retention |
| `channel_delivery_failed` | A listener could not take the message; publish again, then check `beam agent logs` on that machine |
| `coordinator_timeout`, `coordinator_unreachable` | Retry; check `beam agent status` and network access |
| `agent_capability_unavailable` | A member's agent is too old for the operation, such as a stream; `beam update` on that machine |
| `worker_capability_unavailable`, `stream_renewal_failed`, `channel_setup_timeout` | No Beam Worker could serve it; Beam-side, so retry later and tell the user rather than looping |
| `no_active_targets` | Every stream receiver dropped out, usually because none was listening; start `listen` first |
| `stream_truncated`, `stream_key_unavailable` | The stream ended incomplete, or its encryption key was not ready; retry, and listen before publishing |
