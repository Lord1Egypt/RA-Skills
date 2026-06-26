# Category Playbooks

## Contents

- Web
- Pwn
- Reverse
- Crypto
- Forensics and Stego
- Misc and OSINT

## Web

Start by mapping the attack surface before trying payloads.

- Inspect routes, parameters, headers, cookies, auth flows, file uploads, and JavaScript bundles.
- Check for common classes of bugs:
  - injection: SQLi, SSTI, command injection, NoSQL injection
  - access control: IDOR, forced browsing, missing authorization checks
  - request handling: SSRF, open redirect, request smuggling clues, cache poisoning
  - state and tokens: JWT confusion, weak session handling, CSRF edge cases
  - file handling: traversal, LFI/RFI, upload bypass, archive extraction issues
  - frontend logic: source maps, hidden API routes, leaked secrets, prototype pollution
- Prefer short confirmation probes with `curl`, browser devtools, or Burp before chaining a full exploit.
- Read client-side code when the server behavior looks inconsistent or hidden functionality is likely.

## Pwn

Characterize the binary and mitigations first.

- Identify format and architecture with `file`.
- Check hardening with `checksec` or an equivalent.
- Enumerate symbols, imports, strings, and interesting functions.
- Determine the primitive:
  - buffer overflow
  - format string
  - arbitrary read/write
  - use-after-free / double free / tcache abuse
  - integer overflow / sign issue
  - shellcode injection
- Separate local from remote assumptions:
  - exact libc
  - ASLR/PIE behavior
  - I/O timing and menu structure
- Build the shortest chain that can work:
  - leak
  - calculate base
  - gain control
  - pivot to code execution or flag read
- When stuck, inspect constraints:
  - bad bytes
  - seccomp
  - stack alignment
  - one-shot input limits

## Reverse

Focus on control flow, data flow, and validation logic.

- Identify the entry path and the code that gates success or prints the flag.
- Collect strings, imports, constants, tables, and cryptographic-looking routines.
- Determine whether the target is:
  - native binary
  - packed sample
  - script or bytecode
  - VM or custom interpreter
- Prefer static analysis first, then confirm with runtime tracing when needed.
- Look for:
  - XOR/add/sub rolling transforms
  - lookup tables
  - anti-debug or anti-VM checks
  - encoded resources
  - staged decryption or self-modifying logic

## Crypto

Identify the primitive before attempting recovery.

- Distinguish encoding from encryption:
  - base encodings
  - hex
  - URL encoding
  - compression
- Ask what evidence points to the scheme:
  - block size
  - alphabet
  - modulus/exponent pairs
  - repeated blocks
  - nonce/IV reuse
  - known plaintext structure
- Common directions:
  - XOR or repeating-key XOR
  - Caesar/Vigenere/substitution
  - textbook RSA mistakes
  - broadcast/small exponent RSA
  - weak Diffie-Hellman parameters
  - ECB/CBC misuse
  - padding oracle style behavior
  - LCG or predictable RNG
- Write down assumptions explicitly. Crypto work derails quickly when the primitive guess is wrong.

## Forensics and Stego

Start with file truth, metadata, and container structure.

- Confirm the actual file type instead of trusting the extension.
- Inspect timestamps, EXIF, embedded documents, alternate streams, appended data, and nested archives.
- For PCAPs:
  - identify unusual protocols or conversations
  - follow streams
  - extract files and credentials
  - reconstruct transfer artifacts
- For images/audio:
  - inspect metadata
  - search for appended archives or unusual chunks
  - compare channels, bit planes, spectrograms, and dimensions
- For memory or disk artifacts:
  - note the format early and choose tools that match the artifact.

## Misc and OSINT

Treat "misc" as a signal that the real category is hidden.

- Re-check whether the prompt is actually encoding, logic, web, or forensics in disguise.
- Look for:
  - puzzle constraints
  - custom parsers
  - QR/barcode content
  - geolocation clues
  - social profile traces
  - DNS or certificate breadcrumbs
- Keep a list of discarded interpretations so the search does not loop.
