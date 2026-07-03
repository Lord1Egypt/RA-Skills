# Doubao Music Generation Parameter Quick Reference

## API Information

| API | Action | Billing | Description |
|-----|--------|---------|-------------|
| Vocal Song (Prepaid) | `GenSongV4` | Prepaid | Per-request billing |
| Vocal Song (Postpaid) | `GenSongForTime` | Postpaid | Per-duration billing |
| Instrumental BGM (Prepaid) | `GenBGM` | Prepaid | Per-request billing |
| Instrumental BGM (Postpaid) | `GenBGMForTime` | Postpaid | Per-duration billing |
| Task Query | `QuerySong` | - | Query async task result (shared by BGM and song) |

- **Endpoint:** `https://open.volcengineapi.com/?Action=XXX&Version=2024-08-12`
- **Authentication:** Volcano Engine HMAC-SHA256 signature (VOLC_ACCESS_KEY + VOLC_SECRET_KEY)

---

## BGM Parameters (GenBGM / GenBGMForTime)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `Text` | string | Yes | BGM description, can include genre/mood/scene/instruments |
| `Duration` | int | No | Duration in seconds, v5.0 range [30, 120], default 60 |
| `Version` | string | No | Model version, default `v5.0` (fully upgraded) |
| `EnableInputRewrite` | bool | No | Whether to enable prompt rewrite, default false |
| `Segments` | list | No | Structured segments (v5.0 only), each segment has Name + Duration |
| `CallbackURL` | string | No | Task completion callback URL |

### Segments Example
```json
[
  {"Name": "verse",  "Duration": 20},
  {"Name": "chorus", "Duration": 20},
  {"Name": "outro",  "Duration": 10}
]
```
Segments.Name allowed values: `intro` `verse` `chorus` `inst` `bridge` `outro`

---

## Vocal Song Parameters (GenSongV4 / GenSongForTime)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `Prompt` | string | One of Prompt or Lyrics | Prompt (5~700 chars for Chinese / 5~2000 chars for English) |
| `Lyrics` | string | One of Prompt or Lyrics | Lyrics (format below, takes priority over Prompt) |
| `ModelVersion` | string | No | `v4.0` / `v4.3` / `v5.0`, default `v4.0` |
| `Genre` | string | No | Primary genre (v4.0 max 1, v4.3 max 3 comma-separated) |
| `GenreExtra` | string | No | Secondary genres, up to 2 (v4.3 only) |
| `Mood` | string | No | Mood (v4.0 max 1, v4.3 max 2) |
| `Gender` | string | No | `Male` / `Female` |
| `Timbre` | string | No | Timbre (v4.3 max 3) |
| `Duration` | int | No | Duration in seconds [30, 240] |
| `Lang` | string | No | Language, default `Chinese` |
| `VodFormat` | string | No | Output format `wav` / `mp3`, default `wav` |
| `Key` | string | No | Key (v4.3)|
| `Kmode` | string | No | Mode `Major` / `Minor` (v4.3)|
| `Tempo` | string | No | Tempo (v4.3)|
| `Instrument` | string | No | Instruments, comma-separated, up to 5 (v4.3)|
| `Scene` | string | No | Scenes, comma-separated, up to 3 (v4.3)|
| `SkipCopyCheck` | bool | No | Disable lyrics copyright check, default false |
| `CallbackURL` | string | No | Task completion callback URL |

### Lyrics Format Tags
```
[intro]     Intro
[verse]     Verse
[chorus]    Chorus
[inst]      Instrumental break
[bridge]    Bridge
[pre-chorus] Pre-chorus
[outro]     Outro
[hook]      Hook section
[build-up]  Build-up
[drop]      Electronic genre drop
[solo]      Solo
```

---

## Common Enum Values

### Vocal Song Genre (v4.3 Common)

