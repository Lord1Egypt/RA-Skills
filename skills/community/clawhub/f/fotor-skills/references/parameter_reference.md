# Parameter Reference

All task functions are `async` and accept `client: FotorClient` as the first positional argument.
Every function also accepts `on_poll: Callable[[TaskResult], None] | None = None` for progress monitoring during polling.

## Image Tasks

### text2image

```python
await text2image(client, *, prompt, model_id, aspect_ratio="1:1", resolution="1k", on_poll=None, **extra)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | str | Yes | -- | Text description of the image |
| model_id | str | Yes | -- | See `image_models.md` |
| aspect_ratio | str | No | `"1:1"` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `9:21` |
| resolution | str | No | `"1k"` | `1k`, `2k`, `4k` |
| on_poll | Callable | No | `None` | Called each poll cycle with current `TaskResult` |
| **extra | Any | No | -- | Additional fields merged into the API payload |

### image2image

```python
await image2image(client, *, prompt, model_id, image_urls, aspect_ratio="1:1", resolution="1k", on_poll=None, **extra)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | str | Yes | -- | Edit instructions or style description |
| model_id | str | Yes | -- | Must support I2I (see `image_models.md`) |
| image_urls | list[str] | Yes | -- | 1 URL for single edit, 2-5 for multi-reference |
| aspect_ratio | str | No | `"1:1"` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `9:21` |
| resolution | str | No | `"1k"` | `1k`, `2k`, `4k` |
| on_poll | Callable | No | `None` | Progress callback |
| **extra | Any | No | -- | Additional payload fields |

Raises `ValueError` if `image_urls` is empty.

### image_upscale

```python
await image_upscale(client, *, image_url, upscale_ratio=2.0, on_poll=None)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| image_url | str | Yes | -- | Input image URL |
| upscale_ratio | float | No | `2.0` | Only `2.0` or `4.0` |
| on_poll | Callable | No | `None` | Progress callback |

Fixed payload values: `max_image_width=2048`, `max_image_height=2048`.

### background_remove

```python
await background_remove(client, *, image_url, on_poll=None)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| image_url | str | Yes | -- | Input image URL |
| on_poll | Callable | No | `None` | Progress callback |

Fixed payload value: `action="auto"`.

---

## Video Tasks

All video functions share a common internal payload structure:
- All payloads include `scenes: "normal"` automatically
- `audio_enable` maps to `enableAudio` in the API payload
- `audio_prompt` is **not** a named parameter -- pass it via `**extra`

### text2video

```python
await text2video(client, *, prompt, model_id, duration=5, resolution="1080p", aspect_ratio="16:9", audio_enable=False, on_poll=None, **extra)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | str | Yes | -- | Text description |
| model_id | str | Yes | -- | See `video_models.md` (must support T2V) |
| duration | int | No | `5` | Seconds (model-dependent, typically 4-10) |
| resolution | str | No | `"1080p"` | `720p`, `1080p` |
| aspect_ratio | str | No | `"16:9"` | `1:1`, `9:16`, `16:9`, `21:9` etc. |
| audio_enable | bool | No | `False` | Enable audio generation |
| on_poll | Callable | No | `None` | Progress callback |
| **extra | Any | No | -- | e.g. `audio_prompt="..."` when audio is enabled |

### single_image2video

```python
await single_image2video(client, *, prompt, model_id, image_url, duration=5, resolution="1080p", aspect_ratio="16:9", audio_enable=False, on_poll=None, **extra)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | str | Yes | -- | Motion/animation description |
| model_id | str | Yes | -- | Must support I2V |
| image_url | str | Yes | -- | Source image URL |
| duration | int | No | `5` | Seconds |
| resolution | str | No | `"1080p"` | |
| aspect_ratio | str | No | `"16:9"` | `1:1`, `9:16`, `16:9` etc. |
| audio_enable | bool | No | `False` | |
| on_poll | Callable | No | `None` | |
| **extra | Any | No | -- | e.g. `audio_prompt="..."` |

### start_end_frame2video

```python
await start_end_frame2video(client, *, prompt, model_id, start_image_url, end_image_url, duration=5, resolution="1080p", aspect_ratio="16:9", audio_enable=False, on_poll=None, **extra)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | str | Yes | -- | Transition description |
| model_id | str | Yes | -- | Must support SE interpolation |
| start_image_url | str | Yes | -- | Start frame URL |
| end_image_url | str | Yes | -- | End frame URL |
| duration | int | No | `5` | Seconds |
| resolution | str | No | `"1080p"` | |
| aspect_ratio | str | No | `"16:9"` | `1:1`, `9:16`, `16:9` etc. |
| audio_enable | bool | No | `False` | |
| on_poll | Callable | No | `None` | |
| **extra | Any | No | -- | e.g. `audio_prompt="..."` |

### multiple_image2video

```python
await multiple_image2video(client, *, prompt, model_id, image_urls, duration=5, resolution="1080p", aspect_ratio="16:9", audio_enable=False, on_poll=None, **extra)
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | str | Yes | -- | Narrative/overall description |
| model_id | str | Yes | -- | Must support MI |
| image_urls | list[str] | Yes | -- | Minimum 2 URLs |
| duration | int | No | `5` | Seconds |
| resolution | str | No | `"1080p"` | |
| aspect_ratio | str | No | `"16:9"` | `1:1`, `9:16`, `16:9` etc. |
| audio_enable | bool | No | `False` | |
| on_poll | Callable | No | `None` | |
| **extra | Any | No | -- | e.g. `audio_prompt="..."` |

Raises `ValueError` if `image_urls` contains fewer than 2 URLs.
