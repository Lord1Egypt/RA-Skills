#!/usr/bin/env python3
"""Biome Config Validator — validate biome.json for structure, conflicts, deprecated options."""

import sys
import os
import json
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    file: str
    path: str  # JSON path
    rule: str
    severity: Severity
    message: str
    category: str


VALID_TOP_LEVEL = {
    '$schema', 'extends', 'files', 'vcs', 'formatter', 'linter',
    'javascript', 'typescript', 'json', 'css', 'graphql',
    'organizeImports', 'overrides', 'assists'
}

VALID_FORMATTER_KEYS = {
    'enabled', 'formatWithErrors', 'indentStyle', 'indentWidth',
    'lineWidth', 'lineEnding', 'attributePosition', 'bracketSpacing',
    'ignore', 'include'
}

VALID_LINTER_KEYS = {'enabled', 'rules', 'ignore', 'include'}

VALID_RULE_GROUPS = {
    'recommended', 'all', 'nursery', 'suspicious', 'correctness',
    'style', 'complexity', 'performance', 'security', 'a11y'
}

KNOWN_RULES = {
    'suspicious': [
        'noArrayIndexKey', 'noAssignInExpressions', 'noAsyncPromiseExecutor',
        'noCatchAssign', 'noClassAssign', 'noCommentText', 'noCompareNegZero',
        'noConfusingLabels', 'noConfusingVoidType', 'noConsoleLog',
        'noConstEnum', 'noControlCharactersInRegex', 'noDebugger',
        'noDoubleEquals', 'noDuplicateCase', 'noDuplicateClassMembers',
        'noDuplicateJsxProps', 'noDuplicateObjectKeys', 'noDuplicateParameters',
        'noEmptyInterface', 'noExplicitAny', 'noExtraNonNullAssertion',
        'noFallthroughSwitchClause', 'noFunctionAssign', 'noGlobalAssign',
        'noImportAssign', 'noLabelVar', 'noMisleadingCharacterClass',
        'noPrototypeBuiltins', 'noRedeclare', 'noRedundantUseStrict',
        'noSelfCompare', 'noShadowRestrictedNames', 'noSparseArray',
        'noUnsafeDeclarationMerging', 'noUnsafeNegation',
    ],
    'correctness': [
        'noChildrenProp', 'noConstAssign', 'noConstructorReturn',
        'noEmptyCharacterClassInRegex', 'noEmptyPattern', 'noGlobalObjectCalls',
        'noInnerDeclarations', 'noInvalidConstructorSuper',
        'noInvalidNewBuiltin', 'noNewSymbol', 'noNodejsModules',
        'noNonoctalDecimalEscape', 'noPrecisionLoss', 'noRenderReturnValue',
        'noSetterReturn', 'noStringCaseMismatch', 'noSwitchDeclarations',
        'noUndeclaredVariables', 'noUnnecessaryContinue', 'noUnreachable',
        'noUnreachableSuper', 'noUnsafeFinally', 'noUnsafeOptionalChaining',
        'noUnusedLabels', 'noUnusedVariables', 'noVoidElementsWithChildren',
        'noVoidTypeReturn', 'useExhaustiveDependencies', 'useIsNan',
        'useValidForDirection', 'useYield',
    ],
    'style': [
        'noArguments', 'noCommaOperator', 'noDefaultExport',
        'noImplicitBoolean', 'noInferrableTypes', 'noNamespace',
        'noNegationElse', 'noNonNullAssertion', 'noParameterAssign',
        'noParameterProperties', 'noRestrictedGlobals', 'noShoutyConstants',
        'noUnusedTemplateLiteral', 'noUselessElse', 'noVar',
        'useBlockStatements', 'useCollapsedElseIf', 'useConst',
        'useDefaultParameterLast', 'useEnumInitializers',
        'useExponentiationOperator', 'useExportType', 'useFilenamingConvention',
        'useForOf', 'useFragmentSyntax', 'useImportType',
        'useLiteralEnumMembers', 'useNamingConvention', 'useNodejsImportProtocol',
        'useNumberNamespace', 'useNumericLiterals', 'useSelfClosingElements',
        'useShorthandArrayType', 'useShorthandAssign', 'useShorthandFunctionType',
        'useSingleCaseStatement', 'useSingleVarDeclarator', 'useTemplate',
    ],
    'complexity': [
        'noBannedTypes', 'noExcessiveCognitiveComplexity',
        'noExtraBooleanCast', 'noForEach', 'noMultipleSpacesInRegularExpressionLiterals',
        'noStaticOnlyClass', 'noThisInStatic', 'noUselessCatch',
        'noUselessConstructor', 'noUselessEmptyExport', 'noUselessFragments',
        'noUselessLabel', 'noUselessLoneBlockStatements', 'noUselessRename',
        'noUselessSwitchCase', 'noUselessTernary', 'noUselessThisAlias',
        'noUselessTypeConstraint', 'noVoid', 'noWith',
        'useFlatMap', 'useLiteralKeys', 'useOptionalChain',
        'useRegexLiterals', 'useSimpleNumberKeys', 'useSimplifiedLogicExpression',
    ],
    'performance': [
        'noAccumulatingSpread', 'noBarrelFile', 'noDelete',
        'noReExportAll',
    ],
    'security': [
        'noDangerouslySetInnerHtml', 'noDangerouslySetInnerHtmlWithChildren',
        'noGlobalEval',
    ],
    'a11y': [
        'noAccessKey', 'noAriaHiddenOnFocusable', 'noAriaUnsupportedElements',
        'noAutofocus', 'noBlankTarget', 'noDistractingElements',
        'noHeaderScope', 'noInteractiveElementToNoninteractiveRole',
        'noNoninteractiveElementToInteractiveRole', 'noNoninteractiveTabindex',
        'noPositiveTabindex', 'noRedundantAlt', 'noRedundantRoles',
        'noSvgWithoutTitle', 'useAltText', 'useAnchorContent',
        'useAriaActivedescendantWithTabindex', 'useAriaPropsForRole',
        'useButtonType', 'useHeadingContent', 'useHtmlLang',
        'useIframeTitle', 'useKeyWithClickEvents', 'useKeyWithMouseEvents',
        'useMediaCaption', 'useValidAnchor', 'useValidAriaProps',
        'useValidAriaRole', 'useValidAriaValues', 'useValidLang',
    ],
}

