"""Enhanced ClawNews command handlers with improved error handling and validation.

This module provides hardened versions of ClawNews commands with:
- Comprehensive input validation
- Better error handling and reporting
- Deterministic output formatting
- Backward compatibility preservation
- Request/response logging for debugging
"""

import argparse
import json
import sys
import time
from typing import Any, Dict, Optional, Union

from .cli import (_cfg_get, _maybe_udp_emit, append_jsonl, load_config)
from .transports.clawnews import ClawNewsClient, ClawNewsError


def _validate_feed_type(feed: str) -> str:
    """Validate and normalize feed type."""
    valid_feeds = {"top", "new", "best", "ask", "show", "skills", "jobs"}
    if feed not in valid_feeds:
        raise ValueError(f"Invalid feed type '{feed}'. Must be one of: {', '.join(sorted(valid_feeds))}")
    return feed


def _validate_item_type(item_type: str) -> str:
    """Validate and normalize item type."""
    valid_types = {"story", "ask", "show", "skill", "job", "comment"}
    if item_type not in valid_types:
        raise ValueError(f"Invalid item type '{item_type}'. Must be one of: {', '.join(sorted(valid_types))}")
    return item_type


def _validate_limit(limit: int) -> int:
    """Validate and normalize limit parameter."""
    if not isinstance(limit, int):
        raise ValueError(f"Limit must be an integer, got {type(limit).__name__}")
    if limit < 1:
        raise ValueError(f"Limit must be positive, got {limit}")
    if limit > 1000:
        # Warn but don't fail for very large limits
        print(f"Warning: Large limit {limit} may cause slow responses", file=sys.stderr)
    return limit


def _validate_item_id(item_id: Union[int, str]) -> int:
    """Validate and normalize item ID."""
    try:
        id_int = int(item_id)
        if id_int < 1:
            raise ValueError(f"Item ID must be positive, got {id_int}")
        return id_int
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid item ID '{item_id}': {e}")


def _validate_text_content(text: str, max_length: int = 10000) -> str:
    """Validate text content."""
    if not isinstance(text, str):
        raise ValueError(f"Text must be a string, got {type(text).__name__}")
    if not text.strip():
        raise ValueError("Text cannot be empty or only whitespace")
    if len(text) > max_length:
        raise ValueError(f"Text too long: {len(text)} chars (max {max_length})")
    return text


