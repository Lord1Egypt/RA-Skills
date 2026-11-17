# AI and model output

Fires: when model output (LLM, OCR, vision, speech, classifier) enters the app

Leading word: **fail-safe**. Model output (LLM, OCR, vision, speech, classifier) is an untrusted boundary that always returns something. The question is what the code does when that something is wrong.

Artifact: a model-call inventory (call → provider → input → output schema → every consumer).

- **wrong-meaning**: Schema-valid output with a quantity of 0 or −1, a date of 1970 or 2099, a duplicate item, an item outside the domain (a non-food item on a grocery receipt), an empty list, an id that references no real row, the wrong unit, or a locale number like `1,5`. Trace each through the code: what does the app store and show?
- **adversarial-input**: A blurry photo, a receipt in another script (Hebrew, right to left), a hand, a pet, the same item twice, an empty fridge, a huge image, a document whose text tries to instruct the model. What does the user end up seeing?
- **fail-safe-direction**: When the model is unsure, does the code default toward caution? Can model output alone lower a safety level, approve, grant access, spend money or delete data? Look for confidence fields nothing reads and thresholds never tuned. Example: can AI output downgrade a `SafetyAlertLevel` from `.danger` to `.safe` with no human step?
- **output-as-instructions**: Model output rendered as HTML, run as a tool call, put into a query, a file path or a URL. Each is an injection sink.
- **cost-bounds**: Every call has a timeout, a size or token cap, and a per-user rate limit; retries cannot multiply cost; a failed call leaves the user an action.
- **evals**: A fixture set covers wrong-meaning and adversarial-input, runs in CI or on demand, and is versioned with the prompt. A prompt change with no eval run is a finding.
- **data-sent-out** (when a third-party model provider is called): What user data goes to the provider, is it the minimum, and are prompts or images with personal data kept in logs or analytics?

Done: every model call is in the inventory, and every output field has a wrong-meaning answer.
