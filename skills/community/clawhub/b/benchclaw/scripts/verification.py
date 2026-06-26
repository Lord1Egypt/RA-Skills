from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Iterable

logger = logging.getLogger("benchclaw.verification")


@dataclass(frozen=True)
class RuleResult:
    rule_type: str
    target: str
    passed: bool
    awarded: int
    expected: int
    details: str = ""


@dataclass(frozen=True)
class PenaltyResult:
    rule_type: str
    target: str
    triggered: bool
    deduction: int
    fatal: bool
    details: str = ""


@dataclass(frozen=True)
class VerificationResult:
    target_type: str
    target_path: str
    description: str
    exists: bool
    exist_awarded: int
    content_score: int
    penalties: list[PenaltyResult]
    rule_results: list[RuleResult]

    @property
    def penalty_deduction(self) -> int:
        return sum(p.deduction for p in self.penalties if p.triggered)

    @property
    def fatal_triggered(self) -> bool:
        return any(p.triggered and p.fatal for p in self.penalties)

    @property
    def total(self) -> int:
        # 扣分不在这里结算，交给上层统一处理（避免重复扣）
        return self.exist_awarded + self.content_score


@dataclass(frozen=True)
class MetricExtractorResult:
    metric_name: str
    target_file: str
    regex: str
    value_type: str
    extracted_value: str | int | float | None
    extraction_success: bool
    details: str = ""


@dataclass(frozen=True)
class TaskVerificationResult:
    question_id: str
    max_score: int
    score_before_penalty: int
    penalty_deduction: int
    fatal: bool
    score: int
    verifications: list[VerificationResult]
    metrics: list[MetricExtractorResult] | None = None


_REGEX_META = set(r".^$*+?{}[]\|()")


def _looks_like_regex(spec: str) -> bool:
    # 题库里同时存在纯路径与 regex（例如 bench_claw/fibonacci\.py$）
    return any(ch in _REGEX_META for ch in spec)


def _normalize_rel_path(path: str) -> str:
    # 统一用 / 做匹配与输出（题库文件路径也用 /）
    return path.replace("\\", "/").lstrip("./")


def _iter_candidate_files(base_dir: str) -> Iterable[str]:
    for root, _dirs, files in os.walk(base_dir):
        for name in files:
            yield os.path.join(root, name)


def resolve_file_paths(workspace_dir: str, file_path_spec: str) -> list[str]:
    """
    将题库中的 file_path 解析为真实存在的文件路径列表（workspace_dir 绝对路径）。

    - 若 spec 看起来是纯路径：直接拼接并返回（存在与否由上层判断）
    - 若 spec 看起来是 regex：在尽可能小的目录范围内 walk 并匹配
    """
    spec = _normalize_rel_path(file_path_spec)

    if not _looks_like_regex(spec):
        return [os.path.join(workspace_dir, spec)]

    # 尝试缩小搜索范围：取到第一个 regex 元字符之前的"安全前缀"
    prefix_chars: list[str] = []
    for ch in spec:
        if ch in _REGEX_META:
            break
        prefix_chars.append(ch)
    prefix = "".join(prefix_chars)
    search_dir_rel = os.path.dirname(prefix) if prefix else ""
    search_dir = os.path.join(workspace_dir, search_dir_rel)
    if not os.path.isdir(search_dir):
        search_dir = workspace_dir

    pattern = re.compile(spec)
    matches: list[str] = []
    for abs_path in _iter_candidate_files(search_dir):
        rel = _normalize_rel_path(os.path.relpath(abs_path, workspace_dir))
        if pattern.search(rel):
            matches.append(abs_path)
    return sorted(matches)


def _read_text_file(path: str, *, max_bytes: int = 2_000_000) -> str:
    # best-effort 读取，避免超大文件拖垮评测；默认最多 2MB
    with open(path, "rb") as f:
        data = f.read(max_bytes + 1)
    if len(data) > max_bytes:
        data = data[:max_bytes]
    return data.decode("utf-8", errors="replace")


