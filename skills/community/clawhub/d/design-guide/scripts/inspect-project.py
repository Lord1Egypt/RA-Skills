#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys
from typing import Iterable

try:
    from i18n import add_locale_argument, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, t


SCHEMA_VERSION = "1.0"
IGNORED_DIRS = {
    ".git",
    ".next",
    ".nuxt",
    ".output",
    ".svelte-kit",
    ".turbo",
    ".vercel",
    ".vite",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
    "vendor",
}
SOURCE_SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".css", ".scss"}

DEPENDENCY_GROUPS = {
    "frameworks": {
        "next": "Next.js",
        "react": "React",
        "vue": "Vue",
        "nuxt": "Nuxt",
        "svelte": "Svelte",
        "@sveltejs/kit": "SvelteKit",
        "@angular/core": "Angular",
        "vite": "Vite",
        "astro": "Astro",
        "@remix-run/react": "Remix",
    },
    "uiLibraries": {
        "@mui/material": "MUI",
        "@chakra-ui/react": "Chakra UI",
        "@mantine/core": "Mantine",
        "@radix-ui/themes": "Radix Themes",
        "antd": "Ant Design",
        "@carbon/react": "Carbon",
        "@fluentui/react-components": "Fluent UI",
        "shadcn": "shadcn/ui",
    },
    "iconLibraries": {
        "lucide-react": "Lucide",
        "@phosphor-icons/react": "Phosphor",
        "@tabler/icons-react": "Tabler Icons",
        "@radix-ui/react-icons": "Radix Icons",
        "react-icons": "React Icons",
    },
    "stateLibraries": {
        "@reduxjs/toolkit": "Redux Toolkit",
        "redux": "Redux",
        "zustand": "Zustand",
        "jotai": "Jotai",
        "mobx": "MobX",
        "xstate": "XState",
        "@tanstack/react-query": "TanStack Query",
        "swr": "SWR",
        "pinia": "Pinia",
    },
    "testLibraries": {
        "@playwright/test": "Playwright",
        "playwright": "Playwright",
        "vitest": "Vitest",
        "jest": "Jest",
        "@testing-library/react": "Testing Library",
        "cypress": "Cypress",
    },
    "accessibilityTools": {
        "axe-core": "axe-core",
        "@axe-core/playwright": "axe Playwright",
        "eslint-plugin-jsx-a11y": "jsx-a11y",
        "pa11y": "Pa11y",
    },
    "performanceTools": {
        "lighthouse": "Lighthouse",
        "@lhci/cli": "Lighthouse CI",
        "webpack-bundle-analyzer": "Webpack Bundle Analyzer",
        "rollup-plugin-visualizer": "Rollup Visualizer",
    },
    "styling": {
        "tailwindcss": "Tailwind CSS",
        "@tailwindcss/vite": "Tailwind CSS",
        "styled-components": "styled-components",
        "@emotion/react": "Emotion",
        "sass": "Sass",
    },
}


def iter_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            yield path


def relative_paths(root: pathlib.Path, paths: Iterable[pathlib.Path], limit: int = 300) -> list[str]:
    return sorted({path.relative_to(root).as_posix() for path in paths})[:limit]


def load_package(root: pathlib.Path) -> dict:
    package_path = root / "package.json"
    if not package_path.is_file():
        return {}
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return {"_error": str(exc)}
    return package if isinstance(package, dict) else {"_error": "package.json must contain an object"}


def detect_package_manager(root: pathlib.Path) -> str | None:
    for filename, manager in (
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("package-lock.json", "npm"),
        ("bun.lock", "bun"),
        ("bun.lockb", "bun"),
    ):
        if (root / filename).is_file():
            return manager
    return None


def detect_dependency_groups(dependencies: dict[str, str]) -> dict[str, list[str]]:
    detected = {}
    for group, names in DEPENDENCY_GROUPS.items():
        detected[group] = sorted(
            {label for name, label in names.items() if name in dependencies}
        )
    return detected


