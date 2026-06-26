import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

import airtap_common as common


SCRIPT_DIR = Path(__file__).resolve().parent
DOTENV_PATH = SCRIPT_DIR / ".env"
LOG_PATH = Path("/tmp/log")
common.load_skill_env(DOTENV_PATH)


@dataclass
class RelayState:
    openclaw_bin: str
    target: str
    channel: Optional[str] = None
    account: Optional[str] = None
    thread_id: Optional[str] = None
    reply_to: Optional[str] = None
    verbose: bool = False
    notified_update_count: int = 0
    suppressed_update_count: int = 0
    plan_delivered: bool = False
    ack_sent: bool = False
    last_notified_update: Optional[str] = None


def _build_milestone_message(title: str, body: Optional[str] = None) -> str:
    if body:
        return f"{title}\n\n{body}"
    return title


def _build_verbose_openclaw_message(
    task_details: Dict[str, Any],
    latest_update: str,
    *,
    is_historical_update: bool = False,
) -> str:
    task_id = task_details.get("taskId", "")
    task_title = common.get_task_title(task_details)
    task_state = task_details.get("taskState", "UNKNOWN")
    message_lines = [
        "Airtap task update",
        f"Task ID: {task_id}",
        f"Task Title: {task_title}",
        f"Current Task State: {task_state}",
    ]
    if is_historical_update:
        message_lines.append(
            "Note: this agent update was discovered in the latest task snapshot and may be older "
            "than the current task state."
        )

    message_lines.extend(
        [
            "",
            "Agent update:",
            latest_update,
        ]
    )
    return "\n".join(message_lines)


def _build_openclaw_ack_message(task_details: Dict[str, Any]) -> str:
    return _build_milestone_message(f"Started: {common.get_task_title(task_details)}")


def _build_openclaw_plan_message(
    task_details: Dict[str, Any],
    plan_text: str,
    *,
    needs_plan_prefix: bool,
) -> str:
    body = plan_text if not needs_plan_prefix else f"Plan:\n{plan_text}"
    return _build_milestone_message(f"Plan: {common.get_task_title(task_details)}", body)


def _build_openclaw_final_message(
    task_details: Dict[str, Any],
    summary_text: Optional[str],
) -> str:
    task_state = str(task_details.get("taskState", "UNKNOWN")).upper()
    task_title = common.get_task_title(task_details)
    title_by_state = {
        "COMPLETED": f"Completed: {task_title}",
        "FAILED": f"Failed: {task_title}",
        "CANCELLED": f"Cancelled: {task_title}",
    }
    return _build_milestone_message(
        title_by_state.get(task_state, f"Finished: {task_title}"),
        summary_text,
    )


def _build_openclaw_blocked_message(
    task_details: Dict[str, Any],
    summary_text: Optional[str],
) -> str:
    task_state = str(task_details.get("taskState", "UNKNOWN")).upper()
    task_title = common.get_task_title(task_details)
    title_by_state = {
        "WAITING_FOR_USER_INPUT": f"Needs your input: {task_title}",
        "WAITING_FOR_USER_INTERVENTION": f"Needs you to take control: {task_title}",
        "WAITING_FOR_USER_CONTINUE": f"Needs your approval to continue: {task_title}",
    }
    return _build_milestone_message(
        title_by_state.get(task_state, f"Action needed: {task_title}"),
        summary_text,
    )


def _resolve_openclaw_executable(command: str) -> str:
    expanded_command = os.path.expanduser(command)
    if Path(expanded_command).name != "openclaw":
        raise ValueError(
            "--openclaw-bin must point to the OpenClaw CLI executable named 'openclaw'."
        )

    if os.path.sep in expanded_command:
        if not os.path.isfile(expanded_command):
            raise ValueError(f"OpenClaw CLI not found: {expanded_command}")
        if not os.access(expanded_command, os.X_OK):
            raise ValueError(f"OpenClaw CLI is not executable: {expanded_command}")
        return expanded_command

    resolved_command = shutil.which(expanded_command)
    if not resolved_command:
        raise ValueError(
            f"OpenClaw CLI not found on PATH: {expanded_command}. Install it or pass --openclaw-bin."
        )

    return resolved_command


