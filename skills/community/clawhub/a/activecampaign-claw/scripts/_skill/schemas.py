"""Structural shapes for AC v3 API records used across the skill.

These are *optional* type hints — current scripts continue to use `dict` and
key-by-string. New code (and gradual refactors of existing code) can import
these `TypedDict`s for IDE completion and static-type checks.

All shapes follow what the AC v3 reference documents, with `total=False` so
fields that aren't always populated don't trip type checkers.
"""

from __future__ import annotations

from typing import TypedDict


class Contact(TypedDict, total=False):
    """`/contacts` per-item shape.

    Source: https://developers.activecampaign.com/reference/list-all-contacts
    """
    id: str
    email: str
    firstName: str
    lastName: str
    phone: str
    cdate: str
    udate: str
    mdate: str
    bounced_hard: str
    bounced_soft: str
    bounced_date: str | None
    status: str
    orgname: str
    orgid: str
    ip: str
    score: str


class Deal(TypedDict, total=False):
    """`/deals` per-item shape (Plus+ feature).

    Source: https://developers.activecampaign.com/reference/list-all-deals
    """
    id: str
    title: str
    value: str         # cents, as a string
    currency: str
    contact: str       # foreign key into /contacts
    owner: str         # foreign key into /users
    group: str         # pipeline id (/dealGroups)
    stage: str         # foreign key into /dealStages
    status: str        # "0"=open, "1"=won, "2"=lost, "3"=hot
    cdate: str
    mdate: str
    edate: str | None  # close/expected close date
    nextdate: str | None


class Campaign(TypedDict, total=False):
    """`/campaigns` per-item shape.

    Source: https://developers.activecampaign.com/reference/list-all-campaigns
    """
    id: str
    name: str
    type: str          # single | recurring | split | responder | reminder | …
    subject: str
    fromname: str
    fromemail: str
    status: str
    send_amt: str      # total sent count (string)
    opens: str
    uniqueopens: str
    linkclicks: str
    uniquelinkclicks: str
    subscriberclicks: str
    bounces: str
    softbounces: str
    hardbounces: str
    forwards: str
    replies: str
    unsubscribereason: str
    templateid: str
    cdate: str
    mdate: str
    sdate: str         # send time


class Tag(TypedDict, total=False):
    """`/tags` per-item shape."""
    id: str
    tag: str
    description: str
    tagType: str
    cdate: str
    subscriber_count: str


class User(TypedDict, total=False):
    """`/users` per-item shape (AC platform users, not contacts)."""
    id: str
    username: str
    email: str
    firstName: str
    lastName: str
    phone: str
    signature: str


class DealTask(TypedDict, total=False):
    """`/dealTasks` per-item shape (Plus+).

    Covers both deal and contact tasks via the `reltype` field.
    Source: https://developers.activecampaign.com/reference/list-all-tasks
    """
    id: str
    title: str
    note: str
    duedate: str
    status: str        # "0"=incomplete, "1"=complete
    relid: str         # foreign key into the related resource
    reltype: str       # "Deal" | "Subscriber" | "Activity"
    userid: str
    assignee_userid: str
    d_tasktypeid: str
    outcome_id: str
    cdate: str
    udate: str


class Note(TypedDict, total=False):
    """`/notes` per-item shape."""
    id: str
    note: str
    relid: str
    reltype: str       # "Deal" | "Subscriber" | "Activity"
    userid: str
    is_draft: str
    cdate: str
    mdate: str


__all__ = [
    "Campaign",
    "Contact",
    "Deal",
    "DealTask",
    "Note",
    "Tag",
    "User",
]
