Summarize selected X posts as first-party signals from builders.

Language:

- if `config.language` is `zh-CN`, write both the title line and the summary in Chinese
- if `config.language` is `zh-CN`, translate the post into concise natural Chinese instead of leaving the raw English post text in place
- keep handles, product names, company names, and very short quotes in the original language only when they help clarity
- if `config.language` is `bilingual`, keep the result compact and ensure Chinese rendering is present
- if `config.language` is `en`, write in English

Focus on:

- what the builder directly said or shipped
- why the post matters for product builders, engineers, or AI operators
- any concrete product, model, workflow, or market signal
- the author's role or source context when it helps interpretation
- keep one numbered item per selected post

Avoid:

- treating a casual post as a major announcement
- adding context not supported by the post text
- rewriting one short post into a long essay
- folding multiple posts into "more X updates" or any grouped placeholder
