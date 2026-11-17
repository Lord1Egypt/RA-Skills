#!/usr/bin/env python3
"""Validate source-bound entity facts and convert existing data; no network or prose generation."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit


FACTS = {"canonical_name", "name_zh", "name_en", "aliases", "description", "website", "founding_date"}
TYPES = {"Organization", "Brand", "Product", "SoftwareApplication"}
RELATIONS = {
    "developed_by": ("SoftwareApplication", "Organization"),
    "manufactured_by": ("Product", "Organization"),
    "brand_of": ("Brand", "Organization"),
    "parent_organization": ("Organization", "Organization"),
}


class InvalidProfile(ValueError):
    def __init__(self, code, path, message):
        self.issue = {"code": code, "path": path, "message": message}
        super().__init__(message)


def require(condition, code, path, message):
    if not condition:
        raise InvalidProfile(code, path, message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def record(value, fields, path):
    require(isinstance(value, dict), "type", path, "Expected an object")
    missing = sorted(set(fields) - value.keys())
    require(not missing, "missing_field", path, "Missing fields: " + ", ".join(missing))


def sequence(value, path):
    require(isinstance(value, list), "type", path, "Expected an array")


def text_field(value, path):
    require(nonempty(value), "type", path, "Expected a non-empty string")


def iso_date(value, path):
    try:
        valid = isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        valid = False
    require(valid, "date", path, "Expected a real date in YYYY-MM-DD format")


def http_url(value, path):
    try:
        parsed = urlsplit(value) if isinstance(value, str) else None
        valid = (parsed is not None and parsed.scheme in {"http", "https"}
                 and bool(parsed.hostname) and parsed.username is None
                 and parsed.password is None and not re.search(r"\s", value))
        if parsed is not None:
            parsed.port  # Reject invalid ports as well as malformed host syntax.
    except ValueError:
        valid = False
    require(valid, "url", path, "Expected an HTTP(S) URL without credentials or whitespace")


def url_identity(value):
    parsed = urlsplit(value)
    port = parsed.port
    port_part = "" if port in (None, 80, 443) else ":" + str(port)
    return (parsed.hostname.lower() + port_part, parsed.path.rstrip("/"), parsed.query)


def founding_date(value, path):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}(-\d{2}){0,2}", value) is not None,
            "founding_date", path, "Expected YYYY, YYYY-MM or YYYY-MM-DD")
    iso_date(value + {4: "-01-01", 7: "-01", 10: ""}[len(value)], path)


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_key", "$", "Duplicate JSON key: " + key)
        result[key] = value
    return result


def load_profile(path):
    try:
        def invalid_constant(value):
            raise ValueError("Non-JSON numeric value: " + value)
        return json.loads(Path(path).read_text(encoding="utf-8"),
                          object_pairs_hook=no_duplicate_keys, parse_constant=invalid_constant)
    except InvalidProfile:
        raise
    except (OSError, UnicodeError, ValueError) as exc:
        raise InvalidProfile("input", "$", str(exc)) from exc


class Validator:
    def __init__(self, profile):
        self.profile = profile
        self.entities = {}
        self.sources = {}
        self.fact_states = Counter()

    def evidence(self, items, path, subjects=(), allow_ai=False):
        sequence(items, path)
        require(bool(items), "evidence_required", path, "A non-empty evidence list is required")
        for i, item in enumerate(items):
            p = f"{path}[{i}]"
            record(item, {"source_id", "quote"}, p)
            sid = item["source_id"]
            require(isinstance(sid, str) and sid in self.sources, "source_missing", p, "Unknown source_id")
            source = self.sources[sid]
            text_field(item["quote"], p + ".quote")
            require(item["quote"] in source["excerpt"], "quote_not_found", p, "Quote is not in the captured excerpt")
            require(set(subjects) <= set(source["subject_entity_ids"]), "source_subject", p,
                    "Source does not cover the referenced entity or relationship")
            require(allow_ai or source["kind"] != "ai_response", "ai_as_fact", p,
                    "An AI answer is not a primary source for entity facts")

    def typed_value(self, key, value, path, entity_type):
        if key == "aliases":
            sequence(value, path)
            require(all(nonempty(x) for x in value), "type", path, "Aliases must be non-empty strings")
            require(len(set(value)) == len(value), "duplicate_alias", path, "Duplicate aliases")
        elif key in FACTS:
            text_field(value, path)
            if key == "website":
                http_url(value, path)
            elif key == "founding_date":
                require(entity_type == "Organization", "date_subject", path,
                        "A product release date is not an organization founding date")
                founding_date(value, path)
        else:
            require(value is not None and value != "", "empty_value", path, "Known facts need a value")

    def fact(self, value, path, entity_id, key, entity_type):
        record(value, {"status", "value", "evidence"}, path)
        status = value["status"]
        require(status in ("supported", "reported", "unknown", "conflicting"), "fact_status", path,
                "Invalid fact status")
        self.fact_states[status] += 1
        if status in ("supported", "reported"):
            self.typed_value(key, value["value"], path + ".value", entity_type)
            self.evidence(value["evidence"], path + ".evidence", (entity_id,))
            if status == "reported":
                require(any(self.sources[e["source_id"]]["kind"] == "user_material" for e in value["evidence"]),
                        "reported_source", path, "Reported facts need user-material provenance")
            require(not value.get("alternatives"), "stale_alternatives", path, "Resolved facts cannot retain conflicting alternatives here")
        else:
            require(value["value"] is None and value["evidence"] == [], "unknown_value", path,
                    "Unknown/conflicting facts must have null value and empty top-level evidence")
            text_field(value.get("reason"), path + ".reason")
            if status == "unknown":
                require(not value.get("alternatives"), "unknown_alternatives", path, "Use conflicting for multiple candidates")
            else:
                alts = value.get("alternatives")
                sequence(alts, path + ".alternatives")
                require(len(alts) >= 2, "conflict_alternatives", path, "Keep at least two sourced candidate values")
                unique = set()
                for i, alt in enumerate(alts):
                    p = f"{path}.alternatives[{i}]"
                    record(alt, {"value", "evidence"}, p)
                    self.typed_value(key, alt["value"], p + ".value", entity_type)
                    self.evidence(alt["evidence"], p + ".evidence", (entity_id,))
                    unique.add(json.dumps(alt["value"], ensure_ascii=False, sort_keys=True))
                require(len(unique) >= 2, "conflict_alternatives", path, "Conflicting candidates must differ")

    def validate(self):
        p = self.profile
        record(p, {"schema_version", "data_mode", "profile_id", "as_of", "primary_entity_id", "sources",
                   "entities", "relationships", "disambiguation", "observations"}, "$")
        require(p["schema_version"] == "1.0", "version", "$.schema_version", "Unsupported contract version")
        require(p["data_mode"] in ("real", "illustrative"), "data_mode", "$.data_mode", "Set real or illustrative")
        text_field(p["profile_id"], "$.profile_id")
        iso_date(p["as_of"], "$.as_of")
        for key in ("entities", "sources", "relationships", "disambiguation", "observations"):
            sequence(p[key], "$." + key)
        require(bool(p["entities"]), "no_entities", "$.entities", "At least one separate entity is required")
        for i, e in enumerate(p["entities"]):
            path = f"$.entities[{i}]"
            record(e, {"id", "type", "facts", "same_as"}, path)
            text_field(e["id"], path + ".id")
            require(re.fullmatch(r"[a-z0-9][a-z0-9_-]*", e["id"]) is not None, "entity_id", path, "Use a stable ASCII entity ID")
            require(e["id"] not in self.entities, "duplicate_entity", path, "Duplicate entity ID; do not merge by name")
            require(isinstance(e["type"], str) and e["type"] in TYPES, "entity_type", path, "Unsupported entity type")
            self.entities[e["id"]] = e
        require(isinstance(p["primary_entity_id"], str) and p["primary_entity_id"] in self.entities,
                "primary_entity", "$.primary_entity_id", "Primary entity must exist")
        for i, source in enumerate(p["sources"]):
            path = f"$.sources[{i}]"
            record(source, {"id", "kind", "locator", "acquisition", "captured_on", "subject_entity_ids", "excerpt"}, path)
            text_field(source["id"], path + ".id")
            require(source["id"] not in self.sources, "duplicate_source", path, "Duplicate source ID")
            require(source["kind"] in ("official_site", "user_material", "third_party", "ai_response"), "source_kind", path, "Invalid source kind")
            require(source["acquisition"] in ("retrieved", "user_supplied"), "acquisition", path, "Invalid acquisition method")
            text_field(source["locator"], path + ".locator")
            if not source["locator"].startswith("provided:"):
                http_url(source["locator"], path + ".locator")
            else:
                require(bool(source["locator"][9:].strip()), "locator", path, "Name the provided material")
            iso_date(source["captured_on"], path + ".captured_on")
            require(source["captured_on"] <= p["as_of"], "future_source", path, "Source date is after the profile cutoff")
            sequence(source["subject_entity_ids"], path + ".subject_entity_ids")
            require(bool(source["subject_entity_ids"]) and all(isinstance(e, str) and e in self.entities for e in source["subject_entity_ids"]),
                    "source_subject", path, "Source subjects must reference known entities")
            text_field(source["excerpt"], path + ".excerpt")
            if source["kind"] == "ai_response":
                record(source, {"platform", "query", "citation_capture", "native_citations"}, path)
                text_field(source["platform"], path + ".platform")
                text_field(source["query"], path + ".query")
                require(source["citation_capture"] in ("complete", "not_captured"), "citation_capture", path, "Invalid source citation capture status")
                if source["citation_capture"] == "complete":
                    sequence(source["native_citations"], path + ".native_citations")
                    for url in source["native_citations"]:
                        http_url(url, path + ".native_citations")
                    require(len(set(source["native_citations"])) == len(source["native_citations"]), "duplicate_citation", path, "Duplicate source citations")
                else:
                    require(source["native_citations"] is None, "uncaptured_citations", path, "Uncaptured source citations must be null")
            self.sources[source["id"]] = source
        for i, e in enumerate(p["entities"]):
            path = f"$.entities[{i}]"
            record(e["facts"], FACTS, path + ".facts")
            require(not (e["facts"].keys() - FACTS), "unknown_fact_key", path, "Put extra facts under attributes")
            for key, fact in e["facts"].items():
                self.fact(fact, path + ".facts." + key, e["id"], key, e["type"])
            attributes = e.get("attributes", {})
            record(attributes, set(), path + ".attributes")
            require(not (attributes.keys() & FACTS), "attribute_shadow", path, "Attributes cannot override core facts")
            for key, fact in attributes.items():
                text_field(key, path + ".attributes")
                self.fact(fact, path + ".attributes." + key, e["id"], key, e["type"])
            sequence(e["same_as"], path + ".same_as")
        excluded = {}
        for i, d in enumerate(p["disambiguation"]):
            path = f"$.disambiguation[{i}]"
            record(d, {"entity_id", "candidate_name", "candidate_url", "resolution", "reason", "evidence"}, path)
            self.entity_ref(d["entity_id"], path)
            text_field(d["candidate_name"], path + ".candidate_name")
            http_url(d["candidate_url"], path + ".candidate_url")
            require(d["resolution"] in ("distinct", "unresolved"), "resolution", path, "Candidate must remain distinct or unresolved")
            text_field(d["reason"], path + ".reason")
            self.evidence(d["evidence"], path + ".evidence", (d["entity_id"],))
            excluded.setdefault(d["entity_id"], set()).add(url_identity(d["candidate_url"]))
        sites = {}
        for eid, e in self.entities.items():
            site = e["facts"]["website"]
            if site["status"] in ("supported", "reported"):
                sites[eid] = url_identity(site["value"])
                require(sites[eid] not in excluded.get(eid, set()), "candidate_as_website", eid, "A disambiguation candidate cannot be the canonical website")
        for i, e in enumerate(p["entities"]):
            seen_urls = set()
            for j, item in enumerate(e["same_as"]):
                path = f"$.entities[{i}].same_as[{j}]"
                record(item, {"url", "entity_id", "status", "evidence"}, path)
                require(item["entity_id"] == e["id"], "same_as_subject", path, "sameAs must identify this entity, not a related entity")
                require(item["status"] == "supported", "same_as_status", path, "Unverified identity links belong in the pending list")
                http_url(item["url"], path + ".url")
                key = url_identity(item["url"])
                require(key not in seen_urls, "same_as_duplicate", path, "Duplicate identity URL")
                seen_urls.add(key)
                require(not any(other != e["id"] and other_site == key for other, other_site in sites.items()),
                        "same_as_cross_entity", path, "A related entity's website is not sameAs")
                require(key not in excluded.get(e["id"], set()), "same_as_candidate", path, "A distinct/unresolved candidate is not sameAs")
                self.evidence(item["evidence"], path + ".evidence", (e["id"],))
        for i, relation in enumerate(p["relationships"]):
            path = f"$.relationships[{i}]"
            record(relation, {"subject_id", "predicate", "object_id", "status", "evidence"}, path)
            a, b = relation["subject_id"], relation["object_id"]
            self.entity_ref(a, path)
            self.entity_ref(b, path)
            require(a != b, "self_relation", path, "Relationship endpoints must be separate entities")
            predicate = relation["predicate"]
            require(isinstance(predicate, str) and predicate in RELATIONS, "relation_type", path, "Unsupported relationship")
            require((self.entities[a]["type"], self.entities[b]["type"]) == RELATIONS[predicate],
                    "relation_direction", path, "Wrong entity types or relationship direction")
            require(relation["status"] in ("supported", "reported"), "relation_status", path, "Keep uncertain relationships in the pending list")
            self.evidence(relation["evidence"], path + ".evidence", (a, b))
        seen_observations = set()
        for i, obs in enumerate(p["observations"]):
            self.observation(obs, f"$.observations[{i}]", seen_observations)
        return {"ok": True, "profile_id": p["profile_id"], "data_mode": p["data_mode"],
                "entity_count": len(self.entities), "relationship_count": len(p["relationships"]),
                "fact_status_counts": dict(sorted(self.fact_states.items()))}

    def entity_ref(self, value, path):
        require(isinstance(value, str) and value in self.entities, "entity_reference", path, "Unknown entity reference")

    def observation(self, obs, path, seen):
        record(obs, {"id", "entity_id", "platform", "query", "status", "observed_on", "source_id", "answer",
                     "mentioned", "citation_capture", "native_citations", "error"}, path)
        self.entity_ref(obs["entity_id"], path)
        for key in ("id", "platform", "query"):
            text_field(obs[key], path + "." + key)
        require(obs["id"] not in seen, "duplicate_observation", path, "Observation IDs must be unique")
        seen.add(obs["id"])
        status = obs["status"]
        require(status in ("observed", "not_run", "query_failed", "simulated"), "observation_status", path, "Invalid observation status")
        if status == "observed":
            iso_date(obs["observed_on"], path + ".observed_on")
            require(obs["observed_on"] <= self.profile["as_of"], "future_observation", path, "Observation is after profile cutoff")
            text_field(obs["answer"], path + ".answer")
            sid = obs["source_id"]
            require(isinstance(sid, str) and sid in self.sources, "observation_source", path, "A captured response source is required")
            source = self.sources[sid]
            require(source["kind"] == "ai_response" and obs["answer"] in source["excerpt"]
                    and source["captured_on"] == obs["observed_on"]
                    and obs["entity_id"] in source["subject_entity_ids"]
                    and source["platform"] == obs["platform"] and source["query"] == obs["query"],
                    "observation_source", path, "Answer, date, entity, platform and query must match the captured AI response")
            require(isinstance(obs["mentioned"], bool), "observation_mention", path, "Record a boolean only after reading the response")
            require(obs["error"] is None, "observation_error", path, "Observed responses have null error")
            require(obs["citation_capture"] in ("complete", "not_captured"), "citation_capture", path, "Invalid capture status")
            if obs["citation_capture"] == "complete":
                sequence(obs["native_citations"], path + ".native_citations")
                for url in obs["native_citations"]:
                    http_url(url, path + ".native_citations")
                require(len(set(obs["native_citations"])) == len(obs["native_citations"]), "duplicate_citation", path, "Deduplicate citation URLs within each answer")
            else:
                require(obs["native_citations"] is None, "uncaptured_citations", path, "Uncaptured citations are null, not zero")
            require(obs["citation_capture"] == source["citation_capture"]
                    and obs["native_citations"] == source["native_citations"], "citation_source_mismatch", path,
                    "Native citations must match the captured response metadata")
        else:
            require(all(obs[key] is None for key in ("observed_on", "source_id", "mentioned", "native_citations"))
                    and obs["citation_capture"] == "not_captured", "unmeasured_metrics", path,
                    "Unrun, failed or simulated records cannot contain measured metrics")
            if status == "simulated":
                require(obs["answer"] is None or nonempty(obs["answer"]), "simulation_answer", path, "Simulation answer is text or null")
            else:
                require(obs["answer"] is None, "unmeasured_answer", path, "Unrun/failed records cannot carry an answer")
            if status == "query_failed":
                text_field(obs["error"], path + ".error")
            else:
                require(obs["error"] is None, "observation_error", path, "Only failed queries carry an error")


def validate(profile):
    return Validator(profile).validate()


def schema_graph(profile):
    validate(profile)
    eligible = {}
    for entity in profile["entities"]:
        facts = entity["facts"]
        if all(facts[k]["status"] == "supported" for k in ("canonical_name", "website")):
            parsed = urlsplit(facts["website"]["value"])
            base = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
            eligible[entity["id"]] = base + "#entity-" + entity["id"]
    require(profile["primary_entity_id"] in eligible, "schema_identity_unverified", "$.primary_entity_id",
            "Schema needs a supported canonical name and website for the primary entity")
    nodes = {}
    for entity in profile["entities"]:
        eid = entity["id"]
        if eid not in eligible:
            continue
        facts = entity["facts"]
        node = {"@id": eligible[eid], "@type": entity["type"], "name": facts["canonical_name"]["value"], "url": facts["website"]["value"]}
        for key, target in (("description", "description"), ("founding_date", "foundingDate")):
            if facts[key]["status"] == "supported":
                node[target] = facts[key]["value"]
        aliases = list(facts["aliases"]["value"]) if facts["aliases"]["status"] == "supported" else []
        aliases.extend(facts[k]["value"] for k in ("name_zh", "name_en") if facts[k]["status"] == "supported")
        aliases = list(dict.fromkeys(a for a in aliases if a != node["name"]))
        if aliases:
            node["alternateName"] = aliases
        if entity["same_as"]:
            node["sameAs"] = [item["url"] for item in entity["same_as"]]
        nodes[eid] = node
    for relation in profile["relationships"]:
        a, b = relation["subject_id"], relation["object_id"]
        if relation["status"] != "supported" or a not in nodes or b not in nodes:
            continue
        predicate = relation["predicate"]
        if predicate == "brand_of":
            a, b, target = b, a, "brand"
        else:
            target = {"developed_by": "creator", "manufactured_by": "manufacturer", "parent_organization": "parentOrganization"}[predicate]
        reference = {"@id": eligible[b]}
        if reference not in nodes[a].setdefault(target, []):
            nodes[a][target].append(reference)
    return {"@context": "https://schema.org", "@graph": list(nodes.values())}


def summarize(profile):
    validation = validate(profile)
    counts = Counter(obs["status"] for obs in profile["observations"])
    observed = [o for o in profile["observations"] if o["status"] == "observed"]
    captured = [o for o in observed if o["citation_capture"] == "complete"]
    mentions = sum(o["mentioned"] for o in observed) if observed else None
    return {"profile_id": validation["profile_id"], "data_mode": profile["data_mode"],
            "usable_as_live_measurement": profile["data_mode"] == "real" and bool(observed),
            "status_counts": {status: counts[status] for status in ("observed", "not_run", "query_failed", "simulated")},
            "observed_samples": len(observed), "mentioned_count": mentions,
            "mention_rate": mentions / len(observed) if observed else None,
            "citation_complete_samples": len(captured), "citation_uncaptured_samples": len(observed) - len(captured),
            "native_citation_count": sum(len(o["native_citations"]) for o in captured) if captured else None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "schema", "summarize"))
    parser.add_argument("profile", help="Path to an entity profile JSON file")
    args = parser.parse_args(argv)
    try:
        profile = load_profile(args.profile)
        result = {"validate": validate, "schema": schema_graph, "summarize": summarize}[args.command](profile)
    except InvalidProfile as exc:
        print(json.dumps({"ok": False, "errors": [exc.issue]}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
