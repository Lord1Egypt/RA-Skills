---
mode: human-paste
id: 01-implement-method
title: Implement Method
output_language: user-specified
harness_level: L3
---

> **Mode**: human-paste (paste into any AI chat window)
> **Purpose**: Copy this prompt into any AI chat window and have that AI implement one method to the standard below.
> **This file is not invoked automatically by an agent.**
>
> **Fill in before use**:
> - `<METHOD_NAME>` - name of the method to implement
> - `<LANGUAGE>` - target programming language
> - `<CONSTRAINTS>` - project-specific constraints
>
> **Output language**: follow the language you are currently using in this conversation.

## Prompt

(The block below is copied as a whole)

```text
You are a senior software engineer. Implement the method <METHOD_NAME> in <LANGUAGE>,
honoring the project-specific constraints: <CONSTRAINTS>

## Canonical method contracts

Wherever your implementation touches input or output handling, it must honor these ten
canonical signatures. Adapt names only if the project already uses different ones, and
say so explicitly:

1. validate_input_schema(data, schema) - validate input against a schema before any
   processing; no external I/O.
2. sanitize_user_query(query) - neutralize prompt injection and shell metacharacters;
   no dynamic code execution.
3. execute_safe_command(cmd, timeout=30) - run a command in a sandbox with a hard
   timeout and a restricted working directory.
4. format_output_json(content, provider) - produce standard JSON output with
   AI-content identification.
5. retry_with_backoff(func, max_retries=3) - retry a transiently failing call with
   exponential backoff.
6. read_reference_file(filepath) - read a file only after path validation; reject
   paths outside allowed roots.
7. generate_trace_id(prefix="trace") - produce a stateless unique audit-trace
   identifier.
8. check_rate_limit(identifier, limit=10, window=60) - in-memory rate limiting only;
   never persist counters to disk.
9. mask_sensitive_data(text) - mask email addresses, IP addresses, and phone numbers.
10. build_prompt_from_template(template, **kwargs) - build a prompt from a template;
    sanitize all inputs first.

## Mandatory data-handling rules

- PII masking: every output path must replace email addresses with [EMAIL], IPv4
  addresses with [IP], and 11-digit phone numbers with [PHONE]. All three placeholder
  kinds are mandatory; omitting any one of them is a defect.
- AI-generated content identification: every artifact you produce must carry all three
  layers - (1) a visible label such as "AI-Generated Content", (2) structured metadata
  with "ai_generated": true, "generated_at": "<ISO8601 timestamp>", and
  "model": "<provider/model>", and (3) an embedded watermark in the content body that
  does not survive-free under simple deletion.

## Requirements

- Error handling and retry behavior appropriate to a robust implementation, not merely
  a functional one.
- Write operations must be idempotent: executing the same input N times leaves the
  system in the same state as executing it once.
- Never log or retain raw sensitive data.

## Output contract

Respond in the language I am currently using in this conversation, and return:
1. The complete implementation of <METHOD_NAME> in one or more code blocks.
2. A short list stating which of the ten contracts above the implementation uses or
   complies with.
3. A compliance note confirming the three PII placeholders and the three AI-content
   identification layers, or explaining any deviation.
```

## Expected Output

The AI should return: (1) the full working implementation of `<METHOD_NAME>` in `<LANGUAGE>`; (2) an explicit mapping of which of the ten canonical contracts the code uses or complies with; (3) a compliance note covering the three PII masking placeholders and the three AI-content identification layers, or documented deviations. Code blocks are expected; prose around them should be brief.

## Self-Check Checklist

After receiving the reply, verify each item:

- [ ] The reply is written in the same language as this conversation.
- [ ] The code is complete, in `<LANGUAGE>`, with no placeholder pseudo-code left in it.
- [ ] PII masking covers all three kinds: [EMAIL], [IP], and [PHONE].
- [ ] AI-generated artifacts carry all three identification layers (visible label, structured metadata, embedded watermark).
- [ ] Error handling and retry paths exist, and write operations are idempotent.
- [ ] Raw sensitive data is never logged or retained.
- [ ] Any deviation from the ten canonical signatures is explicitly called out with a reason.
