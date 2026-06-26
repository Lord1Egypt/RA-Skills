'''
EODHD API Client

This script provides a Python class to interact with the EOD Historical Data API.

Usage:
1. Make sure you have a `config.json` file in the root of the skill directory 
   with your API token: `{"api_token": "YOUR_API_TOKEN"}`.
2. Import the client: `from eodhd_client import EODHDClient`
3. Instantiate the client: `client = EODHDClient()`
4. Call the desired methods.
'''

import json
import os
import requests

class EODHDClient:
    def __init__(self, api_token=None):
        if api_token:
            self.api_token = api_token
        else:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            if not os.path.exists(config_path):
                raise FileNotFoundError("config.json not found. Please create it with your API token.")
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.api_token = config.get("api_token")

        if not self.api_token or self.api_token == "YOUR_API_TOKEN":
            raise ValueError("API token is not set or is invalid. Please check your config.json.")

        self.base_url = "https://eodhd.com/api"

    def _get_request(self, endpoint, params=None):
        '''Helper function to make a GET request to the API.'''
        if params is None:
            params = {}
        params['api_token'] = self.api_token
        params['fmt'] = 'json'
        
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "url": url, "params": params}

    def get_eod_historical_data(self, symbol, **kwargs):
        '''Get End-of-Day historical data.'''
        return self._get_request(f"eod/{symbol}", params=kwargs)

    def get_intraday_historical_data(self, symbol, **kwargs):
        '''Get intraday historical data.'''
        return self._get_request(f"intraday/{symbol}", params=kwargs)

    def get_real_time_data(self, symbol, **kwargs):
        '''Get real-time (delayed) data.'''
        return self._get_request(f"real-time/{symbol}", params=kwargs)

    def get_fundamental_data(self, symbol, **kwargs):
        '''Get fundamental data for stocks, ETFs, and funds.'''
        return self._get_request(f"fundamentals/{symbol}", params=kwargs)

    def get_technical_indicator(self, symbol, **kwargs):
        '''Get technical indicator data.'''
        if 'function' not in kwargs:
            return {"error": "The 'function' parameter is required for technical indicators."}
        return self._get_request(f"technical/{symbol}", params=kwargs)

    def get_financial_news(self, **kwargs):
        '''Get financial news.'''
        if 's' not in kwargs and 't' not in kwargs:
            return {"error": "Either a symbol 's' or a tag 't' is required for news."}
        return self._get_request("news", params=kwargs)

    def get_sentiment_data(self, **kwargs):
        '''Get sentiment data.'''
        return self._get_request("sentiments", params=kwargs)

    def get_options_data(self, symbol, **kwargs):
        '''Get options data.'''
        return self._get_request(f"options/{symbol}", params=kwargs)

    def get_screener_data(self, **kwargs):
        '''Get stock screener data.'''
        return self._get_request("screener", params=kwargs)

    def get_macro_indicator_data(self, country, **kwargs):
        '''Get macroeconomic indicator data.'''
        return self._get_request(f"macro-indicator/{country}", params=kwargs)

    def get_calendar_events(self, event_type, **kwargs):
        '''Get calendar events (earnings, IPOs).'''
        return self._get_request(f"calendar/{event_type}", params=kwargs)

    def get_exchange_list(self, **kwargs):
        '''Get the list of supported exchanges.'''
        return self._get_request("exchanges-list", params=kwargs)

    def get_exchange_symbols(self, exchange_code, **kwargs):
        '''Get the list of symbols for an exchange.'''
        return self._get_request(f"exchange-symbol-list/{exchange_code}", params=kwargs)

    def search_instrument(self, query, **kwargs):
        '''Search for an instrument.'''
        return self._get_request(f"search/{query}", params=kwargs)

    def get_dividends(self, symbol, **kwargs):
        '''Get dividend data.'''
        return self._get_request(f"div/{symbol}", params=kwargs)

    def get_splits(self, symbol, **kwargs):
        '''Get stock split data.'''
        return self._get_request(f"splits/{symbol}", params=kwargs)

    def get_bulk_eod(self, exchange_code, **kwargs):
        '''Get bulk EOD data for an exchange.'''
        return self._get_request(f"eod-bulk-last-day/{exchange_code}", params=kwargs)

# Example usage:
if __name__ == '__main__':
    try:
        client = EODHDClient()
        
        # Example 1: Get EOD data for AAPL.US
        print("Fetching EOD data for AAPL.US...")
        eod_data = client.get_eod_historical_data('AAPL.US', from_date='2023-01-01', to_date='2023-01-10')
        if 'error' in eod_data:
            print(f"Error: {eod_data['error']}")
        else:
            print(json.dumps(eod_data[:2], indent=2)) # Print first 2 results

        # Example 2: Get fundamental data for AAPL.US
        print("\nFetching fundamental data for AAPL.US...")
        fundamental_data = client.get_fundamental_data('AAPL.US', filter='General::Name,General::Sector')
        if 'error' in fundamental_data:
            print(f"Error: {fundamental_data['error']}")
        else:
            print(json.dumps(fundamental_data, indent=2))

        # Example 3: Get news for the technology tag
        print("\nFetching news for tag 'technology'...")
        news_data = client.get_financial_news(t='technology', limit=1)
        if 'error' in news_data:
            print(f"Error: {news_data['error']}")
        else:
            print(json.dumps(news_data, indent=2))

    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration Error: {e}")
