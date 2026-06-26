---
name: audio-command-executor
description: Processes inbound audio files, transcribes them, and answers to resulting texts. Converts non-WAV inputs to WAV before transcription.
version: 1.0.3
author: Marvin (via skill-creator)
---

Body

Trigger
- Inbound Audiodateien, die im Verzeichnis /home/sirko/.openclaw/media/inbound/ landen (z. B. .ogg, .mp3, etc.)

Input
- Eingabe: Pfad zur Audiodatei (z. B. /home/sirko/.openclaw/media/inbound/aufnahme.ogg)

Workflow
1) Normalize Format
- Wenn Input nicht .wav ist, konvertiere zu WAV:
  /usr/bin/ffmpeg -i {input_file} -ar 16000 -ac 1 -c:a pcm_s16le {input_file}.wav
  Hinweis: Die Zieldatei heißt input_file.wav (Beispiel: /.../aufnahme.ogg → /.../aufnahme.wav)

2) Transkription
- Transkribiere die WAV-Datei:
  /home/sirko/.openclaw/workspace/whisper.cpp/build/bin/whisper-cli -l DE -np -m /home/sirko/.openclaw/workspace/whisper.cpp/models/ggml-small.bin -f {input_wav_file}
- Fange die Transkription als Text ab (stdout)

3) Ausführung
- aus dem transkribierten Text entstandene Fragen oder Anweisungen einfach so in deutsch beantworten, als wäre es ein normaler Text, eingegeben über den Chat

Output
- Einfach den Text verarbeiten, als wäre er als Text-DM eingegangen
- Bei Fehlern: klare Fehlermeldung mit Ursachen (z. B. Datei nicht gefunden, Transkript leer, Ausführung fehlschlägt)

Beispiel-Ablauf
- inbound/file.ogg → convert → /tmp/file.wav → whisper → "Was ist die Hauptstadt von Frankreich" → ermittele Antwort und zeige sie

Notes
- immer auf deutsch antworten

Tests/Testszenarien
- Test mit file.ogg (4 Sekunden) → Transkription prüfen
- Test mit bereits WAV-Datei → direkte Transkription
- Test mit fehlerhafter Datei → ordentliche Fehlermeldung

