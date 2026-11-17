# Defect-class specific requirements

> When adjudicating a claim, **first fix the class, then apply that class's default assumptions**.
>
> Because across classes, "what counts as suspicious" and "what counts as a false positive" are **opposite**. Judging every class
> with the same intuition guarantees systematic errors in some classes.

---

## 0. Default assumptions flip by class

This is the most important rule in this file, and the most counter-intuitive:

| Class | Direction of the default assumption |
|---|---|
| **memory corruption** | default to **false positive**. In memory-safe languages it is almost always a false positive, unless there is a compiler defect or a type-system hole |
| **logic defect** | default to **not a false positive**. "Logic defects pass every boundary check" — **do not let clean static analysis convince you it is a false positive** |
| remaining classes | see below, class by class |

Flip these two rows and you flood memory corruption with false positives while missing real logic-defect vulnerabilities.

---

## 1. Memory corruption

**Do the language check first**: memory corruption in safe Rust, in Go without `unsafe.Pointer`/cgo, and in every managed language
(Java / C# / Python / JS) is **almost always a false positive**. Passing this gate first saves most of the work.

After the language check, examine:

- what exactly is corrupted (stack / heap / global / object)
- whether the size and offset of the corruption **are attacker-controlled**
- whether it is a useful primitive (arbitrary read, arbitrary write, vtable overwrite) or merely a crash
- whether allocator hardening is in place
- the object lifetime of a use-after-free (UAF): can it actually be referenced again after being freed
- type confusion: give **proof of the type mismatch**, not "it looks like one"

---

## 2. Logic defect

**The default assumption is reversed: do not let "static analysis is clean" convince you this is a false positive.**

- judge against the **spec / RFC / design documents**, not by reading code alone
- draw **every state transition** — can an unexpected state be reached?
- find **implicit assumptions that are never enforced**
- for authentication-class defects, verify **all** authentication and authorization paths, not just the main path

---

## 3. Race condition

- is the real race window **nanoseconds or seconds**? The two are entirely different problems
- can the attacker **widen the window** (slow filesystem, large allocations, CPU contention)
- verify the threading model: single-threaded / event loop / multi-threaded — the conclusions are entirely different
- check every synchronization primitive, not just whether a lock exists
- for filesystem classes, look at **symlink races** (the classic TOCTOU form)

---

## 4. Integer issues

- the **exact type and value range** at every point, not "roughly an integer"
- signed overflow (undefined behavior in C/C++) vs unsigned wraparound (**defined**) — they must not be conflated
- trace every cast / conversion / promotion
- **is the result actually used for something dangerous**: allocation size, array index, loop bound. An overflow used for log printing is not a vulnerability
- enable checks such as `-Wconversion` and `-Wsign-compare`, and let the compiler find them for you

---

## 5. Crypto weaknesses

- check parameters against NIST / IETF standards and known attacks
- verify the randomness source: is it cryptographically secure
- **nonce reuse must be shown to actually occur twice in practice**, not "theoretically possible"
- for timing side channels, look at two things: whether the attacker can reach it, and whether network jitter makes a remote attack impractical
- compare against the reference implementation's test vectors

---

## 6. Injection

- trace the attacker's input along its **full path** from entry to sink, and whether it is sanitized or escaped along the way
- is the framework's automatic escaping enabled, **and not bypassed**
- XSS depends on context: HTML body / attribute / JS / URL — **each needs different escaping**; one escaping cannot cover all
- path traversal: was the path normalized **before** the access check
- run all intermediate processing with **real payloads**; do not verify in hand-written examples

---

## 7. Information disclosure

- **what exactly is leaked**: a stack leak (can yield an ASLR base or canary) is serious; a static string is worthless
- is the leaked data **actually useful** for further exploitation
- for uninitialized memory, **prove that the read point is really uninitialized**
- for timing side channels, look at measurement precision and noise level
- can the error information **actually reach the attacker** — being written to a log does not count

---

## 8. Denial of service

- is the resource consumption ratio or amplification factor **meaningful**
- are resources recoverable or permanently exhausted — the two differ greatly in severity
- **a complexity claim must show that a real worst-case input triggers it**, not just assert O(n²):
  name the concrete input and give the measured time
- is the crash triggered **reliably**
- does the service restart automatically: a 100-millisecond restart and a human having to intervene are two entirely different problems

---

## 9. Deserialization

- does the attacker **actually control** the data that reaches the deserialization point
- is there a **usable gadget chain** in the classpath / import graph —
  **without a gadget chain, unsafe deserialization is a design smell, not an exploitable defect**
- the library and version, and the chains known for that version
- are type restrictions / allowlist filters in place
- language-specific forms: Java `ObjectInputStream`, Python `pickle`, PHP `unserialize`, .NET `BinaryFormatter`

---

## Usage

1. Classify the assertion at Stage C's **step zero**
2. The class sets the direction of the default assumption (see §0)
3. When running data-flow and exploitability analysis, **layer on** that class's specific checks (table above)
4. When evaluating the gates, that class's particular "what counts as prevented" is judged by the definitions above

> Classify wrong and everything after is wrong. **When unsure, say you are unsure — do not pick a plausible-looking one to fill in.**
