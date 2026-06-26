# Publish (Optional)

Push the chat branch and open a pull request.

Only run this after step 6 (Confirm & Save) is complete, and only with explicit user confirmation.

> ⚠️ **Never push directly to the `gh-pages` branch.**
> That branch is generated exclusively by a GitHub Actions workflow triggered on merge to `main`.
> Pushing to it directly will corrupt the deployment and cause build errors.

## Steps

By the time this step runs, the branch `chat/{YYYYMMDD}-{topic}` already exists and the file is already committed (step 6).

1. Push:
   ```bash
   cd {projectDir}
   git push -u origin chat/{YYYYMMDD}-{topic}
   ```
2. Show guidance:
   ```
   ✓ Branch pushed: chat/{YYYYMMDD}-{topic}

   Next steps:
   1. Open https://github.com/{repo}/pull/new/chat/{YYYYMMDD}-{topic}
   2. Set the base branch to `main` (not gh-pages)
   3. Review and create PR → merging to main will trigger the GitHub Actions build
   ```
