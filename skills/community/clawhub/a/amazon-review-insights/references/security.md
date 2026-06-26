# AstrMap Desktop Client Security Guide

## Privacy Risk Statement

Using this skill involves the following data access. Users should understand before installation:

| Component | Data Access Scope | Risk Level |
|-----------|------------------|------------|
| AstrMap Desktop Client | Log in to Amazon buyer account, read review data | Medium (third-party app accessing your Amazon account) |
| This Skill (api_client.py) | Only calls AstrMap API, does not directly access Amazon | Low (only communicates with api.astrmap.com) |
| API Key | Sent to api.astrmap.com for authentication | Medium (sensitive credential) |

**Important Notes**:
- This skill does not request or handle your Amazon account credentials
- Amazon login is handled locally by the AstrMap desktop client; skill code does not participate
- If not using desktop client features (like querying completed analysis results), Amazon login is not required

## Desktop Client Download Verification

Download links are obtained from `https://www.astrmap.com/download-config.json`. **You must verify after downloading**:

- **HTTPS Verification**: Ensure download links start with `https://`; browsers validate TLS certificates
- **File Integrity**: After downloading, **must** verify file integrity using the checksum (included in download config)
- **Code Signature Verification** (macOS): Right-click Astrmap.app → Get Info, confirm it's signed by AstrMap official
- **Source Verification**: Download link is from `https://www.astrmap.com`, official AstrMap source

## Amazon Account Security

The desktop client requires logging in to an Amazon buyer account for data collection. Recommended:

- **Do not use primary account**: Do not use your seller main account or business-related account
- **Dedicated account**: Create a dedicated buyer account for data collection
- **Account isolation**: Strictly separate the dedicated account from your seller account

## API Key Security

The API Key is sent to `api.astrmap.com` for authentication. Please:

- **Keep it safe**: Do not share your API Key in public
- **Regular rotation**: If you stop using the service, consider disabling or rotating your API Key
- **Environment variable**: Recommended to pass via `CUSTOMER_INSIGHTS_API_KEY` environment variable rather than hardcoding in scripts

> Tip: After initial launch, you can directly double-click Astrmap.app (or desktop shortcut) to start.
