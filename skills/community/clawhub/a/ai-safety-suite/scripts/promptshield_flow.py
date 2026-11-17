#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
promptshield_flow.py — PromptShield (ai-safety-suite) orchestrator (read-only playbook router).

This is a thin DISPATCHER. It does NOT vendor or re-implement any sub-skill; it only
points you at the independently published sub-skill slug for each safety stage.
All real work is done by the referenced sub-skills.

Usage:
  python3 promptshield_flow.py --list
  python3 promptshield_flow.py --route guard
  python3 promptshield_flow.py --route tool-call-guard
"""
import sys
import argparse

# stage key -> (slug, when to use, expected output)
FLOW = [
    ("redteam", "agent-redteam-kit",
     "Before launch: adversarially stress-test the agent (confidential kit; capability name only).",
     "Scored attack-surface report + fix list."),
    ("drill", "prompt-injection-drill",
     "Generate adversarial injection samples to harden the agent against.",
     "Drill cases + pass/fail verdicts on your prompt type."),
    ("shield", "prompt-injection-shield",
     "Hostile user/tool input must be blocked at runtime.",
     "Allow/block guard decision for the given prompt."),
    ("leak", "prompt-leak-scanner",
     "Before shipping a system prompt: check it leaks internals/secrets.",
     "Leak findings list with line-level hints."),
    ("token-disclosure", "token-disclosure-check",
     "Before publishing any token/asset disclosure document externally.",
     "Disclosure-completeness verdict + missing items."),
    ("tool-guard", "tool-call-guard",
     "Before the agent calls external tools: gate the call by risk level.",
     "L0-L4 allow/block decision on the proposed call."),
    ("loop-guard", "agent-loop-guard",
     "Long-running agents that may loop, repeat-read, or drift off-task.",
     "Repeat/loop detection on the run trace + stop advice."),
    ("mcp-guard", "mcp-security-scan",
     "Before wiring a new MCP server / toolset into the agent.",
     "Risk findings + high-risk count for the MCP config."),
    ("gate", "skill-admission-gate",
     "Before any third-party skill enters the library.",
     "Admission gate verdict; blocks on blocking findings."),
]


# friendly aliases -> canonical stage key (so --route guard "just works")
ALIASES = {
    "guard": "tool-guard",
    "guards": "tool-guard",
    "loop": "loop-guard",
    "mcp": "mcp-guard",
    "leakscan": "leak",
    "token": "token-disclosure",
    "admission": "gate",
    "gate": "gate",
}


def main():
    ap = argparse.ArgumentParser(
        prog="promptshield-flow",
        description="PromptShield (ai-safety-suite) — read-only router over 9 published agent-runtime-safety sub-skills.")
    ap.add_argument("--list", action="store_true",
                    help="list the full safety lifecycle (stage | slug | when | output)")
    ap.add_argument("--route", metavar="STAGE|SLUG",
                    help="show the call note for one stage key or sub-skill slug")
    args = ap.parse_args()

    if args.route:
        key = ALIASES.get(args.route.strip().lower(), args.route.strip().lower())
        hit = None
        for (k, slug, when, out) in FLOW:
            if key == k or key == slug:
                hit = (k, slug, when, out)
                break
        if not hit:
            print("no such stage/slug: %s" % key)
            print("known: %s" % ", ".join(k for (k, _, _, _) in FLOW))
            return 2
        k, slug, when, out = hit
        print("stage=%s  sub-skill=%s" % (k, slug))
        print("  when-to-use : %s" % when)
        print("  expected-out: %s" % out)
        print("  call        : invoke the '%s' sub-skill directly (its own CLI/help)." % slug)
        return 0

    # default: list
    print("PromptShield (ai-safety-suite) — safety lifecycle (9 sub-skills, orchestrated by slug):")
    print("=" * 78)
    for (i, (k, slug, when, out)) in enumerate(FLOW, 1):
        print("%d. %s  ->  %s" % (i, k, slug))
        print("     when: %s" % when)
        print("     out : %s" % out)
    print("=" * 78)
    print("tip: python3 promptshield_flow.py --route <stage|slug>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
