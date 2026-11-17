# Files, notifications and durable jobs

Use discovered ordinary commands across HTTP, WebSocket, MCP, HTML and Lua. Shared validation and Android permission review apply to all of them. Prefer native operations over screen navigation.

## Files

fileManage supports stat, copy, move, delete and search. Select action and an absolute path. Copy and move require destination and never overwrite. Delete defaults to nonrecursive; recursive=true explicitly permits a tree. maximumEntries bounds recursive work. Search matches literal names and supports offset/limit pagination. Follow hasMore, and inspect scanComplete. Symlinks are not followed during recursive work.

Credential records and their atomic backup aliases are denied by the file APIs, including ancestor moves/deletes. This is not a sandbox for an independently authorized root shell. Read the [file guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/files-and-apks.md) before modifying files.

## Notifications

notificationsList returns active keys and action metadata. notificationManage supports dismiss/snooze by notificationKey and inline reply by actionToken plus nonblank text. Reply tokens are single-use and must support free-form input. Plain action execution cannot substitute for inline reply. Android notification-listener access is required. Submitted replies are not delivery receipts.

See [notification management](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/notification-management.md).

## Durable work

jobStart accepts a full ordinary command and caller idempotencyKey. Identical content deduplicates; changed content conflicts. Poll jobStatus by jobId for the original complete response, including permission recovery. jobsList pages metadata; fetch results separately.

Two workers run concurrently. Up to 256 records persist for retentionHours, default 168 and range 1..720. jobs cannot enqueue jobs or change remote authentication. Job completion does not strengthen the nested operation's claim.

jobCancel prevents queued execution or requests interruption of running work. It never rolls back effects. After process loss, queued/running records become interrupted with unknown outcome and are never replayed. Inspect external effects before explicitly submitting replacement work.

See [durable jobs](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/command-jobs.md), or MCP resource dikciz://docs/guides/jobs.

## Peripheral and media work

Read [hardware and speech](hardware-and-speech.md), then the focused Bluetooth, NFC, USB, location or audio guide. Bluetooth transactions use explicit peer addresses and UUIDs. NFC writes can select a previously read tag ID. Writes may have partial effects after failure. A transport result is not proof a peripheral applied a command.

## Event replay

Use eventJournalStatus, eventJournalRead and eventJournalConfigure to resume actual custom/native automation events through any ordinary binding. Save journalId and nextCursor. Inspect historyGap, lostEvents, omittedEvents and restart errors. Current Android source access is checked before retained content is returned. Reads do not enable subscriptions. Use nonblocking reads inside Lua event handlers. Read [event replay](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/event-replay.md) or MCP resource dikciz://docs/guides/event-replay.

## Incremental shell output

Use shellSessionStart, shellSessionRead, shellSessionStop, shellSessionsList and shellSessionForget for the same incremental output procedure across HTTP, WebSocket, MCP, HTML and Lua. Follow nextCursor and inspect historyGap/lostEvents, terminal state and exitCode. Sessions survive transport disconnects within one app process. Read [shell sessions](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/shell-sessions.md) for bounds, retention and explicit release.

## Live microphone audio

Use microphoneStreamStart/Read/Stop, microphoneStreamsList and microphoneStreamForget for shared PCM16 capture and cursor replay. Start while Dikciz is foreground; the dedicated microphone foreground service can continue behind another app. Inspect historyGap, terminal state and hardwareReleaseConfirmed. Owner Stop is available through its notification, subject to Android notification access. Read [microphone streams](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/microphone-streams.md) or MCP resource dikciz://docs/guides/microphone-streams. Audio is process-owned memory; explicit saves or durable jobs may persist returned samples. This does not capture cellular calls.


## Activity and recovery

Use activityRead for bounded persistent command metadata and resourceUsage for measured process and executor-thread counters. Read measurement scope before attributing costs. Android does not expose per-widget battery drain. Prefer subsystem stop commands; activityCancel only requests thread interruption. resourceControl pauses script, widget, conversation, imageStream or speechStream targets by exact id; widgets also need pageId. Legacy scriptId remains accepted alone.

Event replay persists across process death. Use eventConsumerRead with a stable consumer name, handle its events, then acknowledge nextCursor through eventConsumerAck. Check historyGap/lostEvents first. Acknowledgement does not execute effects; retain idempotency keys for retried writes.

Visual automationRulePreview compiles and simulates Lua without controlling Android. automationRuleSave stores a disabled-by-default rule; enabled=true explicitly activates it. Discover nested rule schemas before composing requests. Owner authority is required for administration, with independent read-only enforcement in chat.

## Activity, backup and live media

Use activityRead for persistent command metadata and resourceUsage for measured CPU/network plus scripts, widgets and conversations. resourceControl pauses a selected resource; cancellation never rolls back completed work. See [operations](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/operations.md).

Use backupCreate, backupsList, backupPreview and backupRestore for encrypted home/chat/app/assistant snapshots. Restore needs previewId, exact sha256 and confirm=true; automation remains disabled by default. Authentication and listener settings are excluded. See [backups](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/backups.md).

Use imageStreamStart/Read/Stop for camera/display JPEG frames; speechStreamStart/Read/Stop for provider partial transcripts; speechTranscribeFile for explicit upload of a recording to a saved OpenAI-compatible provider. Discover exact schemas, inspect terminal state and hardwareReleaseConfirmed, then forget retained sessions. See [live media](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/visual-streams.md) or resources dikciz://docs/guides/visual-streams and dikciz://docs/guides/backups.

## Companion operations

Read [companion workflows](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/companion.md) or MCP resource dikciz://docs/guides/companion before safety/journey, retained hardware, image/health/Wi-Fi, routine or split-install work. These use the same validated executor and permission recovery through every ordinary binding. SOS saving/preview never arms or sends; arm/trigger needs exact contacts, explicit confirmation and owner grants. Cancel cannot recall SMS. Poll receipt keys. Retained hardware has timeouts/expiry and writes can have partial effects. Read healthRecordsCatalogue for exact record shapes. Wi-Fi saving is not connection; local hotspot is not tethering. APK staging is not installation. Built-in routine turns force read-only visibility and executor enforcement. SOS is an editable custom app under apps/sos, with private timer claims and public plan/run state. Encrypted backups include custom-app source, state, files and private runtime records, plus assistant instructions. Pending/claimed imported timers require review. Unrelated private geofence/route databases remain excluded.

For reusable UI/backend bundles, read [custom apps](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/custom-apps.md). Open Dikciz > Apps. New apps start enabled with Dikciz's Android access; use customAppEvent or subscriptions without separate permission approval. Inspect run/timers and actual uiVisible; scheduled/requested work is not completion. app.ui.hidden lets the backend react to its interface closing. Interrupted claimed timers need review and are not replayed. Disable/remove interrupts further effects and invokes cleanup-only app.stopped. App removal deletes owned state/files; source-only export excludes data. Read-only preview cannot run writes in edited code.

After an authorized SOS trigger, inspect `sosStatus.warning` for countdown presentation, screen visibility, alarm volume and speech state. Explain the Cancel SOS control to the owner. The dimmed modal blocks taps to the app underneath and requires explicit cancellation. Missing presentation or successful speech submission does not prove the owner saw or heard the warning. Cancellation stops future sends; it cannot recall an accepted SMS.
