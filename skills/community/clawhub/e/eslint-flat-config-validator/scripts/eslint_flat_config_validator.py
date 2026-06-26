#!/usr/bin/env python3
"""
ESLint Flat Config Validator
Validate ESLint v9+ flat configuration files (JSON-exported) for structural
correctness, language options, rules configuration, plugin hygiene, file
patterns, and best practices.
Usage: python3 eslint_flat_config_validator.py <command> <file> [--strict] [--format text|json|summary]
Commands: validate, lint, rules, plugins
"""

import sys
import os
import re
import json
import argparse
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_CONFIG_KEYS = {
    "files", "ignores", "languageOptions", "linterOptions", "plugins",
    "processor", "rules", "settings", "name",
}

VALID_SEVERITY_STRINGS = {"off", "warn", "error"}
VALID_SEVERITY_NUMBERS = {0, 1, 2}

VALID_SOURCE_TYPES = {"module", "script", "commonjs"}

VALID_GLOBAL_VALUES = {"readonly", "writable", "off", "readable"}
VALID_GLOBAL_BOOLEANS = {True, False}

DEPRECATED_RULES = {
    "no-buffer-constructor": "Deprecated in ESLint v7. Use Buffer.from() / Buffer.alloc() instead.",
    "no-new-require": "Deprecated in ESLint v7. Use ESM imports.",
    "no-path-concat": "Deprecated in ESLint v7. Use path.join() or path.resolve().",
    "no-process-env": "Deprecated in ESLint v7.",
    "no-process-exit": "Deprecated in ESLint v7. Use process.exitCode instead.",
    "no-restricted-modules": "Deprecated in ESLint v7. Use no-restricted-imports.",
    "no-sync": "Deprecated in ESLint v7.",
    "no-mixed-requires": "Deprecated in ESLint v7.",
    "callback-return": "Deprecated in ESLint v7.",
    "global-require": "Deprecated in ESLint v7. Use ESM imports.",
    "handle-callback-err": "Deprecated in ESLint v7.",
    "no-catch-shadow": "Deprecated. Use no-shadow instead.",
    "no-native-reassign": "Deprecated. Use no-global-assign instead.",
    "no-negated-in-lhs": "Deprecated. Use no-unsafe-negation instead.",
    "no-spaced-func": "Deprecated. Use func-call-spacing instead.",
    "prefer-reflect": "Deprecated in ESLint v7.",
    "require-jsdoc": "Deprecated in ESLint v5.10.",
    "valid-jsdoc": "Deprecated in ESLint v5.10.",
    "id-blacklist": "Deprecated. Use id-denylist instead.",
    "no-return-await": "Deprecated in ESLint v8.46. Use @typescript-eslint/return-await for TS.",
}

CONFLICTING_RULE_PAIRS = [
    ("indent", "@typescript-eslint/indent"),
    ("no-unused-vars", "@typescript-eslint/no-unused-vars"),
    ("no-shadow", "@typescript-eslint/no-shadow"),
    ("no-use-before-define", "@typescript-eslint/no-use-before-define"),
    ("no-redeclare", "@typescript-eslint/no-redeclare"),
    ("no-loop-func", "@typescript-eslint/no-loop-func"),
    ("no-extra-semi", "@typescript-eslint/no-extra-semi"),
    ("no-empty-function", "@typescript-eslint/no-empty-function"),
    ("semi", "@typescript-eslint/semi"),
    ("quotes", "@typescript-eslint/quotes"),
    ("comma-dangle", "@typescript-eslint/comma-dangle"),
    ("brace-style", "@typescript-eslint/brace-style"),
    ("no-array-constructor", "@typescript-eslint/no-array-constructor"),
    ("no-dupe-class-members", "@typescript-eslint/no-dupe-class-members"),
    ("no-loss-of-precision", "@typescript-eslint/no-loss-of-precision"),
]


# ---------------------------------------------------------------------------
# Finding class
# ---------------------------------------------------------------------------

