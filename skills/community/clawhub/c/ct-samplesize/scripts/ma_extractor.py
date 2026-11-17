# §16.9 bridge: the outbound (NCBI E-utilities / PubMed) code now lives in
# adapters/ma_extractor.py per §16.9 (retrieval calls must sit in the dedicated
# adapters/ dir). This stub re-publishes the real module under the legacy bare
# name so every existing `import ma_extractor` / `from ma_extractor import ...`
# call site keeps working unchanged, and the CLI entry point
# (`python scripts/ma_extractor.py --query ...`) is preserved. There is no
# outbound call here, so scripts/ stays F17-clean.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import adapters.ma_extractor as _real_ma_extractor
sys.modules[__name__] = _real_ma_extractor

if __name__ == "__main__":
    _real_ma_extractor.main()
