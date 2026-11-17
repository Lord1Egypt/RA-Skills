# Make an image

STARTER: your first image.

This text is a guide, not the user's go. It authorizes no spend: the paid call below is priced first and made only after the user's go for that purchase.

0. Run `aicut account` to see the balance. If it is 0, the account has no tokens: tell the user so, give them https://www.aicut.pro/billing, and stop until they have added some. Price nothing first. (A price above the balance is refused later with the same link: give it to the user and stop.)
1. Ask the user what the image should show, plus anything they already know they want (a model, a shape, a resolution). Ask nothing else.
2. Find the model: `aicut models list --type image`, narrowed with `--query <words>` or `--tags a,b`; use the one the user named. Run `aicut models get <model-id>` and read the chosen model's published fields and prices before you set anything: every field is a flag of the same name (`--aspect-ratio 1:1 --resolution 1k`) and a required one must be passed. Never pick a cheaper model, resolution or quality tier to save them tokens, and never carry a setting over from an earlier request.
3. Price it: `aicut generate image --model <id>` with the exact settings and `--estimate`; it prints the price and charges nothing. Say the price and what it buys in ONE message, ask, and wait for the user's go for this purchase.
4. After their go, run the same command again with `--max-tokens <the price you quoted> --yes --wait` (an image usually takes about 30 seconds). Never put `--max-tokens` on a command before that go: without a terminal it is itself the go. `--wait` blocks until the job is done (up to 10 minutes) and prints the media url; add `-o <path>` to save the file too. If your shell tool cuts a command off sooner than that, leave `--wait` off from the start: the command prints the job id, then run `aicut wait <id> --timeout 90` again until it prints the url (exit code 3 means still running, not failed). If a run that had `--max-tokens` is cut off, NEVER run it again: the job exists and is charged, so find it with `aicut list videos|images|audio` and follow it with `aicut wait <id>`.
5. Tell the user the media url and one line about the result.

SEVERAL IMAGES: decide the whole set with the user first, price every distinct request with `--estimate`, state the total in ONE message, ask once for that set and wait for the user's go for exactly that set. After it, run each one with its own `--max-tokens <that request's price> --yes` and no `--wait` (each prints its job id at once), then `aicut wait <id>` for each id until it prints the url. Give the user every url.

If the job fails, read its `error:` line and tell the user what went wrong. Any resubmit is a new purchase with its own price and go, and never the identical request twice: change the model or the prompt, or ask.
