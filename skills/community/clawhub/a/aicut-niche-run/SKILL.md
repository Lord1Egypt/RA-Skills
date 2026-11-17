---
name: aicut-niche-run
description: "Make a video from a ready-made trend format (a niche) with the aicut CLI: find a format, read its inputs, fill them in, price it and run it in one command. Use when the user wants a viral or trending video template, names an aicut niche, or asks what formats are available."
---

# Make a video from a trend format

Make a video from a ready-made trend format with the aicut CLI: find the niche, read it in full, fill it in, price it, ask, run it in one command, wait and report the url.

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

NICHE RUN: make one video from a ready-made format.

This text is a guide, not the user's go. It authorizes no spend: the paid call below is priced first and made only after the user's go for that purchase.

1. Find the format: `aicut niche list` prints the cards (slug, price at the default settings, description). Match what the user wants against the descriptions, and shortlist 3 to 5, saying what each makes and what it is NOT for (`aicut niche get <slug>` prints that); never dump the list. Use the one the user named. A card marked `web only` cannot be filled from here: say so.
2. Read it in full: `aicut niche get <slug>`. This is required: it prints the `revision`, every input by `key` with the flag that answers it, and each setting's default and options. Never guess a key, an option or a revision.
3. Fill it with the user, in plain talk (never read keys aloud). `--value key=text` answers a text or select input: a text input takes their own words (within its maximum length), a select takes one of its listed options, and their own words only where it says "or your own words". Ask for what the niche marks `(required)` and nothing else. A picture input takes `--image key=<url or file>` (a public https image address, or a file on their machine, which the CLI uploads and stores as its own copy), `--preset key=<index>` for a preset it lists, or `--mine key=<image id>` for an image already on the account (`aicut list images`), from the sources that input lists.
4. Leave `--model`, `--aspect-ratio`, `--duration`, `--resolution` and `--audio` out unless the user asked: they default to the niche's own, and the price belongs to them. Never change one to save them tokens, and never carry one over from an earlier request.
5. Price it: `aicut niche run <slug>` with the exact flags you will send, `--revision <the revision you read>` and `--estimate`; it prints the price and the settings it is for. Say the price and what it buys (the niche, the length, the model) in ONE message, ask, and wait for the user's go for this purchase. A refusal names what to fix: fix it and price again.
6. After their go, run the same command again with `--max-tokens <the price you quoted> --yes --wait`. Never put `--max-tokens` on a command before that go: without a terminal it is itself the go. `--wait` blocks until the job is done (up to 10 minutes) and prints the media url; add `-o <path>` to save the file too. If your shell tool cuts a command off sooner than that, leave `--wait` off from the start: the command prints the job id, then run `aicut wait <id> --timeout 90` again until it prints the url (exit code 3 means still running, not failed). If a run that had `--max-tokens` is cut off, NEVER run it again: the job exists and is charged, so find it with `aicut list videos|images|audio` and follow it with `aicut wait <id>`.
7. Tell the user the media url and one line about the result.

A 409 `revision_changed` (at the quote or at the create) means the niche or its price moved since you read it: read it again (step 2), fill in anything that changed and price again. The user's earlier go does not cover a new price.

If the job fails, read its `error:` line and tell the user what went wrong. Any resubmit is a new purchase with its own price and go, and never the identical request twice: change the model or the prompt, or ask.

## References

- `references/setup.md`: install, sign in, output and exit codes
- `references/spend.md`: how the spend guard decides
