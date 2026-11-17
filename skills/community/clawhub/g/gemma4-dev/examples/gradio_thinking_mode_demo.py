"""
Reference implementation: Gradio UI with Gemma 4 Thinking Mode Inspector.
Demonstrates how to parse and inspect <thought> blocks separately from final output.

SECURITY & AUDIT COMPLIANCE:
- Lazy Loading: Pipeline initialization is deferred inside function scope, avoiding
  unexpected network access or resource allocation at import time.
- Immutable Artifact Pinning: Remote models are pinned to immutable commit hashes with
  trust_remote_code=False.
- Offline Capability: Accepts a local directory path via LOCAL_MODEL_PATH to run in
  air-gapped or restricted network environments.
"""

import os
import re
from typing import Tuple, Optional
import gradio as gr

# Default pinned repository and immutable commit revision
DEFAULT_MODEL_ID = "google/gemma-4-E2B-it"
DEFAULT_MODEL_REVISION = "e9a0c10825eb6e2897621c1723c4a24f0c406214"

# Global pipeline instance (lazily initialized)
_pipeline = None

def get_pipeline(model_path_or_id: Optional[str] = None, revision: Optional[str] = None):
    """
    Lazily loads text-generation pipeline with pinned revision and trust_remote_code=False.
    """
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    from transformers import pipeline

    target = model_path_or_id or os.environ.get("GEMMA_MODEL_PATH") or DEFAULT_MODEL_ID
    target_rev = None if os.path.exists(target) else (revision or DEFAULT_MODEL_REVISION)

    _pipeline = pipeline(
        "text-generation",
        model=target,
        revision=target_rev,
        trust_remote_code=False,
        device_map="auto",
        dtype="auto",
    )
    return _pipeline

def extract_thinking_and_response(text: str) -> Tuple[str, str]:
    """Extracts all internal reasoning from <thought> tags and isolates user-facing response."""
    thoughts = re.findall(r"<thought>(.*?)(?:</thought>|$)", text, re.DOTALL)
    thought_text = "\n---\n".join(t.strip() for t in thoughts if t.strip())
    response_text = re.sub(r"<thought>.*?(?:</thought>|$)", "", text, flags=re.DOTALL).strip()
    return thought_text, response_text

def stream_developer_turn(prompt: str):
    """Processes user prompt and streams reasoning trace alongside final response."""
    from transformers import TextIteratorStreamer, GenerationConfig
    from threading import Thread

    pipe = get_pipeline()
    messages = [{"role": "user", "content": prompt}]
    streamer = TextIteratorStreamer(pipe.tokenizer, skip_prompt=True, skip_special_tokens=True)
    config = GenerationConfig(max_new_tokens=512)

    thread = Thread(target=pipe, args=(messages,), kwargs=dict(
        generation_config=config,
        streamer=streamer
    ))
    thread.start()

    raw_text = ""
    for new_text in streamer:
        raw_text += new_text
        thought, final_answer = extract_thinking_and_response(raw_text)
        yield thought, final_answer

def build_demo():
    with gr.Blocks(title="Gemma 4 Developer Thinking Inspector") as demo:
        gr.Markdown("## Gemma 4 Developer Reference: Thinking Inspector")
        gr.Markdown(
            "Inspect internal model reasoning (<thought> blocks) separately from client responses.\n\n"
            "**Security Notice**: Model weights are loaded with pinned revisions and `trust_remote_code=False`. "
            "Set `GEMMA_MODEL_PATH` in the environment to point to a verified local directory for offline operation."
        )

        with gr.Row():
            user_input = gr.Textbox(label="Developer Prompt", placeholder="Enter query or coding task...")
            submit_btn = gr.Button("Inspect Reasoning & Output")

        with gr.Row():
            thought_output = gr.Textbox(label="Internal Reasoning Traces (<thought>)", lines=8)
            final_output = gr.Textbox(label="User Response", lines=8)

        submit_btn.click(stream_developer_turn, inputs=[user_input], outputs=[thought_output, final_output])
    return demo

if __name__ == "__main__":
    demo = build_demo()
    demo.launch()
