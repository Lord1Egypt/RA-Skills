---
name: audio-transcription
description: Transcreve arquivos de áudio para texto usando Whisper local ou API. Use quando o usuário solicitar transcrição de áudios, mensagens de voz, ou converter fala em texto. Suporta formatos OGG, MP3, WAV, M4A e outros via conversão automática.
---

# Audio Transcription

Transcreve arquivos de áudio para texto.

## Recursos

- Transcrição de áudios em português e outros idiomas
- Suporte a múltiplos formatos (OGG, MP3, WAV, M4A, etc.)
- Conversão automática de formatos se necessário
- Detecção automática de idioma

## Como Usar

### Pré-requisitos

A skill tenta usar as seguintes ferramentas na ordem:
1. `whisper` (OpenAI Whisper via pip)
2. `whisper.cpp` se instalado em `~/whisper.cpp`
3. API OpenAI (requer OPENAI_API_KEY)

### Script de Transcrição

Use o script `scripts/transcribe.sh`:

```bash
scripts/transcribe.sh <arquivo_audio> [idioma]
```

Exemplo:
```bash
scripts/transcribe.sh /path/to/audio.ogg pt
```

### Parâmetros

- `arquivo_audio`: Caminho para o arquivo de áudio
- `idioma` (opcional): Código do idioma (pt, en, es, etc.). Padrão: auto-detect

## Instalação de Dependências

Se nenhuma ferramenta estiver disponível, a skill pode instalar whisper:

```bash
pip install openai-whisper
```

Para whisper.cpp local:
```bash
git clone https://github.com/ggerganov/whisper.cpp.git ~/whisper.cpp
cd ~/whisper.cpp
make
```

## NOTAS

- O formato OGG (Opus) do Telegram requer ffmpeg para conversão
- A transcrição pode levar alguns segundos dependendo do tamanho do áudio
- Qualidade da transcrição depende do modelo Whisper usado
