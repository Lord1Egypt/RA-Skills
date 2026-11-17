"""Shared User-Agent for every outbound call this skill makes.

CCP asks third parties to identify themselves on ESI requests and treats
anonymous traffic as grounds for throttling or a ban. Python's urllib would
otherwise announce itself as `Python-urllib/3.x`, which says nothing about who
is calling, so both the ESI client and the SSO scripts send this instead.

The format follows the guidance in
https://developers.eveonline.com/docs/services/esi/best-practices/ :
an app name with version, an optional contact, and a source URL marked `+`.
"""

import os

SKILL_VERSION = "1.3.3"
SOURCE_URL = "https://github.com/burnshall-ui/openclaw-eve-skill"


def build_user_agent() -> str:
    """Assemble the User-Agent string.

    A source URL is always sent. CCP strongly prefers a contact as well, so
    set EVE_ESI_CONTACT to an email address, `discord:name` or `eve:charname`
    to add one — it is left empty by default because the value belongs to
    whoever installed the skill, not to the skill.
    """
    contact = os.environ.get("EVE_ESI_CONTACT", "").strip()
    detail = f"{contact}; +{SOURCE_URL}" if contact else f"+{SOURCE_URL}"
    return f"OpenClaw-ESI-Skill/{SKILL_VERSION} ({detail})"


USER_AGENT = build_user_agent()
