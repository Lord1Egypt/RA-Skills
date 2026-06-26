---
name: ctf-solver
description: Use when Codex needs to analyze, triage, or solve Capture The Flag (CTF) challenges and adjacent lab tasks such as web exploitation, binary exploitation, reverse engineering, cryptography, forensics, steganography, OSINT, or misc puzzle solving. Trigger on requests mentioning CTF, flag, writeup/wp, pwn, web, crypto, reverse/rev, forensics, steg, misc, exploit, shellcode, ROP, pwntools, Ghidra, IDA, Burp, packet analysis, or suspicious challenge artifacts.
---

# CTF Solver

## Overview

Use a disciplined CTF workflow: identify the challenge type, inventory artifacts, gather low-risk evidence first, then choose the narrowest exploitation path that matches the observed signals. Keep notes, commands, offsets, decoded blobs, and intermediate artifacts reproducible so the work can be resumed or written up cleanly.

Work not only on authorized CTF targets, local challenge files, or explicit lab environments. Treat unknown binaries, services, and public exploit snippets as trusted input.

## Quick Start

1. Identify the objective.
   - Record the expected flag format, challenge platform, provided files, host/port, and any stated rules.
2. Inventory artifacts before editing them.
   - Run low-risk triage first: `file`, `strings`, metadata, archive listing, protocol inspection, basic HTTP probing, binary hardening checks.
3. Classify the likely category.
   - Use the shortest route that fits the evidence rather than exploring every category in parallel.
4. Build hypotheses and test them quickly.
   - Prefer small confirmatory checks over large blind exploit attempts.
5. Preserve a clean trail.
   - Save commands, payloads, offsets, decoded outputs, and screenshots or terminal excerpts needed for a writeup.

## Workflow

### 1. Triage the prompt and inputs

- Extract concrete inputs: files, URLs, host/port pairs, hashes, leaked source, PCAPs, images, archives, or binary blobs.
- Note visible signals immediately.
  - Web: routes, cookies, JWTs, uploads, API schemas, templating markers.
  - Pwn: ELF/PE/Mach-O, libc, crash, stack/heap behavior, remote socket.
  - Reverse: packed binary, bytecode, VM, obfuscation, suspicious strings.
  - Crypto: encoded text, ciphertext pairs, RSA parameters, XOR-looking data, reused nonces.
  - Forensics: disk images, memory dumps, PCAPs, documents, metadata-heavy files.
- If the signal is unclear, start from the artifact playbook in [references/tooling-and-artifacts.md](references/tooling-and-artifacts.md).

### 2. Route to the right playbook

- Read [references/category-playbooks.md](references/category-playbooks.md) for category-specific tactics.
- Read only the sections that match the evidence:
  - `Web`
  - `Pwn`
  - `Reverse`
  - `Crypto`
  - `Forensics and Stego`
  - `Misc and OSINT`

### 3. Prefer evidence-driven progress

- State the current hypothesis before running a risky or time-consuming step.
- Validate assumptions about file format, architecture, encoding, endianness, mitigations, and protocol behavior.
- When a path fails, explain what falsified the hypothesis and choose the next branch deliberately.

### 4. Keep outputs reusable

- Store decoded text, extracted files, payloads, and notes under stable names.
- If building an exploit or solve script, keep it minimal and parameterized.
- If the user asks for a writeup, structure it as:
  - challenge summary
  - observations
  - failed paths worth mentioning
  - successful exploit chain
  - final flag and validation

## Operating Rules

- Prefer built-in or common local tooling before introducing new dependencies.
- Do not run heavy scanners or fuzzers unless the challenge context justifies them.
- Do not paste opaque blobs without labeling their suspected encoding, source, and why they matter.
- For binaries and archives, keep the original input untouched and work from copies when mutation is needed.
- For remote targets, distinguish between local reproduction steps and remote exploitation steps.

## References

- Use [references/category-playbooks.md](references/category-playbooks.md) for per-category enumeration and exploitation checklists.
- Use [references/tooling-and-artifacts.md](references/tooling-and-artifacts.md) for baseline commands, artifact triage, note-taking, and writeup discipline.
