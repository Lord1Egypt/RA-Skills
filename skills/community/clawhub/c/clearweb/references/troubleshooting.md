# Troubleshooting Reference

Common errors, their causes, and solutions for ClearWeb / Bright Data CLI.

## Installation Issues

| Problem | Solution |
|---------|----------|
| `bdata: command not found` | Install: `curl -fsSL https://cli.brightdata.com/install.sh \| bash` or `npm i -g @brightdata/cli` |
| `npm ERR! engine` | Node.js >= 20 required. Update Node.js first. |
| Install succeeds but command not found | Shell PATH not updated. Run `source ~/.bashrc` or start a new terminal. |
| Permission denied on install | Use `sudo npm i -g @brightdata/cli` or fix npm prefix: `npm config set prefix ~/.npm-global` |

## Authentication Issues

| Problem | Solution |
|---------|----------|
| "Invalid or expired API key" | Re-run `bdata login` |
| Browser doesn't open on login | Use `bdata login --device` for headless environments |
| "No Web Unlocker zone specified" | Run `bdata login` (auto-creates zones) or `bdata config set default_zone_unlocker <zone>` |
| "Access denied" | Check zone permissions in the [Bright Data control panel](https://brightdata.com/cp) |
| Need to switch accounts | `bdata logout` then `bdata login` |

## Scraping Issues

| Problem | Solution |
|---------|----------|
| Empty or minimal output | The page may require JS rendering. Try `bdata scrape <url> -f html` to check raw content. |
| Timeout on large pages | Use `--async` mode: `bdata scrape <url> --async`, then `bdata status <id> --wait --timeout 1200` |
| Wrong geo-content | Add `--country <code>`: `bdata scrape <url> --country us` |
| Binary output to terminal | Use `-o file.png` for screenshots. Never pipe binary to stdout. |
| "Rate limit exceeded" | Wait 30 seconds and retry, or use `--async` for large jobs |

## Search Issues

| Problem | Solution |
|---------|----------|
| No results returned | Check query spelling. Try broader terms. |
| Results in wrong language | Add `--country` and `--language` flags |
| Bing/Yandex returns markdown, not JSON | Only Google returns structured JSON. For Bing/Yandex, parse the markdown output. |
| Pagination not working | Pages are 0-indexed: `--page 0` is first, `--page 1` is second |

## Pipeline Issues

| Problem | Solution |
|---------|----------|
| "Unknown pipeline type" | Run `bdata pipelines list` to see available types |
| Timeout during polling | Increase: `--timeout 1200` or `BRIGHTDATA_POLLING_TIMEOUT=1200` |
| Empty results from pipeline | Verify the URL format matches the platform (e.g., Amazon needs `/dp/` in URL) |
| "Dataset not found" | The pipeline type name may have changed. Check `bdata pipelines list` |
| LinkedIn returns empty | Ensure the profile URL is complete (no shortened URLs) |

## Output Issues

| Problem | Solution |
|---------|----------|
| Colors/ANSI codes in output | Pipe through `cat` or use `--json` flag for clean output |
| JSON parsing errors | Use `--json` flag to ensure valid JSON output |
| File output empty | Check the path exists and you have write permissions |
| CSV formatting issues | Ensure `--format csv` is specified (not just `.csv` extension) |

## Environment Variable Reference

Set these to override stored configuration:

```bash
# Skip login entirely — provide API key directly
export BRIGHTDATA_API_KEY="your-api-key"

# Override default Web Unlocker zone
export BRIGHTDATA_UNLOCKER_ZONE="my_zone"

# Override default SERP zone
export BRIGHTDATA_SERP_ZONE="my_serp_zone"

# Increase polling timeout (seconds)
export BRIGHTDATA_POLLING_TIMEOUT=1200
```

## Configuration Priority

CLI flags > Environment variables > config.json > Defaults

```bash
# View all current config
bdata config

# Reset a config value
bdata config set default_zone_unlocker cli_unlocker

# View stored credentials location
# macOS: ~/Library/Application Support/brightdata-cli/
# Linux: ~/.config/brightdata-cli/
# Windows: %APPDATA%\brightdata-cli\
```

## Getting Help

```bash
# CLI version and system info
bdata version

# Command help
bdata --help
bdata scrape --help
bdata search --help
bdata pipelines --help

# Check account balance
bdata budget
```

## Nuclear Reset

If everything is broken, start fresh:

```bash
# Clear all stored data
bdata logout

# Re-authenticate (creates fresh zones)
bdata login

# Verify
bdata config
bdata budget
```