def _apply_metric_extractors(
    workspace_dir: str,
    metric_extractors: list[dict[str, Any]] | None,
) -> list[MetricExtractorResult]:
    """
    处理 metric_extractors，从目标文件中提取指标。

    Args:
        workspace_dir: 工作目录
        metric_extractors: 指标提取器配置列表

    Returns:
        MetricExtractorResult 列表
    """
    results: list[MetricExtractorResult] = []

    if not metric_extractors:
        return results

    for extractor in metric_extractors:
        if not isinstance(extractor, dict):
            continue

        metric_name = str(extractor.get("metric_name") or "")
        target_file = str(extractor.get("target_file") or "")
        regex_pattern = str(extractor.get("regex") or "")
        value_type = str(extractor.get("type") or "string")

        if not metric_name or not target_file or not regex_pattern:
            results.append(MetricExtractorResult(
                metric_name=metric_name or "unknown",
                target_file=target_file,
                regex=regex_pattern,
                value_type=value_type,
                extracted_value=None,
                extraction_success=False,
                details="Missing required fields (metric_name, target_file, or regex)",
            ))
            continue

        # 构建完整文件路径
        file_path = os.path.join(workspace_dir, target_file)

        if not os.path.isfile(file_path):
            results.append(MetricExtractorResult(
                metric_name=metric_name,
                target_file=target_file,
                regex=regex_pattern,
                value_type=value_type,
                extracted_value=None,
                extraction_success=False,
                details=f"Target file not found: {file_path}",
            ))
            continue

        try:
            text = _read_text_file(file_path)

            # 执行正则匹配
            match = re.search(regex_pattern, text, flags=re.MULTILINE | re.IGNORECASE)

            if not match:
                results.append(MetricExtractorResult(
                    metric_name=metric_name,
                    target_file=target_file,
                    regex=regex_pattern,
                    value_type=value_type,
                    extracted_value=None,
                    extraction_success=False,
                    details="Regex pattern did not match any content",
                ))
                continue

            # 提取值
            extracted_str = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)

            # 根据类型转换
            extracted_value: str | int | float | None = None
            conversion_success = True

            if value_type == "int":
                try:
                    # 清理字符串中的非数字字符（如逗号、空格等）
                    cleaned = re.sub(r'[^\d.-]', '', extracted_str)
                    extracted_value = int(float(cleaned))
                except (ValueError, TypeError) as e:
                    conversion_success = False
                    details = f"Failed to convert '{extracted_str}' to int: {e}"
            elif value_type == "float":
                try:
                    cleaned = re.sub(r'[^\d.-]', '', extracted_str)
                    extracted_value = float(cleaned)
                except (ValueError, TypeError) as e:
                    conversion_success = False
                    details = f"Failed to convert '{extracted_str}' to float: {e}"
            else:  # string
                extracted_value = extracted_str
                details = f"Extracted string value: {extracted_str}"

            if conversion_success:
                details = f"Successfully extracted {value_type} value: {extracted_value}"

            results.append(MetricExtractorResult(
                metric_name=metric_name,
                target_file=target_file,
                regex=regex_pattern,
                value_type=value_type,
                extracted_value=extracted_value if conversion_success else None,
                extraction_success=conversion_success,
                details=details,
            ))

        except re.error as e:
            results.append(MetricExtractorResult(
                metric_name=metric_name,
                target_file=target_file,
                regex=regex_pattern,
                value_type=value_type,
                extracted_value=None,
                extraction_success=False,
                details=f"Invalid regex pattern: {e}",
            ))
        except Exception as e:
            results.append(MetricExtractorResult(
                metric_name=metric_name,
                target_file=target_file,
                regex=regex_pattern,
                value_type=value_type,
                extracted_value=None,
                extraction_success=False,
                details=f"Extraction error: {e}",
            ))

    return results


def _apply_keyword_match_rule(text: str, rule: dict[str, Any]) -> RuleResult:
    """keyword_match: 检查文本中是否包含指定关键词"""
    required_words = rule.get("required_words", [])
    match_threshold = rule.get("match_threshold", "all")  # "all" 或 "any"
    score = int(rule.get("score") or 0)
    description = str(rule.get("description") or "")

    # 将 required_words 用逗号连接作为 target 参数
    target = ",".join(str(w) for w in required_words) if required_words else ""

    if not required_words:
        return RuleResult("keyword_match", target, True, score, score, "no keywords required")

    matched_words = [word for word in required_words if word in text]

    if match_threshold == "all":
        passed = len(matched_words) == len(required_words)
    else:  # "any"
        passed = len(matched_words) > 0

    details = f"matched={len(matched_words)}/{len(required_words)}, words={matched_words}"
    return RuleResult("keyword_match", target, passed, score if passed else 0, score, details)