ALL_KNOWN_RULES = set()
RULE_TO_GROUP = {}
for group, rules in KNOWN_RULES.items():
    for r in rules:
        ALL_KNOWN_RULES.add(r)
        RULE_TO_GROUP[r] = group

DEPRECATED_RULES = {
    'noExcessiveComplexity': 'noExcessiveCognitiveComplexity',
    'useShorthandFunctionType': 'useShorthandFunctionType',
    'noImplicitAnyLet': 'removed in Biome 2.0',
}

CONFLICTING_PAIRS = [
    ('useConst', 'noVar'),  # not conflicting, complementary - skip
    ('noDefaultExport', 'useFilenamingConvention'),  # can conflict
]

VALID_INDENT_STYLES = {'tab', 'space'}
VALID_QUOTE_STYLES = {'double', 'single'}
VALID_LINE_ENDINGS = {'lf', 'crlf', 'cr'}
VALID_SEVERITIES = {'error', 'warn', 'off', 'info'}


def load_config(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, OSError) as e:
        return None, str(e)

    try:
        config = json.loads(content)
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"

    return config, None


def lint_structure(filepath, config):
    issues = []

    for key in config:
        if key not in VALID_TOP_LEVEL:
            issues.append(Issue(filepath, key, "unknown-top-level", Severity.WARNING,
                                f"Unknown top-level key '{key}'", "structure"))

    schema = config.get('$schema', '')
    if schema and 'biomejs.dev' not in schema and 'biome' not in schema.lower():
        issues.append(Issue(filepath, '$schema', "invalid-schema", Severity.WARNING,
                            f"$schema URL doesn't appear to be a Biome schema", "structure"))

    if 'linter' not in config:
        issues.append(Issue(filepath, '', "missing-linter", Severity.INFO,
                            "No 'linter' section — Biome defaults will be used", "structure"))

    if 'formatter' not in config:
        issues.append(Issue(filepath, '', "missing-formatter", Severity.INFO,
                            "No 'formatter' section — Biome defaults will be used", "structure"))

    for section in ('files', 'formatter', 'linter'):
        sect = config.get(section, {})
        if isinstance(sect, dict):
            for pat_key in ('ignore', 'include'):
                patterns = sect.get(pat_key, [])
                if isinstance(patterns, list):
                    for pat in patterns:
                        if isinstance(pat, str) and pat.strip() == '':
                            issues.append(Issue(filepath, f"{section}.{pat_key}",
                                                "empty-pattern", Severity.WARNING,
                                                f"Empty pattern in {section}.{pat_key}", "structure"))

    extends = config.get('extends', [])
    if isinstance(extends, list):
        for ext in extends:
            if isinstance(ext, str) and not ext.startswith('@') and not os.path.exists(ext):
                base_dir = os.path.dirname(filepath)
                full_path = os.path.join(base_dir, ext)
                if not os.path.exists(full_path):
                    issues.append(Issue(filepath, 'extends', "missing-extends", Severity.WARNING,
                                        f"Extended config '{ext}' not found", "structure"))

    return issues


