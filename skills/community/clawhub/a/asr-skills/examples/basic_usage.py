#!/usr/bin/env python3
"""Basic usage examples for the ASR skill Python API."""

from asr_skill import transcribe, SUPPORTED_FORMATS, SUPPORTED_VIDEO_FORMATS


def example_basic_transcription():
    """Basic transcription with default settings."""
    result = transcribe("audio.mp3")
    print(f"Text: {result['text']}")
    print(f"Output: {result['output_path']}")


def example_json_output():
    """Transcription with JSON output for structured data."""
    result = transcribe("audio.mp3", format="json")

    # Access segments with metadata
    for segment in result['segments']:
        print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")

        # Word-level data available in JSON format
        if 'words' in segment:
            for word in segment['words']:
                print(f"  {word['word']}: {word['confidence']:.2f}")


def example_srt_subtitles():
    """Generate SRT subtitles for video."""
    result = transcribe("video.mp4", format="srt")
    print(f"Subtitles saved to: {result['output_path']}")


def example_ass_styled_subtitles():
    """Generate ASS subtitles with speaker-specific colors."""
    result = transcribe("meeting.mp4", format="ass")
    print(f"Styled subtitles: {result['output_path']}")

    # Speaker information available
    if 'speakers' in result:
        print(f"Speakers detected: {', '.join(result['speakers'])}")


def example_markdown_output():
    """Generate Markdown with speaker sections."""
    result = transcribe("podcast.mp3", format="md")
    print(f"Markdown document: {result['output_path']}")


def example_custom_output_dir():
    """Specify custom output directory."""
    result = transcribe("audio.mp3", output_dir="./transcripts", format="json")
    print(f"Output saved to: {result['output_path']}")


def example_no_diarization():
    """Disable speaker diarization for faster processing."""
    result = transcribe("audio.mp3", diarize=False, format="txt")
    print(f"Text (no speakers): {result['text']}")


if __name__ == "__main__":
    print("ASR Skill - Python API Examples")
    print(f"Supported audio: {SUPPORTED_FORMATS}")
    print(f"Supported video: {SUPPORTED_VIDEO_FORMATS}")
    print("\nRun individual example functions to see usage.")
