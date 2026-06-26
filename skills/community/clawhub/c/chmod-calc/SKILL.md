---
name: chmod-calc
description: Calculate chmod permissions — convert between numeric (octal) and symbolic notation, and generate the chmod command. Use when the user asks what chmod 755 means, how to set file permissions, or what symbolic notation rwxr-xr-x translates to.
---

# chmod Calculator

Convert file permission specifications between numeric (octal) and symbolic notation, and produce the corresponding `chmod` command.

## Input
- Either a numeric permission string (e.g. `755`, `644`, `4755`)
- Or a description of permissions per entity (owner/group/others with read/write/execute)
- Or a symbolic string (e.g. `rwxr-xr-x`)

## Output
- Numeric notation (3 or 4 digits)
- Symbolic notation (9 characters, e.g. `rwxr-xr-x`)
- Numeric chmod command: `chmod 755 filename`
- Symbolic chmod command: `chmod u+rwx,g+rx,o+rx filename`
- Plain-English description of what each entity can do

## Instructions

### Permission bit values
Each entity (owner/group/others) is a sum of:
- Read (r) = 4
- Write (w) = 2
- Execute (x) = 1

### Special permission bits (4th leading digit)
- Setuid = 4 (runs as owner)
- Setgid = 2 (runs as group)
- Sticky = 1 (only owner can delete in directory)

### Numeric → Symbolic conversion
Given a 3-digit octet `OGO`:
- For each digit, decompose: `r` if bit 2 set, `w` if bit 1 set, `x` if bit 0 set, else `-`.
- With leading special digit `S`: setuid sets `s/S` in owner execute position; setgid sets `s/S` in group execute position; sticky sets `t/T` in others execute position.

### Symbolic → Numeric conversion
Map each 3-char group to a digit using the bit values above.

### Symbolic chmod command format
Build clauses for each entity with permissions set:
- `u` = owner, `g` = group, `o` = others
- Emit `{entity}+{perms}` for each entity that has any permissions
- Special bits: `u+s` (setuid), `g+s` (setgid), `+t` (sticky)

### Common permission reference
| Numeric | Symbolic    | Description                    |
|---------|-------------|--------------------------------|
| 644     | rw-r--r--   | Standard file (owner rw, rest r) |
| 755     | rwxr-xr-x   | Standard directory/executable  |
| 600     | rw-------   | Private file (owner only)      |
| 700     | rwx------   | Private directory/executable   |
| 777     | rwxrwxrwx   | Full access (avoid in production) |
| 4755    | rwsr-xr-x   | Setuid executable              |
| 2755    | rwxr-sr-x   | Setgid executable              |
| 1755    | rwxr-xr-t   | Sticky directory               |

## Options
- Input can be numeric, symbolic, or a plain-English description of desired permissions.

## Examples

**Input:** `755`
**Output:**
```
Numeric:          755
Symbolic:         rwxr-xr-x
Command (numeric):   chmod 755 filename
Command (symbolic):  chmod u+rwx,g+rx,o+rx filename

Owner: read, write, execute
Group: read, execute
Others: read, execute
```

**Input:** `644`
**Output:**
```
Numeric:          644
Symbolic:         rw-r--r--
Command (numeric):   chmod 644 filename
Command (symbolic):  chmod u+rw,g+r,o+r filename

Owner: read, write
Group: read
Others: read
```

**Input:** `rwxr-xr-x`
**Output:**
```
Numeric:          755
Symbolic:         rwxr-xr-x
Command (numeric):   chmod 755 filename
Command (symbolic):  chmod u+rwx,g+rx,o+rx filename
```

**Input:** "owner can read and write, group can read, others nothing"
**Output:**
```
Numeric:          640
Symbolic:         rw-r-----
Command (numeric):   chmod 640 filename
Command (symbolic):  chmod u+rw,g+r filename
```

## Error Handling
- If numeric input has more than 4 digits or contains non-octal characters, say so.
- If a digit in the octet exceeds 7, explain that each permission digit must be 0–7.
- If symbolic input is not exactly 9 or 10 characters in valid format, ask for clarification.
- Warn the user if they request `777` that this allows full access to everyone and is a security risk.
