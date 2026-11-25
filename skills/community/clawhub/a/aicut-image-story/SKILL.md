---
name: aicut-image-story
description: "Make a narrated AI image story video with the aicut CLI: the user's script is cut into scenes, each one an AI image, read aloud with captions. Use for facts, history, horror, storytime and explainer videos built from a written script."
---

# Make an AI image story video

Make a narrated AI image story video with the aicut CLI: write the narration script, show it, price it by image count, ask, and generate it in one command.

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

AI IMAGE STORY: a narrated script cut into scenes, each one an AI image, read aloud with captions over it. Suited to facts, history, horror, storytime and explainers.

This text is a guide, not the user's go. It authorizes no spend: the paid call is priced first and made only after the user's go for that purchase.

1. YOU WRITE THE SCRIPT, AND ONLY THE SCRIPT. The text you send is the narration that is spoken, verbatim, in that order: save it as a text file and pass it with `--text @story.txt`. Write it the way a voiceover sounds when read ALOUD: plain prose, short sentences, a hook in the first line, one idea at a time. No scene numbers, no image directions, no stage notes, no speaker labels: aicut cuts the script into scenes and writes every image prompt itself, and you never write one. A worked example of the text: "In 1943 a Soviet pilot was shot down behind enemy lines. He walked eighteen days through the snow on two broken legs. When he reached his own trenches, they did not believe he was alive. Then he asked for his plane back."
2. Show the script to the user as plain text BEFORE spending anything and change it until they like it. Iterating on the script costs nothing. Write the text in the language you name with `--language`: a script in another language is translated, which changes its length and therefore the price, and a quote is exact only for the script you sent.
3. Price it: `aicut image-story create --text @story.txt --estimate`. The price is driven by the IMAGE COUNT, not the words, so the quote line carries the scene count and the voice provider next to the money: say the count and the price. The levers, in the order to reach for them: `--seconds-per-image` (3 is the default; 5 buys fewer images for the same script and is the cheap direction, 2 is the busy and expensive one), `--image-model` (`zit-realism` is the cheap default; `gpt-image-2.5` costs noticeably more per image, so offer it only when the user asks and quote it before you pick it), and `--voice-provider` (ElevenLabs costs more per character of narration than openai). Re-quote after changing any of the three and never carry an older number across a change. Sound effects (`--sound-effects`) add to the price by the video's length: quote them.
4. Styles are optional and not free: `aicut image-story styles` lists authored looks, and passing one as `--style <id>` forces the expensive edit-capable image model, so re-quote after adding one. Most videos use no style. If you offer styles, name at most 3 that fit what the user described, one line each; `aicut image-story styles --json` carries each one's `preview_url`, so show it as a markdown image and they pick by eye.
5. Ask, and wait for the user's go. After it, run the same command again with `--max-tokens <the price you quoted> --yes --wait`. Never put `--max-tokens` on a command before that go: without a terminal it is itself the go. One command makes the finished video: there is no fire step and no render step. It takes longer than a single image because every scene is generated. `--wait` blocks until the job is done (up to 10 minutes) and prints the media url; add `-o <path>` to save the file too. If your shell tool cuts a command off sooner than that, leave `--wait` off from the start: the command prints the job id, then run `aicut wait <id> --timeout 90` again until it prints the url (exit code 3 means still running, not failed). If a run that had `--max-tokens` is cut off, NEVER run it again: the job exists and is charged, so find it with `aicut list videos|images|audio` and follow it with `aicut wait <id>`.
6. Hand the user ONE thing: the finished video. Do not read the script back at them. Videos carry no aicut watermark, free accounts included.

## References

- `references/setup.md`: install, sign in, output and exit codes
- `references/spend.md`: how the spend guard decides
