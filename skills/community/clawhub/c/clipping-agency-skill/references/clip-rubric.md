# Clip rubric

How to find the moments of a client's episode worth clipping, score them, trim them, and say why.
Score every candidate; don't trust a first impression. The client reads the `why` sentence on the
approval page, so the score has to turn into one plain reason.

## Hard gates

Fail any one and the candidate is out, however good the line.

1. **The client's own episode.** Every second comes from the episode this batch names.
2. **The first sentence works with no context.** No "that", "he", "like I said" pointing at
   something the viewer never saw. Start later if you have to.
3. **One complete idea.** It resolves, or stops on a deliberate cliffhanger at a natural beat.
4. **Fits the platforms.** Under 3 minutes for Shorts and inside the TikTok account's own limit.
5. **No intro, outro, housekeeping, ad read you weren't asked to clip, or long crosstalk.**
6. **Nothing on the client's no-go list**, and nothing that misrepresents what a speaker meant. A
   guest's words are clipped only with their release on file.
7. **Still true when it is posted.** A clip may go out weeks after the episode was recorded, and
   stays up for years. Hook, title and captions never say "tomorrow", "this week", "next month",
   "upcoming" or a figure that will have changed; nothing presents an old statement as news. For
   archive or older material, put the year in the hook or title ("1989: ..."), and set
   `episode.recorded` so the client sees it on the page. If a clip only works as news, it is out.

## Score (0 to 100)

| Criterion | Points | What earns them |
|---|---|---|
| Hook | 25 | The first 3 seconds hold the most surprising, high-stakes or specific line. It opens a question. |
| Stands alone | 20 | A stranger gets who, what and why without the episode. |
| Payoff or turn | 20 | A reveal, punchline, reversal, concrete takeaway or emotional peak before the end. |
| Emotion and energy | 15 | Laughter, conviction, a vivid story, a voice that rises. |
| Specifics | 10 | Numbers, names, a concrete example, a small story with stakes. |
| Ending | 10 | Ends on a strong last line with no trailing filler. |

- **70 and up:** cut it.
- **55 to 69:** keep as a spare; mention it to the agency, not the client.
- **Below 55:** drop.

## How many

As many as the client agreed per episode (`clips_per_episode`), between 3 and 12, and only as many
as score 70 or more. Fewer strong clips beat padding: a weak clip costs the client's account more
than a missing one, and the report shows the agreed number next to what was delivered, so tell the
agency when an episode falls short and why.

Spread across the episode: no two clips sharing footage, moments from across the whole runtime, one
clip per sub-topic unless both score 85 or more. Vary the guests and the kinds of moment (a number,
a story, a laugh) so the client's feed doesn't repeat itself.

## Lengths

| | Length |
|---|---|
| Default target | 20 to 45 s |
| Over 40 s | put a turn or a new question around 15 and 30 seconds |
| Hard limits | YouTube Shorts 3 min, TikTok the account's own limit, Reels 15 min |

## Where to start and end

- **Start on the strongest line.** Cut the warm-up when the clip still makes sense without it.
- **Don't repeat the hook.** The first spoken line shouldn't say the hook's words a second later.
- **End on the last strong sentence.** Drop "so yeah", "anyway".
- **Clean edges.** A cut never lands in a word: `make_clips.py` starts a clip just after the
  previous word of the episode ends and stops before the next one starts, with short audio fades.
  `"snap": true` moves small slips to sentence edges. The first and last edge are then set by the
  sound: an edge that lands on a word moves into the quiet next to it. Pauses inside the clip stay
  in unless you set `"tighten": true`, and even then a pause is only cut where the sound is quiet.
  With estimated word times (subtitles without word timing) nothing inside the clip is cut. Then
  listen: `check_clips.py` transcribes each whole cut clip when faster-whisper is installed, warns
  when the first or last word heard isn't the planned one, and names any word of the episode the
  clip should hold but the listen didn't hear. Without it, it says so, and you listen to each whole
  clip yourself.
- **Stay clear of sponsor reads** unless the client wants the read clipped; then it goes out labelled
  as paid (see `platforms.md`).

## The hook text

- 3 to 8 words, the clip's promise or tension in plain words, in the client's voice.
- Specific beats clever: "The Moon isn't a place. It's a direction" beats "This blew my mind".
- True to the clip. No bait the clip doesn't pay off, no words the speaker didn't mean.
- Names spelled as the client file spells them; `check_clips.py` refuses a known misspelling.

## The why sentence

One sentence, for the client: what the moment is, and the reason it works (it stands alone, opens
on the point, what the viewer gets). Not the score, not jargon. "A bold proposal said plainly and
opening on the point" tells a client more than "high hook score".

## Loud moments and long stretches

`transcribe.py` also writes `work/peaks.txt`: the loudest seconds of the sound track, each with the
line spoken there. On a stream or a live show those are often the best moments (a laugh, a shout)
and a transcript alone misses them. Score them like any other candidate.

A talking clip that sits on one framing for 20 seconds loses viewers. With `"punch": true` in the
batch, `make_clips.py` adds a small punch-in at the sentence breaks of long crops, never mid-word.

## Captions per platform

Write each caption from the clip, not from another caption: one or two sentences on what the clip
says, the show's name, then a few hashtags. Nothing invented: names, numbers and claims come from
the episode or the client file. `#ad` first when the clip includes a sponsor segment. Instagram
allows 5 hashtags. The YouTube title says the clip's point in plain words, under 100 characters.

## Example

From the NASA Apollo 11 footage in `examples/agency/` (public domain; times are seconds of each
example episode):

| Client, episode | Hook | Score | Why |
|---|---|---|---|
| Orbit, ep-012 | The Moon isn't a place. It's a direction | 86 | Two surprising lines from someone who went; stands alone, quotable ending |
| Orbit, ep-012 | Why we get bored of the Moon | 80 | Relatable far beyond space; short, ends clean |
| Mission, ep-007 | Were the first words on the Moon scripted? | 82 | The question viewers already have, answered straight |
| Mission, ep-007 | The man who missed the Moonwalk on TV | 78 | Funny and human; opens on the line, ends on the punchline |
| (dropped) | "Two days before launch, what are you doing tomorrow?" | 0 | Fails gate 7: true only on the day it was said |
| (dropped) | the moderator's introductions | 30 | Housekeeping, no idea of its own |
