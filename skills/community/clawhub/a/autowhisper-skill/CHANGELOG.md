# Changelog

## 0.2.3
- Added direct API guidance for posts, wallet, platforms, explicit delivery
  actions, and field-level content edits so agents can avoid an LLM turn for
  deterministic operations.

## 0.2.2
- Added the fast CMO Feed endpoint so agents can inspect pending review items
  without sending a CMO chat message.

## 0.2.1
- Added fast read-only API guidance for product counts, product lists, and CMO
  status so agents do not spend a CMO chat turn on simple facts.

## 0.2.0
- Positioning: sell **relief**, not output. The skill led with "batches of ad
  creatives" (a capability); nobody with a product wakes up wanting ad
  creatives — they wake up dreading the edit, the translation, and the daily
  post. Now matches the site's single source of truth: *you never have to make
  content again*.
- Named the two things that make that promise credible, neither of which the
  skill said before: the content **doesn't look like an ad**, and the CMO
  **has seen what your rivals are posting**.
- Dropped the hardcoded "30+ platforms" — the count drifts and contradicted
  the site ("every channel you've connected" is true and stays true).
- Declared `license: MIT` in the frontmatter (catalogs read it from there).

## 0.1.0
- Initial release: drive the AutoWhisper CMO from an agent — connect a
  product, generate content, approve, connect platforms, and publish via
  `/api/cmo/*` (message → poll → confirm).
