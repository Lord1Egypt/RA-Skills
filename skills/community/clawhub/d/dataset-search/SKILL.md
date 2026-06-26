---
name: dataset-search
description: "Find, compare, and obtain datasets or data lakes across ML repositories, cloud public data registries, government portals, scientific archives, geospatial/climate catalogs, NLP corpora, and generic web dataset indexes."
metadata: '{"openclaw":{"requires":{"bins":["python3"]}}}'
---

# Dataset Search

Use this skill when the user needs a dataset, benchmark, public data lake, open-data portal, or data source for analysis, ML, BI, RAG, geospatial work, climate, NLP, multimodal projects, or data engineering.

## Workflow

1. Convert the user request into a dataset brief:
   - research question or analysis goal
   - domain and task type: classification, forecasting, geospatial, NLP, BI, econometrics, image-text, logs, etc.
   - geography, language, period, granularity, expected scale, file format, license, access constraints
   - must-have fields, acceptable proxies, and sources to prefer or avoid
2. Start broad with the bundled script:

```bash
python3 skills/dataset-search/scripts/dataset_search.py search "solar radiation hourly Brazil agriculture" --profile climate --region BR --limit 8 --format markdown
```

3. Narrow by source when the best family is clear:

```bash
python3 skills/dataset-search/scripts/dataset_search.py search "credit card fraud transactions" --source kaggle,huggingface,openml --limit 10
python3 skills/dataset-search/scripts/dataset_search.py search "sentinel crop classification" --profile geospatial --source aws-open-data,copernicus,huggingface
```

4. Compare candidates by relevance, provenance, license, update cadence, schema/metadata quality, access method, size, and whether the source supports direct download or cloud-native querying.
5. For huge cloud data lakes, prefer native access paths such as S3, BigQuery, Delta Sharing, Spark, Athena, Databricks, or cloud storage instead of downloading everything locally.
6. Before downloading gated, paid, huge, sensitive, or license-restricted data, summarize the source, expected size, license, and access requirements for the user.

## Bundled Script

`scripts/dataset_search.py` is a standard-library Python helper. It queries direct APIs/CLIs where practical and emits resilient fallback search links for sources without a stable public search API.

Common commands:

```bash
python3 skills/dataset-search/scripts/dataset_search.py sources
python3 skills/dataset-search/scripts/dataset_search.py search "income inequality Brazil time series" --profile economics --format json --output /tmp/dataset-results.json
python3 skills/dataset-search/scripts/dataset_search.py search "large multilingual instruction dataset" --profile nlp --offline --format markdown
python3 skills/dataset-search/scripts/dataset_search.py download --from-results /tmp/dataset-results.json --index 0 --output-dir /tmp/datasets
python3 skills/dataset-search/scripts/dataset_search.py download --from-results /tmp/dataset-results.json --index 0 --output-dir /tmp/datasets --yes
```

By default, `download` prints a safe acquisition plan. It only executes downloads or source CLIs with `--yes`.

Useful options:

- `--profile`: `general`, `ml`, `nlp`, `geospatial`, `climate`, `economics`, `government`, `brazil`, `biomed`, `multimodal`, `cloud`
- `--region`: country, state, language, or geographic hint, such as `BR`, `EU`, `US`, `Ceara`, `Portuguese`
- `--source`: comma-separated source ids, or `all`
- `--brief`: JSON file with structured fields such as `question`, `domain`, `task`, `geography`, `period`, `format`, `license`, `must_have`, `avoid`, `preferred_sources`
- `--offline`: do not call the network; return source-specific search URLs and acquisition guidance

## Source Coverage

The script has direct adapters for Hugging Face Datasets, Kaggle CLI, OpenML, UCI when its API is reachable, Zenodo, Figshare, data.gov CKAN, NASA/CDC Socrata catalogs, Harvard Dataverse, GBIF, and generic CKAN-style portals when configured in the script.

It also produces guided search/acquisition entries for AWS Registry of Open Data, Google Cloud Public Datasets, Azure Open Datasets, Databricks Marketplace, Snowflake Marketplace, World Bank Open Data, data.europa.eu, IBGE, dados.gov.br, Eurostat, UN Data, WHO GHO, FRED, IMF, Our World in Data, CERN Open Data, NOAA, Copernicus, NASA POWER, NASA Earthdata, USGS, OpenStreetMap/Geofabrik, OpenAQ, Google Dataset Search, DataHub, data.world, Dryad, Mendeley Data, OpenAIRE, Awesome Public Datasets, Common Crawl, The Pile/EleutherAI, LAION, Nasdaq Data Link, and other registry-style sources.

## Source-Specific Notes

- Kaggle downloads require the `kaggle` CLI and local credentials.
- Hugging Face downloads work best with `huggingface-cli`; gated datasets require authentication and acceptance of the dataset terms.
- Databricks Marketplace, Google Cloud, Azure, and many enterprise catalogs often require browser/account access; use the script output as a discovery plan, then use the available browser, web, SQL, Spark, or cloud tools.
- Government and CKAN portals vary in metadata quality. Prefer resources with explicit formats, update dates, dictionaries, and licenses.
- Scientific repositories often expose DOI metadata and file URLs, but the files may be large or numerous. Inspect before downloading all files.

## Response Rules

- Return the top candidates with source, title, URL, why it matches, access method, license, format, and caveats.
- Distinguish confirmed API results from generated search links.
- If the script reports network failures, say which sources failed and whether the result is a fallback.
- Do not claim a dataset is usable until license/access and minimum schema suitability are checked.
- For cloud data lakes, include query/access examples instead of promising a local file.
