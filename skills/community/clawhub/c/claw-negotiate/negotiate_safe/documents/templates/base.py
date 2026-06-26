"""Base document template class."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod


class DocumentTemplate(ABC):
    """Base class for all document templates. Extend for new document types."""

    def __init__(self, terms: dict, parties: dict):
        self.terms = terms
        self.parties = parties

    @abstractmethod
    def validate_terms(self) -> tuple[bool, str]:
        """Check all required fields are present and valid."""

    @abstractmethod
    def generate_pdf(self, output_path: str) -> str:
        """Generate PDF and return SHA-256 hash of the file."""

    def _hash_file(self, path: str) -> str:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
