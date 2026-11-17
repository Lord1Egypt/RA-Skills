"""Shared fixtures — parse sdef files once, share across all tests."""

import pytest

from clam.scanner.sdef_parser import parse_sdef

MUSIC_SDEF = "/System/Applications/Music.app/Contents/Resources/com.apple.Music.sdef"
CALENDAR_SDEF = "/System/Applications/Calendar.app/Contents/Resources/iCal.sdef"


@pytest.fixture(scope="session")
def music_sdef_info():
    """Parse Music.sdef once for the entire test session."""
    return parse_sdef(MUSIC_SDEF, "Music")


@pytest.fixture(scope="session")
def calendar_sdef_info():
    """Parse Calendar.sdef once for the entire test session."""
    return parse_sdef(CALENDAR_SDEF, "Calendar")
