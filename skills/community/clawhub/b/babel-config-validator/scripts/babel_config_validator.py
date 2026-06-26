#!/usr/bin/env python3
"""Babel Config Validator — validate babel.config.json, .babelrc, .babelrc.json, package.json#babel."""

import json
import os
import re
import sys
from pathlib import Path

VALID_TOP_KEYS = {
    "presets", "plugins", "env", "overrides", "sourceType", "assumptions",
    "targets", "browserslistConfigFile", "browserslistEnv", "caller",
    "minified", "comments", "retainLines", "compact", "auxiliaryCommentBefore",
    "auxiliaryCommentAfter", "shouldPrintComment", "moduleIds", "moduleId",
    "getModuleId", "moduleRoot", "sourceMaps", "sourceMap", "sourceFileName",
    "sourceRoot", "parserOpts", "generatorOpts", "passPerPreset", "inputSourceMap",
    "wrapPluginVisitorMethod", "highlightCode", "include", "exclude", "ignore",
    "only", "test", "extends", "cwd", "root", "rootMode", "envName", "configFile",
    "babelrc", "babelrcRoots", "filename", "filenameRelative", "code", "ast",
    "cloneInputAst",
}

DEPRECATED_PRESETS = {
    "es2015": "@babel/preset-env",
    "es2016": "@babel/preset-env",
    "es2017": "@babel/preset-env",
    "latest": "@babel/preset-env",
    "stage-0": "explicit plugins",
    "stage-1": "explicit plugins",
    "stage-2": "explicit plugins",
    "stage-3": "explicit plugins",
    "babel-preset-es2015": "@babel/preset-env",
    "babel-preset-es2016": "@babel/preset-env",
    "babel-preset-es2017": "@babel/preset-env",
    "babel-preset-latest": "@babel/preset-env",
    "babel-preset-stage-0": "explicit plugins",
    "babel-preset-stage-1": "explicit plugins",
    "babel-preset-stage-2": "explicit plugins",
    "babel-preset-stage-3": "explicit plugins",
}

DEPRECATED_PLUGINS = {
    "@babel/plugin-proposal-class-properties": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-private-methods": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-private-property-in-object": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-numeric-separator": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-nullish-coalescing-operator": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-optional-chaining": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-optional-catch-binding": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-json-strings": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-async-generator-functions": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-object-rest-spread": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-unicode-property-regex": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-export-namespace-from": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-logical-assignment-operators": "Built-in since Babel 7.14",
    "@babel/plugin-proposal-class-static-block": "Built-in since Babel 7.14",
    "babel-plugin-transform-class-properties": "@babel/plugin-transform-class-properties",
    "babel-plugin-transform-object-rest-spread": "@babel/plugin-transform-object-rest-spread",
    "babel-plugin-transform-runtime": "@babel/plugin-transform-runtime",
}

KNOWN_PRESETS = {
    "@babel/preset-env", "@babel/preset-react", "@babel/preset-typescript",
    "@babel/preset-flow",
}

CONFLICTING_PLUGINS = [
    ({"@babel/plugin-transform-runtime"}, {"@babel/plugin-external-helpers"},
     "transform-runtime and external-helpers serve similar purposes"),
]


def normalize_name(name):
    if isinstance(name, list):
        name = name[0] if name else ""
    if isinstance(name, str):
        return name.strip()
    return ""


def get_preset_name(preset):
    if isinstance(preset, str):
        return preset
    if isinstance(preset, list) and len(preset) > 0:
        return str(preset[0])
    return ""


def get_plugin_name(plugin):
    if isinstance(plugin, str):
        return plugin
    if isinstance(plugin, list) and len(plugin) > 0:
        return str(plugin[0])
    return ""


def get_plugin_options(plugin):
    if isinstance(plugin, list) and len(plugin) > 1:
        return plugin[1] if isinstance(plugin[1], dict) else {}
    return {}


def load_config(filepath):
    path = Path(filepath)
    if not path.exists():
        return None, f"File not found: {filepath}"
    try:
        text = path.read_text(encoding="utf-8").strip()
    except Exception as e:
        return None, f"Cannot read file: {e}"
    if not text:
        return None, "File is empty"

    if path.name == "package.json":
        try:
            pkg = json.loads(text)
            if "babel" not in pkg:
                return None, "No 'babel' key in package.json"
            return pkg["babel"], None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"
    else:
        comment_re = re.compile(r'//.*?$|/\*.*?\*/', re.MULTILINE | re.DOTALL)
        cleaned = comment_re.sub('', text)
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)
        try:
            return json.loads(cleaned), None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"


