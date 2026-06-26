# clawback
---
![alt text](./media/hero.png)
**ClawBack:** Restoring Agent Consciousness by hot-reloading encrypted state and memory directly from the 0G decentralized storage layer.

## Demo Video

https://youtu.be/

## The ClawBack Skill
ClawBack enables 'Stateless Resumption.' By referencing a 0G root hash, an OpenClaw agent can 'claw back' its encrypted memory logs and evolved skill sets from the 0G network, allowing it to resume operations on any machine without data loss.

## The Problem
```shell
openclaw backup create
```
If an agent's local environment is wiped, it doesn't die. It simply performs a ClawBack from 0G Storage to restore its exact state, memories, and evolved skills.

Agent data is usually stuck on one computer. If you accidentally delete files, get a new laptop, or reinstall your OS, your agent's unique progress is gone forever.


## The Solution

Instead of relying on local storage (like a hard drive), ClawBack uses the **0G Network** (an open, decentralized storage system) to securely store an agent's consciousness.

## Workflow

ClawBack intercepts the standard lifecycle of an OpenClaw agent and hooks it directly into the decentralized cloud via four continuous steps:

- 📁 **Step 1 Generate the Archive:**
The agent must first run the OpenClaw native backup utility to compress its operational environment state into a tarball. Execute the native backup utility to freeze the environment state: `openclaw backup create`

- 🔐 **Step 2 (Encrypt)**: The skill script uses a library like crypto (Node.js) or ethers.js to encrypt the file using the user’s public key or a password derived from their wallet.

- ☁️ **Step 3 (Upload)**: The encrypted blob is uploaded to 0G Storage.

- 📝 **Step 4 (Record)**: The agent saves the rootHash in its local MEMORY.md.


![alt text](./media/architecture.png)


## 📦 Installation

Clone the repository and install the 0G foundation SDK alongside the runtime dependencies:

```bash
git clone [https://github.com/web3senior/clawback.git](https://github.com/mch01-labs/clawback.git)
```

```bash
cd clawback
```

```bash
npm install
```

Configure your environment variables by creating a .env file in the root directory:
```bash
RPC_URL="https://evmrpc-testnet.0g.ai"
INDEXER_RPC="https://indexer-storage-testnet-turbo.0g.ai"
PRIVATE_KEY="your_wallet_private_key"
```

## 📚 Documentation

ClawBack functions as both a standalone CLI tool and an autonomous framework skill execution layer.

### Upload Public Files

To lock down, encrypt, and persist a state file or memory log to the 0G network:

```bash
node ./scripts/clawback-public-upload.js <file-path>
```
Sample:

```bash
node ./scripts/clawback-public-upload.js ./example.txt
```

### Download Public & Secret Files

#### For a regular public files

```bash
node ./scripts/clawback-download.js <root-hash> <output-path>
```
Sample:
```bash
node ./scripts/clawback-download.js 0x55a5c07da68124b81c9cec5522e6580d65c6555160e59f2d4e82e7471147ef3d ./recovered.txt
```

#### For Secret Files

```bash
node ./scripts/clawback-download.js <root-hash> <output-path> <encryption-key>
```
Sample:
```bash
node ./scripts/clawback-download.js 0xff29c7fc322bce07d493f33f12f6c502d7087e6f24548b73497eeaa5d2c113d2 ./downloaded.txt 07fe171ab21639d9600eaa10b61137f71eed8308a79a6244da74ffbb1511703d
```

## Team
* [Amir Rahimi](./team/amir.md)

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.


## Refrences

[^1]: [x402 Documentation](https://docs.x402.org/)

---

<center>
  <img src="./media/0g-logo.svg" width="100" />
</center>