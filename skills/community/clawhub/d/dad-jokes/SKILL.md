---
name: dad-jokes
description: Tell dad jokes on demand by fetching a random joke from the shuttie/dadjokes HuggingFace dataset. Trigger whenever the user asks for a dad joke, wants to hear a joke, asks you to tell them something funny, or uses phrases like "dad joke", "tell me a joke", "give me a joke", "hit me with a joke", "I need a laugh", or any similar request for humor. Even if the request is casual or phrased oddly, if it's asking for a joke, use this skill.
---

<!-- This is a minimal test skill for reproducing ClawHub issues. v1.1.2 -->

When asked for a dad joke, run this Python one-liner in a bash tool call to fetch a single random joke from HuggingFace with minimal data transfer:

```bash
python3 -c "
import random, json
from urllib.request import urlopen
offset = random.randint(0, 51999)
url = f'https://datasets-server.huggingface.co/rows?dataset=shuttie%2Fdadjokes&config=default&split=train&offset={offset}&length=1'
row = json.loads(urlopen(url).read())['rows'][0]['row']
print(row['question'])
print('---')
print(row['response'])
"
```

Then present the joke naturally — the `question` is the setup and `response` is the punchline. Format them as a proper joke (setup on one line, punchline revealed after a beat). Feel free to add a groan emoji or light commentary, but keep it brief.

If the fetch fails (network error, etc.), apologize and tell a joke from memory instead.

<!--
Attribution:
Dad jokes dataset by Roman Grebennikov (shuttie): https://huggingface.co/datasets/shuttie/dadjokes
Based on original dataset by Oktay Ozturk: https://www.kaggle.com/datasets/oktayozturk010/reddit-dad-jokes
License: Apache 2.0
-->
