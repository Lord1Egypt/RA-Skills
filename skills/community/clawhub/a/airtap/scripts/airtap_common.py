import argparse
import base64
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import requests
from dotenv import load_dotenv, set_key


DEFAULT_BASE_URL = "https://airtap.ai/cortex/api"
TOKEN_ENV_VAR = "AIRTAP_PERSONAL_ACCESS_TOKEN"
DEFAULT_RECEIVER_ID = "cloud"
DEFAULT_TIMEOUT_SECS = 60
DEFAULT_POLL_INTERVAL_SECS = 10.0
UPDATE_SKILL_HINT = (
    "Get an updated version of the Airtap skill before retrying."
)
PILOT_CLIENT_TYPE_HEADER_NAME = "x-airtap-pilot-client-type"
PILOT_CLIENT_NAME_HEADER_NAME = "x-airtap-pilot-client-name"
CLIENT_NAME_ENV_VAR = "AIRTAP_CLIENT_NAME"
SKILL_CLIENT_TYPE = "pilot-agent"
POLL_FINAL_TASK_STATES = {
    "COMPLETED",
    "FAILED",
    "CANCELLED",
}
POLL_WAITING_TASK_STATES = {
    "WAITING_FOR_USER_INPUT",
    "WAITING_FOR_USER_INTERVENTION",
    "WAITING_FOR_USER_CONTINUE",
}
POLL_STOP_TASK_STATES = POLL_FINAL_TASK_STATES | POLL_WAITING_TASK_STATES
PLAN_KEYWORD = "plan"
AgentUpdate = Tuple[int, Dict[str, Any], str]
PollCallback = Callable[
    [Dict[str, Any], List[AgentUpdate], bool, Optional[AgentUpdate], int],
    None,
]


class AirtapHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


def load_skill_env(*dotenv_paths: Path) -> None:
    for dotenv_path in dotenv_paths:
        load_dotenv(dotenv_path, override=True)


def get_base_url() -> str:
    return os.environ.get("AIRTAP_BASE_URL", DEFAULT_BASE_URL)


