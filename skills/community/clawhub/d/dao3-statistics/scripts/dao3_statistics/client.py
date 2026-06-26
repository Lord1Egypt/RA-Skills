from __future__ import annotations

from typing import Any, Dict, Optional

from .api import create_auth_headers, make_api_request


# Public (no auth)

def get_user_profile_by_user_id(user_id: str) -> Dict[str, Any]:
    return make_api_request(f"/user/profile/{user_id}")


def get_map_info_by_map_id(map_id: str) -> Dict[str, Any]:
    return make_api_request(f"/content/detail/{map_id}")


def get_map_comment_list(
    content_id: str,
    limit: int,
    offset: int,
    order_by: int,
    content_type: int,
) -> Dict[str, Any]:
    endpoint = (
        f"/comment/list?contentId={content_id}&limit={limit}&offset={offset}"
        f"&contentType={content_type}&orderBy={order_by}"
    )
    return make_api_request(endpoint)


def get_map_release_info(content_id: str, limit: int, offset: int) -> Dict[str, Any]:
    endpoint = f"/map/release-info/{content_id}?limit={limit}&offset={offset}"
    return make_api_request(endpoint)


def get_map_list_by_user_id(user_id: str, limit: int, offset: int) -> Dict[str, Any]:
    endpoint = f"/user/experience?limit={limit}&offset={offset}&userId={user_id}"
    return make_api_request(endpoint)


def get_model_list_by_user_id(user_id: str, limit: int, offset: int) -> Dict[str, Any]:
    endpoint = f"/user/models?limit={limit}&offset={offset}&userId={user_id}"
    return make_api_request(endpoint)


def get_favorite_list_by_user_id(
    user_id: str, limit: int, offset: int, content_type: int
) -> Dict[str, Any]:
    endpoint = (
        f"/user/favorites?limit={limit}&offset={offset}&userId={user_id}"
        f"&contentType={content_type}"
    )
    return make_api_request(endpoint)


def get_recently_play_list_by_user_id(user_id: str, limit: int, offset: int) -> Dict[str, Any]:
    endpoint = f"/user/recently-play?limit={limit}&offset={offset}&userId={user_id}"
    return make_api_request(endpoint)


def get_follower_list_by_user_id(user_id: str, limit: int, offset: int) -> Dict[str, Any]:
    endpoint = f"/follow/follower/v2?userId={user_id}&limit={limit}&offset={offset}"
    return make_api_request(endpoint)


def get_friend_list_by_user_id(user_id: str, limit: int, offset: int) -> Dict[str, Any]:
    endpoint = f"/follow/friends/v2?userId={user_id}&limit={limit}&offset={offset}"
    return make_api_request(endpoint)


def get_following_list_by_user_id(user_id: str, limit: int, offset: int) -> Dict[str, Any]:
    endpoint = f"/follow/following/v2?userId={user_id}&limit={limit}&offset={offset}"
    return make_api_request(endpoint)


def search_map_list_by_keyword(keyword: str, limit: int, offset: int, order_by: int) -> Dict[str, Any]:
    endpoint = (
        f"/map/tab/maps?offset={offset}&limit={limit}&keyword={keyword}&orderBy={order_by}"
    )
    return make_api_request(endpoint)


# Auth required

def get_comment_list(offset: int, limit: int, token: str, user_agent: str) -> Dict[str, Any]:
    headers = create_auth_headers(token, user_agent)
    return make_api_request(f"/msg/comment?offset={offset}&limit={limit}", headers=headers)


def get_like_list(offset: int, limit: int, token: str, user_agent: str) -> Dict[str, Any]:
    headers = create_auth_headers(token, user_agent)
    return make_api_request(f"/msg/like?offset={offset}&limit={limit}", headers=headers)


def get_system_msg_list(offset: int, limit: int, token: str, user_agent: str) -> Dict[str, Any]:
    headers = create_auth_headers(token, user_agent)
    return make_api_request(f"/msg/sys?offset={offset}&limit={limit}", headers=headers)


def get_map_stat_list(start_time: str, end_time: str, token: str, user_agent: str) -> Dict[str, Any]:
    headers = create_auth_headers(token, user_agent)
    endpoint = f"/statistics/map/user-maps?startTime={start_time}&endTime={end_time}"
    return make_api_request(endpoint, headers=headers)


def get_map_player_stat_list(
    start_time: str, end_time: str, map_id: str, token: str, user_agent: str
) -> Dict[str, Any]:
    return _map_stats("/statistics/map/player", start_time, end_time, map_id, token, user_agent)


def get_map_player_retention(
    start_time: str, end_time: str, map_id: str, token: str, user_agent: str
) -> Dict[str, Any]:
    return _map_stats(
        "/statistics/map/player-retention", start_time, end_time, map_id, token, user_agent
    )


def get_map_player_behavior(
    start_time: str, end_time: str, map_id: str, token: str, user_agent: str
) -> Dict[str, Any]:
    return _map_stats(
        "/statistics/map/player-behavior", start_time, end_time, map_id, token, user_agent
    )


def _map_stats(
    path: str, start_time: str, end_time: str, map_id: str, token: str, user_agent: str
) -> Dict[str, Any]:
    headers = create_auth_headers(token, user_agent)
    endpoint = f"{path}?startTime={start_time}&endTime={end_time}&mapId={map_id}"
    return make_api_request(endpoint, headers=headers)


def raw_get(endpoint: str, token: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
    headers = None
    if token is not None or user_agent is not None:
        if not token or not user_agent:
            raise ValueError("token 和 user_agent 必须同时提供")
        headers = create_auth_headers(token, user_agent)
    return make_api_request(endpoint, headers=headers)
