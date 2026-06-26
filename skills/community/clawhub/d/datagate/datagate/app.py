"""
DataGate API — FastAPI application.

Single endpoint: POST /v1/validate
Accepts a JSON Schema and payload, returns validation report.
"""

import jsonschema
from fastapi import FastAPI

from .models import ValidateRequest, ValidateResponse, ValidationError

app = FastAPI(
    title="DataGate API",
    description="Stateless JSON Schema validation for AI agent pipelines.",
    version="0.1.0",
)


@app.post("/v1/validate", response_model=ValidateResponse)
async def validate(request: ValidateRequest) -> ValidateResponse:
    """Validate a payload against a JSON Schema."""
    errors: list[ValidationError] = []

    try:
        validator_cls = jsonschema.validators.validator_for(request.json_schema)
        validator_cls.check_schema(request.json_schema)
    except jsonschema.SchemaError as e:
        errors.append(
            ValidationError(path="$schema", message=f"Invalid schema: {e.message}")
        )
        return ValidateResponse(valid=False, error_count=len(errors), errors=errors)

    validator = jsonschema.Draft202012Validator(request.json_schema)

    for error in sorted(validator.iter_errors(request.payload), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path) or "$"
        errors.append(ValidationError(path=path, message=error.message))

    return ValidateResponse(
        valid=len(errors) == 0,
        error_count=len(errors),
        errors=errors,
    )