def _send_openclaw_message(
    logger,
    *,
    relay_state: RelayState,
    message_text: str,
) -> None:
    command = [relay_state.openclaw_bin, "message", "send"]
    if relay_state.channel:
        command.extend(["--channel", relay_state.channel])
    if relay_state.account:
        command.extend(["--account", relay_state.account])
    command.extend(["--target", relay_state.target])
    if relay_state.thread_id:
        command.extend(["--thread-id", relay_state.thread_id])
    if relay_state.reply_to:
        command.extend(["--reply-to", relay_state.reply_to])
    command.extend(["--message", message_text])
    logger.info(
        "OpenClaw send target=%s channel=%s account=%s threadId=%s replyTo=%s preview=%s",
        relay_state.target,
        relay_state.channel or "",
        relay_state.account or "",
        relay_state.thread_id or "",
        relay_state.reply_to or "",
        common.truncate_text(message_text),
    )

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info("OpenClaw send succeeded target=%s", relay_state.target)
    except FileNotFoundError as exc:
        logger.exception("OpenClaw CLI not found: %s", relay_state.openclaw_bin)
        raise ValueError(
            f"OpenClaw CLI not found: {relay_state.openclaw_bin}. Install it or pass --openclaw-bin."
        ) from exc
    except subprocess.CalledProcessError as exc:
        error_output = (exc.stderr or exc.stdout or "").strip()
        if not error_output:
            error_output = str(exc)
        logger.exception(
            "OpenClaw send failed target=%s error=%s",
            relay_state.target,
            error_output,
        )
        raise RuntimeError(f"OpenClaw send failed: {error_output}") from exc


def _handle_poll_snapshot(
    logger,
    relay_state: RelayState,
    task_details: Dict[str, Any],
    unseen_agent_messages: List[common.AgentUpdate],
    has_historical_backlog: bool,
    latest_agent_update: Optional[common.AgentUpdate],
) -> None:
    task_id = task_details.get("taskId", "")
    task_state = task_details.get("taskState")
    latest_agent_update_index = latest_agent_update[0] if latest_agent_update else None
    latest_agent_update_text = latest_agent_update[2] if latest_agent_update else None

    if relay_state.verbose:
        for position, (_, _, latest_update) in enumerate(unseen_agent_messages):
            is_historical_update = (
                has_historical_backlog and position < len(unseen_agent_messages) - 1
            )

            _send_openclaw_message(
                logger,
                relay_state=relay_state,
                message_text=_build_verbose_openclaw_message(
                    task_details,
                    latest_update,
                    is_historical_update=is_historical_update,
                ),
            )
            relay_state.notified_update_count += 1
            relay_state.last_notified_update = latest_update
            logger.info(
                "Forwarded Airtap update taskId=%s notifiedUpdateCount=%s historical=%s preview=%s",
                task_id,
                relay_state.notified_update_count,
                is_historical_update,
                common.truncate_text(latest_update),
            )
        return

    if not relay_state.ack_sent:
        ack_message = _build_openclaw_ack_message(task_details)
        _send_openclaw_message(
            logger,
            relay_state=relay_state,
            message_text=ack_message,
        )
        relay_state.ack_sent = True
        relay_state.notified_update_count += 1
        relay_state.last_notified_update = ack_message
        logger.info("Forwarded Airtap ack taskId=%s", task_id)

    delivered_plan_index: Optional[int] = None
    if not relay_state.plan_delivered:
        for index, agent_message, _ in unseen_agent_messages:
            plan_update = common.get_plan_update_text(agent_message)
            if not plan_update:
                continue

            plan_text, needs_plan_prefix = plan_update
            _send_openclaw_message(
                logger,
                relay_state=relay_state,
                message_text=_build_openclaw_plan_message(
                    task_details,
                    plan_text,
                    needs_plan_prefix=needs_plan_prefix,
                ),
            )
            relay_state.plan_delivered = True
            delivered_plan_index = index
            relay_state.notified_update_count += 1
            relay_state.last_notified_update = (
                f"Plan:\n{plan_text}" if needs_plan_prefix else plan_text
            )
            logger.info(
                "Forwarded Airtap plan update taskId=%s preview=%s",
                task_id,
                common.truncate_text(plan_text),
            )
            break

    delivered_state_summary_index: Optional[int] = None
    if isinstance(task_state, str) and task_state in common.POLL_STOP_TASK_STATES:
        if task_state in common.POLL_FINAL_TASK_STATES:
            state_message = _build_openclaw_final_message(
                task_details,
                latest_agent_update_text,
            )
        else:
            state_message = _build_openclaw_blocked_message(
                task_details,
                latest_agent_update_text,
            )

        _send_openclaw_message(
            logger,
            relay_state=relay_state,
            message_text=state_message,
        )
        delivered_state_summary_index = latest_agent_update_index
        relay_state.notified_update_count += 1
        relay_state.last_notified_update = latest_agent_update_text or state_message
        logger.info(
            "Forwarded Airtap state milestone taskId=%s taskState=%s preview=%s",
            task_id,
            task_state,
            common.truncate_text(latest_agent_update_text or state_message),
        )

    suppressed_this_poll = 0
    for index, _, _ in unseen_agent_messages:
        if delivered_plan_index == index:
            continue
        if delivered_state_summary_index == index:
            continue
        suppressed_this_poll += 1

    relay_state.suppressed_update_count += suppressed_this_poll
    if suppressed_this_poll:
        logger.info(
            "Suppressed Airtap intermediate updates taskId=%s suppressedThisPoll=%s totalSuppressed=%s",
            task_id,
            suppressed_this_poll,
            relay_state.suppressed_update_count,
        )


