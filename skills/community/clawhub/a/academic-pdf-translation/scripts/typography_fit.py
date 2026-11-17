from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Iterable


class TypographyFitError(RuntimeError):
    pass


@dataclass(frozen=True)
class PageTextProfile:
    page: int
    translated_chars: int
    paragraph_count: int
    heading_count: int
    note_count: int
    available_width_pt: float
    available_height_pt: float

    @property
    def estimated_density(self) -> float:
        area = max(self.available_width_pt * self.available_height_pt, 1.0)
        return self.translated_chars / area


@dataclass(frozen=True)
class PageFitMeasurement:
    page: int
    fits: bool
    content_width_pt: float
    content_height_pt: float
    available_height_pt: float
    fill_ratio: float
    has_orphan_line: bool = False


MeasurePage = Callable[
    [PageTextProfile, float, float],
    PageFitMeasurement,
]


def descending_values(upper: float, lower: float, step: float) -> list[float]:
    if upper <= 0 or lower <= 0:
        raise TypographyFitError("字号和行距搜索边界必须大于 0")
    if upper < lower:
        raise TypographyFitError("搜索上界不得小于下界")
    if step <= 0:
        raise TypographyFitError("搜索步长必须大于 0")
    values: list[float] = []
    current = upper
    while current >= lower - 1e-9:
        values.append(round(current, 3))
        current -= step
    if values[-1] > lower + 1e-9:
        values.append(round(lower, 3))
    return values


def candidate_groups(
    *,
    body_font_range_pt: tuple[float, float],
    body_font_step_pt: float,
    leading_range: tuple[float, float],
    leading_step: float,
    preferred_body_font_pt: float | None = None,
    preferred_leading: float | None = None,
    selection_priority: str = "leading-then-font",
) -> list[list[tuple[float, float]]]:
    """构造字号与行距的候选搜索空间，按外层变量分组。

    这是全项目唯一的候选网格定义。排版器和文档级选型都从这里取值，
    避免两处各写一套而慢慢分叉。

    - 组间按外层变量降序，组内按内层变量降序；
    - `preferred_body_font_pt` 会把字号上界收到"偏好值加 1pt"以内；
    - `preferred_leading` 会并入行距集合，再整体降序排列。

    返回值是分组后的候选表；需要原顺序的一维列表时用 `flatten_candidates`。
    """

    body_lower, body_upper = body_font_range_pt
    leading_lower, leading_upper = leading_range
    if preferred_body_font_pt is not None:
        body_upper = min(body_upper, float(preferred_body_font_pt) + 1.0)
    body_sizes = descending_values(body_upper, body_lower, body_font_step_pt)
    leading_ratios = descending_values(
        leading_upper,
        leading_lower,
        leading_step,
    )
    if preferred_leading is not None:
        leading_ratios = sorted(
            set(leading_ratios) | {round(float(preferred_leading), 3)},
            reverse=True,
        )

    if selection_priority == "leading-then-font":
        return [
            [(body_size, leading_ratio) for body_size in body_sizes]
            for leading_ratio in leading_ratios
        ]
    if selection_priority == "font-then-leading":
        return [
            [
                (body_size, leading_ratio)
                for leading_ratio in leading_ratios
            ]
            for body_size in body_sizes
        ]
    raise TypographyFitError(
        "selection_priority 仅支持 leading-then-font 或 font-then-leading"
    )


def flatten_candidates(
    groups: list[list[tuple[float, float]]],
) -> list[tuple[float, float]]:
    return [candidate for group in groups for candidate in group]


