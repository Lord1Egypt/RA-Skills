# Public company starter profile

Begin with one Organization and only explicitly evidenced Product/BusinessSegment/Topic entities. Candidate relation meanings may include `offers_product` or `has_segment`, but creating a relation requires supporting disclosure. A mention in a customer list does not establish a current contract or quantified revenue relationship.

Metric concepts should have narrow meanings. Keep accounting basis, exclusions, reporting period and units on each fact. IFRS operating profit, non-IFRS operating profit and non-IFRS operating profit excluding a product group are distinct fact scopes; do not average or overwrite them. Reported capex and cash capital payments require distinct definitions if the disclosure makes that distinction.

Do not infer a company-wide ontology from one document. State which source sections and business questions were covered. Begin with approximately 5–15 useful concepts; expand only for the task. A concept count is not a quality score.

Three practical questions:

- Which businesses/products are explicitly described, and by which source?
- Which disclosed figures are comparable across periods, and which qualifier changes prevent comparison?
- Which newly observed statements contradict or qualify prior source claims?

Examples of reasons to leave a question unresolved: unavailable footnote, ambiguous entity identity, missing comparison period, conflicting disclosure, nonexhaustive list, or absent underlying source. Do not replace any of these with a numeric zero.

Derived calculations belong in the answer with disclosed inputs, arithmetic and precision limits, not in v0.2 reported-claim storage. No investment rating, credit decision, operational action or enterprise authorization follows automatically from a packaged fact.
