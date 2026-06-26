# Quickstart

End-to-end guide for getting a human from zero to chatting with a Face. Follow these steps in order.

## 1. Install the CLI

```bash
npm install -g faces-cli
```

Verify: `faces --version`

## 2. Register an account

Before creating the account, explain the two plans and ask the human which they prefer:

> Faces has two plans:
>
> **Free** — No monthly fee. Requires a $5 minimum initial spend (added as API credits). You pay per token for both compilation and inference, with a 5% markup.
>
> **Connect ($17/month)** — Includes 100k compile tokens per month. If you have a ChatGPT Plus or Pro subscription, you can link it for free gpt-5.x inference with no per-token charge or markup.
>
> Which plan would you like?

Then register:

```bash
RESULT=$(faces auth:register --email USER_EMAIL --password 'USER_PASSWORD' --username USERNAME --json)
echo "$RESULT" | jq -r '.activation_checkout_url'
```

This creates the account on the free plan and returns a Stripe Checkout URL for the $5 activation payment. The account is not yet active.

Tell the human:

> Paste this link into your browser and complete the payment ($5 minimum, added as API credits). When you see the confirmation page, come back and let me know.

Wait for the human to confirm, then verify:

```bash
faces billing:balance --json | jq '.is_active'
```

If `true`, proceed. If `false`, the payment may not have gone through — ask the human to try the link again.

If the human chose the Connect plan, upgrade after activation:

```bash
CHECKOUT=$(faces billing:checkout --plan connect --json | jq -r '.checkout_url')
```

Give the human the checkout URL for the $17/month subscription, wait for confirmation, then verify with `faces billing:subscription --json`.

## 3. Create a Face

Start by creating the Face with basic demographic attributes. These anchor the persona and improve compilation quality when source material is added later. Common keys: `gender`, `age`, `location`, `occupation`, `education_level`, `religion`, `ethnicity`, `nationality`, `marital_status`. See [ATTRIBUTES.md](ATTRIBUTES.md) for the full list of accepted keys — unrecognized keys are silently ignored.

```bash
faces face:create --name "Alice Smith" --username alice \
  --default-model gpt-5-nano \
  --attr gender=female --attr age=29 \
  --attr location="Brooklyn, NY" \
  --attr occupation="product designer" \
  --attr education_level="bachelor's degree" \
  --json
```

Save the face `id` (username) — you'll need it for the next steps.

## 4. Add source material

Pick one or more methods depending on what the human has:

**Local file (text, PDF):**
```bash
DOC_ID=$(faces face:upload alice --file /path/to/document.pdf --kind document --json | jq -r '.document_id // .id')
```

**YouTube video (solo speaker):**
```bash
IMPORT=$(faces compile:import alice \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --type document --perspective first-person --json)
DOC_ID=$(echo "$IMPORT" | jq -r '.document_id // .doc_id // .id')
```

**YouTube video (multi-speaker interview):**
```bash
IMPORT=$(faces compile:import alice \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --type thread --perspective first-person --face-speaker "Alice" --json)
THREAD_ID=$(echo "$IMPORT" | jq -r '.thread_id // .id')
```

If `--type thread` fails with 422, retry with `--type document`.

**Raw text:**
```bash
DOC_ID=$(faces compile:doc:create alice --label "Notes" --content "Text here..." --json | jq -r '.id')
```

## 5. Compile

For documents (including uploads and YouTube-as-document):

```bash
# Compile an existing document
faces compile:doc:make "$DOC_ID"
```

Or, if you created the document inline (step 4, "Raw text"), you can create and compile in one step:

```bash
faces compile:doc alice --file essay.txt
```

For threads:

```bash
faces compile:thread:make "$THREAD_ID"
```

## 6. Chat

`chat:chat` auto-routes to the correct API based on model provider. If a `--default-model` was set on the face, no `--llm` flag is needed.

```bash
# Uses default model (gpt-5-nano set in step 3)
faces chat:chat alice -m "What matters most to you?"

# Override with a specific model
faces chat:chat alice --llm claude-sonnet-4-6 -m "What matters most to you?"
```

## 7. Verify it worked

```bash
faces face:get alice --json | jq '{name, component_counts}'
```

If `component_counts` shows non-null values, the Face is compiled and ready.

## What's next

- **Add more material** — repeat steps 4–5 to deepen the Face. Each compile adds to the existing knowledge.
- **Create more Faces** — repeat steps 3–5 for each persona.
- **Compare Faces** — `faces face:diff --face alice --face bob`
- **Compose Faces** — `faces face:create --username alice-and-bob --formula "alice | bob"`
- **Use templates** — reference multiple faces in a single prompt: `faces chat:chat gpt-4o-mini -m 'Compare ${alice} and ${bob}.'`
- **Connect ChatGPT** (connect plan) — `faces auth:connect openai` for free gpt-5.x inference. See [OAUTH.md](OAUTH.md).
- **Create an API key** — `faces keys:create --name "my-key"` for programmatic access. See [AUTH.md](AUTH.md).