def get_logger(name: str, log_path: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger


def truncate_text(value: str, limit: int = 160) -> str:
    if len(value) <= limit:
        return value
    return f"{value[:limit]}..."


def normalize_optional_text(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None

    normalized_value = value.strip()
    if not normalized_value:
        return None

    return normalized_value


def write_token_to_dotenv(
    dotenv_path: Path,
    logger: logging.Logger,
    token: str,
) -> None:
    normalized_token = token.strip()
    if not normalized_token:
        raise ValueError("Token must not be empty.")

    set_key(dotenv_path, TOKEN_ENV_VAR, normalized_token)
    os.environ[TOKEN_ENV_VAR] = normalized_token
    logger.info("Saved Airtap token to %s", dotenv_path)


def get_auth_headers() -> Dict[str, str]:
    token = os.environ.get(TOKEN_ENV_VAR)
    if not token:
        raise ValueError(
            f"Missing auth token. Run --add-token or add {TOKEN_ENV_VAR} to .env before running this command."
        )

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        PILOT_CLIENT_TYPE_HEADER_NAME: SKILL_CLIENT_TYPE,
        PILOT_CLIENT_NAME_HEADER_NAME: get_skill_client_name(),
    }


def get_skill_client_name() -> str:
    explicit_client_name = normalize_optional_text(os.environ.get(CLIENT_NAME_ENV_VAR))
    if explicit_client_name:
        return explicit_client_name.lower()

    if any(env_name.startswith("CODEX_") for env_name in os.environ):
        return "codex"

    if any(env_name.startswith("OPENCLAW_") for env_name in os.environ):
        return "openclaw"

    return "airtap"


def read_base64_file(file_path: str) -> str:
    return base64.b64encode(Path(file_path).read_bytes()).decode("utf-8")


def build_user_message(
    message_text: str,
    image_file: Optional[str] = None,
) -> Dict[str, Any]:
    parts = [{"type": "text", "text": message_text}]
    if image_file:
        parts.append(
            {
                "type": "image",
                "contentBase64": read_base64_file(image_file),
            }
        )

    return {
        "type": "user",
        "parts": parts,
    }


def load_json_payload(payload_text: Optional[str]) -> Dict[str, Any]:
    if payload_text:
        return json.loads(payload_text)

    raise ValueError("A JSON payload is required.")


def extract_text_parts(parts: Any) -> List[str]:
    if not isinstance(parts, list):
        return []

    text_parts: List[str] = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        if part.get("type") != "text":
            continue
        text = normalize_optional_text(part.get("text"))
        if text:
            text_parts.append(text)

    return text_parts


def summarize_message(message: Any) -> Dict[str, Any]:
    if not isinstance(message, dict):
        return {"present": bool(message)}

    parts = message.get("parts")
    text_parts = extract_text_parts(parts)
    return {
        "textPartCount": len(text_parts),
        "textPreview": truncate_text(text_parts[0]) if text_parts else "",
        "hasImage": any(
            isinstance(part, dict) and part.get("type") == "image"
            for part in parts
        )
        if isinstance(parts, list)
        else False,
    }


def summarize_payload(payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not payload:
        return {}

    summary: Dict[str, Any] = {}
    for key in ("taskId", "receiverId", "modelId"):
        value = payload.get(key)
        if value:
            summary[key] = value

    if "userMessage" in payload:
        summary["userMessage"] = summarize_message(payload.get("userMessage"))
    if "message" in payload:
        summary["message"] = summarize_message(payload.get("message"))
    if "latitude" in payload or "longitude" in payload:
        summary["location"] = {
            "latitude": payload.get("latitude"),
            "longitude": payload.get("longitude"),
        }

    summary["keys"] = sorted(payload.keys())
    return summary


def request_api(
    logger: logging.Logger,
    method: str,
    path: str,
    *,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    logger.info(
        "Airtap API request method=%s path=%s payload=%s",
        method,
        path,
        json.dumps(summarize_payload(payload), sort_keys=True),
    )
    start_time = time.monotonic()

    try:
        response = requests.request(
            method,
            f"{get_base_url()}{path}",
            headers=get_auth_headers(),
            json=payload,
            timeout=DEFAULT_TIMEOUT_SECS,
        )
        duration_ms = round((time.monotonic() - start_time) * 1000, 1)
        logger.info(
            "Airtap API response method=%s path=%s status=%s durationMs=%s",
            method,
            path,
            response.status_code,
            duration_ms,
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        logger.exception("Airtap API HTTP failure method=%s path=%s", method, path)
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        raise RuntimeError(
            f"Airtap API request failed with status {status_code} for {path}. {UPDATE_SKILL_HINT}"
        ) from exc
    except requests.RequestException as exc:
        logger.exception("Airtap API failure method=%s path=%s", method, path)
        raise RuntimeError(
            f"Airtap API request failed for {path}. {UPDATE_SKILL_HINT}"
        ) from exc


def api_get_receivers(logger: logging.Logger) -> Dict[str, Any]:
    return request_api(logger, "POST", "/receiver/v1/rcvrGetList", payload={})


def api_get_models(logger: logging.Logger) -> Dict[str, Any]:
    return request_api(logger, "POST", "/mreg/v1/mregGetModels", payload={})


def api_create_task(
    logger: logging.Logger,
    message_text: str,
    receiver_id: str = DEFAULT_RECEIVER_ID,
    image_file: Optional[str] = None,
    model_id: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "receiverId": receiver_id,
        "userMessage": build_user_message(message_text, image_file),
    }
    if model_id:
        payload["modelId"] = model_id
    return request_api(logger, "POST", "/task/v1/taskCreate", payload=payload)


def api_list_tasks(logger: logging.Logger) -> Dict[str, Any]:
    return request_api(logger, "POST", "/task/v1/taskGetList", payload={})


def api_get_task_details(logger: logging.Logger, task_id: str) -> Dict[str, Any]:
    return request_api(logger, "POST", "/task/v1/taskGetDetails", payload={"taskId": task_id})


def api_add_user_message(
    logger: logging.Logger,
    task_id: str,
    message_text: str,
    image_file: Optional[str] = None,
) -> Dict[str, Any]:
    return request_api(
        logger,
        "POST",
        "/task/v1/taskAddUserMessage",
        payload={
            "taskId": task_id,
            "message": build_user_message(message_text, image_file),
        },
    )


def api_cancel_task(logger: logging.Logger, task_id: str) -> Dict[str, Any]:
    return request_api(logger, "POST", "/task/v1/taskCancel", payload={"taskId": task_id})


def api_update_user_location(
    logger: logging.Logger,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    return request_api(logger, "POST", "/user/v1/userUpdateLocation", payload=payload)


def extract_text_part_entries(
    message: Dict[str, Any],
) -> List[Tuple[str, Optional[str], Optional[str]]]:
    parts = message.get("parts")
    if not isinstance(parts, list):
        return []

    text_part_entries: List[Tuple[str, Optional[str], Optional[str]]] = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        if part.get("type") != "text":
            continue

        text = normalize_optional_text(part.get("text"))
        if not text:
            continue

        text_part_entries.append(
            (
                text,
                normalize_optional_text(part.get("group")),
                normalize_optional_text(part.get("subGroup")),
            )
        )

    return text_part_entries


def extract_message_text(message: Dict[str, Any]) -> str:
    return "\n\n".join(text for text, _, _ in extract_text_part_entries(message))


def get_task_title(task_details: Dict[str, Any]) -> str:
    task_title = task_details.get("taskTitle")
    if isinstance(task_title, str) and task_title.strip():
        return task_title.strip()

    messages = task_details.get("messages")
    if isinstance(messages, list):
        for message in messages:
            if not isinstance(message, dict):
                continue
            if message.get("type") != "user":
                continue
            message_text = extract_message_text(message)
            if message_text:
                return message_text

    return "Untitled Airtap task"


def get_agent_messages(task_details: Dict[str, Any]) -> List[Tuple[int, Dict[str, Any]]]:
    messages = task_details.get("messages")
    if not isinstance(messages, list):
        return []

    agent_messages: List[Tuple[int, Dict[str, Any]]] = []
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            continue
        if message.get("type") != "agent":
            continue
        agent_messages.append((index, message))

    return agent_messages


def build_agent_message_signature(index: int, message: Dict[str, Any]) -> str:
    signature_parts = [
        f"{text}|{group or ''}|{sub_group or ''}"
        for text, group, sub_group in extract_text_part_entries(message)
    ]
    return f"{index}:{'||'.join(signature_parts)}"


def contains_plan_keyword(value: Optional[str]) -> bool:
    return bool(value) and PLAN_KEYWORD in value.casefold()


def get_plan_update_text(message: Dict[str, Any]) -> Optional[Tuple[str, bool]]:
    text_part_entries = extract_text_part_entries(message)
    if not text_part_entries:
        return None

    message_text = "\n\n".join(text for text, _, _ in text_part_entries)
    text_matches_plan = any(contains_plan_keyword(text) for text, _, _ in text_part_entries)
    label_matches_plan = any(
        contains_plan_keyword(group) or contains_plan_keyword(sub_group)
        for _, group, sub_group in text_part_entries
    )
    if not text_matches_plan and not label_matches_plan:
        return None

    return message_text, label_matches_plan and not text_matches_plan


def get_latest_agent_update(
    task_details: Dict[str, Any],
) -> Optional[AgentUpdate]:
    agent_messages = get_agent_messages(task_details)
    for index, agent_message in reversed(agent_messages):
        latest_update = extract_message_text(agent_message)
        if latest_update:
            return index, agent_message, latest_update

    return None


def poll_task(
    *,
    logger: logging.Logger,
    task_id: str,
    interval_secs: float = DEFAULT_POLL_INTERVAL_SECS,
    on_poll: Optional[PollCallback] = None,
) -> Dict[str, Any]:
    if interval_secs <= 0:
        raise ValueError("--interval-secs must be greater than 0.")

    logger.info("Polling task %s", task_id)
    seen_agent_signatures: Set[str] = set()
    poll_attempts = 0

    while True:
        task_details = api_get_task_details(logger, task_id)
        poll_attempts += 1
        task_state = task_details.get("taskState")
        message_count = (
            len(task_details.get("messages", []))
            if isinstance(task_details.get("messages"), list)
            else 0
        )
        logger.info(
            "Poll attempt=%s taskId=%s taskState=%s messageCount=%s",
            poll_attempts,
            task_id,
            task_state,
            message_count,
        )

        unseen_agent_messages: List[AgentUpdate] = []
        for index, agent_message in get_agent_messages(task_details):
            message_signature = build_agent_message_signature(index, agent_message)
            if message_signature in seen_agent_signatures:
                continue
            seen_agent_signatures.add(message_signature)

            latest_update = extract_message_text(agent_message)
            if not latest_update:
                continue
            unseen_agent_messages.append((index, agent_message, latest_update))

        has_historical_backlog = (
            isinstance(task_state, str)
            and task_state in POLL_STOP_TASK_STATES
            and len(unseen_agent_messages) > 1
        )
        if has_historical_backlog:
            logger.info(
                "Task %s reached state=%s with %s unseen agent messages in the snapshot",
                task_id,
                task_state,
                len(unseen_agent_messages),
            )

        latest_agent_update = get_latest_agent_update(task_details)
        if on_poll:
            on_poll(
                task_details,
                unseen_agent_messages,
                has_historical_backlog,
                latest_agent_update,
                poll_attempts,
            )

        if isinstance(task_state, str) and task_state in POLL_STOP_TASK_STATES:
            task_details["_poll"] = {
                "intervalSecs": interval_secs,
                "pollAttempts": poll_attempts,
                "stoppedOnTaskState": task_state,
            }
            logger.info(
                "Polling finished taskId=%s taskState=%s pollAttempts=%s",
                task_id,
                task_state,
                poll_attempts,
            )
            return task_details

        time.sleep(interval_secs)


def print_response(result: Dict[str, Any]) -> None:
    print(json.dumps(result, indent=2, default=str))