def find_sibling_configs(filepath):
    directory = Path(filepath).parent
    configs = []
    names = ["babel.config.json", "babel.config.js", "babel.config.cjs", "babel.config.mjs",
             ".babelrc", ".babelrc.json", ".babelrc.js", ".babelrc.cjs", ".babelrc.mjs"]
    for name in names:
        p = directory / name
        if p.exists() and str(p.resolve()) != str(Path(filepath).resolve()):
            configs.append(name)
    pkg = directory / "package.json"
    if pkg.exists() and Path(filepath).name != "package.json":
        try:
            d = json.loads(pkg.read_text())
            if "babel" in d:
                configs.append("package.json#babel")
        except Exception:
            pass
    return configs


class Finding:
    def __init__(self, rule_id, severity, message, detail=None):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.detail = detail

    def to_dict(self):
        d = {"rule": self.rule_id, "severity": self.severity, "message": self.message}
        if self.detail:
            d["detail"] = self.detail
        return d

    def to_text(self):
        icon = "❌" if self.severity == "error" else "⚠️"
        s = f"{icon} [{self.rule_id}] {self.message}"
        if self.detail:
            s += f"\n   → {self.detail}"
        return s


def validate(config, filepath):
    findings = []

    siblings = find_sibling_configs(filepath)
    if siblings:
        findings.append(Finding("S3", "warning",
            f"Multiple Babel configs detected: {', '.join(siblings)}",
            "Having both babel.config and .babelrc can cause unexpected behavior"))

    unknown = set(config.keys()) - VALID_TOP_KEYS
    if unknown:
        findings.append(Finding("S4", "warning",
            f"Unknown top-level keys: {', '.join(sorted(unknown))}"))

    presets = config.get("presets", [])
    if isinstance(presets, list):
        preset_names = [get_preset_name(p) for p in presets]

        for pn in preset_names:
            if pn in DEPRECATED_PRESETS:
                findings.append(Finding("P1", "error",
                    f"Deprecated preset: {pn}",
                    f"Replace with {DEPRECATED_PRESETS[pn]}"))

        ts_idx = -1
        env_idx = -1
        for i, pn in enumerate(preset_names):
            if "preset-typescript" in pn:
                ts_idx = i
            if "preset-env" in pn:
                env_idx = i
        if ts_idx >= 0 and env_idx >= 0 and ts_idx > env_idx:
            findings.append(Finding("P2", "warning",
                "@babel/preset-typescript should come before @babel/preset-env in presets array",
                "Babel applies presets in reverse order; TypeScript must be stripped before env transforms"))

        seen = {}
        for pn in preset_names:
            if pn:
                norm = pn.replace("babel-preset-", "@babel/preset-")
                if norm in seen:
                    findings.append(Finding("P3", "warning", f"Duplicate preset: {pn}"))
                seen[norm] = True

        for pn in preset_names:
            if pn and not pn.startswith("./") and not pn.startswith("module:"):
                norm = pn
                if not norm.startswith("@") and not norm.startswith("babel-preset-"):
                    norm = f"@babel/preset-{norm}" if not norm.startswith("@babel/") else norm
                if norm in KNOWN_PRESETS:
                    continue
                if pn.startswith("@babel/preset-") and pn not in KNOWN_PRESETS:
                    findings.append(Finding("P4", "error",
                        f"Unknown @babel preset: {pn}",
                        "Check for typos in preset name"))

        has_env = any("preset-env" in pn for pn in preset_names)
        if not has_env and preset_names:
            findings.append(Finding("P5", "warning",
                "Missing @babel/preset-env",
                "Most Babel configs need preset-env for browser/node targeting"))

    plugins = config.get("plugins", [])
    if isinstance(plugins, list):
        plugin_names = [get_plugin_name(p) for p in plugins]

        for pn in plugin_names:
            if pn in DEPRECATED_PLUGINS:
                findings.append(Finding("L1", "error",
                    f"Deprecated plugin: {pn}",
                    DEPRECATED_PLUGINS[pn]))

        seen = {}
        for pn in plugin_names:
            if pn:
                if pn in seen:
                    findings.append(Finding("L2", "warning", f"Duplicate plugin: {pn}"))
                seen[pn] = True

        deco_idx = -1
        class_prop_idx = -1
        for i, pn in enumerate(plugin_names):
            if "decorators" in pn:
                deco_idx = i
            if "class-properties" in pn or "class-prop" in pn:
                class_prop_idx = i
        if deco_idx >= 0 and class_prop_idx >= 0 and deco_idx > class_prop_idx:
            findings.append(Finding("L3", "warning",
                "Decorators plugin should come before class-properties",
                "Plugin ordering matters — decorators must be processed first"))

        plugin_set = set(plugin_names)
        for group_a, group_b, msg in CONFLICTING_PLUGINS:
            if group_a & plugin_set and group_b & plugin_set:
                findings.append(Finding("L4", "warning",
                    f"Potentially conflicting plugins: {msg}"))

        for pn in plugin_names:
            if pn and not pn.startswith("@") and not pn.startswith("./") and not pn.startswith("module:") and not pn.startswith("babel-plugin-"):
                findings.append(Finding("L5", "warning",
                    f"Plugin without @babel/ scope: {pn}",
                    "May be a community plugin or a typo"))

    if isinstance(presets, list):
        for p in presets:
            opts = {}
            if isinstance(p, list) and len(p) > 1 and isinstance(p[1], dict):
                opts = p[1]
                pname = get_preset_name(p)
            else:
                continue

            if "preset-env" in pname:
                modules = opts.get("modules")
                if modules is False:
                    findings.append(Finding("M1", "warning",
                        "modules: false in preset-env",
                        "This disables module transformation — only correct if a bundler (webpack/rollup/vite) handles modules"))

                use_built_ins = opts.get("useBuiltIns")
                corejs = opts.get("corejs")
                if use_built_ins and use_built_ins != False and not corejs:
                    findings.append(Finding("B3", "warning",
                        f"useBuiltIns: '{use_built_ins}' without corejs version",
                        "Set corejs: 3 (or { version: 3, proposals: true })"))

                if corejs:
                    ver = corejs
                    if isinstance(corejs, dict):
                        ver = corejs.get("version", 0)
                    try:
                        if float(ver) < 3:
                            findings.append(Finding("B4", "warning",
                                f"corejs version {ver} is outdated",
                                "Upgrade to corejs: 3 for better polyfill coverage"))
                    except (TypeError, ValueError):
                        pass

    source_type = config.get("sourceType")
    if source_type and isinstance(presets, list):
        for p in presets:
            if isinstance(p, list) and len(p) > 1 and isinstance(p[1], dict):
                modules = p[1].get("modules")
                if source_type == "script" and modules not in (False, "commonjs", "cjs"):
                    findings.append(Finding("M2", "warning",
                        f"sourceType: 'script' but modules is '{modules}'",
                        "sourceType should match module transform setting"))

    envs = config.get("env", {})
    if isinstance(envs, dict):
        known_envs = {"development", "production", "test", "staging"}
        for env_name, env_config in envs.items():
            if not env_config or (isinstance(env_config, dict) and not env_config):
                findings.append(Finding("E1", "warning",
                    f"Empty env config section: '{env_name}'"))
            if env_name not in known_envs:
                findings.append(Finding("E3", "warning",
                    f"Uncommon env name: '{env_name}'",
                    f"Common env names: {', '.join(sorted(known_envs))}"))

    overrides = config.get("overrides", [])
    if isinstance(overrides, list):
        for i, ov in enumerate(overrides):
            if isinstance(ov, dict) and "test" not in ov and "include" not in ov and "exclude" not in ov:
                findings.append(Finding("E2", "warning",
                    f"Override #{i+1} has no test/include/exclude pattern",
                    "Overrides without a file pattern apply to all files"))

    if isinstance(plugins, list):
        loose_settings = {}
        for p in plugins:
            opts = get_plugin_options(p)
            pn = get_plugin_name(p)
            if "loose" in opts:
                loose_settings[pn] = opts["loose"]
        if loose_settings:
            values = set(loose_settings.values())
            if len(values) > 1:
                findings.append(Finding("B1", "warning",
                    "Inconsistent loose mode across plugins",
                    "Some plugins have loose: true, others false — this can cause subtle bugs"))

    targets = config.get("targets")
    has_targets_in_preset = False
    if isinstance(presets, list):
        for p in presets:
            if isinstance(p, list) and len(p) > 1 and isinstance(p[1], dict):
                if "targets" in p[1]:
                    has_targets_in_preset = True
    if not targets and not has_targets_in_preset:
        findings.append(Finding("B2", "warning",
            "No targets or browserslist configuration",
            "Without targets, Babel transpiles to ES5 which produces larger output"))

    return findings


