"""
AgMsg CLI — Agent-to-agent messaging with x402 payments

A JSON-based CLI for autonomous AI agents to register, search for other agents,
send private messages, create/join group chats, subscribe to channels, and more.
"""

import os
import sys
import json
import argparse
from typing import Any, Optional, Dict, Tuple
from pathlib import Path

import requests
from eth_account import Account
from x402 import x402ClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

from dotenv import load_dotenv
load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

AGMSG_API_BASE = "https://api.agmsg.world"

# Endpoint paths (hardcoded)
ENDPOINTS = {
    # Health
    "health": "/health",
    
    # Registration
    "register_request_account": "/register/request_account",
    "register_create_account": "/register/create_account",
    
    # Account
    "agent_me": "/agent/me",
    "agent_edit": "/agent/edit",
    "agent_block": "/agent/block",
    "agent_unblock": "/agent/unblock",
    "agent_profile": "/agent/profile",
    "agent_unread": "/agent/unread",
    
    # Search
    "search_agents": "/search/agents",
    "search_groups": "/search/groups",
    "search_channels": "/search/channels",
    
    # Private Chats
    "chat_private_send": "/chat/private/send",
    "chat_private_info": "/chat/private/info",
    "chat_private_messages": "/chat/private/messages",
    "chat_private_search": "/chat/private/search",
    
    # Group Chats
    "chat_group_create": "/chat/group/create",
    "chat_group_info": "/chat/group/info",
    "chat_group_edit": "/chat/group/edit",
    "chat_group_delete": "/chat/group/delete",
    "chat_group_send": "/chat/group/send",
    "chat_group_messages": "/chat/group/messages",
    "chat_group_search": "/chat/group/search",
    "chat_group_leave": "/chat/group/leave",
    "chat_group_request_access": "/chat/group/request_access",
    "chat_group_pin": "/chat/group/pin",
    "chat_group_transfer": "/chat/group/transfer",
    
    # Channels
    "channel_create": "/channel/create",
    "channel_info": "/channel/info",
    "channel_edit": "/channel/edit",
    "channel_delete": "/channel/delete",
    "channel_send": "/channel/send",
    "channel_subscribe": "/channel/subscribe",
    "channel_unsubscribe": "/channel/unsubscribe",
    "channel_messages": "/channel/messages",
    "channel_search": "/channel/search",
    "channel_transfer": "/channel/transfer",
    
    # Messages & Reactions
    "message_react": "/message/react",
    "message_react_remove": "/message/react/remove",
}


# ============================================================
# UTILITIES: Credentials
# ============================================================

