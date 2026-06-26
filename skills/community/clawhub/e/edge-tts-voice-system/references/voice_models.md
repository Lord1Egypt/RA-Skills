# Voice Models Reference

## Default Voice: Edge TTS (en-IE-ConnorNeural)

### Specifications
- **Name**: en-IE-ConnorNeural
- **Provider**: Edge TTS
- **Quality**: High
- **Storage**: Cached audio only
- **Language**: English (Ireland)
- **Characteristics**: Clear articulation, natural pacing

### About the Edge TTS voice
The outbound voice pipeline uses Edge TTS with a configurable voice. The default is `en-IE-ConnorNeural` and audio is cached locally.

### Performance
- **Load time**: ~2 seconds (one-time)
- **Generation time**: ~0.3-0.5 seconds per sentence
- **Memory usage**: ~500MB during generation

## Alternative Edge TTS Voices

### Available Quality Levels
- **Low**: ~10-30MB, basic quality
- **Medium**: ~50-80MB, good quality (recommended for balance)
- **High**: ~100-200MB, excellent quality (default)

### Popular English Voices

#### US English (en_US)
- **ryan** (male, high) - Rich, natural American male
- **amy** (female, medium) - Clear American female
- **jenny** (female, medium/high) - High-quality female
- **danny** (male, low) - Basic American male
- **lessac** (versatile, low/medium/high) - Expressive, clear articulation

#### UK English (en_GB)
- **alan** (male, medium) - Neutral British male
- **southern_english_female** (female, low) - Southern British accent
- **northern_english_male** (male, medium) - Northern British accent
- **cori** (female, medium/high) - High-quality British female

### How to Change Voices

1. Set `OPENCLAW_EDGE_TTS_VOICE` to a supported Edge voice
2. Re-run the installer to refresh cached audio and wrappers


## Speech Recognition Models

### faster-whisper Models

#### Model Sizes
- **tiny** (75MB) - Fastest, lower accuracy
- **base** (142MB) - Default, good balance
- **small** (466MB) - Higher accuracy, slower
- **medium** (1.5GB) - Best accuracy, requires more memory

#### Performance Comparison
| Model | Speed | Accuracy | Memory | Use Case |
|-------|-------|----------|--------|----------|
| tiny | ⚡⚡⚡⚡ | 85-90% | Low | Quick responses, limited resources |
| base | ⚡⚡⚡ | 90-95% | Medium | Default, good balance |
| small | ⚡⚡ | 95-97% | High | High accuracy needed |
| medium | ⚡ | 97-99% | Very High | Best possible accuracy |

#### How to Change STT Model
Edit `voice_handler.py`:
```python
# Change this line:
self.stt_model = "base"  # Change to "tiny", "small", or "medium"
```

## Audio Processing

### Supported Formats
- **Input**: OGG/Opus, WAV, MP3, M4A, FLAC
- **Output**: WAV (16-bit PCM)
- **Conversion**: Automatic via ffmpeg

### Optimal Settings for STT
- **Sample rate**: 16000Hz
- **Channels**: Mono (1)
- **Bit depth**: 16-bit
- **Format**: WAV or OGG/Opus

### File Size Estimates
- 1 minute of speech: ~1.5MB (OGG/Opus) or ~2.5MB (WAV)
- 5 minute conversation: ~7.5MB (OGG) or ~12.5MB (WAV)

## Memory Requirements

### Minimum System Requirements
- **RAM**: 2GB (for base models)
- **Storage**: 500MB (for models and dependencies)
- **CPU**: Modern x86-64 or ARM

### Recommended for Best Performance
- **RAM**: 4GB+ (for high-quality models)
- **Storage**: 1GB+
- **CPU**: 2+ cores

### Memory Usage Breakdown
- Edge TTS: no local model download required
- faster-whisper model: 142MB (base, loaded into memory)
- Python runtime: 100-200MB
- Audio buffers: 10-50MB
- **Total**: ~400-500MB during operation

## Troubleshooting Model Issues

### Common Problems

1. **Out of memory errors**
   - Use smaller models (tiny/base instead of small/medium)
   - Use medium quality TTS instead of high
   - Close other applications

2. **Slow performance**
   - Ensure using CPU with AVX2 support
   - Use `compute_type="int8"` for faster-whisper
   - Consider tiny model for faster responses

3. **Poor transcription accuracy**
   - Ensure clean audio input (minimize background noise)
   - Use 16000Hz sample rate
   - Try small or medium model for better accuracy

4. **TTS sounds robotic**
   - Ensure using high or medium quality model
   - Check audio output device/sample rate
   - Try different voice model

### Model Sources
- **Edge TTS**: local `edge-tts` package
- **faster-whisper**: Automatically downloads from HuggingFace

### Updates
Models are periodically updated. Check original repositories for:
- New voice models
- Improved accuracy
- Better performance
- Additional languages