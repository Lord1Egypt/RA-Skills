# Setup

Install with Go 1.26 or newer, or use the Docker image below.

```bash
go install github.com/psyb0t/assctl/cmd/assctl@latest
assctl version
assctl fonts-install
```

The `psyb0t/assctl:v0.4.1@sha256:9ee38ba5e8e6f450c919a4831e6c7449d6372ba1180e3c8a9ca082ec2f46cb2c` Docker image already holds assctl, FFmpeg with libass for `burn`, and every preset font, so it needs no font download. Mount the working directory at `/work` and run as the current user:

```bash
docker run --rm --network none --user "$(id -u):$(id -g)" -v "$PWD:/work" psyb0t/assctl:v0.4.1@sha256:9ee38ba5e8e6f450c919a4831e6c7449d6372ba1180e3c8a9ca082ec2f46cb2c validate captions.ass
docker run --rm --network none --user "$(id -u):$(id -g)" -v "$PWD:/work" psyb0t/assctl:v0.4.1@sha256:9ee38ba5e8e6f450c919a4831e6c7449d6372ba1180e3c8a9ca082ec2f46cb2c \
  burn input.mp4 --subtitles captions.ass --output output.mp4
```

`--network none` gives the container no network, which these commands do not need because the fonts are already in the image. Only files under the mounted directory are visible to the container, and it can write there. Mount a directory that holds just the inputs and the output. See [Docker](https://psyb0t.github.io/assctl/install/#docker).

## Named looks

- `black-gold` uses a black background, white text, and gold as its secondary karaoke color.
- `ivory-navy` uses a navy background, ivory text, and sky blue as its secondary karaoke color.
- `mint-plum` uses a plum background, mint text, and peach as its secondary karaoke color.
- `clean` uses an outline on a clear background.
- `tiktok-bold` uses TikTok Sans Bold for lower-middle speech captions.
- `reels-bold` uses Barlow Condensed ExtraBold for lower-middle speech captions.
- `shorts-impact` uses yellow Anton text with a black outline.
- `social-center` centers white Anton text; `social-hook` puts yellow Barlow Condensed ExtraBold near the top.
- `social-box` uses TikTok Sans Bold on translucent black.
- `the-bold` uses the free version of THE BOLD FONT, downloaded from the author's DaFont page. Use uppercase text.

Run `assctl presets --json` for complete parameters. Existing inline tags remain intact and take precedence over the style definition.

Social presets scale their horizontal margins with the script width and their vertical margins with its height. Supply the intended video dimensions. Keep phrases short and check the result against the destination app's controls. Font download links, terms, and position details are in the [preset guide](https://psyb0t.github.io/assctl/presets/).

## Precise edits

Inspect a document first. Its JSON output shows the exact field names. Supply an edit spec with `Info`, `Styles`, or `Events`. An event index starts at one. Use typed `Override` fields to add tags without replacing dialogue text.

```json
{
  "Styles": [
    {
      "Name": "Default",
      "Fields": {
        "Fontsize": "52"
      }
    }
  ]
}
```

```bash
assctl edit --spec edits.json --output updated.ass captions.ass
```

See the [CLI guide](https://psyb0t.github.io/assctl/cli/) for the full creation and editing examples.

## Independent placement and tags

Use `assctl positions --json` to list `portrait-upper`, `portrait-center`, and `portrait-lower-middle`. `--text-position NAME` works with `create`, `captions`, and `theme`. For a placement-only edit, use `assctl position INPUT --text-position NAME --output FILE`; `--style NAME` limits it to one style. Every named layout stays inside the safe area TikTok, YouTube Shorts and Instagram Reels publish for vertical video of any size. `assctl safe-area FILE --platform all|tiktok|shorts|reels` checks a finished file; it reads style and event margins, not inline `\an`, `\pos` or `\move` tags.

`assctl tags --spec override.json` prints an ASS override block. The JSON shape is `ass.Override`, also accepted by event creation and edits. See [ASS features](https://psyb0t.github.io/assctl/ass-features/) for drawing, karaoke, clipping, wrapping, and validation boundaries.
