# Biomedical Reference Verifier

Verify and normalize biomedical and life-science reference lists, with a focus on AI-caused citation errors.

The skill checks DOI, PMID, title, authors, journal, year, and other bibliographic metadata through Crossref, PubMed, and OpenAlex. It can also normalize references to AMA, APA, Vancouver, or GB/T 7714 style without overwriting the source document.

## Highlights

- Fast, Balanced, and Strict verification modes
- DOI-first batch verification and early DOI recovery
- Crossref, PubMed, and OpenAlex evidence
- Bounded retries and PubMed batch-failure isolation
- Detection of identifier hijacking and shifted identifiers
- Reusable audit indexes with lossless audit/index conversion
- Tolerant handling of user-edited prior artifacts
- Runtime metrics and request-event logging
- No hidden persistent cache
- Severe references are reported, never automatically deleted

## Requirements

- Python 3
- Standard library only
- Optional `NCBI_API_KEY` for higher PubMed limits
- Optional `OPENALEX_API_KEY`

## Quick start

```bash
python3 scripts/verify_references.py refs.md --mode balanced --output-dir reference-audit
```

Format without external verification:

```bash
python3 scripts/verify_references.py refs.md --pipeline format-only --citation-style ama
```

Run the offline regression suite:

```bash
python3 scripts/self_test_verify_references.py
```

See [SKILL.md](SKILL.md) for the complete workflow and [verification_policy.md](references/verification_policy.md) for classification and evidence rules.

## License

MIT-0
