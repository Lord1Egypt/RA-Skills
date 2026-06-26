#!/usr/bin/env python3

from __future__ import annotations

from typing import Any

ACCEPTED_STATUSES = {"accept", "accepted"}
DECLINED_STATUSES = {"decline", "declined"}
PENDING_STATUSES = {"needs_action", "tentative", "pending", "pending_accept", "requested"}
ATTENDEE_STATUS_KEYS = (
    "rsvp_status",
    "status",
    "response_status",
    "attendee_status",
    "invitee_status",
)
ATTENDEE_ID_KEYS = ("open_id", "user_id", "attendee_id", "id", "room_id")
STATUS_VALUE_KEYS = ("status", "value", "name")


def normalize_status_value(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip().lower()
    if isinstance(value, dict):
        for key in STATUS_VALUE_KEYS:
            nested = value.get(key)
            if isinstance(nested, str) and nested.strip():
                return nested.strip().lower()
    return ""


def get_attendee_identifier(attendee: Any) -> str:
    if not isinstance(attendee, dict):
        return ""
    for key in ATTENDEE_ID_KEYS:
        value = attendee.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def is_self_attendee(attendee: Any, user_id: str, _organizer_id: str) -> bool:
    if not isinstance(attendee, dict):
        return False
    if attendee.get("is_self") is True:
        return True

    attendee_id = get_attendee_identifier(attendee)
    if user_id and attendee_id == user_id:
        return True
    return False


def get_attendee_status(attendee: Any) -> str:
    if not isinstance(attendee, dict):
        return ""
    for key in ATTENDEE_STATUS_KEYS:
        status = normalize_status_value(attendee.get(key))
        if status:
            return status
    return ""


def get_self_attendee_status(event: dict[str, Any], user_id: str) -> str:
    event_status = normalize_status_value(event.get("self_rsvp_status"))
    if event_status:
        return event_status

    organizer = event.get("event_organizer", {})
    organizer_id = get_attendee_identifier(organizer)
    if user_id and organizer_id == user_id:
        return "accepted"

    attendees = event.get("attendees", [])
    if not isinstance(attendees, list):
        return ""

    for attendee in attendees:
        if not is_self_attendee(attendee, user_id, organizer_id):
            continue
        status = get_attendee_status(attendee)
        if status:
            return status

    return "needs_action"


def get_resource_attendees(event: dict[str, Any]) -> list[dict[str, Any]]:
    attendees = event.get("attendees", [])
    if not isinstance(attendees, list):
        return []
    return [
        attendee for attendee in attendees
        if isinstance(attendee, dict) and normalize_status_value(attendee.get("type")) == "resource"
    ]


def classify_resource_attendees(
    event: dict[str, Any],
    expected_room_id: str | None = None,
) -> dict[str, str]:
    resource_attendees = get_resource_attendees(event)
    if expected_room_id:
        resource_attendees = [
            attendee for attendee in resource_attendees
            if get_attendee_identifier(attendee) == expected_room_id
        ]

    if not resource_attendees:
        return {"status": "missing", "reason": "room_missing"}

    statuses = [get_attendee_status(attendee) for attendee in resource_attendees]
    if any(status in DECLINED_STATUSES for status in statuses):
        return {"status": "failed", "reason": "room_declined"}
    if any(status in ACCEPTED_STATUSES for status in statuses):
        return {"status": "confirmed", "reason": "already_has_confirmed_room"}
    if any(status in PENDING_STATUSES or not status for status in statuses):
        return {"status": "pending", "reason": "room_pending"}
    return {"status": "pending", "reason": "room_pending"}


def classify_event_for_scan(event: dict[str, Any], user_id: str) -> dict[str, str]:
    self_status = get_self_attendee_status(event, user_id)
    if not self_status:
        return {"status": "pending", "reason": "self_status_missing"}
    if self_status not in ACCEPTED_STATUSES:
        return {"status": "failed", "reason": "self_not_accepted"}

    resource_state = classify_resource_attendees(event)
    if resource_state["status"] == "confirmed":
        return {"status": "failed", "reason": "already_has_confirmed_room"}
    if resource_state["status"] == "pending":
        return {"status": "pending", "reason": "room_pending"}
    if resource_state["status"] == "failed":
        return {"status": "confirmed", "reason": "room_declined"}
    return {"status": "confirmed", "reason": "needs_room"}


def classify_post_booking(
    event: dict[str, Any],
    user_id: str,
    expected_room_id: str | None = None,
) -> dict[str, str]:
    self_status = get_self_attendee_status(event, user_id)
    if not self_status:
        return {"status": "pending", "reason": "self_status_missing"}
    if self_status not in ACCEPTED_STATUSES:
        return {"status": "failed", "reason": "self_not_accepted"}

    resource_state = classify_resource_attendees(event, expected_room_id)
    if resource_state["status"] == "confirmed":
        return {"status": "confirmed", "reason": "booking_confirmed"}
    if resource_state["status"] == "pending":
        return {"status": "pending", "reason": "room_pending"}
    return {"status": "failed", "reason": resource_state["reason"]}
