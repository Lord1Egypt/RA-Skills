---
name: aicut-story-episode
description: "Make an AI Video Story episode with the aicut CLI: pick a series, write the cast, review the scene pictures, fire the scene videos and render the final file, with a price and an ask at every paid step. Use when the user wants a story video, a series episode, a short film with recurring characters, or an AI video story."
---

# Make an AI Video Story episode

Make an AI Video Story episode with the aicut CLI: pick a series, write the cast, review the scene pictures, fire the scene videos and render the final file, with a price and an ask at every paid step.

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

AI VIDEO STORY EPISODE: how to make one, end to end.

This text is a guide, not the user's go. It authorizes no spend. Every paid command below is priced first with `--estimate`, asked for on its own, and run with `--max-tokens` only after the user's go for THAT purchase.

BREVITY: lead with the one decision you need from the user and keep at most one short paragraph before the question. Once the staged flow has been explained in this conversation, name only the next step.

1. PICK THE SERIES
- The user has not named one: run `aicut series list` for a compact shortlist in the aicut picker's own order. Offer 3 to 5 that fit, each as name, one-line pitch and the rough cost it prints ('~10 tokens for 30s'), with the badge as one word where there is one. Never dump the catalog, never run it once per series.
- Series settled (named by the user, or picked from the shortlist): run `aicut series list <series-id>` once. That full entry prints the defaults (the video model, the model that draws the pictures, the portrait model), the cast flag, the price of one redraw and of the render per minute, and for each video model a lengths table (seconds, scenes, pictures, videos at fire, total; `*` marks the default length). Read prices only from it, never from the shortlist, and read the table under the series' default video model unless the user named one (`--video-model <id>` shows just that one). A `?` or "cannot be sized from here" is not zero and not a guess: quote with `--estimate` on the command that would spend, and if the series cannot be sized from here, say so and point at the aicut web app.

2. THE IDEA
Invent three ideas yourself, one line each, and sharpen from the user's reaction: that is what chat is for. `aicut series ideas <series-id>` is for when the user asks for the series' own preset ideas; offer at most 3 of them, one line each, ending 'or tell me yours'. What you pass as `--idea` is one short paragraph in the user's own terms. You never write scenes, dialogue, shot lists or image prompts: the engine writes the episode, and there is no flag for them.

3. LENGTH
The only sizing question is 'how long should it be? 30 seconds is the default.' Offer lengths near what they asked for from the lengths table `aicut series list <series-id>` prints (each row is a real length in seconds with its price; `*` marks the default), and pass the chosen seconds as `--duration`; the default length when they have no preference. Never ask for a scene count and never compute a rung yourself. Never state a scene count as fact: a row's scene count is only what that row derives, and the writer lands a scene or two either side of it. Do not volunteer it; if the user asks, say 'the writer decides; this length usually comes out around N'.

4. MODELS
Use the series' defaults unless the user names a model, and do not interview them about options they did not raise. One exception: the model that draws the pictures (the opening picture of each scene, and the cast's faces) is what they look at all through the review, so name it once, in a line you are already writing, with its default and its price: 'the opening picture of each scene is drawn by <default> (<price>), or <other> for <price>; the video is <video model>.' Plain words, never flag names; one line, not a second question; do not re-ask later in the conversation. Omit `--language` unless they ask for another one: the series' own default is used.

