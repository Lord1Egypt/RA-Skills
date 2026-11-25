# Network-specific commands

All of these sit under `fopost accounts <network>` and take the FoPost account id from
`fopost accounts list`. Add `--json` to parse the result. Set a default once, and every post to
that account uses it, so the post itself needs no extra settings.

## Reddit

```bash
fopost accounts reddit subreddits <account-id>              # where it can post
fopost accounts reddit rules <account-id> <subreddit>       # read before posting
fopost accounts reddit flairs <account-id> <subreddit>
fopost accounts reddit set-default <account-id> <subreddit> # where posts go
fopost accounts reddit set-default <account-id> --clear     # back to the profile page
```

Read the subreddit's rules first. Many ban self-promotion or require a flair.

## YouTube

```bash
fopost accounts youtube playlists <account-id>
fopost accounts youtube create-playlist <account-id> "Tutorials" --privacy public
fopost accounts youtube set-default-playlist <account-id> <playlist-id>
fopost accounts youtube captions <account-id> <video-id>
fopost accounts youtube transcript <account-id> <caption-id>
```

A YouTube post needs a video. Use `posts create --title` for the video title.

## TikTok

```bash
fopost accounts tiktok creator-info <account-id>      # limits TikTok enforces at publish time
fopost accounts tiktok music <account-id> "lofi" --limit 10
fopost accounts tiktok locations <account-id> "Berlin"
fopost accounts tiktok video <account-id> <share-url>
```

Check `creator-info` before scheduling: it reports the longest video allowed and which privacy
options the account may use.

## Instagram

```bash
fopost accounts instagram publishing-limit <account-id>  # posts left in the 24-hour window
fopost accounts instagram audio <account-id> "summer"
fopost accounts instagram stories <account-id>
```

Instagram needs at least one image or video on every post.

## Pinterest

```bash
fopost accounts pinterest boards <account-id>
fopost accounts pinterest create-board <account-id> "Recipes" --privacy PUBLIC
```

## LinkedIn

```bash
fopost accounts linkedin mentions <account-id> "Acme"   # prints the annotation to paste into the text
```

## Bluesky

```bash
fopost accounts bluesky languages <account-id>
fopost accounts bluesky set-languages <account-id> en de
```

## X

```bash
fopost x post <post-id> --account <account-id>
fopost x search --account <account-id> --q "fopost" --max-results 10
fopost accounts x follow <account-id> --user-id <numeric-user-id>
```

Every X read is charged per request. Search only when asked.

## Discord, Telegram, Slack

```bash
fopost accounts discord channels <account-id>
fopost accounts discord switch-channel <account-id> <channel-id>
fopost accounts telegram connect-code          # one-time code that connects a chat
fopost accounts telegram connect-status <code>
fopost accounts slack channels <account-id>
```

## Google Business Profile

```bash
fopost accounts gbp location <account-id>
fopost accounts gbp performance <account-id>    # impressions, calls, directions, clicks
fopost accounts gbp keywords <account-id>       # search terms that found the listing
fopost accounts gbp place-actions <account-id>  # Book, Order and Reserve links
```

Changing the listing (`update-location`, `replace-menus`, `replace-services`, `add-media`) edits
what customers see on Google. Treat it like publishing: show the change and ask first.

## Anything else

`fopost <command> --help` lists every flag. The full reference is at https://fopost.com/docs/cli.
