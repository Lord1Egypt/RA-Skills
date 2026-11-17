# §16.9 bridge: the outbound (openFDA / FAERS) code now lives in
# adapters/fetch_faers.py per §16.9 (retrieval/website calls must sit in the
# dedicated adapters/ dir). This stub re-publishes the real module under the
# legacy bare name so every existing `import fetch_faers` / `from fetch_faers
# import ...` call site keeps working unchanged. There is no outbound call here,
# so scripts/ stays F17-clean.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import adapters.fetch_faers as _real_fetch_faers
sys.modules[__name__] = _real_fetch_faers
