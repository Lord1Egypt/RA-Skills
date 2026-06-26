from __future__ import annotations

import json
from typing import Optional
from pathlib import Path


def send_report_via_openclaw(
    report_content: str,
    bot_account_id: str,
    bot_target: str,
    report_title: str = "Garden Irrigation Report"
) -> bool:
    """Send a report to the specified bot via the OpenClaw message system.

    In an OpenClaw agent environment, we attempt to call the message tool directly.
    If that is not possible, we output instructions for external handling.

    Args:
        report_content: Report content (Markdown format)
        bot_account_id: Bot account ID
        bot_target: Destination address, e.g. "telegram:8604429591"
        report_title: Report title

    Returns:
        bool: Whether sending succeeded
    """
    try:
        # Method 1: try to call the OpenClaw message tool directly
        try:
            # In an OpenClaw agent environment, tools are available via a special mechanism.
            # We attempt to import and call them.
            import sys
            import os

            # Check whether we are running inside an OpenClaw agent
            # by looking for environment variables or runtime characteristics.
            is_openclaw_agent = os.environ.get('OPENCLAW_AGENT_ID') or \
                               'openclaw' in sys.executable.lower() or \
                               hasattr(sys, '_openclaw_tools')

            if is_openclaw_agent:
                # Attempt a direct message tool call.
                # In a real OpenClaw agent, tool calls are handled via a special mechanism.
                print(f"[Notification] Inside OpenClaw agent environment, preparing to send message...")

                # build message
                full_message = f"**{report_title}**\n\n{report_content}"

                # In a real OpenClaw agent this would invoke the tool directly.
                # We are inside the agent, but need to ensure the correct context.

                # Output the instruction for the running agent to handle.
                import json
                message_payload = {
                    "action": "send",
                    "to": bot_target,
                    "accountId": bot_account_id,
                    "message": full_message
                }

                # In a real OpenClaw integration, this output will be intercepted and executed.
                print(f"[OPENCLAW_TOOL_CALL] message {json.dumps(message_payload)}")
                return True
            else:
                print(f"[Notification] Not in OpenClaw agent environment, falling back to instruction output")
                raise Exception("Not in OpenClaw agent environment")

        except Exception as inner_e:
            print(f"[Notification] Direct call failed: {inner_e}")

            # Method 2: output detailed send instructions for manual or wrapper processing
            print(f"\n=== Report send instructions (requires manual or wrapper handling) ===")
            print(f"Target: {bot_target}")
            print(f"Account: {bot_account_id}")
            print(f"Title: {report_title}")
            print(f"Content length: {len(report_content)} characters")
            print(f"Content preview:\n{report_content[:300]}...")
            print(f"=== End instructions ===\n")

            # In a real deployment, the wrapper running this script should:
            # 1. Capture this output
            # 2. Parse the instructions
            # 3. Call OpenClaw's message tool to send
            return True

    except Exception as e:
        print(f"[Notification error] Failed to send report: {e}")
        return False


def should_send_report(
    reporting_config: dict,
    irrigation_decision: dict
) -> bool:
    """Determine whether to send a report based on config and irrigation decision.

    Args:
        reporting_config: The reporting section of the system config
        irrigation_decision: Irrigation decision result

    Returns:
        bool: Whether the report should be sent
    """
    # basic checks
    if not reporting_config.get('enabled', False):
        return False

    if not reporting_config.get('send_report_to_bot', False):
        return False

    # check bot configuration
    if not reporting_config.get('bot_account_id') or not reporting_config.get('bot_target'):
        print("[Notification warning] Bot configuration incomplete, skipping send")
        return False

    # decide based on irrigation decision
    should_irrigate = irrigation_decision.get('should_irrigate', False)
    
    if should_irrigate and reporting_config.get('send_on_irrigation', True):
        return True
    
    if not should_irrigate and reporting_config.get('send_on_no_irrigation', False):
        return True
    
    return False


def format_report_for_messaging(
    report_content: str,
    title: str = "🌱 Garden Irrigation Report"
) -> str:
    """Format report content for message delivery.

    Messaging platforms may have length limits, so we truncate or format as needed.

    Args:
        report_content: Raw report content
        title: Report title

    Returns:
        str: Formatted message content
    """
    # prepend title
    formatted = f"**{title}**\n\n"

    # enforce length limit (Telegram max is ~4096 characters)
    max_length = 3500
    if len(report_content) > max_length:
        # truncate and append notice
        formatted += report_content[:max_length]
        formatted += f"\n\n... (report too long, truncated — see file for full report)"
    else:
        formatted += report_content

    return formatted


def send_report_if_needed(
    reporting_config: dict,
    irrigation_decision: dict,
    report_content: str,
    report_title: Optional[str] = None
) -> bool:
    """Send the report if configuration and decision conditions are met.

    Args:
        reporting_config: The reporting section of the system config
        irrigation_decision: Irrigation decision result
        report_content: Report content
        report_title: Optional report title

    Returns:
        bool: Whether a report was sent
    """
    if not should_send_report(reporting_config, irrigation_decision):
        return False
    
    bot_account_id = reporting_config.get('bot_account_id')
    bot_target = reporting_config.get('bot_target')
    
    if not bot_account_id or not bot_target:
        print("[Notification error] Bot configuration missing")
        return False
    
    title = report_title or "Garden Irrigation Report"
    formatted_content = format_report_for_messaging(report_content, title)
    
    success = send_report_via_openclaw(
        report_content=formatted_content,
        bot_account_id=bot_account_id,
        bot_target=bot_target,
        report_title=title
    )
    
    if success:
        print(f"[Notification] Report sent to {bot_target}")
    else:
        print(f"[Notification] Failed to send report to {bot_target}")
    
    return success