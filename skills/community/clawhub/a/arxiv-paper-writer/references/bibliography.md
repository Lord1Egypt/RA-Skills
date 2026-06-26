# Bibliography Reference

Use this reference when building or reviewing `references.bib`.

## Principles

- Prefer real, verifiable academic references.
- Do not invent titles, authors, venues, arXiv IDs, DOIs, or years.
- If metadata is uncertain, mark the entry for verification in a note outside the BibTeX entry.
- Use stable lowercase keys: `authorYYYYshorttitle`.
- Keep keys readable and consistent.

## Search strategy

For survey papers, split the topic into 5-8 literature clusters. For each cluster, identify:

- foundational works
- recent surveys
- representative systems
- benchmark/evaluation papers
- critique/safety/limitations papers

For the AI-agent-survey pattern, useful clusters were:

- symbolic agents and BDI
- reinforcement learning agents
- large language models
- LLM reasoning and planning
- tool use and memory
- agent frameworks
- multi-agent systems
- evaluation and safety

## Target counts

- Short paper: 15-25 references
- Standard survey: 35-60 references
- Large survey: 60+ references with stronger taxonomy and related-work coverage

## BibTeX entry shape

Article or arXiv paper:

```bibtex
@article{keyYYYYtopic,
  title={Full Title},
  author={Author, First and Second, Author},
  journal={Journal Name or arXiv preprint arXiv:XXXX.XXXXX},
  year={YYYY},
  doi={10.xxxx/example}
}
```

Conference paper:

```bibtex
@inproceedings{keyYYYYtopic,
  title={Full Title},
  author={Author, First and Second, Author},
  booktitle={Conference Name},
  pages={1--12},
  year={YYYY}
}
```

## Citation rules

Use `\citet{key}` when the author is part of the sentence:

```latex
\citet{vaswani2017attention} introduced the Transformer architecture.
```

Use `\citep{key}` when the citation supports a claim:

```latex
Transformers became foundational for modern language models \citep{vaswani2017attention}.
```

Use multiple citations when summarizing a research direction:

```latex
LLM agents combine reasoning, acting, and tool use \citep{yao2023react,shinn2024reflexion}.
```
