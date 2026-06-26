# Debug map

## If the DM request does not create a lane post

Suspect:

- controller trigger detection
- controller lane posting
- controller allowlist or channel configuration

## If the lane task appears but the worker bot does not answer

Suspect:

- worker runtime is down
- worker-side Discord plugin issue
- worker-side bot-authored message filter
- worker-side guild or channel binding mismatch

## If the lane answer appears but the DM does not receive the result

Suspect:

- controller-side final-result capture
- trusted-author filtering
- source metadata correlation
- DM send path not firing

## Common worker-side blocker

Many Discord worker plugins drop all bot-authored server-channel messages with a guard like:

```ts
if (msg.author.bot) return
```

If that is present, a controller bot can post into the lane successfully while the worker still ignores the message.

## Safe worker-side patch pattern

Do not remove the default bot guard globally.

Instead, add a narrow allowlist exception for:

- one trusted controller bot id
- one dedicated worker-lane channel id
- one canonical task prefix such as `[WORKER_TASK]`

## Common worker runtime mismatch

Some Discord runtimes expose the channel on `msg.channelId` instead of `msg.channel.id`.
If a narrow allowlist helper checks the wrong property path, trusted worker-lane messages can still be rejected.

## Common controller-side relay bug

Trusted worker final replies may arrive with initially empty content and require hydration before classification. If the controller computes text/bypass flags before hydration, a valid worker result can still be dropped before relay-back.
