#!/usr/bin/env python3
"""Ask an EmpirioLabs AI text model a question and print its answer.

Examples:
  python3 chat.py "Explain the tradeoffs between optimistic and pessimistic locking"
  python3 chat.py "Review this function for bugs" --file ./src/parser.py
  python3 chat.py "What does this screenshot show?" --image ./screenshot.png
  python3 chat.py "Summarize the risks" --system "You are a careful security reviewer." --model MODEL_ID
  python3 chat.py "Which design is simpler to operate?" --model MODEL_A --model MODEL_B
  python3 chat.py "Summarize these notes in five bullet points" --file ./notes.md --out ./summary.md
  git diff | python3 chat.py - --system "Review this diff for bugs."
  python3 chat.py --list-models              # add --vision for the models that read images

Prints the answer as text (or the full result as JSON with --json) to stdout. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

CHAT = "POST /v1/chat/completions"
PATH = "/chat/completions"
# A long answer from a reasoning model can take minutes; the request stays open until it is ready.
TIMEOUT = 600.0
MAX_TEXT_BYTES = 1024 * 1024
# A model of one of these kinds answers a chat request with media, which this script does not return.
MEDIA_KINDS = ("image", "video", "audio", "3d")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="chat.py",
        description="Ask an EmpirioLabs AI text model a question and print its answer.",
        epilog=(
            "When --model is omitted, a text model from the live catalog is used.\n"
            "A request is billed at the model's listed price, per token for a text model; check --list-models first.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", nargs="?",
                        help="The question or instruction. Pass - to read it from standard input.")
    parser.add_argument("--system", help="Instructions the model follows for this request.")
    parser.add_argument("--file", action="append", metavar="PATH",
                        help="Attach a text file to the prompt, for example source code or notes. Repeatable.")
    parser.add_argument("--image", action="append", metavar="URL_OR_PATH",
                        help="Attach an image for a model that reads images (https URL or local file). Repeatable.")
    parser.add_argument("--model", action="append", metavar="MODEL_ID",
                        help="Model id. Repeat it to have several models answer the same prompt. See --list-models.")
    parser.add_argument("--max-tokens", type=int, help="Upper limit on the length of the answer, in tokens.")
    parser.add_argument("--temperature", type=float, help="Sampling temperature.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param reasoning_effort=high. Repeatable.")
    parser.add_argument("--out", help="Save the answer here (.json saves the full result).")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing --out file.")
    parser.add_argument("--json", action="store_true", help="Print the full result as JSON.")
    parser.add_argument("--list-models", action="store_true",
                        help="List the text models with prices, then exit.")
    parser.add_argument("--vision", action="store_true",
                        help="With --list-models, list only the models that read images.")
    return parser


def reads_images(model):
    return "image" in (model.get("input_modalities") or [])


def chat_models(models, images=False):
    """Text models that answer a chat request, in catalog order; with images, the ones that read them."""
    pool = api.candidates(models, CHAT, category="text")
    return [m for m in pool if reads_images(m)] if images else pool


def media_kind(entry):
    kind = str((entry or {}).get("modality") or "").strip().lower()
    return kind if kind in MEDIA_KINDS else None


def resolve(args):
    """The (model id, catalog entry or None) pairs to ask, checked before anything is sent."""
    images = bool(args.image)
    if not args.model:
        pool = chat_models(api.list_models(), images)
        if not pool:
            raise api.ApiError("No text model in the live catalog " + ("reads images" if images else "answers a chat request")
                               + ". Pass --model explicitly.")
        entry = api.pick_default(pool, CHAT)
        return [(entry["id"], entry)]
    chosen = []
    for name in args.model:
        model_id, entry = api.resolve_model(name, CHAT)
        kind = media_kind(entry)
        if kind:
            raise api.ApiError(
                model_id + " is " + ("a 3D" if kind == "3d" else "an " + kind if kind[0] in "aeiou" else "a " + kind)
                + " model, which answers with media, not text. Run with --list-models to choose a text model.",
                code="unsupported_model", exit_code=api.EXIT_USAGE)
        if images and entry is not None and not reads_images(entry):
            raise api.ApiError(model_id + " does not read images. Run with --list-models --vision to see models that do.",
                               code="unsupported_input", exit_code=api.EXIT_USAGE)
        if model_id not in [seen for seen, _ in chosen]:
            chosen.append((model_id, entry))
    return chosen


def list_models(images):
    models = api.list_models()
    pool = chat_models(models, images)
    default = api.pick_default(pool, CHAT)["id"] if pool else None
    for model in pool:
        mark = "*" if model["id"] == default else " "
        print(mark + " " + model["id"].ljust(32) + " " + api.price_summary(model))
    api.log(str(len(pool)) + " text models " + ("read images" if images else "answer a chat request")
            + ". * marks the default when --model is omitted.")


def fence_for(text):
    """A code fence longer than any run of backticks in the text it wraps."""
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def attached_text(paths):
    """The attached files as fenced blocks, each under its file name."""
    blocks = []
    total = 0
    for value in paths or []:
        path = os.path.expanduser(value)
        if not os.path.isfile(path):
            raise api.ApiError("File not found: " + value, exit_code=api.EXIT_USAGE)
        with open(path, "rb") as handle:
            payload = handle.read()
        total += len(payload)
        if total > MAX_TEXT_BYTES:
            raise api.ApiError("The attached files are larger than " + str(MAX_TEXT_BYTES // 1024)
                               + " KB in total. Attach less, or pass only the part that matters.",
                               exit_code=api.EXIT_USAGE)
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            raise api.ApiError(value + " is not a UTF-8 text file. Use --image for a picture.",
                               exit_code=api.EXIT_USAGE)
        fence = fence_for(text)
        blocks.append("File: " + os.path.basename(path) + "\n" + fence + "\n" + text.rstrip("\n") + "\n" + fence)
    return blocks


def read_prompt(args, parser):
    prompt = args.prompt
    if prompt == "-":
        prompt = sys.stdin.read()
    if not prompt or not prompt.strip():
        parser.error("a prompt is required (or pass --list-models)")
    return "\n\n".join([prompt.strip()] + attached_text(args.file))


def build_messages(args, prompt):
    content = prompt
    if args.image:
        content = [{"type": "text", "text": prompt}]
        for value in args.image:
            content.append({"type": "image_url", "image_url": {"url": api.inline_file(value)}})
    messages = []
    if args.system and args.system.strip():
        messages.append({"role": "system", "content": args.system.strip()})
    messages.append({"role": "user", "content": content})
    return messages


def request_params(args):
    params = {}
    if args.max_tokens is not None:
        params["max_tokens"] = args.max_tokens
    if args.temperature is not None:
        params["temperature"] = args.temperature
    params.update(api.parse_params(args.param))
    return params


def answer_of(result):
    """The text of the first choice, or None when the model returned none."""
    choices = result.get("choices") if isinstance(result, dict) else None
    message = (choices[0].get("message") if isinstance(choices, list) and choices and isinstance(choices[0], dict)
               else None) or {}
    content = message.get("content")
    if isinstance(content, list):
        content = "".join(part.get("text") or "" for part in content if isinstance(part, dict))
    return content.strip() if isinstance(content, str) and content.strip() else None


def finish_reason(result):
    choices = result.get("choices") if isinstance(result, dict) else None
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        return choices[0].get("finish_reason")
    return None


def log_usage(model_id, result):
    usage = result.get("usage") if isinstance(result, dict) else None
    if isinstance(usage, dict) and usage.get("prompt_tokens") is not None:
        api.log(model_id + ": " + str(usage.get("prompt_tokens")) + " prompt tokens, "
                + str(usage.get("completion_tokens") or 0) + " generated tokens.")


def ask(model_id, messages, params):
    """One answer: {"model", "text", "result"} or {"model", "error"}."""
    body = {"model": model_id, "messages": messages, "stream": False}
    body.update(params)
    api.log("Asking " + model_id + " ...")
    result = api.post_json(PATH, body, timeout=TIMEOUT).json()
    log_usage(model_id, result)
    text = answer_of(result)
    if text is None:
        reason = finish_reason(result)
        hint = " Raise --max-tokens." if reason == "length" else ""
        return {"model": model_id, "result": result,
                "error": "The model returned no text" + (" (finish reason: " + str(reason) + ")" if reason else "")
                         + "." + hint}
    return {"model": model_id, "text": text, "result": result}


def render(answers):
    """Plain text for an agent to read: one answer as is, several under a heading each."""
    if len(answers) == 1:
        return answers[0].get("text")
    parts = []
    for answer in answers:
        parts.append("## " + answer["model"] + "\n\n" + (answer.get("text") or "No answer: " + answer["error"]))
    return "\n\n".join(parts)


def as_json(answers):
    if len(answers) == 1 and "result" in answers[0]:
        return answers[0]["result"]
    return {"answers": [{key: answer[key] for key in ("model", "result", "error") if key in answer}
                        for answer in answers]}


def finish(args, answers):
    failed = [answer for answer in answers if "error" in answer]
    for answer in failed:
        api.log(answer["model"] + ": " + answer["error"])
    if len(failed) == len(answers) and not args.json:
        # No model answered: there is nothing to print or to save.
        return api.EXIT_ERROR
    text = None if args.json else render(answers)
    if args.out:
        out = os.path.expanduser(args.out)
        if api.is_dir_target(out):
            path = api.target_path(out, api.default_stem("chat"), ".json" if text is None else ".md", 1, 1,
                                   args.overwrite)
        else:
            path = os.path.abspath(out)
            if not args.overwrite:
                path = api.free_path(path)
        if path.lower().endswith(".json") or text is None:
            content = json.dumps(as_json(answers), indent=2, ensure_ascii=False)
        else:
            content = text
        api.write_bytes(path, (content.rstrip("\n") + "\n").encode("utf-8"))
        api.log("Saved " + path)
        models = [answer["model"] for answer in answers]
        summary = {"model": models[0]} if len(models) == 1 else {"models": models}
        summary.update({"file": path, "characters": sum(len(answer.get("text") or "") for answer in answers)})
        api.print_json(summary)
    elif text is None:
        api.print_json(as_json(answers))
    else:
        print(text, flush=True)
    return api.EXIT_ERROR if failed else api.EXIT_OK


def run(args, parser):
    if args.list_models:
        list_models(args.vision or bool(args.image))
        return api.EXIT_OK
    prompt = read_prompt(args, parser)
    api.api_key()
    chosen = resolve(args)
    messages = build_messages(args, prompt)
    params = request_params(args)
    answers = []
    for model_id, _entry in chosen:
        try:
            answers.append(ask(model_id, messages, params))
        except api.ApiError as exc:
            if len(chosen) == 1:
                raise
            answers.append({"model": model_id, "error": api.redact(exc.message)})
    return finish(args, answers)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.ApiError as exc:
        return api.fail(exc)
    except OSError as exc:
        return api.fail(api.ApiError("Could not read or write a file: " + str(exc)))
    except KeyboardInterrupt:
        api.log("Interrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
