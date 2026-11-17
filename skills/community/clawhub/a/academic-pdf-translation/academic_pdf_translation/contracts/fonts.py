"""跨平台字体发现、兼容性探测与角色选择。

原来的字体解析只扫 macOS 目录，并且只看文件后缀就认为字体可用。
两个后果：

1. Linux 上会选到 ReportLab 装不进去的字体（例如带 PostScript/CFF 轮廓的
   ``NotoSansCJK-Regular.ttc``）。文件存在，渲染时才炸。
2. 正体和粗体可能解析成同一个文件，然后一声不吭。表格里靠粗体表达的
   语义（最优值、强调列）就此消失，QA 也看不出来。

所以这里的规矩是：**先真的用 ReportLab 装一次，装得进去才算数**，
并且正体、粗体、题录体分别选、分别记证据。
"""

from __future__ import annotations

import hashlib
import os
import platform
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from reportlab.pdfbase.ttfonts import TTFont

#: 字体角色。正体与粗体必须分别选择。
ROLE_REGULAR = "regular"
ROLE_BOLD = "bold"
ROLE_REFERENCE = "reference"
#: 数学符号后备：正文字体画不出的 ∈、Ω 这类字符按字符段改用它。
ROLE_MATH = "math"
FONT_ROLES = (ROLE_REGULAR, ROLE_BOLD, ROLE_REFERENCE, ROLE_MATH)

FONT_SUFFIXES = (".ttf", ".ttc", ".otf")
#: ReportLab 对 TrueType 轮廓支持最好，优先级最高。
SUFFIX_PRIORITY = {".ttf": 0, ".ttc": 1, ".otf": 2}

MACOS_FONT_DIRS = (
    "/System/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "/Library/Fonts",
    "~/Library/Fonts",
)
LINUX_FONT_DIRS = (
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    "~/.fonts",
    "~/.local/share/fonts",
)
WINDOWS_FONT_DIR_TEMPLATES = (
    "${WINDIR}/Fonts",
    "${LOCALAPPDATA}/Microsoft/Windows/Fonts",
)

#: 只有这些才算真正的粗体。"medium" 是中等字重，不是粗体，不能算进来。
#: 后面几个是常见的缩写字重后缀：msyhbd.ttc 就是 Microsoft YaHei Bold，
#: 只认全拼会把真正的粗体漏掉。
BOLD_TOKENS = (
    "bold",
    "semibold",
    "demibold",
    "heavy",
    "black",
    "bd",
    "sb",
    "blk",
)

#: 缩写字重后缀。剥掉它们才能算出字体家族名。
ABBREVIATED_WEIGHT_SUFFIXES = ("bd", "sb", "blk", "lt", "md", "rg")

#: 剥掉字重后缀后，家族名至少要剩这么多字符，否则说明剥错了。
MIN_FAMILY_TOKEN_LENGTH = 3

#: 常见字体的文件名别名。字体家族名和磁盘文件名经常对不上。
FONT_NAME_ALIASES = {
    "microsoftyahei": ("msyh", "yahei"),
    "sourcehansanssc": ("sourcehansans", "sourcesans", "notosanscjk"),
    "notosanscjksc": ("notosanscjk", "notosans"),
    "pingfangsc": ("pingfang",),
    "stheiti": ("stheiti",),
    "arialunicodems": ("arialunicode",),
    "songti": ("songti",),
    "hiraginosansgb": ("hiraginosans",),
}
STYLE_SUFFIXES = frozenset(
    {
        "",
        "regular",
        "book",
        "roman",
        "medium",
        "light",
        "bold",
        "semibold",
        "demibold",
        "heavy",
        "black",
        "italic",
        "oblique",
        "bolditalic",
        "boldoblique",
        "semibolditalic",
    }
)

