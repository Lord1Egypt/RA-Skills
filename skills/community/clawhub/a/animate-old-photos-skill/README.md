# Animate Old Photos Skill

Use this skill to turn old photos into 5-second AI-generated videos through the [Animate Old Photos](https://animateoldphotos.org/) API.

This repository is a portable agent skill package for AI tools that support file-based skills and shell execution. It helps an agent:

- authenticate with your Animate Old Photos API key
- upload a local JPEG or PNG image
- submit an animation task
- poll until the video is ready
- download the final MP4

## Who This Is For

This skill is for users who want an AI agent to handle the full photo-to-video workflow for them.

It works best with agents that can:

- load a `SKILL.md` file
- run shell commands
- access `curl` and `jq`

If your client supports MCP, you may also prefer the hosted MCP server at:

```text
https://animateoldphotos.org/api/mcp
```

## Requirements

This is a paid service.

- Official website: [animateoldphotos.org](https://animateoldphotos.org/)
- Get an API key: [Profile > API Key](https://animateoldphotos.org/profile/interface-key)
- Buy credits: [Pricing](https://animateoldphotos.org/pricing)

System requirements:

- `bash`
- `curl`
- `jq`

Usage limits:

- 3 credits per animation
- JPEG and PNG only
- max file size: 10 MB
- minimum dimensions: 300 x 300 px
- output video length: 5 seconds

## Install

Clone this repository:

```bash
git clone <your-public-repo-url>
```

Then copy the `animate-old-photos-skill` folder into your agent's skills directory.

Examples:

### Cursor

```bash
cp -r animate-old-photos-skill ~/.cursor/skills/
```

### Claude Code

```bash
cp -r animate-old-photos-skill ~/.claude/skills/
```

For other agents, place the folder wherever that tool expects local skills.

## How To Use

Once installed, ask your agent something like:

- `Animate this old photo`
- `Turn this photo into a video`
- `Bring this old photo to life`

The agent should then:

1. ask for your API key, unless `AOP_API_KEY` is already set
2. ask for the image path
3. ask for an optional motion prompt
4. confirm the 3-credit cost
5. run the upload, animation, polling, and download steps

## Direct Script Usage

This repository also includes a standalone Bash script if you want to run the full workflow yourself.

```bash
bash scripts/animate.sh <API_KEY> <IMAGE_PATH> [PROMPT] [OUTPUT_PATH]
```

Example:

```bash
bash scripts/animate.sh aop_xxxx ./grandma.jpg "gentle smile and slight head turn" ./result.mp4
```

You can also store the API key in an environment variable:

```bash
export AOP_API_KEY="aop_xxxx"
bash scripts/animate.sh "$AOP_API_KEY" ./grandma.jpg
```

## Prompt Tips

The prompt is optional. Short motion instructions usually work best.

- `grandmother smiling and waving`
- `soft smile with a slight nod`
- `eyes blinking slowly while looking at the camera`

If you leave the prompt empty, the service will generate motion automatically.

## Repository Structure

```text
animate-old-photos-skill/
├── LICENSE
├── README.md
├── SKILL.md
├── references/
│   └── animate-old-photos-api.md
└── scripts/
    └── animate.sh
```

## Files

- `SKILL.md` contains the instructions the agent follows
- `references/animate-old-photos-api.md` contains the API reference
- `scripts/animate.sh` runs the whole workflow in Bash

## Typical Workflow

1. Authenticate with your API key
2. Check your credit balance
3. Upload the input image
4. Finalize the upload
5. Submit the animation task
6. Poll every 30 seconds
7. Download the MP4 when ready

Typical processing time is 2 to 5 minutes.

## Troubleshooting

**Invalid or expired API key**

Create a new key at [Profile > API Key](https://animateoldphotos.org/profile/interface-key).

**Insufficient credits**

Buy more credits at [animateoldphotos.org/pricing](https://animateoldphotos.org/pricing).

**`jq` not installed**

Install `jq` before using the skill or script.

**Image upload fails**

Make sure the file is a local JPEG or PNG under 10 MB.

**Task takes too long**

The script waits up to 10 minutes by default. The task may still be processing on the server if it times out locally.

## Notes

- This skill uses the Animate Old Photos extension API endpoints under `https://animateoldphotos.org/api/extension/*`.
- The skill is designed for local-file workflows.
- If you want a hosted tool integration instead of shell-based automation, use the MCP server.

## License

[MIT](./LICENSE)