def lint_rules(filepath, config):
    issues = []
    linter = config.get('linter', {})
    if not isinstance(linter, dict):
        return issues

    rules = linter.get('rules', {})
    if not isinstance(rules, dict):
        return issues

    for group_name, group_config in rules.items():
        if group_name in ('recommended', 'all'):
            continue

        if group_name not in VALID_RULE_GROUPS and group_name != 'nursery':
            issues.append(Issue(filepath, f"linter.rules.{group_name}",
                                "unknown-rule-group", Severity.WARNING,
                                f"Unknown rule group '{group_name}'", "linting"))
            continue

        if not isinstance(group_config, dict):
            continue

        if not group_config:
            issues.append(Issue(filepath, f"linter.rules.{group_name}",
                                "empty-rule-group", Severity.INFO,
                                f"Rule group '{group_name}' is empty", "linting"))
            continue

        for rule_name, rule_config in group_config.items():
            if rule_name in ('recommended', 'all'):
                continue

            if rule_name in DEPRECATED_RULES:
                replacement = DEPRECATED_RULES[rule_name]
                issues.append(Issue(filepath, f"linter.rules.{group_name}.{rule_name}",
                                    "deprecated-rule", Severity.WARNING,
                                    f"Rule '{rule_name}' is deprecated → {replacement}", "linting"))

            if rule_name in RULE_TO_GROUP:
                expected_group = RULE_TO_GROUP[rule_name]
                if group_name != expected_group and group_name != 'nursery':
                    issues.append(Issue(filepath, f"linter.rules.{group_name}.{rule_name}",
                                        "rule-wrong-group", Severity.ERROR,
                                        f"Rule '{rule_name}' belongs in '{expected_group}', "
                                        f"not '{group_name}'", "linting"))
            elif rule_name not in ALL_KNOWN_RULES and group_name != 'nursery':
                issues.append(Issue(filepath, f"linter.rules.{group_name}.{rule_name}",
                                    "unknown-rule", Severity.WARNING,
                                    f"Unknown rule '{rule_name}' in group '{group_name}'", "linting"))

            severity = None
            if isinstance(rule_config, str):
                severity = rule_config
            elif isinstance(rule_config, dict):
                severity = rule_config.get('level', '')
            if severity and severity not in VALID_SEVERITIES:
                issues.append(Issue(filepath, f"linter.rules.{group_name}.{rule_name}",
                                    "invalid-severity", Severity.ERROR,
                                    f"Invalid severity '{severity}' for rule '{rule_name}' "
                                    f"(valid: {', '.join(sorted(VALID_SEVERITIES))})", "linting"))

    enabled_rules = set()
    for group_name, group_config in rules.items():
        if not isinstance(group_config, dict):
            continue
        for rule_name, rule_config in group_config.items():
            sev = rule_config if isinstance(rule_config, str) else (
                rule_config.get('level', '') if isinstance(rule_config, dict) else '')
            if sev and sev != 'off':
                enabled_rules.add(rule_name)

    return issues