def api_poll_task_with_openclaw(
    *,
    logger,
    task_id: str,
    interval_secs: float = common.DEFAULT_POLL_INTERVAL_SECS,
    openclaw_bin: str = "openclaw",
    openclaw_target: str,
    openclaw_channel: Optional[str] = None,
    openclaw_account: Optional[str] = None,
    openclaw_thread_id: Optional[str] = None,
    openclaw_reply_to: Optional[str] = None,
    openclaw_verbose: bool = False,
) -> Dict[str, Any]:
    resolved_openclaw_bin = _resolve_openclaw_executable(openclaw_bin)
    relay_state = RelayState(
        openclaw_bin=resolved_openclaw_bin,
        target=openclaw_target,
        channel=openclaw_channel,
        account=openclaw_account,
        thread_id=openclaw_thread_id,
        reply_to=openclaw_reply_to,
        verbose=openclaw_verbose,
    )
    logger.info(
        "Polling task %s with OpenClaw delivery mode=%s channel=%s target=%s threadId=%s replyTo=%s",
        task_id,
        "verbose" if openclaw_verbose else "milestone",
        openclaw_channel or "",
        openclaw_target,
        openclaw_thread_id or "",
        openclaw_reply_to or "",
    )

    task_details = common.poll_task(
        logger=logger,
        task_id=task_id,
        interval_secs=interval_secs,
        on_poll=lambda details, unseen_messages, has_backlog, latest_update, _attempt: _handle_poll_snapshot(
            logger,
            relay_state,
            details,
            unseen_messages,
            has_backlog,
            latest_update,
        ),
    )
    task_details["_poll"].update(
        {
            "notifiedUpdateCount": relay_state.notified_update_count,
            "openclawDeliveryEnabled": True,
            "openclawVerbose": openclaw_verbose,
            "suppressedUpdateCount": relay_state.suppressed_update_count,
            "planDelivered": relay_state.plan_delivered,
            "lastNotifiedUpdate": relay_state.last_notified_update,
        }
    )
    return task_details


