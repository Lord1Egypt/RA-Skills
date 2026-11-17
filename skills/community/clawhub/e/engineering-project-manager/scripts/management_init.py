#!/usr/bin/env python3
"""Explicit, idempotent opt-in for management registries; never migrate records."""

import argparse
import importlib
from pathlib import Path
import sys

from management_audit import MARKER, MODELS, marker_errors
from management_common import RecordError, Store, project_file, require_text
from pm_common import write_json_atomic


def initialize(project, actor):
    actor = require_text(actor, "actor")
    project = Path(project).resolve()
    errors, enabled = marker_errors(project)
    if errors:
        raise RecordError("; ".join(errors))
    stores = [(Store(project, relative, kind, prefix), module)
              for kind, relative, prefix, module in MODELS]
    # Validate existing data before enabling anything else. Subsequent failures
    # leave completed individual stores intact; rerun explicitly to resume.
    for store, module in stores:
        if store.exists():
            data = store.read()
            errors = importlib.import_module(module).validate_registry(project, data)
            if errors:
                raise RecordError("; ".join(errors))
        elif enabled:
            raise RecordError("An enabled management registry is missing; restore it first")
    for store, module_name in stores:
        data = store.initialize(actor)
        importlib.import_module(module_name).render(project, data)
    if not enabled:
        write_json_atomic(project_file(project, MARKER, must_exist=False),
                          {"schema_version": 1, "enabled": True, "registries": [m[0] for m in MODELS]})
    return {"enabled": [m[0] for m in MODELS], "records_preserved": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--actor", required=True)
    args = parser.parse_args(argv)
    try:
        initialize(args.project, args.actor)
        print("MANAGEMENT INITIALIZATION: PASS (existing records preserved)")
        return 0
    except (RecordError, OSError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