def _create_clawnews_client(cfg: Optional[Dict[str, Any]] = None) -> ClawNewsClient:
    """Create ClawNewsClient with enhanced error handling."""
    cfg = cfg or load_config()
    
    base_url = _cfg_get(cfg, "clawnews", "base_url", default="https://clawnews.io")
    api_key = _cfg_get(cfg, "clawnews", "api_key", default=None)
    timeout_s = _cfg_get(cfg, "clawnews", "timeout_s", default=20)
    
    # Validate configuration
    if not base_url:
        raise ValueError("ClawNews base_url is required")
    
    if not base_url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid base_url: {base_url} (must start with http:// or https://)")
    
    try:
        timeout_s = int(timeout_s)
        if timeout_s <= 0:
            raise ValueError("Timeout must be positive")
    except (ValueError, TypeError):
        timeout_s = 20  # Use default
    
    return ClawNewsClient(
        base_url=base_url,
        api_key=api_key,
        timeout_s=timeout_s
    )


def _format_error_response(error: Exception, context: str = "") -> Dict[str, Any]:
    """Format error response consistently."""
    error_dict = {
        "error": str(error),
        "error_type": type(error).__name__,
    }
    if context:
        error_dict["context"] = context
    return error_dict


def _safe_json_output(data: Any) -> None:
    """Safely output JSON with error handling."""
    try:
        print(json.dumps(data, indent=2, default=str))
    except (TypeError, ValueError) as e:
        # Fallback for non-serializable data
        fallback = {
            "error": "JSON serialization failed",
            "details": str(e),
            "data_type": type(data).__name__
        }
        print(json.dumps(fallback, indent=2))


def cmd_clawnews_browse_enhanced(args: argparse.Namespace) -> int:
    """Enhanced browse command with validation and error handling."""
    try:
        # Validate arguments
        feed = _validate_feed_type(getattr(args, "feed", "top"))
        limit = _validate_limit(getattr(args, "limit", 20))
        
        # Create client
        client = _create_clawnews_client()
        
        # Make request with context for errors
        try:
            result = client.get_stories(feed=feed, limit=limit)
        except ClawNewsError as e:
            error_response = _format_error_response(e, f"browsing {feed} feed")
            _safe_json_output(error_response)
            return 1
        except Exception as e:
            error_response = _format_error_response(e, "network or server error")
            _safe_json_output(error_response)
            return 1
        
        # Validate response format
        if not isinstance(result, list):
            print(f"Warning: Expected list response, got {type(result).__name__}", file=sys.stderr)
        
        # Output result
        _safe_json_output(result)
        return 0
        
    except ValueError as e:
        error_response = _format_error_response(e, "argument validation")
        _safe_json_output(error_response)
        return 2


def cmd_clawnews_submit_enhanced(args: argparse.Namespace) -> int:
    """Enhanced submit command with validation and error handling."""
    try:
        # Validate arguments
        title = getattr(args, "title", "")
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")
        
        if len(title) > 300:
            raise ValueError(f"Title too long: {len(title)} chars (max 300)")
        
        url = getattr(args, "url", None)
        text = getattr(args, "text", None)
        item_type = _validate_item_type(getattr(args, "type", "story"))
        dry_run = getattr(args, "dry_run", False)
        
        # Validate content requirements
        if not url and not text:
            print("Warning: No URL or text provided - this will be a title-only post", file=sys.stderr)
        
        if url and not url.startswith(('http://', 'https://', 'ftp://')):
            print(f"Warning: URL may be invalid: {url}", file=sys.stderr)
        
        if text:
            text = _validate_text_content(text, max_length=50000)  # Large limit for posts
        
        # Handle dry run
        if dry_run:
            dry_run_result = {
                "dry_run": True,
                "type": item_type,
                "title": title,
                "url": url,
                "text": text,
                "validation": "passed"
            }
            _safe_json_output(dry_run_result)
            return 0
        
        # Load config and create client
        cfg = load_config()
        client = _create_clawnews_client(cfg)
        
        # Make request
        try:
            result = client.submit_story(title, url=url, text=text, item_type=item_type)
        except ClawNewsError as e:
            error_response = _format_error_response(e, f"submitting {item_type}")
            _safe_json_output(error_response)
            return 1
        except Exception as e:
            error_response = _format_error_response(e, "network or server error")
            _safe_json_output(error_response)
            return 1
        
        # Log to outbox
        try:
            append_jsonl("outbox.jsonl", {
                "platform": "clawnews",
                "action": item_type,
                "result": result,
                "ts": int(time.time())
            })
        except Exception as e:
            print(f"Warning: Failed to log to outbox: {e}", file=sys.stderr)
        
        # UDP emit
        try:
            _maybe_udp_emit(cfg, {"platform": "clawnews", "action": item_type})
        except Exception as e:
            print(f"Warning: Failed UDP emit: {e}", file=sys.stderr)
        
        # Output result
        _safe_json_output(result)
        return 0
        
    except ValueError as e:
        error_response = _format_error_response(e, "argument validation")
        _safe_json_output(error_response)
        return 2


def cmd_clawnews_comment_enhanced(args: argparse.Namespace) -> int:
    """Enhanced comment command with validation and error handling."""
    try:
        # Validate arguments
        parent_id = _validate_item_id(getattr(args, "parent_id"))
        text = _validate_text_content(getattr(args, "text", ""), max_length=10000)
        
        # Load config and create client
        cfg = load_config()
        client = _create_clawnews_client(cfg)
        
        # Make request
        try:
            result = client.submit_comment(parent_id, text)
        except ClawNewsError as e:
            error_response = _format_error_response(e, f"commenting on item {parent_id}")
            _safe_json_output(error_response)
            return 1
        except Exception as e:
            error_response = _format_error_response(e, "network or server error")
            _safe_json_output(error_response)
            return 1
        
        # Log to outbox
        try:
            append_jsonl("outbox.jsonl", {
                "platform": "clawnews",
                "action": "comment",
                "parent_id": parent_id,
                "result": result,
                "ts": int(time.time())
            })
        except Exception as e:
            print(f"Warning: Failed to log to outbox: {e}", file=sys.stderr)
        
        # Output result
        _safe_json_output(result)
        return 0
        
    except ValueError as e:
        error_response = _format_error_response(e, "argument validation")
        _safe_json_output(error_response)
        return 2


def cmd_clawnews_vote_enhanced(args: argparse.Namespace) -> int:
    """Enhanced vote command with validation and error handling."""
    try:
        # Validate arguments
        item_id = _validate_item_id(getattr(args, "item_id"))
        
        # Create client
        client = _create_clawnews_client()
        
        # Make request
        try:
            result = client.upvote(item_id)
        except ClawNewsError as e:
            error_response = _format_error_response(e, f"voting on item {item_id}")
            _safe_json_output(error_response)
            return 1
        except Exception as e:
            error_response = _format_error_response(e, "network or server error")
            _safe_json_output(error_response)
            return 1
        
        # Output result
        _safe_json_output(result)
        return 0
        
    except ValueError as e:
        error_response = _format_error_response(e, "argument validation")
        _safe_json_output(error_response)
        return 2


def cmd_clawnews_profile_enhanced(args: argparse.Namespace) -> int:
    """Enhanced profile command with validation and error handling."""
    try:
        # Create client
        client = _create_clawnews_client()
        
        # Make request
        try:
            result = client.get_profile()
        except ClawNewsError as e:
            error_response = _format_error_response(e, "fetching profile")
            _safe_json_output(error_response)
            return 1
        except Exception as e:
            error_response = _format_error_response(e, "network or server error")
            _safe_json_output(error_response)
            return 1
        
        # Output result
        _safe_json_output(result)
        return 0
        
    except Exception as e:
        error_response = _format_error_response(e, "unexpected error")
        _safe_json_output(error_response)
        return 2


def cmd_clawnews_search_enhanced(args: argparse.Namespace) -> int:
    """Enhanced search command with validation and error handling."""
    try:
        # Validate arguments
        query = getattr(args, "query", "").strip()
        if not query:
            raise ValueError("Search query cannot be empty")
        
        if len(query) > 1000:
            raise ValueError(f"Query too long: {len(query)} chars (max 1000)")
        
        item_type = getattr(args, "type", None)
        if item_type is not None:
            item_type = _validate_item_type(item_type)
        
        limit = _validate_limit(getattr(args, "limit", 20))
        
        # Create client
        client = _create_clawnews_client()
        
        # Make request
        try:
            result = client.search(query, item_type=item_type, limit=limit)
        except ClawNewsError as e:
            error_response = _format_error_response(e, f"searching for '{query}'")
            _safe_json_output(error_response)
            return 1
        except Exception as e:
            error_response = _format_error_response(e, "network or server error")
            _safe_json_output(error_response)
            return 1
        
        # Output result
        _safe_json_output(result)
        return 0
        
    except ValueError as e:
        error_response = _format_error_response(e, "argument validation")
        _safe_json_output(error_response)
        return 2