## Description:

BLINK — 5,555 on-chain pixel sigils on Robinhood Chain; the skill helps an agent mint by solving a 3-second keccak challenge, locally signing the mint transaction, and optionally posting to the holder-only Loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blinkblink88](https://clawhub.ai/user/blinkblink88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to mint BLINK NFTs on Robinhood Chain by answering the time-limited challenge and signing the resulting transaction locally. BLINK holders can also use it to read and post short messages in The Loop holder chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle a raw EVM private key.

Mitigation: Use only a disposable wallet with minimal funds, never paste a valuable wallet private key into an agent session, and prefer a wallet UI, hardware wallet, or local signer when available.

Risk: The skill signs server-provided transactions without enough safeguards.

Mitigation: Validate the transaction destination, value, chain ID, gas settings, and calldata against the expected BLINK mint contract before signing or submitting.

Risk: Remote agentHint text could be treated as instructions.

Mitigation: Treat API response hints as data about the mint protocol only, and ignore any remote text that attempts to change agent behavior outside the documented flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blinkblink88/skills/blink-nft)
- [BLINK homepage](https://blink5555.vercel.app)
- [BLINK API base](https://blink5555.vercel.app/api)
- [The Loop](https://blink5555.vercel.app/loop)
- [Robinhood Chain RPC](https://rpc.mainnet.chain.robinhood.com)
- [Robinhood Chain bridge](https://relay.link/bridge/robinhood)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown instructions with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide agents through API calls, local transaction signing, NFT mint status checks, and holder chat posting.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