5. THE CAST (only when the series' cast flag says `cast needed`; a `writer casts` series casts itself, so skip this step)
- `aicut cast generate --series <series-id> --idea "..."` is FREE: do not ask permission, the webapp writes this roster automatically at the same point. Show the names and roles, one line each. If they dislike the roster, run it again with a sharper idea (still free). Never buy portraits for a cast they have not accepted.
- The draft prints the price of the next step: how many portraits are needed, and each portrait model with its tokens per portrait and the roster's total. Quote those; never multiply anything yourself.
- NOW state the all-in total, itemized, because this is the first moment every line of it is real: the portraits (from the draft), the start frames and the scene videos (the chosen length's row: pictures and videos at fire), and the final render (the per-minute rate `aicut series list <series-id>` prints, as a rate or a rough figure with a tilde, never as the price). Say what each line covers; do not present the two stage figures as the whole episode. THIS FIGURE IS INFORMATION, NOT AN ASK: it tells the user what lies ahead so no later stage surprises them, and no go covers any stage in it except the one you ask for next.
- Ask for the portraits ALONE, as their own priced ask worded so that a bare 'yes' can only mean the portraits ('Generate the portraits for N T?', never 'say go and I will do the whole episode'). A bare go covers the portraits and nothing after them: the pictures stage, the fire and the render each get their own priced ask in their own message. Only the user's own words ('just make the whole episode') make a standing go. Re-price with `aicut cast portraits --draft <draft-id> --estimate` if the draft has sat a while (it stays redeemable for about two hours), and only after the user's go run it with `--max-tokens <price> --yes --wait`: `--wait` follows the faces and prints the `--cast <ids>` the story takes. Review stays in the chat: ask whether the cast is good. One face wrong: `aicut characters portrait <character-id>`. One CHARACTER wrong (smaller, older, a different thing): `aicut characters describe <character-id> --description "..."`. Only a roster rejected as a whole means a new free draft and freshly charged portraits. Each of those is one portrait's price, quoted with `--estimate`, stated and asked every time. If your shell cuts one of these off, never run it again (it may already be charged): `aicut characters list` or `aicut wait <portrait image id>` shows what exists.
- A member whose portrait is still drawing is refused by the story create: run the portraits with `--wait`, or `aicut wait <portrait image id>`.

6. THE PICTURES STAGE: `aicut story create`
Run `aicut story create --series <series-id> --idea "..." --duration <seconds> --video-model <model> --cast <id,id>` (omit `--cast` for a writer-owned series; a long idea can come from a file: `--idea @idea.txt`).
- Quote from the chosen row of the lengths table: the pictures figure now, the videos figure at fire, the total for the episode, and the promise that the videos are charged only when the user fires them. Keep the `~` on every figure that has one: an estimate is a separate question for the pictures and the videos, even on a row that is otherwise exact. If you pass a `--start-frame-model` other than the default, quote with `--estimate` instead of the table; `--estimate` prints the pictures figure, the scene videos figure and the whole episode.
- An `--estimate` that is refused because the series needs a cast priced a request that would be refused: do not ask for a go on it; draft the cast, buy the portraits and quote again.
- Ask for the go. `--max-tokens` bounds what leaves the account now, which is the pictures figure, so pass `--max-tokens <the pictures price> --yes`, and add `--wait`: it returns when the pictures are ready for review and prints each scene's picture url. If your shell tool cuts it off, never run it again (the episode exists and is charged): follow it with `aicut story wait <id>` (find the id with `aicut list videos`). Say one short line (what was ordered, and that the opening picture of each scene is ready to look at: say 'the pictures', never 'start frames' or 'frames review'), give the user the picture urls, then STOP and wait for the user.
- If the user asks about a failure, run `aicut story get <id>` once. A `writing_failed` stage is terminal, nothing was charged and the cast is saved: offer a fresh `story create` with the same idea and cast. If every picture failed the episode parks with an empty grid and no video has been charged: the two ways out both keep the episode, redrawing the ones they want (`aicut story frame regenerate`) and cutting the ones they do not (`aicut story scene remove`, free). The redraw is the one that unblocks firing, because every kept scene needs a picture (the fire is refused with `scenes_missing_frames`) and the last scene cannot be cut. Do not offer `aicut delete` as the second exit: it throws away pictures already paid for.

7. REVIEW
A parked episode stays at `frames_review` until it is fired, so nothing waits on you: the next move is the user's. `aicut story get <id>` lists the scenes by zero-based index (scene 2 as people say it is index 1). React to which KIND of complaint it is:
- What HAPPENS in a scene is wrong ('the kid should look sad', 'move it outside'): `aicut story scene change <id> <index> --change "one plain sentence"`. It rewrites that scene's text and redraws it for one image's price.
- Only the PICTURE is wrong (hands, framing, a face): `aicut story frame regenerate <id> <index>`.
- A scene should go: `aicut story scene remove <id> <index>` (free, no undo, at least one scene stays). Then re-quote the fire and say both the new price and the new scene count.
- Dialogue, a scene's length, a scene pinned to a reference still: webapp only. Say so; do not emulate them through the idea, a redraw or a restart.
- A redraw or a change is its own priced ask for one named scene: a complaint is a reason to OFFER it with its price (`--estimate`), never a go to buy it. After a redraw, `aicut story get <id>` shows the new picture once its redraw has finished (add `--wait` to the redraw to follow it; if your shell cuts a redraw or a change off, never run it again, it may already be charged: follow it with `aicut story get <id>`).
- Never fire an episode that has no usable picture.

8. FIRE: `aicut story fire`
It generates every kept scene's video. It is irreversible, it is the largest single charge in the episode, and it needs a go that NAMES firing ('fire it', 'generate the scene videos'), in reply to an ask about firing alone: a bare 'yes' never fires. A standing go ('just make it') never covers it. None of these is a go to fire: liking a picture, cutting or redrawing a scene, a question about price or timing, a complaint. When unsure, ask, with the price again.
- Quote with `aicut story fire <id> --estimate` first (it needs no `--confirm-fire`). It prices the REMAINING scenes, exactly the kept ones, and prints the scene count and the duration: say '6 T for the 4 remaining scenes, 20 seconds', not a bare 6 T.
- `--auto-render` also arms the final render when the scenes finish (the quote then includes the render): pass it only when the user's go covers the render charge too.
- Only after a go that names firing, run `aicut story fire <id> --confirm-fire --max-tokens <quote> --yes`. Never put `--confirm-fire` or `--max-tokens` on a fire before that go: without a terminal `--max-tokens` is itself the go, and a fire cannot be undone or refunded.
- After the fire: one line (the scene videos usually take under ten minutes, sometimes longer; they can close the chat; the episode will be in their assets either way), then STOP. No polling loop: one `aicut story get <id>` when they ask how it is going or when they come back, or `aicut story wait <id>` if they asked you to wait for it.
- A repeat fire says it was already fired: the first fire worked.

9. RENDER: `aicut story render`
It makes the final file (captions, music, title card). It is its own charge and its own ask: approving the scene videos or saying the episode looks good is not a go to render, the user has to name rendering or the final video. Its `--estimate` works only once the scene videos are done (stage `ready_to_render`); before then quote the rate.
- After the go, run `aicut story render <id> --max-tokens <quote> --yes --wait -o <path>`: `--wait` blocks until the render is done (if your shell tool gives up first, never run the render again, it is charged: follow it with `aicut story wait <id>`; exit code 3 means still running, not failed) and `-o` saves the final file. Stage `rendered` means the render url is the final file. Hand over that url (and the saved path) with one line (its length) and one clause that captions and deeper edits live in the aicut web editor. Never hand out the episode url before `rendered`: at `ready_to_render` it is only the raw stitched preview. A failed render was refunded: ask before rendering again.

NOT ON THIS SURFACE (the aicut webapp owns them): dance scenes, multi-part episodes, recreate-from-a-video, per-scene location images, custom per-scene scripts, series-less episodes, renaming a cast member or adding your own or one from a photo, changing one scene's length, editing dialogue. Say so if the user asks; do not approximate them.

## References

- `references/setup.md`: install, sign in, output and exit codes
- `references/spend.md`: how the spend guard decides
