"""Dida Coach 工具集合。"""

from .config_manager import (
    get_personality_preset,
    get_reminder_config,
    get_work_method_config,
    load_config,
    save_user_config,
)
from .dida_semantics import (
    is_current_task_completed,
    normalize_priority_name,
    priority_label,
    priority_to_numeric,
)
from .mcp_client import check_mcp_configured, get_mcp_setup_command
from .mcp_client import (
    build_openclaw_connect_guide,
    write_openclaw_mcp_config,
)
from .openapi_auth import (
    build_authorization_url,
    exchange_code_for_token,
    get_openapi_env_path,
    read_openapi_env,
    wait_for_oauth_callback,
    write_openapi_env,
)
from .productivity_system import (
    build_productivity_snapshot,
    get_productivity_root,
    initialize_productivity_system,
    is_productivity_system_initialized,
    summarize_productivity_state,
    update_productivity_files,
)
from .review_analyzer import (
    analyze_daily_tasks,
    analyze_weekly_trends,
    generate_daily_report,
    generate_weekly_report,
)
from .task_parser import (
    extract_priority,
    extract_tags,
    parse_goal_input,
    parse_reschedule_request,
    parse_timebox_input,
)
from .timebox_calculator import (
    calculate_timeboxes,
    extend_box_duration,
    format_timebox_schedule,
    reschedule_boxes,
)
from .work_method_recommender import (
    explain_work_method,
    get_work_method_reasoning,
    recommend_work_method,
)

__all__ = [
    "analyze_daily_tasks",
    "analyze_weekly_trends",
    "build_productivity_snapshot",
    "build_openclaw_connect_guide",
    "build_authorization_url",
    "calculate_timeboxes",
    "check_mcp_configured",
    "explain_work_method",
    "extend_box_duration",
    "extract_priority",
    "extract_tags",
    "format_timebox_schedule",
    "generate_daily_report",
    "generate_weekly_report",
    "get_mcp_setup_command",
    "get_openapi_env_path",
    "get_personality_preset",
    "get_productivity_root",
    "get_reminder_config",
    "get_work_method_config",
    "get_work_method_reasoning",
    "initialize_productivity_system",
    "is_productivity_system_initialized",
    "load_config",
    "normalize_priority_name",
    "parse_goal_input",
    "parse_reschedule_request",
    "parse_timebox_input",
    "priority_label",
    "priority_to_numeric",
    "read_openapi_env",
    "recommend_work_method",
    "reschedule_boxes",
    "save_user_config",
    "is_current_task_completed",
    "summarize_productivity_state",
    "update_productivity_files",
    "wait_for_oauth_callback",
    "write_openclaw_mcp_config",
    "write_openapi_env",
    "exchange_code_for_token",
]
