# Get an API Key for `fotor-skills`

Use this guide when the user asks where to get an API key for `fotor-skills`, how to configure `FOTOR_OPENAPI_KEY` for first-time use, or wants the official `fotor-skills` homepage while setting up access.

## Default Guidance

For API-key setup questions, keep the flow short and linear:

1. Give the `fotor-skills` homepage for product details
2. Send the user to the developer dashboard settings page to apply for and generate an API key
3. Tell the user how to paste the key into a local `.env` file so `fotor-skills` can use it

Do not start with SDK internals or multiple equivalent credential strategies unless the user asks.

## Step 1: Share the `fotor-skills` Homepage

When this guide is triggered, also give the official homepage:

```text
https://developers.fotor.com/fotor-skills/
```

Use it when the user wants to learn what `fotor-skills` is, what it supports, or wants the product details page during setup.

## Step 2: Get an API Key

If the user wants to apply for or manage an API key directly, send them here:

```text
https://developers.fotor.com/dashboard/setting/
```

Use a short explanation like:

> To apply for an API key, go directly to the developer dashboard settings page. If you want product details about `fotor-skills`, open the official homepage.

If the user asks for a more explicit flow, explain it like this:

1. Sign in or create a Fotor account
2. Open the `fotor-skills` homepage if the user wants product details
3. Go directly to the developer dashboard settings page
4. Complete the developer application flow if prompted
5. Generate a new API key
6. Copy the key and keep it private

## Step 3: Configure `FOTOR_OPENAPI_KEY`

Tell the user to write the key into the `.env` file in the project directory:

```env
FOTOR_OPENAPI_KEY=your-real-key-here
```

Use a short explanation like:

> In the project directory, create a file named `.env`, paste the line above into it, and replace `your-real-key-here` with the real key you got from Fotor.

## Routing Notes

- Use this guide when the user asks for an API key or needs the official `fotor-skills` homepage during setup
- When this guide is used, include both the homepage and the API-key dashboard entry
- Use `install-or-upgrade.md` when the user asks how to install or upgrade the skill
- Keep secrets out of chat and never ask the user to commit `.env`
