#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys

try:
    from i18n import add_locale_argument, resolve_locale, t
except ModuleNotFoundError:  # Imported by verify-ui and the test suite.
    from scripts.i18n import add_locale_argument, resolve_locale, t


SCHEMA_VERSION = "1.0"
DEFAULT_SCHEMA = pathlib.Path(__file__).resolve().parents[1] / "references" / "design-contract.schema.json"


def contract_template() -> dict:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "contractStatus": "draft",
        "productRole": "Describe the product role",
        "audience": "Describe the primary audience",
        "primaryFlow": ["entry", "primary action", "completion"],
        "breakpoints": [390, 1024, 1440],
        "requiredStates": ["loading", "empty", "error", "success"],
        "flows": [
            {
                "id": "state-coverage",
                "coversStates": ["loading", "empty", "error", "success"],
                "start": "/",
                "steps": [
                    {"action": "expect-visible", "selector": "body"},
                    {"action": "press", "selector": "body", "value": "Tab"},
                ],
            }
        ],
        "designSystem": {
            "color": "neutral base, one accent, semantic colors",
            "typography": "existing project typography",
            "spacing": "existing spacing scale",
            "radius": "one consistent radius strategy",
            "motion": "150-240ms with reduced-motion support",
        },
        "accessibility": {
            "maxAxeViolations": 0,
            "keyboardComplete": True,
            "requireAccessibleNames": True,
            "reducedMotion": True,
        },
        "performance": {
            "maxLoadMs": 3000,
            "maxTransferBytes": 1500000,
            "maxRequests": 80,
            "maxConsoleErrors": 0,
            "maxVisualDiffRatio": 0.01,
            "minLighthouseScore": 0.8,
        },
        "dataContracts": [],
        "visualBaselines": {},
        "approval": {"direction": "", "artifacts": [], "tradeoffs": []},
    }


