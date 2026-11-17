# Clip rubric

How to find the moments worth clipping in a transcript, score them, trim them, and give every
account its own edit. Score every candidate; don't trust a first impression.

## Hard gates

Fail any one and the candidate is out, however good the line.

1. **The campaign's footage only.** Every second comes from a file the brief supplied or allows.
2. **The first sentence works with no context.** No "that", "he", "like I said" pointing at
   something the viewer never saw. Start later if you have to.
3. **One complete idea.** It resolves, or stops on a deliberate cliffhanger at a natural beat.
4. **Inside the campaign's length** (`length` in campaign.json) and the platform's.
5. **No intro, outro, housekeeping or long crosstalk.**
6. **Nothing the brief bans**, and nothing that misrepresents what the speaker meant.

## Score (0 to 100)

| Criterion | Points | What earns them |
|---|---|---|
| Hook | 25 | The first 3 seconds hold the most surprising, high-stakes or specific line. It opens a question. |
| Stands alone | 20 | A stranger gets who, what and why without the source. |
| Payoff or turn | 20 | A reveal, punchline, reversal, concrete takeaway or emotional peak before the end. |
| Emotion and energy | 15 | Laughter, conviction, a vivid story, a voice that rises. |
| Specifics | 10 | Numbers, names, a concrete example, a small story with stakes. |
| Ending | 10 | Ends on a strong last line with no trailing filler. |

- **70 and up:** cut it.
- **55 to 69:** show the user as "maybe".
- **Below 55:** drop.

## Lengths

| | Length |
|---|---|
| Default target | 20 to 45 s, inside the campaign's minimum and maximum |
| Over 40 s | put a turn or a new question around 15 and 30 seconds |
| Hard limits | YouTube Shorts 3 min, TikTok the account's own limit, Reels 15 min |

## Where to start and end

- **Start on the strongest line.** Cut the warm-up when the clip still makes sense without it.
- **Leave room for the disclosure.** The first seconds carry "Paid partnership with <brand>" at the
  top and the hook in the middle; a strong first spoken line still works under both.
- **Don't repeat the hook.** The first spoken line shouldn't say the hook's words a second later.
- **End on the last strong sentence.** Drop "so yeah", "anyway".
- **Snap to word edges.** Never cut mid-word.

## The hook text

- 3 to 8 words, the clip's promise or tension in plain words.
- Specific beats clever: "Astronauts train so nothing surprises them" beats "This blew my mind".
- True to the clip. No bait the clip doesn't pay off, no words the speaker didn't mean.

## One edit per account

Clippers run several accounts. Each one gets its own edit:

- **Best:** another moment. Give each account a different candidate from the scored list.
- **Allowed across platforms:** the same moment with its own hook and its own caption, when the
  footage is too short for more moments. `check_clips.py` warns.
- **Blocked:** the same file on two accounts; two accounts on the same platform sharing more than
  `max_overlap` (default half) of their footage; the same moment with the same hook or caption.
- **Never:** speed changes, mirroring, a different crop, filters, a watermark swap or any other
  trick to make one edit look like two. The platforms count that as reused content, and it is the
  pattern YouTube's spam policy describes.

Spread across a batch: no overlapping clips on one platform, moments from across the whole source,
one clip per sub-topic unless both score 85 or more.

## Loud moments and long stretches

`transcribe.py` also writes `work/peaks.txt`: the loudest seconds of the sound track, each with the
line spoken there. On a stream or a live show those are often the best moments (a crowd, a laugh,
a shout) and a transcript alone misses them. Score them like any other candidate.

A talking clip that sits on one framing for 20 seconds loses viewers. With `"punch": true` in
clips.json, `make_clips.py` adds a small punch-in at the sentence breaks of long stretches, never
mid-word. It changes nothing about which moment is used: it is the edit, not a trick to make one
clip look like another.

## Captions per account

Write each caption from the clip, not from another caption: `#ad` first, one or two sentences on
what the clip says, then the brief's hashtags, @mentions and link. Nothing invented: names, numbers
and claims come from the footage or the brief. Instagram allows 5 hashtags.

## Example

From the NASA interview in `examples/orbit-campaign/` (public domain):

| Account | Window | Score | Why |
|---|---|---|---|
| TikTok | 8:10 to 8:33 | 86 | Groundhog Day analogy: vivid, known reference, clear payoff |
| Reels | 3:34 to 3:56 | 82 | "Save the crew, not the mission": quotable, concrete stakes |
| Shorts | 1:12 to 1:42 | 76 | Future crews cursing their names: funny, human, stands alone |
| (dropped) | 0:47 to 1:09 | 48 | Abstract, no payoff, opens with "And so" |
