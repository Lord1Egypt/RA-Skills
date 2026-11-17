"""pytest bootstrap: make `adversarial_review` and `adversarial_common` importable."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "scripts"))
sys.path.insert(0, os.path.join(_HERE, "..", "adversarial-common"))
