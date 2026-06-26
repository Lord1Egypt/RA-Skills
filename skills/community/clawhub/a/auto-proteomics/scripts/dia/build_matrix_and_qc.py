#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import median

CONTRACT_FAMILY = "header-sample-matrix-v1"
CONTRACT_VERSION = "1.0"
SUPPORTED_DECLARED_INPUT_FORMATS = {CONTRACT_FAMILY, "generic-tsv"}
FEATURE_ID_CANDIDATES = ["feature_id", "Protein.Group", "ProteinName", "PG.ProteinGroups", "Protein"]


class ContractValidationError(Exception):
    def __init__(self, code: str, message: str, *, details: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a minimal DIA prototype quant matrix and basic QC summaries from one explicit contract family."
    )
    parser.add_argument("--input-table", required=True)
    parser.add_argument("--sample-sheet", required=True)
    parser.add_argument("--sample-id-column", required=True)
    parser.add_argument("--group-column", required=True)
    parser.add_argument("--feature-id-column", required=True)
    parser.add_argument("--delimiter", default="auto")
    parser.add_argument("--output-matrix", required=True)
    parser.add_argument("--output-filtered-matrix", required=True)
    parser.add_argument("--output-sample-metadata", required=True)
    parser.add_argument("--output-detected-columns", required=True)
    parser.add_argument("--output-sample-qc", required=True)
    parser.add_argument("--output-feature-qc", required=True)
    parser.add_argument("--output-filtering-report", required=True)
    parser.add_argument("--output-qc-summary", required=True)
    parser.add_argument("--output-normalized-matrix", required=True)
    parser.add_argument("--output-log-normalized-matrix", required=True)
    parser.add_argument("--output-normalization-summary", required=True)
    parser.add_argument("--output-normalization-qc", required=True)
    parser.add_argument("--output-input-summary", required=True)
    parser.add_argument("--output-format-diagnostics", required=True)
    parser.add_argument("--output-contract-report", required=True)
    parser.add_argument("--input-format", required=True)
    parser.add_argument("--declared-input-format", required=True)
    parser.add_argument("--quant-level", required=True)
    parser.add_argument("--max-missing-rate", type=float, default=0.5)
    parser.add_argument("--allow-partial-match", action="store_true")
    return parser.parse_args()


def choose_delimiter(path: Path, mode: str) -> str:
    if mode == "tab":
        return "\t"
    if mode == "comma":
        return ","
    return "," if path.suffix.lower() == ".csv" else "\t"


def read_table(path_str: str, mode: str):
    path = Path(path_str)
    delimiter = choose_delimiter(path, mode)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    return delimiter, fieldnames, rows


def ordered_feature_candidates(preferred: str) -> list[str]:
    candidates: list[str] = []
    for candidate in [preferred] + FEATURE_ID_CANDIDATES:
        if candidate and candidate not in candidates:
            candidates.append(candidate)
    return candidates


def detect_feature_column(table_fields: list[str], preferred: str) -> str:
    candidates = ordered_feature_candidates(preferred)
    for candidate in candidates:
        if candidate in table_fields:
            return candidate
    if not table_fields:
        raise ContractValidationError("input-table-no-columns", "Input table has no columns")
    return table_fields[0]


