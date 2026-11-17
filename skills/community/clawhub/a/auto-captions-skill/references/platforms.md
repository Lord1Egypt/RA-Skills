# Platforms: shapes, limits and subtitle files

| Platform | Best shape | Length (API) | Notes |
|---|---|---|---|
| TikTok | 9:16 | 3 s to 10 min (the account's own limit can be lower) | 23 to 60 fps, up to 4 GB; no subtitle file through the API, so burn in |
| Instagram Reels | 9:16 | 3 s to 15 min | up to 300 MB, 23 to 60 fps, 5 hashtags at most; no subtitle file through the API |
| YouTube Shorts | 9:16 or 1:1 | up to 3 min | subtitle file in YouTube Studio |
| YouTube | 16:9 | long | prefer a subtitle file (viewers can switch it off) over burned-in captions |
| Facebook | 9:16 Reels (3 to 90 s), any for video | | subtitle file in the video's settings |
| LinkedIn | 4:5, 1:1 or 16:9 | 3 s to 15 min | up to 5 GB; autoplays muted, so clean captions plus the SRT |
| X | 16:9 or 1:1 | up to 2 min 20 s on most accounts | up to 512 MB |
| Threads | 9:16 or 4:5 | up to 5 min | |
| Bluesky | any | up to 3 min | up to 100 MB |

`post_plan.py` checks these before anything is uploaded.

Burned-in captions are the only captions you control on TikTok and Instagram when posting
through an API. YouTube, Facebook, LinkedIn and X also accept a subtitle (SRT) file in their own
apps, which viewers can switch on and off; `plan.md` lists where to add each one.

What's documented about search: TikTok lists a video's captions, sounds and hashtags as
information it uses for recommendations, and Instagram and YouTube read the post's own text. No
platform has confirmed that burned-in captions help ranking. The post text is what to optimise:
plain words saying what the video is about.