def lint_formatter(filepath, config):
    issues = []
    formatter = config.get('formatter', {})
    if not isinstance(formatter, dict):
        return issues

    indent_style = formatter.get('indentStyle', 'tab')
    indent_width = formatter.get('indentWidth', 2)

    if indent_style not in VALID_INDENT_STYLES:
        issues.append(Issue(filepath, 'formatter.indentStyle', "invalid-indent-style", Severity.ERROR,
                            f"Invalid indent style '{indent_style}' (valid: tab, space)", "formatting"))

    if isinstance(indent_width, int):
        if indent_width < 1 or indent_width > 16:
            issues.append(Issue(filepath, 'formatter.indentWidth', "invalid-indent-width", Severity.ERROR,
                                f"Indent width {indent_width} out of range (1-16)", "formatting"))

    line_width = formatter.get('lineWidth', 80)
    if isinstance(line_width, int):
        if line_width < 20:
            issues.append(Issue(filepath, 'formatter.lineWidth', "line-width-too-small", Severity.WARNING,
                                f"Line width {line_width} is unusually small (< 20)", "formatting"))
        elif line_width > 320:
            issues.append(Issue(filepath, 'formatter.lineWidth', "line-width-too-large", Severity.WARNING,
                                f"Line width {line_width} is unusually large (> 320)", "formatting"))

    line_ending = formatter.get('lineEnding', '')
    if line_ending and line_ending not in VALID_LINE_ENDINGS:
        issues.append(Issue(filepath, 'formatter.lineEnding', "invalid-line-ending", Severity.ERROR,
                            f"Invalid line ending '{line_ending}' (valid: lf, crlf, cr)", "formatting"))

    for lang in ('javascript', 'typescript', 'json', 'css'):
        lang_config = config.get(lang, {})
        if isinstance(lang_config, dict):
            lang_fmt = lang_config.get('formatter', {})
            if isinstance(lang_fmt, dict):
                quote_style = lang_fmt.get('quoteStyle', '')
                if quote_style and quote_style not in VALID_QUOTE_STYLES:
                    issues.append(Issue(filepath, f'{lang}.formatter.quoteStyle',
                                        "invalid-quote-style", Severity.ERROR,
                                        f"Invalid quote style '{quote_style}' in {lang} "
                                        f"(valid: double, single)", "formatting"))

                lang_indent = lang_fmt.get('indentWidth')
                if lang_indent and isinstance(lang_indent, int) and isinstance(indent_width, int):
                    if lang_indent != indent_width:
                        issues.append(Issue(filepath, f'{lang}.formatter.indentWidth',
                                            "indent-width-mismatch", Severity.INFO,
                                            f"{lang} indent width ({lang_indent}) differs from "
                                            f"global ({indent_width})", "formatting"))

    return issues


