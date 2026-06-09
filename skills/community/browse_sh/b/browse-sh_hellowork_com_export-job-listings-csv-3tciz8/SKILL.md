---
name: "export-job-listings-csv"
description: "Reverse-engineer HelloWork.com's job-listing surface (no public XHR/Fetch API — it's SSR HTML + JSON-LD), reconstruct the canonical /fr-fr/emploi/metier_{slug}-ville_{city}-{postal}.html requests, paginate, parse each card and detail page JobPosting JSON-LD, dedup by raw_id/jo…"
category: "jobs"
source: "browse.sh"
tags: [jobs, scraping, csv, reverse-engineering, france, ssr]
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install browse-sh/hellowork.com/export-job-listings-csv-3tciz8"
sourceUrl: "https://github.com/browserbase/browse.sh/blob/main/skills/hellowork.com/export-job-listings-csv-3tciz8/SKILL.md"
---

# export-job-listings-csv

> Reverse-engineer HelloWork.com's job-listing surface (no public XHR/Fetch API — it's SSR HTML + JSON-LD), reconstruct the canonical /fr-fr/emploi/metier_{slug}-ville_{city}-{postal}.html requests, paginate, parse each card and detail page JobPosting JSON-LD, dedup by raw_id/jo…

- **Category:** jobs
- **Source:** browse.sh
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install browse-sh/hellowork.com/export-job-listings-csv-3tciz8`
- **Source URL:** [https://github.com/browserbase/browse.sh/blob/main/skills/hellowork.com/export-job-listings-csv-3tciz8/SKILL.md](https://github.com/browserbase/browse.sh/blob/main/skills/hellowork.com/export-job-listings-csv-3tciz8/SKILL.md)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install browse-sh/hellowork.com/export-job-listings-csv-3tciz8
```
