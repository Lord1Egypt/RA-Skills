# Onboarding Flow

When a user first triggers this skill and doesn't have `FRAMER_PROJECT_URL` or `FRAMER_API_KEY` set up, walk them through this onboarding.

---

## Step 1: Get project URL

Ask the user:

> What's your Framer project URL?
> You can find it in the browser address bar when editing your project in Framer, e.g.:
> `https://framer.com/projects/MyProject--KCwUA0XT66ZkfkIGMSsP-0e6rK`

The URL format is: `https://framer.com/projects/{ProjectName}--{ProjectId}`

---

## Step 2: Get API key

Ask the user:

> What's your Framer Server API key?
> To create one: open your project in Framer → Site Settings → General → scroll to "Server API" → generate a key.
> Save it somewhere safe — you won't be able to see it again.

The key format is: `fr_` followed by alphanumeric characters (e.g., `fr_20xy69s6wb83bvh2mr1effssaa`).

---

## Step 3: Install framer-api

Check if `framer-api` is in the project's `node_modules`. If not:

```bash
npm i framer-api
```

If no `package.json` exists, initialize first:

```bash
npm init -y && npm i framer-api
```

---

## Step 4: Store credentials

Save the credentials to the project's `.env` file:

```bash
FRAMER_PROJECT_URL=https://framer.com/projects/MyProject--xxxxx
FRAMER_API_KEY=fr_xxxxx
```

If a `.env` file already exists, append these variables. Don't overwrite existing content.

**Important:** Check that `.env` is in `.gitignore`. If not, add it.

---

## Step 5: Test connection

Run a quick test to verify the connection works:

```javascript
import { connect } from "framer-api"

const framer = await connect(process.env.FRAMER_PROJECT_URL, process.env.FRAMER_API_KEY)
const info = await framer.getProjectInfo()
console.log("Connected to:", info.name)

const collections = await framer.getCollections()
console.log("Collections:", collections.map(c => `${c.name} (${c.id})`))

framer.disconnect()
```

If this succeeds, onboarding is complete. Show the user:
- Project name
- Number of collections found
- Collection names and IDs

---

## Step 6: Summarize

Tell the user what's available and how to use it:

> Your Framer project "{name}" is connected with {N} CMS collections:
> - {collection names}
>
> You can now:
> - List/read CMS items
> - Create/update/delete articles
> - Upload images
> - Publish previews and deploy to production
>
> Just ask me to "push an article to Framer", "list my Framer collections", or "publish my Framer site".