def lint_best_practices(filepath, config):
    issues = []

    if 'vcs' not in config:
        issues.append(Issue(filepath, '', "missing-vcs", Severity.INFO,
                            "No 'vcs' section — consider enabling VCS integration", "best-practices"))

    if 'organizeImports' not in config:
        issues.append(Issue(filepath, '', "missing-organize-imports", Severity.INFO,
                            "No 'organizeImports' section — consider enabling import organization",
                            "best-practices"))

    files = config.get('files', {})
    if isinstance(files, dict):
        ignore = files.get('ignore', [])
        if isinstance(ignore, list):
            broad_patterns = ['*', '**', '**/*']
            for pat in ignore:
                if isinstance(pat, str) and pat in broad_patterns:
                    issues.append(Issue(filepath, 'files.ignore', "overly-broad-ignore", Severity.WARNING,
                                        f"Overly broad ignore pattern '{pat}' — ignores everything",
                                        "best-practices"))

    linter = config.get('linter', {})
    if isinstance(linter, dict):
        if linter.get('enabled') is False:
            issues.append(Issue(filepath, 'linter.enabled', "linter-disabled", Severity.WARNING,
                                "Linter is disabled — consider enabling for code quality",
                                "best-practices"))

    formatter = config.get('formatter', {})
    if isinstance(formatter, dict):
        if formatter.get('enabled') is False:
            issues.append(Issue(filepath, 'formatter.enabled', "formatter-disabled", Severity.WARNING,
                                "Formatter is disabled — consider enabling for consistent style",
                                "best-practices"))

    for lang in ('javascript', 'typescript'):
        if lang not in config:
            issues.append(Issue(filepath, '', f"missing-{lang}-config", Severity.INFO,
                                f"No '{lang}' section — language-specific settings use defaults",
                                "best-practices"))

    return issues


def format_text(issues):
    if not issues:
        return "\033[32m\u2714 No issues found\033[0m"

    icons = {Severity.ERROR: "\033[31m\u2716\033[0m", Severity.WARNING: "\033[33m\u26a0\033[0m",
             Severity.INFO: "\033[36m\u2139\033[0m"}
    lines = []
    current_file = None
    for issue in sorted(issues, key=lambda i: (i.file, i.severity.value)):
        if issue.file != current_file:
            current_file = issue.file
            lines.append(f"\n\033[1m{current_file}\033[0m")
        icon = icons.get(issue.severity, "")
        path_str = f" ({issue.path})" if issue.path else ""
        lines.append(f"  {icon} {issue.rule}{path_str} — {issue.message}")

    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    lines.append(f"\n{errors} error(s), {warnings} warning(s), {infos} info(s)")
    return '\n'.join(lines)


def format_json(issues):
    return json.dumps([{
        'file': i.file, 'path': i.path, 'rule': i.rule,
        'severity': i.severity.value, 'message': i.message,
        'category': i.category
    } for i in issues], indent=2)


def format_summary(issues):
    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    return f"Errors: {errors} | Warnings: {warnings} | Info: {infos} | Total: {len(issues)}"


def main():
    if len(sys.argv) < 3:
        print("Usage: biome_config_validator.py <command> <biome.json> [options]")
        print("Commands: lint, conflicts, deprecated, validate")
        print("Options: --format json|text|summary")
        sys.exit(2)

    command = sys.argv[1]
    filepath = sys.argv[2]
    fmt = 'text'

    for i, arg in enumerate(sys.argv):
        if arg == '--format' and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]

    config, error = load_config(filepath)
    if error:
        print(f"Error: {error}")
        sys.exit(2)

    if not isinstance(config, dict):
        print("Error: biome.json root must be an object")
        sys.exit(2)

    issues = []
    if command == 'lint':
        issues.extend(lint_structure(filepath, config))
        issues.extend(lint_rules(filepath, config))
        issues.extend(lint_formatter(filepath, config))
        issues.extend(lint_best_practices(filepath, config))
    elif command == 'conflicts':
        issues.extend(lint_rules(filepath, config))
    elif command == 'deprecated':
        issues.extend([i for i in lint_rules(filepath, config) if i.rule == 'deprecated-rule'])
    elif command == 'validate':
        issues.extend(lint_structure(filepath, config))
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)

    if fmt == 'json':
        print(format_json(issues))
    elif fmt == 'summary':
        print(format_summary(issues))
    else:
        print(format_text(issues))

    has_errors = any(i.severity == Severity.ERROR for i in issues)
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