def search_first_acceptable(
    *,
    groups: list[list[tuple[float, float]]],
    evaluate: Callable[[int, int], dict | None],
) -> tuple[tuple[int, int] | None, str, str]:
    """在候选表中找出原顺序里第一个可接受的组合。

    `evaluate(组下标, 组内下标)` 由调用方实现，返回含 `fits` 的字典；
    带上 `page_count` 时还会参与单调性审计。返回 None 表示这次测量失败。

    依据两条单调性：同一组内内层变量变小时页数不增；组间外层变量变小时，
    该组最紧凑组合的页数也不增。因此可以先在组之间二分，再在组内二分，
    用对数次测量得到与线性扫描相同的结果。

    每次测量都进入单调性审计。观测到"内层变量更小却页数更多"或"更靠后的
    组反而更厚"就立即回退，让调用方改用完整线性扫描并记录原因。

    两条快速路径保证容易排版的文档不比线性扫描多测：先测原顺序第一个
    候选（达标即定案），再测第一组最紧凑的组合（达标则只在组内二分）。

    已知局限：审计只覆盖实际测量过的组合。若两个都未被测量的组合之间存在
    单调性破坏，本搜索可能选到比穷举更靠后的组合；它仍然通过了真实测量。

    "没有任何组合达标"这一结论不由本函数给出。二分只测每组最紧凑的组合，
    据此断定无解会把本可排版的文档误报为失败，因此这种情况一律返回
    linear-fallback，由调用方用完整线性扫描确认。
    """

    observed: dict[tuple[int, int], int] = {}
    violation = ""
    if not groups:
        return None, "linear-fallback", "no-typography-candidates"

    def probe(group_index: int, item_index: int) -> dict | None:
        nonlocal violation
        result = evaluate(group_index, item_index)
        if result is None:
            return None
        pages = result.get("page_count")
        if not isinstance(pages, int):
            return result
        observed[(group_index, item_index)] = pages
        for (other_group, other_item), other_pages in observed.items():
            if other_group == group_index:
                if other_item < item_index and other_pages < pages:
                    violation = "page-count-not-monotonic-within-leading"
                elif other_item > item_index and other_pages > pages:
                    violation = "page-count-not-monotonic-within-leading"
                continue
            last_item = len(groups[group_index]) - 1
            other_last = len(groups[other_group]) - 1
            if item_index != last_item or other_item != other_last:
                continue
            if other_group < group_index and other_pages < pages:
                violation = "page-count-not-monotonic-across-leading"
            elif other_group > group_index and other_pages > pages:
                violation = "page-count-not-monotonic-across-leading"
        return result

    first = probe(0, 0)
    if first is None:
        return None, "linear-fallback", "render-failed-during-search"
    if first["fits"]:
        return (0, 0), "bounded-binary", ""

    target_group: int | None = None
    leading_group = probe(0, len(groups[0]) - 1)
    if leading_group is None:
        return None, "linear-fallback", "render-failed-during-search"
    if leading_group["fits"]:
        target_group = 0

    low = 1
    high = len(groups) - 1 if target_group is None else 0
    while low <= high:
        middle = (low + high) // 2
        result = probe(middle, len(groups[middle]) - 1)
        if result is None:
            return None, "linear-fallback", "render-failed-during-search"
        if result["fits"]:
            target_group = middle
            high = middle - 1
        else:
            low = middle + 1
    if violation:
        return None, "linear-fallback", violation
    if target_group is None:
        return None, "linear-fallback", "no-feasible-group-verify-exhaustively"

    low = 0
    high = len(groups[target_group]) - 1
    target_item = high
    while low <= high:
        middle = (low + high) // 2
        result = probe(target_group, middle)
        if result is None:
            return None, "linear-fallback", "render-failed-during-search"
        if result["fits"]:
            target_item = middle
            high = middle - 1
        else:
            low = middle + 1
    if violation:
        return None, "linear-fallback", violation

    if target_item > 0:
        previous = probe(target_group, target_item - 1)
    elif target_group > 0:
        previous = probe(target_group - 1, len(groups[target_group - 1]) - 1)
    else:
        previous = None
    if violation:
        return None, "linear-fallback", violation
    if previous is not None and previous["fits"]:
        return None, "linear-fallback", "earlier-candidate-also-fits"
    return (target_group, target_item), "bounded-binary", ""


