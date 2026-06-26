# ASO Suite CLI

ASO Suite CLI is a small command-line client for [ASO Suite](https://www.asosuite.com/) subscribers.

## Install (npm global)

Install from npm:

```bash
npm install -g asosuite

# Check that it's working
asosuite help
```

## Install (local development)

Clone the repo, then from the root folder:

```bash
# Install dependencies
npm install

# Link the CLI globally
npm link

# Check that it's working
asosuite help
```

## Commands

- `asosuite login`
- `asosuite logout`
- `asosuite subscription [--json]`
- `asosuite search-apps [--json] [--region <REGION>] [--platform <PLATFORM>] <query...>`
- `asosuite list-apps [--json]`
- `asosuite keywords [--json] [--region <REGION>] [--platform <PLATFORM>] [--app <APP_ID_OR_URL>] <keyword...>`
- `asosuite track-app [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`
- `asosuite untrack-app [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`
- `asosuite plan-app [--json] --name <APP_NAME> [--id <PLANNED_APP_ID>] [--region <REGION>] [--platform <PLATFORM>]`
- `asosuite unplan-app [--json] --id <PLANNED_APP_ID> [--region <REGION>] [--platform <PLATFORM>]`
- `asosuite tracked-keywords list [--json] [--region <REGION>] [--platform <PLATFORM>] [--page <NUMBER>] [--sort <FIELD>] [--order <asc|desc>] [--tag <TAG_ID> | --tags <TAG_IDS>] --app <APP_ID_OR_URL_OR_PLANNED_ID>`
- `asosuite tracked-keywords add [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL_OR_PLANNED_ID> <keyword...>`
- `asosuite tracked-keywords remove [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL_OR_PLANNED_ID> <keyword...>`
- `asosuite tracked-keywords note set [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL_OR_PLANNED_ID> --keyword <KEYWORD> --text <TEXT>`
- `asosuite tracked-keywords note clear [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL_OR_PLANNED_ID> --keyword <KEYWORD>`
- `asosuite tracked-keywords tags set [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL_OR_PLANNED_ID> --keyword <KEYWORD> [--tag <TAG_ID> | --tags <TAG_IDS>]`
- `asosuite tags list [--json]`
- `asosuite tags create [--json] --name <NAME> --color <COLOR>`
- `asosuite tags edit [--json] --id <TAG_ID> [--name <NAME>] [--color <COLOR>]`
- `asosuite tags delete [--json] --id <TAG_ID>`
- `asosuite related-apps list [--json] --app <APP_ID_OR_URL> [--platform <PLATFORM>]`
- `asosuite related-apps add [--json] --app <APP_ID_OR_URL> --related <APP_ID_OR_URL> [--platform <PLATFORM>] [--region <REGION>]`
- `asosuite related-apps remove [--json] --app <APP_ID_OR_URL> --related <APP_ID_OR_URL> [--platform <PLATFORM>]`
- `asosuite events list [--json] [--app <APP_ID_OR_URL>]`
- `asosuite events add [--json] --text <TEXT> [--date <YYYY-MM-DD>] [--app <APP_ID_OR_URL>]`
- `asosuite events delete [--json] <EVENT_ID>`
- `asosuite charts [--json] [--period <7|30|90>] [--region <REGION> | --regions <REGION,REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`
- `asosuite features [--json] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`
- `asosuite ratings [--json] [--period <7|30|90>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`

Defaults:

- `region=US`
- `platform=iphone`
- `period=30` (for `charts` and `ratings`)

Supported platforms: `iphone`, `ipad`, `mac`, `appletv`, `watch`, `vision`.

Use `--json` on any data command for single-line JSON output.

`tracked-keywords list` is paginated to 50 keywords per page. Supported sort fields are: `keyword`, `tags`, `notes`, `relevance`, `popularity`, `difficulty`, `position`, `lastUpdate`.

## Examples

### Keyword metrics

```bash
asosuite keywords --region US --platform iphone --app 6448311069 "step counter" "water tracker"
```

### Search apps (marks already tracked apps)

```bash
asosuite search-apps --region US --platform iphone "chat gpt"
```

### List tracked and planned apps

```bash
asosuite list-apps
```

### Track an app

```bash
asosuite track-app --app 6448311069 --platform iphone --region US
```

### Untrack an app

```bash
asosuite untrack-app --app 6448311069 --platform iphone --region US
```

### Plan an app

```bash
asosuite plan-app --name "My Next App" --platform iphone --region US
```

### Unplan an app

```bash
asosuite unplan-app --id my-next-app --platform iphone --region US
```

### Add tracked keywords (tracked app or planned app)

```bash
asosuite tracked-keywords add --app 6448311069 --platform iphone --region US "step counter" "water tracker"
```

```bash
asosuite tracked-keywords add --app my-next-app --platform iphone --region US "step counter" "water tracker"
```

### Remove tracked keywords (tracked app or planned app)

```bash
asosuite tracked-keywords remove --app 6448311069 --platform iphone --region US "step counter" "water tracker"
```

```bash
asosuite tracked-keywords remove --app my-next-app --platform iphone --region US "step counter" "water tracker"
```

### List related apps for a tracked app

```bash
asosuite related-apps list --app 6448311069 --platform iphone
```

### Add a related app

```bash
asosuite related-apps add --app 6448311069 --related 333903271 --platform iphone --region US
```

### Remove a related app

```bash
asosuite related-apps remove --app 6448311069 --related 333903271 --platform iphone
```

### List events (app filter includes global + app events)

```bash
asosuite events list --app 6448311069
```

### Add an event

```bash
asosuite events add --app 6448311069 --text "Started ASO for 'keyword x'" --date 2026-02-25
```

### Delete an event

```bash
asosuite events delete 123
```

### Fetch tracked keywords for a specific app (paginated)

```bash
asosuite tracked-keywords list --app 6448311069 --platform iphone --region US --page 1 --sort keyword --order asc
```

### Fetch tracked keywords for a planned app id (paginated)

```bash
asosuite tracked-keywords list --app my-next-app --platform iphone --region US --page 1 --sort relevance --order desc
```

### Create and list keyword tags

```bash
asosuite tags create --name important --color "#ef4444"
```

```bash
asosuite tags list
```

### Add notes and tags to a keyword

```bash
asosuite tracked-keywords note set --app 6448311069 --platform iphone --region US --keyword "step counter" --text "1: 26.7k,12.9k"
```

```bash
asosuite tracked-keywords tags set --app 6448311069 --platform iphone --region US --keyword "step counter" --tag 1
```

### Filter tracked keywords by tag

```bash
asosuite tracked-keywords list --app 6448311069 --platform iphone --region US --tag 1 --sort tags --order asc
```

### Fetch chart rankings

```bash
asosuite charts --app 6448311069 --platform iphone --period 30
```

### Fetch featured/editorial appearances

```bash
asosuite features --app 6448311069 --platform iphone
```

### Fetch ratings

```bash
asosuite ratings --app 6448311069 --platform iphone --period 30
```

### JSON output

```bash
asosuite charts --json --app 6448311069 --platform iphone
```

## Authentication flow

`asosuite login` starts a device-style sign-in flow:

1. CLI asks the server for a short-lived device code.
2. CLI opens your browser at `https://www.asosuite.com/cli/auth?code=...`.
3. You sign in and approve the CLI request.
4. CLI polls the server and receives a long-lived CLI access token.

The token is stored at `~/.asosuite/config.json`.

## Notes

- Keyword metrics are currently limited to 50 keywords per request on the server.
- `tracked-keywords add` and `tracked-keywords remove` are currently limited to 200 keywords per request.
