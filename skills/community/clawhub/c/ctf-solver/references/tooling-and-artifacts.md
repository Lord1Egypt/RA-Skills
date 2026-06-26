# Tooling and Artifacts

## Baseline Triage

Use the lowest-cost checks that reveal structure.

### Generic files

```bash
file <target>
strings -a -n 6 <target>
xxd -l 256 <target>
```

### Archives and containers

```bash
7z l <target>
binwalk <target>
```

### Binaries

```bash
file <target>
checksec --file=<target>
objdump -d <target> | less
```

### Network artifacts

```bash
tshark -r <pcap> -q
strings -a <pcap> | less
```

### Web targets

```bash
curl -i <url>
curl -s <url>/robots.txt
```

## Working Style

- Keep one notes file with:
  - target summary
  - commands run
  - promising observations
  - dead ends
  - next hypotheses
- Keep extracted or decoded artifacts in labeled files instead of overwriting the terminal scrollback.
- When a blob changes form, label each stage: `sample.b64`, `sample.bin`, `sample.decoded.txt`.

## Minimal Tool Preferences

Prefer tools that are commonly present or easy to reason about.

- Binary work: `file`, `strings`, `objdump`, `gdb`, `pwndbg`, `readelf`, `checksec`
- Reverse: Ghidra, IDA Free, `rabin2`, `strings`
- Web: browser devtools, `curl`, Burp Suite, `ffuf` when enumeration is justified
- Forensics: `exiftool`, `binwalk`, `7z`, `tshark`, Wireshark, SQLite tools
- General solving: Python for tiny decode/exploit scripts instead of repetitive manual transformations

## Artifact Discipline

- Preserve the original challenge file.
- Use copies for patching, unpacking, or repeated mutation.
- Record hashes or at least filenames when multiple similar artifacts exist.
- Distinguish clearly between:
  - raw input
  - extracted content
  - transformed content
  - final exploit or solver

## Writeup Discipline

When the user asks for a writeup or wants the solve process preserved, keep this order:

1. Restate the challenge objective and provided artifacts.
2. Summarize the observations that narrowed the category.
3. Show the key failed branches only if they explain an important pivot.
4. Present the successful exploit or decode path step by step.
5. State how the flag was validated.

Avoid pretending certainty. If the artifact is incomplete or the flag is still missing, say exactly what is known, what was attempted, and what evidence would unblock the next step.
