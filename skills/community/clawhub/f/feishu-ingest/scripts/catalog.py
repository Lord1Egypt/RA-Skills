import json

from utils import now, unique


LABELS = {
    "overview": "Overview",
    "project": "Projects",
    "projects": "Projects",
    "paper": "Papers",
    "papers": "Papers",
    "survey": "Surveys",
    "surveys": "Surveys",
    "code": "Code",
    "codebase": "Code",
    "meeting": "Meetings",
    "meetings": "Meetings",
    "experiment": "Experiments",
    "experiments": "Experiments",
    "doc": "Tech Notes",
    "tech-note": "Tech Notes",
    "tech-notes": "Tech Notes",
    "note": "Notes",
    "notes": "Notes",
    "concept": "Concepts",
    "concepts": "Concepts",
    "resource": "Resources",
    "resources": "Resources",
    "qa": "Q&A",
}
RELATION_ROOTS = {"overview", "projects", "papers", "surveys", "code", "meetings", "experiments", "tech-notes", "notes", "concepts", "resources", "qa"}


def catalog_from_raw(raw):
    try:
        data = json.loads(raw) if raw else {"version": 1, "pages": []}
        if not isinstance(data.get("pages"), list):
            data["pages"] = []
        return data
    except json.JSONDecodeError:
        return {"version": 1, "pages": []}


def page_type_from_path(path):
    folder = str(path or "").split("/", 1)[0]
    if folder == "concepts":
        return "concept"
    if folder == "resources":
        return "resource"
    if folder == "notes":
        return "note"
    if folder == "code":
        return "code"
    return folder or "wiki"


def catalog_entry(page):
    return {
        "path": page.get("path"),
        "title": page.get("title"),
        "type": page.get("type") or page_type_from_path(page.get("path")),
        "kbType": page.get("kbType") or page.get("kb_type") or "wiki",
        "sourceIds": unique(page.get("sourceIds") or []),
        "updatedAt": now(),
        "keywords": unique(page.get("keywords") or []),
        "projectIds": unique(page.get("projectIds") or ["general"]),
        "relatedConcepts": normalize_relation_paths(page.get("relatedConcepts") or []),
        "relatedResources": normalize_relation_paths(page.get("relatedResources") or []),
        "relatedCodePages": normalize_relation_paths(page.get("relatedCodePages") or []),
        "relatedPages": normalize_relation_paths(page.get("relatedPages") or []),
        "contentHash": page.get("contentHash") or "",
        "sourceStatus": page.get("sourceStatus") or "active",
    }


def merge_catalog(catalog, entries):
    pages_by_path = {}
    for item in catalog.get("pages") or []:
        path = item.get("path")
        if path:
            pages_by_path[path] = dict(item)
    for entry in entries:
        path = entry.get("path")
        if not path:
            continue
        old = pages_by_path.get(path, {})
        merged = dict(old)
        merged.update({key: value for key, value in entry.items() if value not in (None, "")})
        for key in ["sourceIds", "projectIds", "keywords", "relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            merged[key] = unique((old.get(key) or []) + (entry.get(key) or []))
        pages_by_path[path] = merged
    catalog["version"] = catalog.get("version") or 1
    catalog["updatedAt"] = now()
    catalog["pages"] = sorted(normalize_graph(list(pages_by_path.values())), key=lambda item: item.get("path") or "")
    return catalog


def normalize_graph(pages):
    by_path = {page.get("path"): dict(page) for page in pages if page.get("path")}
    for page in list(by_path.values()):
        path = page.get("path")
        for key in ["relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            page[key] = normalize_relation_paths(page.get(key) or [])
        page_type = page.get("type") or page_type_from_path(path)
        if page_type == "code":
            for concept_path in page.get("relatedConcepts") or []:
                if concept_path in by_path:
                    by_path[concept_path]["relatedCodePages"] = unique((by_path[concept_path].get("relatedCodePages") or []) + [path])
            for resource_path in page.get("relatedResources") or []:
                if resource_path in by_path:
                    by_path[resource_path]["relatedCodePages"] = unique((by_path[resource_path].get("relatedCodePages") or []) + [path])
        for resource_path in page.get("relatedResources") or []:
            if resource_path in by_path and page_type == "concept":
                by_path[resource_path]["relatedConcepts"] = unique((by_path[resource_path].get("relatedConcepts") or []) + [path])
        for concept_path in page.get("relatedConcepts") or []:
            if concept_path in by_path and page_type == "resource":
                by_path[concept_path]["relatedResources"] = unique((by_path[concept_path].get("relatedResources") or []) + [path])
        for related_path in page.get("relatedPages") or []:
            if related_path in by_path:
                by_path[related_path]["relatedPages"] = unique((by_path[related_path].get("relatedPages") or []) + [path])
    return list(by_path.values())


def normalize_relation_paths(values):
    result = []
    for raw in values or []:
        value = raw
        if isinstance(raw, dict):
            value = raw.get("path") or raw.get("target") or raw.get("href") or ""
        if not isinstance(value, str):
            continue
        value = value.strip()
        if value.startswith("[[") and "]]" in value:
            value = value[2:value.find("]]")]
        if "|" in value:
            value = value.split("|", 1)[0].strip()
        if not value:
            continue
        value = value.replace("\\", "/").strip("/")
        if not value.endswith(".md"):
            value = value.rstrip("/") + ".md"
        if value.startswith("../") or "/../" in value or value == "..":
            continue
        root = value.split("/", 1)[0]
        if root not in RELATION_ROOTS or value.startswith("source_files/") or "/" not in value:
            continue
        result.append(value)
    return unique(result)


def render_index(catalog):
    groups = {}
    for page in catalog.get("pages") or []:
        path = page.get("path") or ""
        page_type = page.get("type") or page_type_from_path(path)
        label = LABELS.get(page_type, LABELS.get(path.split("/", 1)[0], page_type))
        groups.setdefault(label, []).append(page)

    lines = ["# Knowledge Base Index", "", f"Updated at: {catalog.get('updatedAt') or now()}", ""]
    for label in sorted(groups):
        lines.extend([f"## {label}", ""])
        for page in sorted(groups[label], key=lambda item: item.get("title") or item.get("path") or ""):
            title = page.get("title") or page.get("path")
            path = page.get("path") or ""
            keywords = page.get("keywords") or []
            suffix = f" - {', '.join(keywords[:5])}" if keywords else ""
            lines.append(f"- [{title}]({path}){suffix}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
