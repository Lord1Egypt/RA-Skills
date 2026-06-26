import time

class Cache:

    def __init__(self):
        self.store = {}

    def get(self, key):

        item = self.store.get(key)

        if not item:
            return None

        value, expiry = item

        if time.time() > expiry:
            del self.store[key]
            return None

        return value

    def set(self, key, value, ttl):

        self.store[key] = (
            value,
            time.time() + ttl
        )

    def get_or_fetch(self, key, fetch_fn, ttl=900):

        cached = self.get(key)

        if cached:
            return cached

        value = fetch_fn()

        self.set(key, value, ttl)

        return value