def parse_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    lowered = text.lower()
    if lowered in {"na", "nan", "null", "none", "inf", "+inf", "-inf"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def compute_sample_qc(table_rows: list[dict[str, str]], quant_columns: list[str]) -> list[dict[str, object]]:
    qc_rows = []
    for sample_id in quant_columns:
        numeric_values = []
        missing_count = 0
        non_numeric_count = 0
        for row in table_rows:
            raw = row.get(sample_id, "")
            if not (raw or "").strip():
                missing_count += 1
                continue
            value = parse_float(raw)
            if value is None:
                non_numeric_count += 1
                continue
            numeric_values.append(value)
        total_features = len(table_rows)
        detected_features = len(numeric_values)
        detection_rate = (detected_features / total_features) if total_features else 0.0
        qc_rows.append(
            {
                "sample_id": sample_id,
                "total_features": total_features,
                "detected_features": detected_features,
                "missing_values": missing_count,
                "non_numeric_values": non_numeric_count,
                "detection_rate": round(detection_rate, 4),
                "min_intensity": min(numeric_values) if numeric_values else "",
                "median_intensity": round(median(numeric_values), 6) if numeric_values else "",
                "max_intensity": max(numeric_values) if numeric_values else "",
            }
        )
    return qc_rows


def compute_feature_qc(
    table_rows: list[dict[str, str]], feature_column: str, quant_columns: list[str]
) -> tuple[list[dict[str, object]], dict[str, object]]:
    qc_rows = []
    total_features = len(table_rows)
    fully_missing_features = 0
    complete_features = 0
    partial_missing_features = 0
    for row in table_rows:
        feature_id = row.get(feature_column, "")
        numeric_values = []
        missing_count = 0
        non_numeric_count = 0
        for sample_id in quant_columns:
            raw = row.get(sample_id, "")
            if not (raw or "").strip():
                missing_count += 1
                continue
            value = parse_float(raw)
            if value is None:
                non_numeric_count += 1
                continue
            numeric_values.append(value)
        detected_sample_count = len(numeric_values)
        total_sample_count = len(quant_columns)
        missing_total = missing_count + non_numeric_count
        missing_rate = (missing_total / total_sample_count) if total_sample_count else 0.0
        if missing_total == total_sample_count:
            fully_missing_features += 1
        elif missing_total == 0:
            complete_features += 1
        else:
            partial_missing_features += 1
        qc_rows.append(
            {
                "feature_id": feature_id,
                "total_samples": total_sample_count,
                "detected_samples": detected_sample_count,
                "missing_values": missing_count,
                "non_numeric_values": non_numeric_count,
                "missing_rate": round(missing_rate, 4),
                "min_intensity": min(numeric_values) if numeric_values else "",
                "mean_intensity": round(sum(numeric_values) / detected_sample_count, 6) if numeric_values else "",
                "median_intensity": round(median(numeric_values), 6) if numeric_values else "",
                "max_intensity": max(numeric_values) if numeric_values else "",
            }
        )

    summary = {
        "feature_count": total_features,
        "complete_features": complete_features,
        "partial_missing_features": partial_missing_features,
        "fully_missing_features": fully_missing_features,
        "missingness_rate_mean": round(
            (sum(row["missing_rate"] for row in qc_rows) / total_features) if total_features else 0.0,
            4,
        ),
        "features_with_any_missing": partial_missing_features + fully_missing_features,
    }
    return qc_rows, summary


def apply_prototype_filter(
    table_rows: list[dict[str, str]],
    feature_qc_rows: list[dict[str, object]],
    feature_column: str,
    quant_columns: list[str],
    *,
    max_missing_rate: float,
) -> tuple[list[dict[str, str]], list[dict[str, object]], dict[str, object]]:
    keep_lookup: dict[str, bool] = {}
    report_rows: list[dict[str, object]] = []
    kept = 0
    dropped = 0

    for row in feature_qc_rows:
        feature_id = str(row["feature_id"])
        missing_rate = float(row["missing_rate"])
        detected_samples = int(row["detected_samples"])
        keep = detected_samples > 0 and missing_rate <= max_missing_rate
        decision_reason = "keep" if keep else "drop-high-missingness-or-no-detection"
        keep_lookup[feature_id] = keep
        report_rows.append(
            {
                "feature_id": feature_id,
                "missing_rate_threshold": round(max_missing_rate, 4),
                "missing_rate": round(missing_rate, 4),
                "detected_samples": detected_samples,
                "filter_decision": "keep" if keep else "drop",
                "decision_reason": decision_reason,
            }
        )
        if keep:
            kept += 1
        else:
            dropped += 1

    filtered_rows = [row for row in table_rows if keep_lookup.get(str(row.get(feature_column, "")), False)]
    summary = {
        "filter_rule": "prototype-missingness-threshold",
        "max_missing_rate": round(max_missing_rate, 4),
        "input_feature_count": len(table_rows),
        "kept_features": kept,
        "dropped_features": dropped,
    }
    return filtered_rows, report_rows, summary


def summarize_sample_median_alignment(sample_rows: list[dict[str, object]], target_median: float | None) -> dict[str, object]:
    aligned_post_medians = []
    aligned_pre_medians = []
    residuals = []
    for row in sample_rows:
        pre_value = row["pre_median_intensity"]
        post_value = row["post_median_intensity"]
        if pre_value != "":
            aligned_pre_medians.append(float(pre_value))
        if post_value != "":
            post_float = float(post_value)
            aligned_post_medians.append(post_float)
            if target_median is not None:
                residuals.append(abs(post_float - target_median))

    def spread(values: list[float]) -> float | None:
        if not values:
            return None
        return max(values) - min(values)

    pre_spread = spread(aligned_pre_medians)
    post_spread = spread(aligned_post_medians)
    improvement = None
    if pre_spread is not None and post_spread is not None:
        improvement = pre_spread - post_spread

    return {
        "diagnostic_status": "prototype-descriptive-only",
        "samples_evaluated": len(aligned_post_medians),
        "pre_sample_median_range": round(pre_spread, 6) if pre_spread is not None else None,
        "post_sample_median_range": round(post_spread, 6) if post_spread is not None else None,
        "median_range_reduction": round(improvement, 6) if improvement is not None else None,
        "max_post_alignment_error": round(max(residuals), 6) if residuals else None,
        "mean_post_alignment_error": round(sum(residuals) / len(residuals), 6) if residuals else None,
        "limitations": [
            "describes sample-median alignment only",
            "does not validate biological comparability",
            "does not assess replicate variance or batch effects",
        ],
    }


def compute_normalization_preview(
    filtered_rows: list[dict[str, str]], feature_column: str, quant_columns: list[str]
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    sample_medians: dict[str, float | None] = {}
    sample_counts: dict[str, int] = {}
    for sample_id in quant_columns:
        numeric_values = []
        for row in filtered_rows:
            value = parse_float(row.get(sample_id, ""))
            if value is None or value <= 0:
                continue
            numeric_values.append(value)
        sample_counts[sample_id] = len(numeric_values)
        sample_medians[sample_id] = median(numeric_values) if numeric_values else None

    usable_sample_medians = [value for value in sample_medians.values() if value is not None and value > 0]
    target_median = median(usable_sample_medians) if usable_sample_medians else None

    scale_factors: dict[str, float | None] = {}
    for sample_id in quant_columns:
        sample_median = sample_medians[sample_id]
        if target_median is None or sample_median is None or sample_median <= 0:
            scale_factors[sample_id] = None
        else:
            scale_factors[sample_id] = target_median / sample_median

    normalized_rows: list[dict[str, object]] = []
    for row in filtered_rows:
        normalized_row: dict[str, object] = {feature_column: row.get(feature_column, "")}
        for sample_id in quant_columns:
            raw = row.get(sample_id, "")
            value = parse_float(raw)
            factor = scale_factors[sample_id]
            if value is None or factor is None:
                normalized_row[sample_id] = raw
            else:
                normalized_row[sample_id] = round(value * factor, 6)
        normalized_rows.append(normalized_row)

    sample_rows: list[dict[str, object]] = []
    for sample_id in quant_columns:
        factor = scale_factors[sample_id]
        before_median = sample_medians[sample_id]
        after_median = (before_median * factor) if before_median is not None and factor is not None else None
        sample_rows.append(
            {
                "sample_id": sample_id,
                "features_used": sample_counts[sample_id],
                "pre_median_intensity": round(before_median, 6) if before_median is not None else "",
                "normalization_factor": round(factor, 6) if factor is not None else "",
                "post_median_intensity": round(after_median, 6) if after_median is not None else "",
                "normalization_status": "preview-scaled" if factor is not None else "insufficient-data",
            }
        )

    normalization_qc_rows: list[dict[str, object]] = []
    for row in sample_rows:
        pre_value = row["pre_median_intensity"]
        post_value = row["post_median_intensity"]
        pre_float = float(pre_value) if pre_value != "" else None
        post_float = float(post_value) if post_value != "" else None
        pre_error = abs(pre_float - target_median) if pre_float is not None and target_median is not None else None
        post_error = abs(post_float - target_median) if post_float is not None and target_median is not None else None
        normalization_qc_rows.append(
            {
                "sample_id": row["sample_id"],
                "features_used": row["features_used"],
                "pre_median_intensity": pre_value,
                "post_median_intensity": post_value,
                "target_global_median": round(target_median, 6) if target_median is not None else "",
                "normalization_factor": row["normalization_factor"],
                "pre_alignment_error": round(pre_error, 6) if pre_error is not None else "",
                "post_alignment_error": round(post_error, 6) if post_error is not None else "",
                "normalization_status": row["normalization_status"],
                "diagnostic_scope": "sample-median-alignment-only",
            }
        )

    alignment_summary = summarize_sample_median_alignment(sample_rows, target_median)
    summary = {
        "method": "prototype-global-median-scaling",
        "stage": "post-filter-preview-only",
        "status": "prototype",
        "support_level": "internal-prototype",
        "public_support": "not-shipped",
        "statistical_claims": "none",
        "normalization_basis": "per-sample median over filtered positive numeric intensities",
        "target_global_median": round(target_median, 6) if target_median is not None else None,
        "filtered_feature_count": len(filtered_rows),
        "matched_sample_count": len(quant_columns),
        "samples_with_scaling": sum(1 for value in scale_factors.values() if value is not None),
        "normalization_qc_scope": "sample-median-alignment-only",
        "normalization_qc_summary": alignment_summary,
        "limitations": [
            "preview only for internal prototype evaluation",
            "not software-specific normalization",
            "not validated for scientific interpretation",
            "uses only filtered positive intensities",
            "does not correct batch effects or composition bias",
            "no statistical claims or downstream testing support",
        ],
        "samples": sample_rows,
    }
    return normalized_rows, sample_rows, normalization_qc_rows, summary


def compute_log2_normalized_preview(
    normalized_rows: list[dict[str, object]], feature_column: str, quant_columns: list[str]
) -> tuple[list[dict[str, object]], dict[str, object]]:
    log_rows: list[dict[str, object]] = []
    transformed_values = 0
    skipped_values = 0

    for row in normalized_rows:
        log_row: dict[str, object] = {feature_column: row.get(feature_column, "")}
        for sample_id in quant_columns:
            value = parse_float(str(row.get(sample_id, "")))
            if value is None or value <= 0:
                log_row[sample_id] = ""
                skipped_values += 1
                continue
            log_row[sample_id] = round(math.log2(value), 6)
            transformed_values += 1
        log_rows.append(log_row)

    summary = {
        "method": "log2-of-prototype-normalized-preview",
        "stage": "post-filter-post-normalization-preview-only",
        "status": "prototype",
        "support_level": "internal-prototype",
        "public_support": "not-shipped",
        "statistical_claims": "none",
        "transform_basis": "log2 applied only to positive values from the prototype normalized preview",
        "pseudocount": None,
        "transformed_value_count": transformed_values,
        "skipped_value_count": skipped_values,
        "limitations": [
            "preview only for internal prototype evaluation",
            "derived from preview-only median scaling output",
            "not software-specific normalization",
            "not validated for scientific interpretation",
            "missing or non-positive values remain blank",
            "no statistical claims or downstream testing support",
        ],
    }
    return log_rows, summary


def base_contract_report(args: argparse.Namespace) -> dict[str, object]:
    return {
        "workflow": "dia-quant",
        "mode": "prototype-technical-minimum",
        "status": "prototype",
        "support_level": "internal-prototype",
        "public_support": "not-shipped",
        "contract_family": CONTRACT_FAMILY,
        "contract_version": CONTRACT_VERSION,
        "declared_input_format": args.declared_input_format,
        "normalized_input_format": args.input_format,
        "quant_level": args.quant_level,
        "validation_status": "running",
        "validation_errors": [],
        "contract_spec": {
            "description": "Single wide processed DIA quant table plus sample sheet with exact sample-header matching.",
            "input_table_shape": "wide-feature-by-sample-matrix",
            "sample_matching_rule": "exact-sample-id-to-header",
            "feature_id_detection_order": ordered_feature_candidates(args.feature_id_column),
            "required_sample_sheet_columns": [args.sample_id_column, args.group_column],
            "supported_delimiters": ["tab", "comma"],
            "long_format_supported": False,
            "software_specific_family": False,
            "notes": [
                "This is the first explicit DIA prototype contract family.",
                "It is narrower than generic processed-table support and should not be described as universal DIA intake.",
            ],
        },
        "input_files": {
            "input_table": str(Path(args.input_table).resolve()),
            "sample_sheet": str(Path(args.sample_sheet).resolve()),
        },
    }


def emit_contract_report(path_str: str, payload: dict[str, object]) -> None:
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_format_diagnostics(
    *,
    table_fields: list[str],
    feature_column: str,
    sample_ids: list[str],
    quant_columns: list[str],
    extra_candidate_columns: list[str],
    unmatched_samples: list[str],
) -> dict[str, object]:
    column_positions = {name: idx for idx, name in enumerate(table_fields)}
    matched_positions = [column_positions[name] for name in quant_columns if name in column_positions]

    first_sample_idx = min(matched_positions) if matched_positions else None
    last_sample_idx = max(matched_positions) if matched_positions else None
    annotation_columns_before_samples = table_fields[:first_sample_idx] if first_sample_idx is not None else []
    columns_after_last_sample = table_fields[last_sample_idx + 1 :] if last_sample_idx is not None else []

    interleaved_non_sample_columns = []
    if first_sample_idx is not None and last_sample_idx is not None:
        for idx in range(first_sample_idx, last_sample_idx + 1):
            column_name = table_fields[idx]
            if column_name not in quant_columns:
                interleaved_non_sample_columns.append(column_name)

    return {
        "contract_family": CONTRACT_FAMILY,
        "contract_version": CONTRACT_VERSION,
        "diagnostic_status": "prototype-structural-only",
        "support_level": "internal-prototype",
        "public_support": "not-shipped",
        "diagnostic_scope": "family-aware export structure checks only",
        "diagnostic_limitations": [
            "does not validate scientific quant quality",
            "does not verify upstream software provenance",
            "does not replace a software-specific parser",
            "does not certify normalization or downstream statistics",
        ],
        "family_assumptions": {
            "description": "single wide quant table plus sample sheet with exact sample-header matching",
            "annotation_columns_expected_before_sample_block": True,
            "sample_block_should_be_contiguous": True,
            "one_quant_column_per_sample": True,
        },
        "feature_id_column": feature_column,
        "sample_sheet_sample_count": len(sample_ids),
        "matched_sample_count": len(quant_columns),
        "unmatched_sample_count": len(unmatched_samples),
        "matched_sample_headers": quant_columns,
        "unmatched_samples": unmatched_samples,
        "table_column_count": len(table_fields),
        "sample_block_starts_at_column_index": first_sample_idx,
        "sample_block_ends_at_column_index": last_sample_idx,
        "sample_block_is_contiguous": bool(matched_positions) and not interleaved_non_sample_columns,
        "annotation_columns_before_first_matched_sample": annotation_columns_before_samples,
        "interleaved_non_sample_columns_within_sample_block": interleaved_non_sample_columns,
        "columns_after_last_matched_sample": columns_after_last_sample,
        "extra_candidate_columns": extra_candidate_columns,
        "agent_interpretation": [
            "use this file only to verify that the export still fits the first explicit intake family",
            "if unmatched samples exist or non-sample columns are interleaved inside the sample block, stop before pretending the export is stable",
            "annotation columns outside the sample block are tolerated as structure, not treated as quant columns",
        ],
    }


def validate_contract(
    args: argparse.Namespace,
    table_delim: str,
    table_fields: list[str],
    table_rows: list[dict[str, str]],
    sheet_delim: str,
    sheet_fields: list[str],
    sheet_rows: list[dict[str, str]],
) -> dict[str, object]:
    if args.input_format != CONTRACT_FAMILY:
        raise ContractValidationError(
            "unsupported-contract-family",
            f"DIA prototype currently validates only '{CONTRACT_FAMILY}'.",
            details={"normalized_input_format": args.input_format},
        )
    if args.declared_input_format not in SUPPORTED_DECLARED_INPUT_FORMATS:
        raise ContractValidationError(
            "unsupported-declared-input-format",
            "Declared input format is outside the checked-in DIA prototype contract aliases.",
            details={
                "declared_input_format": args.declared_input_format,
                "supported_declared_input_formats": sorted(SUPPORTED_DECLARED_INPUT_FORMATS),
            },
        )
    if not table_fields:
        raise ContractValidationError("input-table-no-header", f"Input table has no header: {args.input_table}")
    if not sheet_fields:
        raise ContractValidationError("sample-sheet-no-header", f"Sample sheet has no header: {args.sample_sheet}")
    if args.sample_id_column not in sheet_fields:
        raise ContractValidationError(
            "sample-sheet-missing-sample-id-column",
            f"Sample sheet missing required column: {args.sample_id_column}",
            details={"available_columns": sheet_fields},
        )
    if args.group_column not in sheet_fields:
        raise ContractValidationError(
            "sample-sheet-missing-group-column",
            f"Sample sheet missing required column: {args.group_column}",
            details={"available_columns": sheet_fields},
        )
    if not sheet_rows:
        raise ContractValidationError("sample-sheet-empty", "Sample sheet contains no data rows")
    if not table_rows:
        raise ContractValidationError("input-table-empty", "Input table contains no data rows")
    if not 0.0 <= args.max_missing_rate <= 1.0:
        raise ContractValidationError(
            "invalid-max-missing-rate",
            "--max-missing-rate must be between 0 and 1",
            details={"max_missing_rate": args.max_missing_rate},
        )

    sample_ids = []
    for row_index, row in enumerate(sheet_rows, start=2):
        sample_id = (row.get(args.sample_id_column) or "").strip()
        if not sample_id:
            raise ContractValidationError(
                "blank-sample-id",
                f"Blank sample ID detected in column: {args.sample_id_column}",
                details={"row_index": row_index},
            )
        sample_ids.append(sample_id)
    if len(sample_ids) != len(set(sample_ids)):
        duplicate_ids = sorted({sample_id for sample_id in sample_ids if sample_ids.count(sample_id) > 1})
        raise ContractValidationError(
            "duplicate-sample-id",
            "Duplicate sample IDs found in sample sheet",
            details={"duplicate_sample_ids": duplicate_ids},
        )

    feature_column = detect_feature_column(table_fields, args.feature_id_column)
    matched_pairs = []
    unmatched_samples = []
    for sample_id in sample_ids:
        if sample_id in table_fields:
            matched_pairs.append((sample_id, sample_id, "exact-header-match"))
        else:
            unmatched_samples.append(sample_id)

    quant_columns = [pair[1] for pair in matched_pairs]
    known_annotation = {feature_column, args.sample_id_column, args.group_column}
    extra_candidate_columns = [
        field for field in table_fields if field not in quant_columns and field not in known_annotation
    ]

    if unmatched_samples and not args.allow_partial_match:
        raise ContractValidationError(
            "sample-id-header-mismatch",
            "Sample IDs not found as input-table columns under the first explicit DIA contract family.",
            details={
                "sample_matching_rule": "exact-sample-id-to-header",
                "unmatched_samples": unmatched_samples,
                "hint": "Use exact sample IDs in the table header or rerun with --allow-partial-match for prototype output only.",
            },
        )
    if not quant_columns:
        raise ContractValidationError(
            "no-matched-quant-columns",
            "No matched quant columns found after sample-sheet validation",
            details={"sample_ids": sample_ids},
        )

    return {
        "feature_column": feature_column,
        "sample_ids": sample_ids,
        "matched_pairs": matched_pairs,
        "unmatched_samples": unmatched_samples,
        "quant_columns": quant_columns,
        "extra_candidate_columns": extra_candidate_columns,
        "observed_shape": {
            "input_table_delimiter": "tab" if table_delim == "\t" else "comma",
            "sample_sheet_delimiter": "tab" if sheet_delim == "\t" else "comma",
            "input_table_columns": table_fields,
            "sample_sheet_columns": sheet_fields,
            "row_counts": {
                "input_table": len(table_rows),
                "sample_sheet": len(sheet_rows),
            },
            "matched_samples": len(matched_pairs),
            "unmatched_samples": unmatched_samples,
            "quant_columns": quant_columns,
            "extra_candidate_columns": extra_candidate_columns,
        },
    }


def main() -> int:
    args = parse_args()
    contract_report = base_contract_report(args)

    try:
        table_delim, table_fields, table_rows = read_table(args.input_table, args.delimiter)
        sheet_delim, sheet_fields, sheet_rows = read_table(args.sample_sheet, args.delimiter)

        contract_state = validate_contract(
            args,
            table_delim,
            table_fields,
            table_rows,
            sheet_delim,
            sheet_fields,
            sheet_rows,
        )

        feature_column = contract_state["feature_column"]
        matched_pairs = contract_state["matched_pairs"]
        unmatched_samples = contract_state["unmatched_samples"]
        quant_columns = contract_state["quant_columns"]
        extra_candidate_columns = contract_state["extra_candidate_columns"]
        sample_ids = contract_state["sample_ids"]
        format_diagnostics = build_format_diagnostics(
            table_fields=table_fields,
            feature_column=feature_column,
            sample_ids=sample_ids,
            quant_columns=quant_columns,
            extra_candidate_columns=extra_candidate_columns,
            unmatched_samples=unmatched_samples,
        )

        contract_report["validation_status"] = "passed"
        contract_report["observed_shape"] = contract_state["observed_shape"]
        contract_report["match_policy"] = {
            "allow_partial_match": args.allow_partial_match,
            "matched_pair_count": len(matched_pairs),
            "unmatched_sample_count": len(unmatched_samples),
        }

        output_matrix = Path(args.output_matrix)
        output_matrix.parent.mkdir(parents=True, exist_ok=True)
        with output_matrix.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow([feature_column] + quant_columns)
            for row in table_rows:
                writer.writerow([row.get(feature_column, "")] + [row.get(col, "") for col in quant_columns])

        output_metadata = Path(args.output_sample_metadata)
        output_metadata.parent.mkdir(parents=True, exist_ok=True)
        with output_metadata.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=sheet_fields + ["column_match_status"], delimiter="\t")
            writer.writeheader()
            matched_lookup = {sample_id: status for sample_id, _, status in matched_pairs}
            for row in sheet_rows:
                sample_id = (row.get(args.sample_id_column) or "").strip()
                out = dict(row)
                out["column_match_status"] = matched_lookup.get(sample_id, "missing")
                writer.writerow(out)

        output_detected = Path(args.output_detected_columns)
        output_detected.parent.mkdir(parents=True, exist_ok=True)
        with output_detected.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow(["column_name", "column_role"])
            writer.writerow([feature_column, "feature_id"])
            for column in quant_columns:
                writer.writerow([column, "matched_quant_sample"])
            for column in extra_candidate_columns:
                writer.writerow([column, "unclassified"])

        sample_qc_rows = compute_sample_qc(table_rows, quant_columns)
        output_sample_qc = Path(args.output_sample_qc)
        output_sample_qc.parent.mkdir(parents=True, exist_ok=True)
        with output_sample_qc.open("w", encoding="utf-8", newline="") as handle:
            fields = [
                "sample_id",
                "total_features",
                "detected_features",
                "missing_values",
                "non_numeric_values",
                "detection_rate",
                "min_intensity",
                "median_intensity",
                "max_intensity",
            ]
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            writer.writerows(sample_qc_rows)

        feature_qc_rows, feature_missingness_summary = compute_feature_qc(table_rows, feature_column, quant_columns)
        output_feature_qc = Path(args.output_feature_qc)
        output_feature_qc.parent.mkdir(parents=True, exist_ok=True)
        with output_feature_qc.open("w", encoding="utf-8", newline="") as handle:
            fields = [
                "feature_id",
                "total_samples",
                "detected_samples",
                "missing_values",
                "non_numeric_values",
                "missing_rate",
                "min_intensity",
                "mean_intensity",
                "median_intensity",
                "max_intensity",
            ]
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            writer.writerows(feature_qc_rows)

        filtered_rows, filtering_report_rows, filtering_summary = apply_prototype_filter(
            table_rows,
            feature_qc_rows,
            feature_column,
            quant_columns,
            max_missing_rate=args.max_missing_rate,
        )

        output_filtered_matrix = Path(args.output_filtered_matrix)
        output_filtered_matrix.parent.mkdir(parents=True, exist_ok=True)
        with output_filtered_matrix.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow([feature_column] + quant_columns)
            for row in filtered_rows:
                writer.writerow([row.get(feature_column, "")] + [row.get(col, "") for col in quant_columns])

        output_filtering_report = Path(args.output_filtering_report)
        output_filtering_report.parent.mkdir(parents=True, exist_ok=True)
        with output_filtering_report.open("w", encoding="utf-8", newline="") as handle:
            fields = [
                "feature_id",
                "missing_rate_threshold",
                "missing_rate",
                "detected_samples",
                "filter_decision",
                "decision_reason",
            ]
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            writer.writerows(filtering_report_rows)

        normalized_rows, normalization_sample_rows, normalization_qc_rows, normalization_summary = compute_normalization_preview(
            filtered_rows, feature_column, quant_columns
        )
        log_normalized_rows, log_normalization_summary = compute_log2_normalized_preview(
            normalized_rows, feature_column, quant_columns
        )

        output_normalized_matrix = Path(args.output_normalized_matrix)
        output_normalized_matrix.parent.mkdir(parents=True, exist_ok=True)
        with output_normalized_matrix.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow([feature_column] + quant_columns)
            for row in normalized_rows:
                writer.writerow([row.get(feature_column, "")] + [row.get(col, "") for col in quant_columns])

        output_log_normalized_matrix = Path(args.output_log_normalized_matrix)
        output_log_normalized_matrix.parent.mkdir(parents=True, exist_ok=True)
        with output_log_normalized_matrix.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow([feature_column] + quant_columns)
            for row in log_normalized_rows:
                writer.writerow([row.get(feature_column, "")] + [row.get(col, "") for col in quant_columns])

        output_normalization_summary = Path(args.output_normalization_summary)
        output_normalization_summary.parent.mkdir(parents=True, exist_ok=True)
        normalization_bundle = {
            "normalized_preview": normalization_summary,
            "log2_normalized_preview": log_normalization_summary,
        }
        output_normalization_summary.write_text(json.dumps(normalization_bundle, indent=2) + "\n", encoding="utf-8")

        output_normalization_qc = Path(args.output_normalization_qc)
        output_normalization_qc.parent.mkdir(parents=True, exist_ok=True)
        with output_normalization_qc.open("w", encoding="utf-8", newline="") as handle:
            fields = [
                "sample_id",
                "features_used",
                "pre_median_intensity",
                "post_median_intensity",
                "target_global_median",
                "normalization_factor",
                "pre_alignment_error",
                "post_alignment_error",
                "normalization_status",
                "diagnostic_scope",
            ]
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            writer.writerows(normalization_qc_rows)

        output_format_diagnostics = Path(args.output_format_diagnostics)
        output_format_diagnostics.parent.mkdir(parents=True, exist_ok=True)
        output_format_diagnostics.write_text(json.dumps(format_diagnostics, indent=2) + "\n", encoding="utf-8")

        qc_summary = {
            "workflow": "dia-quant",
            "mode": "prototype-technical-minimum",
            "status": "prototype",
            "support_level": "internal-prototype",
            "public_support": "not-shipped",
            "contract_family": CONTRACT_FAMILY,
            "contract_version": CONTRACT_VERSION,
            "qc_scope": "structural-intake-plus-basic-numeric-summary-with-family-aware-export-diagnostics-feature-missingness-prototype-filtering-and-sample-median-normalization-diagnostics",
            "qc_limitations": [
                "not scientific DIA QC",
                "format-aware diagnostics are structural only",
                "validated only for the first explicit contract family",
                "feature missingness is descriptive only",
                "filtering is a prototype rule report, not a final scientific decision",
                "normalization is preview-only median scaling after filtering",
                "normalization QC is limited to sample-median alignment diagnostics",
                "no missingness modeling or imputation",
                "no replicate CV analysis",
                "no instrument or software specific QC dashboard",
                "no differential statistics",
            ],
            "feature_count": len(table_rows),
            "matched_sample_count": len(quant_columns),
            "unmatched_samples": unmatched_samples,
            "format_diagnostics": format_diagnostics,
            "feature_missingness_summary": feature_missingness_summary,
            "prototype_filtering_summary": filtering_summary,
            "normalization_preview_summary": normalization_summary,
            "log2_normalized_preview_summary": log_normalization_summary,
            "normalization_qc": normalization_qc_rows,
            "normalization_samples": normalization_sample_rows,
            "samples": sample_qc_rows,
        }
        Path(args.output_qc_summary).write_text(json.dumps(qc_summary, indent=2) + "\n", encoding="utf-8")

        input_summary = {
            "workflow": "dia-quant",
            "mode": "prototype-technical-minimum",
            "status": "prototype",
            "support_level": "internal-prototype",
            "public_support": "not-shipped",
            "contract_family": CONTRACT_FAMILY,
            "contract_version": CONTRACT_VERSION,
            "declared_input_format": args.declared_input_format,
            "normalized_input_format": args.input_format,
            "qc_scope": "structural-intake-plus-basic-numeric-summary-with-family-aware-export-diagnostics-feature-missingness-prototype-filtering-and-sample-median-normalization-diagnostics",
            "qc_limitations": [
                "not scientific DIA QC",
                "format-aware diagnostics are structural only",
                "validated only for the first explicit contract family",
                "feature missingness is descriptive only",
                "filtering is a prototype rule report, not a final scientific decision",
                "normalization is preview-only median scaling after filtering",
                "normalization QC is limited to sample-median alignment diagnostics",
                "no missingness modeling or imputation",
                "no replicate CV analysis",
                "no instrument or software specific QC dashboard",
                "no differential statistics",
            ],
            "input_table": str(Path(args.input_table).resolve()),
            "sample_sheet": str(Path(args.sample_sheet).resolve()),
            "input_format": args.input_format,
            "quant_level": args.quant_level,
            "filter_rule": {
                "name": "prototype-missingness-threshold",
                "max_missing_rate": round(args.max_missing_rate, 4),
            },
            "detected_delimiters": {
                "input_table": "tab" if table_delim == "\t" else "comma",
                "sample_sheet": "tab" if sheet_delim == "\t" else "comma",
            },
            "input_table_columns": table_fields,
            "sample_sheet_columns": sheet_fields,
            "row_counts": {
                "input_table": len(table_rows),
                "sample_sheet": len(sheet_rows),
            },
            "feature_id_column": feature_column,
            "sample_id_column": args.sample_id_column,
            "group_column": args.group_column,
            "matched_samples": len(matched_pairs),
            "unmatched_samples": unmatched_samples,
            "quant_columns": quant_columns,
            "extra_candidate_columns": extra_candidate_columns,
            "format_diagnostics": format_diagnostics,
            "contract_validation": {
                "report": str(Path(args.output_contract_report).resolve()),
                "validation_status": contract_report["validation_status"],
                "sample_matching_rule": "exact-sample-id-to-header",
            },
            "prototype_outputs": {
                "contract_validation": str(Path(args.output_contract_report).resolve()),
                "checked_metadata": str(output_metadata.resolve()),
                "detected_columns": str(output_detected.resolve()),
                "format_diagnostics": str(output_format_diagnostics.resolve()),
                "prototype_quant_preview": str(output_matrix.resolve()),
                "prototype_filtered_preview": str(output_filtered_matrix.resolve()),
                "sample_qc": str(output_sample_qc.resolve()),
                "feature_qc": str(output_feature_qc.resolve()),
                "filtering_report": str(output_filtering_report.resolve()),
                "prototype_normalized_preview": str(output_normalized_matrix.resolve()),
                "prototype_log2_normalized_preview": str(output_log_normalized_matrix.resolve()),
                "normalization_qc": str(output_normalization_qc.resolve()),
                "normalization_summary": str(output_normalization_summary.resolve()),
                "qc_summary": str(Path(args.output_qc_summary).resolve()),
            },
            "not_implemented": [
                "upstream DIA search",
                "software-specific DIA export parsing",
                "format-specific normalization beyond prototype median scaling and log2 preview",
                "missing-value imputation",
                "statistical testing",
                "biological report interpretation",
            ],
        }
        Path(args.output_input_summary).write_text(json.dumps(input_summary, indent=2) + "\n", encoding="utf-8")

        emit_contract_report(args.output_contract_report, contract_report)
        return 0
    except ContractValidationError as exc:
        contract_report["validation_status"] = "failed"
        contract_report["validation_errors"] = [
            {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        ]
        emit_contract_report(args.output_contract_report, contract_report)
        print(exc.message)
        return 1
    except Exception as exc:  # pragma: no cover - defensive path for CLI use
        contract_report["validation_status"] = "failed"
        contract_report["validation_errors"] = [
            {
                "code": "unexpected-error",
                "message": str(exc),
                "details": {"exception_type": type(exc).__name__},
            }
        ]
        emit_contract_report(args.output_contract_report, contract_report)
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
