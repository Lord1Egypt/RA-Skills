#!/usr/bin/env python3
import os
import ccxt

def get_lighter_client():
    private_key = os.getenv("LIGHTER_API_PRIVATE_KEY")
    api_key_index = int(os.getenv("LIGHTER_API_KEY_INDEX"))
    account_index = int(os.getenv("LIGHTER_ACCOUNT_INDEX"))

    exchange = ccxt.lighter({
        'privateKey': private_key,
        'options': {
            'apiKeyIndex': api_key_index,
            'accountIndex': account_index,
        },
        'enableRateLimit': True,
    })
    return exchange