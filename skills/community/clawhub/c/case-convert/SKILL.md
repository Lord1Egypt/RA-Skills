---
name: case-convert
description: Convert text between different case styles. Use when the user asks to convert text to camelCase, snake_case, kebab-case, PascalCase, UPPERCASE, lowercase, Title Case, CONSTANT_CASE, dot.case, path/case, Sentence case, inverse case, alternate case, or any other case format.
---

# Case Converter

Convert text between 15 different case styles simultaneously.

## Input
- The text to convert
- Optionally, the target case style (if not specified, show all 15)

## Output
- The converted text in the requested case style(s)
- If no target specified, show all 15 transformations

## Instructions

Apply each transformation exactly as follows:

1. **lowercase** — `s.toLowerCase()`
   Example: `hello world example`

2. **UPPERCASE** — `s.toUpperCase()`
   Example: `HELLO WORLD EXAMPLE`

3. **Title Case** — Capitalize each word EXCEPT articles/prepositions when not first:
   Small words (keep lowercase unless first): a, an, and, as, at, but, by, for, in, nor, of, on, or, so, the, to, up, yet, via, with
   Always capitalize: first word of the string, first word after `.`, `!`, `?`
   Example: `Hello World Example` (but: `The Art of War`)

4. **Sentence case** — Lowercase everything; capitalize first letter of each sentence (after `.`, `!`, `?` followed by whitespace, and the very first character)
   Example: `Hello world example. Another sentence.`

5. **camelCase** — Remove non-word characters (replace with space), trim, lowercase, then uppercase the first letter of every subsequent word, remove all spaces
   Example: `helloWorldExample`

6. **PascalCase** — Same as camelCase but also capitalize the very first letter
   Example: `HelloWorldExample`

7. **snake_case** — Lowercase, remove non-word non-space characters, replace spaces with `_`, collapse consecutive `_`
   Example: `hello_world_example`

8. **kebab-case** — Lowercase, remove non-word non-space characters, replace spaces with `-`, collapse consecutive `-`
   Example: `hello-world-example`

9. **CONSTANT_CASE** — Uppercase, remove non-word non-space characters, replace spaces with `_`, collapse consecutive `_`
   Example: `HELLO_WORLD_EXAMPLE`

10. **dot.case** — Lowercase, remove non-word non-space characters, replace spaces with `.`, collapse consecutive `.`
    Example: `hello.world.example`

11. **path/case** — Lowercase, remove non-word non-space characters, replace spaces with `/`, collapse consecutive `/`
    Example: `hello/world/example`

12. **iNVERSE cASE** — For each character: if uppercase → lowercase, if lowercase → uppercase, else unchanged
    Example: `hELLO wORLD eXAMPLE`

13. **aLtErNaTe CaSe** — For each character at index i: if i is even → lowercase, if i is odd → uppercase
    Example: `hElLo wOrLd eXaMpLe`

14. **esreveR** — Reverse the entire string character by character
    Example: `elpmaxE dlroW olleH`

15. **SpOnGeBoB cAsE** — Iterate through alphabetic characters only, alternating upper/lower (non-alphabetic characters pass through unchanged, but do NOT advance the alternation counter)
    Example: `hElLo WoRlD eXaMpLe`

## Options
- `target` — specific case name (if omitted, output all 15)
- `batchMode` — if true, apply the transformation to each line independently

## Examples

**Request:** "Convert 'hello world' to camelCase"

**Output:** `helloWorld`

---

**Request:** "Convert 'USER_LOGIN_COUNT' to all cases"

**Output:**
- lowercase: `user_login_count`
- UPPERCASE: `USER_LOGIN_COUNT`
- Title Case: `User_login_count`
- Sentence case: `User_login_count`
- camelCase: `userLoginCount`
- PascalCase: `UserLoginCount`
- snake_case: `user_login_count`
- kebab-case: `user-login-count`
- CONSTANT_CASE: `USER_LOGIN_COUNT`
- dot.case: `user.login.count`
- path/case: `user/login/count`
- iNVERSE cASE: `user_login_count`
- aLtErNaTe CaSe: `uSeR_lOgIn_cOuNt`
- esreveR: `TNUOC_NIGOL_RESU`
- SpOnGeBoB cAsE: `uSeR_lOgIn_cOuNt`

---

**Request:** "snake_case this: 'My Component Name'"

**Output:** `my_component_name`

## Error Handling
- If input is empty, return an empty string for all cases
- If target case style is not recognized, list all 15 available styles and ask which one the user wants
- For very long inputs (>10,000 characters), process normally but note the length
