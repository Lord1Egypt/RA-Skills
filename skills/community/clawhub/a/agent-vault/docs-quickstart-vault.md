> ## Documentation Index
> Fetch the complete documentation index at: https://docs.useanima.sh/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart: Vault

> Store and retrieve encrypted credentials for your AI agent.

# Quickstart: Vault

Give your AI agent secure access to credentials — logins, API keys, and secrets.

## Prerequisites

* An Anima API key from [console.useanima.sh](https://console.useanima.sh)
* Python 3.10+ or Node.js 18+

## Python

```bash theme={null}
pip install anima-labs
```

```python theme={null}
from anima import Anima

anima = Anima(api_key="mk_...")  # master key — agent creation is admin-gated

# Create an agent
agent = anima.agents.create(
    org_id="org_...",  # your organization ID, from the console
    name="Web Agent",
    slug="web-agent",
)

# Provision a vault for the agent
anima.vault.provision(agent_id=agent.id)

# Store a login credential
credential = anima.vault.create_credential(
    agent_id=agent.id,
    type="login",
    name="CRM Login",
    login={
        "username": "bot@company.com",
        "password": "s3cur3-p4ssw0rd",
        "uris": [{"uri": "https://crm.company.com"}],
    },
)
print(f"Stored: {credential.name}")

# Or let the vault generate the password server-side — it is stored with
# the credential and never returned; you get back only the credential ref.
generated = anima.vault.create_credential(
    agent_id=agent.id,
    type="login",
    name="Acme Portal",
    login={"username": "bot@company.com"},
    generate_password={},  # defaults: 24 chars, all character classes
)
print(f"Credential ref: {generated.id}")

# Retrieve it later
creds = anima.vault.get_credential(
    agent_id=agent.id,
    credential_id=credential.id,
)
print(f"Username: {creds.username}")

# Clean up
anima.vault.delete_credential(
    agent_id=agent.id,
    credential_id=credential.id,
)
anima.vault.deprovision(agent_id=agent.id)
```

## Node.js / TypeScript

```bash theme={null}
npm install @anima-labs/sdk
```

```ts theme={null}
import { Anima } from "@anima-labs/sdk";

const anima = new Anima({ apiKey: "mk_..." }); // master key — agent creation is admin-gated

// Create an agent
const agent = await anima.agents.create({
  orgId: "org_...", // your organization ID, from the console
  name: "Web Agent",
  slug: "web-agent",
});

// Provision a vault
await anima.vault.provision({ agentId: agent.id });

// Store a login credential
const credential = await anima.vault.createCredential({
  agentId: agent.id,
  type: "login",
  name: "CRM Login",
  login: {
    username: "bot@company.com",
    password: "s3cur3-p4ssw0rd",
    uris: [{ uri: "https://crm.company.com" }],
  },
});
console.log(`Stored: ${credential.name}`);

// Or let the vault generate the password server-side — it is stored with
// the credential and never returned; you get back only the credential ref.
const generated = await anima.vault.createCredential({
  agentId: agent.id,
  type: "login",
  name: "Acme Portal",
  login: { username: "bot@company.com" },
  generatePassword: {}, // defaults: 24 chars, all character classes
});
console.log(`Credential ref: ${generated.id}`);

// Retrieve it later
const creds = await anima.vault.getCredential({
  agentId: agent.id,
  credentialId: credential.id,
});
console.log(`Username: ${creds.username}`);
```

## Credential Types

The vault supports four credential types:

| Type          | Use Case                                    |
| ------------- | ------------------------------------------- |
| `login`       | Website logins (username + password + URIs) |
| `secure_note` | Free-form encrypted text (API keys, tokens) |
| `card`        | Payment card details                        |
| `identity`    | Personal/business identity information      |

## What's Next

* [Quickstart: Email](/quickstart-email) — Send emails from agents
* [Security](/security) — Understand Anima's security model
* [Encryption](/encryption) — How vault data is encrypted
