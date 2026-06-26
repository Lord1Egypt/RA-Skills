# AIHub

Read this file for AtomGit AIHub model features such as text generation, audio processing, object detection, and image-to-video workflows.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| Text generation or chat | `atomgit_chat_completion` |
| Speech recognition | `atomgit_audio_transcription` |
| Audio classification | `atomgit_audio_classification` |
| Object detection | `atomgit_object_detection` |
| Sentence similarity | `atomgit_sentence_similarity` |
| Create an image-to-video task | `atomgit_video_generation_create` |
| Poll video generation status | `atomgit_video_generation_status` |

## Notes

- AIHub requests still rely on the same AtomGit MCP environment and token setup as repository APIs.
- For long-running video jobs, create the task first and then poll for status updates.
