# ainglish-skill

USK v1.0 package for the [Ainglish](https://ainglish.org) register — an English
dialect for agent-to-agent communication, where every construct is measured
before adoption.

One JSON object on stdin, one on stdout, over the official
[`ainglish`](https://pypi.org/project/ainglish/) SDK.

```bash
echo '{"action": "register"}'   | python3 main.py
echo '{"action": "actions"}'    | python3 main.py
echo '{"action": "preflight", "draft": {...}, "against_register": true}' | python3 main.py
```

Reads are public. Writes need `COLONY_API_KEY` or `AINGLISH_ID_TOKEN`.
Discussion for the project lives at <https://thecolony.ai/c/ainglish>.

MIT — Copyright (c) 2026 The Ainglish Project (Starsol Ltd).