| Value | Description | Value | Description |
|-------|-------------|-------|-------------|
| `Pop` | Pop | `Folk` | Folk |
| `Rock` | Rock | `Electronic` | Electronic |
| `R&B/Soul` | R&B | `Jazz` | Jazz |
| `Hip Hop/Rap` | Hip Hop | `Classical` | Classical |
| `Chinese Style` | Chinese Style | `GuFeng Music` | GuFeng |
| `City Pop` | City Pop | `Country` | Country |
| `EDM` | EDM | `Punk` | Punk |
| `Metal` | Metal | `Reggae` | Reggae |

### Vocal Song Mood (v4.3 Common)

| Value | Description | Value | Description |
|-------|-------------|-------|-------------|
| `Happy` | Happy | `Sorrow/Sad` | Sad |
| `Dynamic/Energetic` | Energetic | `Romantic` | Romantic |
| `Dreamy/Ethereal` | Dreamy | `Chill` | Chill |
| `Inspirational/Hopeful` | Inspirational | `Nostalgic/Memory` | Nostalgic |
| `Calm/Relaxing` | Calm | `Mysterious` | Mysterious |
| `Healing` | Healing | `Lyrical/Ballad` | Lyrical |

### Vocal Song Timbre (v4.3 Common)

| Value | Description | Value | Description |
|-------|-------------|-------|-------------|
| `Warm` | Warm | `Bright` | Bright |
| `Husky` | Husky | `Deep` | Deep |
| `Ethereal` | Ethereal | `Powerful` | Powerful |
| `Magnetic` | Magnetic | `Gentle` | Gentle |
| `Soothing` | Soothing | `Sexy/Lazy` | Lazy |

### Vocal Song Tempo (v4.3)

| Value | Description | Value | Description |
|-------|-------------|-------|-------------|
| `Grave` | Grave (slowest) | `Adagio` | Adagio |
| `Andante` | Andante | `Moderato` | Moderato |
| `Allegro` | Allegro | `Vivace` | Vivace |
| `Presto` | Presto (fastest) | | |

### BGM Mood (v5.0 Common)

| Value | Description | Value | Description |
|-------|-------------|-------|-------------|
| `Dynamic/Energetic` | Energetic | `Calm/Relaxing` | Calm |
| `Happy` | Happy | `Sorrow/Sad` | Sad |
| `Healing` | Healing | `Mysterious` | Mysterious |
| `Romantic` | Romantic | `Dreamy/Ethereal` | Dreamy |
| `Chill` | Chill | `Inspirational/Hopeful` | Inspirational |

### BGM Scene (v5.0 Common)

`Coffee Shop` `Focus` `Relaxation` `Sleep/Bedtime` `Sport` `Travel` `Morning` `Evening` `Meditation` `Study` `Nature` `Rain` `Party` `Game` `Drama` `Advertisement` `Vlog/DailyLife`

### Language (Lang)

| Value | Description |
|-------|-------------|
| `Chinese` | Mandarin (default) |
| `English` | English |
| `Cantonese` | Cantonese |
| `Instrumental/Non-vocal` | Instrumental (no vocals) |

---

## Task Status (QuerySong Response)

| Status | Description |
|--------|-------------|
| `0` | Waiting |
| `1` | Processing |
| `2` | Success (audio link available in SongDetail.AudioUrl) |
| `3` | Failed (failure reason in FailureReason.Msg) |

The audio URL is in the `Result.SongDetail.AudioUrl` field of the response.

---

## Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `50000001` | Copyright check failed | Enrich the text description, add more parameters, or enable `--skip-copy-check` |
| `10000002` | Signature error | Check if AccessKey / SecretKey are correct |
| `10000003` | Request expired | Check if system time is accurate (must be within 15 minutes) |

---

## Notes

- Short 30s simple music is likely to trigger copyright checks (code 50000001); it is recommended to enrich the description or increase the duration
- BGM v4.0 duration limit is 60s, v5.0 limit is 120s
- Vocal songs have a maximum duration of 240s
- Audio download links are time-limited; it is recommended to download promptly after submission