def _summarize_args(args: argparse.Namespace) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "resource": getattr(args, "resource", None),
        "action": getattr(args, "action", None),
        "taskId": getattr(args, "task_id", None),
        "receiverId": getattr(args, "receiver_id", None),
        "modelId": getattr(args, "model_id", None),
        "openclawTarget": getattr(args, "openclaw_target", None),
        "openclawVerbose": getattr(args, "openclaw_verbose", None),
    }
    return {key: value for key, value in summary.items() if value}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Airtap API client for receivers, models, tasks, and user location updates.\n\n"
            f"Authentication: load {common.TOKEN_ENV_VAR} from .env before running any API command.\n"
            f"Base URL: {common.get_base_url()}"
        ),
        epilog=(
            "Examples:\n"
            "  python3 airtap.py --add-token \"your-key\"\n"
            "  python3 airtap.py receiver get-list\n"
            "  python3 airtap.py model get-list\n"
            "  python3 airtap.py task create --message \"Open Instagram\"\n"
            "  python3 airtap.py task create --message \"Compare Amazon and Zepto prices\" "
            "--model-id airtap-1.0\n"
            "  python3 airtap.py task get-details --task-id task_abc123\n"
            "  python3 airtap.py task poll --task-id task_abc123\n"
            "  python3 airtap.py task poll --task-id task_abc123 --openclaw-target channel:123\n"
            "  python3 airtap.py task add-user-message --task-id task_abc123 --message \"Continue\"\n"
            "  python3 airtap.py task cancel --task-id task_abc123\n"
            "  python3 airtap.py user update-location --payload "
            '\'{"latitude":12.9716,"longitude":77.5946}\''
        ),
        formatter_class=common.AirtapHelpFormatter,
    )
    parser.add_argument(
        "--add-token",
        metavar="TOKEN",
        help=f"Create or update {DOTENV_PATH.name} next to airtap.py with {common.TOKEN_ENV_VAR}",
    )
    subparsers = parser.add_subparsers(
        dest="resource",
        title="Resources",
        metavar="{receiver,model,task,user}",
    )

    receiver_parser = subparsers.add_parser(
        "receiver",
        help="List available receivers",
        description="Receiver APIs.\n\nUse this resource to inspect available devices.",
        formatter_class=common.AirtapHelpFormatter,
    )
    receiver_subparsers = receiver_parser.add_subparsers(
        dest="action",
        required=True,
        title="Actions",
    )
    receiver_subparsers.add_parser(
        "get-list",
        help="List available receivers",
        description="POST /receiver/v1/rcvrGetList\n\nReturns the receivers you can target.",
        formatter_class=common.AirtapHelpFormatter,
    )

    model_parser = subparsers.add_parser(
        "model",
        help="List available models",
        description="Model APIs.\n\nUse this resource to inspect available task models.",
        formatter_class=common.AirtapHelpFormatter,
    )
    model_subparsers = model_parser.add_subparsers(
        dest="action",
        required=True,
        title="Actions",
    )
    model_subparsers.add_parser(
        "get-list",
        help="List available models",
        description="POST /mreg/v1/mregGetModels\n\nReturns the models you can use for task creation.",
        formatter_class=common.AirtapHelpFormatter,
    )

    task_parser = subparsers.add_parser(
        "task",
        help="Create, inspect, message, or cancel tasks",
        description=(
            "Task APIs.\n\nUse these commands to create a task, inspect its state, "
            "send follow-up input, cancel execution, or optionally forward updates to OpenClaw."
        ),
        formatter_class=common.AirtapHelpFormatter,
    )
    task_subparsers = task_parser.add_subparsers(dest="action", required=True, title="Actions")

    task_create_parser = task_subparsers.add_parser(
        "create",
        help="Create a new task",
        description=(
            "POST /task/v1/taskCreate\n\nCreates a new Airtap task with the initial user message."
        ),
        formatter_class=common.AirtapHelpFormatter,
    )
    task_create_parser.add_argument(
        "--message",
        required=True,
        help="Initial task message the agent should act on",
    )
    task_create_parser.add_argument(
        "--receiver-id",
        default=common.DEFAULT_RECEIVER_ID,
        help="Receiver ID to run the task on",
    )
    task_create_parser.add_argument(
        "--image-file",
        help="Optional image file to attach to the initial message",
    )
    task_create_parser.add_argument(
        "--model-id",
        help="Optional model ID to use for the task. If omitted, the server default is used.",
    )

    task_subparsers.add_parser(
        "get-list",
        help="List tasks",
        description="POST /task/v1/taskGetList\n\nReturns the tasks visible to your account.",
        formatter_class=common.AirtapHelpFormatter,
    )

    task_details_parser = task_subparsers.add_parser(
        "get-details",
        help="Fetch task details",
        description="POST /task/v1/taskGetDetails\n\nFetches the details for a single task.",
        formatter_class=common.AirtapHelpFormatter,
    )
    task_details_parser.add_argument("--task-id", required=True, help="Task ID")

    task_poll_parser = task_subparsers.add_parser(
        "poll",
        help="Poll task details until the task needs user input or finishes",
        description=(
            "Polls task details until the task reaches a terminal or waiting state. "
            "By default it polls Airtap locally. When OpenClaw delivery options are provided, "
            "milestone updates are forwarded with `openclaw message send` by default."
        ),
        formatter_class=common.AirtapHelpFormatter,
    )
    task_poll_parser.add_argument("--task-id", required=True, help="Task ID")
    task_poll_parser.add_argument(
        "--interval-secs",
        type=float,
        default=common.DEFAULT_POLL_INTERVAL_SECS,
        help="Seconds to wait between task detail polls",
    )
    task_poll_parser.add_argument(
        "--openclaw-bin",
        default="openclaw",
        help="Path to the OpenClaw CLI executable named 'openclaw'",
    )
    task_poll_parser.add_argument(
        "--openclaw-channel",
        help="Optional OpenClaw channel name, for example discord or telegram",
    )
    task_poll_parser.add_argument(
        "--openclaw-account",
        help="Optional OpenClaw account scope for the channel",
    )
    task_poll_parser.add_argument(
        "--openclaw-target",
        help="Optional OpenClaw target to notify, for example channel:123 or @username",
    )
    task_poll_parser.add_argument(
        "--openclaw-thread-id",
        help="Optional OpenClaw thread or topic identifier for the outbound message",
    )
    task_poll_parser.add_argument(
        "--openclaw-reply-to",
        help="Optional OpenClaw message ID to reply to inside the target conversation",
    )
    task_poll_parser.add_argument(
        "--openclaw-verbose",
        action="store_true",
        help="Forward every new Airtap agent update instead of milestone-only OpenClaw updates",
    )

    task_message_parser = task_subparsers.add_parser(
        "add-user-message",
        help="Send a follow-up message to a task",
        description=(
            "POST /task/v1/taskAddUserMessage\n\nAdds a user follow-up message to an existing task."
        ),
        formatter_class=common.AirtapHelpFormatter,
    )
    task_message_parser.add_argument("--task-id", required=True, help="Task ID")
    task_message_parser.add_argument(
        "--message",
        required=True,
        help="Follow-up message text",
    )
    task_message_parser.add_argument(
        "--image-file",
        help="Optional image file to attach to the follow-up message",
    )

    task_cancel_parser = task_subparsers.add_parser(
        "cancel",
        help="Cancel a task",
        description="POST /task/v1/taskCancel\n\nCancels a running or queued task.",
        formatter_class=common.AirtapHelpFormatter,
    )
    task_cancel_parser.add_argument("--task-id", required=True, help="Task ID")

    user_parser = subparsers.add_parser(
        "user",
        help="Manage user-specific APIs",
        description="User APIs.\n\nCurrently supports updating user location.",
        formatter_class=common.AirtapHelpFormatter,
    )
    user_subparsers = user_parser.add_subparsers(dest="action", required=True, title="Actions")
    user_location_parser = user_subparsers.add_parser(
        "update-location",
        help="Update the user location",
        description=(
            "POST /user/v1/userUpdateLocation\n\nUpdates the user's location using a JSON payload."
        ),
        formatter_class=common.AirtapHelpFormatter,
    )
    user_location_parser.add_argument(
        "--payload",
        help='Raw JSON payload string, for example \'{"latitude":12.9716,"longitude":77.5946}\'',
    )

    return parser


