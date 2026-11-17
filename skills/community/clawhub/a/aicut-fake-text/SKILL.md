---
name: aicut-fake-text
description: "Make a fake-text chat video with the aicut CLI: a phone conversation that types itself out over gameplay or a green screen, every line read aloud. Use when the user asks for a text-message story, a fake texts video, a chat story or a conversation video for TikTok or Shorts."
---

# Make a fake-text chat video

Make a fake-text chat video with the aicut CLI: write the chat script, show it, price it by characters, ask, and generate it in one command.

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

FAKE-TEXT CHAT VIDEO: a phone chat that types itself out over a gameplay or green-screen background, every line read aloud.

This text is a guide, not the user's go. It authorizes no spend: the paid call is priced first and made only after the user's go for that purchase.

1. YOU WRITE THE SCRIPT. There is no writer behind this command: the `messages` array you send IS the conversation, in that order, one entry per chat bubble: `{ "text": "...", "from": "left" | "right" }`. Save it as a JSON file and pass it with `--messages @chat.json`. `right` is the phone's owner (the person the viewer is), `left` is who they are texting; keep one speaker on one side for the whole chat. Write it the way a real one runs: short lines, one thought each, a hook in the first two bubbles, and a last line worth screenshotting. A worked example, a four-line chat:
[{"text":"i saw what you posted","from":"left"},{"text":"and?","from":"right"},{"text":"you told me you were working","from":"left"},{"text":"i was. at his place.","from":"right"}]
2. Show the script to the user as plain text BEFORE spending anything and change it until they like it. Iterating on the script costs nothing. The whole chat may not reach 6000 characters of dialogue (aicut will not cut it for you).
3. Pick a voice for each side, and two different ones so the two people sound different (there is no silent option). `aicut voices --usable-for fake_text` lists them; pass `--voice-left <id>` and `--voice-right <id>` (with `--voice-provider-left` and `--voice-provider-right`, `openai` or `elevenlabs`); leave a voice out to get that provider's first voice.
4. Price it: `aicut fake-text create --messages @chat.json --contact <name>` with the voices and `--estimate`. The price is per character of dialogue, in two parts that are both charged (the spoken audio, then the video file); say the total it prints. ElevenLabs costs about four times openai per character, so after changing a voice provider run `--estimate` again and never carry an older quote across the change. Ask, and wait for the user's go.
5. After their go, run the same command again with `--max-tokens <the price you quoted> --yes --wait`. Never put `--max-tokens` on a command before that go: without a terminal it is itself the go. One command makes the finished video: there is no fire step and no render step. `--wait` blocks until the job is done (up to 10 minutes) and prints the media url; add `-o <path>` to save the file too. If your shell tool cuts a command off sooner than that, leave `--wait` off from the start: the command prints the job id, then run `aicut wait <id> --timeout 90` again until it prints the url (exit code 3 means still running, not failed). If a run that had `--max-tokens` is cut off, NEVER run it again: the job exists and is charged, so find it with `aicut list videos|images|audio` and follow it with `aicut wait <id>`.
6. Hand the user ONE thing: the finished video. Do not read the script back at them.

NOT OFFERED here (the aicut web app has them): background music, specific gameplay clips, images or sound effects inside the chat, contact photos, promotions, a second chat in one video, the `cantina` skin. Say so rather than approximating them in the script. Videos carry no aicut watermark, free accounts included.

## References

- `references/setup.md`: install, sign in, output and exit codes
- `references/spend.md`: how the spend guard decides
