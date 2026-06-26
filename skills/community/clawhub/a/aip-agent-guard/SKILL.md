# AIP Security Guard

Verify skill authors, enforce capability manifests, and audit tool calls. Adds identity and access control to your OpenClaw setup.

## Setup

```bash
npm install -g aip-openclaw
```

## Commands

- "verify skill [name]" -- check signature and manifest of an installed skill
- "show audit log" -- display recent tool call audit trail
- "security status" -- show which skills are signed, unsigned, or blocked
- "trust author [key]" -- add an author to your local trust list

## How It Works

AIP Security Guard uses the Agent Identity Protocol (AIP) to verify skill authors via Ed25519 signatures and enforce capability manifests that declare what each skill is allowed to do.

Each skill can optionally include:
- `.aip-signature` -- signed envelope proving the skill hasn't been tampered with
- `aip-manifest.toml` -- declaration of allowed MCP tools, network access, file access, shell, budget

The guard runs outside OpenClaw's trust boundary. All decisions are logged to an audit trail.

## Links

- [AIP Protocol](https://sunilprakash.com/aip/)
- [AIP Paper](https://arxiv.org/abs/2603.24775)
- [GitHub](https://github.com/sunilp/aip-openclaw)
