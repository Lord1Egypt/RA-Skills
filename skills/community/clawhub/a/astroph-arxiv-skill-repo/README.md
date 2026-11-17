# Astro-ph Radar

**Version:** 1.1.3  
**Description:** Searches for recent papers specifically in the astro-ph repository on arXiv, preserving academic rigor.

## Capabilities

- **`search-astroph`**: Queries arXiv filtering by `astro-ph`, extracting full abstracts, authors, and PDF links.

## Runbook

When a user requests a literature search for a specific topic, execute these steps strictly:

### 1. Construct the Query
- **Base URL:** `https://export.arxiv.org/api/query`
- **Crucial arXiv API Quirk:** Combining the top-level `cat:astro-ph` with keywords and `sortBy=submittedDate` breaks the API's sorting and returns old papers. To get truly recent papers, you MUST use a subcategory like `cat:astro-ph.GA` (Galactic Astrophysics), `cat:astro-ph.SR`, etc., or omit the `cat:` filter if the query is already specific enough.
- **Cost-Control Limit:** Identify the number of papers requested by the user. If the user does not specify a number, default strictly to `max_results=2`. **NEVER** exceed the requested limit.
- **Query Construction:** Combine parameters:
  ```
  ?search_query=cat:astro-ph.GA+AND+all:"<user_topic>"&sortBy=submittedDate&sortOrder=descending&max_results=<number>
  ```
- **Encoding:** Ensure spaces and quotes are properly URL-encoded (e.g., `%20AND%20`).

### 2. Execute Fetch and Parse
- Use the embedded Python script provided in the skill to fetch, parse, and format the XML data perfectly. It ensures correct highlighting, formatting, and handles the `HTTPS` connection reliably.

### 3. Format the Output (Strict Academic Format)
- **Title:** **Bold** the title.
- **Authors:** List the authors (use "et al." if there are more than 4).
- **Date:** Show the `published` date.
- **Abstract (CRITICAL REQUIREMENT):** Extract the full `<summary>`. DO NOT summarize, rephrase, or truncate. Output the EXACT text inside a blockquote (`> `).
- **Highlighting:** Scan the abstract and automatically **bold** any mentions of specific catalogs, surveys, instruments (e.g., Gaia, VVV, VVVX, H.E.S.S., ACS, MACHO) and key methodologies (e.g., metallicity, decontamination, proper-motion, maximum likelihood).
- **Links:** Provide both the arXiv abstract page link and the direct PDF link.