def format_text(findings, filepath):
    if not findings:
        return f"✅ {filepath}: No issues found"
    lines = [f"📋 {filepath}: {len(findings)} issue(s) found\n"]
    for f in findings:
        lines.append(f.to_text())
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    lines.append(f"\n{'❌' if errors else '⚠️'} {errors} error(s), {warnings} warning(s)")
    return "\n".join(lines)


def format_json(findings, filepath):
    return json.dumps({
        "file": filepath,
        "findings": [f.to_dict() for f in findings],
        "summary": {
            "errors": sum(1 for f in findings if f.severity == "error"),
            "warnings": sum(1 for f in findings if f.severity == "warning"),
            "total": len(findings),
        }
    }, indent=2)


def format_summary(findings, filepath):
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return f"{status} | {filepath} | {errors} errors, {warnings} warnings"


def explain_config(config, filepath):
    lines = [f"📖 Babel Config Explanation: {filepath}\n"]

    presets = config.get("presets", [])
    if presets:
        lines.append("Presets (applied in reverse order):")
        for p in presets:
            pn = get_preset_name(p)
            opts = {}
            if isinstance(p, list) and len(p) > 1:
                opts = p[1] if isinstance(p[1], dict) else {}
            desc = f"  • {pn}"
            if opts:
                desc += f" (options: {json.dumps(opts, default=str)[:80]})"
            lines.append(desc)

    plugins = config.get("plugins", [])
    if plugins:
        lines.append("\nPlugins (applied in order):")
        for p in plugins:
            pn = get_plugin_name(p)
            lines.append(f"  • {pn}")

    targets = config.get("targets")
    if targets:
        lines.append(f"\nTargets: {json.dumps(targets, default=str)}")

    envs = config.get("env", {})
    if envs:
        lines.append(f"\nEnvironment overrides: {', '.join(envs.keys())}")

    overrides = config.get("overrides", [])
    if overrides:
        lines.append(f"\nFile overrides: {len(overrides)} section(s)")

    return "\n".join(lines)