#: 题录体允许的字重：正常粗细的散文字重。粗体家族（Bold/Semibold/
#: Demibold/Heavy/Black 及缩写）一律拒绝——"Arial Black" 名字里带
#: Arial，按名字匹配会把整页参考文献排成海报粗。
REFERENCE_ALLOWED_WEIGHTS = ("regular", "book", "roman", "medium")
REFERENCE_FORBIDDEN_WEIGHT_TOKENS = BOLD_TOKENS

#: 题录体的默认候选，按偏好顺序。
DEFAULT_REFERENCE_NAMES = (
    "Arial",
    "Helvetica",
    "DejaVuSans",
    "LiberationSans",
    "NotoSans",
)

_TOKEN_RE = re.compile(r"[^a-z0-9]+")


def normalized_token(value: str) -> str:
    return _TOKEN_RE.sub("", str(value).casefold())


def font_search_dirs(system: str | None = None) -> tuple[Path, ...]:
    """按当前系统返回字体搜索目录。

    不在 Linux 上扫 macOS 的空路径，也不在 Windows 上扫 Linux 的空路径：
    扫不存在的目录既慢又会让日志失去意义。
    """

    name = (system or platform.system()).casefold()
    if name == "darwin":
        raw: Iterable[str] = MACOS_FONT_DIRS
    elif name == "windows":
        raw = [
            os.path.expandvars(template)
            for template in WINDOWS_FONT_DIR_TEMPLATES
        ]
    else:
        raw = LINUX_FONT_DIRS
    return tuple(Path(value).expanduser() for value in raw)


def discover_font_files(
    system: str | None = None,
    *,
    dirs: Iterable[Path] | None = None,
) -> list[Path]:
    """列出可用的字体文件，按 ReportLab 友好程度排序。"""

    search = tuple(dirs) if dirs is not None else font_search_dirs(system)
    found: list[Path] = []
    for directory in search:
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if path.suffix.casefold() in FONT_SUFFIXES and path.is_file():
                found.append(path)
    found.sort(
        key=lambda path: (
            SUFFIX_PRIORITY.get(path.suffix.casefold(), 9),
            str(path),
        )
    )
    return found


@dataclass(frozen=True)
class FontProbe:
    """一次真实的 ReportLab 加载探测结果。"""

    path: str
    loadable: bool
    reason: str = ""
    subfont_index: int | None = None
    covered_codepoints: int = 0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _probe_once(path: Path, subfont_index: int | None) -> FontProbe:
    name = f"FontProbe{abs(hash((str(path), subfont_index))) % 10_000_000}"
    kwargs: dict[str, Any] = {}
    if subfont_index is not None:
        kwargs["subfontIndex"] = subfont_index
    try:
        font = TTFont(name, str(path), **kwargs)
    except Exception as exc:  # noqa: BLE001 - 需要把真实原因原样带出去
        return FontProbe(
            path=str(path),
            loadable=False,
            reason=f"{type(exc).__name__}: {exc}"[:400],
            subfont_index=subfont_index,
        )
    mapping = getattr(font.face, "charToGlyph", None)
    if not isinstance(mapping, dict) or not mapping:
        return FontProbe(
            path=str(path),
            loadable=False,
            reason="字体没有可用的字符到字形映射",
            subfont_index=subfont_index,
        )
    return FontProbe(
        path=str(path),
        loadable=True,
        subfont_index=subfont_index,
        covered_codepoints=len(mapping),
    )


def probe_reportlab_font(
    path: Path | str,
    *,
    max_subfonts: int = 8,
) -> FontProbe:
    """真的用 ReportLab 装一次这个字体。

    不看后缀猜。``.ttc`` 会逐个子字体试；带 CFF/PostScript 轮廓的字体
    ReportLab 装不进去，这里会带着真实异常信息返回 ``loadable=False``。
    """

    path = Path(path)
    if not path.is_file():
        return FontProbe(path=str(path), loadable=False, reason="字体文件不存在")
    if path.suffix.casefold() == ".ttc":
        last = FontProbe(path=str(path), loadable=False, reason="TTC 没有可用子字体")
        for index in range(max_subfonts):
            probe = _probe_once(path, index)
            if probe.loadable:
                return probe
            last = probe
            if "index" not in probe.reason.casefold():
                # 子字体越界以外的错误（例如 CFF 轮廓）不必继续试。
                break
        return last
    return _probe_once(path, None)


