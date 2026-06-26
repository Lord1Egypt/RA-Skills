---
name: newtranx-cli
description: >
  newtranx CLI for translate MP4 videos, Used for directly translating video files on the terminal.
  When you want to translate video files from one country's accent to another from URLs or local files,
  it supports exporting the original video,translated video, original subtitles and translated subtitle files, including speaker recognition 
---

# newtranx CLI (`newtranx`)

Translate videos and podcasts from the terminal using the newtranx API.

## Installation

```bash
npx --yes newtranx-ai
```

## Usage Process

### 1. login

```bash
npx newtranx-ai login
```

Automatically obtain device ID, call the registration login interface to obtain token, and save it to `~/. newtranx/config. json `. The token is valid for 15 days.
### 2. Upload videos

Supports local files and HTTP URLs, only supports mp4 format. If the format is not supported, please use ffmepg to transcode to mp4 file size not exceeding 5GB and duration not exceeding 4 hours.
Important: URLs containing ? or & must be quoted to avoid shell glob errors.

```bash

npx newtranx-ai upload ./video.mp4

# HTTP URL
npx newtranx-ai upload https://example.com/video.mp4
```

Restrictions:
-Format: mp4 only
-Size: not exceeding 5GB

Automatically upload videos in 4MB chunks and display upload progress. After uploading, output the task ID.

### 3. Submit translation task

```bash
npx newtranx-ai  translate --id <taskID> \
  --audio-lang en-US \
  --trans-lang zh-CN \
  --max-speakers 2 \
  --export-subtitle
```

Parameter description:
- `--id` (Required): Upload the returned task ID
- `--audio-lang`(Required): Call the ` npx newtranx-ai language ` command in the original language of the video to view
- `--trans-lang`(Required): Call the ` npx newtranx-ai language ` command to view the target translation language
- `--max-speakers`: Number of speakers
- `--export-subtitle`: Do you want to merge subtitles into the video
- `--re-transwrite`: Do you want to rewrite it
- `--subtitle-font-size`: Subtitle Font Size
- `--subtitle-max-chars`: Maximum number of characters per subtitle segment
- `--subtitle-outline-color`: Subtitle outline color
- `--subtitle-primary-color`: Subtitle main color

### 4. Regularly query query results

```bash
# default output translated video download link
npx newtranx-ai status --id <taskID>

# output original VTT subtitles download link
npx newtranx-cli status --id <taskID> --subtitle

# output translated VTT subtitles download link
npx newtranx-cli status --id <taskID> --targetSubtitle 

# output metadata include speaker information download link
npx newtranx-cli status --id <taskID> --metadata 

```

When 'iterationStatus==Succeeded', the result contains:
- Translated video download link
- Source language subtitle file link
- Target language subtitle file link
- Metadata file link

### 5. Query supported languages

```bash

npx newtranx-ai language

npx newtranx-ai language --region CN
```

Return a list of language codes and names that can be used for the ` audio lang ` and ` trans lang ` parameters of the ` translate ` command.



## Usage Tips

1. If the token expires, call `npx newtranx ai login` and then retry.
2. It must be called according to the process.