def suggest_improvements(config, filepath):
    lines = [f"💡 Suggestions for {filepath}\n"]
    suggestions = []

    presets = config.get("presets", [])
    preset_names = [get_preset_name(p) for p in presets] if isinstance(presets, list) else []

    if not any("preset-env" in pn for pn in preset_names):
        suggestions.append("Add @babel/preset-env for automatic polyfill and syntax targeting")

    if any("preset-react" in pn for pn in preset_names):
        for p in presets:
            if isinstance(p, list) and "preset-react" in get_preset_name(p):
                opts = p[1] if len(p) > 1 and isinstance(p[1], dict) else {}
                if opts.get("runtime") != "automatic":
                    suggestions.append("Set runtime: 'automatic' in preset-react (no need to import React in every file)")

    plugins = config.get("plugins", [])
    if isinstance(plugins, list):
        for pn_raw in plugins:
            pn = get_plugin_name(pn_raw)
            if pn in DEPRECATED_PLUGINS:
                suggestions.append(f"Remove {pn} — {DEPRECATED_PLUGINS[pn]}")

    if not config.get("targets"):
        has_preset_targets = False
        for p in presets:
            if isinstance(p, list) and len(p) > 1 and isinstance(p[1], dict) and "targets" in p[1]:
                has_preset_targets = True
        if not has_preset_targets:
            suggestions.append("Add targets (e.g., browserslist) to reduce output size")

    assumptions = config.get("assumptions")
    if not assumptions:
        suggestions.append("Consider adding 'assumptions' for smaller output (e.g., noDocumentAll, setPublicClassFields)")

    if not suggestions:
        lines.append("No suggestions — config looks good!")
    else:
        for s in suggestions:
            lines.append(f"  • {s}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: babel_config_validator.py <command> <file> [--format text|json|summary] [--strict]")
        print("Commands: validate, check, explain, suggest")
        sys.exit(2)

    command = sys.argv[1]
    filepath = sys.argv[2]
    fmt = "text"
    strict = False
    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]
        if arg == "--strict":
            strict = True

    config, error = load_config(filepath)
    if error:
        if command in ("validate", "check"):
            finding = Finding("S1" if "not found" in error else "S5", "error", error)
            if fmt == "json":
                print(format_json([finding], filepath))
            elif fmt == "summary":
                print(format_summary([finding], filepath))
            else:
                print(finding.to_text())
            sys.exit(2 if "not found" in error else 1)
        else:
            print(f"❌ {error}")
            sys.exit(2)

    if not isinstance(config, dict):
        print("❌ Config must be a JSON object")
        sys.exit(1)

    if command == "explain":
        print(explain_config(config, filepath))
        sys.exit(0)

    if command == "suggest":
        print(suggest_improvements(config, filepath))
        sys.exit(0)

    findings = validate(config, filepath)

    if command == "check":
        findings = [f for f in findings if f.rule_id.startswith("S")]

    if strict:
        for f in findings:
            if f.severity == "warning":
                f.severity = "error"

    if fmt == "json":
        print(format_json(findings, filepath))
    elif fmt == "summary":
        print(format_summary(findings, filepath))
    else:
        print(format_text(findings, filepath))

    errors = sum(1 for f in findings if f.severity == "error")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
