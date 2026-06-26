import argparse
import json
from typing import Any, Callable, Dict, Optional

from . import client


def _print(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False))


def _add_common_paging_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--offset", type=int, required=True)
    parser.add_argument("--limit", type=int, required=True)


def _add_auth_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--token", type=str, required=True)
    parser.add_argument("--user-agent", type=str, required=True)


def _run_and_print(fn: Callable[..., Dict[str, Any]], kwargs: Dict[str, Any]) -> None:
    _print(fn(**kwargs))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dao3_statistics")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("user-profile")
    p.add_argument("--user-id", required=True)
    p.set_defaults(_fn=client.get_user_profile_by_user_id, _map={"user_id": "user_id"})

    p = sub.add_parser("map-info")
    p.add_argument("--map-id", required=True)
    p.set_defaults(_fn=client.get_map_info_by_map_id, _map={"map_id": "map_id"})

    p = sub.add_parser("map-comments")
    p.add_argument("--content-id", required=True)
    p.add_argument("--limit", type=int, required=True)
    p.add_argument("--offset", type=int, required=True)
    p.add_argument("--order-by", type=int, required=True)
    p.add_argument("--content-type", type=int, required=True)
    p.set_defaults(
        _fn=client.get_map_comment_list,
        _map={
            "content_id": "content_id",
            "limit": "limit",
            "offset": "offset",
            "order_by": "order_by",
            "content_type": "content_type",
        },
    )

    p = sub.add_parser("map-release")
    p.add_argument("--content-id", required=True)
    p.add_argument("--limit", type=int, required=True)
    p.add_argument("--offset", type=int, required=True)
    p.set_defaults(
        _fn=client.get_map_release_info,
        _map={"content_id": "content_id", "limit": "limit", "offset": "offset"},
    )

    p = sub.add_parser("user-maps")
    p.add_argument("--user-id", required=True)
    _add_common_paging_args(p)
    p.set_defaults(
        _fn=client.get_map_list_by_user_id,
        _map={"user_id": "user_id", "limit": "limit", "offset": "offset"},
    )

    p = sub.add_parser("user-models")
    p.add_argument("--user-id", required=True)
    _add_common_paging_args(p)
    p.set_defaults(
        _fn=client.get_model_list_by_user_id,
        _map={"user_id": "user_id", "limit": "limit", "offset": "offset"},
    )

    p = sub.add_parser("user-favorites")
    p.add_argument("--user-id", required=True)
    _add_common_paging_args(p)
    p.add_argument("--content-type", type=int, required=True)
    p.set_defaults(
        _fn=client.get_favorite_list_by_user_id,
        _map={
            "user_id": "user_id",
            "limit": "limit",
            "offset": "offset",
            "content_type": "content_type",
        },
    )

    p = sub.add_parser("user-recent")
    p.add_argument("--user-id", required=True)
    _add_common_paging_args(p)
    p.set_defaults(
        _fn=client.get_recently_play_list_by_user_id,
        _map={"user_id": "user_id", "limit": "limit", "offset": "offset"},
    )

    p = sub.add_parser("user-followers")
    p.add_argument("--user-id", required=True)
    _add_common_paging_args(p)
    p.set_defaults(
        _fn=client.get_follower_list_by_user_id,
        _map={"user_id": "user_id", "limit": "limit", "offset": "offset"},
    )

    p = sub.add_parser("user-friends")
    p.add_argument("--user-id", required=True)
    _add_common_paging_args(p)
    p.set_defaults(
        _fn=client.get_friend_list_by_user_id,
        _map={"user_id": "user_id", "limit": "limit", "offset": "offset"},
    )

    p = sub.add_parser("user-following")
    p.add_argument("--user-id", required=True)
    _add_common_paging_args(p)
    p.set_defaults(
        _fn=client.get_following_list_by_user_id,
        _map={"user_id": "user_id", "limit": "limit", "offset": "offset"},
    )

    p = sub.add_parser("search")
    p.add_argument("--keyword", required=True)
    _add_common_paging_args(p)
    p.add_argument("--order-by", type=int, required=True)
    p.set_defaults(
        _fn=client.search_map_list_by_keyword,
        _map={
            "keyword": "keyword",
            "limit": "limit",
            "offset": "offset",
            "order_by": "order_by",
        },
    )

    p = sub.add_parser("msg-comments")
    _add_common_paging_args(p)
    _add_auth_args(p)
    p.set_defaults(
        _fn=client.get_comment_list,
        _map={"offset": "offset", "limit": "limit", "token": "token", "user_agent": "user_agent"},
    )

    p = sub.add_parser("msg-likes")
    _add_common_paging_args(p)
    _add_auth_args(p)
    p.set_defaults(
        _fn=client.get_like_list,
        _map={"offset": "offset", "limit": "limit", "token": "token", "user_agent": "user_agent"},
    )

    p = sub.add_parser("msg-sys")
    _add_common_paging_args(p)
    _add_auth_args(p)
    p.set_defaults(
        _fn=client.get_system_msg_list,
        _map={"offset": "offset", "limit": "limit", "token": "token", "user_agent": "user_agent"},
    )

    p = sub.add_parser("stats-maps")
    p.add_argument("--start-time", required=True)
    p.add_argument("--end-time", required=True)
    _add_auth_args(p)
    p.set_defaults(
        _fn=client.get_map_stat_list,
        _map={
            "start_time": "start_time",
            "end_time": "end_time",
            "token": "token",
            "user_agent": "user_agent",
        },
    )

    p = sub.add_parser("stats-player")
    p.add_argument("--start-time", required=True)
    p.add_argument("--end-time", required=True)
    p.add_argument("--map-id", required=True)
    _add_auth_args(p)
    p.set_defaults(
        _fn=client.get_map_player_stat_list,
        _map={
            "start_time": "start_time",
            "end_time": "end_time",
            "map_id": "map_id",
            "token": "token",
            "user_agent": "user_agent",
        },
    )

    p = sub.add_parser("stats-retention")
    p.add_argument("--start-time", required=True)
    p.add_argument("--end-time", required=True)
    p.add_argument("--map-id", required=True)
    _add_auth_args(p)
    p.set_defaults(
        _fn=client.get_map_player_retention,
        _map={
            "start_time": "start_time",
            "end_time": "end_time",
            "map_id": "map_id",
            "token": "token",
            "user_agent": "user_agent",
        },
    )

    p = sub.add_parser("stats-behavior")
    p.add_argument("--start-time", required=True)
    p.add_argument("--end-time", required=True)
    p.add_argument("--map-id", required=True)
    _add_auth_args(p)
    p.set_defaults(
        _fn=client.get_map_player_behavior,
        _map={
            "start_time": "start_time",
            "end_time": "end_time",
            "map_id": "map_id",
            "token": "token",
            "user_agent": "user_agent",
        },
    )

    p = sub.add_parser("raw")
    p.add_argument("--endpoint", required=True)
    p.add_argument("--token", required=False)
    p.add_argument("--user-agent", required=False)
    p.set_defaults(
        _fn=client.raw_get,
        _map={"endpoint": "endpoint", "token": "token", "user_agent": "user_agent"},
    )

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    fn = getattr(args, "_fn")
    mapping = getattr(args, "_map")
    kwargs = {k: getattr(args, v) for k, v in mapping.items()}
    _run_and_print(fn, kwargs)


if __name__ == "__main__":
    main()