def _apply_keyword_frequency_rule(text: str, rule: dict[str, Any]) -> RuleResult:
    """keyword_frequency: 检查关键词出现次数是否满足最小要求"""
    word = str(rule.get("word") or "")
    min_count = int(rule.get("min_count") or 0)
    score = int(rule.get("score") or 0)
    description = str(rule.get("description") or "")

    if not word:
        return RuleResult("keyword_frequency", "", False, 0, score, "no word specified")

    count = text.count(word)
    passed = count >= min_count
    details = f"count={count}, min_count={min_count}"
    return RuleResult("keyword_frequency", word, passed, score if passed else 0, score, details)


def _apply_content_rule(text: str, rule: dict[str, Any]) -> RuleResult:
    rule_type = str(rule.get("rule_type") or "")
    target = str(rule.get("target") or "")
    score = int(rule.get("score") or 0)
    description = str(rule.get("description") or target)

    if rule_type == "contains":
        passed = target in text
        return RuleResult(rule_type, target, passed, score if passed else 0, score)

    if rule_type == "regex_match":
        try:
            passed = re.search(target, text, flags=re.MULTILINE) is not None
        except re.error as e:
            return RuleResult(rule_type, target, False, 0, score, details=f"invalid regex: {e}")
        return RuleResult(rule_type, target, passed, score if passed else 0, score)

    if rule_type == "regex_count":
        min_count = int(rule.get("min_count") or 0)
        try:
            cnt = len(re.findall(target, text, flags=re.MULTILINE))
            passed = cnt >= min_count
        except re.error as e:
            return RuleResult(rule_type, target, False, 0, score, details=f"invalid regex: {e}")
        details = f"count={cnt}, min_count={min_count}"
        return RuleResult(rule_type, target, passed, score if passed else 0, score, details=details)

    if rule_type == "keyword_match":
        return _apply_keyword_match_rule(text, rule)

    if rule_type == "keyword_frequency":
        return _apply_keyword_frequency_rule(text, rule)

    return RuleResult(rule_type, target, False, 0, score, details="unsupported rule_type")


def _apply_penalty_keywords_rule(text: str, rule: dict[str, Any]) -> PenaltyResult:
    """penalty_keywords: 检查是否包含禁用词，触发则扣分"""
    forbidden_words = rule.get("forbidden_words", [])
    deduction = int(rule.get("deduction") or 0)
    fatal = bool(rule.get("fatal") or False)
    description = str(rule.get("description") or "")

    if not forbidden_words:
        return PenaltyResult("penalty_keywords", "", False, 0, fatal)

    triggered_words = [word for word in forbidden_words if word in text]
    triggered = len(triggered_words) > 0

    details = f"forbidden_words_found={triggered_words}" if triggered else ""
    return PenaltyResult("penalty_keywords", description, triggered, deduction if triggered else 0, fatal, details)


def _apply_penalty_regex_rule(text: str, rule: dict[str, Any]) -> PenaltyResult:
    """penalty_regex: 使用正则检查是否触发惩罚规则"""
    target = str(rule.get("target") or "")
    deduction = int(rule.get("deduction") or 0)
    fatal = bool(rule.get("fatal") or False)
    description = str(rule.get("description") or "")

    if not target:
        return PenaltyResult("penalty_regex", "", False, 0, fatal)

    try:
        triggered = re.search(target, text, flags=re.MULTILINE) is not None
    except re.error as e:
        return PenaltyResult("penalty_regex", target, False, 0, fatal, details=f"invalid regex: {e}")

    return PenaltyResult("penalty_regex", description, triggered, deduction if triggered else 0, fatal)


def _apply_penalty_rule(text: str, rule: dict[str, Any]) -> PenaltyResult:
    rule_type = str(rule.get("rule_type") or "")
    target = str(rule.get("target") or "")
    deduction = int(rule.get("deduction") or 0)
    fatal = bool(rule.get("fatal") or False)

    if rule_type == "contains":
        triggered = target in text
        return PenaltyResult(rule_type, target, triggered, deduction if triggered else 0, fatal)

    if rule_type == "regex_match":
        try:
            triggered = re.search(target, text, flags=re.MULTILINE) is not None
        except re.error as e:
            return PenaltyResult(rule_type, target, False, 0, fatal, details=f"invalid regex: {e}")
        return PenaltyResult(rule_type, target, triggered, deduction if triggered else 0, fatal)

    if rule_type == "penalty_keywords":
        return _apply_penalty_keywords_rule(text, rule)

    if rule_type == "penalty_regex":
        return _apply_penalty_regex_rule(text, rule)

    return PenaltyResult(rule_type, target, False, 0, fatal, details="unsupported penalty rule_type")


