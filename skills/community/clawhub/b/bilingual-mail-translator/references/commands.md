# Commands

Adapt these examples to your own project layout.

## Prompt regression test

```bash
python3 -m unittest tests/test_mail_body_translate.py
```

## Sample acceptance run

```bash
python3 scripts/mail_translate.py < tmp/sample-mail.eml
```

## Main translation entrypoint

```bash
python3 scripts/mail_translate.py
```

## Notes

- Runtime translation can use a lightweight worker agent or another LLM runtime
- Do not move formatting logic into postprocess
- When behavior changes are accepted, update both prompt contract docs and tests
