# AstrMap Browser Extension Security Guide

## Privacy Risk Statement

Using this skill involves the following data access. Users should understand before installation:

| Component | Data Access Scope | Risk Level |
|-----------|------------------|------------|
| AstrMap Browser Extension | Sign in to an Amazon buyer account in the browser, read review data | Medium (extension can access data of sites you are signed in to) |
| This Skill (api_client.py) | Only calls AstrMap API, does not directly access Amazon | Low (only communicates with api.astrmap.com) |
| API Key | Sent to api.astrmap.com for authentication | Medium (sensitive credential) |

**Important Notes**:
- This skill does not request or handle your Amazon account credentials
- Amazon login happens inside your browser; skill code does not participate
- If you only query completed analysis results, no collection component and no Amazon login is required

## Extension Download Verification

Download links are obtained from `https://www.astrmap.com/download-config.json`. **You must verify after downloading**:

- **HTTPS Verification**: Ensure download links start with `https://`; browsers validate TLS certificates
- **Source Verification**: Download link is from `https://www.astrmap.com`, official AstrMap source
- **Installation Method**: Installed via Chrome's "Load unpacked"; you can review its requested permissions at `chrome://extensions/` before installing

## Amazon Account Security

The browser extension requires signing in to an Amazon buyer account for data collection. Recommended:

- **Do not use primary account**: Do not use your seller main account or business-related account
- **Dedicated account**: Create a dedicated buyer account for data collection
- **Account isolation**: Strictly separate the dedicated account from your seller account

## API Key Security

The API Key is sent to `api.astrmap.com` for authentication. Please:

- **Keep it safe**: Do not share your API Key in public
- **Regular rotation**: If you stop using the service, go to https://app.astrmap.com/, open the **User Menu (bottom-left) → API Keys**, and disable or rotate it
- **Environment variable**: Recommended to pass via `CUSTOMER_INSIGHTS_API_KEY` environment variable rather than hardcoding in scripts
