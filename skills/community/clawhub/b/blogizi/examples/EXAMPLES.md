# Blogizi CLI examples

Practical samples for drafting and publishing markdown with the [Blogizi CLI](../README.md).

| File | Description |
| --- | --- |
| [COMMAND_LINE_GUIDE.md](./COMMAND_LINE_GUIDE.md) | Step-by-step CLI walkthrough |
| [basic-usage.sh](./basic-usage.sh) | Shell script: write a sample post, draft it, optionally publish |
| [list-projects.js](./list-projects.js) | List projects for your account API key |
| [create-post.js](./create-post.js) | Create a draft post via `POST /api/posts` |
| [sample-post.md](./sample-post.md) | Example markdown with Blogizi frontmatter |

## Prerequisites

```sh
npm install -g blogizi
blogizi auth YOUR_ACCOUNT_API_KEY
blogizi use your-project-slug   # if you have more than one project
```

Get your key from [Dashboard → Account → API](https://blogizi.com). Never commit API keys.

## Quick start

```sh
# From the repo root
chmod +x examples/basic-usage.sh
./examples/basic-usage.sh

# Or call the CLI directly
blogizi draft examples/sample-post.md
# blogizi update examples/sample-post.md   # after edits, same slug
# blogizi publish examples/sample-post.md   # only when you want it live
```

Node examples (Node 20+):

```sh
export BLOGIZI_API_KEY="your-key"
export BLOGIZI_PROJECT_SLUG="your-project-slug"   # optional if you have one project

node examples/list-projects.js
node examples/create-post.js
```

## Notes

- `blogizi draft` saves a **draft** in the dashboard (not live).
- `blogizi update` updates an existing post by **slug**.
- `blogizi publish` makes the post **live**.
- Prefer the CLI over raw HTTP unless you are building an integration.
- Full reference: [README.md](../README.md) · Agent guide: [SKILL.md](../SKILL.md)
