# Spotify Setup Guide for Bumblebee 🐝🎧

## What You Need

- **Spotify Premium** account (free tier doesn't support playback control)
- **Node.js** 18+ installed
- **OpenClaw** installed and running

## Step 1: Create a Spotify App

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click **"Create App"**
4. Fill in:
   - **App name:** Bumblebee (or whatever you want)
   - **App description:** AI music agent
   - **Redirect URI:** `http://localhost:8888/callback`
   - **APIs used:** Check "Web API" and "Web Playback SDK"
5. Click **"Save"**
6. Go to **Settings** → copy your **Client ID** and **Client Secret**

## Step 2: Set Up Credentials

Create a directory for your Spotify tokens:

```bash
mkdir -p ~/. openclaw/workspace/projects/spotify
```

Create `projects/spotify/.env`:

```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## Step 3: Get Your OAuth Tokens

Run this one-time authorization flow. Paste this into a terminal:

```bash
# Set your credentials
CLIENT_ID="your_client_id"
CLIENT_SECRET="your_client_secret"
REDIRECT_URI="http://localhost:8888/callback"

# Scopes needed for full playback + library control
SCOPES="playlist-read-private playlist-read-collaborative streaming user-modify-playback-state user-library-read user-library-modify playlist-modify-private playlist-modify-public user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read"

# URL-encode the scopes
ENCODED_SCOPES=$(echo "$SCOPES" | sed 's/ /%20/g')

# Open this URL in your browser
echo "Open this URL in your browser:"
echo "https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&response_type=code&redirect_uri=$(echo $REDIRECT_URI | sed 's/:/%3A/g' | sed 's/\//%2F/g')&scope=${ENCODED_SCOPES}"
```

1. Open the URL in your browser
2. Click **"Agree"** to authorize
3. You'll be redirected to `localhost:8888/callback?code=XXXXXX`
4. Copy the `code` value from the URL

Now exchange the code for tokens:

```bash
CODE="paste_your_code_here"
CLIENT_ID="your_client_id"
CLIENT_SECRET="your_client_secret"

curl -X POST https://accounts.spotify.com/api/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic $(echo -n "${CLIENT_ID}:${CLIENT_SECRET}" | base64)" \
  -d "grant_type=authorization_code&code=${CODE}&redirect_uri=http://localhost:8888/callback"
```

Save the JSON response as `projects/spotify/tokens.json`. It should look like:

```json
{
  "access_token": "BQAt...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "AQDf...",
  "scope": "playlist-read-private streaming user-modify-playback-state ..."
}
```

**Important:** The `refresh_token` is permanent. The `access_token` expires every hour but the skill auto-refreshes it using your client credentials.

## Step 4: Install the Skill

Copy the `bumblebee` folder into your OpenClaw skills directory:

```bash
cp -r bumblebee ~/.openclaw/workspace/skills/
```

Or if you downloaded the `.skill` zip:

```bash
unzip bumblebee.skill -d ~/.openclaw/workspace/skills/bumblebee
```

## Step 5: Test It

Make sure Spotify is open on at least one device (phone, desktop, speaker), then ask your agent:

- **"Play music"** → R2-DJ auto-detects the vibe and queues tracks
- **"Say it with music"** → Bumblebee mode, communicates through lyrics
- **"Play something to focus"** → Architect frequency
- **"What's playing?"** → Current track info

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No active device" | Open Spotify on your phone/desktop and play any track for 1 second |
| 401 errors | Token expired — the skill auto-refreshes, but if `refresh_token` is invalid, redo Step 3 |
| 403 on playlist creation | Spotify dev mode limits playlist creation. Direct playback works fine. |
| Songs won't play | Make sure you have Spotify Premium, not Free |

## File Structure

```
skills/bumblebee/
├── SKILL.md          # Agent instructions (read by OpenClaw)
├── SETUP.md          # This file
├── scripts/
│   ├── bumblebee.js  # Intent-based playback (moods/intents)
│   ├── r2-dj.js      # Contextual DJ (reads the room)
│   ├── lyric-engine.js   # Lyric search + clip playback
│   ├── lyric-index.json  # Indexed lyrics database
│   └── lyrics-db.json    # Full lyrics store
└── references/
    └── song-library.md   # Curated song catalog with moods
```

## How It Works

**Bumblebee** chains exact lyric lines from songs to form sentences — like Bumblebee from Transformers speaking through radio clips. Your agent searches for lyrics that say what it means, then plays the exact timestamps.

**R2-DJ** reads the time of day, checks your recent Spotify history, and auto-detects which "frequency" (mood profile) fits the moment. Then it searches and queues 10-15 tracks. Five frequencies: Architect (focus), Dreamer (synthwave), Mexican Soul (heritage), Seeker (healing/sleep), Cinephile (film scores).

---

*Built with 🤖 by SWATS.ai — Your AI, Your Rules*