def load_json(path: pathlib.Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return data


def fallback_validate(data: dict) -> list[str]:
    errors = []
    required = (
        "schemaVersion",
        "contractStatus",
        "productRole",
        "audience",
        "primaryFlow",
        "breakpoints",
        "requiredStates",
        "flows",
        "designSystem",
        "accessibility",
        "performance",
        "dataContracts",
        "approval",
    )
    for key in required:
        if key not in data:
            errors.append(f"missing required field: {key}")
    if data.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(f"schemaVersion must be {SCHEMA_VERSION}")
    if data.get("contractStatus") not in {"draft", "approved"}:
        errors.append("contractStatus must be draft or approved")
    for key in ("primaryFlow", "breakpoints", "requiredStates", "flows", "dataContracts"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{key} must be an array")
    for key in ("designSystem", "accessibility", "performance", "approval"):
        if key in data and not isinstance(data[key], dict):
            errors.append(f"{key} must be an object")
    for key in ("productRole", "audience"):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            errors.append(f"{key} must be a non-empty string")

    for key in ("primaryFlow", "requiredStates"):
        values = data.get(key)
        if isinstance(values, list) and (
            not values or any(not isinstance(value, str) or not value.strip() for value in values)
        ):
            errors.append(f"{key} must contain non-empty strings")

    breakpoints = data.get("breakpoints")
    if isinstance(breakpoints, list) and not breakpoints:
        errors.append("breakpoints must not be empty")
    flows = data.get("flows")
    valid_actions = {
        "goto",
        "click",
        "fill",
        "press",
        "expect-visible",
        "expect-hidden",
        "expect-text",
        "expect-url",
        "screenshot",
    }
    if isinstance(flows, list):
        if not flows:
            errors.append("flows must not be empty")
        for index, flow in enumerate(flows):
            prefix = f"flows[{index}]"
            if not isinstance(flow, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("id", "coversStates", "start", "steps"):
                if key not in flow:
                    errors.append(f"{prefix} missing required field: {key}")
            if not isinstance(flow.get("id"), str) or not flow.get("id"):
                errors.append(f"{prefix}.id must be a non-empty string")
            if not isinstance(flow.get("coversStates"), list) or not flow.get("coversStates"):
                errors.append(f"{prefix}.coversStates must be a non-empty array")
            if not isinstance(flow.get("start"), str) or not flow.get("start"):
                errors.append(f"{prefix}.start must be a non-empty string")
            steps = flow.get("steps")
            if not isinstance(steps, list):
                errors.append(f"{prefix}.steps must be an array")
                continue
            for step_index, step in enumerate(steps):
                step_prefix = f"{prefix}.steps[{step_index}]"
                if not isinstance(step, dict) or step.get("action") not in valid_actions:
                    errors.append(f"{step_prefix}.action is invalid")

    nested_required = {
        "designSystem": ("color", "typography", "spacing", "radius", "motion"),
        "accessibility": (
            "maxAxeViolations",
            "keyboardComplete",
            "requireAccessibleNames",
            "reducedMotion",
        ),
        "performance": (
            "maxLoadMs",
            "maxTransferBytes",
            "maxRequests",
            "maxConsoleErrors",
            "maxVisualDiffRatio",
            "minLighthouseScore",
        ),
        "approval": ("direction", "artifacts", "tradeoffs"),
    }
    for group, keys in nested_required.items():
        value = data.get(group)
        if isinstance(value, dict):
            for key in keys:
                if key not in value:
                    errors.append(f"{group} missing required field: {key}")
    return errors


def schema_validate(data: dict, schema_path: pathlib.Path) -> tuple[list[str], str]:
    try:
        import jsonschema
    except ModuleNotFoundError:
        return fallback_validate(data), "built-in"

    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(
            validator.iter_errors(data),
            key=lambda item: tuple(str(part) for part in item.absolute_path),
        )
    ]
    return errors, "jsonschema"


def semantic_validate(data: dict, project_root: pathlib.Path, require_approved: bool) -> list[str]:
    errors = []
    required_states_value = data.get("requiredStates", [])
    required_states = {
        value for value in required_states_value if isinstance(value, str)
    } if isinstance(required_states_value, list) else set()
    flows = data.get("flows", [])
    if not isinstance(flows, list):
        flows = []
    covered_states = {
        state
        for flow in flows
        if isinstance(flow, dict)
        for state in (flow.get("coversStates", []) if isinstance(flow.get("coversStates"), list) else [])
        if isinstance(state, str)
    }
    missing_states = sorted(required_states - covered_states)
    if missing_states:
        errors.append(f"required states without flow coverage: {', '.join(missing_states)}")

    flow_ids = [
        flow.get("id")
        for flow in flows
        if isinstance(flow, dict) and isinstance(flow.get("id"), str)
    ]
    if len(flow_ids) != len(set(flow_ids)):
        errors.append("flow ids must be unique")

    breakpoints = data.get("breakpoints", [])
    if not isinstance(breakpoints, list):
        breakpoints = []
    if any(not isinstance(value, int) or value < 240 for value in breakpoints):
        errors.append("breakpoints must be integers >= 240")
    hashable_breakpoints = [value for value in breakpoints if isinstance(value, int)]
    if len(hashable_breakpoints) != len(set(hashable_breakpoints)):
        errors.append("breakpoints must be unique")

    data_contracts = data.get("dataContracts", [])
    if not isinstance(data_contracts, list):
        data_contracts = []
    for item in data_contracts:
        if not isinstance(item, dict) or not item.get("required"):
            continue
        path_value = item.get("path", "")
        if not isinstance(path_value, str) or not path_value:
            errors.append("required data contract path must be a non-empty string")
            continue
        relative = pathlib.Path(path_value)
        contract_path = (project_root / relative).resolve()
        try:
            contract_path.relative_to(project_root)
        except ValueError:
            errors.append(f"data contract escapes project root: {relative}")
            continue
        if not contract_path.is_file():
            errors.append(f"required data contract not found: {relative}")

    visual_baselines = data.get("visualBaselines", {})
    if not isinstance(visual_baselines, dict):
        visual_baselines = {}
    for key, value in visual_baselines.items():
        if not isinstance(value, str):
            errors.append(f"visual baseline path must be a string: {key}")
            continue
        baseline_path = (project_root / value).resolve()
        try:
            baseline_path.relative_to(project_root)
        except ValueError:
            errors.append(f"visual baseline escapes project root: {key}")

    approval = data.get("approval", {})
    if not isinstance(approval, dict):
        approval = {}
    approved = data.get("contractStatus") == "approved"
    if approved and not approval.get("direction"):
        errors.append("approved contracts require approval.direction")
    if approved and not approval.get("artifacts"):
        errors.append("approved contracts require at least one approval artifact")
    if require_approved and not approved:
        errors.append("contract is not approved")
    return errors


def validate_contract(
    contract_path: pathlib.Path,
    project_root: pathlib.Path,
    schema_path: pathlib.Path = DEFAULT_SCHEMA,
    require_approved: bool = False,
) -> tuple[list[str], str]:
    data = load_json(contract_path)
    errors, engine = schema_validate(data, schema_path)
    errors.extend(semantic_validate(data, project_root, require_approved))
    return errors, engine


def command_init(args: argparse.Namespace) -> int:
    output = pathlib.Path(args.out).expanduser().resolve()
    if output.exists() and not args.force:
        print(t("Refusing to overwrite existing contract: {output}", args.locale, output=output), file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(contract_template(), indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


def command_validate(args: argparse.Namespace) -> int:
    contract = pathlib.Path(args.contract).expanduser().resolve()
    project_root = pathlib.Path(args.project_root).expanduser().resolve()
    schema = pathlib.Path(args.schema).expanduser().resolve()
    try:
        errors, engine = validate_contract(
            contract,
            project_root,
            schema,
            require_approved=args.require_approved,
        )
    except ValueError as exc:
        print(t("design-contract failed: {error}", args.locale, error=exc), file=sys.stderr)
        return 1
    if errors:
        print(t("Contract: invalid ({engine})", args.locale, engine=engine))
        for error in errors:
            print(f"- {error}")
        return 1
    print(t("Contract: valid ({engine})", args.locale, engine=engine))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    locale = resolve_locale(argv)
    parser = argparse.ArgumentParser(description=t("Initialize and validate design-guide implementation contracts.", locale))
    add_locale_argument(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init", help=t("Create a draft contract", locale))
    add_locale_argument(init_parser, suppress_default=True)
    init_parser.add_argument("--out", default=".codex/design-guide/design-contract.json")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(handler=command_init)

    validate_parser = subparsers.add_parser("validate", help=t("Validate a contract", locale))
    add_locale_argument(validate_parser, suppress_default=True)
    validate_parser.add_argument("contract")
    validate_parser.add_argument("--project-root", default=".")
    validate_parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    validate_parser.add_argument("--require-approved", action="store_true")
    validate_parser.set_defaults(handler=command_validate)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
