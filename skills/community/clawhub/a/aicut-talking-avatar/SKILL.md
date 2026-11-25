---
name: aicut-talking-avatar
description: "Make a picture of a person speak a script with the aicut CLI: a voice-over first, then a lip-synced video of the picture. Use when the user asks for a talking head, a presenter or spokesperson video, an AI avatar, or a lip-sync video from a photo."
---

# Make a talking avatar

Make a picture of a person speak with the aicut CLI: write the voice-over, choose a voice by preview, price and make the audio, then price and make the lip-synced video.

## Setup

Check the CLI first: `aicut --version`. If the command is missing, install it with `npm i -g aicut-cli` (Node 20 or newer), then sign in with `aicut login`: it opens the browser and the user approves. `aicut account` shows who is signed in and the token balance. More in `references/setup.md`.

Never read the CLI's credentials file and never run `aicut token`: the CLI looks after its own session.

## Spending tokens: the rule

Creating video, images and audio costs tokens from the user's aicut balance. Every command that spends can price itself first. The flow, every time:

1. Run the command with `--estimate`. It prints the price and charges nothing.
2. Tell the user the price and what it buys, in the same message as your ask, and wait for their explicit go for THAT purchase. A bare "yes" counts only as the direct answer to your priced ask, with nothing else raised or outstanding; if it is ambiguous, ask which purchase they mean.
3. Only after the go, run the same command with `--max-tokens <quote> --yes`, where `<quote>` is the price you told them.

Without a terminal (you, a script, CI) `--max-tokens` on its own is already a go: the command spends as soon as the quote is within the number. So never put `--max-tokens` on a command before the user has said go. `--yes` only skips the y/N question, and only together with `--max-tokens`.

Two steps need more than a go:

- `aicut story fire` generates every scene video and cannot be undone or refunded. It needs a go that NAMES firing ("fire it"), given in reply to an ask about firing alone, and then `--confirm-fire --max-tokens <quote> --yes`. A bare "yes" never fires.
- `aicut post publish` puts a post live under the user's name. It needs a go that NAMES publishing, and then `--confirm-publish`.

A go covers one purchase at the price you quoted. If anything changes (the model, the length, the text, a setting) estimate again and ask again. A retry after a failure is a new purchase: new estimate, new go. But a paid command your shell cut off may already be charged, so never run it again: find the job (`aicut list videos|images|audio`, or `aicut story get <id>`) and follow it with `aicut wait <id>`. Never switch to a cheaper model or lower settings to save tokens without saying so. Pictures of real people only with their permission, never public figures. When a price is more than the balance the command refuses and prints a top-up link: give it to the user and stop.

## The flow

TALKING AVATAR: make a picture of a person speak a script (a presenter, a spokesperson, a character).

This text is a guide, not the user's go. It authorizes no spend: the paid call below is priced first and made only after the user's go for that purchase.

0. Run `aicut account` to see the balance. If it is 0, the account has no tokens: tell the user so, give them https://www.aicut.pro/billing, and stop until they have added some. Price nothing first. (A price above the balance is refused later with the same link: give it to the user and stop.)
1. Ask the user for the words to be spoken (exactly, as they should be said), the picture of the person who speaks them, and what the voice should be like. Ask nothing else. The picture is a clear, front-facing portrait: a URL (public https, or from an earlier generation), a file on their machine (below), or one you make with `aicut generate image` if they have none (a paid image: price it with `--estimate` and wait for the user's go first). CONSENT: only a picture of the user, of someone who gave their permission, or of a fictional or AI-generated character; never a real person without their permission, and never a public figure or celebrity (decline and offer a generated character). A file on the user's own machine: pass its path where the flag takes a URL (for example `--character ./photo.png`); the CLI uploads it first and uses the finished url. A file that is already a URL needs no upload.
2. Find the speech model: `aicut models list --type audio`; run `aicut models get <model-id>` and read its fields before you set anything. Choose the voice by PREVIEW, not by spend: run `aicut voices --provider elevenlabs --usable-for audio --limit 100 --json`, propose 2 or 3 that fit what the user described, each with its `preview_url` link beside its name (a link the user can play; OpenAI voices have none, so describe those), and let them pick BEFORE any paid call. Never generate the same line in several voices to compare them, unless the user asks for that and has been told the total price of it.
3. Price the voice-over: `aicut generate audio --model <id> --text "..." --voice <voice id>` with `--estimate`. Audio is priced on a rate, so the quote is the only price; never multiply a rate yourself. Say the price and that the video itself is priced next, from the finished audio's length (the server measures it), ask, and wait for the user's go for the voice-over.
4. After their go, run the same command again with `--max-tokens <the price you quoted> --yes --wait`. Never put `--max-tokens` on a command before that go: without a terminal it is itself the go. `--wait` blocks until the job is done (up to 10 minutes) and prints the media url; add `-o <path>` to save the file too. If your shell tool cuts a command off sooner than that, leave `--wait` off from the start: the command prints the job id, then run `aicut wait <id> --timeout 90` again until it prints the url (exit code 3 means still running, not failed). If a run that had `--max-tokens` is cut off, NEVER run it again: the job exists and is charged, so find it with `aicut list videos|images|audio` and follow it with `aicut wait <id>`. The finished audio is the only audio `aicut transform lipsync` accepts: pass its id (the job id the command printed) as `--source-audio`.
5. Price the video: `aicut transform lipsync --character <file or url> --source-audio <audio id> --resolution 720p` with `--estimate`. There is no length flag: the price is the audio's measured length times a per-second rate. `--resolution` is required: use `720p` unless the user asked for `1080p`, which costs twice as much, and name the choice. A local picture is uploaded first, even with `--estimate` (it costs no tokens). Say the price and what it buys in ONE message, ask, and wait for the user's go for this purchase.
6. After their go, run the same command again with `--max-tokens <the price you quoted> --yes --wait` (a video takes 1 to 3 minutes, sometimes 6). Never put `--max-tokens` on a command before that go: without a terminal it is itself the go. `--wait` blocks until the job is done (up to 10 minutes) and prints the media url; add `-o <path>` to save the file too. If your shell tool cuts a command off sooner than that, leave `--wait` off from the start: the command prints the job id, then run `aicut wait <id> --timeout 90` again until it prints the url (exit code 3 means still running, not failed). If a run that had `--max-tokens` is cut off, NEVER run it again: the job exists and is charged, so find it with `aicut list videos|images|audio` and follow it with `aicut wait <id>`. Then tell the user the media url and one line about the result.

If the job fails, read its `error:` line and tell the user what went wrong. Any resubmit is a new purchase with its own price and go, and never the identical request twice: change the model or the prompt, or ask.

## References

- `references/setup.md`: install, sign in, output and exit codes
- `references/spend.md`: how the spend guard decides
