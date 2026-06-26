# Personas Package
# M-A3 人设系统：幕僚长 + 专业Agent人设

from personas.base import AgentPersona, PersonaType
from personas.chiefofstaff import CHIEF_OF_STAFF
from personas.geo_analyst import GEO_ANALYST
from personas.amazon_operator import AMAZON_OPERATOR
from personas.content_creator import CONTENT_CREATOR

__all__ = [
    "AgentPersona",
    "PersonaType",
    "CHIEF_OF_STAFF",
    "GEO_ANALYST",
    "AMAZON_OPERATOR",
    "CONTENT_CREATOR",
]
