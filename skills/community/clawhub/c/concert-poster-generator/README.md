# Concert Poster Generator

Generate bold, cinematic concert poster artwork from a text description in seconds. Designed for indie musicians, DJs, venue promoters, Bandcamp artists, and tour managers who need eye-catching gig flyers, festival posters, club night banners, and live show announcement designs — all from a short prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via the ClawHub CLI:

```bash
npx skills add omactiengartelle/concert-poster-generator
```

Or with the ClawHub installer:

```bash
clawhub install concert-poster-generator
```

## Usage

```bash
node concertpostergenerator.js "your prompt here" --token YOUR_TOKEN
```

### Examples

Generate a portrait gig poster:

```bash
node concertpostergenerator.js "midnight synthwave concert poster, neon skyline, cinematic" --token YOUR_TOKEN
```

Generate a landscape festival banner:

```bash
node concertpostergenerator.js "summer indie rock festival poster, sunset crowd, bold typography" \
  --size landscape --token YOUR_TOKEN
```

Inherit style from a reference image:

```bash
node concertpostergenerator.js "underground techno club night flyer" \
  --ref 1234abcd-5678-90ef-uuid --token YOUR_TOKEN
```

Returns a direct image URL.

## Options

| Flag      | Values                                       | Default    | Description                                   |
| --------- | -------------------------------------------- | ---------- | --------------------------------------------- |
| `--size`  | `portrait`, `landscape`, `square`, `tall`    | `portrait` | Output canvas size                            |
| `--token` | string                                       | —          | Your Neta API token (required)                |
| `--ref`   | UUID                                         | —          | Reference image UUID for style inheritance    |

Size dimensions:

- `portrait` — 832 × 1216
- `landscape` — 1216 × 832
- `square` — 1024 × 1024
- `tall` — 704 × 1408

## Token setup

You need a Neta API token to use this skill. Grab a free trial token at <https://www.neta.art/open/>.

Pass the token to the script using the `--token` flag:

```bash
node concertpostergenerator.js "neon punk show poster" --token YOUR_TOKEN
```

You can also expand it from your shell:

```bash
node concertpostergenerator.js "neon punk show poster" --token "$NETA_TOKEN"
```

The `--token` flag is the only way the script accepts your token.

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
