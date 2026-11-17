"""Static verifier policy constants; no execution behavior lives here."""

SEVERE_STATUSES = {
    "parser_error",
    "identifier_hijacking",
    "shifted_identifier",
    "total_fabrication",
    "placeholder_generation",
    "unresolved",
}
PROBLEM_STATUSES = SEVERE_STATUSES | {
    "partial_attribute_corruption",
    "minor_fix",
    "minor_format_error",
    "verified_identifier_only",
}
TITLE_RECOVERY_STATUSES = {
    "identifier_hijacking",
    "shifted_identifier",
    "partial_attribute_corruption",
    "unresolved",
    "placeholder_generation",
}

CROSSREF_POLITE_RATE_PER_SECOND = 10.0
CROSSREF_POLITE_CONCURRENCY = 3
CROSSREF_PUBLIC_RATE_PER_SECOND = 5.0
CROSSREF_PUBLIC_CONCURRENCY = 1
NCBI_DEFAULT_RATE_PER_SECOND = 3.0
NCBI_API_KEY_RATE_PER_SECOND = 10.0
OPENALEX_DEFAULT_RATE_PER_SECOND = 5.0
OPENALEX_DEFAULT_CONCURRENCY = 2
