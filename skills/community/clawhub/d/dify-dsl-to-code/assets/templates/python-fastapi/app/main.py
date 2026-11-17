"""FastAPI entrypoint.

POST /run        {inputs} -> {outputs}  (one-shot)
POST /run/stream {inputs} -> SSE stream of answer chunks + a final event
GET  /healthz    liveness probe
"""
from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()

from .workflow.definition import DEFINITION, build_handlers
from .workflow.runner import Engine

app = FastAPI(title=os.environ.get("APP_NAME", "dify-workflow-service"))


class RunRequest(BaseModel):
    inputs: dict


class RunResponse(BaseModel):
    outputs: dict


def _run_engine(inputs: dict) -> Engine:
    engine = Engine(DEFINITION, build_handlers())
    engine.run(inputs)
    return engine


@app.post("/run", response_model=RunResponse)
def run(req: RunRequest):
    try:
        engine = _run_engine(req.inputs)
        return RunResponse(outputs=engine.outputs)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@app.post("/run/stream")
def run_stream(req: RunRequest):
    engine = Engine(DEFINITION, build_handlers())

    def events():
        try:
            for event, payload in engine.run_stream(req.inputs):
                yield f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
        except Exception as e:  # noqa: BLE001
            yield (f"event: error\ndata: "
                   f"{json.dumps(f'{type(e).__name__}: {e}', ensure_ascii=False)}\n\n")

    return StreamingResponse(events(), media_type="text/event-stream")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
