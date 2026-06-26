"""
Rate limiter for Twitter API calls.
Prevents exceeding safe thresholds to avoid account suspension.
"""

import time
from collections import deque
from dataclasses import dataclass, field


@dataclass
class RateLimiter:
    """Sliding window rate limiter for Twitter actions."""

    max_per_hour: int = 30
    max_per_day: int = 200
    tweet_per_day: int = 20

    _hourly_window: deque = field(default_factory=deque)
    _daily_window: deque = field(default_factory=deque)
    _tweet_window: deque = field(default_factory=deque)

    def _prune(self, window: deque, max_age: float) -> None:
        now = time.time()
        while window and (now - window[0]) > max_age:
            window.popleft()

    def check_general(self) -> dict:
        """Check if a general API call is allowed."""
        self._prune(self._hourly_window, 3600)
        self._prune(self._daily_window, 86400)

        hourly_remaining = self.max_per_hour - len(self._hourly_window)
        daily_remaining = self.max_per_day - len(self._daily_window)

        allowed = hourly_remaining > 0 and daily_remaining > 0
        return {
            "allowed": allowed,
            "hourly_remaining": max(0, hourly_remaining),
            "daily_remaining": max(0, daily_remaining),
            "hourly_used": len(self._hourly_window),
            "daily_used": len(self._daily_window),
        }

    def check_tweet(self) -> dict:
        """Check if posting a tweet is allowed."""
        general = self.check_general()
        self._prune(self._tweet_window, 86400)
        tweet_remaining = self.tweet_per_day - len(self._tweet_window)
        allowed = general["allowed"] and tweet_remaining > 0
        return {
            **general,
            "allowed": allowed,
            "tweet_remaining": max(0, tweet_remaining),
            "tweets_today": len(self._tweet_window),
        }

    def record_action(self, is_tweet: bool = False) -> None:
        """Record that an action was performed."""
        now = time.time()
        self._hourly_window.append(now)
        self._daily_window.append(now)
        if is_tweet:
            self._tweet_window.append(now)

    def get_status(self) -> dict:
        """Get current rate limit status."""
        self._prune(self._hourly_window, 3600)
        self._prune(self._daily_window, 86400)
        self._prune(self._tweet_window, 86400)
        return {
            "hourly_used": len(self._hourly_window),
            "hourly_limit": self.max_per_hour,
            "hourly_remaining": max(0, self.max_per_hour - len(self._hourly_window)),
            "daily_used": len(self._daily_window),
            "daily_limit": self.max_per_day,
            "daily_remaining": max(0, self.max_per_day - len(self._daily_window)),
            "tweets_today": len(self._tweet_window),
            "tweet_limit": self.tweet_per_day,
            "tweet_remaining": max(0, self.tweet_per_day - len(self._tweet_window)),
        }
