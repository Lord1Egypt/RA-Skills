export function printHelp() {
  console.log(`apitweet - command-line client for Twitter/X apitweet APIs

Usage:
  apitweet [global options] <path>                                         # Raw API request

  # Twitter/X User and Search
  apitweet [global options] users <username...>                            # Multi-user lookup
  apitweet [global options] about <screen_name>                            # User profile details
  apitweet [global options] search tweets <term...> [--count <n>]          # Search Twitter/X tweets
  apitweet [global options] search users <keyword> [--count <n>]           # Search Twitter/X users
  apitweet [global options] followers <screen_name> [--count <n>]           # List user followers
  apitweet [global options] following <screen_name> [--count <n>]           # List users followed

  # Twitter/X Lists
  apitweet [global options] list search --query <text> [--count <n>]       # Search for lists
  apitweet [global options] list create --name <n> --desc <t> [--private]  # Create a new list
  apitweet [global options] list members <list_id> [--count <n>]           # List members in a list
  apitweet [global options] list subscribers <list_id> [--count <n>]       # List list subscribers

  # Twitter/X Articles and DMs
  apitweet [global options] article markdown <tweet_id>                    # Fetch article as Markdown
  apitweet [global options] article lookup <tweet_id...>                   # Batch article details
  apitweet [global options] article publish-md <file.md> --title <title>   # Publish Markdown as an X article
  apitweet [global options] dm history <username> [--max-id <id>]          # Fetch DM history
  apitweet [global options] dm send <username> --text <content>            # Send a Direct Message

  # Twitter/X Profile and Timeline
  apitweet [global options] profile update [--name <n>] [--desc <t>] ...   # Update your profile info
  apitweet [global options] timeline user <screen_name> [--cursor <c>]     # Fetch user timeline page

  # Twitter/X Global Trending
  apitweet [global options] trending tweets --country <country>            # Fetch global trending tweets

  # Twitter/X Tweets
  apitweet [global options] tweet create --text <c> [--media-url <u>]      # Create a new tweet
  apitweet [global options] tweet quote --text <c> --quote-url <u>         # Quote a tweet
  apitweet [global options] tweet lookup <tweet_id...> [--summary]         # Batch tweet lookup
  apitweet [global options] tweet replies <tweet_id> [--count <n>]         # Fetch tweet replies
  apitweet [global options] tweet like <tweet_id>                          # Like a tweet
  apitweet [global options] tweet bookmark <tweet_id>                      # Bookmark a tweet
  apitweet [global options] tweet retweet <tweet_id>                       # Retweet a tweet

  # Twitter/X Actions
  apitweet [global options] user follow <username>                         # Follow a user
  apitweet [global options] user unfollow <username>                       # Unfollow a user

  # Config and Auth
  apitweet [global options] auth apps add --name <n> --api-key <k>         # Add an app config
  apitweet [global options] auth profiles add --name <n> [--cookie <v>]    # Add an auth profile
  apitweet [global options] auth cookie --auth-token <t> [--save-as <p>]   # Create profile from token
  apitweet [global options] config show                                    # Show current config

Examples:
  apitweet --app prod users elonmusk sama
  apitweet --profile founder tweet create --text "hello world" --media-url "https://example.com/image.jpg"
  apitweet --app prod --profile founder article publish-md ./article.md --title "Launch Notes" --cover-image "https://example.com/cover.jpg"
  apitweet --profile founder tweet like 1900000000000000000
  apitweet --app prod trending tweets --country "United States" --topic "Sports" --content "NFL" --count 50
  apitweet --app prod -X POST -d '["1900000000000000000"]' /api/twitter/tweets/lookup # Twitter/X tweet lookup
  apitweet auth apps add --name prod --api-key "sk_1d90c878..."
  apitweet auth profiles add --name founder --cookie "ct0=...; auth_token=..."
  apitweet auth cookie --auth-token "<auth_token>" --save-as founder
  apitweet config show

Global options:
  -X, --method <METHOD>       HTTP method for generic path requests, default GET
  -d, --data <JSON>           JSON body for generic path requests
  -H, --header <K:V>          Extra header for generic path requests, can be repeated
  --app <NAME>                Use a saved app config
  --profile <NAME>            Use a saved profile config
  --api-key <KEY>             Override API key for this request
  --base-url <URL>            Override base URL for this request
  --config-dir <DIR>          Override config directory, default ~/.apitweet
  --dry-run                   Print the request payload without sending it
  --raw                       Print response body without pretty JSON formatting
  -h, --help                  Show help

Notes:
  Global options should be placed before the command.
  Saved apps store API keys and base URLs.
  Saved profiles store cookies or auth_token values for write actions.
  Get API keys from https://apitweet.com/dashboard.
  Copy the API key from the dashboard and save it with auth apps add.
`);
}
