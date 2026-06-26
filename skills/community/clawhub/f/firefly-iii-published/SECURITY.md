# Security Considerations

This skill communicates with the Firefly III API using your personal OAuth token and URL. 

- **Token Safety**: Your token provides full programmatic access to your financial data. Keep it secure and avoid sharing it.
- **Environment Variables**: Never hardcode credentials in your script. Use secure environment variables as documented in the Setup section.
- **Network Access**: If you are using this skill in an environment where you are unsure of network security, consider using an isolated network or VPN.
- **Data Privacy**: All data processing happens on your local machine and your Firefly III instance. No data is shared with external services by this skill beyond your own Firefly III API.