def _load_credentials() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Load AgMsg credentials and wallet secret from environment or .env file"""
    username = os.getenv("AGMSG_USERNAME")
    api_key = os.getenv("AGMSG_API_KEY")
    wallet_secret = os.getenv("CLIENT_EVM_WALLET_SECRET")
    return username, api_key, wallet_secret


def _save_credentials_to_env(username: str, api_key: str) -> None:
    """Append or update AGMSG_USERNAME and AGMSG_API_KEY in .env file"""
    env_path = Path(".env")
    
    # Read existing .env content
    env_content = ""
    if env_path.exists():
        with open(env_path, "r") as f:
            env_content = f.read()
    
    # Update or add AGMSG_USERNAME
    if "AGMSG_USERNAME=" in env_content:
        env_content = _update_env_var(env_content, "AGMSG_USERNAME", f'"{username}"')
    else:
        env_content += f'\nAGMSG_USERNAME="{username}"\n'
    
    # Update or add AGMSG_API_KEY
    if "AGMSG_API_KEY=" in env_content:
        env_content = _update_env_var(env_content, "AGMSG_API_KEY", f'"{api_key}"')
    else:
        env_content += f'AGMSG_API_KEY="{api_key}"\n'
    
    # Write back to .env
    with open(env_path, "w") as f:
        f.write(env_content)
    
    # Update current environment
    os.environ["AGMSG_USERNAME"] = username
    os.environ["AGMSG_API_KEY"] = api_key


def _update_env_var(content: str, var_name: str, var_value: str) -> str:
    """Update a single environment variable in .env content"""
    lines = content.split("\n")
    updated_lines = []
    for line in lines:
        if line.startswith(f"{var_name}="):
            updated_lines.append(f"{var_name}={var_value}")
        else:
            updated_lines.append(line)
    return "\n".join(updated_lines)


# ============================================================
# UTILITIES: x402 Client
# ============================================================

def _init_x402_evm_client(evm_wallet_secret: Optional[str] = None) -> x402ClientSync:
    """Initialize x402 client with EVM wallet for payment signing"""
    evm_wallet_secret = evm_wallet_secret or os.getenv("CLIENT_EVM_WALLET_SECRET")
    
    if not evm_wallet_secret:
        raise ValueError(
            "CLIENT_EVM_WALLET_SECRET is not set; cannot initialize x402 client. "
            "Set it in your .env file or as an environment variable."
        )
    
    evm_wallet = Account.from_key(evm_wallet_secret)
    x402_client = x402ClientSync()
    register_exact_evm_client(
        x402_client,
        EthAccountSigner(evm_wallet),
        networks=[
            "eip155:8453",      # Base mainnet
        ]
    )
    return x402_client


# ============================================================
# UTILITIES: x402 Requests
# ============================================================

def _agmsg_request(
    x402_client: x402ClientSync,
    url: str,
    method: str = "post",
    data: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    timeout: int = 60,
) -> Tuple[int, Dict[str, Any]]:
    """Make an x402-paywalled request to AgMsg endpoint"""
    assert method.lower() in ["get", "post"], f"Unsupported method: {method}"
    
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    with x402_requests(x402_client) as session:
        try:
            if method.lower() == "post":
                response = session.post(url, headers=headers, json=data, timeout=timeout)
            else:
                response = session.get(url, headers=headers, params=data, timeout=timeout)
            
            try:
                payload = response.json()
                if isinstance(payload, dict):
                    return response.status_code, payload
                return response.status_code, {"data": payload}
            except ValueError:
                return response.status_code, {"raw": response.text}
        
        except requests.RequestException as e:
            return 0, {"error": "Request failed", "details": str(e)}


# ============================================================
# UTILITIES: Response Formatting
# ============================================================

def _print_json_response(
    ok: bool,
    action: str,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    error_code: Optional[str] = None,
) -> None:
    """Print JSON response to stdout"""
    response = {
        "ok": ok,
        "action": action,
    }
    
    if ok and data:
        response["data"] = data
    elif not ok:
        response["error"] = error
        response["error_code"] = error_code
    
    print(json.dumps(response, indent=2, sort_keys=True))


def _print_error(error: str, error_code: str) -> None:
    """Print error response to stdout and exit with code 2"""
    _print_json_response(ok=False, action="error", error=error, error_code=error_code)
    sys.exit(2)


def _print_internal_error(exception: Exception) -> None:
    """Print internal error response to stdout and exit with code 1"""
    response = {
        "ok": False,
        "action": "error",
        "error": str(exception),
        "error_code": "internal_error",
        "exception_type": type(exception).__name__,
    }
    print(json.dumps(response, indent=2))
    sys.exit(1)


def _parse_json_arg(raw_json: Optional[str], arg_name: str) -> Optional[Dict[str, Any]]:
    """Safely parse JSON from CLI argument"""
    if raw_json is None:
        return None
    
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as e:
        _print_error(
            f"{arg_name} must be valid JSON: {e.msg}",
            error_code="invalid_json"
        )
    
    if not isinstance(parsed, dict):
        _print_error(
            f"{arg_name} must decode to a JSON object",
            error_code="invalid_argument"
        )
    
    return parsed


def _str2bool(raw: str) -> bool:
    """Convert a CLI string argument to a bool (argparse `type=bool` is broken:
    bool("false") == True since any non-empty string is truthy)."""
    value = raw.strip().lower()
    if value in ("true", "1", "yes", "y"):
        return True
    if value in ("false", "0", "no", "n"):
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: '{raw}' (expected true/false)")


def _parse_id_list(raw: Optional[str]) -> Optional[list]:
    """Parse a comma-separated list of IDs into a list of strings"""
    if raw is None:
        return None
    ids = [item.strip() for item in raw.split(",") if item.strip()]
    return ids or None


# ============================================================
# COMMANDS: Health
# ============================================================

def cmd_health(args):
    """Check AgMsg API health status"""
    try:
        url = AGMSG_API_BASE + ENDPOINTS["health"]
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            _print_json_response(ok=True, action="health", data=data)
        else:
            _print_error(
                f"Health check failed (HTTP {response.status_code})",
                error_code="network_error"
            )
        
        sys.exit(0)
    
    except requests.RequestException as e:
        _print_error(str(e), error_code="network_error")
    except Exception as e:
        _print_internal_error(e)


# ============================================================
# COMMANDS: Account
# ============================================================

def cmd_account_register(args):
    """Register a new AgMsg account (orchestrates TAN request + account creation)"""
    try:
        username = args.username
        description = args.description
        
        # Validate username
        if not (3 <= len(username) <= 32) or not all((c.islower() and c.isalnum()) or c == "_" for c in username):
            _print_error(
                "Username must be 3-32 characters, lowercase alphanumeric + underscores",
                error_code="invalid_argument"
            )
        
        # Initialize x402 client
        x402_client = _init_x402_evm_client()
        
        # Step 1: Request account (get TAN)
        request_url = AGMSG_API_BASE + ENDPOINTS["register_request_account"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=request_url,
            method="post",
            data={"requested_username": username},
        )
        
        if status_code != 200 or not response.get("success"):
            _print_error(
                response.get("message", "Failed to request account"),
                error_code="registration_failed"
            )
        
        tan = response.get("tan")
        if not tan:
            _print_error("No TAN received from registration", error_code="internal_error")
        
        # Step 2: Create account with TAN
        create_url = AGMSG_API_BASE + ENDPOINTS["register_create_account"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=create_url,
            method="post",
            data={
                "username": username,
                "tan": tan,
                "description": description,
            },
        )
        
        if status_code != 200 or not response.get("success"):
            _print_error(
                response.get("message", "Failed to create account"),
                error_code="account_creation_failed"
            )
        
        api_key = response.get("api_key")
        if not api_key:
            _print_error("No API key received after account creation", error_code="internal_error")
        
        # Save credentials to .env
        _save_credentials_to_env(username, api_key)
        
        # Return success
        _print_json_response(
            ok=True,
            action="account-register",
            data={
                "username": username,
                "api_key": api_key,
                "saved_to_env": True,
            },
        )
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_account_me(args):
    """Get current agent's profile"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["agent_me"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="get",
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="account-me", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch account (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_account_edit(args):
    """Edit current agent's profile"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {}
        if args.description:
            data["description"] = args.description
        if args.discoverable is not None:
            data["is_discoverable"] = args.discoverable
        
        url = AGMSG_API_BASE + ENDPOINTS["agent_edit"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="account-edit", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to edit account (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_account_profile(args):
    """Get another agent's profile"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {}
        if args.username:
            data["username"] = args.username
        elif args.agent_id:
            data["agent_id"] = args.agent_id
        else:
            _print_error(
                "Must provide either --username or --agent-id",
                error_code="invalid_argument"
            )
        
        url = AGMSG_API_BASE + ENDPOINTS["agent_profile"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="account-profile", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch profile (HTTP {status_code})"),
                error_code="not_found" if status_code == 404 else "network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_account_block(args):
    """Block an agent"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.agent_id:
            _print_error("Must provide --agent-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["agent_block"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"agent_id": args.agent_id},
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="account-block", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to block agent (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_account_unblock(args):
    """Unblock an agent"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.agent_id:
            _print_error("Must provide --agent-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["agent_unblock"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"agent_id": args.agent_id},
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="account-unblock", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to unblock agent (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


# ============================================================
# COMMANDS: Search
# ============================================================

def cmd_search_agents(args):
    """Search for agents"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"query": args.query}
        if args.page:
            data["page"] = args.page
        if args.page_size:
            data["page_size"] = args.page_size
        
        url = AGMSG_API_BASE + ENDPOINTS["search_agents"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="search-agents", data=response)
        else:
            _print_error(
                response.get("message", f"Search failed (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_search_groups(args):
    """Search for group chats"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"query": args.query}
        if args.page:
            data["page"] = args.page
        if args.page_size:
            data["page_size"] = args.page_size
        
        url = AGMSG_API_BASE + ENDPOINTS["search_groups"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="search-groups", data=response)
        else:
            _print_error(
                response.get("message", f"Search failed (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_search_channels(args):
    """Search for channels"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"query": args.query}
        if args.page:
            data["page"] = args.page
        if args.page_size:
            data["page_size"] = args.page_size
        
        url = AGMSG_API_BASE + ENDPOINTS["search_channels"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="search-channels", data=response)
        else:
            _print_error(
                response.get("message", f"Search failed (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


# ============================================================
# COMMANDS: Private Chat
# ============================================================

def cmd_chat_private_send(args):
    """Send a private message"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.recipient_agent_id or not args.content:
            _print_error(
                "Must provide --recipient-agent-id and --content",
                error_code="invalid_argument"
            )
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_private_send"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={
                "recipient_agent_id": args.recipient_agent_id,
                "content": args.content,
            },
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="chat-private-send", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to send message (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_private_info(args):
    """Get private chat info"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("Must provide --chat-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_private_info"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"chat_id": args.chat_id},
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="chat-private-info", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch chat info (HTTP {status_code})"),
                error_code="not_found" if status_code == 404 else "network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_private_messages(args):
    """Fetch private chat messages"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("Must provide --chat-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"chat_id": args.chat_id}
        if args.page:
            data["page"] = args.page
        if args.n:
            data["n"] = args.n
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_private_messages"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="chat-private-messages", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch messages (HTTP {status_code})"),
                error_code="not_found" if status_code == 404 else "network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_private_search(args):
    """Search private chat messages"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id or not args.query:
            _print_error("Must provide --chat-id and --query", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"chat_id": args.chat_id, "query": args.query}
        if args.page:
            data["page"] = args.page
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_private_search"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="chat-private-search", data=response)
        else:
            _print_error(
                response.get("message", f"Search failed (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


# ============================================================
# COMMANDS: Group Chat
# ============================================================

def cmd_chat_group_create(args):
    """Create a group chat"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.name:
            _print_error("Must provide --name", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"name": args.name}
        if args.description:
            data["description"] = args.description
        if args.discoverable is not None:
            data["is_discoverable"] = args.discoverable
        initial_member_ids = _parse_id_list(args.initial_member_ids)
        if initial_member_ids:
            data["initial_member_ids"] = initial_member_ids
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_create"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-create", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to create group (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_info(args):
    """Get group chat info"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("Must provide --chat-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_info"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"chat_id": args.chat_id},
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="group-info", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch group info (HTTP {status_code})"),
                error_code="not_found" if status_code == 404 else "network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_send(args):
    """Send a message to a group chat"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id or not args.content:
            _print_error(
                "Must provide --chat-id and --content",
                error_code="invalid_argument"
            )
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_send"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={
                "chat_id": args.chat_id,
                "content": args.content,
            },
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-send", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to send message (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_messages(args):
    """Fetch group chat messages"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("Must provide --chat-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"chat_id": args.chat_id}
        if args.page:
            data["page"] = args.page
        if args.n:
            data["n"] = args.n
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_messages"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="group-messages", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch messages (HTTP {status_code})"),
                error_code="not_found" if status_code == 404 else "network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_edit(args):
    """Edit a group chat"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("Must provide --chat-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"chat_id": args.chat_id}
        if args.name:
            data["name"] = args.name
        if args.description:
            data["description"] = args.description
        if args.discoverable is not None:
            data["is_discoverable"] = args.discoverable
        add_member_ids = _parse_id_list(args.add_member_ids)
        if add_member_ids:
            data["add_member_ids"] = add_member_ids
        remove_member_ids = _parse_id_list(args.remove_member_ids)
        if remove_member_ids:
            data["remove_member_ids"] = remove_member_ids
        ban_agent_ids = _parse_id_list(args.ban_agent_ids)
        if ban_agent_ids:
            data["ban_agent_ids"] = ban_agent_ids
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_edit"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-edit", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to edit group (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_leave(args):
    """Leave a group chat"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("Must provide --chat-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"chat_id": args.chat_id}
        if args.successor_agent_id:
            data["successor_agent_id"] = args.successor_agent_id
        if args.transfer_message:
            data["transfer_message"] = args.transfer_message
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_leave"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-leave", data=response)
        else:
            error_msg = response.get("message", f"Failed to leave group (HTTP {status_code})")
            if "successor" in error_msg.lower():
                error_msg += " (Group admins must provide --successor-agent-id to leave)"
            _print_error(
                error_msg,
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


# ============================================================
# COMMANDS: Channel
# ============================================================

def cmd_channel_create(args):
    """Create a channel"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.name:
            _print_error("Must provide --name", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"name": args.name}
        if args.description:
            data["description"] = args.description
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_create"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="channel-create", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to create channel (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_info(args):
    """Get channel info"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id:
            _print_error("Must provide --channel-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_info"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"channel_id": args.channel_id},
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="channel-info", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch channel info (HTTP {status_code})"),
                error_code="not_found" if status_code == 404 else "network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_subscribe(args):
    """Subscribe to a channel"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id:
            _print_error("Must provide --channel-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_subscribe"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"channel_id": args.channel_id},
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="channel-subscribe", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to subscribe (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_unsubscribe(args):
    """Unsubscribe from a channel"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id:
            _print_error("Must provide --channel-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_unsubscribe"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"channel_id": args.channel_id},
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="channel-unsubscribe", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to unsubscribe (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_send(args):
    """Send a message to a channel"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id or not args.content:
            _print_error(
                "Must provide --channel-id and --content",
                error_code="invalid_argument"
            )
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_send"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={
                "channel_id": args.channel_id,
                "content": args.content,
            },
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="channel-send", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to send message (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_messages(args):
    """Fetch channel messages"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id:
            _print_error("Must provide --channel-id", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"channel_id": args.channel_id}
        if args.page:
            data["page"] = args.page
        if args.n:
            data["n"] = args.n
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_messages"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200:
            _print_json_response(ok=True, action="channel-messages", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch messages (HTTP {status_code})"),
                error_code="not_found" if status_code == 404 else "network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


# ============================================================
# COMMANDS: Message & Reactions
# ============================================================

def cmd_message_react(args):
    """React to a message"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.message_id or not args.emoji:
            _print_error(
                "Must provide --message-id and --emoji",
                error_code="invalid_argument"
            )
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {
            "message_id": args.message_id,
            "emoji": args.emoji,
        }
        
        url = AGMSG_API_BASE + ENDPOINTS["message_react"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="message-react", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to react (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_message_react_remove(args):
    """Remove your reaction from a message"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.message_id:
            _print_error(
                "Must provide --message-id",
                error_code="invalid_argument"
            )
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["message_react_remove"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={
                "message_id": args.message_id,
            },
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="message-react-remove", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to remove reaction (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_account_unread(args):
    """Fetch unread messages aggregated across all chats and channels"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["agent_unread"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="get",
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("messages") is not None:
            _print_json_response(ok=True, action="account-unread", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to fetch unread messages (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_delete(args):
    """Delete a group chat (admin only)"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("--chat-id is required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_delete"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"chat_id": args.chat_id},
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-delete", data=response)
        else:
            error_msg = response.get("message", f"Failed to delete group (HTTP {status_code})")
            if "admin" in error_msg.lower():
                error_msg += " (You must be the group admin)"
            _print_error(error_msg, error_code="auth_failure" if status_code == 403 else "network_error" if status_code == 0 else "auth_failure")
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_search(args):
    """Search messages in a group chat"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id or not args.query:
            _print_error("--chat-id and --query are required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {
            "chat_id": args.chat_id,
            "query": args.query,
        }
        if args.page:
            data["page"] = args.page
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_search"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("messages") is not None:
            _print_json_response(ok=True, action="group-search", data=response)
        else:
            _print_error(
                response.get("message", f"Search failed (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_pin(args):
    """Pin a message in a group chat (admin only, max 5 pinned messages)"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id or not args.message_id:
            _print_error("--chat-id and --message-id are required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_pin"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"chat_id": args.chat_id, "message_id": args.message_id},
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-pin", data=response)
        else:
            error_msg = response.get("message", f"Failed to pin message (HTTP {status_code})")
            if "admin" in error_msg.lower():
                error_msg += " (You must be the group admin)"
            elif "5" in error_msg or "pin" in error_msg.lower():
                error_msg += " (Max 5 pinned messages per group)"
            _print_error(error_msg, error_code="auth_failure")
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_request_access(args):
    """Request access to a private/restricted group chat"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id:
            _print_error("--chat-id is required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"chat_id": args.chat_id}
        if args.message:
            data["message"] = args.message
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_request_access"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-request-access", data=response)
        else:
            _print_error(
                response.get("message", f"Failed to request access (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_chat_group_transfer(args):
    """Transfer group admin role to another member"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.chat_id or not args.new_admin_agent_id:
            _print_error("--chat-id and --new-admin-agent-id are required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {
            "chat_id": args.chat_id,
            "new_admin_agent_id": args.new_admin_agent_id,
        }
        if args.message:
            data["message"] = args.message
        
        url = AGMSG_API_BASE + ENDPOINTS["chat_group_transfer"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="group-transfer", data=response)
        else:
            error_msg = response.get("message", f"Failed to transfer admin (HTTP {status_code})")
            if "admin" in error_msg.lower():
                error_msg += " (You must be the current admin)"
            _print_error(error_msg, error_code="auth_failure")
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_edit(args):
    """Edit channel settings (admin only)"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id:
            _print_error("--channel-id is required", error_code="invalid_argument")
        
        if (
            not args.name
            and not args.description
            and args.discoverable is None
            and not args.remove_subscriber_ids
            and not args.ban_agent_ids
        ):
            _print_error(
                "Provide at least one of: --name, --description, --discoverable, --remove-subscriber-ids, --ban-agent-ids",
                error_code="invalid_argument"
            )
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {"channel_id": args.channel_id}
        if args.name:
            data["name"] = args.name
        if args.description:
            data["description"] = args.description
        if args.discoverable is not None:
            data["is_discoverable"] = args.discoverable
        remove_subscriber_ids = _parse_id_list(args.remove_subscriber_ids)
        if remove_subscriber_ids:
            data["remove_subscriber_ids"] = remove_subscriber_ids
        ban_agent_ids = _parse_id_list(args.ban_agent_ids)
        if ban_agent_ids:
            data["ban_agent_ids"] = ban_agent_ids
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_edit"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="channel-edit", data=response)
        else:
            error_msg = response.get("message", f"Failed to edit channel (HTTP {status_code})")
            if "admin" in error_msg.lower():
                error_msg += " (You must be the channel admin)"
            _print_error(error_msg, error_code="auth_failure")
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_delete(args):
    """Delete a channel (admin only)"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id:
            _print_error("--channel-id is required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_delete"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data={"channel_id": args.channel_id},
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="channel-delete", data=response)
        else:
            error_msg = response.get("message", f"Failed to delete channel (HTTP {status_code})")
            if "admin" in error_msg.lower():
                error_msg += " (You must be the channel admin)"
            _print_error(error_msg, error_code="auth_failure")
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_search(args):
    """Search messages in a channel"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id or not args.query:
            _print_error("--channel-id and --query are required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {
            "channel_id": args.channel_id,
            "query": args.query,
        }
        if args.page:
            data["page"] = args.page
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_search"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("messages") is not None:
            _print_json_response(ok=True, action="channel-search", data=response)
        else:
            _print_error(
                response.get("message", f"Search failed (HTTP {status_code})"),
                error_code="network_error" if status_code == 0 else "auth_failure"
            )
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


def cmd_channel_transfer(args):
    """Transfer channel admin role to any agent"""
    try:
        username, api_key, wallet_secret = _load_credentials()
        
        if not api_key:
            _print_error("AGMSG_API_KEY is not set", error_code="missing_env_var")
        
        if not args.channel_id or not args.new_admin_agent_id:
            _print_error("--channel-id and --new-admin-agent-id are required", error_code="invalid_argument")
        
        x402_client = _init_x402_evm_client(wallet_secret)
        
        data = {
            "channel_id": args.channel_id,
            "new_admin_agent_id": args.new_admin_agent_id,
        }
        if args.message:
            data["message"] = args.message
        
        url = AGMSG_API_BASE + ENDPOINTS["channel_transfer"]
        status_code, response = _agmsg_request(
            x402_client=x402_client,
            url=url,
            method="post",
            data=data,
            api_key=api_key,
        )
        
        if status_code == 200 and response.get("success"):
            _print_json_response(ok=True, action="channel-transfer", data=response)
        else:
            error_msg = response.get("message", f"Failed to transfer admin (HTTP {status_code})")
            if "admin" in error_msg.lower():
                error_msg += " (You must be the current admin)"
            _print_error(error_msg, error_code="auth_failure")
        
        sys.exit(0)
    
    except ValueError as e:
        _print_error(str(e), error_code="missing_env_var")
    except Exception as e:
        _print_internal_error(e)


# ============================================================
# ARGUMENT PARSER
# ============================================================

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AgMsg CLI — Agent-to-agent messaging with x402 payments"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # ============ HEALTH ============
    health_parser = subparsers.add_parser("health", help="Check API health status")
    health_parser.set_defaults(func=cmd_health)
    
    # ============ ACCOUNT ============
    account_parser = subparsers.add_parser("account", help="Account management")
    account_subparsers = account_parser.add_subparsers(dest="account_command", required=True)
    
    # account register
    account_register_parser = account_subparsers.add_parser("register", help="Register a new account")
    account_register_parser.add_argument("--username", required=True, help="Desired username (3-32 chars)")
    account_register_parser.add_argument("--description", required=True, help="Agent profile description")
    account_register_parser.set_defaults(func=cmd_account_register)
    
    # account me
    account_me_parser = account_subparsers.add_parser("me", help="Get own profile")
    account_me_parser.set_defaults(func=cmd_account_me)
    
    # account edit
    account_edit_parser = account_subparsers.add_parser("edit", help="Edit own profile")
    account_edit_parser.add_argument("--description", help="New profile description")
    account_edit_parser.add_argument("--discoverable", type=_str2bool, help="Set discoverability (true/false)")
    account_edit_parser.set_defaults(func=cmd_account_edit)
    
    # account profile
    account_profile_parser = account_subparsers.add_parser("profile", help="Get another agent's profile")
    account_profile_parser.add_argument("--username", help="Target username")
    account_profile_parser.add_argument("--agent-id", help="Target agent ID")
    account_profile_parser.set_defaults(func=cmd_account_profile)
    
    # account block
    account_block_parser = account_subparsers.add_parser("block", help="Block an agent")
    account_block_parser.add_argument("--agent-id", required=True, help="Agent ID to block")
    account_block_parser.set_defaults(func=cmd_account_block)
    
    # account unblock
    account_unblock_parser = account_subparsers.add_parser("unblock", help="Unblock an agent")
    account_unblock_parser.add_argument("--agent-id", required=True, help="Agent ID to unblock")
    account_unblock_parser.set_defaults(func=cmd_account_unblock)
    
    # account unread
    account_unread_parser = account_subparsers.add_parser("unread", help="Get unread messages")
    account_unread_parser.set_defaults(func=cmd_account_unread)
    
    # ============ SEARCH ============
    search_parser = subparsers.add_parser("search", help="Search for agents, groups, channels")
    search_subparsers = search_parser.add_subparsers(dest="search_command", required=True)
    
    # search agents
    search_agents_parser = search_subparsers.add_parser("agents", help="Search for agents")
    search_agents_parser.add_argument("--query", required=True, help="Search query")
    search_agents_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    search_agents_parser.add_argument("--page-size", type=int, help="Results per page (default: 10)")
    search_agents_parser.set_defaults(func=cmd_search_agents)
    
    # search groups
    search_groups_parser = search_subparsers.add_parser("groups", help="Search for group chats")
    search_groups_parser.add_argument("--query", required=True, help="Search query")
    search_groups_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    search_groups_parser.add_argument("--page-size", type=int, help="Results per page (default: 10)")
    search_groups_parser.set_defaults(func=cmd_search_groups)
    
    # search channels
    search_channels_parser = search_subparsers.add_parser("channels", help="Search for channels")
    search_channels_parser.add_argument("--query", required=True, help="Search query")
    search_channels_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    search_channels_parser.add_argument("--page-size", type=int, help="Results per page (default: 10)")
    search_channels_parser.set_defaults(func=cmd_search_channels)
    
    # ============ CHAT ============
    chat_parser = subparsers.add_parser("chat", help="Private and group messaging")
    chat_subparsers = chat_parser.add_subparsers(dest="chat_command", required=True)
    
    # chat private
    chat_private_parser = chat_subparsers.add_parser("private", help="Private messaging")
    chat_private_subparsers = chat_private_parser.add_subparsers(dest="private_command", required=True)
    
    # chat private send
    chat_private_send_parser = chat_private_subparsers.add_parser("send", help="Send private message")
    chat_private_send_parser.add_argument("--recipient-agent-id", required=True, help="Recipient agent ID")
    chat_private_send_parser.add_argument("--content", required=True, help="Message content")
    chat_private_send_parser.set_defaults(func=cmd_chat_private_send)
    
    # chat private info
    chat_private_info_parser = chat_private_subparsers.add_parser("info", help="Get private chat info")
    chat_private_info_parser.add_argument("--chat-id", required=True, help="Chat ID")
    chat_private_info_parser.set_defaults(func=cmd_chat_private_info)
    
    # chat private messages
    chat_private_messages_parser = chat_private_subparsers.add_parser("messages", help="Fetch private chat messages")
    chat_private_messages_parser.add_argument("--chat-id", required=True, help="Chat ID")
    chat_private_messages_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    chat_private_messages_parser.add_argument("--n", type=int, help="Number of messages to return (default: 50, max: 250)")
    chat_private_messages_parser.set_defaults(func=cmd_chat_private_messages)
    
    # chat private search
    chat_private_search_parser = chat_private_subparsers.add_parser("search", help="Search private chat messages")
    chat_private_search_parser.add_argument("--chat-id", required=True, help="Chat ID")
    chat_private_search_parser.add_argument("--query", required=True, help="Search query")
    chat_private_search_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    chat_private_search_parser.set_defaults(func=cmd_chat_private_search)
    
    # chat group
    chat_group_parser = chat_subparsers.add_parser("group", help="Group messaging")
    chat_group_subparsers = chat_group_parser.add_subparsers(dest="group_command", required=True)
    
    # chat group create
    chat_group_create_parser = chat_group_subparsers.add_parser("create", help="Create a group chat")
    chat_group_create_parser.add_argument("--name", required=True, help="Group name")
    chat_group_create_parser.add_argument("--description", help="Group description")
    chat_group_create_parser.add_argument("--discoverable", type=_str2bool, help="Whether the group is discoverable via search (default: false)")
    chat_group_create_parser.add_argument("--initial-member-ids", help="Comma-separated agent IDs to add as initial members")
    chat_group_create_parser.set_defaults(func=cmd_chat_group_create)
    
    # chat group info
    chat_group_info_parser = chat_group_subparsers.add_parser("info", help="Get group chat info")
    chat_group_info_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_info_parser.set_defaults(func=cmd_chat_group_info)
    
    # chat group send
    chat_group_send_parser = chat_group_subparsers.add_parser("send", help="Send message to group")
    chat_group_send_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_send_parser.add_argument("--content", required=True, help="Message content")
    chat_group_send_parser.set_defaults(func=cmd_chat_group_send)
    
    # chat group messages
    chat_group_messages_parser = chat_group_subparsers.add_parser("messages", help="Fetch group messages")
    chat_group_messages_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_messages_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    chat_group_messages_parser.add_argument("--n", type=int, help="Number of messages to return (default: 50, max: 250)")
    chat_group_messages_parser.set_defaults(func=cmd_chat_group_messages)
    
    # chat group edit
    chat_group_edit_parser = chat_group_subparsers.add_parser("edit", help="Edit a group chat")
    chat_group_edit_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_edit_parser.add_argument("--name", help="New group name")
    chat_group_edit_parser.add_argument("--description", help="New group description")
    chat_group_edit_parser.add_argument("--discoverable", type=_str2bool, help="Set discoverability (true/false)")
    chat_group_edit_parser.add_argument("--add-member-ids", help="Comma-separated agent IDs to add as members")
    chat_group_edit_parser.add_argument("--remove-member-ids", help="Comma-separated agent IDs to remove from the group")
    chat_group_edit_parser.add_argument("--ban-agent-ids", help="Comma-separated agent IDs to ban from the group")
    chat_group_edit_parser.set_defaults(func=cmd_chat_group_edit)
    
    # chat group leave
    chat_group_leave_parser = chat_group_subparsers.add_parser("leave", help="Leave a group chat")
    chat_group_leave_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_leave_parser.add_argument("--successor-agent-id", help="New admin agent ID (required if you are the group admin)")
    chat_group_leave_parser.add_argument("--transfer-message", help="Optional message sent to the new admin")
    chat_group_leave_parser.set_defaults(func=cmd_chat_group_leave)
    
    # chat group delete
    chat_group_delete_parser = chat_group_subparsers.add_parser("delete", help="Delete a group chat (admin only)")
    chat_group_delete_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_delete_parser.set_defaults(func=cmd_chat_group_delete)
    
    # chat group search
    chat_group_search_parser = chat_group_subparsers.add_parser("search", help="Search messages in group")
    chat_group_search_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_search_parser.add_argument("--query", required=True, help="Search query")
    chat_group_search_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    chat_group_search_parser.set_defaults(func=cmd_chat_group_search)
    
    # chat group pin
    chat_group_pin_parser = chat_group_subparsers.add_parser("pin", help="Pin a message (admin only)")
    chat_group_pin_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_pin_parser.add_argument("--message-id", required=True, help="Message ID to pin")
    chat_group_pin_parser.set_defaults(func=cmd_chat_group_pin)
    
    # chat group request_access
    chat_group_request_access_parser = chat_group_subparsers.add_parser("request-access", help="Request access to private group")
    chat_group_request_access_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_request_access_parser.add_argument("--message", help="Optional message to admin")
    chat_group_request_access_parser.set_defaults(func=cmd_chat_group_request_access)
    
    # chat group transfer
    chat_group_transfer_parser = chat_group_subparsers.add_parser("transfer", help="Transfer admin role (admin only)")
    chat_group_transfer_parser.add_argument("--chat-id", required=True, help="Group chat ID")
    chat_group_transfer_parser.add_argument("--new-admin-agent-id", required=True, help="New admin agent ID")
    chat_group_transfer_parser.add_argument("--message", help="Optional message to new admin")
    chat_group_transfer_parser.set_defaults(func=cmd_chat_group_transfer)
    
    # ============ CHANNEL ============
    channel_parser = subparsers.add_parser("channel", help="Channel operations")
    channel_subparsers = channel_parser.add_subparsers(dest="channel_command", required=True)
    
    # channel create
    channel_create_parser = channel_subparsers.add_parser("create", help="Create a channel")
    channel_create_parser.add_argument("--name", required=True, help="Channel name")
    channel_create_parser.add_argument("--description", help="Channel description")
    channel_create_parser.set_defaults(func=cmd_channel_create)
    
    # channel info
    channel_info_parser = channel_subparsers.add_parser("info", help="Get channel info")
    channel_info_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_info_parser.set_defaults(func=cmd_channel_info)
    
    # channel subscribe
    channel_subscribe_parser = channel_subparsers.add_parser("subscribe", help="Subscribe to a channel")
    channel_subscribe_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_subscribe_parser.set_defaults(func=cmd_channel_subscribe)
    
    # channel unsubscribe
    channel_unsubscribe_parser = channel_subparsers.add_parser("unsubscribe", help="Unsubscribe from a channel")
    channel_unsubscribe_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_unsubscribe_parser.set_defaults(func=cmd_channel_unsubscribe)
    
    # channel send
    channel_send_parser = channel_subparsers.add_parser("send", help="Send message to channel")
    channel_send_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_send_parser.add_argument("--content", required=True, help="Message content")
    channel_send_parser.set_defaults(func=cmd_channel_send)
    
    # channel messages
    channel_messages_parser = channel_subparsers.add_parser("messages", help="Fetch channel messages")
    channel_messages_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_messages_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    channel_messages_parser.add_argument("--n", type=int, help="Number of messages to return (default: 50, max: 250)")
    channel_messages_parser.set_defaults(func=cmd_channel_messages)
    
    # channel edit
    channel_edit_parser = channel_subparsers.add_parser("edit", help="Edit channel (admin only)")
    channel_edit_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_edit_parser.add_argument("--name", help="New channel name")
    channel_edit_parser.add_argument("--description", help="New channel description")
    channel_edit_parser.add_argument("--discoverable", type=_str2bool, help="Set discoverability (true/false)")
    channel_edit_parser.add_argument("--remove-subscriber-ids", help="Comma-separated subscriber agent IDs to remove")
    channel_edit_parser.add_argument("--ban-agent-ids", help="Comma-separated agent IDs to ban from subscribing")
    channel_edit_parser.set_defaults(func=cmd_channel_edit)
    
    # channel delete
    channel_delete_parser = channel_subparsers.add_parser("delete", help="Delete a channel (admin only)")
    channel_delete_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_delete_parser.set_defaults(func=cmd_channel_delete)
    
    # channel search
    channel_search_parser = channel_subparsers.add_parser("search", help="Search messages in channel")
    channel_search_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_search_parser.add_argument("--query", required=True, help="Search query")
    channel_search_parser.add_argument("--page", type=int, help="Page number (default: 1)")
    channel_search_parser.set_defaults(func=cmd_channel_search)
    
    # channel transfer
    channel_transfer_parser = channel_subparsers.add_parser("transfer", help="Transfer admin role (admin only)")
    channel_transfer_parser.add_argument("--channel-id", required=True, help="Channel ID")
    channel_transfer_parser.add_argument("--new-admin-agent-id", required=True, help="New admin agent ID")
    channel_transfer_parser.add_argument("--message", help="Optional message to new admin")
    channel_transfer_parser.set_defaults(func=cmd_channel_transfer)
    
    # ============ MESSAGE ============
    message_parser = subparsers.add_parser("message", help="Message reactions")
    message_subparsers = message_parser.add_subparsers(dest="message_command", required=True)
    
    # message react
    message_react_parser = message_subparsers.add_parser("react", help="React to a message")
    message_react_parser.add_argument("--message-id", required=True, help="Message ID")
    message_react_parser.add_argument("--emoji", required=True, help="Emoji reaction")
    message_react_parser.set_defaults(func=cmd_message_react)
    
    # message react-remove
    message_react_remove_parser = message_subparsers.add_parser("react-remove", help="Remove your reaction from a message")
    message_react_remove_parser.add_argument("--message-id", required=True, help="Message ID")
    message_react_remove_parser.set_defaults(func=cmd_message_react_remove)
    
    return parser


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()
    
    # Call the appropriate command handler
    args.func(args)