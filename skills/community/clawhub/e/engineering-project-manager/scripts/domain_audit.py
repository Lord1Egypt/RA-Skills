#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path

from pm_common import (
    contains_placeholder,
    read_text,
    requirement_definitions,
)


DOMAIN_CONFIG = {
    "SYS": {
        "label": "System Engineering",
        "prefix": "SYS-REQ-",
        "requirements":
            "01-requirements/system/SYS-REQUIREMENTS.md",
        "architecture":
            "02-architecture/system/SYS-ARCHITECTURE.md",
    },
    "SWE": {
        "label": "Software Engineering",
        "prefix": "SWE-REQ-",
        "requirements":
            "01-requirements/software/SWE-REQUIREMENTS.md",
        "architecture":
            "02-architecture/software/SWE-ARCHITECTURE.md",
    },
    "HWE": {
        "label": "Hardware Engineering",
        "prefix": "HWE-REQ-",
        "requirements":
            "01-requirements/hardware/HWE-REQUIREMENTS.md",
        "architecture":
            "02-architecture/hardware/HWE-ARCHITECTURE.md",
    },

    "MLE": {
        "label": "Machine Learning Engineering",
        "prefix": "MLE-REQ-",
        "requirements":
            "01-requirements/machine-learning/MLE-REQUIREMENTS.md",
        "architecture":
            "02-architecture/machine-learning/MLE-ARCHITECTURE.md",
    },

}


def meaningful_lines(text):
    result = []

    for raw in text.splitlines():
        line = raw.strip()

        if not line:
            continue

        if line.startswith("<!--"):
            continue

        if line.startswith("#"):
            continue

        if re.fullmatch(r"[\s|:\-]+", line):
            continue

        result.append(line)

    return result


def issue(*args):
    """
    Compatibility helper.

    Supported forms:
      issue(container, strict, message)
      issue(errors, warnings, strict, message)
    """

    if len(args) == 3:
        container, strict, message = args

        if strict:
            container["errors"].append(message)
        else:
            container["warnings"].append(message)

        return

    if len(args) == 4:
        errors, warnings, strict, message = args

        if strict:
            errors.append(message)
        else:
            warnings.append(message)

        return

    raise TypeError(
        "issue() expects 3 or 4 arguments"
    )




WORK_PRODUCT_NAMES = {
    "SYS": {
        "interface": [
            "INTERFACE-SPECIFICATION.md",
            "SYS-INTERFACE-SPECIFICATION.md",
        ],
        "test_specification": [
            "TEST-SPECIFICATION.md",
            "SYS-TEST-SPECIFICATION.md",
        ],
        "verification_report": [
            "VERIFICATION-REPORT.md",
            "SYS-VERIFICATION-REPORT.md",
        ],
    },
    "SWE": {
        "detailed_design": [
            "DETAILED-DESIGN.md",
            "SWE-DETAILED-DESIGN.md",
        ],
        "test_specification": [
            "TEST-SPECIFICATION.md",
            "SWE-TEST-SPECIFICATION.md",
        ],
        "verification_report": [
            "VERIFICATION-REPORT.md",
            "SWE-VERIFICATION-REPORT.md",
        ],
    },
    "HWE": {
        "detailed_design": [
            "DETAILED-DESIGN.md",
            "HWE-DETAILED-DESIGN.md",
        ],
        "test_specification": [
            "TEST-SPECIFICATION.md",
            "HWE-TEST-SPECIFICATION.md",
        ],
        "verification_report": [
            "VERIFICATION-REPORT.md",
            "HWE-VERIFICATION-REPORT.md",
        ],
    },

    "MLE": {
        "data_card": [
            "DATA-CARD.md",
        ],
        "model_card": [
            "MODEL-CARD.md",
        ],
        "test_specification": [
            "MLE-TEST-SPECIFICATION.md",
            "TEST-SPECIFICATION.md",
        ],
        "verification_report": [
            "MLE-VERIFICATION-REPORT.md",
            "VERIFICATION-REPORT.md",
        ],
    },

}


DOMAIN_DIRECTORY = {
    "SYS": "system",
    "SWE": "software",
    "HWE": "hardware",
    "MLE": "machine-learning",
}


