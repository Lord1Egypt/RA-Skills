---
name: aicut-generate
description: "Make AI video clips, images, speech, music, songs and sound effects with the aicut CLI (`aicut generate`), on models like Veo, Kling, Seedance, Flux and ElevenLabs. Use when the user asks to generate or make a video, an image, a voice-over, a track or a sound effect, asks which AI model to use, or mentions aicut. Prices every job first and asks before it spends tokens."
---

# Generate AI video, images and audio

Make a video clip, an image or an audio clip with the aicut CLI: find a model, price the job, ask the person, generate, wait and report the url.

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

## Choosing a model

The model catalog is the API's own and changes without a CLI release, so ask it and never guess a model, a field or a price from memory. `aicut models list --type video|image|audio --query <words>` finds models (add `--tags a,b` to narrow), and `aicut models get <model-id>` prints one model's fields (each is a flag of the same name), the media it takes and its prices. Use the model the user named. With no preference, offer two or three that fit with their prices from `models get` and let the user choose: prices differ by ten times or more between models, and picking a cheaper model or lower settings for them without saying so is not your call.

## Choose the flow

Decide what the user wants made, then read the matching file BEFORE the first command: `references/video.md` for a video clip, `references/image.md` for a picture, `references/audio.md` for speech, music, a song or a sound effect. Each is a short, ordered flow that ends with the finished file's url.

## References

- `references/video.md`: Make a video
- `references/image.md`: Make an image
- `references/audio.md`: Make audio
- `references/setup.md`: install, sign in, output and exit codes
- `references/spend.md`: how the spend guard decides