def select_document_typography(
    page_profiles: Iterable[PageTextProfile],
    measure_page: MeasurePage,
    *,
    body_font_range_pt: tuple[float, float],
    body_font_step_pt: float,
    leading_range: tuple[float, float],
    leading_step: float,
    selection_priority: str = "leading-then-font",
    max_densest_fill_ratio: float = 1.0,
) -> dict:
    profiles = list(page_profiles)
    if not profiles:
        raise TypographyFitError("没有可用于文档级字号计算的普通正文页")
    if len({profile.page for profile in profiles}) != len(profiles):
        raise TypographyFitError("普通正文页画像存在重复页码")
    if not 0 < max_densest_fill_ratio <= 1:
        raise TypographyFitError("最密页舒适填充率必须在 0 到 1 之间")

    body_lower, body_upper = body_font_range_pt
    leading_lower, leading_upper = leading_range
    candidates = flatten_candidates(
        candidate_groups(
            body_font_range_pt=body_font_range_pt,
            body_font_step_pt=body_font_step_pt,
            leading_range=leading_range,
            leading_step=leading_step,
            selection_priority=selection_priority,
        )
    )

    ordered_profiles = sorted(
        profiles,
        key=lambda profile: (
            profile.estimated_density,
            profile.translated_chars,
        ),
        reverse=True,
    )
    tested_candidates = 0
    failed_candidates: list[dict] = []
    for body_size, leading_ratio in candidates:
        tested_candidates += 1
        measurements: list[PageFitMeasurement] = []
        failed_measurement: PageFitMeasurement | None = None
        for profile in ordered_profiles:
            measurement = measure_page(profile, body_size, leading_ratio)
            if measurement.page != profile.page:
                raise TypographyFitError(
                    "测量回调返回的页码与页面画像不一致"
                )
            measurements.append(measurement)
            if not measurement.fits or measurement.has_orphan_line:
                failed_measurement = measurement
                break
        if failed_measurement is not None:
            if len(failed_candidates) < 24:
                failed_candidates.append(
                    {
                        "body_font_pt": body_size,
                        "leading_ratio": leading_ratio,
                        "first_failed_page": failed_measurement.page,
                        "fill_ratio": round(
                            failed_measurement.fill_ratio,
                            4,
                        ),
                        "has_orphan_line": (
                            failed_measurement.has_orphan_line
                        ),
                    }
                )
            continue

        densest = max(measurements, key=lambda item: item.fill_ratio)
        if densest.fill_ratio > max_densest_fill_ratio:
            if len(failed_candidates) < 24:
                failed_candidates.append(
                    {
                        "body_font_pt": body_size,
                        "leading_ratio": leading_ratio,
                        "first_failed_page": densest.page,
                        "fill_ratio": round(densest.fill_ratio, 4),
                        "has_orphan_line": False,
                        "reason": "densest-page-comfort-limit",
                    }
                )
            continue
        widest = max(measurements, key=lambda item: item.content_width_pt)
        page_profile_payload = [
            {
                **asdict(profile),
                "estimated_density": round(profile.estimated_density, 8),
            }
            for profile in sorted(profiles, key=lambda item: item.page)
        ]
        measurement_payload = [
            asdict(measurement)
            for measurement in sorted(
                measurements,
                key=lambda item: item.page,
            )
        ]
        return {
            "algorithm": "translated-page-fit-v1",
            "selection_method": "densest-page-fit",
            "selection_priority": selection_priority,
            "body_font_pt": round(body_size, 3),
            "leading_ratio": round(leading_ratio, 3),
            "body_font_range_pt": [
                round(body_lower, 3),
                round(body_upper, 3),
            ],
            "body_font_step_pt": round(body_font_step_pt, 3),
            "leading_range": [
                round(leading_lower, 3),
                round(leading_upper, 3),
            ],
            "leading_step": round(leading_step, 3),
            "max_densest_fill_ratio": round(
                max_densest_fill_ratio,
                4,
            ),
            "tested_candidate_count": tested_candidates,
            "selected_at_body_font_upper_bound": (
                abs(body_size - body_upper) < body_font_step_pt / 2
            ),
            "densest_page": densest.page,
            "densest_fill_ratio": round(densest.fill_ratio, 4),
            "widest_body_page": widest.page,
            "widest_body_width_pt": round(widest.content_width_pt, 3),
            "total_translated_chars": sum(
                profile.translated_chars for profile in profiles
            ),
            "page_profiles": page_profile_payload,
            "page_measurements": measurement_payload,
            "failed_candidate_sample": failed_candidates,
        }

    raise TypographyFitError(
        "全篇统一正文字号无法在批准版心内排下；应调整分页、版心或内容结构，"
        "不得逐页缩小字号。"
    )
