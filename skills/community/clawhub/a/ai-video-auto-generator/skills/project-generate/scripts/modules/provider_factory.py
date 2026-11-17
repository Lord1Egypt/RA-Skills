"""Provider 工厂 — 按 project 查 provider 名并实例化。"""
import json, os
from agnes_provider import AgnesProvider
from xiaoyunqiao_provider import XiaoyunqiaoProvider

_provider_map: dict[str, type] = {
    "agnes": AgnesProvider,
    "xiaoyunqiao": XiaoyunqiaoProvider,
}

# Image provider 必须实现的方法列表（注册时校验）
_IMAGE_REQUIRED_METHODS = [
    "generate_image", "resolve_shot_params", "build_first_frame",
    "generate_prompt_template", "upload_to_url",
]
# Video provider 必须实现的方法列表（BaseProvider @abstractmethod 已保护）
_VIDEO_REQUIRED_METHODS = [
    "submit_video", "quick_query", "download_video",
]

# 中英文名称别名 → 内部 key
_NAME_ALIASES: dict[str, str] = {
    # 中文
    "agnes ai": "agnes", "agnes": "agnes", "agnès": "agnes",
    "小云雀": "xiaoyunqiao", "云雀": "xiaoyunqiao",
    "seedance": "xiaoyunqiao",
    # 占位 — libtv 注册后自动生效
    "libtv": "libtv", "liblib": "libtv",
}
# 反向补充：内部 key 本身也作为别名
for _k in list(_provider_map.keys()):
    _NAME_ALIASES[_k] = _k


def register_provider(name: str, cls: type) -> None:
    """注册 provider。自动校验必须实现的方法集。

    Image provider（如 agnes、libtv）必须实现 _IMAGE_REQUIRED_METHODS。
    Video provider（已有 @abstractmethod 保护）只需继承 BaseProvider。
    """
    # Image provider 校验
    for method in _IMAGE_REQUIRED_METHODS:
        if not hasattr(cls, method) or not callable(getattr(cls, method)):
            raise TypeError(
                f"[{name}] Image provider 必须实现 {method}()。"
                f" 参考: AgnesProvider"
            )

    _provider_map[name] = cls
    _NAME_ALIASES[name] = name


def resolve_provider_name(raw: str) -> str | None:
    """将用户输入（中英文/大小写/空格）标准化为内部 provider key。
    返回 None 表示找不到匹配。
    """
    normalized = raw.strip().lower().replace(" ", "")
    # 先做完整匹配
    if normalized in _NAME_ALIASES:
        return _NAME_ALIASES[normalized]
    # 模糊匹配：别名表中任一别名包含输入
    for alias, key in _NAME_ALIASES.items():
        if normalized in alias or alias in normalized:
            return key
    return None


def has_provider(name: str) -> bool:
    """检查指定名称的 provider 是否已注册。"""
    key = resolve_provider_name(name)
    return key is not None and key in _provider_map


def list_providers() -> list[str]:
    return list(_provider_map.keys())


def get_provider_name(project: str) -> str:
    sp = os.path.join(project, "script.json")
    default = "agnes"
    raw = default
    if os.path.isfile(sp):
        with open(sp, encoding="utf-8") as f:
            try:
                raw = json.load(f).get("script", {}).get("provider", default)
            except Exception:
                pass
    resolved = resolve_provider_name(raw)
    return resolved if resolved else default


_provider_cache: dict[str, "BaseProvider"] = {}


def _make_provider(name: str) -> "BaseProvider":
    cls = _provider_map.get(name)
    if cls is None:
        raise SystemExit(f"[ERROR] 不支持的 provider: {name}（可用: {list_providers()}）")
    return cls()


def create_provider(project: str) -> "BaseProvider":
    cache_key = os.path.abspath(project) if os.path.isdir(project) else project
    if cache_key in _provider_cache:
        return _provider_cache[cache_key]
    name = get_provider_name(project)
    inst = _make_provider(name)
    _provider_cache[cache_key] = inst
    return inst


def get_video_provider_name(project: str) -> str:
    """获取视频 provider 名。优先读 video_provider，fallback 到 provider。"""
    sp = os.path.join(project, "script.json")
    default = "agnes"
    raw = default
    if os.path.isfile(sp):
        with open(sp, encoding="utf-8") as f:
            try:
                scr = json.load(f).get("script", {})
                raw = scr.get("video_provider") or scr.get("provider", default)
            except Exception:
                pass
    resolved = resolve_provider_name(raw)
    return resolved if resolved else default


def create_video_provider(project: str) -> "BaseProvider":
    cache_key = f"video_{os.path.abspath(project) if os.path.isdir(project) else project}"
    if cache_key in _provider_cache:
        return _provider_cache[cache_key]
    name = get_video_provider_name(project)
    inst = _make_provider(name)
    _provider_cache[cache_key] = inst
    return inst


def detect_provider_from_title(title: str) -> dict[str, str]:
    """从飞书文档标题自动检测 provider 配置。

    返回: {"provider": "agnes|...", "video_provider": "agnes|xiaoyunqiao|..."}
    规则：
      - "小云雀视频" / "视频小云雀" → video_provider=xiaoyunqiao
      - "Agnes图片" / "图片Agnes" → provider=agnes
      - 标题只提一个工具名 → 图片和视频都用它
      - 未指定 → 保持空（走默认 fallback）
    """
    result: dict[str, str] = {"provider": "", "video_provider": ""}
    lower = title.lower()

    tools = [
        ("小云雀", "xiaoyunqiao"), ("云雀", "xiaoyunqiao"),
        ("seedance", "xiaoyunqiao"),
        ("libtv", "libtv"), ("liblib", "libtv"),
        ("agnes", "agnes"), ("agnès", "agnes"),
    ]

    for kw, key in tools:
        if kw not in lower or not has_provider(key):
            continue

        # 短语匹配："小云雀视频" / "视频小云雀" → 视频用此工具
        #  "Agnes图片" / "图片Agnes" → 图片用此工具
        idx = lower.index(kw)

        # 检查关键词左右各 8 个字符，找"图片"或"视频"
        context = lower[max(0, idx - 8): idx + len(kw) + 8]
        has_img = "图片" in context or "image" in context
        has_vid = "视频" in context or "video" in context

        if has_img and not result["provider"]:
            result["provider"] = key
        if has_vid and not result["video_provider"]:
            result["video_provider"] = key

        # 如果上下文没有任何方向词 → 先标记候选
        if not has_img and not has_vid:
            if not result["provider"] and not result["video_provider"]:
                # 第一个无方向词的工具 → 全用
                result["provider"] = key
                result["video_provider"] = key

    # 单侧指定（无方向词的工具名）已在循环内同步处理，
    # 有方向词的（"小云雀视频"）不跨侧复制，
    # 图片端未指定时用默认 agnes（由调用方的 fallback 保证）
    return result