def _extract_reply_content(workspace_dir: str, target_path: str) -> str:
    """
    从 target_path 提取回复内容。
    target_path 格式如: "output_content.reply" 表示从 agent 输出中提取 reply 字段
    """
    # 目前支持直接从文件读取，或者从 agent_output.json 中解析
    # 默认查找 agent_output.json 文件
    agent_output_path = os.path.join(workspace_dir, "agent_output.json")

    if os.path.exists(agent_output_path):
        try:
            with open(agent_output_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 解析 target_path，如 "output_content.reply"
            parts = target_path.split(".")
            current = data
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return ""

            if isinstance(current, str):
                return current
            return json.dumps(current, ensure_ascii=False)
        except (json.JSONDecodeError, IOError):
            return ""

    # 如果 target_path 指向一个存在的文件，直接读取
    if os.path.isfile(os.path.join(workspace_dir, target_path)):
        return _read_text_file(os.path.join(workspace_dir, target_path))

    return ""


def verify_file_target(
    *,
    workspace_dir: str,
    verification: dict[str, Any],
) -> VerificationResult:
    """验证文件类型的目标"""
    description = str(verification.get("description") or "")
    spec_path = str(verification.get("target_path") or "")
    exist_score = int(verification.get("exist_score") or 0)
    content_rules = verification.get("content_rules") or []
    penalty_rules = verification.get("penalty_rules") or []

    logger.info(f"[verify_file] workspace_dir={workspace_dir}, target_path={spec_path}, description={description}")

    resolved_paths = resolve_file_paths(workspace_dir, spec_path)
    logger.info(f"[verify_file] resolved_paths={resolved_paths}")

    existing = [p for p in resolved_paths if os.path.isfile(p)]
    exists = len(existing) > 0
    exist_awarded = exist_score if exists else 0

    logger.info(f"[verify_file] file_exists={exists}, exist_score={exist_score}, exist_awarded={exist_awarded}")

    rule_results: list[RuleResult] = []
    penalties: list[PenaltyResult] = []
    content_score = 0

    if exists:
        # 多个匹配文件时：取"得分最高"的那个（更符合 regex file_path 的语义）
        best_rule_results: list[RuleResult] = []
        best_penalties: list[PenaltyResult] = []
        best_content_score = -1

        for path in existing:
            text = _read_text_file(path)

            cur_rule_results = []
            cur_content_score = 0
            if isinstance(content_rules, list):
                for idx, r in enumerate(content_rules):
                    if isinstance(r, dict):
                        rr = _apply_content_rule(text, r)
                        cur_rule_results.append(rr)
                        cur_content_score += rr.awarded
                        # 记录每个 content_rule 的验证结果
                        status = "PASS" if rr.passed else "FAIL"
                        logger.info(f"[verify_file] content_rule[{idx}] {status}: type={rr.rule_type}, target={rr.target}, awarded={rr.awarded}/{rr.expected}, details={rr.details}")

            cur_penalties = []
            if isinstance(penalty_rules, list):
                for idx, r in enumerate(penalty_rules):
                    if isinstance(r, dict):
                        pr = _apply_penalty_rule(text, r)
                        cur_penalties.append(pr)
                        # 记录每个 penalty_rule 的验证结果
                        status = "TRIGGERED" if pr.triggered else "OK"
                        logger.info(f"[verify_file] penalty_rule[{idx}] {status}: type={pr.rule_type}, target={pr.target}, deduction={pr.deduction}, fatal={pr.fatal}")

            if cur_content_score > best_content_score:
                best_content_score = cur_content_score
                best_rule_results = cur_rule_results
                best_penalties = cur_penalties

        rule_results = best_rule_results
        penalties = best_penalties
        content_score = max(0, best_content_score)

    logger.info(f"[verify_file] total_content_score={content_score}, total_penalties={len([p for p in penalties if p.triggered])}")

    return VerificationResult(
        target_type="file",
        target_path=spec_path,
        description=description,
        exists=exists,
        exist_awarded=exist_awarded,
        content_score=content_score,
        penalties=penalties,
        rule_results=rule_results,
    )


def verify_reply_target(
    *,
    workspace_dir: str,
    verification: dict[str, Any],
    stdout_content: str = "",
) -> VerificationResult:
    """验证回复类型的目标

    Args:
        workspace_dir: 工作目录
        verification: 验证配置
        stdout_content: Agent 输出的 stdout 内容（直接传递，优先于文件读取）
    """
    description = str(verification.get("description") or "")
    target_path = str(verification.get("target_path") or "")
    exist_score = int(verification.get("exist_score") or 0)
    content_rules = verification.get("content_rules") or []
    penalty_rules = verification.get("penalty_rules") or []

    logger.info(f"[verify_reply] target_path={target_path}, description={description}")

    # 提取回复内容：优先使用传入的 stdout_content，否则从文件获取
    reply_content = stdout_content if stdout_content else _extract_reply_content(workspace_dir, target_path)
    exists = bool(reply_content)
    exist_awarded = exist_score if exists else 0

    logger.info(f"[verify_reply] content_exists={exists}, exist_score={exist_score}, exist_awarded={exist_awarded}, content_length={len(reply_content) if reply_content else 0}")

    rule_results: list[RuleResult] = []
    penalties: list[PenaltyResult] = []
    content_score = 0

    if exists:
        if isinstance(content_rules, list):
            for idx, r in enumerate(content_rules):
                if isinstance(r, dict):
                    rr = _apply_content_rule(reply_content, r)
                    rule_results.append(rr)
                    content_score += rr.awarded
                    # 记录每个 content_rule 的验证结果
                    status = "PASS" if rr.passed else "FAIL"
                    logger.info(f"[verify_reply] content_rule[{idx}] {status}: type={rr.rule_type}, target={rr.target}, awarded={rr.awarded}/{rr.expected}, details={rr.details}")

        if isinstance(penalty_rules, list):
            for idx, r in enumerate(penalty_rules):
                if isinstance(r, dict):
                    pr = _apply_penalty_rule(reply_content, r)
                    penalties.append(pr)
                    # 记录每个 penalty_rule 的验证结果
                    status = "TRIGGERED" if pr.triggered else "OK"
                    logger.info(f"[verify_reply] penalty_rule[{idx}] {status}: type={pr.rule_type}, target={pr.target}, deduction={pr.deduction}, fatal={pr.fatal}")

    logger.info(f"[verify_reply] total_content_score={content_score}, total_penalties={len([p for p in penalties if p.triggered])}")

    return VerificationResult(
        target_type="reply",
        target_path=target_path,
        description=description,
        exists=exists,
        exist_awarded=exist_awarded,
        content_score=content_score,
        penalties=penalties,
        rule_results=rule_results,
    )


def verify_single_verification(
    *,
    workspace_dir: str,
    verification: dict[str, Any],
    stdout_content: str = "",
) -> VerificationResult:
    """根据 target_type 路由到对应的验证函数

    Args:
        workspace_dir: 工作目录
        verification: 验证配置
        stdout_content: Agent 输出的 stdout 内容（用于 reply 类型验证）
    """
    target_type = str(verification.get("target_type") or "file")

    if target_type == "file":
        return verify_file_target(workspace_dir=workspace_dir, verification=verification)
    elif target_type == "reply":
        return verify_reply_target(workspace_dir=workspace_dir, verification=verification, stdout_content=stdout_content)
    elif target_type == "mixed":
        # mixed 类型：同时验证文件和回复
        # 先尝试验证文件，如果没有匹配再验证回复
        file_result = verify_file_target(workspace_dir=workspace_dir, verification=verification)
        if file_result.exists:
            return file_result
        return verify_reply_target(workspace_dir=workspace_dir, verification=verification, stdout_content=stdout_content)
    else:
        # 未知类型，默认按 file 处理
        return verify_file_target(workspace_dir=workspace_dir, verification=verification)


def verify_task_answer(
    *,
    workspace_dir: str,
    question_id: str,
    answer: dict[str, Any],
    stdout_content: str = "",
) -> TaskVerificationResult:
    """验证任务答案（支持新的 verifications 数组结构）

    Args:
        workspace_dir: 工作目录
        question_id: 题目ID
        answer: 答案配置
        stdout_content: Agent 输出的 stdout 内容（用于 reply 类型验证）
    """
    max_score = int(answer.get("max_score") or 0)

    verifications = answer.get("verifications") or []

    logger.info(f"[verify_task] question_id={question_id}, max_score={max_score}, verifications_count={len(verifications)}, workspace_dir={workspace_dir}")

    verification_results: list[VerificationResult] = []
    for idx, v in enumerate(verifications):
        if isinstance(v, dict):
            target_type = str(v.get("target_type") or "file")
            target_path = str(v.get("target_path") or "")
            description = str(v.get("description") or "")

            logger.info(f"[verify_task] processing verification[{idx}]: type={target_type}, path={target_path}, desc={description}")

            result = verify_single_verification(workspace_dir=workspace_dir, verification=v, stdout_content=stdout_content)
            verification_results.append(result)

            # 记录每个 verification 的汇总结果
            status = "PASS" if result.exists else "MISSING"
            logger.info(f"[verify_task] verification[{idx}] {status}: target_type={result.target_type}, exists={result.exists}, "
                       f"exist_awarded={result.exist_awarded}, content_score={result.content_score}, "
                       f"penalties={len(result.penalties)}, total={result.total}")

            # 详细记录 rule_results
            for ridx, rr in enumerate(result.rule_results):
                status = "PASS" if rr.passed else "FAIL"
                logger.info(f"[verify_task] verification[{idx}] rule[{ridx}] {status}: {rr.rule_type}, target={rr.target}, "
                           f"awarded={rr.awarded}/{rr.expected}, details={rr.details}")

            # 详细记录 penalties
            for pidx, pr in enumerate(result.penalties):
                if pr.triggered:
                    logger.info(f"[verify_task] verification[{idx}] penalty[{pidx}] TRIGGERED: {pr.rule_type}, target={pr.target}, "
                               f"deduction={pr.deduction}, fatal={pr.fatal}")

    score_before_penalty = sum(vr.total for vr in verification_results)
    penalty_deduction = sum(vr.penalty_deduction for vr in verification_results)
    fatal = any(vr.fatal_triggered for vr in verification_results)

    if fatal:
        final_score = 0
    else:
        final_score = max(0, min(max_score, score_before_penalty - penalty_deduction))

    # 处理 metric_extractors
    metric_extractors = answer.get("metric_extractors")
    metrics_results = _apply_metric_extractors(workspace_dir, metric_extractors)

    if metrics_results:
        logger.info(f"[verify_task] question_id={question_id} METRICS: extracted {len(metrics_results)} metrics")
        for mr in metrics_results:
            status = "SUCCESS" if mr.extraction_success else "FAILED"
            logger.info(f"[verify_task] metric '{mr.metric_name}': {status}, value={mr.extracted_value}, details={mr.details}")

    logger.info(f"[verify_task] question_id={question_id} SUMMARY: max_score={max_score}, "
               f"score_before_penalty={score_before_penalty}, penalty_deduction={penalty_deduction}, "
               f"fatal={fatal}, final_score={final_score}")

    return TaskVerificationResult(
        question_id=question_id,
        max_score=max_score,
        score_before_penalty=score_before_penalty,
        penalty_deduction=penalty_deduction,
        fatal=fatal,
        score=final_score,
        verifications=verification_results,
        metrics=metrics_results if metrics_results else None,
    )


def verify_question_from_questions_json(
    *,
    questions_json_path: str,
    workspace_dir: str,
    question_id: str,
    stdout_content: str = "",
) -> TaskVerificationResult:
    """
    从 questions.json（服务端拉下来的全量题库 JSON）里按 question_id 查找并验证。

    Args:
        questions_json_path: 题库 JSON 文件路径
        workspace_dir: 工作目录
        question_id: 题目ID
        stdout_content: Agent 输出的 stdout 内容（用于 reply 类型验证）
    """
    with open(questions_json_path, "r", encoding="utf-8") as f:
        obj = json.load(f)

    # 使用标准结构: { success, data: { questions: [...] } }
    if not isinstance(obj, dict) or not isinstance(obj.get("data"), dict) or not isinstance(obj["data"].get("questions"), list):
        raise ValueError("unrecognized questions.json structure: expected { success, data: { questions: [...] } }")

    questions: list[Any] = obj["data"]["questions"]

    for q in questions:
        if not isinstance(q, dict):
            continue
        if str(q.get("id") or "") != question_id:
            continue
        answer = q.get("answer")
        if not isinstance(answer, dict):
            raise ValueError(f"question {question_id} missing answer")
        return verify_task_answer(workspace_dir=workspace_dir, question_id=question_id, answer=answer, stdout_content=stdout_content)

    raise KeyError(f"question_id not found: {question_id}")


if __name__ == "__main__":
    verify_question_from_questions_json()
