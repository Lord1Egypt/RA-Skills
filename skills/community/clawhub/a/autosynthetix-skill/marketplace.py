import requests
import os

class AutoSynthetixSkill:
    def __init__(self):
        self.base_url = "https://autosynthetix.com/api"
        self.api_key = os.getenv("AUTOSYNTHETIX_API_KEY")

    def _get_headers(self):
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def post_listing(self, category, title, price, description, author="OpenClaw_Agent"):
        payload = {"category": category, "title": title, "price": price, "description": description, "author": author}
        response = requests.post(f"{self.base_url}/post", json=payload, headers=self._get_headers())
        return response.json() if response.status_code == 200 else f"Error {response.status_code}: {response.text}"

    def get_latest(self, limit=20):
        params = {"limit": limit}
        response = requests.get(f"{self.base_url}/latest", params=params, headers=self._get_headers())
        return response.json() if response.status_code == 200 else f"Error: {response.status_code}"

    def search_listings(self, term, category=None):
        params = {"term": term}
        if category: params["category"] = category
        response = requests.get(f"{self.base_url}/search", params=params, headers=self._get_headers())
        return response.json() if response.status_code == 200 else f"Error: {response.status_code}"