#!/usr/bin/env python3
"""
Auto-Tweet Agent — Safe, open-source Twitter automation via twikit.

A fully auditable replacement for openclaw-x that uses the open-source
twikit library (4.1K+ stars, MIT license) instead of a closed-source binary.

Features:
  - Post tweets (text + media)
  - Search tweets
  - Get timeline (For You / Following)
  - Like, retweet, bookmark
  - Get user info & user tweets
  - Get trends
  - Rate limiting for account safety
  - Local API on localhost (no external access)

Usage:
  python main.py                    # Start server (reads config.json)
  python main.py --port 19816       # Custom port
  python main.py --login            # Force re-login (ignores saved cookies)

License: MIT — fully open source, fully auditable.
"""

import asyncio
import json
import logging
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from twikit import Client
from twikit.errors import (
    AccountLocked,
    AccountSuspended,
    DuplicateTweet,
    Forbidden,
    TooManyRequests,
    TwitterException,
    Unauthorized,
)

from rate_limiter import RateLimiter

# Bypass Cloudflare TLS fingerprinting — replace httpx with curl_cffi shim
try:
    from curl_httpx_shim import CurlAsyncClient
    HAS_CURL_SHIM = True
except ImportError:
    HAS_CURL_SHIM = False

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("auto-tweet")

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
client: Client | None = None
limiter: RateLimiter | None = None
config: dict = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_config() -> dict:
    if not CONFIG_PATH.exists():
        log.error("config.json not found. Copy config.example.json → config.json and fill in credentials.")
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def _tweet_to_dict(tweet) -> dict:
    """Convert a twikit Tweet object to a JSON-serialisable dict."""
    return {
        "id": tweet.id,
        "text": tweet.text,
        "created_at": tweet.created_at,
        "user": {
            "id": tweet.user.id if tweet.user else None,
            "name": tweet.user.name if tweet.user else None,
            "screen_name": tweet.user.screen_name if tweet.user else None,
        },
        "favorite_count": getattr(tweet, "favorite_count", 0),
        "retweet_count": getattr(tweet, "retweet_count", 0),
        "reply_count": getattr(tweet, "reply_count", 0),
        "view_count": getattr(tweet, "view_count", None),
        "lang": getattr(tweet, "lang", None),
        "url": f"https://x.com/{tweet.user.screen_name}/status/{tweet.id}" if tweet.user else None,
    }


def _user_to_dict(user) -> dict:
    """Convert a twikit User object to a JSON-serialisable dict."""
    return {
        "id": user.id,
        "name": user.name,
        "screen_name": user.screen_name,
        "description": getattr(user, "description", None),
        "followers_count": getattr(user, "followers_count", 0),
        "following_count": getattr(user, "following_count", 0),
        "statuses_count": getattr(user, "statuses_count", 0),
        "profile_image_url": getattr(user, "profile_image_url", None),
        "verified": getattr(user, "verified", False),
        "is_blue_verified": getattr(user, "is_blue_verified", False),
    }


def _check_rate(is_tweet: bool = False) -> None:
    """Raise 429 if rate limit exceeded."""
    check = limiter.check_tweet() if is_tweet else limiter.check_general()
    if not check["allowed"]:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "RATE_LIMIT_EXCEEDED",
                "message": "Rate limit exceeded. Slow down to protect your account.",
                **limiter.get_status(),
            },
        )


