#!/usr/bin/env python3
"""Search and obtain datasets/data lakes from many public catalogs.

The helper is intentionally dependency-free. It uses direct APIs and local CLIs
where stable enough, and returns guided search links where a source is better
accessed through a browser, marketplace, SQL engine, or cloud-native tool.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


USER_AGENT = "openclaw-dataset-search/1.0 (+https://openclaw.ai)"
DEFAULT_TIMEOUT = 15
MAX_TEXT = 600


PROFILES: dict[str, dict[str, Any]] = {
    "general": {
        "terms": ["dataset", "data", "open data"],
        "sources": [],
    },
    "ml": {
        "terms": ["machine learning", "benchmark", "classification", "regression"],
        "sources": ["kaggle", "huggingface", "openml", "uci", "zenodo"],
    },
    "nlp": {
        "terms": ["nlp", "text", "language", "corpus"],
        "sources": ["huggingface", "common-crawl", "the-pile", "laion", "zenodo"],
    },
    "geospatial": {
        "terms": ["geospatial", "satellite", "remote sensing", "gis"],
        "sources": [
            "aws-open-data",
            "google-cloud-public",
            "copernicus",
            "earthdata",
            "nasa",
            "noaa",
            "usgs",
            "openstreetmap",
            "gbif",
            "huggingface",
        ],
    },
    "climate": {
        "terms": ["climate", "weather", "meteorological", "environment"],
        "sources": [
            "noaa",
            "nasa-power",
            "earthdata",
            "aws-open-data",
            "google-cloud-public",
            "copernicus",
            "nasa",
            "openaq",
        ],
    },
    "economics": {
        "terms": ["economic indicators", "time series", "country", "development"],
        "sources": [
            "world-bank",
            "our-world-in-data",
            "eurostat",
            "fred",
            "imf",
            "data-gov",
            "data-europa",
            "ibge",
            "dados-gov-br",
            "google-cloud-public",
        ],
    },
    "government": {
        "terms": ["government open data", "public data", "statistics"],
        "sources": ["data-gov", "data-europa", "dados-gov-br", "ibge", "world-bank", "un-data", "cdc"],
    },
    "brazil": {
        "terms": ["Brazil", "Brasil", "IBGE", "dados abertos"],
        "sources": ["ibge", "dados-gov-br", "world-bank", "data-gov", "google-cloud-public"],
    },
    "biomed": {
        "terms": ["biology", "genomics", "health", "biomedical"],
        "sources": [
            "aws-open-data",
            "zenodo",
            "figshare",
            "harvard-dataverse",
            "gbif",
            "cdc",
            "who-gho",
            "huggingface",
            "data-gov",
        ],
    },
    "multimodal": {
        "terms": ["image text", "vision language", "multimodal"],
        "sources": ["huggingface", "laion", "kaggle", "zenodo"],
    },
    "cloud": {
        "terms": ["data lake", "public cloud dataset", "big data"],
        "sources": [
            "aws-open-data",
            "google-cloud-public",
            "azure-open-datasets",
            "databricks",
            "snowflake-marketplace",
        ],
    },
}


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    categories: tuple[str, ...]
    homepage: str
    search_url: str
    access: str
    notes: str
    adapter: str = "link"
    api_url: str | None = None
    search_context: str | None = None


SOURCES: dict[str, Source] = {
    "huggingface": Source(
        id="huggingface",
        name="Hugging Face Datasets",
        categories=("ml", "nlp", "multimodal", "audio", "vision"),
        homepage="https://huggingface.co/datasets",
        search_url="https://huggingface.co/datasets?search={query}",
        access="api/cli/browser",
        notes="Best for ML/NLP/multimodal datasets. Some datasets are gated.",
        adapter="huggingface",
        api_url="https://huggingface.co/api/datasets",
    ),
    "kaggle": Source(
        id="kaggle",
        name="Kaggle Datasets",
        categories=("ml", "analytics", "education"),
        homepage="https://www.kaggle.com/datasets",
        search_url="https://www.kaggle.com/datasets?search={query}",
        access="cli/browser",
        notes="Requires Kaggle CLI credentials for download. Good for portfolios and notebooks.",
        adapter="kaggle",
    ),
    "openml": Source(
        id="openml",
        name="OpenML",
        categories=("ml", "benchmarks"),
        homepage="https://www.openml.org/search?type=data",
        search_url="https://www.openml.org/search?type=data&sort=runs&qualities.NumberOfInstances=between_0_1000000000&id=0&status=active&q={query}",
        access="api/browser",
        notes="ML datasets, tasks, benchmarks, and reproducible evaluations.",
        adapter="openml",
        api_url="https://www.openml.org/api/v1/json/data/list/data_name/{query}",
    ),
    "uci": Source(
        id="uci",
        name="UCI Machine Learning Repository",
        categories=("ml", "education", "benchmarks"),
        homepage="https://archive.ics.uci.edu/",
        search_url="https://archive.ics.uci.edu/datasets?search={query}",
        access="api/browser",
        notes="Classic small and medium ML datasets. API availability may vary.",
        adapter="uci",
        api_url="https://archive.ics.uci.edu/api/dataset/search?search={query}",
    ),
    "zenodo": Source(
        id="zenodo",
        name="Zenodo",
        categories=("science", "doi", "research"),
        homepage="https://zenodo.org/",
        search_url="https://zenodo.org/search?q={query}&f=resource_type%3Adataset",
        access="api/browser/doi",
        notes="Research datasets with DOI metadata and files.",
        adapter="zenodo",
        api_url="https://zenodo.org/api/records",
    ),
    "figshare": Source(
        id="figshare",
        name="Figshare",
        categories=("science", "doi", "research"),
        homepage="https://figshare.com/",
        search_url="https://figshare.com/search?q={query}",
        access="api/browser/doi",
        notes="Scientific datasets, articles, figures, and supplementary files.",
        adapter="figshare",
        api_url="https://api.figshare.com/v2/articles/search",
    ),
    "data-gov": Source(
        id="data-gov",
        name="data.gov",
        categories=("government", "us", "ckan"),
        homepage="https://catalog.data.gov/dataset",
        search_url="https://catalog.data.gov/dataset/?q={query}",
        access="api/browser",
        notes="US government open data catalog.",
        adapter="ckan",
        api_url="https://catalog.data.gov/api/3/action/package_search",
    ),
    "nasa": Source(
        id="nasa",
        name="NASA Open Data",
        categories=("science", "space", "earth", "socrata"),
        homepage="https://data.nasa.gov/",
        search_url="https://data.nasa.gov/browse?q={query}",
        access="api/browser",
        notes="NASA open data catalog. Also check Earthdata and NASA POWER for specialized access.",
        adapter="socrata",
        api_url="https://api.us.socrata.com/api/catalog/v1",
        search_context="data.nasa.gov",
    ),
    "harvard-dataverse": Source(
        id="harvard-dataverse",
        name="Harvard Dataverse",
        categories=("science", "doi", "research", "dataverse"),
        homepage="https://dataverse.harvard.edu/",
        search_url="https://dataverse.harvard.edu/dataverse/harvard?q={query}",
        access="api/browser/doi",
        notes="Large Dataverse repository for research datasets with rich citation metadata.",
        adapter="dataverse",
        api_url="https://dataverse.harvard.edu/api/search",
    ),
    "gbif": Source(
        id="gbif",
        name="GBIF",
        categories=("biodiversity", "biology", "geospatial", "science"),
        homepage="https://www.gbif.org/dataset/search",
        search_url="https://www.gbif.org/dataset/search?q={query}",
        access="api/browser",
        notes="Biodiversity occurrence and checklist datasets with DOI-backed downloads.",
        adapter="gbif",
        api_url="https://api.gbif.org/v1/dataset/search",
    ),
    "aws-open-data": Source(
        id="aws-open-data",
        name="Registry of Open Data on AWS",
        categories=("cloud", "s3", "big-data", "geospatial", "climate"),
        homepage="https://registry.opendata.aws/",
        search_url="https://registry.opendata.aws/search?q={query}",
        access="s3/athena/spark/browser",
        notes="Large cloud-hosted public datasets. Prefer S3/Athena/Spark over local downloads.",
    ),
    "google-cloud-public": Source(
        id="google-cloud-public",
        name="Google Cloud Public Datasets",
        categories=("cloud", "bigquery", "analytics"),
        homepage="https://cloud.google.com/public-datasets",
        search_url="https://cloud.google.com/datasets?query={query}",
        access="bigquery/cloud-storage/browser",
        notes="Best for SQL analytics at scale through BigQuery and Cloud Storage.",
    ),
    "azure-open-datasets": Source(
        id="azure-open-datasets",
        name="Azure Open Datasets",
        categories=("cloud", "azure", "ml"),
        homepage="https://azure.microsoft.com/products/open-datasets",
        search_url="https://learn.microsoft.com/search/?terms={query}%20Azure%20Open%20Datasets",
        access="azure/synapse/ml/browser",
        notes="Curated datasets integrated with Azure Machine Learning and analytics services.",
    ),
    "databricks": Source(
        id="databricks",
        name="Databricks Marketplace",
        categories=("cloud", "delta", "lakehouse", "marketplace"),
        homepage="https://www.databricks.com/product/marketplace",
        search_url="https://marketplace.databricks.com/search?q={query}",
        access="marketplace/delta-sharing/browser",
        notes="Marketplace and Delta Sharing datasets; often requires account/workspace access.",
    ),
    "world-bank": Source(
        id="world-bank",
        name="World Bank Open Data",
        categories=("economics", "development", "statistics"),
        homepage="https://data.worldbank.org/",
        search_url="https://datacatalog.worldbank.org/search/dataset?query={query}",
        access="api/browser/csv",
        notes="Economic, social, education, health, energy, and country indicators.",
    ),
    "our-world-in-data": Source(
        id="our-world-in-data",
        name="Our World in Data",
        categories=("statistics", "global", "csv", "research"),
        homepage="https://ourworldindata.org/",
        search_url="https://ourworldindata.org/search?q={query}",
        access="csv/github/browser",
        notes="Curated global indicator datasets and charts, often with CSV/GitHub sources.",
    ),
    "eurostat": Source(
        id="eurostat",
        name="Eurostat",
        categories=("statistics", "eu", "economics", "government"),
        homepage="https://ec.europa.eu/eurostat/data/database",
        search_url="https://ec.europa.eu/eurostat/search?p_auth=&queryText={query}",
        access="api/browser",
        notes="Official EU statistics. Prefer Eurostat API once the dataset code is identified.",
    ),
    "un-data": Source(
        id="un-data",
        name="UN Data",
        categories=("statistics", "global", "government"),
        homepage="https://data.un.org/",
        search_url="https://data.un.org/Search.aspx?q={query}",
        access="browser/api",
        notes="United Nations statistical databases across global development topics.",
    ),
    "who-gho": Source(
        id="who-gho",
        name="WHO Global Health Observatory",
        categories=("health", "statistics", "global"),
        homepage="https://www.who.int/data/gho",
        search_url="https://www.who.int/search?query={query}%20GHO%20data",
        access="api/browser",
        notes="Global public health indicators and time series.",
    ),
    "cdc": Source(
        id="cdc",
        name="CDC Open Data",
        categories=("health", "government", "us", "socrata"),
        homepage="https://data.cdc.gov/",
        search_url="https://data.cdc.gov/browse?q={query}",
        access="api/browser",
        notes="US public health datasets hosted on Socrata.",
        adapter="socrata",
        api_url="https://api.us.socrata.com/api/catalog/v1",
        search_context="data.cdc.gov",
    ),
    "fred": Source(
        id="fred",
        name="FRED Economic Data",
        categories=("economics", "finance", "time-series", "us"),
        homepage="https://fred.stlouisfed.org/",
        search_url="https://fred.stlouisfed.org/searchresults/?search_type=series&search={query}",
        access="api/browser/csv",
        notes="Economic time series. FRED API downloads may require an API key.",
    ),
    "imf": Source(
        id="imf",
        name="IMF Data",
        categories=("economics", "finance", "statistics", "global"),
        homepage="https://data.imf.org/",
        search_url="https://www.imf.org/en/Search#q={query}%20data",
        access="api/browser",
        notes="Macroeconomic and financial datasets from the International Monetary Fund.",
    ),
    "data-europa": Source(
        id="data-europa",
        name="data.europa.eu",
        categories=("government", "eu", "open-data"),
        homepage="https://data.europa.eu/",
        search_url="https://data.europa.eu/data/datasets?query={query}",
        access="api/browser",
        notes="European Union and member-state open data catalog.",
    ),
    "dados-gov-br": Source(
        id="dados-gov-br",
        name="Portal Brasileiro de Dados Abertos",
        categories=("government", "brazil", "open-data"),
        homepage="https://dados.gov.br/",
        search_url="https://dados.gov.br/dados/conjuntos-dados?termo={query}",
        access="api/browser",
        notes="Brazilian federal open data portal. APIs and metadata shape can vary by dataset.",
    ),
    "ibge": Source(
        id="ibge",
        name="IBGE",
        categories=("government", "brazil", "statistics", "geography"),
        homepage="https://www.ibge.gov.br/",
        search_url="https://www.ibge.gov.br/busca.html?searchword={query}",
        access="api/browser/csv",
        notes="Brazilian census, geography, social, demographic, and economic statistics.",
    ),
    "cern": Source(
        id="cern",
        name="CERN Open Data Portal",
        categories=("science", "physics"),
        homepage="https://opendata.cern.ch/",
        search_url="https://opendata.cern.ch/search?q={query}",
        access="browser/api",
        notes="Particle physics data and derived educational datasets.",
    ),
    "noaa": Source(
        id="noaa",
        name="NOAA Open Data",
        categories=("climate", "weather", "ocean", "environment"),
        homepage="https://www.noaa.gov/information-technology/open-data-dissemination",
        search_url="https://www.noaa.gov/search?query={query}%20data",
        access="api/cloud/browser",
        notes="Weather, climate, ocean, atmospheric, and environmental time series.",
    ),
    "copernicus": Source(
        id="copernicus",
        name="Copernicus Data Space Ecosystem",
        categories=("geospatial", "satellite", "remote-sensing", "eu"),
        homepage="https://dataspace.copernicus.eu/",
        search_url="https://dataspace.copernicus.eu/search?search={query}",
        access="browser/api/cloud",
        notes="Sentinel satellite data and remote-sensing workflows.",
    ),
    "nasa-power": Source(
        id="nasa-power",
        name="NASA POWER",
        categories=("climate", "energy", "agriculture"),
        homepage="https://power.larc.nasa.gov/",
        search_url="https://power.larc.nasa.gov/data-access-viewer/?query={query}",
        access="api/browser",
        notes="Solar, wind, temperature, and meteorological parameters for energy/agriculture.",
    ),
    "earthdata": Source(
        id="earthdata",
        name="NASA Earthdata",
        categories=("earth", "climate", "geospatial", "satellite"),
        homepage="https://www.earthdata.nasa.gov/",
        search_url="https://search.earthdata.nasa.gov/search?q={query}",
        access="api/browser/cloud",
        notes="NASA Earth science collections; many products require Earthdata Login.",
    ),
    "usgs": Source(
        id="usgs",
        name="USGS Data",
        categories=("geospatial", "earth", "government", "us"),
        homepage="https://www.usgs.gov/products/data",
        search_url="https://www.usgs.gov/search?keywords={query}",
        access="api/browser",
        notes="US geological, hydrological, remote sensing, and hazards data.",
    ),
    "openstreetmap": Source(
        id="openstreetmap",
        name="OpenStreetMap / Geofabrik",
        categories=("geospatial", "maps", "osm"),
        homepage="https://download.geofabrik.de/",
        search_url="https://download.geofabrik.de/index.html",
        access="pbf/shp/browser",
        notes="OpenStreetMap extracts by region; select geography before downloading.",
    ),
    "openaq": Source(
        id="openaq",
        name="OpenAQ",
        categories=("air-quality", "environment", "api"),
        homepage="https://openaq.org/",
        search_url="https://openaq.org/#/locations?query={query}",
        access="api/browser",
        notes="Air quality measurements and station metadata.",
    ),
    "google-dataset-search": Source(
        id="google-dataset-search",
        name="Google Dataset Search",
        categories=("search", "catalog"),
        homepage="https://datasetsearch.research.google.com/",
        search_url="https://datasetsearch.research.google.com/search?query={query}",
        access="browser",
        notes="Meta-search for datasets across publishers, universities, portals, and repositories.",
    ),
    "datahub": Source(
        id="datahub",
        name="DataHub",
        categories=("catalog", "csv", "json"),
        homepage="https://datahub.io/",
        search_url="https://datahub.io/search?q={query}",
        access="browser/http",
        notes="Community data packages; useful for quick CSV/JSON studies.",
    ),
    "data-world": Source(
        id="data-world",
        name="data.world",
        categories=("catalog", "collaboration", "sql"),
        homepage="https://data.world/",
        search_url="https://data.world/search?context=community&q={query}&type=resources",
        access="api/browser/sql",
        notes="Community and organizational datasets with SQL/API access for many resources.",
    ),
    "dryad": Source(
        id="dryad",
        name="Dryad",
        categories=("science", "doi", "research"),
        homepage="https://datadryad.org/",
        search_url="https://datadryad.org/search?utf8=%E2%9C%93&q={query}",
        access="api/browser/doi",
        notes="Curated research datasets linked to publications.",
    ),
    "mendeley-data": Source(
        id="mendeley-data",
        name="Mendeley Data",
        categories=("science", "doi", "research"),
        homepage="https://data.mendeley.com/",
        search_url="https://data.mendeley.com/research-data/?search={query}",
        access="browser/doi",
        notes="Research datasets and supplementary data with DOI metadata.",
    ),
    "openaire": Source(
        id="openaire",
        name="OpenAIRE Explore",
        categories=("science", "research", "eu"),
        homepage="https://explore.openaire.eu/",
        search_url="https://explore.openaire.eu/search/find/research-outcomes?keyword={query}&type=dataset",
        access="browser/api",
        notes="European research graph for datasets, publications, software, and grants.",
    ),
    "snowflake-marketplace": Source(
        id="snowflake-marketplace",
        name="Snowflake Marketplace",
        categories=("cloud", "warehouse", "marketplace"),
        homepage="https://app.snowflake.com/marketplace",
        search_url="https://app.snowflake.com/marketplace?search={query}",
        access="marketplace/sql/browser",
        notes="Commercial and free data products for Snowflake. Account access is usually required.",
    ),
    "nasdaq-data-link": Source(
        id="nasdaq-data-link",
        name="Nasdaq Data Link",
        categories=("finance", "economics", "market-data"),
        homepage="https://data.nasdaq.com/",
        search_url="https://data.nasdaq.com/search?query={query}",
        access="api/browser/csv",
        notes="Financial and alternative datasets. Many downloads require an API key or subscription.",
    ),
    "awesome-public-datasets": Source(
        id="awesome-public-datasets",
        name="Awesome Public Datasets",
        categories=("catalog", "github", "curated-list"),
        homepage="https://github.com/awesomedata/awesome-public-datasets",
        search_url="https://github.com/search?q={query}%20awesome%20public%20datasets&type=repositories",
        access="github/browser",
        notes="Curated lists for discovering domain-specific sources.",
    ),
    "common-crawl": Source(
        id="common-crawl",
        name="Common Crawl",
        categories=("nlp", "web", "large-scale"),
        homepage="https://commoncrawl.org/",
        search_url="https://commoncrawl.org/?s={query}",
        access="s3/http/spark",
        notes="Massive web crawl corpus. Use WARC/WET indexes and cloud workflows.",
    ),
    "the-pile": Source(
        id="the-pile",
        name="The Pile / EleutherAI datasets",
        categories=("nlp", "llm", "research"),
        homepage="https://pile.eleuther.ai/",
        search_url="https://huggingface.co/datasets?search={query}%20EleutherAI%20Pile",
        access="browser/huggingface",
        notes="LLM research corpora. Check licenses and content restrictions carefully.",
    ),
    "laion": Source(
        id="laion",
        name="LAION datasets",
        categories=("multimodal", "image-text", "research"),
        homepage="https://laion.ai/",
        search_url="https://laion.ai/?s={query}",
        access="browser/http/cloud",
        notes="Large image-text metadata datasets. Requires ethical/legal review before use.",
    ),
}


@dataclass
class SearchResult:
    source: str
    source_name: str
    title: str
    url: str
    id: str | None = None
    description: str | None = None
    license: str | None = None
    formats: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    access: str | None = None
    size: str | None = None
    updated: str | None = None
    confirmed: bool = False
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    downloads: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "source_name": self.source_name,
            "title": self.title,
            "id": self.id,
            "url": self.url,
            "description": self.description,
            "license": self.license,
            "formats": self.formats,
            "tags": self.tags,
            "access": self.access,
            "size": self.size,
            "updated": self.updated,
            "confirmed": self.confirmed,
            "score": round(self.score, 3),
            "reasons": self.reasons,
            "downloads": self.downloads,
            "raw": self.raw,
        }


class HttpClient:
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout

    def request(
        self,
        url: str,
        *,
        method: str = "GET",
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, str, bytes]:
        req_headers = {"User-Agent": USER_AGENT, "Accept": "application/json, text/plain, */*"}
        if headers:
            req_headers.update(headers)
        req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            return resp.status, content_type, body

    def json(
        self,
        url: str,
        *,
        method: str = "GET",
        payload: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        data = None
        req_headers = headers or {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            req_headers = {"Content-Type": "application/json", **req_headers}
        _status, _content_type, body = self.request(url, method=method, data=data, headers=req_headers)
        return json.loads(body.decode("utf-8", errors="replace"))


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def compact_text(value: Any, limit: int = MAX_TEXT) -> str | None:
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        value = " ".join(str(x) for x in value if x)
    text = re.sub(r"\s+", " ", str(value)).strip()
    if not text:
        return None
    if len(text) > limit:
        return text[: limit - 1].rstrip() + "..."
    return text


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def uniq(values: Iterable[Any]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(text)
    return out


def source_search_url(source: Source, query: str) -> str:
    quoted = urllib.parse.quote_plus(query)
    return source.search_url.format(query=quoted)


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[A-Za-z0-9_À-ÿ-]{3,}", text.lower()) if t not in STOPWORDS]


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "dataset",
    "datasets",
    "data",
    "open",
    "public",
    "uma",
    "para",
    "com",
    "dos",
    "das",
    "que",
    "por",
    "dados",
    "base",
    "bases",
    "conjunto",
    "conjuntos",
}


def load_brief(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise SystemExit("--brief must point to a JSON object")
    return value


def build_query(args: argparse.Namespace, brief: dict[str, Any]) -> str:
    parts: list[str] = []
    if args.query:
        parts.append(args.query)
    for key in ("question", "domain", "task", "geography", "period", "granularity", "modality", "format", "license"):
        value = brief.get(key)
        if isinstance(value, str):
            parts.append(value)
    for key in ("must_have", "keywords", "entities"):
        values = brief.get(key)
        if isinstance(values, list):
            parts.extend(str(v) for v in values)
    if args.region:
        parts.append(args.region)
    profile = PROFILES.get(args.profile or "general", PROFILES["general"])
    parts.extend(profile.get("terms", []))
    query = " ".join(p for p in parts if p)
    query = re.sub(r"\s+", " ", query).strip()
    if not query:
        raise SystemExit("Provide QUERY or --brief with enough fields to build a query")
    return query


def select_sources(source_arg: str, profile: str, brief: dict[str, Any]) -> list[Source]:
    requested: list[str] = []
    if source_arg and source_arg != "all":
        requested = [s.strip() for s in source_arg.split(",") if s.strip()]
    preferred = brief.get("preferred_sources")
    if not requested and isinstance(preferred, list) and preferred:
        requested = [str(s).strip() for s in preferred if str(s).strip()]

    if requested:
        unknown = [s for s in requested if s not in SOURCES]
        if unknown:
            raise SystemExit(f"Unknown source id(s): {', '.join(unknown)}. Use the sources command.")
        return [SOURCES[s] for s in requested]

    source_ids = list(SOURCES)
    profile_sources = PROFILES.get(profile, {}).get("sources", [])
    if profile_sources:
        preferred_set = set(profile_sources)
        source_ids.sort(key=lambda s: (0 if s in preferred_set else 1, s))
    return [SOURCES[s] for s in source_ids]


def score_result(result: SearchResult, query: str, profile: str, source: Source) -> SearchResult:
    q_tokens = set(tokenize(query))
    corpus = " ".join(
        [
            result.title or "",
            result.description or "",
            " ".join(result.tags),
            " ".join(result.formats),
            result.source_name,
        ]
    )
    c_tokens = set(tokenize(corpus))
    matches = sorted(q_tokens & c_tokens)
    score = 0.15
    reasons: list[str] = []
    if matches:
        score += min(0.5, len(matches) / max(3, len(q_tokens)))
        reasons.append("matched query terms: " + ", ".join(matches[:8]))
    if result.confirmed:
        score += 0.18
        reasons.append("confirmed through API/CLI")
    if result.license:
        score += 0.06
        reasons.append("license metadata present")
    if result.formats:
        score += 0.05
        reasons.append("format/resource metadata present")
    if result.downloads.get("commands") or result.downloads.get("urls"):
        score += 0.06
        reasons.append("acquisition path available")
    profile_sources = set(PROFILES.get(profile, {}).get("sources", []))
    if source.id in profile_sources:
        score += 0.08
        reasons.append(f"source fits {profile} profile")
    if not result.confirmed:
        reasons.append("fallback discovery link; verify manually")
    result.score = min(score, 1.0)
    result.reasons = uniq([*result.reasons, *reasons])
    return result


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def search_huggingface(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    url = source.api_url + "?" + urllib.parse.urlencode({"search": query, "limit": limit, "full": "true"})
    data = client.json(url)
    results: list[SearchResult] = []
    if not isinstance(data, list):
        return results
    for item in data[:limit]:
        repo_id = item.get("id") or item.get("_id")
        if not repo_id:
            continue
        card = item.get("cardData") if isinstance(item.get("cardData"), dict) else {}
        license_value = card.get("license") or item.get("license")
        if isinstance(license_value, list):
            license_value = ", ".join(str(x) for x in license_value)
        tags = uniq([*as_list(item.get("tags")), *as_list(card.get("tags"))])
        description = compact_text(card.get("pretty_name") or card.get("description") or item.get("description"))
        commands = [
            f"huggingface-cli download {shell_quote(repo_id)} --repo-type dataset --local-dir \"$OUTPUT_DIR/{safe_slug(repo_id)}\""
        ]
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=repo_id,
                id=repo_id,
                url=f"https://huggingface.co/datasets/{repo_id}",
                description=description,
                license=compact_text(license_value, 120),
                tags=tags[:20],
                access=source.access,
                updated=item.get("lastModified"),
                confirmed=True,
                downloads={"commands": commands, "requires": ["huggingface-cli for full repo download"]},
                raw=safe_raw(item),
            )
        )
    return results


def search_kaggle(source: Source, query: str, limit: int) -> list[SearchResult]:
    if not command_exists("kaggle"):
        return []
    cmd = ["kaggle", "datasets", "list", "-s", query, "--csv"]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=30, check=False)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "kaggle CLI failed").strip())
    text = proc.stdout.strip()
    if not text:
        return []
    rows = list(csv.DictReader(text.splitlines()))
    results: list[SearchResult] = []
    for row in rows[:limit]:
        ref = row.get("ref") or row.get("Ref") or row.get("datasetRef")
        title = row.get("title") or row.get("Title") or ref
        if not ref or not title:
            continue
        formats = []
        if row.get("fileType"):
            formats.append(row["fileType"])
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=title,
                id=ref,
                url=f"https://www.kaggle.com/datasets/{ref}",
                description=compact_text(row.get("subtitle") or row.get("description")),
                license=compact_text(row.get("licenseName") or row.get("license")),
                formats=formats,
                access=source.access,
                size=row.get("size") or row.get("Size"),
                updated=row.get("lastUpdated") or row.get("LastUpdated"),
                confirmed=True,
                downloads={
                    "commands": [f"kaggle datasets download -d {shell_quote(ref)} -p \"$OUTPUT_DIR/{safe_slug(ref)}\" --unzip"],
                    "requires": ["kaggle CLI credentials"],
                },
                raw={k: v for k, v in row.items() if v},
            )
        )
    return results


def search_openml(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    url = source.api_url.format(query=urllib.parse.quote(query, safe=""))
    data = client.json(url)
    datasets = (((data or {}).get("data") or {}).get("datasets") or {}).get("dataset", [])
    if isinstance(datasets, dict):
        datasets = [datasets]
    results: list[SearchResult] = []
    for item in datasets[:limit]:
        did = str(item.get("did") or item.get("id") or "")
        name = item.get("name") or f"OpenML dataset {did}"
        if not did:
            continue
        file_id = item.get("file_id")
        download_url = item.get("url")
        if not download_url and file_id:
            download_url = f"https://www.openml.org/data/v1/download/{file_id}"
        commands = []
        urls = []
        if download_url:
            urls.append(download_url)
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=name,
                id=did,
                url=f"https://www.openml.org/d/{did}",
                description=compact_text(item.get("description") or item.get("default_target_attribute")),
                license=compact_text(item.get("licence") or item.get("license")),
                formats=uniq([item.get("format"), "ARFF" if download_url else None]),
                tags=uniq([item.get("status"), item.get("version_label")]),
                access=source.access,
                size=compact_text(
                    " ".join(
                        str(x)
                        for x in [
                            item.get("NumberOfInstances") and f"{item.get('NumberOfInstances')} rows",
                            item.get("NumberOfFeatures") and f"{item.get('NumberOfFeatures')} features",
                        ]
                        if x
                    ),
                    120,
                ),
                updated=item.get("date"),
                confirmed=True,
                downloads={"urls": urls, "commands": commands},
                raw=safe_raw(item),
            )
        )
    return results


def search_uci(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    url = source.api_url.format(query=urllib.parse.quote_plus(query))
    data = client.json(url)
    candidates = []
    if isinstance(data, dict):
        for key in ("data", "datasets", "results"):
            if isinstance(data.get(key), list):
                candidates = data[key]
                break
        if not candidates and isinstance(data.get("payload"), list):
            candidates = data["payload"]
    elif isinstance(data, list):
        candidates = data
    results: list[SearchResult] = []
    for item in candidates[:limit]:
        dataset_id = item.get("id") or item.get("dataset_id") or item.get("slug")
        title = item.get("name") or item.get("title") or item.get("dataset_name")
        if not title:
            continue
        page = item.get("url") or item.get("repository_url")
        if not page:
            page = "https://archive.ics.uci.edu/dataset/" + str(dataset_id or safe_slug(title))
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=title,
                id=str(dataset_id) if dataset_id is not None else None,
                url=page,
                description=compact_text(item.get("abstract") or item.get("description") or item.get("summary")),
                license=compact_text(item.get("license")),
                formats=uniq(as_list(item.get("data_format")) + as_list(item.get("format"))),
                tags=uniq(as_list(item.get("tasks")) + as_list(item.get("subject_area"))),
                access=source.access,
                size=compact_text(item.get("instances") or item.get("num_instances")),
                updated=compact_text(item.get("last_updated") or item.get("year")),
                confirmed=True,
                downloads={"commands": ["Use the UCI page or ucimlrepo package after verifying metadata."]},
                raw=safe_raw(item),
            )
        )
    return results


def search_zenodo(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    params = {"q": query, "size": limit, "type": "dataset", "sort": "bestmatch"}
    url = source.api_url + "?" + urllib.parse.urlencode(params)
    data = client.json(url)
    hits = ((data or {}).get("hits") or {}).get("hits") or []
    results: list[SearchResult] = []
    for item in hits[:limit]:
        meta = item.get("metadata") or {}
        files = item.get("files") or []
        file_urls = []
        formats = []
        for f in files[:10]:
            link = ((f.get("links") or {}).get("self") or (f.get("links") or {}).get("download"))
            if link:
                file_urls.append(link)
            key = f.get("key") or ""
            if "." in key:
                formats.append(key.rsplit(".", 1)[-1].upper())
        license_value = meta.get("license")
        if isinstance(license_value, dict):
            license_value = license_value.get("id") or license_value.get("title")
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=meta.get("title") or f"Zenodo record {item.get('id')}",
                id=str(item.get("id")) if item.get("id") else None,
                url=item.get("links", {}).get("html") or item.get("doi_url") or source_search_url(source, query),
                description=compact_text(meta.get("description")),
                license=compact_text(license_value, 120),
                formats=uniq(formats),
                tags=uniq(as_list(meta.get("keywords")) + as_list(meta.get("subjects"))),
                access=source.access,
                updated=item.get("updated") or meta.get("publication_date"),
                confirmed=True,
                downloads={"urls": file_urls, "doi": meta.get("doi")},
                raw=safe_raw({"id": item.get("id"), "metadata": meta, "files": files[:5]}),
            )
        )
    return results


def search_figshare(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    payload = {"search_for": query, "item_type": 3, "page_size": limit}
    data = client.json(source.api_url, method="POST", payload=payload)
    if not isinstance(data, list):
        return []
    results: list[SearchResult] = []
    for item in data[:limit]:
        article_id = item.get("id")
        details: dict[str, Any] = {}
        if article_id:
            try:
                details = client.json(f"https://api.figshare.com/v2/articles/{article_id}")
            except Exception:
                details = {}
        files = details.get("files") or []
        file_urls = [f.get("download_url") for f in files if f.get("download_url")]
        formats = []
        for f in files:
            name = f.get("name") or ""
            if "." in name:
                formats.append(name.rsplit(".", 1)[-1].upper())
        license_value = details.get("license")
        if isinstance(license_value, dict):
            license_value = license_value.get("name") or license_value.get("value")
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=item.get("title") or details.get("title") or f"Figshare article {article_id}",
                id=str(article_id) if article_id else None,
                url=item.get("url_public_html") or details.get("url_public_html") or source_search_url(source, query),
                description=compact_text(details.get("description")),
                license=compact_text(license_value, 120),
                formats=uniq(formats),
                tags=uniq(as_list(details.get("tags")) + as_list(item.get("tags"))),
                access=source.access,
                updated=item.get("published_date") or details.get("published_date") or item.get("modified_date"),
                confirmed=True,
                downloads={"urls": file_urls, "doi": details.get("doi") or item.get("doi")},
                raw=safe_raw({"search": item, "details": details}),
            )
        )
    return results


def search_ckan(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    url = source.api_url + "?" + urllib.parse.urlencode({"q": query, "rows": limit})
    data = client.json(url)
    packages = ((data or {}).get("result") or {}).get("results") or []
    results: list[SearchResult] = []
    for item in packages[:limit]:
        name = item.get("name") or item.get("id")
        title = item.get("title") or name
        resources = item.get("resources") or []
        formats = uniq([r.get("format") for r in resources])
        urls = [r.get("url") for r in resources if r.get("url")]
        page = item.get("url")
        if not page and name:
            page = source.homepage.rstrip("/") + "/" + name
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=title or "Untitled CKAN dataset",
                id=name,
                url=page or source_search_url(source, query),
                description=compact_text(item.get("notes") or item.get("description")),
                license=compact_text(item.get("license_title") or item.get("license_id")),
                formats=formats,
                tags=uniq([t.get("display_name") or t.get("name") for t in item.get("tags", []) if isinstance(t, dict)]),
                access=source.access,
                updated=item.get("metadata_modified") or item.get("metadata_created"),
                confirmed=True,
                downloads={"urls": urls[:20], "resource_count": len(resources)},
                raw=safe_raw(item),
            )
        )
    return results


def search_socrata(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    domain = source.search_context or "data.nasa.gov"
    params = {"search_context": domain, "search": query, "limit": limit}
    url = source.api_url + "?" + urllib.parse.urlencode(params)
    data = client.json(url)
    items = (data or {}).get("results") or []
    results: list[SearchResult] = []
    for item in items[:limit]:
        resource = item.get("resource") or {}
        meta = item.get("metadata") or {}
        link = (item.get("link") or resource.get("permalink") or resource.get("link"))
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=resource.get("name") or item.get("name") or "Untitled Socrata dataset",
                id=resource.get("id"),
                url=link or source_search_url(source, query),
                description=compact_text(resource.get("description")),
                license=compact_text(resource.get("license") or meta.get("license")),
                formats=uniq(as_list(resource.get("type")) + ["CSV", "JSON"] if resource.get("id") else []),
                tags=uniq(as_list(resource.get("tags"))),
                access=source.access,
                updated=resource.get("updatedAt") or resource.get("createdAt"),
                confirmed=True,
                downloads={
                    "urls": socrata_download_urls(domain, resource.get("id")),
                    "commands": ["Use Socrata API endpoints after checking schema."],
                },
                raw=safe_raw(item),
            )
        )
    return results


def socrata_download_urls(domain: str, dataset_id: str | None) -> list[str]:
    if not dataset_id:
        return []
    base = f"https://{domain}/resource/{dataset_id}"
    return [base + ".json", base + ".csv"]


def search_dataverse(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    params = {"q": query, "type": "dataset", "per_page": limit}
    url = source.api_url + "?" + urllib.parse.urlencode(params)
    data = client.json(url)
    items = ((data or {}).get("data") or {}).get("items") or []
    results: list[SearchResult] = []
    for item in items[:limit]:
        global_id = item.get("global_id") or item.get("identifier")
        authors = as_list(item.get("authors"))
        tags = uniq(as_list(item.get("subjects")) + [a.get("name") for a in authors if isinstance(a, dict)])
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=item.get("name") or item.get("title") or f"Dataverse dataset {global_id}",
                id=global_id,
                url=item.get("url") or source_search_url(source, query),
                description=compact_text(item.get("description") or item.get("description_plain")),
                license=compact_text(item.get("license") or item.get("license_name")),
                formats=[],
                tags=tags,
                access=source.access,
                updated=item.get("published_at") or item.get("updated_at"),
                confirmed=True,
                downloads={
                    "commands": ["Open the Dataverse record and inspect file-level terms before downloading files."],
                },
                raw=safe_raw(item),
            )
        )
    return results


def search_gbif(source: Source, query: str, limit: int, client: HttpClient) -> list[SearchResult]:
    params = {"q": query, "limit": limit}
    url = source.api_url + "?" + urllib.parse.urlencode(params)
    data = client.json(url)
    items = (data or {}).get("results") or []
    results: list[SearchResult] = []
    for item in items[:limit]:
        key = item.get("key")
        page = f"https://www.gbif.org/dataset/{key}" if key else source_search_url(source, query)
        results.append(
            SearchResult(
                source=source.id,
                source_name=source.name,
                title=item.get("title") or item.get("alias") or f"GBIF dataset {key}",
                id=str(key) if key else None,
                url=page,
                description=compact_text(item.get("description")),
                license=compact_text(item.get("license")),
                formats=uniq(as_list(item.get("type"))),
                tags=uniq(as_list(item.get("subtype")) + as_list(item.get("tags"))),
                access=source.access,
                updated=item.get("modified") or item.get("created"),
                confirmed=True,
                downloads={
                    "commands": ["Use GBIF occurrence/download APIs after checking citation, license, and filters."],
                },
                raw=safe_raw(item),
            )
        )
    return results


def fallback_result(source: Source, query: str) -> SearchResult:
    commands = []
    if source.id == "aws-open-data":
        commands = [
            "Inspect the registry page for S3 bucket, requester-pays status, region, and example AWS CLI/Spark access.",
            "Prefer aws s3 ls/cp, Athena, or Spark against the documented bucket instead of bulk download.",
        ]
    elif source.id == "google-cloud-public":
        commands = [
            "Open the dataset page and prefer BigQuery SQL or documented Cloud Storage paths.",
            "Use bq ls/bq query only after confirming project and billing requirements.",
        ]
    elif source.id == "databricks":
        commands = [
            "Open Databricks Marketplace, verify provider terms, then access through Marketplace or Delta Sharing.",
        ]
    elif source.id == "huggingface":
        commands = ["Use huggingface-cli download <repo-id> --repo-type dataset after selecting a repository."]
    elif source.id == "kaggle":
        commands = ["Use kaggle datasets download -d <owner/dataset> -p <dir> --unzip after selecting a dataset."]
    return SearchResult(
        source=source.id,
        source_name=source.name,
        title=f"Search {source.name} for: {query}",
        id=None,
        url=source_search_url(source, query),
        description=source.notes,
        license=None,
        formats=[],
        tags=list(source.categories),
        access=source.access,
        confirmed=False,
        downloads={"commands": commands} if commands else {},
    )


def safe_raw(value: Any, limit: int = 4000) -> dict[str, Any]:
    try:
        text = json.dumps(value, ensure_ascii=False, default=str)
    except TypeError:
        return {}
    if len(text) > limit:
        text = text[:limit]
    try:
        loaded = json.loads(text)
        return loaded if isinstance(loaded, dict) else {"value": loaded}
    except json.JSONDecodeError:
        return {"value": text}


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", text.strip()).strip("-")
    if not slug:
        slug = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return slug[:120]


def shell_quote(text: str) -> str:
    return "'" + text.replace("'", "'\\''") + "'"


def search_source(
    source: Source,
    query: str,
    limit: int,
    client: HttpClient,
    offline: bool,
) -> tuple[list[SearchResult], dict[str, Any]]:
    status = {"source": source.id, "name": source.name, "status": "ok", "adapter": source.adapter}
    if offline:
        status["status"] = "offline-fallback"
        return [fallback_result(source, query)], status
    try:
        if source.adapter == "huggingface":
            results = search_huggingface(source, query, limit, client)
        elif source.adapter == "kaggle":
            results = search_kaggle(source, query, limit)
        elif source.adapter == "openml":
            results = search_openml(source, query, limit, client)
        elif source.adapter == "uci":
            results = search_uci(source, query, limit, client)
        elif source.adapter == "zenodo":
            results = search_zenodo(source, query, limit, client)
        elif source.adapter == "figshare":
            results = search_figshare(source, query, limit, client)
        elif source.adapter == "ckan":
            results = search_ckan(source, query, limit, client)
        elif source.adapter == "socrata":
            results = search_socrata(source, query, limit, client)
        elif source.adapter == "dataverse":
            results = search_dataverse(source, query, limit, client)
        elif source.adapter == "gbif":
            results = search_gbif(source, query, limit, client)
        else:
            results = []
        if not results:
            status["status"] = "fallback"
            results = [fallback_result(source, query)]
        return results, status
    except Exception as exc:
        status["status"] = "error-fallback"
        status["error"] = compact_text(str(exc), 300)
        return [fallback_result(source, query)], status


def dedupe_results(results: list[SearchResult]) -> list[SearchResult]:
    seen: set[str] = set()
    out: list[SearchResult] = []
    for result in results:
        key = result.url or f"{result.source}:{result.id or result.title}"
        norm = key.lower().strip()
        if norm in seen:
            continue
        seen.add(norm)
        out.append(result)
    return out


def make_search_payload(args: argparse.Namespace) -> dict[str, Any]:
    brief = load_brief(args.brief)
    query = build_query(args, brief)
    sources = select_sources(args.source, args.profile, brief)
    client = HttpClient(args.timeout)
    all_results: list[SearchResult] = []
    statuses: list[dict[str, Any]] = []
    for source in sources:
        results, status = search_source(source, query, args.limit, client, args.offline)
        statuses.append(status)
        for result in results:
            all_results.append(score_result(result, query, args.profile, source))
    all_results = dedupe_results(all_results)
    all_results.sort(key=lambda r: (r.score, r.confirmed), reverse=True)
    return {
        "generated_at": utc_now(),
        "query": query,
        "profile": args.profile,
        "region": args.region,
        "brief": brief,
        "source_count": len(sources),
        "statuses": statuses,
        "results": [r.to_dict() for r in all_results],
    }


def print_markdown(payload: dict[str, Any], limit: int | None = None) -> None:
    results = payload.get("results", [])
    if limit is not None:
        results = results[:limit]
    print(f"# Dataset search results\n")
    print(f"- Query: `{payload.get('query')}`")
    print(f"- Profile: `{payload.get('profile')}`")
    print(f"- Generated: `{payload.get('generated_at')}`")
    print(f"- Sources searched: `{payload.get('source_count')}`\n")
    failures = [s for s in payload.get("statuses", []) if "error" in s]
    if failures:
        print("## Source warnings\n")
        for s in failures:
            print(f"- {s.get('source')}: {s.get('error')}")
        print()
    print("## Candidates\n")
    for i, item in enumerate(results, start=1):
        confirmed = "confirmed" if item.get("confirmed") else "fallback"
        print(f"### {i}. {item.get('title')} ({item.get('source_name')}, {confirmed}, score {item.get('score')})")
        print(f"- URL: {item.get('url')}")
        if item.get("id"):
            print(f"- ID: `{item.get('id')}`")
        if item.get("description"):
            print(f"- Description: {item.get('description')}")
        if item.get("license"):
            print(f"- License: {item.get('license')}")
        if item.get("formats"):
            print(f"- Formats: {', '.join(item.get('formats'))}")
        if item.get("access"):
            print(f"- Access: {item.get('access')}")
        if item.get("updated"):
            print(f"- Updated: {item.get('updated')}")
        if item.get("reasons"):
            print(f"- Why: {'; '.join(item.get('reasons'))}")
        downloads = item.get("downloads") or {}
        commands = downloads.get("commands") or []
        urls = downloads.get("urls") or []
        if commands:
            print("- Acquisition commands/guidance:")
            for command in commands[:4]:
                print(f"  - `{command}`" if command.startswith(("kaggle ", "huggingface-cli ")) else f"  - {command}")
        if urls:
            print("- Direct file/API URLs:")
            for url in urls[:5]:
                print(f"  - {url}")
        print()


def write_payload(payload: dict[str, Any], output: str | None, fmt: str) -> None:
    if fmt == "json":
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    else:
        from io import StringIO

        old = sys.stdout
        buf = StringIO()
        try:
            sys.stdout = buf
            print_markdown(payload)
            text = buf.getvalue()
        finally:
            sys.stdout = old
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def cmd_sources(args: argparse.Namespace) -> int:
    rows = []
    for source in SOURCES.values():
        rows.append(
            {
                "id": source.id,
                "name": source.name,
                "categories": list(source.categories),
                "homepage": source.homepage,
                "search_url": source.search_url,
                "access": source.access,
                "adapter": source.adapter,
                "notes": source.notes,
            }
        )
    if args.format == "json":
        print(json.dumps({"sources": rows, "profiles": PROFILES}, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print(f"{row['id']}: {row['name']} [{row['access']}]")
            print(f"  {row['notes']}")
            print(f"  {row['homepage']}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    payload = make_search_payload(args)
    write_payload(payload, args.output, args.format)
    return 0


def load_result_from_file(path: str, index: int) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    results = data.get("results")
    if not isinstance(results, list):
        raise SystemExit("Result file does not contain a results list")
    if index < 0 or index >= len(results):
        raise SystemExit(f"--index must be between 0 and {len(results) - 1}")
    return results[index]


def download_url(url: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    parsed = urllib.parse.urlparse(url)
    name = os.path.basename(parsed.path.rstrip("/")) or safe_slug(url)
    if "." not in name:
        name += ".data"
    target = output_dir / name
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        with open(target, "wb") as f:
            shutil.copyfileobj(resp, f)
    return target


def build_download_plan(result: dict[str, Any], output_dir: Path) -> list[dict[str, Any]]:
    source = result.get("source")
    result_id = result.get("id")
    downloads = result.get("downloads") or {}
    plan: list[dict[str, Any]] = []
    commands = downloads.get("commands") or []
    urls = downloads.get("urls") or []
    for command in commands:
        if isinstance(command, str) and command.startswith(("kaggle ", "huggingface-cli ")):
            command = command.replace("$OUTPUT_DIR", str(output_dir))
            plan.append({"type": "command", "command": command})
    for url in urls:
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            plan.append({"type": "url", "url": url})
    if not plan and source == "huggingface" and result_id:
        plan.append(
            {
                "type": "command",
                "command": f"huggingface-cli download {shell_quote(result_id)} --repo-type dataset --local-dir {shell_quote(str(output_dir / safe_slug(result_id)))}",
            }
        )
    if not plan and source == "kaggle" and result_id:
        plan.append(
            {
                "type": "command",
                "command": f"kaggle datasets download -d {shell_quote(result_id)} -p {shell_quote(str(output_dir / safe_slug(result_id)))} --unzip",
            }
        )
    return plan


def run_command(command: str) -> int:
    proc = subprocess.run(shlex.split(command), text=True)
    return proc.returncode


def cmd_download(args: argparse.Namespace) -> int:
    if args.from_results:
        result = load_result_from_file(args.from_results, args.index)
    else:
        if not args.url and not (args.source and args.id):
            raise SystemExit("Provide --from-results, --url, or --source plus --id")
        source = SOURCES.get(args.source) if args.source else None
        result = {
            "source": args.source,
            "source_name": source.name if source else args.source,
            "id": args.id,
            "url": args.url,
            "downloads": {"urls": [args.url] if args.url else []},
        }
        if args.source == "huggingface" and args.id:
            result["downloads"] = {
                "commands": [
                    f"huggingface-cli download {shell_quote(args.id)} --repo-type dataset --local-dir \"$OUTPUT_DIR/{safe_slug(args.id)}\""
                ]
            }
        if args.source == "kaggle" and args.id:
            result["downloads"] = {
                "commands": [f"kaggle datasets download -d {shell_quote(args.id)} -p \"$OUTPUT_DIR/{safe_slug(args.id)}\" --unzip"]
            }

    output_dir = Path(args.output_dir).expanduser().resolve()
    plan = build_download_plan(result, output_dir)
    if not plan:
        print(json.dumps({"status": "no_download_plan", "result": result}, ensure_ascii=False, indent=2))
        return 2

    if not args.yes:
        print(json.dumps({"status": "dry_run", "output_dir": str(output_dir), "plan": plan}, ensure_ascii=False, indent=2))
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    executed: list[dict[str, Any]] = []
    for step in plan:
        if step["type"] == "url":
            target = download_url(step["url"], output_dir)
            executed.append({"type": "url", "url": step["url"], "target": str(target), "status": "ok"})
        elif step["type"] == "command":
            rc = run_command(step["command"])
            executed.append({"type": "command", "command": step["command"], "returncode": rc})
            if rc != 0:
                print(json.dumps({"status": "command_failed", "executed": executed}, ensure_ascii=False, indent=2))
                return rc
    print(json.dumps({"status": "ok", "output_dir": str(output_dir), "executed": executed}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search and obtain datasets/data lakes from public catalogs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              dataset_search.py sources
              dataset_search.py search "Brazil census income municipality" --profile brazil --format markdown
              dataset_search.py search "instruction tuning portuguese" --profile nlp --source huggingface,zenodo
              dataset_search.py download --from-results /tmp/dataset-results.json --index 0 --output-dir /tmp/datasets
            """
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_sources = sub.add_parser("sources", help="List known dataset sources and profiles.")
    p_sources.add_argument("--format", choices=("text", "json"), default="text")
    p_sources.set_defaults(func=cmd_sources)

    p_search = sub.add_parser("search", help="Search for datasets.")
    p_search.add_argument("query", nargs="?", help="Natural language dataset query.")
    p_search.add_argument("--brief", help="Optional JSON brief with structured dataset requirements.")
    p_search.add_argument("--profile", choices=sorted(PROFILES), default="general")
    p_search.add_argument("--region", help="Geographic/language hint such as BR, EU, US, Ceara, Portuguese.")
    p_search.add_argument("--source", default="all", help="Comma-separated source ids or all.")
    p_search.add_argument("--limit", type=int, default=5, help="Per-source limit for direct adapters.")
    p_search.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    p_search.add_argument("--offline", action="store_true", help="Do not call APIs or CLIs; emit search links only.")
    p_search.add_argument("--format", choices=("json", "markdown"), default="json")
    p_search.add_argument("--output", help="Write output to file.")
    p_search.set_defaults(func=cmd_search)

    p_download = sub.add_parser("download", help="Create or execute an acquisition plan for a selected result.")
    p_download.add_argument("--from-results", help="JSON output from the search command.")
    p_download.add_argument("--index", type=int, default=0, help="Zero-based result index in --from-results.")
    p_download.add_argument("--source", choices=sorted(SOURCES), help="Source id for direct source/id download.")
    p_download.add_argument("--id", help="Dataset id, such as owner/name for Kaggle or repo-id for Hugging Face.")
    p_download.add_argument("--url", help="Direct file/API URL to download.")
    p_download.add_argument("--output-dir", default="/tmp/openclaw-datasets")
    p_download.add_argument("--yes", action="store_true", help="Execute downloads/commands. Without this, dry-run only.")
    p_download.set_defaults(func=cmd_download)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