class Finding:
    """A single validation finding."""

    SEVERITIES = ("error", "warning", "info")

    def __init__(self, rule_id: str, severity: str, message: str, detail: str = ""):
        assert severity in self.SEVERITIES, f"Invalid severity: {severity}"
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.detail = detail

    def to_dict(self) -> dict:
        d = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
        }
        if self.detail:
            d["detail"] = self.detail
        return d

    def __repr__(self):
        return f"Finding({self.rule_id}, {self.severity}, {self.message!r})"


# ---------------------------------------------------------------------------
# JSON loading
# ---------------------------------------------------------------------------

def load_config(path: str) -> tuple:
    """Load and parse an ESLint flat config JSON file. Returns (data, error_finding)."""
    # S1: File not found or unreadable
    if not os.path.exists(path):
        return None, Finding("S1", "error", f"File not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return None, Finding("S1", "error", f"Cannot read file: {e}")

    # S2: Empty config
    if len(content.strip()) == 0:
        return None, Finding("S2", "error", "Config file is empty")

    # S3: Invalid JSON syntax
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return None, Finding("S3", "error", f"Invalid JSON syntax: {e}")

    # S4: Not an array (flat config must be array)
    if not isinstance(data, list):
        return None, Finding("S4", "error",
            "Flat config must be a JSON array of config objects (got {})".format(
                type(data).__name__))

    # S2: Empty array
    if len(data) == 0:
        return None, Finding("S2", "error",
            "Config is an empty array — no config objects defined")

    return data, None


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------

def check_structure(data: list) -> list:
    """S5: Check for unknown top-level keys in config objects."""
    findings = []

    for i, obj in enumerate(data):
        idx = i + 1
        if not isinstance(obj, dict):
            findings.append(Finding("S4", "error",
                f"Config object #{idx} is not an object (got {type(obj).__name__})",
                "Each element in the flat config array must be a config object."))
            continue

        unknown = set(obj.keys()) - VALID_CONFIG_KEYS
        if unknown:
            for key in sorted(unknown):
                findings.append(Finding("S5", "warning",
                    f"Unknown top-level key in config object #{idx}: '{key}'",
                    f"'{key}' is not valid in flat config. Valid keys: "
                    f"{', '.join(sorted(VALID_CONFIG_KEYS))}"))

    return findings


def check_language_options(data: list) -> list:
    """L1-L5: Check languageOptions in config objects."""
    findings = []
    any_ecma_version = False

    for i, obj in enumerate(data):
        if not isinstance(obj, dict):
            continue
        idx = i + 1

        lang = obj.get("languageOptions")
        if lang is None:
            continue

        if not isinstance(lang, dict):
            findings.append(Finding("L1", "error",
                f"languageOptions in config object #{idx} must be an object",
                "Set languageOptions: { ecmaVersion: 'latest', sourceType: 'module' }"))
            continue

        # L1: Invalid ecmaVersion
        ecma = lang.get("ecmaVersion")
        if ecma is not None:
            any_ecma_version = True
            if isinstance(ecma, str):
                if ecma != "latest":
                    findings.append(Finding("L1", "error",
                        f"Invalid ecmaVersion in config object #{idx}: '{ecma}'",
                        "ecmaVersion must be a number >= 3 or 'latest'."))
            elif isinstance(ecma, (int, float)):
                ecma_int = int(ecma)
                if ecma_int < 3:
                    findings.append(Finding("L1", "error",
                        f"Invalid ecmaVersion in config object #{idx}: {ecma_int}",
                        "ecmaVersion must be >= 3. Common values: 2020, 2022, 2024, or 'latest'."))
            else:
                findings.append(Finding("L1", "error",
                    f"Invalid ecmaVersion type in config object #{idx}: {type(ecma).__name__}",
                    "ecmaVersion must be a number >= 3 or 'latest'."))

        # L2: Invalid sourceType
        source_type = lang.get("sourceType")
        if source_type is not None:
            if source_type not in VALID_SOURCE_TYPES:
                findings.append(Finding("L2", "error",
                    f"Invalid sourceType in config object #{idx}: '{source_type}'",
                    "sourceType must be 'module', 'script', or 'commonjs'."))

        # L3: Invalid parser value
        parser = lang.get("parser")
        if parser is not None:
            if isinstance(parser, str):
                findings.append(Finding("L3", "warning",
                    f"Parser in config object #{idx} is a string: '{parser}'",
                    "In flat config, parser should be a parser object (imported module), "
                    "not a string. Import the parser and pass the object directly."))
            elif isinstance(parser, dict):
                has_parse = "parse" in parser or "parseForESTree" in parser
                if not has_parse:
                    findings.append(Finding("L3", "warning",
                        f"Parser object in config object #{idx} missing parse/parseForESTree method",
                        "A valid parser object should have a 'parse' or 'parseForESTree' method."))

        # L4: globals with invalid values
        globals_obj = lang.get("globals")
        if isinstance(globals_obj, dict):
            for glob_name, glob_val in globals_obj.items():
                if isinstance(glob_val, str):
                    if glob_val.lower() not in VALID_GLOBAL_VALUES:
                        findings.append(Finding("L4", "error",
                            f"Invalid global value for '{glob_name}' in config object #{idx}: '{glob_val}'",
                            "Valid global values: 'readonly', 'writable', 'off', 'readable', true, false."))
                elif isinstance(glob_val, bool):
                    pass  # true/false are valid
                else:
                    findings.append(Finding("L4", "error",
                        f"Invalid global value type for '{glob_name}' in config object #{idx}: "
                        f"{type(glob_val).__name__}",
                        "Global values must be 'readonly', 'writable', 'off', true, or false."))

    # L5: Missing ecmaVersion hint
    if not any_ecma_version:
        has_any_lang = any(
            isinstance(obj, dict) and "languageOptions" in obj
            for obj in data
        )
        if has_any_lang:
            findings.append(Finding("L5", "info",
                "No ecmaVersion specified in any languageOptions",
                "ESLint v9 defaults ecmaVersion to 'latest'. Set it explicitly if you "
                "need to target a specific ECMAScript version."))

    return findings


def check_rules(data: list) -> list:
    """R1-R5: Check rules configuration."""
    findings = []
    any_rules = False
    all_rule_names = set()

    for i, obj in enumerate(data):
        if not isinstance(obj, dict):
            continue
        idx = i + 1

        rules = obj.get("rules")
        if rules is None:
            continue

        if not isinstance(rules, dict):
            findings.append(Finding("R5", "error",
                f"rules in config object #{idx} must be an object",
                "Set rules: { 'rule-name': 'error', ... }"))
            continue

        # R4: Empty rules object
        if len(rules) == 0:
            findings.append(Finding("R4", "info",
                f"Empty rules object in config object #{idx}",
                "The rules object is empty. Add rules or remove the key."))
            continue

        any_rules = True

        for rule_name, rule_config in rules.items():
            all_rule_names.add(rule_name)

            # R5: Rule config must be severity or [severity, ...options]
            severity = None
            if isinstance(rule_config, (int, float)):
                severity = int(rule_config)
            elif isinstance(rule_config, str):
                severity = rule_config
            elif isinstance(rule_config, list):
                if len(rule_config) == 0:
                    findings.append(Finding("R5", "error",
                        f"Rule '{rule_name}' in config object #{idx} has empty array config",
                        "Rule config array must have at least a severity: ['error', ...options]"))
                    continue
                severity = rule_config[0]
                if isinstance(severity, (int, float)):
                    severity = int(severity)
            else:
                findings.append(Finding("R5", "error",
                    f"Rule '{rule_name}' in config object #{idx} has invalid config type: "
                    f"{type(rule_config).__name__}",
                    "Rule config must be a severity ('off'/'warn'/'error' or 0/1/2) "
                    "or an array [severity, ...options]."))
                continue

            # R1: Unknown severity
            if severity is not None:
                valid = False
                if isinstance(severity, int) and severity in VALID_SEVERITY_NUMBERS:
                    valid = True
                elif isinstance(severity, str) and severity in VALID_SEVERITY_STRINGS:
                    valid = True
                if not valid:
                    findings.append(Finding("R1", "error",
                        f"Invalid rule severity for '{rule_name}' in config object #{idx}: "
                        f"{severity!r}",
                        "Severity must be 'off'/0, 'warn'/1, or 'error'/2."))

            # R2: Deprecated rule names
            if rule_name in DEPRECATED_RULES:
                findings.append(Finding("R2", "warning",
                    f"Deprecated rule '{rule_name}' in config object #{idx}",
                    DEPRECATED_RULES[rule_name]))

    # R3: Conflicting rules (across all config objects)
    for base_rule, ts_rule in CONFLICTING_RULE_PAIRS:
        if base_rule in all_rule_names and ts_rule in all_rule_names:
            findings.append(Finding("R3", "warning",
                f"Conflicting rules: '{base_rule}' and '{ts_rule}'",
                f"When using '{ts_rule}', disable the base rule '{base_rule}' "
                f"to avoid duplicate reports. Set '{base_rule}': 'off'."))

    return findings, any_rules


def check_plugins(data: list) -> list:
    """P1-P3: Check plugin configuration."""
    findings = []
    seen_plugins = {}  # plugin_key -> first config object index

    for i, obj in enumerate(data):
        if not isinstance(obj, dict):
            continue
        idx = i + 1

        plugins = obj.get("plugins")
        if plugins is None:
            continue

        if not isinstance(plugins, dict):
            findings.append(Finding("P2", "error",
                f"plugins in config object #{idx} must be an object",
                "Set plugins: { 'plugin-name': pluginObject, ... }"))
            continue

        # P1: Empty plugins object
        if len(plugins) == 0:
            findings.append(Finding("P1", "info",
                f"Empty plugins object in config object #{idx}",
                "The plugins object is empty. Add plugins or remove the key."))
            continue

        for plugin_key, plugin_val in plugins.items():
            # P2: Plugin value not object
            if not isinstance(plugin_val, dict):
                findings.append(Finding("P2", "error",
                    f"Plugin '{plugin_key}' in config object #{idx} is not an object "
                    f"(got {type(plugin_val).__name__})",
                    "Plugin values must be plugin objects (imported modules). "
                    "Import the plugin and pass the object directly."))

            # P3: Duplicate plugin across config objects
            if plugin_key in seen_plugins:
                prev_idx = seen_plugins[plugin_key]
                findings.append(Finding("P3", "warning",
                    f"Duplicate plugin '{plugin_key}' in config object #{idx} "
                    f"(first seen in #{prev_idx})",
                    "Plugins only need to be registered once. Registering the same "
                    "plugin in multiple config objects is redundant."))
            else:
                seen_plugins[plugin_key] = idx

    return findings


def check_files_ignores(data: list) -> list:
    """F1-F4: Check files and ignores configuration."""
    findings = []

    for i, obj in enumerate(data):
        if not isinstance(obj, dict):
            continue
        idx = i + 1

        files = obj.get("files")
        ignores = obj.get("ignores")

        # F1: Missing files pattern (non-global config hint)
        has_files = files is not None
        has_ignores = ignores is not None
        has_rules = "rules" in obj or "plugins" in obj or "languageOptions" in obj
        if not has_files and not has_ignores and has_rules:
            findings.append(Finding("F1", "info",
                f"Config object #{idx} has no files/ignores — applies globally",
                "Config objects without files or ignores apply to all files. "
                "Add a files pattern to scope this config (e.g., files: ['**/*.js'])."))

        # F3: files as string instead of array
        if files is not None:
            if isinstance(files, str):
                findings.append(Finding("F3", "error",
                    f"files in config object #{idx} is a string instead of array",
                    "files must be an array of glob patterns: "
                    "files: ['**/*.js', '**/*.ts']"))
            elif isinstance(files, list):
                # F2: Invalid glob patterns
                for pattern in files:
                    if isinstance(pattern, str) and len(pattern.strip()) == 0:
                        findings.append(Finding("F2", "error",
                            f"Empty glob pattern in files of config object #{idx}",
                            "Remove empty strings from the files array."))
                    elif isinstance(pattern, list):
                        # Nested array (files can be array of arrays for AND patterns)
                        for sub in pattern:
                            if isinstance(sub, str) and len(sub.strip()) == 0:
                                findings.append(Finding("F2", "error",
                                    f"Empty glob pattern in nested files array of config object #{idx}",
                                    "Remove empty strings from file patterns."))

        # F4: ignores as string instead of array
        if ignores is not None:
            if isinstance(ignores, str):
                findings.append(Finding("F4", "error",
                    f"ignores in config object #{idx} is a string instead of array",
                    "ignores must be an array of glob patterns: "
                    "ignores: ['node_modules/**', 'dist/**']"))
            elif isinstance(ignores, list):
                # F2: Invalid glob patterns in ignores
                for pattern in ignores:
                    if isinstance(pattern, str) and len(pattern.strip()) == 0:
                        findings.append(Finding("F2", "error",
                            f"Empty glob pattern in ignores of config object #{idx}",
                            "Remove empty strings from the ignores array."))

    return findings


def check_best_practices(data: list, any_rules: bool) -> list:
    """X1-X3: Check best practices."""
    findings = []

    # X1: No rules defined in any config object
    if not any_rules:
        findings.append(Finding("X1", "warning",
            "No rules defined in any config object",
            "At least one config object should define rules for ESLint to enforce "
            "anything. Add a rules object with your desired rule settings."))

    # X2: Many config objects (>20) suggest consolidation
    obj_count = len(data)
    if obj_count > 20:
        findings.append(Finding("X2", "warning",
            f"Config has {obj_count} objects — consider consolidation",
            "Having more than 20 config objects can make the config hard to maintain. "
            "Consider merging related configs or using shared config presets."))

    # X3: Missing name property
    for i, obj in enumerate(data):
        if not isinstance(obj, dict):
            continue
        idx = i + 1
        if "name" not in obj:
            findings.append(Finding("X3", "info",
                f"Config object #{idx} missing 'name' property",
                "Adding a name helps identify config objects in ESLint's debug output "
                "and error messages. Example: name: 'my-app/base'"))

    return findings


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def validate_all(data: list) -> list:
    """Run all checks and return combined findings."""
    findings = []
    findings.extend(check_structure(data))
    findings.extend(check_language_options(data))
    rules_findings, any_rules = check_rules(data)
    findings.extend(rules_findings)
    findings.extend(check_plugins(data))
    findings.extend(check_files_ignores(data))
    findings.extend(check_best_practices(data, any_rules))
    return findings


def validate_rules_only(data: list) -> list:
    """Run only rules-related checks (R1-R5, plus structure)."""
    findings = []
    findings.extend(check_structure(data))
    rules_findings, _ = check_rules(data)
    findings.extend(rules_findings)
    return findings


def validate_plugins_only(data: list) -> list:
    """Run only plugin-related checks (P1-P3, plus structure)."""
    findings = []
    findings.extend(check_structure(data))
    findings.extend(check_plugins(data))
    return findings


# ---------------------------------------------------------------------------
# Rule explanations
# ---------------------------------------------------------------------------

RULE_EXPLANATIONS = {
    "S1": {
        "name": "File Not Found",
        "category": "Structure",
        "severity": "error",
        "description": "The config JSON file does not exist or cannot be read.",
        "fix": "Ensure the file path is correct and the file has read permissions.",
    },
    "S2": {
        "name": "Empty Config",
        "category": "Structure",
        "severity": "error",
        "description": "The config file is empty or contains an empty array.",
        "fix": "Export your ESLint flat config to JSON: node -e \"import('./eslint.config.js').then(m => console.log(JSON.stringify(m.default)))\" > eslint.config.json",
    },
    "S3": {
        "name": "Invalid JSON",
        "category": "Structure",
        "severity": "error",
        "description": "The file contains invalid JSON syntax that cannot be parsed.",
        "fix": "Fix the JSON syntax error. Use a JSON linter or re-export from eslint.config.js.",
    },
    "S4": {
        "name": "Not an Array",
        "category": "Structure",
        "severity": "error",
        "description": "Flat config must be an array of config objects. Got a non-array value.",
        "fix": "Export the config as an array: export default [{ ... }, { ... }]",
    },
    "S5": {
        "name": "Unknown Config Key",
        "category": "Structure",
        "severity": "warning",
        "description": "A config object contains a key not recognized by ESLint v9 flat config.",
        "fix": "Valid keys: files, ignores, languageOptions, linterOptions, plugins, processor, rules, settings, name.",
    },
    "L1": {
        "name": "Invalid ecmaVersion",
        "category": "Language Options",
        "severity": "error",
        "description": "ecmaVersion must be a number >= 3 (e.g., 2020, 2024) or the string 'latest'.",
        "fix": "Set ecmaVersion to a year (2020-2024), a version number (3-15), or 'latest'.",
    },
    "L2": {
        "name": "Invalid sourceType",
        "category": "Language Options",
        "severity": "error",
        "description": "sourceType must be 'module', 'script', or 'commonjs'.",
        "fix": "Set sourceType: 'module' for ESM, 'commonjs' for CJS, or 'script' for plain scripts.",
    },
    "L3": {
        "name": "Invalid Parser",
        "category": "Language Options",
        "severity": "warning",
        "description": "Parser should be a parser object, not a string. In flat config, import the parser module.",
        "fix": "Import the parser: import tsParser from '@typescript-eslint/parser'; then use parser: tsParser.",
    },
    "L4": {
        "name": "Invalid Global Value",
        "category": "Language Options",
        "severity": "error",
        "description": "Global variable values must be 'readonly', 'writable', 'off', 'readable', true, or false.",
        "fix": "Use 'readonly'/'writable'/'off' or true (writable) / false (readonly).",
    },
    "L5": {
        "name": "Missing ecmaVersion",
        "category": "Language Options",
        "severity": "info",
        "description": "No ecmaVersion set. ESLint v9 defaults to 'latest'.",
        "fix": "Set ecmaVersion explicitly if targeting a specific ECMAScript version.",
    },
    "R1": {
        "name": "Invalid Severity",
        "category": "Rules",
        "severity": "error",
        "description": "Rule severity must be 'off'/0, 'warn'/1, or 'error'/2.",
        "fix": "Use 'off' (or 0), 'warn' (or 1), or 'error' (or 2) as the severity.",
    },
    "R2": {
        "name": "Deprecated Rule",
        "category": "Rules",
        "severity": "warning",
        "description": "A deprecated ESLint rule is in use. It may be removed in future versions.",
        "fix": "Remove the deprecated rule or replace with the recommended alternative.",
    },
    "R3": {
        "name": "Conflicting Rules",
        "category": "Rules",
        "severity": "warning",
        "description": "Both a base ESLint rule and its TypeScript-ESLint equivalent are enabled, causing duplicate reports.",
        "fix": "Disable the base rule when using the @typescript-eslint equivalent.",
    },
    "R4": {
        "name": "Empty Rules Object",
        "category": "Rules",
        "severity": "info",
        "description": "A config object has an empty rules object with no rule definitions.",
        "fix": "Add rules or remove the empty rules object.",
    },
    "R5": {
        "name": "Invalid Rule Config",
        "category": "Rules",
        "severity": "error",
        "description": "Rule config must be a severity value or an array with severity as the first element.",
        "fix": "Use 'error', ['error', options], or 2 / [2, options].",
    },
    "P1": {
        "name": "Empty Plugins Object",
        "category": "Plugins",
        "severity": "info",
        "description": "A config object has an empty plugins object.",
        "fix": "Add plugins or remove the empty plugins object.",
    },
    "P2": {
        "name": "Invalid Plugin Value",
        "category": "Plugins",
        "severity": "error",
        "description": "Plugin values must be plugin objects (imported modules), not strings or other types.",
        "fix": "Import the plugin: import pluginName from 'eslint-plugin-name'; then plugins: { name: pluginName }.",
    },
    "P3": {
        "name": "Duplicate Plugin",
        "category": "Plugins",
        "severity": "warning",
        "description": "The same plugin key appears in multiple config objects.",
        "fix": "Register each plugin once. Subsequent config objects can reference plugin rules without re-registering.",
    },
    "F1": {
        "name": "Global Config Object",
        "category": "Files/Ignores",
        "severity": "info",
        "description": "A config object has no files or ignores pattern, so it applies globally to all files.",
        "fix": "Add files: ['**/*.js'] to scope the config, or leave global intentionally.",
    },
    "F2": {
        "name": "Invalid Glob Pattern",
        "category": "Files/Ignores",
        "severity": "error",
        "description": "An empty string was found in files or ignores glob patterns.",
        "fix": "Remove empty strings from the glob pattern array.",
    },
    "F3": {
        "name": "Files as String",
        "category": "Files/Ignores",
        "severity": "error",
        "description": "files must be an array, not a string.",
        "fix": "Wrap the pattern in an array: files: ['**/*.js'] instead of files: '**/*.js'.",
    },
    "F4": {
        "name": "Ignores as String",
        "category": "Files/Ignores",
        "severity": "error",
        "description": "ignores must be an array, not a string.",
        "fix": "Wrap the pattern in an array: ignores: ['node_modules/**'] instead of ignores: 'node_modules/**'.",
    },
    "X1": {
        "name": "No Rules Defined",
        "category": "Best Practices",
        "severity": "warning",
        "description": "No config object defines any rules. ESLint will not enforce anything.",
        "fix": "Add rules to at least one config object, or extend a shared config that includes rules.",
    },
    "X2": {
        "name": "Too Many Config Objects",
        "category": "Best Practices",
        "severity": "warning",
        "description": "The config has more than 20 objects, which can be hard to maintain.",
        "fix": "Consolidate related configs or use shared config presets to reduce complexity.",
    },
    "X3": {
        "name": "Missing Name",
        "category": "Best Practices",
        "severity": "info",
        "description": "A config object is missing the 'name' property recommended in ESLint v9.",
        "fix": "Add name: 'my-app/base' to help identify configs in debug output.",
    },
}


# ---------------------------------------------------------------------------
# Summary helper
# ---------------------------------------------------------------------------

def _summary_counts(findings: list) -> dict:
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    return {"errors": errors, "warnings": warnings, "infos": infos, "total": len(findings)}


def _summary_text(findings: list) -> str:
    c = _summary_counts(findings)
    parts = []
    if c["errors"]:
        parts.append(f"{c['errors']} error(s)")
    if c["warnings"]:
        parts.append(f"{c['warnings']} warning(s)")
    if c["infos"]:
        parts.append(f"{c['infos']} info")
    return ", ".join(parts) if parts else "No issues found"


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_validate(data: list, path: str) -> dict:
    """Comprehensive validation with all rules and summary."""
    findings = validate_all(data)
    errors = [f for f in findings if f.severity == "error"]
    return {
        "command": "validate",
        "file": path,
        "valid": len(errors) == 0,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_lint(data: list, path: str) -> dict:
    """Run all rules (same as validate but labeled lint)."""
    findings = validate_all(data)
    has_errors = any(f.severity == "error" for f in findings)
    return {
        "command": "lint",
        "file": path,
        "passed": not has_errors,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_rules(data: list, path: str) -> dict:
    """Check rules configuration only."""
    findings = validate_rules_only(data)
    has_errors = any(f.severity == "error" for f in findings)
    return {
        "command": "rules",
        "file": path,
        "passed": not has_errors,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_plugins(data: list, path: str) -> dict:
    """Check plugin configuration only."""
    findings = validate_plugins_only(data)
    has_errors = any(f.severity == "error" for f in findings)
    return {
        "command": "plugins",
        "file": path,
        "passed": not has_errors,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    title = f"eslint.config {cmd} — {path}"
    lines.append(title)
    lines.append("=" * len(title))

    findings = result.get("findings", [])
    if not findings:
        lines.append("[OK] No issues found")
    else:
        for f in findings:
            sev = f["severity"].upper().ljust(7)
            lines.append(f"[{sev}] {f['rule_id']}: {f['message']}")
            if f.get("detail"):
                lines.append(f"         {f['detail']}")

    if "valid" in result:
        valid_str = "VALID" if result.get("valid") else "INVALID"
        lines.append("")
        lines.append(f"Result: {valid_str}")

    if "passed" in result:
        passed_str = "PASSED" if result.get("passed") else "FAILED"
        lines.append("")
        lines.append(f"Result: {passed_str}")

    summary = result.get("summary")
    if summary:
        lines.append(f"Summary: {summary}")

    return "\n".join(lines)


def format_json(result: dict) -> str:
    return json.dumps(result, indent=2)


def format_summary(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    lines.append(f"eslint.config {cmd}: {path}")

    counts = result.get("counts", {})
    lines.append(f"Errors: {counts.get('errors', 0)}")
    lines.append(f"Warnings: {counts.get('warnings', 0)}")
    lines.append(f"Info: {counts.get('infos', 0)}")

    if "valid" in result:
        lines.append(f"Valid: {'yes' if result['valid'] else 'no'}")
    if "passed" in result:
        lines.append(f"Passed: {'yes' if result['passed'] else 'no'}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate ESLint v9+ flat configuration files (JSON-exported)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Commands:
  validate   Comprehensive validation with all rules and summary
  lint       Run all rules
  rules      Check rules configuration
  plugins    Check plugin configuration

Export your eslint.config.js to JSON first:
  node -e "import('./eslint.config.js').then(m => console.log(JSON.stringify(m.default)))" > eslint.config.json

Examples:
  python3 eslint_flat_config_validator.py validate eslint.config.json
  python3 eslint_flat_config_validator.py validate eslint.config.json --strict
  python3 eslint_flat_config_validator.py lint eslint.config.json --format json
  python3 eslint_flat_config_validator.py rules eslint.config.json
  python3 eslint_flat_config_validator.py plugins eslint.config.json --format summary
"""
    )
    parser.add_argument("command", choices=["validate", "lint", "rules", "plugins"],
                        help="Command to run")
    parser.add_argument("file", help="Path to ESLint flat config JSON file")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (CI mode)")
    parser.add_argument("--format", choices=["text", "json", "summary"], default="text",
                        help="Output format (default: text)")

    args = parser.parse_args()

    # Load and parse file
    data, parse_error = load_config(args.file)
    if parse_error:
        result = {
            "command": args.command,
            "file": args.file,
            "findings": [parse_error.to_dict()],
            "counts": {"errors": 1, "warnings": 0, "infos": 0, "total": 1},
            "summary": "1 error(s)",
        }
        if args.command == "validate":
            result["valid"] = False
        elif args.command in ("lint", "rules", "plugins"):
            result["passed"] = False

        formatter = {"text": format_text, "json": format_json, "summary": format_summary}
        print(formatter[args.format](result))
        sys.exit(2)

    # Run command
    if args.command == "validate":
        result = cmd_validate(data, args.file)
    elif args.command == "lint":
        result = cmd_lint(data, args.file)
    elif args.command == "rules":
        result = cmd_rules(data, args.file)
    elif args.command == "plugins":
        result = cmd_plugins(data, args.file)

    # Format output
    formatter = {"text": format_text, "json": format_json, "summary": format_summary}
    print(formatter[args.format](result))

    # Exit code
    findings = result.get("findings", [])
    has_errors = any(f["severity"] == "error" for f in findings)
    has_warnings = any(f["severity"] == "warning" for f in findings)

    if has_errors:
        sys.exit(1)
    if args.strict and has_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
