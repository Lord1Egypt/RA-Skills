# Bias lens

An agent skill for spotting passages whose reasoning resembles a cognitive bias,
cognitive distortion or logical fallacy. It reads a public, regularly updated
[bias catalog](https://tarot.catarchy.space/biases/), quotes the reasoning step,
and suggests a concrete way to check it.

Most bias checkers look for words and topics. Bias lens looks for steps in an
argument: it maps what the text claims, infers and compares, and only then asks
which thinking shortcut would produce that exact step.

Findings concern the reasoning in a passage, not the author's character or mental
health. The reader can reject a match. No findings is a valid result.

## Install and use

Clone this repository into the skills directory your agent reads, naming the
directory `bias-lens`:

```bash
git clone https://github.com/troioi-vn/bias-lens-skill.git bias-lens
```

The entry point is [SKILL.md](SKILL.md). Ask your agent:

```text
Use bias-lens to check this draft for possible cognitive biases.
Quote each passage you flag and give me a concrete check for it.
```

The skill maps reasoning before consulting the catalog, checks context and
ownership, compares nearby patterns, and reports at most five current findings
per speaker. Corrected past reasoning stays separate. Religious identity,
distress, disagreement and factual errors do not establish a bias.

## Catalog client

Python 3.9 or newer is required. There are no third-party Python dependencies,
accounts or API tokens to configure.

```bash
python3 scripts/bias_lens.py index
python3 scripts/bias_lens.py detail confirmation-bias
python3 scripts/bias_lens.py index --offline
```

`index` fetches or ETag-revalidates a snapshot from the public catalog API.
`detail` reads that snapshot without network access, including descriptions,
public examples, research links and related IDs. Both commands print the catalog
version to stderr. Keep one version throughout a reading.

Only catalog requests reach the service. The client never sends the text being
examined. Public catalog data is cached under `~/.cache/bias-lens`, or under
`$XDG_CACHE_HOME/bias-lens` when configured. Give concurrent readings separate
`XDG_CACHE_HOME` directories so they cannot replace one another's snapshots.
Network failures do not silently fall back to stale data; choose `index --offline`
explicitly when needed.

Set `BIAS_LENS_CATALOG_URL` to use another server implementing the same version 1
schema. The default is
`https://tarot.catarchy.space/api/public/v1/catalog/`.

The catalog includes editorial drafts. Catalog membership is not evidence that a
description has passed human research review, and matching a passage does not
diagnose its author. Preserve the descriptions' qualifications.

## Free catalog API

The catalog behind this skill is open to anyone. No account, key or payment is
needed:

```bash
curl https://tarot.catarchy.space/api/public/v1/catalog/
```

One GET returns the whole English catalog as JSON: about 270 cognitive biases,
cognitive distortions and logical fallacies. Each entry has a stable `id`,
`name`, `family` (`bias`, `distortion` or `fallacy`), page `url`, description
`body`, public `examples`, research `sources` and `related` IDs. The response
also carries `schemaVersion` and a content hash in `catalogVersion`; record the
hash when you need to say which catalog an analysis used.

The API only serves the catalog. It accepts no text, does no matching and
stores nothing you send. Responses carry an ETag and may be cached for five
minutes, so fetch once per session and revalidate with `If-None-Match`.
Browse the same entries at [tarot.catarchy.space/biases](https://tarot.catarchy.space/biases/).
The full description is at [tarot.catarchy.space/biases/api](https://tarot.catarchy.space/biases/api/).

The catalog text is licensed
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You can share
and adapt it if you credit "Catastrophic Thinking bias catalog" with a link and
release adaptations under the same license.

## Development

Run the tests without network access to the catalog service:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The tests use a temporary local HTTP server and synthetic catalog data.

## License

The skill instructions, client and tests in this repository use the
[MIT license](LICENSE). Catalog text is fetched separately, is not included in
this repository, and is licensed CC BY-SA 4.0 by its publisher.
