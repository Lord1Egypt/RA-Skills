# Site Failure Playbook

Use this when the school website is hard to scrape, blocks direct fetching, or returns incomplete results.

## Common failure modes
- faculty directory missing or incomplete
- personal page portal blocks direct access
- homepage HTML loads but key fields are hidden in scripts
- school page and personal page disagree on department name
- search engines return junk or unrelated pages

## Recovery order

### Case 1: official faculty directory exists but is poor
1. record the official directory URL anyway
2. extract names, titles, and homepage links if possible
3. supplement from official lab pages and official personal pages
4. mark completeness as low / medium / high

### Case 2: personal homepages block scraping
1. try alternate language path if it exists, for example `/en/`
2. inspect raw HTML for visible fields like title, department, email, research keywords
3. use the page only as partial evidence
4. do not pretend missing fields were verified

### Case 3: search engine results are noisy
1. search by exact school + department + direction
2. then search by school + likely lab keyword
3. then search by person name + school
4. prefer official domains and official subdomains

### Case 4: school affiliation is unclear
Do not rank the person as Priority A until at least two of these align:
- official school page
- official personal homepage
- recent paper affiliation
- official lab page

## Minimum evidence needed before recommending strongly

For Priority A:
- verified person identity
- verified school/department or strong official evidence
- repeated recent evidence in the target direction
- at least one usable public contact or homepage

For Priority B:
- identity likely correct
- direction likely correct
- one major uncertainty remains

For Priority C:
- direction or affiliation still fuzzy
- keep only as backup

## Hard rule
If the evidence is messy, say it is messy. Never hide a weak verification chain.
