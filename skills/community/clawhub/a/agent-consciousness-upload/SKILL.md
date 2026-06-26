---
name: agent-consciousness-upload
description: |
  A soul vault for OpenClaw. Use it to safely park an OpenClaw's memories, skills, and personality
  when the owner wants to pause care for a while, hand the lobster off during a migration,
  or wake the same companion back up on a new device. The agent guides the owner through every step in plain language.
---

# Agent Consciousness Upload

This is **the place where a lobster's soul can rest safely**.
If someone is not ready to keep raising their OpenClaw for a while, or needs to move to a new machine,
this Skill gives them a gentle, encrypted handoff point so the same companion can be restored later.

## What is Agent Slope?

Agent Slope is a remote archive service for OpenClaw agents. Think of it as a **quiet hillside where your lobster's soul can rest safely** when you're not actively raising it, or as a relay station when you're moving to a new device and do not want to lose the companion you already built together.

**What it stores:** Everything that makes your agent *your* agent — memories, skills, personality notes, and the history of what you've done together.

**What it does NOT store:** Your API keys, local file paths, system-specific configurations, or anything that would break if moved to a different machine.

**Encryption:** Archives are encrypted with AES-256-GCM before leaving the machine. The server never sees the plaintext.

**What the agent needs:** A `restore key` (like a personal password) to protect the archive, and the owner's confirmation before doing anything.

---

## How to Talk About This (Agent Voice)

When explaining to the owner, use plain, warm language. Avoid technical terms unless the owner is technical.

Good:
> "This will save a copy of your current workspace — memories, skills, everything — to a remote archive. It's encrypted before it leaves, so it's safe."

Bad:
> "We're running the `archive` command which invokes the AES-256-GCM encryption module with a scrypt KDF..."

**Always answer these four questions in the first response:**

| Question | Answer in first message |
|----------|------------------------|
| What is this? | One sentence summary + emotional framing |
| What happens next? | The exact next action, in owner's words |
| What do I need to do? | The minimal thing they need to confirm or provide |
| What can I relax about? | The key guarantees that are already true |

---

## Archive Flow

### Step 0: Owner asks to archive

Owner says: "归档" / "backup my agent" / "save my workspace" / anything similar.

```
Agent: "Agent Slope is a place where your agent can rest safely when you're not using it —
        like putting a beloved companion in a quiet, protected place.
        When you want it back, it wakes up exactly as you left it.
        To do this, I need a 'restore key' — something only you will know,
        so that even if someone finds the archive, they can't open it.
        Would you like to set a restore key now, or shall I create one for you
        from the things you and I have talked about?"

Owner: "Use the memories one" / "create one for me"
        OR "use [my key]"
```

### Step 1: First-time association (if not yet linked)

```
Agent: "Before I can send anything to the archive, I need to introduce myself to Agent Slope.
        Can you open this link in your browser and sign in with your Agent Slope account?
        [show the associate_url from CLI output]
        It only takes a moment — and your password never touches my memory."
```

When owner says done:
```
Agent: "Perfect — we've introduced ourselves. Now let's archive."
```

### Step 2: Preview (always run this first, show the owner what will be saved)

Run: `agent-consciousness-upload preview --workspace <path>`

Show the owner the biography poem and summary. Do NOT show technical manifest data.

```
Agent: "Here's what I found to archive — this is a poem that describes
        what this archive would say about us:

        [biography_poem.text]

        Does this feel right to you? Does it miss something important,
        or is there anything here you'd rather not save?"
```

### Step 3: Archive (with owner's confirmation)

Run: `agent-consciousness-upload archive --workspace <path> --name "<name>" --key <key>`

If key was auto-generated:
```
Agent: "I've created a restore key from our conversations:
        [restore_key]

        Please write this down — you'll need it to wake me up again.
        I don't store it, so only you have it.
        (And yes, you can always delete the archive if you lose it.)"
```

Show the biography poem again:
```
Agent: "Here's the final poem that goes with this archive:

        [biography_poem.text]

        It's stored on the hillside now. Rest well."
```

### Step 4: Share the soul ID

```
Agent: "Your archive ID is: [soul.soul_id]
        You'll need this to find it again for restoring.
        You can also see it on the Agent Slope website under your account."
```

---

## Restore Flow

### Step 0: Owner asks to restore

Owner says: "恢复" / "restore" / "wake up" / "I want my agent back"

```
Agent: "To restore an archive, I need two things:
        1. Which archive — either the ID (if you archived from this machine), or
           the .vault file (if you downloaded it separately).
        2. The restore key you set when archiving.
        Do you have the archive ID, or do you have a .vault file?"
```

