# Cloudflare Pages + GitHub Deployment

## Goal

Publish static legal pages (`index.html`, `privacy.html`, `terms.html`) from a GitHub repo to Cloudflare Pages.

## A) Create GitHub Repository

```bash
mkdir app-legal-site && cd app-legal-site
# copy generated files into this folder
git init
git add .
git commit -m "init legal site"
git branch -M main
git remote add origin git@github.com:YOUR_NAME/YOUR_REPO.git
git push -u origin main
```

## B) Create Cloudflare Pages Project

1. Open Cloudflare Dashboard → Workers & Pages → Create application → Pages.
2. Choose **Connect to Git** and authorize GitHub.
3. Select the repo.
4. Build settings for plain static site:
   - Framework preset: **None**
   - Build command: *(empty)*
   - Build output directory: `/`
5. Deploy.

## C) Verify

After deployment, verify URLs:

- `https://<project>.pages.dev/`
- `https://<project>.pages.dev/privacy.html`
- `https://<project>.pages.dev/terms.html`

## D) Optional Custom Domain

1. Pages project → Custom domains → Set up a custom domain.
2. Add DNS records in Cloudflare.
3. Wait for SSL to become active.

## E) App Store Connect Placement

- Privacy Policy URL → `.../privacy.html`
- Terms of Use URL (if provided) → `.../terms.html`
- Support URL (optional) → legal site home or separate support page

## F) Update Workflow

```bash
# edit files

git add .
git commit -m "update legal copy"
git push
```

Cloudflare Pages redeploys automatically after push.