def main() -> None:
    parser = build_parser()
    logger = common.get_logger("airtap_cli", LOG_PATH)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(2)

    args = parser.parse_args()
    logger.info("CLI invocation %s", json.dumps(_summarize_args(args), sort_keys=True))

    try:
        if args.add_token:
            common.write_token_to_dotenv(DOTENV_PATH, logger, args.add_token)
            print(f"Saved {common.TOKEN_ENV_VAR} to {DOTENV_PATH}")
            if args.resource is None:
                return

        if args.resource == "receiver" and args.action == "get-list":
            common.print_response(common.api_get_receivers(logger))
            return

        if args.resource == "model" and args.action == "get-list":
            common.print_response(common.api_get_models(logger))
            return

        if args.resource == "task":
            if args.action == "create":
                common.print_response(
                    common.api_create_task(
                        logger,
                        message_text=args.message,
                        receiver_id=args.receiver_id,
                        image_file=args.image_file,
                        model_id=args.model_id,
                    )
                )
                return

            if args.action == "get-list":
                common.print_response(common.api_list_tasks(logger))
                return

            if args.action == "get-details":
                common.print_response(common.api_get_task_details(logger, args.task_id))
                return

            if args.action == "poll":
                if args.openclaw_target:
                    common.print_response(
                        api_poll_task_with_openclaw(
                            logger=logger,
                            task_id=args.task_id,
                            interval_secs=args.interval_secs,
                            openclaw_bin=args.openclaw_bin,
                            openclaw_channel=args.openclaw_channel,
                            openclaw_account=args.openclaw_account,
                            openclaw_target=args.openclaw_target,
                            openclaw_thread_id=args.openclaw_thread_id,
                            openclaw_reply_to=args.openclaw_reply_to,
                            openclaw_verbose=args.openclaw_verbose,
                        )
                    )
                else:
                    common.print_response(
                        common.poll_task(
                            logger=logger,
                            task_id=args.task_id,
                            interval_secs=args.interval_secs,
                        )
                    )
                return

            if args.action == "add-user-message":
                common.print_response(
                    common.api_add_user_message(
                        logger,
                        args.task_id,
                        args.message,
                        args.image_file,
                    )
                )
                return

            if args.action == "cancel":
                common.print_response(common.api_cancel_task(logger, args.task_id))
                return

        if args.resource == "user" and args.action == "update-location":
            payload = common.load_json_payload(args.payload)
            common.print_response(common.api_update_user_location(logger, payload))
            return

        parser.error("No valid command handler matched the parsed arguments.")
    except requests.exceptions.ConnectionError:
        logger.exception("Could not connect to Airtap API at %s", common.get_base_url())
        print(f"Error: Could not connect to API server at {common.get_base_url()}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        logger.exception(
            "Request to Airtap API timed out after %s seconds",
            common.DEFAULT_TIMEOUT_SECS,
        )
        print(
            f"Error: Request to API server timed out after {common.DEFAULT_TIMEOUT_SECS} seconds",
            file=sys.stderr,
        )
        sys.exit(1)
    except requests.exceptions.HTTPError as exc:
        logger.exception("HTTP error while calling Airtap API")
        response = exc.response
        if response is not None and response.text:
            print(response.text, file=sys.stderr)
        else:
            print(f"HTTP error: {exc}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as exc:
        logger.exception("File not found")
        print(f"Error: File not found: {exc}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        logger.exception("Invalid JSON payload")
        print(f"Error: Invalid JSON payload: {exc}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        logger.exception("Runtime error")
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        logger.exception("Value error")
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
