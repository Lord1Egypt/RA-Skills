# Quick Start Guide
## System Requirements
- Windows 10+ / Linux / macOS
- Python 3.10+
- OpenClaw >= 2026.3.22
- BGE-M3 vector model (pre-installed in OpenClaw memory system)

## Installation
### One-click install (recommended)
```bash
# Windows
install.bat

# Linux/macOS
chmod +x install.sh && ./install.sh
```

### Manual install
```bash
pip install chromadb sentence-transformers openclaw-extension-chromadb
```

## Configuration
Update your `config.yaml` file:
```yaml
vector_store:
  type: chromadb
  path: "./chromadb"
  model: "BAAI/bge-m3"
  gpu_accelerate: true
```

## Verify Installation
Run the test script:
```bash
python test_chromadb.py
```
Expected output:
```
[+] ChromaDB connection successful
[+] Vector model loaded successfully
[+] All tests passed!
```

## Next Steps
- See [LanceDB Migration Guide](migration_en.md) to import existing data
- See [Configuration Guide](configuration_en.md) for advanced settings
- See [API Reference](api_reference_en.md) for usage examples
