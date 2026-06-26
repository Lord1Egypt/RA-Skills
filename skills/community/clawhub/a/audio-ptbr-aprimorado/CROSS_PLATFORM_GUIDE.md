# 🔄 Cross-Platform Compatibility Guide

**Esta skill agora funciona em AMBOS os ambientes:**

## 🎯 Ambientes Suportados

### 1️⃣ OpenClaw (Original)
- ✅ Integração completa com OpenClaw agent
- ✅ Envio automático de mensagens via Telegram
- ✅ Comandos de voz `/voz`
- ✅ Resposta com Claude OU OpenClaw agent
- **Workspace:** `~/.openclaw/workspace`

### 2️⃣ Claude Desktop (Novo!)
- ✅ Funciona como app standalone
- ✅ Resposta com Claude API
- ✅ Sem dependência de OpenClaw
- ✅ Interface Claude normal
- ❌ Não envia automático (Claude não tem acesso ao Telegram)
- **Workspace:** `~/.claude-audio-pt`

### 3️⃣ Claude API (Novo!)
- ✅ Pode ser integrado em qualquer aplicação
- ✅ Processa áudio/texto via API
- ✅ Retorna respostas em JSON
- ❌ Sem persistência
- **Workspace:** `/tmp` (temporário)

### 4️⃣ Standalone (Novo!)
- ✅ Funciona sem OpenClaw ou Claude Desktop
- ✅ CLI simples para usar
- ✅ Configuração local
- **Workspace:** `~/.audio-pt-autoreply`

## 🔍 Detecção Automática

O arquivo `environment.py` detecta automaticamente:

```
┌─────────────────────────────────┐
│   Executar Script               │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   environment.py detecta:        │
│   1. OpenClaw?                  │
│   2. Claude Desktop?            │
│   3. Claude API?                │
│   4. Standalone?                │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Configura automaticamente:    │
│   - Workspace                   │
│   - Piper directory             │
│   - Config file location        │
│   - Recursos disponíveis        │
└─────────────────────────────────┘
```

## 📊 Recurso Comparison

| Recurso | OpenClaw | Claude Desktop | Claude API | Standalone |
|---------|----------|----------------|------------|-----------|
| **Transcrição** | ✅ | ✅ | ✅ | ✅ |
| **Síntese** | ✅ | ✅ | ✅ | ✅ |
| **Claude respostas** | ✅ | ✅ | ✅ | ✅ |
| **OpenClaw agent** | ✅ | ❌ | ❌ | ❌ |
| **Telegram** | ✅ | ❌ | ❌ | ❌ |
| **Persistência** | ✅ | ✅ | ❌ | ✅ |
| **Configuração vozes** | ✅ | ✅ | ❌ | ✅ |

## 🚀 Como Usar em Cada Ambiente

### OpenClaw (Original - Sem Mudança)
```bash
# Instalação
cd ~/.openclaw/skills/audio-ptbr-autoreply
bash install.sh

# Uso
openclaw gateway restart
/voz jeff  # Comando no chat
# Enviar áudio → Resposta automática de áudio
```

### Claude Desktop (Novo!)
```bash
# 1. Copiar para um local acessível
mkdir -p ~/.claude-audio-pt
cp -r audio-ptbr-autoreply/* ~/.claude-audio-pt/

# 2. Instalar dependências
cd ~/.claude-audio-pt
bash install.sh

# 3. No Claude Desktop, adicionar como ferramenta
# (Se suportar custom tools via MCP)

# 4. Ou usar como script Python
python3 health_check.py  # Validar instalação
python3 scripts/transcribe_universal.py audio.wav
python3 scripts/synthesize_universal.py "Olá"
```

### Como Library Python (Novo!)
```python
from synthesize_universal import synthesize_to_file, synthesize_to_bytes
from transcribe_universal import transcribe_file

# Transcrever áudio
text = transcribe_file("audio.wav")
print(f"Transcribed: {text}")

# Sintetizar fala
audio_path = synthesize_to_file("Olá, como vai?", voice="miro")
print(f"Audio saved to: {audio_path}")

# Ou obter bytes diretamente
audio_bytes = synthesize_to_bytes("Hello", voice="jeff")
# Usar audio_bytes em qualquer lugar
```

### Standalone CLI (Novo!)
```bash
# Transcrever
python3 scripts/transcribe_universal.py audio.wav

# Sintetizar
python3 scripts/synthesize_universal.py "Texto para ler"

# Processar com Claude
ANTHROPIC_API_KEY="sk-..." python3 scripts/claude_adapter.py "pergunta"

# Validar instalação
python3 health_check.py
```

## 🔧 Scripts Universais

### `transcribe_universal.py`
```python
# CLI Usage
python3 transcribe_universal.py audio.wav

# Python Import
from transcribe_universal import transcribe_file, transcribe_file_json

text = transcribe_file("audio.wav")
result_dict = transcribe_file_json("audio.wav")
```