def font_covers(probe_path: Path | str, characters: str, subfont_index: int | None = None) -> bool:
    """这个字体能不能画出给定的全部字符。"""

    probe = _probe_once(Path(probe_path), subfont_index)
    if not probe.loadable:
        return False
    kwargs: dict[str, Any] = {}
    if subfont_index is not None:
        kwargs["subfontIndex"] = subfont_index
    font = TTFont(f"CoverCheck{abs(hash(str(probe_path))) % 10_000_000}", str(probe_path), **kwargs)
    mapping = font.face.charToGlyph
    return all(ord(character) in mapping for character in characters)


def _family_token(path: Path) -> str:
    """去掉字重后缀，得到字体家族名。"""

    token = normalized_token(path.stem)
    candidates = sorted(
        (STYLE_SUFFIXES - {""}) | set(ABBREVIATED_WEIGHT_SUFFIXES),
        key=len,
        reverse=True,
    )
    for suffix in candidates:
        if token.endswith(suffix):
            stripped = token[: -len(suffix)]
            if len(stripped) >= MIN_FAMILY_TOKEN_LENGTH:
                return stripped
    return token


def _file_weight(path: Path) -> str:
    """按文件名判定真实字重，写进证据供人核对。"""

    return "bold" if _is_bold_file(path) else "regular"


_REFERENCE_FORBIDDEN_RE = re.compile(
    r"bold|black|heavy|semibold|demibold|bd(?![a-z])|blk|italic|oblique"
)


def reference_weight_ok(path: Path) -> bool:
    """题录体的字重闸门：正常字重才许进参考文献正文。

    与判"这是不是一把粗体"不同，这里是排他闸门：名字里**任何位置**
    出现粗体或斜体记号都拒——"Arial Bold Italic" 尾缀是 italic，
    只看结尾会漏掉它；整页参考文献也不该是斜体。"""

    return not _REFERENCE_FORBIDDEN_RE.search(normalized_token(path.stem))


def _score_fallbacks(paths: list[Path]) -> list[Path]:
    """第二阶段候选的确定性排序。

    真正的加载与字符覆盖由 pick() 逐个探测，这里只决定先试谁：
    TrueType 轮廓优先、正常字重优先、路径短且稳定优先、
    最后按路径字典序保证可复现。
    """

    def score(path: Path) -> tuple:
        suffix = path.suffix.casefold()
        return (
            0 if suffix in (".ttf", ".ttc", ".otf") else 1,
            1 if _is_bold_file(path) else 0,
            len(path.parts),
            str(path),
        )

    return sorted(paths, key=score)


def _is_bold_file(path: Path) -> bool:
    token = normalized_token(path.stem)
    for marker in BOLD_TOKENS:
        if token.endswith(marker) and len(token) - len(marker) >= MIN_FAMILY_TOKEN_LENGTH:
            return True
    return False


def _score_one(requested_token: str, stem_token: str) -> int:
    if not requested_token or not stem_token.startswith(requested_token):
        return 0
    suffix = stem_token[len(requested_token) :]
    if suffix not in STYLE_SUFFIXES and suffix not in ABBREVIATED_WEIGHT_SUFFIXES:
        return 0
    if not suffix:
        return 100
    if suffix in {"regular", "book", "roman"}:
        return 90
    if suffix in BOLD_TOKENS:
        return 80
    return 60


