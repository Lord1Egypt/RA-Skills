# Examples

## Paragraph Polish

User context:

```text
Field: biomedical research
Section: discussion
Intent: The treatment may improve outcomes, but our data are observational, so we should avoid causal language.
Edit strength: moderate rewrite
```

Draft:

```text
These results prove that the treatment improves patient survival and should be used broadly in clinical settings.
```

Better revision:

```text
These findings suggest that the treatment is associated with improved patient survival, although the observational design prevents causal interpretation. Further prospective studies are needed before broad clinical adoption can be recommended.
```

Meaning risk:

```text
The original "prove" was too strong for observational data. The revision keeps the positive association but lowers the certainty.
```

## Reviewer Response

Reviewer comment:

```text
The authors should clarify how missing values were handled.
```

User notes:

```text
We added a sentence to Methods, page 6, lines 120-123. We used multiple imputation with 20 datasets.
```

Response:

```text
Thank you for this helpful suggestion. We have clarified the handling of missing values in the Methods section (page 6, lines 120-123). Specifically, we now state that missing covariate values were handled using multiple imputation with 20 imputed datasets.
```

## Launch Copy

Short social post:

```text
I turned a context-first academic writing workflow into an installable Agent Skill.

It helps researchers polish paragraphs, abstracts, and reviewer responses without inventing claims or silently changing the author's meaning.

The Agent asks for context first, revises second, and always outputs a meaning-risk check.
```

GitHub repository description:

```text
Nature-inspired academic writing Skill for polishing research paragraphs, abstracts, reviewer responses, and peer-review feedback while preserving author intent.
```
