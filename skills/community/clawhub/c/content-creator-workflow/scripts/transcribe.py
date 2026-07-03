"""Audio transcription helper built on the OpenAI Whisper API.

Splits large audio files into time-bounded chunks (the Whisper API accepts up
to 25MB per request) and concatenates the resulting text.
"""

import io
import os
import sys
from typing import List

from openai import OpenAI, OpenAIError
from pydub import AudioSegment

try:
    from pydub.exceptions import CouldntDecodeError
except ImportError:  # Older/newer pydub layouts may not expose this path.
    class CouldntDecodeError(Exception):
        """Fallback used when pydub does not expose CouldntDecodeError."""

DEFAULT_OUTPUT_DIR = os.environ.get(
    "CONTENT_CREATOR_OUTPUT_DIR", os.path.join(os.getcwd(), "generated")
)
WHISPER_MODEL = "whisper-1"
MS_PER_MINUTE = 60 * 1000


class TranscriptionError(RuntimeError):
    """Raised when an audio file cannot be transcribed."""


def _get_client() -> OpenAI:
    """Return an OpenAI client, failing clearly if the API key is missing."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise TranscriptionError(
            "OPENAI_API_KEY environment variable is not set."
        )
    return OpenAI(api_key=api_key)


def transcribe_audio(file_path: str, chunk_size_mins: int = 10) -> str:
    """Transcribe an audio file, splitting large files into chunks.

    Args:
        file_path: Path to the audio file (mp3, mp4, mpeg, mpga, m4a, wav, webm).
        chunk_size_mins: Maximum length of each chunk sent to the API, in minutes.

    Returns:
        The full transcript with chunk boundaries joined by newlines.

    Raises:
        TranscriptionError: If the file is missing, undecodable, or the API fails.
    """
    if not file_path or not os.path.isfile(file_path):
        raise TranscriptionError(f"Audio file not found: {file_path!r}")
    if chunk_size_mins <= 0:
        raise TranscriptionError("chunk_size_mins must be a positive integer.")

    client = _get_client()

    try:
        audio = AudioSegment.from_file(file_path)
    except (CouldntDecodeError, FileNotFoundError, OSError) as exc:
        raise TranscriptionError(f"Could not load audio file: {exc}") from exc

    chunk_size_ms = chunk_size_mins * MS_PER_MINUTE
    chunks = [audio[i:i + chunk_size_ms] for i in range(0, len(audio), chunk_size_ms)]
    if not chunks:
        raise TranscriptionError("Audio file appears to be empty.")

    transcript_parts: List[str] = []
    for index, chunk in enumerate(chunks):
        buffer = io.BytesIO()
        buffer.name = f"chunk_{index}.mp3"
        chunk.export(buffer, format="mp3")
        buffer.seek(0)

        try:
            transcript = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=buffer,
                response_format="text",
            )
        except OpenAIError as exc:
            raise TranscriptionError(
                f"Whisper API failed on chunk {index + 1}/{len(chunks)}: {exc}"
            ) from exc

        transcript_parts.append(str(transcript))
        print(f"Processed chunk {index + 1}/{len(chunks)}")

    return "\n".join(transcript_parts).strip()


def main() -> None:
    """CLI entry point: transcribe a single audio file and save the result."""
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <audio_file_path>")
        sys.exit(1)

    audio_path = sys.argv[1]
    try:
        transcript = transcribe_audio(audio_path)
    except TranscriptionError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(
        DEFAULT_OUTPUT_DIR, f"{os.path.basename(audio_path)}.txt"
    )
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(transcript)

    print(f"Transcription saved to {output_path}")
    print("\nTranscript:")
    print(transcript)


if __name__ == "__main__":
    main()
