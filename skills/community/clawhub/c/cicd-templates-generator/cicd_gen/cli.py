#!/usr/bin/env python3
"""CLI entry point for cicd-gen."""

import argparse
import sys
import os
from pathlib import Path

from cicd_gen.generator.github_actions import GitHubActionsGenerator
from cicd_gen.generator.gitlab_ci import GitLabCIGenerator
from cicd_gen.generator.jenkins import JenkinsGenerator


def parse_args():
    parser = argparse.ArgumentParser(
        prog="cicd-gen",
        description="Generate production-ready CI/CD workflows "
                    "(GitHub Actions, GitLab CI, Jenkins)",
    )
    parser.add_argument(
        "language",
        choices=["python", "javascript", "go"],
        help="Programming language",
    )
    parser.add_argument(
        "framework",
        nargs="?",
        help="Framework (e.g., flask, django, node, gin, echo)",
    )
    parser.add_argument(
        "--test", "-t",
        help="Test framework: pytest, unittest (Python), "
             "jest, mocha (JavaScript), go-test (Go)",
    )
    parser.add_argument(
        "--deploy", "-d",
        help="Deployment target: docker, azure, aliyun, tencent, k8s, serverless",
    )
    parser.add_argument(
        "--release", "-r",
        help="Release tool: npm (JS), goreleaser (Go)",
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Enable coverage reporting",
    )
    parser.add_argument(
        "--cloud",
        help="Cloud provider (for --deploy docker + cloud config)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["github", "gitlab", "jenkins", "all"],
        default="github",
        help="Output format (default: github)",
    )
    parser.add_argument(
        "--output", "-o",
        default="./.github/workflows",
        help="Output directory (default: ./.github/workflows)",
    )
    parser.add_argument(
        "--name", "-n",
        default="CI",
        help="Workflow name (default: CI)",
    )
    parser.add_argument(
        "--python-version",
        default="3.11",
        help="Python version (default: 3.11)",
    )
    parser.add_argument(
        "--node-version",
        default="20",
        help="Node.js version (default: 20)",
    )
    parser.add_argument(
        "--go-version",
        default="1.22",
        help="Go version (default: 1.22)",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print to stdout instead of writing files",
    )
    return parser.parse_args()


def get_generators():
    return {
        "github": GitHubActionsGenerator(),
        "gitlab": GitLabCIGenerator(),
        "jenkins": JenkinsGenerator(),
    }


def get_output_info(fmt, output_dir, language):
    if fmt == "github":
        return output_dir, "ci.yml"
    elif fmt == "gitlab":
        return "./", ".gitlab-ci.yml"
    elif fmt == "jenkins":
        return "./", "Jenkinsfile"


def main():
    args = parse_args()
    generators = get_generators()

    # Auto-detect test framework from language if not provided
    test = args.test
    if not test:
        if args.language == "python":
            test = "pytest"
        elif args.language == "javascript":
            test = "jest"
        elif args.language == "go":
            test = "go-test"

    kwargs = dict(
        language=args.language,
        framework=args.framework,
        test=test,
        deploy=args.deploy,
        release=args.release,
        coverage=args.coverage,
        cloud=args.cloud,
        name=args.name,
        python_version=args.python_version,
        node_version=args.node_version,
        go_version=args.go_version,
    )

    formats = ["github", "gitlab", "jenkins"] if args.format == "all" \
              else [args.format]

    exit_code = 0

    for fmt in formats:
        gen = generators[fmt]
        try:
            content = gen.generate(**kwargs)
        except ValueError as e:
            print(f"[cicd-gen] Error: {e}", file=sys.stderr)
            exit_code = 1
            continue

        out_dir, filename = get_output_info(fmt, args.output, args.language)

        if args.print_only:
            print(f"=== {fmt.upper()} ({filename}) ===")
            print(content)
            continue

        try:
            saved_path = gen.save(content, out_dir, filename)
            print(f"[cicd-gen] Generated: {saved_path}")
        except Exception as e:
            print(f"[cicd-gen] Save error: {e}", file=sys.stderr)
            exit_code = 2

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