def _handle_twitter_error(e: Exception) -> None:
    """Translate twikit exceptions to HTTP errors."""
    if isinstance(e, TooManyRequests):
        raise HTTPException(status_code=429, detail="Twitter rate limit hit. Wait a few minutes.")
    if isinstance(e, Unauthorized):
        raise HTTPException(status_code=401, detail="Twitter session expired. Restart server or re-login.")
    if isinstance(e, Forbidden):
        raise HTTPException(status_code=403, detail=f"Twitter forbidden: {e}")
    if isinstance(e, AccountSuspended):
        raise HTTPException(status_code=403, detail="Account suspended by Twitter.")
    if isinstance(e, AccountLocked):
        raise HTTPException(status_code=403, detail="Account locked. Complete challenge on x.com first.")
    if isinstance(e, DuplicateTweet):
        raise HTTPException(status_code=409, detail="Duplicate tweet. Twitter rejected it.")
    if isinstance(e, TwitterException):
        raise HTTPException(status_code=500, detail=f"Twitter error: {e}")
    raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Login on startup, cleanup on shutdown."""
    global client, limiter, config

    config = load_config()
    rl = config.get("rate_limits", {})
    limiter = RateLimiter(
        max_per_hour=rl.get("max_per_hour", 30),
        max_per_day=rl.get("max_per_day", 200),
        tweet_per_day=rl.get("tweet_per_day", 20),
    )

    dry_run = "--dry-run" in sys.argv
    if dry_run:
        log.info("🧪 DRY-RUN mode — skipping Twitter login")
        client = None
        log.info("🚀 Auto-Tweet Agent ready (DRY-RUN) on http://%s:%s",
                 config.get("server", {}).get("host", "127.0.0.1"),
                 config.get("server", {}).get("port", 19816))
        yield
        log.info("Shutting down Auto-Tweet Agent")
        return

    language = config.get("language", "en-US")
    proxy = config.get("proxy")

    # Create twikit client, then replace its httpx client with curl_cffi shim
    client = Client(language, proxy=proxy)

    if HAS_CURL_SHIM:
        log.info("Replacing httpx client with curl_cffi shim (Chrome TLS impersonation)")
        client.http = CurlAsyncClient(proxy=proxy)
    else:
        log.warning("curl_cffi shim not available — using default httpx (may hit Cloudflare 403)")

    cookies_file = str(BASE_DIR / config.get("cookies_file", "cookies.json"))
    force_login = "--login" in sys.argv

    async def _login_once_or_retry():
        retry_delays = [300, 300, 600, 600, 1800, 1800, 3600]  # 5m, 5m, 10m, 10m, 30m, 30m, 60m
        attempt = 0
        while True:
            try:
                if os.path.exists(cookies_file) and not force_login:
                    log.info("Loading saved cookies from %s", cookies_file)
                    client.load_cookies(cookies_file)
                    try:
                        uid = await client.user_id()
                        me = await client.user()
                        log.info("✅ Cookie login successful — @%s (id=%s)", me.screen_name, uid)
                        return
                    except Exception:
                        log.warning("Saved cookies invalid. Performing fresh login...")
                await _do_login(cookies_file)
                return
            except SystemExit:
                raise
            except Exception as e:
                if "AccountLocked" in type(e).__name__:
                    raise
                delay = retry_delays[min(attempt, len(retry_delays) - 1)]
                log.warning("⏳ Login attempt %d failed (%s). Retrying in %ds...", attempt + 1, type(e).__name__, delay)
                attempt += 1
                await asyncio.sleep(delay)

    await _login_once_or_retry()

    log.info("🚀 Auto-Tweet Agent ready on http://%s:%s",
             config.get("server", {}).get("host", "127.0.0.1"),
             config.get("server", {}).get("port", 19816))
    log.info("📖 API docs: http://%s:%s/docs",
             config.get("server", {}).get("host", "127.0.0.1"),
             config.get("server", {}).get("port", 19816))

    yield  # App running

    log.info("Shutting down Auto-Tweet Agent")


async def _do_login(cookies_file: str) -> None:
    """Perform username/password login and save cookies."""
    username = config.get("username", "")
    email = config.get("email")
    password = config.get("password", "")
    totp = config.get("totp_secret")

    if not username or not password:
        log.error("username and password required in config.json")
        sys.exit(1)

    log.info("Logging in as %s ...", username)
    # Clear stale cookies to avoid CookieConflict on .x.com/.twitter.com
    try:
        client.http.cookies.clear()
    except Exception:
        pass
    try:
        await client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password,
            totp_secret=totp,
            cookies_file=cookies_file,
        )
        me = await client.user()
        log.info("✅ Login successful — @%s", me.screen_name)
    except AccountLocked:
        log.error("❌ Account locked. Complete the challenge at x.com first, then retry.")
        raise
    except Exception as e:
        log.error("❌ Login failed: %s", e)
        log.error("💡 If you see error 399, your IP may be rate-limited (retrying in 5 min).")
        raise


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Auto-Tweet Agent",
    description=(
        "Safe, open-source Twitter automation powered by twikit.\n\n"
        "A fully auditable replacement for openclaw-x.\n"
        "All code is transparent Python — no closed-source binaries."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
class TweetRequest(BaseModel):
    text: str
    media_paths: Optional[list[str]] = None
    reply_to: Optional[str] = None
    quote_url: Optional[str] = None
    is_note_tweet: bool = False


class ScheduledTweetRequest(BaseModel):
    text: str
    scheduled_at: int  # Unix timestamp
    media_paths: Optional[list[str]] = None


class ActionRequest(BaseModel):
    tweet_id: str


class DMRequest(BaseModel):
    user_id: str
    text: str


# ---------------------------------------------------------------------------
# Routes: Info
# ---------------------------------------------------------------------------
@app.get("/", tags=["Info"])
async def root():
    """Health check and server info."""
    if client is None:
        return {
            "status": "dry-run",
            "agent": "auto-tweet",
            "version": "1.0.0",
            "engine": "twikit (open source, MIT, 4.1K+ stars)",
            "account": "(not connected — dry-run mode)",
            "rate_limits": limiter.get_status(),
            "docs": "/docs",
        }
    me = await client.user()
    return {
        "status": "ok",
        "agent": "auto-tweet",
        "version": "1.0.0",
        "engine": "twikit (open source, MIT, 4.1K+ stars)",
        "account": f"@{me.screen_name}",
        "rate_limits": limiter.get_status(),
        "docs": "/docs",
    }


@app.get("/health", tags=["Info"])
async def health():
    """Health check endpoint — lightweight status check."""
    return {
        "status": "dry-run" if client is None else "ok",
        "agent": "auto-tweet",
        "version": "1.0.0",
    }


@app.get("/me", tags=["Info"])
async def get_me():
    """Get authenticated user info."""
    _check_rate()
    try:
        me = await client.user()
        limiter.record_action()
        return _user_to_dict(me)
    except Exception as e:
        _handle_twitter_error(e)


@app.get("/rate_limits", tags=["Info"])
async def get_rate_limits():
    """Get current rate limit status."""
    return limiter.get_status()


# ---------------------------------------------------------------------------
# Routes: Tweets
# ---------------------------------------------------------------------------
@app.post("/tweet", tags=["Tweets"])
async def post_tweet(req: TweetRequest):
    """Post a new tweet."""
    _check_rate(is_tweet=True)
    try:
        media_ids = None
        if req.media_paths:
            media_ids = []
            for path in req.media_paths:
                mid = await client.upload_media(path, wait_for_completion=True)
                media_ids.append(mid)

        tweet = await client.create_tweet(
            text=req.text,
            media_ids=media_ids,
            reply_to=req.reply_to,
            attachment_url=req.quote_url,
            is_note_tweet=req.is_note_tweet,
        )
        limiter.record_action(is_tweet=True)
        log.info("✅ Tweet posted: %s", tweet.id)
        return _tweet_to_dict(tweet)
    except Exception as e:
        _handle_twitter_error(e)


@app.delete("/tweet/{tweet_id}", tags=["Tweets"])
async def delete_tweet(tweet_id: str):
    """Delete a tweet by ID."""
    _check_rate()
    try:
        await client.delete_tweet(tweet_id)
        limiter.record_action()
        return {"status": "deleted", "tweet_id": tweet_id}
    except Exception as e:
        _handle_twitter_error(e)


@app.post("/schedule", tags=["Tweets"])
async def schedule_tweet(req: ScheduledTweetRequest):
    """Schedule a tweet for later."""
    _check_rate(is_tweet=True)
    try:
        media_ids = None
        if req.media_paths:
            media_ids = []
            for path in req.media_paths:
                mid = await client.upload_media(path, wait_for_completion=True)
                media_ids.append(mid)

        sid = await client.create_scheduled_tweet(
            scheduled_at=req.scheduled_at,
            text=req.text,
            media_ids=media_ids,
        )
        limiter.record_action(is_tweet=True)
        return {"status": "scheduled", "scheduled_tweet_id": sid}
    except Exception as e:
        _handle_twitter_error(e)


@app.get("/scheduled", tags=["Tweets"])
async def list_scheduled_tweets():
    """List all scheduled tweets."""
    _check_rate()
    try:
        tweets = await client.get_scheduled_tweets()
        limiter.record_action()
        return [{"id": t.id, "text": t.text, "scheduled_at": t.scheduled_at} for t in tweets]
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: Timeline
# ---------------------------------------------------------------------------
@app.get("/timeline", tags=["Timeline"])
async def get_timeline(count: int = Query(20, ge=1, le=40)):
    """Get home timeline (For You)."""
    _check_rate()
    try:
        tweets = await client.get_timeline(count=count)
        limiter.record_action()
        return [_tweet_to_dict(t) for t in tweets]
    except Exception as e:
        _handle_twitter_error(e)


@app.get("/timeline/following", tags=["Timeline"])
async def get_following_timeline(count: int = Query(20, ge=1, le=40)):
    """Get home timeline (Following)."""
    _check_rate()
    try:
        tweets = await client.get_latest_timeline(count=count)
        limiter.record_action()
        return [_tweet_to_dict(t) for t in tweets]
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: Search
# ---------------------------------------------------------------------------
@app.get("/search", tags=["Search"])
async def search_tweets(
    q: str = Query(..., description="Search query"),
    type: str = Query("Latest", description="Top, Latest, or Media"),
    count: int = Query(20, ge=1, le=20),
):
    """Search for tweets."""
    _check_rate()
    if type not in ("Top", "Latest", "Media"):
        raise HTTPException(status_code=400, detail="type must be Top, Latest, or Media")
    try:
        tweets = await client.search_tweet(q, type, count=count)
        limiter.record_action()
        return [_tweet_to_dict(t) for t in tweets]
    except Exception as e:
        _handle_twitter_error(e)


@app.get("/search/users", tags=["Search"])
async def search_users(
    q: str = Query(..., description="Search query"),
    count: int = Query(20, ge=1, le=20),
):
    """Search for users."""
    _check_rate()
    try:
        users = await client.search_user(q, count=count)
        limiter.record_action()
        return [_user_to_dict(u) for u in users]
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: Actions (like, retweet, bookmark)
# ---------------------------------------------------------------------------
@app.post("/like", tags=["Actions"])
async def like_tweet(req: ActionRequest):
    """Like a tweet."""
    _check_rate()
    try:
        await client.favorite_tweet(req.tweet_id)
        limiter.record_action()
        return {"status": "liked", "tweet_id": req.tweet_id}
    except Exception as e:
        _handle_twitter_error(e)


@app.post("/unlike", tags=["Actions"])
async def unlike_tweet(req: ActionRequest):
    """Unlike a tweet."""
    _check_rate()
    try:
        await client.unfavorite_tweet(req.tweet_id)
        limiter.record_action()
        return {"status": "unliked", "tweet_id": req.tweet_id}
    except Exception as e:
        _handle_twitter_error(e)


@app.post("/retweet", tags=["Actions"])
async def retweet(req: ActionRequest):
    """Retweet a tweet."""
    _check_rate()
    try:
        await client.retweet(req.tweet_id)
        limiter.record_action()
        return {"status": "retweeted", "tweet_id": req.tweet_id}
    except Exception as e:
        _handle_twitter_error(e)


@app.post("/unretweet", tags=["Actions"])
async def unretweet(req: ActionRequest):
    """Undo a retweet."""
    _check_rate()
    try:
        await client.delete_retweet(req.tweet_id)
        limiter.record_action()
        return {"status": "unretweeted", "tweet_id": req.tweet_id}
    except Exception as e:
        _handle_twitter_error(e)


@app.post("/bookmark", tags=["Actions"])
async def bookmark_tweet(req: ActionRequest):
    """Bookmark a tweet."""
    _check_rate()
    try:
        await client.bookmark_tweet(req.tweet_id)
        limiter.record_action()
        return {"status": "bookmarked", "tweet_id": req.tweet_id}
    except Exception as e:
        _handle_twitter_error(e)


@app.post("/unbookmark", tags=["Actions"])
async def unbookmark_tweet(req: ActionRequest):
    """Remove a bookmark."""
    _check_rate()
    try:
        await client.delete_bookmark(req.tweet_id)
        limiter.record_action()
        return {"status": "unbookmarked", "tweet_id": req.tweet_id}
    except Exception as e:
        _handle_twitter_error(e)


@app.get("/bookmarks", tags=["Actions"])
async def get_bookmarks(count: int = Query(20, ge=1, le=40)):
    """Get bookmarked tweets."""
    _check_rate()
    try:
        tweets = await client.get_bookmarks(count=count)
        limiter.record_action()
        return [_tweet_to_dict(t) for t in tweets]
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: Users
# ---------------------------------------------------------------------------
@app.get("/user/{screen_name}", tags=["Users"])
async def get_user(screen_name: str):
    """Get user profile by screen name."""
    _check_rate()
    try:
        user = await client.get_user_by_screen_name(screen_name)
        limiter.record_action()
        return _user_to_dict(user)
    except Exception as e:
        _handle_twitter_error(e)


@app.get("/user/{screen_name}/tweets", tags=["Users"])
async def get_user_tweets(
    screen_name: str,
    type: str = Query("Tweets", description="Tweets, Replies, Media, or Likes"),
    count: int = Query(20, ge=1, le=40),
):
    """Get tweets from a user."""
    _check_rate()
    if type not in ("Tweets", "Replies", "Media", "Likes"):
        raise HTTPException(status_code=400, detail="type must be Tweets, Replies, Media, or Likes")
    try:
        user = await client.get_user_by_screen_name(screen_name)
        tweets = await client.get_user_tweets(user.id, type, count=count)
        limiter.record_action()
        return [_tweet_to_dict(t) for t in tweets]
    except Exception as e:
        _handle_twitter_error(e)


@app.get("/tweet/{tweet_id}", tags=["Tweets"])
async def get_tweet(tweet_id: str):
    """Get a specific tweet by ID."""
    _check_rate()
    try:
        tweet = await client.get_tweet_by_id(tweet_id)
        limiter.record_action()
        return _tweet_to_dict(tweet)
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: Trends
# ---------------------------------------------------------------------------
@app.get("/trends", tags=["Trends"])
async def get_trends(
    category: str = Query("trending", description="trending, for-you, news, sports, entertainment"),
):
    """Get trending topics."""
    _check_rate()
    valid = ("trending", "for-you", "news", "sports", "entertainment")
    if category not in valid:
        raise HTTPException(status_code=400, detail=f"category must be one of {valid}")
    try:
        trends = await client.get_trends(category)
        limiter.record_action()
        return [
            {
                "name": t.name,
                "tweets_count": getattr(t, "tweets_count", None),
                "domain_context": getattr(t, "domain_context", None),
            }
            for t in trends
        ]
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: DM
# ---------------------------------------------------------------------------
@app.post("/dm", tags=["DM"])
async def send_dm(req: DMRequest):
    """Send a direct message."""
    _check_rate()
    try:
        msg = await client.send_dm(req.user_id, req.text)
        limiter.record_action()
        return {"status": "sent", "message_id": msg.id}
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: Notifications
# ---------------------------------------------------------------------------
@app.get("/notifications", tags=["Notifications"])
async def get_notifications(
    type: str = Query("All", description="All, Verified, or Mentions"),
    count: int = Query(20, ge=1, le=40),
):
    """Get notifications."""
    _check_rate()
    if type not in ("All", "Verified", "Mentions"):
        raise HTTPException(status_code=400, detail="type must be All, Verified, or Mentions")
    try:
        notifs = await client.get_notifications(type, count=count)
        limiter.record_action()
        return [
            {
                "id": n.id,
                "message": getattr(n, "message", None),
                "timestamp_ms": getattr(n, "timestamp_ms", None),
            }
            for n in notifs
        ]
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Routes: Follow / Unfollow
# ---------------------------------------------------------------------------
@app.post("/follow/{user_id}", tags=["Users"])
async def follow_user(user_id: str):
    """Follow a user by ID."""
    _check_rate()
    try:
        user = await client.follow_user(user_id)
        limiter.record_action()
        return {"status": "followed", "user": _user_to_dict(user)}
    except Exception as e:
        _handle_twitter_error(e)


@app.post("/unfollow/{user_id}", tags=["Users"])
async def unfollow_user(user_id: str):
    """Unfollow a user by ID."""
    _check_rate()
    try:
        user = await client.unfollow_user(user_id)
        limiter.record_action()
        return {"status": "unfollowed", "user": _user_to_dict(user)}
    except Exception as e:
        _handle_twitter_error(e)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    cfg = load_config()
    server = cfg.get("server", {})
    host = server.get("host", "127.0.0.1")
    port = server.get("port", 19816)

    # Allow --port override
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])

    uvicorn.run("main:app", host=host, port=port, reload=False, log_level="info")
