# Setup

## Prerequisites

- **git** — must be installed and identity configured (`user.name` / `user.email`)
- **gh** — GitHub CLI, authenticated (`gh auth login`)
- **Node.js ≥ 18** or **Bun** — for running `npx`/`bun` commands

---

## First-Time Setup

Run once to create a brand-new clawpage project.

### 1. Ask for a Repository Name

Ask the user what to name their clawpage repository (e.g. `my-chats`). Use this name as `{repoName}` throughout the steps below.

### 2. Create a Private GitHub Repository

```bash
gh repo create {repoName} --private
```

Note the resulting `{owner}/{repoName}` for later steps.

### 3. Choose a Local Directory

Ask the user where they want the project stored locally. Use this as `{localDir}` (absolute path, e.g. `~/projects/{repoName}`). If the user has no preference, suggest the platform default (see platform profile), or fall back to `~/{repoName}`.

### 4. Scaffold the Project

```bash
npx create-clawpage {repoName} --dir {localDir}
```

This scaffolds `clawpage.toml`, a `chats/` directory, deployment configuration for GitHub Pages, Netlify, Vercel, and Cloudflare Pages, and initializes a git repository with an initial commit.
`{repoName}` is used as the project label in the initial commit message; `--dir` sets the exact output path regardless of whether it matches the repo name.

### 5. Choose a Deployment Platform

Ask the user which platform they want to deploy to:

| Platform | Free private repos | Notes |
|---|---|---|
| **GitHub Pages** | No (requires GitHub Pro) | Default; fully automated via included GitHub Actions workflow |
| **Netlify** | Yes | Connect repo in Netlify dashboard |
| **Vercel** | Yes | Hobby plan: personal non-commercial use only |
| **Cloudflare Pages** | Yes | 500 builds/month |

> If the user is on the free GitHub plan and their repo is private, GitHub Pages is not available. Recommend Netlify, Vercel, or Cloudflare Pages instead. Keeping the repo private is recommended best practice — see [how to protect sensitive info](https://clawpage.yelo.ooo/chats/how-to-protect-sensitive-info/).

Use `{platform}` for the chosen value in the steps below.

### 6. Configure the Site URL

Edit `{localDir}/clawpage.toml`.

**GitHub Pages:**

```toml
site = "https://{owner}.github.io"
base = "/{repoName}"
```

**Netlify / Vercel / Cloudflare Pages:**

Leave `site` unset for now — the platform assigns a URL on first deploy. You will fill it in after step 8.

Also set `[template.options]` title/subtitle if the user wants custom branding.

### 7. Push to GitHub

```bash
cd {localDir}
git remote add origin https://github.com/{owner}/{repoName}.git
git push -u origin main
```

### 8. Enable Deployment

**GitHub Pages:**

```bash
gh api repos/{owner}/{repoName}/pages --method POST -f build_type=workflow
```

If this fails (e.g. Pages not yet initialized), guide the user to enable it manually:
**Settings → Pages → Source → GitHub Actions**

Deployment triggers automatically on every push to `main`. The site will be live at `https://{owner}.github.io/{repoName}/`.

**Netlify:**

1. Go to [app.netlify.com](https://app.netlify.com) → **Add new site → Import an existing project**.
2. Select the `{owner}/{repoName}` repository. Netlify reads `netlify.toml` automatically.
3. Click **Deploy site**. The site will be live at `https://{site-name}.netlify.app`.

**Vercel:**

1. Go to [vercel.com/new](https://vercel.com/new) → **Import Project**.
2. Select the `{owner}/{repoName}` repository. Vercel reads `vercel.json` automatically.
3. Click **Deploy**. The site will be live at `https://{project-name}.vercel.app`.

**Cloudflare Pages:**

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages → Create → Pages → Connect to Git**.
2. Select the `{owner}/{repoName}` repository and set:
   - **Build command:** `bun run build`
   - **Build output directory:** `dist`
   - **Environment variable:** `BUN_VERSION = latest`
3. Click **Save and Deploy**. The site will be live at `https://{project-name}.pages.dev`.

For custom domain setup and free tier details, see the [deployment guide](https://github.com/imyelo/clawpage/blob/main/docs/deployment.md).

Once the first deployment completes, copy the assigned URL back into `clawpage.toml`:

```toml
site = "https://{assigned-url}"
```

Then commit and push the update:

```bash
cd {localDir}
git add clawpage.toml
git commit -m "chore: set site URL"
git push
```

### 9. Register with Your Agent

→ See [Register & Verify](#register--verify) below.

---

## Existing Repo, New Environment

Use this when a clawpage repo already exists on GitHub but hasn't been registered on the current machine yet.

### 1. Ask for the Repo

Ask the user for their existing clawpage GitHub repo (e.g. `your-username/my-chats`) and where they'd like to clone it locally.

### 2. Clone the Repo

```bash
git clone https://github.com/{owner}/{repoName}.git {localDir}
cd {localDir}
```

### 3. Verify Configuration

Check that `clawpage.toml` already has `site` set. If it's missing or empty, ask the user for their deployed site URL and fill it in.

### 4. Register with Your Agent

→ See [Register & Verify](#register--verify) below.

---

## Register & Verify

Follow the **Registration** section in your agent profile:

| Agent | Profile |
|-------|---------|
| OpenClaw | [platforms/openclaw.md](platforms/openclaw.md#registration) |
| _(others)_ | [platforms/unknown.md](platforms/unknown.md#registration) — provide project path manually |

Then confirm `{projectDir}/clawpage.toml` has `site` set and the agent profile lists the correct project path.
