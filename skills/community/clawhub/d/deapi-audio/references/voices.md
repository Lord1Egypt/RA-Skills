# Voice Reference

## Kokoro

Voice ID format: `{lang}{gender}_{name}`

**Language prefixes:** `a`=American, `b`=British, `e`=Spanish, `f`=French, `h`=Hindi, `i`=Italian, `p`=Portuguese

**Gender:** `f`=female, `m`=male

| Voice ID | Language | Name | Description |
|----------|----------|------|-------------|
| `af_alloy` | English (US) | Alloy | |
| `af_aoede` | English (US) | Aoede | |
| `af_bella` | English (US) | Bella | Warm, friendly (best quality) |
| `af_heart` | English (US) | Heart | Expressive, emotional |
| `af_jessica` | English (US) | Jessica | |
| `af_kore` | English (US) | Kore | |
| `af_nicole` | English (US) | Nicole | Professional |
| `af_nova` | English (US) | Nova | |
| `af_river` | English (US) | River | |
| `af_sarah` | English (US) | Sarah | Casual |
| `af_sky` | English (US) | Sky | Light, airy |
| `am_adam` | English (US) | Adam | Deep, authoritative |
| `am_echo` | English (US) | Echo | |
| `am_eric` | English (US) | Eric | |
| `am_fenrir` | English (US) | Fenrir | |
| `am_liam` | English (US) | Liam | |
| `am_michael` | English (US) | Michael | Energetic |
| `am_onyx` | English (US) | Onyx | |
| `am_puck` | English (US) | Puck | |
| `am_santa` | English (US) | Santa | |
| `bf_alice` | English (GB) | Alice | |
| `bf_emma` | English (GB) | Emma | Elegant (best British) |
| `bf_isabella` | English (GB) | Isabella | Refined |
| `bf_lily` | English (GB) | Lily | |
| `bm_daniel` | English (GB) | Daniel | |
| `bm_fable` | English (GB) | Fable | |
| `bm_george` | English (GB) | George | Sophisticated |
| `bm_lewis` | English (GB) | Lewis | Warm British male |
| `ef_dora` | Spanish | Dora | |
| `em_alex` | Spanish | Alex | |
| `em_santa` | Spanish | Santa | |
| `ff_siwis` | French | Siwis | Best quality |
| `hf_alpha` | Hindi | Alpha | |
| `hf_beta` | Hindi | Beta | |
| `hm_omega` | Hindi | Omega | |
| `hm_psi` | Hindi | Psi | |
| `if_sara` | Italian | Sara | |
| `im_nicola` | Italian | Nicola | |
| `pf_dora` | Portuguese (BR) | Dora | |
| `pm_alex` | Portuguese (BR) | Alex | |
| `pm_santa` | Portuguese (BR) | Santa | |

### Language codes for --lang (Kokoro)

| Code | Language |
|------|----------|
| `en-us` | American English |
| `en-gb` | British English |
| `es` | Spanish |
| `fr-fr` | French |
| `hi` | Hindi |
| `it` | Italian |
| `pt-br` | Brazilian Portuguese |

## Chatterbox

Voice is always `default`. Speed is fixed at `1`.

### Language codes for --lang (Chatterbox)

| Code | Language |
|------|----------|
| `ar` | Arabic |
| `da` | Danish |
| `de` | German |
| `en` | English |
| `es` | Spanish |
| `fi` | Finnish |
| `fr` | French |
| `he` | Hebrew |
| `hi` | Hindi |
| `it` | Italian |
| `ja` | Japanese |
| `ko` | Korean |
| `ms` | Malay |
| `nl` | Dutch |
| `no` | Norwegian |
| `pl` | Polish |
| `pt` | Portuguese |
| `ru` | Russian |
| `sv` | Swedish |
| `sw` | Swahili |
| `tr` | Turkish |
| `zh` | Chinese |

## Qwen3

Three Qwen3 models share the same 10 languages. Speed is fixed at `1`.

- **Qwen3_TTS_12Hz_1_7B_CustomVoice** — custom voice TTS (`--model Qwen3` in text-to-speech.sh)
- **Qwen3_TTS_12Hz_1_7B_Base** — voice cloning (voice-clone.sh)
- **Qwen3_TTS_12Hz_1_7B_VoiceDesign** — voice design (voice-design.sh)

### Voices (CustomVoice model)

Default voice: `Vivian`. Voice Clone and Voice Design use `default` only.

| Voice | Gender |
|-------|--------|
| `Vivian` | Male |
| `Serena` | Female |
| `Uncle_Fu` | Male |
| `Dylan` | Male |
| `Eric` | Male |
| `Ryan` | Male |
| `Aiden` | Male |
| `Ono_Anna` | Female |
| `Sohee` | Female |

> **Note:** Chinese language does not have `Ryan` voice.

### Languages for --lang (Qwen3)

Qwen3 models use full language names (not codes):

| Language |
|----------|
| `English` |
| `Italian` |
| `Spanish` |
| `Portuguese` |
| `Russian` |
| `French` |
| `German` |
| `Korean` |
| `Japanese` |
| `Chinese` |
