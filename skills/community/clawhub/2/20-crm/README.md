# twenty-crm (VirusTotal-hardened fork)

This repository is based on the original work:
https://github.com/openclaw/skills/tree/main/skills/jhumanj/twenty-crm

This version focuses on fixing the VirusTotal issues that caused the original skill to be classified as suspicious.

## VirusTotal issue statement

"The skill is classified as suspicious primarily due to a query parameter injection vulnerability in `scripts/twenty-find-companies.sh` and `scripts/twenty-rest-get.sh`. User-provided search terms are incorporated into a URL query string without proper URL encoding, potentially allowing an attacker to inject arbitrary query parameters into the API request. Additionally, `scripts/twenty-config.sh` uses a hardcoded absolute path (`/Users/jhumanj/clawd/config/twenty.env`) for loading configuration, which is a poor practice and indicates a lack of portability or an assumption about a specific execution environment."

## Security fixes included

- Query parameter injection in `scripts/twenty-find-companies.sh` and `scripts/twenty-rest-get.sh` is fixed by removing raw query string concatenation and URL-encoding query parameter values safely.
- The hardcoded absolute config path in `scripts/twenty-config.sh` is removed and replaced with portable config resolution via `TWENTY_CONFIG_FILE` or repo-relative `config/twenty.env`.
- `scripts/twenty-create-company.sh` no longer writes request payload data to a fixed `/tmp` file.
- REST helpers now validate REST path input and reject embedded query strings in the path.

## Runtime requirements

- `curl`
- `python3`

## Secret handling

- Do not commit `TWENTY_API_KEY`.
- If using `config/twenty.env`, keep it private (for example: `chmod 600 config/twenty.env`).

## Scope

This fork is intended as a minimal, compatibility-oriented security remediation of the original `twenty-crm` skill.
