# AI & Extensions Reference

## Table of Contents

- [Chromia Extensions Overview](#chromia-extensions-overview)
- [Vector Database Extension](#vector-database-extension)
- [AI Inference Extension](#ai-inference-extension)
- [Stork Oracle Extension](#stork-oracle-extension)
- [Zero-Knowledge Proofs](#zero-knowledge-proofs)
- [Common Mistakes](#common-mistakes)

---

## Chromia Extensions Overview

Extensions are modular add-ons that expand Chromia's core capabilities. Introduced with the Asgard Mainnet Upgrade (Dec 2024), they run as customized Docker containers alongside Chromia nodes.

**Available extensions:**
- Stork Oracle (price feeds)
- Vector Database (similarity search)
- AI Inference (on-chain LLM execution)
- Zero-Knowledge Proofs (proof generation/validation)

When leasing a container for deployment, select the required extensions.

---

## Vector Database Extension

Enables storage and querying of multi-dimensional vector data on-chain. Built for AI-driven applications.

### Use Cases

- Recommendation systems
- Natural language processing / semantic search
- Image recognition / similarity matching
- AI agent memory and retrieval

### How It Works

- Define vector-based schemas in Rell
- Store embeddings as vector data
- Execute similarity searches using built-in operations
- Results are returned ranked by similarity score

### Configuration

```yaml
blockchains:
  my_ai_dapp:
    module: main
    config:
      gtx:
        modules:
          - "net.postchain.vectordb.VectorDbGTXModule"
```

Add the Vector DB library:

```yaml
libs:
  vectordb:
    registry: https://gitlab.com/chromaway/core/vectordb-extension
    path: rell/src/vectordb
    tagOrBranch: <version>
```

### Key Advantage

Unlike centralized vector databases (Pinecone, Weaviate), Chromia's Vector DB provides verifiable, tamper-proof storage with on-chain transparency.

---

## AI Inference Extension

Enables deploying and running LLMs (GPT, DeepSeek, Llama) directly on Chromia provider nodes instead of cloud servers.

### Architecture

- Models are hosted on Chromia nodes (not external servers)
- Inference runs on provider node compute resources
- Inputs and outputs can be recorded on-chain via Neural Interface
- GPU cluster support planned for production workloads

### Key Concepts

- **Neural Interface**: Records AI agent inputs/outputs on-chain for transparency
- **On-chain inference**: The model processes input and generates output on a Chromia node
- **Transparency**: Model parameters, version history, and computations are traceable

### Current Status

- Testnet demos available
- Production deployment requires GPU-capable nodes (AI Cluster)
- Python framework integration for broader model support

### Configuration

```yaml
blockchains:
  my_ai_dapp:
    module: main
    config:
      gtx:
        modules:
          - "net.postchain.ai.AiInferenceGTXModule"
```

---

## Stork Oracle Extension

Provides real-time asset price feeds with sub-millisecond latency. Prices are injected at the beginning of each block.

### Configuration

```yaml
blockchains:
  my_defi_dapp:
    module: main
    config:
      gtx:
        modules:
          - "net.postchain.stork.StorkOracleGTXModule"
      sync_ext:
        - "net.postchain.stork.StorkOracleSynchronizationInfrastructureExtension"
      stork:
        assets:
          - "BTCUSD"
          - "ETHUSD"
          - "CHRUSD"
```

### Rell Library Setup

```yaml
libs:
  stork:
    registry: https://gitlab.com/chromaway/core/stork-oracle-chromia-extension
    path: rell/src/stork
    tagOrBranch: 1.0.1
    rid: x"EBB409F91EBC5EB3816570C9FDB5A170180249CF7F74EEDFC09C428E288F4114"
    insecure: false
```

### Rell Data Structures

```rell
// Returned by the oracle
struct stork_oracle_prices {
  asset: text;
  stork_price;
  publisher_prices: list<publisher_price>;
}

struct stork_price {
  price: big_integer;      // 18 decimal places
  signature;
  timestamp_nanos: integer;
  merkle_root: byte_array;
  type: text;
  version: text;
  checksum: byte_array;
}
```

### Price Conversion

Prices are `big_integer` with 18 decimal places. Use the utility function:

```rell
function convert_price_to_decimal(price: big_integer): decimal
```

### Key Details

- Signatures are auto-verified by the extension — no verification logic needed in Rell
- Complete asset list available at Stork documentation
- Override Stork and publisher public keys in config if needed

---

## Zero-Knowledge Proofs

ZK proof functionality enables proof generation and validation within Chromia dApps.

- Developers implement proof generation and validation as needed
- Supports privacy-preserving computations
- Detailed documentation available in the extensions section of Chromia docs

---

## Common Mistakes

1. **Missing GTX module registration**: Every extension requires its GTX module in `chromia.yml` `config.gtx.modules`.
2. **Missing sync extension for Stork**: The `StorkOracleSynchronizationInfrastructureExtension` is required alongside the GTX module.
3. **Not selecting extension when leasing container**: Extensions must be enabled at the container/deployment level, not just in config.
4. **Using raw `big_integer` prices**: Stork prices have 18 decimal places. Always use `convert_price_to_decimal()` for display.
5. **Expecting real-time inference in production**: AI Inference is evolving. GPU cluster is needed for production-grade LLM workloads. Test on testnet first.
