#!/usr/bin/env python3
"""Release-level human presentation-quality acceptance contract.

Automated QA and Jev may recommend review or blocking, but only an explicit
human review of the exact artifact may produce PASS.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


ERROR_HUMAN_PRESENTATION_QUALITY_INVALID = "HUMAN_PRESENTATION_QUALITY_INVALID"


class HumanPresentationQualityState(str, Enum):
    PASS = "PASS"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCK = "BLOCK"


class ReviewAuthority(str, Enum):
    HUMAN = "HUMAN"
    AUTOMATED_ASSISTANCE = "AUTOMATED_ASSISTANCE"


@dataclass(frozen=True)
class HumanPresentationQualityRecord:
    artifact_sha256: str
    state: HumanPresentationQualityState
    authority: ReviewAuthority
    detail: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[0-9a-f]{64}", self.artifact_sha256):
            raise ValueError(ERROR_HUMAN_PRESENTATION_QUALITY_INVALID)
        if not isinstance(self.state, HumanPresentationQualityState):
            raise ValueError(ERROR_HUMAN_PRESENTATION_QUALITY_INVALID)
        if not isinstance(self.authority, ReviewAuthority) or not self.detail.strip():
            raise ValueError(ERROR_HUMAN_PRESENTATION_QUALITY_INVALID)
        if self.authority is not ReviewAuthority.HUMAN and self.state is HumanPresentationQualityState.PASS:
            raise ValueError("automated assistance cannot pass HUMAN_PRESENTATION_QUALITY")


def human_quality_review(
    artifact_sha256: str,
    *,
    accepted: bool,
    detail: str,
) -> HumanPresentationQualityRecord:
    """Record the human decision for one exact artifact; rejection is blocking."""
    return HumanPresentationQualityRecord(
        artifact_sha256,
        HumanPresentationQualityState.PASS if accepted else HumanPresentationQualityState.BLOCK,
        ReviewAuthority.HUMAN,
        detail,
    )


def automated_quality_assistance(
    artifact_sha256: str,
    *,
    blocking: bool,
    detail: str,
) -> HumanPresentationQualityRecord:
    """Record assistance without granting release acceptance."""
    return HumanPresentationQualityRecord(
        artifact_sha256,
        HumanPresentationQualityState.BLOCK if blocking else HumanPresentationQualityState.REVIEW_REQUIRED,
        ReviewAuthority.AUTOMATED_ASSISTANCE,
        detail,
    )


__all__ = [
    "ERROR_HUMAN_PRESENTATION_QUALITY_INVALID",
    "HumanPresentationQualityRecord",
    "HumanPresentationQualityState",
    "ReviewAuthority",
    "automated_quality_assistance",
    "human_quality_review",
]
