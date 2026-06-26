# Pipeline Notes

## Purpose

Provide a shell-native path for:

1. input audio -> transcript
2. optional text reply -> MP3 reply

## JSON contract

The pipeline prints JSON with:

- `out_dir`
- `transcript_path`
- `transcript`
- `reply_audio_path`

This structure is designed to be easy for wrappers and adapters to parse.

## Good fit

Use the pipeline for lightweight bot automation, testing, and glue-code workflows where a full SDK would be overkill.
