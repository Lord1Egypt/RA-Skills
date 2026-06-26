"""音乐管理工具模块

提供音乐相关的操作工具：
- match_background_music: 智能匹配背景音乐
- get_music_tags: 获取音乐标签
- search_music: 搜索音乐
- add_background_music: 添加背景音乐到作品
"""

from typing import Any, Dict, List, Optional

from ..api import get_api
from ..config import get_config
from ..utils.response import Response, ListResponse, format_success, format_error, format_list


class MusicTools:
    """音乐管理工具类"""

    # 音乐类型映射
    MUSIC_MOOD_MAP = {
        "happy": ["欢快", "轻松", "活泼", "快乐"],
        "sad": ["悲伤", "忧伤", "低沉", "哀伤"],
        "calm": ["平静", "舒缓", "放松", "宁静"],
        "epic": ["史诗", "震撼", "大气", "壮观"],
        "romantic": ["浪漫", "温馨", "甜蜜", "柔情"],
        "mysterious": ["神秘", "诡异", "悬疑", "紧张"],
        "nature": ["自然", "清新", "原生态", "环境"],
    }

    # 音乐场景匹配规则
    MUSIC_SCENE_RULES = {
        "panorama": ["大气", "沉浸", "全景", "壮阔"],
        "tour": ["引导", "游览", "轻松", "舒适"],
        "vr": ["科技", "未来", "现代", "炫酷"],
        "real estate": ["专业", "高端", "品质", "优雅"],
        "hotel": ["舒适", "放松", "温馨", "奢华"],
        "restaurant": ["品味", "格调", "优雅", "浪漫"],
        "museum": ["文化", "历史", "典雅", "厚重"],
        "nature": ["自然", "清新", "和谐", "原生态"],
    }

    def __init__(self):
        """初始化音乐工具"""
        self.config = get_config()
        self.api = get_api()

    def get_music_tags(
        self,
        tag_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取音乐标签

        Args:
            tag_type: 标签类型筛选（可选）
                     可选值: mood(心情), genre(风格), scene(场景), instrument(乐器)

        Returns:
            音乐标签列表

        Example:
            >>> tools = MusicTools()
            >>> result = tools.get_music_tags()
            >>> print(result)

            # 获取心情标签
            >>> result = tools.get_music_tags(tag_type="mood")
            >>> print(result)
        """
        params: Dict[str, Any] = {}

        if tag_type:
            if tag_type not in ("mood", "genre", "scene", "instrument"):
                return format_error(
                    "tag_type must be one of: mood, genre, scene, instrument",
                    code=400
                )
            params["type"] = tag_type

        response = self.api.get("/api/mcp/getMusicTag", data=params)

        # 格式化输出
        if response.get("code") == 0:
            data = response.get("data", {})
            tags = data.get("tags", [])

            # 格式化标签
            formatted_tags = []
            for tag in tags:
                formatted_tag = self._format_tag(tag)
                formatted_tags.append(formatted_tag)

            return format_success(
                data={
                    "items": formatted_tags,
                    "total": len(formatted_tags)
                }
            )

        return response

    def search_music(
        self,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        music_type: Optional[str] = None,
        duration_range: Optional[tuple] = None,
        tag_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """搜索音乐

        Args:
            keyword: 关键词搜索（可选）
            page: 页码，默认1
            page_size: 每页数量，默认20，最大100
            music_type: 音乐类型筛选（可选）
                       可选值: background, sound_effect, voice
            duration_range: 时长范围筛选（可选），格式为 (min_seconds, max_seconds)
            tag_ids: 标签ID列表（可选）

        Returns:
            音乐列表

        Example:
            >>> tools = MusicTools()
            >>> result = tools.search_music(keyword="轻音乐", page=1, page_size=10)
            >>> print(result)

            # 按标签筛选
            >>> result = tools.search_music(tag_ids=["tag1", "tag2"])
            >>> print(result)

            # 按时长筛选（30秒到5分钟）
            >>> result = tools.search_music(duration_range=(30, 300))
            >>> print(result)
        """
        # 参数校验
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
        if page_size > 100:
            page_size = 100

        params: Dict[str, Any] = {
            "page": page,
            "page_size": page_size
        }

        if keyword:
            params["keyword"] = keyword.strip()
        if music_type:
            if music_type not in ("background", "sound_effect", "voice"):
                return format_error(
                    "music_type must be one of: background, sound_effect, voice",
                    code=400
                )
            params["type"] = music_type
        if duration_range:
            if not isinstance(duration_range, tuple) or len(duration_range) != 2:
                return format_error("duration_range must be a tuple of (min, max)", code=400)
            params["duration_min"] = duration_range[0]
            params["duration_max"] = duration_range[1]
        if tag_ids:
            if not isinstance(tag_ids, list):
                return format_error("tag_ids must be a list", code=400)
            params["tag_ids"] = ",".join(tag_ids)

        response = self.api.get("/api/mcp/getMusicList", data=params)

        # 格式化输出
        if response.get("code") == 0:
            data = response.get("data", {})
            items = data.get("items", [])
            total = data.get("total", 0)

            # 格式化音乐列表
            formatted_items = []
            for item in items:
                formatted_item = self._format_music(item)
                formatted_items.append(formatted_item)

            return format_list(
                items=formatted_items,
                total=total,
                page=page,
                page_size=page_size
            )

        return response

    def match_background_music(
        self,
        work_id: str,
        work_type: Optional[str] = None,
        mood: Optional[str] = None,
        duration: Optional[int] = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        """智能匹配背景音乐

        根据作品类型、氛围和时长智能推荐合适的背景音乐。

        Args:
            work_id: 作品ID（必填）
            work_type: 作品类型（可选）
                      可选值: panorama, tour, vr, real_estate, hotel, restaurant, museum, nature
            mood: 氛围/心情（可选）
                  可选值: happy, sad, calm, epic, romantic, mysterious, nature
            duration: 期望时长，秒数（可选）
            limit: 返回数量限制，默认5，最大20

        Returns:
            推荐的背景音乐列表

        Example:
            >>> tools = MusicTools()
            >>> result = tools.match_background_music(
            ...     work_id="work123",
            ...     work_type="panorama",
            ...     mood="epic",
            ...     limit=3
            ... )
            >>> print(result)

            # 智能匹配（仅提供作品ID）
            >>> result = tools.match_background_music(work_id="work123")
            >>> print(result)
        """
        # 参数校验
        if not work_id or not work_id.strip():
            return format_error("work_id is required", code=400)

        if limit < 1:
            limit = 1
        if limit > 20:
            limit = 20

        # 构建匹配参数
        params: Dict[str, Any] = {
            "work_id": work_id.strip(),
            "page": 1,
            "page_size": limit * 2  # 获取更多以便筛选
        }

        # 根据作品类型确定推荐的关键词
        search_keywords = []
        if work_type:
            work_type_key = work_type.lower().replace(" ", "_")
            if work_type_key in self.MUSIC_SCENE_RULES:
                search_keywords.extend(self.MUSIC_SCENE_RULES[work_type_key])

        # 根据氛围确定关键词
        if mood:
            mood_key = mood.lower()
            if mood_key in self.MUSIC_MOOD_MAP:
                search_keywords.extend(self.MUSIC_MOOD_MAP[mood_key])

        # 如果有搜索关键词，进行搜索
        matched_music = []
        if search_keywords:
            # 搜索匹配的music
            for keyword in set(search_keywords):
                params["keyword"] = keyword
                response = self.api.get("/api/mcp/getMusicList", data=params)

                if response.get("code") == 0:
                    items = response.get("data", {}).get("items", [])
                    for item in items:
                        if item not in matched_music:
                            matched_music.append(item)

                # 重置keyword参数
                del params["keyword"]

            # 如果没有匹配到，使用空关键词搜索全部
            if not matched_music:
                response = self.api.get("/api/mcp/getMusicList", data=params)
                if response.get("code") == 0:
                    matched_music = response.get("data", {}).get("items", [])

        else:
            # 没有偏好时，获取流行音乐
            response = self.api.get("/api/mcp/getMusicList", data=params)
            if response.get("code") == 0:
                matched_music = response.get("data", {}).get("items", [])

        # 按规则筛选和排序
        scored_music = []
        for music in matched_music:
            score = 0

            # 作品类型匹配度评分
            if work_type:
                music_tags = music.get("tags", [])
                work_type_key = work_type.lower().replace(" ", "_")
                if work_type_key in self.MUSIC_SCENE_RULES:
                    for tag in music_tags:
                        if any(scene_tag in str(tag) for scene_tag in self.MUSIC_SCENE_RULES[work_type_key]):
                            score += 10

            # 氛围匹配度评分
            if mood:
                music_tags = music.get("tags", [])
                mood_key = mood.lower()
                if mood_key in self.MUSIC_MOOD_MAP:
                    for tag in music_tags:
                        if any(mood_tag in str(tag) for mood_tag in self.MUSIC_MOOD_MAP[mood_key]):
                            score += 5

            # 时长匹配度评分
            if duration:
                music_duration = music.get("duration", 0)
                if music_duration > 0:
                    # 时长接近期望值，评分更高
                    duration_diff = abs(music_duration - duration)
                    if duration_diff < 30:
                        score += 10
                    elif duration_diff < 60:
                        score += 5

            music["_match_score"] = score
            scored_music.append(music)

        # 按匹配度排序
        scored_music.sort(key=lambda x: x.get("_match_score", 0), reverse=True)

        # 取前limit个
        final_music = scored_music[:limit]

        # 格式化输出
        formatted_items = []
        for music in final_music:
            formatted = self._format_music(music)
            formatted["match_score"] = music.get("_match_score", 0)
            formatted_items.append(formatted)

        return format_success(
            data={
                "items": formatted_items,
                "total": len(formatted_items),
                "work_id": work_id,
                "work_type": work_type,
                "mood": mood
            }
        )

    def add_background_music(
        self,
        work_id: str,
        music_id: str,
        volume: float = 0.5,
        fade_in: int = 0,
        fade_out: int = 0,
        start_time: int = 0,
        loop: bool = True
    ) -> Dict[str, Any]:
        """添加背景音乐到作品

        Args:
            work_id: 作品ID（必填）
            music_id: 音乐ID（必填）
            volume: 音量，0.0-1.0，默认0.5
            fade_in: 淡入时长，秒数，默认0
            fade_out: 淡出时长，秒数，默认0
            start_time: 开始播放时间，秒数，默认0
            loop: 是否循环播放，默认True

        Returns:
            添加结果

        Example:
            >>> tools = MusicTools()
            >>> result = tools.add_background_music(
            ...     work_id="work123",
            ...     music_id="music456",
            ...     volume=0.7,
            ...     fade_in=2,
            ...     loop=True
            ... )
            >>> print(result)
        """
        # 参数校验
        if not work_id or not work_id.strip():
            return format_error("work_id is required", code=400)

        if not music_id or not music_id.strip():
            return format_error("music_id is required", code=400)

        if volume < 0.0 or volume > 1.0:
            return format_error("volume must be between 0.0 and 1.0", code=400)

        if fade_in < 0:
            return format_error("fade_in must be non-negative", code=400)

        if fade_out < 0:
            return format_error("fade_out must be non-negative", code=400)

        if start_time < 0:
            return format_error("start_time must be non-negative", code=400)

        # 构建音乐配置数据
        music_config = {
            "music_id": music_id.strip(),
            "volume": volume,
            "fade_in": fade_in,
            "fade_out": fade_out,
            "start_time": start_time,
            "loop": loop
        }

        # 使用 /api/tour/info 接口保存作品音乐
        save_data = {
            "work_id": work_id.strip(),
            "music": music_config
        }

        response = self.api.post("/api/tour/info", data=save_data)

        # 格式化输出
        if response.get("code") == 0:
            return format_success(
                data={
                    "work_id": work_id,
                    "music_id": music_id,
                    "config": music_config
                },
                message="Background music added successfully"
            )

        return response

    def _format_tag(self, tag: Dict[str, Any]) -> Dict[str, Any]:
        """格式化标签

        Args:
            tag: 原始标签数据

        Returns:
            格式化后的标签数据
        """
        return {
            "id": tag.get("id") or tag.get("tag_id"),
            "name": tag.get("name", ""),
            "type": tag.get("type", "custom"),
            "count": tag.get("count", 0),
            "description": tag.get("description", ""),
        }

    def _format_music(self, music: Dict[str, Any]) -> Dict[str, Any]:
        """格式化音乐

        Args:
            music: 原始音乐数据

        Returns:
            格式化后的音乐数据
        """
        return {
            "id": music.get("id") or music.get("music_id"),
            "name": music.get("name", "Untitled Music"),
            "artist": music.get("artist", "Unknown Artist"),
            "album": music.get("album", ""),
            "duration": music.get("duration", 0),
            "duration_formatted": self._format_duration(music.get("duration", 0)),
            "url": music.get("url", ""),
            "thumbnail": music.get("thumbnail", music.get("cover", "")),
            "type": music.get("type", "background"),
            "tags": music.get("tags", []),
            "lyrics": music.get("lyrics", ""),
            "format": music.get("format", "mp3"),
            "bitrate": music.get("bitrate", 128),
            "file_size": music.get("file_size", 0),
            "created_at": music.get("created_at", ""),
        }

    @staticmethod
    def _format_duration(seconds: int) -> str:
        """格式化时长为 MM:SS 格式

        Args:
            seconds: 秒数

        Returns:
            格式化后的时长字符串
        """
        if seconds <= 0:
            return "00:00"
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02d}:{remaining_seconds:02d}"


# 导出便捷函数
def get_music_tags(**kwargs) -> Dict[str, Any]:
    """获取音乐标签"""
    return MusicTools().get_music_tags(**kwargs)


def search_music(**kwargs) -> Dict[str, Any]:
    """搜索音乐"""
    return MusicTools().search_music(**kwargs)


def match_background_music(**kwargs) -> Dict[str, Any]:
    """智能匹配背景音乐"""
    return MusicTools().match_background_music(**kwargs)


def add_background_music(**kwargs) -> Dict[str, Any]:
    """添加背景音乐到作品"""
    return MusicTools().add_background_music(**kwargs)