def _match_score(requested: str, path: Path) -> int:
    """字体家族名与磁盘文件名的匹配分；别名比正名低一档。"""

    requested_token = normalized_token(requested)
    stem_token = normalized_token(path.stem)
    best = _score_one(requested_token, stem_token)
    for alias in FONT_NAME_ALIASES.get(requested_token, ()):
        score = _score_one(alias, stem_token)
        if score:
            best = max(best, score - 5)
    return best


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass
class FontSelection:
    """一个角色最终选中的字体，连同它的证据。"""

    role: str
    path: str
    sha256: str
    subfont_index: int | None
    probe: FontProbe
    source: str = "candidate-match"
    #: 真实字重（按文件名判定）："bold" 或 "regular"。
    weight: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "path": self.path,
            "sha256": self.sha256,
            "subfont_index": self.subfont_index,
            "source": self.source,
            "weight": self.weight or _file_weight(Path(self.path)),
            "probe": self.probe.as_dict(),
        }


@dataclass
class FontResolution:
    """一次完整的字体解析结果。"""

    selections: dict[str, FontSelection] = field(default_factory=dict)
    rejected: list[FontProbe] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def paths(self) -> list[str]:
        return [self.selections[role].path for role in FONT_ROLES if role in self.selections]

    def evidence(self) -> list[dict[str, Any]]:
        return [
            self.selections[role].as_dict()
            for role in FONT_ROLES
            if role in self.selections
        ]


def _ordered_candidates(
    requested: list[str],
    available: list[Path],
) -> list[Path]:
    scored: list[tuple[int, int, str, Path]] = []
    for path in available:
        best = 0
        rank = len(requested)
        for index, name in enumerate(requested):
            score = _match_score(name, path)
            if score > best:
                best, rank = score, index
        if best:
            # 先按调用方给出的偏好顺序，再按匹配质量。
            # 兜底字体不能因为文件名匹配得更整齐就压过首选字体。
            scored.append((rank, -best, str(path), path))
    scored.sort()
    return [item[3] for item in scored]


