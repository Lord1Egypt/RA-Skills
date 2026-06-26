# Children's Book Illustration Generator

Generate beautiful children's book illustrations from text descriptions using AI. Create whimsical storybook art, picture book pages, fairy tale scenes, and kids' story illustrations — perfect for self-publishing authors, KDP creators, teachers, and parents making bedtime story books, educational materials, and nursery wall art.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/children-book-illustration-generator
```

or

```bash
clawhub install children-book-illustration-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node childrenbookillustrationgenerator.js "a friendly dragon helping a child plant flowers" --token "$NETA_TOKEN"
```

```bash
node childrenbookillustrationgenerator.js "two kittens sharing an umbrella in the rain" --token "$NETA_TOKEN" --size portrait
```

```bash
node childrenbookillustrationgenerator.js "a magical forest with talking animals" --token "$NETA_TOKEN" --ref abc123-uuid
```

Returns a direct image URL.

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image size: `portrait`, `landscape`, `square`, `tall` | `landscape` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size Dimensions

| Size | Dimensions |
|------|-----------|
| `square` | 1024 x 1024 |
| `portrait` | 832 x 1216 |
| `landscape` | 1216 x 832 |
| `tall` | 704 x 1408 |

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
