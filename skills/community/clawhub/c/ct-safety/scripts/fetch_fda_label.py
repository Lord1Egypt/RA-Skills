# §16.9 bridge: the outbound (openFDA) code now lives in
# adapters/fetch_fda_label.py per §16.9 (retrieval/website calls must sit in the
# dedicated adapters/ dir). This stub re-publishes the real module under the
# legacy bare name so every existing `import fetch_fda_label` / `from
# fetch_fda_label import ...` call site keeps working unchanged. There is no
# outbound call here, so scripts/ stays F17-clean.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import adapters.fetch_fda_label as _real_fetch_fda_label
sys.modules[__name__] = _real_fetch_fda_label