def resolve_fonts(
    requested_names: Iterable[str],
    *,
    required_characters: str = "",
    available: Iterable[Path] | None = None,
    system: str | None = None,
    fallback_names: Iterable[str] = (),
    reference_names: Iterable[str] = DEFAULT_REFERENCE_NAMES,
    reference_characters: str = "",
    math_characters: str = "",
) -> FontResolution:
    """按角色解析字体，全部经过真实 ReportLab 探测。

    ``required_characters`` 用来确认这套字体真的能显示目标语言；
    传空串时只做加载探测。
    """

    files = list(available) if available is not None else discover_font_files(system)
    requested = [str(value).strip() for value in requested_names if str(value).strip()]
    requested += [str(value).strip() for value in fallback_names if str(value).strip()]
    resolution = FontResolution()

    # 两阶段候选队列。第一阶段：名字匹配的偏好字体。第二阶段：其余
    # **全部**字体按可用性打分排队——匹配的候选全部加载失败时，
    # 系统里明明还有能用的字体（Linux 上常见 uming.ttc），
    # 不能因为名字不像就不试。
    preferred = _ordered_candidates(requested, files)
    remaining = [path for path in files if path not in set(preferred)]
    ranked = preferred + _score_fallbacks(remaining)

    def pick(role: str, predicate) -> FontSelection | None:
        for path in ranked:
            if not predicate(path):
                continue
            probe = probe_reportlab_font(path)
            if not probe.loadable:
                resolution.rejected.append(probe)
                continue
            if required_characters and not font_covers(
                path, required_characters, probe.subfont_index
            ):
                resolution.rejected.append(
                    FontProbe(
                        path=str(path),
                        loadable=True,
                        reason="字体无法显示目标语言所需字符",
                        subfont_index=probe.subfont_index,
                        covered_codepoints=probe.covered_codepoints,
                    )
                )
                continue
            return FontSelection(
                role=role,
                path=str(path),
                sha256=sha256_file(path),
                subfont_index=probe.subfont_index,
                probe=probe,
            )
        return None

    regular = pick(ROLE_REGULAR, lambda path: not _is_bold_file(path))
    if regular is None:
        regular = pick(ROLE_REGULAR, lambda path: True)
    if regular is not None:
        resolution.selections[ROLE_REGULAR] = regular

    if regular is not None:
        family = _family_token(Path(regular.path))
        # 粗体必须来自同一个字体家族。拿另一个家族的粗体顶上去，
        # 版面会突然换脸，比没有粗体更糟。
        bold = pick(
            ROLE_BOLD,
            lambda path: _is_bold_file(path) and _family_token(path) == family,
        )
        if bold is None:
            # 找不到真正的粗体时必须说出来，不能静默用正体顶替：
            # 表格里靠粗体表达的语义会就此消失。
            resolution.warnings.append(
                "FONT_BOLD_FALLS_BACK_TO_REGULAR: 未找到与正体同族的粗体字体，"
                "粗体语义（例如表格最优值）在候选中无法体现"
            )
            bold = FontSelection(
                role=ROLE_BOLD,
                path=regular.path,
                sha256=regular.sha256,
                subfont_index=regular.subfont_index,
                probe=regular.probe,
                source="regular-fallback",
            )
        resolution.selections[ROLE_BOLD] = bold

    # 题录体：参考文献题录是拉丁文，用拉丁字体更好看。但它必须能画出
    # 题录里真实出现的字符，否则会退化成空字符。探测不过就回落到正体。
    reference = None
    for name in reference_names:
        for path in files:
            if _match_score(name, path) < 60:
                continue
            if not reference_weight_ok(path):
                # "Arial Black" 也叫 Arial。字重不合格就拒，且要说清楚。
                resolution.rejected.append(
                    FontProbe(
                        path=str(path),
                        loadable=True,
                        reason=(
                            "题录体只许正常字重（regular/book/roman/"
                            "medium），该文件按名字判定是粗体家族"
                        ),
                    )
                )
                continue
            probe = probe_reportlab_font(path)
            if not probe.loadable:
                resolution.rejected.append(probe)
                continue
            if reference_characters and not font_covers(
                path, reference_characters, probe.subfont_index
            ):
                continue
            reference = FontSelection(
                role=ROLE_REFERENCE,
                path=str(path),
                sha256=sha256_file(path),
                subfont_index=probe.subfont_index,
                probe=probe,
            )
            break
        if reference is not None:
            break
    if reference is None and regular is not None:
        reference = FontSelection(
            role=ROLE_REFERENCE,
            path=regular.path,
            sha256=regular.sha256,
            subfont_index=regular.subfont_index,
            probe=regular.probe,
            source="regular-fallback",
        )
    if reference is not None:
        resolution.selections[ROLE_REFERENCE] = reference

    # 数学符号与核心中文分开检查：正文字体覆盖不了的符号字符，
    # 从全部候选里找一把能画的当后备。找不到就明说，不许静默丢字。
    if math_characters and regular is not None:
        uncovered = "".join(
            character
            for character in dict.fromkeys(math_characters)
            if not character.isspace()
            and not font_covers(
                Path(regular.path), character, regular.subfont_index
            )
        )
        if uncovered:
            math = None
            for path in ranked:
                if _is_bold_file(path):
                    continue
                probe = probe_reportlab_font(path)
                if not probe.loadable:
                    continue
                if font_covers(path, uncovered, probe.subfont_index):
                    math = FontSelection(
                        role=ROLE_MATH,
                        path=str(path),
                        sha256=sha256_file(path),
                        subfont_index=probe.subfont_index,
                        probe=probe,
                    )
                    break
            if math is not None:
                resolution.selections[ROLE_MATH] = math
            else:
                resolution.warnings.append(
                    "FONT_MATH_SYMBOLS_UNCOVERED: 正文字体画不出这些"
                    "数学/符号字符，且候选里没有能补齐的后备字体: "
                    + "".join(uncovered[:20])
                )

    return resolution
