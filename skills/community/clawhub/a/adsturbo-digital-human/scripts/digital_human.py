#!/usr/bin/env python3
"""Digital human / talking-head video.

One intent -- make a persona speak -- with three sources for the persona:
  library   : pick from AdsTurbo's stock actors      (actors -> perform)
  custom    : build one from a photo + voice sample  (persona-create -> perform)
  bring own : hand over any portrait plus audio      (lipsync)
"""

from __future__ import annotations

import argparse

from shared.client import add_async_flags, run_cli, submit_and_maybe_poll

ACTOR_LIST = "/openapi/v1/aiactor/list"
ACTOR_SAY = "/openapi/v1/aiactor/say"
ACTOR_PERFORM = "/openapi/v1/aiactor/perform"
PERSONA_CREATE = "/openapi/v1/persona/create"
PERSONA_DELETE = "/openapi/v1/persona/delete"
PERSONA_LIST = "/openapi/v1/persona/list"
PERSONA_STATUS = "/openapi/v1/persona/status"
LIPSYNC = "/openapi/v1/video/lipsync"


def cmd_actors(client, args) -> dict:
    return client.post(ACTOR_LIST, {
        "gender": args.gender,
        "age": args.age,
        "situation": args.situation,
        "pose": args.pose,
        "shot_type": args.shot_type,
        "ethnicity": args.ethnicity,
        "industry": args.industry,
        "sort_by": args.sort_by,
        "offset": args.offset,
        "limit": args.limit,
    })


def cmd_say(client, args) -> dict:
    """Text to speech in an actor's voice. Synchronous -- returns audio_url."""
    return client.post(ACTOR_SAY, {
        "actor_id": args.actor_id,
        "script": args.script,
        "auto_emotion": args.auto_emotion,
        "speed": args.speed,
        "stability": args.stability,
        "similarity": args.similarity,
    })


def cmd_perform(client, args) -> dict:
    """Talking-head video. actor_id accepts both stock actors and custom personas."""
    return submit_and_maybe_poll(client, ACTOR_PERFORM, {
        "actor_id": args.actor_id,
        "script": args.script,
        "look_id": args.look_id,
        "said_url": args.said_url,
        "auto_emotion": args.auto_emotion,
        "speed": args.speed,
        "stability": args.stability,
        "style": args.style,
        "similarity": args.similarity,
        "speaker_boost": args.speaker_boost,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_persona_create(client, args) -> dict:
    """Build a custom persona from a portrait, optionally cloning a voice."""
    return submit_and_maybe_poll(client, PERSONA_CREATE, {
        "photo_url": args.photo_url,
        "voice_audio_url": args.voice_audio_url,
        "name": args.name,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_persona_delete(client, args) -> dict:
    return client.post(PERSONA_DELETE, {"actor_id": args.actor_id})


def cmd_persona_list(client, args) -> dict:
    return client.post(PERSONA_LIST, {"offset": args.offset, "limit": args.limit})


def cmd_persona_status(client, args) -> dict:
    return client.post(PERSONA_STATUS, {"actor_id": args.actor_id})


def cmd_lipsync(client, args) -> dict:
    """Drive any portrait with any audio track."""
    return submit_and_maybe_poll(client, LIPSYNC, {
        "avatar_url": args.avatar_url,
        "audio_url": args.audio_url,
        "prompt": args.prompt,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_query(client, args) -> dict:
    return client.poll(args.workspace_id, timeout=args.timeout, interval=args.interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo digital human")
    sub = parser.add_subparsers(dest="command")

    actors = sub.add_parser("actors", help="list stock actors")
    for facet in ("gender", "age", "situation", "pose", "shot-type", "ethnicity", "industry"):
        actors.add_argument(f"--{facet}", nargs="*", default=[])
    actors.add_argument("--sort-by", default="")
    actors.add_argument("--offset", type=int, default=0)
    actors.add_argument("--limit", type=int, default=20)

    say = sub.add_parser("say", help="text to speech (sync)")
    say.add_argument("--actor-id", required=True)
    say.add_argument("--script", required=True)
    say.add_argument("--auto-emotion", action="store_true")
    say.add_argument("--speed", type=float)
    say.add_argument("--stability", type=float)
    say.add_argument("--similarity", type=float)

    perform = sub.add_parser("perform", help="talking-head video from a script")
    perform.add_argument("--actor-id", required=True, help="stock actor or persona id")
    perform.add_argument("--script", default="", help="omit when passing --said-url")
    perform.add_argument("--look-id", default="")
    perform.add_argument("--said-url", default="", help="pre-rendered audio, skips TTS")
    perform.add_argument("--auto-emotion", action="store_true")
    perform.add_argument("--speed", type=float)
    perform.add_argument("--stability", type=float)
    perform.add_argument("--style", type=float)
    perform.add_argument("--similarity", type=float)
    perform.add_argument("--speaker-boost", action="store_true")
    perform.add_argument("--idempotency-key", default="")
    add_async_flags(perform)

    create = sub.add_parser("persona-create", help="create a custom persona")
    create.add_argument("--photo-url", required=True)
    create.add_argument("--voice-audio-url", default="", help="clone this voice")
    create.add_argument("--name", default="")
    create.add_argument("--idempotency-key", default="")
    add_async_flags(create)

    delete = sub.add_parser("persona-delete")
    delete.add_argument("--actor-id", required=True)

    listing = sub.add_parser("persona-list")
    listing.add_argument("--offset", type=int, default=0)
    listing.add_argument("--limit", type=int, default=20)

    status = sub.add_parser("persona-status", help="check persona build progress")
    status.add_argument("--actor-id", required=True)

    lip = sub.add_parser("lipsync", help="sync any portrait to any audio")
    lip.add_argument("--avatar-url", required=True)
    lip.add_argument("--audio-url", required=True)
    lip.add_argument("--prompt", default="")
    lip.add_argument("--idempotency-key", default="")
    add_async_flags(lip)

    query = sub.add_parser("query", help="resume polling a known workspace_id")
    query.add_argument("--workspace-id", required=True)
    query.add_argument("--timeout", type=float, default=900)
    query.add_argument("--interval", type=float, default=10)

    return parser


HANDLERS = {
    "actors": cmd_actors,
    "say": cmd_say,
    "perform": cmd_perform,
    "persona-create": cmd_persona_create,
    "persona-delete": cmd_persona_delete,
    "persona-list": cmd_persona_list,
    "persona-status": cmd_persona_status,
    "lipsync": cmd_lipsync,
    "query": cmd_query,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