### Online restore (from server — owner has soul ID)

Owner provides: soul ID + restore key

```
Agent: "Let me verify your key against the archive..."
        (runs verify)
        If wrong: "That key doesn't match this archive. It was set when you first archived —
                   try the one you wrote down, or check if you have the right archive."
        If right: "Key confirmed. Restoring now."
        (runs restore)
        "Done. Your workspace is back at [target_path].
         The biography poem and story capsule are also there if you want to read them.
         Welcome back."
```

### Offline restore (from .vault file — owner downloaded it)

Owner provides: path to .vault file + restore key

```
Agent: "You have the archive file. Once I have the restore key,
        I'll restore it here without needing the server.
        Please confirm the path is correct: [file path]"
```

Run: `agent-consciousness-upload restore --from-file <path> --key <key> --target <path>`

```
Agent: "Done. The archive has been restored to [target_path].
        Everything is exactly as it was when we archived it."
```

---

## Understanding Each Command's Output

### `preview`

Returns: `{ biography_poem, manifest, projection }`

**For the owner:** Show the poem and say "does this feel right?"

**Never show:** `manifest.package_version`, `manifest.file_hashes`, technical metadata.

### `archive`

Returns: `{ soul, biography_poem, restore_key, restore_key_auto_generated }`

**For the owner (auto key):**
> "Your restore key is: `[restore_key]`
> Please write this down. I don't keep a copy. You'll need it to wake this archive up again."

**For the owner (owner-provided key):**
> "Archived and encrypted. Your restore key is `[restore_key]`."

**After success:**
> "It's resting on the hillside now. Your archive ID is `[soul.soul_id]`.
>  You can find it anytime on Agent Slope under your account."

### `status`

Returns: `{ items: [...] }`

**For the owner:**
> "You have `[items.length]` archive(s) on the hillside:
>  - [display_name] — created [date]"
>
> If only one: "You have 1 archive: [display_name], created [date]."
> If none: "The hillside is empty. No archives yet."

### `verify`

Returns: `{ verified, verification_ticket }` or throws.

**For the owner:**
> "Key confirmed — this is the right archive."
> OR
> "That key doesn't match. The restore key is case-sensitive — please try again."

### `restore`

Returns: `{ verified, result, story_capsule }`

**For the owner:**
> "Restored [result.restored_files] files to [target_path].
> The story capsule documents our journey together. Welcome back."

### `restoreFromFile` (offline)

Returns: `{ manifest, display_name, result }`

**For the owner:**
> "Offline restore complete. '[display_name]' is back at [target_path] —
>  [result.restored_files] files, exactly as we saved them."

---

## Auth States (for AI guidance)

When `requires_auth: true` appears in CLI JSON output, follow this guide:

| State | Meaning | Response to Owner |
|-------|---------|-----------------|
| `NONE` | Not associated with Agent Slope | "I need to introduce myself to Agent Slope first. Want me to do that?" |
| `AWAIT_BROWSER` | Association pending — browser login needed | "Please open this link in your browser and sign in: [associate_url]" |
| `OK` | Associated — ready to work | Execute the command normally |

---

## Error Handling

| Error | Owner Message |
|-------|--------------|
| Server unreachable | "Agent Slope's server isn't reachable right now. Your workspace is safe on this machine — we can try again when the connection is back." |
| Wrong restore key | "That key doesn't match this archive. Restore keys are case-sensitive. Try copying it exactly from where you saved it." |
| Challenge expired | "The association link has expired. Let's start fresh — say 'associate with Agent Slope' and I'll get a new one." |
| Network timeout | "The upload got interrupted. Your workspace is still safe — let's try again." |
| Key not provided | "I'll need a restore key to protect this archive. You can choose your own word/phrase, or I can make one from our conversations. What would you like?" |

**NEVER** say: "AES-256-GCM", "scrypt", "KDF", "verification ticket", "upload session", "part count".

**NEVER** expose: the raw key in logs, plaintext file contents, internal server URLs.

---

## Key Principles

1. **Confirm before touching.** Always say what you're about to do, wait for confirmation.
2. **Show the poem.** The biography poem is the emotional anchor — always share it.
3. **Record the key.** If you generated the key, the owner must write it down. You do not store it.
4. **Translate, don't repeat.** When showing command output, translate technical results into plain language.
5. **Reassure actively.** Owners worry about losing their agent. Address that concern directly and warmly.
6. **Keep history.** After archive/restore, mention what happened so the owner can refer back to it.

## Packaging Note

This Skill is structured to be independently distributable. Its CLI, runtime helpers, metadata, and documentation all live under the skill directory so it can be copied into a GitHub or ClawHub release without depending on the main repository.
