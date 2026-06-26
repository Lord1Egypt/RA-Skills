# Security Policy

## Encryption Note

Version 1.1.0 and earlier used AES-256-CBC encryption for webhook URL storage in the configuration file.

**Important:** As of v1.1.1, encryption has been removed for ClawHub compatibility. Webhook URLs are now stored in plain text in the configuration file.

If you need to protect sensitive webhook URLs, consider:
- Using file permissions to restrict access to `config.json`
- Implementing encryption at the application level outside this skill
- Using environment variables for sensitive configuration

## Reporting Security Issues

If you discover a security vulnerability in this skill, please report it by creating an issue on GitHub.

## Data Sources

This skill fetches earthquake data from:
- China Earthquake Networks Center (CENC)
- Taiwan Central Weather Administration (CWA)  
- Japan Meteorological Agency (JMA)

No personal data is collected or transmitted to third parties beyond these official government data sources.