def scan_project(root_value: str | pathlib.Path) -> dict:
    root = pathlib.Path(root_value).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Project root is not a directory: {root}")

    files = list(iter_files(root))
    package = load_package(root)
    package_present = (root / "package.json").is_file()
    dependencies = {}
    for key in ("dependencies", "devDependencies"):
        values = package.get(key, {})
        if isinstance(values, dict):
            dependencies.update(values)
    dependency_groups = detect_dependency_groups(dependencies)

    config_names = {
        "next.config.js",
        "next.config.mjs",
        "next.config.ts",
        "nuxt.config.ts",
        "vite.config.js",
        "vite.config.ts",
        "svelte.config.js",
        "astro.config.mjs",
        "tailwind.config.js",
        "tailwind.config.ts",
        "postcss.config.js",
        "tsconfig.json",
        "jsconfig.json",
        "eslint.config.js",
        "eslint.config.mjs",
        "biome.json",
        "playwright.config.ts",
        "playwright.config.js",
        "vitest.config.ts",
        "cypress.config.ts",
    }
    source_dirs = [
        name
        for name in ("src", "app", "pages", "components", "styles", "public", "tests", "e2e")
        if (root / name).is_dir()
    ]
    route_files = [
        path
        for path in files
        if path.suffix in SOURCE_SUFFIXES
        and (
            any(part in {"app", "pages", "routes"} for part in path.relative_to(root).parts[:-1])
            or path.name in {"router.ts", "router.js", "routes.ts", "routes.js"}
        )
    ]
    component_files = [
        path
        for path in files
        if path.suffix in SOURCE_SUFFIXES
        and "components" in {part.lower() for part in path.relative_to(root).parts[:-1]}
    ]
    token_files = [
        path
        for path in files
        if path.suffix.lower() in {".css", ".scss", ".sass", ".less", ".js", ".ts", ".json"}
        and any(term in path.name.lower() for term in ("token", "theme", "variable", "design-system"))
    ]
    data_contract_files = [
        path
        for path in files
        if (
            path.name.lower() in {"openapi.json", "openapi.yaml", "openapi.yml", "swagger.json", "schema.graphql"}
            or path.name.lower().endswith((".schema.json", ".schema.ts", ".schema.js"))
        )
    ]
    test_files = [
        path
        for path in files
        if (
            path.name.lower().endswith(
                (".test.js", ".test.jsx", ".test.ts", ".test.tsx", ".spec.js", ".spec.jsx", ".spec.ts", ".spec.tsx")
            )
            or any(part.lower() in {"tests", "test", "e2e", "__tests__"} for part in path.relative_to(root).parts[:-1])
        )
    ]

    scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
    if not isinstance(scripts, dict):
        scripts = {}
    risks = []
    if package.get("_error"):
        risks.append("package.json could not be parsed")
    if package_present and not dependency_groups["testLibraries"] and not test_files:
        risks.append("no automated frontend tests detected")
    if package_present and not dependency_groups["accessibilityTools"]:
        risks.append("no accessibility engine detected")
    if package_present and "typecheck" not in scripts and not (root / "tsconfig.json").is_file():
        risks.append("no typecheck contract detected")
    if package_present and "lint" not in scripts:
        risks.append("no lint script detected")
    if package_present and not data_contract_files:
        risks.append("no API or data schema detected")

    return {
        "schemaVersion": SCHEMA_VERSION,
        "root": str(root),
        "package": {
            "present": package_present,
            "name": package.get("name") if isinstance(package, dict) else None,
            "packageManager": detect_package_manager(root),
            "scripts": {key: scripts[key] for key in sorted(scripts)},
        },
        "capabilities": dependency_groups,
        "structure": {
            "sourceDirectories": source_dirs,
            "configs": sorted(path.name for path in files if path.name in config_names),
            "routes": relative_paths(root, route_files),
            "components": relative_paths(root, component_files),
            "designTokens": relative_paths(root, token_files),
            "dataContracts": relative_paths(root, data_contract_files),
            "tests": relative_paths(root, test_files),
        },
        "counts": {
            "files": len(files),
            "sourceFiles": sum(path.suffix in SOURCE_SUFFIXES for path in files),
            "routes": len(route_files),
            "components": len(component_files),
            "tests": len(test_files),
        },
        "risks": risks,
    }


def render_markdown(report: dict) -> str:
    lines = ["# Frontend Project Intelligence", "", f"Root: `{report['root']}`", ""]
    package = report["package"]
    lines.extend(
        [
            "## Package",
            "",
            f"- Present: {'yes' if package['present'] else 'no'}",
            f"- Name: {package['name'] or 'not detected'}",
            f"- Package manager: {package['packageManager'] or 'not detected'}",
            "",
            "## Capabilities",
            "",
        ]
    )
    for group, values in report["capabilities"].items():
        lines.append(f"- {group}: {', '.join(values) if values else 'not detected'}")
    lines.extend(["", "## Structure", ""])
    for group, values in report["structure"].items():
        lines.append(f"- {group}: {len(values)}")
    lines.extend(["", "## Risks", ""])
    lines.extend(f"- {risk}" for risk in report["risks"])
    if not report["risks"]:
        lines.append("- none detected")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=t("Inspect a frontend project and emit structured context."))
    add_locale_argument(parser)
    parser.add_argument("root", nargs="?", default=".", help=t("Project root"))
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--out", help=t("Output path; stdout when omitted"))
    args = parser.parse_args()

    try:
        report = scan_project(args.root)
    except ValueError as exc:
        print(t("inspect-project failed: {error}", args.locale, error=exc), file=sys.stderr)
        return 1
    output = (
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.format == "json"
        else render_markdown(report)
    )
    if args.out:
        output_path = pathlib.Path(args.out).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(output_path)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
