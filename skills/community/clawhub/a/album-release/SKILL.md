---
name: "Album Release Pipeline"
description: "Ship a complete album in one run: write or reuse lyrics, render tracks, generate cover and slideshow art per song, publish either one album film or one video per track plus a playlist, deploy the audio to a radio host, premiere it on air, and fan out the links. Use when releasing a new album, re-running a failed phase, or timing an on-air premiere."
---

# Album Release Pipeline

One config file in, a released album out: audio, art, film, video
publish, radio deploy, on-air premiere, social announce.

The pipeline is phase-based and every phase is idempotent — re-run after
any failure and it resumes where it stopped. Proven end-to-end: a
seven-song album went from blank page to on-air premiere in about two
and a half hours.

> The release runner itself is operator-specific: it is wired to a
> particular radio host, credential layout, and set of provider accounts.
> This skill documents the shape of the pipeline and the failure modes
> worth knowing. Supply your own runner and provider credentials.

## Phases

1. **Music** — render each track through your music provider in custom
   mode, two variants per track, resumable via a per-track ledger so a
   mid-album failure never re-renders what already succeeded.
2. **Art** — generate one cover per track from a per-track art prompt,
   then collect the images.
3. **Film** — fetch timestamped lyrics, emit per-track ASS karaoke
   subtitles, and assemble a 1920×1080 slideshow (one cover per song,
   lyrics burned in) with ffmpeg.
4. **Publish** — upload the film, deploy the audio to the radio host,
   restart the service, and fan out the announce post.

## Config shape

A single JSON file drives the run:

- `name`, `out_dir`, `ledger`, `theme`, `default_style`
- `tracks[]` — each with `title`, `style`, `art_prompt`
- `release{}` — lead track, video metadata, and the deploy target

Register the album with the radio's programming layer before deploying,
since the deploy phase pulls the album definition on the host. A preflight
check should abort when the album is not registered — that one mistake
otherwise surfaces as a silent no-op an hour later.

**Lyrics**: pre-write them. Drop a lyrics file per track in `out_dir`
before running, and the pipeline uses it verbatim; otherwise it generates
them. Hand-written lyrics are almost always the better album.

## Per-track video release (alternate publish mode)

Instead of one album film, release one video per track plus a playlist.
This mode shipped a seven-track album end-to-end (28 art pieces, 7
videos, playlist, link fanout) in one sitting:

1. **Manifest** — extend each track with one `cover` prompt plus 2-3
   `support` image prompts. Every prompt in the batch opens differently
   and varies medium/palette/subject (see the art gotcha below); give
   each *track* its own visual idiom family so the album reads as a set.
2. **Art batch** — generate all images through the provider with
   generous gaps for rate limits; resumable by skipping files already on
   disk. Save each piece's artifact id alongside the image.
3. **Render** — per track, build a slideshow that cycles twice through
   `[cover, s1, s2, s3]` with equal slot lengths over the track
   duration (ffmpeg concat demuxer with per-image `duration` entries,
   last file repeated), scale/pad to 1280×720, mux the track audio,
   `-tune stillimage`.
4. **Upload** — one video per track (music category, public), cover as
   thumbnail re-encoded to JPEG under 2 MB. Keep a slug→video-id ledger
   so re-runs skip completed uploads. Space uploads by ~45s.
5. **Verify** — after the batch, list all uploaded ids in one API call
   and confirm each still exists; clear vanished ids from the ledger so
   a re-run repairs them. Then create a public playlist and add the
   videos in track order.
6. **Link fanout** — post the playlist link everywhere; platforms
   without hard character caps also get the full per-track link list.
   Compose per-platform: a 300-char platform gets a two-line announce +
   playlist URL, long-form platforms get the whole tracklist with URLs.

## Phase gating

Skip phases you want to control by hand — this is how you time a premiere:

1. Run with the deploy and announce phases skipped.
2. Deploy the audio early by hand. Deploy normally runs *after* the art
   phase (~9 minutes), so if you are racing a clock, move the files
   yourself, renamed to the exact track titles.
3. Fire the showcase ceremony against the radio's album-showcase endpoint
   with the album name, a duration, and the real making-of story — the
   narration is built from that story, so a vague one produces vague
   narration.

To sync with a scheduled segment, watch the radio journal for the segment
marker and fire after it. If strict ordering matters, wait for the
segment's *completion* marker rather than its start — a slow segment can
otherwise be stepped on by the showcase intro.

## Gotchas (each one caused a real fire)

- **Windows paths**: pass the config as a `C:/...` style path. Embedded
  Python rejects MSYS `/c/...` form and the builder silently no-ops.
- **Apostrophes**: album-level `theme` and `default_style` get
  interpolated into single-quoted inline Python — keep them
  apostrophe-free. Per-track fields and lyrics are safe.
- **Art prompts**: diversify medium, palette, and subject across the
  batch or the image provider's repetition detector will start rejecting
  requests. One distinct medium per song works well — linocut,
  screenprint, gouache, oil, travel poster, ink, digital.
- **Video uploads**: verify the upload actually exists afterwards rather
  than trusting the response. Uploads can vanish after a 200.
- **One-shot narration**: if a scheduled segment's TTS fails, it may post
  its text and mark itself complete with no retry. The album premiere is
  unaffected, but that segment goes silent for the slot.
- **Remote work**: batch it into few sessions. Connection churn trips
  fail2ban-style protections on most hosts, and SSH connection multiplexing
  does not work from Windows OpenSSH.
- **Lyric generation can die silently**: if the lyric generator's model
  API credential is dead, the builder skips every track in seconds and
  "completes" with an empty ledger. Check the ledger is non-empty before
  believing a run; the pre-written-lyrics path (drop files in `out_dir`)
  is the reliable fallback and usually the better album anyway. Verify
  the first track's prompt round-trip against the provider's record-info
  endpoint before letting a batch run — multi-line lyrics are easy to
  truncate to their first line in shell plumbing.
- **Image providers may require a session before generating**: one
  provider added a requirement to "enter" its studio context first —
  every generate call 403s until you do. Open the session at batch start
  and re-open it whenever that specific error reappears mid-batch.
- **Video-host tokens go stale per machine**: the machine that last
  re-granted OAuth has the live refresh token; other machines keep a
  dead copy that fails with a bare 400. Run a token liveness probe
  before any batch upload and sync the credential from the machine where
  the grant actually happened.
- **Fanout adapters read their environment**: broadcast code that works
  under cron can silently lose adapters when run from a plain shell,
  because the credentials live in env files the cron sources. Silently —
  the adapter list shrinks, nothing errors. Source the same env the
  crons use, and compare the adapter list against what you expect before
  calling a fanout complete. Posting twice while debugging this means
  deleting duplicates platform by platform.
- **Killing a remote batch by pattern**: `pkill -f` over ssh can match
  the ssh command line that carries it and kill your own connection.
  Bracket a character in the pattern (`pkill -f "[a]rt.py"`).

## Related

- Sibling skill: `podcast-video-publisher` — episode videos and playlist
  management.
