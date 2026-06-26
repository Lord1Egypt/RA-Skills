
## v3.1 — 2026-03-19
### Fixed
- **Clone auth fix**: Replaced manual `GH_TOKEN` URL injection (`git clone https://$TOKEN@...`) with `gh repo clone` in both `backup.sh` and `restore.sh`. The old method failed silently when git's credential helper intercepted the URL or on systems where private repo auth via token-in-URL is blocked. `gh repo clone` uses the gh auth system directly and is always reliable.
