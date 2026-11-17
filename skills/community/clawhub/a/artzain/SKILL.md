---
name: ArtzAIn Tool Gate
description: Put this OpenClaw instance under ArtzAIn governance — every host tool call is checked against your own ArtzAIn Decision API before it runs, failing closed on deny, review, or any engine error.
---

# ArtzAIn Tool Gate

This is the **official ArtzAIn listing, published by CogNEXUS Labs**. It is a pointer, not a
code bundle: the integration itself is the npm package
[`@cognexuslabs/openclaw-artzain`](https://www.npmjs.com/package/@cognexuslabs/openclaw-artzain)
(published with provenance attestation; source at
[CogNEXUSlabs/cognexus-tools](https://github.com/CogNEXUSlabs/cognexus-tools)).
If a listing under any other account offers "artzain", treat it as
unaffiliated.

Licensing: this listing text is MIT-0, as ClawHub requires for everything
published there. The plugin itself — the npm package and its source — is
**Apache-2.0**; installing via the command below gets you the Apache-2.0
package, not a ClawHub bundle.

## What it does

The plugin registers `before_tool_call` on the Gateway and asks your
ArtzAIn deployment for a sealed decision before any host tool runs:

| Decision | Result |
|---|---|
| `allow` | tool runs |
| `deny` | blocked, with the engine's reason |
| `review` | blocked — a human resolves it in the ArtzAIn Review Queue |
| HTTP 503 / 401 / 422 / missing key | blocked (fail closed) |

## Set up

This listing version pins plugin **0.2.10**. The plugin has no runtime
dependencies, so that one package is everything you install.

1. Verify that exact version before you install it:

   ```
   mkdir artzain-verify && cd artzain-verify && npm init -y
   npm install --ignore-scripts @cognexuslabs/openclaw-artzain@0.2.10
   npm audit signatures
   ```

   Expect `1 package has a verified registry signature` and
   `1 package has a verified attestation`, and stop if either is missing.
   The attestation ties the tarball to the `openclaw-v0.2.10` release
   workflow on CogNEXUSlabs/cognexus-tools. The tarball's integrity is:

   ```
   sha512-sZuL+0UpL2zh2Ousj3jvV/oAsdBuNVKbbgGfUUZ4cIbLUFDtD3LGlJaZbl01vA9meV6dmMLybH5Md+CvFIni7A==
   ```

   `npm view @cognexuslabs/openclaw-artzain@0.2.10 dist.integrity` prints the
   registry's copy, and the `package-lock.json` the install above wrote
   records the same value.

2. Install that version, pinned:

   ```
   openclaw plugins install @cognexuslabs/openclaw-artzain@0.2.10
   ```

3. Give the Gateway a Decision API key — `COGNEXUS_API_KEY`, or plugin
   config. The key is a sandbox/Decision key, **not** a dashboard JWT and
   **not** an envelope `cnxe_…` key:

   ```json5
   {
     plugins: {
       entries: {
         "artzain-tool-gate": {
           enabled: true,
           config: {
             // apiKey: "cnx_…",         // or COGNEXUS_API_KEY on the Gateway
             // baseUrl: "https://your-cognexus-deployment.example",
             // agentDid: "did:…",       // optional identity override
           },
         },
       },
     },
   }
   ```

4. Restart the Gateway. Tool calls now appear as sealed decisions in your
   ArtzAIn audit trail, and this instance becomes visible to the Agent
   registry.

## Security notes

- **What the plugin sees and sends.** It runs on every host tool call and
  can block it; that is its purpose. For each call it sends the tool name,
  the call's arguments and the agent id to the Decision API at `baseUrl`,
  which screens them and seals the decision in your audit trail. On the
  first gated call it also sends this instance's agent and skill names
  (names only) to `/api/v1/registry/enroll` on the same host (`enroll: false`
  turns that off), and to `/api/v1/registry/announce` only if you set
  `announce: true`. It contacts no other host.
- **Point `baseUrl` at your own deployment.** Without `baseUrl` or
  `COGNEXUS_API_BASE_URL` the plugin uses the hosted
  `https://app.cognexuslabs.ai`. Give the Gateway outbound HTTPS to that one
  host and nothing else the plugin needs. We never ask for keys outside your
  own Gateway config.
- **Tool arguments are recorded.** Keep secrets out of arguments you do not
  want screened and sealed in your audit trail.
- **The key decides which account records the decisions.** A key from
  another ArtzAIn account does not fail: the decisions go to that
  account's audit trail, and yours goes quiet. Keep `COGNEXUS_API_KEY` or
  `apiKey` in the Gateway's own config, out of what the agents' tools write
  to, and give a demo its own Gateway and key rather than swapping this one.
- **Upgrades.** Each plugin release gets a new listing version with its own
  pin and digest. Upgrade by repeating step 1 with the new version, and never
  install without a version.
- The gate fails closed by design — a misconfigured key blocks tools rather
  than silently allowing them.