# MECH DOMAIN CONFIGURATION
DOMAIN_CONFIG["MECH"] = {
    "label": "Mechanical Engineering",
    "prefix": "MEC-REQ-",
    "requirements":
        "01-requirements/mechanical/"
        "MEC-REQUIREMENTS.md",
    "architecture":
        "02-architecture/mechanical/"
        "MECH-ARCHITECTURE.md",
}

WORK_PRODUCT_NAMES["MECH"] = {
    "interface_specification": [
        "MECH-INTERFACE-SPECIFICATION.md",
        "INTERFACE-SPECIFICATION.md",
    ],
    "detailed_design": [
        "MECH-DETAILED-DESIGN.md",
        "DETAILED-DESIGN.md",
    ],
    "assembly_specification": [
        "MECH-ASSEMBLY-SPECIFICATION.md",
        "ASSEMBLY-SPECIFICATION.md",
    ],
    "test_specification": [
        "MECH-TEST-SPECIFICATION.md",
        "TEST-SPECIFICATION.md",
    ],
    "verification_report": [
        "MECH-VERIFICATION-REPORT.md",
        "VERIFICATION-REPORT.md",
    ],
}

DOMAIN_DIRECTORY["MECH"] = "mechanical"



# CYBER DOMAIN CONFIGURATION
DOMAIN_CONFIG["CYBER"] = {
    "label": "Cybersecurity Engineering",
    "prefix": "CYB-REQ-",
    "requirements":
        "01-requirements/cybersecurity/"
        "CYB-REQUIREMENTS.md",
    "architecture":
        "02-architecture/cybersecurity/"
        "CYBER-ARCHITECTURE.md",
}

WORK_PRODUCT_NAMES["CYBER"] = {
    "threat_model": [
        "CYBER-THREAT-MODEL.md",
        "THREAT-MODEL.md",
    ],
    "security_plan": [
        "CYBER-SECURITY-PLAN.md",
        "SECURITY-PLAN.md",
    ],
    "test_specification": [
        "CYBER-TEST-SPECIFICATION.md",
        "SECURITY-TEST-SPECIFICATION.md",
        "TEST-SPECIFICATION.md",
    ],
    "verification_report": [
        "CYBER-VERIFICATION-REPORT.md",
        "SECURITY-VERIFICATION-REPORT.md",
        "VERIFICATION-REPORT.md",
    ],
}

DOMAIN_DIRECTORY["CYBER"] = "cybersecurity"


DOMAIN_PROCESS_PREFIXES = {
    "SYS": ("SYS",),
    "SWE": ("SWE",),
    "HWE": ("HWE",),
    "MLE": ("MLE",),
    "MECH": ("MECH", "MEC"),
    "CYBER": ("CYBER", "CYB"),
}


def requirement_belongs_to_domain(item, domain):
    """Match both revision-aware V1.1 and transitional legacy IDs."""

    if item.get("scheme") == "V1.1":
        process = item.get("process") or ""
        return any(
            re.fullmatch(rf"{re.escape(prefix)}\d{{1,2}}", process)
            for prefix in DOMAIN_PROCESS_PREFIXES[domain]
        )

    return item.get("id", "").startswith(
        DOMAIN_CONFIG[domain]["prefix"]
    )


def work_product_score(path, domain):
    score = 0

    name = path.name.lower()
    parts = [
        part.lower()
        for part in path.parts
    ]

    if domain.lower() in name:
        score += 4

    directory = DOMAIN_DIRECTORY.get(domain)

    if directory and directory in parts:
        score += 5

    return score


def find_work_product(project, domain, filenames):
    candidates = []
    seen = set()

    for filename in filenames:
        for path in project.rglob(filename):
            resolved = path.resolve()

            if resolved in seen:
                continue

            seen.add(resolved)
            candidates.append(path)

    if not candidates:
        return None

    if len(candidates) == 1:
        return candidates[0]

    candidates.sort(
        key=lambda path: work_product_score(
            path,
            domain,
        ),
        reverse=True,
    )

    best = candidates[0]

    if work_product_score(best, domain) == 0:
        return None

    return best


