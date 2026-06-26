# API Key Creation Steps

## Prerequisites

Before generating an API key with trading functionality, please ensure that "Two-Factor Authentication (2FA)" is enabled. For API creation, KYC "C0 level (unverified)" is sufficient.

Note: If the API is only for read-only access, completing "Two-Factor Authentication (2FA)" is not required.

## Creation Steps

1. Log in to your CoinW account.
2. Navigate to the user ID next to "Deposit" in the upper right corner of the homepage, and select "API Management" from the dropdown menu.
3. Click "Create API" and enter a name for the API key. Then click "Confirm".
4. For security purposes, CoinW requires verification for each API key creation. Enter the authentication code and passkey to continue.
5. After verification, the "API Key" and "Secret Key" will be generated. The "Secret Key" is only visible for one hour, so please ensure it is securely stored.
6. By default, newly created API keys only have read-only access, and trading functionality is disabled. To enable trading, click "Edit" and select the necessary permissions.
7. By default, the user account has "Spot Trading" enabled. However, to activate "Futures Trading", the user must agree to the terms in the pop-up window when enabling "Futures Trading" for the API key.
8. To enable the "Withdrawal" option for the API, the user must configure an IP whitelist.
9. API access permissions are determined by "whether IP whitelist is enabled", not by the API's remark name. Therefore, if a new key is recreated and correctly IP-bound, deleting the old key will not affect current usage.