### `synthesize_universal.py`
```python
# CLI Usage
python3 synthesize_universal.py "Texto" [voice]

# Python Import
from synthesize_universal import synthesize_to_file, synthesize_to_bytes

# Salvar em arquivo
path = synthesize_to_file("Olá", voice="jeff")

# Obter bytes
audio_bytes = synthesize_to_bytes("Hello")
```

### `environment.py`
```python
from environment import get_environment, get_config

env = get_environment()  # Returns: Environment.OPENCLAW, etc.

config = get_config()
print(config["name"])              # "OpenClaw", "Claude Desktop", etc.
print(config["piper_dir"])         # Workspace-specific path
print(config["supports_claude"])   # True/False
```

## 📦 Estrutura de Arquivos Universal

```
audio-ptbr-autoreply/
├── install.sh                    # Auto-installer (funciona em todos)
├── health_check.py               # Validador (funciona em todos)
├── environment.py                # ⭐ Detector automático
├── requirements.txt              # Dependências (iguais para todos)
│
├── scripts/
│   ├── transcribe_universal.py   # ⭐ Funciona em OpenClaw + Claude
│   ├── synthesize_universal.py   # ⭐ Funciona em OpenClaw + Claude
│   ├── voice_config.py           # Funciona em OpenClaw + Standalone
│   ├── claude_adapter.py         # Inteligência AI (todos)
│   │
│   ├── transcribe.py             # [DEPRECATED] OpenClaw only
│   ├── synthesize.py             # [DEPRECATED] OpenClaw only
│   ├── process.sh                # [DEPRECATED] OpenClaw only
│   └── ...
│
├── README.md                     # Documentação universal
└── QUICKSTART.md                 # Quick start (todos ambientes)
```

## 🔀 Migração de Ambientes

### De OpenClaw → Claude Desktop

```bash
# 1. Backup da configuração
cp ~/.openclaw/workspace/.audio_pt_voice_config ~/voice_backup.json

# 2. Copiar skill
mkdir -p ~/.claude-audio-pt
cp -r ~/.openclaw/skills/audio-ptbr-autoreply/* ~/.claude-audio-pt/

# 3. Instalar novamente
cd ~/.claude-audio-pt
bash install.sh

# 4. Restaurar preferência de voz (opcional)
# Editar ~/.claude-audio-pt/config.json com os dados do backup
```

### De Claude Desktop → OpenClaw

```bash
# 1. Copiar para OpenClaw
cp -r ~/.claude-audio-pt ~/.openclaw/skills/audio-ptbr-autoreply

# 2. Reiniciar OpenClaw
openclaw gateway restart
```

## 🎓 Exemplos de Uso

### Exemplo 1: Em Claude Desktop
```python
# transcribe_audio.py (pode ser usado no Claude Desktop)
import json
from transcribe_universal import transcribe_file

audio_file = "recording.wav"
text = transcribe_file(audio_file)

# Claude entende esse output
print(json.dumps({
    "transcribed": text,
    "language": "pt-BR"
}))
```

### Exemplo 2: Como API
```python
# api.py - Expor como REST API
from flask import Flask, request
from synthesize_universal import synthesize_to_bytes
from transcribe_universal import transcribe_file

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    audio = request.files['audio']
    audio.save('temp.wav')
    text = transcribe_file('temp.wav')
    return {'text': text}

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    audio = synthesize_to_bytes(data['text'], data.get('voice', 'jeff'))
    return audio, 200, {'Content-Type': 'audio/ogg'}

if __name__ == '__main__':
    app.run()
```

### Exemplo 3: Em OpenClaw (Sem Mudança)
```bash
# Funciona exatamente igual a antes
bash install.sh
openclaw gateway restart
/voz jeff
# Enviar áudio...
```

## ✅ Checklist de Compatibilidade

- [x] Detecção automática de ambiente
- [x] Scripts universais (transcribe, synthesize)
- [x] Suporte a Claude API
- [x] Suporte a Claude Desktop
- [x] Suporte a OpenClaw (original)
- [x] Standalone mode
- [x] Health check em todos os ambientes
- [x] Documentação unificada
- [x] Fallbacks automáticos
- [x] Workspace automático por ambiente

## 🚨 Troubleshooting Cross-Platform

### Script não detecta ambiente corretamente
```bash
# Debug
python3 environment.py

# Force um ambiente específico (para testes)
export OPENCLAW_HOME="/path/to/openclaw"  # Force OpenClaw
export ANTHROPIC_API_KEY="sk-..."         # Force Claude API
```

### Paths incorretos
```bash
# Verificar
python3 health_check.py

# Editar environment.py se necessário
# Seção get_config() tem hardcoded paths
```

### Dependências missing em novo ambiente
```bash
# Reinstalar
bash install.sh

# Ou manual
pip install -r requirements.txt
```

## 📝 Próximos Passos

1. ✅ Usar `environment.py` em todos os scripts
2. ✅ Testar em cada ambiente
3. ✅ Documentar casos de uso específicos
4. ✅ Criar exemplos de integração

---

**A skill agora é verdadeiramente multi-plataforma!** 🎉

Use em OpenClaw, Claude Desktop, Claude API, ou standalone - funciona em tudo!
