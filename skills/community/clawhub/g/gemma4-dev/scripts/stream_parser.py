"""
Gemma 4 Real-Time Thinking Stream Parser.

Parses streaming token chunks from Gemma 4 models, separating internal reasoning
(<thought>...</thought>) from user-facing responses while handling split tags
across chunk boundaries, multiple thought blocks, and fail-closed termination.
"""

from typing import Generator, Tuple


class GemmaThoughtStreamParser:
    """
    State machine parser for Gemma 4 token streams.
    Supports:
    - Multiple <thought>...</thought> blocks throughout a stream
    - Response text before, between, and after thought blocks
    - Split tags across arbitrary chunk boundaries
    - Fail-closed handling for unclosed thought blocks
    
    Yields (event_type, chunk_text) tuples where event_type is:
    - 'thought': Internal reasoning text
    - 'response': User-facing response text
    """

    OPEN_TAG = "<thought>"
    CLOSE_TAG = "</thought>"

    def __init__(self):
        self.state = "OUTSIDE_THOUGHT"  # 'OUTSIDE_THOUGHT' or 'IN_THOUGHT'
        self.buffer = ""
        self.thought_text = ""
        self.response_text = ""

    def feed(self, chunk: str) -> Generator[Tuple[str, str], None, None]:
        """
        Feeds a chunk of streamed text and yields zero or more (kind, text) tuples.
        """
        self.buffer += chunk

        while self.buffer:
            if self.state == "OUTSIDE_THOUGHT":
                # Check for the complete opening tag
                tag_idx = self.buffer.find(self.OPEN_TAG)
                if tag_idx != -1:
                    prefix = self.buffer[:tag_idx]
                    self.buffer = self.buffer[tag_idx + len(self.OPEN_TAG):]
                    self.state = "IN_THOUGHT"
                    if prefix:
                        self.response_text += prefix
                        yield ("response", prefix)
                else:
                    # Check if the tail of the buffer matches the start of <thought>
                    held_len = 0
                    for i in range(min(len(self.buffer), len(self.OPEN_TAG) - 1), 0, -1):
                        if self.OPEN_TAG.startswith(self.buffer[-i:]):
                            held_len = i
                            break

                    to_emit = self.buffer[:-held_len] if held_len > 0 else self.buffer
                    self.buffer = self.buffer[-held_len:] if held_len > 0 else ""
                    if to_emit:
                        self.response_text += to_emit
                        yield ("response", to_emit)
                    break

            elif self.state == "IN_THOUGHT":
                # Inside thought tags, looking for </thought>
                close_idx = self.buffer.find(self.CLOSE_TAG)
                if close_idx != -1:
                    thought_content = self.buffer[:close_idx]
                    self.buffer = self.buffer[close_idx + len(self.CLOSE_TAG):]
                    self.state = "OUTSIDE_THOUGHT"
                    if thought_content:
                        self.thought_text += thought_content
                        yield ("thought", thought_content)
                else:
                    # Check if the tail of the buffer matches the start of </thought>
                    held_len = 0
                    for i in range(min(len(self.buffer), len(self.CLOSE_TAG) - 1), 0, -1):
                        if self.CLOSE_TAG.startswith(self.buffer[-i:]):
                            held_len = i
                            break

                    to_emit = self.buffer[:-held_len] if held_len > 0 else self.buffer
                    self.buffer = self.buffer[-held_len:] if held_len > 0 else ""
                    if to_emit:
                        self.thought_text += to_emit
                        yield ("thought", to_emit)
                    break

    def finalize(self) -> Generator[Tuple[str, str], None, None]:
        """
        Flushes any remaining buffered text at end-of-stream.
        Fail-closed: if the stream ends while inside a thought tag, the buffered
        content is treated as thought to prevent reasoning leakage into response.
        """
        if self.buffer:
            kind = "thought" if self.state == "IN_THOUGHT" else "response"
            if kind == "thought":
                self.thought_text += self.buffer
            else:
                self.response_text += self.buffer
            rem = self.buffer
            self.buffer = ""
            yield (kind, rem)

    def get_summary(self) -> Tuple[str, str]:
        """Returns the full (thought_text, response_text) accumulated so far."""
        return self.thought_text.strip(), self.response_text.strip()
