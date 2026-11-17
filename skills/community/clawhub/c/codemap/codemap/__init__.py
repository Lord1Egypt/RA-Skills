"""codemap - a local code-symbol index.

Ask "where is X defined / what's its signature" and get back one compact record
(file:line + signature) instead of grepping then reading the whole file.
"""
from .index import build, find, outline, stats, Hit
from .extractors import Symbol, extract

__all__ = ["build", "find", "outline", "stats", "Hit", "Symbol", "extract"]