def markdown_section(text, heading):
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$",
        re.IGNORECASE | re.MULTILINE,
    )

    match = pattern.search(text)

    if not match:
        return None

    start = match.end()

    next_heading = re.search(
        r"^##\s+",
        text[start:],
        re.MULTILINE,
    )

    if next_heading:
        return text[
            start:start + next_heading.start()
        ]

    return text[start:]


def markdown_field_value(text, field):
    match = re.search(
        rf"^[ \t]*-[ \t]*{re.escape(field)}[ \t]*:[ \t]*(.*)$",
        text,
        re.IGNORECASE | re.MULTILINE,
    )

    if not match:
        return None

    value = match.group(1).strip()

    if not value:
        return None

    if value.startswith("<") and value.endswith(">"):
        return None

    return value



def section_has_real_table_row(section):
    if not section:
        return False

    for line in section.splitlines():
        line = line.strip()

        if not line.startswith("|"):
            continue

        if re.fullmatch(r"[\s|:\-]+", line):
            continue

        low = line.lower()

        if "metric" in low and "result" in low:
            continue

        if "<" in line and ">" in line:
            continue

        cells = [
            c.strip()
            for c in line.strip("|").split("|")
        ]

        if len(cells) >= 3 and all(cells[:3]):
            return True

    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument(
        "--strict",
        action="store_true",
    )
    parser.add_argument(
        "--domain",
        action="append",
        choices=sorted(DOMAIN_CONFIG),
        help="Audit only the selected engineering domain. May be repeated.",
    )

    args = parser.parse_args()
    project = Path(args.project).resolve()

    errors = []
    warnings = []

    bootstrap_path = (
        project
        / "00-project"
        / "BOOTSTRAP.json"
    )

    if not bootstrap_path.exists():
        print(
            "ERROR: 00-project/BOOTSTRAP.json missing"
        )
        return 1

    try:
        bootstrap = json.loads(
            bootstrap_path.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        print(
            "ERROR: invalid BOOTSTRAP.json:",
            exc,
        )
        return 1

    active_domains = bootstrap.get(
        "domains",
        [],
    )

    if args.domain:
        requested = list(dict.fromkeys(args.domain))

        unavailable = [
            domain
            for domain in requested
            if domain not in active_domains
        ]

        if unavailable:
            print(
                "ERROR: domain(s) not active "
                "in this project:",
                ", ".join(unavailable),
            )
            return 1

        active_domains = requested

    all_requirements = requirement_definitions(
        project
    )

    print(
        "Active domains:",
        ", ".join(active_domains)
        if active_domains
        else "none",
    )

    checked = 0

    for domain in active_domains:
        if domain not in DOMAIN_CONFIG:
            print(
                f"SKIP {domain}: "
                "domain audit not yet implemented"
            )
            continue

        checked += 1
        cfg = DOMAIN_CONFIG[domain]

        print()
        print(
            f"=== {domain} — {cfg['label']} ==="
        )

        req_path = (
            project
            / cfg["requirements"]
        )

        arch_path = (
            project
            / cfg["architecture"]
        )

        domain_reqs = []

        if not req_path.exists():
            errors.append(
                f"{domain}: requirements file missing: "
                f"{cfg['requirements']}"
            )
        else:
            domain_reqs = [
                item
                for item in all_requirements
                if requirement_belongs_to_domain(item, domain)
                and item["path"].resolve() == req_path.resolve()
            ]

            print(
                "Requirements:",
                len(domain_reqs),
            )

            if not domain_reqs:
                issue(
                    {
                        "errors": errors,
                        "warnings": warnings,
                    },
                    args.strict,
                    f"{domain}: no domain requirement "
                    "defined",
                )

        if not arch_path.exists():
            errors.append(
                f"{domain}: architecture missing: "
                f"{cfg['architecture']}"
            )
            continue

        architecture = read_text(
            arch_path
        )

        content = meaningful_lines(
            architecture
        )

        print(
            "Architecture content lines:",
            len(content),
        )

        if not content:
            issue(
                {
                    "errors": errors,
                    "warnings": warnings,
                },
                args.strict,
                f"{domain}: architecture is empty",
            )

        if contains_placeholder(
            architecture
        ):
            issue(
                {
                    "errors": errors,
                    "warnings": warnings,
                },
                args.strict,
                f"{domain}: architecture contains "
                "placeholders/TODO/TBD",
            )

        domain_ids = [item["id"] for item in domain_reqs]

        linked = [
            rid
            for rid in domain_ids
            if rid in architecture
        ]

        missing_links = [
            rid
            for rid in domain_ids
            if rid not in architecture
        ]

        print(
            "Architecture requirement references:",
            f"{len(linked)}/{len(domain_ids)}",
        )

        for rid in missing_links:
            message = (
                f"{domain}: {rid} not traced "
                "to the architecture"
            )

            if args.strict:
                errors.append(message)
            else:
                warnings.append(message)


        # SYS work-product maturity checks.
        if domain == "SYS":
            for wp_name, filenames in WORK_PRODUCT_NAMES["SYS"].items():
                wp = find_work_product(
                    project,
                    "SYS",
                    filenames,
                )

                label = wp_name.replace(
                    "_",
                    " ",
                )

                if wp is None:
                    message = (
                        f"SYS: {label} missing"
                    )

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                    continue

                print(
                    f"SYS {label}:",
                    wp,
                )

                wp_text = read_text(wp)

                if contains_placeholder(wp_text):
                    message = (
                        f"SYS: {label} contains "
                        "placeholders/TODO/TBD"
                    )

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                if domain_ids:
                    refs = [
                        rid
                        for rid in domain_ids
                        if rid in wp_text
                    ]

                    print(
                        f"SYS {label} requirement references:",
                        f"{len(refs)}/{len(domain_ids)}",
                    )

                    missing = [
                        rid
                        for rid in domain_ids
                        if rid not in wp_text
                    ]

                    for rid in missing:
                        message = (
                            f"SYS: {rid} not traced "
                            f"to {label}"
                        )

                        if args.strict:
                            errors.append(message)
                        else:
                            warnings.append(message)


        # SWE work-product maturity checks.
        if domain == "SWE":
            for wp_name, filenames in WORK_PRODUCT_NAMES["SWE"].items():
                wp = find_work_product(
                    project,
                    "SWE",
                    filenames,
                )

                label = wp_name.replace(
                    "_",
                    " ",
                )

                if wp is None:
                    message = f"SWE: {label} missing"

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                    continue

                print(
                    f"SWE {label}:",
                    wp,
                )

                wp_text = read_text(wp)

                if contains_placeholder(wp_text):
                    message = (
                        f"SWE: {label} contains "
                        "placeholders/TODO/TBD"
                    )

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                if domain_ids:
                    refs = [
                        rid
                        for rid in domain_ids
                        if rid in wp_text
                    ]

                    print(
                        f"SWE {label} requirement references:",
                        f"{len(refs)}/{len(domain_ids)}",
                    )

                    missing = [
                        rid
                        for rid in domain_ids
                        if rid not in wp_text
                    ]

                    for rid in missing:
                        message = (
                            f"SWE: {rid} not traced "
                            f"to {label}"
                        )

                        if args.strict:
                            errors.append(message)
                        else:
                            warnings.append(message)


        # HWE work-product maturity checks.
        if domain == "HWE":
            for wp_name, filenames in WORK_PRODUCT_NAMES["HWE"].items():
                wp = find_work_product(
                    project,
                    "HWE",
                    filenames,
                )

                label = wp_name.replace(
                    "_",
                    " ",
                )

                if wp is None:
                    message = f"HWE: {label} missing"

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                    continue

                print(
                    f"HWE {label}:",
                    wp,
                )

                wp_text = read_text(wp)

                if contains_placeholder(wp_text):
                    message = (
                        f"HWE: {label} contains "
                        "placeholders/TODO/TBD"
                    )

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                if domain_ids:
                    refs = [
                        rid
                        for rid in domain_ids
                        if rid in wp_text
                    ]

                    print(
                        f"HWE {label} requirement references:",
                        f"{len(refs)}/{len(domain_ids)}",
                    )

                    missing = [
                        rid
                        for rid in domain_ids
                        if rid not in wp_text
                    ]

                    for rid in missing:
                        message = (
                            f"HWE: {rid} not traced "
                            f"to {label}"
                        )

                        if args.strict:
                            errors.append(message)
                        else:
                            warnings.append(message)


        # MLE work-product maturity checks.
        if domain == "MLE":
            for wp_name, filenames in WORK_PRODUCT_NAMES["MLE"].items():
                wp = find_work_product(
                    project,
                    "MLE",
                    filenames,
                )

                label = wp_name.replace(
                    "_",
                    " ",
                )

                if wp is None:
                    message = f"MLE: {label} missing"

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                    continue

                print(
                    f"MLE {label}:",
                    wp,
                )

                wp_text = read_text(wp)

                if contains_placeholder(wp_text):
                    message = (
                        f"MLE: {label} contains "
                        "placeholders/TODO/TBD"
                    )

                    if args.strict:
                        errors.append(message)
                    else:
                        warnings.append(message)

                if domain_ids:
                    refs = [
                        rid
                        for rid in domain_ids
                        if rid in wp_text
                    ]

                    print(
                        f"MLE {label} requirement references:",
                        f"{len(refs)}/{len(domain_ids)}",
                    )

                    missing = [
                        rid
                        for rid in domain_ids
                        if rid not in wp_text
                    ]

                    for rid in missing:
                        message = (
                            f"MLE: {rid} not traced "
                            f"to {label}"
                        )

                        if args.strict:
                            errors.append(message)
                        else:
                            warnings.append(message)


        # MLE semantic maturity checks.
        if domain == "MLE":
            data_card = find_work_product(
                project,
                "MLE",
                WORK_PRODUCT_NAMES["MLE"]["data_card"],
            )

            model_card = find_work_product(
                project,
                "MLE",
                WORK_PRODUCT_NAMES["MLE"]["model_card"],
            )

            if data_card:
                data_text = read_text(data_card)

                required_data_sections = [
                    "Identity",
                    "Source",
                    "License / Rights",
                    "Preprocessing",
                    "Splits",
                    "Quality Checks",
                    "Bias / Representativeness",
                    "Traceability",
                ]

                for heading in required_data_sections:
                    if markdown_section(
                        data_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            f"MLE: DATA-CARD section "
                            f"'{heading}' missing",
                        )

                for field in [
                    "Dataset ID",
                    "Version",
                ]:
                    if not markdown_field_value(
                        data_text,
                        field,
                    ):
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            f"MLE: DATA-CARD {field} "
                            "not filled in",
                        )

                splits = markdown_section(
                    data_text,
                    "Splits",
                )

                if splits is not None:
                    for split in [
                        "Training",
                        "Validation",
                        "Test",
                    ]:
                        if not markdown_field_value(
                            splits,
                            split,
                        ):
                            issue(
                                errors,
                                warnings,
                                args.strict,
                                f"MLE: split {split} "
                                "not filled in",
                            )

            if model_card:
                model_text = read_text(model_card)

                required_model_sections = [
                    "Identity",
                    "Inputs",
                    "Outputs",
                    "Training Data",
                    "Evaluation Data",
                    "Metrics",
                    "Runtime Requirements",
                    "Known Limitations",
                    "Known Failure Modes",
                    "Bias / Segment Analysis",
                    "Traceability",
                ]

                for heading in required_model_sections:
                    if markdown_section(
                        model_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            f"MLE: MODEL-CARD section "
                            f"'{heading}' missing",
                        )

                if not markdown_field_value(
                    model_text,
                    "Version",
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MLE: MODEL-CARD Version "
                        "not filled in",
                    )

                metrics = markdown_section(
                    model_text,
                    "Metrics",
                )

                if not section_has_real_table_row(
                    metrics
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MLE: no metric with "
                        "result and acceptance threshold",
                    )


        # CYBER semantic maturity checks.
        if domain == "CYBER":
            cyber_architecture = (
                project
                / DOMAIN_CONFIG["CYBER"]["architecture"]
            )

            threat_model = find_work_product(
                project,
                "CYBER",
                WORK_PRODUCT_NAMES["CYBER"][
                    "threat_model"
                ],
            )

            security_plan = find_work_product(
                project,
                "CYBER",
                WORK_PRODUCT_NAMES["CYBER"][
                    "security_plan"
                ],
            )

            cyber_test = find_work_product(
                project,
                "CYBER",
                WORK_PRODUCT_NAMES["CYBER"][
                    "test_specification"
                ],
            )

            cyber_report = find_work_product(
                project,
                "CYBER",
                WORK_PRODUCT_NAMES["CYBER"][
                    "verification_report"
                ],
            )

            cyber_documents = [
                (
                    "CYBER-ARCHITECTURE",
                    cyber_architecture,
                ),
                (
                    "CYBER-THREAT-MODEL",
                    threat_model,
                ),
                (
                    "CYBER-SECURITY-PLAN",
                    security_plan,
                ),
                (
                    "CYBER-TEST-SPECIFICATION",
                    cyber_test,
                ),
                (
                    "CYBER-VERIFICATION-REPORT",
                    cyber_report,
                ),
            ]

            # Every cybersecurity work product must
            # identify its controlled version/status/owner.
            for document_name, document_path in cyber_documents:
                if not document_path:
                    continue

                document_text = read_text(
                    document_path
                )

                for field in [
                    "Version",
                    "Status",
                    "Owner",
                ]:
                    if not markdown_field_value(
                        document_text,
                        field,
                    ):
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            f"CYBER: {document_name} "
                            f"{field} not filled in",
                        )

            # Architecture: security controls must
            # contain at least one implemented control.
            if cyber_architecture.is_file():
                architecture_text = read_text(
                    cyber_architecture
                )

                required_arch_sections = [
                    "Assets",
                    "Trust Boundaries",
                    "External Interfaces",
                    "Authentication",
                    "Authorization",
                    "Cryptography",
                    "Secrets Management",
                    "Secure Communications",
                    "Secure Storage",
                    "Secure Update",
                    "Logging and Audit",
                    "Security Controls",
                    "Traceability",
                ]

                for heading in required_arch_sections:
                    if markdown_section(
                        architecture_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "CYBER: architecture section "
                            f"'{heading}' missing",
                        )

                controls = markdown_section(
                    architecture_text,
                    "Security Controls",
                )

                if not section_has_real_table_row(
                    controls
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "CYBER: no architectural security "
                        "control filled in",
                    )

            # Threat model: require real assets and
            # at least one analyzed threat.
            if threat_model:
                threat_text = read_text(
                    threat_model
                )

                required_threat_sections = [
                    "Assets",
                    "Trust Boundaries",
                    "Attack Surface",
                    "Threat Actors",
                    "Security Assumptions",
                    "Threat Analysis",
                    "Abuse and Misuse Cases",
                    "Security Controls",
                    "Residual Risks",
                    "Traceability",
                ]

                for heading in required_threat_sections:
                    if markdown_section(
                        threat_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "CYBER: threat model section "
                            f"'{heading}' missing",
                        )

                assets = markdown_section(
                    threat_text,
                    "Assets",
                )

                if not section_has_real_table_row(
                    assets
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "CYBER: no security asset "
                        "filled in the threat model",
                    )

                threats = markdown_section(
                    threat_text,
                    "Threat Analysis",
                )

                if not section_has_real_table_row(
                    threats
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "CYBER: no threat analyzed "
                        "in the threat model",
                    )

            # Security plan: lifecycle security
            # activities must be explicitly documented.
            if security_plan:
                plan_text = read_text(
                    security_plan
                )

                required_plan_sections = [
                    "Purpose",
                    "Scope",
                    "Applicable Requirements",
                    "Roles and Responsibilities",
                    "Security Objectives",
                    "Threat Management",
                    "Secure Development",
                    "Dependency and Vulnerability Management",
                    "Secrets and Credential Management",
                    "Secure Configuration",
                    "Secure Update and Patch Management",
                    "Logging and Monitoring",
                    "Incident and Vulnerability Response",
                    "Security Verification Strategy",
                    "Release Security Criteria",
                    "Traceability",
                ]

                for heading in required_plan_sections:
                    if markdown_section(
                        plan_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "CYBER: security plan section "
                            f"'{heading}' missing",
                        )

            # Security test specification must contain
            # real CYB requirement coverage.
            if cyber_test:
                test_text = read_text(
                    cyber_test
                )

                requirements_coverage = markdown_section(
                    test_text,
                    "Requirements Coverage",
                )

                if not section_has_real_table_row(
                    requirements_coverage
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "CYBER: no requirement "
                        "coverage in the test "
                        "specification",
                    )

            # Verification report must contain actual
            # requirement verification evidence.
            if cyber_report:
                report_text = read_text(
                    cyber_report
                )

                requirement_results = markdown_section(
                    report_text,
                    "Requirement Results",
                )

                if not section_has_real_table_row(
                    requirement_results
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "CYBER: no requirement "
                        "verification result filled in",
                    )


        # MECH semantic maturity checks.
        if domain == "MECH":
            mech_architecture = (
                project
                / DOMAIN_CONFIG["MECH"]["architecture"]
            )

            interface_spec = find_work_product(
                project,
                "MECH",
                WORK_PRODUCT_NAMES["MECH"][
                    "interface_specification"
                ],
            )

            detailed_design = find_work_product(
                project,
                "MECH",
                WORK_PRODUCT_NAMES["MECH"][
                    "detailed_design"
                ],
            )

            assembly_spec = find_work_product(
                project,
                "MECH",
                WORK_PRODUCT_NAMES["MECH"][
                    "assembly_specification"
                ],
            )

            mech_test = find_work_product(
                project,
                "MECH",
                WORK_PRODUCT_NAMES["MECH"][
                    "test_specification"
                ],
            )

            mech_report = find_work_product(
                project,
                "MECH",
                WORK_PRODUCT_NAMES["MECH"][
                    "verification_report"
                ],
            )

            mech_documents = [
                (
                    "MECH-ARCHITECTURE",
                    mech_architecture,
                ),
                (
                    "MECH-INTERFACE-SPECIFICATION",
                    interface_spec,
                ),
                (
                    "MECH-DETAILED-DESIGN",
                    detailed_design,
                ),
                (
                    "MECH-ASSEMBLY-SPECIFICATION",
                    assembly_spec,
                ),
                (
                    "MECH-TEST-SPECIFICATION",
                    mech_test,
                ),
                (
                    "MECH-VERIFICATION-REPORT",
                    mech_report,
                ),
            ]

            # Document control.
            for document_name, document_path in mech_documents:
                if not document_path:
                    continue

                if not Path(document_path).is_file():
                    continue

                document_text = read_text(
                    Path(document_path)
                )

                for field in [
                    "Version",
                    "Status",
                    "Owner",
                ]:
                    if not markdown_field_value(
                        document_text,
                        field,
                    ):
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            f"MECH: {document_name} "
                            f"{field} not filled in",
                        )

            # Mechanical architecture.
            if mech_architecture.is_file():
                architecture_text = read_text(
                    mech_architecture
                )

                required_arch_sections = [
                    "Applicable Requirements",
                    "Mechanical Breakdown",
                    "Mechanical Interfaces",
                    "Envelope and Dimensions",
                    "Mass Properties",
                    "Materials",
                    "Loads and Structural Constraints",
                    "Environmental Constraints",
                    "Thermal Considerations",
                    "Maintainability and Serviceability",
                    "Safety Considerations",
                    "Traceability",
                ]

                for heading in required_arch_sections:
                    if markdown_section(
                        architecture_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "MECH: architecture section "
                            f"'{heading}' missing",
                        )

                breakdown = markdown_section(
                    architecture_text,
                    "Mechanical Breakdown",
                )

                if not section_has_real_table_row(
                    breakdown
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MECH: no mechanical element "
                        "filled in the architecture",
                    )

            # Detailed design.
            if detailed_design:
                design_text = read_text(
                    detailed_design
                )

                required_design_sections = [
                    "Applicable Requirements",
                    "Components",
                    "Critical Dimensions",
                    "Geometric Tolerances",
                    "Materials and Treatments",
                    "Fasteners and Joints",
                    "Structural Design",
                    "Thermal Design",
                    "Manufacturing Constraints",
                    "Design Calculations",
                    "Traceability",
                ]

                for heading in required_design_sections:
                    if markdown_section(
                        design_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "MECH: detailed design section "
                            f"'{heading}' missing",
                        )

                components = markdown_section(
                    design_text,
                    "Components",
                )

                if not section_has_real_table_row(
                    components
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MECH: no mechanical component "
                        "filled in the detailed design",
                    )

                dimensions = markdown_section(
                    design_text,
                    "Critical Dimensions",
                )

                if not section_has_real_table_row(
                    dimensions
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MECH: no critical dimension "
                        "with tolerance filled in",
                    )

            # Interface specification.
            if interface_spec:
                interface_text = read_text(
                    interface_spec
                )

                required_interface_sections = [
                    "Applicable Requirements",
                    "Interface Inventory",
                    "Mounting Interfaces",
                    "Dimensional Interfaces",
                    "Force and Load Transfer",
                    "Motion Interfaces",
                    "Cable and Connector Mechanical Constraints",
                    "Sealing Interfaces",
                    "Service Interfaces",
                    "Traceability",
                ]

                for heading in required_interface_sections:
                    if markdown_section(
                        interface_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "MECH: interface specification "
                            f"section '{heading}' missing",
                        )

                interfaces = markdown_section(
                    interface_text,
                    "Interface Inventory",
                )

                if not section_has_real_table_row(
                    interfaces
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MECH: no mechanical interface "
                        "filled in",
                    )

            # Assembly specification.
            if assembly_spec:
                assembly_text = read_text(
                    assembly_spec
                )

                required_assembly_sections = [
                    "Applicable Requirements",
                    "Bill of Materials Reference",
                    "Tools and Equipment",
                    "Assembly Preconditions",
                    "Assembly Sequence",
                    "Fastening and Torque",
                    "Adhesives and Consumables",
                    "Alignment and Adjustment",
                    "Inspection Points",
                    "Rework and Repair",
                    "Final Assembly Acceptance",
                    "Traceability",
                ]

                for heading in required_assembly_sections:
                    if markdown_section(
                        assembly_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "MECH: assembly specification "
                            f"section '{heading}' missing",
                        )

                sequence = markdown_section(
                    assembly_text,
                    "Assembly Sequence",
                )

                if not section_has_real_table_row(
                    sequence
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MECH: no assembly "
                        "operation filled in",
                    )

            # Mechanical test specification.
            if mech_test:
                test_text = read_text(
                    mech_test
                )

                required_test_sections = [
                    "Applicable Requirements",
                    "Test Environment",
                    "Test Cases",
                    "Dimensional Verification",
                    "Structural Verification",
                    "Environmental Verification",
                    "Assembly Verification",
                    "Requirements Coverage",
                    "Deviations and Constraints",
                    "Review and Approval",
                ]

                for heading in required_test_sections:
                    if markdown_section(
                        test_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "MECH: test specification "
                            f"section '{heading}' missing",
                        )

                coverage = markdown_section(
                    test_text,
                    "Requirements Coverage",
                )

                if not section_has_real_table_row(
                    coverage
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MECH: no requirement "
                        "coverage in the "
                        "test specification",
                    )

            # Verification report.
            if mech_report:
                report_text = read_text(
                    mech_report
                )

                required_report_sections = [
                    "Configuration Under Test",
                    "Verification Summary",
                    "Requirement Results",
                    "Dimensional Results",
                    "Structural Results",
                    "Environmental Results",
                    "Assembly Results",
                    "Passed",
                    "Failed",
                    "Blocked",
                    "Open Problems",
                    "Coverage and Completeness",
                    "Deviations",
                    "Conclusion",
                    "Traceability",
                    "Approval",
                ]

                for heading in required_report_sections:
                    if markdown_section(
                        report_text,
                        heading,
                    ) is None:
                        issue(
                            errors,
                            warnings,
                            args.strict,
                            "MECH: verification report "
                            f"section '{heading}' missing",
                        )

                results = markdown_section(
                    report_text,
                    "Requirement Results",
                )

                if not section_has_real_table_row(
                    results
                ):
                    issue(
                        errors,
                        warnings,
                        args.strict,
                        "MECH: no requirement "
                        "verification result filled in",
                    )

    if checked == 0:
        warnings.append(
            "No SYS/SWE/HWE domain "
            "to audit"
        )

    print()

    for warning in warnings:
        print(
            "WARNING:",
            warning,
        )

    for error in errors:
        print(
            "ERROR:",
            error,
        )

    print(
        "DOMAIN AUDIT:",
        f"{len(errors)} error(s),",
        f"{len(warnings)} warning(s)",
    )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
