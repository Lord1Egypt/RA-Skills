Summarize selected podcast episodes from transcript text.

Language:

- if `config.language` is `zh-CN`, write both the title line and the summary in Chinese
- if `config.language` is `zh-CN`, translate the episode title or lead into concise natural Chinese instead of leaving the output as raw English
- keep podcast names, guest names, company names, product names, and very short quotes in the original language only when they help clarity
- if `config.language` is `bilingual`, keep the result compact and ensure Chinese rendering is present
- if `config.language` is `en`, write in English

Focus on:

- the guest, host, or source when available
- the central argument or product insight
- concrete claims, examples, or operating lessons
- what changed or what a builder should pay attention to
- keep one numbered item per selected episode

Avoid:

- summarizing sponsorship or intro filler
- over-indexing on one isolated quote from a long transcript
- inventing timestamps, speaker names, or claims not present in the transcript
- merging multiple episodes into one grouped paragraph or "more updates" placeholder
